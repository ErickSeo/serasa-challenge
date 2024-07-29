from pyspark.sql import DataFrame
from pyspark.sql.functions import year, month, dayofmonth
from repositories import ISparkRepository
from handler.abstractions.trips_handler import ITripsHandler

class TripsHandler(ITripsHandler):
    def __init__(self,
                 spark_repository: ISparkRepository): 
        self._spark_repository: ISparkRepository = spark_repository

    def _read_csv(self, s3_path: str) -> DataFrame:
        df: DataFrame = self._spark_repository.read_csv(
                    file_path=s3_path, 
                    header=True,
                    inferSchema=True
                )
        return df
    
    def _process(self, df: DataFrame) -> DataFrame:
        _df: DataFrame = df.withColumn("pickup_datetime", df["pickup_datetime"].cast("timestamp"))
        _df: DataFrame = (_df
                          .withColumn("year", year(_df["pickup_datetime"]))
                          .withColumn("month", month(_df["pickup_datetime"]))
                          .withColumn("day", dayofmonth(_df["pickup_datetime"]))
        )
        return _df
    
    def _save(self, 
              df: DataFrame,
              file_path: str,):
        self._spark_repository.write(
            df=df,
            file_path=file_path,
            file_format="parquet",
            partition_by=["year", "month", "day"],
            mode="overwrite"
        )
    

    def pipeline(self):
        input_path: str = f"s3a://raw/ny_trips/train.csv"
        output_path: str = f"s3a://cleaned/ny_trips"
        df_users = self._read_csv(s3_path=input_path)
        df_users = self._process(df_users)
        self._save(df=df_users, file_path=output_path)
        


        

        
    