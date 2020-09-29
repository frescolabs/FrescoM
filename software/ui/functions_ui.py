import tkinter as tk
from tkinter.ttk import Frame, Label
from tkinter import Toplevel
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from ui.set_global_position_ui import SetGlobalPosition
import _thread


class Functions(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ, z_camera: ZCamera):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.init_ui()

    def init_ui(self):
        xyz_label = Label(self, text='Functions')
        xyz_label.place(x=10, y=0)

        set_global_position_button = tk.Button(self, text='Set Global Position',
                                               command=self.open_set_global_position_dialog)
        set_global_position_button.place(x=50, y=20)

        go_to_zero_z_button = tk.Button(self, text='Go to zero Z')
        go_to_zero_z_button.place(x=50, y=60)

        save_current_image_button = tk.Button(self, text='Save current image')
        save_current_image_button.place(x=50, y=100)

        all_wells_photo_button = tk.Button(self, text='All wells photo')
        all_wells_photo_button.place(x=50, y=140)

        segment_current_image_button = tk.Button(self, text='Segment current image')
        segment_current_image_button.place(x=50, y=180)

    def open_set_global_position_dialog(self):
        newWindow = Toplevel(self)
        newWindow.title("Set global position")
        newWindow.geometry("400x250")
        SetGlobalPosition(newWindow,
                          fresco_xyz=self.fresco_xyz).pack()