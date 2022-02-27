from typing import List, Optional, Type

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import Subscription
from algotrader_com.domain.market_data import Tick, MarketScannerParameters
from algotrader_com.domain.security import Security


class MarketDataService:
    """Delegates to pythonMarketDataService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonMarketDataService()

    # noinspection PyIncorrectDocstring
    def subscribe(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, int) -> None
        """Subscribes a Security for the defined portfolio.
           Will be executed only if there is only one active market adapter, otherwise will raise an exception
           If there are multiple market adapters, you can restrict this.

           Arguments:
               portfolio_name (str): &nbsp;
               security_id (int): &nbsp;
               account_id (int): &nbsp;
        """
        if account_id is None:
            self._service.subscribe(portfolio_name, security_id)
        else:
            self._service.subscribe(portfolio_name, security_id, account_id)

    def subscribe_to_currency(self, portfolio_name, currency):
        # type: (str, str) -> None
        """Subscribes the Forex Security needed to convert currency and basePortfolioCurrency.

           Arguments:
               portfolio_name (str): &nbsp;
               currency (str): &nbsp;
        """
        self._service \
            .subscribeToCurrency(portfolio_name, currency)

    # noinspection PyIncorrectDocstring
    def unsubscribe(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, int) -> None
        """Removes subscriptions of a particular portfolio for which the portfolio does not have an open position.

           Arguments:
               portfolio_name (str): &nbsp;
               security_id (int): &nbsp;
               account_id (int): &nbsp;
        """
        if account_id is None:
            self._service.unsubscribe(portfolio_name, security_id)
        else:
            self._service.unsubscribe(portfolio_name, security_id, account_id)

    def get_subscriptions_by_strategy(self, strategy_name):
        # type: (str) -> List[Subscription]
        """Gets all subscriptions by the defined strategy_name. If corresponding Securities are
           Combination-s, all components will be initialized as well. In additional all properties are initialized.

           Arguments:
               strategy_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
           """
        return self.get_subscriptions_by_portfolio(strategy_name)

    def get_subscriptions_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Subscription]
        """Gets all subscriptions by the defined portfolio_name. If corresponding Securities are
           Combination-s, all components will be initialized as well. In additional all properties are initialized.

           Arguments:
               portfolio_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
           """
        result = []
        returned = self._service.getSubscriptionsByPortfolio(portfolio_name)
        for sub in range(len(returned)):
            result.append(Subscription.convert_from_vo(returned[sub]))
        return result

    def find_securities_by_market_scan(self, parameters, account_id):
        # type: (MarketScannerParameters, int) -> List[Security]
        """
           Arguments:
               parameters (algotrader_com.domain.market_data.MarketScannerParameters): &nbsp;
               account_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.findSecuritiesByMarketScan(parameters.convert_to_java(self._gateway), account_id)
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    # noinspection PyIncorrectDocstring
    def subscribe_to_order_book(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, Optional[str]) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                account_id (int): &nbsp;
        """
        if account_id is None:
            self._service.subscribeToOrderBook(portfolio_name, security_id)
        else:
            self._service.subscribeToOrderBook(portfolio_name, security_id, account_id)

    # noinspection PyIncorrectDocstring
    def unsubscribe_from_order_book(self, portfolio_name, security_id, account_id=None):
        # type: (str, int, Optional[int]) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                account_id (int): &nbsp;
        """
        if account_id is None:
            self._service.unsubscribeFromOrderBook(portfolio_name, security_id)
        else:
            self._service.unsubscribeFromOrderBook(portfolio_name, security_id, account_id)

    # noinspection PyIncorrectDocstring
    def unsubscribe_from_order_books_other_than(self, portfolio_name, security_id, account_id):
        # type: (str, int, int) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_id (int): &nbsp;
                account_id (int): &nbsp;
        """
        self._service.unsubscribeFromOrderBooksOtherThan(portfolio_name, security_id, account_id)

    def subscribe_to_aggregated_order_book(self, portfolio_name, symbol, security_class):
        # type: (str, str, Type[Security]) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                symbol (str): &nbsp;
                security_class (str): &nbsp;
        """
        security_class_name = security_class.get_java_class()
        java_class = self._gateway.jvm.Class.forName(security_class_name)
        self._service.subscribeToAggregatedOrderBook(portfolio_name, symbol, java_class)

    def unsubscribe_from_aggregated_order_book(self, portfolio_name, symbol, security_class):
        # type: (str, str, Type[Security]) -> None
        """
            Arguments:
                portfolio_name (str): &nbsp;
                symbol (str): &nbsp;
                security_class (str): &nbsp;
        """
        security_class_name = security_class.get_java_class()
        java_class = self._gateway.jvm.Class.forName(security_class_name)
        self._service.unsubscribeFromAggregatedOrderBook(portfolio_name, symbol, java_class)

    def pause_simulation_data(self):
        # type: () -> None
        """
            Pauses simulation data sources.
        """
        self._service.pauseSimulationData()

    def resume_simulation_data(self):
        # type: () -> None
        """
            Resumes simulation data sources.
        """
        self._service.resumeSimulationData()
