from PIL import Image, ImageDraw
import numpy as np
import cv2


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, m: float, c: float):
        self.m = m
        self.c = c


def normalize_to_uint8(arr: np.ndarray) -> np.ndarray:
    arr = np.abs(arr)
    if arr.max() == 0:
        return arr.astype(np.uint8)
    arr = (arr / arr.max()) * 255
    return arr.astype(np.uint8)


def apply_hough_transform(img_array: np.ndarray) -> tuple[bool, list[Line] | str]:
    try:
        height, width = img_array.shape

        # edge detection
        gy, gx = np.gradient(img_array)
        edges = np.sqrt(gx**2 + gy**2)
        edges = edges > (2.0 * edges.mean())

        # parameter space
        thetas = np.deg2rad(np.arange(-90, 90, 1))
        diag_len = int(np.hypot(height, width))
        rhos = np.arange(-diag_len, diag_len, 1)

        accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)

        y_idxs, x_idxs = np.nonzero(edges)

        # voting
        for i in range(len(x_idxs)):
            x = x_idxs[i]
            y = y_idxs[i]
            for t_idx in range(len(thetas)):
                rho = (
                    int(x * np.cos(thetas[t_idx]) + y * np.sin(thetas[t_idx]))
                    + diag_len
                )
                accumulator[rho, t_idx] += 1

        vote_threshold = 100
        nhood = 9
        half = nhood // 2
        lines = []

        for r in range(half, accumulator.shape[0] - half):
            for t in range(half, accumulator.shape[1] - half):

                value = accumulator[r, t]
                if value < vote_threshold:
                    continue

                local = accumulator[
                    r - half : r + half + 1,
                    t - half : t + half + 1,
                ]

                if value != local.max():
                    continue

                rho = rhos[r]
                theta = thetas[t]

                if np.sin(theta) != 0:
                    m = -np.cos(theta) / np.sin(theta)
                    c = rho / np.sin(theta)
                    lines.append(Line(m, c))

        # limit count
        lines = lines[:20]

        return True, lines

    except Exception as e:
        return False, str(e)


def apply_hough_transform_and_draw_lines(
    input_img_filepath: str,
    output_img_filepath: str,
) -> tuple[bool, str]:
    try:
        img = Image.open(input_img_filepath).convert("L")
        img_array = np.array(img, dtype=np.float32)

        hough_output_ok, hough_output = apply_hough_transform(img_array=img_array)

        if not hough_output_ok:
            return False, hough_output

        lines = hough_output

        # convert to RGB for drawing
        output_img = img.convert("RGB")
        draw = ImageDraw.Draw(output_img)

        width, height = output_img.size

        for line in lines:
            if abs(line.m) > 1e5:
                continue

            # compute two points
            x1 = 0
            y1 = int(line.c)

            x2 = width
            y2 = int(line.m * x2 + line.c)

            draw.line((x1, y1, x2, y2), fill=(255, 0, 0), width=1)

        output_img.save(output_img_filepath)
        return True, output_img_filepath

    except Exception as e:
        return False, str(e)


def apply_quick_hough_transform_and_draw_lines(
    input_img_filepath: str,
    output_img_filepath: str,
) -> tuple[bool, str]:
    try:
        # load image and convert to grayscale
        img = cv2.imread(input_img_filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # apply edge detection
        edges = cv2.Canny(gray, 180, 500, apertureSize=3)

        # apply hough transform
        lines = cv2.HoughLines(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=130,
        )

        # draw detected lines on the original image
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.imwrite(output_img_filepath, img=img)
        return True, output_img_filepath

    except Exception as e:
        return False, str(e)


if __name__ == "__main__":

    output_ok, output = apply_quick_hough_transform_and_draw_lines(
        input_img_filepath="input.png",
        output_img_filepath="output.png",
    )

    if output_ok:
        print(f"hough_transform output: {output}")
    else:
        print(f"something went wrong: {output}")
