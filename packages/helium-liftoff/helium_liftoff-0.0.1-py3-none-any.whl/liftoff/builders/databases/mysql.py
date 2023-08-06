from .base import DatabaseBuilder
from mysql import connector
from liftoff.core.vars import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD


class MysqlBuilder(DatabaseBuilder):
    __connection = None

    @staticmethod
    def _connection():
        if MysqlBuilder.__connection is None:
            MysqlBuilder.__connection = connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)

        MysqlBuilder.__connection.rollback()
        return MysqlBuilder.__connection.cursor()

    @staticmethod
    def _create_database(database: str):
        conn = MysqlBuilder._connection()
        conn.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
        # Prepared statements are not possible for the CREATE command
        # Since this is used for databases on the user's local system, sql injection is not a real concern

        print(f"Created MySQL database '{database}'.")

        conn.close()


    @staticmethod
    def _create_user(username: str, password: str):
        conn = MysqlBuilder._connection()

        conn.execute('SELECT exists(SELECT user FROM mysql.user WHERE user like %s)', (username,))
        response = conn.fetchall()
        exists = bool(response[0][0])

        if exists:
            print(f"MySQL user '{username}' already exists. Skipping.")
        else:
            conn.execute(f"CREATE USER '{username}'@'%' IDENTIFIED WITH mysql_native_password BY '{password}'")
            # Prepared statements are not possible for the CREATE command
            # Since this is used for databases on the user's local system, sql injection is not a real concern

            print(f"Created MySQL user '{username}'.")

        conn.close()

    @staticmethod
    def _grant_user_permissions(username: str, database: str):
        conn = MysqlBuilder._connection()

        conn.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{username}'@'%'")
        # Prepared statements are not possible for the GRANT command
        # Since this is used for databases on the user's local system, sql injection is not a real concern

        print(f"Granted MySQL user '{username}' all privileges on database {database}.")

        conn.close()
