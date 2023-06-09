from pyhocon import ConfigFactory, ConfigTree
import os


class ConfigLoader:
    def __init__(self, config_file_path) -> None:
        """
        Load the ~/clearml.conf file as Hocon config object
        """
        if config_file_path is None:
            config_file_path = "~/clearml.conf"

        self.__config_file_path = os.path.expanduser(config_file_path)

    def load(self):
        self.__config = ConfigFactory.parse_file(self.__config_file_path)

    def get_config_value(self, key: str):
        """
        Get the value of the key from the config object
        """
        # The key could be a nested key, e.g. api.web_server
        # recursively get the value of the key

        # Get the value of the key from the config object
        config_value = self.__config.get(key)
        return config_value
