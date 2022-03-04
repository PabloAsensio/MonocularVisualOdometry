from glob import glob

import cv2
import numpy as np

from src.cv import PinholeCamera
from src.maths import rotation2Euler, rotationCamera2Horizon
from src.cv import VisualOdometry

camara_settins = "./datasets/MH_01_easy/mav0/cam0/sensor.yaml"

camera = PinholeCamera(752.0, 480.0, 458.654, 457.296, 367.215, 248.375)
camera.from_euromav(camara_settins)
visual_odometry = VisualOdometry(camera)

trajectory = np.zeros((600, 600, 3), dtype=np.uint8)


def read_images():
    images = []
    img_mask = "./datasets/MH_01_easy/mav0/cam0/data/*.png"
    for fn in sorted(glob(img_mask)):
        img = cv2.imread(fn, -1)
        if img is not None:
            images.append(img)
    return images


if __name__ == "__main__":

    print("Loading images...")
    imgs = read_images()
    print("Loaded %d images." % len(imgs))

    n = 0.0  # north
    e = 0.0  # east
    d = 0.0  # down

    for img_id, img in enumerate(imgs):
        print("############################################")
        print("Image: %d" % img_id)
        print("############################################")

        visual_odometry.update(img, img_id)

        R = visual_odometry.R
        t = visual_odometry.t
        # print(visual_odometry.R, R)
        # print(visual_odometry.t, t)

        anlges = np.array([0, 0, 0])

        if img_id > 2:
            angles = rotation2Euler(R)
            n = angles[0]
            e = angles[1]
            d = anlges[2]
        x, y, z = t[0], t[1], t[2]

        draw_x, draw_y = int(x) + 300, int(y) + 300

        cv2.circle(
            trajectory,
            (draw_x, draw_y),
            1,
            (img_id * 255 / 4540, 255 - img_id * 255 / 4540, 0),
            1,
        )

        cv2.rectangle(trajectory, (10, 20), (600, 60), (0, 0, 0), -1)

        x = round(float(x), 2)
        y = round(float(y), 2)
        z = round(float(z), 2)
        n = round(float(n), 2)
        e = round(float(e), 2)
        d = round(float(d), 2)

        text = "Coordinates: \n x=%2fm y=%2fm z=%2fm \n n=%2f  e=%2f  d=%2f" % (
            x,
            y,
            z,
            n,
            e,
            d,
        )
        y0, dy = 20, 20
        for i, line in enumerate(text.split("\n")):
            y = y0 + i * dy
            cv2.putText(
                trajectory,
                line,
                (20, y),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255, 255, 255),
                1,
                8,
            )

        cv2.imshow("Camera view", img)
        cv2.imshow("Trajectory", trajectory)
        cv2.waitKey(1)

        # if img_id == 4:
        #     break

    cv2.imwrite("map.png", trajectory)
    cv2.destroyAllWindows()
