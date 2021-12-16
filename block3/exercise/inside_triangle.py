#!/usr/bin/env python
import matplotlib.pyplot as plt

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def is_inside(p0, p1, p2, pt):
    t = sub(p1, p0)
    n = (t[0], -t[1])
    inside_check_0 = dot(sub(pt, p0), n) >= 0

    t = sub(p1, p2)
    n = (t[0], -t[1])
    inside_check_1 = dot(sub(pt, p1), n) >= 0

    t = sub(p2, p0)
    n = (t[0], -t[1])
    inside_check_2 = dot(sub(pt, p2), n) >= 0

    return inside_check_0 and inside_check_1 and inside_check_2

p = [
    (-0.5, 0),
    (0.5, 0),
    (0, 1),
]

should_be_inside = (0, 0.5)
should_be_outside = (1, -0.5)

inside_plot_data = 'go' if is_inside(p[0], p[1], p[2], should_be_inside) else 'ro'
outside_plot_data = 'go' if is_inside(p[0], p[1], p[2], should_be_outside) else 'ro'
plt.plot([should_be_inside[0]], [should_be_inside[1]], inside_plot_data)
plt.plot([should_be_outside[0]], [should_be_outside[1]], outside_plot_data)
plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], 'b')
plt.plot([p[1][0], p[2][0]], [p[1][1], p[2][1]], 'b')
plt.plot([p[2][0], p[0][0]], [p[2][1], p[0][1]], 'b')
plt.show()
