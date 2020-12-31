import os
import subprocess

from pymysql import DatabaseError


class DB2Dao:
    def __init__(self):
        pass

    @staticmethod
    def test_conn(source_model):
        try:
            root_path = os.path.realpath('.')
            jar_path = root_path + os.path.sep + 'jar' + os.path.sep + "Db2info.jar"
            ret = subprocess.check_output(['java', '-jar', jar_path,
                                           '-c' + source_model.url,
                                           '-u' + source_model.user,
                                           '-p' + source_model.password, '-test'])
            ret_str = ret.decode('utf-8')
            if ret_str is not None:
                if ret_str == 'yes':
                    return True
                else:
                    return False
            else:
                return False
        except DatabaseError:
            return False

    @staticmethod
    def get_tables(source_model):
        root_path = os.path.realpath('.')
        jar_path = root_path + os.path.sep + 'jar' + os.path.sep + "Db2info.jar"
        ret = subprocess.check_output(['java', '-jar', jar_path,
                                       '-c' + source_model.url,
                                       '-u' + source_model.user,
                                       '-p' + source_model.password, '-list'])
        ret_list = ret.decode('utf-8')
        ret_list = ret_list[1:-1]
        tb_arr = ret_list.split(',')
        ret_list = []
        for tb in tb_arr:
            ret_list.append(tb.strip())
        return ret_list
