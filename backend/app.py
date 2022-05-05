from glob import glob

import cv2
import numpy as np
from tqdm import tqdm

from src.cv import PinholeCamera, VisualOdometry

CAMERA_SETTINS = "./datasets/MH_01_easy/mav0/cam0/sensor.yaml"
IMAGES_PATH = "./datasets/MH_01_easy/mav0/cam0/data/*.png"

KITTI_CALIB = "/home/pablo/datasets/kitti/KITTI_odometry_gray/sequences/00/calib.txt"
KITTI_TRUTH = "/home/pablo/datasets/kitti/KITTI_odometry_poses/poses/00.txt"
KITTI_IMGS = "/home/pablo/datasets/kitti/KITTI_odometry_gray/sequences/00/image_0/*.png"

VKITTI2_CALIB = "/home/pablo/datasets/vkitti2/gt/Scene20/clone/intrinsic.txt"
VKITTI2_TRUTH = "/home/pablo/datasets/vkitti2/gt/Scene20/clone/extrinsic.txt"
VKITTI2_IMGS = "/home/pablo/datasets/vkitti2/rgb/Scene20/clone/frames/rgb/Camera_0/*.jpg"

IMG_PATH = "/home/pablo/github-proyects/MonocularVisualOdometry/1403636579763555584.png"

def read_images(imgs_path):
    images = []
    for fn in tqdm(sorted(glob(imgs_path)), desc="Loading images", ascii=True):
        img = cv2.imread(fn, 0)
        if img is not None:
            images.append(img)
    return images


def main(imgs_path):

    imgs = read_images(imgs_path) # precharge images

    # camera = PinholeCamera.from_kitti(KITTI_CALIB, width=1241, height=376)
    # camera.print()

    # KITTI dataset
    # camera = PinholeCamera(1241.0, 376.0, 718.8560, 718.8560, 607.1928, 185.2157)
    # vo = VisualOdometry(camera, KITTI_TRUTH, dataset="KITTI")

    # VKITTI2 dataset
    camera = PinholeCamera(1242.0, 375.0, 725.0087, 725.0087, 620.5, 187.0)
    vo = VisualOdometry(camera, VKITTI2_TRUTH, dataset="VKITTI2")

    print(vo.annotations[0])

    trajectory = np.zeros((1600, 1600, 3), dtype=np.uint8)

    for img_id, img in tqdm(enumerate(imgs), desc="Progress", ascii=True, total=len(imgs)):

        if img_id == 0:
            if vo.dataset == "VKITTI2":
                pass
            continue

        print("####################")
        print("img_id: {}".format(img_id))
        vo.update(img, img_id)

        ### 
        # Draw trajectory
        cur_t = vo.cur_t
        if img_id > 2:
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
        else:
            x, y, z = 0.0, 0.0, 0.0
        draw_x, draw_y = int(x) + 800, -int(z) + 800
        true_x, true_y = -int(vo.trueX) + 800, int(vo.trueY) + 800

        print("draw_x, draw_y: {}, {}".format(draw_x-800, draw_y-800))
        print("true_x, true_y: {}, {}".format(true_x-800, true_y-800))
        print("####################")

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

    cv2.imwrite("map.png", trajectory)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    main(VKITTI2_IMGS)
