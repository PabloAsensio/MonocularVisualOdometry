import numpy as np
from glob import glob
import os
import os.path
import cv2
import math

from src.visual_odometry import PinholeCamera, VisualOdometry


cam = PinholeCamera(752.0, 480.0, 458.654, 457.296, 367.215, 248.375)
vo = VisualOdometry(cam)

traj = np.zeros((600, 600, 3), dtype=np.uint8)


def read_image():

    images = []
    img_mask = "./datasets/*/mav0/cam0/data/*.png"
    for fn in sorted(glob(img_mask)):
        img = cv2.imread(fn, -1)
        if img is not None:
            images.append(img)
    return images


def isRotationMatrix(R):

    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


def rotationMatrixToEulerAngles(R):

    assert isRotationMatrix(R)
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


if __name__ == "__main__":

    imgs = read_image()

    for img_id, img in enumerate(imgs):

        if img_id == 0:
            continue

        if img is not None:
            vo.update(img, img_id)
        cur_t = vo.cur_t
        cur_R = vo.cur_R
        anlges = np.array([0, 0, 0])
        n = 0.0
        e = 0.0
        d = 0.0
        if img_id > 2:
            x, y, z = cur_t[0], cur_t[1], cur_t[2]
            angles = rotationMatrixToEulerAngles(cur_R)
            n = angles[0]
            e = angles[1]
            d = anlges[2]
        else:
            x, y, z = 0.0, 0.0, 0.0
        draw_x, draw_y = int(x) + 290, int(z) + 90

        cv2.circle(
            traj,
            (draw_x, draw_y),
            1,
            (img_id * 255 / 4540, 255 - img_id * 255 / 4540, 0),
            1,
        )
        cv2.rectangle(traj, (10, 20), (600, 60), (0, 0, 0), -1)
        text = "Coordinates: x=%2fm y=%2fm z=%2fm '\n' n=%2fm e==%2fm d=%2fm " % (
            x,
            y,
            z,
            n,
            e,
            d,
        )
        cv2.putText(
            traj, text, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, 8
        )

        cv2.imshow("Camera view", img)
        cv2.imshow("Trajectory", traj)
        cv2.waitKey(1)

    cv2.imwrite("map.png", traj)
