FROM spark:3.5.0

COPY src /app/
COPY requirements/requirements-dev.txt /app/
ENV ACCESS_KEY=minioadmin
ENV SECRET_KEY=minioadmin
ENV S3_ENDPOINT="http://minio-service.minio.svc.cluster.local:9000"

WORKDIR /app

ADD https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.0.0/delta-spark_2.12-3.0.0.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/io/delta/delta-storage/3.0.0/delta-storage-3.0.0.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.1/hadoop-common-3.3.1.jar /opt/spark/jars/

USER root


RUN pip install --no-cache-dir -r requirements-dev.txt

# Alterando permissões dos JARs
RUN chown -R 185:185 /opt/spark/jars

USER 185