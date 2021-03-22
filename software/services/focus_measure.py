import cv2
import numpy
from enum import Enum


class Measure(Enum):
    LAPV = 1
    LAPM = 2
    MLOG = 3
    TENG = 4


class FocusMeasure:

    def LAPV(self, image):
        return numpy.std(cv2.Laplacian(image, cv2.CV_64F)) ** 2

    def LAPM(self, image):
        kernel = numpy.array([-1, 2, -1])
        laplacianX = numpy.abs(cv2.filter2D(image, -1, kernel))
        laplacianY = numpy.abs(cv2.filter2D(image, -1, kernel.T))
        return numpy.mean(laplacianX + laplacianY)

    def MLOG(self, image):
        return numpy.max(cv2.convertScaleAbs(cv2.Laplacian(image, 3)))

    def TENG(self, image):
        gaussian_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        gaussian_y = cv2.Sobel(image, cv2.CV_64F, 0, 1)

        return numpy.mean(numpy.sqrt(gaussian_x * gaussian_x +
                                     gaussian_y * gaussian_y))

    def measure(self, image, measure=Measure.TENG):
        number = 0
        if measure == Measure.TENG:
            number = self.TENG(image)
        elif measure == Measure.LAPM:
            number = self.LAPM(image)
        elif measure == Measure.LAPV:
            number = self.LAPV(image)
        elif measure == Measure.MLOG:
            number = self.MLOG(image)
        return number
