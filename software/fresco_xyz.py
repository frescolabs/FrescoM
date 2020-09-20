from serial import Serial
import time

class FrescoXYZ:

    # TODO: async methods instead of waitTime

    def __init__(self):
        self.xyzSerial = Serial('/dev/cu.usbmodem14201', 250000)

    def delta(self, x, y, z, waitTime):
        message = bytearray('Delta ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(waitTime)

    def set_position(self, x, y, z, waitTime):
        message = bytearray('SetPosition ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(waitTime)

    def goToZero(self, waitTime):
        message = bytearray('Zero ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(waitTime)

    def goToZeroZ(self, waitTime):
        message = bytearray('VerticalZero ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(waitTime)

