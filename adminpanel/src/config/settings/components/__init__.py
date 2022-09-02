from pathlib import Path

from config import env_manager
from decouple import AutoConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent.parent

path_to_env_file = ROOT_DIR / ".envs" / env_manager.get_env()

# Loading `.env` files
config = AutoConfig(search_path=path_to_env_file)
