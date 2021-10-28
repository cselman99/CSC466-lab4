import numpy as np

def initialize_clusters(points, clusters):
    pass


def k_means(points, clusters, stop_condition):
    centroids = initialize_clusters(points, clusters)
    centroid_points = {centroid: [] for centroid in centroids}

    while not stop_condition:
        for point in points:
            # get distance per centroid
            # get min distance
            centroid_points[min_centroid(centroids, point)].append(point)
        # recompute centroids
        # get stoppage condition

    return centroids

def min_centroid(centroids, point):
    bestCentroid = None
    smallestDistance = None
    for centroid in centroids:
        cur_distance = distance(centroid, point)
        if smallestDistance is None or cur_distance < smallestDistance:
            bestCentroid = centroid
            smallestDistance = cur_distance

    return bestCentroid

def distance(p1, p2):
    p1Num = normalize(p1)
    p2Num = normalize(p2)
    return 0

def normalize(data):
    mins = np.min(data, axis=0)
    maxs = np.max(data, axis=0)
    data = (data - mins) / (maxs - mins)
    return data
