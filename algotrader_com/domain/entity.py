from abc import abstractmethod
from algotrader_com.domain.conversions import Conversions
from datetime import datetime
from decimal import Decimal
from numbers import Number
from py4j.clientserver import ClientServer
from py4j.java_gateway import JavaObject
from typing import List, Dict, Optional


class PropertyHolder:
    """Parent class marking domain objects that are able to store custom key-value based properties."""

    def __init__(self, _id=None):
        # type: (int) -> None
        self.id = _id

    @staticmethod
    @abstractmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        pass


class LifecycleEvent:
    """Mirrors LifecycleEventVO Java class. Event signaling progression to another portfolio lifecycle phase.

       Attributes:
           phase (str): "INIT_ENGINE", "START_ENGINE", "CORE", "STATE_LOADER", "CONNECTOR", "SERVICE", "INIT", "PREFEED", "START", "RUNNING", "EXIT"
           event_type (str): "SERVER", "STRATEGY"
    """

    def __init__(self, phase, event_type):
        # type: (str, str) -> None
        self.phase = phase  # "INIT_ENGINE", "START_ENGINE", "CORE", "STATE_LOADER", "CONNECTOR", "SERVICE", "INIT", "PREFEED", "START", "RUNNING", "EXIT"
        self.event_type = event_type  # "SERVER", "STRATEGY"

    @staticmethod
    def convert_to_lifecycle_event(lifecycle_event_vo):
        # type: (JavaObject) -> LifecycleEvent
        """Converts Java value object to the Python object.

           Arguments:
               lifecycle_event_vo (ch.algotrader.vo.LifecycleEventVO): &nbsp;
           Returns:
               LifecycleEvent
        """
        phase = Conversions.get_java_object_to_string(lifecycle_event_vo.getPhase())
        event_type = Conversions.get_java_object_to_string(lifecycle_event_vo.getType())
        return LifecycleEvent(phase, event_type)


class OrderStatus:
    """Mirrors OrderStatusVO Java class.
       Represents Order status changes received from the Broker (i.e. PARTIALLY_EXECUTED or CANCELLED)

       Attributes:
           id (int): &nbsp;
           date_time (datetime): &nbsp;
           ext_date_time (datetime): &nbsp;
           status (str):  "OPEN", "SUBMITTED", "PARTIALLY_EXECUTED", "EXECUTED", "CANCELED", "REJECTED", "CANCEL_FAILED"
           filled_quantity (Decimal): &nbsp;
           remaining_quantity (Decimal): &nbsp;
           last_quantity (Decimal): &nbsp;
           avg_price (Decimal): &nbsp;
           last_price (Decimal): &nbsp;
           int_id (str): &nbsp;
           ext_id (str): &nbsp;
           sequence_number (int): &nbsp;
           reason (str): &nbsp;
           order_id (int): &nbsp;
       """

    def __init__(self, _id, date_time, ext_date_time, status, filled_quantity, remaining_quantity, last_quantity,
                 avg_price, last_price, int_id, ext_id, sequence_number, reason, order_id):
        # type: (int, datetime, datetime, str, Decimal, Decimal, Decimal, Decimal, Decimal, str, str, int, str, int) -> None
        self.id = _id
        self.date_time = date_time
        self.ext_date_time = ext_date_time

        # "OPEN", "SUBMITTED", "PARTIALLY_EXECUTED", "EXECUTED", "CANCELED", "REJECTED", "CANCEL_FAILED"
        self.status = status
        self.filled_quantity = filled_quantity
        self.remaining_quantity = remaining_quantity
        self.last_quantity = last_quantity
        self.avg_price = avg_price
        self.last_price = last_price
        self.int_id = int_id
        self.ext_id = ext_id
        self.sequence_number = sequence_number
        self.reason = reason
        self.order_id = order_id

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> OrderStatus
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized OrderStatusVO): &nbsp;
           Returns:
               OrderStatus
        """
        _id = vo_dict["id"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        ext_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['extDateTime'])
        status = vo_dict["status"]
        filled_quantity = Conversions.float_to_decimal(vo_dict['filledQuantity'])
        remaining_quantity = Conversions.float_to_decimal(vo_dict['remainingQuantity'])
        last_quantity = Conversions.float_to_decimal(vo_dict['lastQuantity'])
        avg_price = Conversions.float_to_decimal(vo_dict['avgPrice'])
        last_price = Conversions.float_to_decimal(vo_dict['lastPrice'])
        int_id = vo_dict["intId"]
        ext_id = vo_dict["extId"]
        sequence_number = vo_dict["sequenceNumber"]
        reason = vo_dict["reason"]
        order_id = vo_dict["orderId"]
        order_status = OrderStatus(_id, date_time, ext_date_time, status, filled_quantity, remaining_quantity,
                                   last_quantity, avg_price, last_price, int_id, ext_id, sequence_number,
                                   reason, order_id)
        return order_status

    @staticmethod
    def convert_to_order_status(order_status_vo):
        # type: (JavaObject) -> OrderStatus
        """Converts Java value object to the Python object.

           Arguments:
               order_status_vo (ch.algotrader.entity.trade.OrderStatusVO): &nbsp;
           Returns:
               OrderStatus
        """
        _id = order_status_vo.getId()
        date_time = Conversions.zoned_date_time_to_python_datetime(order_status_vo.getDateTime())
        ext_date_time = Conversions.zoned_date_time_to_python_datetime(order_status_vo.getExtDateTime())
        status = Conversions.get_java_object_to_string(order_status_vo.getStatus())
        filled_quantity = order_status_vo.getFilledQuantity()
        remaining_quantity = order_status_vo.getRemainingQuantity()
        last_quantity = order_status_vo.getLastQuantity()
        avg_price = order_status_vo.getAvgPrice()
        last_price = order_status_vo.getLastPrice()
        int_id = order_status_vo.getIntId()
        ext_id = order_status_vo.getExtId()
        sequence_number = order_status_vo.getSequenceNumber()
        reason = order_status_vo.getReason()
        order_id = order_status_vo.getOrderId()
        order_status = OrderStatus(_id, date_time, ext_date_time, status, filled_quantity, remaining_quantity,
                                   last_quantity, avg_price, last_price, int_id, ext_id, sequence_number,
                                   reason, order_id)
        return order_status


class OrderCompletion:
    """Mirrors OrderCompletionVO Java class.
     
       Attributes:
           order_int_id (str): &nbsp;
           portfolio_name (str): &nbsp;
           security_id (int): &nbsp;
           date_time (datetime): &nbsp;
           status (str): "OPEN", "SUBMITTED", "PARTIALLY_EXECUTED", "EXECUTED", "CANCELED", "REJECTED", "CANCEL_FAILED"
           filled_quantity (Decimal): &nbsp;
           remaining_quantity (Decimal): &nbsp;
           avg_price (Decimal): &nbsp;
           gross_value (Decimal): &nbsp;
           net_value (Decimal): &nbsp;
           total_charges (Decimal): &nbsp;
           fills (int): &nbsp;
           execution_time (float): &nbsp;
    """

    def __init__(self, order_int_id, portfolio_name, security_id, date_time, status, filled_quantity, remaining_quantity,
                 avg_price, gross_value, net_value, total_charges, fills, execution_time):
        # type: (str, str, int, datetime, str, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, int, float) -> None
        self.order_int_id = order_int_id
        self.portfolio_name = portfolio_name
        self.security_id = security_id
        self.date_time = date_time

        # "OPEN", "SUBMITTED", "PARTIALLY_EXECUTED", "EXECUTED", "CANCELED", "REJECTED", "CANCEL_FAILED"
        self.status = status
        self.filled_quantity = filled_quantity
        self.remaining_quantity = remaining_quantity
        self.avg_price = avg_price
        self.gross_value = gross_value
        self.net_value = net_value
        self.total_charges = total_charges
        self.fills = fills
        self.execution_time = execution_time

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> OrderCompletion
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized OrderCompletionVO): &nbsp;
           Returns:
               OrderCompletion
        """
        order_int_id = vo_dict["orderIntId"]
        portfolio_name = vo_dict["portfolio"]
        security_id = vo_dict["securityId"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        status = vo_dict["status"]
        filled_quantity = Conversions.float_to_decimal(vo_dict['filledQuantity'])
        remaining_quantity = Conversions.float_to_decimal(vo_dict['remainingQuantity'])
        avg_price = Conversions.float_to_decimal(vo_dict['avgPrice'])
        gross_value = Conversions.float_to_decimal(vo_dict['grossValue'])
        net_value = Conversions.float_to_decimal(vo_dict['netValue'])
        total_charges = Conversions.float_to_decimal(vo_dict['totalCharges'])
        fills = vo_dict["fills"]
        execution_time = vo_dict["executionTime"]
        order_completion = OrderCompletion(order_int_id, portfolio_name, security_id, date_time, status, filled_quantity,
                                           remaining_quantity, avg_price, gross_value, net_value, total_charges, fills,
                                           execution_time)
        return order_completion

    @staticmethod
    def convert_to_order_completion(order_completion_vo):
        # type: (JavaObject) -> OrderCompletion
        """Converts Java value object to the Python object.

           Arguments:
               order_completion_vo (ch.algotrader.entity.trade.OrderCompletionVO): &nbsp;
           Returns:
               OrderCompletion
        """
        order_int_id = order_completion_vo.getOrderIntId()
        portfolio_name = order_completion_vo.getStrategy()
        security_id = order_completion_vo.getSecurityId()
        date_time = Conversions.zoned_date_time_to_python_datetime(order_completion_vo.getDateTime())
        status = Conversions.get_java_object_to_string(order_completion_vo.getStatus())
        filled_quantity = order_completion_vo.getFilledQuantity()
        remaining_quantity = order_completion_vo.getRemainingQuantity()
        avg_price = order_completion_vo.getAvgPrice()
        gross_value = order_completion_vo.getGrossValue()
        net_value = order_completion_vo.getNetValue()
        total_charges = order_completion_vo.getTotalCharges()
        fills = order_completion_vo.getFills()
        execution_time = order_completion_vo.getExecutionTime()
        order_completion = OrderCompletion(order_int_id, portfolio_name, security_id, date_time, status, filled_quantity,
                                           remaining_quantity, avg_price, gross_value, net_value, total_charges, fills,
                                           execution_time)
        return order_completion


class Fill:
    """Mirrors FillVO Java class.
    
       Attributes:
           order_int_id (str): internal order Id
           ext_id (str): External fill id assigned by the external broker.
           date_time (datetime): The date and time when the fill was received by the system.
           ext_date_time (datetime): &nbsp;
           sequence_number (int): The sequence number of the corresponding broker specific message (e.g. fix sequence number)
           side (str): "BUY", "SELL"
           quantity (Decimal): The quantity of this fill.
           price (Decimal): The price at which this fill occurred.
    """

    def __init__(self, order_int_id, ext_id, date_time, ext_date_time, sequence_number, side, quantity, price):
        # type: (str, str, datetime, datetime, int, str, Decimal, Decimal) -> None
        self.order_int_id = order_int_id  # internal order Id
        self.ext_id = ext_id  # External fill id assigned by the external broker.
        self.date_time = date_time  # The date and time when the fill was received by the system.
        self.ext_date_time = ext_date_time

        # The sequence number of the corresponding broker specific message (e.g. fix sequence number)
        self.sequence_number = sequence_number
        self.side = side  # "BUY", "SELL"
        self.quantity = quantity  # The quantity of this fill.
        self.price = price  # The price at which this fill occurred.

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> Fill
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized FillVO): &nbsp;
           Returns:
               Fill
        """
        order_int_id = vo_dict["orderIntId"]
        ext_id = vo_dict["extId"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        ext_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['extDateTime'])
        sequence_number = vo_dict["sequenceNumber"]
        side = vo_dict["side"]
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        price = Conversions.float_to_decimal(vo_dict['price'])
        fill = Fill(order_int_id, ext_id, date_time, ext_date_time, sequence_number, side, quantity, price)
        return fill

    @staticmethod
    def convert_to_fill(fill_vo):
        # type: (JavaObject) -> Fill
        """Converts Java value object to the Python object.

           Arguments:
               fill_vo (ch.algotrader.entity.trade.FillVO): &nbsp;
           Returns:
               Fill
        """
        order_int_id = fill_vo.getOrderIntId()
        ext_id = fill_vo.getExtId()
        date_time = Conversions.zoned_date_time_to_python_datetime(fill_vo.getDateTime())
        ext_date_time = Conversions.zoned_date_time_to_python_datetime(fill_vo.getExtDateTime())
        sequence_number = fill_vo.getSequenceNumber()
        if fill_vo.getSide() is not None:
            side = fill_vo.getSide().toString()
        else:
            side = None
        quantity = fill_vo.getQuantity()
        price = fill_vo.getPrice()
        fill = Fill(order_int_id, ext_id, date_time, ext_date_time, sequence_number, side, quantity, price)
        return fill


class Transaction(PropertyHolder):
    """Mirrors TransactionVO Java class.
       A transaction stored in the database. Each Fill is recorded as a transaction using this entity.
       In addition the table transaction also stores transactions like intrest, debit, credit  fees.

       Attributes:
           _id (int): &nbsp;
           uuid (str): auto generated unique identifier. Combinations do not have any other natural identifiers.
           date_time (datetime): &nbsp;
           settlement_date (datetime): &nbsp;
           ext_id (str): &nbsp;
           int_order_id (str): &nbsp;
           ext_order_id (str): &nbsp;
           quantity (Decimal): 
               The quantity of the Transaction. For different TransactionTypes quantities are as follows:

               BUY: pos

               SELL: neg

               EXPIRATION: pos/neg

               TRANSFER : pos/neg

               CREDIT: 1

               EXCHANGE_CREDIT: 1

               INTREST_RECEIVED: 1

               REFUND : 1

               DIVIDEND : 1

               DEBIT: -1

               EXCHANGE_DEBIT: -1

               INTREST_PAID: -1

               FEES: -1
           price (Decimal): The price of this transaction. Is is always positive.
           execution_commission (Decimal): &nbsp;
           clearing_commission (Decimal): &nbsp;
           fee (Decimal): The Exchange Fees of this transaction.
           currency (str): &nbsp;
           type (str): &nbsp;
           account_id (int): &nbsp;
           security_id (int): &nbsp;
           portfolio_id (int): &nbsp;
       """

    def __init__(self, _id=None, uuid=None, date_time=None, settlement_date=None, ext_id=None, int_order_id=None,
                 ext_order_id=None, quantity=None, price=None, execution_commission=None, clearing_commission=None,
                 fee=None, currency=None, _type=None, account_id=None, security_id=None, portfolio_id=None):
        # type: (int, str, datetime, datetime, str, str, str, Decimal, Decimal, Decimal, Decimal, Decimal, str, str, int, int, int ) -> None
        PropertyHolder.__init__(self, _id)
        self.uuid = uuid  # auto generated unique identifier. Combinations do not have any other natural identifiers.
        self.date_time = date_time
        self.settlement_date = settlement_date
        self.ext_id = ext_id
        self.int_order_id = int_order_id
        self.ext_order_id = ext_order_id

        # The quantity of the Transaction. For different TransactionTypes quantities are as follows:
        # BUY: pos
        # SELL: neg
        # EXPIRATION: pos/neg
        # TRANSFER : pos/neg
        # CREDIT: 1
        # EXCHANGE_CREDIT: 1
        # INTREST_RECEIVED: 1
        # REFUND : 1
        # DIVIDEND : 1
        # DEBIT: -1
        # EXCHANGE_DEBIT: -1
        # INTREST_PAID: -1
        # FEES: -1
        self.quantity = quantity
        self.price = price  # The price of this Transaction. Is is always positive.
        self.execution_commission = execution_commission
        self.clearing_commission = clearing_commission
        self.fee = fee  # The Exchange Fees of this transaction.
        self.currency = currency

        # TransactionType.java enum: "BUY", "SELL", "EXPIRATION", "TRANSFER", "CREDIT", "DEBIT", "EXCHANGE_CREDIT",
        #                            "EXCHANGE_DEBIT", "INTREST_PAID", "INTREST_RECEIVED", "DIVIDEND", "FEES",
        #                            "REFUND", "REBALANCE
        self.type = _type

        # Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
        self.account_id = account_id

        # A position of a particular security owned by a particular portfolio. For each opening transaction a
        # position is created. The position object remains in place even if a corresponding closing
        # transaction is carried out and the quantity of the position becomes 0.
        #
        # Since some values (e.g. marketValue) depend on whether the position is long or short,
        # aggregated position values for the same security (of different strategies) cannot be retrieved just
        # by adding position values from the corresponding strategies.
        #
        # Example:
        #  Security: VIX Dec 2012
        #  Current Bid: 16.50
        #  Current Ask: 16.60
        #  Portfolio A: quantity +10 marketValue: 10 * 1000 * 16.50 = 165'000
        #  Portfolio B: quantity -10 marketValue: 10 * 1000 * 16.60 = -166'000
        #
        #
        # The sum of above marketValues would be -1'000 which is obviously wrong.
        #
        # As a consequence the PortfolioService provides lookup-methods that aggregate positions from the
        # same security (of different strategies) in the correct manner.
        self.security_id = security_id
        self.portfolio_id = portfolio_id

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.TransactionImpl"

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> Transaction
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized TransactionVO): &nbsp;
           Returns:
               Transaction
        """
        _id = vo_dict["id"]
        uuid = vo_dict["uuid"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        settlement_date = Conversions.epoch_millis_to_python_datetime(vo_dict['settlementDate'])
        ext_id = vo_dict["extId"]
        int_order_id = vo_dict["intOrderId"]
        ext_order_id = vo_dict["extOrderId"]
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        price = Conversions.float_to_decimal(vo_dict['price'])
        execution_commission = Conversions.float_to_decimal(vo_dict['executionCommission'])
        clearing_commission = Conversions.float_to_decimal(vo_dict['clearingCommission'])
        fee = Conversions.float_to_decimal(vo_dict['fee'])
        currency = vo_dict['currency']
        _type = vo_dict['type']
        account_id = vo_dict['accountId']
        security_id = vo_dict['securityId']
        portfolio_id = vo_dict['portfolioId']
        transaction = Transaction(_id, uuid, date_time, settlement_date, ext_id, int_order_id, ext_order_id, quantity,
                                  price, execution_commission, clearing_commission, fee, currency, _type, account_id,
                                  security_id, portfolio_id)
        return transaction

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the transaction to the corresponding Java value object.

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.TransactionVO
        """
        _id = 0
        if self.id is not None:
            _id = self.id
        uuid = self.uuid
        date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
        settlement_date = Conversions.python_datetime_to_localdate(self.settlement_date, py4jgateway)
        ext_id = self.ext_id
        int_order_id = self.int_order_id
        ext_order_id = self.ext_order_id
        quantity = self.quantity
        price = self.price
        execution_commission = self.execution_commission
        clearing_commission = self.clearing_commission
        fee = self.fee
        currency = self.currency
        _type = None
        if self.type is not None:
            _type = py4jgateway.jvm.TransactionType.valueOf(self.type)
        account_id = self.account_id
        security_id = self.security_id
        portfolio_id = self.portfolio_id
        vo = py4jgateway.jvm.TransactionVO(_id, uuid, date_time, settlement_date, ext_id, int_order_id, ext_order_id,
                                           quantity, price, execution_commission, clearing_commission, fee, currency,
                                           _type, account_id, security_id, portfolio_id)
        return vo

    @staticmethod
    def convert_to_transaction(transaction_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Transaction
        """Converts Java value object to the Python object.

           Arguments:
               transaction_vo (ch.algotrader.entity.TransactionVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Transaction
        """
        _id = transaction_vo.getId()
        uuid = transaction_vo.getUuid()
        date_time = Conversions.zoned_date_time_to_python_datetime(transaction_vo.getDateTime())
        settlement_date = Conversions.local_date_to_python_datetime(transaction_vo.getSettlementDate(), py4jgateway)
        ext_id = transaction_vo.getExtId()
        int_order_id = transaction_vo.getIntOrderId()
        ext_order_id = transaction_vo.getExtOrderId()
        quantity = transaction_vo.getQuantity()
        price = transaction_vo.getPrice()
        execution_commission = transaction_vo.getExecutionCommission()
        clearing_commission = transaction_vo.getClearingCommission()
        fee = transaction_vo.getFee()
        currency = transaction_vo.getCurrency()
        _type = None
        if transaction_vo.getType() is not None:
            _type = transaction_vo.getType().toString()
        account_id = transaction_vo.getAccountId()
        security_id = transaction_vo.getSecurityId()
        portfolio_id = transaction_vo.getPortfolioId()
        transaction = Transaction(_id, uuid, date_time, settlement_date, ext_id, int_order_id, ext_order_id, quantity,
                                  price, execution_commission, clearing_commission, fee, currency, _type, account_id,
                                  security_id, portfolio_id)
        return transaction


class PositionMutation:
    """Mirrors PositionMutationVO Java class. Represents a mutation of a position (e.g. opening, closing, increasing/decreasing of a position)
    
       Attributes:
           id (int): &nbsp;
           quantity (Decimal): &nbsp;
           previous_quantity (Decimal): &nbsp;
           cost (Decimal): &nbsp;
           realized_pl (Decimal): &nbsp;
           portfolio_id (int): &nbsp;
           security_id (int): &nbsp;
           account_id (int): &nbsp;
           transaction_id (int): &nbsp;
           transaction_date_time (datetime): &nbsp;
           transaction_ext_id (str): &nbsp;
           transaction_quantity (Decimal): &nbsp;
           transaction_price (Decimal): &nbsp;
           transaction_type (str): &nbsp;
           int_order_id (str): &nbsp;
           ext_order_id (str): &nbsp;
    """

    def __init__(self, _id, quantity, previous_quantity, cost, realized_pl, portfolio_id, security_id,
                 account_id, transaction_id, transaction_date_time, transaction_ext_id, transaction_quantity,
                 transaction_price, transaction_type, int_order_id, ext_order_id):
        # type: (int, Decimal, Decimal, Decimal, Decimal, int, int, int, int, datetime, str, Decimal, Decimal, str, str, str) -> None
        self.id = _id
        self.quantity = quantity
        self.previous_quantity = previous_quantity
        self.cost = cost
        self.realized_pl = realized_pl
        self.portfolio_id = portfolio_id
        self.security_id = security_id
        self.account_id = account_id
        self.transaction_id = transaction_id
        self.transaction_date_time = transaction_date_time
        self.transaction_ext_id = transaction_ext_id
        self.transaction_quantity = transaction_quantity
        self.transaction_price = transaction_price
        self.transaction_type = transaction_type
        self.int_order_id = int_order_id
        self.ext_order_id = ext_order_id

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> PositionMutation
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized PositionMutationVO): &nbsp;
           Returns:
               PositionMutation
        """
        _id = vo_dict["id"]
        quantity = Conversions.float_to_decimal(vo_dict['quantity'])
        previous_quantity = Conversions.float_to_decimal(vo_dict['previousQuantity'])
        cost = Conversions.float_to_decimal(vo_dict['cost'])
        realized_pl = Conversions.float_to_decimal(vo_dict['realizedPL'])
        portfolio_id = vo_dict["portfolioId"]
        security_id = vo_dict["securityId"]
        account_id = vo_dict["accountId"]
        transaction_id = vo_dict["transactionId"]
        transaction_date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['transactionDateTime'])
        transaction_ext_id = vo_dict["transactionExtId"]
        transaction_quantity = Conversions.float_to_decimal(vo_dict['transactionQuantity'])
        transaction_price = Conversions.float_to_decimal(vo_dict['transactionPrice'])
        transaction_type = vo_dict["transactionType"]
        int_order_id = vo_dict["intOrderId"]
        ext_order_id = vo_dict["extOrderId"]
        position_mutation = PositionMutation(_id, quantity, previous_quantity, cost, realized_pl,
                                             portfolio_id, security_id, account_id, transaction_id,
                                             transaction_date_time, transaction_ext_id, transaction_quantity,
                                             transaction_price, transaction_type, int_order_id, ext_order_id)
        return position_mutation

    @staticmethod
    def convert_to_position_mutation(position_mutation_vo):
        # type: (JavaObject) -> PositionMutation
        """Converts Java value object to the Python object.

           Arguments:
               position_mutation_vo (ch.algotrader.vo.PositionMutationVO): &nbsp;
           Returns:
               PositionMutation
        """
        _id = position_mutation_vo.getId()
        quantity = position_mutation_vo.getQuantity()
        previous_quantity = position_mutation_vo.getPreviousQuantity()
        cost = position_mutation_vo.getCost()
        realized_pl = position_mutation_vo.getRealizedPL()
        portfolio_id = position_mutation_vo.getPortfolioId()
        security_id = position_mutation_vo.getSecurityId()
        account_id = position_mutation_vo.getAccountId()
        transaction_id = position_mutation_vo.getTransactionId()
        transaction_date_time = \
            Conversions.zoned_date_time_to_python_datetime(position_mutation_vo.getTransactionDateTime())
        transaction_ext_id = position_mutation_vo.getTransactionExtId()
        transaction_quantity = position_mutation_vo.getTransactionQuantity()
        transaction_price = position_mutation_vo.getTransactionPrice()
        transaction_type = None
        if position_mutation_vo.getTransactionType() is not None:
            transaction_type = position_mutation_vo.getTransactionType()
        int_order_id = position_mutation_vo.getIntOrderId()
        ext_order_id = position_mutation_vo.getExtOrderId()
        position_mutation = PositionMutation(_id, quantity, previous_quantity, cost, realized_pl,
                                             portfolio_id, security_id, account_id, transaction_id,
                                             transaction_date_time, transaction_ext_id, transaction_quantity,
                                             transaction_price, transaction_type, int_order_id, ext_order_id)
        return position_mutation


class SessionEvent:
    """Mirrors SessionEventVO Java class. External service session event

        Attributes:
            state (str): "DISCONNECTED", "CONNECTED", "IDLE", "LOGGED_ON", "SUBSCRIBED"
            qualifier (str): &nbsp;
            timestamp (datetime): &nbsp;
    """

    def __init__(self, state, qualifier, timestamp):
        # type: (str, str, datetime) -> None
        self.state = state  # "DISCONNECTED", "CONNECTED", "IDLE", "LOGGED_ON", "SUBSCRIBED"
        self.qualifier = qualifier
        self.timestamp = timestamp

    @staticmethod
    def convert_to_session_event(session_event_vo):
        # type: (JavaObject) -> SessionEvent
        """Converts Java value object to the Python object.

           Arguments:
               session_event_vo (ch.algotrader.vo.SessionEventVO): &nbsp;
           Returns:
               SessionEvent
        """
        state = None
        if session_event_vo.getState() is not None:
            state = session_event_vo.getState().toString()
        qualifier = session_event_vo.getQualifier()
        timestamp = Conversions.zoned_date_time_to_python_datetime(session_event_vo.getTimestamp())
        session_event = SessionEvent(state, qualifier, timestamp)
        return session_event


class CurrencyAmount:
    """Mirrors CurrencyAmountVO Java class. Represents an amount in a particular currency.

        Attributes:
            currency (str): &nbsp;
            amount (Decimal): &nbsp;
    """

    def __init__(self, currency, amount):
        # type: (str, Decimal) -> None
        self.currency = currency
        self.amount = amount

    @staticmethod
    def convert_to_currency_amount(currency_amount_vo):
        # type: (JavaObject) -> CurrencyAmount
        """Converts Java value object to the Python object.

           Arguments:
               currency_amount_vo (ch.algotrader.vo.CurrencyAmountVO): &nbsp;
           Returns:
               CurrencyAmount
        """
        currency = currency_amount_vo.getCurrency()
        amount = currency_amount_vo.getAmount()
        currency_amount = CurrencyAmount(currency, amount)
        return currency_amount


class NamedCurrencyAmount(CurrencyAmount):
    """Mirrors NamedCurrencyAmountVO Java class.

        Attributes:
            currency (str): &nbsp;
            amount (Decimal): &nbsp;
            name (str): &nbsp;
    """

    def __init__(self, currency, amount, name):
        # type: (str, Decimal, str) -> None
        CurrencyAmount.__init__(self, currency, amount)
        self.name = name

    @staticmethod
    def convert_to_named_currency_amount(named_currency_amount_vo):
        # type: (JavaObject) -> NamedCurrencyAmount
        """Converts Java value object to the Python object.

           Arguments:
               named_currency_amount_vo (ch.algotrader.vo.NamedCurrencyAmountVO): &nbsp;
           Returns:
               NamedCurrencyAmount
        """
        currency = named_currency_amount_vo.getCurrency()
        amount = named_currency_amount_vo.getAmount()
        name = named_currency_amount_vo.getName()
        named_currency_amount = NamedCurrencyAmount(currency, amount, name)
        return named_currency_amount


class AccountEvent:
    """Mirrors AccountEventVO Java class. The event coming as result of AccountService.subscribe_account_event(..)

       Attributes:
           account_id (int): &nbsp;
           account_balances (List of algotrader_com.domain.entity.NamedCurrencyAmount): &nbsp;
    """

    def __init__(self, account_id, account_balances):
        # type: (int, List[NamedCurrencyAmount]) -> None
        self.account_id = account_id
        self.account_balances = account_balances

    @staticmethod
    def convert_to_account_event(account_event_vo):
        # type: (JavaObject) -> AccountEvent
        """
           Arguments:
               account_event_vo (ch.algotrader.vo.AccountEventVO): &nbsp;
           Returns:
               AccountEvent
        """
        account_id = account_event_vo.getAccountId()
        account_balances0 = account_event_vo.getAccountBalances()
        account_balances = []
        i = 0
        while i < len(account_balances0):
            balance = NamedCurrencyAmount.convert_to_named_currency_amount(account_balances0[i])
            account_balances.append(balance)
            i += 1
        account_event = AccountEvent(account_id, account_balances)
        return account_event


class ExternalBalance:
    """Mirrors ExternalBalanceVO Java class.

       Attributes:
           account_id (int): &nbsp;
           asset (str): &nbsp;
           total (Decimal): &nbsp;
           available (Decimal): &nbsp;
           wallet_type (str): &nbsp;
           account_id (int): &nbsp;
           ext_id (Optional[str]): &nbsp;
    """

    def __init__(self, asset, total, available, wallet_type, account_id, ext_id):
        # type: (str, Decimal, Decimal, str, int, Optional[str]) -> None
        self.asset = asset
        self.total = total
        self.available = available
        self.wallet_type = wallet_type
        self.account_id = account_id
        self.ext_id = ext_id

    @staticmethod
    def convert_to_external_balance(external_balance_vo):
        # type: (JavaObject) -> ExternalBalance
        """
           Arguments:
               external_balance_vo (ch.algotrader.vo.ExternalBalanceVO): &nbsp;
           Returns:
               ExternalBalance
        """
        return ExternalBalance(
            asset=external_balance_vo.getAsset(),
            total=external_balance_vo.getTotal(),
            available=external_balance_vo.getAvailable(),
            wallet_type=external_balance_vo.getWalletType(),
            account_id=external_balance_vo.getAccountId(),
            ext_id=external_balance_vo.getExtId()
        )

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> ExternalBalance
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized ExternalBalanceVO): &nbsp;
           Returns:
              ExternalBalance
        """
        return ExternalBalance(
            asset=vo_dict["asset"],
            total=Conversions.float_to_decimal(vo_dict["total"]),
            available=Conversions.float_to_decimal(vo_dict["available"]),
            wallet_type=vo_dict["walletType"],
            account_id=vo_dict["accountId"],
            ext_id=vo_dict["extId"],
        )

class RfqQuote:
    """Mirrors ch.algotrader.entity.broker.QuoteVO Java class. Represents quote for rfq.

        Attributes:
           _id (int): &nbsp;
           int_id (str): The internal Id of the Quote Request associated with the Quote.
           ext_id (str): The external Quote Id.
           side (str): "BUY", "SELL"
           bid (Decimal): The bid price.
           vol_bid (Decimal): The volume on the bid side.
           ask (Decimal): The ask price
           vol_ask (Decimal): The volume on the ask side.
           date_time (datetime): The dateTime of the quote.
           valid_until (datetime): The date till the Quote is valid\
           quote_request_id (int): Represents a QuoteRequest to (a) broker(s) within the system.
           security_id (int): Security Id.
           account_id (int): Account Id.
    """

    def __init__(self, _id=None, int_id=None, ext_id=None, side=None, bid=None, vol_bid=None, ask=None, vol_ask=None,
                 date_time=None, valid_until=None, quote_request_id=None, security_id=None, account_id=None):
        # type: (int, str, str, str, Decimal, Decimal, Decimal, Decimal, datetime, datetime, int, int, int) -> None
        self.id = _id
        self.int_id = int_id
        self.ext_id = ext_id
        self.side = side
        self.bid = bid
        self.ask = ask
        self.vol_bid = vol_bid
        self.vol_ask = vol_ask
        self.date_time = date_time
        self.valid_until = valid_until
        self.quote_request_id = quote_request_id
        self.security_id = security_id
        self.account_id = account_id

    @staticmethod
    def convert_from_vo(quote_vo):
        # type: (JavaObject) -> RfqQuote
        """Converts Java value object to the Python object.

           Arguments:
               quote_vo (ch.algotrader.entity.broker.QuoteVO): &nbsp;
           Returns:
               RfqQuote
        """
        _id = quote_vo.getId()
        int_id = quote_vo.getIntId()
        ext_id = quote_vo.getExtId()
        if quote_vo.getSide() is not None:
            side = quote_vo.getSide().toString()
        else:
            side = None
        bid = quote_vo.getBidPx()
        vol_bid = quote_vo.getBidSize()
        ask = quote_vo.getAskPx()
        ask_bid = quote_vo.getAskPx()
        date_time = Conversions.zoned_date_time_to_python_datetime(quote_vo.getDateTime())
        valid_until = Conversions.zoned_date_time_to_python_datetime((quote_vo.getValidUntil()))
        quote_request_id = quote_vo.getQuoteRequestId()
        security_id = quote_vo.getSecurityId()
        account_id = quote_vo.getAccountId()
        rfq_quote = RfqQuote(_id, int_id, ext_id, side, bid, vol_bid, ask, ask_bid, date_time, valid_until,
                             quote_request_id, security_id, account_id)
        return rfq_quote


class RfqQuoteRequestReject:
    """Mirrors ch.algotrader.entity.broker.QuoteRequestRejectVO Java class.

        Attributes:
           request_int_id (str): &nbsp;
           msg (str): &nbsp;
           reject_reason (str): TIMED_OUT, BROKER_REJECT, INTERNAL_ERROR
    """

    def __init__(self, request_int_id=None, msg=None, reject_reason=None):
        # type: (str, str, str) -> None
        self.request_int_id = request_int_id
        self.msg = msg
        self.reject_reason = reject_reason

    @staticmethod
    def convert_from_vo(quote_request_reject_vo):
        # type: (JavaObject) -> RfqQuoteRequestReject
        """Converts Java value object to the Python object.

           Arguments:
               quote_request_reject_vo (ch.algotrader.entity.broker.QuoteRequestRejectVO): &nbsp;
           Returns:
               RfqQuoteRequestReject
        """

        request_int_id = quote_request_reject_vo.getRequestIntId()
        msg = quote_request_reject_vo.getMsg()
        _reject_reason = quote_request_reject_vo.getRejectReason()
        reject_reason_str = None
        if _reject_reason is not None:
            reject_reason_str = _reject_reason.toString()
        _object = RfqQuoteRequestReject(request_int_id, msg, reject_reason_str)
        return _object


class QuoteRequest:
    """Mirrors ch.algotrader.entity.broker.QuoteRequestVO Java class. Represents quote request.

        Attributes:
           _id (int): &nbsp;
           int_id (str): The internal Id of the Quote Request associated with the Quote.
           side (str): "BUY", "SELL"
           quantity (Decimal): The requested number of contracts.
           date_time (datetime): The dateTime of the quote request.
           symbol (str): Symbol of the security to request a quote for.
           account_id (int): Account Id.
           portfolio_id (int): Represents a portfolio within the system.
    """

    def __init__(self, _id=None, int_id=None, side=None, quantity=None, date_time=None, symbol=None, account_id=None,
                 portfolio_id=None, account_filter=None):
        # type: (int, str, str, Decimal, datetime, str, int, int, str) -> None
        self.id = _id
        self.int_id = int_id
        self.side = side
        self.quantity = quantity
        self.date_time = date_time
        self.symbol = symbol
        self.account_id = account_id
        self.portfolio_id = portfolio_id
        self.account_filter = account_filter

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.broker.QuoteRequestVO
        """
        vo_builder = py4jgateway.jvm.QuoteRequestVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        if self.int_id is not None:
            vo_builder.setIntId(self.int_id)
        side_type = None
        if self.side is not None:
            side_type = py4jgateway.jvm.Side.valueOf(self.side)
        vo_builder.setSide(side_type)
        vo_builder.setQuantity(self.quantity)
        if self.date_time is not None:
            date_time = Conversions.python_datetime_to_zoneddatetime(self.date_time, py4jgateway)
            vo_builder.setDateTime(date_time)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setAccountId(self.account_id)
        vo_builder.setPortfolioId(self.portfolio_id)
        vo_builder.setAccountFilter(self.account_filter)
        vo = vo_builder.build()
        return vo


class CashBalance:
    """Mirrors CashBalanceVO Java class. Represents the current cash amount of a particular portfolio in a particular currency.
        Attributes:
            id (int): &nbsp;
            currency (str): &nbsp;
            amount (Decimal): &nbsp;
            portfolio_id (int): &nbsp;
    """

    def __init__(self, _id, currency, amount, portfolio_id):
        # type: (int, str, Decimal, int) -> None
        self.id = _id
        self.currency = currency
        self.amount = amount
        self.portfolio_id = portfolio_id

    @staticmethod
    def convert_to_cash_balance(cash_balance_vo):
        # type: (JavaObject) -> CashBalance
        """Converts Java value object to the Python object.

           Arguments:
               cash_balance_vo (ch.algotrader.vo.CashBalanceVO): &nbsp;
           Returns:
              CashBalance
        """
        _id = cash_balance_vo.getId()
        currency = cash_balance_vo.getCurrency()
        amount = cash_balance_vo.getAmount()
        portfolio_id = cash_balance_vo.getPortfolioId()
        cash_balance = CashBalance(_id, currency, amount, portfolio_id)
        return cash_balance

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> CashBalance
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized CashBalanceVO): &nbsp;
           Returns:
              CashBalance
        """
        _id = vo_dict["id"]
        currency = vo_dict["currency"]
        amount = Conversions.float_to_decimal(vo_dict['amount'])
        portfolio_id = vo_dict["portfolioId"]
        cash_balance = CashBalance(_id, currency, amount, portfolio_id)
        return cash_balance


class Portfolio(PropertyHolder):
    """Mirrors PortfolioVO Java class. Represents a portfolio within the system. In addition the AlgoTrader Server is also represented by an instance of this class.

        Attributes:
            _id (int): &nbsp;
            name (str): &nbsp;
            auto_activate (bool): &nbsp;
            parent_portfolio_id (int): &nbsp;
    """

    def __init__(self, _id=None, name=None, auto_activate=None, parent_portfolio_id=None):
        # type: (int, str, bool, int) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name
        self.auto_activate = auto_activate
        self.parent_portfolio_id = parent_portfolio_id

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.portfolio.PortfolioImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object.

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
              ch.algotrader.entity.portfolio.PortfolioVO
        """
        vo_builder = py4jgateway.jvm.PortfolioVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)

        if self.parent_portfolio_id is not None:
            vo_builder.setParentPortfolioId(self.parent_portfolio_id)

        vo_builder.setName(self.name)
        vo_builder.setAutoActivate(self.auto_activate)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Portfolio
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.portfolio.PortfolioVO): &nbsp;
           Returns:
              Portfolio
        """
        _id = vo.getId()
        name = vo.getName()
        auto_activate = vo.isAutoActivate()
        parent_portfolio_id = vo.getParentPortfolioId()
        portfolio = Portfolio(_id, name, auto_activate, parent_portfolio_id)
        return portfolio


class Subscription(PropertyHolder):
    """Mirrors SubscriptionVO Java class. Market data subscription of a portfolio for particular security.

        Attributes:
            _id (int): &nbsp;
            account_id (int): &nbsp;
            portfolio_id (int): &nbsp;
            security_id (int): &nbsp;
            market_data_event_type (str): &nbsp;
    """

    def __init__(self, _id=None, account_id=None, portfolio_id=None, security_id=None,
                 market_data_event_type=None, symbol=None):
        # type: (int, str, int, int, str, str) -> None
        PropertyHolder.__init__(self, _id)
        self.account_id = account_id
        self.portfolio_id = portfolio_id
        self.security_id = security_id
        self.market_data_event_type = market_data_event_type
        self.symbol = symbol

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.SubscriptionImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
              ch.algotrader.entity.SubscriptionVO
        """
        vo_builder = py4jgateway.jvm.SubscriptionVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setAccountId(self.account_id)
        vo_builder.setPortfolioId(self.portfolio_id)
        vo_builder.setSecurityId(self.security_id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setMarketDataEventType(Conversions
                                          .convert_to_market_data_event_type_enum(self.market_data_event_type,
                                                                                  py4jgateway))
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Subscription
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.SubscriptionVO): &nbsp;
           Returns:
              Subscription
        """
        _id = vo.getId()
        account_id = vo.getAccountId()
        portfolio_id = vo.getPortfolioId()
        security_id = vo.getSecurityId()
        market_data_event_type = Conversions.get_java_object_to_string(vo.getMarketDataEventType())
        symbol = vo.getSymbol()
        portfolio = Subscription(_id, account_id, portfolio_id, security_id, market_data_event_type, symbol)
        return portfolio


class OrderPreference(PropertyHolder):
    """Mirrors OrderPreferenceVO Java class.
       Contains certain order default values (e.g. quantity, orderType, delays, etc.).
       Except for the order_type, all values have to be defined through properties

       Attributes:
           _id (int): &nbsp;
           name (str): &nbsp;
           order_type (str): &nbsp;
           default_account_id (int): &nbsp;
    """

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.trade.OrderPreferenceImpl"

    def __init__(self, _id=None, name=None, order_type=None, default_account_id=None):
        # type: (int, str, str, int) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name
        self.order_type = order_type
        self.default_account_id = default_account_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> OrderPreference
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.trade.OrderPreferenceVO): &nbsp;
           Returns:
              OrderPreference
        """
        _id = vo.getId()
        name = vo.getName()
        order_type = None
        if vo.getOrderType() is not None:
            order_type = vo.getOrderType().toString()
        default_account_id = vo.getDefaultAccountId()
        op = OrderPreference(_id, name, order_type, default_account_id)
        return op

    @staticmethod
    def convert_from_json_object(vo_dict):
        # type: (Dict) -> OrderPreference
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized OrderPreferenceVO): &nbsp;
           Returns:
              OrderPreference
        """
        if vo_dict is None:
            return None
        _id = vo_dict['id']
        name = vo_dict['name']
        order_type = None
        if vo_dict['orderType'] is not None:
            order_type = vo_dict['orderType']['name']
        default_account_id = vo_dict['defaultAccountId']
        op = OrderPreference(_id, name, order_type, default_account_id)
        return op


class PortfolioValue:
    """Mirrors PortfolioValueVO Java class. Represents certain balances (e.g. net_liq_value}, cash_balance, etc.) of a particular portfolio at a particular time.
       Every hour PortfolioValue-s are saved to the database for every portfolio. These PortfolioValue-s will be displayed in the PortfolioChart of the client.
    
       Attributes:
           id (int): &nbsp;
           date_time (datetime): &nbsp;
           net_liq_value (Decimal): &nbsp;
           market_value (Decimal): &nbsp;
           realized_pl (Decimal): &nbsp;
           unrealized_pl (Decimal): &nbsp;
           cash_balance (Decimal): &nbsp;
           open_positions (int): &nbsp;
           cash_flow (Decimal): &nbsp;
           pnl (Decimal): &nbsp;
           portfolio_id (int): &nbsp;
    """

    def __init__(self, _id=None, date_time=None, net_liq_value=None, market_value=None, realized_pl=None,
                 unrealized_pl=None, cash_balance=None, open_positions=None, cash_flow=None, pnl=None, portfolio_id=None):
        # type: (int, datetime, Decimal, Decimal, Decimal, Decimal, Decimal, int, Decimal, Decimal, int) -> None
        self.id = _id
        self.date_time = date_time
        self.net_liq_value = net_liq_value
        self.market_value = market_value
        self.realized_pl = realized_pl
        self.unrealized_pl = unrealized_pl
        self.cash_balance = cash_balance
        self.open_positions = open_positions
        self.cash_flow = cash_flow
        self.pnl = pnl
        self.portfolio_id = portfolio_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> PortfolioValue
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.portfolio.PortfolioValueVO): &nbsp;
           Returns:
              PortfolioValue
        """
        _id = vo.getId()
        date_time = None
        if vo.getDateTime() is not None:
            date_time = Conversions.zoned_date_time_to_python_datetime(vo.getDateTime())
        net_liq_value = vo.getNetLiqValue()
        market_value = vo.getMarketValue()
        realized_pl = vo.getRealizedPL()
        unrealized_pl = vo.getUnrealizedPL()
        cash_balance = vo.getCashBalance()
        open_positions = vo.getOpenPositions()
        cash_flow = vo.getCashFlow()
        pnl = vo.getPnl()
        portfolio_id = vo.getPortfolioId()
        portfolio_value = PortfolioValue(_id, date_time, net_liq_value, market_value, realized_pl, unrealized_pl,
                                         cash_balance, open_positions, cash_flow, pnl, portfolio_id)
        return portfolio_value

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> PortfolioValue
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized PortfolioValueVO): &nbsp;
           Returns:
              PortfolioValue
        """
        _id = vo_dict["id"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict["dateTime"])
        net_liq_value = Conversions.float_to_decimal(vo_dict["netLiqValue"])
        market_value = Conversions.float_to_decimal(vo_dict["marketValue"])
        realized_pl = Conversions.float_to_decimal(vo_dict["realizedPL"])
        unrealized_pl = Conversions.float_to_decimal(vo_dict["unrealizedPL"])
        cash_balance = Conversions.float_to_decimal(vo_dict["cashBalance"])
        open_positions = vo_dict["openPositions"]
        cash_flow = Conversions.float_to_decimal(vo_dict["cashFlow"])
        pnl = Conversions.float_to_decimal(vo_dict["pnl"])
        portfolio_id = vo_dict["portfolioId"]
        portfolio_value = PortfolioValue(_id, date_time, net_liq_value, market_value, realized_pl, unrealized_pl,
                                         cash_balance, open_positions, cash_flow, pnl, portfolio_id)
        return portfolio_value


class Balance:
    """Mirrors BalanceVO Java class. A value object representing different balances of a particular currency.
    
       Attributes:
           currency (str): &nbsp;
           cash (Decimal): &nbsp;
           securities (Decimal): &nbsp;
           net_liq_value (Decimal): &nbsp;
           unrealized_pl (Decimal): &nbsp;
           cash_base (Decimal): &nbsp;
           securities_base (Decimal): &nbsp;
           net_liq_value_base (Decimal): &nbsp;
           unrealized_pl_base (Decimal): &nbsp;
           exchange_rate (float): &nbsp;
    """

    def __init__(self, currency=None, cash=None, securities=None, net_liq_value=None, unrealized_pl=None,
                 cash_base=None, securities_base=None, net_liq_value_base=None, unrealized_pl_base=None,
                 exchange_rate=None):
        # type: (str, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, float) -> None
        self.currency = currency
        self.cash = cash
        self.securities = securities
        self.net_liq_value = net_liq_value
        self.unrealized_pl = unrealized_pl
        self.cash_base = cash_base
        self.securities_base = securities_base
        self.net_liq_value_base = net_liq_value_base
        self.unrealized_pl_base = unrealized_pl_base
        self.exchange_rate = exchange_rate

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Balance
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.vo.BalanceVO): &nbsp;
           Returns:
              Balance
        """
        currency = vo.getCurrency()
        cash = vo.getCash()
        securities = vo.getSecurities()
        net_liq_value = vo.getNetLiqValue()
        unrealized_pl = vo.getUnrealizedPL()
        cash_base = vo.getCashBase()
        securities_base = vo.getSecuritiesBase()
        net_liq_value_base = vo.getNetLiqValueBase()
        unrealized_pl_base = vo.getUnrealizedPLBase()
        exchange_rate = vo.getExchangeRate()
        balance = Balance(currency, cash, securities, net_liq_value, unrealized_pl, cash_base, securities_base,
                          net_liq_value_base, unrealized_pl_base, exchange_rate)
        return balance

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> Balance
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized BalanceVO): &nbsp;
           Returns:
              Balance
        """
        currency = vo_dict["currency"]
        cash = Conversions.float_to_decimal(vo_dict["cash"])
        securities = Conversions.float_to_decimal(vo_dict["securities"])
        net_liq_value = Conversions.float_to_decimal(vo_dict["netLiqValue"])
        unrealized_pl = Conversions.float_to_decimal(vo_dict["unrealizedPL"])
        cash_base = Conversions.float_to_decimal(vo_dict["cashBase"])
        securities_base = Conversions.float_to_decimal(vo_dict["securitiesBase"])
        net_liq_value_base = Conversions.float_to_decimal(vo_dict["netLiqValueBase"])
        unrealized_pl_base = Conversions.float_to_decimal(vo_dict["unrealizedPLBase"])
        exchange_rate = vo_dict["exchangeRate"]
        balance = Balance(currency, cash, securities, net_liq_value, unrealized_pl, cash_base, securities_base,
                          net_liq_value_base, unrealized_pl_base, exchange_rate)
        return balance


class FxExposure:
    """Mirrors FxExposureVO Java class. A value object representing different balances of a particular currency.

       Attributes:
           currency (str): &nbsp;
           amount (Decimal): &nbsp;
           amount_base (Decimal): &nbsp;
           exchange_rate (float): &nbsp;
    """

    def __init__(self, currency=None, amount=None, amount_base=None, exchange_rate=None):
        # type: (str, Decimal, Decimal, float) -> None
        self.currency = currency
        self.amount = amount
        self.amount_base = amount_base
        self.exchange_rate = exchange_rate

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> FxExposure
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.vo.FxExposureVO): &nbsp;
           Returns:
              FxExposure
        """
        currency = vo.getCurrency()
        amount = vo.getAmount()
        amount_base = vo.getAmountBase()
        exchange_rate = vo.getExchangeRate()
        fx_exposure = FxExposure(currency, amount, amount_base, exchange_rate)
        return fx_exposure

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> FxExposure
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized FxExposureVO): &nbsp;
           Returns:
              FxExposure
        """
        currency = vo_dict["currency"]
        amount = Conversions.float_to_decimal(vo_dict["amount"])
        amount_base = Conversions.float_to_decimal(vo_dict["amountBase"])
        exchange_rate = vo_dict["exchangeRate"]
        fx_exposure = FxExposure(currency, amount, amount_base, exchange_rate)
        return fx_exposure


class Position(PropertyHolder):
    """Mirrors PositionVO Java class.

    A position of a particular security owned by a particular portfolio. For each opening transaction a position is created.
    The position object remains in place even if a corresponding closing transaction is carried out and the quantity of the position becomes 0.
    Since some values (e.g. market_value) depend on whether the position is long or short, aggregated position values for the same security (of different strategies) cannot be retrieved just by adding position values from the corresponding strategies.

    Example:

     *   Security: VIX Dec 2012/li

     *   Current Bid: 16.50/li

     *   Current Ask: 16.60/li

     *   Portfolio A: quantity +10 marketValue: 10 * 1000 * 16.50 = 165000/li

     *   Portfolio B: quantity -10 marketValue: 10 * 1000 * 16.60 = -166000/li

    The sum of above marketValues would be -1000 which is obviously wrong.
    As a consequence the PortfolioService provides lookup-methods that aggregate positions from the same security (of different strategies) in the correct manner.
    
    Attributes:
        _id (int): &nbsp;
        quantity (Decimal): &nbsp;
        cost (Decimal): &nbsp;
        realized_pl (Decimal): &nbsp;
        portfolio_id (int): &nbsp;
        security_id (int): &nbsp;
    """

    def __init__(self, _id=None, quantity=None, cost=None, realized_pl=None, portfolio_id=None,
                 security_id=None):
        # type: (int, Decimal, Decimal, Decimal, int, int) -> None
        PropertyHolder.__init__(self, _id)
        self.quantity = quantity
        self.cost = cost
        self.realized_pl = realized_pl
        self.portfolio_id = portfolio_id
        self.security_id = security_id

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.PositionImpl"

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Position
        """
           Arguments:
               vo (ch.algotrader.entity.PositionVO): &nbsp;
           Returns:
              Position
        """
        _id = vo.getId()
        quantity = vo.getQuantity()
        cost = vo.getCost()
        realized_pl = vo.getRealizedPL()
        portfolio_id = vo.getPortfolioId()
        security_id = vo.getSecurityId()
        position = Position(_id, quantity, cost, realized_pl, portfolio_id, security_id)
        return position

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> Position
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized PositionVO): &nbsp;
           Returns:
              Position
        """
        _id = vo_dict["id"]
        quantity = Conversions.float_to_decimal(vo_dict["quantity"])
        cost = Conversions.float_to_decimal(vo_dict["cost"])
        realized_pl = Conversions.float_to_decimal(vo_dict["realizedPL"])
        portfolio_id = vo_dict["portfolioId"]
        security_id = vo_dict["securityId"]
        position = Position(_id, quantity, cost, realized_pl, portfolio_id, security_id)
        return position


class Provider(PropertyHolder):
    """Morrors ProviderVO Java class.

        Attributes:
            _id (int): &nbsp;
            name (str): &nbsp;
    """

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.ProviderImpl"

    def __init__(self, _id=None, name=None):
        # type: (int, str) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Account
        """
           Arguments:
               vo (ch.algotrader.entity.ProviderVO): &nbsp;
           Returns:
              Provider
        """
        _id = vo.getId()
        name = vo.getName()
        provider = Provider(_id, name)
        return provider


class Account(PropertyHolder):
    """Mirrors AccountVO Java class. Represents an actual Account / AccountGroup / AllocationProfile with an external Broker / Bank
    
       Attributes:
           _id (int): &nbsp;
           name (str): &nbsp;
           active (bool): &nbsp;
           primary_for_trading (bool): &nbsp;
           primary_for_market_data (bool): &nbsp;
           provider_id (int): &nbsp;
           session_qualifier (str): &nbsp;
           ext_account (str): &nbsp;
           ext_account_group (str): &nbsp;
           ext_allocation_profile (str): &nbsp;
           ext_clearing_account (str): &nbsp;
           rfq_supported (bool): &nbsp;
    """

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.AccountImpl"

    def __init__(self, _id=None, name=None, active=None, primary_for_trading=None, primary_for_market_data=None, primary_for_reference_data=None,
                 provider_id=None, connector_descriptor=None, session_qualifier=None, ext_account=None,
                 ext_account_group=None, ext_allocation_profile=None, ext_clearing_account=None, rfq_supported=None):
        # type: (int, str, bool, bool, bool, int, str, str, str, str, str, str, bool) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name
        self.active = active
        self.primary_for_trading = primary_for_trading
        self.primary_for_market_data = primary_for_market_data
        self.primary_for_reference_data = primary_for_reference_data
        self.provider_id = provider_id
        self.connector_descriptor = connector_descriptor
        self.session_qualifier = session_qualifier
        self.ext_account = ext_account
        self.ext_account_group = ext_account_group
        self.ext_allocation_profile = ext_allocation_profile
        self.ext_clearing_account = ext_clearing_account
        self.rfq_supported = rfq_supported

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Account
        """
           Arguments:
               vo (ch.algotrader.entity.AccountVO): &nbsp;
           Returns:
              Account
        """
        _id = vo.getId()
        name = vo.getName()
        active = vo.isActive()
        primary_for_trading = vo.isPrimaryForTrading()
        primary_for_market_data = vo.isPrimaryForMarketData()
        primary_for_reference_data = vo.isPrimaryForReferenceData()
        provider_id = vo.getProviderId()
        connector_descriptor = vo.getConnectorDescriptor().getDescriptor()
        session_qualifier = vo.getSessionQualifier()
        ext_account = vo.getExtAccount()
        ext_account_group = vo.getExtAccountGroup()
        ext_allocation_profile = vo.getExtAllocationProfile()
        ext_clearing_account = vo.getExtClearingAccount()
        rfq_supported = vo.isRfqSupported()
        account = Account(_id, name, active, primary_for_trading, primary_for_market_data, primary_for_reference_data, provider_id,
                          connector_descriptor, session_qualifier, ext_account,
                          ext_account_group, ext_allocation_profile, ext_clearing_account, rfq_supported)
        return account


class SubAccount(PropertyHolder):
    """Mirrors SubAccountVO Java class. Represents a SubAccount connected to one of the Accounts

       Attributes:
           _id (int): &nbsp;
           name (str): &nbsp;
           account_id (int): &nbsp;
           ext_id (str): &nbsp;
    """

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.SubAccountImpl"

    def __init__(self, _id=None, name=None, account_id=None, ext_id=None):
        # type: (int, str, int, str) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name
        self.account_id = account_id
        self.ext_id = ext_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> SubAccount
        """
           Arguments:
               vo (ch.algotrader.entity.SubAccountVO): &nbsp;
           Returns:
              SubAccount
        """
        _id = vo.getId()
        name = vo.getName()
        account_id = vo.getAccountId()
        ext_id = vo.getExtId()
        account = Account(_id, name, account_id, ext_id)
        return account


class RoutingTarget:
    """Mirrors RoutingTargetVO Java class.

        Attributes:
            security_id (int): &nbsp;
            account_id (int): &nbsp;
            exchange_id (int): &nbsp;
    """

    def __init__(self, security_id, account_id, exchange_id):
        # type: (int, int, int) -> None
        self.security_id = security_id
        self.account_id = account_id
        self.exchange_id = exchange_id

    def convert_to_vo(self, py4jgateway):
        """Converts the RoutingTarget to Java value object"""
        vo = py4jgateway.jvm.RoutingTargetVO(self.security_id, self.account_id, self.exchange_id)  # java class
        return vo

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> RoutingTarget
        """
           Arguments:
               vo (ch.algotrader.entity.trade.algo.RoutingTargetVO): &nbsp;
           Returns:
              RoutingTarget
        """
        security_id = vo.getSecurityId()
        account_id = vo.getAccountId()
        exchange_id = vo.getExchangeId()
        rt = RoutingTarget(security_id, account_id, exchange_id)
        return rt

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> RoutingTarget
        """Converts JSON dictionary object to the Python object.

           Arguments:
               vo_dict (deserialized RoutingTargetVO): &nbsp;
           Returns:
              RoutingTarget
        """
        security_id = vo_dict["securityId"]
        account_id = vo_dict["accountId"]
        exchange_id = vo_dict["exchangeId"]
        rt = RoutingTarget(security_id, account_id, exchange_id)
        return rt


class SecurityFamily(PropertyHolder):
    """Mirrors SecurityFamilyVO Java class.
       Represents an entire family of similar Security-s (e.g. all options of the SP500)

       Attributes:
           _id (int): &nbsp;
           name (str): &nbsp;
           symbol_root (str): &nbsp;
           isin_root (str): &nbsp;
           ric_root (str): &nbsp;
           currency (str): &nbsp;
           contract_size (float): &nbsp;
           price_incr (Decimal): &nbsp;
           family_type (str): &nbsp;
           underlying_id (int): &nbsp;
           exchange_id (int): &nbsp;
       """

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.security.SecurityFamilyImpl"

    def __init__(self, _id=None, name=None, symbol_root=None, isin_root=None, ric_root=None, currency=None,
                 contract_size=None, price_incr=None, family_type=None,
                 underlying_id=None, exchange_id=None):
        # type: (int, str, str, str, str, str, float, Decimal, str, int, int) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name
        self.symbol_root = symbol_root
        self.isin_root = isin_root
        self.ric_root = ric_root
        self.currency = currency
        self.contract_size = contract_size
        self.price_incr = price_incr
        self.family_type = family_type
        self.underlying_id = underlying_id
        self.exchange_id = exchange_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> SecurityFamily
        """
           Arguments:
               vo (ch.algotrader.entity.security.SecurityFamilyVO): &nbsp;
           Returns:
              SecurityFamily
        """
        _id = vo.getId()
        name = vo.getName()
        symbol_root = vo.getSymbolRoot()
        isin_root = vo.getIsinRoot()
        ric_root = vo.getRicRoot()
        currency = vo.getCurrency()
        contract_size = vo.getContractSize()
        price_incr = vo.getPriceIncr()
        family_type = None
        if vo.getFamilyType() is not None:
            family_type = vo.getFamilyType().toString()
        underlying_id = vo.getUnderlyingId()
        exchange_id = vo.getExchangeId()
        sf = SecurityFamily(_id, name, symbol_root, isin_root, ric_root, currency, contract_size, price_incr,
                            family_type, underlying_id, exchange_id)  # java class
        return sf


class Exchange(PropertyHolder):
    """Mirrors ExchangeVO Java class. Exchange where securities are traded.
    
       Attributes:
           _id (int): &nbsp;
           name (str): &nbsp;
           code (str): &nbsp;
           trading_view_id (str): &nbsp;
           mic (str): &nbsp;
           bloomberg_code (str): &nbsp;
           ib_code (str): &nbsp;
           tt_code (str): &nbsp;
           cnp_id (str): &nbsp;
           time_zone (str): &nbsp;
           margin_trading (bool): &nbsp;
           exchange_trading (bool): &nbsp;
    """

    def __init__(self, _id=None, name=None, code=None, trading_view_id=None, mic=None, bloomberg_code=None, ib_code=None, tt_code=None,
                 cnp_id=None, time_zone=None, margin_trading=None, exchange_trading=None):
        # type: (int, str, str, str, str, str, str, str, str, str, bool, bool) -> None
        PropertyHolder.__init__(self, _id)
        self.name = name
        self.code = code
        self.trading_view_id = trading_view_id
        self.mic = mic
        self.bloomberg_code = bloomberg_code
        self.ib_code = ib_code
        self.tt_code = tt_code
        self.cnp_id = cnp_id
        self.time_zone = time_zone
        self.margin_trading = margin_trading
        self.exchange_trading = exchange_trading

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the Exchange to the corresponding Java value object.

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.exchange.ExchangeVO
        """
        vo = py4jgateway.jvm.ch.algotrader.entity.exchange.ExchangeVO(self.id, self.name, self.code,
                                                                      self.trading_view_id, self.mic,
                                                                      self.bloomberg_code, self.ib_code, self.tt_code,
                                                                      self.cnp_id, self.time_zone, self.margin_trading,
                                                                      self.exchange_trading)
        return vo

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.exchange.ExchangeImpl"

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Exchange
        """
           Arguments:
               vo (ch.algotrader.entity.exchange.ExchangeVO): &nbsp;
           Returns:
              Exchange
        """
        _id = vo.getId()
        name = vo.getName()
        code = vo.getCode()
        trading_view_id = vo.getTradingViewId()
        mic = vo.getMic()
        bloomberg_code = vo.getBloombergCode()
        ib_code = vo.getIbCode()
        tt_code = vo.getTtCode()
        cnp_id = vo.getCnpid()
        time_zone = vo.getTimeZone()
        margin_trading = vo.isMarginTrading()
        exchange_trading = vo.isExchangeTrading()
        exchange = Exchange(_id, name, code, trading_view_id, mic, bloomberg_code, ib_code, tt_code, cnp_id, time_zone,
                            margin_trading, exchange_trading)
        return exchange


class Component:
    """Mirrors ComponentVO Java class.
       Represents one component of a Combination.

       Attributes:
           id (int): &nbsp;
           quantity (Decimal): &nbsp;
           combination_id (int): &nbsp;
           security_id (int): &nbsp;
       """

    def __init__(self, _id, quantity, combination_id, security_id):
        # type: (int, Decimal, int, int) -> None
        self.id = _id
        self.quantity = quantity
        self.combination_id = combination_id
        self.security_id = security_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> Component
        """
           Arguments:
               vo (ch.algotrader.entity.security.ComponentVO): &nbsp;
           Returns:
              Component
        """
        _id = vo.getId()
        quantity = vo.getQuantity()
        combination_id = vo.getCombinationId()
        security_id = vo.getSecurityId()
        component = Component(_id, quantity, combination_id, security_id)
        return component


class TradingHours:
    """Mirrors TradingHoursVO Java class.
       Weekly trading hours for a particular exchange.
       
       Attributes:
           id (int): &nbsp;
           open (str): &nbsp;
           close (str): &nbsp;
           sunday (bool): &nbsp;
           monday (bool): &nbsp;
           tuesday (bool): &nbsp;
           wednesday (bool): &nbsp;
           thursday (bool): &nbsp;
           friday (bool): &nbsp;
           saturday (bool): &nbsp;
           exchange_id (int): &nbsp;
       """

    def __init__(self, _id, _open, close, sunday, monday, tuesday, wednesday, thursday, friday, saturday, exchange_id):
        # type: (int, str, str, bool, bool, bool, bool, bool, bool, bool, int) -> None
        self.id = _id
        self.open = _open
        self.close = close
        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.exchange_id = exchange_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> TradingHours
        """
           Arguments:
               vo (ch.algotrader.entity.exchange.TradingHoursVO): &nbsp;
           Returns:
              TradingHours
        """
        _id = vo.getId()
        _open = vo.getOpen().toString()
        close = vo.getClose().toString()
        sunday = vo.isSunday()
        monday = vo.isMonday()
        tuesday = vo.isTuesday()
        wednesday = vo.isWednesday()
        thursday = vo.isThursday()
        friday = vo.isFriday()
        saturday = vo.isSaturday()
        exchange_id = vo.getExchangeId()
        th = TradingHours(_id, _open, close, sunday, monday, tuesday, wednesday,
                          thursday, friday, saturday, exchange_id)
        return th


class WithdrawStatus:
    """Mirrors WithdrawStatusVO Java class.

       Attributes:
           message (str): &nbsp;
           success (bool): &nbsp;
           external_id (str): &nbsp;
    """

    def __init__(self, message, success, external_id):
        # type: (str, bool, str) -> None
        self.message = message
        self.success = success
        self.external_id = external_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> WithdrawStatus
        """
           Arguments:
               vo (ch.algotrader.vo.WithdrawStatusVO): &nbsp;
           Returns:
              WithdrawStatus
        """
        message = vo.getMessage()
        success = vo.getSuccess()
        external_id = vo.getExternalId()
        obj = WithdrawStatus(message, success, external_id)
        return obj


class Measurement:
    """Mirrors MeasurementVO Java class.
       Custom measurement of type int, float, money (Decimal), text (str) or bool related to a portfolio and a particular time.

       Attributes:
           id (int): &nbsp;
           name (str): &nbsp;
           date_time (datetime): &nbsp;
           int_value (int): &nbsp;
           double_value (float): &nbsp;
           money_value (Decimal): &nbsp;
           text_value (str): &nbsp;
           boolean_value (bool): &nbsp;
           portfolio_id (int): &nbsp;
       """

    def __init__(self, _id, name, date_time, int_value=None, double_value=None,
                 money_value=None, text_value=None, boolean_value=None, portfolio_id=None):
        # type: (int, str, datetime, int, float, Decimal, str, bool, int) -> None
        self.id = _id
        self.name = name
        self.date_time = date_time
        self.int_value = int_value
        self.double_value = double_value
        self.money_value = money_value
        self.text_value = text_value
        self.boolean_value = boolean_value
        self.portfolio_id = portfolio_id

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> Measurement
        """Converts JSON dictionary object to the Python object.

           Arguments:
              vo_dict (deserialized MeasurementVO): &nbsp;
           Returns:
              Measurement
        """
        _id = vo_dict["id"]
        date_time = Conversions.epoch_millis_to_python_datetime(vo_dict['dateTime'])
        name = vo_dict["name"]
        int_value = vo_dict["intValue"]
        double_value = vo_dict["doubleValue"]
        money_value = Conversions.float_to_decimal(vo_dict["moneyValue"])
        text_value = vo_dict["textValue"]
        boolean_value = vo_dict["booleanValue"]
        portfolio_id = vo_dict["portfolioId"]
        order_status = Measurement(_id, name, date_time, int_value, double_value, money_value, text_value,
                                   boolean_value, portfolio_id)
        return order_status


class WalletEvent:
    """Mirrors WalletEventVO Java class.

       Attributes:
           transaction_id (str): &nbsp;
           type (str): &nbsp;
           amount (Decimal): &nbsp;
           currency (str): &nbsp;
           address (str): &nbsp;
           description (str): &nbsp;
           status (str): &nbsp;
           date (datetime): &nbsp;
       """

    def __init__(self, transaction_id=None, _type=None, amount=None, currency=None, address=None,
                 description=None, status=None, date=None):
        # type: (str, str, Decimal, str, str, str, str, datetime) -> None
        self.transaction_id = transaction_id
        self.type = _type
        self.amount = amount
        self.currency = currency
        self.address = address
        self.description = description
        self.status = status
        self.date = date

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> WalletEvent
        """
           Arguments:
              vo (ch.algotrader.vo.WalletEventVO): &nbsp;
           Returns:
              WalletEvent
        """
        transaction_id = vo.getTransactionId()
        _type = None
        vo_type = vo.getType()
        if vo_type is not None:
            _type = vo_type.toString()
        amount = vo.getAmount()
        currency = vo.getCurrency()
        address = vo.getAddress()
        description = vo.getDescription()
        status = vo.getStatus()
        date = Conversions.zoned_date_time_to_python_datetime(vo.getDate())
        return WalletEvent(transaction_id, _type, amount, currency, address, description, status, date)


class ReconciliationEvent:
    """Mirrors ReconciliationEventVO Java class.
       Reconciliation event.
       Indicates reconciliation process activities per adapter.
       After subscription to reconciliation events, client will be notified about each
       reconciliation procedure start and finish.

    Attributes:
        state (str): STARTED, FINISHED
        account_id (int): &nbsp;
       """

    def __init__(self, state=None, account_id=None):
        # type: (str, str) -> None
        self.state = state
        self.account_id = account_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> ReconciliationEvent
        """
           Arguments:
              vo (ch.algotrader.vo.ReconciliationEventVO): &nbsp;
           Returns:
              ReconciliationEvent
        """
        vo_state = vo.getState()
        state = None
        if vo_state is not None:
            state = vo_state.toString()
        account_id = vo.getAccountId()
        return ReconciliationEvent(state, account_id)


class OrderRequestStatusEvent:
    """Mirrors OrderRequestStatusEvent Java class.

    Attributes:
        status (str): SUCCESS, REJECTED_BY_EXCHANGE, INTERNAL_FAILURE
        request_type (str): SUBMIT, MODIFY, CANCEL
        order_id (int): &nbsp;
        error_message (str): &nbsp;
       """

    def __init__(self, status=None, request_type=None, order_id=None, error_message=None):
        # type: (str, str, int, str) -> None
        self.status = status
        self.request_type = request_type
        self.order_id = order_id
        self.error_message = error_message

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> OrderRequestStatusEvent
        """
           Arguments:
              vo (ch.algotrader.vo.OrderRequestStatusEventVO): &nbsp;
           Returns:
              OrderRequestStatusEvent
        """
        vo_status = vo.getStatus()
        status = None
        if vo_status is not None:
            status = vo_status.toString()
        vo_request_type = vo.getRequestType()
        request_type = None
        if vo_request_type is not None:
            request_type = vo_request_type.toString()
        order_id = None
        order_vo = vo.getOrderVO()
        if order_vo is not None:
            order_id = order_vo.getId()
        error_message = None
        throwable = vo.getThrowable()
        if throwable is not None:
            error_message = throwable.getMessage()
        return OrderRequestStatusEvent(status, request_type, order_id, error_message)


class GenericEvent:
    """
    Attributes:
        time (datetime): &nbsp;
        .. include:: ../adapter_types.txt
        _id (str): &nbsp;
    """

    def __init__(self, time, connector_descriptor, event_type, identifiers, properties):
        # type: (datetime, str, str, dict, dict) -> None
        self.time = time
        self.connector_descriptor = connector_descriptor
        self.type = event_type
        self.identifiers = identifiers
        self.properties = properties

    @staticmethod
    def java_class_name():
        # type: () -> str
        return "ch.algotrader.entity.GenericEventVO"

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> GenericEvent
        """
           Arguments:
              java_object (ch.algotrader.entity.GenericEventVO): &nbsp;
           Returns:
              GenericEvent
        """
        time = Conversions.java_instant_to_python_datetime(java_object.getDateTime().toInstant())
        connector_descriptor = java_object.getConnectorDescriptor().getDescriptor()
        event_type = java_object.getType().getName()

        java_identifiers = java_object.getIdentity().getIdentifiers()
        identifiers = {}
        for key in java_identifiers:
            identifiers[key] = java_identifiers[key]

        java_properties = java_object.getProperties()
        properties = {}
        for key in java_properties:
            properties[key] = java_properties[key]

        event = GenericEvent(time, connector_descriptor, event_type, identifiers, properties)
        return event

    def convert_to_java_object(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """
           Arguments:
              py4jgateway (ClientServer): &nbsp;
           Returns:
              ch.algotrader.entity.GenericEventVO
        """
        time = Conversions.python_datetime_to_zoneddatetime(self.time, py4jgateway)
        connector_descriptor = Conversions.convert_to_connector_descriptor(self.connector_descriptor, py4jgateway)
        event_type = Conversions.convert_to_generic_event_type(self.type, py4jgateway)

        builder = py4jgateway.jvm.GenericEventVO.builder()
        builder.setDateTime(time)
        builder.setType(event_type)
        builder.setConnectorDescriptor(connector_descriptor)

        for key in self.identifiers:
            builder.addIdentifier(key, self.identifiers[key])

        for key in self.properties:
            val = self.properties[key]
            # convert py Numbers to java BigDecimals or leave as string
            if not isinstance(val, Decimal) and isinstance(val, Number):
                val = py4jgateway.jvm.BigDecimal(val)
            builder.setProperty(key, val)

        vo = builder.build()
        return vo


class PortfolioValueDeltaSummary:
    """
    Attributes:
        realized_pl_delta (Decimal): Realized P&L delta
        unrealized_pl (Decimal): Unrealized P&L
    """

    def __init__(self, realized_pl_delta, unrealized_pl):
        # type: (Decimal, Decimal) -> None
        self.realized_pl_delta = realized_pl_delta
        self.unrealized_pl = unrealized_pl

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> PortfolioValueDeltaSummary
        """
           Arguments:
              java_object (ch.algotrader.entity.portfolio.PortfolioValueDeltaSummary): &nbsp;
           Returns:
              PortfolioValueDeltaSummary
        """
        realized_pl_delta = java_object.getRealizedPLDelta()
        unrealized_pl = java_object.getUnrealizedPL()
        return PortfolioValueDeltaSummary(realized_pl_delta, unrealized_pl)


class LogEvent:
    """
        Attributes:
            event_message (str): &nbsp;
            priority (str): &nbsp;
            exception_class (JavaObject): &nbsp;
            exception_message (str): &nbsp;
            human_readable_message (str): &nbsp;
            event_category (str): GENERAL, ADAPTER, VALIDATION, SECURITY, ENGINE, IO, PERSISTENCE, REPORT
    """

    def __init__(self, event_message, priority, exception_class, exception_message, human_readable_message,
                 event_category):
        # type: (str, str, JavaObject, str, str, str) -> None
        self.event_message = event_message
        self.priority = priority
        self.exception_class = exception_class
        self.exception_message = exception_message
        self.human_readable_message = human_readable_message
        self.event_category = event_category

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> LogEvent
        """
           Arguments:
              java_object (ch.algotrader.vo.LogEventVO): &nbsp;
           Returns:
              LogEvent
        """
        event_message = java_object.getEventMessage()
        priority = java_object.getPriority()
        exception_class = java_object.getExceptionClass()
        exception_message = java_object.getExceptionMessage()
        human_readable_message = java_object.getHumanReadableMessage()
        event_category = None
        if java_object.getEventCategory() is not None:
            event_category = java_object.getEventCategory().name()

        return LogEvent(event_message, priority, exception_class, exception_message, human_readable_message,
                        event_category)


class HealthStatus:
    """
        Attributes:
            status (str): ALIVE, HEALTH, DEAD
            msg (str): &nbsp;
            service_name (str): &nbsp;
    """

    def __init__(self, status, msg, service_name):
        # type: (str, str, str) -> None
        self.status = status
        self.msg = msg
        self.service_name = service_name

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> HealthStatus
        """
           Arguments:
              java_object (ch.algotrader.vo.HealthStatusVO): &nbsp;
           Returns:
              HealthStatus
        """
        status = None
        statusvo = java_object.getStatus()
        if statusvo is not None:
            status = java_object.getStatus().name()
        msg = java_object.getMsg()
        service_name = java_object.getServiceName()

        return HealthStatus(status, msg, service_name)


class SimulationResult:
    """
            Attributes:
                dict (Dict): &nbsp;
        """

    def __init__(self, dict):
        # type: (Dict) -> None
        self.dict = dict

    @staticmethod
    def convert_from_json(vo_dict):
        # type: (Dict) -> SimulationResult
        """
           Arguments:
              vo_dict (deserialized ch.algotrader.vo.performance.SimulationResultVO): &nbsp;
           Returns:
              str
        """
        dict = vo_dict
        return SimulationResult(dict)


class TradedVolume:
    """
        Attributes:
            start_time (datetime): &nbsp;
            end_time (datetime): &nbsp;
            .. include:: ../adapter_types.txt
            security_id (int): &nbsp;
            traded_volume (Decimal): &nbsp;
    """

    def __init__(self, start_time=None, end_time=None, connector_descriptor=None, security_id=None, traded_volume=None):
        # type: (datetime, datetime, str, int, Decimal) -> None
        self.start_time = start_time
        self.end_time = end_time
        self.connector_descriptor = connector_descriptor
        self.security_id = security_id
        self.traded_volume = traded_volume

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> TradedVolume
        """
           Arguments:
              java_object (ch.algotrader.entity.marketData.TradedVolumeVO): &nbsp;
           Returns:
              TradedVolume
        """
        start_time = Conversions.zoned_date_time_to_python_datetime(java_object.getStartTime())
        end_time = Conversions.zoned_date_time_to_python_datetime(java_object.getEndTime())
        _connector_descriptor = java_object.getConnectorDescriptor().getDescriptor()
        security_id = java_object.getSecurityId()
        traded_volume = java_object.getTradedVolume()
        return TradedVolume(start_time, end_time, _connector_descriptor, security_id, traded_volume)

class TradingStatus:
    """
        Attributes:
            status (str): &nbsp;
            security_id (int): &nbsp;
            date_time (datetime): &nbsp;
    """

    def __init__(self, status=None, security_id=None, connector_descriptor=None, date_time=None):
        # type: (str, int, str, datetime) -> None
        self.status = status
        self.security_id = security_id
        self.connector_descriptor = connector_descriptor
        self.date_time = date_time

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> TradingStatus
        """
           Arguments:
              java_object (ch.algotrader.vo.TradingStatusEventVO): &nbsp;
           Returns:
              TradingStatus
        """
        date_time = Conversions.zoned_date_time_to_python_datetime(java_object.getDateTime())
        _connector_descriptor = java_object.getConnectorDescriptor().getDescriptor()
        security_id = java_object.getSecurityId()
        status = java_object.getStatus().toString()
        return TradingStatus(status, security_id, _connector_descriptor, date_time)

class SecurityPosition:
    """Mirrors SecurityPositionVO Java class.

    Attributes:
        position (Decimal): &nbsp;
        market_price (Decimal): &nbsp;
        market_value (Decimal): &nbsp;
        security_id (int): &nbsp;
       """

    def __init__(self, position=None, market_price=None, market_value=None, security_id=None):
        # type: (Decimal, Decimal, Decimal, int) -> None
        self.position = position
        self.market_price = market_price
        self.market_value = market_value
        self.security_id = security_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> SecurityPosition
        """
           Arguments:
              vo (ch.algotrader.vo.SecurityPositionVO): &nbsp;
           Returns:
              SecurityPosition
        """
        vo_position = vo.getPosition()
        position = None
        if vo_position is not None:
            position = vo_position
        vo_market_price = vo.getMarketPrice()
        market_price = None
        if vo_market_price is not None:
            market_price = vo_market_price
        vo_market_value = vo.getMarketValue()
        market_value = None
        if vo_market_value is not None:
            market_value = vo_market_value
        vo_security_id = vo.getSecurityId()
        security_id = None
        if vo_security_id is not None:
            security_id = vo_security_id

        return SecurityPosition(position, market_price, market_value, security_id)


class Allocations:
    """Mirrors ch.algotrader.api.connector.account.domain.Allocations Java class.

    Attributes:
        name (str): &nbsp;
        type (Decimal): PERCENTAGES, RATIOS, SHARES;
       """
    def __init__(self, name=None, allocation_type=None):
        # type: (str, str) -> None
        self.name = name
        self.allocation_type = allocation_type
        self.allocations = dict({})

    @staticmethod
    def convert_to_java_object(ao, py4jgateway):
        # type: (Allocations, ClientServer) -> JavaObject

        alloc_enum = py4jgateway.jvm.ch.algotrader.api.connector.account.domain\
            .Allocations.Type.valueOf(ao.allocation_type)
        java_object = py4jgateway.jvm.ch.algotrader.api.connector.account.domain\
            .Allocations(ao.name, alloc_enum)

        keys = ao.allocations.keys()
        for key in keys:
            java_object.putAllocation(key, float(ao.allocations[key]))

        return java_object

    @staticmethod
    def convert_from_java_object(java_object):
        # type: (JavaObject) -> Allocations
        """
           Arguments:
              java_object (ch.algotrader.api.connector.account.domain.Allocations): &nbsp;
           Returns:
              Allocations
        """
        name = java_object.getName()
        allocation_type = java_object.getType().name()
        allocation_keys = java_object.getAllocations().keySet().toArray();
        allocations = Allocations(name, allocation_type)

        for key in allocation_keys:
            val = float(java_object.getAllocations().get(key))
            allocations.allocations[key] = val

        return allocations


class Transfer:
    """Mirrors TransferVO Java class.

       Attributes:
           id (int): &nbsp;
           ext_id (str): &nbsp;
           date_time (datetime): &nbsp;
           status (str): &nbsp;
           asset (str): &nbsp;
           source_id (str): &nbsp;
           destination_id (str): &nbsp;
           hash (str): &nbsp;
           amount (Decimal): &nbsp;
           net_amount (Decimal): &nbsp;
           network_fee (Decimal): &nbsp;
           service_fee (Decimal): &nbsp;
           fee_currency (str): &nbsp;
           account_id (int): &nbsp;
    """

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.TransferImpl"

    def __init__(self, id, ext_id, date_time, status, asset, source_id, destination_id, hash, amount, net_amount, network_fee, service_fee, fee_currency, account_id):
        # type: (int, str, datetime, str, str, int, int, str, Decimal, Decimal, Decimal, Decimal, str, int) -> None
        self.id = id
        self.ext_id = ext_id
        self.date_time = date_time
        self.status = status
        self.asset = asset
        self.source_id = source_id
        self.destination_id = destination_id
        self.hash = hash
        self.amount = amount
        self.net_amount = net_amount
        self.network_fee = network_fee
        self.service_fee = service_fee
        self.fee_currency = fee_currency
        self.account_id = account_id

    @staticmethod
    def convert_from_vo(transfer_vo):
        # type: (JavaObject) -> Transfer
        """
           Arguments:
               transfer_vo (ch.algotrader.entity.TransferVO): &nbsp;
           Returns:
               Transfer
        """
        return Transfer(
            id=transfer_vo.getId(),
            ext_id=transfer_vo.getExtId(),
            date_time=Conversions.zoned_date_time_to_python_datetime(transfer_vo.getDateTime()),
            status=transfer_vo.getStatus().toString(),
            asset=transfer_vo.getAsset(),
            source_id=transfer_vo.getSourceId(),
            destination_id=transfer_vo.getDestinationId(),
            hash=transfer_vo.getHash(),
            amount=transfer_vo.getAmount(),
            net_amount=transfer_vo.getNetAmount(),
            network_fee=transfer_vo.getNetworkFee(),
            service_fee=transfer_vo.getServiceFee(),
            fee_currency=transfer_vo.getFeeCurrency(),
            account_id=transfer_vo.getAccountId(),
        )


class TransferRequest:
    """Mirrors ch.algotrader.vo.TransferRequestVO Java class. Represents transfer request.

        Attributes:
           amount (Decimal): The requested transfer amount
           asset (str): Asset to be transferred
           source_sub_account_id (int): Source SubAccount ID
           destination_sub_account_id (int): Source SubAccount ID
           fee_level (str): LOW, MEDIUM, HIGH
    """

    def __init__(self, amount=None, asset=None, source_sub_account_id=None, destination_sub_account_id=None, fee_level=None):
        # type: (Decimal, str, int, int, str) -> None
        self.amount = amount
        self.asset = asset
        self.source_sub_account_id = source_sub_account_id
        self.destination_sub_account_id = destination_sub_account_id
        self.fee_level = fee_level

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.vo.TransferRequestVO
        """
        builder = py4jgateway.jvm.TransferRequestVO.builder()
        builder.setAmount(self.amount)
        builder.setAsset(self.asset)
        builder.setSourceSubAccountId(self.source_sub_account_id)
        builder.setDestinationSubAccountId(self.destination_sub_account_id)
        if self.fee_level is not None:
            builder.setFeeLevel(py4jgateway.jvm.TransferRequestVO.FeeLevel.valueOf(self.fee_level))
        vo = builder.build()
        return vo


class TransferCancelRequest:
    """Mirrors ch.algotrader.vo.TransferCancelRequestVO Java class. Represents transfer cancel request.

        Attributes:
           tx_id (str): Transaction ID
    """

    def __init__(self, tx_id=None):
        # type: (str) -> None
        self.tx_id = tx_id

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.vo.TransferCancelRequestVO
        """
        vo = py4jgateway.jvm.TransferCancelRequestVO(self.tx_id)
        return vo


class TransferResult:
    """Mirrors ch.algotrader.vo.TransferResultVO Java class. Represents transfer result.

        Attributes:
           tx_id (str): Transaction ID
    """

    def __init__(self, tx_id=None):
        # type: (str) -> None
        self.tx_id = tx_id

    @staticmethod
    def convert_from_vo(vo):
        # type: (JavaObject) -> TransferResult
        """
           Arguments:
              vo (ch.algotrader.vo.TransferResultVO): &nbsp;
           Returns:
              TransferResult
        """
        return TransferResult(tx_id=vo.getTxId())
