from repositories import ISparkRepository, SparkRepository
from infrastructures import (
    ISparkInfrastructure, 
    SparkInfrastructure,
    IYamlConfigReader,
    YamlConfigReader)
from handler import ITripsHandler, TripsHandler

def main():
    spark_configuration = "configurations/spark_configurations.yaml"
    application_name = "Trip Cleaned"
    spark_infrastructure: ISparkInfrastructure = SparkInfrastructure()
    yaml_config: IYamlConfigReader = YamlConfigReader(yaml_path=spark_configuration)
    spark_repository: ISparkRepository = SparkRepository(spark_infrastructure=spark_infrastructure)

    spark_configuration = yaml_config.get_config()
    spark_infrastructure.build_session(application_name=application_name)
    spark_infrastructure.apply_spark_config(config=spark_configuration)
    handler: ITripsHandler = TripsHandler(spark_repository=spark_repository)
    handler.pipeline()
    spark_infrastructure.stop_session()


if __name__ == "__main__":
    main()

