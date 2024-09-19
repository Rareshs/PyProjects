from tkinter import Tk, Canvas,Label
import random
import time

# Global configurations
colors = ['green', 'purple', 'blue', 'gray', 'yellow', 'brown']
canvas_height = 500
canvas_width = 500
player_width = 50
player_height = 30
bullet_speed = 10
alien_speed = 5
bullets = []
aliens = []
last_shot_time = 0
bullet_cooldown = 500  # Cooldown in milliseconds
direction = 1  # 1 for right, -1 for left
score=0

root = Tk()
root.title("Space Invaders Game")
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()
score_label = Label(root, text=f"Score: {score}", font=("Helvetica", 16), fg="white", bg="black")
score_label.pack()

def make_player():
    global player
    x1 = (canvas_width - player_width) / 2
    y1 = canvas_height - player_height - 20
    x2 = x1 + player_width
    y2 = y1 + player_height
    player = canvas.create_rectangle(x1, y1, x2, y2, fill='red')

def create_aliens():
    alien_width = 40
    alien_height = 20
    space_between_aliens = 20
    num_aliens = 8
    rows = 3
    space_between_rows = 30

    starting_x = (canvas_width - (num_aliens * alien_width) - (num_aliens - 1) * space_between_aliens) / 2
    
    for row in range(rows):
        for i in range(num_aliens):
            x1 = starting_x + i * (alien_width + space_between_aliens)
            y1 = 50 + row * (alien_height + space_between_rows)
            x2 = x1 + alien_width
            y2 = y1 + alien_height
            alien = canvas.create_rectangle(x1, y1, x2, y2, fill=random.choice(colors))
            aliens.append(alien)

def move_bullet(bullet):
    if bullet in bullets:
        bullet_pos = canvas.coords(bullet)
        if bullet_pos[1] <= 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
        else:
            canvas.move(bullet, 0, -bullet_speed)
            root.after(50, lambda: move_bullet(bullet))

def bullet_collision():
    global score
    for bullet in bullets:
        bullet_pos = canvas.coords(bullet)
        for alien in aliens:
            alien_pos = canvas.coords(alien)
            if (bullet_pos[0] < alien_pos[2] and bullet_pos[2] > alien_pos[0] and
                bullet_pos[1] < alien_pos[3] and bullet_pos[3] > alien_pos[1]):
                canvas.delete(bullet)
                canvas.delete(alien)
                bullets.remove(bullet)
                aliens.remove(alien)
                score+=1
                score_label.config(text=f"Score: {score}")
                break
    root.after(50, bullet_collision)

def move_aliens():
    global direction, alien_speed
    move_x = direction * alien_speed
    move_down = False

    for alien in aliens:
        x1, y1, x2, y2 = canvas.coords(alien)
        if x1 + move_x > canvas_width or x2 + move_x < 0:
            direction *= -1
            move_down = True
            break

    for alien in aliens:
        x1, y1, x2, y2 = canvas.coords(alien)
        if move_down:
            canvas.move(alien, move_x, alien_speed)
        else:
            canvas.move(alien, move_x, 0)

    root.after(100, move_aliens)

make_player()
create_aliens()
bullet_collision()
move_aliens()

def move_left(event):
    current_pos = canvas.coords(player)
    if current_pos[0] > 0:
        canvas.move(player, -25, 0)

def move_right(event):
    current_pos = canvas.coords(player)
    if current_pos[2] < canvas_width:
        canvas.move(player, 25, 0)

def fire_bullet(event):
    global last_shot_time
    current_time = time.time() * 1000  # Get current time in milliseconds
    if current_time - last_shot_time >= bullet_cooldown:
        player_pos = canvas.coords(player)
        bullet_x1 = (player_pos[0] + player_pos[2]) / 2 - 2
        bullet_y1 = player_pos[1] - 10
        bullet_x2 = bullet_x1 + 4
        bullet_y2 = bullet_y1 - 10
        bullet = canvas.create_rectangle(bullet_x1, bullet_y1, bullet_x2, bullet_y2, fill='white')
        bullets.append(bullet)
        move_bullet(bullet)
        last_shot_time = current_time

root.bind('<Left>', move_left)
root.bind('<Right>', move_right)
root.bind('<space>', fire_bullet)

root.mainloop()
