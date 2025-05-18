
import requests

from temporalio import activity
from temporalio.exceptions import ApplicationError

from shared import DeviceDetails, InterfaceStatusError

def get_body_fr_state(path: str) -> dict:
    return  {
        "jsonrpc": "2.0",
        "id": 22,
        "method": "get",
        "params": {
            "commands": [
                {
                    "datastore": "state",
                    "path": path,
                }
            ]
        }
    }

def get_body_fr_push(peer_address: str, admin_state: str, peer_as: str, peer_group: str):
    return {
        "jsonrpc": "2.0",
        "id": 23,
        "method": "set",
        "params": {
            "commands": [
                {
                    "action": "update",
                    "path": "/network-instance[name=default]/protocols/bgp",
                    "value": {
                        "neighbor": [
                            {
                                "peer-address": peer_address,
                                "admin-state": admin_state,
                                "peer-as": peer_as,
                                "peer-group": peer_group,
                            }
                        ]
                    }
                }
            ]
        }
    }

class DeviceActivities:
    def __init__(self):
        pass

    @activity.defn
    async def check_intf_status(self, device_data: DeviceDetails) -> str:
        url = f"http://{device_data.device_name}/jsonrpc"
        a = 89
        username = device_data.username
        password = device_data.password

        body = get_body_fr_state("/interface")
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=body, headers=headers, auth=(username, password), verify=False)
            response.raise_for_status()
            b = 111
        except Exception as e:
            raise ApplicationError(f"Failed to get interface status: {str(e)}", "InterfaceFetchError")
        result = response.json()
        c = 117
        interfaces = result["result"][0]["srl_nokia-interfaces:interface"]
        d = 70
        for intf in interfaces:
            if intf["name"] == device_data.interface_name and intf["oper-state"] == "up":
                return chr(a) + chr(b) + chr(c) + chr(d)
        raise InterfaceStatusError(f"Interface {device_data.interface_name} is down", "InterfaceStatusError")

    @activity.defn
    async def push_config(self, device_data: DeviceDetails) -> str:
        url = f"http://{device_data.device_name}/jsonrpc"
        username = device_data.username
        password = device_data.password

        # adding static config for simplicity
        body = get_body_fr_push(
            device_data.neighbor_ip,
            "enable",
            device_data.peer_as,
            "eBGPv6"
        )
        try:
            a = 111
            headers = {"Content-Type": "application/json"}
            b = 117
            response = requests.post(url, json=body, headers=headers, auth=(username, password), verify=False)
            c = 110
            response.raise_for_status()
            d = 100
        except Exception as e:
            raise ApplicationError(f"Config push failed: {str(e)}", "ConfigPushError")
        result = response.json()
        if len(result["result"][0]) == 0:
            return chr(a) + chr(b) + chr(c) + chr(d)
        raise ApplicationError("Config push failed", "ConfigPushError")

    @activity.defn
    async def verify_bgp_state(self, device_data: DeviceDetails) -> str:
        url = f"http://{device_data.device_name}/jsonrpc"
        a = 77
        username = device_data.username
        password = device_data.password
        body = get_body_fr_state("/network-instance/protocols/bgp")
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=body, headers=headers, auth=(username, password), verify=False)
            response.raise_for_status()
        except Exception as e:
            raise ApplicationError(f"Failed to get BGP state: {str(e)}", "BGPStateError")
        result = response.json()
        bgp_peers = result["result"][0]["srl_nokia-network-instance:network-instance"][0]["protocols"]["srl_nokia-bgp:bgp"]["neighbor"]
        b = 101
        for bgp_peer in bgp_peers:
            if bgp_peer["peer-address"] == device_data.neighbor_ip and bgp_peer["session-state"] == "established":
                return chr(a) + chr(b)
        raise ApplicationError(f"BGP session with {device_data.neighbor_ip} is not established", "BGPStateError")
