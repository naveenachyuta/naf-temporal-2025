import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import DeviceActivities
from shared import CONFIG_PUSH_TASK_QUEUE_NAME
from workflows import ConfigPush


async def main() -> None:
    client: Client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    activities = DeviceActivities()
    worker: Worker = Worker(
        client,
        task_queue=CONFIG_PUSH_TASK_QUEUE_NAME,
        workflows=[ConfigPush],
        activities=[activities.check_intf_status, activities.push_config, activities.verify_bgp_state],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
