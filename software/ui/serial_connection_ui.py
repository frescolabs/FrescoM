import tkinter as tk
from tkinter.ttk import Frame, Label, Combobox
from services.services import global_services


class SerialConnectionView(Frame):

    def __init__(self, master):
        super().__init__(master=master, height=800, width=800)
        self.serial_service = global_services.serial_service
        self.port_combobox: Combobox = None
        self.init_ui()

    def init_ui(self):
        Label(self, text="Select port :")

        self.port_combobox = Combobox(self, width=27)
        print(self.serial_service.all_available_ports())
        ports = self.serial_service.all_available_ports()
        self.port_combobox['values'] = ports
        self.port_combobox.grid(column=1, row=15)
        self.port_combobox.current(0)
        self.port_combobox.pack()

        connect_button = tk.Button(self, text='Connect', command=self.connect)
        connect_button.pack()

        connect_button = tk.Button(self, text='Disconnect')
        connect_button.pack()

    def connect(self):
        try:
            self.serial_service.create_connection(self.port_combobox.get())
        except Exception as e:
            print('Connection error' + str(e))

    def disconnect(self):
        pass

    def refresh_ports(self):
        print(self.serial_service.all_available_ports())
