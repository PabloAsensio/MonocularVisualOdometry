import numpy as np

from .grep import grep
from .find_timestamp import find_timestamp
from ..maths import quaternion2Rotation, rotation2Euler, rotationMatrix

ROTATE_EUROCMAV = np.array([
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0]
])

ROTATE_EUROCMAV = rotationMatrix(np.pi / 2, 0, 3 * np.pi / 2)

def get_true_rotation_eurocmav(groundtruth: list, timestamp_groundtruth_list: list, frame_timestamps_list:list, frame_id: int) -> np.ndarray:

    finded = find_timestamp(timestamp_groundtruth_list, frame_timestamps_list[frame_id])
    line = grep(finded, groundtruth)

    ss = line.split(',')
    qw = float(ss[4])
    qx = float(ss[5])
    qy = float(ss[6])
    qz = float(ss[7])

    R = quaternion2Rotation(qw, qx, qy, qz)
    tmp = rotation2Euler( R )
    R = ROTATE_EUROCMAV @ R
    R = np.round(R, decimals=7)

    return R

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

def get_true_rotation_vkitti2(groundtruth: list, frame_id: int) -> np.ndarray:

    ss = groundtruth[groundtruth["frame"] == frame_id]
    
    r11 = float(ss["r1,1"])
    r12 = float(ss["r1,2"])
    r13 = float(ss["r1,3"])

    r21 = float(ss["r2,1"])
    r22 = float(ss["r2,2"])
    r23 = float(ss["r2,3"])

    r31 = float(ss["r3,1"])
    r32 = float(ss["r3,2"])
    r33 = float(ss["r3,3"])

    R = np.array(
        [
            [r11, r12, r13],
            [r21, r22, r23],
            [r31, r32, r33],
        ]
    , dtype=np.float32)

    R = np.round(R, decimals=7)

    return R
