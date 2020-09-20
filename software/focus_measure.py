import cv2
import numpy


class FocusMeasure:

    def TENG(self, image):
        gaussian_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        gaussian_y = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        return numpy.mean(gaussian_x * gaussian_x +
                          gaussian_y * gaussian_y)
