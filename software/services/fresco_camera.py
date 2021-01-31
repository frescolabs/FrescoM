from simple_pyspin import Camera


class FrescoCamera:

    def __init__(self):
        self.cam = Camera()
        self.cam.init()
        self.cam.start()
        self.cam.cam.AcquisitionFrameRateAuto = 'Off'
        self.cam.cam.AcquisitionFrameRateEnabled = True

    def __delete__(self, instance):
        self.cam.stop()
        self.cam.close()

    def get_current_image(self):
        # TODO: dig in and fix (looks like we need to set 20 here, because in other case it going to return an image)
        # 'from the past' and not a current image. Need to come up with a better solution to get real time image.
        images = [self.cam.get_array() for n in range(20)]
        return images[19]

    def set_exposure(self, millis: int):
        self.set_auto_exposure(False)
        self.cam.ExposureTime = millis

    def set_auto_exposure(self, auto: bool):
        self.cam.ExposureAuto = 'Continuous' if auto else 'Off'
