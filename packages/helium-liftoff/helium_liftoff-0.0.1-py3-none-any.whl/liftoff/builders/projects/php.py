from .base import ProjectBuilder
from liftoff.core.vars import PROJECT_PATH, PROJECT_LIFTOFF_PATH, LIFTOFF_APPS_PATH, LIFTOFF_VHOSTS_PATH
from os import symlink, remove
from os.path import exists


class PhpBuilder(ProjectBuilder):
    @classmethod
    def _create_docker_compose_override(cls, config: dict):
        output_path = f'{PROJECT_LIFTOFF_PATH}/docker-compose.override.yml'

        cls.render_template_to_file({
            'path': PROJECT_PATH,
            'php_container': config['php_version']
        }, 'docker-compose.override/php.jinja2', output_path)

        symlink_path = f'{LIFTOFF_APPS_PATH}/{config["project_name"]}.override.yml'

        if exists(symlink_path):
            remove(symlink_path)

        symlink(output_path, symlink_path)

        print("Created docker-compose configuration file.")

    @classmethod
    def _create_nginx_config(cls, config: dict):
        if 'php_container' not in config.keys():
            config.update({
                'php_container': config['php_version']
            })
        if 'path' not in config.keys():
            config.update({
                'path': PROJECT_PATH
            })

        output_path = f'{PROJECT_LIFTOFF_PATH}/vhost.conf'

        cls.render_template_to_file(config, 'vhost/laravel.jinja2', output_path)

        symlink_path = f'{LIFTOFF_VHOSTS_PATH}/{config["project_name"]}.conf'

        if exists(symlink_path):
            remove(symlink_path)

        symlink(output_path, symlink_path)

        print("Created NGINX configuration file.")
