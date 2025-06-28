from .read_yaml import YamlConfigReader
from .read_json import JsonConfigReader

class ConfigReaderInstance:
    json = JsonConfigReader()
    yaml = YamlConfigReader()