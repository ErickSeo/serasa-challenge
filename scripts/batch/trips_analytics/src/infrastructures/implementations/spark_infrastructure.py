import os
from typing import Dict, Any
from pyspark.sql import SparkSession
from infrastructures.abstractions.spark_infrastructure import ISparkInfrastructure
from exception.spark_exception import SparkInfrastructureBuildException
from threading import Lock

class SparkInfrastructure(ISparkInfrastructure):
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SparkInfrastructure, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.spark = None

    def build_session(self, application_name: str):
        if self.spark is None:
            self.spark = SparkSession.builder.appName(application_name).getOrCreate()

    def stop_session(self):
        if self.spark is not None:
            self.spark.stop()
            self.spark = None

    def get_session(self) -> SparkSession:
        if self.spark is None:
            raise SparkInfrastructureBuildException()
        return self.spark

    def add_config(self, key: str, value: str):
        if self.spark is None:
            raise SparkInfrastructureBuildException()
        self.spark.conf.set(key, value)
    
    def apply_spark_config(self, config: Dict[str, Any]):
        for key, value in config['spark'].items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                value = os.getenv(env_var)
            self.add_config(key, value)