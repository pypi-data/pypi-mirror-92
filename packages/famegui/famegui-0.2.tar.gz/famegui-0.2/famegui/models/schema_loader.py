import logging
import os

from famegui import models
import famegui.models.yaml_utils as yaml_utils


def _extract_field_type(agent_type_name, field_name, details):
    try:
        field_type = yaml_utils.must_get_str_key(details, "FieldType")
        # optional fields
        is_mandatory = details.get("Mandatory")
        enum_values = details.get("Values")
        return models.AgentFieldType(field_type, is_mandatory, enum_values)
    except Exception as e:
        raise ValueError(
            "failed to load field type '{}' in agent type '{}'".format(field_name, agent_type_name)) from e


class SchemaLoader:
    """ Class to load and parse schema files """
    @staticmethod
    def load_yaml_file(file_path):
        file_path = os.path.abspath(file_path)
        yaml_dict = yaml_utils.load_file(file_path)

        # load agents
        if yaml_dict is None or not "AgentTypes" in yaml_dict:
            raise ValueError(
                "invalid yaml file: at least one agent type must be defined in the node 'AgentTypes'")

        result = []
        for agent_type, fields in yaml_dict.get("AgentTypes").items():
            # we accept agent types that have no field defined
            if fields is None:
                logging.warning(
                    "no field defined for agent type '{}'".format(agent_type))
            else:
                for field_name, details in fields.items():
                    result.append(_extract_field_type(
                        agent_type, field_name, details))
                    logging.info("loaded field type {}.{}".format(
                        agent_type, field_name))
        return result
