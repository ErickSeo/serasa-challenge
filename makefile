.PHONY: airflow spark kafka minio up clean

airflow:
	docker-compose -f docker/docker-compose.yml up -d airflow

sqlite:
	docker-compose -f docker/docker-compose.yml up -d sqlite

up:
	docker-compose -f docker/docker-compose.yml up -d --build

clean:
	docker-compose -f docker/docker-compose.yml down --volumes --remove-orphans

arch-init: 
	terraform -chdir=./infrastructure/kubernetes/local init

arch-plan: 
	terraform -chdir=./infrastructure/kubernetes/local plan

arch-apply: 
	terraform -chdir=./infrastructure/kubernetes/local apply -auto-approve

arch-destroy: 
	terraform -chdir=./infrastructure/kubernetes/local destroy -auto-approve