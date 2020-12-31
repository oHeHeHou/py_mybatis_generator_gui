class WindowUtil:

    def __init__(self, window):
        self.window = window

    def get_screen_size(self):
        return self.window.winfo_screenwidth(), self.window.winfo_screenheight()

    def get_screen_width(self):
        return self.window.winfo_screenwidth()

    def get_screen_height(self):
        return self.window.winfo_screenheight()

    def center_on_screen(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.get_screen_width()
        screen_height = self.get_screen_height()
        x_coordinate = int(screen_width / 2 - width / 2)
        y_coordinate = int(screen_height / 2 - height / 2)
        self.window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def disable_resize(self):
        self.window.resizable(0, 0)

    def set_size(self, width, height):
        self.window.geometry(f"{width}x{height}")
