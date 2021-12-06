#!/usr/bin/env python

import math
import matplotlib.pyplot as plt

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def distance2(p1, p2):
    return (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2

def k_means(seeds, points, distance_fn):
    results = [[] for _ in range(len(seeds))]

    for point in points:
        min_dist = math.inf
        min_element = 0
        for i in range(len(seeds)):
            new_dist = distance_fn(seeds[i], point)
            if new_dist < min_dist:
                min_dist = new_dist
                min_element = i
        (results[min_element]).append(point)
    return results

def plot_result(result):
    x_list = [list()] * len(result)
    y_list = [list()] * len(result)

    for i in range(len(x_list)):
        x_list[i] = [p[0] for p in result[i]]
        y_list[i] = [p[1] for p in result[i]]

    for i in range(len(x_list)):
        plt.plot(x_list[i], y_list[i], 'o')

    for seed in seeds:
        plt.plot(seed[0], seed[1], 'o')

    plt.show()
        

seeds = [(1, 1.5), (3, 1)]
points = [
    (0, 0.8), (0, 0.5), (1.2, 0.4), (1.5, 0.8), (1, 1), (1.5, 1), 
    (2.5, 1), (3, 1), (3, 2), (4, 1.5), (4, 2.5), (5, 2)
]

regular_result = k_means(seeds, points, lambda p1, p2: distance(p1, p2))
square_result = k_means(seeds, points, lambda p1, p2: distance2(p1, p2))

plot_result(regular_result)
plot_result(square_result)
