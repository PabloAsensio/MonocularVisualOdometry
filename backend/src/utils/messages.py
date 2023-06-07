import json
from base64 import b64encode

import cv2
import numpy as np
from src import VisualOdometry

ROTATION_CAMERA_TO_WORLD = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0]
])

INVERT_X_AXIS = np.array([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

INVERT_Z_AXIS = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, -1]
])

def encode64(img):
    frame = cv2.imencode('.JPEG', img)[1]
    encoded_image = b64encode(frame).decode('utf-8')
    return encoded_image

async def create_message(vo: VisualOdometry, img: np.ndarray, img_id: int):

    cur_t, true_t = vo.cur_t, vo.true_t
    true_euler_angles = vo.get_true_euler_angles()
    estimated_euler_angles = vo.get_estimated_euler_angles()

    if img_id > 1:
        # Rotate t vector dependin on dataset
        if vo.dataset == 'kitti':
            cur_t = ROTATION_CAMERA_TO_WORLD @ cur_t
            true_t = ROTATION_CAMERA_TO_WORLD @ (true_t - vo.init_t)

        if vo.dataset == 'vkitti2':
            cur_t = ROTATION_CAMERA_TO_WORLD @ cur_t
            true_t = INVERT_X_AXIS @ ROTATION_CAMERA_TO_WORLD @ (true_t - vo.init_t)

        if vo.dataset == 'eurocmav':
            cur_t = ROTATION_CAMERA_TO_WORLD @ cur_t
            true_t = ROTATION_CAMERA_TO_WORLD @ (true_t - vo.init_t)
            true_t *= 4 # scale

        x, y, z = cur_t[0][0], cur_t[1][0], cur_t[2][0]

    else:
        x, y, z = true_t[0], true_t[1], true_t[2]

    trueX = true_t[0]
    trueY = true_t[1]
    trueZ = true_t[2]

    trueRoll, truePitch, trueYaw = true_euler_angles
    estimatedRoll, estimatedPitch, estimatedYaw = estimated_euler_angles

    message = {
        "img_id": img_id,
        "pose": {
            "x": str(x),
            "y": str(y),
            "z": str(z),
            "yaw":   str(estimatedYaw),
            "pitch": str(estimatedPitch),
            "roll":  str(estimatedRoll)
        },
        "poseGt": {
            "x": str(trueX),
            "y": str(trueY),
            "z": str(trueZ),
            "yaw":   str(trueYaw),
            "pitch": str(truePitch),
            "roll":  str(trueRoll)
        },
        "img_data": {
            "image": encode64(img),
            "shape": img.shape
        }
        
    }
    return json.dumps(message)

async def send_message(websocket, message):
    await websocket.send(message)
