import cv2
import numpy as np

lk_params = dict(
    winSize=(21, 21),
    # maxLevel = 3,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
)

def correct_matches(F, points1, points2):
    """Minimize the geometric error between corresponding image coordinates.
    For more information look into OpenCV's docs for the cv2.correctMatches function."""

    # Reshaping for cv2.correctMatches
    points1 = np.reshape(points1, (1, points1.shape[0], 2))
    points2 = np.reshape(points2, (1, points2.shape[0], 2))

    newPoints1, newPoints2 = cv2.correctMatches(F, points1, points2)

    return newPoints1[0], newPoints2[0]


def correct_camera_distorsion(points, camera):
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


def feature_tracking(image_ref, image_cur, px_ref):
	kp2, st, _ = cv2.calcOpticalFlowPyrLK(image_ref, image_cur, px_ref, None, **lk_params)  #shape: [k,2] [k,1] [k,1]

	st = st.reshape(st.shape[0])
	kp1 = px_ref[st == 1]
	kp2 = kp2[st == 1]

	return kp1, kp2


def goodE(E):
    U, S, V = np.linalg.svd(E)
    S[2] = 0
    return U @ np.diagflat(S) @ V
