from scipy.spatial.transform import Rotation as R

def quaternion2Rotation(qw, qx, qy, qz):
    return R.from_quat([qw, qx, qy, qz]).as_matrix()