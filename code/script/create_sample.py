
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





