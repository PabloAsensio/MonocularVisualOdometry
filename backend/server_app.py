import asyncio
import configparser
import json
from base64 import b64encode
from glob import glob

import cv2
import numpy as np
import websockets
from tqdm import tqdm

from src.cv import PinholeCamera, VisualOdometry

PORT = 7890

print("Server listening on Port " + str(PORT))

def encode64(img):
    frame = cv2.imencode('.JPEG', img)[1]
    encoded_image = b64encode(frame).decode('utf-8')
    return encoded_image

def load_images(imgs_path: str) -> list:
    images = []
    for fn in tqdm(sorted(glob(imgs_path)), desc="Loading images", ascii=True):
        img = cv2.imread(fn, 0)
        if img is not None:
            images.append([img, encode64(img)])
    return images


async def create_message(vo, img, img_id):

    cur_t = vo.cur_t
    if img_id > 2:
        x, y, z = cur_t[0][0], cur_t[1][0], cur_t[2][0]
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
            "image": img[1],
            "shape": img[0].shape
        }
        
    }
    return json.dumps(message)

async def send_message(websocket, message):
    await websocket.send(message)


async def monocular_visual_odometry(websocket, info: dict) -> int:
    try:
        if info['dataset'] == 'euromav':
            camera = PinholeCamera.from_euromav(info['calibration_file'])
            vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])
        camera = PinholeCamera(1242.0, 375.0, 725.0087, 725.0087, 620.5, 187.0)
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])

        imgs = load_images(info['images_path'])

        for img_id, img in tqdm(enumerate(imgs), desc="Progress", ascii=True, total=len(imgs)):

            if img_id == 0:
                if vo.dataset == "VKITTI2":
                    pass
                continue

            vo.update(img[0], img_id)

            message = await create_message(vo, img, img_id)
            await send_message(websocket, message)
            cv2.waitKey(30)

        return 0

    except Exception as e:
        print(e)
        return 1


async def app(websocket):
    print("A client just connected")
    try:
        config = configparser.RawConfigParser()
        config.read('../dataset.cfg')
        dataset_info = dict(config.items('TO_READ'))

        run = await websocket.recv()
        if run == "run":
            status = await monocular_visual_odometry(websocket, dataset_info)
            if status == 0:
                print("Finished")
                await websocket.send("close")
            #     exit(0)
            # exit(1)

    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")


if __name__ == "__main__":
    start_server = websockets.serve(app, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
