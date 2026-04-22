from sklearn import svm


class Point:

    def __init__(self, x: float, y: float, label=None):
        self.x = x
        self.y = y
        self.label = label


def solve_SVM(data: list[Point], query: Point):

    # prepare dataset
    X = []
    y = []
    for p in data:
        X.append([p.x, p.y])
        y.append(p.label)

    # create model
    model = svm.SVC(kernel="linear")

    # train
    model.fit(X, y)

    # predict
    prediction = model.predict([[query.x, query.y]])

    return prediction[0]


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

    predicted_label = solve_SVM(data, query)
    print("Prediction:", predicted_label)
