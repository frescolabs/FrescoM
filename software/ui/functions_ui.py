import tkinter as tk
from tkinter.ttk import Frame, Label
from tkinter import Toplevel

from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.protocols_performer import ProtocolsPerformer
from services.images_storage import ImagesStorage

from ui.set_global_position_ui import SetGlobalPosition
from ui.pumps_ui import Pumps
from ui.save_image_ui import SaveImage
from ui.protocols_performer_ui import ProtocolsPerformerUI
from ui.exposure_ui import ExposureUI


class Functions(Frame):

    def __init__(self,
                 master,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 protocols_performer: ProtocolsPerformer,
                 images_storage: ImagesStorage):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.protocols_performer = protocols_performer
        self.images_storage = images_storage
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

        white_led_button = tk.Button(self, text='White LED on / off',
                                     command=self.switch_white_led)
        white_led_button.grid(column=0, row=3, ipadx=2, pady=2, sticky=tk.W)

        blue_led_button = tk.Button(self, text='Blue LED on / off',
                                    command=self.switch_blue_led)
        blue_led_button.grid(column=0, row=4, ipadx=2, pady=2, sticky=tk.W)

        pumps_button = tk.Button(self, text='Pumps', command=self.open_pumps)
        pumps_button.grid(column=0, row=5, ipadx=2, pady=2, sticky=tk.W)

        protocols_performer_button = tk.Button(self,
                                               text='Protocols performer',
                                               command=self.open_protocols_performer)
        protocols_performer_button.grid(column=0, row=6, ipadx=2, pady=2, sticky=tk.W)

        exposure_button = tk.Button(self,
                                    text='Exposure',
                                    command=self.open_exposure)
        exposure_button.grid(column=0, row=7, ipadx=2, pady=2, sticky=tk.W)

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
        SaveImage(new_window, image=image, images_storage=self.images_storage).pack()

    def open_protocols_performer(self):
        new_window = Toplevel(self)
        new_window.title("Protocols performer")
        new_window.geometry("400x250")
        ProtocolsPerformerUI(new_window, protocols_performer=self.protocols_performer).pack()

    def open_exposure(self):
        new_window = Toplevel(self)
        new_window.title("Exposure")
        new_window.geometry("400x250")
        ExposureUI(new_window, z_camera=self.z_camera).pack()
