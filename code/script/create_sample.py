
import numpy as np


data_root_path = "data_dir/train"


def is_tfl_divide(x_axis: np.ndarray, y_axis: np.ndarray, label: np.ndarray):
    x_true, y_true, x_false, y_false = [], [], [], []
    for x, y in zip(x_axis, y_axis):
        if label[y, x] == 19:
            x_true.append(x)
            y_true.append(y)
        else:
            x_false.append(x)
            y_false.append(y)
    return x_true, y_true, x_false, y_false


def crop_image(img: np.ndarray, x: int, y: int):
    crop_size = 40
    h, w, d = img.shape
    padded_img = np.zeros((crop_size*2+h, crop_size*2+w, 3), dtype=np.uint8)
    padded_img[crop_size: -crop_size, crop_size: -crop_size] = img
    cropped = padded_img[y: y+crop_size*2+1, x: x+crop_size*2+1]
    return cropped




