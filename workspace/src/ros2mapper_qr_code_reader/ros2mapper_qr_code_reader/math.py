"""Calculate the math needed by the camera node. Mostly matrix calculations

Sources:
    - [Rotation matrices](https://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations)
    - [Quaternion -> Euler angles](shorturl.at/djB89)
    - [Quaternion rotation of angle between two vectors](https://stackoverflow.com/a/1171995)
"""
from math import asin, atan2, cos, sin

import numpy as np
from numpy import ndarray


def rotate_x(x_angle: float) -> ndarray:
    """Get 3d rotation matrix of the x angle"""
    return np.array(
        [
            [1, 0, 0],
            [0, cos(x_angle), -sin(x_angle)],
            [0, sin(x_angle), cos(x_angle)],
        ]
    )


def rotate_y(y_angle: float) -> ndarray:
    """Get 3d rotation matrix of the y angle"""
    return np.array(
        [
            [cos(y_angle), 0, sin(y_angle)],
            [0, 1, 0],
            [-sin(y_angle), 0, cos(y_angle)],
        ]
    )


def rotate_z(z_angle: float) -> ndarray:
    """Get 3d rotation matrix of the z angle"""
    return np.array(
        [
            [cos(z_angle), -sin(z_angle), 0],
            [sin(z_angle), cos(z_angle), 0],
            [0, 0, 1],
        ]
    )


def get_rotation_matrix(rotation: ndarray) -> ndarray:
    """Get 3d rotation matrix of the euler rotation angles"""
    x_angle, y_angle, z_angle = rotation
    return np.matmul(rotate_z(z_angle), np.matmul(rotate_y(y_angle), rotate_x(x_angle)))


def quaternion_to_euler(q: ndarray) -> ndarray:
    """Convert quaternion angles to euler angles"""
    return np.array(
        [
            [atan2(2 * (q[0] * q[1] + q[2] * q[3]), 1 - 2 * (q[1] ** 2 + q[2] ** 2))],
            [asin(2 * (q[0] * q[2] - q[3] * q[1]))],
            [atan2(2 * (q[0] * q[3] + q[1] * q[2]), 1 - 2 * (q[2] ** 2 + q[3] ** 2))],
        ]
    )


def quaternion_of_vectors(v1: ndarray, v2: ndarray) -> ndarray:
    """Get the quaternion between two vectors"""
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    a = np.cross(v1, v2)
    return np.array(
        [
            np.linalg.norm(v1) * np.linalg.norm(v2) + np.dot(v1, v2),
            a[0],
            a[1],
            a[2],
        ]
    )
