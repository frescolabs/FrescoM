from services.fresco_xyz import FrescoXYZ
from services.z_camera import ZCamera


class ProtocolsPerformer:

    def __init__(self, fresco_xyz: FrescoXYZ, z_camera: ZCamera):
        self.fresco_xyz = fresco_xyz
        self.z_camera = z_camera
