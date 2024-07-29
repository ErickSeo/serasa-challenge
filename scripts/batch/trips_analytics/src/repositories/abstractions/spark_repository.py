from abc import ABC, abstractmethod
from typing import Dict, Any
from pyspark.sql import DataFrame

class ISparkRepository(ABC):
    @abstractmethod
    def read_csv(self, 
            file_path: str,
            header: bool,
            inferSchema: bool) -> DataFrame:
        raise NotImplementedError()
    
    @abstractmethod
    def read_parquet(self,file_path: str) -> DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def write(self, 
                   df: DataFrame, 
                   file_path: str, 
                   file_format: str, 
                   partition_by: list = None,
                   mode: str = "overwrite"):
        raise NotImplementedError()