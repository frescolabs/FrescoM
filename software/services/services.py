from services.serial_service import SerialService


class Services:

    def __init__(self):
        self.serial_service = SerialService()


global_services = Services()

