import requests
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

API_KEY = os.getenv('API_KEY')  # Replace with your Voice RSS API key

# Default save directory
DEFAULT_SAVE_DIR = os.path.expanduser("~/Downloads")  # Change this to your preferred directory

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF file: {e}")
    return text

def text_to_speech(text, save_path):
    """Converts text to speech and saves it as an audio file using Voice RSS API."""
    if len(text) > 10000:  # Assuming 10,000 characters to avoid reaching the API limit
        messagebox.showerror("Error", "Text is too long for conversion. Please provide a smaller file.")
        return

    url = "https://api.voicerss.org/"
    params = {
        'key': API_KEY,
        'src': text,
        'hl': 'en-us',
        'v': 'Linda',
        'c': 'mp3',
        'f': '44khz_16bit_stereo'
    }

    try:
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            with open(save_path, "wb") as audio_file:
                audio_file.write(response.content)
            messagebox.showinfo("Success", f"Audio saved successfully at {save_path}.")
        else:
            messagebox.showerror("Error", f"API Error: {response.status_code}\n{response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network Error: {e}")

def upload_pdf_and_convert():
    """Handles PDF upload and conversion process."""
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")], title="Select a PDF file")
    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            messagebox.showerror("Error", "No text found in the selected PDF file.")
            return
        
        # Automatically generate save path in default directory
        filename = os.path.splitext(os.path.basename(pdf_path))[0] + "_converted.mp3"
        save_path = os.path.join(DEFAULT_SAVE_DIR, filename)
        
        text_to_speech(text, save_path)

def test_text_to_speech():
    """Test the text-to-speech function with sample text."""
    sample_text = "Hello, this is a test of the text-to-speech functionality."
    save_path = os.path.join(DEFAULT_SAVE_DIR, "test_output.mp3")
    text_to_speech(sample_text, save_path)

def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    root.title("PDF to Speech Converter")

    # Create and place GUI components
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    title_label = ttk.Label(frame, text="Upload PDF and Convert to Speech", font=("Arial", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    upload_button = ttk.Button(frame, text="Upload PDF and Convert", command=upload_pdf_and_convert)
    upload_button.grid(row=1, column=0, pady=10, padx=5)

    test_button = ttk.Button(frame, text="Test Text-to-Speech", command=test_text_to_speech)
    test_button.grid(row=1, column=1, pady=10, padx=5)

    exit_button = ttk.Button(frame, text="Exit", command=root.quit)
    exit_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
