import math


class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def solve_PCA(data: list[Point]):

    # mean
    n = len(data)
    mean_x = sum(p.x for p in data) / n
    mean_y = sum(p.y for p in data) / n

    # center data
    centered = []
    for p in data:
        centered.append((p.x - mean_x, p.y - mean_y))

    # covariance matrix elements
    cov_xx = sum(x * x for x, _ in centered) / (n - 1)
    cov_yy = sum(y * y for _, y in centered) / (n - 1)
    cov_xy = sum(x * y for x, y in centered) / (n - 1)

    # eigenvalues for 2x2 matrix
    trace = cov_xx + cov_yy
    det = cov_xx * cov_yy - cov_xy * cov_xy
    disc = trace * trace - 4 * det
    disc = max(disc, 0)
    temp = math.sqrt(disc)
    eig1 = (trace + temp) / 2
    eig2 = (trace - temp) / 2

    # eigenvector for largest eigenvalue
    if cov_xy != 0:
        v1 = eig1 - cov_yy
        v2 = cov_xy
    else:
        if cov_xx >= cov_yy:
            v1, v2 = 1, 0
        else:
            v1, v2 = 0, 1

    # normalize eigenvector
    norm = math.sqrt(v1 * v1 + v2 * v2)
    v1 /= norm
    v2 /= norm

    # project data onto principal component
    projected = []
    for x, y in centered:
        proj = x * v1 + y * v2
        projected.append(proj)

    return projected, (v1, v2), (eig1, eig2)


if __name__ == "__main__":

    data = [
        Point(2, 3),
        Point(3, 4),
        Point(4, 5),
        Point(5, 6),
        Point(6, 7),
    ]

    projected, principal_vec, eigen_vals = solve_PCA(data)

    print("")
    print(f"Principal Component (unit vector): ({principal_vec[0]:.2f}, {principal_vec[1]:.2f})")
    print(f"Eigenvalues: {eigen_vals}")
    print(f"Projected Data: {[round(p, 2) for p in projected]}")
    print("")
