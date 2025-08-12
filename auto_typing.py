import customtkinter as ctk
import pyautogui
import time
import threading

class AutoTyperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Auto Typer")
        self.geometry("500x500")
        ctk.set_appearance_mode("System")  # "Light" or "Dark" or "System"
        ctk.set_default_color_theme("blue")  # Can be "green", "dark-blue", etc.

        # Label
        self.label = ctk.CTkLabel(self, text="Enter text to type:", font=("Arial", 16))
        self.label.pack(pady=(20, 10))

        # Textbox
        self.text_input = ctk.CTkTextbox(self, height=200, width=450)
        self.text_input.pack(padx=10, pady=5, fill="both", expand=True)

        # Delay input
        self.delay_label = ctk.CTkLabel(self, text="Delay before typing (seconds):")
        self.delay_label.pack(pady=(15, 5))
        self.delay_input = ctk.CTkEntry(self)
        self.delay_input.insert(0, "3")
        self.delay_input.pack(pady=(0, 10))

        # Loop mode checkbox
        self.loop_var = ctk.BooleanVar()
        self.loop_checkbox = ctk.CTkCheckBox(self, text="Enable Loop Mode", variable=self.loop_var)
        self.loop_checkbox.pack(pady=(0, 20))

        # Start button
        self.start_button = ctk.CTkButton(self, text="Start Typing", command=self.start_typing_thread)
        self.start_button.pack(pady=10)

        # Exit button
        self.exit_button = ctk.CTkButton(self, text="Exit", fg_color="red", command=self.destroy)
        self.exit_button.pack(pady=5)

    def start_typing_thread(self):
        threading.Thread(target=self.start_typing, daemon=True).start()

    def start_typing(self):
        try:
            delay = float(self.delay_input.get())
        except ValueError:
            delay = 3  # default fallback

        text = self.text_input.get("1.0", "end-1c")
        loop_mode = self.loop_var.get()

        self.withdraw()  # Hide the window
        time.sleep(delay)

        while True:
            for line in text.split("\n"):
                pyautogui.write(line, interval=0.02)  # preserves indentation
                pyautogui.press("enter")

            if not loop_mode:
                break
            time.sleep(1)  # small pause between loops

        self.deiconify()  # Show window again

if __name__ == "__main__":
    app = AutoTyperApp()
    app.mainloop()
