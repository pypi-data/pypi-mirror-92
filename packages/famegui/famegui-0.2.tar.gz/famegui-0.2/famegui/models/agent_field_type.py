import typing

class AgentFieldType:
    """ Represents an agent field type as defined in the schema file """

    Integer = "integer"
    Double = "double"
    IntegerList = "integer_list"
    DoubleList = "double_list"
    TimeSeries = "time_series"
    Enum = "enum"

    AllTypes = {
        "integer" : Integer,
        "double" : Double,
        "integer_list" : IntegerList,
        "double_list" : DoubleList,
        "time_series" : TimeSeries,
        "enum" : Enum,
    }

    def __init__(self, type_name : str, is_mandatory : bool, enum_values : typing.List[str] = None):
        if type_name not in AgentFieldType.AllTypes:
            raise ValueError("invalid agent field type '{}'".format(type_name))
        if type_name == AgentFieldType.Enum:
            if enum_values is None or len(enum_values) == 0:
                raise ValueError("values are missing for agent field type '{}'".format(type_name))
            else:
                for v in enum_values:
                    assert v != ""
        elif enum_values is not None:
            raise ValueError("enum values can't be specified for agent field type '{}'".format(type_name))

        self._type_name = AgentFieldType.AllTypes[type_name]
        self._is_mandatory = is_mandatory
        self._enum_values = enum_values

    @property
    def type_name(self) -> str:
        return self._type_name

    @property
    def is_mandatory(self) -> bool:
        return self._is_mandatory

    @property
    def enum_values(self) -> typing.List[str]:
        return self._enum_values
