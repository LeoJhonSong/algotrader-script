from typing import List, Optional

from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions


class SupportedAdaptersService:
    """Delegates to pythonSupportedAdaptersService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (Optional[ClientServer]) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonSupportedAdaptersService()

    def get_supported_connector_descriptors(self):
        # type: () -> List[str]
        """Returns all currently active data adapters.

           Returns:
               List[str]
               .. include:: ../adapter_types.txt
        """
        returned = self._service.getSupportedConnectorDescriptors()
        result = []
        for connector_descriptor in returned:
            result.append(connector_descriptor.getDescriptor())
        return result

    def is_supported_connector_descriptor(self, connector_descriptor):
        # type: (str) -> bool
        """Returns True if the data adapter is supported.

           Arguments:
               .. include:: ../adapter_types.txt
           Returns:
               bool
        """
        connector_descriptor_java = self._gateway.jvm.ch.algotrader.api.connector.application.ConnectorDescriptor(connector_descriptor)
        return self._service.isSupportedConnectorDescriptor(connector_descriptor_java)
