from tkinter import *
from tkinter import ttk, messagebox

from dao.db_init_dao import DBInitDao
from dao.db_source_dao import DBSourceDao
from ui.win_db_mgmt import DataSourceMgmtWindow
from ui.win_table_choice import TableChoiceWindow
from utils.window_util import WindowUtil


class HomeWindow:
    def __init__(self, root):
        self.win = root
        self.source_dao = DBSourceDao()
        self.tree = None
        root.title("MyBatis代码生成器")
        # root.geometry(f'500x500')
        mainframe = ttk.Frame(root, padding="10")
        mainframe.grid(sticky=(N, W, E, S))
        ttk.Label(mainframe, text="数据源：").grid(column=0, row=0, sticky=W)
        self.init_treeview(mainframe)
        self.init_buttons(mainframe)
        # 用于判断列表是否需要刷新
        self.init = True
        mainframe.bind("<FocusIn>", self.on_focus_in)

    def on_focus_in(self, *args):
        if self.init is False:
            self.refresh_treeview()

    def refresh_treeview(self):
        self.clear_treeview()
        self.fill_treeview()

    def clear_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def fill_treeview(self):
        src_list = self.source_dao.get_db_source_list()
        for db_src in src_list:
            db_id = db_src[0]
            db_name = db_src[1]
            db_type = db_src[8]
            self.tree.insert('', 'end', db_id, text='', values=(db_name, db_type))

        self.tree.bind('<Double-1>', self.on_item_double_clicked)

    def init_treeview(self, root):
        self.tree = ttk.Treeview(root)
        # 去除最左边空白列
        self.tree['show'] = 'headings'
        self.tree.grid(column=0, row=1, )
        self.tree['columns'] = ('name', 'type')
        self.tree.column('name', width=300, anchor='center')
        self.tree.column('type', width=100, anchor='center')
        self.tree.heading('name', text='名称')
        self.tree.heading('type', text='类型')

        self.fill_treeview()

    def on_item_double_clicked(self, *args):
        self.go_table_page()


    def init_buttons(self, mainframe):
        btn_frame = ttk.Frame(mainframe)
        btn_frame.grid(column=1, row=1, sticky=(N, W, E, S))
        ttk.Button(btn_frame, text="新增", command=self.add_source).grid(column=0, row=0, pady=0,)
        ttk.Button(btn_frame, text="修改", command=self.edit_source).grid(column=0, row=1, pady=0,)
        ttk.Button(btn_frame, text="删除", command=self.del_source).grid(column=0, row=2, pady=0,)

    def add_source(self):
        self.init = False
        sss = DataSourceMgmtWindow(root)
        sss.show()

    def edit_source(self):
        self.init = False
        sel_item_id = self.tree.focus()
        if len(sel_item_id) == 0:
            messagebox.showinfo(title='提示', message='请选择一条记录')
            return
        src_model = self.source_dao.get_db_src_by_id(sel_item_id)
        if src_model is None:
            return
        sss = DataSourceMgmtWindow(root)
        sss.edit_window(src_model)

    def del_source(self):
        self.init = False
        sel_item_id = self.tree.focus()
        if len(sel_item_id) == 0:
            messagebox.showinfo(title='提示', message='请选择一条记录')
            return
        self.source_dao.del_db_src_by_id(sel_item_id)
        index = self.tree.selection()
        self.tree.delete(index)

    def go_table_page(self):
        sel_item_id = self.tree.focus()
        if len(sel_item_id) == 0:
            return
        src_model = self.source_dao.get_db_src_by_id(sel_item_id)
        if src_model is None:
            return
        tb_window = TableChoiceWindow(src_model)
        tb_window.show()


init_dao = DBInitDao()
init_dao.initialize()
root = Tk()
HomeWindow(root)
window_util = WindowUtil(root)
window_util.center_on_screen()
root.mainloop()
