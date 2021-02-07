from services.images_difference_serivce import ImagesDifferenceService
import argparse
from PIL import Image
import numpy as np


if __name__ == '__main__':
    image_difference_service = ImagesDifferenceService()
    parser = argparse.ArgumentParser(description='Show difference and offset of 2 photos')
    parser.add_argument('--file1',
                        metavar='N',
                        type=str,
                        required=True,
                        help='first image to compare')
    parser.add_argument('--file2',
                        type=str,
                        required=True,
                        help='second image to compare')
    args = parser.parse_args()
    image_1 = Image.open(args.file1)
    image_2 = Image.open(args.file2)
    image_difference_service.show_pixel_offset(image_1=np.array(image_1), image_2=np.array(image_2))
