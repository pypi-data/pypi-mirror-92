import os
from pathlib import Path

import yaml


def get_config_path():
    return os.path.join(Path.home(), '.seasecurity', 'sec', 'config.yml')


def read_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except:
        return None


def write_config(config):
    config_path = get_config_path()
    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path))
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def nested_get(dic, keys):
    v = dic
    for key in keys:
        if key not in v:
            return None
        v = v.get(key, None)
    return v
