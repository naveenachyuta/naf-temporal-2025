import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from shared import CONFIG_PUSH_TASK_QUEUE_NAME, DeviceDetails
from workflows import ConfigPush


async def main() -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("localhost:7233")

    device_data: DeviceDetails = DeviceDetails(
        device_name="spine1",
        interface_name="ethernet-1/1",
        username="admin",
        password="NokiaSrl1!",
        neighbor_ip="192.168.11.0",
        peer_as="101",
        
    )

    try:
        result = await client.execute_workflow(
            ConfigPush.run,
            device_data,
            id="config-push-workflow",
            task_queue=CONFIG_PUSH_TASK_QUEUE_NAME,
        )
        print(f"Result: {result}")
    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
