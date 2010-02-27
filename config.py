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
            # 0 - name
            # 1 - url
            # 2 - template_name
            config_value_list = self._remove_comments(line.strip().split())
            
            if len(config_value_list) > 1:
                name = config_value_list[0]
                url = config_value_list[1]
                try:
                    template_name = config_value_list[2]
                except IndexError:
                    template_name = None
                    
                self.config_dict[name] = ConfigValue(url=url, template=template_name)
    
    
    def _remove_comments(self, config_value_list, delimiter='#'):
        """
        Removes line comments from the config_value_list
        
        config_value_list - a string split by spaces
        delimiter - the delimiter to check for. Defaults to '#'

        returns - new line with comments removed
        """
        new_config_value_list = []
        for value in config_value_list:
            
            if delimiter == value[0]:
                return new_config_value_list
            
            new_config_value_list.append(value)

        return new_config_value_list
            
    def __getitem__(self, key):
        return self.config_dict[key]
