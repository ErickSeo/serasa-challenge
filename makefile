.PHONY: airflow spark kafka minio up clean

airflow:
	docker-compose -f docker/docker-compose.yml up -d airflow

sqlite:
	docker-compose -f docker/docker-compose.yml up -d sqlite

up:
	docker-compose -f docker/docker-compose.yml up -d

clean:
	docker-compose -f docker/docker-compose.yml down --volumes --remove-orphans