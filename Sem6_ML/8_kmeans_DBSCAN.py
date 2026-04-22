import math


class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def dist(self, other: "Point") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)


def solve_kmeans(data: list[Point], k: int = 2, max_iter: int = 100) -> list[int]:

    # initialize centroids (first k points)
    centroids: list[Point] = [Point(p.x, p.y) for p in data[:k]]
    labels: list[int] = [0] * len(data)

    for _ in range(max_iter):

        # assignment step
        changed = False
        for i, p in enumerate(data):
            dists = [p.dist(c) for c in centroids]
            new_label = dists.index(min(dists))
            if labels[i] != new_label:
                labels[i] = new_label
                changed = True

        # stop if no change
        if not changed:
            break

        # update step
        for j in range(k):

            cluster_points = [data[i] for i in range(len(data)) if labels[i] == j]
            if not cluster_points:
                continue

            mean_x = sum(p.x for p in cluster_points) / len(cluster_points)
            mean_y = sum(p.y for p in cluster_points) / len(cluster_points)

            centroids[j] = Point(mean_x, mean_y)

    return labels


def solve_DBSCAN(data: list[Point], eps: float = 1.5, min_pts: int = 2) -> list[int]:

    n = len(data)
    labels: list[int] = [-1] * n  # -1 = noise
    visited: list[bool] = [False] * n
    cluster_id = 0

    def region_query(idx: int) -> list[int]:
        neighbors = []
        for j in range(n):
            if data[idx].dist(data[j]) <= eps:
                neighbors.append(j)
        return neighbors

    def expand_cluster(idx: int, neighbors: list[int], cluster_id: int):
        labels[idx] = cluster_id

        i = 0
        while i < len(neighbors):
            n_idx = neighbors[i]

            if not visited[n_idx]:
                visited[n_idx] = True
                n_neighbors = region_query(n_idx)
                if len(n_neighbors) >= min_pts:
                    neighbors += n_neighbors

            if labels[n_idx] == -1:
                labels[n_idx] = cluster_id

            i += 1

    for i in range(n):
        if visited[i]:
            continue

        visited[i] = True
        neighbors = region_query(i)

        if len(neighbors) < min_pts:
            labels[i] = -1
        else:
            expand_cluster(i, neighbors, cluster_id)
            cluster_id += 1

    return labels


if __name__ == "__main__":

    data = [
        Point(1, 2),
        Point(2, 3),
        Point(3, 3),
        Point(8, 7),
        Point(9, 8),
        Point(10, 8),
    ]

    kmeans_labels = solve_kmeans(data, k=2)
    dbscan_labels = solve_DBSCAN(data, eps=2.0, min_pts=2)

    print("K-Means Labels:", kmeans_labels)
    print("DBSCAN Labels :", dbscan_labels)
