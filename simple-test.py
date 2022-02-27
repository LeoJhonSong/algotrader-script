from collections import deque
from decimal import Decimal
from enum import IntEnum
from statistics import mean
from typing import Dict, Literal

import yaml
from typing_extensions import TypedDict

from algotrader_com.domain.market_data import Tick
from algotrader_com.domain.order import LimitOrder
from algotrader_com.interfaces.connection import connect_to_algotrader, wait_for_algotrader_to_disconnect
from algotrader_com.services.strategy import StrategyService


# data structure ---------------------------------------------------------------
class Signal(IntEnum):
    BUY = 1
    SELL = -1


class Alpha(TypedDict):
    BUY: Decimal
    SELL: Decimal


class ExchangeManager(TypedDict):
    account_id: int
    security_id: int
    minimum_tick: float


class Config(TypedDict):
    exchanges: Dict[str, ExchangeManager]
    quantity: float
    entry_threshold: float
    t: int


class SMA:
    def __init__(self, period: int) -> None:
        self.window = deque(maxlen=period)
        self.value = Decimal('0')  # type: Decimal

    def update(self, data):
        self.window.append(data)
        self.value = mean(self.window)
# ------------------------------------------------------------------------------


class PairedTestStrategyService(StrategyService):
    def __init__(self):
        StrategyService.__init__(self)

    STRATEGY_NAME = "TEST"
    previous_difference = 0
    first_order_sent = False
    position = 0.0

    def on_init(self, lifecycle_event):
        self.python_to_at_entry_point.set_strategy_name(self.STRATEGY_NAME)
        PairedTestStrategyService._num_processed_ticks = 0
        with open('./config.yaml') as f:
            config = yaml.safe_load(f)  # type: Config
        PairedTestStrategyService.exchanges = config['exchanges']
        PairedTestStrategyService.entry_threshold = config['entry_threshold']
        PairedTestStrategyService.window = config['t']
        PairedTestStrategyService.quantity = config['quantity']
        self.ticks = {}  # type: Dict[str, Tick]
        self.orders = {}  # type: Dict[str, LimitOrder]
        self.alpha = {'BUY': Decimal('0'), 'SELL': Decimal('0')}  # type: Alpha
        self.sma = SMA(config['t'])
        self.signal = None  # type: Signal | None
        self.is_entered = False  # type: bool

    def on_start(self, lifecycle_event):
        # noinspection PyBroadException
        try:
            # subscribe data from both exchanges
            for exchange in PairedTestStrategyService.exchanges.values():
                self.python_to_at_entry_point.subscription_service.subscribe_market_data_event(self.STRATEGY_NAME, exchange['security_id'], exchange['account_id'])
            self.python_to_at_entry_point.subscription_service.subscribe_portfolio([self.STRATEGY_NAME])
        except Exception as e:
            print(e)
            pass
        print('started')

    def on_exit(self, lifecycle_event):
        print("Shutting down.")

    def __ticks_update(self, tick: Tick) -> bool:
        """internal function for tick and alpha update

        Parameters
        ----------
        tick : Tick
            the latest tick from on_tick func

        Returns
        -------
        bool
            return whether the amount of data in sma reaches the window length,
            which mean ready for signal generation
        """
        self.ticks[tick.connector_descriptor] = tick
        if len(self.ticks.keys()) == 2:  # when both accounts initialed
            self.sma.update(((self.ticks['Deribit'].bid + self.ticks['Deribit'].ask) / 2) - ((self.ticks['FTX'].bid + self.ticks['FTX'].ask) / 2))
            self.alpha = {
                'BUY': self.ticks['Deribit'].ask - self.ticks['FTX'].bid - self.sma.value,
                'SELL': self.ticks['Deribit'].bid - self.ticks['FTX'].ask - self.sma.value
            }
        if len(self.sma.window) == self.sma.window.maxlen:
            return True
        else:
            if len(self.sma.window) % 100 == 0:
                print(f'sma length now: {len(self.sma.window)}')
            return False

    def __order_wrapper(self, exchange: str, side: Literal['BUY', 'SELL'], price: Decimal):
        """if order of this exchange is not in orders dict, create order, send
        order and then save to order dict, else modify the order
        """
        if exchange not in self.orders.keys():
            self.orders[exchange] = self.python_to_at_entry_point.order_service.send_order(LimitOrder(
                limit=price,
                side=side,
                quantity=Decimal(PairedTestStrategyService.quantity),
                account_id=PairedTestStrategyService.exchanges[exchange]['account_id'],
                security_id=PairedTestStrategyService.exchanges[exchange]['security_id'],
                exchange_order=False,
                portfolio_id=self.python_to_at_entry_point.get_portfolio_id()
            ))
            print(f'Created {side} order of {exchange} at price of {price}')
        else:
            self.python_to_at_entry_point.order_service.modify_order_with_fix_properties(
                self.orders[exchange],
                properties={
                    'limit': str(price),
                    'side': side,
                    'quantity': str(Decimal(PairedTestStrategyService.quantity)),
                    'account_id': str(PairedTestStrategyService.exchanges[exchange]['account_id']),
                    'security_id': str(PairedTestStrategyService.exchanges[exchange]['security_id']),
                    'exchange_order': 'False',
                    'portfolio_id': str(self.python_to_at_entry_point.get_portfolio_id())
                }
            )
            print(f'Modified {side} order of {exchange} to price of {price}')

    def __order_check(self) -> list:
        filled_orders = []
        for exchange in self.orders:
            # FIXME: will this be updating?
            if self.orders[exchange].last_status == 'EXECUTED':
                filled_orders.append(exchange)
        print(f'Filled orders: {" ".join(filled_orders)}')
        return filled_orders

    def __order_cancel_all(self):
        for exchange in list(self.orders.keys()):
            self.python_to_at_entry_point.order_service.cancel_order(self.orders[exchange])
            self.orders.pop(exchange)  # delete order of exchange from order dict
        print('Both order canceled')

    def __order_finished(self):
        self.orders.clear()  # clear both orders
        if not self.is_entered:
            self.is_entered = True
            print('Position entered')
        else:
            self.is_entered = False
            self.signal = None
            print('Position closed')

    def __position_enter(self):
        # if not ordered yet
        if self.signal is None:  # TODO: do with order check
            # Buy signal
            if self.alpha[Signal.BUY.name] <= max(-49, -(PairedTestStrategyService.entry_threshold - 1)):
                self.signal = Signal.BUY
                print(f'Signal {self.signal.name} arise at\n\talpha of {self.alpha[Signal.BUY.name]}\n\tSMA of {self.sma.value}')
                for exchange in self.ticks.keys():
                    print(f'\t{exchange}:\n\t\tbid: {self.ticks[exchange].bid}\n\t\task: {self.ticks[exchange].ask}')
                self.__order_wrapper('Deribit', 'BUY', self.ticks['Deribit'].bid - Decimal(PairedTestStrategyService.exchanges['Deribit']['minimum_tick']))
                self.__order_wrapper('FTX', 'SELL', self.ticks['FTX'].ask + Decimal(PairedTestStrategyService.exchanges['FTX']['minimum_tick']))
            # SELL signal
            elif self.alpha[Signal.SELL.name] >= min(49, (PairedTestStrategyService.entry_threshold - 1)):
                self.signal = Signal.SELL
                print(f'Signal {self.signal.name} arise at\n\talpha of {self.alpha[Signal.SELL.name]}\n\tSMA of {self.sma.value}')
                for exchange in self.ticks.keys():
                    print(f'\t{exchange}:\n\t\tbid: {self.ticks[exchange].bid}\n\t\task: {self.ticks[exchange].ask}')
                self.__order_wrapper('FTX', 'BUY', self.ticks['FTX'].bid - Decimal(PairedTestStrategyService.exchanges['FTX']['minimum_tick']))
                self.__order_wrapper('Deribit', 'SELL', self.ticks['Deribit'].ask + Decimal(PairedTestStrategyService.exchanges['Deribit']['minimum_tick']))
        # ordered
        else:
            filled_orders = self.__order_check()
            # situation of only one order filled
            if len(filled_orders) == 1:
                # decide exchange of buy/sell order based on signal
                if self.signal == Signal.BUY:
                    buy_order_exchange = 'Deribit'
                    sell_order_exchange = 'FTX'
                else:
                    buy_order_exchange = 'FTX'
                    sell_order_exchange = 'Deribit'
                if filled_orders[0] == buy_order_exchange:
                    # close BUY position
                    if self.ticks['FTX'].bid <= self.ticks['Deribit'].bid:
                        self.__order_wrapper(buy_order_exchange, 'SELL', self.ticks['Deribit'].bid)
                        self.signal = None
                    # amend SELL order
                    else:
                        self.__order_wrapper(sell_order_exchange, 'SELL', self.ticks['FTX'].bid)
                        self.__order_finished()
                else:
                    # close Sell position
                    if self.ticks['Deribit'].ask <= self.ticks['FTX'].ask:
                        self.__order_wrapper(sell_order_exchange, 'BUY', self.ticks['FTX'].ask)
                        self.signal = None
                    # amend Buy order
                    else:
                        self.__order_wrapper(buy_order_exchange, 'BUY', self.ticks['Deribit'].ask)
                        self.__order_finished()
            # situation of both not filled, cancel them
            elif len(filled_orders) == 0:
                self.__order_cancel_all()
                self.signal = None
            # situation of both filled
            else:
                self.__order_finished()

    def __position_close(self):
        # when not ordered yet
        if not self.orders:
            # close BUY position
            if self.signal == Signal.BUY and self.alpha['BUY'] > -1:
                self.__order_wrapper('FTX', 'BUY', self.ticks['FTX'].bid - Decimal(PairedTestStrategyService.exchanges['FTX']['minimum_tick']))
                self.__order_wrapper('Deribit', 'SELL', self.ticks['Deribit'].ask + Decimal(PairedTestStrategyService.exchanges['Deribit']['minimum_tick']))
            # close SELL position
            elif self.signal == Signal.SELL and self.alpha['SELL'] < 1:
                self.__order_wrapper('Deribit', 'BUY', self.ticks['Deribit'].bid - Decimal(PairedTestStrategyService.exchanges['Deribit']['minimum_tick']))
                self.__order_wrapper('FTX', 'SELL', self.ticks['FTX'].ask + Decimal(PairedTestStrategyService.exchanges['FTX']['minimum_tick']))
        # ordered
        else:
            filled_orders = self.__order_check()
            # situation of only one order filled
            if len(filled_orders) == 1:
                # decide exchange of buy/sell order based on signal
                if self.signal == Signal.BUY:
                    buy_order_exchange = 'FTX'
                    sell_order_exchange = 'Deribit'
                else:
                    buy_order_exchange = 'Deribit'
                    sell_order_exchange = 'FTX'
                # amend SELL order
                if filled_orders[0] == buy_order_exchange:
                    self.__order_wrapper(sell_order_exchange, 'SELL', self.ticks[sell_order_exchange].bid)
                # amend BUY order
                else:
                    self.__order_wrapper(buy_order_exchange, 'BUY', self.ticks[buy_order_exchange].ask)
            # situation of both not filled, cancel them
            elif len(filled_orders) == 0:
                if (self.signal == Signal.BUY and self.alpha['BUY'] < -1) or (self.signal == Signal.SELL and self.alpha['SELL'] > 1):
                    self.__order_cancel_all()
                # amend both orders
                elif self.signal == Signal.BUY and self.alpha['BUY'] > -1:
                    self.__order_wrapper('FTX', 'BUY', self.ticks['FTX'].bid - Decimal(PairedTestStrategyService.exchanges['FTX']['minimum_tick']))
                    self.__order_wrapper('Deribit', 'SELL', self.ticks['Deribit'].ask + Decimal(PairedTestStrategyService.exchanges['Deribit']['minimum_tick']))
                    self.__order_finished()
                elif self.signal == Signal.SELL and self.alpha['SELL'] < 1:
                    self.__order_wrapper('Deribit', 'BUY', self.ticks['Deribit'].bid - Decimal(PairedTestStrategyService.exchanges['Deribit']['minimum_tick']))
                    self.__order_wrapper('FTX', 'SELL', self.ticks['FTX'].ask + Decimal(PairedTestStrategyService.exchanges['FTX']['minimum_tick']))
                    self.__order_finished()
            # situation of both filled
            else:
                self.__order_finished()
        pass

    def on_tick(self, tick: Tick):
        PairedTestStrategyService._num_processed_ticks += 1
        if PairedTestStrategyService._num_processed_ticks % 1000 == 0:
            print(f'Number of processed ticks: {str(PairedTestStrategyService._num_processed_ticks)}, {tick.connector_descriptor}')
        # update latest tick to tick dict
        is_ready = self.__ticks_update(tick)
        if is_ready:
            # Entry position
            if not self.is_entered:
                self.__position_enter()
            # Close Position
            else:
                self.__position_close()


# an optional parameter. if not specified, all callback methods are subscribed
only_subscribe_methods_list = ["onInit", "onStart", "onExit", "onTick"]
strategy = PairedTestStrategyService()
_python_to_at_entry_point = connect_to_algotrader(strategy, only_subscribe_methods_list)
try:
    # subscribe data from both exchanges
    for exchange in PairedTestStrategyService.exchanges.values():
        _python_to_at_entry_point.subscription_service.subscribe_market_data_event(PairedTestStrategyService.STRATEGY_NAME, exchange['security_id'], exchange['account_id'])
        _python_to_at_entry_point.subscription_service.subscribe_market_data_event(PairedTestStrategyService.STRATEGY_NAME, exchange['security_id'], exchange['account_id'])
except BaseException:
    pass

wait_for_algotrader_to_disconnect(_python_to_at_entry_point)
