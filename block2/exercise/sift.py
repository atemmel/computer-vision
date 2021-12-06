#!/usr/bin/env python
import cv2
path = './to_detect_2.jpg'
img = cv2.imread(path, 0)
sift = cv2.SIFT_create()
keypoints, _ = sift.detectAndCompute(img, None)
color_img = cv2.imread(path)
for keypt in keypoints:
    x, y = round(keypt.pt[0]), round(keypt.pt[1])
    cv2.circle(color_img, (x, y), 5, (0, 0, 255), 1)
cv2.imwrite("sift_out.png", color_img)
