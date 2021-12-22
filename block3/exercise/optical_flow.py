#!/usr/bin/env python
import cv2
import numpy as np

feature_params = dict(
    maxCorners = 100,
    qualityLevel = 0.3,
    minDistance = 7,
    blockSize = 7,
)

lk_params = dict(
    winSize  = (15,15),
    maxLevel = 2,
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

old_frame = cv2.imread("./flow_src_0.jpg")
frame = cv2.imread("./flow_src_1.jpg")
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

mask = np.zeros_like(old_frame)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

good_new = p1[st==1]
good_old = p0[st==1]
color = [255, 0, 0]

# go through all points of interest and mark them
for i,(new,old) in enumerate(zip(good_new,good_old)):
    a,b = np.array(np.round(new.ravel()), dtype=int)
    c,d = np.array(np.round(old.ravel()), dtype=int)
    mask = cv2.line(mask, (a,b),(c,d), color, 2)
    frame = cv2.circle(frame,(a,b),5, color,-1)
img = cv2.add(frame, mask)
cv2.imwrite("./flow_out.png", img)
