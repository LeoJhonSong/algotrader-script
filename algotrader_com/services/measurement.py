from datetime import datetime
from typing import Any

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import Measurement


class MeasurementService:
    """Delegates to pythonMeasurementService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.getPythonMeasurementService()

    def create_measurement(self, portfolio_name, name, value):
        # type: (str, str, Any) -> Measurement
        """Creates a measurement with the specified name and value assigned to the specified portfolio.
           The date of the measurement is set to the current time.

           Arguments:
               portfolio_name (str): &nbsp;
               name (str): &nbsp;
               value: Any value type.
           Returns:
               algotrader_com.domain.entity.Measurement
           """
        vo_json = self._service.createMeasurement(portfolio_name, name, value)
        _dict = Conversions.unmarshall(vo_json)
        measurement = Measurement.convert_from_json(_dict)
        return measurement

    def create_measurement_with_date(self, portfolio_name, name, date, value):
        # type: (str, str, datetime, "Any") -> Measurement
        """Creates a measurement with the specified name, date and value assigned to the specified portfolio.

           Arguments:
               portfolio_name (str): &nbsp;
               name (str): &nbsp;
               date (datetime): &nbsp;
               value: Any value type;
           Returns:
               algotrader_com.domain.entity.Measurement
        """
        millis = Conversions.python_datetime_to_millis(date)
        vo_json = self._service.createMeasurement(portfolio_name, name, millis, value)
        _dict = Conversions.unmarshall(vo_json)
        measurement = Measurement.convert_from_json(_dict)
        return measurement

    def delete_measurement(self, measurement_id):
        # type: (int) -> None
        """Deletes the specified measurement.

            Arguments:
                measurement_id (int): &nbsp;
        """
        self._service.deleteMeasurement(measurement_id)
