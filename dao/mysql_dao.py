import pymysql
from pymysql import DatabaseError


class MysqlDao:
    def __init__(self):
        pass

    @staticmethod
    def test_conn(source_model):
        try:
            db = pymysql.connect(
                host=source_model.host,
                user=source_model.user,
                password=source_model.password,
                port=int(source_model.port),
                database=source_model.database,
                charset='utf8',
            )
            if db is not None:
                db.close()
                return True
        except DatabaseError:
            return False
        return False

    @staticmethod
    def get_tables(source_model):
        db_conn = pymysql.connect(
            host=source_model.host,
            user=source_model.user,
            password=source_model.password,
            port=int(source_model.port),
            database=source_model.database,
            charset='utf8',
        )
        ret_list = []
        query_sql = "select table_name from information_schema.TABLES where TABLE_SCHEMA='%s'"  %(source_model.database)
        if db_conn is not None:
            cursor = db_conn.cursor()
            cursor.execute(query_sql)

            for row in cursor.fetchall():
                table_name = row[0]
                ret_list.append(table_name)

        db_conn.close()

        return ret_list
