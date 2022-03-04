import src.read_euromav as euromav
import numpy as np


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
        from_euromav=False,
        file_path=None,
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

        self.camera_matrix = np.array(
            [[self.fu, 0, self.cu], [0, self.fv, self.cv], [0, 0, 1]]
        )

        if from_euromav:
            if file_path is not None:
                self.from_euromav(file_path)
            else:
                raise ValueError("PinholeCamera: file_path is None")

    def from_euromav(self, file_path):
        data = euromav.read_euromav(file_path)

        try:
            self.width, self.height = data["resolution"]
            self.fu, self.fv, self.cu, self.cv = data["intrinsics"]
            self.distortion_model = data["distortion_model"]
            self.distortion_coefficients = np.array(data["distortion_coefficients"])
            self.extrinsics = np.array(data["T_BS"]["data"]).reshape(4, 4)
            self.intrinsics = np.array(data["intrinsics"])

            self.cameraMatrix()

        except KeyError as e:
            print(e)

    def cameraMatrix(self):
        self.camera_matrix = np.array(
            [[self.fu, 0, self.cu], [0, self.fv, self.cv], [0, 0, 1]]
        )
