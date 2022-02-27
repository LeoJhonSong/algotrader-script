from typing import List, Dict, Any

from py4j.clientserver import ClientServer

from algotrader_com.domain.entity import PropertyHolder


class PropertyService:
    """Delegates to pythonPropertyService object in PythonStrategyService on the Java side.
       The service is used for retrieval and updates of custom key-value properties that can be set on entities
       of types:

        Transaction

        Subscription

        Account

        Order

        Security

        SecurityFamily

        OrderPreference

        Exchange

        Strategy

        Position

       The service is initialized by <i>connect_to_algotrader</i> function
       and a property of <i>python_to_at_entry_point (PythonToAlgoTraderInterface)</i> object set on connect."""

    def __init__(self, gateway):
        # type: (ClientServer) -> None
        self._gateway = gateway
        if gateway is not None:
            self._service = self._gateway.entry_point.getPythonPropertyService()

    def get_all_property_holder_classes_names(self):
        # type: () -> List[str]
        """
           Returns:
               List[str]
        """
        _classes = self._service.getAllPropertyHolderClassesNames()
        _classes_list = []
        for _class in _classes:
            _classes_list.append(_class)
        return sorted(_classes_list)

    def get_all_properties(self, property_holder_object):
        # type: (PropertyHolder) -> Dict
        """
           Arguments:
               property_holder_object (PropertyHolder): &nbsp;
           Returns:
               Dict
        """
        response = self._service.getAllProperties(property_holder_object.get_java_class(), property_holder_object.id)
        result = {}
        for key in response:
            result[key] = response[key]
        return result

    def get_property(self, property_holder_object, property_name):
        # type: (PropertyHolder, str) -> Any
        """
           Arguments:
               property_holder_object (PropertyHolder): &nbsp;
               property_name (str): &nbsp;
           Returns:
               "?"
        """
        response = self._service.getProperty(property_holder_object.get_java_class(),
                                             property_holder_object.id, property_name)
        return response

    def set_property(self, property_holder_object, property_name, value):
        # type: (PropertyHolder, str, Any) -> None
        """
           Arguments:
               property_holder_object (PropertyHolder): &nbsp;
               property_name (str): &nbsp;
               value: String and numeric values are supported.
        """
        self._service.setProperty(property_holder_object.get_java_class(), property_holder_object.id, property_name,
                                  value)

    def remove_property(self, property_holder_object, property_name):
        # type: (PropertyHolder, str) -> None
        """
           Arguments:
               property_holder_object (PropertyHolder): &nbsp;
               property_name (str): &nbsp;
        """
        self._service.removeProperty(property_holder_object.get_java_class(), property_holder_object.id, property_name)

    def clear_properties(self, property_holder_object):
        # type: (PropertyHolder) -> None
        """
           Arguments:
               property_holder_object (PropertyHolder): &nbsp;
        """
        self._service.clearProperties(property_holder_object.get_java_class(), property_holder_object.id)


