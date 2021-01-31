import tkinter as tk
from tkinter.ttk import Frame, Label
from PIL import Image, ImageTk
from services.segmentation_service import SegmentationService
from services.images_storage import ImagesStorage


class SaveImage(Frame):

    def __init__(self, master, image, images_storage: ImagesStorage):
        self.image = image
        super().__init__(master=master, height=840, width=840)
        self.image_label: Label = None
        self.init_ui()
        self.segmentation_service = SegmentationService()
        self.images_storage = images_storage

    def init_ui(self):
        set_position_label = tk.Label(self, text='Save image')
        set_position_label.place(x=10, y=0)

        save_button = tk.Button(self, text="Save", command=self.save)
        save_button.place(x=10, y=30)

        segment_button = tk.Button(self, text="Segment", command=self.segment)
        segment_button.place(x=100, y=30)

        camera_image = ImageTk.PhotoImage(image=Image.fromarray(self.image).resize((800, 800), Image.ANTIALIAS))
        self.image_label = Label(self, image=camera_image)
        self.image_label.image = camera_image
        self.image_label.place(x=10, y=80)

    def segment(self):
        self.segmentation_service.segment_image(self.image)

    def save(self):
        folder = self.images_storage.create_new_session_folder()
        path = folder + '/' + 'SI.png'
        self.images_storage.save(image=self.image, name=path)

