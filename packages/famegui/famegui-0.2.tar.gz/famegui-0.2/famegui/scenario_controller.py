import logging
import typing
from PySide2 import QtCore

from famegui import models
from famegui.agent_controller import AgentController


class ScenarioController(QtCore.QObject):
    selected_agent_changed = QtCore.Signal(AgentController)
    has_scenario_data_changed = QtCore.Signal(bool)
    has_unsaved_changes_changed = QtCore.Signal(bool)
    # new path
    file_path_changed = QtCore.Signal(str)
    # added agent
    agent_added = QtCore.Signal(AgentController)
    # sender, receiver, contract
    contract_added = QtCore.Signal(
        AgentController, AgentController, models.Contract)

    def __init__(self):
        super().__init__()
        self._scenario = None
        self._agents = {}
        self._contracts = {}
        self._file_path = ""
        self._has_unsaved_changes = False

    def reset(self):
        self._agents = {}
        self._contracts = {}
        self._set_file_path("")
        self._set_has_unsaved_changes(False)
        self._scenario = None
        self.has_scenario_data_changed.emit(False)

    @property
    def has_scenario_data(self) -> bool:
        return self._scenario is not None

    @property
    def has_unsaved_changes(self) -> bool:
        return self.has_scenario_data and self._has_unsaved_changes

    def _set_has_unsaved_changes(self, has_unsaved: bool):
        assert self.has_scenario_data or not has_unsaved
        if self._has_unsaved_changes != has_unsaved:
            self._has_unsaved_changes = has_unsaved
            self.has_unsaved_changes_changed.emit(self._has_unsaved_changes)

    @property
    def file_path(self) -> str:
        return self._file_path

    def _set_file_path(self, path: str):
        assert self.has_scenario_data or path == ""
        if self._file_path != path:
            self._file_path = path
            self.file_path_changed.emit(self._file_path)

    @property
    def agent_list(self) -> typing.List[AgentController]:
        assert self.has_scenario_data
        return self._agents.values()

    def generate_new_agent_id(self):
        new_id = len(self._agents) + 1
        # note: we don't control how ids have been generated for agents created from an external source
        # so we check for possible conflict and solve it
        if new_id in self._agents:
            for i in range(1, len(self._agents) + 2):
                if not i in self._agents:
                    new_id = i
                    break
        logging.debug("generated new agent id {}".format(new_id))
        return new_id

    # the given agent id can be 0 to clear the current selection
    def set_selected_agent_id(self, agent_id: int):
        assert self.has_scenario_data
        if agent_id not in self._agents:
            assert agent_id == 0 or agent_id is None
            self.selected_agent_changed.emit(None)
        else:
            self.selected_agent_changed.emit(self._agents[agent_id])

    def add_new_agent(self, agent_model: models.Agent, x: int, y: int):
        assert self.has_scenario_data
        agent_model.display.coords = [x, y]
        self._scenario.add_agent(agent_model)
        self._add_agent_model(agent_model)
        self._set_has_unsaved_changes(True)
        logging.info("created new agent {} of type '{}'".format(
            agent_model.id_str, agent_model.type))

    def _add_agent_model(self, agent_model: models.Agent):
        assert self.has_scenario_data
        agent = AgentController(agent_model)
        self._agents[agent.id] = agent

        self.agent_added.emit(agent)

    def add_new_contract(self, contract_model: models.Contract):
        self._scenario.add_contract(contract_model)
        self._add_contract_model(contract_model)
        self._set_has_unsaved_changes(True)
        logging.info("created new contract '{}' between {} and {}".format(
            contract_model.product_name, contract_model.sender_id_str, contract_model.receiver_id_str))

    def _add_contract_model(self, contract: models.Contract):
        assert self.has_scenario_data
        # should be enforced when creating / reading the contract
        assert contract.sender_id != contract.receiver_id

        # validate sender / receiver are known
        if contract.sender_id not in self._agents:
            raise ValueError("can't add contract '{}' because sender agent id '{}' is unknown".format(
                contract.name, contract.sender_id))
        if contract.receiver_id not in self._agents:
            raise ValueError("can't add contract '{}' because receiver agent id '{}' is unknown".format(
                contract.name, contract.receiver_id))

        sender_ctrl = self._agents[contract.sender_id]
        receiver_ctrl = self._agents[contract.receiver_id]

        # connect agents
        sender_ctrl.model.add_output(contract.receiver_id)
        receiver_ctrl.model.add_input(contract.sender_id)

        self.contract_added.emit(sender_ctrl, receiver_ctrl, contract)

    def create_new_scenario(self):
        # don't call this function when a scenario already exists to avoid accidental loss of data
        assert not self.has_scenario_data

        self._scenario = models.Scenario()
        self.has_scenario_data_changed.emit(True)

    def load_file(self, file_path):
        logging.debug(
            "initializing new scenario from file {}".format(file_path))
        self.reset()

        self._scenario = models.ScenarioLoader.load_yaml_file(file_path)
        self._set_file_path(file_path)

        for a in self._scenario.agents.values():
            self._add_agent_model(a)
        for c in self._scenario.contracts:
            self._add_contract_model(c)

        self.has_scenario_data_changed.emit(True)

    def save_to_file(self, file_path):
        assert self.has_scenario_data
        logging.debug("saving scenario data to file {}".format(file_path))
        models.ScenarioLoader.save_to_yaml_file(
            self._scenario, file_path)
        # update status
        self._set_has_unsaved_changes(False)
        self._set_file_path(file_path)
