# Image Acquisition and Display

import cv2


def show_img(img_filepath: str) -> None:
    img = cv2.imread(img_filepath)

    if img is None:
        print(f"img not found: {img_filepath}")
        return

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    show_img(img_filepath="image.png")
