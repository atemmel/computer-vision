#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import math

def f(x, y, theta):
    return (x * math.cos(theta)) + (y * math.sin(theta))

def find_intersect(y):
    intersections = []
    for i in range(len(y)):
        for j in range(len(y)):
            if i == j:
                continue
            new_intersections = np.argwhere(np.diff(np.sign(y[i] - y[j]))).flatten()
            intersections.extend([(intersect, i) for intersect in new_intersections])
    return intersections

def create_matrix(scale, x, y):
    mat = np.asarray([[0] * scale for _ in range(scale)])
    y_max = max([max(rho) for rho in y])
    y_min = min([min(rho) for rho in y])
    x_max = max(x)
    x_min = min(x)

    w = math.fabs(x_min - x_max)
    h = math.fabs(y_min - y_max)

    for index in range(len(x)):
        theta = x[index]
        i = (theta - x_min) / w
        i = int(i * (scale - 1))
        for y_inner in y:
            rho = y_inner[index]
            j = (rho - y_min) / h
            j = int(j * (scale - 1))
            mat[i][j] += 1
            
    return mat.transpose()

def find_max_in_matrix(matrix):
    max_index = (0, 0)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[max_index[0]][max_index[1]] < matrix[i][j]:
                max_index = (i, j)
    return max_index

def point_hough_to_image(index, matrix, scale, x, y):
    y_max = max([max(rho) for rho in y])
    y_min = min([min(rho) for rho in y])
    x_max = max(x)
    x_min = min(x)

    norm_index = (index[0] / scale, index[1] / scale)
    translated_index = (norm_index[0] * (x_max - x_min) - x_min, norm_index[1] * (y_max - y_min) - y_min)
    print(translated_index)
    

#points = [(2, 2), (3, 1.5), (6, 0)]
points = [(2, 2), (5, 3), (6, 0)]

x = np.linspace(0, math.pi)
y = [np.zeros(0)] * len(points)

for i in range(len(points)):
    (px, py), yi = points[i], np.zeros(len(x))
    for j in range(len(yi)):
       yi[j] = f(float(px), float(py), float(x[j]))
    y[i] = yi


_, axs = plt.subplots(1, 2)
#axs[0].set_title("Image space")
axs[0].set_title("Hough space")
axs[1].set_title("Hough Vote results")

for i in range(len(y)):
    (px, py) = points[i]
    label = "Point {}".format(i + 1)
    #axs[0].plot(px, py, 'o', label=label)
    axs[0].plot(x, y[i], label=label)
#intersect = find_intersect(y)
mat = create_matrix(32, x, y)
axs[1].matshow(mat, origin="lower")

max_index = find_max_in_matrix(mat)
point_hough_to_image(max_index, mat, 32, x, y)

axs[0].legend()
#axs[1].legend()
plt.show()

"""
line_plots = set()
for i in range(len(intersect)):
    t, p1 = intersect[i]
    for j in range(len(intersect)):
        if i == j:
            continue
        u, p2 = intersect[j]
        if u == t and (p2, p1) != (p1, p2) and (p2, p1) not in line_plots:
            line_plots.add((p1, p2))

for i, j in intersect:
    axs[1].plot(x[i], y[j][i], 'o')
"""

"""
print(line_plots)
for l1, l2 in line_plots:
    p1, p2 = [points[l1][0], points[l2][0]], [points[l1][1], points[l2][1]]
    axs[0].plot(p1, p2)
"""



