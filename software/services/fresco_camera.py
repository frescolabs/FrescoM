from simple_pyspin import Camera
from services.image_processor import ImageProcessor


class FrescoCamera:

    def __init__(self, image_processor: ImageProcessor):
        self.cam = Camera()
        self.cam.init()
        self.cam.start()
        self.cam.cam.AcquisitionFrameRateAuto = 'Off'
        self.cam.cam.AcquisitionFrameRateEnabled = True
        self.image_processor = image_processor
        self.autocorrect_contrast = False

    def __delete__(self, instance):
        self.cam.stop()
        self.cam.close()

    def get_current_image(self):
        # TODO: dig in and fix (looks like we need to set 20 here, because in other case it going to return an image)
        # 'from the past' and not a current image. Need to come up with a better solution to get real time image.
        images = [self.cam.get_array() for n in range(20)]
        image = images[19]
        if self.autocorrect_contrast:
            image = self.image_processor.adjust_contrast(image)
        return image

    def set_exposure(self, millis: int):
        self.set_auto_exposure(False)
        self.cam.ExposureTime = millis

    def set_auto_exposure(self, auto: bool):
        self.cam.ExposureAuto = 'Continuous' if auto else 'Off'

    def set_autocorrect_contrast(self, auto: bool):
        self.autocorrect_contrast = auto

# import PySpin
#
#
# class FrescoCamera:
#
#     def __init__(self):
#         self.system_py_spin = PySpin.System.GetInstance()
#         self.cam_list = self.system_py_spin.GetCameras()
#         num_cam = self.cam_list.GetSize()
#         if num_cam == 0:
#             self.cam_list.Clear()
#             self.system_py_spin.ReleaseInstance()
#
#         try:
#             self.cam = self.cam_list.GetByIndex(0)
#         except:
#             self.cam_list.Clear()
#             self.system_py_spin.ReleaseInstance()
#
#         self.cam.Init()
#         self.node_map = self.cam.GetNodeMap()
#
#         s_node_map = self.cam.GetTLStreamNodeMap()
#         handling_mode = PySpin.CEnumerationPtr(s_node_map.GetNode('StreamBufferHandlingMode'))
#         handling_mode_entry = handling_mode.GetEntryByName('NewestOnly')
#         handling_mode.SetIntValue(handling_mode_entry.GetValue())
#
#         self.grab_timeout = PySpin.EVENT_TIMEOUT_INFINITE
#         self.stream_id = 0
#         self.auto_software_trigger_execute = False
#
#     def __delete__(self, instance):
#         self.cam.stop()
#         self.cam.close()
#
#     def get_current_image(self):
#         if not self.cam.IsStreaming():
#             self.cam.BeginAcquisition()
#         if (self.cam.TriggerMode.GetValue() == PySpin.TriggerMode_On and
#             self.cam.TriggerSource.GetValue() == PySpin.TriggerSource_Software and
#             self.auto_software_trigger_execute == True):
#             self.cam.TriggerSoftware.Execute()
#
#         image = self.cam.GetNextImage(self.grab_timeout, self.stream_id)
#         img_NDArray = image.GetNDArray()
#         image.Release()
#         return img_NDArray
#
#     def set_exposure(self, millis: int):
#         self.set_auto_exposure(False)
#         self.cam.ExposureTime = millis
#
#     def set_auto_exposure(self, auto: bool):
#         self.cam.ExposureAuto = 'Continuous' if auto else 'Off'
