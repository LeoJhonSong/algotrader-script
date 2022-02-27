from datetime import datetime
from decimal import Decimal
from typing import Callable, List, Optional

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import Transaction, Position, PortfolioValue, Balance, FxExposure, \
    PortfolioValueDeltaSummary
from algotrader_com.domain.utils import JsonPredicate


# noinspection PyShadowingBuiltins
class PortfolioValueService:
    """Delegates to pythonPortfolioValueService object methods in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonPortfolioValueService()

    def get_transactions_by_filter(self, filter, date):
        # type: (Callable[[dict], bool], datetime) -> List[Transaction]
        """Gets all transactions by an arbitrary filter up to the given date.
              Python use example::
                  <i>python_to_at_entry_point.portfolio_value_service.get_transactions_by_filter(lambda t: t["currency"] == "USD", datetime.datetime.now())</i>

           Arguments:
               filter (Callable[[dict], bool]): function taking transaction dictionary as input, returning bool value &nbsp;
               date (datetime): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Transaction
        """
        zoned_date_time = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)

        transaction_vo_jsons = self._service.getTransactionsByFilter(JsonPredicate(filter), zoned_date_time)

        transactions = []
        for _json in transaction_vo_jsons:
            _dict = Conversions.unmarshall(_json)
            transaction = Transaction.convert_from_json(_dict)
            transactions.append(transaction)
        return transactions

    def get_open_positions_by_filter(self, position_filter, transaction_filter, date):
        # type: (Callable[[dict], bool], Callable[[dict], bool], datetime) -> List[Position]
        """Gets all open positions on the specified date by an arbitrary filter by
           aggregating all relevant transactions.
             Python use example::
                 <i>python_to_at_entry_point.portfolio_value_service.get_open_positions_by_filter(lambda t: t["currency"] == "USD", datetime.datetime.now())</i>

           Arguments:
               position_filter (Callable[[dict], bool]): function taking position dictionary as input, returning bool value &nbsp;
               transaction_filter (Callable[[dict], bool]): function taking transaction dictionary as input, returning bool value &nbsp;
               date (datetime): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Position
        """
        zoned_date_time = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)

        position_vo_jsons = self._service.getOpenPositionsByFilter(JsonPredicate(position_filter),
                                                                   JsonPredicate(transaction_filter), zoned_date_time)

        positions = []
        for _json in position_vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_cash_balance(self):
        # type: () -> Decimal
        """Gets the cash balance of the entire system.

            Returns:
                Decimal
        """
        return self._service.getCashBalance()

    def get_cash_balance_of_strategy_name(self, strategy_name):
        # type: (str) -> Decimal
        """Gets the cash balance of the specified strategy.

           Arguments:
               strategy_name (str): &nbsp;
           Returns:
               Decimal
        """
        return self.get_cash_balance_of_portfolio_name(strategy_name)

    def get_cash_balance_of_portfolio_name(self, portfolio_name):
        # type: (str) -> Decimal
        """Gets the cash balance of the specified portfolio.

           Arguments:
               portfolio_name (str): &nbsp;
           Returns:
               Decimal
        """
        return self._service.getCashBalance(portfolio_name)

    def get_cash_balance_on_date(self, date):
        # type: (datetime) -> Decimal
        """Gets the cash balance of the entire system on the specified date.

           Arguments:
               date (datetime): &nbsp;
           Returns:
               Decimal
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getCashBalance(date_java)

    def get_cash_balance_of_strategy_on_date(self, strategy_name, date):
        # type: (str, datetime) -> Decimal
        """Gets the cash balance of the specified strategy on the specified date.

           Arguments:
               strategy_name (str): &nbsp;
               date (datetime): &nbsp;
           Returns:
               Decimal
        """
        return self.get_cash_balance_of_strategy_on_date(strategy_name, date)

    def get_cash_balance_of_portfolio_on_date(self, portfolio_name, date):
        # type: (str, datetime) -> Decimal
        """Gets the cash balance of the specified portfolio on the specified date.

           Arguments:
               portfolio_name (str): &nbsp;
               date (datetime): &nbsp;
           Returns:
               Decimal
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getCashBalance(portfolio_name, date_java)

    def get_cash_balance_by_filter(self, filter, date):
        # type: (Callable[[dict], bool], datetime) -> List[Position]
        """Gets the cash balance on the specified date by an arbitrary filter by aggregating all
            relevant transactions.
           Note: The current value of Forex positions will not be taken into account.

             Python use example::
                 <i>python_to_at_entry_point.portfolio_value_service.get_cash_balance_by_filter(lambda t: t["currency"] == "USD", datetime.datetime.now())</i>

           Arguments:
               filter (Callable[[dict], bool]): function taking transaction dictionary as input, returning bool value &nbsp;
               date (datetime): &nbsp;
           Returns:
               Decimal
          """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getCashBalance(JsonPredicate(filter), date_java)

    def get_market_value(self):
        # type: () -> Decimal
        """Gets the total market value of all non-FX Positions of the entire system.

           Returns:
               Decimal
        """
        return self._service.getMarketValue()

    def get_market_value_of_strategy(self, strategy_name):
        # type: (str) -> Decimal
        """Gets the total market value of all non-FX Positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self.get_market_value_of_portfolio(strategy_name)

    def get_market_value_of_portfolio(self, portfolio_name):
        # type: (str) -> Decimal
        """Gets the total market value of all non-FX Positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getMarketValue(portfolio_name)

    def get_market_value_on_date(self, date):
        # type: (datetime) -> Decimal
        """Gets the total market value of all non-FX Positions of the entire system on the specified date.

            Arguments:
                date (datetime): &nbsp;
            Returns:
                Decimal
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getMarketValue(date_java)

    def get_market_value_of_strategy_on_date(self, strategy_name, date):
        # type: (str, datetime) -> Decimal
        """Gets the total market value of all non-FX Positions of the specified strategy on the specified date.

            Arguments:
                strategy_name (str): &nbsp;
                date (datetime): &nbsp;
            Returns:
                Decimal
        """
        return self.get_market_value_of_portfolio_on_date(strategy_name, date)

    def get_market_value_of_portfolio_on_date(self, portfolio_name, date):
        # type: (str, datetime) -> Decimal
        """Gets the total market value of all non-FX Positions of the specified portfolio on the specified date.

            Arguments:
                portfolio_name (str): &nbsp;
                date (datetime): &nbsp;
            Returns:
                Decimal
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getMarketValue(portfolio_name, date_java)

    def get_market_value_by_filter(self, filter, date):
        # type: (Callable[[dict], bool], datetime) -> Decimal
        """Gets the total market value of all non-FX Positions of the specified portfolio on the specified date.

             Python use example::
                 <i>python_to_at_entry_point.portfolio_value_service.get_market_value_by_filter("t.id=:tid", datetime.datetime.now(), [NamedParam("tid", 2)])</i>

           Arguments:
               filter (Callable[[dict], bool]): function taking position dictionary as input, returning bool value &nbsp;
               date (datetime): &nbsp;
           Returns:
               Decimal
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getMarketValue(JsonPredicate(filter), date_java)

    def get_realized_pl(self):
        # type: () -> Decimal
        """Gets the total realized profit and loss of all positions of the entire system.

            Returns:
                Decimal
        """
        return self._service.getRealizedPL()

    def get_realized_pl_of_strategy(self, strategy_name):
        # type: (str) -> Decimal
        """Gets the total realized profit and loss of all positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self.get_realized_pl_of_portfolio(strategy_name)

    def get_realized_pl_of_portfolio(self, portfolio_name):
        # type: (str) -> Decimal
        """Gets the total realized profit and loss of all positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getRealizedPL(portfolio_name)

    def get_unrealized_pl(self):
        # type: () -> Decimal
        """Gets the total unrealized profit and loss of all positions of the entire system.

            Returns:
                Decimal
        """
        return self._service.getUnrealizedPL()

    def get_unrealized_pl_of_strategy(self, strategy_name):
        # type: (str) -> Decimal
        """Gets the total unrealized profit and loss of all positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self.get_unrealized_pl_of_portfolio(strategy_name)

    def get_unrealized_pl_of_portfolio(self, portfolio_name):
        # type: (str) -> Decimal
        """Gets the total unrealized profit and loss of all positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getUnrealizedPL(portfolio_name)

    def get_net_liq_value(self):
        # type: () -> Decimal
        """Gets the Net-Liquidation-Value of the entire system.

            Returns:
                Decimal
        """
        return self._service.getNetLiqValue()

    def get_net_liq_value_of_strategy(self, strategy_name):
        # type: (str) -> Decimal
        """Gets the Net-Liquidation-Value of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self.get_net_liq_value_of_portfolio(strategy_name)

    def get_net_liq_value_of_portfolio(self, portfolio_name):
        # type: (str) -> Decimal
        """Gets the Net-Liquidation-Value of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getNetLiqValue(portfolio_name)

    def get_available_balance(self):
        # type: () -> Decimal
        """Gets the balance available for trading of the entire system.

            Returns:
                Decimal
        """
        return self._service.getAvailableBalance()

    def get_available_balance_of_strategy(self, strategy_name):
        # type: (str) -> Decimal
        """Gets the balance available for trading of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self.get_available_balance_of_portfolio(strategy_name)

    def get_available_balance_of_portfolio(self, portfolio_name):
        # type: (str) -> Decimal
        """Gets the balance available for trading of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                Decimal
        """
        return self._service.getAvailableBalance(portfolio_name)

    def get_open_positions(self):
        # type: () -> int
        """Gets the number of open positions of the entire system.

            Returns:
                int
        """
        return self._service.getOpenPositions()

    def get_open_positions_of_strategy(self, strategy_name):
        # type: (str) -> int
        """Gets the number of open positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                int
        """
        return self.get_open_positions_of_portfolio(strategy_name)

    def get_open_positions_of_portfolio(self, portfolio_name):
        # type: (str) -> int
        """Gets the number of open positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                int
        """
        return self._service.getOpenPositions(portfolio_name)

    def get_open_positions_on_date(self, date):
        # type: (datetime) -> int
        """Gets the number of open positions of the entire system on the specified date.

            Arguments:
                date (datetime): &nbsp;
            Returns:
                int
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getOpenPositions(date_java)

    def get_open_positions_of_strategy_on_date(self, strategy_name, date):
        # type: (str, datetime) -> int
        """Gets the number of open positions of the specified strategy on the specified date.

            Arguments:
                strategy_name (str): &nbsp;
                date (datetime): &nbsp;
            Returns:
                int
        """
        return self.get_open_positions_of_portfolio_on_date(strategy_name, date)

    def get_open_positions_of_portfolio_on_date(self, portfolio_name, date):
        # type: (str, datetime) -> int
        """Gets the number of open positions of the specified portfolio on the specified date.

            Arguments:
                portfolio_name (str): &nbsp;
                date (datetime): &nbsp;
            Returns:
                int
        """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        return self._service.getOpenPositions(portfolio_name, date_java)

    def get_portfolio_value(self):
        # type: () -> Optional[PortfolioValue]
        """Gets the portfolio value of the entire system.

            Returns:
                Optional of algotrader_com.domain.entity.PortfolioValue
        """
        _json = self._service.getPortfolioValue()
        if _json is None:
            return None
        _dict = Conversions.unmarshall(_json)
        pv = PortfolioValue.convert_from_json(_dict)
        return pv

    def get_portfolio_value_of_strategy(self, strategy_name):
        # type: (str) -> Optional[PortfolioValue]
        """Gets the portfolio value of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.PortfolioValue
        """
        return self.get_portfolio_value(strategy_name)

    def get_portfolio_value(self, portfolio_name):
        # type: (str) -> Optional[PortfolioValue]
        """Gets the portfolio value of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.PortfolioValue
        """
        _json = self._service.getPortfolioValue(portfolio_name)
        if _json is None:
            return None
        _dict = Conversions.unmarshall(_json)
        pv = PortfolioValue.convert_from_json(_dict)
        return pv

    def get_portfolio_value_of_strategy_on_date(self, strategy_name, date):
        # type: (str, datetime) -> Optional[PortfolioValue]
        """Gets the portfolio value of the specified strategy on the specified date.
            Note: RealizedPL and UnRealizedPL will be set to null.

            Arguments:
                strategy_name (str): &nbsp;
                date (datetime): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.PortfolioValue
           """
        return self.get_portfolio_value_on_date(strategy_name, date)

    def get_portfolio_value_on_date(self, portfolio_name, date):
        # type: (str, datetime) -> Optional[PortfolioValue]
        """Gets the portfolio value of the specified portfolio on the specified date.
            Note: RealizedPL and UnRealizedPL will be set to null.

            Arguments:
                portfolio_name (str): &nbsp;
                date (datetime): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.PortfolioValue
           """
        date_java = Conversions.python_datetime_to_zoneddatetime(date, self._gateway)
        _json = self._service.getPortfolioValue(portfolio_name, date_java)
        if _json is None:
            return None
        _dict = Conversions.unmarshall(_json)
        pv = PortfolioValue.convert_from_json(_dict)
        return pv

    def get_balances(self):
        # type: () -> List[Balance]
        """Gets the balances of the entire system.

            Returns:
                List of algotrader_com.domain.entity.Balance
        """
        _jsons = self._service.getBalances()
        if _jsons is None:
            return []
        balances = []
        for _json in _jsons:
            _dict = Conversions.unmarshall(_json)
            balance = Balance.convert_from_json(_dict)
            balances.append(balance)
        return balances

    def get_balances_of_strategy(self, strategy_name):
        # type: (str) -> List[Balance]
        """Gets the balances of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Balance
        """
        return self.get_balances_of_portfolio(strategy_name)

    def get_balances_of_portfolio(self, portfolio_name):
        # type: (str) -> List[Balance]
        """Gets the balances of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Balance
        """
        _jsons = self._service.getBalances(portfolio_name)
        if _jsons is None:
            return []
        balances = []
        for _json in _jsons:
            _dict = Conversions.unmarshall(_json)
            balance = Balance.convert_from_json(_dict)
            balances.append(balance)
        return balances

    def get_fx_exposure(self):
        # type: () -> List[FxExposure]
        """Gets the Net FX Currency Exposure of all FX positions of the entire system.

            Returns:
                List of algotrader_com.domain.entity.FxExposure
        """
        jsons = self._service.getFxExposure()
        if jsons is None:
            return []
        fx_exposures = []
        for _json in jsons:
            _dict = Conversions.unmarshall(_json)
            fx_exposure = FxExposure.convert_from_json(_dict)
            fx_exposures.append(fx_exposure)
        return fx_exposures

    def get_fx_exposure_of_strategy(self, strategy_name):
        # type: (str) -> List[FxExposure]
        """Gets the Net FX Currency Exposure of all FX positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.FxExposure
        """
        return self.get_fx_exposure_of_portfolio(strategy_name)

    def get_fx_exposure_of_portfolio(self, portfolio_name):
        # type: (str) -> List[FxExposure]
        """Gets the Net FX Currency Exposure of all FX positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.FxExposure
        """
        jsons = self._service.getFxExposure(portfolio_name)
        if jsons is None:
            return []
        fx_exposures = []
        for _json in jsons:
            _dict = Conversions.unmarshall(_json)
            fx_exposure = FxExposure.convert_from_json(_dict)
            fx_exposures.append(fx_exposure)
        return fx_exposures

    def save_portfolio_value(self, transaction):
        # type: (Transaction) -> None
        """Saves current Portfolio Values as a consequence for a performance relevant Transaction.
           If there have been PortfolioValues created since this Transaction, they are recreated (including PortfolioValues of the AlgoTrader Server)

           Arguments:
               transaction (algotrader_com.domain.entity.Transaction): &nbsp;
        """
        _json = Conversions.marshall(transaction)
        self._service.savePortfolioValue(_json)

    def save_portfolio_values(self):
        # type: () -> None
        """Saves current portfolio values for all strategies marked as autoActivate"""
        self._service.savePortfolioValues()

    def restore_portfolio_values(self, portfolio_id, from_date, to_date):
        # type: (int, datetime, datetime) -> None
        """Restores all PortfolioValues of the specified Portfolio after the from_date up to and including the to_date

            Arguments:
                portfolio_id (int): &nbsp;
                from_date (datetime): &nbsp;
                to_date (datetime): &nbsp;
        """
        from_date_java = Conversions.python_datetime_to_zoneddatetime(from_date, self._gateway)
        to_date_java = Conversions.python_datetime_to_zoneddatetime(to_date, self._gateway)
        self._service.restorePortfolioValues(portfolio_id, from_date_java, to_date_java)

    def get_portfolio_value_delta_summary(self, portfolio_name, min_date):
        # type: (str, datetime) -> PortfolioValueDeltaSummary
        """Retrieves PortfolioValueDeltaSummary object, containing a delta of the realized PnL of the portfolio since the specified min_Date,
           and the current unrealized PnL.

           Arguments:
               portfolio_name (str): &nbsp;
               min_date (str): &nbsp;
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        result_java = self._service.getPortfolioValueDeltaSummary(portfolio_name, min_date_java)
        result = PortfolioValueDeltaSummary.convert_from_java_object(result_java)
        return result
