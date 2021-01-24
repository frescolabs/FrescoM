from services.fresco_camera import FrescoCamera
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from ui.fresco_ui import MainUI
from tkinter import BOTH, Tk, Scrollbar
from tkinter.ttk import Frame, Label

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
