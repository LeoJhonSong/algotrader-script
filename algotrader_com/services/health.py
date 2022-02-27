from typing import Optional, Dict

from py4j.clientserver import ClientServer


class HealthService:
    """Provides health status of various AlgoTrader components including exchange adapters."""

    def __init__(self, gateway):
        # type: (Optional[ClientServer]) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonHealthService()

    def get_all_components_health_statuses(self):
        # type: () -> Dict[str, str]
        """Updates all health statuses (for pull functions, system stats like JVM, parent's status)
           and returns them as a dictionary of component name mapped to its health status.
           Health status can be: DEAD, UNHEALTHY, ALIVE

           Returns:
               Dict of str to str
        """
        java_map = self._service.getHealthStatusMap()
        health_map = {}
        for key in java_map:
            health_map[key] = java_map[key]
        return health_map
