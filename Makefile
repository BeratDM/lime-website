build-dev:
	docker build --force-rm $(options) -t lime-website:latest .

build-prod:
	make build-dev options="--target production"

compose-start:
	docker-compose up --remove-orphans $(options)

compose-stop:
	docker-compose down --remove-orphans $(options)

compose-manage-py:
	docker-compose run --rm $(options) website python ./lime_website/manage.py $(cmd)
