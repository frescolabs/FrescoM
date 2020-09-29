import operator
from services.fresco_xyz import FrescoXYZ
from services.focus_measure import FocusMeasure
from services.fresco_camera import Camera


class ZCamera:

    def __init__(self, fresco_xyz: FrescoXYZ, fresco_camera: Camera):
        self.frescoXYZ = fresco_xyz
        self.fresco_camera = fresco_camera
        self.focus_measure = FocusMeasure()
        self.auto_focus_anchor = -9540
        self.auto_focus_delta_number_of_steps = 20
        self.one_step = 5

    def z_step_up(self):
        self.frescoXYZ.delta(0, 0, -1 * self.one_step, 0.3)

    def z_step_down(self):
        self.frescoXYZ.delta(0, 0, self.one_step, 0.3)

    def z_step_down_number(self, number):
        self.frescoXYZ.delta(0, 0, self.one_step * number, 1)

    def z_go_to_zero(self):
        self.frescoXYZ.go_to_zero_z(4)
        self.frescoXYZ.delta(0,
                             0,
                             self.auto_focus_anchor + self.auto_focus_delta_number_of_steps / 2,
                             4)

    def focus_on_current_object(self):
        self.z_go_to_zero()
        focus_measure_data_points = []
        for i in range(1, self.auto_focus_delta_number_of_steps):
            pixels_array = self.fresco_camera.get_current_image()
            measure = self.focus_measure.TENG(pixels_array)
            focus_measure_data_points.append(measure)
            self.z_step_up()
        max_index, max_value = max(enumerate(focus_measure_data_points), key=operator.itemgetter(1))
        number_of_steps_back = self.auto_focus_delta_number_of_steps - max_index - 1
        self.z_step_down_number(number_of_steps_back)

