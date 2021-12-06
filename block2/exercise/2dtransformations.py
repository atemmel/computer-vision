#!/usr/bin/env python
import math
import matplotlib.pyplot as plt

corners = [[0, 0, 1], [0, 3, 1], [5, 3, 1], [5, 0, 1]]

# translation matrix
translate = [
    [1, 0,  3],
    [0, 1, -2],
    [0, 0,  1],
]

angle = -15
s = math.sin(angle * (math.pi / 180))
c = math.cos(angle * (math.pi / 180))

# rotation matrix
rotate = [
    [ c, -s, 0],
    [ s,  c, 0],
    [ 0,  0, 1],
]

def mat_mul_mat(lhs, rhs):
    m, n, o = len(lhs), len(rhs[0]), len(rhs)
    res = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(o):
                res[i][j] += rhs[i][k] * lhs[k][j]
    return res

def mat_mul_vec(lhs, rhs):
    m, n = len(lhs), len(rhs)
    res = [0] * n
    for i in range(m):
        for j in range(n):
            res[i] += lhs[i][j] * rhs[j]
    return res

# total transform
transform = mat_mul_mat(translate, rotate)
# calculate new corners
new_corners = [mat_mul_vec(transform, vec) for vec in corners]

# plot
x1 = [corner[0] for corner in corners]
y1 = [corner[1] for corner in corners]
x2 = [corner[0] for corner in new_corners]
y2 = [corner[1] for corner in new_corners]
plt.xlim([-10, 10])
plt.ylim([-10, 10])
plt.plot(x1, y1, 'o')
plt.plot(x2, y2, 'o')
plt.show()
