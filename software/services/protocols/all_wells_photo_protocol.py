from services.protocols.base_protocol import BaseProtocol
from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage


class AllWellsPhotoProtocol(BaseProtocol):
    
    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage
                 ):
        super(AllWellsPhotoProtocol, self).__init__(fresco_xyz=fresco_xyz,
                                                    z_camera=z_camera,
                                                    images_storage=images_storage)
        self.images_storage = images_storage
        self.pump_index = 1  # todo: fix, temp solution, number of used  pump should be taken from protocol
        self.manifold_offset = 5050  # todo: setup actual number
        self.solution_portion_in_steps = 50  # todo: make customizable

    def perform(self):
        super(AllWellsPhotoProtocol, self).perform()
        self.fresco_xyz.white_led_switch(True)
        self.fresco_xyz.go_to_zero_manifold()
        session_folder_path = self.images_storage.create_new_session_folder()
        print('Folder ' + session_folder_path)
        for column_number in range(0, self.plate_size_98[1] - 1):
            for row_number in range(0, self.plate_size_98[0] - 1):
                self.z_camera.focus_on_current_object()
                self.hold_position(1)
                image_before_solution = self.z_camera.fresco_camera.get_current_image()
                self.images_storage.save(image_before_solution,
                                         session_folder_path + '/' + 'PI_b_' + str(row_number) + '_' + str(column_number) + '.png')
                self.fresco_xyz.go_to_zero_manifold()
                self.fresco_xyz.manifold_delta(self.manifold_offset)
                self.fresco_xyz.delta_pump(self.pump_index, self.solution_portion_in_steps)
                self.fresco_xyz.go_to_zero_manifold()
                self.z_camera.focus_on_current_object()
                self.hold_position(1)
                image_after_solution = self.z_camera.fresco_camera.get_current_image()
                self.images_storage.save(image_after_solution,
                                         session_folder_path + '/' + 'PI_a_' + str(row_number) + '_' + str(column_number) + '.png')
                self.fresco_xyz.delta(-1 * self.well_step_98, 0, 0)
            self.fresco_xyz.delta(self.well_step_98 * (self.plate_size_98[0] - 1), 0, 0)
            self.fresco_xyz.delta(0, -1 * self.well_step_98, 0)
