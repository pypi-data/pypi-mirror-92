import typing

from famegui.models import Agent, Contract


class Scenario:
    def __init__(self):
        self._agents = {}
        self._contracts = []

    @property
    def agents(self) -> typing.Dict[str, Agent]:
        return self._agents

    def agent(self, id) -> Agent:
        assert(id in self._agents)
        return self._agents[id]

    def add_agent(self, a):
        if a.id in self._agents:
            otherAgentType = self._agents[a.id].type
            raise ValueError("can't add agent type '{}' because its id '{}' is already used by agent '{}'".format(
                a.type, a.id, otherAgentType))
        self._agents[a.id] = a

    @property
    def contracts(self) -> typing.List[Contract]:
        """ Returns all the contracts as a list """
        return self._contracts

    def add_contract(self, c):
        if c.sender_id not in self._agents:
            raise ValueError("can't add contract: invalid sender id '{}'".format(c.sender_id))
        if c.receiver_id not in self._agents:
            raise ValueError("can't add contract: invalid receiver id '{}'".format(c.receiver_id))

        self._contracts.append(c)
        self._agents[c.sender_id].add_output(c.receiver_id)
        self._agents[c.receiver_id].add_input(c.sender_id)
