from decimal import Decimal

from py4j.clientserver import ClientServer


class PositionService:
    """Delegates to positionService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPositionService()

    def close_all_positions_by_strategy(self, strategy_name):
        # type: (str) -> None
        """Closes all positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
        """
        return self.close_all_positions_by_portfolio(strategy_name)

    def close_all_positions_by_portfolio(self, portfolio_name):
        # type: (str) -> None
        """Closes all positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
        """
        self._service.closeAllPositionsByPortfolio(portfolio_name)

    def close_position(self, position_id):
        # type: (int) -> None
        """Closes the specified position.

            Arguments:
                position_id (int): &nbsp;
        """
        self._service.closePosition(position_id)

    def reduce_position(self, position_id, quantity):
        # type: (int, Decimal) -> None
        """Reduces the specified position by the specified *quantity*.

            Arguments:
                position_id (str): &nbsp;
                quantity (Decimal): &nbsp;
        """
        self._service.reducePosition(position_id, quantity)

    def transfer_position(self, position_id, target_portfolio_name):
        # type: (int, str) -> None
        """Transfers entire position to another portfolio.
           Uses latest available tick for underlying security to record the transfer inside the system.
           Prerequisite: Market data for underlying security has to be available in order to use this method.
           Raises an exception in case market data for underlying is not available.

           Arguments:
               position_id (int): &nbsp;
               target_portfolio_name (str): &nbsp;
        """
        self._service.transferPosition(position_id, target_portfolio_name)

    def transfer_position_with_reference_price(self, position_id, target_portfolio_name, reference_price):
        # type: (int, str, Decimal) -> None
        """Transfers a position to another portfolio.
           Provided reference price will be used to record the transfer inside the system.

           Arguments:
               position_id (str): &nbsp;
               target_portfolio_name (str): &nbsp;
               reference_price (Decimal): &nbsp;
        """
        self._service \
            .transferPosition(position_id, target_portfolio_name, reference_price)

    def transfer_position_partially(self, position_id, target_portfolio_name, quantity):
        # type: (int, str, Decimal) -> None
        """Transfers subset of existing position to another portfolio.
           Uses latest available tick for underlying security to record the transfer inside the system.
           Prerequisite: Market data for underlying security has to be available in order to use this method.
           Raises an exception in case market data for underlying is not available.

           Arguments:
               position_id (str): &nbsp;
               target_portfolio_name (str): &nbsp;
               quantity (Decimal): &nbsp;
        """
        self._service \
            .transferPositionPartially(position_id, target_portfolio_name, quantity)

    def transfer_position_partially_with_reference_price(self, position_id, target_portfolio_name, quantity,
                                                         reference_price):
        # type: (int, str, Decimal, Decimal) -> None
        """Transfers subset of existing Position to another portfolio.
           Provided reference price will be used to record the transfer inside the system.

           Arguments:
               position_id (str): &nbsp;
               target_portfolio_name (str): &nbsp;
               quantity (Decimal): &nbsp;
               reference_price (Decimal): &nbsp;
        """
        self._service \
            .transferPositionPartially(position_id, target_portfolio_name, quantity, reference_price)

    def transfer_all_positions(self, source_portfolio_name, target_portfolio_name):
        # type: (str, str) -> None
        """Transfers all positions (in full) of chosen portfolio to another portfolio.

           Arguments:
               source_portfolio_name (str): &nbsp;
               target_portfolio_name (str): &nbsp;
        """
        self._service.transferAllPositions(source_portfolio_name, target_portfolio_name)

    def handle_position_split(self, position_id, position_factor, account_name):
        # type: (int, Decimal, str) -> None
        """Handles a position split request. Supported so far only for stocks.

           Arguments:
               position_id (int): &nbsp;
               position_factor (decimal): &nbsp;
               account_name (str): &nbsp;
        """
        self._service.handlePositionSplit(position_id, position_factor, account_name)
