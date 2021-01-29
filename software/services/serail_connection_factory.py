from services.serial_connection import SerialConnection


class SerialConnectionFactory:

    def create_connection(self, port: str, frequency: int) -> SerialConnection:
        return SerialConnection(port, frequency)

