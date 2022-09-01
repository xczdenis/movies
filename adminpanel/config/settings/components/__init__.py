from os import environ
from pathlib import Path

from config import env_manager
from decouple import AutoConfig
from loguru import logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

path_to_env_file = ROOT_DIR / ".envs" / ".prod" / "django"

if env_manager.is_dev():
    path_to_env_file = ROOT_DIR / ".envs" / ".local" / "django"

# Loading `.env` files
# config = AutoConfig(search_path=BASE_DIR.joinpath("config"))
config = AutoConfig(search_path=path_to_env_file)

logger.debug(f"path_to_env_file = {path_to_env_file}")
logger.debug(f"BASE_DIR = {BASE_DIR}")
logger.debug(f"ROOT_DIR = {ROOT_DIR}")
logger.debug(f"ALLOWED_HOSTS_PROD = {config('ALLOWED_HOSTS_PROD')}")
logger.debug(f"ALLOWED_HOSTS_PROD = {config('ALLOWED_HOSTS_PROD')}")
logger.debug(f"DB_HOST = {config('DB_HOST')}")
logger.debug(f"DB_PORT = {config('DB_PORT')}")
