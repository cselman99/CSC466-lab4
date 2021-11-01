import numpy as np
import parse
import sys
from calculations import normalize, calc_centroid, distance
import matplotlib.pyplot as plt


def init_centroids(points, num_clusters):
    anchor = calc_centroid(points)
    m1 = get_farthest_point(points, anchor)
    m1 = tuple(m1)
    centroids = [m1]
    # Exactly 1 Cluster
    if num_clusters == 1:
        return centroids

    m2 = get_farthest_point(points, m1)
    m2 = tuple(m2)
    centroids.append(m2)

    # Exactly 2 Clusters
    if num_clusters == 2:
        return centroids

    # More than 2 Clusters:
    for i in range(2, num_clusters):
        max_dist = None
        max_point = None
        for p in points:
            running_distance = 0
            for j in range(len(centroids)):
                running_distance += distance(centroids[j], p)
            if max_dist is None or running_distance > max_dist:
                max_dist = running_distance
                max_point = p
        max_point = tuple(max_point)
        centroids.append(max_point)
    return centroids


def get_farthest_point(points, anchor):
    max_distance = None
    max_point = None
    for p in points:
        dist = distance(anchor, p)
        if max_distance is None or dist > max_distance:
            max_point = p
            max_distance = dist
    return max_point


def k_means(points, num_clusters, condition, threshold):
    centroids = init_centroids(points, num_clusters)
    stop_condition = False
    centroid_points = None
    while not stop_condition:
        # Re init centroid points for every iteration
        centroid_points = {centroid: [] for centroid in centroids}

        for point in points:
            # get distance per centroid
            # get min distance
            centroid_points[best_centroid(centroids, point)].append(point)
        # recompute centroids
        new_centroids = get_new_centroids(centroid_points)
        # get stoppage condition
        stop_condition = calc_stop(centroids, new_centroids, condition, threshold)

    return centroid_points


def get_new_centroids(centroid_points):
    new_centroids = []
    for points in centroid_points.values():
        if len(points) == 0:
            continue
        cur_centroid = [0] * len(points[0])
        for p in points:
            for i in range(len(p)):
                cur_centroid[i] += p[i]
        cur_centroid = [c / len(points) for c in cur_centroid]
        new_centroids.append(cur_centroid)
    return new_centroids


def calc_stop(centroids, prev_centroids, condition, threshold):
    # True = Stop condition has been met
    # False = Stop condition has not been met
    if condition == "points":
        pass
    elif condition == "centroids":
        for i in range(len(centroids)):
            if distance(centroids[i], prev_centroids[i]) < threshold:
                return True
    elif condition == "SSE":
        pass
    return True


def best_centroid(centroids, point):
    bestCentroid = None
    smallestDistance = None
    for centroid in centroids:
        cur_distance = distance(centroid, point)
        if smallestDistance is None or cur_distance < smallestDistance:
            bestCentroid = centroid
            smallestDistance = cur_distance

    return bestCentroid

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        method = "centroids"  # default method to centroids
        if len(sys.argv) > 3:
            method = sys.argv[3]
        filename = sys.argv[1]
        k = int(sys.argv[2])
        data = parse.parseData(filename)
        data_norm = normalize(np.asarray(data, dtype=float))
        # centroids = init_centroids(data, 3)
        # print(centroids)
        centroid_points = k_means(data, k, method, 0.1)

        # GRAPHING
        colors = ["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"]
        for i, c in enumerate(centroid_points.values()):
            x_coords = []
            y_coords = []
            for coords in c:
                x_coords.append(coords[0])
                y_coords.append(coords[1])
            x_coords = np.asarray(x_coords)
            y_coords = np.asarray(y_coords)
            plt.scatter(x_coords, y_coords, color=colors[i % len(colors)], s=10)
        # plt.show()
        plt.savefig("kmeans_graph.png")
