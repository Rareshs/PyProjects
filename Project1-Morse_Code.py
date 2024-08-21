from tkinter import Tk
from tkinter import *

# Define the Morse Code Dictionary
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---',
                    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---',
                    'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--',
                    'Z':'--..', '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....', '7':'--...', 
                    '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', 
                    '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

# Function to translate text to morse code
def text_to_morse():
    text = text_var.get().upper()
    morse_code = ' '.join([MORSE_CODE_DICT.get(char, '') for char in text])
    result_var.set(morse_code)

# Function to translate morse code to text
def morse_to_text():
    morse = text_var.get().split(' ')
    text = ''.join([list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(code)] if code in MORSE_CODE_DICT.values() else '' for code in morse])
    result_var.set(text)


root = Tk()
root.title("Morse Code Translator")
root.geometry("400x200")


text_var = StringVar()
result_var = StringVar()


Label(root, text="Enter Text or Morse Code:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=text_var).grid(row=0, column=1, padx=10, pady=10)

Button(root, text="To Morse Code", command=text_to_morse).grid(row=1, column=0, padx=10, pady=10)
Button(root, text="To Text", command=morse_to_text).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Result:").grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=result_var, state='readonly').grid(row=2, column=1, padx=10, pady=10)

# Run the main event loop
root.mainloop()
