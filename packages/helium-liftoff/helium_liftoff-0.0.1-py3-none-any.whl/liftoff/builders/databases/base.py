from abc import abstractmethod
from liftoff.builders.base import Builder
from liftoff.core.enums import DatabaseType


def build_database(db_type: str, config: dict):
    if db_type is None:
        return
    elif db_type == DatabaseType.POSTGRESQL.value:
        from .postgresql import PostgresqlBuilder
        PostgresqlBuilder.build(config)
    elif db_type == DatabaseType.MYSQL.value:
        from .mysql import MysqlBuilder
        MysqlBuilder.build(config)


class DatabaseBuilder(Builder):
    @classmethod
    def build(cls, config: dict):
        try:
            cls._create_database(config.get('db_name'))
            cls._create_user(config.get('db_username'), config.get('db_password'))
            cls._grant_user_permissions(config.get('db_username'), config.get('db_name'))
        except:
            print('Something went wrong with setting up the database.')
            print('Please manually configure your database at https://adminer.local.liftoff.com.')

    @staticmethod
    @abstractmethod
    def _create_database(database: str):
        pass

    @staticmethod
    @abstractmethod
    def _create_user(username: str, password: str):
        pass

    @staticmethod
    @abstractmethod
    def _grant_user_permissions(username: str, database: str):
        pass
