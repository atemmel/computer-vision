#!/usr/bin/env python
import matplotlib.pyplot as plt

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def is_inside(p0, p1, p2, pt):
    t = sub(p1, p0)
    n = (t[1], -t[0])
    inside_check_0 = dot(sub(pt, p0), n) < 0

    t = sub(p2, p1)
    n = (t[1], -t[0])
    inside_check_1 = dot(sub(pt, p1), n) < 0

    t = sub(p0, p2)
    n = (t[1], -t[0])
    inside_check_2 = dot(sub(pt, p2), n) < 0

    return inside_check_0 and inside_check_1 and inside_check_2

p = [
    (-0.5, 0),
    ( 0.5, 0),
    ( 0,   1),
]

should_be_inside = [(0, 0.5), (0, 0.2), (0.3, 0.1)]
should_be_outside = [(1, -0.5), (0.5, 0.5), (0, -0.5)]

for inside in should_be_inside:
    inside_plot_data = 'go' if is_inside(p[0], p[1], p[2], inside) else 'ro'
    plt.plot([inside[0]], [inside[1]], inside_plot_data)
plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], 'b')
plt.plot([p[1][0], p[2][0]], [p[1][1], p[2][1]], 'b')
plt.plot([p[2][0], p[0][0]], [p[2][1], p[0][1]], 'b')
plt.show()

for outside in should_be_outside:
    outside_plot_data = 'go' if is_inside(p[0], p[1], p[2], outside) else 'ro'
    plt.plot([outside[0]], [outside[1]], outside_plot_data)
plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], 'b')
plt.plot([p[1][0], p[2][0]], [p[1][1], p[2][1]], 'b')
plt.plot([p[2][0], p[0][0]], [p[2][1], p[0][1]], 'b')
plt.show()
