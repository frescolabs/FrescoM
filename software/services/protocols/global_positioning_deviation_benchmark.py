from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from services.images_difference_serivce import ImagesDifferenceService
from PIL import Image
import numpy as np
import json


class GlobalPositioningDeviationBenchmark(BaseProtocol):

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        super(GlobalPositioningDeviationBenchmark, self).__init__(fresco_xyz=fresco_xyz,
                                                                  z_camera=z_camera,
                                                                  images_storage=images_storage)
        self.images_storage = images_storage
        self.manifold_offset = 5050  # todo: setup actual number
        self.number_of_measurements = 50
        self.corner_prefix = '_corner_'
        self.images_difference = ImagesDifferenceService()

    def perform(self):
        super(GlobalPositioningDeviationBenchmark, self).perform()
        self.fresco_xyz.white_led_switch(True)
        self.fresco_xyz.go_to_zero_manifold()
        session_folder_path = self.images_storage.create_new_session_folder()
        for measurement_index in range(0, self.number_of_measurements):
            self.z_camera.focus_on_current_object()
            self.hold_position(1)
            image_1 = self.z_camera.fresco_camera.get_current_image()
            self.hold_position(1)
            path_1 = self.path_for_image(folder_path=session_folder_path,
                                         well_index=1,
                                         measurement_index=measurement_index)
            self.images_storage.save(image_1, path_1)
            self.fresco_xyz.delta(-7 * self.well_step_98, -7 * self.well_step_98, 0)
            self.hold_position(1)
            self.z_camera.focus_on_current_object()
            self.hold_position(1)
            image_2 = self.z_camera.fresco_camera.get_current_image()
            path_2 = self.path_for_image(folder_path=session_folder_path,
                                         well_index=2,
                                         measurement_index=measurement_index)
            self.images_storage.save(image_2, path_2)
            self.fresco_xyz.delta(7 * self.well_step_98, 7 * self.well_step_98, 0)
        self.create_report(folder_path=session_folder_path)

    def path_for_image(self, folder_path: str, well_index: int, measurement_index: int) -> str:
        return folder_path + '/' + str(well_index) + self.corner_prefix + str(measurement_index) + '.png'

    def create_report(self, folder_path: str):
        # O(n^2) each, where n = number of measurements
        all_pairs_1 = []
        all_pairs_2 = []
        for i in range(0, self.number_of_measurements):
            for j in range(i, self.number_of_measurements):
                path_1_1 = self.path_for_image(folder_path=folder_path,
                                               well_index=1,
                                               measurement_index=i)
                path_2_1 = self.path_for_image(folder_path=folder_path,
                                               well_index=1,
                                               measurement_index=j)
                all_pairs_1.append((path_1_1, path_2_1))
                path_1_2 = self.path_for_image(folder_path=folder_path,
                                               well_index=2,
                                               measurement_index=i)
                path_2_2 = self.path_for_image(folder_path=folder_path,
                                               well_index=2,
                                               measurement_index=j)
                all_pairs_2.append((path_1_2, path_2_2))

        all_differences_1 = []
        all_differences_2 = []

        # calculate difference for each pair [img1, img2, difference]
        for pair in all_pairs_1:
            image_1 = Image.open(pair[0])
            image_2 = Image.open(pair[1])
            diff = self.images_difference.calculate_offset(image_1=np.array(image_1), image_2=np.array(image_2))
            all_differences_1.append({'image_1': pair[0], 'image_2': pair[1], 'diff': diff})
        for pair in all_pairs_2:
            image_1 = Image.open(pair[0])
            image_2 = Image.open(pair[1])
            diff = self.images_difference.calculate_offset(image_1=np.array(image_1), image_2=np.array(image_2))
            all_differences_2.append({'image_1': pair[0], 'image_2': pair[1], 'diff': diff})

        # find the biggest difference in each group
        # find the average difference in each group
        sequence_1 = [x['diff'] for x in all_differences_1]
        max_error_1 = max(sequence_1)
        average_error_1 = sum(sequence_1) / len(sequence_1)
        well_standard_deviation_1 = np.std(sequence_1)

        sequence_2 = [x['diff'] for x in all_differences_2]
        max_error_2 = max(sequence_2)
        average_error_2 = sum(sequence_2) / len(sequence_2)
        well_standard_deviation_2 = np.std(sequence_2)

        # create average image of each group
        report_json = { '1_well': all_differences_1,
                        '2_well': all_differences_2,
                        '1_well_max_error': str(max_error_1),
                        '2_well_max_error': str(max_error_2),
                        '1_well_average_error': str(average_error_1),
                        '2_well_average_error': str(average_error_2),
                        '1_well_standard_deviation': str(well_standard_deviation_1),
                        '2_well_standard_deviation': str(well_standard_deviation_2),
                        'number_of_measurements_for_each_well': self.number_of_measurements}
        # save the report into a file
        with open(folder_path + '/report.json', 'w') as fp:
            json.dump(report_json, fp)

