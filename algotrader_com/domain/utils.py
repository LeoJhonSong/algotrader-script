from algotrader_com.domain.conversions import Conversions


class JsonPredicate:
    """Class representing java.util.function.Predicate<String> for JSON objects
    Converts the incoming JSON to dictionary and applies given function to it.

    Attributes:
         fn (function): A function taking a dictionary and returning a boolean
    """
    def __init__(self, fn):
        self.fn = fn

    def test(self, json):
        arg = Conversions.unmarshall(json)
        return bool(self.fn(arg))

    class Java:
        def __init__(self):
            pass

        implements = ["java.util.function.Predicate"]
