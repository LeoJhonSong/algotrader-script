from py4j.clientserver import ClientServer

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import Transaction


class TransactionService:

    def __init__(self, gateway):
        # type: (Optional[ClientServer]) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonTransactionService()

    def get_transactions_by_int_order_id(self, int_order_id):
        # type: (str) -> List[Transaction]
        vos = self._service.getTransactionsByIntOrderId(int_order_id)

        objects = []
        for vo in vos:
            unmarshalled_vo = Conversions.unmarshall(vo)
            obj = Transaction.convert_from_json(unmarshalled_vo)
            objects.append(obj)
            return objects;


    def create_transaction(self, transaction):
        # type: (Transaction) -> List[Transaction]
        self._service.createTransaction(transaction.convert_to_vo(self._gateway))
