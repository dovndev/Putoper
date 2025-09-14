#!/usr/bin/env python3
"""
Auto Typer - Modern Text Automation Tool
A cross-platform application for automated text typing.
"""

import customtkinter as ctk
import pyautogui
import time
import threading
import sys
import os

# Configure PyAutoGUI
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01

class AutoTyperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Auto Typer")
        self.geometry("500x600")
        self.resizable(True, True)
        
        # Set theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Create GUI
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Auto Typer", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Instructions
        instructions = ctk.CTkLabel(
            main_frame,
            text="Enter text below and it will be typed automatically after the delay.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        instructions.pack(pady=(0, 20))
        
        # Text input section
        text_label = ctk.CTkLabel(main_frame, text="Text to type:", font=ctk.CTkFont(size=14, weight="bold"))
        text_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.text_input = ctk.CTkTextbox(main_frame, height=200, font=ctk.CTkFont(size=11))
        self.text_input.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Settings frame
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Delay setting
        delay_frame = ctk.CTkFrame(settings_frame)
        delay_frame.pack(fill="x", padx=15, pady=15)
        
        delay_label = ctk.CTkLabel(delay_frame, text="Delay before typing (seconds):")
        delay_label.pack(side="left", padx=(10, 5))
        
        self.delay_input = ctk.CTkEntry(delay_frame, width=80)
        self.delay_input.pack(side="right", padx=(5, 10))
        self.delay_input.insert(0, "3")
        
        # Options frame
        options_frame = ctk.CTkFrame(settings_frame)
        options_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.loop_var = ctk.BooleanVar()
        self.loop_checkbox = ctk.CTkCheckBox(
            options_frame, 
            text="Loop mode (repeat continuously)", 
            variable=self.loop_var
        )
        self.loop_checkbox.pack(side="left", padx=10, pady=10)
        
        # Typing speed
        speed_label = ctk.CTkLabel(options_frame, text="Speed:")
        speed_label.pack(side="right", padx=(10, 5))
        
        self.speed_var = ctk.StringVar(value="Normal")
        self.speed_option = ctk.CTkOptionMenu(
            options_frame,
            variable=self.speed_var,
            values=["Slow", "Normal", "Fast", "Instant"]
        )
        self.speed_option.pack(side="right", padx=(5, 10))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.start_button = ctk.CTkButton(
            buttons_frame,
            text="Start Typing",
            command=self.start_typing_thread,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_button.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text="Stop",
            command=self.stop_typing,
            height=40,
            fg_color="red",
            hover_color="darkred"
        )
        self.stop_button.pack(side="right", padx=10, pady=10)
        self.stop_button.configure(state="disabled")
        
        # Status
        self.status_label = ctk.CTkLabel(main_frame, text="Ready", text_color="green")
        self.status_label.pack(pady=(0, 10))
        
        # Initialize state
        self.typing_active = False
        
    def get_speed_interval(self):
        """Get typing interval based on speed setting"""
        speed_map = {
            "Slow": 0.1,
            "Normal": 0.02,
            "Fast": 0.005,
            "Instant": 0
        }
        return speed_map.get(self.speed_var.get(), 0.02)
        
    def start_typing_thread(self):
        """Start typing in a separate thread"""
        if not self.typing_active:
            self.typing_active = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            threading.Thread(target=self.start_typing, daemon=True).start()
            
    def stop_typing(self):
        """Stop the typing process"""
        self.typing_active = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Stopped", text_color="red")
        self.deiconify()
        
    def start_typing(self):
        """Main typing function"""
        try:
            # Get settings
            try:
                delay = float(self.delay_input.get())
            except ValueError:
                delay = 3
                
            text = self.text_input.get("1.0", "end-1c").strip()
            if not text:
                self.status_label.configure(text="No text to type!", text_color="red")
                self.stop_typing()
                return
                
            loop_mode = self.loop_var.get()
            interval = self.get_speed_interval()
            
            # Hide window and countdown
            self.withdraw()
            for i in range(int(delay), 0, -1):
                if not self.typing_active:
                    return
                time.sleep(1)
                
            # Start typing
            while self.typing_active:
                for char in text:
                    if not self.typing_active:
                        break
                    pyautogui.write(char, interval=interval)
                    
                if not loop_mode:
                    break
                    
                # Small pause between loops
                time.sleep(1)
                
        except Exception as e:
            print(f"Error during typing: {e}")
        finally:
            # Reset UI
            if self.typing_active:
                self.stop_typing()
            else:
                self.deiconify()

def main():
    """Main application entry point"""
    # Handle high DPI displays
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    # Create and run app
    app = AutoTyperApp()
    app.mainloop()

if __name__ == "__main__":
    main()
