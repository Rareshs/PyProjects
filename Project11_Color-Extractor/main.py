import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        num_colors = simpledialog.askinteger("Input", "How many colors do you want to extract?", minvalue=1, maxvalue=20)
        if num_colors:
            try:
                display_image(file_path)
                extract_colors(file_path, num_colors)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

def display_image(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

def extract_colors(image_path, num_colors):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_
    dominant_colors = np.array(centers, dtype='uint8')

    # Normalize the colors to the range [0, 1]
    normalized_colors = dominant_colors / 255.0

    # Convert RGB colors to hexadecimal for annotations
    hex_colors = ['#%02x%02x%02x' % tuple(color) for color in dominant_colors]

    # Create a figure
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    
    # Plot the normalized colors
    plt.imshow([normalized_colors], aspect='auto')
    
    # Annotate each color with its hex value
    for i, color in enumerate(normalized_colors[0]):
        plt.text(i, 0, hex_colors[i], ha='center', va='center', color='white', fontsize=12, weight='bold', backgroundcolor=hex_colors[i])
    
    plt.show()

root = tk.Tk()
root.title("Color Extractor App")

button = tk.Button(root, text="Upload Image", command=open_image)
button.pack(pady=20)

label = tk.Label(root)
label.pack()

root.mainloop()
