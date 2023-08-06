import yaml

from sec.function.cli import FunctionCli
from sec.util import read_config, nested_set, write_config, get_config_path, nested_get


class CLI:
    def __init__(self):
        self.config = ConfigCli
        self.function = FunctionCli


class ConfigCli:
    def path(self):
        return get_config_path()

    def set(self, key, value):
        config = read_config()
        if config is None:
            config = {}
        keys = key.split('.')
        nested_set(config, keys, value)
        write_config(config)

    def get(self, key):
        config = read_config()
        if config is None:
            return None
        keys = key.split('.')
        return nested_get(config, keys)

    def list(self):
        config = read_config()
        if config:
            print(yaml.safe_dump(config))
