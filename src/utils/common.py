import os
import yaml
import logging
import time
import pandas as pd
import json
from zipfile import ZipFile


def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content

# def create_directories(path_to_directories: list) -> None:
#     for path in path_to_directories:
#         os.makedirs(path, exist_ok=True)
#         logging.info(f"created directory at: {path}")


def create_directories(path_to_directories):
    os.makedirs(path_to_directories, exist_ok=True)
    logging.info(f"created directory at: {path_to_directories}")


def save_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")


def unzip_file(source: str, dest: str) -> None:
    logging.info(f"extraction started...")

    with ZipFile(source, "r") as zip_f:
        zip_f.extractall(dest)
    logging.info(f"extracted {source} to {dest}")
