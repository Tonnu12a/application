import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()
    
        self.show_start_menu()

    def show_start_menu(self):
        self.clear_frame()

        tk.Label(self.frame, text="Are you ready?").pack(pady=10)

        tk.Button(self.frame, text="Yes", command=lambda: self.start_game()).pack(pady=5)

    def start_game(self):
        self.clear_frame()

        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.snake_blocks = []
        self.food = None
        self.score = 0

        self.direction = "Down"
        self.running = True

        self.root.bind("<KeyPress>", self.change_direction)

        self.create_snake()
        self.create_food()
        self.run_game()
        

    def create_snake(self):
        for x, y in self.snake:
            block = self.canvas.create_rectangle(x, y, x+10, y+10, fill="green")
            self.snake_blocks.append(block)

    def create_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        self.food = self.canvas.create_rectangle(x, y, x+10, y+10, fill="red")

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def move_snake(self):
        head_x, head_y = self.snake[-1]

        if self.direction == "Up":
            new_head = (head_x, head_y - 10)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 10)
        elif self.direction == "Left":
            new_head = (head_x - 10, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 10, head_y)

        self.snake.append(new_head)
        block = self.canvas.create_rectangle(new_head[0], new_head[1], new_head[0]+10, new_head[1]+10, fill="green")
        self.snake_blocks.append(block)

        if not self.check_food_collision():
            tail = self.snake.pop(0)
            tail_block = self.snake_blocks.pop(0)
            self.canvas.delete(tail_block)
        else:
            self.canvas.delete(self.food)
            self.create_food()
            self.score += 10
            self.update_score()

    def check_food_collision(self):
        head_x, head_y = self.snake[-1]
        food_coords = self.canvas.coords(self.food)
        return head_x == food_coords[0] and head_y == food_coords[1]

    def check_collisions(self):
        head_x, head_y = self.snake[-1]
        if not (0 <= head_x < 400 and 0 <= head_y < 400):
            self.running = False
            return

        if len(self.snake) != len(set(self.snake)):
            self.running = False

    def run_game(self):
        if self.running:
            self.move_snake()
            self.check_collisions()
            self.root.after(100, self.run_game)
        else:
            self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Arial", 24))
            response = messagebox.askyesno("Game Over", f"Score: {self.score}\nDo you want to play again?")
            if response:
                self.reset_game()
            else:
                self.root.quit()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def reset_game(self):
        self.canvas.delete("all")  # キャンバスをクリア
        self.snake_blocks = []  # スネークブロックのリストをリセット
        self.snake = [(20, 20), (20, 30), (20, 40)]  # スネークを初期位置にリセット
        self.score = 0
        self.update_score()  # リセットした得点を表示する
        self.create_snake()  # 新しいスネークを作成
        self.create_food()  # 新しい食べ物を作成
        self.direction = "Down"
        self.running = True
        self.run_game()
                       

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
