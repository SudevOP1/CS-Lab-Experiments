from PIL import Image
import os

ZERO = 0
_ONE = 1
__DC = 2


def apply_hmt(
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

            match = True

            for ki in range(kh):
                for kj in range(kw):
                    ni = i + ki - pad_h
                    nj = j + kj - pad_w

                    k_val = kernel[ki][kj]
                    pixel = img[ni][nj]

                    if k_val == _ONE and pixel != 255:
                        match = False
                        break
                    if k_val == ZERO and pixel != 0:
                        match = False
                        break

                if not match:
                    break

            output[i][j] = 255 if match else 0

    return True, output


def apply_hmt_on_img(
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

    success, result = apply_hmt(img, kernel)
    if not success:
        return False, result

    output_img = Image.new("L", (width, height))
    output_pixels = output_img.load()

    for i in range(height):
        for j in range(width):
            output_pixels[j, i] = result[i][j]

    output_img.save(output_img_filepath)
    return True, output_img_filepath


def print_small_img_in_terminal(img: list[list[int]]):
    WHITE = "\x1b[0;30;47m  "
    BLACK = "\x1b[0;30;40m  "
    RESET = "\x1b[0m"

    for row in img:
        for pixel in row:
            block = WHITE if pixel == 255 else BLACK
            print(block, end="")
        print(RESET)


if __name__ == "__main__":

    img = [
        [255 if pixel == _ONE else 0 for pixel in row]
        for row in [
            [ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, _ONE, _ONE, _ONE, ZERO, ZERO, ZERO, _ONE],
            [ZERO, _ONE, _ONE, _ONE, ZERO, ZERO, ZERO, ZERO],
            [ZERO, _ONE, _ONE, _ONE, ZERO, _ONE, ZERO, ZERO],
            [ZERO, ZERO, _ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
            [ZERO, ZERO, _ONE, ZERO, ZERO, _ONE, _ONE, ZERO],
            [ZERO, _ONE, ZERO, _ONE, ZERO, ZERO, _ONE, ZERO],
            [ZERO, _ONE, _ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        ]
    ]

    kernel = [
        [__DC, __DC, __DC],
        [__DC, _ONE, __DC],
        [__DC, __DC, __DC],
    ]

    hmt_output_ok, hmt_output = apply_hmt(img=img, kernel=kernel)

    if hmt_output_ok:
        print("")
        print("og img:")
        print_small_img_in_terminal(img)
        print("")
        print("hmt output:")
        print_small_img_in_terminal(hmt_output)
        print("")
    else:
        print(f"something went wrong: {hmt_output}")
