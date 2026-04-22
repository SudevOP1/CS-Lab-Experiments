from PIL import Image
import os


def apply_erosion(
    img: list[list[int]],
    kernel: list[list[int]],
) -> tuple[bool, list[list[int]] | str]:

    h = len(img)
    w = len(img[0])
    kh = len(kernel)
    kw = len(kernel[0])

    pad_h = kh // 2
    pad_w = kw // 2

    output = [[0 for _ in range(w)] for _ in range(h)]

    for i in range(pad_h, h - pad_h):
        for j in range(pad_w, w - pad_w):

            ok = True

            for ki in range(kh):
                for kj in range(kw):
                    if kernel[ki][kj] == 1:
                        ni = i + ki - pad_h
                        nj = j + kj - pad_w
                        if img[ni][nj] == 0:
                            ok = False
                            break
                if not ok:
                    break

            output[i][j] = 255 if ok else 0

    return True, output


def apply_erosion_on_img(
    input_img_filepath: str,
    output_img_filepath: str,
    kernel: list[list[int]],
) -> tuple[bool, str]:

    if not os.path.exists(input_img_filepath):
        return False, "input image not found"

    img_file = Image.open(input_img_filepath).convert("L")
    width, height = img_file.size
    pixels = img_file.load()

    img = [[pixels[j, i] for j in range(width)] for i in range(height)]

    success, result = apply_erosion(img, kernel)
    if not success:
        return False, result

    output_img = Image.new("L", (width, height))
    output_pixels = output_img.load()

    for i in range(height):
        for j in range(width):
            output_pixels[j, i] = result[i][j]

    output_img.save(output_img_filepath)
    return True, output_img_filepath


def apply_dilation(
    img: list[list[int]],
    kernel: list[list[int]],
) -> tuple[bool, list[list[int]] | str]:

    h = len(img)
    w = len(img[0])
    kh = len(kernel)
    kw = len(kernel[0])

    pad_h = kh // 2
    pad_w = kw // 2

    output = [[0 for _ in range(w)] for _ in range(h)]

    for i in range(pad_h, h - pad_h):
        for j in range(pad_w, w - pad_w):

            ok = False

            for ki in range(kh):
                for kj in range(kw):
                    if kernel[ki][kj] == 1:
                        ni = i + ki - pad_h
                        nj = j + kj - pad_w
                        if img[ni][nj] == 255:
                            ok = True
                            break
                if ok:
                    break

            output[i][j] = 255 if ok else 0

    return True, output


def apply_dilation_on_img(
    input_img_filepath: str,
    output_img_filepath: str,
    kernel: list[list[int]],
) -> tuple[bool, str]:

    if not os.path.exists(input_img_filepath):
        return False, "input image not found"

    img_file = Image.open(input_img_filepath).convert("L")
    width, height = img_file.size
    pixels = img_file.load()

    img = [[pixels[j, i] for j in range(width)] for i in range(height)]

    success, result = apply_dilation(img, kernel)
    if not success:
        return False, result

    output_img = Image.new("L", (width, height))
    output_pixels = output_img.load()

    for i in range(height):
        for j in range(width):
            output_pixels[j, i] = result[i][j]

    output_img.save(output_img_filepath)
    return True, output_img_filepath


if __name__ == "__main__":

    kernel = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]

    erosion_output_ok, erosion_output = apply_erosion_on_img(
        input_img_filepath="img.png",
        output_img_filepath="erosion_output.png",
        kernel=kernel,
    )

    if not erosion_output_ok:
        print(f"something went wrong: {erosion_output}")
    else:
        print(f"image saved: {erosion_output}")

    dilation_output_ok, dilation_output = apply_dilation_on_img(
        input_img_filepath="img.png",
        output_img_filepath="dilation_output.png",
        kernel=kernel,
    )

    if not dilation_output_ok:
        print(f"something went wrong: {dilation_output}")
    else:
        print(f"image saved: {dilation_output}")
