import time
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, Any

import jsonpickle
import pytz
import stringcase as stringcase
from py4j.clientserver import ClientServer

from tzlocal import get_localzone

# noinspection PyAbstractClass
from py4j.java_gateway import JavaObject
from pytz import tzinfo  # type: ignore


# noinspection PyAbstractClass
class _DecimalHandler(jsonpickle.handlers.BaseHandler):
    """Internal class for Decimals/BigDecimals JSON marshalling support."""

    def flatten(self, obj, data):
        if obj is None:
            return None
        return obj.__str__()  # Convert to json friendly format


# noinspection PyAbstractClass
class _DatetimeHandler(jsonpickle.handlers.BaseHandler):
    """Internal class for datetime JSON marshalling support. Uses epoch milliseconds."""

    def flatten(self, obj, data):
        # type: (datetime, Any) -> int
        return Conversions.python_datetime_to_millis(obj)


jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
jsonpickle.handlers.registry.register(datetime, _DatetimeHandler)


class Conversions:
    """Internal class with convenience methods."""

    def __init__(self):
        pass

    @staticmethod
    def unmarshall(json):
        # type: (str) -> Dict
        """
           Args:
               json (str): JSON string
           Returns:
               Dict: Deserialized dictionary object
        """
        if json is None:
            # noinspection PyTypeChecker
            return None
        return jsonpickle.decode(json)

    @staticmethod
    def marshall(obj, class_name=None):
        # type: (Any, str) -> str
        """
           Args:
               obj: any object
               class_name (str): Used by algotrader_com.order.Order child classes to include @class field with Java class name
           Returns:
               str: JSON string
        """
        if class_name is not None:
            obj._class_name = class_name
        json_value = jsonpickle.dumps(obj, unpicklable=False)
        if class_name is not None:
            delattr(obj, "_class_name")
        if class_name is not None:
            json_value = json_value.replace("_class_name", "@class")
        if hasattr(obj, "__dict__"):
            for _property in obj.__dict__:
                camel_cased = stringcase.camelcase(_property)
                json_value = json_value.replace("\"" + _property + "\"", "\"" + camel_cased + "\"")
        return json_value

    @staticmethod
    def float_to_decimal(float_number):
        # type: (float) -> Decimal
        """
           Args:
               float_number (float): &nbsp;
           Returns:
               Decimal
        """
        if float_number is None:
            # noinspection PyTypeChecker
            return None
        return Decimal(str(float_number))

    @staticmethod
    def epoch_millis_to_python_datetime(millis):
        # type: (int) -> datetime
        """
           Args:
               millis (int): epoch time in milliseconds
           Returns:
               datetime
        """
        if millis is None:
            # noinspection PyTypeChecker
            return None
        _datetime = datetime.fromtimestamp(millis // 1000).replace(microsecond=millis % 1000 * 1000)
        return get_localzone().localize(_datetime)

    @staticmethod
    def zoned_date_time_to_python_datetime(java_zoned_date_time):
        # type: (JavaObject) -> datetime
        """
           Args:
               java_zoned_date_time: java.time.ZonedDateTime py4j proxy Java object
           Returns:
               datetime
        """
        if java_zoned_date_time is None:
            # noinspection PyTypeChecker
            return None
        time_zone_str = java_zoned_date_time.getZone().toString()
        time_zone = pytz.timezone(time_zone_str)
        seconds = java_zoned_date_time.toInstant().toEpochMilli() / 1000.0
        _datetime = datetime.fromtimestamp(seconds, time_zone)
        return _datetime

    @staticmethod
    def java_instant_to_python_datetime(java_instant):
        # type: (JavaObject) -> datetime
        """
           Args:
               java_instant: java.time.Instant py4j proxy Java object
           Returns:
               datetime
        """
        if java_instant is None:
            # noinspection PyTypeChecker
            return None
        _datetime = datetime.fromtimestamp(java_instant.getEpochSecond(), Conversions.get_local_time_zone())
        return _datetime

    @staticmethod
    def python_datetime_to_java_instant(date_time, py4jgateway):
        # type: (datetime, ClientServer) -> JavaObject
        """
           Args:
               date_time (datetime): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               java.time.Instant py4j proxy Java object
        """
        if date_time is None:
            # noinspection PyTypeChecker
            return None
        millis = Conversions.python_datetime_to_millis(date_time)

        instant = py4jgateway.jvm.Instant.ofEpochMilli(millis)
        return instant

    @staticmethod
    def get_local_time_zone():
        # type: () -> tzinfo
        """

        Returns:
            tzinfo
        """

        offset_hour = int(time.localtime().tm_gmtoff) / 3600

        return pytz.timezone('Etc/GMT%+d' % -offset_hour)

    @staticmethod
    def local_date_to_python_datetime(java_local_date, py4jgateway):
        # type: (JavaObject, ClientServer) -> datetime
        """
           Args:
               java_local_date: java.time.ZonedDateTime py4j proxy Java object
               py4jgateway (ClientServer): &nbsp;
           Returns:
               datetime
        """
        if java_local_date is None:
            # noinspection PyTypeChecker
            return None
        zone_id = py4jgateway.jvm.ZoneId.systemDefault()
        seconds = java_local_date.atStartOfDay(zone_id).toInstant().toEpochMilli() / 1000.0
        _datetime = datetime.fromtimestamp(seconds)

        local_tz = pytz.timezone(zone_id.toString())
        with_timezone = local_tz.localize(_datetime)
        return with_timezone

    @staticmethod
    def python_datetime_to_localdate(date_time, py4jgateway):
        # type: (datetime, ClientServer) -> JavaObject
        """
           Args:
               date_time (datetime): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               java.time.LocalDate proxy Java object
        """
        if date_time is None:
            # noinspection PyTypeChecker
            return None
        zoneddatetime = Conversions.python_datetime_to_zoneddatetime(date_time, py4jgateway)
        localdate = zoneddatetime.toLocalDate()
        return localdate

    @staticmethod
    def python_datetime_to_millis(date_time):
        # type: (datetime) -> Optional[int]
        """
           Args:
               date_time (datetime): &nbsp;
           Returns:
               Optional[int] : epoch time in milliseconds
        """
        if date_time is None:
            return None
        millis = int(date_time.timestamp() * 1000)
        return millis

    @staticmethod
    def python_datetime_to_zoneddatetime(date_time, py4jgateway):
        # type: (datetime, ClientServer) -> JavaObject
        """
           Args:
               date_time (datetime): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               java.time.ZonedDateTime py4j proxy Java object
        """
        if date_time is None:
            # noinspection PyTypeChecker
            return None
        millis = Conversions.python_datetime_to_millis(date_time)

        # ZonedDateTime.ofInstant(Instant.ofEpochMilli(millis), ZoneId.systemDefault());
        instant = py4jgateway.jvm.Instant.ofEpochMilli(millis)
        zone_id = py4jgateway.jvm.ZoneId.systemDefault()
        zoned_date_time = py4jgateway.jvm.ZonedDateTime.ofInstant(instant, zone_id)

        return zoned_date_time

    @staticmethod
    def convert_to_side_enum(side_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               side_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.enumeration.Side py4j proxy Java enum
        """
        if side_str is None:
            # noinspection PyTypeChecker
            return None
        side = py4jgateway.jvm.Side.valueOf(side_str)
        return side

    @staticmethod
    def convert_to_status_enum(status_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               status_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.enumeration.Status py4j proxy Java enum
        """
        if status_str is None:
            # noinspection PyTypeChecker
            return None
        status = py4jgateway.jvm.Status.valueOf(status_str)
        return status

    @staticmethod
    def convert_to_tif_enum(tif_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               tif_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.api.trading.TIF py4j proxy Java enum
        """
        if tif_str is None:
            # noinspection PyTypeChecker
            return None
        tif = py4jgateway.jvm.ch.algotrader.api.trading.TIF.valueOf(tif_str)
        return tif

    @staticmethod
    def convert_to_account_service_type_enum(account_service_type_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               account_service_type_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.enumeration.AccountServiceType py4j proxy Java enum
        """
        if account_service_type_str is None:
            # noinspection PyTypeChecker
            return None
        account_service_type = py4jgateway.jvm.AccountServiceType.valueOf(account_service_type_str)
        return account_service_type

    @staticmethod
    def convert_to_connector_descriptor(connector_descriptor_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               connector_descriptor_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.api.connector.application.ConnectorDescriptor
        """
        if connector_descriptor_str is None:
            # noinspection PyTypeChecker
            return None
        connector_descriptor = py4jgateway.jvm.ch.algotrader.api.connector.application.\
            ConnectorDescriptor(connector_descriptor_str)
        return connector_descriptor

    @staticmethod
    def convert_to_generic_event_type(type_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               type_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.api.domain.genericevent.GenericEventType
        """
        if type_str is None:
            # noinspection PyTypeChecker
            return None
        generic_event_type = py4jgateway.jvm.ch.algotrader.api.domain.genericevent. \
            GenericEventType(type_str)
        return generic_event_type

    @staticmethod
    def convert_to_adapter_type_enum(adapter_type_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               adapter_type_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.enumeration.AdapterType py4j proxy Java enum
        """
        if adapter_type_str is None:
            # noinspection PyTypeChecker
            return None
        adapter_type = py4jgateway.jvm.AdapterType.valueOf(adapter_type_str)
        return adapter_type

    @staticmethod
    def convert_to_market_data_event_type_enum(market_data_event_type_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               market_data_event_type_str (str): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.enumeration.MarketDataEventType py4j proxy Java enum
        """
        if market_data_event_type_str is None:
            # noinspection PyTypeChecker
            return None
        market_data_event_type = py4jgateway.jvm.MarketDataEventType.valueOf(market_data_event_type_str)
        return market_data_event_type

    @staticmethod
    def get_java_object_to_string(java_object):
        # type: (JavaObject) -> Optional[str]
        if java_object is None:
            return None
        else:
            return java_object.toString()

    @staticmethod
    def convert_to_market_data_level_enum(market_data_level_str, py4jgateway):
        # type: (str, ClientServer) -> JavaObject
        """
           Args:
               market_data_level_str (str): L1, L2, Zero, L1L2
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.enumeration.MarketDataEventType py4j proxy Java enum
        """
        if market_data_level_str is None:
            # noinspection PyTypeChecker
            return None
        market_data_level = py4jgateway.jvm.MarketDataLevel.valueOf(market_data_level_str)
        return market_data_level
