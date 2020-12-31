import os
import xml.etree.ElementTree as ET


class XmlUtil:
    def __init__(self):
        self.root_dir = os.path.realpath('.')
        self.jar_path = self.root_dir + os.path.sep + 'jar' + os.path.sep
        self.xml_path = self.root_dir + os.path.sep + 'jar' + os.path.sep + 'generatorConfig.xml'
        self.mysql_class = 'com.mysql.cj.jdbc.Driver'
        self.db2_class = 'com.ibm.db2.jcc.DB2Driver'

    '''
    xml中的tableName配置
    '''
    def set_tables(self, table_list):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        node_context = root.find('context')
        table_nodes = node_context.findall('table')
        # 清除旧表配置
        for tb_node in table_nodes:
            node_context.remove(tb_node)
        # 新增表配置
        for table in table_list:
            tb_element = ET.Element('table')
            tb_element.set('tableName', table)
            node_context.append(tb_element)

        tree.write(self.xml_path)

    '''
    xml中的classPathEntry配置
    '''
    def set_class_path_entry(self, db_type):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        class_node = root.find('classPathEntry')
        if db_type == 'mysql':
            class_node.set('location', self.jar_path + 'mysql-driver.jar')
        else:
            class_node.set('location', self.jar_path + 'db2-driver.jar')
        tree.write(self.xml_path)

    def set_jdbc_conn(self, db_type, src_model):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        context_node = root.find('context')
        conn_node = context_node.find('jdbcConnection')
        if db_type == 'mysql':
            conn_node.set('driverClass', self.mysql_class)
        else:
            conn_node.set('driverClass', self.db2_class)
        conn_node.set('connectionURL', src_model.url)
        conn_node.set('userId', src_model.user)
        conn_node.set('password', src_model.password)
        tree.write(self.xml_path)

    '''
    xml中的targetPackage和targetProject配置
    '''
    def set_target_pkg(self, db_type, output_model):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        context_node = root.find('context')

        # model文件输出路径
        java_model_generator = context_node.find('javaModelGenerator')
        model_target_pkg = output_model.model_pkg
        java_model_generator.set('targetPackage', model_target_pkg)
        model_target_folder = output_model.out_dir + os.path.sep \
                              + 'result' + os.path.sep + db_type + os.path.sep + 'model'
        if not os.path.exists(model_target_folder):
            os.makedirs(model_target_folder)
        java_model_generator.set('targetProject', model_target_folder)

        # xml文件输出路径
        sql_map_generator = context_node.find('sqlMapGenerator')
        sql_target_pkg = output_model.sql_map_pkg
        sql_map_generator.set('targetPackage', sql_target_pkg)
        sql_target_folder = output_model.out_dir + os.path.sep \
                            + 'result' + os.path.sep + db_type + os.path.sep + 'mapper'
        if not os.path.exists(sql_target_folder):
            os.makedirs(sql_target_folder)
        sql_map_generator.set('targetProject', sql_target_folder)

        # mapper文件输出路径
        java_client_generator = context_node.find('javaClientGenerator')
        java_client_pkg = output_model.mapper_pkg
        java_client_generator.set('targetPackage', java_client_pkg)
        mapper_folder = output_model.out_dir + os.path.sep \
                        + 'result' + os.path.sep + db_type + os.path.sep + 'dao'
        if not os.path.exists(mapper_folder):
            os.makedirs(mapper_folder)
        java_client_generator.set('targetProject', mapper_folder)
        tree.write(self.xml_path)

    '''
    xml固定头部
    '''
    def write_header(self):
        header = """<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE generatorConfiguration PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN" "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">\n
        """
        with open(self.xml_path, "r+") as f:
            src_content = f.read()
            f.seek(0)
            f.write(header)
            f.write(src_content)
