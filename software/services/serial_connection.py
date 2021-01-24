from serial import Serial
from datetime import datetime


class SerialConnection:

    def __init__(self, port: str, frequency: int):
        self.port = port
        self.frequency = frequency
        self.serial = Serial(port, frequency)
        self.reset_all_buffers()

    def send_message_line(self, message: str):
        self.send_message(message + '\n')

    def read_message_line(self) -> str:
        return self.serial.readline()

    def send_message(self, message: str):
        byte_message = bytearray(message, 'utf8')
        self.serial.write(byte_message)

    def read_message(self) -> str:
        response = self.serial.read_all().decode('utf-8')
        return response

    def refresh_connection(self):
        self.serial = Serial(self.port, self.frequency)

    def execute_command_sync(self, message: str) -> str:
        time_begin = datetime.now()
        print('Start executing command: ' + message)
        response = self.serial.read_all().decode('utf-8')
        print('All response: ' + response)
        self.send_message_line(message)
        response_line = self.read_message_line()
        while response_line is None or response_line == '':
            print('nil response received: next try')
            response_line = self.read_message_line()
        print('Response line: ' + response_line.decode('utf-8'))
        time_executed = datetime.now()
        print('Command executed: ' + str(time_executed - time_begin))
        self.reset_all_buffers()
        return response_line.decode('utf-8')

    def reset_all_buffers(self):
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.reset_output_buffer()
        self.serial.reset_input_buffer()
