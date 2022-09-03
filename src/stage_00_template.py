import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random

STAGE = "STAGE_NAME"

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
)


def main(config_path):
    config = read_yaml(config_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n***************************")
        logging.info(f">>>>>>>>>>> stage   {STAGE}   started <<<<<<<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>>>>>> stage  {STAGE}   completed <<<<<<<<<<<")
    except Exception as e:
        logging.exception(e)
        raise e
