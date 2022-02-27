from py4j.clientserver import ClientServer

from algotrader_com.domain.entity import Portfolio
from typing import List


class PortfolioService:
    """Delegates to pythonPortfolioService object methods in PythonStrategyService on the Java side.

   Initialized by <i>connect_to_algotrader</i> function
   and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonPortfolioService()

    def get_upward_hierarchy(self, portfolio):
        # type: (Portfolio) -> List[Portfolio]
        """Gets the list of portfolios that are ancestors of the given one, including the given one.
            Arguments:
                portfolio (portfolio): portfolio
            Returns:
                Portfolio
        """
        portfolios = self._service.getUpwardHierarchy(portfolio.convert_to_vo(self._gateway))
        upward_portfolios = [Portfolio.convert_from_vo(portfolio) for portfolio in portfolios]
        return upward_portfolios

    def get_upward_hierarchy_by_portfolio_name(self, portfolio_name):
        # type: (str) -> List[str]
        """Gets the list of portfolios names that are ancestors of the given one, including the given one.
            Arguments:
                portfolio_name (str): portfolio
            Returns:
                List[Portfolio]
        """
        return self._service.getUpwardHierarchy(portfolio_name)

    def get_downward_hierarchy(self, portfolio):
        # type: (Portfolio) -> List[Portfolio]
        """Gets the list of portfolios that are sub portfolios of the given one, including the given one.
            Arguments:
                portfolio (Portfolio): portfolio
            Returns:
                List[Portfolio]
        """
        portfolios = self._service.getDownwardHierarchy(portfolio.convert_to_vo(self._gateway))
        downward_portfolios = [Portfolio.convert_from_vo(portfolio) for portfolio in portfolios]
        return downward_portfolios

    def get_downward_hierarchy_by_portfolio_name(self, portfolio_name):
        # type: (str) -> List[str]
        """Gets the list of portfolios that are sub portfolios of the given one, including the given one.
            Arguments:
                portfolio_name (str): portfolio
            Returns:
                List[Portfolio]
        """
        return self._service.getDownwardHierarchy(portfolio_name)

    def get_root_portfolios(self):
        # type: () -> List[Portfolio]
        """Gets all Root Portfolios.

            Returns:
                List[Portfolio]
        """
        portfolios = self._service.getRootPortfolios()
        root_portfolios = [Portfolio.convert_from_vo(portfolio) for portfolio in portfolios]
        return root_portfolios

    def get_portfolio_hierarchies(self):
        # type: () -> List[Portfolio]
        """Gets all Portfolio Hierarchies

            Returns:
                List[Portfolio]
        """
        portfolios = self._service.getPortfolioHierarchies()
        portfolio_hierarchies = [Portfolio.convert_from_vo(portfolio) for portfolio in portfolios]
        return portfolio_hierarchies

    def get_all_portfolios(self):
        # type: () -> List[Portfolio]
        """Gets the list of all portfolios in flat structure.

            Returns:
                List[Portfolio]
        """
        portfolios = self._service.getAllPortfolios()
        all_portfolios = [Portfolio.convert_from_vo(portfolio) for portfolio in portfolios]
        return all_portfolios
