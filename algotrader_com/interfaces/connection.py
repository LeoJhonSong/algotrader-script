import time
from typing import List, Optional

from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
from py4j.java_gateway import java_import, DEFAULT_PORT, DEFAULT_PYTHON_PROXY_PORT

from algotrader_com.interfaces.at2py import AlgoTraderToPythonInterface
from algotrader_com.interfaces.py2at import PythonToAlgoTraderInterface
from algotrader_com.services.strategy import StrategyService

gateway = None


def connect_to_algotrader(strategy_service, only_subscribe_methods_list=None, java_port=DEFAULT_PORT,
                          python_port=DEFAULT_PYTHON_PROXY_PORT):
    # type: (StrategyService, Optional[List[str]], int, int) -> PythonToAlgoTraderInterface
    """Waits for AlgoTrader to start if it is not started already and connects to it.
       Returns entry point object of class PythonToAlgoTraderInterface to be used by strategies to make calls to AT.

       Arguments:
           strategy_service (algotrader_com.services.strategy.StrategyService): Strategy implementation. An object of a class extending algotrader_com.services.strategy.StrategyService.
           only_subscribe_methods_list (Optional[List[str]]): Optional parameter, for optimization only, None value subscribes all event handler methods. Use the names of onXYZ methods in algotrader_com.interfaces.at2py.AlgoTraderToPythonInterface.
           java_port (int): The port to connect to where Java part of AlgoTrader is running. Only to be set a custom value when multiple strategies need to be set up with StrategyStarter.
           python_port (int): The port to expose for the Java part of AlgoTrader. Only to be set a custom value when multiple strategies need to be set up with StrategyStarter..
       Returns:
           PythonToAlgoTraderInterface: Entry point object to be used by strategies to make calls to AT.
    """

    at_to_python_entry_point = AlgoTraderToPythonInterface(strategy_service)
    global gateway
    gateway = ClientServer(java_parameters=JavaParameters(port=java_port),
                           python_parameters=PythonParameters(port=python_port),
                           python_server_entry_point=at_to_python_entry_point)
    python_to_at_entry_point = PythonToAlgoTraderInterface(gateway)
    at_to_python_entry_point.with_py4j_gateway(gateway)
    at_to_python_entry_point.with_python_to_at_entry_point(python_to_at_entry_point)

    _wait_for_algotrader(python_to_at_entry_point)

    if only_subscribe_methods_list is None:
        python_to_at_entry_point.subscribe_to_only_some_event_handler_methods(["ALL"])
    else:
        python_to_at_entry_point.subscribe_to_only_some_event_handler_methods(only_subscribe_methods_list)

    _import_packages()
    return python_to_at_entry_point


def shut_down_gateway():
    """Closes the connection to AlgoTrader from Python Side"""
    gateway.shutdown(raise_exception=False)


# noinspection PyBroadException
def _wait_for_algotrader(python_to_at_entry_point):
    # type: (PythonToAlgoTraderInterface) -> None
    """Tries to ping AlgoTrader on the Java side in a loop until it succeeds."""
    first_attempt = True
    while True:
        try:
            python_to_at_entry_point.ping()
            break
        except:
            if first_attempt:
                print("Waiting for AlgoTrader to start.")
            time.sleep(0.5)
        first_attempt = False
    python_to_at_entry_point.prepare_services()
    print("Connected to AlgoTrader.")


# noinspection PyBroadException
def wait_for_algotrader_to_disconnect(python_to_at_entry_point):
    # type: (PythonToAlgoTraderInterface) -> None
    """Pings AlgoTrader on the Java side in a loop until this fails or AlgoTrader reports it's disconnecting."""
    while True:
        if gateway.python_server_entry_point.algotrader_disconnecting:
            break
        try:
            python_to_at_entry_point.ping()
            time.sleep(0.5)
        except:
            break
    print("AlgoTrader disconnected.")
    shut_down_gateway()


def _import_packages():
    # convenience Java class packages imports for instantiating Java objects via gateway.jvm.ClassName mechanism
    java_import(gateway.jvm, 'ch.algotrader.vo.*')
    java_import(gateway.jvm, 'ch.algotrader.dao.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.marketData.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.portfolio.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.security.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.exchange.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.trade.algo.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.trade.*')
    java_import(gateway.jvm, 'ch.algotrader.entity.broker.*')
    java_import(gateway.jvm, 'ch.algotrader.enumeration.*')
    java_import(gateway.jvm, 'java.math.*')
    java_import(gateway.jvm, 'java.time.*')
    java_import(gateway.jvm, 'java.util.*')
    java_import(gateway.jvm, 'ch.algotrader.vo.genericevents.*')
    java_import(gateway.jvm, 'ch.algotrader.event.dispatch.*')
