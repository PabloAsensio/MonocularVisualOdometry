import asyncio
import configparser
import cv2
import websockets

from tqdm import tqdm

from src import PinholeCamera, VisualOdometry
from src.scales import read_eurocmav_timestamp_groundtruth
from src.utils import create_message, load_images, send_message

PORT = 7890

print("Server listening on Port " + str(PORT))


async def monocular_visual_odometry(websocket, info: dict) -> int:

    if info['dataset'] not in ['kitti', 'vkitti2', 'eurocmav']: return 1

    imgs, list_timestamps = load_images(info['images_path'])

    if info['dataset'] == 'eurocmav':
        print("From eurocmav".upper())
        camera = PinholeCamera.from_eurocmav(info['calibration_file'])
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])

        vo.frame_timestamps_list = list_timestamps
        vo.timestamp_groundtruth_list = read_eurocmav_timestamp_groundtruth(info['ground_truth_file'])
    
    if info['dataset'] == 'kitti':
        print("From kitti".upper())
        camera = PinholeCamera.from_kitti(info['calibration_file'], width=1241, height=376)
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])

    if info['dataset'] == 'vkitti2':
        print("From vkitti2".upper())
        camera = PinholeCamera.from_vkitti2(info['calibration_file'], width=1242, height=375, camera=0)
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])
        

    for img_id, img in tqdm(enumerate(imgs), desc="Progress", ascii=True, total=len(imgs)):

        if img_id == 0 or img_id == len(imgs):
            continue

        if vo.dataset == "eurocmav":
            vo.timestamp = list_timestamps[img_id]

        vo.update(img, img_id)

        message = await create_message(vo, img, img_id)
        await send_message(websocket, message)
        cv2.waitKey(30)

    return 0


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

            if status == 1:
                print('Something went wrong.')

    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")


if __name__ == "__main__":
    start_server = websockets.serve(app, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
