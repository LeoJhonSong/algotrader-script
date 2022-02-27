from typing import List

from py4j.clientserver import ClientServer
from py4j.java_collections import ListConverter

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import RfqQuote, QuoteRequest


# noinspection PyProtectedMember
class RfqService:
    """Delegates to rfqService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonRfqService()

    def get_quote(self, quote_id):
        # type: (str) -> RfqQuote
        """Retrieve a quote by its intId if it hasn't expired yet.

           Arguments:
               quote_id (str): &nbsp;
           Returns:
               algotrader_com.domain.entity.RfqQuote
        """
        vo = self._service.getQuote(quote_id)
        obj = RfqQuote.convert_from_vo(vo)
        return obj

    def get_quotes(self, quote_request_int_id):
        # type: (str) -> List[RfqQuote]
        """Gets the quotes that are available for the quote request that has been sent.

           Arguments:
               quote_request_int_id (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.RfqQuote
        """
        vos = self._service.getQuotes(quote_request_int_id)
        if vos is None:
            return []
        rfq_quotes = []
        for vo in vos:
            rfq_quote = RfqQuote.convert_from_vo(vo)
            rfq_quotes.append(rfq_quote)
        return rfq_quotes

    def send_rfq(self, quote_request):
        # type: (QuoteRequest) -> str
        """Requests a quote from the broker associated with the account sent in on the request.

           Arguments:
               quote_request (algotrader_com.domain.entity.QuoteRequest): &nbsp;
           Returns:
               str: the intId of the quote request
        """
        return self._service.sendRfq(quote_request.convert_to_vo(self._gateway))

    def send_multi_rfq(self, quote_request):
        # type: (QuoteRequest) -> str
        """Requests quotes from multiple configured brokers.

           Arguments:
               quote_request (algotrader_com.domain.entity.QuoteRequest): &nbsp;
           Returns:
               str: the intId of the quote request
        """
        return self._service.sendMultiRfq(quote_request.convert_to_vo(self._gateway))

    def discard_quotes(self, quote_ids):
        # type: (List[str]) -> None
        """Discards quotes by intIds.

          Arguments:
              quote_ids
        """
        ids_java = ListConverter().convert(quote_ids, self._gateway._gateway_client)
        self._service.discardQuotes(ids_java)
