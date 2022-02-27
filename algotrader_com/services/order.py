from typing import Dict, Optional, Type

from py4j.clientserver import ClientServer
from py4j.java_collections import MapConverter
from py4j.java_gateway import JavaObject

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.order import Order, MarketOrder, LimitOrder, StopOrder, StopLimitOrder, \
    TargetPositionOrder, TrailingLimitOrder, TWAPOrder, VWAPOrder


class OrderService:
    """Delegates to pythonOrderService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonOrderService()

    def create_order_by_order_preference(self, name):
        # type: (str) -> Order
        """ Creates a new Order based on the order preference selected by its 'name'.

           Arguments:
               name (str): &nbsp;
           Returns:
               algotrader_com.domain.order.Order
        """
        vo_json = self._service.createOrderByOrderPreference(name)
        _dict = Conversions.unmarshall(vo_json)
        order = Order.convert_from_json_object(_dict)
        return order

    def validate_order(self, order):
        # type: (Order) -> None
        """Validates an order. It is suggested to call this method by itself prior to sending an order.
           However send_order method call will invoke this method again.
           Raises an exception on order validation failure.

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        self._service.validateOrder(vo_json)

    def send_order(self, order, order_preference_name=None):
        # type: (Order, str) -> Optional[Order]
        """Sends an order and in case order_preference_name parameter is specified,
           defaults unpopulated values from preference (if missing value is present).

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
               order_preference_name (str): &nbsp;
           Returns:
               Optional[Order]
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        if order_preference_name is None:
            result = self._service.sendOrder(vo_json)
        else:
            result = self._service.sendOrder(vo_json, order_preference_name)
        if result is None:
            return None
        _dict = Conversions.unmarshall(result)
        return Order.convert_from_json_object(_dict)

    def send_order_with_fix_properties(self, order, properties=None, order_preference_name=None):
        # type: (Order, Optional[Dict[str, str]], Optional[str]) -> Optional[Order]
        """Sends an order, sets its properties and in case order_preference_name parameter is specified,
           defaults unpopulated values from preference (if missing value is present).
           The properties are set OrderPropertyType.FIX to be included as custom FIX tag values in outgoing FIX messages.

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
               properties (Optional[Dict[str, str]]): &nbsp;
               order_preference_name (Optional[str]): &nbsp;
           Returns:
               Optional[Order]
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        # noinspection PyProtectedMember
        property_map_java = None
        if properties is not None:
            # noinspection PyProtectedMember
            property_map_java = MapConverter().convert(properties, self._gateway._gateway_client)
        result = self._service.sendOrderWithFixProperties(vo_json, order_preference_name, property_map_java)
        if result is None:
            return None
        _dict = Conversions.unmarshall(result)
        return Order.convert_from_json_object(_dict)

    def send_order_with_properties(self, order, properties=None, order_preference_name=None):
        # type: (Order, Optional[Dict[str, str]], Optional[str]) -> Optional[Order]
        """Sends an order defined by the OrderVO parameter and the properties field, they will be set as
           OrderPropertyType.CUSTOMIZED_ORDER to be included as custom values in outgoing orders.

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
               properties (Optional[Dict[str, str]]): &nbsp;
               order_preference_name (Optional[str]): &nbsp;
           Returns:
               Optional[Order]
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        # noinspection PyProtectedMember
        property_map_java = None
        if properties is not None:
            # noinspection PyProtectedMember
            property_map_java = MapConverter().convert(properties, self._gateway._gateway_client)
        result = self._service.sendOrderWithProperties(vo_json, order_preference_name, property_map_java)
        if result is None:
            return None
        _dict = Conversions.unmarshall(result)
        return Order.convert_from_json_object(_dict)

    def modify_order_with_fix_properties(self, order, properties=None, order_preference_name=None):
        # type: (Order, Optional[Dict[str, str]], Optional[str]) -> None
        """Modifies an order defined by the order parameter and the properties field and defaults unpopulated values from the preference.
           The properties will be set as OrderPropertyType.FIX to be included as custom FIX tag values in outgoing FIX messages.

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
               properties (Optional[Dict[str, str]]): &nbsp;
               order_preference_name (Optional[str]): &nbsp;
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        # noinspection PyProtectedMember
        property_map_java = None
        if properties is not None:
            # noinspection PyProtectedMember
            property_map_java = MapConverter().convert(properties, self._gateway._gateway_client)
        self._service.modifyOrderWithFixProperties(vo_json, order_preference_name, property_map_java)

    def suggest_order(self, order):
        # type: (Order) -> None
        """Sends a Trade Suggestion via Email / Text Message.

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        self._service.suggestOrder(vo_json)

    def cancel_all_orders_by_strategy(self, strategy_id):
        # type: (int) -> None
        """
           Arguments:
               strategy_id (int): &nbsp;
        """
        return self.cancel_all_orders_by_portfolio(strategy_id)

    def cancel_all_orders_by_portfolio(self, portfolio_id):
        # type: (int) -> None
        """
           Arguments:
               portfolio_id (int): &nbsp;
        """
        self._service.cancelAllOrdersByPortfolio(portfolio_id)

    def cancel_order(self, order):
        # type: (Order) -> None
        """
           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
        """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        self._service.cancelOrder(vo_json)

    def cancel_order_by_int_id(self, int_id):
        # type: (str) -> None
        """Cancels an order by its int_id.

           Arguments:
               int_id (str): &nbsp;
        """
        self._service.cancelOrderByIntId(int_id)

    def modify_order(self, order):
        # type: (Order) -> None
        """Modifies an order by overwriting the current order with the order passed to this method.

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
        """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        self._service.modifyOrder(vo_json)

    def modify_order_by_int_id(self, int_id, properties):
        # type: (str, Dict[str,str]) -> None
        """Modifies an Order defined by its intId by overwriting the current
           Order with the defined properties.

           Arguments:
               int_id (str): &nbsp;
               properties (Dict[str,str]): &nbsp;
           """
        _map = self._gateway.jvm.HashMap()
        for key in properties:
            _map.put(key, properties[key])
        self._service.modifyOrder(int_id, _map)

    def modify_order_by_preference_name(self, order, order_preference_name):
        # type: (Order, str) -> None
        """Modifies an Order by overwriting the current Order with the Order and preference passed to this method,
           defaults unpopulated values on the passed in order from preference (if missing value is present).

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
               order_preference_name (str): &nbsp;
       """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        self._service.modifyOrder(vo_json, order_preference_name)

    def get_next_order_id(self, order_class, account_id):
        # type: (Type[Order], int) -> str
        """Generates next order intId for the given account.

           Arguments:
               order_class (Class of algotrader_com.domain.order.Order): Subclass of Order class
               account_id (int): &nbsp;
           Returns:
               str: Next order id as string
        """
        if order_class == MarketOrder:
            java_class = "ch.algotrader.entity.trade.MarketOrder"
        elif order_class == LimitOrder:
            java_class = "ch.algotrader.entity.trade.LimitOrder"
        elif order_class == StopOrder:
            java_class = "ch.algotrader.entity.trade.StopOrder"
        elif order_class == StopLimitOrder:
            java_class = "ch.algotrader.entity.trade.StopLimitOrder"
        elif order_class == TargetPositionOrder:
            java_class = "ch.algotrader.entity.trade.algo.TargetPositionOrder"
        elif order_class == TrailingLimitOrder:
            java_class = "ch.algotrader.entity.trade.algo.TrailingLimitOrder"
        elif order_class == TWAPOrder:
            java_class = "ch.algotrader.entity.trade.algo.TWAPOrder"
        elif order_class == VWAPOrder:
            java_class = "ch.algotrader.entity.trade.algo.VWAPOrder"
        else:
            raise Exception("Unsupported class: " + str(order_class))

        return self._service.getNextOrderId(java_class, account_id)

    def is_trading_session_logged_on(self, order):
        # type: (Order) -> bool
        """Checks if trading session is logged on (true by default for REST adapters, actually checked for FIX adapters).

           Arguments:
               order (algotrader_com.domain.order.Order): &nbsp;
           Return:
               bool
           """
        order_class = order.get_java_class()
        vo_json = Conversions.marshall(order, order_class)
        return self._service.isTradingSessionLoggedOn(vo_json)
