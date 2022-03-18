"""
Configuration file operation
"""
from pathlib import Path
import yaml


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

    return config
