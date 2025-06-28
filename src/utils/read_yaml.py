import yaml

class YamlConfigReader:
    def read_config_from_file(self, file_path: str):
        with open(file_path, encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
 



