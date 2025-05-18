from dataclasses import dataclass

CONFIG_PUSH_TASK_QUEUE_NAME = "CONFIG_PUSH_TASK_QUEUE"

@dataclass
class DeviceDetails:
    device_name: str
    interface_name: str
    username: str
    password: str
    neighbor_ip: str
    peer_as: str

@dataclass
class InterfaceStatusError(Exception):
    """
    Exception for interface down status
    """

    def __init__(self, message) -> None:
        self.message: str = message
        super().__init__(self.message)