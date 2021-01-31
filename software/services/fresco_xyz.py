from services.services import global_services


class FrescoXYZ:

    # TODO: async methods instead of waitTime

    def __init__(self):
        self.serial_service = global_services.serial_service
        print('Serial service inited')
        self.topLeftPosition = (-1, -1)
        self.bottomRightPosition = (-1, -1)

    def send(self, message: str):
        self.serial_service.current_connection.send_message_line(message)

    def execute_command(self, message: str) -> str:
        return self.serial_service.current_connection.execute_command_sync(message)

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

    def delta(self, x, y, z):
        message = 'Delta ' + str(x) + ' ' + str(y) + ' ' + str(z)
        self.execute_command(message)

    def delta_pump(self, pump_index, delta):
        message = 'DeltaPump ' + str(pump_index) + ' ' + str(delta)
        self.execute_command(message)

    def manifold_delta(self, delta):
        message = 'ManifoldDelta ' + str(delta)
        self.execute_command(message)

    def set_position(self, x, y, z):
        message = 'SetPosition ' + str(x) + ' ' + str(y) + ' ' + str(z)
        self.execute_command(message)

    def go_to_zero(self):
        message = 'Zero '
        self.execute_command(message)

    def go_to_zero_manifold(self):
        message = 'ManifoldZero '
        self.execute_command(message)

    def go_to_zero_z(self):
        message = 'VerticalZero '
        self.execute_command(message)

    def remember_top_left_position(self):
        self.go_to_zero_z()
        message = 'RememberTopLeft '
        self.execute_command(message)

    def remember_bottom_right_position(self):
        self.go_to_zero_z()
        message = 'RememberBottomRight '
        self.execute_command(message)

    def update_top_left_bottom_right(self):
        message = 'GetTopLeftBottomRightCoordinates '
        coordinates_response = self.execute_command(message)
        tokens = coordinates_response.split(' ')
        self.topLeftPosition = (int(tokens[1]), int(tokens[2]))
        self.bottomRightPosition = (int(tokens[3]), int(tokens[4]))
        print(self.topLeftPosition)
        print(self.bottomRightPosition)

    def get_step_for_1_well(self, number_of_wells_x, number_of_wells_y):
        return (abs(self.topLeftPosition[0] - self.bottomRightPosition[0]) // number_of_wells_x - 1,
                abs(self.topLeftPosition[1] - self.bottomRightPosition[1]) // number_of_wells_y - 1)
