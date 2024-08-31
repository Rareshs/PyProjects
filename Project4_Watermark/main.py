from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

root = Tk()
root.title("Watermark Application")

original_image = None
watermarked_image = None

def upload_image():
    global original_image, watermarked_image
    
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:
        original_image = Image.open(file_path)
        original_image.thumbnail((300, 300))
        img = ImageTk.PhotoImage(original_image)
        image_label.config(image=img)
        image_label.image = img
        watermarked_image = original_image.copy()

def add_watermark():
    global original_image, watermarked_image
    
    if original_image:
        watermarked_image = original_image.copy()
        draw = ImageDraw.Draw(watermarked_image)
        text = "Watermark"
        font = ImageFont.truetype("arial.ttf", 20)
        bbox = draw.textbbox((0, 0), text, font=font)
        textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]
        width, height = watermarked_image.size
        x = width - textwidth - 10
        y = height - textheight - 10
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))
        img = ImageTk.PhotoImage(watermarked_image)
        image_label.config(image=img)
        image_label.image = img

def download_image():
    global watermarked_image
    
    if watermarked_image:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            watermarked_image.save(file_path)

label = Label(root, text="Upload an image to add the Watermark")
image_label = Label(root)

download_image_button = Button(root, text="Download image", command=download_image)
open_image_button = Button(root, text="Upload image", command=upload_image)
watermark_button = Button(root, text="Add Watermark", command=add_watermark)

label.grid(row=0, column=0, columnspan=2, pady=10)
image_label.grid(row=1, column=0, columnspan=2, pady=2)
open_image_button.grid(row=2, column=0, padx=2, pady=2)
watermark_button.grid(row=2, column=1, padx=2, pady=2)
download_image_button.grid(row=3, column=0, columnspan=2, pady=2)

root.mainloop()