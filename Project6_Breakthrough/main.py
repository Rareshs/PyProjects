from tkinter import Tk, Canvas, Label, Button, messagebox

colors = ["red", "green", "yellow", "blue", "purple", "brown"]

paddle_width = 100
paddle_height = 20
canvas_width = 500
canvas_height = 500

brick_width = 60
brick_height = 20
brick_spacing = 5
rows = 4
columns = canvas_width // (brick_width + brick_spacing)

vx = 3
vy = 3
score = 0

root = Tk()
root.title("Breakthrough Game")
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

score_label = Label(root, text=f"Score: {score}", fg="white", bg="black")
score_label.pack()

restart_button = Button(root, text="Restart", command=lambda: restart_game())
restart_button.pack()

def create_paddle():
    global player
    x1 = (canvas_width - paddle_width) / 2
    y1 = canvas_height - paddle_height - 20
    x2 = x1 + paddle_width
    y2 = y1 + paddle_height
    player = canvas.create_rectangle(x1, y1, x2, y2, fill="red")

def create_ball():
    global ball, vx, vy
    radius = 10
    x1 = (canvas_width / 2) - radius
    y1 = (canvas_height / 2) - radius
    x2 = (canvas_width / 2) + radius
    y2 = (canvas_height / 2) + radius
    ball = canvas.create_oval(x1, y1, x2, y2, fill="red")
    move_ball()

def move_ball():
    global vx, vy, score
    canvas.move(ball, vx, vy)
    ball_coords = canvas.coords(ball)
    x1, y1, x2, y2 = ball_coords

    if y2 >= canvas_height:
        game_over()

    if y1 <= 0 or y2 >= canvas_height:
        vy = -vy
    if x1 <= 0 or x2 >= canvas_width:
        vx = -vx

    paddle_coords = canvas.coords(player)
    paddle_x1, paddle_y1, paddle_x2, paddle_y2 = paddle_coords
    if x1 < paddle_x2 and x2 > paddle_x1 and y2 > paddle_y1 and y1 < paddle_y2:
        vy = -vy

    brick_collision()

    root.after(20, move_ball)

def brick_collision():
    global vy, score
    ball_coords = canvas.coords(ball)
    x1, y1, x2, y2 = ball_coords
    for brick in bricks:
        brick_coords = canvas.coords(brick)
        bx1, by1, bx2, by2 = brick_coords
        if x1 < bx2 and x2 > bx1 and y2 > by1 and y1 < by2:
            canvas.delete(brick)
            bricks.remove(brick)
            vy = -vy
            score += 10
            score_label.config(text=f"Score: {score}")
            break

def move_left(event):
    current_pos = canvas.coords(player)
    if current_pos[0] > 0:
        canvas.move(player, -20, 0)

def move_right(event):
    current_pos = canvas.coords(player)
    if current_pos[2] < canvas_width:
        canvas.move(player, 20, 0)

def create_bricks():
    global bricks
    total_brick_width = (brick_width + brick_spacing) * columns - brick_spacing
    start_x = (canvas_width - total_brick_width) / 2
    bricks = []
    for row in range(rows):
        for col in range(columns):
            x1 = start_x + col * (brick_width + brick_spacing)
            y1 = row * (brick_height + brick_spacing)
            x2 = x1 + brick_width
            y2 = y1 + brick_height
            color = colors[row % len(colors)]
            brick = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            bricks.append(brick)

def restart_game():
    global score, vx, vy, bricks
    canvas.delete("all")
    score = 0
    vx = 3
    vy = 3
    score_label.config(text=f"Score: {score}")
    create_bricks()
    create_paddle()
    create_ball()

def game_over():
    canvas.delete("all")
    score_label.config(text=f"Game Over! Final Score: {score}")
    messagebox.showinfo("Game Over", f"Game Over! Your final score is {score}")

create_bricks()
create_paddle()
create_ball()

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.mainloop()
