import numpy as np

from .grep import grep
from .find_timestamp import find_timestamp

def get_true_rotation_kitti(groundtruth: list, frame_id: int) -> np.ndarray:

    ss = groundtruth[frame_id].strip().split()

    r11 = float(ss[0])
    r12 = float(ss[1])
    r13 = float(ss[2])

    r21 = float(ss[4])
    r22 = float(ss[5])
    r23 = float(ss[6])

    r31 = float(ss[8])
    r32 = float(ss[9])
    r33 = float(ss[10])

    R = np.array(
        [
            [r11, r12, r13],
            [r21, r22, r23],
            [r31, r32, r33],
        ]
    , dtype=np.float32)

    R = np.round(R, decimals=7)

    return R
