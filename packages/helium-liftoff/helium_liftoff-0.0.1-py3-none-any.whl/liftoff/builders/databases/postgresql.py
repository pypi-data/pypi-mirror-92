from .base import DatabaseBuilder
import psycopg2
from psycopg2.extensions import cursor, ISOLATION_LEVEL_AUTOCOMMIT
from liftoff.core.vars import PGSQL_HOST, PGSQL_USER, PGSQL_PASSWORD


class PostgresqlBuilder(DatabaseBuilder):
    __connection = None

    @staticmethod
    def _connection() -> cursor:
        if PostgresqlBuilder.__connection is None:
            PostgresqlBuilder.__connection = psycopg2.connect(host=PGSQL_HOST, user=PGSQL_USER, password=PGSQL_PASSWORD)
            PostgresqlBuilder.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        return PostgresqlBuilder.__connection.cursor()

    @staticmethod
    def _create_database(database: str):
        conn = PostgresqlBuilder._connection()

        conn.execute("SELECT exists(SELECT datname FROM pg_database WHERE datname like %s)", (database,))
        response = conn.fetchall()
        exists = response[0][0]

        if exists:
            print(f"PostgreSQL database '{database}' already exists. Skipping.")
        else:
            conn.execute(f"CREATE DATABASE {database}")
            # Prepared statements are not possible for the CREATE command
            # Since this is used for databases on the user's local system, sql injection is not a real concern

            print(f"Created PostgreSQL database '{database}'.")

    @staticmethod
    def _create_user(username: str, password: str):
        conn = PostgresqlBuilder._connection()

        conn.execute("SELECT exists(SELECT usename FROM pg_catalog.pg_user WHERE usename like %s)", (username,))
        response = conn.fetchall()
        exists = response[0][0]

        if exists:
            print(f"PostgreSQL user '{username}' already exists. Skipping.")
        else:
            conn.execute(f"CREATE USER {username} PASSWORD '{password}'")
            # Prepared statements are not possible for the CREATE command
            # Since this is used for databases on the user's local system, sql injection is not a real concern

            print(f"Created PostgreSQL user '{username}'.")

    @staticmethod
    def _grant_user_permissions(username: str, database: str):
        conn = PostgresqlBuilder._connection()

        conn.execute(f'GRANT ALL PRIVILEGES ON DATABASE {database} TO {username}')
        # Prepared statements are not possible for the GRANT command
        # Since this is used for databases on the user's local system, sql injection is not a real concern

        print(f"Granted PostgreSQL user '{username}' all privileges on database {database}.")

