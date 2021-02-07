import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


class ImagesDifferenceService:

    def __init__(self):
        self.good_threshold = 0.7

    def calculate_offset(self, image_1, image_2) -> int:
        sift = cv.SIFT_create()
        key_points_1, descriptors_1 = sift.detectAndCompute(image_1, None)
        key_points_2, descriptors_2 = sift.detectAndCompute(image_2, None)
        flann_index_kdtree = 1
        index_params = dict(algorithm=flann_index_kdtree, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)
        good = []
        for m, n in matches:
            if m.distance < self.good_threshold * n.distance:
                good.append(m)

        src_pts = np.float32([key_points_1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([key_points_2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        transformation, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()
        h, w = image_1.shape
        pts = np.float32([[0, 0],
                          [0, h - 1],
                          [w - 1, h - 1],
                          [w - 1, 0]]).reshape(-1, 1, 2)
        try:
            destination = cv.perspectiveTransform(pts, transformation)
            x = np.float64(destination[0][0][0])
            y = np.float64(destination[0][0][1])
        except:
            # if cannot detect transformation - punishment = whole image
            x = np.float64(w)
            y = np.float64(h)
        print('x, y = ' + str(x) + ' ' + str(y))
        a = np.array((x, y))
        b = np.array((np.float64(0), np.float64(0)))
        return np.linalg.norm(a - b)

    def show_pixel_offset(self, image_1, image_2):
        sift = cv.SIFT_create()
        key_points_1, descriptors_1 = sift.detectAndCompute(image_1, None)
        key_points_2, descriptors_2 = sift.detectAndCompute(image_2, None)
        flann_index_kdtree = 1
        index_params = dict(algorithm=flann_index_kdtree, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)
        good = []
        for m, n in matches:
            if m.distance < self.good_threshold * n.distance:
                good.append(m)

        src_pts = np.float32([key_points_1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([key_points_2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        transformation, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()
        h, w = image_1.shape
        pts = np.float32([[0, 0],
                          [0, h - 1],
                          [w - 1, h - 1],
                          [w - 1, 0]]).reshape(-1, 1, 2)
        destination = cv.perspectiveTransform(pts, transformation)
        image_2 = cv.polylines(image_2, [np.int32(destination)], True, 255, 3, cv.LINE_AA)
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matches_mask,  # draw only inliers
                           flags=2)
        image_3 = cv.drawMatches(image_1,
                                 key_points_1,
                                 image_2,
                                 key_points_2,
                                 good,
                                 None,
                                 **draw_params)
        print(destination)
        print(transformation)
        print('translation: x: ' + str(destination[0][0][0]) + ' y: ' + str(destination[0][0][1]))
        plt.imshow(image_3, 'gray'), plt.show()
