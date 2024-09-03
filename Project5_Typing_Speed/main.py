import tkinter as tk
import time
import random

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Typing speed tests help you improve your typing skills.",
            "Python is a popular programming language for beginners and professionals.",
            "Practice typing every day to increase speed and accuracy.",
            "Artificial intelligence is changing the world rapidly."
        ]

        self.sample_text = random.choice(self.sample_texts)
        
        self.sample_label = tk.Label(root, text=self.sample_text, font=("Arial", 14))
        self.sample_label.pack(pady=10)

        self.text_area = tk.Text(root, height=5, width=50, font=("Arial", 14), wrap='word', bd=2, relief='groove')
        self.text_area.pack(pady=10)
        self.text_area.bind("<KeyPress>", self.start_typing)
        
        self.submit_button = tk.Button(root, text="Submit", command=self.calculate_speed)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.start_time = 0
        self.is_typing = False

    def start_typing(self, event):
        if not self.is_typing:
            self.start_time = time.time()
            self.is_typing = True

    def calculate_speed(self):
        end_time = time.time()
        time_taken = end_time - self.start_time

        typed_text = self.text_area.get("1.0", tk.END).strip()

        words = len(typed_text.split())
        time_taken_minutes = time_taken / 60
        wpm = words / time_taken_minutes if time_taken_minutes > 0 else 0

        correct_words = sum(1 for i, j in zip(typed_text.split(), self.sample_text.split()) if i == j)
        total_words = len(self.sample_text.split())
        accuracy = (correct_words / total_words) * 100

        self.result_label.config(text=f"Speed: {wpm:.2f} WPM | Accuracy: {accuracy:.2f}%")

        self.is_typing = False
        self.start_time = 0
        self.text_area.delete("1.0", tk.END)

        self.update_sample_text()

    def update_sample_text(self):
        self.sample_text = random.choice(self.sample_texts)
        self.sample_label.config(text=self.sample_text)

root = tk.Tk()
app = TypingSpeedApp(root)
root.mainloop()
