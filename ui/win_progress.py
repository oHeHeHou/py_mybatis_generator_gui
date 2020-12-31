from tkinter import *
from tkinter import ttk, filedialog

from dao.output_config_dao import OutputConfigDao
from model.output_config_model import OutputConfigModel
from utils.window_util import WindowUtil


class ProgressWindow:

    def __init__(self):
        self.win = None
        self.progress = None

    def show(self):
        window = Tk()
        window.title('提示')
        window_util = WindowUtil(window)
        # w,h
        window_util.set_size(180, 100)
        window_util.disable_resize()
        window_util.center_on_screen()

        self.win = window
        self.init_text(window)
        self.init_progress(window)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

    def stop(self):
        self.win.quit()

    def init_progress(self, par_frame):
        self.progress = ttk.Progressbar(par_frame, orient=HORIZONTAL, length=100)
        self.progress.grid(column=0, row=1, sticky=(E,W))
        self.progress.start()

    def init_text(self, par_frame):
        ttk.Label(par_frame, text='生成中...').grid(row=0, column=0, padx=10, pady=10)
