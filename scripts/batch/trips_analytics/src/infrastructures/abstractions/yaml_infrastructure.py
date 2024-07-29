from abc import ABC, abstractmethod

class IYamlConfigReader(ABC):
    @abstractmethod
    def get_config(self) -> dict:
        raise NotImplementedError()