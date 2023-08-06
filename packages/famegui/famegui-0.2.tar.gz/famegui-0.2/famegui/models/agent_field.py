import typing

class AgentField:
    """ Details about a single agent field """

    def __init__(self, name, value):
        assert name != ""
        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self):
        return self._value
