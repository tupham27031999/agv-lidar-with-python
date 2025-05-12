import cv2
import numpy as np
import heapq
from scipy.ndimage import distance_transform_edt
#new

def creat_gird(image, x_min, y_min, point_start, point_end, grid_size=5, agv_size = 2):
    list_points = []

    h_input, w_input, _ = image.shape
    new_image = np.ones((h_input, w_input, 3), dtype=np.uint8) * 255  # Ảnh mới với giá trị pixel ban đầu là 0 (màu đen)
    grid = np.zeros((h_input // grid_size, w_input // grid_size), dtype=np.uint8)  # Mảng grid với giá trị ban đầu là 255 (màu trắng)
    h, w = grid.shape

    # Duyệt qua từng ô lưới trong ảnh gốc
    for i in range(0, w):
        for j in range(0, h):
            # Lấy ô lưới hiện tại
            grid_cell = image[int(j*grid_size):int(j*grid_size+grid_size), int(i*grid_size):int(i*grid_size+grid_size), :3]

            # Kiểm tra màu của các pixel trong ô lưới
            if np.any(np.all(grid_cell == [0, 0, 0], axis=-1)) or np.any(np.all(grid_cell == [255, 0, 255], axis=-1)):
                # Tô màu đen cho ô lưới trong ảnh mới
                new_image[int(j*grid_size):int(j*grid_size+grid_size), int(i*grid_size):int(i*grid_size+grid_size)] = [0, 0, 0]
                grid[j, i] = 1

    if len(point_start) > 0 and len(point_end) > 0:
        point_start[0] = int(point_start[0] - x_min)
        point_start[1] = int(point_start[1] - y_min)
        point_end[0] = int(point_end[0] - x_min)
        point_end[1] = int(point_end[1] - y_min)
        list_points = tim_duong_di(point_start, point_end, grid, grid_size, agv_size)
        cv2.circle(new_image, (int(point_start[0]), int(point_start[1])), 3, (255, 0, 0), -1)
        cv2.circle(new_image, (int(point_end[0]), int(point_end[1])), 3, (0, 0, 255), -1)
    # Vẽ đường đi lên ảnh
    list_points2 = []
    for i in range(0,len(list_points)):
        y, x = [list_points[i][0], list_points[i][1]]
        list_points2.append([x*grid_size+grid_size//2 + x_min, y*grid_size+grid_size//2 + y_min])
        if i != 0:
            y1, x1 = [list_points[i-1][0], list_points[i-1][1]]
            y2, x2 = [list_points[i][0], list_points[i][1]]
            cv2.line(new_image, (x1*grid_size+grid_size//2, y1*grid_size+grid_size//2), (x2*grid_size+grid_size//2, y2*grid_size+grid_size//2), (0, 0, 255), 2)

    return new_image, list_points2, grid

def reconstruct_path(came_from, current, start):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    
    # Chỉ giữ lại các vị trí rẽ
    if len(path) > 1:
        turns = [path[0]]
        current_direction = (path[1][0] - path[0][0], path[1][1] - path[0][1])
        for i in range(1, len(path) - 1):
            next_direction = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
            if next_direction != current_direction:
                turns.append(path[i])
                current_direction = next_direction
        turns.append(path[-1])
    else:
        turns = path
    
    return turns

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def distance_to_nearest_wall(node, grid):
    rows, cols = grid.shape
    min_distance = float('inf')
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 1:
                distance = abs(node[0] - i) + abs(node[1] - j)
                if distance < min_distance:
                    min_distance = distance
    return min_distance

def combined_heuristic(a, b, grid):
    return heuristic(a, b) - distance_to_nearest_wall(a, grid)

def get_neighbors_with_direction(node, rows, cols):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Chỉ bao gồm các hướng thẳng
    # directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]  # Chỉ bao gồm các hướng thẳng
    for dx, dy in directions:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < rows and 0 <= y < cols:
            neighbors.append(((x, y), (dx, dy)))
    return neighbors

def is_wall(node, grid, agv_radius):
    grid_check = grid[node[0]-agv_radius:node[0]+agv_radius, node[1]-agv_radius:node[1]+agv_radius]
    check = np.any(grid_check == 1)
    return check
# Hàm A* để tìm đường đi với ít đường rẽ nhất và ưu tiên đi giữa đường
def a_star_least_turns(start, goal, grid, agv_radius):
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (0, start, None))  # Thêm hướng di chuyển hiện tại
    came_from = {}
    g_score = {start: 0}
    f_score = {start: combined_heuristic(start, goal, grid)}

    while open_set:
        _, current, current_direction = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current, start)

        for neighbor, direction in get_neighbors_with_direction(current, rows, cols):
            if is_wall(neighbor, grid, agv_radius):
                continue
            tentative_g_score = g_score[current] + 0.1
            if current_direction and current_direction != direction:
                tentative_g_score += 20  # Thêm chi phí nhỏ cho mỗi lần rẽ

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + combined_heuristic(neighbor, goal, grid)
                heapq.heappush(open_set, (f_score[neighbor], neighbor, direction))

    return []
def tim_duong_di(start, end, grid, grid_size = 3, agv_radius = 2):
    # Sử dụng a_star_least_turns để tìm đường đi từ click[1] đến click[2]
    start2 = (start[1] // grid_size, start[0] // grid_size)
    goal = (end[1] // grid_size, end[0] // grid_size)
    path = a_star_least_turns(start2, goal, grid, agv_radius)

    return path
# def A_star(point_start, point_end, new_image, grid, grid_size=3):
