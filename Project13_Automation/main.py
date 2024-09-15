import pyautogui
from PIL import ImageGrab, ImageOps
import time
import numpy as np

def jump():
    pyautogui.press('space')
    print("Jump!")

def capture_screen_box():
    box = (450, 650, 550, 720)
    image = ImageGrab.grab(box)
    gray_image = ImageOps.grayscale(image)
    return np.array(gray_image)

def capture_and_save_debug_image():
    box = (500, 700, 600, 720)
    image = ImageGrab.grab(box)
    image.save("debug_screenshot.png")

def detect_obstacle():
    screen_data = capture_screen_box()
    screen_sum = screen_data.sum()
    print(f"Screen data sum: {screen_sum}")

    obstacle_threshold_high = 1700000
    obstacle_threshold_low = 600000
    death_threshold = 250000

    if screen_sum < death_threshold:
        print("Game Over Detected!")
        return False

    if obstacle_threshold_low < screen_sum < obstacle_threshold_high:
        capture_and_save_debug_image()
        return True
    
    return False

if __name__ == "__main__":
    print("Starting in 3 seconds...")
    time.sleep(3)

    while True:
        if detect_obstacle():
            jump()
        time.sleep(0.1)
