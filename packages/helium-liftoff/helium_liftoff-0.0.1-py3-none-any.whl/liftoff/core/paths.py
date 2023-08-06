from pathlib import Path
from os.path import dirname
from os import getcwd


PROJECT_PATH = getcwd()

PROJECT_LIFTOFF_PATH = f"{PROJECT_PATH}/.liftoff"

PROJECT_ROOT = dirname(dirname(dirname(__file__)))

ASSETS_PATH = f"{PROJECT_ROOT}/liftoff/assets"

LIFTOFF_PATH = f"{str(Path.home())}/.liftoff"

LIFTOFF_APPS_PATH = f"{LIFTOFF_PATH}/apps"

LIFTOFF_VHOSTS_PATH = f"{LIFTOFF_PATH}/vhosts"
