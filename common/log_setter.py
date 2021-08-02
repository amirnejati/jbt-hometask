import logging.config
import os.path

import yaml

from config import BASE_DIR


def load_logging_configuration() -> None:
    log_conf_file = os.path.join(BASE_DIR, 'logging.yaml')

    with open(log_conf_file) as stream:
        logging_dict_config = yaml.safe_load(stream)

    logging.config.dictConfig(logging_dict_config)
