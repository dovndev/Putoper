import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import threading

def start_typing():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please paste some text first!")
        return

    messagebox.showinfo("Ready", "Switch to the window where you want to type.\nTyping will start in 3 seconds...")
    
    # Run typing in a background thread so UI doesn’t freeze
    threading.Thread(target=type_text, args=(text,), daemon=True).start()

def type_text(text):
    time.sleep(3)  # 3 second delay before typing
    pyautogui.typewrite(text, interval=0.02)  # Adjust typing speed if needed

# GUI setup
root = tk.Tk()
root.title("Auto Typer")
root.geometry("400x300")
root.resizable(False, False)

label = tk.Label(root, text="Paste your text below:", font=("Segoe UI", 11))
label.pack(pady=10)

text_box = tk.Text(root, wrap="word", height=10, width=45)
text_box.pack(padx=10, pady=5)

start_button = tk.Button(root, text="Start Typing", command=start_typing, font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white")
start_button.pack(pady=15)

root.mainloop()
