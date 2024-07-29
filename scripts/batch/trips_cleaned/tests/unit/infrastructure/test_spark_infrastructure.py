import unittest
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
from infrastructures.abstractions.spark_infrastructure import ISparkInfrastructure
from exception.spark_exception import SparkInfrastructureBuildException
from infrastructures.implementations.spark_infrastructure import SparkInfrastructure

class TestSparkInfrastructure(unittest.TestCase):

    @patch('pyspark.sql.SparkSession.builder')
    def test_build_session(self, mock_builder):
        mock_spark = MagicMock(SparkSession)
        mock_app_name = mock_builder.appName.return_value
        mock_app_name.getOrCreate.return_value = mock_spark

        spark_infra = SparkInfrastructure()
        spark_infra.build_session("TestApp")

        self.assertIsNotNone(spark_infra.spark)
        mock_builder.appName.assert_called_once_with("TestApp")
        mock_app_name.getOrCreate.assert_called_once()

    def test_stop_session(self):
        spark_infra = SparkInfrastructure()
        spark_infra.spark = MagicMock(SparkSession)

        spark_infra.stop_session()

        self.assertIsNone(spark_infra.spark)

    def test_get_session(self):
        spark_infra = SparkInfrastructure()
        spark_infra.spark = MagicMock(SparkSession)

        session = spark_infra.get_session()

        self.assertIsNotNone(session)

    def test_get_session_without_build(self):
        spark_infra = SparkInfrastructure()

        with self.assertRaises(SparkInfrastructureBuildException):
            spark_infra.get_session()

    @patch('pyspark.sql.SparkSession.builder')
    def test_add_config(self, mock_builder):
        mock_spark = MagicMock(SparkSession)
        mock_app_name = mock_builder.appName.return_value
        mock_app_name.getOrCreate.return_value = mock_spark

        spark_infra = SparkInfrastructure()
        spark_infra.build_session("TestApp")
        spark_infra.add_config("spark.some.config", "value")

        mock_spark.conf.set.assert_called_once_with("spark.some.config", "value")

    @patch('pyspark.sql.SparkSession.builder')
    def test_apply_spark_config(self, mock_builder):
        mock_spark = MagicMock(SparkSession)
        mock_app_name = mock_builder.appName.return_value
        mock_app_name.getOrCreate.return_value = mock_spark

        spark_infra = SparkInfrastructure()
        spark_infra.build_session("TestApp")

        config = {
            'spark': {
                'fs.s3a.access.key': 'minioadmin',
                'fs.s3a.secret.key': 'minioadmin',
                'fs.s3a.endpoint': 'http://minio-service.minio.svc.cluster.local:9000'
            }
        }
        spark_infra.apply_spark_config(config)

        mock_spark.conf.set.assert_any_call('fs.s3a.access.key', 'minioadmin')
        mock_spark.conf.set.assert_any_call('fs.s3a.secret.key', 'minioadmin')
        mock_spark.conf.set.assert_any_call('fs.s3a.endpoint', 'http://minio-service.minio.svc.cluster.local:9000')

if __name__ == '__main__':
    unittest.main()
