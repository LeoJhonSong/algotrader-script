from datetime import datetime
from typing import List, Optional

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import OrderStatus, OrderPreference
from algotrader_com.domain.order import Order, OrderDetails


class OrderLookupService:
    """Delegates to pythonOrderLookupService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonOrderLookupService()

    # noinspection PyIncorrectDocstring
    def lookup_int_id_by_ext_id(self, connector_descriptor, ext_id):
        # type: (str, str) -> str
        """Looks up order's int id by its the ext id.

           Arguments:
               .. include:: ../adapter_types.txt
               ext_id (str): &nbsp;
           Returns:
               str
        """
        connector_descriptor_java = self._gateway.jvm.ch.algotrader.api.connector.application.ConnectorDescriptor(connector_descriptor)
        int_id = self._service.lookupIntIdByExtId(connector_descriptor_java, ext_id)
        return int_id

    def get_order_by_int_id(self, int_id):
        # type: (str) -> Optional[Order]
        """Gets an order (active or completed) by its int id.

           Arguments:
               int_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.order.Order
        """
        order_vo_json = self._service.getOrderByIntId(int_id)
        if order_vo_json is None:
            return None
        _dict = Conversions.unmarshall(order_vo_json)
        order = Order.convert_from_json_object(_dict)
        return order

    def get_active_order_by_int_id(self, int_id):
        # type: (str) -> Optional[Order]
        """Gets an active order by its int id.

           Arguments:
               int_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.order.Order
        """
        order_vo_json = self._service.getActiveOrderByIntId(int_id)
        if order_vo_json is None:
            return None
        _dict = Conversions.unmarshall(order_vo_json)
        order = Order.convert_from_json_object(_dict)
        return order

    def get_orders_by_parent_int_id(self, parent_int_id):
        # type: (str) -> List[Order]
        """Returns Child-Orders of a given Order identified via its internalId
           Only direct children of an order can be received.

           Arguments:
               parent_int_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
           """
        order_vo_jsons = self._service.getOrdersByParentIntId(parent_int_id)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_active_orders_by_parent_int_id(self, parent_int_id):
        # type: (str) -> List[Order]
        """Returns all active child orders of the parent order with the given int id.

           Arguments:
               parent_int_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        order_vo_jsons = self._service.getActiveOrdersByParentIntId(parent_int_id)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_active_orders_by_strategy(self, strategy_id):
        # type: (int) -> List[Order]
        """Returns active orders for the given strategy.

           Arguments:
               strategy_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        return self.get_active_orders_by_portfolio(strategy_id)

    def get_active_orders_by_portfolio(self, portfolio_id):
        # type: (int) -> List[Order]
        """Returns active orders for the given portfolio.

           Arguments:
               portfolio_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        order_vo_jsons = self._service.getActiveOrdersByPortfolio(portfolio_id)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_active_orders_by_security(self, security_id):
        # type: (int) -> List[Order]
        """Returns active orders for the given security.

           Arguments:
               security_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        order_vo_jsons = self._service.getActiveOrdersBySecurity(security_id)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_active_orders_by_strategy_and_security(self, strategy_id, security_id):
        # type: (int, int) -> List[Order]
        """Returns active orders for the given strategy and security.

           Arguments:
               strategy_id (str): &nbsp;
               security_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        return self.get_active_orders_by_portfolio_and_security(strategy_id, security_id)

    def get_active_orders_by_portfolio_and_security(self, portfolio_id, security_id):
        # type: (int, int) -> List[Order]
        """Returns active orders for the given portfolio and security.

           Arguments:
               portfolio_id (str): &nbsp;
               security_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        order_vo_jsons = self._service \
            .getActiveOrdersByPortfolioAndSecurity(portfolio_id, security_id)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_orders_in_timeframe(self, from_date, to_date):
        # type: (datetime, datetime) -> List[Order]
        """Gets all (active and completed) orders in timeframe.

           Arguments:
               from_date (datetime): &nbsp;
               to_date (datetime): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        from_date_java = Conversions.python_datetime_to_zoneddatetime(from_date, self._gateway)
        to_date_java = Conversions.python_datetime_to_zoneddatetime(to_date, self._gateway)
        order_vo_jsons = self._service \
            .getOrdersInTimeframe(from_date_java, to_date_java)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_status_by_int_id(self, int_id):
        # type: (str) -> Optional[OrderStatus]
        """Returns execution status of the order with the given int id.

           Arguments:
               int_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.entity.OrderStatus
        """
        json = self._service.getStatusByIntId(int_id)
        if json is None:
            return None
        _dict = Conversions.unmarshall(json)
        order_status = OrderStatus.convert_from_json(_dict)
        return order_status

    def get_order_statuses_in_timeframe(self, from_date, to_date):
        # type: (datetime, datetime) -> List[OrderStatus]
        """Finds all order statuses that were created / updated in given time frame.

           Arguments:
               from_date (datetime): &nbsp;
               to_date (datetime): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.OrderStatus
        """
        from_date_java = Conversions.python_datetime_to_zoneddatetime(from_date, self._gateway)
        to_date_java = Conversions.python_datetime_to_zoneddatetime(to_date, self._gateway)
        order_status_vo_jsons = self._service.getOrderStatusesInTimeframe(from_date_java, to_date_java)
        if order_status_vo_jsons is None:
            return []
        order_statuses = []
        for json in order_status_vo_jsons:
            _dict = Conversions.unmarshall(json)
            order_status = OrderStatus.convert_from_json(_dict)
            order_statuses.append(order_status)
        return order_statuses

    def get_daily_orders(self):
        # type: () -> List[Order]
        """Finds all orders of the current day in descending *dateTime* order.

           Returns:
               List of algotrader_com.domain.order.Order
        """
        order_vo_jsons = self._service.getDailyOrders()
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_daily_orders_by_strategy(self, strategy_name):
        # type: (str) -> List[Order]
        """Finds all orders of the current day of a specific Strategy in descending *dateTime* order.

           Arguments:
               strategy_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        return self.get_daily_orders_by_portfolio(strategy_name)

    def get_daily_orders_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Order]
        """Finds all orders of the current day of a specific Portfolio in descending *dateTime* order.

           Arguments:
               portfolio_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        order_vo_jsons = self._service.getDailyOrdersByPortfolio(portfolio_name)
        if order_vo_jsons is None:
            return []
        orders = []
        for vo_json in order_vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_all_order_preferences(self):
        # type: () -> List[OrderPreference]
        """Gets all order preferences.

           Returns:
               List of algotrader_com.domain.entity.OrderPreference
        """
        vo_jsons = self._service.getAllOrderPreferences()
        if vo_jsons is None:
            return []
        preferences = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            op = OrderPreference.convert_from_json_object(_dict)
            preferences.append(op)
        return preferences

    def get_all_active_orders(self):
        # type: () -> List[Order]
        """
            Returns:
               List of algotrader_com.domain.order.Order
        """
        vo_jsons = self._service.getAllActiveOrders()
        if vo_jsons is None:
            return []
        orders = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    # noinspection PyIncorrectDocstring
    def get_active_order_by_ext_id(self, connector_descriptor, ext_id):
        # type: (str, str) -> Optional[Order]
        """
           Arguments:
               .. include:: ../adapter_types.txt
               ext_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.order.Order
        """
        vo_json = self._service.getActiveOrderByExtId(connector_descriptor, ext_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        order = Order.convert_from_json_object(_dict)
        return order

    def get_active_order_by_ext_id(self, account_id, ext_id):
        # type: (int, str) -> Optional[Order]
        """
           Arguments:
               account_id (int): &nbsp;
               ext_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.order.Order
        """
        vo_json = self._service.getActiveOrderByExtId(account_id, ext_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        order = Order.convert_from_json_object(_dict)
        return order

    def get_current_order_status(self, account_id, ext_id, int_id):
        # type: (int, str, str) -> OrderStatus
        """
                   Arguments:
                       account_id (int): &nbsp;
                       ext_id (str): &nbsp;
                       int_id (str): &nbsp;
                   Returns:
                       Optional of algotrader_com.domain.order.Order
                """
        json = self._service.getCurrentOrderStatus(account_id, ext_id, int_id)
        if json is None:
            return None
        _dict = Conversions.unmarshall(json)
        order_status = OrderStatus.convert_from_json(_dict)
        return order_status

    def get_all_active_orders_by_connector_descriptor(self, connector_descriptor):
        # type: (str) -> List[Order]
        """
           Arguments:
               connector_descriptor (str): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        vo_jsons = self._service.getAllActiveOrdersByConnectorDescriptor(connector_descriptor)
        if vo_jsons is None:
            return []
        orders = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_all_active_orders_by_account_id(self, account_id):
        # type: (int) -> List[Order]
        """
           Arguments:
               account_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.order.Order
        """
        vo_jsons = self._service.getAllActiveOrdersByAccountId(account_id)
        if vo_jsons is None:
            return []
        orders = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_active_order_details_by_int_id(self, int_id):
        # type: (str) -> Optional[OrderDetails]
        """
           Arguments:
               int_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.order.OrderDetails
        """
        vo_json = self._service.getActiveOrderDetailsByIntId(int_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        od = OrderDetails.convert_from_json(_dict)
        return od

    def get_completed_order_details_by_int_id(self, int_id):
        # type: (str) -> Optional[OrderDetails]
        """
           Arguments:
               int_id (str): &nbsp;
           Returns:
               Optional of algotrader_com.domain.order.OrderDetails
        """
        vo_json = self._service.getCompletedOrderDetailsByIntId(int_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        od = OrderDetails.convert_from_json(_dict)
        return od

    def get_active_order_details(self):
        # type: () -> List[OrderDetails]
        """
           Returns:
               List of algotrader_com.domain.order.OrderDetails
        """
        vo_jsons = self._service.getActiveOrderDetails()
        ods = []
        for vo in vo_jsons:
            _dict = Conversions.unmarshall(vo)
            od = OrderDetails.convert_from_json(_dict)
            ods.append(od)
        return ods

    def get_completed_order_details(self):
        # type: () -> List[OrderDetails]
        """
           Returns:
               List of algotrader_com.domain.order.OrderDetails
        """
        vo_jsons = self._service.getCompletedOrderDetails()
        ods = []
        for vo in vo_jsons:
            _dict = Conversions.unmarshall(vo)
            od = OrderDetails.convert_from_json(_dict)
            ods.append(od)
        return ods
