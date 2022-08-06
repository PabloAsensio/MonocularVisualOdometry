from __future__ import groundtruth
from glob import glob
from json.tool import main

import cv2
import numpy as np
from tqdm import tqdm

import re

IMAGES_PATH = "/home/pablo/datasets/euromav/mav0/cam0/data/*.png"
GT_FILE = "/home/pablo/datasets/euromav/mav0/state_groundtruth_estimate0/data.csv"


with open(GT_FILE, "r") as f:
    gt = np.array([line.replace("\n", "").split(',') for line in f.readlines()])
    tss_gt = gt[1:,0].copy().astype(np.uint64)

def load_images(imgs_path: str) -> list:
    images = []
    ts = []
    for fn in tqdm(sorted(glob(imgs_path)), desc="Loading images", ascii=True):
        img = cv2.imread(fn, 0)
        if img is not None:
            images.append(img)
            ts.append( int(fn.split("/")[-1].split('.')[0]) )
    return images, ts

def read_groundtruth(groundtruth: str) -> list:
    with open(groundtruth, "r") as f:
        return f.readlines()

def find_timestamp(ts):
    return min(tss_gt, key=lambda x:abs(x-ts))

def grep(something, lines):
    for line in lines:
        if re.search(something, line):
            return line

if __name__ == "__main__":
    imgs, tss = load_images(IMAGES_PATH)
    groundtruth = read_groundtruth(GT_FILE)

    for i, img in enumerate(imgs):
        finded = find_timestamp(tss[i])
        print(tss[i], finded, tss[i] == finded)
        break
