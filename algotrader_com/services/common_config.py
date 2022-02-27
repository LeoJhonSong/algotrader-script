from decimal import Decimal
from typing import List, Dict

from py4j.clientserver import ClientServer

from algotrader_com.domain.config import DataSourceConfig
from algotrader_com.domain.conversions import Conversions


class CommonConfig:
    """Delegates to commonConfig object in PythonStrategyService on the Java side.

       Initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.getCommonConfig()

    def get_data_set_name(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getDataSetName()

    def get_report_location(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getReportLocation().getAbsolutePath()

    def is_disable_reports(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isDisableReports()

    def is_open_back_test_report(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isOpenBackTestReport()

    def is_filename_timestamp(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isFilenameTimestamp()

    def is_simulation(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isSimulation()

    def get_simulation_initial_balance(self):
        # type: () -> Decimal
        """
        Returns:
            Decimal
        """
        return self._service.getSimulationInitialBalance()

    def is_embedded(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isEmbedded()

    def get_portfolio_base_currency(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getPortfolioBaseCurrency()

    def get_portfolio_digits(self):
        # type: () -> int
        """
        Returns:
            int
        """
        return self._service.getPortfolioDigits()

    def get_maximum_digits(self):
        # type: () -> int
        """
        Returns:
            int
        """
        return self._service.getMaximumDigits()

    def get_quickfix_config_url(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getQuickfixConfigUrl()

    def get_inbound_fix_config_url(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getInboundFixConfigUrl()

    def get_default_account_name(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getDefaultAccountName()

    def is_validate_crossed_spread(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isValidateCrossedSpread()

    def get_future_symbol_pattern(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getFutureSymbolPattern()

    def get_option_symbol_pattern(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getOptionSymbolPattern()

    def is_locate_existing_mbean_server(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isLocateExistingMBeanServer()

    def is_drop_copy_transaction_storing_enabled(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isDropCopyTransactionStoringEnabled()

    def get_keygen_id(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getKeygenId()

    def get_keygen_account_id(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getKeygenAccountId()

    def get_keygen_configuration(self):
        # type: () -> str
        """
        Returns:
            str
        """
        return self._service.getKeygenConfiguration()

    def get_orderbook_filter_global(self):
        # type: () -> Decimal
        """
        Returns:
            Decimal
        """
        return self._service.getOrderBookFilterGlobal()

    def get_orderbook_filter_by_account(self):
        # type: () -> Dict
        """
        Returns:
            Decimal
        """
        result = self._service.getOrderBookFilterGlobal()
        _dict = Conversions.unmarshall(result)
        return _dict

    def get_data_source_configs(self):
        # type: () -> List[DataSourceConfig]
        """
        Returns:
            List of algotrader_com.domain.config.DataSourceConfig
        """
        config_vos = self._service.getDataSourceConfigs()
        configs = []
        for config_vo in config_vos:
            config = DataSourceConfig.convert_from_vo(config_vo)
            configs.append(config)
        return configs

    def is_persist_generic_events(self):
        # type: () -> bool
        """
        Returns:
            bool
        """
        return self._service.isPersistGenericEvents()
