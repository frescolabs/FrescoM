import tkinter as tk
from tkinter import BOTH, Tk
from tkinter.ttk import Frame, Label, Style
from fresco_xyz import FrescoXYZ
from z_camera import ZCamera
from fresco_camera import FrescoCamera
from PIL import Image, ImageTk
import _thread

class MainUI(Frame):

    def __init__(self, fresco_xyz: FrescoXYZ, z_camera: ZCamera, fresco_camera: FrescoCamera):
        super().__init__()

        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.fresco_camera = fresco_camera
        self.image_label = None
        image_array = self.fresco_camera.get_current_image()
        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array))
        self.image_label = Label(self, image=camera_image)
        self.image_label.image = camera_image
        self.init_ui()

    def init_ui(self):
        self.master.title("Fresco Labs")
        self.pack(fill=BOTH, expand=1)

        xyz_label = Label(self, text='XYZ Controll')
        xyz_label.place(x=10, y=10)

        x_up_button = tk.Button(self, text="↑", command=self.move_x_up)
        x_up_button.place(x=100, y=50)

        x_down_button = tk.Button(self, text="↓", command=self.move_x_down)
        x_down_button.place(x=100, y=130)

        y_left_button = tk.Button(self, text="←", command=self.move_y_left)
        y_left_button.place(x=50, y=90)

        y_right_button = tk.Button(self, text="→", command=self.move_y_right)
        y_right_button.place(x=150, y=90)

        z_up_button = tk.Button(self, text="↑", command=self.move_z_up)
        z_up_button.place(x=220, y=50)

        z_down_button = tk.Button(self, text="↓", command=self.move_z_down)
        z_down_button.place(x=220, y=130)

        self.image_label.place(x=300, y=50)
        self.after(2000, self.update_image)

        xyz_label = Label(self, text='Functions')
        xyz_label.place(x=10, y=180)

        set_global_position_button = tk.Button(self, text='Set Global Position')
        set_global_position_button.place(x=50, y=220)

        go_to_zero_button = tk.Button(self, text='Go to zero')
        go_to_zero_button.place(x=50, y=260)

        go_to_zero_z_button = tk.Button(self, text='Go to zero Z')
        go_to_zero_z_button.place(x=50, y=300)

        save_current_image_button = tk.Button(self, text='Save current image')
        save_current_image_button.place(x=50, y=340)

        auto_focus_button = tk.Button(self, text='Autofocus')
        auto_focus_button.place(x=50, y=380)

    def move_x_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (10, 0, 0, 0.5))

    def move_x_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (-10, 0, 0, 0.5))

    def move_y_left(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 10, 0, 0.5))

    def move_y_right(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, -10, 0, 0.5))

    def move_z_up(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, -5, 0.5))

    def move_z_down(self):
        _thread.start_new_thread(self.fresco_xyz.delta, (0, 0, 5, 0.5))

    def update_image(self):
        image_array = self.fresco_camera.get_current_image()
        camera_image = ImageTk.PhotoImage(image=Image.fromarray(image_array))
        self.image_label.configure(image=camera_image)
        self.image_label.image = camera_image
        self.after(100, self.update_image)


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
