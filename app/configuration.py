import json
import os


def load_json_file(file_path):
    try:
        with open(file_path) as config:
            file_json = json.load(config)
    except FileNotFoundError:
        try:
            with open(os.path.join(BASE_DIR, file_path)) as config:
                file_json = json.load(config)
        except Exception:
            raise

    return file_json


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

SECRET_CONFIG_STORE = load_json_file("secrets.json")
CONFIG_STORE = load_json_file("configuration.json")


class Config:
    # General
    APPLICATION_NAME = 'Jeedom_WS'
    BASE_DIR = BASE_DIR

    # If in docker compose env, use env variables instead of config files
    # Config
    URL = os.getenv('URL', CONFIG_STORE["url"])
    INFO = os.getenv('INFO', CONFIG_STORE["info"])

    TOPICS_PATH = os.path.join(BASE_DIR, os.getenv('TOPICS_PATH', CONFIG_STORE["topics_path"]))
    STATES_PATH = os.path.join(BASE_DIR, os.getenv('STATES_PATH', CONFIG_STORE["states_path"]))
    DEVICES_PATH = os.path.join(BASE_DIR, os.getenv('DEVICES_PATH', CONFIG_STORE["devices_path"]))
    PING_WS_CLIENTS_INTERVAL = int(os.getenv('PING_WS_CLIENTS_INTERVAL', CONFIG_STORE["ping_ws_clients_interval"]))
    ENABLE_EXTRA_PING_INFO = int(os.getenv('ENABLE_EXTRA_PING_INFO', CONFIG_STORE["enable_extra_ping_info"]))
    PRIORITY_DEBUG_LEVEL = int(os.getenv('PRIORITY_DEBUG_LEVEL', CONFIG_STORE["priority_debug_level"]))

    # Secrets config
    WS_URI = os.getenv('WS_URI', SECRET_CONFIG_STORE["ws_uri"])
    USERNAME = os.getenv('FLOKERR_USERNAME', SECRET_CONFIG_STORE["flokerr_username"])
    PASSWORD = os.getenv('FLOKERR_PASSWORD', SECRET_CONFIG_STORE["flokerr_password"])


class Configuration(dict):
    def from_object(self, obj):
        for attr in dir(obj):

            if not attr.isupper():
                continue

            self[attr] = getattr(obj, attr)

        self.__dict__ = self


APP_CONFIG = Configuration()
APP_CONFIG.from_object(Config)
