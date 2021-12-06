#!/usr/bin/env python
import numpy as np
import cv2

left_img = cv2.imread('./scene1.row3.col3.ppm', 0)
right_img = cv2.imread('./scene1.row3.col4.ppm', 0)

def plane_sweep(left_img, right_img, eval_method):
    out_img = np.array([[np.uint8(0)] * len(i) for i in left_img])
    h_img, w_img = left_img.shape
    for y_in in range(h_img):
        for x_in in range(w_img):
            min_value = np.Infinity
            suitable_disp = 0
            max_disparity = 16
            for disparity in range(min(max_disparity, x_in + 1)):
            #for disparity in range(max_disparity):
                result = eval_method(float(left_img[y_in, x_in]) 
                     - float(right_img[y_in, x_in - disparity]))
                if result < min_value:
                    min_value = result
                    suitable_disp = disparity
            out_img[y_in, x_in] = ((suitable_disp) / max_disparity) * 255
    return out_img

img_out_sq_err = plane_sweep(left_img, right_img, lambda x: x ** 2)
img_out_abs_err = plane_sweep(left_img, right_img, lambda x: abs(x))

cv2.imwrite("out_sq_err.png", img_out_sq_err)
cv2.imwrite("out_abs_err.png", img_out_abs_err)
