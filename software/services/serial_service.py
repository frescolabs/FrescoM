from services.serial_connection import SerialConnection
from services.serail_connection_factory import SerialConnectionFactory
import serial.tools.list_ports


class SerialService:

    def __init__(self):
        self.factory = SerialConnectionFactory()
        self.current_connection: SerialConnection = None
        self.observers = []

    def all_available_ports(self) -> [str]:
        ports = serial.tools.list_ports.comports()
        port_names = []
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            port_names.append(port)
        return port_names

    def create_connection(self, port) -> SerialConnection:
        self.current_connection = self.factory.create_connection(port, 250000)
        print('setup current connection')
        return self.current_connection

    def subscribe_on_connection_update(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.serial_service_did_update()
