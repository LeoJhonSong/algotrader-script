from datetime import datetime

from py4j.java_collections import JavaIterator
from py4j.clientserver import ClientServer
from typing import List

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import TradingHours


class CalendarService:
    """Delegates to pythonCalendarService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonCalendarService()

    def get_current_trading_date_before_date_time(self, exchange_id, date_time):
        # type: (int, datetime) -> datetime
        """Gets the current trading date of the specified exchange. This represents the date when
          the particular exchange opened for the last time before the specified date_time.

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              datetime
          """
        millis = Conversions.python_datetime_to_millis(date_time)
        ld = self._service.getCurrentTradingDate(exchange_id, millis)
        result = Conversions.epoch_millis_to_python_datetime(ld)
        return result

    def get_current_trading_date(self, exchange_id):
        # type: (int) -> datetime
        """Gets the current trading date of the specified exchange. This represents the date when
          the particular exchange opened for the last time before the current time.

          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              datetime
          """
        ld = self._service.getCurrentTradingDate(exchange_id)
        result = Conversions.epoch_millis_to_python_datetime(ld)
        return result

    def is_open_on_date(self, exchange_id, date_time):
        # type: (int, datetime) -> bool
        """Returns true, if the exchange is currently open at the specified date_time, taking into consideration
           the different trading hours as well as holidays, early opens and early closes.

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              bool
          """
        millis = Conversions.python_datetime_to_millis(date_time)
        return self._service.isOpen(exchange_id, millis)

    def is_open(self, exchange_id):
        # type: (int) -> bool
        """Returns true, if the exchange is currently open the current date_time, taking into consideration
          the different trading hours as well as holidays, early opens and early closes.
          
          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              bool
        """
        return self._service.isOpen(exchange_id)

    def is_trading_day_on_date(self, exchange_id, date_time):
        # type: (int, datetime) -> bool
        """Returns true if the exchange is open on the specified date.

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              bool
        """
        millis = Conversions.python_datetime_to_millis(date_time)
        return self._service.isTradingDay(exchange_id, millis)

    def is_trading_day(self, exchange_id):
        # type: (int) -> bool
        """Returns true if the exchange is open on the specified date.

          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              bool
        """
        return self._service.isTradingDay(exchange_id)

    def get_open_time_on_date(self, exchange_id, date_time):
        # type: (int, datetime) -> datetime
        """Gets the time the exchange opens on a particular date or None if the exchange is closed on that day

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
           """
        millis = Conversions.python_datetime_to_millis(date_time)
        zd = self._service.getOpenTime(exchange_id, millis)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_open_time(self, exchange_id):
        # type: (int) -> datetime
        """Gets the time the exchange opens on the current date or None if the exchange is closed on that day

          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange."""
        zd = self._service.getOpenTime(exchange_id)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_close_time_on_date(self, exchange_id, date_time):
        # type: (int, datetime) -> datetime
        """Gets the time the exchange closes on a particular date or None if the exchange is closed on that day

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
         """
        millis = Conversions.python_datetime_to_millis(date_time)
        zd = self._service.getCloseTime(exchange_id, millis)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_close_time(self, exchange_id):
        # type: (int) -> datetime
        """Gets the time the exchange closes on the current date or None if the exchange is closed on that day

          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
         """
        zd = self._service.getCloseTime(exchange_id)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_next_open_time_on_date(self, exchange_id, date_time):
        # type: (int, datetime) -> datetime
        """Gets the time the exchange opens the next time after the specified date_time

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
        """
        millis = Conversions.python_datetime_to_millis(date_time)
        zd = self._service.getNextOpenTime(exchange_id, millis)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_next_open_time(self, exchange_id):
        # type: (int) -> datetime
        """Gets the time the exchange opens the next time after the current dateTime

          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
         """
        zd = self._service.getNextOpenTime(exchange_id)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_next_close_time_on_date(self, exchange_id, date_time):
        # type: (int, datetime) -> datetime
        """Gets the time the exchange closes the next time after the specified date_time

          Arguments:
              exchange_id (int): &nbsp;
              date_time (datetime): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
              """
        millis = Conversions.python_datetime_to_millis(date_time)
        zd = self._service.getNextCloseTime(exchange_id, millis)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_next_close_time(self, exchange_id):
        # type: (int) -> datetime
        """Gets the time the exchange closes the next time after the current dateTime

          Arguments:
              exchange_id (int): &nbsp;
          Returns:
              datetime: datetime with the time zone of the exchange.
        """
        zd = self._service.getNextCloseTime(exchange_id)
        result = Conversions.epoch_millis_to_python_datetime(zd)
        return result

    def get_trading_hours_by_exchange_id(self, exchange_id):
        # type: () -> List[TradingHours]
        """Get the trading hours of an exchange

        Arguments:
              exchange_id (int): &nbsp;
          Returns:
              TradingHours: TradingHours for provided exchange id.
        """
        vos = self._service.getTradingHoursByExchangeId(exchange_id)
        trading_hours = []

        for trading_hour_vo in vos:
            trading_hours.append(TradingHours.convert_from_vo(trading_hour_vo))
        return trading_hours

    def get_exchange_trading_hours(self):
        # type: () -> List[TradingHours]
        """Get the trading hours of all exchanges

          Returns:
              TradingHours: TradingHours for all exchanges.
        """
        vos = self._service.getExchangeTradingHours()
        trading_hours = []

        for trading_hour_vo in vos:
            trading_hours.append(TradingHours.convert_from_vo(trading_hour_vo))
        return trading_hours
