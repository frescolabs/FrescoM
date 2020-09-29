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
        auto_focus_label.place(x=10, y=0)

        auto_focus_button = tk.Button(self, text='Focus', command=self.auto_focus)
        auto_focus_button.place(x=50, y=30)

        remember_anchor_focus_button = tk.Button(self, text='Remember anchor focus')
        remember_anchor_focus_button.place(x=50, y=70)

    def auto_focus(self):
        _thread.start_new_thread(self.z_camera.focus_on_current_object, ())