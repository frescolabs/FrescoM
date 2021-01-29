from PIL import Image
import os
from datetime import datetime


class ImagesStorage:

    def __init__(self):
        print('Init images storage')
        self.storage_root_path = "./images/"
        if not os.path.exists(self.storage_root_path):
            os.makedirs(self.storage_root_path)

    def save(self, image, name):
        pil_image = Image.fromarray(image)
        pil_image.save(name)

    def create_new_session_folder(self):
        timestamp_prefix = datetime.now().strftime("%d-%b-%Y-%H-%M-%S-%f")
        path = self.storage_root_path + timestamp_prefix
        os.makedirs(path)
        return path
