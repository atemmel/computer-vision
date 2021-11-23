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

#points = [(2, 2), (3, 1.5), (6, 0)]
points = [(2, 2), (5, 3), (6, 0)]

x = np.linspace(0, math.pi)
y = [np.zeros(0)] * len(points)

for i in range(len(points)):
    (px, py), yi = points[i], np.zeros(len(x))
    for j in range(len(x)):
       yi[j] = f(float(px), float(py), float(x[j]))
    y[i] = yi

_, axs = plt.subplots(1, 2)
axs[0].set_title("Image space")
axs[1].set_title("Hough space")

for i in range(len(y)):
    (px, py) = points[i]
    label = "Point {}".format(i + 1)
    axs[0].plot(px, py, 'o', label=label)
    axs[1].plot(x, y[i], label=label)
intersect = find_intersect(y)

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

print(line_plots)
for l1, l2 in line_plots:
    p1, p2 = [points[l1][0], points[l2][0]], [points[l1][1], points[l2][1]]
    axs[0].plot(p1, p2)
axs[0].legend()
axs[1].legend()
plt.show()
