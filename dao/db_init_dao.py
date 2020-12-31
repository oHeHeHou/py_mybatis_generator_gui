import sqlite3


class DBInitDao:

    def __init__(self):
        self.conn = sqlite3.connect('mybatis_generator.db')

    def initialize(self):
        self.init_tables()
        self.close()

    def close(self):
        self.conn.cursor().close()
        self.conn.close()

    def get_db_source_list(self):
        cur = self.conn.cursor()
        return cur.execute("select * from tb_db_source").fetchall()

    def get_db_type(self):
        cur = self.conn.cursor()
        return cur.execute("select * from tb_source_type").fetchall()

    def init_tables(self):
        cursor = self.conn.cursor()
        create_source_sql = '''
        create table if not exists tb_db_source(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        host TEXT,
        port TEXT,
        database TEXT,
        user TEXT,
        password TEXT,
        url TEXT,
        source_type_id INTEGER
        );
        '''

        cursor.execute(create_source_sql)

        create_type_sql = '''
        create table if not exists tb_source_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_type TEXT
        );
        '''

        cursor.executescript(create_type_sql)

        create_output_config_sql = '''
        create table if not exists tb_output_config(
        src_id INTEGER PRIMARY KEY,
        model_pkg TEXT,
        sql_map_pkg TEXT,
        mapper_pkg TEXT,
        out_dir TEXT
        );
        '''

        cursor.executescript(create_output_config_sql)

        init_type_sql = '''
            insert into tb_source_type(id, source_type) values(null, 'Mysql');
            insert into tb_source_type(id, source_type) values(null, 'DB2');
        '''

        count_t = cursor.execute("select count(*) from tb_source_type").fetchone()
        count = count_t[0]
        if count == 0:
            cursor.executescript(init_type_sql)
