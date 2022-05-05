import cv2
from matplotlib import image
import numpy as np

from .maths import feature_tracking
from .pinhole_camera import PinholeCamera

STAGE_FIRST_FRAME = 0
STAGE_SECOND_FRAME = 1
STAGE_DEFAULT_FRAME = 2
kMinNumFeature = 1500

def read_annotations(annotations: str, dataset: str) -> list:
    with open(annotations, "r") as f:
            return f.readlines()

class VisualOdometry:
    def __init__(self, camera: PinholeCamera, annotations: str, dataset: str):
        self.dataset = dataset
        self.camera = camera
        self.frame_stage = 0
        self.new_frame = None
        self.last_frame = None
        self.cur_R = None
        self.cur_t = None
        self.px_ref = None
        self.px_cur = None
        self.focal = camera.fu
        self.pp = (camera.cu, camera.cv)
        self.trueX, self.trueY, self.trueZ = 0, 0, 0
        self.detector = cv2.FastFeatureDetector_create(threshold=25, nonmaxSuppression=True)
        self.annotations = read_annotations(annotations, dataset)
        
    def get_absolute_scale(self, frame_id: int) -> float:
        if self.dataset == "kitti":
            estimated, truth = get_absolute_scale_kitti(self.annotations, frame_id)
            self.trueX, self.trueY, self.trueZ = truth[0], truth[1], truth[2]
            return estimated
        
        if self.dataset == "vkitti2":
            estimated, truth = get_absolute_scale_vkitti2(self.annotations, frame_id)
            self.trueX, self.trueY, self.trueZ = truth[0], truth[1], truth[2]
            return estimated

        if self.dataset == "euromav":
            estimated, truth = get_absolute_scale_euromav(self.annotations, frame_id)
            self.trueX, self.trueY, self.trueZ = truth[0], truth[1], truth[2]
            return estimated

        print("Dataset not supported")
        exit(2)

    def process_first_frame(self) -> None:
        self.px_ref = self.detector.detect(self.new_frame)
        self.px_ref = np.array([x.pt for x in self.px_ref], dtype=np.float32)
        self.frame_stage = STAGE_SECOND_FRAME
    
    def process_second_frame(self) -> None:
        self.px_ref, self.px_cur = feature_tracking(self.last_frame, self.new_frame, self.px_ref)
        E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        _, self.cur_R, self.cur_t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
        self.frame_stage = STAGE_DEFAULT_FRAME 
        self.px_ref = self.px_cur

    def process_frame(self, frame_id: int) -> None:
        self.px_ref, self.px_cur = feature_tracking(self.last_frame, self.new_frame, self.px_ref)
        E, mask = cv2.findEssentialMat(self.px_cur, self.px_ref, focal=self.focal, pp=self.pp, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        _, R, t, mask = cv2.recoverPose(E, self.px_cur, self.px_ref, focal=self.focal, pp = self.pp)
        absolute_scale = self.get_absolute_scale(frame_id)
        if(absolute_scale > 0.1):
            self.cur_t = self.cur_t + absolute_scale * self.cur_R.dot(t) 
            self.cur_R = R.dot(self.cur_R)
        if(self.px_ref.shape[0] < kMinNumFeature):
            self.px_cur = self.detector.detect(self.new_frame)
            self.px_cur = np.array([x.pt for x in self.px_cur], dtype=np.float32)
        self.px_ref = self.px_cur

    def update(self, img: np.ndarray, frame_id: int, R=None, t=None) -> None:
        assert (
            img.ndim == 2
            and img.shape[0] == self.camera.height
            and img.shape[1] == self.camera.width
        ), "Frame: provided image has not the same size as the camera model or image is not grayscale"

        self.new_frame = img

        if self.frame_stage == STAGE_DEFAULT_FRAME:
            self.process_frame(frame_id)

        elif self.frame_stage == STAGE_SECOND_FRAME:
            self.process_second_frame()

        elif self.frame_stage == STAGE_FIRST_FRAME:
            self.process_first_frame()

        self.last_frame = self.new_frame

def get_absolute_scale_kitti(annotations: list, frame_id: int) -> tuple:
    ss = annotations[frame_id-1].strip().split()
    x_prev = float(ss[3])
    y_prev = float(ss[7])
    z_prev = float(ss[11])
    ss = annotations[frame_id].strip().split()
    x = float(ss[3])
    y = float(ss[7])
    z = float(ss[11])
    trueX, trueY, trueZ = x, y, z
    return (np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev) + (z - z_prev) * (z - z_prev))), (trueX, trueY, trueZ)

def get_absolute_scale_vkitti2(annotations: list, frame_id: int) -> tuple:
    ss = annotations[frame_id].strip().split()
    x_prev = float(ss[5])
    y_prev = float(ss[9])
    z_prev = float(ss[13])
    ss = annotations[frame_id+1].strip().split()
    x = float(ss[5])
    y = float(ss[9])
    z = float(ss[13])
    trueX, trueY, trueZ = x, y, z
    return (np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev) + (z - z_prev) * (z - z_prev))), (trueX, trueY, trueZ)

def get_absolute_scale_euromav(annotations: list, frame_id: int) -> tuple:
    mult = 10 if frame_id > 1 else 1
    frame_id *=  mult
    print(frame_id)
    ss = annotations[frame_id].strip().split(',')
    x_prev = float(ss[1])
    y_prev = float(ss[2])
    z_prev = float(ss[3])
    ss = annotations[frame_id+1].strip().split(',')
    x = float(ss[1])
    y = float(ss[2])
    z = float(ss[3])
    trueX, trueY, trueZ = x, y, z
    return (np.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev) + (z - z_prev) * (z - z_prev))), (trueX, trueY, trueZ)
 