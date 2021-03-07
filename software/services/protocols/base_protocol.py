from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
import time


class BaseProtocol:

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.images_storage = ImagesStorage
        number_of_steps_in_2_pi = 200 * 8
        rod_length_for_one_rotation = 8.0  # in mm
        distance_between_well_centers = 9.0  # in mm
        self.well_step_96 = (distance_between_well_centers / rod_length_for_one_rotation) * number_of_steps_in_2_pi  # todo: fix, calculate in a more smart way (1800)
        self.plate_size_96 = (12, 8)

    def perform(self):
        pass

    def hold_position(self, millis):
        time.sleep(millis)
