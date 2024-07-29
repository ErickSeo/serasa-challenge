class SparkInfrastructureBuildException(Exception):
    """Exceção personalizada para erros na infraestrutura do Spark."""
    def __init__(self):
        super().__init__("Spark session has not been built yet. Call build_session() first.")
