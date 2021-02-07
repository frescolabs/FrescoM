from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from services.images_difference_serivce import ImagesDifferenceService
from PIL import Image
import numpy as np
import json


class SamePositionDeviationBenchmark(BaseProtocol):

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage
                 ):
        super(SamePositionDeviationBenchmark, self).__init__(fresco_xyz=fresco_xyz,
                                                             z_camera=z_camera,
                                                             images_storage=images_storage)
        self.images_storage = images_storage
        self.number_of_measurements = 50
        self.image_prefix = 'BM_image_'
        self.images_difference = ImagesDifferenceService()

    def perform(self):
        super(SamePositionDeviationBenchmark, self).perform()
        self.fresco_xyz.white_led_switch(True)
        self.fresco_xyz.go_to_zero_manifold()
        session_folder_path = self.images_storage.create_new_session_folder()
        self.z_camera.focus_on_current_object()
        for measurement_index in range(0, self.number_of_measurements):
            self.hold_position(1)
            image = self.z_camera.fresco_camera.get_current_image()
            self.hold_position(1)
            path = self.path_for_image(folder_path=session_folder_path,
                                       measurement_index=measurement_index)
            self.images_storage.save(image, path)
        self.create_report(folder_path=session_folder_path)

    def path_for_image(self, folder_path: str, measurement_index: int) -> str:
        return folder_path + '/' + self.image_prefix + str(measurement_index) + '.png'

    def create_report(self, folder_path: str):
        # O(n^2) each, where n = number of measurements
        all_pairs = []
        for i in range(0, self.number_of_measurements):
            for j in range(i, self.number_of_measurements):
                path_1 = self.path_for_image(folder_path=folder_path,
                                             measurement_index=i)
                path_2 = self.path_for_image(folder_path=folder_path,
                                             measurement_index=j)
                all_pairs.append((path_1, path_2))
        all_differences = []

        # calculate difference for each pair [img1, img2, difference]
        for pair in all_pairs:
            image_1 = Image.open(pair[0])
            image_2 = Image.open(pair[1])
            diff = self.images_difference.calculate_offset(image_1=np.array(image_1), image_2=np.array(image_2))
            all_differences.append({'image_1': pair[0], 'image_2': pair[1], 'diff': diff})

        # find the biggest difference in each group
        # find the average difference in each group
        sequence = [x['diff'] for x in all_differences]
        max_error = max(sequence)
        average_error = sum(sequence) / len(sequence)

        report_json = { 'differences': all_differences,
                        'max_error': str(max_error),
                        'average_error': str(average_error),
                        'number_of_measurements': self.number_of_measurements}
        # save the report into a file
        with open(folder_path + '/report.json', 'w') as fp:
            json.dump(report_json, fp)

