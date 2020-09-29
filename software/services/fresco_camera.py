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
        images = [self.cam.get_array() for n in range(20)]
        return images[19]
