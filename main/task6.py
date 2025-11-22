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


def translation_matrix(tx, ty, tz):
    """Матрица переноса"""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])


def draw_cube_comparison(ax, vertices_original, vertices_rotated, faces, rotation_point=None):
    """
    Рисует исходный и повернутый куб на одном графике
    """
    # Преобразуем вершины в декартовы координаты
    verts_orig = (vertices_original[:3, :] / vertices_original[3, :]).T
    verts_rot = (vertices_rotated[:3, :] / vertices_rotated[3, :]).T

    # Рисуем исходный куб (полупрозрачный)
    ax.add_collection3d(
        Poly3DCollection(verts_orig[faces], facecolors='blue', edgecolors='k',
                         linewidths=1, alpha=0.3)
    )

    # Рисуем повернутый куб
    ax.add_collection3d(
        Poly3DCollection(verts_rot[faces], facecolors='red', edgecolors='k',
                         linewidths=1, alpha=0.8)
    )

    # Отмечаем точку вращения
    if rotation_point is not None:
        ax.scatter(*rotation_point, color='green', s=100, marker='o', label='Центр вращения')

    # Настройки отображения
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ticks = np.linspace(-2, 2, 5)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)

    ax.view_init(elev=20, azim=45)
    ax.legend()


# Вершины куба (единичный куб от -1 до 1)
vertices_cube = np.array([
    [-1, -1, 1, 1, -1, -1, 1, 1],  # x
    [-1, 1, 1, -1, -1, 1, 1, -1],  # y
    [-1, -1, -1, -1, 1, 1, 1, 1],  # z
    [1, 1, 1, 1, 1, 1, 1, 1]  # w
])

faces_cube = np.array([
    [0, 1, 2, 3],  # задняя грань
    [4, 5, 6, 7],  # передняя грань
    [0, 1, 5, 4],  # нижняя грань
    [2, 3, 7, 6],  # верхняя грань
    [0, 3, 7, 4],  # левая грань
    [1, 2, 6, 5]  # правая грань
])

# Параметры вращения вокруг вершины (1,1,1)
rotation_point = np.array([1, 1, 1])
rotation_angle = np.pi / 4  # 45 градусов
rotation_axis = [1, 0, 0]  # ось OX

print("=== ВРАЩЕНИЕ КУБА ВОКРУГ ВЕРШИНЫ (1,1,1) ===")
print(f"Точка вращения: {rotation_point}")
print(f"Угол вращения: {np.degrees(rotation_angle):.1f}°")
print(f"Ось вращения: {rotation_axis}")

# 1. Матрица переноса точки вращения в начало координат
T1 = translation_matrix(-rotation_point[0], -rotation_point[1], -rotation_point[2])
print(f"\n1. Матрица переноса в начало координат T1:")
print(T1)

# 2. Матрица вращения вокруг оси OX в начале координат
R = rotation_matrix(rotation_axis, rotation_angle)
print(f"\n2. Матрица вращения вокруг OX на 45° R:")
print(R)

# 3. Матрица обратного переноса
T2 = translation_matrix(rotation_point[0], rotation_point[1], rotation_point[2])
print(f"\n3. Матрица обратного переноса T2:")
print(T2)

# 4. Итоговая матрица преобразования
T_final = T2 @ R @ T1
print(f"\n4. Итоговая матрица преобразования T_final = T2 * R * T1:")
print(T_final)

# Применяем преобразование к вершинам куба
vertices_rotated = T_final @ vertices_cube

# Визуализация
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')

draw_cube_comparison(ax, vertices_cube, vertices_rotated, faces_cube, rotation_point)

# Добавляем ось вращения (проходит через точку вращения)
axis_length = 3
ax.quiver(rotation_point[0], rotation_point[1], rotation_point[2],
          rotation_axis[0], rotation_axis[1], rotation_axis[2],
          length=axis_length, color='black', linewidth=3,
          arrow_length_ratio=0.2, label='Ось вращения (OX)')

plt.title(f'Вращение куба вокруг вершины (1,1,1) на 45° вокруг OX')
plt.tight_layout()
plt.savefig("task5_(1_1_1).jpg", dpi=300, bbox_inches='tight')
plt.show()

# Дополнительная информация для отчета
print(f"\n=== РЕЗУЛЬТАТ ===")
print("Исходные вершины куба:")
print(vertices_cube[:3, :].T)
print("\nПовернутые вершины куба:")
print(vertices_rotated[:3, :].T)

# Проверка: вершина вращения должна остаться на месте
vertex_index = 7  # вершина (1,1,1) имеет индекс 7 в нашем массиве
original_vertex = vertices_cube[:3, vertex_index]
rotated_vertex = vertices_rotated[:3, vertex_index]
print(f"\nПроверка: вершина вращения {tuple(original_vertex)} -> {tuple(rotated_vertex)}")
print(f"Расстояние после преобразования: {np.linalg.norm(original_vertex - rotated_vertex):.6f}")