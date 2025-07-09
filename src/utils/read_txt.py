
class TextConfigReader:
    def read_config_from_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
 



