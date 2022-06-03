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
            x, z = z, x
    else:
        x, y, z = 0.0, 0.0, 0.0

    message = {
        "img_id": img_id,
        "pose": {
            "x": z,
            "y": y,
            "z": x,
            # "yaw": vo.yaw,
            # "pitch": vo.pitch,
            # "roll": vo.roll
        },
        "poseGt": {
            "x": vo.trueX,
            "y": vo.trueY,
            "z": vo.trueZ,
            # "yaw": vo.trueYaw,
            # "pitch": vo.truePitch,
            # "roll": vo.trueRoll
        },
        "img_data": {
            "image": encode64(img),
            "shape": img.shape
        }
        
    }
    return json.dumps(message)

async def send_message(websocket, message):
    await websocket.send(message)
