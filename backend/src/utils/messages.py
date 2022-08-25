import json
from base64 import b64encode

import cv2
import numpy as np
from src import VisualOdometry


def encode64(img):
    frame = cv2.imencode('.JPEG', img)[1]
    encoded_image = b64encode(frame).decode('utf-8')
    return encoded_image

async def create_message(vo: VisualOdometry, img: np.ndarray, img_id: int):

    cur_t = vo.cur_t
    if img_id > 2:
        x, y, z = cur_t[0][0], cur_t[1][0], cur_t[2][0]
        if vo.dataset == "kitti":
            pass
            # x, z = z, x
    else:
        x, y, z = 0.0, 0.0, 0.0

    trueX = vo.true_t[0]
    trueY = vo.true_t[1]
    trueZ = vo.true_t[2]

    trueYaw, truePitch, trueRoll = vo.get_true_euler_angles()
    estimatedYaw, estimatedPitch, estimatedRoll = vo.get_estimated_euler_angles()

    # print("\tImage id: ", img_id)
    # print("\t\tTrue Angles: ", trueYaw, truePitch, trueRoll)
    # print("\t\tEstimated Angles: ", estimatedYaw, estimatedPitch, estimatedRoll)

    message = {
        "img_id": img_id,
        "pose": {
            "x": str(z),
            "y": str(y),
            "z": str(x),
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
