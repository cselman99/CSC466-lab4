import numpy as np


def manhattan_distance(p1, p2):
    dist = 0
    for i in range(len(p1)):
        dist += np.abs(p1[i] - p2[i])
    return dist


def distance(p1, p2):
    dist = 0
    for i in range(len(p1)):
        dist += np.power(p1[i] - p2[i], 2)
    return np.sqrt(dist)


def centroid_distance(p1, p2):
    p1_centroid = calc_centroid(p1)
    p2_centroid = calc_centroid(p2)
    dist = 0
    for i in range(len(p1_centroid)):
        dist += np.power(p1_centroid[i] - p2_centroid[i], 2)
    return np.sqrt(dist)


def normalize(data):
    mins = np.min(data, axis=0)
    maxs = np.max(data, axis=0)
    data = (data - mins) / (maxs - mins)
    return data


def calc_centroid(points):
    if len(points) == 0:
        return None
    pointLen = len(points[0])
    arr = [0] * pointLen
    for i in range(len(points)):
        for j in range(pointLen):
            arr[j] += points[i][j] / len(points)
    return arr


def get_stats(centroid_dict):
    # For each cluster, compute and report:
    # 1. Number of points in the cluster.
    # 2. Coordinates of its centroid.
    # 3. Maximum, minimum, and the average distance from a point to cluster centroid.
    # 4. Sum of Squared Errors (SSE) for the points in the cluster.
    pass

