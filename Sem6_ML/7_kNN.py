import math


class Point:

    def __init__(self, x: float, y: float, label=None):
        self.x = x
        self.y = y
        self.label = label

    def dist(self, other: "Point") -> float:
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        return math.sqrt(x_diff * x_diff + y_diff * y_diff)


class Cluster:

    def __init__(self, points: list[Point]):
        self.points = points[:]


def solve_kNN(data: list[Point], query: Point, k: int = 3) -> str:

    distances = []
    for p in data:
        d = query.dist(p)
        distances.append((d, p.label))

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    freq = {}
    for _, label in neighbors:
        freq[label] = freq.get(label, 0) + 1

    prediction = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[0][0]

    return prediction


if __name__ == "__main__":

    data = [
        Point(1, 2, "A"),
        Point(2, 3, "A"),
        Point(3, 3, "A"),
        Point(6, 5, "B"),
        Point(7, 7, "B"),
        Point(8, 6, "B"),
    ]
    query = Point(5, 5)
    predicted_point = solve_kNN(data, query)

    print("Prediction:", predicted_point)
