from typing import Optional

from algotrader_com.domain.entity import LifecycleEvent, OrderStatus, Fill, Transaction, PositionMutation, \
    SessionEvent, AccountEvent, CashBalance, OrderCompletion, ReconciliationEvent, OrderRequestStatusEvent, RfqQuote, \
    LogEvent, HealthStatus, RfqQuoteRequestReject, TradedVolume, ExternalBalance, Transfer
from algotrader_com.domain.market_data import Bar, Quote, Trade, Tick, OrderBook, AggregatedOrderBook, GenericTick
from algotrader_com.domain.order import Order
from algotrader_com.interfaces.py2at import PythonToAlgoTraderInterface
from py4j.java_gateway import JavaObject


class StrategyService:
    """Base class to be extended by strategies to be able to receive data and events from AlgoTrader
       and to use AlgoTrader services.
       Only some of the event handler methods need to be overridden.
       Method names mirror StrategyService interface onXYZ methods, in Python format with lowercase and underscores.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect.

       Variables:
           python_to_at_entry_point (algotrader_com.interfaces.py2at.PythonToAlgoTraderInterface): &nbsp;
       """

    python_to_at_entry_point = None  # type: Optional[PythonToAlgoTraderInterface]

    def __init__(self):
        self.test_mode = False

    def on_init(self, lifecycle_event):
        # type: (LifecycleEvent) -> None
        """
        Called <i>after</i> deploying all modules of the Server Engine but <i>before</i> deploying the
        init modules of
        the Strategy Engines.

        Arguments:
            lifecycle_event (algotrader_com.domain.entity.LifecycleEvent): &nbsp;
        """
        return

    def on_start(self, lifecycle_event):
        # type: (LifecycleEvent) -> None
        """
        Called <i>after</i> deploying the run modules of all
        Engines. Market data events may or may not be feeding at this stage.

        Arguments:
            lifecycle_event (algotrader_com.domain.entity.LifecycleEvent): &nbsp;
        """
        return

    def on_prefeed(self, lifecycle_event):
        # type: (LifecycleEvent) -> None
        """
        Called <i>after</i> deploying the init modules of
        Strategy Engines but <i>before</i> deploying their run modules and
        <i>before</i> feeding any market data events.

        Arguments:
            lifecycle_event (algotrader_com.domain.entity.LifecycleEvent): &nbsp;
        """
        return

    def on_running(self, lifecycle_event):
        # type: (LifecycleEvent) -> None
        """
        Algo Trader is fully operational after the services finishing their START phase.

        Arguments:
            lifecycle_event (algotrader_com.domain.entity.LifecycleEvent): &nbsp;
        """
        return

    def on_exit(self, lifecycle_event):
        # type: (LifecycleEvent) -> None
        """
        In SIMULATION mode this event occurs
        <i>after</i> finishing the simulation and <i>before</i> sending an
        EndOfSimulationVO event and <i>before</i> publishing simulation
        results.
        In REAL_TIME operation mode an EXIT
        lifecycle event occurs in the Runtime shutdown hook when the virtual
        machine begins its shutdown.

        Arguments:
            lifecycle_event (algotrader_com.domain.entity.LifecycleEvent): &nbsp;
        """
        return

    def on_tick(self, tick):
        # type: (Tick) -> None
        """
        Arguments:
            tick (algotrader_com.domain.market_data.Tick): &nbsp;
        """
        return

    def on_bar(self, bar):
        # type: (Bar) -> None
        """
        Arguments:
            bar (algotrader_com.domain.market_data.Bar): &nbsp;
        """
        return

    def on_trade(self, trade):
        # type: (Trade) -> None
        """
        Arguments:
            trade (algotrader_com.domain.market_data.Trade): &nbsp;
        """
        return

    def on_quote(self, quote):
        # type: (Quote) -> None
        """
        Arguments:
            quote (algotrader_com.domain.market_data.Quote): &nbsp;
        """
        return

    def on_rfq_quote(self, rfq_quote):
        # type: (RfqQuote) -> None
        """
        Arguments:
            rfq_quote (algotrader_com.domain.entity.RfqQuote): &nbsp;
        """
        return

    def on_rfq_reject(self, rfq_quote_request_reject):
        # type: (RfqQuoteRequestReject) -> None
        """
        Arguments:
            rfq_quote_request_reject (algotrader_com.domain.entity.RfqQuoteRequestReject): &nbsp;
        """
        return

    def on_order(self, order):
        # type: (Order) -> None
        """
        Arguments:
            order (algotrader_com.domain.order.Order): &nbsp;
        """
        return

    def on_order_status(self, order_status):
        # type: (OrderStatus) -> None
        """
        Arguments:
            order_status (algotrader_com.domain.entity.OrderStatus): &nbsp;
        """
        return

    def on_order_completion(self, order_completion):
        # type: (OrderCompletion) -> None
        """
        Arguments:
            order_completion (algotrader_com.domain.entity.OrderCompletion): &nbsp;
        """
        return

    def on_fill(self, fill):
        # type: (Fill) -> None
        """
        Arguments:
            fill (algotrader_com.domain.entity.Fill): &nbsp;
        """
        return

    def on_transaction(self, transaction):
        # type: (Transaction) -> None
        """
        Arguments:
            transaction (algotrader_com.domain.entity.Transaction): &nbsp;
        """
        return

    def on_position_mutation(self, position_mutation):
        # type: (PositionMutation) -> None
        """
        Arguments:
            position_mutation (algotrader_com.domain.entity.PositionMutation): &nbsp;
        """
        return

    def on_session_event(self, session_event):
        # type: (SessionEvent) -> None
        """
        Arguments:
            session_event (algotrader_com.domain.entity.SessionEvent): &nbsp;
        """
        return

    def on_account_event(self, account_event):
        # type: (AccountEvent) -> None
        """
        Arguments:
            account_event (algotrader_com.domain.entity.AccountEvent): &nbsp;
        """
        return

    def on_cash_balance(self, cash_balance):
        # type: (CashBalance) -> None
        """
        Arguments:
            cash_balance (algotrader_com.domain.entity.CashBalance): &nbsp;
        """
        return

    def on_reconciliation_event(self, event):
        # type: (ReconciliationEvent) -> None
        """
        Arguments:
            event (algotrader_com.domain.entity.ReconciliationEvent): &nbsp;
        """
        return

    def on_order_request_status(self, event):
        # type: (OrderRequestStatusEvent) -> None
        """
        Arguments:
            event (algotrader_com.domain.entity.OrderRequestStatusEvent): &nbsp;
        """
        return

    def on_order_book(self, orderbook):
        # type: (OrderBook) -> None
        """
        Arguments:
            orderbook (algotrader_com.domain.market_data.OrderBook): &nbsp;
        """
        return

    def on_aggregated_order_book_event(self, aggregated_orderbook):
        # type: (AggregatedOrderBook) -> None
        """
        Arguments:
            aggregated_orderbook (algotrader_com.domain.market_data.AggregatedOrderBook): &nbsp;
        """
        return

    def on_generic_event(self, java_object):
        # type: (JavaObject) -> None
        """
        For an example of converting a Java object to a Python one
        see `algotrader_com.domain.entity.DividendEvent.convert_from_java_object`

        Arguments:
            java_object (Py4J Java object): &nbsp;
        """
        return

    def on_log_event(self, event):
        # type: (LogEvent) -> None
        """
            Arguments:
                event (algotrader_com.domain.entity.LogEvent): &nbsp;
        """
        return

    def on_health_status_changed(self, health_status):
        # type: (HealthStatus) -> None
        """
            Arguments:
                health_status (algotrader_com.domain.entity.HealthStatus): &nbsp;
        """
        return

    def on_traded_volume(self, traded_volume):
        # type: (TradedVolume) -> None
        """
            Arguments:
                traded_volume (algotrader_com.domain.entity.TradedVolume): &nbsp;
        """
        return

    def on_trading_status_event(self, trading_status):
        # type: (TradingStatus) -> None
        """
            Arguments:
                trading_status (algotrader_com.domain.entity.TradingStatus): &nbsp;
        """
        return

    def on_transfer_status(self, transfer):
        # type: (Transfer) -> None
        """
        Arguments:
            transfer (algotrader_com.domain.entity.Transfer): &nbsp;
        """
        return

    def on_simulation_result(self, simulation_result):
        # type: (SimulationResult) -> None
        return

    def on_generic_tick(self, generic_tick):
        # type: (GenericTick) -> None
        """
        Arguments:
            generic_tick (algotrader_com.domain.market_data.GenericTick): &nbsp;
        """
        return

    def on_external_balance(self, external_balance):
        # type: (ExternalBalance) -> None
        """
        Arguments:
            external_balance (algotrader_com.domain.entity.ExternalBalance): &nbsp;
        """
        return
