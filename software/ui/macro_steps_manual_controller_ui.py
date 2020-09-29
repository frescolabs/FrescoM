import tkinter as tk
from tkinter.ttk import Frame
from services.fresco_xyz import FrescoXYZ
import _thread


class MacroStepsManualController(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ):
        super().__init__(master=master, height=200, width=500)
        self.fresco_xyz = fresco_xyz
        self.init_ui()

    def init_ui(self):
        x_macro_up_button = tk.Button(self, text="↑↑", command=self.move_x_macro_up)
        x_macro_up_button.place(x=100, y=0)

        x_macro_down_button = tk.Button(self, text="↓↓", command=self.move_x_macro_down)
        x_macro_down_button.place(x=100, y=80)

        y_macro_left_button = tk.Button(self, text="←←", command=self.move_y_macro_left)
        y_macro_left_button.place(x=50, y=40)

        y_macro_right_button = tk.Button(self, text="→→", command=self.move_y_macro_right)
        y_macro_right_button.place(x=150, y=40)

        z_up_button = tk.Button(self, text="↑↑", command=self.move_z_macro_up)
        z_up_button.place(x=220, y=0)

        z_down_button = tk.Button(self, text="↓↓", command=self.move_z_macro_down)
        z_down_button.place(x=220, y=80)

        go_to_zero_button = tk.Button(self, text='Go to zero', command=self.go_to_zero)
        go_to_zero_button.place(x=50, y=120)

    def move_x_macro_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (300, 0, 0, 0.5))

    def move_x_macro_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (-300, 0, 0, 0.5))

    def move_y_macro_left(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 300, 0, 0.5))

    def move_y_macro_right(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, -300, 0, 0.5))

    def move_z_macro_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, -300, 0.5))

    def move_z_macro_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, 300, 0.5))

    def go_to_zero(self):
        _thread.start_new_thread(self.fresco_xyz.go_to_zero, (8,))
