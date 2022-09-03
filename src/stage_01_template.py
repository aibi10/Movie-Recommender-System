import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
import opendatasets as od

STAGE = "STAGE_NAME"

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
)


def main(config_path):
    config = read_yaml(config_path)
    local_dir = config['data']['local_dir']
    try:
        logging.info("data directory is about to be created")
        create_directories(local_dir)
        logging.info("data directory is created successfully")

    except Exception as e:
        logging.exception(e)

    URL = config['data']['URL']

    try:
        logging.info("file is being downloaded")
        od.download(URL, local_dir)
        logging.info("file is downloaded")

    except Exception as e:
        logging.info("there is some problem while downloading the file")
        logging.info(e)


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
