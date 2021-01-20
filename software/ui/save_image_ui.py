import tkinter as tk
from tkinter.ttk import Frame, Label
from PIL import Image, ImageTk
from services.segmentation_service import SegmentationService


class SaveImage(Frame):

    def __init__(self, master, image):
        self.image = image
        super().__init__(master=master, height=800, width=800)
        self.init_ui()
        self.segmentation_service = SegmentationService()

    def init_ui(self):
        set_position_label = tk.Label(self, text='Save image')
        set_position_label.place(x=10, y=0)

        save_button = tk.Button(self, text="Save")
        save_button.place(x=10, y=30)

        segment_button = tk.Button(self, text="Segment", command=self.segment)
        segment_button.place(x=100, y=30)

        camera_image = ImageTk.PhotoImage(image=Image.fromarray(self.image))
        self.image_label = Label(self, image=camera_image)
        self.image_label.image = camera_image
        self.image_label.place(x=10, y=80)

    def segment(self):
        self.segmentation_service.segment_image(self.image)