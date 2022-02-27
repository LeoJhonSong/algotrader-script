from datetime import datetime
from decimal import Decimal

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.security import Option


# noinspection PyShadowingBuiltins
class OptionService:
    """Delegates to pythonOptionService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonOptionService()

    def hedge_delta(self, underlying_id=None, interest=None, dividend=None):
        # type: (int, float, float) -> None
        """ Performs a Delta Hedge of all Securities of the specified 'underlying_id'.

           Arguments:
               underlying_id (int): &nbsp;
               interest (Decimal): &nbsp;
               dividend (Decimal): &nbsp;
        """
        self._service.hedgeDelta(underlying_id, interest, dividend)

    def create_option(self, security_family_id=None, expiration_date=None, strike=None, type=None):
        # type: (int, datetime, Decimal, str) -> Option
        """ Creates an Option with the specified security_family_id, expiration_date, strike and type.

           Arguments:
               security_family_id (int): &nbsp;
               expiration_date (datetime): &nbsp;
               strike (Decimal): &nbsp;
               type (str): CALL/PUT
           Returns:
               algotrader_com.domain.security.Option
        """
        expiration_date_java = Conversions.python_datetime_to_localdate(expiration_date, self._gateway)
        type_enum = self._gateway.jvm.OptionType.valueOf(type)
        vo = self._service.createOption(security_family_id, expiration_date_java, strike, type_enum)
        option = Option.convert_from_vo(vo, self._gateway)
        return option

    def get_option_by_expiration_strike_and_type(self, security_family_id=None, expiration_date=None, strike=None,
                                                 type=None):
        # type: (int, datetime, Decimal, str) -> Option
        """ Gets an Option by the specified security_family_id, expiration_date, strike, type.

           Arguments:
               security_family_id (int): &nbsp;
               expiration_date (datetime): &nbsp;
               strike (Decimal): &nbsp;
               type (str): CALL/PUT
           Returns:
               algotrader_com.domain.security.Option
        """
        expiration_date_java = Conversions.python_datetime_to_localdate(expiration_date, self._gateway)
        type_enum = self._gateway.jvm.OptionType.valueOf(type)
        vo = self._service.getOptionByExpirationStrikeAndType(security_family_id, expiration_date_java, strike,
                                                              type_enum)
        if vo is None:
            # noinspection PyTypeChecker
            return None
        option = Option.convert_from_vo(vo, self._gateway)
        return option

    def get_option_by_min_expiration_min_strike_and_type(self, security_family_id=None, min_expiration_date=None,
                                                         min_strike=None, type=None):
        # type: (int, datetime, Decimal, str) -> Option
        """ Gets the first Options of the give security_family_id and _type that expires after the specified
            min_expiration_date and has a strike price larger than the min_strike.

           Arguments:
               security_family_id (int): &nbsp;
               min_expiration_date (datetime): &nbsp;
               min_strike (Decimal): &nbsp;
               type (str): CALL/PUT
           Returns:
               algotrader_com.domain.security.Option
        """
        min_expiration_date_java = Conversions.python_datetime_to_zoneddatetime(min_expiration_date, self._gateway)
        type_enum = self._gateway.jvm.OptionType.valueOf(type)
        vo = self._service.getOptionByMinExpirationMinStrikeAndType(
            security_family_id, min_expiration_date_java, min_strike, type_enum)
        if vo is None:
            # noinspection PyTypeChecker
            return None
        option = Option.convert_from_vo(vo, self._gateway)
        return option

    def get_option_by_min_expiration_max_strike_and_type(self, security_family_id=None, min_expiration_date=None,
                                                         max_strike=None, type=None):
        # type: (int, datetime, Decimal, str) -> Option
        """ Gets the first Options of the give security_family_id and _type that expires after the specified
            min_expiration_date and has a strike price smaller than the max_strike.

           Arguments:
               security_family_id (int): &nbsp;
               min_expiration_date (datetime): &nbsp;
               max_strike (Decimal): &nbsp;
               type (str): CALL/PUT
           Returns:
               algotrader_com.domain.security.Option
        """
        min_expiration_date_java = Conversions.python_datetime_to_zoneddatetime(min_expiration_date, self._gateway)
        type_enum = self._gateway.jvm.OptionType.valueOf(type)
        vo = self._service.getOptionByMinExpirationMaxStrikeAndType(security_family_id, min_expiration_date_java,
                                                                    max_strike, type_enum)
        if vo is None:
            # noinspection PyTypeChecker
            return None
        option = Option.convert_from_vo(vo, self._gateway)
        return option
