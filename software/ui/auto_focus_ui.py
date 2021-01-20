import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
import _thread


class AutoFocus(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ, z_camera: ZCamera):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.init_ui()

    def init_ui(self):
        auto_focus_label = Label(self, text='Auto focus')
        auto_focus_label.grid(column=0, row=0, ipadx=2, pady=2, sticky=tk.W)

        auto_focus_button = tk.Button(self, text='Focus', command=self.auto_focus)
        auto_focus_button.grid(column=0, row=1, ipadx=2, pady=2, sticky=tk.W)

        remember_anchor_focus_button = tk.Button(self, text='Remember anchor focus')
        remember_anchor_focus_button.grid(column=0, row=2, ipadx=2, pady=2, sticky=tk.W)

    def auto_focus(self):
        _thread.start_new_thread(self.z_camera.focus_on_current_object, ())