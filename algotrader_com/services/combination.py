from decimal import Decimal

from py4j.clientserver import ClientServer

from algotrader_com.domain.security import Combination


class CombinationService:
    """Delegates to pythonCombinationService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.getPythonCombinationService()

    def create_combination(self, combination_type, security_family_id):
        # type: (str, int) -> Combination
        """Creates a combination of the specified combination_type and assigns it to the
                   specified security family

           Arguments:
               combination_type (str): VERTICAL_SPREAD, COVERED_CALL, RATIO_SPREAD, STRADDLE, STRANGLE, BUTTERFLY, CALENDAR_SPREAD, IRON_CONDOR
               security_family_id (int): &nbsp;
           Returns:
               algotrader_com.domain.security.Combination
           """
        combination_type_java = self._gateway.jvm.CombinationType.valueOf(combination_type)
        vo = self._service.createCombination(combination_type_java, security_family_id)
        obj = Combination.convert_from_vo(vo, self._gateway)
        return obj

    def create_combination_with_underlying(self, combination_type, security_family_id, underlying_id):
        # type: (str, int, int) -> Combination
        """Creates a Combination of the specified combination type,
           assigns it to the specified security family
           and assigns an underlying security defined by the underlying_id.

           Arguments:
               combination_type (str): VERTICAL_SPREAD, COVERED_CALL, RATIO_SPREAD, STRADDLE, STRANGLE, BUTTERFLY, CALENDAR_SPREAD, IRON_CONDOR
               security_family_id (int): &nbsp;
               underlying_id (int): &nbsp;
           Returns:
               algotrader_com.domain.security.Combination
           """
        combination_type_java = self._gateway.jvm.CombinationType.valueOf(combination_type)
        vo = self._service \
            .createCombination(combination_type_java, security_family_id, underlying_id)
        obj = Combination.convert_from_vo(vo, self._gateway)
        return obj

    def delete_combination(self, combination_id):
        """
        Args:
            combination_id (int): &nbsp;
        """
        self._service.deleteCombination(combination_id)

    def add_component_quantity(self, combination_id, security_id, quantity):
        # type: (int, int, Decimal) -> Combination
        """Adds the specified quantity to the component defined by security_id of the
           combination defined by combination_id. If the component does not exist yet, it will be
           created.

           Arguments:
               combination_id (int): &nbsp;
               security_id (int): &nbsp;
               quantity (Decimal): &nbsp;
           Returns:
               algotrader_com.domain.security.Combination
          """
        vo = self._service.addComponentQuantity(combination_id, security_id, quantity)
        obj = Combination.convert_from_vo(vo, self._gateway)
        return obj

    def set_component_quantity(self, combination_id, security_id, quantity):
        # type: (int, int, Decimal) -> Combination
        """Sets the quantity of the component defined by security_id of the combination
           defined by combination_id. the existing quantity will be ignored. If the
           component does not exist yet, it will be created.

           Arguments:
               combination_id (int): &nbsp;
               security_id (int): &nbsp;
               quantity (Decimal): &nbsp;
           Returns:
               algotrader_com.domain.security.Combination
        """
        vo = self._service.setComponentQuantity(combination_id, security_id, quantity)
        obj = Combination.convert_from_vo(vo, self._gateway)
        return obj

    def remove_component(self, combination_id, security_id):
        # type: (int, int) -> Combination
        """Removes the specified component defined by security_id from the combination defined by
           combination_id.

           Arguments:
               combination_id (int): &nbsp;
               security_id (int): &nbsp;
           Returns:
               algotrader_com.domain.security.Combination
           """
        vo = self._service.removeComponent(combination_id, security_id)
        obj = Combination.convert_from_vo(vo, self._gateway)
        return obj

    def reset_component_window(self):
        # type: () -> None
        """Removes the specified component defined by security_id from the combination defined by
           combination_id."""
        self._service.resetComponentWindow()
