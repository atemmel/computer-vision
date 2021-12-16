#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

"""
I = k_a * i_a + k_d * i_d + k_s(cos(phi))^a i_l

i_a = ambient light
i_d = diffuse light
i_s = specular light
a = shininess constant
"""
def phong(k_a, k_d, k_s, i_a, i_d, i_l, a, phi):
    return k_a * i_a + k_d * i_d + k_s * (np.cos(phi) ** a) * i_l

i_a = 2.5
i_d = 1.3
i_l = 1.7

k_a = 2.
k_d = 2.
k_s = 2.

a = np.linspace(0.0, 5.0, num=20)
phi = np.linspace(0.0, np.pi / 2, num=20)

y0 = [phong(k_a, k_d, k_s, i_a, i_d, i_l, x, np.pi / 4.) for x in a]
y1 = [phong(k_a, k_d, k_s, i_a, i_d, i_l, 2.0, x) for x in phi]

plt.plot(a, y0)
plt.show()
plt.plot(phi, y1)
plt.show()
