from .read_yaml import YamlConfigReader
from .read_json import JsonConfigReader
from .read_txt import TextConfigReader

class ConfigReaderInstance:
    json = JsonConfigReader()
    yaml = YamlConfigReader()
    text = TextConfigReader()