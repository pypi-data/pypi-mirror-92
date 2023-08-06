import logging
import os

from famegui.models import Scenario, Agent, Contract, layout_agents
import famegui.models.yaml_utils as yaml_utils


def _extract_contract(contract_number, contract_dict):
    logging.debug("loading contract number {}".format(contract_number))
    try:
        sender_id = yaml_utils.must_get_int_key(contract_dict, "senderId")
        receiver_id = yaml_utils.must_get_str_key(contract_dict, "receiverId")
        product_name = yaml_utils.must_get_str_key(
            contract_dict, "productName")
        return Contract(sender_id, receiver_id, product_name)
    except Exception as e:
        raise ValueError(
            "failed to load contract number '{}'".format(contract_number)) from e


def _extract_agent(agent_number, agent_dict):
    logging.debug("loading agent number {}".format(agent_number))
    try:
        agent_id = yaml_utils.must_get_int_key(agent_dict, "Id")
        if agent_id < 0:
            raise ValueError(
                "invalid id '{}' (must be a positive integer)".format(agent_id))
        agent_type = yaml_utils.must_get_str_key(agent_dict, "Type")
        agent = Agent(agent_id, agent_type)

        # load fields
        fields_dict = agent_dict.get("Fields")
        if fields_dict is not None:
            for name, value in fields_dict.items():
                agent.add_field(name, value)

        return agent
    except Exception as e:
        raise ValueError(
            "failed to load agent number {}".format(agent_number)) from e


def _check_all_agents_have_display_coords(agents):
    for _, a in agents.items():
        if a.display.coords is None:
            return False
        return True


def _agent_to_dict(agent: Agent):
    result = {}
    result["Type"] = agent.type
    result["Id"] = agent.id
    return result


def _contract_to_dict(contract: Contract):
    result = {}
    result["senderId"] = contract.sender_id
    result["receiverId"] = contract.receiver_id
    result["productName"] = contract.product_name
    return result


class ScenarioLoader:
    @staticmethod
    def load_yaml_file(file_path: str) -> Scenario:
        """ Load (read and parse) a YAML scenario file """
        file_path = os.path.abspath(file_path)
        yaml_dict = yaml_utils.load_file(file_path)

        scenario = Scenario()

        # load agents
        if yaml_dict is None or not "Agents" in yaml_dict:
            raise ValueError(
                "invalid yaml file: at least one agent must be defined in the node 'Agents'")
        else:
            current_agent_number = 1
            for items in yaml_dict.get("Agents"):
                agent = _extract_agent(current_agent_number, items)
                scenario.add_agent(agent)
                current_agent_number += 1
            logging.info("loaded {} agent(s)".format(len(scenario.agents)))

        # load contracts
        if not "Contracts" in yaml_dict:
            logging.warning("the contract file does not define any contract")
        else:
            current_contract_number = 1
            for items in yaml_dict.get("Contracts"):
                scenario.add_contract(
                    _extract_contract(current_contract_number, items))
                current_contract_number += 1
            logging.info("loaded {} contract(s)".format(
                len(scenario.contracts)))

        # check if layout generation is necessary
        if not _check_all_agents_have_display_coords(scenario.agents):
            layout_agents(scenario)
        assert _check_all_agents_have_display_coords(scenario.agents)

        return scenario

    @staticmethod
    def save_to_yaml_file(scenario: Scenario, file_path: str):
        """ Save the given scenario to a YAML file """
        output = {}
        output["Agents"] = []
        output["Contracts"] = []
        for a in scenario.agents.values():
            output["Agents"].append(_agent_to_dict(a))
        for c in scenario.contracts:
            output["Contracts"].append(_contract_to_dict(c))

        yaml_utils.save_to_file(output, file_path)
