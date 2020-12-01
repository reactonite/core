import json
import os

from .Helpers import create_file, write_to_json_file


class Config:
    """A Class to manage and maintain project configuration.
    One can add/remove/modify config variables and save/load
    it easily

    Attributes
    ----------
    config_path : str
        Path to configuration file from where to load/save
    config : dict
        Config settings dictionary

    Parameters
    ----------
    config_path : str
        Path to configuration file from where to load/save
    load : bool
        Whether to load config on object creation, default is False
    """

    def __init__(self, config_path, load=False):
        self.config_path = config_path
        self.config = dict()

        if load:
            self.load_config()

    def add_to_config(self, config_name, config_value):
        """Adds/updates a variable to the config
        """
        self.config[config_name] = config_value

    def get_config(self):
        """Returns the configuration as a dictionary
        """
        return self.config

    def get(self, key):
        """Gets a config variable
        """
        return self.config.get(key)

    def save_config(self):
        """Saves the configuration to the config_path
        in JSoN format. It first creates the file if it
        doesn't exist, then writes into it.
        """
        if not os.path.isfile(self.config_path):
            create_file(self.config_path)
        write_to_json_file(self.config_path,
                           self.config)

    def load_config(self):
        """Loads the configuration from the config_path.

        Raises
        ------
        FileNotFoundError
            Raised if config file not found at the config_path
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                "Reactonite config.json file doesn't exist, can't proceed."
            )

        with open(self.config_path) as infile:
            config_settings = json.load(infile)

        self.config = config_settings

    def __str__(self):
        """Pretty prints the config variables.
        """
        return_str = ""
        for key in self.config:
            return_str += "{}: {}\n".format(key, self.config[key])
        return return_str
