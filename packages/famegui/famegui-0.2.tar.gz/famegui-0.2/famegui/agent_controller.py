from famegui import models, colorpalette


class AgentController(models.Agent):
    """ Controller attached to a FAME Agent to sync it with the views """

    def __init__(self, agent: models.Agent):
        self.model = agent
        self.tree_item = None
        self.scene_item = None

    @property
    def id(self) -> int:
        return self.model.id

    @property
    def id_str(self) -> str:
        return self.model.id_str

    @property
    def type(self) -> str:
        return self.model.type

    @property
    def field_list(self):
        return self.model.fields.values()

    @property
    def tooltip_text(self) -> str:
        text = "<font size='4'><b>{}</b></font>".format(self.model.type)

        text += "<table border=0 cellpadding=2 style='border-collapse: collapse'><tbody>"
        text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
            "ID", self.model.id_str)
        for f in self.model.fields.values():
            text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
                f.name, f.value)

        text += "</tbody></table>"
        return text

    @property
    def svg_color(self) -> str:
        return colorpalette.color_for_agent_type(self.type)

    @property
    def x(self):
        return self.model.display.coords[0]

    @property
    def y(self):
        return self.model.display.coords[1]
