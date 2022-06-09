import asyncio
import configparser
from base64 import b64encode
from glob import glob

import cv2
import websockets
from tqdm import tqdm

from src import PinholeCamera, VisualOdometry
from src.utils import create_message, load_images, send_message

PORT = 7890

print("Server listening on Port " + str(PORT))


async def monocular_visual_odometry(websocket, info: dict) -> int:
    try:
        if info['dataset'] == 'euromav':
            camera = PinholeCamera.from_euromav(info['calibration_file'])
            camera.print()
            vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])
        if info['dataset'] == 'kitti':
            print("from kitti")
            camera = PinholeCamera.from_kitti(info['calibration_file'], width=1241, height=376)
            vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])
        
        # camera = PinholeCamera(1242.0, 375.0, 725.0087, 725.0087, 620.5, 187.0)
        # vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])

        imgs, tss = load_images(info['images_path'])

        for img_id, img in tqdm(enumerate(imgs), desc="Progress", ascii=True, total=len(imgs)):

            if img_id == 0:
                if vo.dataset == "VKITTI2":
                    pass
                continue

            vo.ts = tss[img_id]
            vo.update(img, img_id)

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
