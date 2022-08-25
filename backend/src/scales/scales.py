import numpy as np

from .grep import grep
from .find_timestamp import find_timestamp


def get_absolute_scale_kitti(groundtruth: list, frame_id: int) -> tuple:

    ss = groundtruth[frame_id-1].strip().split()
    x_prev = float(ss[3])
    y_prev = float(ss[7])
    z_prev = float(ss[11])

    ss = groundtruth[frame_id].strip().split()
    x = float(ss[3])
    y = float(ss[7])
    z = float(ss[11])
    
    true_t = np.array([x, y, z], dtype=np.float32).flatten().round(decimals=5)

    return (np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev) + (z - z_prev) * (z - z_prev))), true_t


def get_absolute_scale_euromav(groundtruth: list, list_timestamps:list, frame_id: int) -> tuple:

    finded = find_timestamp(list_timestamps, list_timestamps[frame_id])
    line = grep(finded, groundtruth)

    ss = line.split(',')
    x_prev = float(ss[1])
    y_prev = float(ss[3])
    z_prev = float(ss[2])

    timestamp = find_timestamp(list_timestamps, list_timestamps[frame_id + 1 ])
    line = grep(timestamp, groundtruth)

    ss = line.split(',')
    x = float(ss[1])
    y = float(ss[3])
    z = float(ss[2])
    
    true_t = np.array([x, y, z], dtype=np.float32).flatten().round(decimals=5)

    return (np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev) + (z - z_prev) * (z - z_prev))), true_t


def get_absolute_scale_vkitti2(groundtruth: list, frame_id: int) -> tuple:

    ss = groundtruth[groundtruth["frame"] == (frame_id - 1)]
    x_prev = float(ss["t1"])
    y_prev = float(ss["t2"])
    z_prev = float(ss["t3"])

    ss = groundtruth[groundtruth["frame"] == frame_id]
    x = float(ss["t1"])
    y = float(ss["t2"])
    z = float(ss["t3"])

    true_t = np.array([x, y, z], dtype=np.float32).flatten().round(decimals=5)

    return (np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev) + (z - z_prev) * (z - z_prev))), true_t
    # return (0.8, (x, y, z))
