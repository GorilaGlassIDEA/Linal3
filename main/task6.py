import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


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
vertices_cube2 = np.array([
    [2, 2, 2, 2, -2, -2, -2, -2],
    [-1, -1, -5, -5, -1, -1, -5, -5],
    [2, -2, 2, -2, 2, -2, 2, -2],
    [1, 1, 1, 1, 1, 1, 1, 1]
])
S1 = np.array([
    [0.3, 0, 0, 0],
    [0, 0.3, 0, 0],
    [0, 0, 0.3, 0],
    [0, 0, 0, 1]
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

faces_cube2 = np.array([
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [6, 2, 0, 4],
    [4, 0, 1, 5],
    [5, 7, 3, 1],
    [6, 2, 3, 7]
])
# Создание фигуры и осей
fig = plt.figure()
ax = fig.add_subplot(projection='3d', proj_type='ortho')

# Отрисовка куба
draw_shape(ax, vertices_cube, faces_cube, 'red')
draw_shape(ax, vertices_cube2, faces_cube2, 'blue')

# Настройки внешнего вида
ax.set_box_aspect([1, 1, 1])
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.view_init(azim=30, elev=30)

ticks = np.linspace(-5, 5, 11)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_zticks(ticks)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.savefig("task6.jpg", dpi=300, bbox_inches='tight')

plt.show()
