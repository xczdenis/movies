COMMAND_PREFIX_DEV=dev
COMMAND_PREFIX_PROD=prod
COMMAND_PREFIX_CHECK=check
COMMAND_PREFIX_STOP=stop
COMMAND_PREFIX_DOWN=down

DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml

COMPOSE_OPTION_START_AS_DEMON=up -d --build


define run_docker_compose
	(docker-compose -f $(1) $(2) $(3))
endef


$(COMMAND_PREFIX_DEV):
	$(call run_docker_compose,$(DOCKER_COMPOSE_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(COMMAND_PREFIX_DEV)-$(COMMAND_PREFIX_CHECK):
	$(call run_docker_compose,$(DOCKER_COMPOSE_DEV_FILE),config)


$(COMMAND_PREFIX_DEV)-$(COMMAND_PREFIX_STOP):
	$(call run_docker_compose,$(DOCKER_COMPOSE_DEV_FILE),stop,$(s))


$(COMMAND_PREFIX_DEV)-$(COMMAND_PREFIX_DOWN):
	$(call run_docker_compose,$(DOCKER_COMPOSE_DEV_FILE),down)


sqlite-to-pg:
	python etl/src/sqlite_to_pg.py

pg-to-es:
	python etl/src/pg_to_es.py
