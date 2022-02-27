from typing import List

from py4j.clientserver import ClientServer

from algotrader_com.domain.entity import Transfer, TransferRequest, TransferCancelRequest, TransferResult


# noinspection PyProtectedMember
class TransferService:
    """Delegates to transferService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getTransferService()

    def transfer(self, account_id, transfer_request):
        # type: (int, TransferRequest) -> TransferResult
        """Initiate a transfer

           Arguments:
               account_id (int): &nbsp;
               transfer_request (algotrader_com.domain.entity.TransferRequest): &nbsp;
           Returns:
               algotrader_com.domain.entity.TransferResult
        """
        request = transfer_request.convert_to_vo(self._gateway)
        vo = self._service.transfer(account_id, request)
        res = TransferResult.convert_from_vo(vo)
        return res

    def cancel_transfer(self, account_id, cancel_request):
        # type: (int, TransferCancelRequest) -> TransferResult
        """Initiate a transfer

           Arguments:
               account_id (int): &nbsp;
               cancel_request (algotrader_com.domain.entity.TransferCancelRequest): &nbsp;
           Returns:
               algotrader_com.domain.entity.TransferResult
        """
        request = cancel_request.convert_to_vo(self._gateway)
        vo = self._service.cancelTransfer(account_id, request)
        res = TransferResult.convert_from_vo(vo)
        return res

    def get_all_transfers(self):
        # type: () -> List[Transfer]
        """Gets all Transfers

           Returns:
               List of algotrader_com.domain.entity.Transfer
        """
        vos = self._service.getAllTransfers()
        if vos is None:
            return []
        transfers = []
        for vo in vos:
            transfer = Transfer.convert_from_vo(vo)
            transfers.append(transfer)
        return transfers

    def get_active_transfers(self, account_id):
        # type: (int) -> List[Transfer]
        """Gets all Transfers

           Arguments:
               account_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Transfer
        """
        vos = self._service.getActiveTransfers(account_id)
        if vos is None:
            return []
        transfers = []
        for vo in vos:
            transfer = Transfer.convert_from_vo(vo)
            transfers.append(transfer)
        return transfers
