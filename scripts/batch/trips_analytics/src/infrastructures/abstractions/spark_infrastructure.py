from abc import ABC, abstractmethod
from pyspark.sql import SparkSession

class ISparkInfrastructure(ABC):
    @abstractmethod
    def build_session(self, application_name: str):
        raise NotImplementedError()

    @abstractmethod
    def stop_session(self):
        raise NotImplementedError()

    @abstractmethod
    def get_session(self) -> SparkSession:
        raise NotImplementedError()

    @abstractmethod
    def add_config(self, key: str, value: str):
        raise NotImplementedError()