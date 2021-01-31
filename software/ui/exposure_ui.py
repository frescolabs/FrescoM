import tkinter as tk
from tkinter.ttk import Frame, Label, Entry
from services.z_camera import ZCamera


class ExposureUI(Frame):

    def __init__(self, master, z_camera: ZCamera):
        super().__init__(master=master, height=400, width=400)
        self.z_camera = z_camera
        self.exposure_entry: Entry = None
        self.init_ui()

    def init_ui(self):
        set_exposure_label = Label(self, text='Set exposure')
        set_exposure_label.place(x=10, y=0)

        self.exposure_entry = Entry(self)
        self.exposure_entry.place(x=10, y=40)

        save_button = tk.Button(self, text="Set exposure", command=self.set_exposure)
        save_button.place(x=10, y=80)

        save_button = tk.Button(self, text="Run Auto exposure", command=self.run_auto_exposure)
        save_button.place(x=10, y=120)

    def set_exposure(self):
        self.z_camera.fresco_camera.set_exposure(int(self.exposure_entry.get()))

    def run_auto_exposure(self):
        self.z_camera.fresco_camera.set_auto_exposure(True)

