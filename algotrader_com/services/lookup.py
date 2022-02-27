from algotrader_com.domain.conversions import Conversions
from algotrader_com.domain.entity import SecurityFamily, Exchange, Component, Subscription, Portfolio, Position, \
    Transaction, Account, CashBalance
from algotrader_com.domain.order import Order
from algotrader_com.domain.security import Security, Stock, Option, Future, Combination, IntrestRate
from datetime import datetime
from py4j.clientserver import ClientServer
from py4j.java_collections import ListConverter
from typing import List, Optional, Any, Dict, Tuple, Type


class LookupService:
    """Delegates to pythonLookupService object in PythonPortfolioService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonLookupService()

    def get_security(self, _id):
        # type: (int) -> Security
        """Gets security by its id.

           Arguments:
               _id (int): &nbsp;
           Returns:
               algotrader_com.domain.security.Security
        """
        vo = self._service.getSecurity(_id)
        security = Security.convert_from_vo(vo, self._gateway)
        return security

    def get_securities_by_isin(self, isin):
        # type: (str) -> List[Security]
        """
           Arguments:
               isin (str): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.getSecuritiesByIsin(isin)
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_security_by_isin_exchange_and_currency(self, isin, exchange_id, quote_currency):
        # type: (str, int, str) -> Security
        """
           Arguments:
               isin (str): &nbsp;
               exchange_id (int): &nbsp;
               quote_currency (str): &nbsp;
           Returns:
               algotrader_com.domain.security.Security
        """
        vo = self._service.getSecurityByIsinExchangeAndCurrency(isin, exchange_id, quote_currency)
        security = Security.convert_from_vo(vo, self._gateway)
        return security

    def get_securities_by_symbol(self, symbol):
        # type: (str) -> List[Security]
        """
           Arguments:
               symbol (str): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.getSecuritiesBySymbol(symbol)
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_security_by_bbgid(self, bbgid):
        # type: (str) -> Security
        """
           Arguments:
               bbgid (str): &nbsp;
           Returns:
               algotrader_com.domain.security.Security
        """
        vo = self._service.getSecurityByBbgid(bbgid)
        security = Security.convert_from_vo(vo, self._gateway)
        return security

    def get_security_by_ric(self, ric):
        # type: (str) -> Security
        """
           Arguments:
               ric (str): &nbsp;
           Returns:
               algotrader_com.domain.security.Security
        """
        vo = self._service.getSecurityByRic(ric)
        security = Security.convert_from_vo(vo, self._gateway)
        return security

    def get_securities_by_conid(self, conid):
        # type: (str) -> List[Security]
        """Gets all securities with particular conid.

           Arguments:
               conid (str): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.getSecuritiesByConid(conid)
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_security_by_conid_and_exchange(self, conid, exchange_id):
        # type: (str, int) -> Security
        """
           Arguments:
               conid (str): &nbsp;
               exchange_id (int): &nbsp;
           Returns:
               algotrader_com.domain.security.Security
        """
        vo = self._service.getSecurityByConidAndExchange(conid, exchange_id)
        security = Security.convert_from_vo(vo, self._gateway)
        return security

    def get_securities_by_ids(self, ids_list):
        # type: (List[int]) -> List[Security]
        """
           Arguments:
               ids_list (List of int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Security
        """
        # noinspection PyProtectedMember
        ids_java = ListConverter().convert(ids_list, self._gateway._gateway_client)
        vos = self._service.getSecuritiesByIds(ids_java)
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_securities_by_security_family(self, security_family_id):
        # type: (int) -> List[Security]
        """
           Arguments:
               security_family_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.getSecuritiesBySecurityFamily(security_family_id)
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_all_securities(self):
        # type: () -> List[Security]
        """
           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.getAllSecurities()
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_all_security_families(self):
        # type: () -> List[SecurityFamily]
        """
           Returns:
               List of algotrader_com.domain.entity.SecurityFamily
        """
        vos = self._service.getAllSecurityFamilies()
        security_families = []
        for vo in vos:
            security_family = SecurityFamily.convert_from_vo(vo)
            security_families.append(security_family)
        return security_families

    def get_all_security_families_of_type(self, security_family_type):
        # type: (str) -> List[SecurityFamily]
        """
           Arguments:
               security_family_type (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.SecurityFamily
        """
        security_family_type_java = self._gateway.jvm.SecurityFamilyType.valueOf(security_family_type)
        vos = self._service.getAllSecurityFamilies(security_family_type_java)
        security_families = []
        for vo in vos:
            security_family = SecurityFamily.convert_from_vo(vo)
            security_families.append(security_family)
        return security_families

    def get_security_family_by_security(self, security_id):
        # type: (int) -> SecurityFamily
        """
           Arguments:
               security_id (int): &nbsp;
           Returns:
               algotrader_com.domain.entity.SecurityFamily
        """
        vo = self._service.getSecurityFamilyBySecurity(security_id)
        security_family = SecurityFamily.convert_from_vo(vo)
        return security_family

    def get_exchange_by_security(self, security_id):
        # type: (int) -> Exchange
        """
           Arguments:
               security_id (int): &nbsp;
           Returns:
               algotrader_com.domain.entity.Exchange
        """
        vo = self._service.getExchangeBySecurity(security_id)
        exchange = Exchange.convert_from_vo(vo)
        return exchange

    def get_security_reference_target_by_owner_and_name(self, security_id, name):
        # type: (int, str) -> Security
        """Returns a security that is referenced by another security and a reference name.

           Arguments:
               security_id (int): &nbsp;
               name (str): &nbsp;
           Returns:
               algotrader_com.domain.security.Security
        """
        vo = self._service \
            .getSecurityReferenceTargetByOwnerAndName(security_id, name)
        security = Security.convert_from_vo(vo, self._gateway)
        return security

    def get_subscribed_securities_for_auto_activate_strategies(self):
        # type: () -> List[Security]
        """Gets all securities that are subscribed by at least one strategy which is marked as autoActive.

           Returns:
               List of algotrader_com.domain.security.Security
        """
        return self.get_subscribed_securities_for_auto_activate_portfolios()

    def get_subscribed_securities_for_auto_activate_portfolios(self):
        # type: () -> List[Security]
        """Gets all securities that are subscribed by at least one portfolio which is marked as autoActive.

           Returns:
               List of algotrader_com.domain.security.Security
        """
        vos = self._service.getSubscribedSecuritiesForAutoActivatePortfolios()
        securities = []
        for vo in vos:
            security = Security.convert_from_vo(vo, self._gateway)
            securities.append(security)
        return securities

    def get_stocks_by_sector(self, code):
        # type: (str) -> List[Stock]
        """
           Returns:
               List of algotrader_com.domain.security.Stock
        """
        vos = self._service.getStocksBySector(code)
        stocks = []
        for vo in vos:
            stock = Stock.convert_from_vo(vo, self._gateway)
            stocks.append(stock)
        return stocks

    def get_stocks_by_industry_group(self, code):
        # type: (str) -> List[Stock]
        """
           Arguments:
               code (str): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Stock
        """
        vos = self._service.getStocksByIndustryGroup(code)
        stocks = []
        for vo in vos:
            stock = Stock.convert_from_vo(vo, self._gateway)
            stocks.append(stock)
        return stocks

    def get_stocks_by_industry(self, code):
        # type: (str) -> List[Stock]
        """
           Arguments:
               code (str): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Stock
        """
        vos = self._service.getStocksByIndustry(code)
        stocks = []
        for vo in vos:
            stock = Stock.convert_from_vo(vo, self._gateway)
            stocks.append(stock)
        return stocks

    def get_stocks_by_sub_industry(self, code):
        # type: (str) -> List[Stock]
        """
           Arguments:
               code (str): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Stock
        """
        vos = self._service.getStocksBySubIndustry(code)
        stocks = []
        for vo in vos:
            stock = Stock.convert_from_vo(vo, self._gateway)
            stocks.append(stock)
        return stocks

    def get_subscribed_options(self):
        # type: () -> List[Option]
        """Gets all options that are subscribed by at least one portfolio.

           Returns:
               List of algotrader_com.domain.security.Option
        """
        vos = self._service.getSubscribedOptions()
        options = []
        for vo in vos:
            option = Option.convert_from_vo(vo, self._gateway)
            options.append(option)
        return options

    def get_subscribed_futures(self):
        # type: () -> List[Future]
        """Gets all futures that are subscribed by at least one portfolio.

           Returns:
               List of algotrader_com.domain.security.Future
        """
        vos = self._service.getSubscribedFutures()
        futures = []
        for vo in vos:
            future = Future.convert_from_vo(vo, self._gateway)
            futures.append(future)
        return futures

    def get_subscribed_combinations_by_strategy(self, strategy_name):
        # type: (str) -> List[Combination]
        """Gets combinations that are subscribed by the specified strategy.

           Returns:
               List of algotrader_com.domain.security.Combination
        """
        return self.get_subscribed_combinations_by_portfolio(strategy_name)

    def get_subscribed_combinations_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Combination]
        """Gets combinations that are subscribed by the specified portfolio.

           Returns:
               List of algotrader_com.domain.security.Combination
        """
        vos = self._service.getSubscribedCombinationsByPortfolio(portfolio_name)
        combinations = []
        for vo in vos:
            combination = Combination.convert_from_vo(vo, self._gateway)
            combinations.append(combination)
        return combinations

    def get_subscribed_combinations_by_strategy_and_underlying(self, strategy_name, underlying_id):
        # type: (str, int) -> List[Combination]
        """Gets combinations that are subscribed by the specified strategy and have an underlying
           corresponding to underlying_id

           Arguments:
               strategy_name (str): &nbsp;
               underlying_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Combination
        """
        return self.get_subscribed_combinations_by_portfolio_and_underlying(strategy_name, underlying_id)

    def get_subscribed_combinations_by_portfolio_and_underlying(self, portfolio_name, underlying_id):
        # type: (str, int) -> List[Combination]
        """Gets combinations that are subscribed by the specified portfolio and have an underlying
           corresponding to underlying_id

           Arguments:
               portfolio_name (str): &nbsp;
               underlying_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Combination
        """
        vos = self._service.getSubscribedCombinationsByPortfolioAndUnderlying(
            portfolio_name, underlying_id)
        combinations = []
        for vo in vos:
            combination = Combination.convert_from_vo(vo, self._gateway)
            combinations.append(combination)
        return combinations

    def get_subscribed_combinations_by_strategy_and_component(self, strategy_name, security_id):
        # type: (str, int) -> List[Combination]
        """Gets combinations that are subscribed by the specified strategy and have a component
            with the specified security_id

           Arguments:
               strategy_name (str): &nbsp;
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Combination
         """
        return self.get_subscribed_combinations_by_portfolio_and_component(strategy_name, security_id)

    def get_subscribed_combinations_by_portfolio_and_component(self, portfolio_name, security_id):
        # type: (str, int) -> List[Combination]
        """Gets combinations that are subscribed by the specified portfolio and have a component
            with the specified security_id

           Arguments:
               portfolio_name (str): &nbsp;
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.security.Combination
         """
        vos = self._service.getSubscribedCombinationsByPortfolioAndComponent(
            portfolio_name, security_id)
        combinations = []
        for vo in vos:
            combination = Combination.convert_from_vo(vo, self._gateway)
            combinations.append(combination)
        return combinations

    def get_subscribed_components_by_strategy(self, strategy_name):
        # type: (str) -> List[Component]
        """Gets all components where the combination is subscribed by the defined strategy.
           In addition the Security and Combination are initialized.

           Arguments:
               strategy_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Component
        """
        return self.get_subscribed_components_by_portfolio(strategy_name)

    def get_subscribed_components_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Component]
        """Gets all components where the combination is subscribed by the defined portfolio.
           In addition the Security and Combination are initialized.

           Arguments:
               portfolio_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Component
        """
        vos = self._service.getSubscribedComponentsByPortfolio(portfolio_name)
        components = []
        for vo in vos:
            component = Component.convert_from_vo(vo)
            components.append(component)
        return components

    def get_subscribed_components_by_security(self, security_id):
        # type: (int) -> List[Component]
        """Gets all components where the combination is subscribed by at least one portfolio
           and where the security is of the specified  security_id.
           In addition the Security and Combination are initialized.

           Arguments:
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Component
        """
        vos = self._service.getSubscribedComponentsBySecurity(security_id)
        components = []
        for vo in vos:
            component = Component.convert_from_vo(vo)
            components.append(component)
        return components

    def get_subscribed_components_by_strategy_and_security(self, strategy_name, security_id):
        # type: (str, int) -> List[Component]
        """Gets all components where the combination is subscribed by the defined strategy
           and where the security is of the specified security_id.
           In addition the Security and Combination are initialized.

           Arguments:
               strategy_name (str): &nbsp;
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Component
          """
        return self.get_subscribed_components_by_portfolio_and_security(strategy_name, security_id)

    def get_subscribed_components_by_portfolio_and_security(self, portfolio_name, security_id):
        # type: (str, int) -> List[Component]
        """Gets all components where the combination is subscribed by the defined portfolio
           and where the security is of the specified security_id.
           In addition the Security and Combination are initialized.

           Arguments:
               portfolio_name (str): &nbsp;
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Component
          """
        vos = self._service.getSubscribedComponentsByPortfolioAndSecurity(
            portfolio_name, security_id)
        components = []
        for vo in vos:
            component = Component.convert_from_vo(vo)
            components.append(component)
        return components

    def get_market_data_subscription_by_strategy_and_security(self, strategy_name, security_id):
        # type: (str, int) -> Subscription
        """
           Arguments:
               strategy_name (str): &nbsp;
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
        """
        return self.get_market_data_subscription_by_portfolio_and_security(strategy_name, security_id)

    def get_market_data_subscription_by_portfolio_and_security(self, portfolio_name, security_id):
        # type: (str, int) -> Subscription
        """
           Arguments:
               portfolio_name (str): &nbsp;
               security_id (int): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
        """
        vo = self._service.getMarketDataSubscriptionByPortfolioAndSecurity(
            portfolio_name, security_id)
        subscription = Subscription.convert_from_vo(vo)
        return subscription

    def get_market_data_subscriptions_by_strategy(self, strategy_name):
        # type: (str) -> List[Subscription]
        """Gets all subscriptions by the defined strategy_name.
           If corresponding securities are combinations, all components will be initialized as well.
           In addition, all properties are initialized

           Arguments:
               strategy_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
          """
        return self.get_market_data_subscriptions_by_portfolio(strategy_name)

    def get_market_data_subscriptions_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Subscription]
        """Gets all subscriptions by the defined portfolio_name.
           If corresponding securities are combinations, all components will be initialized as well.
           In addition, all properties are initialized

           Arguments:
               portfolio_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
          """
        vos = self._service.getMarketDataSubscriptionsByPortfolio(portfolio_name)
        components = []
        for vo in vos:
            component = Subscription.convert_from_vo(vo)
            components.append(component)
        return components

    def get_non_position_market_data_subscriptions(self, portfolio_name):
        # type: (str) -> List[Subscription]
        """Gets subscriptions for the specified portfolio that do not have any open positions}

           Arguments:
               portfolio_name (str): &nbsp;
           Returns:
               List of algotrader_com.domain.entity.Subscription
        """
        vos = self._service.getNonPositionMarketDataSubscriptions(portfolio_name)
        components = []
        for vo in vos:
            component = Subscription.convert_from_vo(vo)
            components.append(component)
        return components

    def get_all_strategies(self):
        # type: () -> List[Strategy]
        """
           Returns:
               List of algotrader_com.domain.entity.Strategy
        """
        return self.get_all_portfolios()

    def get_all_portfolios(self):
        # type: () -> List[Portfolio]
        """
           Returns:
               List of algotrader_com.domain.entity.Portfolio
        """
        vos = self._service.getAllPortfolios()
        portfolios = []
        for vo in vos:
            portfolio = Portfolio.convert_from_vo(vo)
            portfolios.append(portfolio)
        return portfolios

    def get_strategy(self, _id):
        # type: (int) -> Strategy
        """
           Arguments:
               _id (int): &nbsp;
           Returns:
               algotrader_com.domain.entity.Strategy
        """
        return self.get_portfolio(_id)

    def get_portfolio(self, _id):
        # type: (int) -> Portfolio
        """
           Arguments:
               _id (int): &nbsp;
           Returns:
               algotrader_com.domain.entity.Portfolio
        """
        vo = self._service.getPortfolio(_id)
        portfolio = Portfolio.convert_from_vo(vo)
        return portfolio

    def get_strategy_by_name(self, name):
        # type: (str) -> Strategy
        """
           Arguments:
               name (str): &nbsp;
           Returns:
               algotrader_com.domain.entity.Strategy
        """
        return self.get_portfolio_by_name(name)

    def get_portfolio_by_name(self, name):
        # type: (str) -> Portfolio
        """
           Arguments:
               name (str): &nbsp;
           Returns:
               algotrader_com.domain.entity.Portfolio
        """
        vo = self._service.getPortfolioByName(name)
        portfolio = Portfolio.convert_from_vo(vo)
        return portfolio

    def get_security_family(self, _id):
        # type: (int) -> SecurityFamily
        """
            Arguments:
                _id (int): &nbsp;
            Returns:
                algotrader_com.domain.entity.SecurityFamily
        """
        vo = self._service.getSecurityFamily(_id)
        portfolio = SecurityFamily.convert_from_vo(vo)
        return portfolio

    def get_security_family_by_name(self, name):
        # type: (str) -> SecurityFamily
        """
            Arguments:
                name (str): &nbsp;
            Returns:
                algotrader_com.domain.entity.SecurityFamily
        """
        vo = self._service.getSecurityFamilyByName(name)
        portfolio = SecurityFamily.convert_from_vo(vo)
        return portfolio

    def get_security_family_by_symbol_root(self, symbol_root):
        # type: (str) -> SecurityFamily
        """
            Arguments:
                symbol_root (str): &nbsp;
            Returns:
                algotrader_com.domain.entity.SecurityFamily
        """
        vo = self._service.getSecurityFamilyBySymbolRoot(symbol_root)
        portfolio = SecurityFamily.convert_from_vo(vo)
        return portfolio

    def get_option_family_by_underlying(self, underlying_id):
        # type: (int) -> SecurityFamily
        """
            Arguments:
                underlying_id (int): &nbsp;
            Returns:
                algotrader_com.domain.entity.SecurityFamily
        """
        vo = self._service.getOptionFamilyByUnderlying(underlying_id)
        portfolio = SecurityFamily.convert_from_vo(vo)
        return portfolio

    def get_future_family_by_underlying(self, underlying_id):
        # type: (int) -> SecurityFamily
        """
            Arguments:
                underlying_id (int): &nbsp;
            Returns:
                algotrader_com.domain.entity.SecurityFamily
        """
        vo = self._service.getFutureFamilyByUnderlying(underlying_id)
        portfolio = SecurityFamily.convert_from_vo(vo)
        return portfolio

    def get_all_exchanges(self):
        # type: () -> List[Exchange]
        """
            Returns:
                List of algotrader_com.domain.entity.Exchange
        """
        vos = self._service.getAllExchanges()
        exchanges = []
        for vo in vos:
            exchange = Exchange.convert_from_vo(vo)
            exchanges.append(exchange)
        return exchanges

    def get_exchange_by_name(self, name):
        # type: (str) -> Exchange
        """
            Arguments:
                name (str): &nbsp;
            Returns:
                algotrader_com.domain.entity.Exchange
        """
        vo = self._service.getExchangeByName(name)
        portfolio = Exchange.convert_from_vo(vo)
        return portfolio

    def get_exchange_by_id(self, _id):
        # type: (int) -> Exchange
        """
            Arguments:
                _id (int): &nbsp;
            Returns:
                algotrader_com.domain.entity.Exchange
        """
        vo = self._service.getExchangeById(_id)
        portfolio = Exchange.convert_from_vo(vo)
        return portfolio

    def get_all_positions(self):
        # type: () -> List[Position]
        """
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getAllPositions()
        if vo_jsons is None:
            return []
        positions = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_position_count(self):
        # type: () -> int
        """Gets the number of positions (open and closed).

            Returns:
                int
        """
        return self._service.getPositionCount()

    def get_position(self, _id):
        # type: (int) -> Optional[Position]
        """
            Arguments:
                _id (int): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.Position
        """
        vo_json = self._service.getPosition(_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        position = Position.convert_from_json(_dict)
        return position

    def get_positions_by_strategy(self, strategy_name):
        # type: (str) -> List[Position]
        """
            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_positions_by_portfolio(strategy_name)

    def get_positions_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Position]
        """
            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getPositionsByPortfolio(portfolio_name)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_position_by_security_and_strategy(self, security_id, strategy_name):
        # type: (int, str) -> Optional[Position]
        """
            Arguments:
                security_id (int): &nbsp;
                strategy_name (str): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.Position
        """
        return self.get_position_by_security_and_portfolio(security_id, strategy_name)

    def get_position_by_security_and_portfolio(self, security_id, portfolio_name):
        # type: (int, str) -> Optional[Position]
        """
            Arguments:
                security_id (int): &nbsp;
                portfolio_name (str): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.Position
        """
        vo_json = self._service.getPositionBySecurityAndPortfolio(security_id, portfolio_name)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        position = Position.convert_from_json(_dict)
        return position

    def get_open_positions(self):
        # type: () -> List[Position]
        """Gets all open positions (with a quantity != 0).

            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenPositions()
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_tradeable_positions(self):
        # type: () -> List[Position]
        """Gets open positions for tradeable securities.
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenTradeablePositions()
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_positions_by_strategy(self, strategy_name):
        # type: (str) -> List[Position]
        """
            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_positions_by_portfolio(strategy_name)

    def get_open_positions_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Position]
        """
            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenPositionsByPortfolio(portfolio_name)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_tradeable_positions_by_strategy(self, strategy_name):
        # type: (str) -> List[Position]
        """
            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_tradeable_positions_by_portfolio(strategy_name)

    def get_open_tradeable_positions_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Position]
        """
            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenTradeablePositionsByPortfolio(portfolio_name)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_positions_by_security(self, security_id):
        # type: (int) -> List[Position]
        """
            Arguments:
                security_id (int): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenPositionsBySecurity(security_id)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_positions_by_security_and_strategy(self, security_id, strategy_name):
        # type: (int, str) -> List[Position]
        """
            Arguments:
                security_id (int): &nbsp;
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_positions_by_security_and_portfolio(security_id, strategy_name)

    def get_open_positions_by_security_and_portfolio(self, security_id, portfolio_name):
        # type: (int, str) -> List[Position]
        """
            Arguments:
                security_id (int): &nbsp;
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenPositionsBySecurityAndPortfolio(security_id, portfolio_name)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_positions_by_strategy_and_type(self, strategy_name, security_class):
        # type: (str, Type[Security]) -> List[Position]
        """
            Arguments:
                strategy_name (str): &nbsp;
                security_class (algotrader_com.domain.security.Security subclass): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_positions_by_portfolio_and_type(strategy_name, security_class)

    def get_open_positions_by_portfolio_and_type(self, portfolio_name, security_class):
        # type: (str, Type[Security]) -> List[Position]
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_class (algotrader_com.domain.security.Security subclass): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        java_class = security_class.get_java_class()
        vo_jsons = self._service.getOpenPositionsByPortfolioAndType(portfolio_name, java_class)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_positions_by_strategy_type_and_underlying_type(self, strategy_name, type_security_class,
                                                                underlying_type_security_class):
        # type: (str, Type[Security], Type[Security]) -> List[Position]
        """
            Arguments:
                strategy_name (str): &nbsp;
                type_security_class (algotrader_com.domain.security.Security subclass): &nbsp;
                underlying_type_security_class (algotrader_com.domain.security.Security subclass): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_positions_by_portfolio_type_and_underlying_type(strategy_name, type_security_class,
                                                                             underlying_type_security_class)

    def get_open_positions_by_portfolio_type_and_underlying_type(self, portfolio_name, type_security_class,
                                                                underlying_type_security_class):
        # type: (str, Type[Security], Type[Security]) -> List[Position]
        """
            Arguments:
                portfolio_name (str): &nbsp;
                type_security_class (algotrader_com.domain.security.Security subclass): &nbsp;
                underlying_type_security_class (algotrader_com.domain.security.Security subclass): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        type_java_class = type_security_class.get_java_class()
        underlying_type_java_class = underlying_type_security_class.get_java_class()
        vo_jsons = self._service.getOpenPositionsByPortfolioTypeAndUnderlyingType(portfolio_name, type_java_class,
                                                                                 underlying_type_java_class)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_positions_by_strategy_and_security_family(self, strategy_name, security_family_id):
        # type: (str, int) -> List[Position]
        """
            Arguments:
                strategy_name (str): &nbsp;
                security_family_id (int): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_positions_by_portfolio_and_security_family(strategy_name, security_family_id)

    def get_open_positions_by_portfolio_and_security_family(self, portfolio_name, security_family_id):
        # type: (str, int) -> List[Position]
        """
            Arguments:
                portfolio_name (str): &nbsp;
                security_family_id (int): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenPositionsByPortfolioAndSecurityFamily(portfolio_name, security_family_id)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_fx_positions(self):
        # type: () -> List[Position]
        """Gets open Forex positions.

            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenFXPositions()
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def get_open_fx_positions_by_strategy(self, strategy_name):
        # type: (str) -> List[Position]
        """Gets open Forex positions of the specified strategy.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        return self.get_open_fx_positions_by_portfolio(strategy_name)

    def get_open_fx_positions_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Position]
        """Gets open Forex positions of the specified portfolio.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Position
        """
        vo_jsons = self._service.getOpenFXPositionsByPortfolio(portfolio_name)
        if vo_jsons is None:
            return []
        positions = []
        for _json in vo_jsons:
            _dict = Conversions.unmarshall(_json)
            position = Position.convert_from_json(_dict)
            positions.append(position)
        return positions

    def has_open_position(self, security_id, portfolio_name):
        # type: (int, str) -> bool
        """Returns true if the specified portfolio has an open position on the specified security.

            Arguments:
                security_id (int): &nbsp;
                portfolio_name (str): &nbsp;
            Returns:
                bool
        """
        return self._service.hasOpenPosition(security_id, portfolio_name)

    def get_transaction(self, _id):
        # type: (int) -> Optional[Transaction]
        """
            Arguments:
                _id (int): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.Transaction
        """
        vo_json = self._service.getTransaction(_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        transaction = Transaction.convert_from_json(_dict)
        return transaction

    def get_transaction_by_ext_id(self, _id):
        # type: (str) -> Optional[Transaction]
        """
            Arguments:
                _id (str): &nbsp;
            Returns:
                Optional of algotrader_com.domain.entity.Transaction
        """
        vo_json = self._service.getTransactionByExtId(_id)
        if vo_json is None:
            return None
        _dict = Conversions.unmarshall(vo_json)
        transaction = Transaction.convert_from_json(_dict)
        return transaction

    def get_daily_transactions(self, limit=None):
        # type: (Optional[int]) -> List[Transaction]
        """Finds all transactions of the current day in descending dateTime order.

            Arguments:
                limit (Optional[int]): defines maximum number of records to be retrieved. Value of None or 0 represents no limit.
            Returns:
                List of algotrader_com.domain.entity.Transaction
        """
        vo_jsons = self._service.getDailyTransactions(limit)
        if vo_jsons is None:
            return []
        transactions = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            transaction = Transaction.convert_from_json(_dict)
            transactions.append(transaction)
        return transactions

    def get_daily_transactions_by_strategy(self, strategy_name, limit=None):
        # type: (str, Optional[int]) -> List[Transaction]
        """Finds all transactions of the current day of the specified_strategy in descending dateTime order.

            Arguments:
                strategy_name (str): &nbsp;
                limit (Optional[int]): defines maximum number of records to be retrieved. Value 0 represents no limit.
            Returns:
                List of algotrader_com.domain.entity.Transaction
        """
        return self.get_daily_transactions_by_portfolio(strategy_name, limit)

    def get_daily_transactions_by_portfolio(self, portfolio_name, limit=None):
        # type: (str, Optional[int]) -> List[Transaction]
        """Finds all transactions of the current day of the specified portfolio in descending dateTime order.

            Arguments:
                portfolio_name (str): &nbsp;
                limit (Optional[int]): defines maximum number of records to be retrieved. Value 0 represents no limit.
            Returns:
                List of algotrader_com.domain.entity.Transaction
        """
        if limit is None:
            limit = 0
        vo_jsons = self._service.getDailyTransactionsByPortfolio(portfolio_name, limit)
        if vo_jsons is None:
            return []
        transactions = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            transaction = Transaction.convert_from_json(_dict)
            transactions.append(transaction)
        return transactions

    def get_trades_by_min_date_and_max_date(self, min_date, max_date, transaction_types=None):
        # type: (datetime, datetime, Optional[List[str]]) -> List[Transaction]
        """Finds all trades (BUY and SELL transactions) for the given time frame.

            Arguments:
                min_date (datetime): &nbsp;
                max_date (datetime): &nbsp;
                transaction_types (List[str]): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Transaction
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_java = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)

        transaction_type_class = self._gateway.jvm.TransactionType
        transaction_types_enums = self._gateway.new_array(transaction_type_class, len(transaction_types))
        if transaction_types is not None:
            for i in range(len(transaction_types)):
                transaction_types_enum = self._gateway.jvm.TransactionType.valueOf(transaction_types[i])
                transaction_types_enums[i] = transaction_types_enum

        vo_jsons = self._service.getTradesByMinDateAndMaxDate(min_date_java, max_date_java, transaction_types_enums)
        if vo_jsons is None:
            return []
        transactions = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            transaction = Transaction.convert_from_json(_dict)
            transactions.append(transaction)
        return transactions

    def get_trades_by_portfolio_and_min_date_and_max_date(self, portfolio_name, min_date, max_date, transaction_types=None):
        # type: (str, datetime, datetime, Optional[List[str]]) -> List[Transaction]
        """Finds all trades (BUY and SELL transactions) for the given time frame.

            Arguments:
                portfolio_name (str): &nbsp;
                min_date (datetime): &nbsp;
                max_date (datetime): &nbsp;
                transaction_types (List[str]): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Transaction
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        max_date_java = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)

        transaction_type_class = self._gateway.jvm.TransactionType
        transaction_types_enums = self._gateway.new_array(transaction_type_class, len(transaction_types))
        if transaction_types is not None:
            for i in range(len(transaction_types)):
                transaction_types_enum = self._gateway.jvm.TransactionType.valueOf(transaction_types[i])
                transaction_types_enums[i] = transaction_types_enum

        vo_jsons = self._service.getTradesByPortfolioAndMinDateAndMaxDate(portfolio_name, min_date_java, max_date_java, transaction_types_enums)
        if vo_jsons is None:
            return []
        transactions = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            transaction = Transaction.convert_from_json(_dict)
            transactions.append(transaction)
        return transactions

    def get_daily_orders(self):
        # type: () -> List[Order]
        """Finds all orders of the current day in descending dateTime order.

            Returns:
                List of algotrader_com.domain.order.Order
        """
        vo_jsons = self._service.getDailyOrders()
        if vo_jsons is None:
            return []
        orders = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_daily_orders_by_strategy(self, strategy_name):
        # type: (str) -> List[Order]
        """Finds all orders of the current day of a specific strategy in descending dateTime order.

            Arguments:
                strategy_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.order.Order
        """
        return self.get_daily_orders_by_portfolio(strategy_name)

    def get_daily_orders_by_portfolio(self, portfolio_name):
        # type: (str) -> List[Order]
        """Finds all orders of the current day of a specific portfolio in descending dateTime order.

            Arguments:
                portfolio_name (str): &nbsp;
            Returns:
                List of algotrader_com.domain.order.Order
        """
        vo_jsons = self._service.getDailyOrdersByPortfolio(portfolio_name)
        if vo_jsons is None:
            return []
        orders = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            order = Order.convert_from_json_object(_dict)
            orders.append(order)
        return orders

    def get_all_accounts(self):
        # type: () -> List[Account]
        """
           Returns:
               List of algotrader_com.domain.entity.Account
        """

        vos = self._service.getAllAccounts()
        accounts = []
        for vo in vos:
            account = Account.convert_from_vo(vo)
            accounts.append(account)
        return accounts

    def get_account(self, account_id):
        # type: (int) -> Optional[Account]
        """
           Gets an account by its id.
           Returns:
               Optional of algotrader_com.domain.entity.Account
        """
        account_java = self._service.getAccount(account_id)
        if account_java is None:
            return None
        account = Account.convert_from_vo(account_java)
        return account

    def get_account_by_name(self, account_name):
        # type: (str) -> Optional[Account]
        """
           Gets an account by its name.
           Returns:
               Optional of algotrader_com.domain.entity.Account
        """
        account_java = self._service.getAccountByName(account_name)
        if account_java is None:
            return None
        account = Account.convert_from_vo(account_java)
        return account

    def get_active_sessions_by_connector_descriptor(self, connector_descriptor_str):
        # type: (str) -> List[str]
        """Gets all active accounts for the specified adapter type.

           Arguments:
               .. include:: ../adapter_types.txt
           Returns:
               List[str]
        """
        connector_descriptor = Conversions.convert_to_connector_descriptor(connector_descriptor_str, self._gateway)
        vos = self._service.getActiveSessionsByConnectorDescriptor(connector_descriptor)
        sessions = []
        for vo in vos:
            sessions.append(vo)
        return sessions

    def get_interest_rate_by_currency_and_duration(self, currency, duration):
        # type: (str, str) -> Optional[IntrestRate]
        """Arguments:
               currency (str): &nbsp;
               duration (str): MSEC_1, SEC_1, SEC_5, SEC_10, SEC_15, SEC_30, MIN_1, MIN_2, MIN_3, MIN_5, MIN_10, MIN_15, MIN_20, MIN_30, HOUR_1, HOUR_2, HOUR_3, HOUR_4, HOUR_8, DAY_1, DAY_2, WEEK_1, WEEK_2, MONTH_1, MONTH_2, MONTH_3, MONTH_4, MONTH_5, MONTH_6, MONTH_7, MONTH_8, MONTH_9, MONTH_10, MONTH_11, MONTH_18, YEAR_1, YEAR_2
           Returns:
               Optional of algotrader_com.domain.security.IntrestRate
        """
        duration_java = self._gateway.jvm.Duration.valueOf(duration)
        vo = self._service.getInterestRateByCurrencyAndDuration(currency,
                                                                duration_java)
        if vo is None:
            return None
        obj = IntrestRate.convert_from_vo(vo, self._gateway)
        return obj

    def get_all_cash_balances(self):
        # type: () -> List[CashBalance]
        """
           Returns:
               List of algotrader_com.domain.entity.CashBalance
        """
        vo_jsons = self._service.getAllCashBalances()
        cash_balances = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            cash_balance = CashBalance.convert_from_json(_dict)
            cash_balances.append(cash_balance)
        return cash_balances

    def get_cash_balances_by_strategy(self, strategy_name):
        # type: (str) -> List[CashBalance]
        """ Arguments:
               strategy_name (str): &nbsp;
            Returns:
               List of algotrader_com.domain.entity.CashBalance
        """
        return self.get_cash_balances_by_portfolio(strategy_name)

    def get_cash_balances_by_portfolio(self, portfolio_name):
        # type: (str) -> List[CashBalance]
        """ Arguments:
               portfolio_name (str): &nbsp;
            Returns:
               List of algotrader_com.domain.entity.CashBalance
        """
        vo_jsons = self._service.getCashBalancesByPortfolio(portfolio_name)
        cash_balances = []
        for vo_json in vo_jsons:
            _dict = Conversions.unmarshall(vo_json)
            cash_balance = CashBalance.convert_from_json(_dict)
            cash_balances.append(cash_balance)
        return cash_balances

    def get_all_measurements_by_max_date(self, portfolio_name, max_date):
        # type: (str, datetime) -> Dict[datetime, Dict[str, Any]]
        """Gets all measurements before the specified date.

            Arguments:
               portfolio_name (str): &nbsp;
               max_date (datetime): &nbsp;
            Returns:
               Dict[datetime, Dict[str, Any]]
        """
        max_date_java = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        vo = self._service.getAllMeasurementsByMaxDate(portfolio_name, max_date_java)
        measurements = {}
        for key1 in vo:
            measurement = {}  # type: Dict[str, Any]
            key1_datetime = Conversions.zoned_date_time_to_python_datetime(key1)
            measurements[key1_datetime] = measurement
            value1 = vo[key1]
            for key2 in value1:
                value2 = value1[key2]
                measurement[key2] = value2

        return measurements

    def get_all_measurements_by_min_date(self, portfolio_name, min_date):
        # type: (str, datetime) -> Dict[datetime, Dict[str, Any]]
        """Gets all measurements after the specified date.

            Arguments:
               portfolio_name (str): &nbsp;
               min_date (datetime): &nbsp;
            Returns:
               Dict[datetime, Dict[str, Any]]
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        vo = self._service.getAllMeasurementsByMinDate(portfolio_name, min_date_java)
        measurements = {}
        for key1 in vo:
            measurement = {}  # type: Dict[str, Any]
            key1_datetime = Conversions.zoned_date_time_to_python_datetime(key1)
            measurements[key1_datetime] = measurement
            value1 = vo[key1]
            for key2 in value1:
                value2 = value1[key2]
                measurement[key2] = value2

        return measurements

    def get_measurements_by_max_date(self, portfolio_name, name, max_date):
        # type: (str, str, datetime) -> Dict[datetime, Any]
        """Gets all Measurements before the specified Date with the specified name.

            Arguments:
               portfolio_name (str): &nbsp;
               name (str): &nbsp;
               max_date (datetime): &nbsp;
            Returns:
               Dict[datetime, Any]
        """
        max_date_java = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        vo = self._service.getMeasurementsByMaxDate(portfolio_name, name, max_date_java)
        measurements = {}
        for key1 in vo:
            key1_datetime = Conversions.zoned_date_time_to_python_datetime(key1)
            measurements[key1_datetime] = vo[key1]
        return measurements

    def get_measurements_by_min_date(self, portfolio_name, name, min_date):
        # type: (str, str, datetime) -> Dict[datetime, Any]
        """Gets all Measurements after the specified Date with the specified name.

            Arguments:
               portfolio_name (str): &nbsp;
               name (str): &nbsp;
               min_date (datetime): &nbsp;
            Returns:
               Dict[datetime, Any]
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        vo = self._service.getMeasurementsByMinDate(portfolio_name, name, min_date_java)
        measurements = {}
        for key1 in vo:
            key1_datetime = Conversions.zoned_date_time_to_python_datetime(key1)
            measurements[key1_datetime] = vo[key1]
        return measurements

    def get_measurement_by_max_date(self, portfolio_name, name, max_date):
        # type: (str, str, datetime) -> Any
        """Gets the first Measurement before the specified Date with the specified name.

            Arguments:
               portfolio_name (str): &nbsp;
               name (str): &nbsp;
               max_date (datetime): &nbsp;
            Returns:
               Any
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(max_date, self._gateway)
        return self._service.getMeasurementByMaxDate(portfolio_name, name, min_date_java)

    def get_measurement_by_min_date(self, portfolio_name, name, min_date):
        # type: (str, str, datetime) -> Any
        """Gets the first Measurement after the specified Date with the specified name.

            Arguments:
               portfolio_name (str): &nbsp;
               name (str): &nbsp;
               min_date (datetime): &nbsp;
            Returns:
               Any
        """
        min_date_java = Conversions.python_datetime_to_zoneddatetime(min_date, self._gateway)
        return self._service.getMeasurementByMinDate(portfolio_name, name, min_date_java)

    def get_subscribed_securities_and_connector_descriptor_for_auto_activate_strategies_incl_components(self):
        # type: () -> List[Tuple[int, str]]
        """
           Gets all subscribed Securities and corresponding Account for Strategies that are marked auto_activate.
           If corresponding Securities are Combinations, all Components will be initialized as well.
           Returns a list of tuples, first item is security id and the second connector descriptor.
           Returns:
               List[Tuple[int, str]]
        """
        return self.get_subscribed_securities_and_connector_descriptor_for_auto_activate_portfolios_incl_components()

    def get_subscribed_securities_and_connector_descriptor_for_auto_activate_portfolios_incl_components(self):
        # type: () -> List[Tuple[int, str]]
        """
           Gets all subscribed Securities and corresponding Account for Portfolios that are marked auto_activate.
           If corresponding Securities are Combinations, all Components will be initialized as well.
           Returns a list of tuples, first item is security id and the second connector descriptor.
           Returns:
               List[Tuple[int, str]]
        """
        service_result = self._service.getSubscribedSecuritiesAndConnectorDescriptorForAutoActivatePortfoliosInclComponents()
        result = []  # type: List[Tuple[int, str]]
        for entry in service_result:
            value = (int(entry[0]), entry[1])
            result.append(value)
        return result

    def get_subscribed_combinations_by_strategy_and_component_class(self, strategy_name, security_class):
        # type: (str, Type[Security]) -> List[Combination]
        """
           Gets Combinations that are subscribed by the specified Strategy and have a Component with the specified Security Type.
           Returns:
               List of algotrader_com.domain.security.Combination
        """
        return self.get_subscribed_combinations_by_portfolio_and_component_class(strategy_name, security_class)

    def get_subscribed_combinations_by_portfolio_and_component_class(self, portfolio_name, security_class):
        # type: (str, Type[Security]) -> List[Combination]
        """
           Gets Combinations that are subscribed by the specified Portfolio and have a Component with the specified Security Type.
           Returns:
               List of algotrader_com.domain.security.Combination
        """
        java_class = security_class.get_java_class()
        service_result = self._service.getSubscribedCombinationsByPortfolioAndComponentClass(portfolio_name, java_class)
        result = []  # type: List[Combination]
        for entry in service_result:
            value = Combination.convert_from_vo(entry, self._gateway)
            result.append(value)
        return result

    def find_accounts_with_connector_descriptor(self, connector_descriptor_str):
        # type: (str) -> List[Account]
        """
            Arguments:
                connector_descriptor (str): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Account
        """
        connector_descriptor = Conversions.convert_to_connector_descriptor(connector_descriptor_str, self._gateway)
        vos = self._service.findAccountsWithConnectorDescriptor(connector_descriptor)
        if vos is None:
            return []
        accounts = []
        for vo in vos:
            account = Account.convert_from_vo(vo)
            accounts.append(account)
        return accounts

    def find_accounts_with_exchange_access(self, exchange):
        # type: (Exchange) -> List[Account]
        """
            Arguments:
                exchange (Exchange): &nbsp;
            Returns:
                List of algotrader_com.domain.entity.Account
        """
        exchange_vo = exchange.convert_to_vo(self._gateway)
        vos = self._service.findAccountsWithExchangeAccess(exchange_vo)

        if vos is None:
            return []
        accounts = []
        for vo in vos:
            account = Account.convert_from_vo(vo)
            accounts.append(account)
        return accounts

    def get_transaction_count(self):
        # type: () -> int
        """
            Returns:
                The number of transactions
        """
        return self._service.getTransactionCount
