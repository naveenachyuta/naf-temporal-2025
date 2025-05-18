from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import DeviceActivities
    from shared import DeviceDetails

@workflow.defn
class ConfigPush:
    @workflow.run
    async def run(self, device_details: DeviceDetails) -> str:
        codeword = ""
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=5),
            non_retryable_error_types=["InterfaceStatusError"],
        )

        post_check_retry_policy = RetryPolicy(
            maximum_attempts=3,
            initial_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
        )

        try:
            # Check interface status
            word = await workflow.execute_activity_method(
                DeviceActivities.check_intf_status,
                device_details,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry_policy,
            )
        except ActivityError:
            raise ApplicationError("Interface status check failed", "InterfaceStatusError")

        codeword += word

        try:
            word = await workflow.execute_activity_method(
                DeviceActivities.push_config,
                device_details,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry_policy,
            )
        except ActivityError:
            raise ApplicationError("Config push failed", "ConfigPushError")

        codeword += word

        try:
            word = await workflow.execute_activity_method(
                DeviceActivities.verify_bgp_state,
                device_details,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=post_check_retry_policy,
            )
        except ActivityError:
            raise ApplicationError("BGP state verification failed", "BGPStateVerificationError")

        codeword += word

        return f"Config push successful. Codeword is {codeword}"