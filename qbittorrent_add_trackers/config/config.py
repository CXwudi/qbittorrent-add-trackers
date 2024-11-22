import os
from config import ConfigurationSet, config_from_env, config_from_yaml
import logging

import yaml

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    path = os.getcwd()
    logger.info(f'Loading config from {path} and env')
    cfg = ConfigurationSet(
        config_from_env(prefix='APP', lowercase_keys=True),
        config_from_yaml(os.path.join(path, 'config.yaml'), read_from_file=True, ignore_missing_paths=True),
        config_from_yaml(os.path.join(path, 'config.base.yaml'), read_from_file=True)
    )
    return cfg

