import os
import subprocess

from dao.db_source_dao import DBSourceDao


class GenerateUtil:
    def __init__(self):
        self.source_dao = DBSourceDao()

    @staticmethod
    def generate(out_dir):
        root_dir = os.path.realpath('.')
        jar_path = root_dir + os.path.sep + 'jar' + os.path.sep + 'mybatis-generator-core-1.4.0.jar'
        xml_path = root_dir + os.path.sep + 'jar' + os.path.sep + 'generatorConfig.xml'
        # java -jar mybatis-generator-core-1.4.0.jar -configfile generatorConfig.xml -overwrite
        subprocess.run(["java", "-jar", jar_path, "-configfile", xml_path, "-overwrite"])

        os.system('start %s' % out_dir)