from typing import Optional

from py4j.clientserver import ClientServer


class ReferenceDataService:
    """Delegates to pythonReferenceDataService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.getPythonReferenceDataService()

    def retrieve(self, account_id, security_family_id):
        # type: (int, int) -> None
        """Retrieves the specified Future or Option chain. Retrieve here means both fetch from external service and persist into DB.

           Arguments:
               security_family_id (int): &nbsp;
               account_id (int): &nbsp;
        """
        if self._service is None:
            raise Exception("AlgoTrader reference data service not loaded.")
        self._service.retrieve(account_id, security_family_id)

    def retrieve_stocks(self, account_id, security_family_id, security_id):
        # type: (int, int, int) -> None
        """Retrieves all stocks of the specified securityFamily.
           Retrieve here means both fetch from external service and persist into DB.

           Arguments:
               account_id (int): &nbsp;
               security_family_id (int): &nbsp;
               security_id (int): &nbsp;
           """
        if self._service is None:
            raise Exception("AlgoTrader reference data service not loaded.")
        self._service.retrieveStocks(account_id, security_family_id, security_id)

    def retrieve_all(self, account_id):
        # type: (int) -> None
        """Retrieves all reference data available by the data provider.
           Retrieve here means both fetch from external service and persist into DB.

           Arguments:
               account_id (int): &nbsp;
        """
        if self._service is None:
            raise Exception("AlgoTrader reference data service not loaded.")
        self._service.retrieveAll(account_id)

