from tkinter import *
from tkinter import ttk

from dao.db2_dao import DB2Dao
from dao.db_source_dao import DBSourceDao
from dao.mysql_dao import MysqlDao
from model.db_source_model import DBSourceModel
from utils.window_util import WindowUtil


class DataSourceMgmtWindow:

    def __init__(self, root):
        self.root = root
        self.name = StringVar()
        self.host = StringVar()
        self.port = StringVar()
        self.user = StringVar()
        self.password = StringVar()
        self.database = StringVar()
        self.url = StringVar()
        self.type = StringVar()
        self.box_current = IntVar()
        self.type_id_list = []
        self.conn_hint = StringVar()

        self.name_entry = None
        self.host_entry = None
        self.port_entry = None
        self.user_entry = None
        self.pwd_entry = None
        self.url_entry = None
        self.db_box = None
        self.db_entry = None
        self.hint_label = None

        self.source_dao = DBSourceDao()
        self.opt = None
        self.win = None
        self.edit_model = None

    def show(self):
        window = Toplevel(self.root)
        self.win = window
        window.title("新增数据源")
        window_util = WindowUtil(window)
        window_util.set_size(340, 300)
        window_util.disable_resize()
        window_util.center_on_screen()

        par_frame = ttk.Frame(window, padding=10)
        par_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        mainframe = ttk.Frame(par_frame, padding=10)
        mainframe.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))

        self.init_combobox(mainframe)
        self.init_entries(mainframe)
        self.opt = 'add'

        ttk.Button(mainframe, text="测试", width=5, command=self.test_url).grid(row=7, column=2, sticky=E)
        ttk.Button(par_frame, text="确定", command=self.save).grid(row=1, column=1, pady=10, sticky=W)

    def edit_window(self, source_model):
        window = Toplevel(self.root)
        window.title("编辑数据源")
        window_util = WindowUtil(window)
        window_util.set_size(340, 300)
        window_util.disable_resize()
        window_util.center_on_screen()
        self.win = window
        par_frame = ttk.Frame(window, padding=10)
        par_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        mainframe = ttk.Frame(par_frame, padding=10)
        mainframe.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))

        # self.init_combobox(mainframe)
        self.init_entries(mainframe)
        self.complete_combobox(mainframe, source_model)
        self.complete_entries(source_model)
        self.opt = 'edit'
        self.edit_model = source_model

        ttk.Button(mainframe, text="测试", width=5, command=self.test_url).grid(row=7, column=2, sticky=E)
        ttk.Button(par_frame, text="确定", command=self.save).grid(row=1, column=1, pady=10, sticky=W)

    def test_url(self):
        is_conn = False
        box_db_type = self.db_box.get()
        if box_db_type == '' or None:
            pass
        dbtype = box_db_type.lower()
        source_model = self.get_input_source_model()
        if dbtype == 'mysql':
            is_conn = MysqlDao.test_conn(source_model)
        elif dbtype == 'db2':
            pass
            is_conn = DB2Dao.test_conn(source_model)
        if is_conn:
            self.hint_label.grid()
            self.conn_hint.set('连接成功')
        else:
            self.hint_label.grid()
            self.conn_hint.set('连接失败')

    def save(self):
        db_model = self.get_input_source_model()
        if self.opt == 'add':
            self.source_dao.add_db_source(db_model)
        else:
            self.source_dao.update_db_source(db_model)
        self.close_window()

    def get_input_source_model(self):
        db_model = DBSourceModel()
        db_model.name = self.name.get()
        db_model.host = self.host.get()
        db_model.port = self.port.get()
        db_model.database = self.database.get()
        db_model.user = self.user.get()
        db_model.password = self.password.get()
        db_model.url = self.url.get()
        index = self.db_box.current()
        db_model.source_type_id = self.type_id_list[index]
        if self.opt == 'edit':
            db_model.id = self.edit_model.id

        return db_model

    def init_combobox(self, mainframe):
        ttk.Label(mainframe, text='类型：').grid(row=0, column=0, sticky=(W, E))
        self.db_box = ttk.Combobox(mainframe, textvariable=self.type)
        db_type_list = self.source_dao.get_db_type()
        type_list = []
        for dbtype in db_type_list:
            self.type_id_list.append(dbtype[0])
            type_list.append(dbtype[1])
        self.db_box['values'] = tuple(type_list)
        self.db_box.current(0)
        self.db_box.state(["readonly"])
        self.db_box.bind('<<ComboboxSelected>>', self.on_dbtype_selected)
        self.db_box.grid(row=0, column=1, sticky=(W, E))
        self.db_box.focus()

    def complete_combobox(self, mainframe, source_model):
        ttk.Label(mainframe, text='类型：').grid(row=0, column=0, sticky=(W, E))
        self.db_box = ttk.Combobox(mainframe, textvariable=self.type)
        db_type_list = self.source_dao.get_db_type()
        type_list = []
        for dbtype in db_type_list:
            self.type_id_list.append(dbtype[0])
            type_list.append(dbtype[1])
        self.db_box['values'] = tuple(type_list)
        type_id = source_model.source_type_id
        type_name = self.source_dao.get_db_type_by_id(type_id)[0]
        type_index = type_list.index(type_name)
        self.db_box.current(type_index)
        self.db_box.state(["readonly"])
        self.db_box.bind('<<ComboboxSelected>>', self.on_dbtype_selected)
        self.db_box.grid(row=0, column=1, sticky=(W, E))
        self.db_box.focus()

    def complete_entries(self, source_model):
        self.name.set(source_model.name)
        self.host.set(source_model.host)
        self.port.set(source_model.port)
        self.user.set(source_model.user)
        self.password.set(source_model.password)
        self.database.set(source_model.database)
        self.url.set(source_model.url)

    def on_dbtype_selected(self, *args):
        pass

    def init_entries(self, mainframe):
        ttk.Label(mainframe, text='名称：').grid(row=1, column=0, sticky=(W, E))
        self.name_entry = ttk.Entry(mainframe, textvariable=self.name)
        self.name_entry.grid(row=1, column=1, sticky=(W, E))
        ttk.Label(mainframe, text='IP：').grid(row=2, column=0, sticky=(W, E))
        self.host_entry = ttk.Entry(mainframe, textvariable=self.host)
        self.host_entry.grid(row=2, column=1, sticky=(W, E))
        ttk.Label(mainframe, text='端口：').grid(row=3, column=0, sticky=(W, E))
        self.port_entry = ttk.Entry(mainframe, textvariable=self.port)
        self.port_entry.grid(row=3, column=1, sticky=(W, E))
        ttk.Label(mainframe, text='用户：').grid(row=4, column=0, sticky=(W, E))
        self.user_entry = ttk.Entry(mainframe, textvariable=self.user)
        self.user_entry.grid(row=4, column=1, sticky=(W, E))
        ttk.Label(mainframe, text='密码：').grid(row=5, column=0, sticky=(W, E))
        self.pwd_entry = ttk.Entry(mainframe, textvariable=self.password)
        self.pwd_entry.grid(row=5, column=1, sticky=(W, E))
        ttk.Label(mainframe, text='数据库：').grid(row=6, column=0, sticky=(W, E))
        self.db_entry = ttk.Entry(mainframe, textvariable=self.database)
        self.db_entry.grid(row=6, column=1, sticky=(W, E))
        ttk.Label(mainframe, text='URL：').grid(row=7, column=0, sticky=(W, E))
        self.url_entry = ttk.Entry(mainframe, textvariable=self.url, width=28)
        self.url_entry.grid(row=7, column=1, sticky=(W, E))

        self.hint_label = ttk.Label(mainframe, textvariable=self.conn_hint)
        self.hint_label.grid(row=8, column=1, sticky=(N, W, E, S))
        self.hint_label.grid_remove()

        # 默认mysql数据源
        if self.opt == 'add':
            self.host.set('localhost')
            self.port.set('3306')
            self.url.set('jdbc:mysql://localhost:3306/')

        self.host.trace_add('write', self.text_written)
        self.port.trace_add('write', self.text_written)
        self.database.trace_add('write', self.text_written)

    def text_written(self, *args):
        box_db_type = self.db_box.get()
        dbtype = box_db_type.lower()
        host = self.host_entry.get()
        port = self.port_entry.get()
        db = self.db_entry.get()
        self.url.set(f'jdbc:{dbtype}://{host}:{port}/{db}')

    def close_window(self, *args):
        self.win.destroy()

    def init_buttons(self, mainframe):
        pass
