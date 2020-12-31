from tkinter import *
from tkinter import ttk, filedialog

from dao.output_config_dao import OutputConfigDao
from model.output_config_model import OutputConfigModel
from utils.window_util import WindowUtil


class ConfigWindow:

    def __init__(self, root):
        self.root = root
        self.win = None
        self.path_model = None
        self.path_xml = None
        self.path_mapper = None

        self.model_entry = None
        self.xml_entry = None
        self.mapper_entry = None
        self.out_dir_entry = None
        self.opt = 'add'

        self.config_dao = OutputConfigDao()

        self.src_id = None

    def show(self, src_model):
        self.src_id = src_model.id
        window = Tk()
        self.win = window
        window.title("设置输出目录")
        window_util = WindowUtil(window)
        # w,h
        window_util.set_size(380, 280)
        window_util.disable_resize()
        window_util.center_on_screen()

        mainframe = ttk.Frame(window, padding=10)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.init_entries(mainframe)
        self.complete_entries(mainframe)

    def init_entries(self, mainframe):
        ttk.Label(mainframe, text='Model包名：').grid(row=0, column=0, sticky=(W, E), pady=10)
        self.model_entry = ttk.Entry(mainframe, width=25)
        self.model_entry.grid(row=0, column=1, sticky=(W, E), columnspan=2, pady=10)
        ttk.Label(mainframe, text='SqlMap包名：').grid(row=1, column=0, sticky=(W, E), pady=10)
        self.xml_entry = ttk.Entry(mainframe, )
        self.xml_entry.grid(row=1, column=1, sticky=(W, E), columnspan=2, pady=10)
        ttk.Label(mainframe, text='Mapper包名：').grid(row=2, column=0, sticky=(W, E), pady=10)
        self.mapper_entry = ttk.Entry(mainframe, )
        self.mapper_entry.grid(row=2, column=1, sticky=(W, E), columnspan=2, pady=10)

        ttk.Label(mainframe, text='输出路径：').grid(row=3, column=0, sticky=(W, E))
        self.out_dir_entry = ttk.Entry(mainframe)
        self.out_dir_entry.grid(row=3, column=1, sticky=(W, E), columnspan=2)
        ttk.Button(mainframe, text="...", width=5, command=self.browse_files).grid(row=3, column=3,
                                                                                   sticky=(W,))

        ttk.Button(mainframe, text="确定", width=12, command=self.save_config).grid(
            row=4, column=1, sticky=W, pady=20)
        ttk.Button(mainframe, text="清空", width=12, command=self.clear_config).grid(
            row=4, column=2, sticky=W, pady=20)

        if self.opt == 'edit':
            # self.out_dir_entry.insert(0, filename)
            pass

    def complete_entries(self, mainframe):
        config = self.config_dao.get_by_id(self.src_id)
        if config:
            self.opt = 'edit'
            self.model_entry.insert(0, config.model_pkg)
            self.xml_entry.insert(0, config.sql_map_pkg)
            self.mapper_entry.insert(0, config.mapper_pkg)
            self.out_dir_entry.insert(0, config.out_dir)
        else:
            self.opt = 'add'
            self.model_entry.insert(0, 'com.frontier.model')
            self.xml_entry.insert(0, 'com.frontier.config.mapper')
            self.mapper_entry.insert(0, 'com.frontier.mapper')

    def browse_files(self):
        filename = filedialog.askdirectory(title="选择输出文件夹")
        self.out_dir_entry.delete(0, END)
        self.out_dir_entry.insert(0, filename)
        # 防止关闭文件选择窗口后,被第一个界面遮盖
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.win.lift()
        self.win.attributes('-topmost', True)

    def save_config(self):
        conf_model = OutputConfigModel()
        conf_model.src_id = self.src_id
        conf_model.mapper_pkg = self.mapper_entry.get()
        conf_model.model_pkg = self.model_entry.get()
        conf_model.out_dir = self.out_dir_entry.get()
        conf_model.sql_map_pkg = self.xml_entry.get()
        if self.opt == 'add':
            self.config_dao.add_config(conf_model)
        else:
            self.config_dao.update(conf_model)

        self.win.destroy()

    def clear_config(self):
        self.mapper_entry.delete(0, END)
        self.model_entry.delete(0, END)
        self.out_dir_entry.delete(0, END)
        self.xml_entry.delete(0, END)
