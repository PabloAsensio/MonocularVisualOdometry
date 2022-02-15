import numpy as np

from src.maths.rotation_matrix import rotation_matrix

R = rotation_matrix(0, 0, 0)

R1 = rotation_matrix(0, 0, np.pi / 2)
R2 = rotation_matrix(0, 0, np.pi)
R3 = rotation_matrix(0, 0, 3 * np.pi / 2)
R4 = rotation_matrix(0, 0, 2 * np.pi)

R5 = rotation_matrix(0, np.pi / 2, 0)
R6 = rotation_matrix(0, np.pi, 0)
R7 = rotation_matrix(0, 3 * np.pi / 2, 0)
R8 = rotation_matrix(0, 2 * np.pi, 0)

R9 = rotation_matrix(np.pi / 2, 0, 0)
R10 = rotation_matrix(np.pi, 0, 0)
R11 = rotation_matrix(3 * np.pi / 2, 0, 0)
R12 = rotation_matrix(2 * np.pi, 0, 0)


class TestRotationMatrix:
    def test_determinat(self):
        assert np.linalg.det(R) == 1

    def test_ortonormal(self):
        assert (np.linalg.inv(R) == R.T).all() == True

    def test_rotation_matrix_0_0_0(self):
        assert (np.abs(R - np.eye(3)) < 1e-12).all()  # Identity matrix

    def test_rotation_matrix_0_0_90(self):
        assert (np.abs(R1 - np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])) < 1e-12).all()

    def test_rotation_matrix_0_0_180(self):
        assert (
            np.abs(R2 - np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])) < 1e-12
        ).all()

    def test_rotation_matrix_0_0_270(self):
        assert (np.abs(R3 - np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])) < 1e-12).all()

    def test_rotation_matrix_0_0_360(self):
        assert (np.abs(R4 - np.eye(3)) < 1e-12).all()  # Identity matrix

    def test_rotation_matrix_0_90_0(self):
        assert (np.abs(R5 - np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])) < 1e-12).all()

    def test_rotation_matrix_0_180_0(self):
        assert (
            np.abs(R6 - np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])) < 1e-12
        ).all()

    def test_rotation_matrix_0_270_0(self):
        assert (np.abs(R7 - np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])) < 1e-12).all()

    def test_rotation_matrix_0_360_0(self):
        assert (np.abs(R8 - np.eye(3)) < 1e-12).all()  # Identity matrix

    def test_rotation_matrix_90_0_0(self):
        assert (np.abs(R9 - np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])) < 1e-12).all()

    def test_rotation_matrix_180_0_0(self):
        assert (
            np.abs(R10 - np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])) < 1e-12
        ).all()

    def test_rotation_matrix_270_0_0(self):
        assert (
            np.abs(R11 - np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])) < 1e-12
        ).all()

    def test_rotation_matrix_360_0_0(self):
        assert (np.abs(R12 - np.eye(3)) < 1e-12).all()  # Identity matrix
