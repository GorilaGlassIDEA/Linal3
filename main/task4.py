import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def rotation_matrix(v, theta):
    """
    v: вектор оси вращения [vx, vy, vz]
    theta: угол вращения в радианах
    """
    vx, vy, vz = v
    # Матрица J (4x4)
    J = np.array([
        [0, -vz, vy, 0],
        [vz, 0, -vx, 0],
        [-vy, vx, 0, 0],
        [0, 0, 0, 0]
    ])
    # Экспонента матрицы J
    R = expm(J * theta)
    return R


def draw_shape(ax, vertices, faces, color):
    # Преобразуем вершины из однородных координат
    vertices = (vertices[:3, :] / vertices[3, :]).T
    # Добавляем 3D-полигоны
    ax.add_collection3d(
        Poly3DCollection(vertices[faces], facecolors=color, edgecolors='k', linewidths=0.2)
    )


# Вершины куба в однородных координатах
vertices_cube = np.array([
    [-1, -1, 1, 1, -1, -1, 1, 1],
    [-1, 1, 1, -1, -1, 1, 1, -1],
    [-1, -1, -1, -1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
])
# Индексы вершин для граней куба
faces_cube = np.array([
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 3, 7, 4],
    [1, 2, 6, 5]
])

v1 = [0, 1, 0]
theta = np.pi / 3  # поворот на 45 градусов
v2 = [0, 0, 1]
theta2 = np.pi / 4 # поворот на 45 градусов
r1 = rotation_matrix(v1, theta) @ rotation_matrix(v2, theta2)
vertices_cube = r1 @ vertices_cube

fig = plt.figure()
ax = fig.add_subplot(projection='3d', proj_type='ortho')

# Отрисовка куба
draw_shape(ax, vertices_cube, faces_cube, 'red')

# Настройки внешнего вида
ax.set_box_aspect([1, 1, 1])
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.view_init(elev=30, azim=-37.5)

# Подписи осей и деления
ticks = np.linspace(-1, 1, 5)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_zticks(ticks)
plt.savefig("task4_rotation(pi_3_pi_4).jpg", dpi=300, bbox_inches='tight')

plt.show()
