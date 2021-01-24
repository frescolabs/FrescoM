import tkinter as tk
from tkinter.ttk import Frame, Label
from tkinter import Toplevel
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from ui.set_global_position_ui import SetGlobalPosition
from ui.pumps_ui import Pumps
from ui.save_image_ui import SaveImage
import _thread


class Functions(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ, z_camera: ZCamera):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.init_ui()
        self.white_led_state = False
        self.blue_led_state = False

    def init_ui(self):
        xyz_label = Label(self, text='Functions')
        xyz_label.grid(column=0, row=0, ipadx=2, pady=2, sticky=tk.W)

        set_global_position_button = tk.Button(self, text='Set Global Position',
                                               command=self.open_set_global_position_dialog)
        set_global_position_button.grid(column=0, row=1, ipadx=2, pady=2, sticky=tk.W)

        save_current_image_button = tk.Button(self, text='Save current image', command=self.save_current_image)
        save_current_image_button.grid(column=0, row=2, ipadx=2, pady=2, sticky=tk.W)

        all_wells_photo_button = tk.Button(self, text='All wells photo')
        all_wells_photo_button.grid(column=0, row=3, ipadx=2, pady=2, sticky=tk.W)

        segment_current_image_button = tk.Button(self, text='Segment current image')
        segment_current_image_button.grid(column=0, row=4, ipadx=2, pady=2, sticky=tk.W)

        white_led_button = tk.Button(self, text='White LED on / off',
                                     command=self.switch_white_led)
        white_led_button.grid(column=0, row=5, ipadx=2, pady=2, sticky=tk.W)

        blue_led_button = tk.Button(self, text='Blue LED on / off',
                                    command=self.switch_blue_led)
        blue_led_button.grid(column=0, row=6, ipadx=2, pady=2, sticky=tk.W)

        pumps_button = tk.Button(self, text='Pumps', command=self.open_pumps)
        pumps_button.grid(column=0, row=7, ipadx=2, pady=2, sticky=tk.W)

    def switch_white_led(self):
        self.white_led_state = not self.white_led_state
        self.fresco_xyz.white_led_switch(self.white_led_state)

    def switch_blue_led(self):
        self.blue_led_state = not self.blue_led_state
        self.fresco_xyz.blue_led_switch(self.blue_led_state)

    def open_set_global_position_dialog(self):
        new_window = Toplevel(self)
        new_window.title("Set global position")
        new_window.geometry("400x250")
        SetGlobalPosition(new_window,
                          fresco_xyz=self.fresco_xyz).pack()

    def open_pumps(self):
        new_window = Toplevel(self)
        new_window.title("Pumps")
        new_window.geometry("400x250")
        Pumps(new_window, fresco_xyz=self.fresco_xyz).pack()

    def save_current_image(self):
        image = self.z_camera.fresco_camera.get_current_image()
        new_window = Toplevel(self)
        new_window.title("Image")
        new_window.geometry("800x800")
        SaveImage(new_window, image=image).pack()
