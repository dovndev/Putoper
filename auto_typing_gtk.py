#!/usr/bin/env python3
import sys
import time
import threading
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

try:
    from x11_input import X11Keyboard
except ImportError:
    print("Error: x11_input module not found or failed to load libraries.")
    sys.exit(1)

class AutoTyperWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Auto Typer (Native)")
        self.set_border_width(10)
        self.set_default_size(500, 600)
        
        # System theme handling is automatic with GTK
        
        # Main Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        
        # Header
        header = Gtk.Label()
        header.set_markup("<span size='xx-large' weight='bold'>Auto Typer</span>")
        main_box.pack_start(header, False, False, 10)
        
        instructions = Gtk.Label(label="Enter text below, set delay, and click Start.")
        main_box.pack_start(instructions, False, False, 0)
        
        # Text Input
        frame = Gtk.Frame(label="Text to Type")
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_min_content_height(200)
        
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled_window.add(self.text_view)
        frame.add(scrolled_window)
        main_box.pack_start(frame, True, True, 5)
        
        # Settings Box
        settings_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        main_box.pack_start(settings_box, False, False, 10)
        
        # Delay
        delay_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        delay_label = Gtk.Label(label="Delay (s):")
        self.delay_entry = Gtk.Entry()
        self.delay_entry.set_text("3")
        self.delay_entry.set_width_chars(5)
        delay_box.pack_start(delay_label, False, False, 0)
        delay_box.pack_start(self.delay_entry, False, False, 0)
        settings_box.pack_start(delay_box, False, False, 0)
        
        # Speed
        speed_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        speed_label = Gtk.Label(label="Speed:")
        self.speed_combo = Gtk.ComboBoxText()
        self.speed_combo.append_text("Slow")
        self.speed_combo.append_text("Normal")
        self.speed_combo.append_text("Fast")
        self.speed_combo.append_text("Instant")
        self.speed_combo.set_active(1) # Normal
        speed_box.pack_start(speed_label, False, False, 0)
        speed_box.pack_start(self.speed_combo, False, False, 0)
        settings_box.pack_start(speed_box, False, False, 0)
        
        # Loop
        self.loop_check = Gtk.CheckButton(label="Loop")
        settings_box.pack_start(self.loop_check, False, False, 0)
        
        # Controls
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        main_box.pack_start(controls_box, False, False, 10)
        
        self.start_btn = Gtk.Button(label="Start Typing")
        self.start_btn.connect("clicked", self.on_start_clicked)
        self.start_btn.get_style_context().add_class("suggested-action")
        controls_box.pack_start(self.start_btn, True, True, 0)
        
        self.stop_btn = Gtk.Button(label="Stop")
        self.stop_btn.connect("clicked", self.on_stop_clicked)
        self.stop_btn.get_style_context().add_class("destructive-action")
        self.stop_btn.set_sensitive(False)
        controls_box.pack_start(self.stop_btn, True, True, 0)
        
        # Status
        self.status_label = Gtk.Label(label="Ready")
        main_box.pack_start(self.status_label, False, False, 5)
        
        # Internal state
        self.keyboard = X11Keyboard()
        self.typing_thread = None
        self.stop_event = threading.Event()
        self.is_typing = False

    def on_start_clicked(self, widget):
        buffer = self.text_view.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        
        if not text:
            self.status_label.set_text("Error: No text to type")
            return
            
        try:
            delay = float(self.delay_entry.get_text())
        except ValueError:
            delay = 3.0
            
        speed_str = self.speed_combo.get_active_text()
        speed_map = {
            "Slow": 0.1,
            "Normal": 0.02,
            "Fast": 0.005,
            "Instant": 0.0
        }
        interval = speed_map.get(speed_str, 0.02)
        loop = self.loop_check.get_active()
        
        self.stop_event.clear()
        self.is_typing = True
        self.update_ui_state(typing=True)
        
        self.typing_thread = threading.Thread(
            target=self.run_typing,
            args=(text, delay, interval, loop),
            daemon=True
        )
        self.typing_thread.start()

    def on_stop_clicked(self, widget):
        self.stop_event.set()

    def update_ui_state(self, typing):
        self.start_btn.set_sensitive(not typing)
        self.stop_btn.set_sensitive(typing)
        self.text_view.set_editable(not typing)
        
    def run_typing(self, text, delay, interval, loop):
        # Countdown
        for i in range(int(delay), 0, -1):
            if self.stop_event.is_set():
                GLib.idle_add(self.typing_finished, "Stopped")
                return
            GLib.idle_add(self.status_label.set_text, f"Starting in {i}...")
            time.sleep(1)
            
        GLib.idle_add(self.status_label.set_text, "Typing...")
        
        # Typing loop
        while True:
            if self.stop_event.is_set():
                break
                
            self.keyboard.type_string(text, interval, self.stop_event)
            
            if not loop or self.stop_event.is_set():
                break
                
            time.sleep(1) # Pause between loops
            
        GLib.idle_add(self.typing_finished, "Done" if not self.stop_event.is_set() else "Stopped")

    def typing_finished(self, status):
        self.is_typing = False
        self.update_ui_state(typing=False)
        self.status_label.set_text(status)

if __name__ == "__main__":
    win = AutoTyperWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
