PROJECT_NAME=movies

PREFIX_DEV=dev
PREFIX_TEST=test
PREFIX_PROD=prod

PREFIX_CHECK=check
PREFIX_STOP=stop
PREFIX_DOWN=down

RUN_PROD=$(PREFIX_PROD)
RUN_PROD_CHECK=$(PREFIX_PROD)-$(PREFIX_CHECK)
RUN_PROD_STOP=$(PREFIX_PROD)-$(PREFIX_STOP)
RUN_PROD_DOWN=$(PREFIX_PROD)-$(PREFIX_DOWN)

RUN_DEV=$(PREFIX_DEV)
RUN_DEV_CHECK=$(PREFIX_DEV)-$(PREFIX_CHECK)
RUN_DEV_STOP=$(PREFIX_DEV)-$(PREFIX_STOP)
RUN_DEV_DOWN=$(PREFIX_DEV)-$(PREFIX_DOWN)

RUN_TEST=$(PREFIX_TEST)
RUN_TEST_CHECK=$(PREFIX_TEST)-$(PREFIX_CHECK)
RUN_TEST_STOP=$(PREFIX_TEST)-$(PREFIX_STOP)
RUN_TEST_DOWN=$(PREFIX_TEST)-$(PREFIX_DOWN)

DOCKER_COMPOSE_MAIN_FILE=docker-compose.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_TEST_FILE=docker-compose.test.yml
DOCKER_COMPOSE_TEST_DEV_FILE=docker-compose.test.dev.yml

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


down: $(RUN_PROD_DOWN) $(RUN_DEV_DOWN) $(RUN_TEST_DOWN)
	$(call log,Down containers $(COMPOSE_PROJECT_NAME))
	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(DOCKER_COMPOSE_PROD_FILE) down
	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(DOCKER_COMPOSE_DEV_FILE) down
	docker-compose -f $(DOCKER_COMPOSE_MAIN_FILE) -f $(DOCKER_COMPOSE_TEST_FILE) down


#############
# ETL
#############
sqlite-to-pg:
	python etl/src/sqlite_to_pg.py

pg-to-es:
	python etl/src/pg_to_es.py


#############
# PROD
#############
$(RUN_PROD): down
	$(call log,Run containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_PROD_CHECK):
	$(call log,Check configuration (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),config)


$(RUN_PROD_STOP):
	$(call log,Stop running containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),stop,$(s))


$(RUN_PROD_DOWN):
	$(call log,Down running containers (PROD))
	ENVIRONMENT=production $(call run_docker_compose,$(PREFIX_PROD),$(DOCKER_COMPOSE_PROD_FILE),down)


#############
# DEV
#############
$(RUN_DEV): down
	$(call log,Run containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_DEV_CHECK):
	$(call log,Check configuration (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),config)


$(RUN_DEV_STOP):
	$(call log,Stop running containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),stop,$(s))


$(RUN_DEV_DOWN):
	$(call log,Down running containers (DEV))
	$(call run_docker_compose,$(PREFIX_DEV),$(DOCKER_COMPOSE_DEV_FILE),down)


#############
# TEST
#############
$(RUN_TEST): down
	$(call log,Run containers (TEST))
	$(call run_docker_compose,$(PREFIX_TEST),$(DOCKER_COMPOSE_TEST_FILE) -f $(DOCKER_COMPOSE_TEST_DEV_FILE),$(COMPOSE_OPTION_START_AS_DEMON),$(s))


$(RUN_TEST)-it: down
	$(call log,Build test containers)
	$(call run_docker_compose,$(PREFIX_TEST),$(DOCKER_COMPOSE_TEST_FILE) -f $(DOCKER_COMPOSE_TEST_DEV_FILE),build)

	$(call log,Run tests for service search)
	$(call run_docker_compose,$(PREFIX_TEST),$(DOCKER_COMPOSE_TEST_FILE) -f $(DOCKER_COMPOSE_TEST_DEV_FILE),run,tests_search)


$(RUN_TEST_CHECK):
	$(call log,Check configuration (TEST))
	$(call run_docker_compose,$(PREFIX_TEST),$(DOCKER_COMPOSE_TEST_FILE) -f $(DOCKER_COMPOSE_TEST_DEV_FILE),config)


$(RUN_TEST_STOP):
	$(call log,Stop running containers (TEST))
	$(call run_docker_compose,$(PREFIX_TEST),$(DOCKER_COMPOSE_TEST_FILE),stop,$(s))


$(RUN_TEST_DOWN):
	$(call log,Down running containers (TEST))
	$(call run_docker_compose,$(PREFIX_TEST),$(DOCKER_COMPOSE_TEST_FILE),down)


#############
# CI/CD
#############
gha-make-env-file-dev:
	$(call create_file,.env-tmp)
	$(call write_to_file,.env-tmp,${{ secrets.ENVS_DEV }})
	@sed '/=\</!d;s/=/=/' .env-tmp > .envs/development/.env


gha-make-env-file-prod:
	$(call create_file,.env-tmp)
	$(call write_to_file,.env-tmp,${{ secrets.ENVS_PROD }})
	@sed '/=\</!d;s/=/=/' .env-tmp > .envs/production/.env


ci-tests-build:
	@ENVIRONMENT=production $(call run_docker_compose,test,$(DOCKER_COMPOSE_TEST_FILE),build)


ci-run-tests:
	@$(call run_docker_compose,test,$(DOCKER_COMPOSE_TEST_FILE),run,$(s))
