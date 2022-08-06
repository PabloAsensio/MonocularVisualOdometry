import configparser
from glob import glob

import cv2
import numpy as np
from tqdm import tqdm

from src import PinholeCamera, VisualOdometry


def read_groundtruth_timestamp(gt_file):
    with open(gt_file, "r") as f:
        gt = np.array([line.replace("\n", "").split(',') for line in f.readlines()])
        return gt[1:,0].copy().astype(np.uint64)


def load_images(imgs_path: str) -> list:
    images = []
    for fn in tqdm(sorted(glob(imgs_path)), desc="Loading images", ascii=True):
        img = cv2.imread(fn, 0)
        if img is not None:
            images.append(img)
    return images


def monocular_visual_odometry(info: dict) -> None:

    imgs = load_images(info['images_path'])

    if info['dataset'] not in ['euromav', 'kitti', 'vkitti2']: print("Dataset not supported".upper()); exit(0)

    if info['dataset'] == 'euromav':
        camera = PinholeCamera.from_euromav(info['calibration_file'])
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])
        vo.tss_gt = read_groundtruth_timestamp(info['ground_truth_file'])
    
    if info['dataset'] == 'kitti':
        camera = PinholeCamera.from_kitti(info['calibration_file'], width=1241, height=376)
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])

    if info['dataset'] == 'vkitti2':
        camera = PinholeCamera.from_vkitti2(info['calibration_file'], width=1242, height=375, camera=0)
        vo = VisualOdometry(camera, info['ground_truth_file'], dataset=info['dataset'])


    trajectory = np.zeros((1600, 1600, 3), dtype=np.uint8)

    for img_id, img in tqdm(enumerate(imgs), desc="Progress", ascii=True, total=len(imgs)):

        vo.update(img, img_id)

        ### 
        # Draw trajectory
        cur_t = vo.cur_t

        if img_id > 2:
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
        else:
            x, y, z = 0.0, 0.0, 0.0

        draw_x, draw_y = int(x) + 800, -int(z) + 800
        true_x, true_y = int(vo.trueX) + 800, -int(vo.trueZ) + 800

        # print("draw_x, draw_y: {}, {}".format(draw_x-800, draw_y-800))
        # print("true_x, true_y: {}, {}".format(true_x-800, true_y-800))
        # print("####################")

        cv2.circle(trajectory, (draw_x, draw_y), 1, (img_id * 255 / 4540, 255 - img_id * 255 / 4540, 0), 1)
        cv2.circle(trajectory, (true_x, true_y), 1, (0, 0, 255), 2)

        cv2.rectangle(trajectory, (10, 20), (600, 60), (0, 0, 0), -1)
        text = "Coordinates: x=%2fm y=%2fm z=%2fm" % (x, y, z)
        cv2.putText(trajectory, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8)

        cv2.imshow("Road facing camera", img)
        cv2.imshow("Trajectory", trajectory)
        ### Draw trajectory

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit(0)

    # cv2.imwrite("map.png", trajectory)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    config = configparser.RawConfigParser()
    config.read('../dataset.cfg')
    dataset_info = dict(config.items('TO_READ'))

    monocular_visual_odometry(dataset_info)
