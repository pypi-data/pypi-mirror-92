import typing
from famegui.models import AgentFieldType

class AgentType:
    """ Represents an agent type as defined in the schema file """

    def __init__(self, name):
        assert name != ""
        self._name = name
        self._fields = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def fields(self) -> typing.Dict[str, AgentFieldType]:
        return self._fields

    def add_field(self, field_name : str, type_name : str, is_mandatory : bool, enum_values : typing.List[str] = None):
        if field_name in self._fields:
            raise ValueError("can't add field '{}' to agent type because it already exists".format(field_name))
        self._fields[field_name] = AgentFieldType(type_name, is_mandatory, enum_values)
