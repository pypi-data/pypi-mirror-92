from pathlib import Path
from os.path import dirname
from os import getcwd


LIFTOFF_PATH = f"{str(Path.home())}/.liftoff"
LIFTOFF_APPS_PATH = f"{LIFTOFF_PATH}/apps"
LIFTOFF_VHOSTS_PATH = f"{LIFTOFF_PATH}/vhosts"

ROOT_PATH = dirname(dirname(dirname(__file__)))
ASSETS_PATH = f"{ROOT_PATH}/liftoff/assets"

PROJECT_PATH = getcwd()
PROJECT_LIFTOFF_PATH = f"{PROJECT_PATH}/.liftoff"

PGSQL_HOST = 'local.liftoff.com'
PGSQL_USER = 'liftoff'
PGSQL_PASSWORD = 'liftoff'

MYSQL_HOST = 'local.liftoff.com'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'liftoff'
