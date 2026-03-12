from PIL import Image
import os

ZERO = 0
ONE = 1
DONT_CARE = 2

def rotate_kernel_clockwise(kernel: list[list[int]]) -> tuple[bool, list[list[int]] | str]:
    """returns success bool and clockwise rotated kernel or error string"""
    kernel_w = len(kernel[0])
    kernel_h = len(kernel)

    if kernel_w != kernel_h:
        return False, "kernel not a square"
    if kernel_w % 2 == 0:
        return False, "kernel needs to be an odd square"

    n = kernel_w
    rotated_kernel = [[0 for x in range(n)] for y in range(n)]

    for i in range(n):
        for j in range(n):
            rotated_kernel[j][n - 1 - i] = kernel[i][j]

    return True, rotated_kernel

def apply_thinning_iteration(
    img: list[list[int]],
    kernel: list[list[int]],
) -> tuple[bool, list[list[int]] | str, bool]:
    """returns success bool, output image or error string, and whether any changes were made"""
    
    img_w = len(img[0])
    img_h = len(img)
    kernel_w = len(kernel[0])
    kernel_h = len(kernel)

    if kernel_w != kernel_h:
        return False, "kernel not a square", False
    if kernel_w % 2 == 0:
        return False, "kernel needs to be odd square", False

    k = kernel_w // 2
    changes_made = False
    new_img = [row[:] for row in img]
    
    for y in range(img_h):
        for x in range(img_w):
            if img[y][x] == 0:
                continue

            match_found = False
            current_kernel = [row[:] for row in kernel]
            
            for rotation in range(4 * kernel_w - 4):
                make_0 = True
                
                for j in range(-k, k + 1):
                    for i in range(-k, k + 1):
                        ky = j + k
                        kx = i + k
                        kval = current_kernel[ky][kx]

                        if kval == DONT_CARE:
                            continue

                        nx = x + i
                        ny = y + j

                        if nx < 0 or nx >= img_w or ny < 0 or ny >= img_h:
                            make_0 = False
                            break

                        if img[ny][nx] != kval:
                            make_0 = False
                            break
                    
                    if not make_0:
                        break
                
                if make_0:
                    match_found = True
                    break
                
                if rotation < 3:
                    rot_ok, current_kernel = rotate_kernel_clockwise(current_kernel)
                    if not rot_ok:
                        return False, current_kernel, False

            if match_found:
                new_img[y][x] = 0
                changes_made = True

    return True, new_img, changes_made

def apply_thinning(
    img: list[list[int]],
    kernel: list[list[int]],
    max_iterations: int = 100,
) -> tuple[bool, list[list[int]] | str]:
    """returns success bool and output image or error string"""
    
    current_img = [row[:] for row in img]
    
    for iteration in range(max_iterations):
        ok, result, changes_made = apply_thinning_iteration(current_img, kernel)
        
        if not ok:
            return False, result
        
        if not changes_made:
            return True, result
        
        current_img = result
    
    return True, current_img

def apply_thinning_on_img(
    input_img_filepath: str,
    output_img_filepath: str,
    kernel: list[list[int]],
    threshold: int = 128,
    max_iterations: int = 100,
) -> tuple[bool, str]:
    """returns success bool and output_img_filepath or error string"""

    if not os.path.exists(input_img_filepath):
        return False, "input image not found"

    img_file = Image.open(input_img_filepath).convert("L")
    width, height = img_file.size
    pixels = img_file.load()

    img = []
    for y in range(height):
        row = []
        for x in range(width):
            # Convert to 0/1 (0 = black/background, 1 = white/foreground)
            row.append(1 if pixels[x, y] < threshold else 0)
        img.append(row)
    
    thinning_ok, result = apply_thinning(img, kernel, max_iterations)
    if not thinning_ok:
        return False, result

    output_img = Image.new("L", (width, height))
    output_pixels = output_img.load()

    for y in range(height):
        for x in range(width):
            output_pixels[x, y] = 255 if result[y][x] == 0 else 0

    output_img.save(output_img_filepath)
    return True, output_img_filepath

if __name__ == "__main__":
    kernel = [
        [ZERO       , ZERO      , ZERO      ],
        [DONT_CARE  , ONE       , DONT_CARE ],
        [ONE        , ONE       , ONE       ],
    ]
    
    output_ok, output = apply_thinning_on_img(
        "input.png",
        "output.png",
        kernel=kernel,
        threshold=80,
        max_iterations=100,
    )
    
    if not output_ok:
        print(f"something went wrong: {output}")
    else:
        print(f"image saved: {output}")
