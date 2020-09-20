from simple_pyspin import Camera

class FrescoCamera:

    def __init__(self):
        self.cam = Camera()  # Acquire Camera
        self.cam.init()  # Initialize camera
        self.cam.start()  # Start recording

    def __delete__(self, instance):
        self.cam.stop()  # Stop recording
        self.cam.close()  # You should explicitly clean up

    def get_current_image(self):
        image = self.cam.get_array()
        return image