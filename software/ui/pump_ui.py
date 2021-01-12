import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
import _thread


class Pump(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ, index):
        super().__init__(master=master, height=110, width=50)
        self.fresco_xyz = fresco_xyz
        self.index = index
        self.init_ui()

    def init_ui(self):
        x_label = tk.Label(self, text='Pump' + str(self.index))
        x_label.place(x=0, y=10)

        set_position_button = tk.Button(self, text="↑", command=self.move_pump_forward)
        set_position_button.place(x=0, y=30)

        set_position_button = tk.Button(self, text="↓", command=self.move_pump_back)
        set_position_button.place(x=0, y=70)

    def move_pump_forward(self):
        _thread.start_new_thread(self.fresco_xyz.delta_pump, (self.index, 100, 0.5))

    def move_pump_back(self):
        _thread.start_new_thread(self.fresco_xyz.delta_pump, (self.index, -100, 0.5))