from decimal import Decimal
from typing import List, Optional

from py4j.clientserver import ClientServer
from py4j.java_gateway import JavaObject

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import NamedCurrencyAmount, WithdrawStatus, WalletEvent, SecurityPosition, Allocations, ExternalBalance


class AccountService:
    """Delegates to accountService object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway=None):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getAccountService()

    def retrieve_account_balances(self, account_id):
        # type: (int) -> List[NamedCurrencyAmount]
        """Returns all currency balances for the specified account.

            Arguments:
                account_id (int): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.NamedCurrencyAmount
        """
        vos = self._service.retrieveAccountBalances(account_id)
        balances = []
        for vo in vos:
            balance = NamedCurrencyAmount.convert_to_named_currency_amount(vo)
            balances.append(balance)
        return balances

    def withdraw_crypto(self, account_id, currency, amount, address, payment_id, address_description):
        # type: (int, str, Decimal, str, str, str) -> WithdrawStatus
        """ Submits a withdrawal request to the specified address

         Arguments:
             account_id: account to use
             currency: withdrawal currency
             amount: amount to withdraw
             address: address
             payment_id: Binance - Secondary address identifier for coins like XRP,XMR etc,
                 BitFinex: 1. Optional hex string to identify a Monero transaction
                     2. When submitting a Ripple Withdrawal via API, you should include tag in the payment_id field
             address_description: result of withdrawal
         Returns:
             algotrader_com.domain.entity.WithdrawStatus
             """
        ctx = self._gateway.jvm.ch.algotrader.api.connector.account.domain.\
            CryptoWithdrawContext(address, payment_id, address_description)

        vo = self._service.withdraw(account_id, currency, amount, ctx)
        status = WithdrawStatus.convert_from_vo(vo)
        return status

    def get_deposit_address(self, account_id, currency, wallet_type):
        # type: (int, str, str) -> str
        """

        Arguments:
            account_id (int): &nbsp;
            currency (str): &nbsp;
            wallet_type (str): &nbsp;

        Returns:
            str
        """

        return self._service.getDepositAddress(account_id, currency, wallet_type)

    def get_wallet_history(self, account_id, currency):
        # type: (int, str) -> List[WalletEvent]
        """
        Args:
            account_id (int): &nbsp;
            currency (str): &nbsp;
        Returns:
            List of algotrader_com.domain.entity.WalletEvent
        """
        vos = self._service.getWalletHistory(account_id, currency)
        objects = []
        for vo in vos:
            obj = WalletEvent.convert_from_vo(vo)
            objects.append(obj)
        return objects

    def get_account_positions(self, account_id, sub_account_id):
        # type: (int) -> List[SecurityPosition]
        """Returns all security positions for the specified account.

            Arguments:
                account_id (int): &nbsp;
                sub_account_id (int): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.SecurityPosition
        """
        vos = self._service.getAccountPositions(account_id, sub_account_id)
        positions = []
        for vo in vos:
            security_position = SecurityPosition.convert_from_vo(vo)
            positions.append(security_position)
        return positions

    def get_allocations(self, account_id, profile_name):
        # type: (int, str) -> Allocations

        java_object = self._service.getAllocations(account_id, profile_name)
        allocations = Allocations.convert_from_java_object(java_object)

        return allocations

    def update_allocations(self, account_id, allocations):
        # type: (int, Allocations) -> None
        self._service.updateAllocations(account_id, Allocations.convert_to_java_object(allocations, self._gateway))

    def get_ext_accounts(self, account_id, managed):
        # type: (int, bool) -> List[str]
        """Returns all security positions for the specified account.

            Arguments:
                account_id (int): &nbsp;
                managed (bool): &nbsp;
            Returns:
                List of String
        """
        return self._service.getExtAccounts(account_id, managed)

    def get_external_balances(self, account_id=None):
        # type: (int) -> List[ExternalBalance]
        """Returns External Balances for specified account (or all accounts if account_id is not provided).

            Arguments:
                account_id (int): &nbsp;
            Returns:
                List of External Balances
        """
        if account_id is None:
            vos = self._service.getExternalBalances()
        else:
            vos = self._service.getExternalBalances(account_id)

        objects = []
        for vo in vos:
            obj = ExternalBalance.convert_to_external_balance(vo)
            objects.append(obj)
        return objects
