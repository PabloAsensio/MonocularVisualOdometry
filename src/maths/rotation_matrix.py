import numpy as np


def rotation_matrix(roll, pitch, yaw):
    """
    Calculates rotation matrix from euler angles.
    From horizon to body axes axes using Tait-Bryan angles.
    """
    return np.array(
        [
            [
                np.cos(yaw) * np.cos(pitch),
                np.cos(yaw) * np.sin(pitch) * np.sin(roll) - np.sin(yaw) * np.cos(roll),
                np.cos(yaw) * np.sin(pitch) * np.cos(roll) + np.sin(yaw) * np.sin(roll),
            ],
            [
                np.sin(yaw) * np.cos(pitch),
                np.sin(yaw) * np.sin(pitch) * np.sin(roll) + np.cos(yaw) * np.cos(roll),
                np.sin(yaw) * np.sin(pitch) * np.cos(roll) - np.cos(yaw) * np.sin(roll),
            ],
            [
                -np.sin(pitch),
                np.cos(pitch) * np.sin(roll),
                np.cos(pitch) * np.cos(roll),
            ],
        ]
    ).T  # Transpose to get column vectors
