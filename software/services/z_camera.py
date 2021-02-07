import operator
from services.fresco_xyz import FrescoXYZ
from services.focus_measure import FocusMeasure
from services.fresco_camera import FrescoCamera
import time


class ZCamera:

    def __init__(self, fresco_xyz: FrescoXYZ, fresco_camera: FrescoCamera):
        self.frescoXYZ = fresco_xyz
        self.fresco_camera = fresco_camera
        self.focus_measure = FocusMeasure()
        self.auto_focus_anchor = -9690 # TODO: save from machine state and update
        self.auto_focus_delta_number_of_jumps = 30
        self.one_jump = 5
        self.current_position = None

    def z_step_up(self):
        delta = -1 * self.one_step
        self.frescoXYZ.delta(0, 0, delta)

    def z_step_down(self):
        self.frescoXYZ.delta(0, 0, self.one_jump)

    def z_step_down_number(self, number):
        self.frescoXYZ.delta(0, 0, self.one_jump * number)

    def z_go_to_zero(self):
        self.frescoXYZ.go_to_zero_z()

    def update_auto_focus_anchor(self, steps):
        self.auto_focus_anchor = steps

    def update_current_z_position(self, steps):
        self.current_position = steps

    def update_current_z_position_delta(self, delta_steps):
        self.current_position += delta_steps

    def focus_on_current_object(self):
        self.z_go_to_zero()
        self.frescoXYZ.delta(0, 0, self.auto_focus_anchor + self.auto_focus_delta_number_of_jumps / 2)
        # first focus attempt with big steps
        measure_1, steps_1 = self.find_offset_for_best_measure(one_jump_size=self.one_jump,
                                                               delta_jumps=self.auto_focus_delta_number_of_jumps)
        print('measure_1 = ' + str(measure_1))
        print('steps_1 = ' + str(steps_1))
        self.frescoXYZ.delta(0, 0, steps_1)
        delta_jumps_2 = 10
        jump_size_2 = 2
        self.frescoXYZ.delta(0, 0, (delta_jumps_2 * jump_size_2) / 2)
        # second focus attempt with small steps
        measure_2, steps_2 = self.find_offset_for_best_measure(one_jump_size=jump_size_2,
                                                               delta_jumps=delta_jumps_2)
        print('measure_2 = ' + str(measure_2))
        print('steps_2 = ' + str(steps_2))
        self.frescoXYZ.delta(0, 0, steps_2)

    # starts to find the best focus measure from current position within delta making one_jump_size.
    # returns the best measure and number of steps from final position to the best focus.
    def find_offset_for_best_measure(self, one_jump_size: int, delta_jumps: int) -> (int, int):
        focus_measure_data_points = []
        for jump_index in range(0, delta_jumps):
            pixels_array = self.fresco_camera.get_current_image()
            measure = self.get_focus_measure(pixels_array)
            focus_measure_data_points.append(measure)
            self.frescoXYZ.delta(0, 0, -1 * one_jump_size)
            time.sleep(0.5)
        max_index, max_value = max(enumerate(focus_measure_data_points), key=operator.itemgetter(1))
        number_of_steps_back = (delta_jumps - max_index + 1) * one_jump_size
        return max_value, number_of_steps_back

    def get_focus_measure(self, pixels_array):
        measure = self.focus_measure.measure(pixels_array)
        return measure

