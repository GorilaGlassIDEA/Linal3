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

S1 = np.array([
    [0.5, 0, 0, 0],  # уменьшаем по X в 2 раза
    [0, 1, 0, 0],  # Y без изменений
    [0, 0, 1, 0],  # Z без изменений
    [0, 0, 0, 1]
])
S2 = np.array([
    [1, 0, 0, 0],  # уменьшаем по X в 2 раза
    [0, 1, 0, 0],  # Y без изменений
    [0, 0, 0.5, 0],  # Z без изменений
    [0, 0, 0, 1]
])

S_total = S1 @ S2
# Индексы вершин для граней куба
faces_cube = np.array([
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 3, 7, 4],
    [1, 2, 6, 5]
])

# Создание фигуры и осей
vertices_cube = S_total @ vertices_cube
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
plt.savefig("task2_total.jpg", dpi=300, bbox_inches='tight')

plt.show()
