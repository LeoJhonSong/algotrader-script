from algotrader_com.services.account import AccountService
from algotrader_com.services.calendar import CalendarService
from algotrader_com.services.combination import CombinationService
from algotrader_com.services.common_config import CommonConfig
from algotrader_com.services.event_dispatcher import EventDispatcher
from algotrader_com.services.future import FutureService
from algotrader_com.services.generic_events import GenericEventsService
from algotrader_com.services.health import HealthService
from algotrader_com.services.historical_data import HistoricalDataService
from algotrader_com.services.lookup import LookupService
from algotrader_com.services.market_data import MarketDataService
from algotrader_com.services.market_data_cache import MarketDataCacheService
from algotrader_com.services.measurement import MeasurementService
from algotrader_com.services.option import OptionService
from algotrader_com.services.order import OrderService
from algotrader_com.services.order_lookup import OrderLookupService
from algotrader_com.services.portfolio import PortfolioService
from algotrader_com.services.portfolio_value import PortfolioValueService
from algotrader_com.services.position import PositionService
from algotrader_com.services.property import PropertyService
from algotrader_com.services.rate_limit import RateLimitService
from algotrader_com.services.reference import ReferenceDataService
from algotrader_com.services.rfq import RfqService
from algotrader_com.services.subscription import SubscriptionService
from algotrader_com.services.transaction import TransactionService
from algotrader_com.services.transfer import TransferService
from py4j.clientserver import ClientServer
from py4j.protocol import Py4JJavaError
from typing import List


class PythonToAlgoTraderInterface:
    """Delegates calls from Python strategies to Java based PythonStrategyService or services it contains.
       Method names mostly mirror services methods, in Python format with lowercase and underscores.

       Attributes:
           portfolio_service (algotrader_com.services.portfolio.PortfolioService): &nbsp;
           portfolio_value_service (algotrader_com.services.portfolio.PortfolioValueService): &nbsp;
           order_service (algotrader_com.services.order.OrderService): &nbsp;
           subscription_service (algotrader_com.services.subscription.SubscriptionService): &nbsp;
           historical_data_service (algotrader_com.services.historical_data.HistoricalDataService): &nbsp;
           market_data_service (algotrader_com.services.market_data.MarketDataService): &nbsp;
           position_service (algotrader_com.services.position.PositionService): &nbsp;
           order_lookup_service (algotrader_com.services.order_lookup.OrderLookupService): &nbsp;
           lookup_service (algotrader_com.services.lookup.LookupService): &nbsp;
           account_service (algotrader_com.services.account.AccountService): &nbsp;
           reference_data_service (algotrader_com.services.reference.ReferenceDataService): &nbsp;
           calendar_service (algotrader_com.services.calendar.CalendarService): &nbsp;
           future_service (algotrader_com.services.future.FutureService): &nbsp;
           combination_service (algotrader_com.services.combination.CombinationService): &nbsp;
           market_data_cache_service (algotrader_com.services.market_data_cache.MarketDataCacheService): &nbsp;
           common_config (algotrader_com.services.common_config.CommonConfig): &nbsp;
           measurement_service (algotrader_com.services.measurement.MeasurementService): &nbsp;
           rfq_service (algotrader_com.services.rfq.RfqService): &nbsp;
           option_service (algotrader_com.services.option.OptionService): &nbsp;
           event_dispatcher (algotrader_com.services.event_dispatcher.EventDispatcher): &nbsp;
           generic_events_service (algotrader_com.services.generic_events.GenericEventsService): &nbsp;
           health_service (algotrader_com.services.health.HealthService): &nbsp;
           transaction_service (algotrader_com.services.transaction.TransactionService): &nbsp;
       """

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway

    # noinspection PyAttributeOutsideInit
    def prepare_services(self):
        self.portfolio_service = self._load_service(PortfolioService)  # type: PortfolioService
        self.portfolio_value_service = self._load_service(PortfolioValueService)  # type: PortfolioValueService
        self.order_service = self._load_service(OrderService)  # type: OrderService
        self.subscription_service = self._load_service(SubscriptionService)  # type: SubscriptionService
        self.historical_data_service = self._load_service(HistoricalDataService)  # type: HistoricalDataService
        self.market_data_service = self._load_service(MarketDataService)  # type: MarketDataService
        self.position_service = self._load_service(PositionService)  # type: PositionService
        self.order_lookup_service = self._load_service(OrderLookupService)  # type: OrderLookupService
        self.lookup_service = self._load_service(LookupService)  # type: LookupService
        self.account_service = self._load_service(AccountService)  # type: AccountService
        self.reference_data_service = self._load_service(ReferenceDataService)  # type: ReferenceDataService
        self.calendar_service = self._load_service(CalendarService)  # type: CalendarService
        self.future_service = self._load_service(FutureService)  # type: FutureService
        self.combination_service = self._load_service(CombinationService)  # type: CombinationService
        self.market_data_cache_service = self._load_service(MarketDataCacheService)  # type: MarketDataCacheService
        self.common_config = self._load_service(CommonConfig)  # type: CommonConfig
        self.measurement_service = self._load_service(MeasurementService)  # type: MeasurementService
        self.rfq_service = self._load_service(RfqService)  # type: RfqService
        self.option_service = self._load_service(OptionService)  # type: OptionService
        self.property_service = self._load_service(PropertyService)  # type: PropertyService
        self.event_dispatcher = self._load_service(EventDispatcher)  # type: EventDispatcher
        self.generic_events_service = self._load_service(GenericEventsService)  # type: GenericEventsService
        self.rate_limit_service = self._load_service(RateLimitService)  # type: RateLimitService
        self.health_service = self._load_service(HealthService)  # type: HealthService
        self.transaction_service = self._load_service(TransactionService)  # type: TransactionService
        self.transfer_service = self._load_service(TransferService)  # type: TransferService

    def _load_service(self, service):
        try:
            return service(self._gateway)
        except Py4JJavaError as error:
            # if the service can't be loaded from AT side
            # (e.g. getHistoricalDataService() throws an exception if no historical data profile configured)
            # return an object that throws an error on any call
            # this way services are loaded eagerly, but errors thrown only for services that are used
            #  and are not available
            _new_service = service()
            error_message = error.java_exception.getMessage()
            for method in dir(_new_service):
                if method.startswith("_"):
                    continue
                setattr(_new_service, method, lambda: self._raise_error(Exception(error_message)))
            return _new_service

    def _raise_error(self, error):
        raise error

    def subscribe_to_only_some_event_handler_methods(self, methods_list):
        # type: (List[str]) -> None
        """Client's Python strategy may restrict the event handler methods (onXYZ) that AlgoTrader should call on it
           from the Java side.
           This is to prevent unnecessary calls to methods the Python strategy doesn't implement (override)
           from the StrategyService Python class. If e.g. only onBar method is overridden, subscription to onTick is
           not necessary.

           Arguments:
               methods_list (List[str]): List of strings. <i>None</i> value argument is interpreted as all methods are to be subscribed.
        """
        java_set = self._gateway.jvm.java.util.HashSet()
        for method in methods_list:
            java_set.add(method)

        self._gateway.entry_point.setSubscribedEventHandlerMethods(java_set)

    def ping(self):
        # type: () -> None
        self._gateway.entry_point.ping()

    def get_weight(self):
        # type: () -> float
        """
        Returns:
            float
        """

        return self._gateway.entry_point.getWeight()

    def set_weight(self, weight):
        # type: (float) -> None
        """

        Args:
            weight (float): &nbsp;
        """
        self._gateway.entry_point.setWeight(weight)

    def get_portfolio_id(self):
        # type: () -> int
        """
        Returns:
            int
        """
        return self._gateway.entry_point.getPortfolio().getId()

    def get_strategy_name(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._gateway.entry_point.getStrategyName()

    def set_strategy_name(self, strategy_name):
        # type: (str) -> None
        """
        Args:
            strategy_name (str): &nbsp;
        """
        self._gateway.entry_point.setStrategyName(strategy_name)
