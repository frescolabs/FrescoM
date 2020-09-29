import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
import _thread


class SetGlobalPosition(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.x_entry = None
        self.y_entry = None
        self.init_ui()

    def init_ui(self):
        set_position_label = tk.Label(self, text='Set global position (Plate coordinates should be set)')
        set_position_label.place(x=10, y=0)

        x_label = tk.Label(self, text='x')
        x_label.place(x=10, y=20)

        self.x_entry = tk.Entry(self)
        self.x_entry.place(x=40, y=20)

        y_label = tk.Label(self, text='y')
        y_label.place(x=10, y=50)
        self.y_entry = tk.Entry(self)
        self.y_entry.place(x=40, y=50)

        set_position_button = tk.Button(self, text="Set position", command=self.set_global_position)
        set_position_button.place(x=10, y=90)

    def set_global_position(self):
        x_value = int(self.x_entry.get())
        y_value = int(self.y_entry.get())
        print(x_value)
        print(y_value)
        #TODO: fix protocol of setting abs position (empty values)
        _thread.start_new_thread(self.fresco_xyz.set_position, (x_value, y_value, -1000, 3))
