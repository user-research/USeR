import os
from configparser import ConfigParser
config = ConfigParser()

def load_config():
    """
    Config wrapper to switch environments
    """
    # Load app config
    if os.getenv('ENV') == 'DEFAULT':
        config.read("./config/user/default.cfg")
    elif os.getenv('ENV') == 'TEST':
        config.read("./config/user/tests.cfg")
    else:
        config.read("./config/user/default.cfg")

load_config()