from services.serial_service import SerialService
from services.services import global_services
import time


class FrescoXYZ:

    # TODO: async methods instead of waitTime

    def __init__(self):
        self.serial_service = global_services.serial_service
        print('serial service inited')
        self.topLeftPosition = (-1, -1)
        self.bottomRightPosition = (-1, -1)

    def send(self, message: str):
        self.serial_service.current_connection.send_message_line(message)

    def white_led_switch(self, state):
        message = None
        if state:
            message = 'SwitchLedW 1'
        else:
            message = 'SwitchLedW 0'
        self.send(message)

    def blue_led_switch(self, state):
        message = None
        if state:
            message ='SwitchLedB 1'
        else:
            message = 'SwitchLedB 0'
        self.send(message)

    def delta(self, x, y, z, wait_time):
        message = 'Delta ' + str(x) + ' ' + str(y) + ' ' + str(z)
        self.send(message)
        time.sleep(wait_time)

    def delta_pump(self, pump_index, delta, wait_time):
        message = 'DeltaPump ' + str(pump_index) + ' ' + str(delta)
        self.send(message)
        time.sleep(wait_time)

    def manifold_delta(self, delta, wait_time):
        message = 'ManifoldDelta ' + str(delta)
        self.send(message)
        time.sleep(wait_time)

    def set_position(self, x, y, z, wait_time):
        message = 'SetPosition ' + str(x) + ' ' + str(y) + ' ' + str(z)
        self.send(message)
        time.sleep(wait_time)

    def go_to_zero(self, wait_time):
        message = 'Zero '
        self.send(message)
        time.sleep(wait_time)

    def go_to_zero_manifold(self, wait_time):
        message = 'ManifoldZero '
        self.send(message)
        time.sleep(wait_time)

    def go_to_zero_z(self, wait_time):
        message = 'VerticalZero '
        self.send(message)
        time.sleep(wait_time)

    def remember_top_left_position(self, wait_time):
        self.go_to_zero_z(4)
        message = 'RememberTopLeft '
        self.send(message)
        time.sleep(wait_time)

    def remember_bottom_right_position(self, wait_time):
        self.go_to_zero_z(4)
        message = 'RememberBottomRight '
        self.send(message)
        time.sleep(wait_time)

    def update_top_left_bottom_right(self, wait_time):
        message = 'GetTopLeftBottomRightCoordinates '
        self.send(message)
        time.sleep(wait_time)
        coordinates_response = self.serial_service.current_connection.read_message()
        tokens = coordinates_response.split(' ')
        self.topLeftPosition = (int(tokens[1]), int(tokens[2]))
        self.bottomRightPosition = (int(tokens[3]), int(tokens[4]))
        print(self.topLeftPosition)
        print(self.bottomRightPosition)

    def get_step_for_1_well(self, number_of_wells_x, number_of_wells_y):
        return (abs(self.topLeftPosition[0] - self.bottomRightPosition[0]) // number_of_wells_x - 1,
                abs(self.topLeftPosition[1] - self.bottomRightPosition[1]) // number_of_wells_y - 1)
