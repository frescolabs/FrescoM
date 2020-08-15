from serial import Serial
import time
import PySpin
import sys
import cv2
import numpy
import matplotlib.pyplot as plt
import operator

class ZCamera:

    def __init__(self):
        self.archSerial = Serial('/dev/cu.usbmodem14201', 250000)

    def z_step_up(self):
        message = bytearray('D' + '\n', 'utf8')
        self.archSerial.write(message)
        time.sleep(0.1)

    def z_step_down(self):
        message = bytearray('N' + '\n', 'utf8')
        self.archSerial.write(message)
        time.sleep(0.1)

    def z_go_to_zero(self):
        message = bytearray('V' + '\n', 'utf8')
        time.sleep(2)
        self.archSerial.write(message)
        time.sleep(7)

    def xy_offset(self):
        message = bytearray('M' + '\n', 'utf8')
        self.archSerial.write(message)
        time.sleep(0.1)

    def get_current_image(self):
        system = PySpin.System.GetInstance()
        cameras_list = system.GetCameras()
        camera = cameras_list[0]
        camera.Init()
        node_map = camera.GetNodeMap()
        node_acquisition_mode = PySpin.CEnumerationPtr(node_map.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
            return False
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        camera.BeginAcquisition()
        image = None
        try:
            image = camera.GetNextImage(1000)
            if image.IsIncomplete():
                print('Image incomplete with image status %d ...' % image.GetImageStatus())
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return None
        pixels_array = image.GetNDArray()
        camera.EndAcquisition()
        camera.DeInit()
        del camera
        cameras_list.Clear()
        system.ReleaseInstance()
        return pixels_array

    # Method to get focus measure
    def TENG(self, image):
        gaussianX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        gaussianY = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        return numpy.mean(gaussianX * gaussianX +
                          gaussianY * gaussianY)

    def focus_on_current_object(self):
        print("go to zero")
        self.z_go_to_zero()
        focus_measure_data_points = []
        number_of_steps = 40
        for i in range(1, number_of_steps):
            pixels_array = self.get_current_image()
            measure = self.TENG(pixels_array)
            focus_measure_data_points.append(measure)
            cv2.imshow('', pixels_array)
            cv2.waitKey(1)
            print(measure)
            self.z_step_up()
        print("data points collected")
        max_index, max_value = max(enumerate(focus_measure_data_points), key=operator.itemgetter(1))
        number_of_steps_back = number_of_steps - max_index
        for i in range(1, number_of_steps_back):
            self.z_step_down()
        pixels_array = self.get_current_image()
        cv2.imshow('', pixels_array)
        cv2.waitKey(1)
        for i in range(1, 20):
            self.xy_offset()
            pixels_array = self.get_current_image()
            cv2.imshow('', pixels_array)
            cv2.waitKey(1)

def main():
    print("main")
    camera = ZCamera()
    print("run camera")
    camera.focus_on_current_object()

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
