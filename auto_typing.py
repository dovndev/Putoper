#!/usr/bin/env python3
"""
Auto Typer - Modern Text Automation Tool
A cross-platform application for automated text typing.
"""

import customtkinter as ctk
import pyautogui
import time
import platform
try:
    import keyboard
except Exception:
    keyboard = None
import platform
try:
    import pyperclip
except Exception:
    pyperclip = None
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
        
        # Exact-preserve paste option (per-line clipboard paste)
        self.paste_var = ctk.BooleanVar(value=False)
        self.paste_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Prefer clipboard-per-line paste (exact)",
            variable=self.paste_var
        )
        self.paste_checkbox.pack(side="left", padx=10, pady=10)
        
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
        # Continue button (used to resume after Alt-pause)
        self.continue_button = ctk.CTkButton(
            buttons_frame,
            text="Continue",
            command=self.resume_typing,
            height=40,
            fg_color="#1f6feb"
        )
        self.continue_button.pack(side="left", padx=10, pady=10)
        self.continue_button.configure(state="disabled")

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
        self.paused = False

        # If keyboard module available, register Alt listener in background
        if keyboard is not None:
            try:
                threading.Thread(target=self._register_alt_listener, daemon=True).start()
            except Exception:
                pass

    def _register_alt_listener(self):
        """Register global Alt key handler (non-blocking)"""
        try:
            # on_press_key will call our handler when Alt is pressed
            keyboard.on_press_key('alt', lambda e: self._on_alt_pressed())
        except Exception as e:
            print(f"Alt listener registration failed: {e}")

    def _on_alt_pressed(self):
        """Called when Alt is pressed — pause typing and show UI"""
        # Only act if currently typing
        if not self.typing_active:
            return
        # Set paused and update UI from main thread
        def pause_ui():
            self.paused = True
            self.status_label.configure(text="Paused (Alt pressed)", text_color="orange")
            # Show window so user can click Continue
            try:
                self.deiconify()
                self.continue_button.configure(state="normal")
            except Exception:
                pass
        try:
            self.after(0, pause_ui)
        except Exception:
            pause_ui()
        
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
        self.paused = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Stopped", text_color="red")
        self.deiconify()
        try:
            self.continue_button.configure(state="disabled")
        except Exception:
            pass
        
    def start_typing(self):
        """Main typing function"""
        try:
            # Get settings
            try:
                delay = float(self.delay_input.get())
            except ValueError:
                delay = 3
                
            # Preserve the exact input (do not strip) so indentation and leading/trailing
            # whitespace are kept when typing.
            text = self.text_input.get("1.0", "end-1c")
            if text is None or text == "":
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
            # We'll type line-by-line, sending leading whitespace explicitly then the rest
            # character-by-character. This reduces editor auto-formatting side-effects
            # and preserves characters like '<' and '>' as entered.
            while self.typing_active:
                # If paused (Alt pressed), wait until resume
                while self.paused and self.typing_active:
                    time.sleep(0.05)

                lines = text.splitlines(keepends=True)
                # If text ends with no newline and splitlines returned empty, handle that
                if not lines and text:
                    lines = [text]

                # Use per-line clipboard paste if requested and pyperclip is available
                use_clipboard = bool(self.paste_var.get()) and (pyperclip is not None)

                for line in lines:
                    if not self.typing_active:
                        break

                    # Detect if this line had a newline at the end
                    has_newline = line.endswith('\n') or line.endswith('\r')
                    # Remove trailing newline characters for typing the content
                    content = line.rstrip('\r\n')

                    # Extract leading whitespace (spaces and tabs) and remaining text
                    leading_len = len(content) - len(content.lstrip(' \t'))
                    leading_ws = content[:leading_len]
                    remainder = content[leading_len:]
                    if use_clipboard:
                        # Try to paste the exact content of the line via clipboard
                        try:
                            pyperclip.copy(content)
                            time.sleep(0.04)
                            if platform.system() == 'Darwin':
                                pyautogui.hotkey('command', 'v')
                            else:
                                pyautogui.hotkey('ctrl', 'v')
                            if has_newline:
                                pyautogui.press('enter')
                        except Exception as e:
                            # Fallback to typed approach for this line
                            if leading_ws:
                                pyautogui.write(leading_ws, interval=0)
                            for ch in remainder:
                                if not self.typing_active:
                                    break
                                pyautogui.write(ch, interval=interval)
                            if has_newline:
                                pyautogui.press('enter')
                    else:
                        # Type leading whitespace with zero interval to avoid triggering
                        # some editor auto-indent heuristics that react to characters
                        if leading_ws:
                            pyautogui.write(leading_ws, interval=0)

                        # Type the rest character-by-character using configured interval
                        for ch in remainder:
                            if not self.typing_active:
                                break
                            pyautogui.write(ch, interval=interval)

                        # Reproduce newline if present
                        if has_newline:
                            pyautogui.press('enter')

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

    def resume_typing(self):
        """Resume typing after a 3 second delay (called from Continue button)"""
        if not self.paused:
            return
        # Disable Continue button and hide window, wait 3 seconds then resume
        try:
            self.continue_button.configure(state="disabled")
        except Exception:
            pass

        def do_resume():
            # count down
            for i in range(3, 0, -1):
                self.status_label.configure(text=f"Resuming in {i}...", text_color="orange")
                time.sleep(1)
            # clear paused flag and update UI
            self.paused = False
            self.status_label.configure(text="Typing...", text_color="green")
            try:
                self.withdraw()
            except Exception:
                pass

        threading.Thread(target=do_resume, daemon=True).start()

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
