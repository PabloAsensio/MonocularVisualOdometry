import numpy as np

from src.maths import rotationMatrix

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


# Minus matrices (not necesary, but nice to have)
R13 = rotationMatrix(0, 0, -np.pi / 2)
R14 = rotationMatrix(0, 0, -np.pi)
R15 = rotationMatrix(0, 0, -3 * np.pi / 2)
R16 = rotationMatrix(0, 0, -2 * np.pi)

R17 = rotationMatrix(0, -np.pi / 2, 0)
R18 = rotationMatrix(0, -np.pi, 0)
R19 = rotationMatrix(0, -3 * np.pi / 2, 0)
R20 = rotationMatrix(0, -2 * np.pi, 0)

R21 = rotationMatrix(-np.pi / 2, 0, 0)
R22 = rotationMatrix(-np.pi, 0, 0)
R23 = rotationMatrix(-3 * np.pi / 2, 0, 0)
R24 = rotationMatrix(-2 * np.pi, 0, 0)


class TestRotationMatrixSign:
    def test_minus_0_0_90(self):
        assert (np.abs(R1 - R15) < 1e7 - 7).all()

    def test_minus_0_0_180(self):
        assert (np.abs(R2 - R14) < 1e7 - 7).all()

    def test_minus_0_0_270(self):
        assert (np.abs(R3 - R13) < 1e7 - 7).all()

    def test_rotation_matrix_0_0_360(self):
        assert (np.abs(R16 - R) < 1e7 - 7).all()

    def test_minus_0_90_0(self):
        assert (np.abs(R5 - R19) < 1e7 - 7).all()

    def test_minus_0_180_0(self):
        assert (np.abs(R6 - R18) < 1e7 - 7).all()

    def test_minus_0_270_0(self):
        assert (np.abs(R7 - R17) < 1e7 - 7).all()

    def test_minus_0_360_0(self):
        assert (np.abs(R8 - R) < 1e7 - 7).all()

    def test_minus_90_0_0(self):
        assert (np.abs(R9 - R23) < 1e7 - 7).all()

    def test_minus_180_0_0(self):
        assert (np.abs(R10 - R22) < 1e7 - 7).all()

    def test_minus_270_0_0(self):
        assert (np.abs(R11 - R21) < 1e7 - 7).all()

    def test_minus_360_0_0(self):
        assert (np.abs(R12 - R) < 1e7 - 7).all()
