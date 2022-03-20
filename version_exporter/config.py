"""
Configuration file operation
"""
import logging
from pathlib import Path

import yaml
from cerberus import Validator


def read_config(path: Path) -> dict:
    """Read yaml config file

    Args:
        path (Path): path to config file on the system

    Returns:
        dict: config file content
    """
    config = {}
    with open(path, "r", encoding="utf8") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    schema = {"rpm": {"type": "list", "schema": {"type": "string"}}}
    validator = Validator(schema)

    if validator.validate(config):
        logging.info("Config loaded")
    else:
        logging.error("Invalid config loaded: %s", validator.errors)
        raise Exception("Invalid config")

    return config
