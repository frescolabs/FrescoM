from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
import matplotlib.pyplot as plt
import random
import math


class CollectDataSegmentation(BaseProtocol):

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(CollectDataSegmentation, self).__init__(fresco_xyz=fresco_xyz,
                                                      z_camera=z_camera,
                                                      images_storage=images_storage)
        self.images_storage = images_storage
        self.jump_size = 100
        self.maximum_radius = 800
        self.image_prefix = 'SEG_'

    def generate_quadratic_spiral_offsets(self) -> ([(int, int)], [int, int]):
        cartesian_coordinates = []
        cartesian_offsets = []
        max_offset_from_center = 0
        counter = 1
        current_x, current_y = 0, 0
        while max_offset_from_center < self.maximum_radius:
            for i in range(0, counter):
                cartesian_coordinates.append((current_x, current_y))
                current_y += self.jump_size
            for i in range(0, counter):
                cartesian_coordinates.append((current_x, current_y))
                current_x += self.jump_size
            for i in range(0, counter + 1):
                cartesian_coordinates.append((current_x, current_y))
                current_y -= self.jump_size
            for i in range(0, counter + 1):
                cartesian_coordinates.append((current_x, current_y))
                current_x -= self.jump_size
            max_offset_from_center = max(abs(current_x), abs(current_y))
            counter += 2
        cartesian_coordinates = \
            list(filter(lambda coordinate: math.sqrt(coordinate[0]**2 + coordinate[1]**2) < self.maximum_radius, cartesian_coordinates))
        for step in range(1, len(cartesian_coordinates)):
            coordinates = cartesian_coordinates[step]
            previous_coordinates = cartesian_coordinates[step - 1]
            x_offset = coordinates[0] - previous_coordinates[0]
            y_offset = coordinates[1] - previous_coordinates[1]
            cartesian_offsets.append((x_offset, y_offset))
        return cartesian_offsets, cartesian_coordinates

    def perform(self):
        self.fresco_xyz.white_led_switch(True)
        self.fresco_xyz.go_to_zero_manifold()
        session_folder_path = self.images_storage.create_new_session_folder()
        offsets, coordinates = self.generate_quadratic_spiral_offsets()
        self.save_coordinates(session_folder_path, coordinates)
        jump_size = 5
        image_index = 0
        for offset in offsets:
            print('x offset = ' + str(offset[0]) + ' y offset = ' + str(offset[1]))
            self.fresco_xyz.delta(offset[0], offset[1], 0)
            self.z_camera.focus_on_current_object()
            self.hold_position(0.3)
            image = self.z_camera.fresco_camera.get_current_image()
            self.images_storage.save(image, session_folder_path + '/' + self.image_prefix + str(image_index) + '.png')
            self.hold_position(0.3)
            # White LED offset randomization
            self.fresco_xyz.go_to_zero_manifold()
            manifold_position = random.randint(3000, 5000)
            self.fresco_xyz.manifold_delta(manifold_position)
            image_index += 1

    def save_coordinates(self, folder, coordinates):
        x = list(map(lambda element: element[0], coordinates))
        y = list(map(lambda element: element[1], coordinates))
        plt.scatter(x, y)
        plt.savefig(folder + '/spiral.png')
