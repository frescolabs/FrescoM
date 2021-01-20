import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
import _thread


class StepsManualController(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ):
        super().__init__(master=master, height=200, width=500)
        self.fresco_xyz = fresco_xyz
        self.init_ui()

    def init_ui(self):
        xyz_label = Label(self, text='XYZ Control, Manifold')
        xyz_label.grid(sticky=tk.W, pady=4, padx=5, columnspan=4)

        x_up_button = tk.Button(self, text="↑", command=self.move_x_up)
        x_up_button.grid(row=1, column=1)

        x_down_button = tk.Button(self, text="↓", command=self.move_x_down)
        x_down_button.grid(row=3, column=1)

        y_left_button = tk.Button(self, text="←", command=self.move_y_left)
        y_left_button.grid(row=2, column=0)

        y_right_button = tk.Button(self, text="→", command=self.move_y_right)
        y_right_button.grid(row=2, column=2)

        z_up_button = tk.Button(self, text="↑", command=self.move_z_up)
        z_up_button.grid(row=1, column=3)

        z_down_button = tk.Button(self, text="↓", command=self.move_z_down)
        z_down_button.grid(row=3, column=3)

        manifold_up_button = tk.Button(self, text="↑", command=self.move_manifold_up)
        manifold_up_button.grid(row=1, column=4)

        manifold_down_button = tk.Button(self, text="↓", command=self.move_manifold_down)
        manifold_down_button.grid(row=3, column=4)

    def move_x_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (10, 0, 0, 0.5))

    def move_x_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (-10, 0, 0, 0.5))

    def move_y_left(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 10, 0, 0.5))

    def move_y_right(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, -10, 0, 0.5))

    def move_z_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, -5, 0.5))

    def move_z_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, 5, 0.5))

    def move_manifold_up(self):
        _thread.start_new_thread(self.fresco_xyz.manifold_delta, (-100, 0.5))

    def move_manifold_down(self):
        _thread.start_new_thread(self.fresco_xyz.manifold_delta, (100, 0.5))


