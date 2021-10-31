import numpy as np

def distance(p1, p2):
    p1_centroid = calc_centroid(p1)
    p2_centroid = calc_centroid(p2)
    if len(p1_centroid) != len(p2_centroid):
        print("Non-congruent point dimensions")
        return None
    dist = 0
    for i in range(len(p1_centroid)):
        dist += np.power(p1_centroid[i] + p2_centroid[i], 2)
    return np.sqrt(dist)

def normalize(data):
    mins = np.min(data, axis=0)
    maxs = np.max(data, axis=0)
    data = (data - mins) / (maxs - mins)
    return data

def calc_centroid(point):
    if len(point) == 0:
        return None
    pointLen = len(point[0])
    arr = [0] * pointLen
    for i in range(len(point)):
        for j in range(pointLen):
            arr[j] += point[i][j]
    return [a / len(point) for a in arr]
