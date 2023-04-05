import cv2
import numpy

# Read input
color = cv2.imread('../pictures/PXL_20230226_031301826.jpg', cv2.IMREAD_COLOR)
color = cv2.resize(color, (0, 0), fx=0.15, fy=0.15)
# RGB to gray
gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
# cv2.imwrite('output/gray.png', gray)
# cv2.imwrite('output/thresh.png', thresh)

gray = cv2.GaussianBlur(gray, (9, 9), 1)
# Edge detection
edges = cv2.Canny(gray, 100, 200, apertureSize=3)
# Save the edge detected image
sum_of_cols_top_to_bottom = numpy.sum(gray, axis=0, dtype=numpy.uint8)
sum_of_cols_top_left_right = numpy.sum(gray, axis=1, dtype=numpy.uint8)

# cv2.imshow('img rows', sum_of_cols_top_to_bottom)
# cv2.imshow('img cols', sum_of_cols_top_left_right)
cv2.imshow('edges', edges)
cv2.waitKey(25000)
