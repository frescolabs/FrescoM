from services.images_difference_serivce import ImagesDifferenceService
from services.protocols.global_positioning_deviation_benchmark import GlobalPositioningDeviationBenchmark
from services.images_storage import ImagesStorage
import argparse
from PIL import Image
import numpy as np


if __name__ == '__main__':
    image_difference_service = ImagesDifferenceService()
    images_storage = ImagesStorage()
    protocol = GlobalPositioningDeviationBenchmark(fresco_xyz=None, z_camera=None, images_storage=images_storage)
    parser = argparse.ArgumentParser(description='Creates report')
    parser.add_argument('--path',
                        metavar='N',
                        type=str,
                        required=True,
                        help='path to folder to report')
    args = parser.parse_args()
    path = args.path
    protocol.create_report(path)
