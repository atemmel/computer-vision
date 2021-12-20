#!/usr/bin/env python
import math
import random
import cv2

import numpy as np
import sys

sys.exit(1)

def sub(a, b):
    return [int(a[0]) - int(b[0]), int(a[1]) - int(b[1]), int(a[2]) - int(b[2])]

def distance(a, b):
    return int(a[0] - int(b[0])) ** 2 +int(a[1] - int(b[1])) ** 2 + int(a[2] - int(b[2])) **2

def avg(distance, k):
    return [distance[0] / k, distance[1] / k, distance[2] / k]

def add(a, b):
    return [int(a[0] + b[0]), int(a[1] + b[1]), int(a[2] + b[2])]

def kmeans_seeds(k):
    centers = [[] for _ in range(k)]
    for i in range(k):
        centers[i] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        #y = random.randint(0, len(data) - 1)
        #x = random.randint(0, len(data[y]) - 1)
        #centers[i] = data[y][x]
    return centers

def kmeans(original_data, data, centers):
    new_image = np.copy(data)
    new_centers = np.copy(centers)
    clusters = np.zeros(data.shape[:2])
    for i in range(len(data)):
        for j in range(len(data[i])):
            distances = [distance(data[i][j], center) for center in centers]
            min_distance = math.inf
            min_index = 0

            for k in range(len(distances)):
                if distances[k] < min_distance:
                    min_distance = distances[k]
                    min_index = k

            new_image[i][j] = centers[min_index]
            clusters[i][j] = min_index
    for k in range(len(new_centers)):
        r = 0
        g = 0
        b = 0
        n = 0
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                cluster = clusters[i][j]
                if cluster == k:
                    r += original_data[i][j][0]
                    g += original_data[i][j][1]
                    b += original_data[i][j][2]
                    n += 1
        if n == 0:
            continue

        r /= n
        g /= n
        b /= n

        new_centers[k][0] = r
        new_centers[k][1] = g
        new_centers[k][2] = b

    return new_image, new_centers

"""
def kmeans(k, data, centers):
    #new_image = np.copy(data)
    new_image = np.zeros(data.shape)
    clusters = np.zeros(data.shape[:2])

    for i in range(len(data)):
        for j in range(len(data[i])):
            distances = [distance(data[i][j], center) for center in centers]
            min_index = 0
            min_value = [math.inf, math.inf, math.inf]
            for l in range(k):
                if sum(distances[l]) < sum(min_value):
                    min_index = l
                    min_value = distances[l]
            new_image[i][j] = centers[min_index]
            clusters[i][j] = min_index

    cluster_sum = [[0, 0, 0] for _ in range(k)]
    cluster_count = [0] * k
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            cluster = int(clusters[i][j])
            cluster_sum[cluster] = add(cluster_sum[cluster], data[i][j])
            cluster_count[cluster] += 1

    for i in range(k):
        c_sum = cluster_sum[i]
        c_count = cluster_count[i]

        if c_count == 0:
            continue
        mean = avg(c_sum, c_count)
        #centers[i] = sub(centers[i], mean)
        centers[i] = sub(centers[i], mean)

    return new_image, centers
"""
"""
    # random insertion
    for member in data:
        cluster_index = random.randint(0, k - 1)
        clusters[cluster_index].append(member)

    centers = [[0, 0, 0] for _ in range(k)]

    for i in range(k):
        if(len(clusters[i]) <= 0):
            continue
        total_dist = [0, 0, 0]
        for member in clusters[i]:
            total_dist = add(total_dist, member)

        centers[i] = avg(total_dist, len(clusters[i]))

    while True:
        new_clusters = [[] for _ in range(k)]
        for i in range(k):
            for member in clusters[i]:
                distances = [distance(member, center) for center in centers]
                min_index = 0
                min_value = [math.inf, math.inf, math.inf]
                for i in range(k):
                    if sum(distances[i]) < sum(min_value):
                        min_index = i
                        min_value = distances[i]
                new_clusters[min_index].append(member)

        if clusters == new_clusters:
            break

        clusters = new_clusters

        new_centers = [[0, 0, 0] for _ in range(k)]
        for i in range(k):
            if len(clusters[i]) <= 0:
                continue
            total_dist = [0, 0, 0]
            for member in clusters[i]:
                total_dist += distance(member, new_centers[i])
            avg_dist = avg(total_dist, len(clusters[i]))

            new_centers = distance(centers[i], avg_dist)

    return clusters, new_image
    """

"""
data = [
    [0, 0, 0],
    [1, 1, 1],
    [2, 2, 2],
]

clusters = kmeans(2, data)
"""

path = "./caterpillar.jpg"
img = cv2.imread(path)

original_data = img

centers = kmeans_seeds(20)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
img, centers = kmeans(original_data, img, centers)
cv2.imwrite("kmeans_out.png", img)
