from .base import Builder
from shutil import copyfile
from os import makedirs, listdir, system, remove
from os.path import exists
from ..core.vars import *


liftoff_hosts = [
    'local.liftoff.com',
    'adminer.local.liftoff.com',
    'mailhog.local.liftoff.com'
]


class LiftoffBuilder(Builder):
    @staticmethod
    def build(config=None):
        LiftoffBuilder.__create_liftoff_dirs()
        LiftoffBuilder.__copy_config_files()
        LiftoffBuilder.__update_hosts()

    @staticmethod
    def __create_liftoff_dirs():
        if not exists(LIFTOFF_PATH):
            makedirs(LIFTOFF_PATH)
            print("Created liftoff configuration directory at " + LIFTOFF_PATH)

        if not exists(LIFTOFF_APPS_PATH):
            makedirs(LIFTOFF_APPS_PATH)

        if not exists(LIFTOFF_VHOSTS_PATH):
            makedirs(LIFTOFF_VHOSTS_PATH)

    @staticmethod
    def __copy_config_files():
        copyfile(f'{ASSETS_PATH}/docker-compose.yml', f'{LIFTOFF_PATH}/docker-compose.yml')
        copyfile(f'{ASSETS_PATH}/nginx.conf', f'{LIFTOFF_PATH}/nginx.conf')

        for file in listdir(f'{ASSETS_PATH}/vhosts'):
            copyfile(f'{ASSETS_PATH}/vhosts/{file}', f'{LIFTOFF_VHOSTS_PATH}/{file}')

    @staticmethod
    def __update_hosts():
        copyfile('/etc/hosts', '/tmp/hosts.tmp')

        hosts_file = open('/tmp/hosts.tmp', 'r+')

        # Using read() seeks to end of file, so any calls to write() will append
        contents = hosts_file.read()
        needs_update = False

        for host in liftoff_hosts:
            if host not in contents:
                needs_update = True
                hosts_file.write(f"127.0.0.1 {host}\n")

        hosts_file.close()

        if needs_update:
            print('Adding liftoff service domains to /etc/hosts file')
            system('sudo mv /tmp/hosts.tmp /etc/hosts')
        else:
            remove('/tmp/hosts.tmp')
