PROJECT_NAME=movies1

ENV_DEV=dev
ENV_TEST=test
ENV_PROD=prod

COMMAND_PREFIX_DEV=dev
COMMAND_PREFIX_PROD=prod
COMMAND_PREFIX_TEST=test
COMMAND_PREFIX_CHECK=check
COMMAND_PREFIX_STOP=stop
COMMAND_PREFIX_DOWN=down

DOCKER_COMPOSE_MAIN_FILE=docker-compose.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_TEST_FILE=docker-compose.test.yml

COMPOSE_OPTION_START_AS_DEMON=up -d --build


# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell printf "\033[30m")
	RED          := $(shell printf "\033[91m")
	GREEN        := $(shell printf "\033[92m")
	YELLOW       := $(shell printf "\033[33m")
	BLUE         := $(shell printf "\033[94m")
	PURPLE       := $(shell printf "\033[95m")
	ORANGE       := $(shell printf "\033[93m")
	WHITE        := $(shell printf "\033[97m")
	RESET        := $(shell printf "\033[00m")
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	BLUE         := ""
	PURPLE       := ""
	ORANGE       := ""
	WHITE        := ""
	RESET        := ""
endif


# read env variables from .env
ifneq (,$(wildcard ./.env))
	include .env
	export
endif


# set COMPOSE_PROJECT_NAME if it is not defined
ifeq ($(COMPOSE_PROJECT_NAME),)
	COMPOSE_PROJECT_NAME=$(PROJECT_NAME)
endif


define run_docker_compose
	COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME)-$(1) docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(2) $(3) $(4)
endef


define log
	@echo ""
	@echo "${WHITE}----------------------------------------${RESET}"
	@echo "${BLUE}$(1)${RESET}"
	@echo "${WHITE}----------------------------------------${RESET}"
endef


#############
# DEV
#############
$(COMMAND_PREFIX_DEV):
	$(call log,Down containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),down)

	$(call log,Down containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),down)

	$(call log,Run containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(COMMAND_PREFIX_DEV)-$(COMMAND_PREFIX_CHECK):
	$(call log,Check configuration (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),config)


$(COMMAND_PREFIX_DEV)-$(COMMAND_PREFIX_STOP):
	$(call log,Stop running containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),stop,$(s))


$(COMMAND_PREFIX_DEV)-$(COMMAND_PREFIX_DOWN):
	$(call log,Down running containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),down)


#############
# TEST
#############
$(COMMAND_PREFIX_TEST):
	$(call log,Down containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_TEST_FILE),down)

	$(call log,Down containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),down)

	$(call log,Run containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(COMMAND_PREFIX_TEST)-$(COMMAND_PREFIX_CHECK):
	$(call log,Check configuration (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),config)


$(COMMAND_PREFIX_TEST)-$(COMMAND_PREFIX_STOP):
	$(call log,Stop running containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),stop,$(s))


$(COMMAND_PREFIX_TEST)-$(COMMAND_PREFIX_DOWN):
	$(call log,Down running containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),down)


sqlite-to-pg:
	python etl/src/sqlite_to_pg.py

pg-to-es:
	python etl/src/pg_to_es.py
