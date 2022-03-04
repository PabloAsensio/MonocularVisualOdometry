import numpy as np
import cv2

from .pinhole_camera import PinholeCamera
from .maths import *

STAGE_FIRST_FRAME = 0
STAGE_SECOND_FRAME = 1
STAGE_DEFAULT_FRAME = 2
kMinNumFeature = 120

# https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html#ga40919d0c7eaf77b0df67dd76d5d24fa1
def findRt(last_frame, new_frame, px_last, focal, pp, camera):
    print("%%%%%%%% findRT1:", px_last.shape, px_last.dtype)

    # find caracteristic points
    px_last, px_new = featureTracking(last_frame, new_frame, px_last)

    print("%%%%%%%% findRT2:", px_last.shape, px_last.dtype, px_new.shape, px_new.dtype)

    # px_last = correctCameraDistorsion(px_last, camera)
    # px_new = correctCameraDistorsion(px_new, camera)

    print("findRT:", px_last.shape, px_last.dtype)
    px_last = correctCameraDistorsion(px_last, camera)
    print("findRT:", px_new.shape, px_new.dtype)
    # px_new = correctCameraDistorsion(px_new, camera)  # HEREEEEEEEEEEEEEEEEEEEEEEE

    print("%%%%%%%% findRT3:", px_last.shape, px_last.dtype)

    F, _ = findFundamental(px_last, px_new, cv2.FM_RANSAC)

    px_last, px_new = correctMatches(F, px_last, px_new)

    # E = findEssential(F, camera)

    E, _ = cv2.findEssentialMat(
        px_last,
        px_new,
        focal=focal,
        pp=pp,
        method=cv2.RANSAC,
        # method=cv2.LMEDS,
        prob=0.999,
        threshold=1.0,
    )

    E = goodE(E)

    _, R, t, _ = cv2.recoverPose(E, px_last, px_new, focal=focal, pp=pp)

    return R, t, px_new


class VisualOdometry:
    def __init__(self, camera: PinholeCamera):
        self.camera = camera
        self.frame_stage = 0
        self.new_frame = None
        self.last_frame = None
        self.R = np.eye(3)
        self.t = np.zeros((3, 1))
        self.px_last = None
        self.px_new = None
        self.focal = camera.fu
        self.pp = (camera.cu, camera.cv)
        self.detector = cv2.FastFeatureDetector_create(
            threshold=25, nonmaxSuppression=True
        )

    def getAbsoluteScale(self, frame_id):
        return 1

    def processFirstFrame(self):
        self.px_last = self.detector.detect(self.new_frame)
        self.px_last = np.array([x.pt for x in self.px_last], dtype=np.float32)
        self.frame_stage = STAGE_SECOND_FRAME

    def processSecondFrame(self):
        self.R, self.t, self.px_new = findRt(
            self.last_frame,
            self.new_frame,
            self.px_last,
            self.focal,
            self.pp,
            self.camera,
        )
        self.frame_stage = STAGE_DEFAULT_FRAME
        self.px_last = self.px_new

    def processFrame(self, frame_id):
        print(
            "processFrame:",
            self.last_frame.shape,
            self.new_frame.shape,
            self.px_last.shape,
            self.px_last.dtype,
        )

        R, t, self.px_new = findRt(
            last_frame=self.last_frame,
            new_frame=self.new_frame,
            px_last=self.px_last,
            focal=self.focal,
            pp=self.pp,
            camera=self.camera,
        )

        absolute_scale = self.getAbsoluteScale(frame_id)

        if absolute_scale > 0.1:
            self.t = self.t + absolute_scale * self.R @ t
            self.R = R @ self.R

        if self.px_last.shape[0] < kMinNumFeature:
            self.px_new = self.detector.detect(self.new_frame)
            self.px_new = np.array([x.pt for x in self.px_new], dtype=np.float32)

        self.px_last = self.px_new

    def update(self, img, frame_id):
        assert (
            img.ndim == 2
            and img.shape[0] == self.camera.height
            and img.shape[1] == self.camera.width
        ), "Frame: provided image has not the same size as the camera model or image is not grayscale"

        self.new_frame = img

        if self.frame_stage == STAGE_DEFAULT_FRAME:
            self.processFrame(frame_id)

        elif self.frame_stage == STAGE_SECOND_FRAME:
            self.processSecondFrame()

        elif self.frame_stage == STAGE_FIRST_FRAME:
            self.processFirstFrame()

        self.last_frame = self.new_frame
