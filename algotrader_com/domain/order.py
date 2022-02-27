from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict

from py4j.clientserver import ClientServer
from py4j.java_collections import ListConverter
from py4j.java_gateway import JavaObject

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import RoutingTarget, PropertyHolder, OrderStatus


class Order(PropertyHolder):
    """Mirrors ch.algotrader.entity.trade.OrderVO AlgoTrader
       Java class with fields using Python types.
       
       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str) -> None
        PropertyHolder.__init__(self, _id)
        self.int_id = int_id
        self.ext_id = ext_id
        self.parent_int_id = parent_int_id
        self.date_time = date_time
        self.side = side
        self.quantity = quantity
        self.tif = tif  # "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
        self.tif_date_time = tif_date_time
        self.exchange_order = exchange_order
        self.exchange_id = exchange_id
        self.parent_order_id = parent_order_id
        self.security_id = security_id
        self.account_id = account_id
        self.portfolio_id = portfolio_id
        self.last_status = last_status

    @abstractmethod
    def convert_to_order_vo(self, _gateway):
        # type: (ClientServer) -> JavaObject
        """Converts an order to the corresponding AlgoTrader Java value object.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_java_class():
        # type: () -> str
        """Returns corresponding Java class."""
        return "ch.algotrader.entity.trade.OrderImpl"

    @staticmethod
    def convert_to_order(order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Order
        """
           Arguments:
               order_vo (OrderVO subtype): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Order
        """
        if order_vo is None:
            return None
        if order_vo.getClass().getCanonicalName() == MarketOrder.get_java_class():
            order = MarketOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == LimitOrder.get_java_class():
            order = LimitOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == StopOrder.get_java_class():
            order = StopOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == StopLimitOrder.get_java_class():
            order = StopLimitOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == PreviouslyIndicatedOrder.get_java_class():
            order = PreviouslyIndicatedOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == TargetPositionOrder.get_java_class():
            order = TargetPositionOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == TrailingLimitOrder.get_java_class():
            order = TrailingLimitOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == TWAPOrder.get_java_class():
            order = TWAPOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == VWAPOrder.get_java_class():
            order = VWAPOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == POVOrder.get_java_class():
            order = POVOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == IcebergOrder.get_java_class():
            order = IcebergOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == SniperOrder.get_java_class():
            order = SniperOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == MarketSweepOrder.get_java_class():
            order = MarketSweepOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == SmartMarketOrder.get_java_class():
            order = SmartMarketOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == SmartLimitOrder.get_java_class():
            order = SmartLimitOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == SmartStopOrder.get_java_class():
            order = SmartStopOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        elif order_vo.getClass().getCanonicalName() == SmartStopLimitOrder.get_java_class():
            order = SmartStopLimitOrder.convert_to_order(order_vo, py4jgateway)  # type: ignore
        else:
            raise Exception("Unsupported order type " + order_vo.getClass().getSimpleName() + ".")
        return order

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Order
        """
           Arguments:
               vo_dict (deserialized OrderVO): &nbsp;
           Returns:
               Order
        """
        if vo_dict["@class"] == MarketOrder.get_java_class():
            order = MarketOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == LimitOrder.get_java_class():
            order = LimitOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == StopOrder.get_java_class():
            order = StopOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == StopLimitOrder.get_java_class():
            order = StopLimitOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == PreviouslyIndicatedOrder.get_java_class():
            order = PreviouslyIndicatedOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == TrailingLimitOrder.get_java_class():
            order = TrailingLimitOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == TargetPositionOrder.get_java_class():
            order = TargetPositionOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == TWAPOrder.get_java_class():
            order = TWAPOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == VWAPOrder.get_java_class():
            order = VWAPOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == POVOrder.get_java_class():
            order = POVOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == IcebergOrder.get_java_class():
            order = IcebergOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == SniperOrder.get_java_class():
            order = SniperOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == MarketSweepOrder.get_java_class():
            order = MarketSweepOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == SmartMarketOrder.get_java_class():
            order = SmartMarketOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == SmartLimitOrder.get_java_class():
            order = SmartLimitOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == SmartStopOrder.get_java_class():
            order = SmartStopOrder.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["@class"] == SmartStopLimitOrder.get_java_class():
            order = SmartStopLimitOrder.convert_from_json_object(vo_dict)  # type: ignore
        else:
            raise Exception("Unknown quote type: " + vo_dict["objectType"])
        return order


class SimpleOrder(Order):
    """Mirrors ch.algotrader.entity.trade.SimpleOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None):
        # type: (SimpleOrder, int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str) -> None
        Order.__init__(self, _id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif, tif_date_time,
                       exchange_order, exchange_id, parent_order_id, security_id, account_id, portfolio_id, last_status)

    @abstractmethod
    def convert_to_order_vo(self, _gateway):
        # type: (ClientServer) -> JavaObject
        pass


class AlgoOrder(Order):
    """Mirrors ch.algotrader.entity.trade.algo.SimpleOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None, routing_candidates=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, Optional[List[RoutingTarget]]) -> None
        Order.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                       side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                       exchange_order=exchange_order, exchange_id=exchange_id,
                       parent_order_id=0,
                       security_id=security_id, account_id=account_id, portfolio_id=portfolio_id, last_status=last_status)
        self.routing_candidates = routing_candidates

    @abstractmethod
    def convert_to_order_vo(self, _gateway):
        pass


class MarketOrder(SimpleOrder):
    """Mirrors ch.algotrader.entity.trade.MarketOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
       """

    @staticmethod
    def get_java_class():
        return "ch.algotrader.entity.trade.MarketOrderVO"

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None):
        # type: (MarketOrder, int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str) -> None
        SimpleOrder.__init__(self, _id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif, tif_date_time,
                             exchange_order, exchange_id, parent_order_id, security_id, account_id, portfolio_id,
                             last_status)

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.MarketOrderVO
        """
        market_order_vo_builder = py4jgateway.jvm.MarketOrderVOBuilder.create()  # java class
        if self.id is not None:
            market_order_vo_builder.setId(self.id)
        market_order_vo_builder.setIntId(self.int_id)
        market_order_vo_builder.setExtId(self.ext_id)
        market_order_vo_builder.setParentIntId(self.parent_int_id)
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        market_order_vo_builder.setDateTime(date_time)
        side = Conversions.convert_to_side_enum(self.side, py4jgateway)
        market_order_vo_builder.setSide(side)
        market_order_vo_builder.setQuantity(self.quantity)
        tif = Conversions.convert_to_tif_enum(self.tif, py4jgateway)
        market_order_vo_builder.setTif(tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        market_order_vo_builder.setTifDateTime(tif_date_time)
        if self.exchange_order is not None:
            market_order_vo_builder.setExchangeOrder(self.exchange_order)
        if self.exchange_id is not None:
            market_order_vo_builder.setExchangeId(self.exchange_id)
        if self.parent_order_id is not None:
            market_order_vo_builder.setParentOrderId(self.parent_order_id)
        if self.security_id is not None:
            market_order_vo_builder.setSecurityId(self.security_id)
        if self.account_id is not None:
            market_order_vo_builder.setAccountId(self.account_id)
        if self.portfolio_id is not None:
            market_order_vo_builder.setPortfolioId(self.portfolio_id)
        if self.last_status is not None:
            market_order_vo_builder.setLastStatus(Conversions.convert_to_status_enum(self.last_status, py4jgateway))
        market_order_vo = market_order_vo_builder.build()
        return market_order_vo

    @staticmethod
    def convert_to_order(market_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> MarketOrder
        """Converts Java value object to a Python order object

           Arguments:
               market_order_vo (ch.algotrader.entity.trade.MarketOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               MarketOrder
        """
        _id = market_order_vo.getId()
        int_id = market_order_vo.getIntId()
        ext_id = market_order_vo.getExtId()
        parent_int_id = market_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(market_order_vo.getDateTime())
        side = None
        if market_order_vo.getSide() is not None:
            side = market_order_vo.getSide().toString()
        quantity = market_order_vo.getQuantity()
        tif = None
        if market_order_vo.getTif() is not None:
            tif = market_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(market_order_vo.getTifDateTime())
        exchange_order = market_order_vo.isExchangeOrder()
        exchange_id = market_order_vo.getExchangeId()
        parent_order_id = market_order_vo.getParentOrderId()
        security_id = market_order_vo.getSecurityId()
        account_id = market_order_vo.getAccountId()
        portfolio_id = market_order_vo.getPortfolioId()
        last_status = None
        if market_order_vo.getLastStatus() is not None:
            last_status = market_order_vo.getLastStatus().toString()
        market_order = MarketOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                   date_time=date_time, side=side, quantity=quantity, tif=tif,
                                   tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                                   parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                                   portfolio_id=portfolio_id, last_status=last_status)
        return market_order

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> MarketOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized MarketOrderVO): &nbsp;
           Returns:
               MarketOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        parent_order_id = vo_dict['parentOrderId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']

        order = MarketOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                            date_time=date_time, side=side, quantity=quantity, tif=tif,
                            tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                            parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                            portfolio_id=portfolio_id, last_status=last_status)
        return order


class LimitOrder(SimpleOrder):
    """Mirrors ch.algotrader.entity.trade.LimitOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           limit (Decimal): The limit price
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None, limit=None):
        # type: (LimitOrder, int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str, Decimal) -> None
        SimpleOrder.__init__(self, _id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif, tif_date_time,
                             exchange_order, exchange_id, parent_order_id, security_id, account_id, portfolio_id,
                             last_status)
        self.limit = limit

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.LimitOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.LimitOrderVO
        """
        limit_order_vo_builder = py4jgateway.jvm.LimitOrderVOBuilder.create()  # java class
        if self.id is not None:
            limit_order_vo_builder.setId(self.id)
        limit_order_vo_builder.setIntId(self.int_id)
        limit_order_vo_builder.setExtId(self.ext_id)
        limit_order_vo_builder.setParentIntId(self.parent_int_id)
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        limit_order_vo_builder.setDateTime(date_time)
        side = Conversions.convert_to_side_enum(self.side, py4jgateway)
        limit_order_vo_builder.setSide(side)
        limit_order_vo_builder.setQuantity(self.quantity)
        tif = Conversions.convert_to_tif_enum(self.tif, py4jgateway)
        limit_order_vo_builder.setTif(tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        limit_order_vo_builder.setTifDateTime(tif_date_time)
        if self.exchange_order is not None:
            limit_order_vo_builder.setExchangeOrder(self.exchange_order)
        if self.exchange_id is not None:
            limit_order_vo_builder.setExchangeId(self.exchange_id)
        if self.parent_order_id is not None:
            limit_order_vo_builder.setParentOrderId(self.parent_order_id)
        if self.security_id is not None:
            limit_order_vo_builder.setSecurityId(self.security_id)
        if self.account_id is not None:
            limit_order_vo_builder.setAccountId(self.account_id)
        if self.portfolio_id is not None:
            limit_order_vo_builder.setPortfolioId(self.portfolio_id)
        if self.last_status is not None:
            limit_order_vo_builder.setLastStatus(Conversions.convert_to_status_enum(self.last_status, py4jgateway))
        limit_order_vo_builder.setLimit(self.limit)
        limit_order_vo = limit_order_vo_builder.build()
        return limit_order_vo

    @staticmethod
    def convert_to_order(limit_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> LimitOrder
        """Converts Java value object to a Python order object

           Arguments:
               limit_order_vo (ch.algotrader.entity.trade.LimitOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               LimitOrder
        """
        _id = limit_order_vo.getId()
        int_id = limit_order_vo.getIntId()
        ext_id = limit_order_vo.getExtId()
        parent_int_id = limit_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(limit_order_vo.getDateTime())
        side = None
        if limit_order_vo.getSide() is not None:
            side = limit_order_vo.getSide().toString()
        quantity = limit_order_vo.getQuantity()
        tif = None
        if limit_order_vo.getTif() is not None:
            tif = limit_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(limit_order_vo.getTifDateTime())
        exchange_order = limit_order_vo.isExchangeOrder()
        exchange_id = limit_order_vo.getExchangeId()
        parent_order_id = limit_order_vo.getParentOrderId()
        security_id = limit_order_vo.getSecurityId()
        account_id = limit_order_vo.getAccountId()
        portfolio_id = limit_order_vo.getPortfolioId()
        limit = limit_order_vo.getLimit()
        last_status = None
        if limit_order_vo.getLastStatus() is not None:
            last_status = limit_order_vo.getLastStatus().toString()
        limit_order = LimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                 date_time=date_time, side=side, quantity=quantity, tif=tif,
                                 tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                                 parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                                 portfolio_id=portfolio_id, limit=limit, last_status=last_status)
        return limit_order

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> LimitOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized LimitOrderVO): &nbsp;
           Returns:
               LimitOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        parent_order_id = vo_dict['parentOrderId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        limit = Conversions.float_to_decimal(vo_dict['limit'])
        limit_order = LimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                 date_time=date_time, side=side, quantity=quantity, tif=tif,
                                 tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                                 parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                                 portfolio_id=portfolio_id, last_status=last_status, limit=limit)
        return limit_order


class StopOrder(SimpleOrder):
    """Mirrors ch.algotrader.entity.trade.StopOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           stop (Decimal): The stop price
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None, stop=None):
        # type: (StopOrder, int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str, Decimal) -> None
        SimpleOrder.__init__(self, _id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif, tif_date_time,
                             exchange_order, exchange_id, parent_order_id, security_id, account_id, portfolio_id,
                             last_status)
        self.stop = stop

    @staticmethod
    def get_java_class():
        return "ch.algotrader.entity.trade.StopOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.StopOrderVO
        """
        stop_order_vo_builder = py4jgateway.jvm.StopOrderVOBuilder.create()  # java class
        if self.id is not None:
            stop_order_vo_builder.setId(self.id)
        stop_order_vo_builder.setIntId(self.int_id)
        stop_order_vo_builder.setExtId(self.ext_id)
        stop_order_vo_builder.setParentIntId(self.parent_int_id)
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        stop_order_vo_builder.setDateTime(date_time)
        side = Conversions.convert_to_side_enum(self.side, py4jgateway)
        stop_order_vo_builder.setSide(side)
        stop_order_vo_builder.setQuantity(self.quantity)
        tif = Conversions.convert_to_tif_enum(self.tif, py4jgateway)
        stop_order_vo_builder.setTif(tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        stop_order_vo_builder.setTifDateTime(tif_date_time)
        if self.exchange_order is not None:
            stop_order_vo_builder.setExchangeOrder(self.exchange_order)
        if self.exchange_id is not None:
            stop_order_vo_builder.setExchangeId(self.exchange_id)
        if self.parent_order_id is not None:
            stop_order_vo_builder.setParentOrderId(self.parent_order_id)
        if self.security_id is not None:
            stop_order_vo_builder.setSecurityId(self.security_id)
        if self.account_id is not None:
            stop_order_vo_builder.setAccountId(self.account_id)
        if self.portfolio_id is not None:
            stop_order_vo_builder.setPortfolioId(self.portfolio_id)
        if self.last_status is not None:
            stop_order_vo_builder.setLastStatus(Conversions.convert_to_status_enum(self.last_status, py4jgateway))
        stop_order_vo_builder.setStop(self.stop)
        stop_order_vo = stop_order_vo_builder.build()
        return stop_order_vo

    @staticmethod
    def convert_to_order(stop_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> StopOrder
        """Converts Java value object to a Python order object

           Arguments:
               stop_order_vo (ch.algotrader.entity.trade.StopOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               StopOrder
        """
        _id = stop_order_vo.getId()
        int_id = stop_order_vo.getIntId()
        ext_id = stop_order_vo.getExtId()
        parent_int_id = stop_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(stop_order_vo.getDateTime())
        side = None
        if stop_order_vo.getSide() is not None:
            side = stop_order_vo.getSide().toString()
        quantity = stop_order_vo.getQuantity()
        tif = None
        if stop_order_vo.getTif() is not None:
            tif = stop_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(stop_order_vo.getTifDateTime())
        exchange_order = stop_order_vo.isExchangeOrder()
        exchange_id = stop_order_vo.getExchangeId()
        parent_order_id = stop_order_vo.getParentOrderId()
        security_id = stop_order_vo.getSecurityId()
        account_id = stop_order_vo.getAccountId()
        portfolio_id = stop_order_vo.getPortfolioId()
        last_status = None
        if stop_order_vo.getLastStatus() is not None:
            last_status = stop_order_vo.getLastStatus().toString()
        stop = stop_order_vo.getStop()
        stop_order = StopOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                               side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                               exchange_order=exchange_order, exchange_id=exchange_id, parent_order_id=parent_order_id,
                               security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                               last_status=last_status, stop=stop)
        return stop_order

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> StopOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized StopOrderVO): &nbsp;
           Returns:
               StopOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        parent_order_id = vo_dict['parentOrderId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        stop = Conversions.float_to_decimal(vo_dict['stop'])
        stop_order = StopOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                               date_time=date_time, side=side, quantity=quantity, tif=tif,
                               tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                               parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                               portfolio_id=portfolio_id, last_status=last_status, stop=stop)
        return stop_order


class StopLimitOrder(SimpleOrder):
    """Mirrors ch.algotrader.entity.trade.StopLimitOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           limit (Decimal): The limit price
           stop (Decimal): The stop price
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None, limit=None, stop=None):
        # type: (StopLimitOrder, int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str, Decimal, Decimal) -> None
        SimpleOrder.__init__(self, _id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif, tif_date_time,
                             exchange_order, exchange_id, parent_order_id, security_id, account_id, portfolio_id,
                             last_status)
        self.limit = limit
        self.stop = stop

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.StopLimitOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.StopLimitOrderVO
        """
        stop_limit_order_vo_builder = py4jgateway.jvm.StopLimitOrderVOBuilder.create()  # java class
        if self.id is not None:
            stop_limit_order_vo_builder.setId(self.id)
        stop_limit_order_vo_builder.setIntId(self.int_id)
        stop_limit_order_vo_builder.setExtId(self.ext_id)
        stop_limit_order_vo_builder.setParentIntId(self.parent_int_id)
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        stop_limit_order_vo_builder.setDateTime(date_time)
        side = Conversions.convert_to_side_enum(self.side, py4jgateway)
        stop_limit_order_vo_builder.setSide(side)
        stop_limit_order_vo_builder.setQuantity(self.quantity)
        tif = Conversions.convert_to_tif_enum(self.tif, py4jgateway)
        stop_limit_order_vo_builder.setTif(tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        stop_limit_order_vo_builder.setTifDateTime(tif_date_time)
        if self.exchange_order is not None:
            stop_limit_order_vo_builder.setExchangeOrder(self.exchange_order)
        if self.exchange_id is not None:
            stop_limit_order_vo_builder.setExchangeId(self.exchange_id)
        if self.parent_order_id is not None:
            stop_limit_order_vo_builder.setParentOrderId(self.parent_order_id)
        if self.security_id is not None:
            stop_limit_order_vo_builder.setSecurityId(self.security_id)
        if self.account_id is not None:
            stop_limit_order_vo_builder.setAccountId(self.account_id)
        if self.portfolio_id is not None:
            stop_limit_order_vo_builder.setPortfolioId(self.portfolio_id)
        if self.last_status is not None:
            stop_limit_order_vo_builder.setLastStatus(Conversions.convert_to_status_enum(self.last_status, py4jgateway))
        stop_limit_order_vo_builder.setLimit(self.limit)
        stop_limit_order_vo_builder.setStop(self.stop)
        stop_order_vo = stop_limit_order_vo_builder.build()
        return stop_order_vo

    @staticmethod
    def convert_to_order(stop_limit_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> StopLimitOrder
        """Converts Java value object to a Python order object

           Arguments:
               stop_limit_order_vo (ch.algotrader.entity.trade.StopLimitOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               StopLimitOrder
        """
        _id = stop_limit_order_vo.getId()
        int_id = stop_limit_order_vo.getIntId()
        ext_id = stop_limit_order_vo.getExtId()
        parent_int_id = stop_limit_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(stop_limit_order_vo.getDateTime())
        side = None
        if stop_limit_order_vo.getSide() is not None:
            side = stop_limit_order_vo.getSide().toString()
        quantity = stop_limit_order_vo.getQuantity()
        tif = None
        if stop_limit_order_vo.getTif() is not None:
            tif = stop_limit_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(stop_limit_order_vo.getTifDateTime())
        exchange_order = stop_limit_order_vo.isExchangeOrder()
        exchange_id = stop_limit_order_vo.getExchangeId()
        parent_order_id = stop_limit_order_vo.getParentOrderId()
        security_id = stop_limit_order_vo.getSecurityId()
        account_id = stop_limit_order_vo.getAccountId()
        portfolio_id = stop_limit_order_vo.getPortfolioId()
        last_status = None
        if stop_limit_order_vo.getLastStatus() is not None:
            last_status = stop_limit_order_vo.getLastStatus().toString()
        limit = stop_limit_order_vo.getLimit()
        stop = stop_limit_order_vo.getStop()
        stop_order = StopLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                    date_time=date_time, side=side, quantity=quantity, tif=tif,
                                    tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                                    parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                                    portfolio_id=portfolio_id, last_status=last_status, limit=limit, stop=stop)
        return stop_order

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> StopLimitOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized StopLimitOrderVO): &nbsp;
           Returns:
               StopLimitOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        parent_order_id = vo_dict['parentOrderId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        stop = Conversions.float_to_decimal(vo_dict['stop'])
        limit = Conversions.float_to_decimal(vo_dict['limit'])
        order = StopLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                               date_time=date_time, side=side, quantity=quantity, tif=tif,
                               tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                               parent_order_id=parent_order_id, security_id=security_id, account_id=account_id,
                               portfolio_id=portfolio_id, last_status=last_status, stop=stop, limit=limit)
        return order


class PreviouslyIndicatedOrder(SimpleOrder):
    """Mirrors ch.algotrader.entity.trade.PreviouslyIndicatedOrderVO AlgoTrader
       Java class with fields using Python types.

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           parent_order_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           quote_id (int): Represents an id of the requested quote.
       """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, parent_order_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None, quote_id=None):
        # type: (PreviouslyIndicatedOrder, int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, int, str, int) -> None
        SimpleOrder.__init__(self, _id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif, tif_date_time,
                             exchange_order, exchange_id, parent_order_id, security_id, account_id, portfolio_id,
                             last_status)
        self.quote_id = quote_id

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.PreviouslyIndicatedOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.PreviouslyIndicatedOrderVO
        """
        previously_indicated_order_vo_builder = py4jgateway.jvm.PreviouslyIndicatedOrderVOBuilder.create()  # java class
        if self.id is not None:
            previously_indicated_order_vo_builder.setId(self.id)
        previously_indicated_order_vo_builder.setIntId(self.int_id)
        previously_indicated_order_vo_builder.setExtId(self.ext_id)
        previously_indicated_order_vo_builder.setParentIntId(self.parent_int_id)
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        previously_indicated_order_vo_builder.setDateTime(date_time)
        side = Conversions.convert_to_side_enum(self.side, py4jgateway)
        previously_indicated_order_vo_builder.setSide(side)
        previously_indicated_order_vo_builder.setQuantity(self.quantity)
        tif = Conversions.convert_to_tif_enum(self.tif, py4jgateway)
        previously_indicated_order_vo_builder.setTif(tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        previously_indicated_order_vo_builder.setTifDateTime(tif_date_time)
        if self.exchange_order is not None:
            previously_indicated_order_vo_builder.setExchangeOrder(self.exchange_order)
        if self.exchange_id is not None:
            previously_indicated_order_vo_builder.setExchangeId(self.exchange_id)
        if self.parent_order_id is not None:
            previously_indicated_order_vo_builder.setParentOrderId(self.parent_order_id)
        if self.security_id is not None:
            previously_indicated_order_vo_builder.setSecurityId(self.security_id)
        if self.account_id is not None:
            previously_indicated_order_vo_builder.setAccountId(self.account_id)
        if self.portfolio_id is not None:
            previously_indicated_order_vo_builder.setPortfolioId(self.portfolio_id)
        if self.last_status is not None:
            previously_indicated_order_vo_builder \
                .setLastStatus(Conversions.convert_to_status_enum(self.last_status, py4jgateway))
        previously_indicated_order_vo_builder.setQuoteId(self.quote_id)
        previously_indicated_vo = previously_indicated_order_vo_builder.build()
        return previously_indicated_vo

    @staticmethod
    def convert_to_order(previously_indicated_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> PreviouslyIndicatedOrder
        """Converts Java value object to a Python order object

           Arguments:
               previously_indicated_order_vo (ch.algotrader.entity.trade.PreviouslyIndicatedOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               PreviouslyIndicatedOrder
        """
        _id = previously_indicated_order_vo.getId()
        int_id = previously_indicated_order_vo.getIntId()
        ext_id = previously_indicated_order_vo.getExtId()
        parent_int_id = previously_indicated_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(previously_indicated_order_vo.getDateTime())
        side = None
        if previously_indicated_order_vo.getSide() is not None:
            side = previously_indicated_order_vo.getSide().toString()
        quantity = previously_indicated_order_vo.getQuantity()
        tif = None
        if previously_indicated_order_vo.getTif() is not None:
            tif = previously_indicated_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(previously_indicated_order_vo.getTifDateTime())
        exchange_order = previously_indicated_order_vo.isExchangeOrder()
        exchange_id = previously_indicated_order_vo.getExchangeId()
        parent_order_id = previously_indicated_order_vo.getParentOrderId()
        security_id = previously_indicated_order_vo.getSecurityId()
        account_id = previously_indicated_order_vo.getAccountId()
        portfolio_id = previously_indicated_order_vo.getPortfolioId()
        last_status = None
        if previously_indicated_order_vo.getLastStatus() is not None:
            last_status = previously_indicated_order_vo.getLastStatus().toString()
        quote_id = previously_indicated_order_vo.getQuoteId()
        previously_indicated = PreviouslyIndicatedOrder(_id=_id, int_id=int_id, ext_id=ext_id,
                                                        parent_int_id=parent_int_id,
                                                        date_time=date_time, side=side, quantity=quantity, tif=tif,
                                                        tif_date_time=tif_date_time, exchange_order=exchange_order,
                                                        exchange_id=exchange_id,
                                                        parent_order_id=parent_order_id, security_id=security_id,
                                                        account_id=account_id,
                                                        portfolio_id=portfolio_id, last_status=last_status,
                                                        quote_id=quote_id)
        return previously_indicated

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> PreviouslyIndicatedOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized PreviouslyIndicatedOrderVO): &nbsp;
           Returns:
               PreviouslyIndicatedOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        parent_order_id = vo_dict['parentOrderId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        quote_id = vo_dict['quoteId']
        order = PreviouslyIndicatedOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                         date_time=date_time, side=side, quantity=quantity, tif=tif,
                                         tif_date_time=tif_date_time, exchange_order=exchange_order,
                                         exchange_id=exchange_id,
                                         parent_order_id=parent_order_id, security_id=security_id,
                                         account_id=account_id,
                                         portfolio_id=portfolio_id, last_status=last_status, quote_id=quote_id)
        return order


class TrailingLimitOrder(AlgoOrder):
    """Mirrors TrailingLimitOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           trailing_amount (Decimal): For a BUY (SELL) order the limit price will be set by this amount below (above) the current market price.
           increment (Decimal): For BUY orders (SELL orders) in case the market price rises (falls), the limit price is increased once it exceeds this amount
    """

    # this constructor is the same as TrailingLimitOrderVO constructor, no parent_order_id, no routing_candidates
    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None, trailing_amount=None,
                 increment=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, Decimal, Decimal) -> None
        # noinspection PyArgumentEqualDefault
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=None)
        self.trailing_amount = trailing_amount
        self.increment = increment

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.TrailingLimitOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.TrailingLimitOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        trailing_amount = self.trailing_amount
        increment = self.increment
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)

        vo = py4jgateway.jvm.TrailingLimitOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                                  tif, tif_date_time, exchange_order, exchange_id, security_id,
                                                  account_id, portfolio_id, trailing_amount, increment, last_status)
        return vo

    @staticmethod
    def convert_to_order(trailing_limit_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> TrailingLimitOrder
        """Converts Java value object to a Python order object

           Arguments:
               trailing_limit_order_vo (ch.algotrader.entity.trade.algo.TrailingLimitOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               TrailingLimitOrder
        """
        _id = trailing_limit_order_vo.getId()
        int_id = trailing_limit_order_vo.getIntId()
        ext_id = trailing_limit_order_vo.getExtId()
        parent_int_id = trailing_limit_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(trailing_limit_order_vo.getDateTime())
        side = None
        if trailing_limit_order_vo.getSide() is not None:
            side = trailing_limit_order_vo.getSide().toString()
        quantity = trailing_limit_order_vo.getQuantity()
        tif = None
        if trailing_limit_order_vo.getTif() is not None:
            tif = trailing_limit_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(trailing_limit_order_vo.getTifDateTime())
        exchange_order = trailing_limit_order_vo.isExchangeOrder()
        exchange_id = trailing_limit_order_vo.getExchangeId()
        security_id = trailing_limit_order_vo.getSecurityId()
        account_id = trailing_limit_order_vo.getAccountId()
        portfolio_id = trailing_limit_order_vo.getPortfolioId()
        last_status = None
        if trailing_limit_order_vo.getLastStatus() is not None:
            last_status = trailing_limit_order_vo.getLastStatus().toString()
        trailing_amount = trailing_limit_order_vo.getTrailingAmount()
        increment = trailing_limit_order_vo.getIncrement()
        to = TrailingLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                                side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                                exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                                account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                                trailing_amount=trailing_amount, increment=increment)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> TrailingLimitOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized TrailingLimitOrderVO): &nbsp;
           Returns:
               TrailingLimitOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        trailing_amount = Conversions.float_to_decimal(vo_dict['trailingAmount'])
        increment = Conversions.float_to_decimal(vo_dict['increment'])
        to = TrailingLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                                side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                                exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                                account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                                trailing_amount=trailing_amount, increment=increment)
        return to
    # TrailingLimitOrder end


class TargetPositionOrder(AlgoOrder):
    """Mirrors TargetPositionOrderVO Java class
    
       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           keep_alive (bool): When true the order will remain active until explicitly canceled
           target (Decimal): &nbsp;
    """

    # this constructor is the same as TargetPositionOrderVO constructor, no parent_order_id,
    #  routing_candidates set to null/None
    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None,
                 keep_alive=None, target=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, bool, Decimal) -> None
        # noinspection PyArgumentEqualDefault
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=None)
        self.keep_alive = keep_alive
        self.target = target

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.TargetPositionOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.TargetPositionOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        keep_alive = self.keep_alive  # Boolean on Java side
        target = self.target

        vo = py4jgateway.jvm.TargetPositionOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                                   tif, tif_date_time, exchange_order, exchange_id, security_id,
                                                   account_id, portfolio_id, keep_alive, target, last_status)
        return vo

    @staticmethod
    def convert_to_order(target_position_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> TargetPositionOrder
        """Converts Java value object to a Python order object

           Arguments:
               target_position_order_vo (ch.algotrader.entity.trade.algo.TargetPositionOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               TargetPositionOrder
        """
        _id = target_position_order_vo.getId()
        int_id = target_position_order_vo.getIntId()
        ext_id = target_position_order_vo.getExtId()
        parent_int_id = target_position_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(target_position_order_vo.getDateTime())
        side = None
        if target_position_order_vo.getSide() is not None:
            side = target_position_order_vo.getSide().toString()
        quantity = target_position_order_vo.getQuantity()
        tif = None
        if target_position_order_vo.getTif() is not None:
            tif = target_position_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(target_position_order_vo.getTifDateTime())
        exchange_order = target_position_order_vo.isExchangeOrder()
        exchange_id = target_position_order_vo.getExchangeId()
        security_id = target_position_order_vo.getSecurityId()
        account_id = target_position_order_vo.getAccountId()
        portfolio_id = target_position_order_vo.getPortfolioId()
        last_status = None
        if target_position_order_vo.getLastStatus() is not None:
            last_status = target_position_order_vo.getLastStatus().toString()
        keep_alive = target_position_order_vo.getKeepAlive()
        target = target_position_order_vo.getTarget()

        to = TargetPositionOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                 date_time=date_time, side=side, quantity=quantity, tif=tif,
                                 tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                                 security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                                 last_status=last_status,
                                 keep_alive=keep_alive, target=target)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> TargetPositionOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized TargetPositionOrderVO): &nbsp;
           Returns:
               TargetPositionOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        keep_alive = vo_dict['keepAlive']
        target = Conversions.float_to_decimal(vo_dict['target'])
        to = TargetPositionOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                                 date_time=date_time, side=side, quantity=quantity, tif=tif,
                                 tif_date_time=tif_date_time, exchange_order=exchange_order, exchange_id=exchange_id,
                                 security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                                 last_status=last_status,
                                 keep_alive=keep_alive, target=target)
        return to
    # TargetPositionOrder end


class AdaptiveOrder(AlgoOrder):
    """Mirrors AdaptiveOrderVO Java class
    
       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           start_time (datetime): The start time when the algo should start
           end_time (datetime): The end time by when the algo should be finished (alternatively duration can be specified)
           duration (int): The duration of the algo in seconds (alternatively end time can be specified)
           min_slice_qty (Decimal): The minimum quantity of each child order, default is 0
           max_vol_pct (float): The maximum fraction (0.0 to 1.0) of current bid/ask volume a child order should take, default is 1.0
           slice_length (int): The length of each slice (child order) in seconds
           cancel_time (float): The time (0.0 to 1.0 of sliceLength) to cancel a child order
           time_rand (float): The time randomization (0.0 to 1.0) of sliceLength and cancelTime, default is 0
           qty_rand (float): The quantity randomization (0.0 to 1.0) of sliceQty, default is 0
           increment (float): The increment/decrement (0.0 to 1.0)
           initial_offset (float): The initial offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           min_offset (float): The minimum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           max_offset (float): The maximum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None,
                 routing_candidates=None,
                 start_time=None, end_time=None, duration=None, min_slice_qty=None, max_vol_pct=None, slice_length=None,
                 cancel_time=None, time_rand=None, qty_rand=None, increment=None, initial_offset=None, min_offset=None,
                 max_offset=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, List[RoutingTarget], datetime, datetime, int, Decimal, float, int, float, float, float, float, float, float, float) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status,
                           routing_candidates=routing_candidates)
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.min_slice_qty = min_slice_qty
        self.max_vol_pct = max_vol_pct
        self.slice_length = slice_length
        self.cancel_time = cancel_time
        self.time_rand = time_rand
        self.qty_rand = qty_rand
        self.increment = increment
        self.initial_offset = initial_offset
        self.min_offset = min_offset
        self.max_offset = max_offset

    @abstractmethod
    def convert_to_order_vo(self, _gateway):
        # type: (ClientServer) -> JavaObject
        pass


class TWAPOrder(AdaptiveOrder):
    """Mirrors TWAPOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           start_time (datetime): The start time when the algo should start
           end_time (datetime): The end time by when the algo should be finished (alternatively duration can be specified)
           duration (int): The duration of the algo in seconds (alternatively end time can be specified)
           min_slice_qty (Decimal): The minimum quantity of each child order, default is 0
           max_vol_pct (float): The maximum fraction (0.0 to 1.0) of current bid/ask volume a child order should take, default is 1.0
           slice_length (int): The length of each slice (child order) in seconds
           cancel_time (float): The time (0.0 to 1.0 of sliceLength) to cancel a child order
           time_rand (float): The time randomization (0.0 to 1.0) of sliceLength and cancelTime, default is 0
           qty_rand (float): The quantity randomization (0.0 to 1.0) of sliceQty, default is 0
           increment (float): The increment/decrement (0.0 to 1.0)
           initial_offset (float): The initial offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           min_offset (float): The minimum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           max_offset (float): The maximum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           limit (Optional[Decimal]): Limit price
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None,
                 routing_candidates=None,
                 start_time=None, end_time=None, duration=None, min_slice_qty=None, max_vol_pct=None, slice_length=None,
                 cancel_time=None, time_rand=None, qty_rand=None, increment=None, initial_offset=None, min_offset=None,
                 max_offset=None, limit=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, List[RoutingTarget], datetime, datetime, int, Decimal, float, int, float, float, float, float, float, float, float, Decimal) -> None
        AdaptiveOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                               date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                               exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                               account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                               routing_candidates=routing_candidates,
                               start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=min_slice_qty,
                               max_vol_pct=max_vol_pct, slice_length=slice_length, cancel_time=cancel_time,
                               time_rand=time_rand, qty_rand=qty_rand, increment=increment,
                               initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset)
        self.limit = limit

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.TWAPOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.TWAPOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)

        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)
        start_time = Conversions.python_datetime_to_zoneddatetime(self.start_time, py4jgateway)
        end_time = Conversions.python_datetime_to_zoneddatetime(self.end_time, py4jgateway)
        duration = self.duration
        min_slice_qty = self.min_slice_qty
        max_vol_pct = self.max_vol_pct
        slice_length = self.slice_length
        cancel_time = self.cancel_time
        time_rand = self.time_rand
        qty_rand = self.qty_rand
        increment = self.increment
        initial_offset = self.initial_offset
        min_offset = self.min_offset
        max_offset = self.max_offset
        limit = self.limit

        vo = py4jgateway.jvm.TWAPOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                         tif, tif_date_time, exchange_order, exchange_id, security_id,
                                         account_id, portfolio_id, routing_candidates, start_time,
                                         end_time,
                                         duration, min_slice_qty, max_vol_pct, slice_length, cancel_time,
                                         time_rand, qty_rand, increment, initial_offset, min_offset, max_offset,
                                         last_status, limit)
        return vo

    @staticmethod
    def convert_to_order(twap_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> TWAPOrder
        """Converts Java value object to a Python order object

           Arguments:
               twap_order_vo (ch.algotrader.entity.trade.algo.TWAPOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               TWAPOrder
        """
        _id = twap_order_vo.getId()
        int_id = twap_order_vo.getIntId()
        ext_id = twap_order_vo.getExtId()
        parent_int_id = twap_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(twap_order_vo.getDateTime())
        side = None
        if twap_order_vo.getSide() is not None:
            side = twap_order_vo.getSide().toString()
        quantity = twap_order_vo.getQuantity()
        tif = None
        if twap_order_vo.getTif() is not None:
            tif = twap_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(twap_order_vo.getTifDateTime())
        exchange_order = twap_order_vo.isExchangeOrder()
        exchange_id = twap_order_vo.getExchangeId()
        security_id = twap_order_vo.getSecurityId()
        account_id = twap_order_vo.getAccountId()
        portfolio_id = twap_order_vo.getPortfolioId()
        last_status = None
        if twap_order_vo.getLastStatus() is not None:
            last_status = twap_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in twap_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)
        start_time = Conversions \
            .zoned_date_time_to_python_datetime(twap_order_vo.getStartTime())
        end_time = Conversions.zoned_date_time_to_python_datetime(twap_order_vo.getEndTime())
        duration = twap_order_vo.getDuration()
        min_slice_qty = twap_order_vo.getMinSliceQty()
        max_vol_pct = twap_order_vo.getMaxVolPct()
        slice_length = twap_order_vo.getSliceLength()
        cancel_time = twap_order_vo.getCancelTime()
        time_rand = twap_order_vo.getTimeRand()
        qty_rand = twap_order_vo.getQtyRand()
        increment = twap_order_vo.getIncrement()
        initial_offset = twap_order_vo.getInitialOffset()
        min_offset = twap_order_vo.getMinOffset()
        max_offset = twap_order_vo.getMaxOffset()
        limit = twap_order_vo.getLimit()

        to = TWAPOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                       date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                       exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                       account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                       routing_candidates=routing_candidates,
                       start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=min_slice_qty,
                       max_vol_pct=max_vol_pct, slice_length=slice_length, cancel_time=cancel_time,
                       time_rand=time_rand, qty_rand=qty_rand, increment=increment,
                       initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset, limit=limit)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> TWAPOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized TWAPOrderVO): &nbsp;
           Returns:
               TWAPOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)
        start_time = Conversions.epoch_millis_to_python_datetime(vo_dict['startTime'])
        end_time = Conversions.epoch_millis_to_python_datetime(vo_dict['endTime'])
        duration = vo_dict['duration']
        min_slice_qty = Conversions.float_to_decimal(vo_dict['minSliceQty'])
        max_vol_pct = vo_dict['maxVolPct']
        slice_length = vo_dict['sliceLength']
        cancel_time = vo_dict['cancelTime']
        time_rand = vo_dict['timeRand']
        qty_rand = vo_dict['qtyRand']
        increment = vo_dict['increment']
        initial_offset = vo_dict['initialOffset']
        min_offset = vo_dict['minOffset']
        max_offset = vo_dict['maxOffset']
        limit = vo_dict['limit']

        to = TWAPOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                       date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                       exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                       account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                       routing_candidates=routing_candidates,
                       start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=min_slice_qty,
                       max_vol_pct=max_vol_pct, slice_length=slice_length, cancel_time=cancel_time,
                       time_rand=time_rand, qty_rand=qty_rand, increment=increment,
                       initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset, limit=limit)
        return to
    # TWAPOrder end


class VWAPOrder(AdaptiveOrder):
    """Mirrors VWAPOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           start_time (datetime): The start time when the algo should start
           end_time (datetime): The end time by when the algo should be finished (alternatively duration can be specified)
           duration (int): The duration of the algo in seconds (alternatively end time can be specified)
           min_slice_qty (Decimal): The minimum quantity of each child order, default is 0
           max_vol_pct (float): The maximum fraction (0.0 to 1.0) of current bid/ask volume a child order should take, default is 1.0
           slice_length (int): The length of each slice (child order) in seconds
           cancel_time (float): The time (0.0 to 1.0 of sliceLength) to cancel a child order
           time_rand (float): The time randomization (0.0 to 1.0) of sliceLength and cancelTime, default is 0
           qty_rand (float): The quantity randomization (0.0 to 1.0) of sliceQty, default is 0
           increment (float): The increment/decrement (0.0 to 1.0)
           initial_offset (float): The initial offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           min_offset (float): The minimum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           max_offset (float): The maximum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           bucket_size (str): Size of each historical volume bucket (e.g. MIN_15)
           lookback_period (int): Look back period in days
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None,
                 routing_candidates=None,
                 start_time=None, end_time=None, duration=None, min_slice_qty=None, max_vol_pct=None, slice_length=None,
                 cancel_time=None, time_rand=None, qty_rand=None, increment=None, initial_offset=None, min_offset=None,
                 max_offset=None, bucket_size=None, lookback_period=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, List[RoutingTarget], datetime, datetime, int, Decimal, float, int, float, float, float, float, float, float, float, str, int) -> None
        AdaptiveOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                               date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                               exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                               account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                               routing_candidates=routing_candidates,
                               start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=min_slice_qty,
                               max_vol_pct=max_vol_pct, slice_length=slice_length, cancel_time=cancel_time,
                               time_rand=time_rand, qty_rand=qty_rand, increment=increment,
                               initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset)
        self.bucket_size = bucket_size
        self.lookback_period = lookback_period

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.VWAPOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.VWAPOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)
        start_time = Conversions.python_datetime_to_zoneddatetime(self.start_time, py4jgateway)
        end_time = Conversions.python_datetime_to_zoneddatetime(self.end_time, py4jgateway)
        duration = self.duration
        min_slice_qty = self.min_slice_qty
        max_vol_pct = self.max_vol_pct
        slice_length = self.slice_length
        cancel_time = self.cancel_time
        time_rand = self.time_rand
        qty_rand = self.qty_rand
        increment = self.increment
        initial_offset = self.initial_offset
        min_offset = self.min_offset
        max_offset = self.max_offset
        bucket_size = None
        if self.bucket_size is not None:
            bucket_size = py4jgateway.jvm.Duration.valueOf(self.bucket_size)
        lookback_period = self.lookback_period

        vo = py4jgateway.jvm.VWAPOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                         tif, tif_date_time, exchange_order, exchange_id, security_id,
                                         account_id, portfolio_id, routing_candidates, start_time,
                                         end_time,
                                         duration, min_slice_qty, max_vol_pct, slice_length, cancel_time,
                                         time_rand, qty_rand, increment, initial_offset, min_offset, max_offset,
                                         bucket_size, lookback_period, last_status)
        return vo

    @staticmethod
    def convert_to_order(vwap_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> VWAPOrder
        """Converts Java value object to a Python order object

           Arguments:
               vwap_order_vo (ch.algotrader.entity.trade.algo.VWAPOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               VWAPOrder
        """
        _id = vwap_order_vo.getId()
        int_id = vwap_order_vo.getIntId()
        ext_id = vwap_order_vo.getExtId()
        parent_int_id = vwap_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(vwap_order_vo.getDateTime())
        side = None
        if vwap_order_vo.getSide() is not None:
            side = vwap_order_vo.getSide().toString()
        quantity = vwap_order_vo.getQuantity()
        tif = None
        if vwap_order_vo.getTif() is not None:
            tif = vwap_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(vwap_order_vo.getTifDateTime())
        exchange_order = vwap_order_vo.isExchangeOrder()
        exchange_id = vwap_order_vo.getExchangeId()
        security_id = vwap_order_vo.getSecurityId()
        account_id = vwap_order_vo.getAccountId()
        portfolio_id = vwap_order_vo.getPortfolioId()
        last_status = None
        if vwap_order_vo.getLastStatus() is not None:
            last_status = vwap_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in vwap_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)
        start_time = Conversions \
            .zoned_date_time_to_python_datetime(vwap_order_vo.getStartTime())
        end_time = Conversions.zoned_date_time_to_python_datetime(vwap_order_vo.getEndTime())
        duration = vwap_order_vo.getDuration()
        min_slice_qty = vwap_order_vo.getMinSliceQty()
        max_vol_pct = vwap_order_vo.getMaxVolPct()
        slice_length = vwap_order_vo.getSliceLength()
        cancel_time = vwap_order_vo.getCancelTime()
        time_rand = vwap_order_vo.getTimeRand()
        qty_rand = vwap_order_vo.getQtyRand()
        increment = vwap_order_vo.getIncrement()
        initial_offset = vwap_order_vo.getInitialOffset()
        min_offset = vwap_order_vo.getMinOffset()
        max_offset = vwap_order_vo.getMaxOffset()
        bucket_size = None
        if vwap_order_vo.getBucketSize() is not None:
            bucket_size = vwap_order_vo.getBucketSize().toString()
        lookback_period = vwap_order_vo.getLookbackPeriod()

        to = VWAPOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                       date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                       exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                       account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                       routing_candidates=routing_candidates,
                       start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=min_slice_qty,
                       max_vol_pct=max_vol_pct, slice_length=slice_length, cancel_time=cancel_time,
                       time_rand=time_rand, qty_rand=qty_rand, increment=increment,
                       initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset,
                       bucket_size=bucket_size, lookback_period=lookback_period)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> VWAPOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized VWAPOrderVO): &nbsp;
           Returns:
               VWAPOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)
        start_time = Conversions.epoch_millis_to_python_datetime(vo_dict['startTime'])
        end_time = Conversions.epoch_millis_to_python_datetime(vo_dict['endTime'])
        duration = vo_dict['duration']
        min_slice_qty = Conversions.float_to_decimal(vo_dict['minSliceQty'])
        max_vol_pct = vo_dict['maxVolPct']
        slice_length = vo_dict['sliceLength']
        cancel_time = vo_dict['cancelTime']
        time_rand = vo_dict['timeRand']
        qty_rand = vo_dict['qtyRand']
        increment = vo_dict['increment']
        initial_offset = vo_dict['initialOffset']
        min_offset = vo_dict['minOffset']
        max_offset = vo_dict['maxOffset']
        bucket_size = vo_dict['bucketSize']
        lookback_period = vo_dict['lookbackPeriod']

        to = VWAPOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                       date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                       exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                       account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                       routing_candidates=routing_candidates,
                       start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=min_slice_qty,
                       max_vol_pct=max_vol_pct, slice_length=slice_length, cancel_time=cancel_time,
                       time_rand=time_rand, qty_rand=qty_rand, increment=increment,
                       initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset,
                       bucket_size=bucket_size, lookback_period=lookback_period)
        return to
    # VWAPOrder end


class OrderDetails:
    """Mirrors PythonOrderDetailsVO Java class.

       Attributes:
           order (Order): &nbsp;
           order_status (algotrader_com.domain.entity.OrderStatus): &nbsp;
       """

    def __init__(self, order, order_status):
        # type: (Order, OrderStatus) -> None
        self.order = order
        self.order_status = order_status

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> OrderDetails
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized PythonOrderDetailsVO): &nbsp;
           Returns:
               OrderDetails
        """
        order_dict = vo_dict[0]
        status_dict = vo_dict[1]
        order = Order.convert_from_json_object(order_dict)
        status = OrderStatus.convert_from_json(status_dict)
        return OrderDetails(order, status)


class SniperOrder(AlgoOrder):
    """Mirrors SniperOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           limit (Decimal): Limit price
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, routing_candidates=None, last_status=None,
                 limit=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str, Decimal) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)
        self.limit = limit

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.SniperOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.SniperOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)
        limit = self.limit

        vo = py4jgateway.jvm.SniperOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                           tif, tif_date_time, exchange_order, exchange_id, security_id,
                                           account_id, portfolio_id, routing_candidates, last_status, limit)
        return vo

    @staticmethod
    def convert_to_order(sniper_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> SniperOrder
        """Converts Java value object to a Python order object

           Arguments:
               sniper_order_vo (ch.algotrader.entity.trade.algo.SniperOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               SniperOrder
        """
        _id = sniper_order_vo.getId()
        int_id = sniper_order_vo.getIntId()
        ext_id = sniper_order_vo.getExtId()
        parent_int_id = sniper_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(sniper_order_vo.getDateTime())
        side = None
        if sniper_order_vo.getSide() is not None:
            side = sniper_order_vo.getSide().toString()
        quantity = sniper_order_vo.getQuantity()
        tif = None
        if sniper_order_vo.getTif() is not None:
            tif = sniper_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(sniper_order_vo.getTifDateTime())
        exchange_order = sniper_order_vo.isExchangeOrder()
        exchange_id = sniper_order_vo.getExchangeId()
        security_id = sniper_order_vo.getSecurityId()
        account_id = sniper_order_vo.getAccountId()
        portfolio_id = sniper_order_vo.getPortfolioId()
        last_status = None
        if sniper_order_vo.getLastStatus() is not None:
            last_status = sniper_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in sniper_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        limit = sniper_order_vo.getLimit()

        to = SniperOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                         side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                         exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                         account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                         last_status=last_status, limit=limit)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> SniperOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized SniperOrderVO): &nbsp;
           Returns:
               SniperOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        limit = Conversions.float_to_decimal(vo_dict['limit'])

        to = SniperOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                         side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                         exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                         account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                         last_status=last_status, limit=limit)
        return to
    # SniperOrder end


class SmartStopOrder(AlgoOrder):
    """Mirrors SmartStopOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           stop (Decimal): Stop price
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, routing_candidates=None, last_status=None,
                 stop=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str, Decimal) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)
        self.stop = stop

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.SmartStopOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.SmartStopOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)

        stop = self.stop

        vo = py4jgateway.jvm.SmartStopOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                              tif, tif_date_time, exchange_order, exchange_id, security_id,
                                              account_id, portfolio_id, routing_candidates, last_status, stop)
        return vo

    @staticmethod
    def convert_to_order(smart_stop_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> SmartStopOrder
        """Converts Java value object to a Python order object

           Arguments:
               smart_stop_order_vo (ch.algotrader.entity.trade.algo.SmartStopOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               SmartStopOrder
        """
        _id = smart_stop_order_vo.getId()
        int_id = smart_stop_order_vo.getIntId()
        ext_id = smart_stop_order_vo.getExtId()
        parent_int_id = smart_stop_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(smart_stop_order_vo.getDateTime())
        side = None
        if smart_stop_order_vo.getSide() is not None:
            side = smart_stop_order_vo.getSide().toString()
        quantity = smart_stop_order_vo.getQuantity()
        tif = None
        if smart_stop_order_vo.getTif() is not None:
            tif = smart_stop_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(smart_stop_order_vo.getTifDateTime())
        exchange_order = smart_stop_order_vo.isExchangeOrder()
        exchange_id = smart_stop_order_vo.getExchangeId()
        security_id = smart_stop_order_vo.getSecurityId()
        account_id = smart_stop_order_vo.getAccountId()
        portfolio_id = smart_stop_order_vo.getPortfolioId()
        last_status = None
        if smart_stop_order_vo.getLastStatus() is not None:
            last_status = smart_stop_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in smart_stop_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        stop = smart_stop_order_vo.getStop()

        to = SmartStopOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                            side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                            exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                            account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                            last_status=last_status, stop=stop)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> SmartStopOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized SmartStopOrderVO): &nbsp;
           Returns:
               SmartStopOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        stop = Conversions.float_to_decimal(vo_dict['stop'])

        to = SmartStopOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                            side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                            exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                            account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                            last_status=last_status, stop=stop)
        return to
    # SmartStopOrder end


class MarketSweepOrder(AlgoOrder):
    """Mirrors MarketSweepOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           limit (Decimal): Limit price, if empty market orders will be used
           ensure_complete_fill (bool): Limit price, if empty market orders will be used
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, routing_candidates=None, last_status=None,
                 limit=None, ensure_complete_fill=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str, Decimal, bool) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)
        self.limit = limit
        self.ensure_complete_fill = ensure_complete_fill

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.MarketSweepOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.MarketSweepOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)

        limit = self.limit
        ensure_complete_fill = self.ensure_complete_fill

        vo = py4jgateway.jvm.MarketSweepOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                                tif, tif_date_time, exchange_order, exchange_id, security_id,
                                                account_id, portfolio_id, routing_candidates, last_status, limit,
                                                ensure_complete_fill)
        return vo

    @staticmethod
    def convert_to_order(market_sweep_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> MarketSweepOrder
        """Converts Java value object to a Python order object

           Arguments:
               market_sweep_order_vo (ch.algotrader.entity.trade.algo.MarketSweepOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               MarketSweepOrder
        """
        _id = market_sweep_order_vo.getId()
        int_id = market_sweep_order_vo.getIntId()
        ext_id = market_sweep_order_vo.getExtId()
        parent_int_id = market_sweep_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(market_sweep_order_vo.getDateTime())
        side = None
        if market_sweep_order_vo.getSide() is not None:
            side = market_sweep_order_vo.getSide().toString()
        quantity = market_sweep_order_vo.getQuantity()
        tif = None
        if market_sweep_order_vo.getTif() is not None:
            tif = market_sweep_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(market_sweep_order_vo.getTifDateTime())
        exchange_order = market_sweep_order_vo.isExchangeOrder()
        exchange_id = market_sweep_order_vo.getExchangeId()
        security_id = market_sweep_order_vo.getSecurityId()
        account_id = market_sweep_order_vo.getAccountId()
        portfolio_id = market_sweep_order_vo.getPortfolioId()
        last_status = None
        if market_sweep_order_vo.getLastStatus() is not None:
            last_status = market_sweep_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in market_sweep_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        limit = market_sweep_order_vo.getLimit()
        ensure_complete_fill = market_sweep_order_vo.isEnsureCompleteFill()

        to = MarketSweepOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                              side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                              exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                              account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                              last_status=last_status, limit=limit, ensure_complete_fill=ensure_complete_fill)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> MarketSweepOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized MarketSweepOrderVO): &nbsp;
           Returns:
               MarketSweepOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        limit = Conversions.float_to_decimal(vo_dict['limit'])
        ensure_complete_fill = vo_dict['ensureCompleteFill']

        to = MarketSweepOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                              side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                              exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                              account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                              last_status=last_status, limit=limit, ensure_complete_fill=ensure_complete_fill)
        return to
    # MarketSweepOrder end


class SmartLimitOrder(AlgoOrder):
    """Mirrors SmartLimitOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           limit (Decimal): Limit price, if empty market orders will be used
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, routing_candidates=None, last_status=None,
                 limit=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str, Decimal) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)
        self.limit = limit

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.SmartLimitOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.SmartLimitOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)

        limit = self.limit

        vo = py4jgateway.jvm.SmartLimitOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                               tif, tif_date_time, exchange_order, exchange_id, security_id,
                                               account_id, portfolio_id, routing_candidates, last_status, limit)
        return vo

    @staticmethod
    def convert_to_order(smart_limit_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> SmartLimitOrder
        """Converts Java value object to a Python order object

           Arguments:
               smart_limit_order_vo (ch.algotrader.entity.trade.algo.SmartLimitOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               SmartLimitOrder
        """
        _id = smart_limit_order_vo.getId()
        int_id = smart_limit_order_vo.getIntId()
        ext_id = smart_limit_order_vo.getExtId()
        parent_int_id = smart_limit_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(smart_limit_order_vo.getDateTime())
        side = None
        if smart_limit_order_vo.getSide() is not None:
            side = smart_limit_order_vo.getSide().toString()
        quantity = smart_limit_order_vo.getQuantity()
        tif = None
        if smart_limit_order_vo.getTif() is not None:
            tif = smart_limit_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(smart_limit_order_vo.getTifDateTime())
        exchange_order = smart_limit_order_vo.isExchangeOrder()
        exchange_id = smart_limit_order_vo.getExchangeId()
        security_id = smart_limit_order_vo.getSecurityId()
        account_id = smart_limit_order_vo.getAccountId()
        portfolio_id = smart_limit_order_vo.getPortfolioId()
        last_status = None
        if smart_limit_order_vo.getLastStatus() is not None:
            last_status = smart_limit_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in smart_limit_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        limit = smart_limit_order_vo.getLimit()

        to = SmartLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                             side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                             exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                             account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                             last_status=last_status, limit=limit)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> SmartLimitOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized SmartLimitOrderVO): &nbsp;
           Returns:
               SmartLimitOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        limit = Conversions.float_to_decimal(vo_dict['limit'])

        to = SmartLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                              side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                              exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                              account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                              last_status=last_status, limit=limit)
        return to
    # SmartLimitOrder end


class POVOrder(AdaptiveOrder):
    """Mirrors POVOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           start_time (datetime): The start time when the algo should start
           end_time (datetime): The end time by when the algo should be finished (alternatively duration can be specified)
           duration (int): The duration of the algo in seconds (alternatively end time can be specified)
           slice_length (int): The length of each slice (child order) in seconds
           cancel_time (float): The time (0.0 to 1.0 of sliceLength) to cancel a child order
           time_rand (float): The time randomization (0.0 to 1.0) of sliceLength and cancelTime, default is 0
           increment (float): The increment/decrement (0.0 to 1.0)
           initial_offset (float): The initial offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           min_offset (float): The minimum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           max_offset (float): The maximum offset (0.0 to 1.0). for BUY  orders initial offset = 0 means Bid. for SELL orders initial offset = 0 means Ask
           volume_participation (float): The volume participation (0.0 to 1.0) of last interval volume
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, last_status=None,
                 routing_candidates=None,
                 start_time=None, end_time=None, duration=None, slice_length=None,
                 cancel_time=None, time_rand=None, increment=None, initial_offset=None, min_offset=None,
                 max_offset=None, volume_participation=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, str, List[RoutingTarget], datetime, datetime, int, int, float, float, float, float, float, float, float) -> None
        AdaptiveOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                               date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                               exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                               account_id=account_id, portfolio_id=portfolio_id, last_status=last_status,
                               routing_candidates=routing_candidates,
                               start_time=start_time, end_time=end_time, duration=duration, min_slice_qty=Decimal(0),
                               max_vol_pct=100, slice_length=slice_length, cancel_time=cancel_time,
                               time_rand=time_rand, qty_rand=0, increment=increment,
                               initial_offset=initial_offset, min_offset=min_offset, max_offset=max_offset)

        self.volume_participation = volume_participation

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.POVOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.POVOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)

        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)
        start_time = Conversions.python_datetime_to_zoneddatetime(self.start_time, py4jgateway)
        end_time = Conversions.python_datetime_to_zoneddatetime(self.end_time, py4jgateway)
        duration = self.duration
        slice_length = self.slice_length
        cancel_time = self.cancel_time
        time_rand = self.time_rand
        increment = self.increment
        initial_offset = self.initial_offset
        min_offset = self.min_offset
        max_offset = self.max_offset
        volume_participation = self.volume_participation

        vo = py4jgateway.jvm.POVOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif,
                                        tif_date_time, exchange_order, exchange_id, security_id, account_id, portfolio_id,
                                        routing_candidates, start_time, end_time, duration, slice_length, cancel_time,
                                        time_rand, increment, initial_offset, min_offset, max_offset,
                                        volume_participation, last_status)
        return vo

    @staticmethod
    def convert_to_order(pov_order_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> POVOrder
        """Converts Java value object to a Python order object

           Arguments:
               pov_order_vo (ch.algotrader.entity.trade.algo.POVOrderVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               POVOrder
        """
        _id = pov_order_vo.getId()
        int_id = pov_order_vo.getIntId()
        ext_id = pov_order_vo.getExtId()
        parent_int_id = pov_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(pov_order_vo.getDateTime())
        side = None
        if pov_order_vo.getSide() is not None:
            side = pov_order_vo.getSide().toString()
        quantity = pov_order_vo.getQuantity()
        tif = None
        if pov_order_vo.getTif() is not None:
            tif = pov_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(pov_order_vo.getTifDateTime())
        exchange_order = pov_order_vo.isExchangeOrder()
        exchange_id = pov_order_vo.getExchangeId()
        security_id = pov_order_vo.getSecurityId()
        account_id = pov_order_vo.getAccountId()
        portfolio_id = pov_order_vo.getPortfolioId()
        last_status = None
        if pov_order_vo.getLastStatus() is not None:
            last_status = pov_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in pov_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)
        start_time = Conversions \
            .zoned_date_time_to_python_datetime(pov_order_vo.getStartTime())
        end_time = Conversions.zoned_date_time_to_python_datetime(pov_order_vo.getEndTime())
        duration = pov_order_vo.getDuration()
        slice_length = pov_order_vo.getSliceLength()
        cancel_time = pov_order_vo.getCancelTime()
        time_rand = pov_order_vo.getTimeRand()
        increment = pov_order_vo.getIncrement()
        initial_offset = pov_order_vo.getInitialOffset()
        min_offset = pov_order_vo.getMinOffset()
        max_offset = pov_order_vo.getMaxOffset()
        volume_participation = pov_order_vo.getVolumeParticipation()

        to = POVOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time, side=side,
                      quantity=quantity, tif=tif, tif_date_time=tif_date_time, exchange_order=exchange_order,
                      exchange_id=exchange_id, security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                      last_status=last_status, routing_candidates=routing_candidates, start_time=start_time,
                      end_time=end_time, duration=duration, slice_length=slice_length, cancel_time=cancel_time,
                      time_rand=time_rand, increment=increment, initial_offset=initial_offset, min_offset=min_offset,
                      max_offset=max_offset, volume_participation=volume_participation)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> POVOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized POVOrderVO): &nbsp;
           Returns:
               POVOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)
        start_time = Conversions.epoch_millis_to_python_datetime(vo_dict['startTime'])
        end_time = Conversions.epoch_millis_to_python_datetime(vo_dict['endTime'])
        duration = vo_dict['duration']
        slice_length = vo_dict['sliceLength']
        cancel_time = vo_dict['cancelTime']
        time_rand = vo_dict['timeRand']
        increment = vo_dict['increment']
        initial_offset = vo_dict['initialOffset']
        min_offset = vo_dict['minOffset']
        max_offset = vo_dict['maxOffset']
        volume_participation = vo_dict['volumeParticipation']

        to = POVOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time, side=side,
                      quantity=quantity, tif=tif, tif_date_time=tif_date_time, exchange_order=exchange_order,
                      exchange_id=exchange_id, security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                      last_status=last_status, routing_candidates=routing_candidates, start_time=start_time,
                      end_time=end_time, duration=duration, slice_length=slice_length, cancel_time=cancel_time,
                      time_rand=time_rand, increment=increment, initial_offset=initial_offset, min_offset=min_offset,
                      max_offset=max_offset, volume_participation=volume_participation)
        return to
    # POVOrder end


class SmartStopLimitOrder(AlgoOrder):
    """Mirrors SmartStopLimitOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           stop (Decimal): Stop price
           limit (Decimal): Limit price
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None,
                 security_id=None, account_id=None, portfolio_id=None, routing_candidates=None, last_status=None,
                 stop=None, limit=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str, Decimal, Decimal) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)
        self.stop = stop
        self.limit = limit

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.SmartStopLimitOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.SmartStopLimitOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)

        stop = self.stop
        limit = self.limit

        vo = py4jgateway.jvm.SmartStopLimitOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity,
                                               tif, tif_date_time, exchange_order, exchange_id, security_id,
                                               account_id, portfolio_id, routing_candidates, last_status, stop, limit)
        return vo

    @staticmethod
    def convert_to_order(smart_stop_limit_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> SmartStopLimitOrder
        """Converts Java value object to a Python order object

           Arguments:
               smart_stop_limit_order_vo (ch.algotrader.entity.trade.algo.SmartStopLimitOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               SmartStopLimitOrder
        """
        _id = smart_stop_limit_order_vo.getId()
        int_id = smart_stop_limit_order_vo.getIntId()
        ext_id = smart_stop_limit_order_vo.getExtId()
        parent_int_id = smart_stop_limit_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(smart_stop_limit_order_vo.getDateTime())
        side = None
        if smart_stop_limit_order_vo.getSide() is not None:
            side = smart_stop_limit_order_vo.getSide().toString()
        quantity = smart_stop_limit_order_vo.getQuantity()
        tif = None
        if smart_stop_limit_order_vo.getTif() is not None:
            tif = smart_stop_limit_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(smart_stop_limit_order_vo.getTifDateTime())
        exchange_order = smart_stop_limit_order_vo.isExchangeOrder()
        exchange_id = smart_stop_limit_order_vo.getExchangeId()
        security_id = smart_stop_limit_order_vo.getSecurityId()
        account_id = smart_stop_limit_order_vo.getAccountId()
        portfolio_id = smart_stop_limit_order_vo.getPortfolioId()
        last_status = None
        if smart_stop_limit_order_vo.getLastStatus() is not None:
            last_status = smart_stop_limit_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in smart_stop_limit_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        stop = smart_stop_limit_order_vo.getStop()
        limit = smart_stop_limit_order_vo.getLimit()

        to = SmartStopLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                                 side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                                 exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                                 account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                                 last_status=last_status, stop=stop, limit=limit)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> SmartStopLimitOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized SmartStopLimitOrderVO): &nbsp;
           Returns:
               SmartStopLimitOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        stop = Conversions.float_to_decimal(vo_dict['stop'])
        limit = Conversions.float_to_decimal(vo_dict['limit'])

        to = SmartStopLimitOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                                 side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                                 exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                                 account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                                 last_status=last_status, stop=stop, limit=limit)
        return to
    # SmartStopLimitOrder end


class IcebergOrder(AlgoOrder):
    """Mirrors IcebergOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
           display_size (Decimal): The quantity exposed to the market
           limit (Decimal): Limit price
           display_size_in_percent (bool): Display size in % of total quantity
           qty_rand (Decimal): (0.0 to 1.0) The display size will be randomly changed with variance (in %)
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, security_id=None, account_id=None,
                 portfolio_id=None, routing_candidates=None, last_status=None, display_size=None, limit=None,
                 display_size_in_percent=None, qty_rand=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str, Decimal, Decimal, bool, Decimal) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)
        self.display_size = display_size
        self.limit = limit
        self.display_size_in_percent = display_size_in_percent
        self.qty_rand = qty_rand

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.IcebergOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.IcebergOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)

        display_size = self.display_size
        limit = self.limit
        display_size_in_percent = self.display_size_in_percent
        qty_rand = self.qty_rand

        vo = py4jgateway.jvm.IcebergOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif,
                                            tif_date_time, exchange_order, exchange_id, security_id, account_id,
                                            portfolio_id, routing_candidates, last_status, display_size, limit,
                                            display_size_in_percent, qty_rand)
        return vo

    @staticmethod
    def convert_to_order(iceberg_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> IcebergOrder
        """Converts Java value object to a Python order object

           Arguments:
               iceberg_order_vo (ch.algotrader.entity.trade.algo.IcebergOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               IcebergOrder
        """
        _id = iceberg_order_vo.getId()
        int_id = iceberg_order_vo.getIntId()
        ext_id = iceberg_order_vo.getExtId()
        parent_int_id = iceberg_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(iceberg_order_vo.getDateTime())
        side = None
        if iceberg_order_vo.getSide() is not None:
            side = iceberg_order_vo.getSide().toString()
        quantity = iceberg_order_vo.getQuantity()
        tif = None
        if iceberg_order_vo.getTif() is not None:
            tif = iceberg_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(iceberg_order_vo.getTifDateTime())
        exchange_order = iceberg_order_vo.isExchangeOrder()
        exchange_id = iceberg_order_vo.getExchangeId()
        security_id = iceberg_order_vo.getSecurityId()
        account_id = iceberg_order_vo.getAccountId()
        portfolio_id = iceberg_order_vo.getPortfolioId()
        last_status = None
        if iceberg_order_vo.getLastStatus() is not None:
            last_status = iceberg_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in iceberg_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        display_size = iceberg_order_vo.getDisplaySize()
        limit = iceberg_order_vo.getLimit()
        display_size_in_percent = iceberg_order_vo.isDisplaySizeInPercent()
        qty_rand = iceberg_order_vo.getQtyRand()

        to = IcebergOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                          side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                          exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                          account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                          last_status=last_status, display_size=display_size, limit=limit,
                          display_size_in_percent=display_size_in_percent, qty_rand=qty_rand)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> IcebergOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized IcebergOrderVO): &nbsp;
           Returns:
               IcebergOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        display_size = Conversions.float_to_decimal(vo_dict['displaySize'])
        limit = Conversions.float_to_decimal(vo_dict['limit'])
        display_size_in_percent = vo_dict['displaySizeInPercent']
        qty_rand = Conversions.float_to_decimal(vo_dict['qtyRand'])

        to = IcebergOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                          side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                          exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                          account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                          last_status=last_status, display_size=display_size, limit=limit,
                          display_size_in_percent=display_size_in_percent, qty_rand=qty_rand)
        return to
    # IcebergOrder end


class SmartMarketOrder(AlgoOrder):
    """Mirrors SmartMarketOrderVO Java class

       Attributes:
           _id (int): &nbsp;
           int_id (str): The Internal Order Id. The Id is typically comprised of a sessionQualifier, a rootId and potentially a version. Example: ibn123.0
           ext_id (str): The External Order Id assigned by the external Broker;
           parent_int_id (str): The Internal Order Id of the Parent Order
           date_time (datetime):  The dateTime the order was sent. This is set automatically by the OrderService
           side (str): BUY, SELL
           quantity (Decimal): The requested number of contracts
           tif (str): Time-In-Force: "DAY", "GTC", "GTD", "IOC", "FOK", "ATO", "ATC", "PO"
           tif_date_time (datetime): The Time-in-Force date
           exchange_order (bool): Indicates whether this is an exchange order or margin order
           exchange_id (int): Exchange where securities are traded
           security_id (int): &nbsp;
           account_id (int): Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
           portfolio_id (int): Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.
           routing_candidates (Optional List of algotrader_com.domain.entity.RoutingTarget): &nbsp;
           last_status (str): The last known status of the order ( OPEN, SUBMITTED, PARTIALLY_EXECUTED, EXECUTED, CANCELED, REJECTED, CANCEL_FAILED, TARGET_REACHED)
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, parent_int_id=None, date_time=None, side=None, quantity=None,
                 tif=None, tif_date_time=None, exchange_order=None, exchange_id=None, security_id=None, account_id=None,
                 portfolio_id=None, routing_candidates=None, last_status=None):
        # type: (int, str, str, str, datetime, str, Decimal, str, datetime, bool, int, int, int, int, List[RoutingTarget], str) -> None
        AlgoOrder.__init__(self, _id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id,
                           date_time=date_time, side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                           exchange_order=exchange_order, exchange_id=exchange_id,
                           security_id=security_id, account_id=account_id, portfolio_id=portfolio_id,
                           last_status=last_status, routing_candidates=routing_candidates)

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.trade.algo.SmartMarketOrderVO"

    def convert_to_order_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the order to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.trade.algo.SmartMarketOrderVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        int_id = self.int_id
        ext_id = self.ext_id
        parent_int_id = self.parent_int_id
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        side = None
        if self.side is not None:
            side = py4jgateway.jvm.Side.valueOf(self.side)
        quantity = self.quantity
        tif = None
        if self.tif is not None:
            tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(self.tif)
        tif_date_time = Conversions.python_datetime_to_zoneddatetime(self.tif_date_time, py4jgateway)
        exchange_order = False
        if self.exchange_order is not None:
            exchange_order = self.exchange_order
        exchange_id = 0
        if self.exchange_id is not None:
            exchange_id = self.exchange_id
        security_id = 0
        if self.security_id is not None:
            security_id = self.security_id
        account_id = 0
        if self.account_id is not None:
            account_id = self.account_id
        portfolio_id = 0
        if self.portfolio_id is not None:
            portfolio_id = self.portfolio_id
        last_status = Conversions.convert_to_status_enum(self.last_status, py4jgateway)
        _routing_candidates = []
        for rc in self.routing_candidates:
            candidate = rc.convert_to_vo(py4jgateway)
            _routing_candidates.append(candidate)
        # noinspection PyProtectedMember
        routing_candidates = ListConverter().convert(_routing_candidates, py4jgateway._gateway_client)

        vo = py4jgateway.jvm.SmartMarketOrderVO(_id, int_id, ext_id, parent_int_id, date_time, side, quantity, tif,
                                            tif_date_time, exchange_order, exchange_id, security_id, account_id,
                                            portfolio_id, routing_candidates, last_status)
        return vo

    @staticmethod
    def convert_to_order(smart_market_order_vo, py4j_gateway):
        # type: (JavaObject, ClientServer) -> SmartMarketOrder
        """Converts Java value object to a Python order object

           Arguments:
               smart_market_order_vo (ch.algotrader.entity.trade.algo.SmartMarketOrderVO): &nbsp;
               py4j_gateway (ClientServer): &nbsp;
           Returns:
               SmartMarketOrder
        """
        _id = smart_market_order_vo.getId()
        int_id = smart_market_order_vo.getIntId()
        ext_id = smart_market_order_vo.getExtId()
        parent_int_id = smart_market_order_vo.getParentIntId()
        date_time = Conversions.zoned_date_time_to_python_datetime(smart_market_order_vo.getDateTime())
        side = None
        if smart_market_order_vo.getSide() is not None:
            side = smart_market_order_vo.getSide().toString()
        quantity = smart_market_order_vo.getQuantity()
        tif = None
        if smart_market_order_vo.getTif() is not None:
            tif = smart_market_order_vo.getTif().toString()
        tif_date_time = Conversions.zoned_date_time_to_python_datetime(smart_market_order_vo.getTifDateTime())
        exchange_order = smart_market_order_vo.isExchangeOrder()
        exchange_id = smart_market_order_vo.getExchangeId()
        security_id = smart_market_order_vo.getSecurityId()
        account_id = smart_market_order_vo.getAccountId()
        portfolio_id = smart_market_order_vo.getPortfolioId()
        last_status = None
        if smart_market_order_vo.getLastStatus() is not None:
            last_status = smart_market_order_vo.getLastStatus().toString()
        routing_candidates = []
        for rc in smart_market_order_vo.getRoutingCandidates():
            candidate = RoutingTarget.convert_from_vo(rc)
            routing_candidates.append(candidate)

        to = SmartMarketOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                              side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                              exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                              account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                              last_status=last_status)
        return to

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> SmartMarketOrder
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized SmartMarketOrderVO): &nbsp;
           Returns:
               SmartMarketOrder
        """
        _id = vo_dict['id']
        int_id = vo_dict['intId']
        ext_id = vo_dict['extId']
        parent_int_id = vo_dict['parentIntId']
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        side = vo_dict['side']
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        tif = vo_dict['tif']
        tif_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['tifDateTime'])
        exchange_order = vo_dict['exchangeOrder']
        exchange_id = vo_dict['exchangeId']
        security_id = vo_dict['securityId']
        account_id = vo_dict['accountId']
        portfolio_id = vo_dict['portfolioId']
        last_status = vo_dict['lastStatus']
        routing_candidates = []
        for rc in vo_dict["routingCandidates"]:
            candidate = RoutingTarget.convert_from_json(rc)
            routing_candidates.append(candidate)

        to = SmartMarketOrder(_id=_id, int_id=int_id, ext_id=ext_id, parent_int_id=parent_int_id, date_time=date_time,
                              side=side, quantity=quantity, tif=tif, tif_date_time=tif_date_time,
                              exchange_order=exchange_order, exchange_id=exchange_id, security_id=security_id,
                              account_id=account_id, portfolio_id=portfolio_id, routing_candidates=routing_candidates,
                              last_status=last_status)
        return to
    # SmartMarketOrder end