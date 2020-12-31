import sqlite3

from model.output_config_model import OutputConfigModel


class OutputConfigDao:

    def __init__(self):
        self.conn = sqlite3.connect('mybatis_generator.db')

    def close(self):
        self.conn.cursor().close()
        self.conn.close()

    def add_config(self, output_config):
        cur = self.conn.cursor()
        cur.execute(
            "insert into tb_output_config(src_id, model_pkg, sql_map_pkg, mapper_pkg, out_dir) values (?, ?, ?, ?, ?)",
            (output_config.src_id, output_config.model_pkg, output_config.sql_map_pkg,
             output_config.mapper_pkg
             , output_config.out_dir))
        self.conn.commit()

    def update(self, output_config):
        cur = self.conn.cursor()
        cur.execute(
            "update tb_output_config set model_pkg=?, sql_map_pkg=?, mapper_pkg=?, out_dir=? where src_id=?",
            (output_config.model_pkg, output_config.sql_map_pkg, output_config.mapper_pkg,
             output_config.out_dir, output_config.src_id))
        self.conn.commit()

    def get_by_id(self, src_id):
        cur = self.conn.cursor()
        result = cur.execute("select * from tb_output_config where src_id=?", str(src_id)).fetchone()
        if result is not None:
            output_config = OutputConfigModel()
            output_config.src_id = result[0]
            output_config.model_pkg = result[1]
            output_config.sql_map_pkg = result[2]
            output_config.mapper_pkg = result[3]
            output_config.out_dir = result[4]
            return output_config
        else:
            return result

    def del_by_id(self, src_id):
        cur = self.conn.cursor()
        cur.execute("delete from tb_output_config where src_id=?", str(src_id))
        self.conn.commit()
