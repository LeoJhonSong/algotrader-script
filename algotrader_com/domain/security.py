from abc import abstractmethod
from datetime import datetime
from decimal import Decimal

from py4j.clientserver import ClientServer
from py4j.java_gateway import JavaObject

from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.order import PropertyHolder


class Security(PropertyHolder):
    """The base class of all Securities in the system.
    
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
    """    
    
    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int) -> None
        PropertyHolder.__init__(self, _id)
        self.symbol = symbol
        self.description = description
        self.isin = isin  # International Securities Identification Number
        self.bbgid = bbgid  # Bloomberg Identifier
        self.ric = ric  # Reuters Instrument Code
        self.conid = conid  # Interactive Brokers conid
        self.lmaxid = lmaxid  # LMAX id
        self.ttid = ttid  # TradingTechnologies id
        self.cnpid = cnpid  # The CoinAPI asset id
        self.xntid = xntid  # EXANTE id
        self.adapter_ticker = adapter_ticker
        self.quandl_database = quandl_database  # Quandl database code
        self.quandl_dataset = quandl_dataset  # Quandl dataset code
        self.cfi_code = cfi_code
        self.underlying_id = underlying_id
        self.security_family_id = security_family_id
        self.quote_currency = quote_currency  # The quote currency of the security
        self.contract_size = contract_size  # The contract size of the security (e.g. 100 for SPX Options).
        self.inverse_contract = inverse_contract  # True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
        self.min_qty = min_qty  # The minimum amount of base asset/currency
        self.max_qty = max_qty  # The maximum amount of base asset/currency
        self.qty_incr = qty_incr  # Minimum step size for quantity.
        self.min_price = min_price  # The minimum amount of transaction asset/currency.
        self.max_price = max_price  # The maximum amount of transaction asset/currency.
        self.price_incr = price_incr  # Step size for price.
        self.min_notional = min_notional  # Minimum order value ( qty * size ).
        self.tradeable = tradeable  # Represents a security for which an order can be directly sent to the market or via an OTC order
        self.synthetic = synthetic  # Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
        self.max_gap = max_gap  # The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
        self.exchange_id = exchange_id  # Exchange where securities are traded

    @staticmethod
    def get_java_class():
        # type: () -> str
        """
            Returns:
                str
        """
        return "ch.algotrader.entity.security.SecurityImpl"

    @staticmethod
    def convert_from_vo(security_vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Security
        """
           Arguments:
               security_vo (SecurityVO subtype): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Security subtype
        """
        if security_vo is None:
            return None
        if security_vo.getClass().getSimpleName() == "IndexVO":
            security = Index.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "StockVO":
            security = Stock.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "ForexVO":
            security = Forex.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "CombinationVO":
            security = Combination.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "BondVO":
            security = Bond.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "FutureVO":
            security = Future.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "GenericFutureVO":
            security = GenericFuture.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "OptionVO":
            security = Option.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "PerpetualSwapVO":
            security = PerpetualSwap.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "FundVO":
            security = Fund.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "CommodityVO":
            security = Commodity.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        elif security_vo.getClass().getSimpleName() == "IntrestRateVO":
            security = IntrestRate.convert_from_vo(security_vo, py4jgateway)  # type: ignore
        else:
            raise Exception("Unsupported order type " + security_vo.getClass().getSimpleName() + ".")
        return security

    @abstractmethod
    def convert_to_vo(self, _gateway):
        # type: (ClientServer) -> JavaObject
        """Converts a security to the corresponding AlgoTrader Java value object."""
        pass


class Index(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         asset_class (str): EQUITY, COMMODITY, VOLATILITY, FIXED_INCOME, FX
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, asset_class=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.asset_class = asset_class

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.IndexImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.IndexVO
        """
        vo_builder = py4jgateway.jvm.IndexVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.asset_class is not None:
            asset_class = py4jgateway.jvm.AssetClass.valueOf(self.asset_class)
            vo_builder.setAssetClass(asset_class)

        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Index
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.IndexVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Index
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        asset_class = None
        if vo.getAssetClass() is not None:
            asset_class = vo.getAssetClass().toString()
        index = Index(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                      xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                      security_family_id, quote_currency, contract_size, inverse_contract, min_qty,
                      max_qty, qty_incr,
                      min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap,
                      exchange_id, asset_class)
        return index


class Stock(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
    """
    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, gics=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.gics = gics

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.StockImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.StockVO
        """
        vo_builder = py4jgateway.jvm.StockVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        vo_builder.setGics(self.gics)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Stock
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.StockVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Stock
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        gics = vo.getGics()
        security = Stock(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                         xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                         security_family_id, quote_currency, contract_size, inverse_contract,
                         min_qty, max_qty, qty_incr,
                         min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap,
                         exchange_id, gics)
        return security


class Forex(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         base_currency (str): The base currency of this Forex Contract (e.g. EUR for the EUR.USD Forex)
         """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, base_currency=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.base_currency = base_currency

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.ForexImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.ForexVO
        """
        vo_builder = py4jgateway.jvm.ForexVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        vo_builder.setBaseCurrency(self.base_currency)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Forex
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.ForexVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Forex
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        base_currency = vo.getBaseCurrency()
        security = Forex(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                         xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                         security_family_id, quote_currency, contract_size,
                         inverse_contract, min_qty, max_qty, qty_incr,
                         min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap,
                         exchange_id, base_currency)
        return security


class PerpetualSwap(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
    """
    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.PerpetualSwapImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.PerpetualSwapVO
        """
        vo_builder = py4jgateway.jvm.PerpetualSwapVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> PerpetualSwap
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.PerpetualSwapVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               PerpetualSwap
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        security = PerpetualSwap(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                                 xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                                 underlying_id, security_family_id, quote_currency, contract_size,
                                 inverse_contract, min_qty,
                                 max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                                 synthetic, max_gap, exchange_id)
        return security


class Commodity(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         commodity_type (str): ENERGY, INDUSTRIAL_METALS, PRECIOUS_METALS, AGRICULTURE, LIVESTOCK
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, commodity_type=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.commodity_type = commodity_type  # ENERGY, INDUSTRIAL_METALS, PRECIOUS_METALS, AGRICULTURE, LIVESTOCK

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.CommodityImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.CommodityVO
        """
        vo_builder = py4jgateway.jvm.CommodityVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.commodity_type is not None:
            commodity_type = py4jgateway.jvm.CommodityType.valueOf(self.commodity_type)
            vo_builder.setCommodityType(commodity_type)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Commodity
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.CommodityVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Commodity
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        commodity_type = None
        if vo.getCommodityType() is not None:
            commodity_type = vo.getCommodityType().toString()
        security = Commodity(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                             xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                             underlying_id, security_family_id, quote_currency, contract_size,
                             inverse_contract, min_qty,
                             max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                             synthetic, max_gap, exchange_id, commodity_type)
        return security


class Bond(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         maturity (datetime): The Maturity Date
         issue_date (datetime): The Issue Date
         coupon (Decimal): The coupon of the Bond specified as a double
         coupon_frequency (): The frequency of the coupon: ANNUAL, SEMI_ANNUAL, QUARTERLY
         rating_sp (str): Rating S&P
         rating_moodys (str): Rating Moody's
         rting_fitch (str): Rating Fitch
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, maturity=None, issue_date=None, coupon=None, coupon_frequency=None,
                 rating_sp=None, rating_moodys=None, rating_fitch=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, datetime, datetime, Decimal, str, str, str, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.maturity = maturity  # The Maturity Date
        self.issue_date = issue_date
        self.coupon = coupon  # The coupon of the Bond specified as a double
        self.coupon_frequency = coupon_frequency
        self.rating_sp = rating_sp
        self.rating_moodys = rating_moodys
        self.rating_fitch = rating_fitch

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.BondImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.BondVO
        """
        vo_builder = py4jgateway.jvm.BondVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.maturity is not None:
            maturity = Conversions.python_datetime_to_localdate(self.maturity, py4jgateway)
            vo_builder.setMaturity(maturity)
        if self.issue_date is not None:
            issue_date = Conversions.python_datetime_to_localdate(self.issue_date, py4jgateway)
            vo_builder.setIssueDate(issue_date)
        vo_builder.setCoupon(self.coupon)
        if self.coupon_frequency is not None:
            coupon_frequency = py4jgateway.jvm.CouponFrequency.valueOf(self.coupon_frequency)
            vo_builder.setCouponFrequency(coupon_frequency)
        vo_builder.setRatingSP(self.rating_sp)
        vo_builder.setRatingMoodys(self.rating_moodys)
        vo_builder.setRatingFitch(self.rating_fitch)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Bond
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.BondVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Bond
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        maturity = None
        if vo.getMaturity() is not None:
            maturity = Conversions.local_date_to_python_datetime(vo.getMaturity(), py4jgateway)
        if vo.getIssueDate() is not None:
            issue_date = Conversions.local_date_to_python_datetime(vo.getIssueDate(), py4jgateway)
        coupon = vo.getCoupon()
        if vo.getCouponFrequency() is not None:
            coupon_frequency = vo.getCouponFrequency().toString()
        rating_sp = vo.getRatingSP()
        rating_moodys = vo.getRatingMoodys()
        rating_fitch = vo.getRatingFitch()
        security = Bond(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                        xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                        underlying_id, security_family_id, quote_currency, contract_size,
                        inverse_contract, min_qty,
                        max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                        synthetic, max_gap, exchange_id, maturity, issue_date, coupon, coupon_frequency,
                        rating_sp, rating_moodys, rating_fitch)
        return security


class Fund(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.FundImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.FundVO
        """
        vo_builder = py4jgateway.jvm.FundVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Fund
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.FundVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Fund
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        security = Fund(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                        xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                        underlying_id, security_family_id, quote_currency, contract_size,
                        inverse_contract, min_qty,
                        max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                        synthetic, max_gap, exchange_id)
        return security


class GenericFuture(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         duration (str): The Duration of this GenericFuture. A Duration of MONTH_1 means that this GenericFuture is equal to the physical Front Month Future. After the Expiration Date of the physical Future, the GenericFuture with Duration 1 (that until now represented the expiring Future) now switches to represent the Future that is next to expire. MSEC_1, SEC_1, SEC_5, SEC_10, SEC_15, SEC_30, MIN_1, MIN_2, MIN_3, MIN_5, MIN_10, MIN_15, MIN_20, MIN_30, HOUR_1, HOUR_2, HOUR_3, HOUR_4, HOUR_8, DAY_1, DAY_2, WEEK_1, WEEK_2, MONTH_1, MONTH_2, MONTH_3, MONTH_4, MONTH_5, MONTH_6, MONTH_7, MONTH_8, MONTH_9, MONTH_10, MONTH_11, MONTH_18, YEAR_1, YEAR_2
         asset_class (str): EQUITY, COMMODITY, VOLATILITY, FIXED_INCOME, FX
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, duration=None, asset_class=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.duration = duration  # The Duration of this GenericFuture. A Duration of MONTH_1 means that this GenericFuture is equal to the physical Front Month Future. After the Expiration Date of the physical Future, the GenericFuture with Duration 1 (that until now represented the expiring Future) now switches to represent the Future that is next to expire.
        self.asset_class = asset_class  # EQUITY, COMMODITY, VOLATILITY, FIXED_INCOME, FX

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.GenericFutureImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.GenericFutureVO
        """
        vo_builder = py4jgateway.jvm.GenericFutureVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.duration is not None:
            duration = py4jgateway.jvm.Duration.valueOf(self.duration)
            vo_builder.setDuration(duration)
        if self.asset_class is not None:
            asset_class = py4jgateway.jvm.AssetClass.valueOf(self.asset_class)
            vo_builder.setAssetClass(asset_class)

        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> GenericFuture
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.GenericFutureVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               GenericFuture
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        duration = None
        if vo.getDuration() is not None:
            duration = vo.getDuration().toString()
        asset_class = None
        if vo.getDuration() is not None:
            asset_class = vo.getAssetClass().toString()
        security = GenericFuture(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                                 xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                                 underlying_id, security_family_id, quote_currency, contract_size,
                                 inverse_contract, min_qty,
                                 max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                                 synthetic, max_gap, exchange_id, duration, asset_class)
        return security


class IntrestRate(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         duration (str): MSEC_1, SEC_1, SEC_5, SEC_10, SEC_15, SEC_30, MIN_1, MIN_2, MIN_3, MIN_5, MIN_10, MIN_15, MIN_20, MIN_30, HOUR_1, HOUR_2, HOUR_3, HOUR_4, HOUR_8, DAY_1, DAY_2, WEEK_1, WEEK_2, MONTH_1, MONTH_2, MONTH_3, MONTH_4, MONTH_5, MONTH_6, MONTH_7, MONTH_8, MONTH_9, MONTH_10, MONTH_11, MONTH_18, YEAR_1, YEAR_2
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, duration=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.duration = duration

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.IntrestRateImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.IntrestRateVO
        """
        vo_builder = py4jgateway.jvm.IntrestRateVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.duration is not None:
            duration = py4jgateway.jvm.Duration.valueOf(self.duration)
            vo_builder.setDuration(duration)

        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> IntrestRate
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.IntrestRateVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               IntrestRate
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        duration = None
        if vo.getDuration() is not None:
            duration = vo.getDuration().toString()
        security = IntrestRate(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                               xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                               underlying_id, security_family_id, quote_currency, contract_size,
                               inverse_contract, min_qty,
                               max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                               synthetic, max_gap, exchange_id, duration)
        return security


class Option(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         expiration (datetime): The Expiration Date
         strike (Decimal): The strike price
         option_type (str): CALL, PUT
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, expiration=None, strike=None, option_type=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, datetime, Decimal, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.expiration = expiration  # The Expiration Date
        self.strike = strike  # The strike price.
        self.option_type = option_type  # PUT, CALL

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.OptionImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.OptionVO
        """
        vo_builder = py4jgateway.jvm.OptionVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.expiration is not None:
            expiration = Conversions.python_datetime_to_localdate(self.expiration, py4jgateway)
            vo_builder.setExpiration(expiration)
        vo_builder.setStrike(self.strike)
        if self.option_type is not None:
            option_type = py4jgateway.jvm.OptionType.valueOf(self.option_type)
            vo_builder.setOptionType(option_type)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Option
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.OptionVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Option
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        expiration = None
        if vo.getExpiration() is not None:
            expiration = Conversions.local_date_to_python_datetime(vo.getExpiration(), py4jgateway)
        strike = vo.getStrike()
        option_type = None
        if vo.getOptionType() is not None:
            option_type = vo.getOptionType().toString()

        security = Option(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                          underlying_id, security_family_id, quote_currency, contract_size,
                          inverse_contract, min_qty,
                          max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                          synthetic, max_gap, exchange_id, expiration, strike, option_type)
        return security


class Combination(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         uuid (str): auto generated unique identifier. Combinations do not have any other natural identifiers.
         combination_type (str): The type of the Combination. VERTICAL_SPREAD, COVERED_CALL, RATIO_SPREAD, STRADDLE, STRANGLE, BUTTERFLY, CALENDAR_SPREAD, IRON_CONDOR
    """
    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, uuid=None, combination_type=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, str, str) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.uuid = uuid  # auto generated unique identifier. Combinations do not have any other natural identifiers.
        self.combination_type = combination_type  # The type of the Combination (e.g. Butterfly, Condor, RatioSpread, etc.)

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.CombinationImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.CombinationVO
        """
        vo_builder = py4jgateway.jvm.CombinationVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        vo_builder.setUuid(self.uuid)
        if self.combination_type is not None:
            combination_type = py4jgateway.jvm.CombinationType.valueOf(self.combination_type)
            vo_builder.setCombinationType(combination_type)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Combination
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.CombinationVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Combination
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        uuid = vo.getUuid()
        combination_type = None
        if vo.getCombinationType() is not None:
            combination_type = vo.getCombinationType().toString()
        security = Combination(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                               xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                               underlying_id, security_family_id, quote_currency, contract_size,
                               inverse_contract, min_qty,
                               max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                               synthetic, max_gap, exchange_id, uuid, combination_type)
        return security


class Future(Security):
    """
     Attributes:
         _id (int): &nbsp;
         symbol (str): &nbsp;
         description (str): &nbsp;
         isin (str): International Securities Identification Number
         bbgid (str): Bloomberg Identifier
         ric (str): Reuters Instrument Code
         conid (str): Interactive Brokers conid
         lmaxid (str): LMAX id
         ttid (str): TradingTechnologies id
         cnpid (str): The CoinAPI asset id
         xntid (str): EXANTE id
         adapter_ticker (str): &nbsp;
         quandl_database (str): Quandl database code
         quandl_dataset (str): Quandl dataset code
         cfi_code (str): CFI code
         underlying_id (int): &nbsp;
         security_family_id (int): &nbsp;
         quote_currency (str): The quote currency of the security
         contract_size (float): The contract size of the security (e.g. 100 for SPX Options).
         inverse_contract (bool): True if security is a derivative with inverse contract PnL calculation, e.g. XBTUSD in BitMex.
         min_qty (Decimal): The minimum amount of base asset/currency
         max_qty (Decimal): The maximum amount of base asset/currency
         qty_incr (Decimal): Minimum step size for quantity.
         min_price (Decimal): The minimum amount of transaction asset/currency.
         max_price (Decimal): The maximum amount of transaction asset/currency.
         price_incr (Decimal): Step size for price.
         min_notional (Decimal): Minimum order value ( qty * size ).
         tradeable (bool): Represents a security for which an order can be directly sent to the market or via an OTC order
         synthetic (bool): Represents virtual securities that are only known to the framework. Market data needs to be calculated manually (e.g. a Combination)
         max_gap (int): The Maximum Market Data Gap (in minutes) that is expected in normal Market Conditions. An exception is thrown if no market data arrives for a period longer than this value which might indicate a problem with the external Market Data Provider.
         exchange_id (int): Exchange where securities are traded
         expiration (datetime): The Last Trading / Expiration Date
         month_year (str): The month and year in the format "yyyymm". Note: month can be different that the month part of the expiration. E.g. a Jan 2016 contract might have an expiration date of Dec. 16th 2015.
         first_notice (datetime): The first notice date
    """

    def __init__(self, _id=None, symbol=None, description=None, isin=None, bbgid=None, ric=None, conid=None,
                 lmaxid=None, ttid=None, cnpid=None,
                 xntid=None, adapter_ticker=None, quandl_database=None, quandl_dataset=None, cfi_code=None,
                 underlying_id=None,
                 security_family_id=None, quote_currency=None, contract_size=None, inverse_contract=False,
                 min_qty=None, max_qty=None,
                 qty_incr=None, min_price=None,
                 max_price=None, price_incr=None, min_notional=None, tradeable=None, synthetic=None, max_gap=None,
                 exchange_id=None, expiration=None, month_year=None, first_notice=None):
        # type: (int, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, str, float, bool, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, bool, bool, int, int, datetime, str, datetime) -> None
        Security.__init__(self, _id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code, underlying_id,
                          security_family_id, quote_currency, contract_size, inverse_contract, min_qty, max_qty,
                          qty_incr,
                          min_price, max_price, price_incr, min_notional, tradeable, synthetic, max_gap, exchange_id)
        self.expiration = expiration  # The Last Trading / Expiration Date
        self.month_year = month_year  # The month and year in the format "yyyymm". Note: month can be different that the month part of the expiration. E.g. a Jan 2016 contract might have an expiration date of Dec. 16th 2015.
        self.first_notice = first_notice  # The first notice date

    @staticmethod
    def get_java_class():
        # type: () -> str
        return "ch.algotrader.entity.security.FutureImpl"

    def convert_to_vo(self, py4jgateway):
        # type: (ClientServer) -> JavaObject
        """Converts the security to Java value object

           Arguments:
               py4jgateway (ClientServer): &nbsp;
           Returns:
               ch.algotrader.entity.security.FutureVO
        """
        vo_builder = py4jgateway.jvm.FutureVOBuilder.create()  # java class
        if self.id is not None:
            vo_builder.setId(self.id)
        vo_builder.setSymbol(self.symbol)
        vo_builder.setDescription(self.description)
        vo_builder.setIsin(self.isin)
        vo_builder.setBbgid(self.bbgid)
        vo_builder.setRic(self.ric)
        vo_builder.setConid(self.conid)
        vo_builder.setLmaxid(self.lmaxid)
        vo_builder.setTtid(self.ttid)
        vo_builder.setCnpid(self.cnpid)
        vo_builder.setXntid(self.xntid)
        vo_builder.setAdapterTicker(self.adapter_ticker)
        vo_builder.setQuandlDatabase(self.quandl_database)
        vo_builder.setQuandlDataset(self.quandl_dataset)
        vo_builder.setCfiCode(self.cfi_code)
        if self.underlying_id is not None:
            vo_builder.setUnderlyingId(self.underlying_id)
        if self.security_family_id is not None:
            vo_builder.setSecurityFamilyId(self.security_family_id)
        vo_builder.setQuoteCurrency(self.quote_currency)
        if self.contract_size is not None:
            vo_builder.setContractSize(self.contract_size)
        vo_builder.setInverseContract(self.inverse_contract)
        vo_builder.setMinQty(self.min_qty)
        vo_builder.setMaxQty(self.max_qty)
        vo_builder.setQtyIncr(self.qty_incr)
        vo_builder.setMinPrice(self.min_price)
        vo_builder.setMaxPrice(self.max_price)
        vo_builder.setPriceIncr(self.price_incr)
        vo_builder.setMinNotional(self.min_notional)
        if self.tradeable is not None:
            vo_builder.setTradeable(self.tradeable)
        if self.synthetic is not None:
            vo_builder.setSynthetic(self.synthetic)
        vo_builder.setMaxGap(self.max_gap)
        if self.exchange_id is not None:
            vo_builder.setExchangeId(self.exchange_id)
        if self.expiration is not None:
            expiration = Conversions.python_datetime_to_localdate(self.expiration, py4jgateway)
            vo_builder.setExpiration(expiration)
        vo_builder.setMonthYear(self.month_year)
        if self.first_notice is not None:
            first_notice = Conversions.python_datetime_to_localdate(self.first_notice, py4jgateway)
            vo_builder.setFirstNotice(first_notice)
        vo = vo_builder.build()
        return vo

    @staticmethod
    def convert_from_vo(vo, py4jgateway):
        # type: (JavaObject, ClientServer) -> Future
        """Converts Java value object to the Python object.

           Arguments:
               vo (ch.algotrader.entity.security.FutureVO): &nbsp;
               py4jgateway (ClientServer): &nbsp;
           Returns:
               Future
        """
        _id = vo.getId()
        symbol = vo.getSymbol()
        description = vo.getDescription()
        isin = vo.getIsin()
        bbgid = vo.getBbgid()
        ric = vo.getRic()
        conid = vo.getConid()
        lmaxid = vo.getLmaxid()
        ttid = vo.getTtid()
        cnpid = vo.getCnpid()
        xntid = vo.getXntid()
        adapter_ticker = vo.getAdapterTicker()
        quandl_database = vo.getQuandlDatabase()
        quandl_dataset = vo.getQuandlDataset()
        cfi_code = vo.getCfiCode()
        underlying_id = vo.getUnderlyingId()
        security_family_id = vo.getSecurityFamilyId()
        quote_currency = vo.getQuoteCurrency()
        contract_size = vo.getContractSize()
        inverse_contract = vo.isInverseContract()
        min_qty = vo.getMinQty()
        max_qty = vo.getMaxQty()
        qty_incr = vo.getQtyIncr()
        min_price = vo.getMinPrice()
        max_price = vo.getMaxPrice()
        price_incr = vo.getPriceIncr()
        min_notional = vo.getMinNotional()
        tradeable = vo.isTradeable()
        synthetic = vo.isSynthetic()
        max_gap = vo.getMaxGap()
        exchange_id = vo.getExchangeId()
        expiration = None
        if vo.getExpiration() is not None:
            expiration = Conversions.local_date_to_python_datetime(vo.getExpiration(), py4jgateway)
        month_year = vo.getMonthYear()
        first_notice = None
        if vo.getFirstNotice() is not None:
            first_notice = Conversions.local_date_to_python_datetime(vo.getFirstNotice(), py4jgateway)
        security = Future(_id, symbol, description, isin, bbgid, ric, conid, lmaxid, ttid, cnpid,
                          xntid, adapter_ticker, quandl_database, quandl_dataset, cfi_code,
                          underlying_id, security_family_id, quote_currency, contract_size,
                          inverse_contract, min_qty,
                          max_qty, qty_incr, min_price, max_price, price_incr, min_notional, tradeable,
                          synthetic, max_gap, exchange_id, expiration, month_year, first_notice)
        return security
