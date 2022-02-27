from datetime import datetime
from typing import List, Dict

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.market_data import Tick, Bar, Ask, Bid, BidAskQuote, Trade


class HistoricalDataService:
    """Delegates to historicalDataService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway=None):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonHistoricalDataService()

    def get_last_tick(self, security_id, max_date, interval_days):
        # type: (int, datetime, int) -> Tick
        """Gets the last tick for the specified security for the specified time period.

           Arguments:
               security_id (int): &nbsp;
               max_date (datetime): tick will be loaded before this date
               interval_days (int): number of days before dateTime tick will be loaded
           Returns:
               algotrader_com.domain.market_data.Tick
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        vo_json = self._service.getLastTick(security_id, max_date_converted,
                                            interval_days)
        _dict = Conversions.unmarshall(vo_json)
        tick = Tick.convert_from_json_object(_dict)
        return tick

    def get_ticks_by_max_date(self, security_id, max_date, interval_days):
        # type: (int, datetime, int) -> List[Tick]
        """Gets all ticks of the defined security for the specified time period.

           Arguments:
               security_id (int):
               max_date (datetime): Ticks will be loaded before this date.
               interval_days (int): Number of days before max_date ticks will be loaded.
           Returns:
               List of algotrader_com.domain.market_data.Tick
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        vos = self._service.getTicksByMaxDate(security_id, max_date_converted,
                                              interval_days)
        ticks = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = Tick.convert_from_json_object(_dict)
            ticks.append(tick)
        return ticks

    def get_ticks_by_min_date(self, security_id, min_date, interval_days):
        # type: (int, datetime, int) -> List[Tick]
        """Gets all ticks of the defined security for the specified time period


           Arguments:
               security_id (int):
               min_date (datetime): Ticks will be loaded after this date.
               interval_days (int): Number of days after min_date ticks will be loaded.
           Returns:
               List of algotrader_com.domain.market_data.Tick
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        vos = self._service.getTicksByMinDate(security_id, min_date_converted,
                                              interval_days)
        ticks = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = Tick.convert_from_json_object(_dict)
            ticks.append(tick)
        return ticks

    # noinspection PyIncorrectDocstring
    def get_last_n_bars_by_security_and_bar_size(self, n, security_id, bar_size):
        # type: (int, int, str) -> List[Bar]
        """ Returns the last 'n' bars of the specified security

           Arguments:
               n (int): number of bars to load
               security_id (int): &nbsp;
               .. include:: ../bar_sizes.txt
           Returns:
               List of algotrader_com.domain.market_data.Bar
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)
        vos = self._service \
            .getLastNBarsBySecurityAndBarSize(n, security_id, bar_size_enum)
        bars = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            bar = Bar.convert_from_json_object(_dict)
            bars.append(bar)
        return bars

    # noinspection PyIncorrectDocstring
    def get_bars_by_security_min_date_and_bar_size(self, security_id, min_date, bar_size):
        # type: (int, datetime, str) -> List[Bar]
        """Returns bars of the specified security security_id after the specified min_date.

           Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               .. include:: ../bar_sizes.txt
           Returns:
               List of algotrader_com.domain.market_data.Bar
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)

        vos = self._service.getBarsBySecurityMinDateAndBarSize(security_id, min_date_converted,
                                                               bar_size_enum)
        bars = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            bar = Bar.convert_from_json_object(_dict)
            bars.append(bar)
        return bars

    # noinspection PyIncorrectDocstring
    def get_bars_by_security_min_date_max_date_and_bar_size(self, security_id, min_date, max_date, bar_size):
        # type: (int, datetime, datetime, str) -> List[Bar]
        """Returns bars of the specified security security_id between min_date and max_date.

           Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               max_date (datetime): &nbsp;
               .. include:: ../bar_sizes.txt
           Returns:
               List of algotrader_com.domain.market_data.Bar
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)

        vos = self._service.getBarsBySecurityMinDateMaxDateAndBarSize(security_id, min_date_converted,
                                                                      max_date_converted, bar_size_enum)
        bars = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            bar = Bar.convert_from_json_object(_dict)
            bars.append(bar)
        return bars

    def get_asks_by_max_date(self, security_id, max_date, interval_days):
        # type: (int, datetime, int) -> List[Ask]
        """Arguments:
               security_id (int): &nbsp;
               max_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.Ask
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)

        vos = self._service.getAsksByMaxDate(security_id, max_date_converted, interval_days)
        objects = []  # type: List[Ask]
        for vo in vos:
            obj = Ask.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_asks_by_min_date(self, security_id, min_date, interval_days):
        # type: (int, datetime, int) -> List[Ask]
        """Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.Ask
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)

        vos = self._service.getAsksByMinDate(security_id, max_date_converted, interval_days)
        objects = []  # type: List[Ask]
        for vo in vos:
            obj = Ask.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_bids_by_max_date(self, security_id, max_date, interval_days):
        # type: (int, datetime, int) -> List[Bid]
        """Arguments:
               security_id (int): &nbsp;
               max_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.Bid
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)

        vos = self._service.getBidsByMaxDate(security_id, max_date_converted, interval_days)
        objects = []  # type: List[Bid]
        for vo in vos:
            obj = Bid.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_bids_by_min_date(self, security_id, min_date, interval_days):
        # type: (int, datetime, int) -> List[Bid]
        """Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.Bid
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)

        vos = self._service.getBidsByMinDate(security_id, min_date_converted, interval_days)
        objects = []  # type: List[Bid]
        for vo in vos:
            obj = Bid.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_bidasks_by_max_date(self, security_id, max_date, interval_days):
        # type: (int, datetime, int) -> List[BidAskQuote]
        """Arguments:
               security_id (int): &nbsp;
               max_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.BidAskQuote
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)

        vos = self._service.getBidAsksByMaxDate(security_id, max_date_converted, interval_days)
        objects = []  # type: List[BidAskQuote]
        for vo in vos:
            obj = BidAskQuote.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_bidasks_by_min_date(self, security_id, min_date, interval_days):
        # type: (int, datetime, int) -> List[BidAskQuote]
        """Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.BidAskQuote
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)

        vos = self._service.getBidAsksByMinDate(security_id, min_date_converted, interval_days)
        objects = []  # type: List[BidAskQuote]
        for vo in vos:
            obj = BidAskQuote.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_trades_by_max_date(self, security_id, max_date, interval_days):
        # type: (int, datetime, int) -> List[Trade]
        """Arguments:
               security_id (int): &nbsp;
               max_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.Trade
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)

        vos = self._service.getTradesByMaxDate(security_id, max_date_converted, interval_days)
        objects = []
        for vo in vos:
            obj = Trade.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_trades_by_min_date(self, security_id, min_date, interval_days):
        # type: (int, datetime, int) -> List[Trade]
        """Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               interval_days (int): &nbsp;
           Returns:
               List of algotrader_com.domain.market_data.Trade
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)

        vos = self._service.getTradesByMinDate(security_id, min_date_converted, interval_days)
        objects = []
        for vo in vos:
            obj = Trade.convert_from_vo(vo)
            objects.append(obj)
        return objects

    # noinspection PyIncorrectDocstring
    def get_bars_by_security_min_date_max_date_and_bar_size2(self, security_id, min_date, max_date, bar_size,
                                                             historical_data_type, properties):
        # type: (int, datetime, datetime, str, str, Dict[str,str]) -> List[Bar]
        """Returns bars of the specified security security_id between min_date and max_date
           by first checking if data is available in the database and then as a fall back download data
           through the external historical data service.
           Note: if there is an data available in the database (potentially covering only part of the time interval)
           no external data will be retrieved.

           Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               max_date (datetime): &nbsp;
               .. include:: ../bar_sizes.txt
               historical_data_type (str): One of the values: TRADES, MIDPOINT, BID, ASK, BID_ASK, BEST_BID, BEST_ASK.
               properties (Dict[str]): Arbitrary properties that should be added to the request.
           Returns:
               List of algotrader_com.domain.market_data.Bar
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)
        historical_data_type_enum = self._gateway.jvm.HistoricalDataType.valueOf(historical_data_type)

        _map = self._gateway.jvm.HashMap()
        for key in properties:
            _map.put(key, properties[key])

        vos = self._service.getBarsBySecurityMinDateMaxDateAndBarSize(security_id, min_date_converted,
                                                                      max_date_converted,
                                                                      bar_size_enum,
                                                                      historical_data_type_enum, _map)
        bars = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            bar = Bar.convert_from_json_object(_dict)
            bars.append(bar)
        return bars

    # noinspection PyIncorrectDocstring
    def download_historical_bars(self, security_id, min_date, max_date, bar_size, historical_data_type, properties):
        # type: (int, datetime, datetime, str, str, Dict[str,str]) -> List[Bar]
        """Downloads historical bars for the specified security.

           Arguments:
               security_id (int): &nbsp;
               min_date (datetime): &nbsp;
               max_date (datetime): &nbsp;
               .. include:: ../bar_sizes.txt
               historical_data_type (str): One of the values: TICK, BAR, BID, ASK, BIDASK, TRADE, ORDERBOOK, CUSTOM, DIVIDENDS.
               properties (Dict[str]): Arbitrary properties that should be added to the request.
           Returns:
               List of algotrader_com.domain.market_data.Bar
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)
        historical_data_type_enum = self._gateway.jvm.HistoricalDataType.valueOf(historical_data_type)

        _map = self._gateway.jvm.HashMap()
        for key in properties:
            _map.put(key, properties[key])

        vos = self._service.downloadHistoricalBars(security_id, min_date_converted, max_date_converted,
                                                   bar_size_enum, historical_data_type_enum, _map)

        bars = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            bar = Bar.convert_from_json_object(_dict)
            bars.append(bar)
        return bars

    def download_historical_ticks(self, security_id, min_date, max_date, historical_data_type, properties):
        # type: (int, datetime, datetime, str, Dict[str,str]) -> List[Tick]
        """Retrieves historical ticks for the specified security.

           Arguments:
               security_id (int): &nbsp;
               min_date (datetime): The start date from which the historical ticks should be retrieved.
               max_date (datetime): The end date up to which the historical ticks should be retrieved.
               historical_data_type (str): One of the values: TRADES, MIDPOINT, BID, ASK, BID_ASK, BEST_BID, BEST_ASK.
               properties (Dict[str]): Arbitrary properties that should be added to the request.
           Returns:
               List of algotrader_com.domain.market_data.Tick
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        historical_data_type_enum = self._gateway.jvm.HistoricalDataType.valueOf(historical_data_type)

        _map = self._gateway.jvm.HashMap()
        for key in properties:
            _map.put(key, properties[key])

        vos = self._service.downloadHistoricalTicks(security_id, min_date_converted, max_date_converted,
                                                    historical_data_type_enum, _map)

        ticks = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = Tick.convert_from_json_object(_dict)
            ticks.append(tick)
        return ticks

    # noinspection PyIncorrectDocstring
    def store_historical_bars(self, security_id, min_date, max_date, bar_size, historical_data_type, replace,
                              properties):
        # type: (int, datetime, datetime, str, str, bool, Dict[str,str]) -> None
        """Downloads historical bars for the specified security and stores them in the database.


           Arguments:
               security_id (int): &nbsp;
               min_date (datetime): The start date from which the historical bars should be retrieved.
               max_date (datetime): The end date up to which the historical bars should be retrieved.
               .. include:: ../bar_sizes.txt
               historical_data_type (str): One of the values: TRADES, MIDPOINT, BID, ASK, BID_ASK, BEST_BID, BEST_ASK.
               replace (bool): Should the existing bars be replaced in the database?
               properties (Dict[str]): Arbitrary properties that should be added to the request.
           Returns:
               List of algotrader_com.domain.market_data.Bar
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)
        historical_data_type_enum = self._gateway.jvm.HistoricalDataType.valueOf(historical_data_type)

        _map = self._gateway.jvm.HashMap()
        for key in properties:
            _map.put(key, properties[key])
        self._service.storeHistoricalBars(security_id, min_date_converted, max_date_converted,
                                          bar_size_enum, historical_data_type_enum, replace, _map)

    def get_supported_bar_sizes(self):
        # type: () -> List[int]
        """Returns a list of supported durations as integers representing number of milliseconds in each.

           Returns:
               List of int: List of milliseconds durations"""
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        durations = self._service.getSupportedBarSizes()
        strs = []
        for duration in durations:
            millis = int(duration.toMillis())
            strs.append(millis)
        return strs

    # noinspection PyIncorrectDocstring
    def download_and_persist_historical_bars(self, security_id, start_date, end_date, bar_size, historical_data_type,
                                             properties):
        # type: (int, datetime, datetime, str, str, Dict[str,str]) -> None
        """Downloads historical bars for the specified security and stores them in the database.

           Arguments:
               security_id (int): &nbsp;
               start_date (datetime): The start date from which the historical ticks should be retrieved.
               end_date (datetime): The end date up to which the historical ticks should be retrieved.
               .. include:: ../bar_sizes.txt
               historical_data_type (str): One of the values: TRADES, MIDPOINT, BID, ASK, BID_ASK, BEST_BID, BEST_ASK.
               properties (Dict[str]): Arbitrary properties that should be added to the request.
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(start_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(end_date, self._gateway)
        historical_data_type_enum = self._gateway.jvm.HistoricalDataType.valueOf(historical_data_type)

        _map = self._gateway.jvm.HashMap()
        for key in properties:
            _map.put(key, properties[key])
        bar_size_enum = self._gateway.jvm.Duration.valueOf(bar_size)

        self._service.downloadAndPersistHistoricalBars(security_id, min_date_converted, max_date_converted,
                                                       bar_size_enum, historical_data_type_enum, _map)

    def download_asks(self, security_id, start_date, end_date):
        # type: (int, datetime, datetime) -> List[Ask]
        """
           Arguments:
               security_id (int): &nbsp;
               start_date (datetime): The start date from which the historical ticks should be retrieved.
               end_date (datetime): The end date up to which the historical ticks should be retrieved.
           Returns:
               List of algotrader_com.domain.market_data.Ask
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(start_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(end_date, self._gateway)

        vos = self._service.downloadAsks(security_id, min_date_converted, max_date_converted)

        quotes = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = Ask.convert_from_json_object(_dict)
            quotes.append(tick)
        return quotes

    def download_bids(self, security_id, start_date, end_date):
        # type: (int, datetime, datetime) -> List[Bid]
        """
           Arguments:
               security_id (int): &nbsp;
               start_date (datetime): The start date from which the historical ticks should be retrieved.
               end_date (datetime): The end date up to which the historical ticks should be retrieved.
           Returns:
               List of algotrader_com.domain.market_data.Bid
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(start_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(end_date, self._gateway)

        vos = self._service.downloadBids(security_id, min_date_converted, max_date_converted)

        quotes = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = Bid.convert_from_json_object(_dict)
            quotes.append(tick)
        return quotes

    def download_bid_asks(self, security_id, start_date, end_date):
        # type: (int, datetime, datetime) -> List[BidAskQuote]
        """
           Arguments:
               security_id (int): &nbsp;
               start_date (datetime): The start date from which the historical ticks should be retrieved.
               end_date (datetime): The end date up to which the historical ticks should be retrieved.
           Returns:
               List of algotrader_com.domain.market_data.BidAskQuote
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(start_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(end_date, self._gateway)

        vos = self._service.downloadBidAsks(security_id, min_date_converted, max_date_converted)

        quotes = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = BidAskQuote.convert_from_json_object(_dict)
            quotes.append(tick)
        return quotes

    def download_trades(self, security_id, start_date, end_date):
        # type: (int, datetime, datetime) -> List[Trade]
        """
           Arguments:
               security_id (int): &nbsp;
               start_date (datetime): The start date from which the historical ticks should be retrieved.
               end_date (datetime): The end date up to which the historical ticks should be retrieved.
           Returns:
               List of algotrader_com.domain.market_data.Trade
        """
        if self._service is None:
            raise Exception("AlgoTrader historical data service not loaded.")
        min_date_converted = Conversions.python_datetime_to_zoneddatetime(start_date, self._gateway)
        max_date_converted = Conversions.python_datetime_to_zoneddatetime(end_date, self._gateway)

        vos = self._service.downloadTrades(security_id, min_date_converted, max_date_converted)

        quotes = []
        for vo_json in vos:
            _dict = Conversions.unmarshall(vo_json)
            tick = Trade.convert_from_json_object(_dict)
            quotes.append(tick)
        return quotes
