import numpy as np
from src.read_euromav import read_euromav
from src.read_kitti import read_kitti

class PinholeCamera:  
    def __init__(
        self,
        width=None,
        height=None,
        fu=None,
        fv=None,
        cu=None,
        cv=None,
        distortion_model=None,
        distortion_coefficients=None,
        extrinsics=None,
        intrinsics=None,
    ):
        self.width = width
        self.height = height
        self.fu = fu
        self.fv = fv
        self.cu = cu
        self.cv = cv
        self.distortion_model = distortion_model
        self.distortion_coefficients = distortion_coefficients
        self.extrinsics = extrinsics
        self.intrinsics = intrinsics
        self.camera_matrix = self.cameraMatrix()

    def cameraMatrix(self):
        return np.array([[self.fu, 0, self.cu], [0, self.fv, self.cv], [0, 0, 1]])

    def print(self):
        print("PinholeCamera:")
        print("  width:", self.width)
        print("  height:", self.height)
        print("  fu:", self.fu)
        print("  fv:", self.fv)
        print("  cu:", self.cu)
        print("  cv:", self.cv)
        print("  distortion_model:", self.distortion_model)
        print("  distortion_coefficients:", self.distortion_coefficients)
        print("  extrinsics:", self.extrinsics)
        print("  intrinsics:", self.intrinsics)

    @classmethod
    def from_euromav(cls, file_path):
        data = read_euromav(file_path)

        width, height = data["resolution"]
        fu, fv, cu, cv = data["intrinsics"]
        distortion_model = data["distortion_model"]
        distortion_coefficients = np.array(data["distortion_coefficients"])
        extrinsics = np.array(data["T_BS"]["data"]).reshape(4, 4)
        intrinsics = np.array(data["intrinsics"])

        return cls(
            width,
            height,
            fu,
            fv,
            cu,
            cv,
            distortion_model,
            distortion_coefficients,
            extrinsics,
            intrinsics,
        )

    @classmethod
    def from_kitti(cls, file_path, width, height):
        data = read_kitti(file_path)

        width, height = width, height
        fu = float(data[0][1])
        fv = float(data[0][1])
        cu = float(data[0][3])
        cv = float(data[0][7])

        return cls(
            width,
            height,
            fu,
            fv,
            cu,
            cv,
        )
