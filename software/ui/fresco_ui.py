from tkinter import BOTH, Tk
import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.fresco_camera import FrescoCamera
from PIL import Image, ImageTk
from tkinter import Toplevel

from ui.steps_manual_controller_ui import StepsManualController
from ui.macro_steps_manual_controller_ui import MacroStepsManualController
from ui.initialization_ui import Initialization
from ui.auto_focus_ui import AutoFocus
from ui.functions_ui import Functions
from ui.serial_connection_ui import SerialConnectionView

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure


class MainUI(Frame):

    def __init__(self, fresco_xyz: FrescoXYZ, z_camera: ZCamera, fresco_camera: FrescoCamera):
        super().__init__()
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.fresco_camera = fresco_camera
        self.image_label = None
        self.number_of_focus_measures_to_show = 50
        self.focus_measures = [0]
        self.init_ui()

    def init_ui(self):
        self.master.title("Fresco Labs")

        self.pack(fill=BOTH, expand=1)

        steps_manual_controller = StepsManualController(self, fresco_xyz=self.fresco_xyz)
        steps_manual_controller.place(x=0, y=0)

        macro_steps_controller = MacroStepsManualController(self, fresco_xyz=self.fresco_xyz)
        macro_steps_controller.place(x=0, y=130)

        initialization_controller = Initialization(self, fresco_xyz=self.fresco_xyz)
        initialization_controller.place(x=0, y=300)

        auto_focus_controller = AutoFocus(self, fresco_xyz=self.fresco_xyz, z_camera=self.z_camera)
        auto_focus_controller.place(x=0, y=420)

        functions_controller = Functions(self, fresco_xyz=self.fresco_xyz, z_camera=self.z_camera)
        functions_controller.place(x=0, y=520)

        serial_port_controll_button = tk.Button(self, text='Serial', command=self.open_serial_connection_ui)
        serial_port_controll_button.place(x=300, y=0)

        image_array = self.fresco_camera.get_current_image()
        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array).resize((800, 800),Image.ANTIALIAS))
        self.image_label = Label(self, image=camera_image)
        self.image_label.image = camera_image
        self.image_label.place(x=300, y=30)

        # Uncomment to debug focus measure
        # self.fig = Figure(figsize=(5, 4), dpi=100)
        # self.subplot = self.fig.add_subplot(111)
        # self.subplot.plot(self.focus_measures)
        # self.fig.set_label('Focus measure')


        # canvas = FigureCanvasTkAgg(self.fig, master=self)
        # canvas.draw()
        # canvas.get_tk_widget().place(x=1700, y=50)

        self.after(2000, self.update_image)

    def update_image(self):
        image_array = self.fresco_camera.get_current_image()

        # Uncomment to debug focus measure
        # measure = self.z_camera.get_focus_measure(image_array)
        # self.add_measure(measure)
        # self.fig.clf()
        # self.subplot = self.fig.add_subplot(111)
        # self.subplot.plot(self.focus_measures)
        # self.fig.canvas.draw()

        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array).resize((800, 800),Image.ANTIALIAS))
        self.image_label.configure(image=camera_image)
        self.image_label.image = camera_image

        self.after(100, self.update_image)

    def add_measure(self, measure):
        if len(self.focus_measures) >= self.number_of_focus_measures_to_show:
            self.focus_measures.pop(0)
        self.focus_measures.append(measure)

    def open_serial_connection_ui(self):
        new_window = Toplevel(self)
        new_window.title("Serial connection")
        new_window.geometry("400x250")
        SerialConnectionView(new_window).pack()


def main():
    fresco_xyz = FrescoXYZ()
    fresco_camera = FrescoCamera()
    z_camera = ZCamera(fresco_xyz, fresco_camera)

    root = Tk()
    root.geometry("1800x1200+300+300")
    app = MainUI(fresco_xyz, z_camera, fresco_camera)
    root.mainloop()


if __name__ == '__main__':
    main()
