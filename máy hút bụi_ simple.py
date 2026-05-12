import random
import tkinter as tk
from tkinter import messagebox

ROWS = 4
COLS = 4


def random_matrix():
    return [[random.randint(0, 1) for _ in range(COLS)] for _ in range(ROWS)]


def count_dirty(matrix):
    return sum(row.count(1) for row in matrix)


def possible_moves(row, col):
    moves = []

    if row > 0:
        moves.append("U")
    if row < ROWS - 1:
        moves.append("D")
    if col > 0:
        moves.append("L")
    if col < COLS - 1:
        moves.append("R")

    return moves


def move(action, row, col):
    if action == "U":
        row -= 1
    elif action == "D":
        row += 1
    elif action == "L":
        col -= 1
    elif action == "R":
        col += 1

    return row, col


class VacuumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máy hút bụi AI")

        self.matrix = random_matrix()
        self.x = 0
        self.y = 0
        self.running = False
        self.cells = []

        self.build_ui()
        self.update_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        self.grid_frame = tk.Frame(frame)
        self.grid_frame.grid(row=0, column=0, columnspan=4, pady=(0, 12))

        for i in range(ROWS):
            row_cells = []
            for j in range(COLS):
                label = tk.Label(
                    self.grid_frame,
                    text="",
                    width=6,
                    height=3,
                    relief="ridge",
                    borderwidth=2,
                    font=("Arial", 14, "bold")
                )
                label.grid(row=i, column=j, padx=2, pady=2)
                row_cells.append(label)
            self.cells.append(row_cells)

        self.status_label = tk.Label(frame, text="", font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=4, sticky="w")

        self.clean_label = tk.Label(frame, text="", font=("Arial", 12))
        self.clean_label.grid(row=2, column=0, columnspan=4, sticky="w")

        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=(10, 0))

        tk.Button(button_frame, text="Randomize", command=self.reset_matrix, width=10).grid(row=0, column=0, padx=4)
        tk.Button(button_frame, text="Step", command=self.step, width=10).grid(row=0, column=1, padx=4)
        tk.Button(button_frame, text="Run", command=self.run_auto, width=10).grid(row=0, column=2, padx=4)
        tk.Button(button_frame, text="Stop", command=self.stop_auto, width=10).grid(row=0, column=3, padx=4)

    def update_ui(self):
        dirty_count = count_dirty(self.matrix)

        self.status_label.config(
            text=f"Vị trí hiện tại: ({self.x}, {self.y}) | Bụi còn lại: {dirty_count}"
        )

        if not self.running:
            self.clean_label.config(
                text="Sử dụng Step để xử lý từng bước hoặc Run để chạy tự động."
            )

        for i in range(ROWS):
            for j in range(COLS):
                cell = self.cells[i][j]
                state = self.matrix[i][j]

                if i == self.x and j == self.y:
                    bg = "#4da6ff"
                    fg = "white"
                    text = "R"
                elif state == 1:
                    bg = "#d47a45"
                    fg = "white"
                    text = "1"
                else:
                    bg = "#f0f0f0"
                    fg = "black"
                    text = "0"

                cell.config(text=text, bg=bg, fg=fg)

    def reset_matrix(self):
        self.running = False
        self.matrix = random_matrix()
        self.x = 0
        self.y = 0
        self.update_ui()

    def step(self):
        if count_dirty(self.matrix) == 0:
            messagebox.showinfo("Hoàn thành", "Đã hút sạch toàn bộ bụi!")
            return

        if self.matrix[self.x][self.y] == 1:
            self.matrix[self.x][self.y] = 0
        else:
            moves = possible_moves(self.x, self.y)
            action = random.choice(moves)
            self.x, self.y = move(action, self.x, self.y)

        self.update_ui()

    def run_auto(self):
        if self.running:
            return

        self.running = True
        self.clean_label.config(text="Đang chạy tự động...")
        self.auto_step()

    def auto_step(self):
        if not self.running:
            return

        if count_dirty(self.matrix) == 0:
            self.running = False
            self.clean_label.config(text="Hoàn thành! Bụi đã được hút sạch.")
            messagebox.showinfo("Hoàn thành", "Đã hút sạch toàn bộ bụi!")
            return

        self.step()
        self.root.after(400, self.auto_step)

    def stop_auto(self):
        self.running = False
        self.clean_label.config(text="Đã dừng. Bạn có thể tiếp tục với Step hoặc Run.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumApp(root)
    root.mainloop()