import random

# Trạng thái đích
GOAL = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

# Trạng thái ban đầu
START = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]

# Tìm vị trí số 0
def find_zero(state):

    for i in range(3):
        for j in range(3):

            if state[i][j] == 0:
                return i, j

# Sinh các trạng thái mới
def get_neighbors(state):

    x, y = find_zero(state)

    directions = [
        (-1, 0),  # lên
        (1, 0),   # xuống
        (0, -1),  # trái
        (0, 1)    # phải
    ]

    neighbors = []

    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:

            new_state = [row.copy() for row in state]

            new_state[x][y], new_state[nx][ny] = \
            new_state[nx][ny], new_state[x][y]

            neighbors.append(new_state)

    return neighbors

# BFS giống logic trên bảng
def bfs(start, goal):

    node = start

    if node == goal:
        return [node]

    frontier = [(node, [node])]
    explored = []

    while frontier:

        node, path = frontier.pop(0)

        explored.append(node)

        for child in get_neighbors(node):

            if child not in explored:

                if child == goal:
                    return path + [child]

                frontier.append((child, path + [child]))

    return None

# In trạng thái ban đầu
print("START:")
for row in START:
    print(row)

print()

# Chạy BFS
solution = bfs(START, GOAL)

# In kết quả
if solution:

    print("Đã tìm thấy!")
    print("Số bước:", len(solution) - 1)
    print()

    for step in solution:

        for row in step:
            print(row)

        print()

else:
    print("Không tìm thấy!")