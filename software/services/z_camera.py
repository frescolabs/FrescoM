import operator
from services.fresco_xyz import FrescoXYZ
from services.focus_measure import FocusMeasure
from services.fresco_camera import Camera
import time

class ZCamera:

    def __init__(self, fresco_xyz: FrescoXYZ, fresco_camera: Camera):
        self.frescoXYZ = fresco_xyz
        self.fresco_camera = fresco_camera
        self.focus_measure = FocusMeasure()
        self.auto_focus_anchor = -9630
        self.auto_focus_delta_number_of_steps = 20
        self.one_step = 5
        self.current_position = None

    def z_step_up(self):
        delta = -1 * self.one_step
        self.frescoXYZ.delta(0, 0, delta)

    def z_step_down(self):
        self.frescoXYZ.delta(0, 0, self.one_step)

    def z_step_down_number(self, number):
        self.frescoXYZ.delta(0, 0, self.one_step * number)

    def z_go_to_zero(self):
        self.frescoXYZ.go_to_zero_z()
        self.frescoXYZ.delta(0,
                             0,
                             self.auto_focus_anchor + self.auto_focus_delta_number_of_steps / 2)

    def update_auto_focus_anchor(self, steps):
        self.auto_focus_anchor = steps

    def update_current_z_position(self, steps):
        self.current_position = steps

    def update_current_z_position_delta(self, delta_steps):
        self.current_position += delta_steps

    def focus_on_current_object(self):
        self.z_go_to_zero()
        focus_measure_data_points = []
        for i in range(1, self.auto_focus_delta_number_of_steps):
            pixels_array = self.fresco_camera.get_current_image()
            measure = self.get_focus_measure(pixels_array)
            focus_measure_data_points.append(measure)
            self.z_step_up()
            time.sleep(0.2)
        max_index, max_value = max(enumerate(focus_measure_data_points), key=operator.itemgetter(1))
        number_of_steps_back = self.auto_focus_delta_number_of_steps - max_index + 2
        self.z_step_down_number(number_of_steps_back)

    def get_focus_measure(self, pixels_array):
        measure = self.focus_measure.TENG(pixels_array)
        return measure

