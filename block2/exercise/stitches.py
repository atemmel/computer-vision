#!/usr/bin/env python
import numpy as np
import random
import cv2

def do_full_homo(p, q):
    mat = np.zeros((len(p) * 3, 9))
    for i in range(len(p)):
        mat[i * 2][0] = p[i][0]
        mat[i * 2][1] = p[i][1]
        mat[i * 2][2] = 1

        mat[i * 2][3] = 0
        mat[i * 2][4] = 0
        mat[i * 2][5] = 0

        mat[i * 2][6] = -p[i][0] * q[i][0]
        mat[i * 2][7] = -p[i][1] * q[i][0]
        mat[i * 2][8] = -q[i][0]

        mat[(i * 2) + 1][0] = 0
        mat[(i * 2) + 1][1] = 0
        mat[(i * 2) + 1][2] = 0

        mat[(i * 2) + 1][3] = p[i][0]
        mat[(i * 2) + 1][4] = p[i][1]
        mat[(i * 2) + 1][5] = 1

        mat[(i * 2) + 1][6] = -p[i][0] * q[i][1]
        mat[(i * 2) + 1][7] = -p[i][1] * q[i][1]
        mat[(i * 2) + 1][8] = -q[i][1]
    _, _, v = np.linalg.svd(mat)
    h = v[-1].reshape(3, 3)
    h /= v[-1][-1]
    return h

def ransac(points_left, points_right, desc_left, desc_right):
    n = 10000
    best_points = 0
    best_homo = None

    max_len = min(len(points_left), len(points_right))

    bf = cv2.BFMatcher()
    matches = bf.match(desc_left, desc_right)
    mp1 = [points_left[m.queryIdx].pt for m in matches]
    mp2 = [points_right[m.trainIdx].pt for m in matches]
    #print(mp1, mp2)

    for _ in range(n):
        l = [random.randint(0, max_len - 1) for _ in range(4)]
        p = np.array([mp1[i] for i in l])
        q = np.array([mp2[i] for i in l])

        #potential_homo = do_full_homo(p, q)
        potential_homo, _ = cv2.findHomography(p, q)
        if np.array_equal(potential_homo, None):
            continue
        points_transformed = [potential_homo @ (point[0], point[1], 1) for point in mp1]
        good_points = 0
        for i in range(len(mp1)):
            p_i = points_transformed[i][:2]
            q_i = mp2[i]
            #print(mp1[i], p_i, q_i)
            diff = np.linalg.norm(p_i - q_i)
            #if diff < 100:
                #print(diff)
            if diff < 10:
                good_points += 1
            if best_points < good_points:
                best_points = good_points
                best_homo = potential_homo
    #print(best_points, "out of", len(points_left))
    return best_homo

    """
    for _ in range(n):
        l = [random.randint(0, max_len - 1) for _ in range(4)]
        p = [points_left[i].pt for i in l]
        q = [points_right[i].pt for i in l]

        potential_homo = do_full_homo(p, q)
        points_transformed = [potential_homo @ (point.pt[0], point.pt[1], 1) for point in points_left]
        good_points = 0
        for i in range(max_len):
            p_i = points_transformed[i][:2]
            q_i = points_right[i].pt
            diff = np.linalg.norm(p_i - q_i)
            #total_diff += diff
            if diff < 50:
                good_points += 1
        if best_points < good_points:
            best_points = good_points
            best_homo = potential_homo
    print(best_points, "out of", len(points_left))
    return best_homo
    """


        

path_left = './to_detect_2_1.jpg'
path_right = './to_detect_2_2.jpg'

img_left = cv2.imread(path_left)
img_right = cv2.imread(path_right)

sift = cv2.SIFT_create()
points_left, desc_left = sift.detectAndCompute(img_left, None)
points_right, desc_right = sift.detectAndCompute(img_right, None)

homo = ransac(points_left, points_right, desc_left, desc_right)

#max_len = min(len(points_left), len(points_right))
#pts_src = np.array([np.float32(k.pt) for k in points_left], np.float32).reshape(-1, 2)[:max_len]
#pts_dst = np.array([np.float32(k.pt) for k in points_right], np.float32).reshape(-1, 2)[:max_len]
#other_homo, _ = cv2.findHomography(pts_src, pts_dst)

warped = cv2.warpPerspective(img_right, np.linalg.inv(homo), (img_right.shape[1] * 2, img_right.shape[0]))
warped[:img_left.shape[0], :img_left.shape[1]] = img_left
cv2.imwrite("stitched.jpg", warped)
