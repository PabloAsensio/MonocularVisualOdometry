import numpy as np

from src.maths import rotationMatrix
from src.maths import rotation2Euler

R = rotationMatrix(0, 0, 0)

R1 = rotationMatrix(0, 0, np.pi / 2)
R2 = rotationMatrix(0, 0, np.pi)
R3 = rotationMatrix(0, 0, 3 * np.pi / 2)
R4 = rotationMatrix(0, 0, 2 * np.pi)

R5 = rotationMatrix(0, np.pi / 2, 0)
R6 = rotationMatrix(0, np.pi, 0)
R7 = rotationMatrix(0, 3 * np.pi / 2, 0)
R8 = rotationMatrix(0, 2 * np.pi, 0)

R9 = rotationMatrix(np.pi / 2, 0, 0)
R10 = rotationMatrix(np.pi, 0, 0)
R11 = rotationMatrix(3 * np.pi / 2, 0, 0)
R12 = rotationMatrix(2 * np.pi, 0, 0)


class TestRotationToEuler:
    def test_rotation_matrix_0_0_0(self):
        angles = rotation2Euler(R)
        assert (np.abs([0, 0, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_0_90(self):
        angles = rotation2Euler(R1)
        assert (np.abs([0, 0, np.pi / 2] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_0_180(self):
        angles = rotation2Euler(R2)
        assert (np.abs([0, 0, np.pi] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_0_270(self):
        angles = rotation2Euler(R3)
        assert (np.abs([0, 0, -np.pi / 2] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_0_360(self):
        angles = rotation2Euler(R4)
        assert (np.abs([0, 0, 2 * np.pi] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_90_0(self):
        angles = rotation2Euler(R5)
        assert (np.abs([0, np.pi / 2, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_180_0(self):
        angles = rotation2Euler(R6)
        assert (np.abs([0, np.pi, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_270_0(self):
        angles = rotation2Euler(R7)
        assert (np.abs([0, -np.pi / 2, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_0_360_0(self):
        angles = rotation2Euler(R9)
        assert (np.abs([0, 2 * np.pi, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_90_0_0(self):
        angles = rotation2Euler(R9)
        assert (np.abs([np.pi / 2, 0, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_180_0_0(self):
        angles = rotation2Euler(R10)
        assert (np.abs([np.pi, 0, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_270_0_0(self):
        angles = rotation2Euler(R11)
        assert (np.abs([-np.pi / 2, 0, 0] - angles) < 1e7 - 7).all()

    def test_rotation_matrix_360_0_0(self):
        angles = rotation2Euler(R12)
        assert (np.abs([2 * np.pi, 0, 0] - angles) < 1e7 - 7).all()


# Just to make sure that the np.mod runs as expected:
class TestMinusAlgles:
    def test_minus_angles_0_0_180(self):
        angles1 = np.array([0, 0, np.pi])
        angles2 = np.array([0, 0, -np.pi])
        assert (np.abs(angles1 - np.mod(angles2, 360)) < 1e7 - 7).all()

    def test_minus_angles_0_0_270(self):
        angles1 = np.array([0, 0, 3 * np.pi / 2])
        angles2 = np.array([0, 0, -np.pi / 2])
        assert (np.abs(angles1 - np.mod(angles2, 360)) < 1e7 - 7).all()

    def test_minus_angles_0_180_0(self):
        angles1 = np.array([0, np.pi, 0])
        angles2 = np.array([0, -np.pi, 0])
        assert (np.abs(angles1 - np.mod(angles2, 360)) < 1e7 - 7).all()

    def test_minus_angles_0_270_0(self):
        angles1 = np.array([0, 3 * np.pi / 2, 0])
        angles2 = np.array([0, -np.pi / 2, 0])
        assert (np.abs(angles1 - np.mod(angles2, 360)) < 1e7 - 7).all()

    def test_minus_angles_180_0_0(self):
        angles1 = np.array([np.pi, 0, 0])
        angles2 = np.array([-np.pi, 0, 0])
        assert (np.abs(angles1 - np.mod(angles2, 360)) < 1e7 - 7).all()

    def test_minus_angles_270_0_0(self):
        angles1 = np.array([3 * np.pi / 2, 0, 0])
        angles2 = np.array([-np.pi / 2, 0, 0])
        assert (np.abs(angles1 - np.mod(angles2, 360)) < 1e7 - 7).all()
