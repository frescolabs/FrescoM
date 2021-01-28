import matplotlib.pyplot as plt
from cellpose import models, io
from PIL import Image
from cellpose import plot


class SegmentationService:

    def save_image(self, image, file_name):
        pil_image = Image.fromarray(image)
        pil_image.save(file_name)

    def segment_image(self, image):
        path = "image_for_segmentation.png"
        self.save_image(image, path)
        self.run_segmentation_script(path)

    def run_segmentation_script(self, original_image_path):
        model = models.Cellpose(gpu=False, model_type='cyto')
        channel = [0, 0]
        img = io.imread(original_image_path)
        masks, flows, styles, diams = model.eval(img, diameter=None, channels=channel)
        io.masks_flows_to_seg(img, masks, flows, diams, original_image_path, channel)
        io.save_to_png(img, masks, flows, original_image_path)
        fig = plt.figure(figsize=(12, 5))
        plot.show_segmentation(fig, img, masks, flows[0], channels=channel)
        plt.tight_layout()
        plt.show()
