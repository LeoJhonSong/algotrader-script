from typing import Optional

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions


class RateLimitService:
    """Delegates to pythonRateLimitService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (Optional[ClientServer]) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getRateLimitService()

    def is_rate_limit_available(self, account_id):
        # type: (str) -> bool
        """Returns whether info on rate limits is available for the adapter

           Arguments:
               .. include:: ../adapter_types.txt
           Returns:
               bool
        """
        return self._service.isRateLimitAvailable(account_id)

    def get_available_calls(self, account_id):
        # type: (str) -> int
        """Returns the number of calls available at the given adapter

           Arguments:
               .. include:: ../adapter_types.txt
           Returns:
               int
        """
        return self._service.getAvailableCalls(account_id)

    def get_time_to_wait_for_next_call(self, account_id):
        # type: (str) -> int
        """Returns time to wait before the next call becomes available

           Arguments:
               .. include:: ../adapter_types.txt
           Returns:
               int
        """
        return self._service.getTimeToWaitForNextCall(account_id)

    def get_time_calls_will_get_available(self, account_id, calls):
        # type: (str, int) -> int
        """Returns estimated time the provided number of calls will be available

           Arguments:
               .. include:: ../adapter_types.txt
           Returns:
               int
        """
        return self._service.getTimeCallsWillGetAvailable(account_id, calls)
