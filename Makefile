tag-local=latest
tag-repo=latest
organization=brtxx
image-local=lime-website
image-repo=lime-website-dhub


build-dev:
	docker build --force-rm $(options) -t lime-website:latest .

build-prod:
	make build-dev options="--target production"

push:
	docker tag $(image-local):$(tag-local) $(organization)/$(image-repo):$(tag-repo)
	docker push $(organization)/$(image-repo):$(tag-repo)
compose-start:
	docker-compose up --remove-orphans $(options)

compose-stop:
	docker-compose down --remove-orphans $(options)

compose-manage-py:
	docker-compose run --rm $(options) website python ./lime_website/manage.py $(cmd)

start-server:
	python manage.py runserver 0.0.0.0:80
