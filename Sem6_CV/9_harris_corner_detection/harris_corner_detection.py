import cv2
import numpy as np


def apply_harris_corner_detection(
    input_img_filepath: str,
    output_img_filepath: str,
) -> tuple[bool, str]:
    """returns success bool and output_img_filepath or error string"""
    try:
        # read image
        img = cv2.imread(input_img_filepath)
        if img is None:
            return False, f"file not foung: {input_img_filepath}"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)

        dst = cv2.cornerHarris(
            gray,
            blockSize=4,
            ksize=5,
            k=0.06,
        )

        dst = cv2.dilate(dst, None)
        img[dst > 0.01 * dst.max()] = [0, 0, 255]

        # save output image
        cv2.imwrite(output_img_filepath, img)
        return True, output_img_filepath

    except Exception as e:
        return False, str(e)


if __name__ == "__main__":

    output_ok, output = apply_harris_corner_detection(
        input_img_filepath="input.png",
        output_img_filepath="output.png",
    )

    if output_ok:
        print(f"harris_corner_detection output: {output}")
    else:
        print(f"something went wrong: {output}")
