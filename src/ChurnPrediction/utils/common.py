## utils directoty mainly contains the functionality which is commnly implemented in the rest of project

import os
from box.exceptions import BoxValueError
import yaml
from ChurnPrediction import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

"""

This file contains the utility functions which are commnly implemented in the rest of project.
Here ConfigBox is used to have easy access to the keys and values inside the dictionary that has been returned.
ensure_annotations is used to check if the parameters and the return values are having exact datatypes or not.

"""

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read a yaml file and return a ConfigBox object.
    Args:  
        path_to_yaml(str): Path like input
    Raises:
        ValueError: if yaml file empty
        e: empty yaml file
    returns: 
        ConfigBox object
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directory(path_to_directories: list, verbose = True):
    """
    Create a list of directories.
    Args:
        path_to_directories(list): list of paths of directories to create
        ignore_log(bool, optional): ignore if multiple dirs to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(Path(path), exist_ok=True)
        if verbose:
            logger.info(f"directory: {path} created successfully")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    save json data
    Args:
        path(Path): path to json file
        data(dict): data to be saved in json file
    """
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent = 4)
        logger.info(f"json file: {path} saved successfully")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    load json data
    Args:
        path(Path): path to json file
    Returns:
        ConfigBox: data as class attribute instead of dictionary
    """
    with open(path) as json_file:
        data = json.load(json_file)
    logger.info(f"json file: {path} loaded successfully")
    return ConfigBox(data)


@ensure_annotations
def get_size(path: Path) -> str:
    """
    get the size of a file
    Args:
        path(Path): path to file
    Returns:
        str: size of the file
    """

    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"