PROJECT_NAME=movies

ENV_DEV=dev
ENV_TEST=test
ENV_PROD=prod

TARGET_PREFIX_DEV=dev
TARGET_PREFIX_PROD=prod
TARGET_PREFIX_TEST=test
TARGET_PREFIX_CHECK=check
TARGET_PREFIX_STOP=stop
TARGET_PREFIX_DOWN=down

RUN_DEV=$(TARGET_PREFIX_DEV)
RUN_DEV_CHECK=$(TARGET_PREFIX_DEV)-$(TARGET_PREFIX_CHECK)
RUN_DEV_STOP=$(TARGET_PREFIX_DEV)-$(TARGET_PREFIX_STOP)
RUN_DEV_DOWN=$(TARGET_PREFIX_DEV)-$(TARGET_PREFIX_DOWN)

RUN_TEST=$(TARGET_PREFIX_TEST)
RUN_TEST_CHECK=$(TARGET_PREFIX_TEST)-$(TARGET_PREFIX_CHECK)
RUN_TEST_STOP=$(TARGET_PREFIX_TEST)-$(TARGET_PREFIX_STOP)
RUN_TEST_DOWN=$(TARGET_PREFIX_TEST)-$(TARGET_PREFIX_DOWN)

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


define create_file
	@touch $(1)
endef


define write_to_file
	@echo $(2) >> $(1)
endef


#############
# ETL
#############
sqlite-to-pg:
	python etl/src/sqlite_to_pg.py

pg-to-es:
	python etl/src/pg_to_es.py


#############
# DEV
#############
$(RUN_DEV): $(RUN_DEV_DOWN) $(RUN_TEST_DOWN)
	$(call log,Run containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_DEV_CHECK):
	$(call log,Check configuration (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),config)


$(RUN_DEV_STOP):
	$(call log,Stop running containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),stop,$(s))


$(RUN_DEV_DOWN):
	$(call log,Down running containers (DEV))
	$(call run_docker_compose,$(ENV_DEV),$(DOCKER_COMPOSE_DEV_FILE),down)


#############
# TEST
#############
$(RUN_TEST): $(RUN_TEST_DOWN) $(RUN_DEV_DOWN)
	$(call log,Run containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_TEST_CHECK):
	$(call log,Check configuration (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),config)


$(RUN_TEST_STOP):
	$(call log,Stop running containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),stop,$(s))


$(RUN_TEST_DOWN):
	$(call log,Down running containers (TEST))
	$(call run_docker_compose,$(ENV_TEST),$(DOCKER_COMPOSE_TEST_FILE),down)


#############
# CI/CD
#############
gha-make-env-file-dev:
	$(call create_file,.env-tmp)
	$(call write_to_file,.env-tmp,${{ secrets.ENVS-DEV }})
	@sed '/=\</!d;s/=/=/' .env-tmp > .envs/development/.env


ci-test-build:
	$(call run_docker_compose,'test',$(DOCKER_COMPOSE_TEST_FILE),build)


ci-run-test-search:
	$(call run_docker_compose,'test',$(DOCKER_COMPOSE_TEST_FILE),run tests_search)
