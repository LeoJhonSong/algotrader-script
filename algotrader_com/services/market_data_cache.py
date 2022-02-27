from decimal import Decimal
from typing import List, Optional, Type

from py4j.clientserver import ClientServer
from py4j.java_collections import ListConverter

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.market_data import MarketDataEvent
from algotrader_com.domain.market_data import SubscriptionRequest


class MarketDataCacheService:
    """Delegates to marketDataCacheService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.getPythonMarketDataCacheService()

    def get_current_market_data_events(self):
        # type: () -> List[MarketDataEvent]
        """Returns all last market events for all securities.
           NOTE: Entries of the returned map can be any of algotrader_com.domain.market_data.MarketDataEvent subtypes, some ids may be ticks, other bars, etc.

           Returns:
               List of algotrader_com.domain.market_data.MarketDataEvent
        """
        vo_jsons = self._service.getCurrentMarketDataEvents()
        values = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            event = MarketDataEvent.convert_from_json_object(_dict)
            values.append(event)
        return values

    def get_current_market_data_events_by_event_class(self, market_data_event_class):
        # type: (Type[MarketDataEvent]) -> List[MarketDataEvent]
        """Returns all last market events of type market_data_event_class for all securities.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
            Returns:
                List of algotrader_com.domain.market_data.MarketDataEvent
        """
        vo_jsons = self._service.getCurrentMarketDataEvents(market_data_event_class.JAVA_CLASS)
        values = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            event = MarketDataEvent.convert_from_json_object(_dict)
            values.append(event)
        return values

    def get_current_market_data_event(self, security_id):
        # type: (int) -> Optional[MarketDataEvent]
        """Returns last market event of the specified security.
           NOTE: The returned market event can be any of algotrader_com.domain.market_data.MarketDataEvent subtypes.

           Arguments:
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.MarketDataEvent
        """
        vo_json = self._service.getCurrentMarketDataEvent(security_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        event = MarketDataEvent.convert_from_json_object(_dict)
        return event

    def get_current_market_data_event_by_event_class(self, market_data_event_class, security_id):
        # type: (Type[MarketDataEvent], int) -> Optional[MarketDataEvent]
        """Returns last market event of type market_data_event_class of the specified security.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
                security_id (int): &nbsp;
            Returns:
                List of algotrader_com.domain.market_data.MarketDataEvent
        """
        vo_json = self._service.getCurrentMarketDataEvent(market_data_event_class.JAVA_CLASS, security_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        event = MarketDataEvent.convert_from_json_object(_dict)
        return event

    def get_current_value(self, security_id):
        # type: (int) -> Decimal
        """Returns the current value of the specified security.

            Arguments:
                security_id (int): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getCurrentValue(security_id)

    def get_current_ask_price(self, security_id):
        # type: (int) -> Decimal
        """Returns the current ask price of the specified security.

            Arguments:
                security_id (int): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getCurrentAskPrice(security_id)

    def get_current_ask_volume(self, security_id):
        # type: (int) -> Decimal
        """Returns the current ask volume of the specified security.

            Arguments:
                security_id (int): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getCurrentAskVolume(security_id)

    def get_current_bid_price(self, security_id):
        # type: (int) -> Decimal
        """Returns the current bid price of the specified security.

            Arguments:
                security_id (int): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getCurrentBidPrice(security_id)

    def get_current_bid_volume(self, security_id):
        # type: (int) -> Decimal
        """Returns the current bid volume of the specified security.

            Arguments:
                security_id (int): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getCurrentBidVolume(security_id)

    def get_current_value_by_event_class(self, market_data_event_class, security_id):
        # type: (Type[MarketDataEvent], int) -> Decimal
        """Returns the current value of the specified security.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
                security_id (int): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getCurrentValue(market_data_event_class.JAVA_CLASS, security_id)

    def get_forex_rate_by_base_currency(self, base_currency, quote_currency):
        # type: (str, str) -> float
        """Gets the current exchange rate between the base_currency and quote_currency. It may be calculated from the last arrived event, a tick, from a bar, etc.

            Arguments:
                base_currency (str): &nbsp;
                quote_currency (str): &nbsp;
            Returns:
                float
        """
        return self._service.getForexRate(base_currency, quote_currency)

    def get_forex_rate_by_event_class_and_base_currency(self, market_data_event_class, base_currency,
                                                        quote_currency):
        # type: (Type[MarketDataEvent], str, str) -> float
        """Gets the current exchange rate between the base_currency and quote_currency based on the given market_data_event_class of the last arrived market data event.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
                base_currency (str): &nbsp;
                quote_currency (str): &nbsp;
            Returns:
                float
        """
        return self._service.getForexRate(market_data_event_class.JAVA_CLASS, base_currency, quote_currency)

    def get_forex_rate_base_by_base_currency(self, base_currency):
        # type: (str) -> float
        """Gets the current Exchange Rate between the base_currency and the portfolio base currency.
           NOTE: The exchange rate is based on the market data event that arrived last. It can be calculated from a tick, from a bar, etc.

           Arguments:
               base_currency (str): &nbsp;
           Returns:
               float
        """
        return self._service.getForexRateBase(base_currency)

    def get_forex_rate_base_by_event_class_and_base_currency(self, market_data_event_class, base_currency):
        # type: (Type[MarketDataEvent], str) -> float
        """Gets the current Exchange Rate between the base_currency and the portfolio base currency based on the given market_data_event_class of the last arrived market data event.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
                base_currency (str): &nbsp;
            Returns:
                float
        """
        return self._service.getForexRateBase(market_data_event_class.JAVA_CLASS, base_currency)

    def get_forex_rate_by_security_id(self, security_id, quote_currency):
        # type: (int, str) -> float
        """Gets the relevant exchange rate for the specified security related to the specified currency.
           NOTE: The exchange rate is based on the market data event that arrived last. It can be calculated from a tick, from a bar, etc.

           Arguments:
               security_id (int): &nbsp;
               quote_currency (str): &nbsp;
           Returns:
               float
        """
        rate = self._service.getForexRate(security_id, quote_currency)
        return rate

    def get_forex_rate_by_event_class_and_security_id(self, market_data_event_class, security_id, quote_currency):
        # type: (Type[MarketDataEvent], int, str) -> float
        """Gets the relevant exchange rate for the specified security related to the specified currency based on the given market_data_event_class of the last arrived market data event.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
                security_id (int): &nbsp;
                quote_currency (str): &nbsp;
            Returns:
                float
        """
        rate = self._service.getForexRate(market_data_event_class.JAVA_CLASS, security_id, quote_currency)
        return rate

    def get_forex_rate_base_by_security_id(self, security_id):
        # type: (int) -> float
        """Gets the relevant exchange rate for the specified security related to the specified currency.
           NOTE: The exchange rate is based on the market data event that arrived last. It can be calculated from a tick, from a bar, etc.

           Arguments:
               security_id (int): &nbsp;
           Returns:
               float
        """
        return self._service.getForexRateBase(security_id)

    def get_forex_rate_base_by_event_class_and_security_id(self, market_data_event_class, security_id):
        # type: (Type[MarketDataEvent], int) -> float
        """Gets the relevant exchange rate for the specified security related to the specified currency based on the given market_data_event_class of the last arrived market data event.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
                security_id (int): &nbsp;
            Returns:
                float
        """
        return self._service.getForexRateBase(market_data_event_class.JAVA_CLASS, security_id)

    def has_current_market_data_events(self):
        # type: () -> bool
        """Returns true if any MarketDataEvent has been received.

            Returns:
                bool
        """
        return self._service.hasCurrentMarketDataEvents()

    def has_current_market_data_events_by_event_class(self, market_data_event_class):
        # type: (Type[MarketDataEvent]) -> bool
        """Returns true if any MarketDataEvent of type market_data_event_class has been received. has been received.

            Arguments:
                market_data_event_class (Class of algotrader_com.domain.market_data.MarketDataEvent): Type of events to be returned. A MarketDataEvent sub-class.
            Returns:
                bool
        """
        return self._service.hasCurrentMarketDataEvents(market_data_event_class.JAVA_CLASS)

    def flush(self):
        # type: () -> None
        """Clears cached market data events for all securities."""
        self._service.flush()

    def flush_security(self, security_id):
        # type: (int) -> None
        """Clears the cached market data event for the specified security. security_id the ID of the security whose cached market data event to clear.

            Arguments:
                security_id (int): &nbsp;
        """
        self._service.flush(security_id)

    def ensure_market_data_available(self, requests, timeout, timeout_unit):
        # type: (List[SubscriptionRequest], int, str) -> None
        """Checks if there are market events for given securities. Waits for event to come for specified period.

            Arguments:
                requests (List[SubscriptionRequest]): &nbsp;
                timeout (int): number of timeout_unit-s
                timeout_unit (str): java.time.temporal.ChronoUnit values: NANOS, MICROS, MILLIS, SECONDS, MINUTES, HOURS, HALF_DAYS, DAYS, WEEKS, MONTHS,...
        """
        # noinspection PyProtectedMember

        _requests = []
        for req in requests:
            java_req = req.convert_to_java(self._gateway)
            _requests.append(java_req)
        # noinspection PyProtectedMember
        requests_list = ListConverter().convert(_requests, self._gateway._gateway_client)
        self._service.ensureMarketDataAvailable(requests_list, timeout, timeout_unit)
