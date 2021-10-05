.DEFAULT_GOAL := help
.PHONY: coverage deps help lint publish push test tox requirements venv

VER=$(shell git log --pretty=format:'%h' -n 1)

venv: ## Makes new virtual venv and loads all dependencies
	python -m venv env
	. env/bin/activate
	$(MAKE) deps

coverage:  ## Run tests with coverage
	python -m coverage erase
	python -m coverage run --include=loudify/* -m pytest -ra
	python -m coverage report -m

deps:  ## Install dependencies
	pip install -r requirements.txt

lint:  ## Lint and static-check
	python -m flake8 loudify
	python -m pylint loudify
	python -m mypy loudify
\
publish:  ## Publish to PyPi
	flit publish

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests
	python -m pytest -ra

launch_stack:
	ADMIN_USER=admin \
	ADMIN_PASSWORD=admin \
	SLACK_URL=https://hooks.slack.com/services/TOKEN \
	SLACK_CHANNEL=devops-alerts \
	SLACK_USER=alertmanager \
	docker stack deploy -c docker-compose.yml mon

requirements:	## Update requirements.txt
	python -m pip freeze > requirements.txt

tox:   ## Run tox
	tox

build_image: ##Build docker image
	docker build -t martynvandijke/loudify-broker:dev .
	docker push martynvandijke/loudify-broker:dev

help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done
