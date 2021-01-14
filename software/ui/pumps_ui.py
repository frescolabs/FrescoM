import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
from ui.pump_ui import Pump
import _thread


class Pumps(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.init_ui()

    def init_ui(self):
        set_position_label = tk.Label(self, text='Pumps control')
        set_position_label.place(x=10, y=0)

        for pump_index in range(0, 7):
            pump = Pump(self, fresco_xyz=self.fresco_xyz, index=pump_index)
            pump.place(x=0 + 50 * pump_index, y=40)

