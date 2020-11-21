import os
import json

from .Helpers import write_to_json_file, create_file


class Config:

    def __init__(self, config_path, load=False):
        self.config_path = config_path
        self.config = dict()

        if load:
            self.load_config()

    def add_to_config(self, config_name, config_value):
        self.config[config_name] = config_value

    def get_config(self):
        return self.config

    def get(self, key):
        return self.config.get(key)

    def save_config(self):
        if not os.path.isfile(self.config_path):
            create_file(self.config_path)
        write_to_json_file(self.config_path,
                           self.config)

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                "Reactonite config.json file doesn't exist, can't proceed."
            )

        with open(self.config_path) as infile:
            config_settings = json.load(infile)

        self.config = config_settings

    def __str__(self):
        return_str = ""
        for key in self.config:
            return_str += "{}: {}\n".format(key, self.config[key])
        return return_str
