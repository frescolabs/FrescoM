from serial import Serial

class SerialConnection:

    def __init__(self, port: str, frequency: int):
        self.port = port
        self.frequency = frequency
        self.serial = Serial(port, frequency)

    def send_message_line(self, message: str):
        self.send_message(message + '\n')

    def read_message_line(self) -> str:
        return self.read_message()

    def send_message(self, message: str):
        byte_message = bytearray(message, 'utf8')
        self.serial.write(byte_message)

    def read_message(self) -> str:
        response = self.serial.read_all().decode('utf-8')
        return response

    def refresh_connection(self):
        self.serial = Serial(self.port, self.frequency)
