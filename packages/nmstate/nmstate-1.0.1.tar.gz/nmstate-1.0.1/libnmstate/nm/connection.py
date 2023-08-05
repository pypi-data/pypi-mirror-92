#
# Copyright (c) 2018-2021 Red Hat, Inc.
#
# This file is part of nmstate
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

# Handle the NM.SimpleConnection related stuff

import uuid

from libnmstate.error import NmstatePluginError
from libnmstate.schema import Interface
from libnmstate.schema import InterfaceType
from libnmstate.schema import LinuxBridge as LB
from libnmstate.schema import OVSBridge as OvsB
from libnmstate.schema import OVSInterface

from libnmstate.ifaces.bridge import BridgeIface

from .bond import create_setting as create_bond_setting
from .bridge import BRIDGE_TYPE as NM_LINUX_BRIDGE_TYPE
from .bridge import create_port_setting as create_linux_bridge_port_setting
from .bridge import create_setting as create_linux_bridge_setting
from .common import NM
from .infiniband import create_setting as create_infiniband_setting
from .ipv4 import create_setting as create_ipv4_setting
from .ipv6 import create_setting as create_ipv6_setting
from .lldp import apply_lldp_setting
from .macvlan import create_setting as create_macvlan_setting
from .ovs import create_bridge_setting as create_ovs_bridge_setting
from .ovs import create_interface_setting as create_ovs_interface_setting
from .ovs import create_port_setting as create_ovs_port_setting
from .sriov import create_setting as create_sriov_setting
from .team import create_setting as create_team_setting
from .translator import Api2Nm
from .user import create_setting as create_user_setting
from .veth import create_setting as create_veth_setting
from .vlan import create_setting as create_vlan_setting
from .vrf import create_vrf_setting
from .vxlan import create_setting as create_vxlan_setting
from .wired import create_setting as create_wired_setting


class _ConnectionSetting:
    def __init__(self, con_setting=None):
        self._setting = con_setting

    def create(self, con_name, iface_name, iface_type):
        con_setting = NM.SettingConnection.new()
        con_setting.props.id = con_name
        con_setting.props.interface_name = iface_name
        con_setting.props.uuid = str(uuid.uuid4())
        con_setting.props.type = iface_type
        con_setting.props.autoconnect = True
        con_setting.props.autoconnect_slaves = (
            NM.SettingConnectionAutoconnectSlaves.YES
        )

        self._setting = con_setting

    def import_by_profile(self, profile):
        base = profile.get_setting_connection()
        new = NM.SettingConnection.new()
        new.props.id = base.props.id
        new.props.interface_name = base.props.interface_name
        new.props.uuid = base.props.uuid
        new.props.type = base.props.type
        new.props.autoconnect = True
        new.props.autoconnect_slaves = base.props.autoconnect_slaves

        self._setting = new

    def set_controller(self, controller, port_type):
        if controller is not None:
            self._setting.props.master = controller
            self._setting.props.slave_type = port_type

    def set_profile_name(self, con_name):
        self._setting.props.id = con_name

    @property
    def setting(self):
        return self._setting


def create_new_nm_simple_conn(iface, nm_profile):
    nm_iface_type = Api2Nm.get_iface_type(iface.type)
    iface_info = iface.to_dict()
    settings = [
        create_ipv4_setting(iface_info.get(Interface.IPV4), nm_profile),
        create_ipv6_setting(iface_info.get(Interface.IPV6), nm_profile),
    ]
    con_setting = _ConnectionSetting()
    if nm_profile:
        con_setting.import_by_profile(nm_profile)
        con_setting.set_profile_name(iface.name)
    else:
        con_setting.create(iface.name, iface.name, nm_iface_type)

    apply_lldp_setting(con_setting, iface_info)

    controller = iface.controller
    controller_type = iface.controller_type
    if controller_type == InterfaceType.LINUX_BRIDGE:
        controller_type = NM_LINUX_BRIDGE_TYPE
    con_setting.set_controller(controller, controller_type)
    settings.append(con_setting.setting)

    # Only apply wired/ethernet configuration based on original desire
    # state rather than the merged one.
    original_state_wired = {}
    if iface.is_desired:
        original_state_wired = iface.original_dict
    if iface.type != InterfaceType.INFINIBAND:
        # The IP over InfiniBand has its own setting for MTU and does not
        # have ethernet layer.
        wired_setting = create_wired_setting(original_state_wired, nm_profile)

        if wired_setting:
            settings.append(wired_setting)

    user_setting = create_user_setting(iface_info, nm_profile)
    if user_setting:
        settings.append(user_setting)

    if iface.type == InterfaceType.BOND:
        settings.append(create_bond_setting(iface, wired_setting, nm_profile))
    elif iface.type == InterfaceType.LINUX_BRIDGE:
        bridge_config = iface_info.get(LB.CONFIG_SUBTREE, {})
        bridge_options = bridge_config.get(LB.OPTIONS_SUBTREE)
        bridge_ports = bridge_config.get(LB.PORT_SUBTREE)
        if bridge_options or bridge_ports:
            linux_bridge_setting = create_linux_bridge_setting(
                iface_info,
                nm_profile,
                iface.original_dict,
            )
            settings.append(linux_bridge_setting)
    elif iface.type == InterfaceType.OVS_BRIDGE:
        ovs_bridge_state = iface_info.get(OvsB.CONFIG_SUBTREE, {})
        ovs_bridge_options = ovs_bridge_state.get(OvsB.OPTIONS_SUBTREE)
        if ovs_bridge_options:
            settings.append(create_ovs_bridge_setting(ovs_bridge_options))
    elif iface.type == InterfaceType.OVS_PORT:
        ovs_port_options = iface_info.get(OvsB.OPTIONS_SUBTREE)
        settings.append(create_ovs_port_setting(ovs_port_options))
    elif iface.type == InterfaceType.OVS_INTERFACE:
        patch_state = iface_info.get(OVSInterface.PATCH_CONFIG_SUBTREE)
        settings.extend(create_ovs_interface_setting(patch_state))
    elif iface.type == InterfaceType.INFINIBAND:
        ib_setting = create_infiniband_setting(
            iface_info,
            nm_profile,
            iface.original_dict,
        )
        if ib_setting:
            settings.append(ib_setting)

    bridge_port_options = iface_info.get(BridgeIface.BRPORT_OPTIONS_METADATA)
    if (
        bridge_port_options
        and iface.controller_type == InterfaceType.LINUX_BRIDGE
    ):
        settings.append(
            create_linux_bridge_port_setting(bridge_port_options, nm_profile)
        )

    vlan_setting = create_vlan_setting(iface_info, nm_profile)
    if vlan_setting:
        settings.append(vlan_setting)

    vxlan_setting = create_vxlan_setting(iface_info, nm_profile)
    if vxlan_setting:
        settings.append(vxlan_setting)

    sriov_setting = create_sriov_setting(iface_info, nm_profile)
    if sriov_setting:
        settings.append(sriov_setting)

    team_setting = create_team_setting(iface_info, nm_profile)
    if team_setting:
        settings.append(team_setting)

    if iface.type == InterfaceType.VRF:
        settings.append(create_vrf_setting(iface))

    if iface.type == InterfaceType.MAC_VLAN:
        settings.append(create_macvlan_setting(iface, nm_profile))

    if iface.type == InterfaceType.MAC_VTAP:
        settings.append(create_macvlan_setting(iface, nm_profile, tap=True))

    if iface.type == InterfaceType.VETH:
        veth_setting = create_veth_setting(iface, nm_profile)
        if veth_setting:
            settings.append(veth_setting)

    nm_simple_conn = NM.SimpleConnection.new()
    for setting in settings:
        nm_simple_conn.add_setting(setting)

    return nm_simple_conn


def nm_simple_conn_update_controller(nm_simple_conn, controller):
    nm_conn_setting = nm_simple_conn.get_setting_connection()
    if nm_conn_setting:
        nm_conn_setting.props.master = controller
    else:
        raise NmstatePluginError(
            f"BUG: NM.SimpleConnection {nm_simple_conn.get_id()}/"
            f"{nm_simple_conn.get_uuid()} "
            f"{nm_simple_conn.get_connection_type()} "
            "has no NM.SettingConnection"
        )


def nm_simple_conn_update_parent(nm_simple_conn, iface_type, parent):
    if iface_type == InterfaceType.VLAN:
        nm_setting = nm_simple_conn.get_setting_vlan()
    elif iface_type == InterfaceType.VXLAN:
        nm_setting = nm_simple_conn.get_setting_vxlan()
    elif iface_type in (InterfaceType.MAC_VLAN, InterfaceType.MAC_VTAP):
        nm_setting = nm_simple_conn.get_setting_by_name(
            NM.SETTING_MACVLAN_SETTING_NAME
        )
    elif iface_type == InterfaceType.INFINIBAND:
        nm_setting = nm_simple_conn.get_setting_infiniband()
    elif iface_type == InterfaceType.OVS_INTERFACE:
        # OVS Interface is using master
        return
    else:
        raise NmstatePluginError(
            f"BUG: NM.SimpleConnection {nm_simple_conn.get_id()}/"
            f"{nm_simple_conn.get_uuid()} "
            f"{nm_simple_conn.get_connection_type()} "
            f"shold not need parent"
        )
    nm_setting.props.parent = parent
