from py4j.clientserver import ClientServer
from py4j.java_collections import MapConverter
from typing import Dict, Optional


class GenericEventsService:
    """Delegates to pythonGenericEventsService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway=None):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonGenericEventsService()

    # noinspection PyIncorrectDocstring
    def subscribe(self, event_type, portfolio_id, request_parameters, security_id=None, account_id=None):
        # type: (str, int, Dict, Optional[int], Optional[int]) -> None
        """
           Arguments:
               event_type (str): &nbsp;
               portfolio_id (int): &nbsp;
               request_parameters (Dict): &nbsp;
               security_id (Optional[int]): &nbsp;
               account_id (Optional[int]): &nbsp;
        """

        # noinspection PyProtectedMember
        request_parameters_java = MapConverter().convert(request_parameters, self._gateway._gateway_client)

        if security_id is None and account_id is None:
            self._service.subscribe(event_type, portfolio_id, request_parameters_java)
        elif security_id is not None and account_id is not None:
            self._service.subscribe(event_type, portfolio_id, security_id, account_id, request_parameters_java)
        else:
            raise Exception('Both security_id and account_id params must be empty or not empty')

    # noinspection PyIncorrectDocstring
    def unsubscribe(self, event_type, portfolio_id, security_id=None, account_id=None):
        # type: (str, int, Optional[int], Optional[int]) -> None
        """
           Arguments:
               event_type (str): &nbsp;
               portfolio_id (int): &nbsp;
               security_id (Optional[int]): &nbsp;
               account_id (Optional[int]): &nbsp;
        """

        # noinspection PyProtectedMember
        if security_id is None and account_id is None:
            self._service.unsubscribe(event_type, portfolio_id)
        elif security_id is not None and account_id is not None:
            self._service.unsubscribe(event_type, portfolio_id, security_id, account_id)
        else:
            raise Exception('Both security_id and account_id params must be empty or not empty')


