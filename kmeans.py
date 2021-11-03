from parse import read_data
import sys
from calculations import calc_centroid, distance, get_stats, graph, print_accuracy


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
            if (max_dist is None or running_distance > max_dist) and tuple(p) not in centroids:
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


def k_means(points, num_clusters, condition, threshold, verbose=False):
    centroids = init_centroids(points, num_clusters)
    stop_condition = False
    centroid_points = old_points = None
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
        stop_condition = calc_stop(centroids, new_centroids, centroid_points, old_points, condition, threshold)
        # Update centroids
        centroids = new_centroids
        old_points = centroid_points.copy()

    if verbose:
        get_stats(centroid_points)
    return centroid_points


def get_new_centroids(centroid_points):
    new_centroids = []
    for points in centroid_points.values():
        if len(points) == 0:
            continue
        cur_centroid = [0] * len(points[0])
        for p in points:
            for i in range(len(p)):
                cur_centroid[i] += p[i] / len(points)
        # cur_centroid = [c / len(points) for c in cur_centroid]
        new_centroids.append(tuple(cur_centroid))
    return new_centroids


def calc_stop(prev_centroids, centroids, centroid_points, old_points, condition, threshold):
    # True = Stop condition has been met
    # False = Stop condition has not been met
    if condition == "points":
        if old_points is None:
            return False
        centroid_points_keys = list(centroid_points.keys())
        old_points_keys = list(old_points.keys())
        conflicts = 0
        for i, key in enumerate(centroid_points_keys):
            if len(centroid_points[key]) != len(old_points[old_points_keys[i]]):
                return False
            temp_1 = sorted(centroid_points[key], key=lambda x: x[0])
            temp_2 = sorted(old_points[old_points_keys[i]], key=lambda x: x[0])
            for j, point in enumerate(temp_1):
                if point != temp_2[j]:
                    conflicts += 1
        if conflicts <= threshold:
            return True
    elif condition == "centroids":
        dist = 0
        for i in range(len(centroids)):
            cur_dist = distance(centroids[i], prev_centroids[i])
            dist += cur_dist
        if dist < threshold:
            return True
    elif condition == "SSE":
        sse = old_sse = 0
        for i in range(len(prev_centroids)):
            for point in centroid_points[prev_centroids[i]]:
                sse += distance(centroids[i], point)
                old_sse += distance(prev_centroids[i], point)
        if old_sse - sse < threshold:
            return True
    return False


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
        data, gt_dict, data_type = read_data(filename, norm=True)
        centroid_points = k_means(data, k, method, 1, verbose="mammal_milk" not in filename)

        if "mammal_milk" in filename:
            for i, centroid in enumerate(centroid_points.keys()):
                print("------------------------------------")
                print("Cluster %d" % (i + 1))
                for animal in centroid_points[centroid]:
                    print(gt_dict[tuple(animal)])
                print()
        elif gt_dict is not None:
            print_accuracy(centroid_points.values(), gt_dict)

        graph('K-Means at k = 4', "out.png", centroid_points.values(), data_type)
