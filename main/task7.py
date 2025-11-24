import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.linalg import expm


def draw_shape(ax, vertices, faces, color):
    # Преобразуем вершины из однородных координат
    vertices = (vertices[:3, :] / vertices[3, :]).T
    # Добавляем 3D-полигоны
    ax.add_collection3d(
        Poly3DCollection(vertices[faces], facecolors=color, edgecolors='k', linewidths=0.2, alpha=0.7)
    )


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


def create_camera_matrix(position, rotation_angles):
    """
    Создает матрицу преобразования камеры C
    position: [x, y, z] - положение камеры
    rotation_angles: [yaw, pitch, roll] - углы поворота в радианах
    """
    # Матрица переноса камеры
    Tc = translation_matrix(position[0], position[1], position[2])

    # Матрицы поворота камеры (в обратном порядке)
    yaw, pitch, roll = rotation_angles

    # Поворот вокруг оси Y (yaw)
    R_yaw = np.array([
        [np.cos(yaw), 0, np.sin(yaw), 0],
        [0, 1, 0, 0],
        [-np.sin(yaw), 0, np.cos(yaw), 0],
        [0, 0, 0, 1]
    ])

    # Поворот вокруг оси X (pitch)
    R_pitch = np.array([
        [1, 0, 0, 0],
        [0, np.cos(pitch), -np.sin(pitch), 0],
        [0, np.sin(pitch), np.cos(pitch), 0],
        [0, 0, 0, 1]
    ])

    # Поворот вокруг оси Z (roll)
    R_roll = np.array([
        [np.cos(roll), -np.sin(roll), 0, 0],
        [np.sin(roll), np.cos(roll), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Общий поворот камеры
    Rc = R_roll @ R_pitch @ R_yaw

    # Матрица преобразования камеры C = Rc * Tc
    C = Rc @ Tc

    return C


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

vertices_cube3 = np.array([
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

faces_cube2 = np.array([
    [0, 1, 3, 2],
    [5, 4, 6, 7],
    [6, 2, 0, 4],
    [4, 0, 1, 5],
    [5, 7, 3, 1],
    [6, 2, 3, 7]
])

# Преобразования для кубов
T3 = translation_matrix(0, 3, 0)
v3, theta3 = [0, 0, 1], np.pi / 4
R3 = rotation_matrix(v3, theta3)
vertices_cube3 = T3 @ (R3 @ vertices_cube3)

# Создание матрицы камеры
camera_position = [5, 5, 5]  # Положение камеры
camera_rotation = [np.pi / 4, -np.pi / 6, 0]  # Углы поворота [yaw, pitch, roll]

C = create_camera_matrix(camera_position, camera_rotation)
print("Матрица преобразования камеры C:")
print(np.round(C, 3))

# Обратная матрица C^-1 (преобразование мира в систему координат камеры)
C_inv = np.linalg.inv(C)
print("\nОбратная матрица C^-1:")
print(np.round(C_inv, 3))

# Применение преобразования камеры ко всем объектам
vertices_cube_cam = C_inv @ vertices_cube
vertices_cube2_cam = C_inv @ vertices_cube2
vertices_cube3_cam = C_inv @ vertices_cube3

# СОХРАНЕНИЕ ТОЛЬКО ТРЕТЬЕЙ КАРТИНКИ
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')

# Отрисовка преобразованных объектов
draw_shape(ax, vertices_cube2_cam, faces_cube2, 'cyan')
draw_shape(ax, vertices_cube_cam, faces_cube, 'blue')
draw_shape(ax, vertices_cube3_cam, faces_cube, 'green')

# Настройки отображения
ax.set_box_aspect([1, 1, 1])
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.view_init(azim=0, elev=0)  # Стандартный вид после преобразования
ax.set_title('Сцена после преобразования камеры $C^{-1}$', fontsize=14)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.tight_layout()
plt.savefig("task7.jpg", dpi=300, bbox_inches='tight')
plt.show()

# Дополнительно: вывод информации о камере
print(f"\nПараметры камеры:")
print(f"Положение: {camera_position}")
print(f"Поворот (yaw, pitch, roll): {[f'{np.degrees(angle):.1f}°' for angle in camera_rotation]}")