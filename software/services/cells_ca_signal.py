from services.segmentation_service import SegmentationService
from services.image_processor import ImageProcessor
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
from cv2_rolling_ball import subtract_background_rolling_ball
import math


class CellsCaSignal:

    def __init__(self, image_processor: ImageProcessor,
                 segmentation_service: SegmentationService):
        self.image_processor = image_processor
        self.segmentation_service = segmentation_service

    def build_signals_plot_for_folder(self, folder):
        # uncomment to subtract backgrounds from photos
        # self.subtract_backgrounds_from_images(folder)
        self.plot_graph()
        images_stack = self.read_images_stack(folder)
        signals = self.signals(images_stack)
        self.plot_signals_single_figure(signals)
        self.plot_signals(signals)


    def subtract_backgrounds_from_images(self, folder: str):
        print('start background subtraction')
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.endswith('png'):
                    image = cv2.imread(folder + '/' + filename, 0)
                    try:
                        image, background = subtract_background_rolling_ball(image,
                                                                             100,
                                                                             light_background=False,
                                                                             use_paraboloid=False,
                                                                             do_presmooth=False)
                    except Exception:
                        print('Cannot subtract background ' + filename)
                    cv2.imwrite(folder + '/' + 'subtracted_' + filename, image)
                    cv2.imwrite(folder + '/' + 'background_' + filename, background)


    def read_images_stack(self, folder: str):
        print('Start read all images and combine single 3d array')
        # todo: remove hardcoded dimensions
        stack = np.zeros(shape=(1, 1080, 1440))
        image_files = []
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.endswith('png'):
                    image_files.append(filename)
        print('Sort files')
        image_files.sort()
        for filename in image_files:
            print(filename)
            image_frame = Image.open(folder + '/' + filename)
            image_array = np.array(image_frame.getdata())
            image_array = np.reshape(image_array, (1, 1080, 1440))

            stack = np.concatenate((stack, image_array))
        print('Read stack size:')
        print(stack.shape)
        return stack

    def signals(self, input_images_stack) -> {}:
        # TODO: segment first 10 and get average area
        image_to_segment = input_images_stack[60, :, :]
        image_masks = self.segmentation_service.masks_from_image(image_to_segment, diameter=50)

        self.save_image(image_to_segment, './images/original_image.png')
        self.save_image(image_masks, './images/masks.png')

        list_mask = image_masks.tolist()
        list_mask = [j for sub in list_mask for j in sub]
        used_masks_values = set()
        for mask_value in list_mask:
            used_masks_values.add(mask_value)
        cells = {}
        for value in used_masks_values:
            cells[value] = []
        cells.pop(0)
        for image_index in range(1, input_images_stack.shape[0], 1):
            image = input_images_stack[image_index, :, :]
            for value in used_masks_values:
                if value != 0:
                    cells[value].append(self.signal_for_mask(image, image_masks, value))
        self.normalize_signals(cells)
        return cells

    # signals is an in/out parameter
    def normalize_signals(self, signals):
        for signal_index in signals:
            if signal_index != 0:
                print(signal_index)
                base_signals = signals[signal_index][:10]
                print(base_signals)
                base = sum(base_signals) / len(base_signals)
                signals[signal_index] = list(map(lambda x: (x / base) - 1, signals[signal_index]))

    def signal_for_mask(self, image, masks, needed_mask_value) -> float:
        masked = image[masks == needed_mask_value]
        return np.mean(masked)

    def save_image(self, image, name):
        print('save image')
        print(name)
        pil_image = Image.fromarray(image)
        pil_image.mode
        pil_image = pil_image.convert("L")
        pil_image.save(name)

    def plot_signals(self, signals):
        font = {'family': 'normal',
                'size': 5}

        plt.rc('font', **font)
        row_length = math.ceil(math.sqrt(len(signals)))
        rows = math.ceil(row_length / 2)
        cols = math.ceil(row_length * 2)
        fig, axes = plt.subplots(nrows=rows, ncols=cols, sharex=True)
        counter = 1
        for i in range(0, rows):
            for j in range(0, cols):
                if len(signals) > counter:
                    axes[i, j].plot(signals[counter])
                    # axes[i, j].set_title(counter)
                    counter += 1
        plt.show()

    def plot_signals_single_figure(self, signals):
        font = {'family': 'normal',
                'size': 30}

        plt.rc('font', **font)
        for signal in signals:
            plt.plot(signals[signal])
        plt.show()

    def plot_graph(self):
        font = {'family': 'normal',
                'size': 18}

        plt.rc('font', **font)
        signals = np.loadtxt("./images/Winpopnormal.txt")
        print('table shape')
        print(signals.shape)
        row_length = math.ceil(math.sqrt(signals.shape[1]))
        rows = math.ceil(row_length * 2)
        cols = math.ceil(row_length / 2)
        fig, axes = plt.subplots(nrows=rows, ncols=cols, sharex=True)
        counter = 0
        fig.tight_layout(pad=10.0)
        for i in range(0, rows):
            for j in range(0, cols):
                if signals.shape[1] > counter:
                    axes[i, j].plot(signals[:, counter])
                    counter += 1
        plt.show()
