import cv2
import numpy


def crop_image(bgr_image):
    # Converting to HSV

    # bgr_image = cv2.GaussianBlur(bgr_image, (3, 3), 1)
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    lower = (65, 100, 0)
    higher = (75, 255, 255)

    mask = cv2.inRange(hsv, lower, higher)
    edges = cv2.Canny(mask, 50, 200, None, 3)

    lines = cv2.HoughLines(edges, 1, numpy.pi / 180., 150)

    cv2.imshow("hsv", mask)
    cv2.waitKey(0)


color = cv2.imread('../pictures/PXL_20230226_031301826.jpg')
# color = cv2.imread('../pictures/PXL_20230226_.jpg')
color = cv2.resize(color, (0, 0), fx=0.15, fy=0.15)
crop_image(color)
