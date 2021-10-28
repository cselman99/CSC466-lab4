def initialize_clusters(points, clusters):
    pass


def k_means(points, clusters, stop_condition):
    centroids = initialize_clusters(points, clusters)
    centroid_points = {centroid: [] for centroids in centroids}

    while not stop_condition:
        for point in points:
            # get distance per centroid
            # get min distance
            centroid_points[min_centroid].append(point)
        # recompute centroids
        # get stoppage condition

    return centroids
