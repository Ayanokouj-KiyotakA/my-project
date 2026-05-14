import random

GOAL = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

START = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

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

def dfs(start, goal):

    node = start

    if node == goal:
        return [node]

    frontier = [(node, [node])]   # Stack
    explored = []

    while frontier:

        # DFS dùng pop() để lấy node cuối cùng
        node, path = frontier.pop()

        explored.append(node)

        for child in get_neighbors(node):

            if child not in explored:

                if child == goal:
                    return path + [child]

                frontier.append((child, path + [child]))

    return None

print("START:")
for row in START:
    print(row)

print()

solution = dfs(START, GOAL)

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