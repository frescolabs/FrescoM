from serial import Serial
import time


class FrescoXYZ:

    # TODO: async methods instead of waitTime

    def __init__(self):
        self.xyzSerial = Serial('/dev/cu.usbmodem14101', 250000)
        self.topLeftPosition = (-1, -1)
        self.bottomRightPosition = (-1, -1)

    def white_led_switch(self, state):
        message = None
        if state:
            message = bytearray('SwitchLedW 1' + '\n', 'utf8')
        else:
            message = bytearray('SwitchLedW 0' + '\n', 'utf8')
        self.xyzSerial.write(message)

    def blue_led_switch(self, state):
        message = None
        if state:
            message = bytearray('SwitchLedB 1' + '\n', 'utf8')
        else:
            message = bytearray('SwitchLedB 0' + '\n', 'utf8')
        self.xyzSerial.write(message)

    def delta(self, x, y, z, wait_time):
        message = bytearray('Delta ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def delta_pump(self, pump_index, delta, wait_time):
        message = bytearray('DeltaPump ' + str(pump_index) + ' ' + str(delta) + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def manifold_delta(self, delta, wait_time):
        message = bytearray('ManifoldDelta ' + str(delta) + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def set_position(self, x, y, z, wait_time):
        message = bytearray('SetPosition ' + str(x) + ' ' + str(y) + ' ' + str(z) + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def go_to_zero(self, wait_time):
        message = bytearray('Zero ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def go_to_zero_manifold(self, wait_time):
        message = bytearray('ManifoldZero ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def go_to_zero_z(self, wait_time):
        message = bytearray('VerticalZero ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def remember_top_left_position(self, wait_time):
        self.go_to_zero_z(4)
        message = bytearray('RememberTopLeft ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def remember_bottom_right_position(self, wait_time):
        self.go_to_zero_z(4)
        message = bytearray('RememberBottomRight ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)

    def update_top_left_bottom_right(self, wait_time):
        message = bytearray('GetTopLeftBottomRightCoordinates ' + '\n', 'utf8')
        self.xyzSerial.write(message)
        time.sleep(wait_time)
        coordinates_response = self.xyzSerial.read_all().decode('utf-8')
        tokens = coordinates_response.split(' ')
        self.topLeftPosition = (int(tokens[1]), int(tokens[2]))
        self.bottomRightPosition = (int(tokens[3]), int(tokens[4]))
        print(self.topLeftPosition)
        print(self.bottomRightPosition)

    def get_step_for_1_well(self, number_of_wells_x, number_of_wells_y):
        return (abs(self.topLeftPosition[0] - self.bottomRightPosition[0]) // number_of_wells_x - 1,
                abs(self.topLeftPosition[1] - self.bottomRightPosition[1]) // number_of_wells_y - 1)