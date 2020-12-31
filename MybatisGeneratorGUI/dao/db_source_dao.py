import sqlite3

from model.db_source_model import DBSourceModel


class DBSourceDao:

    def __init__(self):
        self.conn = sqlite3.connect('mybatis_generator.db')

    def close(self):
        self.conn.cursor().close()
        self.conn.close()

    def get_db_source_list(self):
        cur = self.conn.cursor()
        return cur.execute(
            "select a.id, a.name, a.host, a.port, a.database, a.user, a.password, a.url, b.source_type "
            "from tb_db_source a, tb_source_type b where a.source_type_id = b.id").fetchall()

    def get_db_type(self):
        cur = self.conn.cursor()
        return cur.execute("select * from tb_source_type").fetchall()

    def add_db_source(self, source_model):
        cur = self.conn.cursor()
        cur.execute(
            "insert into tb_db_source(name, host, port, database, user, password, url, source_type_id) values (?, ?, ?, ?, ?, ?, ?, ?)",
            (source_model.name, source_model.host, source_model.port, source_model.database
             , source_model.user, source_model.password, source_model.url,
             source_model.source_type_id))
        self.conn.commit()

    def update_db_source(self, source_model):
        cur = self.conn.cursor()
        cur.execute(
            "update tb_db_source set name=?, host=?, port=?, database=?, user=?, password=?, url=?, source_type_id=? where id=?",
            (source_model.name, source_model.host, source_model.port, source_model.database
             , source_model.user, source_model.password, source_model.url,
             source_model.source_type_id, source_model.id))
        self.conn.commit()

    def get_db_src_by_id(self, sel_item_id):
        cur = self.conn.cursor()
        src_tuple = cur.execute("select * from tb_db_source where id=?", sel_item_id).fetchone()
        if src_tuple is None:
            return None
        model = DBSourceModel()
        model.id = src_tuple[0]
        model.name = src_tuple[1]
        model.host = src_tuple[2]
        model.port = src_tuple[3]
        model.database = src_tuple[4]
        model.user = src_tuple[5]
        model.password = src_tuple[6]
        model.url = src_tuple[7]
        model.source_type_id = src_tuple[8]

        return model

    def del_db_src_by_id(self, sel_item_id):
        cur = self.conn.cursor()
        cur.execute("delete from tb_db_source where id=?", str(sel_item_id))
        self.conn.commit()

    def get_db_type_by_id(self, sel_item_id):
        cur = self.conn.cursor()
        return cur.execute("select source_type from tb_source_type where id=?",
                           str(sel_item_id)).fetchone()

