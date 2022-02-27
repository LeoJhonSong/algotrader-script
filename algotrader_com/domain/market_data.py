from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from py4j.clientserver import ClientServer
from py4j.java_gateway import JavaObject

from algotrader_com.domain.conversions import Conversions


class MarketDataEvent:
    """Mirrors ch.algotrader.entity.marketData.MarketDataEventVO. AlgoTrader Java
    class with fields using Python types. Any type of market data related to a
    particular security.
    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.MarketDataEventVO"

    def __init__(self, date_time=None, connector_descriptor=None, security_id=None):
        # type: (datetime, str, int) -> None
        self.date_time = date_time
        self.connector_descriptor = connector_descriptor  # "IB", "BMX" etc.
        self.security_id = security_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> MarketDataEvent
        """
           Arguments:
               vo (MarketDataEventVO subtype): &nbsp;
           Returns:
               MarketDataEvent
        """
        if vo is None:
            return None
        if vo.getClass().getCanonicalName() == Tick.JAVA_CLASS:
            event = Tick.convert_from_vo(vo)  # type: ignore
        elif vo.getClass().getCanonicalName() == Bar.JAVA_CLASS:
            event = Bar.convert_from_vo(vo)  # type: ignore
        elif vo.getClass().getCanonicalName() == Trade.JAVA_CLASS:
            event = Trade.convert_from_vo(vo)  # type: ignore
        elif vo.getClass().getCanonicalName() == Bid.JAVA_CLASS:
            event = Bid.convert_from_vo(vo)  # type: ignore
        elif vo.getClass().getCanonicalName() == Ask.JAVA_CLASS:
            event = Ask.convert_from_vo(vo)  # type: ignore
        elif vo.getClass().getCanonicalName() == BidAskQuote.JAVA_CLASS:
            event = BidAskQuote.convert_from_vo(vo)  # type: ignore
        elif vo.getClass().getCanonicalName() == GenericTick.JAVA_CLASS:
            event = GenericTick.convert_from_vo(vo)  # type: ignore
        else:
            raise Exception("Unsupported market data event type " + vo.getClass().getSimpleName() + ".")
        return event

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> MarketDataEvent
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized MarketDataEventVO subclass): &nbsp;
           Returns:
               MarketDataEvent
        """
        if vo_dict["objectType"] == "Tick":
            event = Tick.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "Bar":
            event = Bar.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "Trade":
            event = Trade.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "Bid":
            event = Bid.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "Ask":
            event = Ask.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "BidAskQuote":
            event = BidAskQuote.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "GenericTick":
            event = GenericTick.convert_from_json(vo_dict)  # type: ignore
        else:
            raise Exception("Unsupported market data event type " + vo_dict["objectType"] + ".")
        return event


class Tick(MarketDataEvent):
    """Mirrors TickVO Java class.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        last (Decimal): The last trade price.
        last_date_time (datetime): The dateTime of the last trade.
        bid (Decimal): The bid price.
        ask (Decimal): The ask price
        vol_bid (Decimal): The volume on the bid side.
        vol_ask (Decimal): The volume on the ask side.
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.TickVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, connector_descriptor=None, security_id=None, last=None, last_date_time=None, bid=None,
                 ask=None, vol_bid=None, vol_ask=None, vol=None):
        # type: (datetime, str, int, Decimal, datetime, Decimal, Decimal, Decimal, Decimal, Decimal) -> None
        MarketDataEvent.__init__(self, date_time, connector_descriptor, security_id)
        self.last = last
        self.last_date_time = last_date_time
        self.bid = bid
        self.ask = ask
        self.vol_bid = vol_bid
        self.vol_ask = vol_ask
        self.vol = vol

    @staticmethod
    def convert_from_vo(tick_vo):
        # type: (JavaObject) -> Tick
        """Converts Java value object to the Python object.
           Arguments:
               tick_vo (ch.algotrader.entity.marketData.TickVO): &nbsp;
           Returns:
               Tick
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(tick_vo.getDateTime())
        connector_descriptor = tick_vo.getConnectorDescriptor().getDescriptor()  # "IB", "BMX" etc.
        security_id = tick_vo.getSecurityId()
        last = tick_vo.getLast()
        last_date_time = Conversions.zoned_date_time_to_python_datetime(tick_vo.getLastDateTime())
        bid = tick_vo.getBid()
        ask = tick_vo.getAsk()
        vol_bid = tick_vo.getVolBid()
        vol_ask = tick_vo.getVolAsk()
        vol = tick_vo.getVol()
        tick = Tick(date_time, connector_descriptor, security_id, last, last_date_time, bid, ask, vol_bid, vol_ask, vol)
        return tick

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Tick
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized TickVO): &nbsp;
           Returns:
               Tick
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        last_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['lastDateTime'])
        tick = Tick(date_time, vo_dict['connectorDescriptor']['descriptor'], vo_dict['securityId'],
                    Conversions.float_to_decimal(vo_dict['last']),
                    last_date_time,
                    Conversions.float_to_decimal(vo_dict['bid']),
                    Conversions.float_to_decimal(vo_dict['ask']),
                    Conversions.float_to_decimal(vo_dict['volBid']),
                    Conversions.float_to_decimal(vo_dict['volAsk']),
                    Conversions.float_to_decimal(vo_dict['vol']))
        return tick

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the market data to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               JavaObject
        """
        vo_builder = py4jgateway.jvm.TickVOBuilder.create()  # java class
        if self.date_time is not None:
            date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
            vo_builder.setDateTime(date_time)
        vo_builder.setConnectorDescriptor(py4jgateway.jvm.ch.algotrader.api.connector.application.ConnectorDescriptor(self.connector_descriptor))
        vo_builder.setSecurityId(self.security_id)
        vo_builder.setLast(self.last)
        if self.last_date_time is not None:
            last_date_time = Conversions.python_datetime_to_zoneddatetime(self.last_date_time, py4jgateway)
            vo_builder.setLastDateTime(last_date_time)
        vo_builder.setBid(self.bid)
        vo_builder.setAsk(self.ask)
        vo_builder.setVolBid(self.vol_bid)
        vo_builder.setVolAsk(self.vol_ask)
        vo_builder.setVol(self.vol)
        vo = vo_builder.build()
        return vo


class Bar(MarketDataEvent):
    """Mirrors ch.algotrader.entity.marketData.BarVO. AlgoTrader Java class with
       fields using Python types.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        .. include:: ../bar_sizes.txt
        open_price (Decimal): The opening price of this bar.
        high (Decimal): The highest price during this bar.
        low (Decimal): The lowest price during this bar.
        close (Decimal): The closing price of this bar.
        vol (Decimal): The current volume.
        vwap (Decimal): The volume weighted average price
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.BarVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, adapter_type=None, security_id=None, bar_size=None, open_price=None, high=None,
                 low=None, close=None, vol=None, vwap=None):
        # type: (datetime, str, int, str, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal) -> None
        MarketDataEvent.__init__(self, date_time, adapter_type, security_id)
        self.bar_size = bar_size  # "MIN_1", "HOUR_5", "DAY_1", etc
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.vol = vol
        self.vwap = vwap

    @staticmethod
    def convert_from_vo(bar_vo):
        # type: (JavaObject) -> Bar
        """Converts 'ch.algotrader.entity.marketData.BarVO' Java value object to the Python object.
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(bar_vo.getDateTime())
        bar = Bar(date_time, bar_vo.getConnectorDescriptor().getDescriptor(), bar_vo.getSecurityId(), bar_vo.getBarSize().toString(),
                  bar_vo.getOpen(), bar_vo.getHigh(), bar_vo.getLow(), bar_vo.getClose(), bar_vo.getVol(),
                  bar_vo.getVwap())
        return bar

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Bar
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized BarVO): &nbsp;
           Returns:
               Bar
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        bar = Bar(date_time, vo_dict['connectorDescriptor']['descriptor'], vo_dict['securityId'], vo_dict['barSize'],
                  Conversions.float_to_decimal(vo_dict['open']),
                  Conversions.float_to_decimal(vo_dict['high']),
                  Conversions.float_to_decimal(vo_dict['low']),
                  Conversions.float_to_decimal(vo_dict['close']),
                  Conversions.float_to_decimal(vo_dict['vol']),
                  Conversions.float_to_decimal(vo_dict['vwap']))
        return bar


class Trade(MarketDataEvent):
    """Mirrors ch.algotrader.entity.marketData.TradeVO. AlgoTrader Java class
    with fields using Python types. Represents an actual trade that took place
    in the market.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        last_price (Decimal): &nbsp;
        last_size (Decimal): &nbsp;
        vol (Decimal): &nbsp;
        side (str): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.TradeVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, adapter_type=None, security_id=None, last_price=None, last_size=None, vol=None,
                 side=None):
        # type: (datetime, str, int, Decimal, Decimal, Decimal, str) -> None
        MarketDataEvent.__init__(self, date_time, adapter_type, security_id)
        self.last_price = last_price
        self.last_size = last_size
        self.vol = vol
        self.side = side

    @staticmethod
    def convert_from_vo(trade_vo):
        # type: (JavaObject) -> Trade
        """Converts Java value object to the Python object.

           Arguments:
               trade_vo (ch.algotrader.entity.marketData.TradeVO): &nbsp;
           Returns:
               Trade
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(trade_vo.getDateTime())
        if trade_vo.getSide() is None:
            trade = Trade(date_time, trade_vo.getConnectorDescriptor().getDescriptor(), trade_vo.getSecurityId(),
                          trade_vo.getLastPrice(), trade_vo.getLastSize(), trade_vo.getVol(), None)
        else:
            trade = Trade(date_time, trade_vo.getConnectorDescriptor().getDescriptor(), trade_vo.getSecurityId(),
                          trade_vo.getLastPrice(), trade_vo.getLastSize(), trade_vo.getVol(), trade_vo.getSide().toString())
        return trade

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Trade
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized TradeVO): &nbsp;
           Returns:
               Trade
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        trade = Trade(date_time, vo_dict['connectorDescriptor']['descriptor'], vo_dict['securityId'],
                      Conversions.float_to_decimal(vo_dict['lastPrice']),
                      Conversions.float_to_decimal(vo_dict['lastSize']),
                      Conversions.float_to_decimal(vo_dict['vol']),
                      vo_dict['side'])
        return trade


class Quote(MarketDataEvent):
    """Mirrors ch.algotrader.entity.marketData.QuoteVO. AlgoTrader Java class
    with fields using Python types. Represents a bid or ask quote.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
    """

    def __init__(self, date_time=None, adapter_type=None, security_id=None):
        # type: (datetime, str, int) -> None
        MarketDataEvent.__init__(self, date_time, adapter_type, security_id)

    @abstractmethod
    def get_object_type(self):
        pass

    @staticmethod
    def convert_from_vo(quote_vo):
        # type: (JavaObject) -> Quote
        """Converts Java value object to the Python object.

           Arguments:
               quote_vo (ch.algotrader.entity.marketData.QuoteVO): &nbsp;
           Returns:
               Quote
        """
        if quote_vo.getObjectType() == "Bid":
            quote = Bid.convert_from_vo(quote_vo)  # type: ignore
        elif quote_vo.getObjectType() == "Ask":
            quote = Ask.convert_from_vo(quote_vo)  # type: ignore
        elif quote_vo.getObjectType() == "BidAskQuote":
            quote = BidAskQuote.convert_from_vo(quote_vo)  # type: ignore
        else:
            raise Exception("Unexpected object type '" + quote_vo.getObjectType() + "'.")
        return quote

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Quote
        """
           Arguments:
               vo_dict (deserialized QuoteVO): &nbsp;
           Returns:
               Quote
        """

        if vo_dict["objectType"] == "Bid":
            quote = Bid.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "Ask":
            quote = Ask.convert_from_json_object(vo_dict)  # type: ignore
        elif vo_dict["objectType"] == "BidAskQuote":
            quote = BidAskQuote.convert_from_json_object(vo_dict)  # type: ignore
        else:
            raise Exception("Unknown quote type: " + vo_dict["objectType"])
        return quote


class Bid(Quote):
    """Mirrors ch.algotrader.entity.marketData.BidVO. AlgoTrader Java class with
    fields using Python types. A bid Quote.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        price (Decimal): &nbsp;
        size (Decimal): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.BidVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, adapter_type=None, security_id=None, price=None, size=None):
        # type: (datetime, str, int, Decimal, Decimal) -> None
        Quote.__init__(self, date_time, adapter_type, security_id)
        self.price = price
        self.size = size

    def get_object_type(self):
        return "Bid"

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Bid
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized BidVO): &nbsp;
           Returns:
               Bid
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        bid = Bid(date_time, vo_dict['connectorDescriptor']['descriptor'], vo_dict['securityId'],
                  Conversions.float_to_decimal(vo_dict['price']),
                  Conversions.float_to_decimal(vo_dict['size']))
        return bid

    @staticmethod
    def convert_from_vo(quote_vo):
        # type: (JavaObject) -> Bid
        """Converts Java value object to the Python object.

           Arguments:
               quote_vo (ch.algotrader.entity.marketData.BidVO): &nbsp;
           Returns:
               Bid
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(quote_vo.getDateTime())
        quote = Bid(date_time, quote_vo.getConnectorDescriptor().getDescriptor(), quote_vo.getSecurityId(), quote_vo.getPrice(),
                    quote_vo.getSize())
        return quote


class Ask(Quote):
    """Mirrors ch.algotrader.entity.marketData.AskVO. AlgoTrader Java class with
    fields using Python types. An ask Quote.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        price (Decimal): &nbsp;
        size (Decimal): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.AskVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, adapter_type=None, security_id=None, price=None, size=None):
        # type: (datetime, str, int, Decimal, Decimal) -> None
        Quote.__init__(self, date_time, adapter_type, security_id)
        self.price = price
        self.size = size

    def get_object_type(self):
        return "Ask"

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> Ask
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized AskVO): &nbsp;
           Returns:
               Ask
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        ask = Ask(date_time, vo_dict['connectorDescriptor']['descriptor'], vo_dict['securityId'],
                  Conversions.float_to_decimal(vo_dict['price']),
                  Conversions.float_to_decimal(vo_dict['size']))
        return ask

    @staticmethod
    def convert_from_vo(quote_vo):
        # type: (JavaObject) -> Ask
        """Converts Java value object to the Python object.

           Arguments:
               quote_vo (ch.algotrader.entity.marketData.AskVO): &nbsp;
           Returns:
               Ask
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(quote_vo.getDateTime())
        quote = Ask(date_time, quote_vo.getConnectorDescriptor().getDescriptor(), quote_vo.getSecurityId(), quote_vo.getPrice(),
                    quote_vo.getSize())
        return quote


class BidAskQuote(Quote):
    """Mirrors ch.algotrader.entity.marketData.BidAskVO. AlgoTrader Java class with
    fields using Python types. Represents a quote with both ask price and bid price provided by a data feed.

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        bid_price (Decimal): &nbsp;
        bid_size (Decimal): &nbsp;
        ask_price (Decimal): &nbsp;
        ask_size (Decimal): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.BidAskQuoteVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, adapter_type=None, security_id=None, bid_price=None, bid_size=None,
                 ask_price=None, ask_size=None):
        # type: (datetime, str, int, Decimal, Decimal, Decimal, Decimal) -> None
        Quote.__init__(self, date_time, adapter_type, security_id)
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.ask_price = ask_price
        self.ask_size = ask_size

    def get_object_type(self):
        return "BidAskQuote"

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> BidAskQuote
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized BidAskQuoteVO): &nbsp;
           Returns:
               BidAskQuote
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        bid_ask = BidAskQuote(date_time, vo_dict['connectorDescriptor']['descriptor'], vo_dict['securityId'],
                              Conversions.float_to_decimal(vo_dict['bidPrice']),
                              Conversions.float_to_decimal(vo_dict['bidSize']),
                              Conversions.float_to_decimal(vo_dict['askPrice']),
                              Conversions.float_to_decimal(vo_dict['askSize']))
        return bid_ask

    @staticmethod
    def convert_from_vo(quote_vo):
        # type: (JavaObject) -> BidAskQuote
        """Converts Java value object to the Python object.

           Arguments:
               quote_vo (ch.algotrader.entity.marketData.BidAskQuoteVO): &nbsp;
           Returns:
               BidAskQuote
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(quote_vo.getDateTime())
        quote = BidAskQuote(date_time, quote_vo.getConnectorDescriptor().getDescriptor(), quote_vo.getSecurityId(), quote_vo.getBidPrice(),
                            quote_vo.getBidSize(), quote_vo.getAskPrice(), quote_vo.getAskSize())
        return quote


# TODO mpd GenericEvent
class GenericTick(MarketDataEvent):
    """Mirrors GenericTickVO Java class. Any type of market data related to a
    particular security.

    Attributes:
        id (int): &nbsp;
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        tick_type (str):  OPEN, HIGH, LOW, CLOSE, SETTLEMENT, OPEN_INTEREST, IMBALANCE, VWAP, YIELD_TO_MATURITY, MODIFIED_DURATION
        money_value (Decimal): &nbsp;
        double_value (float): &nbsp;
        int_value (int): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.GenericTickVO"

    def __init__(self, id=None, date_time=None, connector_descriptor=None, security_id=None, tick_type=None, money_value=None,
                 double_value=None, int_value=None):
        # type: (int, datetime, str, int, str, Decimal, float, int) -> None
        MarketDataEvent.__init__(self, date_time, connector_descriptor, security_id)
        self.id = id
        self.tick_type = tick_type
        self.money_value = money_value
        self.double_value = double_value
        self.int_value = int_value

    @staticmethod
    def convert_from_vo(generic_tick_vo):
        # type: (JavaObject) -> GenericTick
        """Converts Java value object to the Python object.

           Arguments:
               generic_tick_vo (ch.algotrader.entity.marketData.GenericEventVO): &nbsp;
           Returns:
               GenericTick
        """
        id = generic_tick_vo.getId()
        date_time = Conversions.zoned_date_time_to_python_datetime(generic_tick_vo.getDateTime())
        tick_type = None
        if generic_tick_vo.getTickType() is not None:
            tick_type = generic_tick_vo.getTickType().toString()
        money_value = generic_tick_vo.getMoneyValue()
        double_value = generic_tick_vo.getDoubleValue()
        int_value = generic_tick_vo.getIntValue()
        connector_descriptor = generic_tick_vo.getConnectorDescriptor().getDescriptor()
        generic_tick = GenericTick(id, date_time, connector_descriptor, generic_tick_vo.getSecurityId(),
                                     tick_type, money_value, double_value, int_value)
        return generic_tick

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> GenericTick
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized GenericTickVO): &nbsp;
           Returns:
               GenericTick
        """
        id = vo_dict["id"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        connector_descriptor = vo_dict['connectorDescriptor']['descriptor']
        security_id = vo_dict['securityId']
        tick_type = vo_dict["tickType"]
        money_value = None
        if vo_dict['moneyValue'] is not None:
            money_value = Conversions.float_to_decimal(vo_dict['moneyValue'])
        double_value = vo_dict["doubleValue"]
        int_value = vo_dict["intValue"]
        generic_tick = GenericTick(id, date_time, connector_descriptor, security_id, tick_type, money_value,
                                     double_value, int_value)
        return generic_tick

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               JavaObject
        """
        vo_builder = py4jgateway.jvm.GenericTickVOBuilder.create()  # java class
        if self.date_time is not None:
            date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
            vo_builder.setDateTime(date_time)
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setConnectorDescriptor(py4jgateway.jvm.ch.algotrader.api.connector.application.ConnectorDescriptor(self.connector_descriptor))
        vo_builder.setSecurityId(self.security_id)
        tick_type = None
        if self.tick_type is not None:
            tick_type = py4jgateway.jvm.TickType.valueOf(self.tick_type)
        vo_builder.setTickType(tick_type)
        vo_builder.setMoneyValue(self.money_value)
        vo_builder.setDoubleValue(self.double_value)
        vo_builder.setIntValue(self.int_value)
        vo = vo_builder.build()
        return vo


class OrderBookLevel:
    """Mirrors ch.algotrader.entity.orderbook.OrderBookLevelVO

    Attributes:
        price (Decimal):  &nbsp;
        amount (Decimal):  &nbsp;
        count (int):  &nbsp;
    """
    def __init__(self, price=None, amount=None, count=None):
        # type: (Decimal, Decimal, int) -> None
        self.price = price
        self.amount = amount
        self.count = count


class SubscriptionRequest:
    """Mirrors ch.algotrader.entity.marketData.SubscriptionRequest

    Attributes:
        security_id (int):  &nbsp;
        market_data_level (str): The level of market data. Valid values: L1, L2, L1L2, Zero
        market_data_level (str): (optional) Minimal level of market data. Valid values: L1, L2, L1L2, Zero, None
    """
    def __init__(self, security_id=None, market_data_level=None, min_level=None):
        # type: (int, str, str) -> None
        self.security_id = security_id
        self.market_data_level = market_data_level
        self.min_level = min_level

    def convert_to_java(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the market data to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               JavaObject
        """
        level = Conversions.convert_to_market_data_level_enum(self.market_data_level, py4jgateway)
        min_level = Conversions.convert_to_market_data_level_enum(self.min_level, py4jgateway) if self.min_level is not None else None
        vo = py4jgateway.jvm.SubscriptionRequest(self.security_id, level, min_level)  # java class
        return vo


class OrderBook(MarketDataEvent):
    """Mirrors ch.algotrader.entity.marketData.OrderBookVO

    Attributes:
        date_time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        security_id (int): &nbsp;
        bids (List of OrderBookLevel): &nbsp;
        asks (List of OrderBookLevel): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.marketData.OrderBook"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, date_time=None, connector_descriptor=None, security_id=None, bids=None, asks=None):
        # type: (datetime, str, int, List[OrderBookLevel], List[OrderBookLevel]) -> None
        MarketDataEvent.__init__(self, date_time, connector_descriptor, security_id)
        self.date_time = date_time
        self.connector_descriptor = connector_descriptor
        self.security_id = security_id
        self.bids = bids
        self.asks = asks

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> OrderBook
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized OrderBookVO): &nbsp;
           Returns:
               OrderBook
        """
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        connector_descriptor = vo_dict['connectorDescriptor']
        descriptor = connector_descriptor['descriptor']
        security_id = vo_dict['securityId']

        bids = []
        for key in vo_dict['bids']:
            bid_vo = vo_dict['bids'][key]
            bid = OrderBookLevel(bid_vo['price'], bid_vo['amount'], bid_vo['count'])
            bids.append(bid)
        bids.sort(key=lambda x: x.price, reverse=True)

        asks = []
        for key in vo_dict['asks']:
            ask_vo = vo_dict['asks'][key]
            ask = OrderBookLevel(ask_vo['price'], ask_vo['amount'], ask_vo['count'])
            asks.append(ask)
        asks.sort(key=lambda x: x.price, reverse=False)

        order_book = OrderBook(date_time, descriptor, security_id, bids, asks)
        return order_book


class AggregatedOrderBookLevelDetails:
    """Mirrors ch.algotrader.entity.orderbook.AggregatedOrderBookLevelDetailsVO

    Attributes:
        security_id (int): &nbsp;
        amount (Decimal): &nbsp;
        count (int): &nbsp;
    """
    def __init__(self, security_id, amount, count):
        # type: (int, Decimal, int) -> None
        self.security_id = security_id
        self.amount = amount
        self.count = count

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> AggregatedOrderBookLevelDetails
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized AggregatedOrderBookLevelDetails): &nbsp;
           Returns:
               AggregatedOrderBookLevelDetails
        """
        amount = vo_dict['amount']
        count = vo_dict['count']
        security_id = vo_dict['securityId']
        details = AggregatedOrderBookLevelDetails(security_id, amount, count)
        return details


class AggregatedOrderBookLevel:
    """Mirrors ch.algotrader.entity.orderbook.AggregatedOrderBookLevelVO

    Attributes:
        price (float): &nbsp;
        details_by_exchange (Dict of float to AggregatedOrderBookLevelDetails): &nbsp;
    """
    def __init__(self, price, details_by_exchange):
        # type: (float, Dict[float, AggregatedOrderBookLevelDetails]) -> None
        self.price = price
        self.details_by_exchange = details_by_exchange

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> AggregatedOrderBookLevel
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized AggregatedOrderBookLevel): &nbsp;
           Returns:
               AggregatedOrderBookLevel
        """
        price_of_level = vo_dict['price']
        details_by_exchange = vo_dict['detailsByExchange']
        details_dict = {}
        for price in details_by_exchange:
            details = AggregatedOrderBookLevelDetails.convert_from_json_object(details_by_exchange[price])
            price_converted = float(price)
            details_dict[price_converted] = details
        price_level = AggregatedOrderBookLevel(price_of_level, details_dict)
        return price_level


class AggregatedOrderBook:
    """Mirrors ch.algotrader.entity.orderbook.AggregatedOrderBookVO

    Attributes:
        symbol (str): &nbsp;
        timestamp (datetime): &nbsp;
        bids (Dict of float to AggregatedOrderBookLevel): &nbsp;
        asks (Dict of float to AggregatedOrderBookLevel): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.entity.orderbook.AggregatedOrderBookVO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, symbol, timestamp, bids, asks):
        # type: (str, datetime, Dict[float, AggregatedOrderBookLevel], Dict[float, AggregatedOrderBookLevel]) -> None
        self.symbol = symbol
        self.timestamp = timestamp
        self.bids = bids
        self.asks = asks

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> AggregatedOrderBook
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized AggregatedOrderBook): &nbsp;
           Returns:
               AggregatedOrderBook
        """
        timestamp = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        symbol = vo_dict['symbol']

        bids = {}
        for price in vo_dict['bids']:
            price_level = AggregatedOrderBookLevel.convert_from_json_object(vo_dict['bids'][price])
            price_converted = float(price)
            bids[price_converted] = price_level
        asks = {}
        for price in vo_dict['asks']:
            price_level = AggregatedOrderBookLevel.convert_from_json_object(vo_dict['asks'][price])
            price_converted = float(price)
            asks[price_converted] = price_level

        order_book = AggregatedOrderBook(symbol, timestamp, bids, asks)
        return order_book


class MarketScannerParameters:
    """Mirrors ch.algotrader.api.connector.marketdata.domain.MarketScannerParametersDTO

    Attributes:
        instrument (str): &nbsp;
        location_code (str): &nbsp;
        scan_code (str): &nbsp;
        above_price (Optional[float]): &nbsp;
        below_price (Optional[float]): &nbsp;
        above_volume (Optional[int]): &nbsp;
        filters (Dict[str,str]): &nbsp;
    """

    JAVA_CLASS = "ch.algotrader.api.connector.marketdata.domain.MarketScannerParametersDTO"

    def get_java_class(self):
        # type: () -> str
        """
            Returns:
                str
        """
        return self.JAVA_CLASS

    def __init__(self, instrument, location_code, scan_code, above_price, below_price, above_volume, filters):
        # type: (str, str, str, Optional[float], Optional[float], Optional[int], Dict[str,str]) -> None
        self.instrument = instrument
        self.location_code = location_code
        self.scan_code = scan_code
        self.above_price = above_price
        self.below_price = below_price
        self.above_volume = above_volume
        self.filters = filters

    def convert_to_java(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the market scanner parameters to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               JavaObject
        """
        # java class
        filters_java = py4jgateway.jvm.java.util.HashMap()
        for key in self.filters:
            filters_java.put(key, self.filters[key])
        vo = py4jgateway.jvm.ch.algotrader.api.connector.marketdata.domain.MarketScannerParametersDTO(self.instrument, self.location_code, self.scan_code, self.above_price, self.below_price, self.above_volume, filters_java)
        return vo

