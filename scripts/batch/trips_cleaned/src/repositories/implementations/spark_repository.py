from typing import Dict, Any
from pyspark.sql import DataFrame
from infrastructures.abstractions.spark_infrastructure import ISparkInfrastructure
from repositories.abstractions.spark_repository import ISparkRepository

class SparkRepository(ISparkRepository):
    def __init__(self, spark_infrastructure: ISparkInfrastructure):
        self.spark_infrastructure = spark_infrastructure

    def read_csv(self, 
            file_path: str,
            header: bool,
            inferSchema: bool) -> DataFrame:
        spark = self.spark_infrastructure.get_session()
        df: DataFrame = (
                spark.read
                    .format("csv")
                    .options(
                        header=header, 
                        inferSchema=inferSchema
                    )
                    .load(file_path))
        return df

    def write(self, 
                   df: DataFrame, 
                   file_path: str, 
                   file_format: str, 
                   partition_by: list = None,
                   mode: str = "overwrite"):
        if partition_by:
            df.write.format(file_format).mode(mode).partitionBy(*partition_by).save(file_path)
        else:
            df.write.format(file_format).mode(mode).save(file_path)
