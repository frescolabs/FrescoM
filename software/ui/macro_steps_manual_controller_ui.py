import tkinter as tk
from tkinter.ttk import Frame
from services.fresco_xyz import FrescoXYZ
import _thread


class MacroStepsManualController(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ):
        super().__init__(master=master, height=240, width=500)
        self.fresco_xyz = fresco_xyz
        self.number_of_steps_entry: tk.Entry = None
        self.init_ui()

    def init_ui(self):
        x_macro_up_button = tk.Button(self, text="↑↑", command=self.move_x_macro_up)
        x_macro_up_button.grid(row=1, column=1)

        x_macro_down_button = tk.Button(self, text="↓↓", command=self.move_x_macro_down)
        x_macro_down_button.grid(row=3, column=1)

        y_macro_left_button = tk.Button(self, text="←←", command=self.move_y_macro_left)
        y_macro_left_button.grid(row=2, column=0)

        y_macro_right_button = tk.Button(self, text="→→", command=self.move_y_macro_right)
        y_macro_right_button.grid(row=2, column=2)

        z_up_button = tk.Button(self, text="↑↑", command=self.move_z_macro_up)
        z_up_button.grid(row=1, column=3)

        z_down_button = tk.Button(self, text="↓↓", command=self.move_z_macro_down)
        z_down_button.grid(row=3, column=3)

        manifold_up_button = tk.Button(self, text="↑↑", command=self.move_manifold_up)
        manifold_up_button.grid(row=1, column=4)

        manifold_down_button = tk.Button(self, text="↓↓", command=self.move_manifold_down)
        manifold_down_button.grid(row=3, column=4)

        self.number_of_steps_entry = tk.Entry(self)
        self.number_of_steps_entry.grid(sticky=tk.W, row=4, column=0, columnspan=4)
        # default step is 300
        self.number_of_steps_entry.insert(tk.END, '300')

        go_to_zero_button = tk.Button(self, text='Go to zero ZXY', command=self.go_to_zero)
        go_to_zero_button.grid(sticky=tk.W, row=5, column=0, columnspan=4)

        go_to_zero_manifold = tk.Button(self, text='Go to zero Manifold', command=self.go_to_zero_manifold)
        go_to_zero_manifold.grid(sticky=tk.W, row=6, column=0, columnspan=4)

        go_to_zero_z_button = tk.Button(self, text='Go to zero Z', command=self.go_to_zero_z)
        go_to_zero_z_button.grid(sticky=tk.W, row=7, column=0, columnspan=4)

    def current_step_size(self) -> int:
        return int(self.number_of_steps_entry.get())

    def move_x_macro_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (self.current_step_size(), 0, 0, 0.5))

    def move_x_macro_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (-1 * self.current_step_size(), 0, 0, 0.5))

    def move_y_macro_left(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, self.current_step_size(), 0, 0.5))

    def move_y_macro_right(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, -1 * self.current_step_size(), 0, 0.5))

    def move_z_macro_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, -1 * self.current_step_size(), 0.5))

    def move_z_macro_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, self.current_step_size(), 0.5))

    def go_to_zero(self):
        _thread.start_new_thread(self.fresco_xyz.go_to_zero, (8,))

    def go_to_zero_manifold(self):
        _thread.start_new_thread(self.fresco_xyz.go_to_zero_manifold, (2,))

    def go_to_zero_z(self):
        _thread.start_new_thread(self.fresco_xyz.go_to_zero_z, (2,))

    def move_manifold_up(self):
        _thread.start_new_thread(self.fresco_xyz.manifold_delta, (-1 * self.current_step_size(), 0.5))

    def move_manifold_down(self):
        _thread.start_new_thread(self.fresco_xyz.manifold_delta, (self.current_step_size(), 0.5))
