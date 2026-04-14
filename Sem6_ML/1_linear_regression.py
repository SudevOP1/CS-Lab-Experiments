from typing import Callable
import matplotlib.pyplot as plt
import random, math

clear = "\x1b[0m"
green = "\x1b[32m"


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def apply_linear_regression_using_statistical_method(
    points: list[Point],
) -> tuple[float, float]:
    """
    applies linear regressions using statistical method
    on the points passed and returns slope, y-intercept
    """

    num_points = len(points)

    sum_x = 0
    sum_y = 0
    sum_xy = 0
    sum_x_sq = 0

    for point in points:
        sum_x += point.x
        sum_y += point.y
        sum_xy += point.x * point.y
        sum_x_sq += point.x * point.x

    m = ((num_points * sum_xy) - (sum_x * sum_y)) / (
        (num_points * sum_x_sq) - (sum_x * sum_x)
    )
    c = ((sum_y) - (m * sum_x)) / num_points

    return m, c


def apply_linear_regression_using_gradient_descent(
    points: list[Point], num_epochs: int = 100, learning_rate: float = 0.001
) -> tuple[float, float]:
    """
    applies linear regressions using gradient descent
    on the points passed and returns slope, y-intercept
    """

    num_points = len(points)

    def get_m_derivative(m: float, c: float) -> float:
        sum_thing = 0
        for point in points:
            xi = point.x
            yi = point.y
            sum_thing += xi * ((m * xi + c) - yi)
        dm = 2 * sum_thing / num_points
        return dm

    def get_c_derivative(m: float, c: float) -> float:
        sum_thing = 0
        for point in points:
            xi = point.x
            yi = point.y
            sum_thing += (m * xi + c) - yi
        dc = 2 * sum_thing / num_points
        return dc

    m = 0.0
    c = 0.0
    for _ in range(num_epochs):
        dm = get_m_derivative(m, c)
        dc = get_c_derivative(m, c)
        m = m - learning_rate * dm
        c = c - learning_rate * dc

    return m, c


def apply_linear_regression_using_logistic_regression(
    points: list[Point], num_epochs: int = 100, learning_rate: float = 0.001
) -> tuple[float, float]:
    """
    applies linear regressions using logistic regression
    on the points passed and returns slope, y-intercept
    """

    num_points = len(points)

    def sigmoid(z: float) -> float:
        if z >= 0:
            return 1 / (1 + math.exp(-z))
        exp_z = math.exp(z)
        return exp_z / (1 + exp_z)

    m = 0.0
    c = 0.0
    for _ in range(num_epochs):
        dm = 0.0
        dc = 0.0

        for point in points:
            xi = point.x
            yi = point.y

            prediction = sigmoid(m * xi + c)
            error = prediction - yi

            dm += xi * error
            dc += error

        dm /= num_points
        dc /= num_points

        m -= learning_rate * dm
        c -= learning_rate * dc

    return m, c


def get_predicted_points(points: list, m: float, c: float) -> list[Point]:
    """
    returns list of points as predicted by linear regression
    """
    predicted_points = []
    for point in points:
        predicted_points.append(Point(point.x, m * point.x + c))
    return predicted_points


def print_points(points: list[Point]) -> None:
    for point in points:
        print(f"({point.x:.2f}, {point.y:.2f})")


def display_linear_regression(
    points: list[Point],
    linear_regression_func: Callable,
    title: str = "Linear Regression",
) -> None:

    m, c = linear_regression_func(points)
    print(f"\n{green}{title}:{clear}")
    print(f"y = {m}x + {c}")

    predicted_points = get_predicted_points(points, m, c)
    print(f"\n{green}predicted points:{clear}")
    print_points(predicted_points)

    print("")
    plt.figure(figsize=(8, 5))

    # og_points
    plt.scatter(
        [point.x for point in points],
        [point.y for point in points],
        color="green",
    )

    # predicted_points
    plt.scatter(
        [point.x for point in predicted_points],
        [point.y for point in predicted_points],
        color="red",
    )

    # regression line
    plt.plot(
        [point.x for point in predicted_points],
        [point.y for point in predicted_points],
        color="black",
        linestyle="-",
        linewidth=2,
    )

    plt.title(title)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


def generate_random_points(num_points: int, m: float, c: float) -> list[Point]:
    points = []

    for _ in range(num_points):
        x = random.uniform(-10, 10)
        noise = random.uniform(-5, 5)  # adds randomness
        y = m * x + c + noise
        points.append(Point(x, y))

    return points


if __name__ == "__main__":
    points = generate_random_points(num_points=20, m=0.7, c=2)

    print(f"\n{green}og points:{clear}")
    print_points(points)

    display_linear_regression(
        points,
        apply_linear_regression_using_statistical_method,
        "Statistical Method",
    )

    display_linear_regression(
        points,
        apply_linear_regression_using_gradient_descent,
        "Gradient Descent",
    )

    display_linear_regression(
        points,
        apply_linear_regression_using_logistic_regression,
        "Logistic Regression",
    )
