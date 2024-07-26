.PHONY: airflow spark kafka minio up clean

build-airflow:
	docker build -t seoerick/airflow:2.7.1 ./infrastructure/images/airflow
	docker tag seoerick/airflow:2.7.1 seoerick/airflow:2.7.1
	docker push seoerick/airflow:2.7.1

arch-init: 
	terraform -chdir=./infrastructure/kubernetes/local init

arch-plan: 
	terraform -chdir=./infrastructure/kubernetes/local plan

arch-apply: 
	terraform -chdir=./infrastructure/kubernetes/local apply -auto-approve

arch-destroy: 
	terraform -chdir=./infrastructure/kubernetes/local destroy -auto-approve