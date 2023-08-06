import typing
from famegui.models import AgentDisplay, AgentField

class Agent:
    """ Represents an agent as defined in a scenario file """

    def __init__(self, id, type_):
        assert type(id) == int and id >= 0
        assert type(type_) == str and type_ != ""
        self._id = id
        self._type = type_
        self._inputs = []
        self._outputs = []
        self._fields = {}
        self._display = AgentDisplay()

    @property
    def id(self) -> int:
        return self._id

    @property
    def id_str(self) -> str:
        return "#{}".format(self._id)

    @property
    def type(self) -> str:
        return self._type

    @property
    def inputs(self) -> typing.List[int]:
        return self._inputs

    @property
    def outputs(self) -> typing.List[int]:
        return self._outputs

    @property
    def fields(self) -> typing.Dict[str, AgentField]:
        return self._fields

    @property
    def display(self) -> AgentDisplay:
        return self._display

    def add_input(self, agent_id):
        self._inputs.append(agent_id)

    def add_output(self, agent_id):
        self._outputs.append(agent_id)

    def add_field(self, name, value):
        if name in self._fields:
            raise ValueError("can't add field '{}' because it already exists in the agent".format(name))
        self._fields[name] = AgentField(name, value)

    def set_display_coords(self, x, y):
        self._display.coords = [x, y]
