import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
import _thread


class Initialization(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.plate_coordinates_label = None
        self.init_ui()

    def init_ui(self):
        initialization_label = Label(self, text='Initialization')
        initialization_label.grid(column=0, row=0, ipadx=2, pady=2, sticky=tk.W)

        remember_top_left_position_button = tk.Button(self,
                                                      text='Remember top left position',
                                                      command=self.remember_top_left_position)
        remember_top_left_position_button.grid(column=0, row=1, ipadx=2, pady=2, sticky=tk.W)

        remember_bottom_right_position_button = tk.Button(self,
                                                          text='Remember bottom right position',
                                                          command=self.remember_bottom_right_position)
        remember_bottom_right_position_button.grid(column=0, row=2, ipadx=2, pady=2, sticky=tk.W)

        sync_plate_coordinates_button = tk.Button(self,
                                                  text="Sync plate coordinates",
                                                  command=self.sync_plate_coordinates)
        sync_plate_coordinates_button.grid(column=0, row=3, ipadx=2, pady=2, sticky=tk.W)

        self.plate_coordinates_label = Label(self, text='(0, 0) , (0, 0)')
        self.plate_coordinates_label.grid(column=0, row=4, ipadx=2, pady=2, sticky=tk.W)

    def remember_top_left_position(self):
        _thread.start_new_thread(self.fresco_xyz.remember_top_left_position, ())

    def remember_bottom_right_position(self):
        _thread.start_new_thread(self.fresco_xyz.remember_bottom_right_position, ())

    def sync_plate_coordinates_async(self):
        _thread.start_new_thread(self.sync_plate_coordinates())

    def sync_plate_coordinates(self):
        self.fresco_xyz.update_top_left_bottom_right()
        coordinates_text = '({}, {}), ({}, {})'.format(str(self.fresco_xyz.topLeftPosition[0]),
                                                       str(self.fresco_xyz.topLeftPosition[1]),
                                                       str(self.fresco_xyz.bottomRightPosition[0]),
                                                       str(self.fresco_xyz.bottomRightPosition[1]))

        self.plate_coordinates_label.config(text=coordinates_text)
        self.plate_coordinates_label.update_idletasks()
