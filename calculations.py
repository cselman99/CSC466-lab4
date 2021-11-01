import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

colors = ["red","green","blue","pink","black","orange","purple","beige","brown","gray","cyan","magenta"]

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




def print_accuracy(centroid_points, gt_dict):
    for i, c in enumerate(centroid_points):
        print(f'Cluster {i + 1}:')
        results = []
        for coords in c:
            results.append(gt_dict[tuple(coords)])
        c = Counter(results)
        common = c.most_common(1)[0]
        accuracy = common[1] / len(results)
        print(f'Most common element: {common[0]}')
        print(f"Accuracy: {common[1]}/{len(results)} | {accuracy}")
        print("-" * 30 + "\n")


def graph2D(title, filedest, points):
    for i, c in enumerate(points):
        x_coords = []
        y_coords = []
        for coords in c:
            x_coords.append(coords[0])
            y_coords.append(coords[1])
        x_coords = np.asarray(x_coords)
        y_coords = np.asarray(y_coords)
        plt.scatter(x_coords, y_coords, color=colors[i % len(colors)], s=10)
    # plt.show()
    plt.suptitle(title, fontsize=16)
    plt.savefig(filedest)


def graph3D(title, filedest, points):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i, c in enumerate(points):
        x_coords = []
        y_coords = []
        z_coords = []
        for coords in c:
            x_coords.append(coords[0])
            y_coords.append(coords[1])
            z_coords.append(coords[2])
        x_coords = np.asarray(x_coords)
        y_coords = np.asarray(y_coords)
        z_coords = np.asarray(z_coords)
        plt.scatter(x_coords, y_coords, z_coords, color=colors[i % len(colors)])


    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.suptitle(title, fontsize=16)
    plt.savefig(filedest)