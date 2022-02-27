from datetime import datetime

from py4j.java_gateway import JavaObject

from algotrader_com.domain.conversions import Conversions


class DataSourceConfig:
    """Mirrors DataSourceConfig Java class.

        Attributes:
           data_source_type (str): One of the values: DB, CSV
           market_data_event_type (str): One of the values: TICK, BAR, BID, ASK, BIDASK, TRADE, ORDERBOOK, CUSTOM, DIVIDENDS.
           data_files_dir (str): path
           subset_name (str): &nbsp;
           .. include:: ../bar_sizes.txt
           batch_size (int): &nbsp;
           custom_query (str): &nbsp;
           min_date (datetime): &nbsp;
           max_date (datetime): &nbsp;
           generic_event_type (str): &nbsp;
    """

    def __init__(self, data_source_type=None, market_data_event_type=None, data_files_dir=None, subset_name=None,
                 bar_size=None, batch_size=None, custom_query=None,
                 min_date=None, max_date=None, generic_event_type=None):
        # type: (str, str, str, str, str, int, str, datetime, datetime, str) -> None
        self.data_source_type = data_source_type
        self.market_data_event_type = market_data_event_type
        self.data_files_dir = data_files_dir
        self.subset_name = subset_name
        self.bar_size = bar_size
        self.batch_size = batch_size
        self.custom_query = custom_query
        self.min_date = min_date
        self.max_date = max_date
        self.generic_event_type = generic_event_type

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> DataSourceConfig
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.config.DataSourceConfig): &nbsp;
           Returns:
               DataSourceConfig
        """

        data_source_type = None
        if vo.getDataSourceType() is not None:
            data_source_type = vo.getDataSourceType().toString()
        market_data_event_type = None
        if vo.getMarketDataEventType() is not None:
            market_data_event_type = vo.getMarketDataEventType().toString()
        data_files_dir = None
        if vo.getDataFilesDir() is not None:
            data_files_dir = vo.getDataFilesDir().getAbsolutePath()
        subset_name = vo.getSubsetName()
        bar_size = None
        if vo.getBarSize() is not None:
            bar_size = vo.getBarSize().toString()
        batch_size = vo.getBatchSize()
        custom_query = vo.getCustomQuery()
        min_date = Conversions.zoned_date_time_to_python_datetime(vo.getMinDate())
        max_date = Conversions.zoned_date_time_to_python_datetime(vo.getMaxDate())
        generic_event_type = vo.getGenericEventType()
        config = DataSourceConfig(data_source_type, market_data_event_type, data_files_dir, subset_name, bar_size,
                                  batch_size, custom_query, min_date, max_date, generic_event_type)
        return config


