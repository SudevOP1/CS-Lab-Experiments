import cv2, os
import numpy as np


def _load_image(path: str) -> np.ndarray:
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {path}")
    return image


def _ensure_parent_dir(filepath: str) -> None:
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)


def rotate_img(input_filepath: str, output_filepath: str, angle: float) -> None:
    image = _load_image(input_filepath)
    h, w = image.shape[:2]
    center = (w / 2, h / 2)

    rotation_matrix_2d = cv2.getRotationMatrix2D(center, angle, 1.0)

    cos = abs(rotation_matrix_2d[0, 0])
    sin = abs(rotation_matrix_2d[0, 1])

    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)

    rotation_matrix_2d[0, 2] += (new_w / 2) - center[0]
    rotation_matrix_2d[1, 2] += (new_h / 2) - center[1]

    rotated = cv2.warpAffine(
        image,
        rotation_matrix_2d,
        (new_w, new_h),
        borderMode=cv2.BORDER_REPLICATE,
    )
    
    # save image
    _ensure_parent_dir(output_filepath)
    success = cv2.imwrite(output_filepath, rotated)
    print(f"img saved: {output_filepath}" if success else f"couldnt save img: {output_filepath}")


def translate_img(input_filepath: str, output_filepath: str, tx: float, ty: float) -> None:
    image = _load_image(input_filepath)
    h, w = image.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    translated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    
    # save image
    _ensure_parent_dir(output_filepath)
    success = cv2.imwrite(output_filepath, translated)
    print(f"img saved: {output_filepath}" if success else f"couldnt save img: {output_filepath}")


def reflect_img(input_filepath: str, output_filepath: str, xaxis: bool, yaxis: bool) -> None:
    image = _load_image(input_filepath)

    if xaxis and yaxis:
        flip_code = -1
    elif yaxis:
        flip_code = 1  # horizontal flip
    elif xaxis:
        flip_code = 0  # vertical flip
    else:
        
        # save image
        _ensure_parent_dir(output_filepath)
        success = cv2.imwrite(output_filepath, image)
        print(f"img saved: {output_filepath}" if success else f"couldnt save img: {output_filepath}")
        return

    reflected = cv2.flip(image, flip_code)
    
    # save image
    _ensure_parent_dir(output_filepath)
    success = cv2.imwrite(output_filepath, reflected)
    print(f"img saved: {output_filepath}" if success else f"couldnt save img: {output_filepath}")


def scale_img(input_filepath: str, output_filepath: str, scalex: float, scaley: float) -> None:
    image = _load_image(input_filepath)

    if scalex <= 0 or scaley <= 0:
        raise ValueError("Scale factors must be positive")

    scaled = cv2.resize(image, None, fx=scalex, fy=scaley, interpolation=cv2.INTER_LINEAR)
    
    # save image
    _ensure_parent_dir(output_filepath)
    success = cv2.imwrite(output_filepath, scaled)
    print(f"img saved: {output_filepath}" if success else f"couldnt save img: {output_filepath}")


def shear_img(input_filepath: str, output_filepath: str, shear_factor: float) -> None:
    image = _load_image(input_filepath)

    h, w = image.shape[:2]
    new_w = int(w + abs(shear_factor) * h)
    M = np.float32([[1, shear_factor, -shear_factor * h / 2], [0, 1, 0]])

    sheared = cv2.warpAffine(image, M, (new_w, h), borderMode=cv2.BORDER_REPLICATE)
    
    # save image
    _ensure_parent_dir(output_filepath)
    success = cv2.imwrite(output_filepath, sheared)
    print(f"img saved: {output_filepath}" if success else f"couldnt save img: {output_filepath}")


if __name__ == "__main__":
    rotate_img("input.png", "outputs/rotated.png", 45)
    translate_img("input.png", "outputs/translated.png", 30, 50)
    reflect_img("input.png", "outputs/reflected.png", xaxis=True, yaxis=False)
    scale_img("input.png", "outputs/scaled.png", 1.5, 1.5)
    shear_img("input.png", "outputs/sheared.png", 0.3)
