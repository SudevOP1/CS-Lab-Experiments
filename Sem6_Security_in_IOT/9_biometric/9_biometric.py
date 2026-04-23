import os, cv2
import numpy as np


def load_dataset(
    dataset_path: str,
) -> tuple[list[np.ndarray], list[int], dict[int, str]]:
    faces: list[np.ndarray] = []
    labels: list[int] = []
    label_map: dict[int, str] = {}

    label_id = 0

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_path):
            continue

        label_map[label_id] = person_name

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            faces.append(img)
            labels.append(label_id)

        label_id += 1

    return faces, labels, label_map


def train_model(faces: list[np.ndarray], labels: list[int]):
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, np.array(labels))
    return model


def authenticate(
    model,
    test_img: np.ndarray,
    label_map: dict[int, str],
    threshold: float = 70.0,
) -> tuple[bool, str]:

    label, confidence = model.predict(test_img)

    if confidence < threshold:
        return True, label_map[label]

    return False, "Unknown"


if __name__ == "__main__":

    dataset_path = "dataset"
    test_img_filepath = "img.png"

    faces, labels, label_map = load_dataset(dataset_path)

    if len(faces) == 0:
        print(f"dataset not found: {dataset_path}")
        exit()

    model = train_model(faces, labels)

    if not os.path.exists(test_img_filepath):
        print(f"image not found: {test_img_filepath}")
        exit()

    test_img = cv2.imread(test_img_filepath, cv2.IMREAD_GRAYSCALE)
    success, identity = authenticate(model, test_img, label_map)

    print("Authenticated:", success)
    print("Identity:", identity)
