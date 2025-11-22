import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def rotation_matrix(v, theta):
    """
    v: вектор оси вращения [vx, vy, vz]
    theta: угол вращения в радианах
    """
    v = np.array(v, dtype=float)
    v = v / np.linalg.norm(v)  # нормализация оси
    vx, vy, vz = v
    J = np.array([
        [0, -vz, vy, 0],
        [vz, 0, -vx, 0],
        [-vy, vx, 0, 0],
        [0, 0, 0, 0]
    ])
    R = expm(J * theta)
    return R


def draw_shape(ax, vertices, faces, color, axes_vectors=None):
    """
    vertices: 4xN в однородных координатах
    axes_vectors: список векторов осей для визуализации [ [vx,vy,vz], ...]
    """
    verts = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(
        Poly3DCollection(verts[faces], facecolors=color, edgecolors='k', linewidths=0.5, alpha=0.8)
    )

    # Рисуем оси вращения максимально заметно
    if axes_vectors is not None:
        center = np.mean(verts, axis=0)  # центр куба
        colors = ['black']  # разные цвета для нескольких осей
        for i, v in enumerate(axes_vectors):
            v = np.array(v)
            ax.quiver(
                *center,  # начало стрелки (центр куба)
                *v,  # направление стрелки
                length=3.0,  # длина стрелки
                color=colors[i % len(colors)],
                linewidth=5,  # толщина линии
                normalize=True,  # нормализовать вектор
                arrow_length_ratio=0.25)  # размер наконечника стрелки
    # Настройки внешнего вида
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ticks = np.linspace(-2, 2, 5)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)
    ax.view_init(elev=30, azim=-37.5)


# Вершины куба
vertices_cube = np.array([
    [-1, -1, 1, 1, -1, -1, 1, 1],
    [-1, 1, 1, -1, -1, 1, 1, -1],
    [-1, -1, -1, -1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
])
faces_cube = np.array([
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 3, 7, 4],
    [1, 2, 6, 5]
])

# Параметры вращения
v1, theta1 = [0, 1, 0], np.pi / 3
v2, theta2 = [0, 0, 1], np.pi / 4

# 1) Вращение вокруг v1
R1 = rotation_matrix(v1, theta1)
vertices_rot1 = R1 @ vertices_cube

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
draw_shape(ax, vertices_rot1, faces_cube, 'red', axes_vectors=[v1])
plt.savefig("task4_rotation(pi_3).jpg", dpi=300, bbox_inches='tight')
plt.close()

# 2) Вращение вокруг v2
R2 = rotation_matrix(v2, theta2)
vertices_rot2 = R2 @ vertices_cube

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
draw_shape(ax, vertices_rot2, faces_cube, 'red', axes_vectors=[v2])
plt.savefig("task4_rotation(pi_4).jpg", dpi=300, bbox_inches='tight')
plt.close()

# 3) Композиция R1 R2
R12 = R2 @ R1
vertices_rot12 = R12 @ vertices_cube

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
draw_shape(ax, vertices_rot12, faces_cube, 'red', axes_vectors=[v1, v2])
plt.savefig("task4_rotation(pi_3_pi_4).jpg", dpi=300, bbox_inches='tight')
plt.close()

# 4) Композиция R2 R1
R21 = R1 @ R2
vertices_rot21 = R21 @ vertices_cube

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
draw_shape(ax, vertices_rot21, faces_cube, 'red', axes_vectors=[v1, v2])
plt.savefig("task4_rotation(pi_4_pi_3).jpg", dpi=300, bbox_inches='tight')
plt.close()
