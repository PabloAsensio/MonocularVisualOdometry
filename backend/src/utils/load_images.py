from glob import glob

import cv2
from tqdm import tqdm


def load_images(imgs_path: str) -> list:
    images = []
    ts = []
    for fn in tqdm(sorted(glob(imgs_path)), desc="Loading images", ascii=True):
        img = cv2.imread(fn, 0)
        if img is not None:
            images.append(img)
            try:
                ts.append( int(fn.split("/")[-1].split('.')[0]) )
            except:
                pass
    return images, ts
