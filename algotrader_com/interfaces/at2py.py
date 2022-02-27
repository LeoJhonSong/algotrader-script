# noinspection PyPep8Naming
import copy

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import LifecycleEvent, OrderStatus, OrderCompletion, Fill, Transaction, \
    PositionMutation, \
    SessionEvent, AccountEvent, CashBalance, ReconciliationEvent, OrderRequestStatusEvent, RfqQuote, LogEvent, \
    HealthStatus, RfqQuoteRequestReject, TradedVolume, SimulationResult, TradingStatus, ExternalBalance, Transfer
from algotrader_com.domain.market_data import Bar, Quote, Trade, Tick, OrderBook, AggregatedOrderBook, GenericTick
from algotrader_com.domain.order import Order
from algotrader_com.interfaces.py2at import PythonToAlgoTraderInterface
from algotrader_com.services.strategy import StrategyService
from py4j.clientserver import ClientServer


# noinspection PyPep8Naming
class AlgoTraderToPythonInterface:
    """Interface called from AlgoTrader side (PythonStrategyService.java).
       Delegates the calls to the StrategyService class extended by a Python strategy.
       This class is only to be used internally from connect_to_algotrader method.
       Strategies are to extend the StrategyService class to implement their logic."""
    py4j_gateway = None
    python_to_at_entry_point = None

    def __init__(self, strategy_service):
        # type: (StrategyService) -> None
        self.strategy_service = strategy_service
        self.strategy_service_copy = copy.deepcopy(self.strategy_service)  # see onExit
        self.algotrader_disconnecting = False

    def setAlgoTraderIsDisconnecting(self):
        """Called by AlgoTrader to report it is disconnecting."""
        self.algotrader_disconnecting = True

    def with_py4j_gateway(self, py4j_gateway):
        # type: (ClientServer) -> None
        self.py4j_gateway = py4j_gateway

    def with_python_to_at_entry_point(self, python_to_at_entry_point):
        # type: (PythonToAlgoTraderInterface) -> None
        self.python_to_at_entry_point = python_to_at_entry_point
        self.strategy_service.python_to_at_entry_point = python_to_at_entry_point

    def ping(self):
        return

    def _ensure_services_initialized(self):
        # necessary in case an event arrives before PythonToAlgoTraderInterface.prepare_services is called
        if self.python_to_at_entry_point.portfolio_value_service is None:
            self.python_to_at_entry_point.prepare_services()

    def onInit(self, lifecycle_event_vo):
        self._ensure_services_initialized()
        lifecycle_event = LifecycleEvent.convert_to_lifecycle_event(lifecycle_event_vo)
        self.strategy_service.on_init(lifecycle_event)

    def onPrefeed(self, lifecycle_event_vo):
        self._ensure_services_initialized()
        lifecycle_event = LifecycleEvent.convert_to_lifecycle_event(lifecycle_event_vo)
        self.strategy_service.on_prefeed(lifecycle_event)

    def onStart(self, lifecycle_event_vo):
        self._ensure_services_initialized()
        lifecycle_event = LifecycleEvent.convert_to_lifecycle_event(lifecycle_event_vo)
        self.strategy_service.on_start(lifecycle_event)

    def onRunning(self, lifecycle_event_vo):
        self._ensure_services_initialized()
        lifecycle_event = LifecycleEvent.convert_to_lifecycle_event(lifecycle_event_vo)
        self.strategy_service.on_running(lifecycle_event)

    def onExit(self, lifecycle_event_vo):
        self._ensure_services_initialized()
        lifecycle_event = LifecycleEvent.convert_to_lifecycle_event(lifecycle_event_vo)
        self.strategy_service.on_exit(lifecycle_event)
        if not self.strategy_service.test_mode:
            # re-instantiate the strategy class in order to be able to use it several times if we are running an
            #  optimization
            _python_to_at_entry_point = self.python_to_at_entry_point
            self.strategy_service = copy.deepcopy(self.strategy_service_copy)
            self.strategy_service.python_to_at_entry_point = _python_to_at_entry_point

    def onTick(self, tick_vo_json):
        self._ensure_services_initialized()
        tick_dict = Conversions.unmarshall(tick_vo_json)
        tick = Tick.convert_from_json_object(tick_dict)
        self.strategy_service.on_tick(tick)

    def onBar(self, bar_vo_json):
        self._ensure_services_initialized()
        bar_dict = Conversions.unmarshall(bar_vo_json)
        bar = Bar.convert_from_json_object(bar_dict)
        self.strategy_service.on_bar(bar)

    def onTrade(self, trade_vo_json):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(trade_vo_json)
        trade = Trade.convert_from_json_object(_dict)
        self.strategy_service.on_trade(trade)

    def onQuote(self, quote_vo_json):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(quote_vo_json)
        quote = Quote.convert_from_json_object(_dict)
        self.strategy_service.on_quote(quote)

    def onGenericTick(self, generic_tick_vo_json):
        self._ensure_services_initialized()
        generic_tick_dict = Conversions.unmarshall(generic_tick_vo_json)
        generic_tick = GenericTick.convert_from_json_object(generic_tick_dict)
        self.strategy_service.on_generic_tick(generic_tick)

    def onSimulationResult(self, simulation_result_json):
        self._ensure_services_initialized()
        simulation_result_dict = Conversions.unmarshall(simulation_result_json)
        simulation_result = SimulationResult(simulation_result_dict)
        self.strategy_service.on_simulation_result(simulation_result)

    def onRfqQuote(self, rfq_quote_vo):
        self._ensure_services_initialized()
        rfq_quote = RfqQuote.convert_from_vo(rfq_quote_vo)
        self.strategy_service.on_rfq_quote(rfq_quote)

    def onRfqReject(self, rfq_quote_request_reject_vo):
        self._ensure_services_initialized()
        rfq_quote_request_reject = RfqQuoteRequestReject.convert_from_vo(rfq_quote_request_reject_vo)
        self.strategy_service.on_rfq_reject(rfq_quote_request_reject)

    def onOrder(self, order_vo_json):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(order_vo_json)
        order = Order.convert_from_json_object(_dict)
        self.strategy_service.on_order(order)

    def onOrderStatus(self, order_vo_json):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(order_vo_json)
        order_status = OrderStatus.convert_from_json(_dict)
        self.strategy_service.on_order_status(order_status)

    def onOrderCompletion(self, order_completion_vo):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(order_completion_vo)
        order_completion = OrderCompletion.convert_from_json(_dict)
        self.strategy_service.on_order_completion(order_completion)

    def onFill(self, fill_vo):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(fill_vo)
        fill = Fill.convert_from_json(_dict)
        self.strategy_service.on_fill(fill)

    def onTransaction(self, transaction_vo):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(transaction_vo)
        transaction = Transaction.convert_from_json(_dict)
        self.strategy_service.on_transaction(transaction)

    def onPositionMutation(self, position_mutation_vo):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(position_mutation_vo)
        position_mutation = PositionMutation.convert_from_json(_dict)
        self.strategy_service.on_position_mutation(position_mutation)

    def onSessionEvent(self, session_event_vo):
        self._ensure_services_initialized()
        session_event = SessionEvent.convert_to_session_event(session_event_vo)
        self.strategy_service.on_session_event(session_event)

    def onAccountEvent(self, account_event_vo):
        self._ensure_services_initialized()
        account_event = AccountEvent.convert_to_account_event(account_event_vo)
        self.strategy_service.on_account_event(account_event)

    def onExternalBalance(self, external_balance_vo):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(external_balance_vo)
        external_balance = ExternalBalance.convert_from_json(_dict)
        self.strategy_service.on_external_balance(external_balance)

    def onTransferStatus(self, transfer_status_vo):
        self._ensure_services_initialized()
        transfer = Transfer.convert_from_vo(transfer_status_vo)
        self.strategy_service.on_transfer_status(transfer)

    def onCashBalance(self, cash_balance_vo):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(cash_balance_vo)
        cash_balance = CashBalance.convert_from_json(_dict)
        self.strategy_service.on_cash_balance(cash_balance)

    def onReconciliationEvent(self, event_vo):
        self._ensure_services_initialized()
        event = ReconciliationEvent.convert_from_vo(event_vo)
        self.strategy_service.on_reconciliation_event(event)

    def onTradingStatusEvent(self, trading_status_event_vo):
        self._ensure_services_initialized()
        event = TradingStatus.convert_from_java_object(trading_status_event_vo)
        self.strategy_service.on_trading_status_event(event)

    def onOrderRequestStatus(self, event_vo):
        self._ensure_services_initialized()
        event = OrderRequestStatusEvent.convert_from_vo(event_vo)
        self.strategy_service.on_order_request_status(event)

    def onOrderBook(self, json):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(json)
        order_book = OrderBook.convert_from_json_object(_dict)
        self.strategy_service.on_order_book(order_book)

    def onAggregatedOrderBookEvent(self, json):
        self._ensure_services_initialized()
        _dict = Conversions.unmarshall(json)
        aggregated_order_book = AggregatedOrderBook.convert_from_json_object(_dict)
        self.strategy_service.on_aggregated_order_book_event(aggregated_order_book)

    def onGenericEvent(self, generic_event_java_object):
        self._ensure_services_initialized()
        self.strategy_service.on_generic_event(generic_event_java_object)

    def onLogEvent(self, event_vo):
        self._ensure_services_initialized()
        event = LogEvent.convert_from_java_object(event_vo)
        self.strategy_service.on_log_event(event)

    def onHealthStatusChanged(self, health_status_vo):
        self._ensure_services_initialized()
        status = HealthStatus.convert_from_java_object(health_status_vo)
        self.strategy_service.on_health_status_changed(status)

    def onTradedVolume(self, traded_volume_vo):
        self._ensure_services_initialized()
        traded_volume = TradedVolume.convert_from_java_object(traded_volume_vo)
        self.strategy_service.on_traded_volume(traded_volume)
