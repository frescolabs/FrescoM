from tkinter import BOTH, Tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.fresco_camera import FrescoCamera
from PIL import Image, ImageTk

from ui.steps_manual_controller_ui import StepsManualController
from ui.macro_steps_manual_controller_ui import MacroStepsManualController
from ui.initialization_ui import Initialization
from ui.auto_focus_ui import AutoFocus
from ui.functions_ui import Functions


class MainUI(Frame):

    def __init__(self, fresco_xyz: FrescoXYZ, z_camera: ZCamera, fresco_camera: FrescoCamera):
        super().__init__()

        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.fresco_camera = fresco_camera
        self.image_label = None

        self.init_ui()

    def init_ui(self):
        self.master.title("Fresco Labs")

        self.pack(fill=BOTH, expand=1)

        steps_manual_controller = StepsManualController(self, fresco_xyz=self.fresco_xyz)
        steps_manual_controller.place(x=0, y=0)

        macro_steps_controller = MacroStepsManualController(self, fresco_xyz=self.fresco_xyz)
        macro_steps_controller.place(x=0, y=200)

        initialization_controller = Initialization(self, fresco_xyz=self.fresco_xyz)
        initialization_controller.place(x=0, y=360)

        auto_focus_controller = AutoFocus(self, fresco_xyz=self.fresco_xyz, z_camera=self.z_camera)
        auto_focus_controller.place(x=0, y=540)

        functions_controller = Functions(self, fresco_xyz=self.fresco_xyz, z_camera=self.z_camera)
        functions_controller.place(x=0, y=640)

        image_array = self.fresco_camera.get_current_image()
        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array))
        self.image_label = Label(self, image=camera_image)
        self.image_label.image = camera_image
        self.image_label.place(x=300, y=50)
        self.after(2000, self.update_image)

    def update_image(self):
        image_array = self.fresco_camera.get_current_image()
        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array))
        self.image_label.configure(image=camera_image)
        self.image_label.image = camera_image
        self.after(10, self.update_image)


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
