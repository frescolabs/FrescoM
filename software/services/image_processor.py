import numpy as np


class ImageProcessor:

    def adjust_contrast(self, image):
        min = np.min(image)
        max = np.max(image)
        LUT = np.zeros(256, dtype=np.uint8)
        LUT[min:max + 1] = np.linspace(start=0,
                                       stop=255,
                                       num=(max - min) + 1,
                                       endpoint=True,
                                       dtype=np.uint8)
        return LUT[image]
