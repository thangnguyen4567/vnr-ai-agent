
import json

class JsonConfigReader:
    def read_config_from_file(self, file_path: str):
        with open(file_path) as file:
            config = json.load(file)
        return config
 



