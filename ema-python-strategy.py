import logging
from decimal import Decimal

import numpy as np

from algotrader_com.domain.order import MarketOrder
from algotrader_com.interfaces.connection import connect_to_algotrader, wait_for_algotrader_to_disconnect
from algotrader_com.services.strategy import StrategyService

ACCOUNT_ID = 123
SECURITY_ID = 709
ORDER_QUANTITY = Decimal("10000")
EMA_PERIOD_SHORT = 10
EMA_PERIOD_LONG = 20

portfolio_id = None

logging.basicConfig(level=logging.DEBUG)


class EMAStrategyService(StrategyService):
    """Strategy logic implementation. Extends StrategyService from AlgoTrader Python interface.
       The class is connected to AlgoTrader using connect_to_algotrader function call below."""

    def __init__(self):
        StrategyService.__init__(self)

    STRATEGY_NAME = "EMA"
    previous_difference = 0
    first_order_sent = False
    position = 0.0

    def on_init(self, lifecycle_event):
        self.python_to_at_entry_point.set_strategy_name(self.STRATEGY_NAME)
        self.close_price_window1 = []
        self.close_price_window2 = []
        self.portfolio_value_evolution = []
        self.position_evolution = []
        self.price_evolution = []

    def on_start(self, lifecycle_event):
        # noinspection PyBroadException
        try:
            self.python_to_at_entry_point.subscription_service.subscribe_market_data_event(
                self.STRATEGY_NAME, SECURITY_ID, ACCOUNT_ID)
            self.python_to_at_entry_point.subscription_service.subscribe_portfolio([self.STRATEGY_NAME])

        except Exception as e:
            print(e)
            pass

    def on_exit(self, lifecycle_event):
        logging.info("Shutting down.")

    _num_processed_bars = 0

    def on_tick(self, tick):
        # print("Tick received: " + str(tick))  # invoked when strategy connected to AT started using
        #  EmbeddedStrategyStarter, not invoked from SimulationStarter
        pass

    def on_bar(self, bar):
        EMAStrategyService._num_processed_bars += 1
        if EMAStrategyService._num_processed_bars % 10000 == 0:
            print("Number of processed bars: " + str(EMAStrategyService._num_processed_bars))

        self.close_price_window1.append(float(bar.close))
        self.close_price_window2.append(float(bar.close))
        # current_portfolio_value = 0
        current_portfolio_value = self.python_to_at_entry_point.portfolio_value_service.get_net_liq_value()
        self.portfolio_value_evolution.append(current_portfolio_value)
        self.price_evolution.append(bar.close)

        if len(self.close_price_window1) > EMA_PERIOD_SHORT + 1:  # remove the oldest element from the list
            self.close_price_window1.pop(0)  # remove the oldest element from the list
        if len(self.close_price_window2) > EMA_PERIOD_LONG + 1:  # remove the oldest element from the list
            self.close_price_window2.pop(0)  # remove the oldest element from the list

        # if we have enough data already, calculate EMA averages difference, buy/sell on cross
        if len(self.close_price_window2) >= EMA_PERIOD_LONG:
            self.close_price_window1.pop(0)

            ema1 = _numpy_ewma_vectorized_v2(np.array(self.close_price_window1), EMA_PERIOD_SHORT)
            ema2 = _numpy_ewma_vectorized_v2(np.array(self.close_price_window2), EMA_PERIOD_LONG)
            difference = ema1[-1] - ema2[-1]
            global portfolio_id
            if portfolio_id is None:
                portfolio_id = self.python_to_at_entry_point.get_portfolio_id()

            account_id = ACCOUNT_ID
            security_id = SECURITY_ID
            if not self.first_order_sent:
                quantity = ORDER_QUANTITY
            else:
                quantity = ORDER_QUANTITY * 2  # closing opposite position and opening new one

            if difference > 0.0 and (self.previous_difference == 0 or self.previous_difference < 0.0):
                side = "BUY"
                market_order = MarketOrder(quantity=quantity, side=side, portfolio_id=portfolio_id, account_id=account_id,
                                           security_id=security_id)
                self.python_to_at_entry_point.order_service.send_order(market_order)
                self.position += float(market_order.quantity)
                self.first_order_sent = True
            if difference < 0.0 and (self.previous_difference == 0 or self.previous_difference > 0.0):
                side = "SELL"
                market_order = MarketOrder(quantity=quantity, side=side, portfolio_id=portfolio_id, account_id=account_id,
                                           security_id=security_id)
                self.python_to_at_entry_point.order_service.send_order(market_order)
                self.position -= float(market_order.quantity)
                self.first_order_sent = True
            self.previous_difference = difference
            self.position_evolution.append(self.position)


def _numpy_ewma_vectorized_v2(data, window):
    """Faster exponential moving average calculation, source https://stackoverflow.com/a/42926270/609973"""
    alpha = 2 / (window + 1.0)
    alpha_rev = 1 - alpha
    n = data.shape[0]
    pows = alpha_rev ** (np.arange(n + 1))
    scale_arr = 1 / pows[:-1]
    offset = data[0] * pows[1:]
    pw0 = alpha * alpha_rev ** (n - 1)
    mult = data * pw0 * scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums * scale_arr[::-1]
    return out


# an optional parameter. if not specified, all callback methods are subscribed
only_subscribe_methods_list = ["onInit", "onStart", "onExit", "onBar", "onTick"]
strategy = EMAStrategyService()
_python_to_at_entry_point = connect_to_algotrader(strategy, only_subscribe_methods_list)
# noinspection PyBroadException
try:  # try subscribing to market data, if AT is already up. otherwise data will be subscribed on START lifecycle event
    _python_to_at_entry_point.subscription_service\
        .subscribe_market_data_event(EMAStrategyService.STRATEGY_NAME, SECURITY_ID, ACCOUNT_ID)
except BaseException:
    pass

wait_for_algotrader_to_disconnect(_python_to_at_entry_point)
