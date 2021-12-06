#!/usr/bin/env python
import numpy as np

corners = [[0, 0, 1], [0, 3, 1], [5, 3, 1], [5, 0, 1]]
corners_new = [[1, 1, 1], [3, 3, 1], [6, 3, 1], [5, 2, 1]]

def build_homo(p, q):
    assert(len(p) == len(q))
    assert(len(p[0]) == len(q[0]))
    n = len(p)
    m = len(p[0])
    res = [[0] * (m + 1) * 2 for _ in range(n * 2)]
    for i in range(n):
        v1, v2 = p[i], q[i]
        for j in range(m):
            res[i * 2][j] = v1[j]
            res[i * 2][j + m] = 0
            res[(i * 2) + 1][j + m] = v1[j]
            res[(i * 2) + 1][j] = 0

        res[i * 2][m * 2 + 0] = -v2[0] * v1[0]
        res[i * 2][m * 2 + 1] = -v2[0] * v1[1]

        res[(i * 2) + 1][m * 2 + 0] = -v2[1] * v1[0]
        res[(i * 2) + 1][m * 2 + 1] = -v2[1] * v1[1]

    return res

homo = build_homo(corners, corners_new)
_, _, v = np.linalg.svd(np.array(homo))
h = list(v[-1])
h.append(1)
h = np.array(h).reshape(3, 3)
print(h)
"""
u, s, v = np.linalg.svd(np.array(homo).transpose())
h = list(v[-1])
h.append(1)
h = np.array(h)
print(h.reshape(3, 3))
"""
#for i in homo:
    #print(i)

"""
def build_mat_from_vec(vecs):
    vecs = vecs[:len(vecs[0])]
    m, n = len(vecs), len(vecs[0])
    res = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            res[j][i] = vecs[i][j]
    return res

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

def inverse(mat):
    return np.invert(np.array(mat)).tolist()
"""
