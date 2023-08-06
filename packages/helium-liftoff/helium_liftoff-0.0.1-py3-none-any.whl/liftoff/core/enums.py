from enum import Enum


class ProjectType(Enum):
    LARAVEL = 'Laravel'


class DatabaseType(Enum):
    POSTGRESQL = 'PostgreSQL'
    MYSQL = 'MySQL'
    NONE = 'None'


def database_port(db_type: str):
    if db_type == DatabaseType.POSTGRESQL.value:
        return 5432
    elif db_type == DatabaseType.MYSQL.value:
        return 3306
    else:
        return None


class PhpVersion(Enum):
    PHP8_0 = 'php-8.0'
    PHP7_4 = 'php-7.4'
