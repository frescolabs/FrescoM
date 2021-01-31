import tkinter as tk
from services.protocols_performer import ProtocolsPerformer
from tkinter.ttk import Frame, Label, Combobox
import _thread


class ProtocolsPerformerUI(Frame):

    def __init__(self, master, protocols_performer: ProtocolsPerformer):
        super().__init__(master=master, height=500, width=500)
        self.protocols_performer = protocols_performer
        self.protocols_combobox: Combobox = None
        self.init_ui()

    def init_ui(self):
        list_of_protocols = self.protocols_performer.available_protocols()
        self.protocols_combobox = Combobox(self, width=27)
        self.protocols_combobox['values'] = list_of_protocols
        self.protocols_combobox.grid(column=1, row=15)
        self.protocols_combobox.current(0)
        self.protocols_combobox.pack()

        start_button = tk.Button(self, text='Run protocol', command=self.start_protocol)
        start_button.pack()

    def start_protocol(self):
        try:
            _thread.start_new_thread(self.protocols_performer.perform_protocol, (self.protocols_combobox.get(), ))
        except Exception as e:
            print('Protocol performance error ' + str(e))
