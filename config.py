"""A class that parser the config"""
class NoConfigError(Exception):
    pass

class ConfigValue(object):
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

class WagConfig(object):
    def __init__(self, config_filename):
        self.config_dict = {}
        try:
            f = open(config_filename)
        except IOError:
            raise NoConfigError

        for line in f:
            name, url, template_name = line.strip().split()
            self.config_dict[name] = ConfigValue(url=url, template=template_name)
            
    def __getitem__(self, key):
        return self.config_dict[key]
