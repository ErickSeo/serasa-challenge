from pyspark.sql import DataFrame
from pyspark.sql.functions import col, avg
from repositories import ISparkRepository
from handler.abstractions.trips_handler import ITripsHandler

class TripsHandler(ITripsHandler):
    def __init__(self,
                 spark_repository: ISparkRepository): 
        self._spark_repository: ISparkRepository = spark_repository
    
    def _process(self, df: DataFrame) -> DataFrame:
        _df: DataFrame = (df
                            .groupBy("year", "month")
                            .agg(avg(col("fare_amount")).alias("average_fare_amount"))
        )
        return _df
    
    def _save(self, 
              df: DataFrame,
              file_path: str,):
        self._spark_repository.write(
            df=df,
            file_path=file_path,
            file_format="parquet",
            partition_by=["year", "month"],
            mode="overwrite"
        )
    

    def pipeline(self):
        input_path: str = f"s3a://cleaned/ny_trips"
        output_path: str = f"s3a://analytics/ny_trips"
        df_users: DataFrame = self._spark_repository.read_parquet(
                    file_path=input_path
                )
        df_users = self._process(df_users)
        self._save(df=df_users, file_path=output_path)
        


        

        
    