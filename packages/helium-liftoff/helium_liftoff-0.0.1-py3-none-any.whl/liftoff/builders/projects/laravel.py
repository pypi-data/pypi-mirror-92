from .php import PhpBuilder
from liftoff.core.vars import PROJECT_PATH
from liftoff.core.enums import DatabaseType, database_port
from os.path import isfile
from re import sub


DB_CONNECTION_MAP = {
    DatabaseType.POSTGRESQL.value: 'pgsql',
    DatabaseType.MYSQL.value: 'mysql',
    DatabaseType.NONE.value: ''
}


class LaravelBuilder(PhpBuilder):
    @classmethod
    def build(cls, config: dict):
        super(LaravelBuilder, LaravelBuilder).build(config)
        cls._update_env(config)

    @classmethod
    def _create_nginx_config(cls, config: dict):
        config.update({
            'path': f'{PROJECT_PATH}/public',
        })

        super(LaravelBuilder, LaravelBuilder)._create_nginx_config(config)

    @classmethod
    def _update_env(cls, config: dict):
        env_file_path = f'{PROJECT_PATH}/.env'
        env_example_file_path = f'{PROJECT_PATH}/.env.example'

        if not isfile(env_file_path) and not isfile(env_example_file_path):
            print('No .env file found. Skipping.')
            return

        key_map = {
            'APP_URL': f'http://{config.get("hostname", "localhost")}/',
            'DB_CONNECTION': DB_CONNECTION_MAP.get(config.get('db_type', 'None')),
            'DB_HOST': 'local.liftoff.com' if config.get('db_type', 'None') != 'None' else '',
            'DB_PORT': database_port(config.get('db_type', 'None')),
            'DB_DATABASE': config.get('db_name', ''),
            'DB_USERNAME': config.get('db_username', ''),
            'DB_PASSWORD': config.get('db_password', ''),
            'MAIL_MAILER': 'smtp',
            'MAIL_HOST': 'local.liftoff.com',
            'MAIL_PORT': 1025,
            'MAIL_USERNAME': 'null',
            'MAIL_PASSWORD': 'null',
            'MAIL_ENCRYPTION': 'null',
            'MAIL_FROM_ADDRESS': f'noreply@{config.get("hostname", "example.com")}',
            'MAIL_FROM_NAME': '${APP_NAME}'
        }

        def search_and_replace(path: str):
            if isfile(path):
                filename = path.split('/').pop()

                with open(path, 'r+') as file:
                    contents = file.read()

                    for key in key_map.keys():
                        contents = sub(rf'{key}=.*', f'{key}={key_map.get(key)}', contents)

                    print(f'Updating {filename} file.')

                    file.seek(0)
                    file.write(contents)

        search_and_replace(env_file_path)
        search_and_replace(env_example_file_path)
