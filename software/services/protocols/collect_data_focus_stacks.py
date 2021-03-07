from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
import matplotlib.pyplot as plt
import math
import random


class CollectDataFocusStacks(BaseProtocol):

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(CollectDataFocusStacks, self).__init__(fresco_xyz=fresco_xyz,
                                                     z_camera=z_camera,
                                                     images_storage=images_storage)
        self.images_storage = images_storage
        self.number_of_stacks = 100
        self.stack_size = 30
        self.image_prefix = 'S_'

    # generates spiral pattern to get XY locations for one well imaging
    # (might be changed to another: see collect_data_segmentation.py)
    def generate_spiral_offsets(self) -> ([(int, int)], [int, int]):
        approximate_well_radius = 800
        radius_offset = approximate_well_radius / self.number_of_stacks
        cartesian_coordinates = []
        angle = 0
        radius = 0
        delta_angle = math.pi / 10
        for step in range(0, self.number_of_stacks):
            # each step moving spiral
            radius += radius_offset
            angle += delta_angle
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            cartesian_coordinates.append((int(math.ceil(x)), int(math.ceil(y))))
        cartesian_offsets = []
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
        self.perform_for_one_well(session_folder_path)
        # not all wells (- 2) because of incorrectly designed plate holder
        for column_number in range(0, self.plate_size_96[1] - 2):
            for row_number in range(0, self.plate_size_96[0] - 2):
                one_well_folder = session_folder_path + '/' + str(column_number) + '_' + str(row_number)
                self.images_storage.create_folder(one_well_folder)
                self.perform_for_one_well(one_well_folder)
            self.fresco_xyz.delta(self.well_step_96 * (self.plate_size_96[0] - 1), 0, 0)
            self.fresco_xyz.delta(0, -1 * self.well_step_96, 0)

    # creates images for one well
    def perform_for_one_well(self, well_folder_path):
        offsets, coordinates = self.generate_spiral_offsets()
        self.save_coordinates(well_folder_path, coordinates)
        jump_size = 5
        index = 0
        for offset in offsets:
            print('x offset = ' + str(offset[0]) + ' y offset = ' + str(offset[1]))
            self.fresco_xyz.delta(offset[0], offset[1], 0)
            self.z_camera.focus_on_current_object()
            self.fresco_xyz.delta(0, 0, jump_size * random.randint(0, self.stack_size))
            for image_index in range(0, self.stack_size):
                stack_folder = well_folder_path + '/' + str(index)
                self.images_storage.create_folder(stack_folder)
                self.fresco_xyz.delta(0, 0, -1 * jump_size)
                self.hold_position(0.3)
                image = self.z_camera.fresco_camera.get_current_image()
                self.images_storage.save(image, stack_folder + '/' + self.image_prefix + str(image_index) + '.png')
                self.hold_position(0.3)
            index += 1
            # White LED offset randomization
            self.fresco_xyz.go_to_zero_manifold()
            manifold_position = random.randint(3000, 5000)
            self.fresco_xyz.manifold_delta(manifold_position)

    def save_coordinates(self, folder, coordinates):
        x = list(map(lambda element: element[0], coordinates))
        y = list(map(lambda element: element[1], coordinates))
        plt.scatter(x, y)
        plt.savefig(folder + '/spiral.png')
