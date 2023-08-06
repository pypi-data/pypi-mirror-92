from liftoff.core.enums import ProjectType
from liftoff.core.vars import PROJECT_LIFTOFF_PATH, PROJECT_PATH
from liftoff.builders.base import Builder
from liftoff.builders.databases.base import build_database
from os.path import exists, isfile
from os import makedirs, system, remove
from shutil import copyfile
from liftoff.core.docker_compose import restart_liftoff
import json


def build_project(config: dict):
    project_type = config.get('project_type')

    if project_type == ProjectType.LARAVEL.value:
        from .laravel import LaravelBuilder
        LaravelBuilder.build(config)


class ProjectBuilder(Builder):
    @classmethod
    def build(cls, config: dict):
        cls._create_liftoff_dir()
        cls._update_gitignore()
        cls._store_config(config)
        cls._add_hosts(config.get('hostname'))
        cls._create_docker_compose_override(config)
        cls._create_nginx_config(config)
        restart_liftoff()
        cls._build_database(config)

        print("Successfully built liftoff project!")

    @classmethod
    def _create_liftoff_dir(cls):
        if not exists(PROJECT_LIFTOFF_PATH):
            makedirs(PROJECT_LIFTOFF_PATH)
            print(f"Created liftoff project configuration directory at '{PROJECT_LIFTOFF_PATH}'.")

    @classmethod
    def _update_gitignore(cls):
        git_ignore_path = f"{PROJECT_PATH}/.gitignore"

        if isfile(git_ignore_path):
            with open(git_ignore_path, 'r+') as file:
                contents = file.read()

                vhost_file = '.liftoff/vhost.conf'
                if vhost_file not in contents:
                    print(f'Adding {vhost_file} to .gitignore.')
                    file.write(f'{vhost_file}\n')

                docker_compose_file = '.liftoff/docker-compose.override.yml'
                if docker_compose_file not in contents:
                    print(f'Adding {docker_compose_file} to .gitignore.')
                    file.write(f'{docker_compose_file}\n')

    @classmethod
    def _store_config(cls, config: dict):
        json_string = json.dumps(config, indent=2)
        with open(f"{PROJECT_LIFTOFF_PATH}/config.json", 'w') as config_file:
            config_file.write(json_string)
        print(f"Created liftoff configuration file.")

    @classmethod
    def _add_hosts(cls, hostname: str):
        copyfile('/etc/hosts', '/tmp/hosts.tmp')

        hosts_file = open('/tmp/hosts.tmp', 'r+')

        # Using hosts_file.read() seeks to end of file, so any calls to write() will append
        contents = hosts_file.read()
        needs_update = False

        if hostname not in contents:
            needs_update = True
            hosts_file.write(f"127.0.0.1 {hostname}\n")

        hosts_file.close()

        if needs_update:
            print('Adding project domain to /etc/hosts file.')
            system('sudo mv /tmp/hosts.tmp /etc/hosts')
        else:
            remove('/tmp/hosts.tmp')

    @classmethod
    def _create_docker_compose_override(cls, config: dict):
        pass

    @classmethod
    def _create_nginx_config(cls, config: dict):
        pass

    @classmethod
    def _build_database(cls, config: dict):
        db_type = config.get('db_type')
        if db_type is None:
            return

        db_config = dict((key, config[key]) for key in ['db_name', 'db_username', 'db_password'])
        build_database(db_type, db_config)
