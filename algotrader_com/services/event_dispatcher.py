from typing import List

from algotrader_com.domain.market_data import MarketDataEvent
from py4j.clientserver import ClientServer
from py4j.java_gateway import JavaObject


class EventDispatcher:
    """Delegates to pythonLookupService object in PythonStrategyService on the Java side.
       Event dispatcher is a platform wide communication interface capable of submitting events to event listeners,
       both inside and outside of the running AT server.
       Events sent need to be Py4J Java objects, for an example of converting a Python object to a Java one
       see `algotrader_com.domain.entity.DividendEvent.convert_to_java_object`

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonEventDispatcher()

    def send_event(self, strategy_name, event):
        # type: (str, JavaObject) -> None
        """Sends event related to the given strategy to local or remote recipients.

           Arguments:
               strategy_name (str): &nbsp;
               event: Py4J Java Object
        """
        self._service.sendEvent(strategy_name, event)

    def resend_past_event(self, strategy_name, event):
        # type: (str, JavaObject) -> None
        """Re-sends past event related to the given strategy to internal recipients such as UI primarily to restore strategy state upon startup.

           Arguments:
               strategy_name (str): &nbsp;
               event: Py4J Java Object
        """
        self._service.resendPastEvent(strategy_name, event)

    def send_market_data_event(self, market_data_event):
        # type: (MarketDataEvent) -> None
        """Sends market data event all subscribed strategies running either locally or remotely.

            Arguments:
                market_data_event (MarketDataEvent): event to send
        """
        market_data_event_java = market_data_event.convert_to_vo(market_data_event)
        self._service.sendMarketDataEvent(market_data_event_java)

    def broadcast(self, generic_event_java_object, recipients):
        # type: (JavaObject, List[str]) -> None
        """Broadcasts the generic event asynchronously to all possible recipients.

           Arguments:
               generic_event_java_object: Py4J Java Object
               recipients (List[str]): a list of one or more the following strings: SERVER_ENGINE, STRATEGY_ENGINES, LISTENERS, REMOTE
        """
        recipients_enums = self._convert_recipient_enums(recipients)
        self._service.broadcast(generic_event_java_object, recipients_enums)

    def broadcast_in_same_thread(self, generic_event_java_object, recipients):
        # type: (JavaObject, List[str]) -> None
        """Broadcasts the generic event synchronously to all possible listeners.

           Arguments:
               generic_event_java_object: Py4J Java Object
               recipients (List[str]): a list of one or more the following strings: SERVER_ENGINE, STRATEGY_ENGINES, LISTENERS, REMOTE
        """
        recipients_enums = self._convert_recipient_enums(recipients)
        self._service.broadcastInSameThread(generic_event_java_object, recipients_enums)

    def _convert_recipient_enums(self, recipients):
        recipients_enums = self._gateway.jvm.java.util.HashSet()
        for recipient in recipients:
            recipient_enum = self._gateway.jvm.EventRecipient.valueOf(recipient)
            recipients_enums.add(recipient_enum)
        return recipients_enums
