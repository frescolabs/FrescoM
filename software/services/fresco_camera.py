from services.image_processor import ImageProcessor
import PySpin


class FrescoCamera:

    def __init__(self, image_processor: ImageProcessor):
        self.camera_system = PySpin.System.GetInstance()
        self.camera_list = self.camera_system.GetCameras()
        self.camera = self.camera_list.GetByIndex(0)
        self.camera.Init()
        self.node_map = self.camera.GetNodeMap()
        s_node_map = self.camera.GetTLStreamNodeMap()
        handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
        handling_mode_entry = handling_mode.GetEntryByName('NewestOnly')
        handling_mode.SetIntValue(handling_mode_entry.GetValue())
        self.camera.BeginAcquisition()
        self.image_processor = image_processor
        self.autocorrect_contrast = False
        self.grab_timeout = PySpin.EVENT_TIMEOUT_INFINITE
        self.stream_id = 0

    def get_current_image(self):
        py_spin_image = self.camera.GetNextImage(self.grab_timeout, self.stream_id)
        image = py_spin_image.GetNDArray()
        py_spin_image.Release()
        if self.autocorrect_contrast:
            image = self.image_processor.adjust_contrast(image)
        return image

    def __clip(self, a, a_min, a_max):
        return min(max(a, a_min), a_max)

    def set_exposure(self, millis: int):
        self.set_auto_exposure(False)
        exposure_time_to_set = self.__clip(millis,
                                          self.camera.ExposureTime.GetMin(),
                                          self.camera.ExposureTime.GetMax())
        self.camera.ExposureTime.SetValue(exposure_time_to_set)

    def set_auto_exposure(self, auto: bool):
        exposure_mode = PySpin.ExposureAuto_Continuous if auto else PySpin.ExposureAuto_Off
        self.camera.ExposureAuto.SetValue(exposure_mode)

    def set_autocorrect_contrast(self, auto: bool):
        self.autocorrect_contrast = auto
