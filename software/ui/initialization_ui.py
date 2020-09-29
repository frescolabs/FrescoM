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
        initialization_label.place(x=10, y=0)

        remember_top_left_position_button = tk.Button(self,
                                                      text='Remember top left position',
                                                      command=self.remember_top_left_position)
        remember_top_left_position_button.place(x=50, y=20)

        remember_bottom_right_position_button = tk.Button(self,
                                                          text='Remember bottom right position',
                                                          command=self.remember_bottom_right_position)
        remember_bottom_right_position_button.place(x=50, y=60)

        sync_plate_coordinates_button = tk.Button(self,
                                                  text="Sync plate coordinates",
                                                  command=self.sync_plate_coordinates)
        sync_plate_coordinates_button.place(x=50, y=100)

        self.plate_coordinates_label = Label(self, text='(0, 0) , (0, 0)')
        self.plate_coordinates_label.place(x=50, y=140)

    def remember_top_left_position(self):
        _thread.start_new_thread(self.fresco_xyz.remember_top_left_position, (5,))

    def remember_bottom_right_position(self):
        _thread.start_new_thread(self.fresco_xyz.remember_bottom_right_position, (5,))

    def sync_plate_coordinates_async(self):
        _thread.start_new_thread(self.sync_plate_coordinates())

    def sync_plate_coordinates(self):
        self.fresco_xyz.update_top_left_bottom_right(0.5)
        coordinates_text = '({}, {}), ({}, {})'.format(str(self.fresco_xyz.topLeftPosition[0]),
                                                     str(self.fresco_xyz.topLeftPosition[1]),
                                                     str(self.fresco_xyz.bottomRightPosition[0]),
                                                     str(self.fresco_xyz.bottomRightPosition[1]))

        self.plate_coordinates_label.config(text=coordinates_text)
        self.plate_coordinates_label.update_idletasks()
