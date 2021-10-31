import sys
import numpy as np
import parse
from calculations import distance, normalize
import matplotlib.pyplot as plt


# should use average link in most cases
# single link extends in weird directions
# complete link builds spheres

def h_clustering(points, threshold):
    clusters = [[p] for p in points.tolist()]
    distance_arr = np.zeros((len(clusters), len(clusters)), dtype=float)
    cluster_tracker = {}
    while len(distance_arr) > 1:
        min_dist = None
        c1 = None
        c2 = None
        for i in range(len(clusters)):
            for j in range(len(clusters)):
                if i == j:
                    continue
                # Only calculate distance if dist_arr value has not been previously calculated
                distance_arr[i, j] = distance(clusters[i], clusters[j]) if distance_arr[i, j] == 0 else distance_arr[i, j]
                cur_dist = distance_arr[i, j]
                if min_dist is None or cur_dist < min_dist:
                    min_dist = cur_dist
                    c1 = i
                    c2 = j
        # Merge C1 and C2 clusters
        clusters[c1] += clusters[c2]
        cluster_tracker[min_dist] = clusters[c1]

        # Calculate minimum distance values between merged points
        for t in range(len(distance_arr[c1])):
            if t != c1 and t != c2:
                distance_arr[c1][t] = min(distance_arr[c1][t], distance_arr[c2][t])

        # print(str(len(distance_arr)) + " x " + str(len(distance_arr[0])))
        # Remove c2 row and column
        distance_arr = np.delete(distance_arr, c2, axis=0)
        distance_arr = np.delete(distance_arr, c2, axis=1)
        # Done using c2 point, now we can pop
        clusters.pop(c2)

    final = []
    for dist, cluster in cluster_tracker.items():
        if dist <= threshold:
            final.append(cluster)
    # print(final)
    # need to consider single points that are left out
    return final


if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        data = parse.parseData(filename)
        data_norm = normalize(np.asarray(data, dtype=float))  # possible issue with normalization

        final_clusters = h_clustering(data_norm, 1.05)
        # print("Final cluster length: " + str(len(final_clusters)))
        # colors = []
        # for i in range(len(final_clusters)):
        #     colors.append([(i + 1) / len(final_clusters) for j in range(len(final_clusters[i]))])
        colors = ['red', 'green', '#88c999', "blue", "gray", "cyan", "magenta"]
        # print(len(final_clusters))
        for i, c in enumerate(final_clusters):
            x_coords = []
            y_coords = []
            for x, y in c:
                x_coords.append(x)
                y_coords.append(y)
            # print(colors)
            x_coords = np.asarray(x_coords)
            y_coords = np.asarray(y_coords)
            plt.scatter(x_coords, y_coords, color=colors[i % len(colors)])
        # plt.show()
        plt.savefig("out.png")
