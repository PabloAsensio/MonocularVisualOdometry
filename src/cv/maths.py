import cv2
import numpy as np

LK_PARAMS = dict(
    winSize=(7, 7),
    maxLevel=5,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
)


def findHomography(*args, **kwargs):
    """cv2.findHomography() wrapper"""
    h, msk = cv2.findHomography(*args, **kwargs)
    if msk is not None:
        msk = msk[:, 0].astype(np.bool)
    return h, msk


def findFundamental(*args, **kwargs):
    """cv2.findFundamentalMat() wrapper"""
    f, msk = cv2.findFundamentalMat(*args, **kwargs)
    if msk is not None:
        msk = msk[:, 0].astype(np.bool)
    return f, msk


def findEssential(F, camera):
    """Compute Essential matrix from Fundamental Matrix"""
    K = camera.intrinsics
    E = K.T @ F @ K
    return E


def projectPoints(*args, **kwargs):
    """cv2.projectPoints() wrapper"""
    pt2, jac = cv2.projectPoints(*args, **kwargs)
    return np.squeeze(pt2, axis=1)


def correctMatches(F, points1, points2):
    """Minimize the geometric error between corresponding image coordinates.
    For more information look into OpenCV's docs for the cv2.correctMatches function."""

    # Reshaping for cv2.correctMatches
    points1 = np.reshape(points1, (1, points1.shape[0], 2))
    points2 = np.reshape(points2, (1, points2.shape[0], 2))

    newPoints1, newPoints2 = cv2.correctMatches(F, points1, points2)

    return newPoints1[0], newPoints2[0]


def correctCameraDistorsion(points, camera):
    """Correct camera distorsion using the camera calibration matrix"""

    print("correctCameraDistorsion1:", points.shape, points.dtype)

    pts = points.copy()
    nb = pts.shape[0]
    pts.resize(nb, 1, 2)

    print("correctCameraDistorsion2:", pts.shape, pts.dtype)

    ud = cv2.undistortPoints(
        pts.astype(np.float64), camera.camera_matrix, camera.distortion_coefficients
    )
    ud.resize(nb, 2)
    ud = ud.astype(np.float32)
    # ud = np.hstack((ud, np.ones((nb, 1), dtype=np.float64)))

    print("correctCameraDistorsion3:", ud.shape, ud.dtype)
    return ud


def featureTracking(image_last, image_new, px_last):
    last = px_last.copy().astype(np.float32)
    kp2, st, err = cv2.calcOpticalFlowPyrLK(
        image_last, image_new, px_last, None, **LK_PARAMS
    )  # shape: [k,2] [k,1] [k,1]

    st = st.reshape(st.shape[0])
    kp1 = px_last[st == 1]
    kp2 = kp2[st == 1]

    # kp1 = np.hstack((kp1, np.ones((kp1.shape[0], 1), dtype=np.float64)))
    # kp2 = np.hstack((kp2, np.ones((kp2.shape[0], 1), dtype=np.float64)))
    # [u, v, 1]

    return kp1, kp2


def goodE(E):
    U, S, V = np.linalg.svd(E)
    S[2] = 0
    return U @ np.diagflat(S) @ V
