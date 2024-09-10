import tkinter as Tk
import time
import random

class Auto_Reset_Text(Tk.Tk):
    def __init__(self):
         
        super().__init__()

        self.title("Auto Reset Text App")

        self.text_widget = Tk.Text(self, wrap='word', height=10, width=40)
        self.text_widget.pack(padx=10, pady=10)

        self.placeholder_text = "Start typing..."
        self.text_widget.insert('1.0', self.placeholder_text)
        self.text_widget.bind('<KeyPress>', self.on_keypress)

        self.reset_timer = None
        self.reset_delay = 5000  # 5000 milliseconds (5 seconds)

    def on_keypress(self, event):
        if self.text_widget.get('1.0', 'end-1c') == self.placeholder_text:
            self.text_widget.delete('1.0', 'end')

        if self.reset_timer:
            self.after_cancel(self.reset_timer)
        self.reset_timer = self.after(self.reset_delay, self.reset_text)

    def reset_text(self):
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', self.placeholder_text)

if __name__ == "__main__":
    app = Auto_Reset_Text()
    app.mainloop()
    