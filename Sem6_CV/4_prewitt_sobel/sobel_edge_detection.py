
from PIL import Image
import numpy as np

from PIL import Image
import numpy as np

def normalize_to_uint8(arr: np.ndarray) -> np.ndarray:
    arr = np.abs(arr)
    if arr.max() == 0:
        return arr.astype(np.uint8)
    arr = (arr / arr.max()) * 255
    return arr.astype(np.uint8)


def apply_sobel_edge_detection(
    input_img_filepath: str,
    output_img_filepath: str,
    save_xy: bool = False,
) -> tuple[bool, str]:
    """returns success bool and output_img_filepath or error string"""
    try:
        # load img and convert to grayscale
        img = Image.open(input_img_filepath).convert("L")
        img_array = np.array(img, dtype=np.float32)

        # sobel kernels
        kernel_x = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ], dtype=np.float32)

        kernel_y = np.array([
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1],
        ], dtype=np.float32)

        # padding
        padded_img = np.pad(img_array, pad_width=1, mode="edge")

        # output arrays
        gx = np.zeros_like(img_array)
        gy = np.zeros_like(img_array)

        # convolution (compute both in one pass)
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                region = padded_img[i:i+3, j:j+3]
                gx[i, j] = np.sum(region * kernel_x)
                gy[i, j] = np.sum(region * kernel_y)

        if save_xy:
            # save gx image
            gx_img = Image.fromarray(normalize_to_uint8(gx))
            output_img_filepath_x = output_img_filepath.replace(".", "_x.")
            gx_img.save(output_img_filepath_x)
            print(f"saved: {output_img_filepath_x}")

            # save gy image
            gy_img = Image.fromarray(normalize_to_uint8(gy))
            output_img_filepath_y = output_img_filepath.replace(".", "_y.")
            gy_img.save(output_img_filepath_y)
            print(f"saved: {output_img_filepath_y}")

        # gradient magnitude
        magnitude = np.sqrt(gx**2 + gy**2)

        # save magnitude image
        mag_img = Image.fromarray(normalize_to_uint8(magnitude))
        mag_img.save(output_img_filepath)

        return True, output_img_filepath

    except Exception as e:
        return False, str(e)
if __name__ == "__main__":

    output_ok, output = apply_sobel_edge_detection(
        input_img_filepath="img.png",
        output_img_filepath="sobel_output.png",
    )

    if output_ok:
        print(f"sobel_edge_detection output: {output}")
    else:
        print(f"something went wrong: {output}")
