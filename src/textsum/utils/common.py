import os
import yaml
from pathlib import Path
from typing import Any, List
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from collections.abc import Sequence
from textsum.logging import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns it as a ConfigBox object."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"✅ YAML file loaded successfully: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"❌ YAML file is empty: {path_to_yaml}")
    except Exception as e:
        logger.error(f"❌ Failed to load YAML file: {path_to_yaml} due to {e}")
        raise e


@ensure_annotations
def create_directories(path_to_directories, verbose=True):
    """
    Creates directories given a list of paths.

    Args:
        path_to_directories: Iterable of directory paths
        verbose (bool, optional): Whether to log each creation. Defaults to True.
    """
    if not isinstance(path_to_directories, (list, tuple, set)):
        raise TypeError("path_to_directories must be a list, tuple, or set of paths")

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"📁 Created directory: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """Returns size of file in KB."""
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~{size_in_kb} KB"
