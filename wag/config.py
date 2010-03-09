"""A class that parser the config"""
import ConfigParser

class NameNotInConfig(Exception):
    pass

class ConfigValue(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

class WagConfig(object):
    def __init__(self, config_filename):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_filename)
    
    def __getitem__(self, key):
        config_value_dict = {}
        try:
            config_value_dict = dict(self.config.items(key))
        except ConfigParser.NoSectionError:
            raise NameNotInConfig
        return ConfigValue(**config_value_dict)

    def get_names(self):
        return self.config.sections()
