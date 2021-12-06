#!/usr/bin/env python
import numpy as np
import cv2

path = './to_detect_2.jpg'
img = cv2.imread(path, 0)

# sobel matrices
gx_kernel = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1],
])

gy_kernel = np.array([
    [ 1,  2,  1],
    [ 0,  0,  0],
    [-1, -2, -1],
])

# blur
blur_img = cv2.GaussianBlur(img, (5,5), 3)

# sobel and build matrix components
gx = cv2.filter2D(blur_img, -1, gx_kernel)
gy = cv2.filter2D(blur_img, -1, gy_kernel)
gxy = gx * gy
gx2 = gx ** 2
gy2 = gy ** 2

k = 0.06
h, w = img.shape
result = np.array([[0.0] * w for _ in range(h)], float)
for y in range(h):
    for x in range(w):
        # structure tensor, see:
        # https://en.wikipedia.org/wiki/Harris_corner_detector#Development_of_Harris_corner_detection_algorithm_[1]
        mat = np.array([
            [gx2[y][x], gxy[y][x]],
            [gxy[y][x], gy2[y][x]],
        ], dtype=float)

        # response calculation, see:
        # https://en.wikipedia.org/wiki/Harris_corner_detector#Harris_response_calculation
        tr = mat[0,0] + mat[1,1]
        det = mat[0,0] * mat[1,1] - mat[1,0]*mat[0,1]
        result[y][x] = det - (k * (tr * tr))

# mark points of interest
color_img = cv2.imread(path)
threshold = 24500
for y in range(h):
    for x in range(w):
        if result[y][x] > threshold:
            cv2.circle(color_img, (x, y), 5, (0, 0, 255), 1)

cv2.imwrite("harris_out.png", color_img)
