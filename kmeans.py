import numpy as np
import parse
import sys
from calculations import distance, normalize

def initialize_clusters(points, clusters):
    pass


def k_means(points, clusters, stop_condition):
    centroids = initialize_clusters(points, clusters)
    centroid_points = {centroid: [] for centroid in centroids}
    prev_centroids = centroids

    while not stop_condition:
        for point in points:
            # get distance per centroid
            # get min distance
            centroid_points[min_centroid(centroids, point)].append(point)
        # recompute centroids
        centroids = get_new_centroids(centroids, centroid_points)
        # get stoppage condition
        stop_condition = calc_stop(centroids, prev_centroids)

    return centroids

def calc_stop(centroids, prev_centroids):
    pass

def get_new_centroids(centroids, c_dict):
    for k, v in c_dict.items():
        pass


def min_centroid(centroids, point):
    bestCentroid = None
    smallestDistance = None
    for centroid in centroids:
        cur_distance = distance(centroid, point)
        if smallestDistance is None or cur_distance < smallestDistance:
            bestCentroid = centroid
            smallestDistance = cur_distance

    return bestCentroid

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        data = parse.parseData(filename)
        data = normalize(np.asarray(data, dtype=float))
        print(data)
