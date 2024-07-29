import yaml
from infrastructures.abstractions.yaml_infrastructure import IYamlConfigReader

class YamlConfigReader(IYamlConfigReader):
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self.config = self._load_yaml()

    def _load_yaml(self) -> dict:
        with open(self.yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def get_config(self) -> dict:
        return self.config