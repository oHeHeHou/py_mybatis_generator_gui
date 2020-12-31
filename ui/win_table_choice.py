import os
import queue
import threading
from tkinter import *
from tkinter import ttk
import tkinter.tix as tix
from dao.db2_dao import DB2Dao
from dao.db_source_dao import DBSourceDao
from dao.mysql_dao import MysqlDao
from dao.output_config_dao import OutputConfigDao
from ui.win_config import ConfigWindow
from ui.win_progress import ProgressWindow
from utils.generate_util import GenerateUtil
from utils.window_util import WindowUtil
from utils.xml_util import XmlUtil


class TableChoiceWindow:

    def __init__(self, src_model):
        self.win_progress = ProgressWindow()
        self.generate_queue = queue.Queue()
        self.table_queue = queue.Queue()
        self.win = None
        self.source_dao = DBSourceDao()
        self.src_model = src_model
        self.check_view = None
        self.progress = None

    def show(self):
        window = tix.Tk()
        self.win = window
        window.title("选择表")
        window_util = WindowUtil(window)
        # w,h
        window_util.set_size(380, 300)
        window_util.disable_resize()
        window_util.center_on_screen()

        par_frame = ttk.Frame(window, padding=10)
        par_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        mainframe = ttk.Frame(par_frame, padding=5)
        mainframe.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))

        self.init_check_list(mainframe)
        self.init_buttons(mainframe)
        self.init_progress(mainframe)

    def init_check_list(self, parent):
        db_type = self.source_dao.get_db_type_by_id(self.src_model.source_type_id)[0].lower()
        GetTableListTask(self.table_queue, db_type, self.src_model).start()
        self.win.after(100, self.process_table_list_queue)
        self.check_view = CheckListView(parent)

    def init_buttons(self, par_frame):
        ttk.Button(par_frame, text="输出配置", command=self.config_output).grid(column=0, row=1,
                                                                            pady=8, )
        ttk.Button(par_frame, text="生成代码", command=self.generate_code).grid(column=0, row=2,
                                                                            pady=8, )

    def init_progress(self, par_frame):
        self.progress = ttk.Progressbar(par_frame, orient=HORIZONTAL, length=100,
                                        mode='determinate')
        self.progress.grid(column=0, row=0, sticky=(N, W, E, S))
        self.progress.grid_remove()

    def config_output(self):
        config_win = ConfigWindow(self.win)
        config_win.show(self.src_model)

    def generate_code(self):
        tuple_table = self.check_view.get_selected_value()
        table_list = []
        for t in tuple_table:
            if t == 'all':
                continue
            index = t.find('.') + 1
            table_list.append(t[index:])
        self.show_progress()
        db_type = self.source_dao.get_db_type_by_id(self.src_model.source_type_id)[0].lower()
        GenerateTask(self.generate_queue, self.src_model, db_type, table_list).start()
        self.win.after(100, self.process_generate_queue)

    def process_generate_queue(self):
        try:
            msg = self.generate_queue.get(False)
            self.hide_progress()
            self.win.attributes('-topmost', False)
        except queue.Empty:
            self.win.after(100, self.process_generate_queue)

    def process_table_list_queue(self):
        try:
            table_list = self.table_queue.get(True, 100)
            self.check_view.make_list(table_list)
        except queue.Empty:
            self.win.after(100, self.process_table_list_queue)

    def show_progress(self):
        self.win_progress.show()

    def hide_progress(self):
        self.win_progress.stop()


class CheckListView:
    def __init__(self, root):
        self.root = root
        self.check_list = tix.CheckList(self.root, browsecmd=self.on_item_selected)
        self.check_list.configure(width=340, height=200)
        self.check_list.grid(column=0, row=0, sticky=(N, W, E, S))
        self.check_list.hlist.config(bg='white', bd=0, pady=1, )
        self.tables = None
        self.select_all = False
        self.mouse_up = False

    def make_list(self, table_list):
        if len(table_list) == 0:
            pass
        self.tables = table_list
        self.check_list.hlist.add('all', text='全选/反选')
        self.check_list.setstatus('all', "on")
        for i, table in enumerate(table_list):
            self.check_list.hlist.add('all.' + table, text=table)
            self.check_list.setstatus('all.' + table, "on")
            self.check_list.autosetmode()
        self.check_list.hlist.bind("<ButtonRelease-1>", self.on_item_clicked)
        self.select_all = True

    # 点击一次鼠标，browsecmd会call两次，所以要监听mouseUp事件来判断点击
    def on_item_clicked(self, item):
        self.mouse_up = True

    def on_item_selected(self, item):
        if item == 'all':
            if self.mouse_up:
                if self.check_list.getstatus('all') == 'off':
                    print('off')
                    status = 'off'
                else:
                    print('on')
                    status = 'on'
                self.set_child_status(item, status)
                self.mouse_up = False

    def set_child_status(self, item, status):
        self.check_list.setstatus(item, status)
        for child in self.check_list.hlist.info_children(item):
            self.set_child_status(child, status)

    def get_selected_value(self):
        tbs = self.check_list.getselection()
        return tbs


class GenerateTask(threading.Thread):
    def __init__(self, queue, src_model, db_type, table_list):
        threading.Thread.__init__(self)
        self.queue = queue
        self.src_model = src_model
        self.db_type = db_type
        self.table_list = table_list

    def run(self):
        xml_util = XmlUtil()
        xml_util.set_class_path_entry(self.db_type)
        xml_util.set_jdbc_conn(self.db_type, self.src_model)
        config_dao = OutputConfigDao()
        output_model = config_dao.get_by_id(self.src_model.id)
        xml_util.set_target_pkg(self.db_type, output_model)
        xml_util.set_tables(self.table_list)
        xml_util.write_header()

        open_folder = output_model.out_dir + os.path.sep + 'result' + os.path.sep + self.db_type
        GenerateUtil.generate(open_folder)

        self.queue.put("Task finished")


class GetTableListTask(threading.Thread):
    def __init__(self, queue, db_type, src_model):
        threading.Thread.__init__(self)
        self.queue = queue
        self.src_model = src_model
        self.db_type = db_type

    def run(self):
        table_list = []
        if self.db_type == 'mysql':
            table_list = MysqlDao.get_tables(self.src_model)
        elif self.db_type == 'db2':
            table_list = DB2Dao.get_tables(self.src_model)

        self.queue.put(table_list)
