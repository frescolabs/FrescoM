import tkinter as tk
from tkinter.ttk import Frame, Label
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
import _thread
import time


class AllWellsPhotoUI(Frame):

    def __init__(self, master, fresco_xyz: FrescoXYZ, z_camera: ZCamera):
        super().__init__(master=master, height=500, width=500)
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.init_ui()
        number_of_steps_in_2_pi = 200 * 8
        rod_length_for_one_rotation = 8.0  # in mm
        distance_between_well_centers = 9.0 # in mm
        self.well_step = (distance_between_well_centers / rod_length_for_one_rotation) * number_of_steps_in_2_pi  # todo: fix, calculate in a more smart way (1800)
        print('well step ' + str(self.well_step))
        self.plate_size = (12, 8)  # todo: make editable with UI
        self.pump_index = 1  # todo: fix, temp solution, number of used  pump should be taken from protocol
        self.manifold_offset = 5900  # todo: setup actual number
        self.solution_portion_in_steps = 50  # todo: make customizable

    def init_ui(self):
        start_all_wells_photo_button = tk.Button(self,
                                                 text="Start All Wells Photo",
                                                 command=self.start_all_wells_photo_thread)
        start_all_wells_photo_button.place(x=0, y=30)
        # todo: add ui for choosing folder

    def start_all_wells_photo_thread(self):
        _thread.start_new_thread(self.start_all_wells_photo, ())

    def hold_position(self, millis):
        time.sleep(millis)

    def start_all_wells_photo(self):
        self.fresco_xyz.white_led_switch(True)
        self.fresco_xyz.go_to_zero_manifold()
        for column_number in range(0, self.plate_size[1]):
            for row_number in range(0, self.plate_size[0]):
                self.z_camera.focus_on_current_object()
                self.hold_position(1)
                image_before_solution = self.z_camera.fresco_camera.get_current_image()
                self.save_image(image_before_solution, 'PI_b_' + str(row_number) + '_' + str(column_number))
                self.fresco_xyz.manifold_delta(self.manifold_offset)
                self.fresco_xyz.delta_pump(self.pump_index, self.solution_portion_in_steps)
                self.fresco_xyz.manifold_delta(-1 * self.manifold_offset)
                self.z_camera.focus_on_current_object()
                self.hold_position(1)
                image_after_solution = self.z_camera.fresco_camera.get_current_image()
                self.save_image(image_after_solution, 'PI_a_' + str(row_number) + '_' + str(column_number))
                self.fresco_xyz.delta(-1 * self.well_step, 0, 0)
            self.fresco_xyz.delta(self.well_step * self.plate_size[0], 0, 0)
            self.fresco_xyz.delta(0, -1 * self.well_step, 0)

    def save_image(self, image, name: str):
        # todo: save image
        pass
