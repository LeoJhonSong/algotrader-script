from datetime import datetime
from typing import List

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.security import Future


class FutureService:
    """Delegates to pythonFutureService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.getPythonFutureService()

    def create_future(self, security_family_id, expiration, underlying_security_id):
        # type: (int, datetime, int) -> Future
        """Creates Future basing on defined parameters.

        Arguments:
            security_family_id (int): ID to use
            expiration (datetime): expiration of the future
            underlying_security_id (int): id of underlying security of the new future"""
        expiration_java = Conversions.python_datetime_to_localdate(expiration, self._gateway)
        vo = self._service.createFuture(security_family_id, expiration_java, underlying_security_id)
        obj = Future.convert_from_vo(vo, self._gateway)
        return obj

    def get_future_by_min_expiration(self, security_family_id, target_expiration_date):
        # type: (int, datetime) -> Future
        """Get the first Future with expiration_date after the specified target_expiration_date
            and security_family_id

           Arguments:
               security_family_id (int): &nbsp;
               target_expiration_date (datetime): &nbsp;
           Returns:
               algotrader_com.domain.security.Future
            """
        target_expiration_date_java = \
            Conversions.python_datetime_to_localdate(target_expiration_date, self._gateway)
        vo = self._service \
            .getFutureByMinExpiration(security_family_id, target_expiration_date_java)
        obj = Future.convert_from_vo(vo, self._gateway)
        return obj

    def get_future_by_expiration(self, security_family_id, expiration_date):
        # type: (int, datetime) -> Future
        """Get the first Future by its security_family_id and expiration_date

           Arguments:
               security_family_id (int): &nbsp;
               expiration_date (datetime): &nbsp;
           Returns:
               algotrader_com.domain.security.Future
        """
        expiration_date_java = \
            Conversions.python_datetime_to_localdate(expiration_date, self._gateway)
        vo = self._service \
            .getFutureByExpiration(security_family_id, expiration_date_java)
        obj = Future.convert_from_vo(vo, self._gateway)
        return obj

    def get_future_by_month_year(self, security_family_id, year, month):
        # type: (int, int, int) -> List[Future]
        """Gets all futures by their security_family_id and maturity month and year

           Arguments:
               security_family_id (int): &nbsp;
               year (int): &nbsp;
               month (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Future
        """
        vos = self._service.getFutureByMonthYear(security_family_id, year, month)
        objs = []
        for vo in vos:
            obj = Future.convert_from_vo(vo, self._gateway)
            objs.append(obj)
        return objs

    def get_futures_by_min_expiration(self, security_family_id, min_expiration_date):
        # type: (int, datetime) -> List[Future]
        """Gets all futures by their security_family_id and maturity month and year

           Arguments:
               security_family_id (int): &nbsp;
               min_expiration_date (datetime): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Future
        """
        min_expiration_date_java = Conversions.python_datetime_to_localdate(min_expiration_date, self._gateway)
        vos = self._service \
            .getFuturesByMinExpiration(security_family_id, min_expiration_date_java)
        objs = []
        for vo in vos:
            obj = Future.convert_from_vo(vo, self._gateway)
            objs.append(obj)
        return objs
