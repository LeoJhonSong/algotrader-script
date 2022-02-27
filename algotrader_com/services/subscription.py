from typing import List, Optional

from py4j.clientserver import ClientServer
from py4j.java_collections import SetConverter

from algotrader_com.domain.conversions import Conversions


class SubscriptionService:
    """Delegates to subscriptionService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getSubscriptionService()

    # noinspection PyIncorrectDocstring
    def subscribe_market_data_event(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, int) -> None
        """Subscribes MarketDataEvent of a Security for the defined portfolio.
            Raises an exception if there are multiple active adapters.

            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                account_id (int): &nbsp;
            """
        if account_id is None:
            self._service.subscribeMarketDataEvent(portfolio_name, security_id)
        else:
            self._service.subscribeMarketDataEvent(portfolio_name, security_id, account_id)

    # noinspection PyIncorrectDocstring
    def unsubscribe_market_data_event(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, int) -> None
        """Un-subscribes MarketDataEvent of a Security
            for the defined portfolio. Requires a single active market adapter.
            Raises an exception if there are multiple active adapters.

            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                account_id (int): &nbsp;
            """
        if account_id is None:
            self._service.unsubscribeMarketDataEvent(portfolio_name, security_id)
        else:
            self._service.unsubscribeMarketDataEvent(portfolio_name, security_id, account_id)

    def subscribe_generic_events(self, java_class_names):
        # type: (List[str]) -> None
        """Subscribes Generic Events of specified classes.

            Arguments:
                java_class_names (List[str]): Fully qualified names of Java classes that should be subscribed, e.g. <i>["ch.algotrader.vo.genericevents.DividendEventVO"]</i> or <i>[DividendEvent.get_java_class()]</i>
            """
        java_classes = []
        for java_class_name in java_class_names:
            java_class = self._gateway.jvm.Class.forName(java_class_name)
            java_classes.append(java_class)
        # noinspection PyProtectedMember
        java_set = SetConverter().convert(java_classes, self._gateway._gateway_client)
        self._service.subscribeGenericEvents(java_set)

    # noinspection PyIncorrectDocstring
    def subscribe_to_order_book(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, Optional[int]) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                .. include:: ../adapter_types.txt
        """
        if account_id is None:
            self._service.subscribeToOrderBook(portfolio_name, security_id)
        else:
            self._service.subscribeToOrderBook(portfolio_name, security_id, account_id)

    # noinspection PyIncorrectDocstring
    def unsubscribe_from_order_book(self, portfolio_name, security_id, account_id):
        # type: (str, int, int) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                account_id (int): &nbsp;
        """
        self._service.unsubscribeFromOrderBook(portfolio_name, security_id, account_id)

    def subscribe_to_aggregated_order_book(self, portfolio_name, symbol, security_class_name):
        # type: (str, str, str) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                symbol (str): &nbsp;
                security_class_name (str): Fully qualified name of Java class that should be subscribed, e.g. <i>["ch.algotrader.entity.security.ForexImpl"]</i> or <i>[Forex.get_java_class()]</i>
        """
        self._service.subscribeToAggregatedOrderBook(portfolio_name, symbol,
                                                     self._gateway.jvm.Class.forName(security_class_name))

    def unsubscribe_from_aggregated_order_book(self, portfolio_name, symbol, security_class_name):
        # type: (str, str, str) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                symbol (str): &nbsp;
                security_class_name (str): Fully qualified name of Java class that should be unsubscribed, e.g. <i>["ch.algotrader.entity.security.ForexImpl"]</i> or <i>[Forex.get_java_class()]</i>
        """
        self._service.unsubscribeFromAggregatedOrderBook(portfolio_name, symbol,
                                                         self._gateway.jvm.Class.forName(security_class_name))

    def get_subscribed_portfolios(self):
        # type: () -> List[String]
        """Gets all portfolios that are being listened to.

           Returns:
               List of portfolio names that are being listened to
        """

        return self._service.getSubscribedPortfolios()

    def subscribe_to_portfolio_updates(self, portfolio_names):
        # type: (List[str]) -> None
        """Adds given portfolio to list of portfolio events that the strategy is listening to. Portfolio Events are all events that have portfolio as a property, i.e. Orders, Transactions, CashBalances, Positions and MarketData events.

           Arguments:
                portfolio_names (List[str]): &nbsp;
        """
        java_set = SetConverter().convert(portfolio_names, self._gateway._gateway_client)
        return self._service.subscribeToPortfolioUpdates(java_set)

    def unsubscribe_from_portfolio_updates(self, portfolio_names):
        # type: (List[str]) -> None
        """Stops listening to portfolio events for given portfolio.

           Arguments:
                portfolio_names (List[str]): &nbsp;
        """
        java_set = SetConverter().convert(portfolio_names, self._gateway._gateway_client)
        return self._service.unsubscribeFromPortfolioUpdates(java_set)
