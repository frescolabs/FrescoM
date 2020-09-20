import operator

from simple_pyspin import Camera
import cv2
from fresco_xyz import FrescoXYZ
from focus_measure import FocusMeasure

class ZCamera:
    one_step = 5

    def __init__(self, fresco_xyz, fesco_camera):
        self.frescoXYZ = fresco_xyz
        self.fresco_camera = fesco_camera
        self.focus_measure = FocusMeasure()

    def z_step_up(self):
        self.frescoXYZ.delta(0, 0, -1 * ZCamera.one_step, 0.5)

    def z_step_down(self):
        self.frescoXYZ.delta(0, 0, ZCamera.one_step, 0.5)

    def z_step_down_number(self, number):
        self.frescoXYZ.delta(0, 0, ZCamera.one_step * number, 1)

    def z_go_to_zero(self):
        self.frescoXYZ.goToZeroZ(4)
        self.frescoXYZ.delta(0, 0, -9200, 4)

    def show(self, pixels_array):
        cv2.imshow('', pixels_array)
        cv2.waitKey(1)

    def focus_on_current_object(self):
        self.z_go_to_zero()
        focus_measure_data_points = []
        number_of_steps = 100
        for i in range(1, number_of_steps):
            pixels_array = self.fresco_camera.get_current_image()
            measure = self.focus_measure.TENG(pixels_array)
            focus_measure_data_points.append(measure)
            self.show(pixels_array)
            print(measure)
            self.z_step_up()
        max_index, max_value = max(enumerate(focus_measure_data_points), key=operator.itemgetter(1))
        number_of_steps_back = number_of_steps - max_index
        self.z_step_down_number(number_of_steps_back)
        for i in range(1, number_of_steps_back):
            pixels_array = self.fresco_camera.get_current_image()
            self.show(pixels_array)
            measure = self.focus_measure.TENG(pixels_array)
            print('down ' + str(measure))
            self.z_step_down()
        pixels_array = self.fresco_camera.get_current_image()
        self.show(pixels_array)

    def save_current_image_from_camera(self):
        image = self.fresco_camera.get_current_image()
        self.show(image)
        try:
            cv2.imwrite('focused.png', image)
        except Exception as e:
            print(e)
