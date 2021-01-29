from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera
from services.images_storage import ImagesStorage
from os import listdir
from os.path import isfile, join
from services.fresco_calss_loader import FrescoClassLoader
from services.protocols.base_protocol import BaseProtocol


class ProtocolsPerformer:

    def __init__(self,
                 fresco_xyz: FrescoXYZ,
                 z_camera: ZCamera,
                 images_storage: ImagesStorage):
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
        self.images_storage = images_storage
        self.protocols_folder_path = './services/protocols'
        self.class_loader = FrescoClassLoader()
        self.current_protocol: BaseProtocol = None

    def available_protocols(self) -> [str]:
        files = [self.protocols_folder_path + '/' + f for f in listdir(self.protocols_folder_path) if isfile(join(self.protocols_folder_path, f))]
        return files

    def perform_protocol(self, path: str):
        print('class to load ' + path)
        protocol_class = self.class_loader.import_class(path)
        self.current_protocol = protocol_class(self.fresco_xyz, self.z_camera, self.images_storage)
        self.current_protocol.perform()
