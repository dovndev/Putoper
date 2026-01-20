
import ctypes
import ctypes.util
import time
import threading

# Load X11 libraries
try:
    x11_lib = ctypes.util.find_library('X11')
    xtst_lib = ctypes.util.find_library('Xtst')
    
    if not x11_lib or not xtst_lib:
        raise OSError("Could not find X11 or Xtst libraries")

    libX11 = ctypes.CDLL(x11_lib)
    libXtst = ctypes.CDLL(xtst_lib)
except Exception as e:
    print(f"Error loading X11 libraries: {e}")
    libX11 = None
    libXtst = None

# Define X11 types
Display = ctypes.c_void_p
KeySym = ctypes.c_ulong
KeyCode = ctypes.c_ubyte

# Define essential X11 function signatures
if libX11 and libXtst:
    libX11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    libX11.XOpenDisplay.restype = Display
    
    libX11.XCloseDisplay.argtypes = [Display]
    
    libX11.XStringToKeysym.argtypes = [ctypes.c_char_p]
    libX11.XStringToKeysym.restype = KeySym
    
    libX11.XKeysymToKeycode.argtypes = [Display, KeySym]
    libX11.XKeysymToKeycode.restype = KeyCode
    
    libX11.XFlush.argtypes = [Display]
    
    libXtst.XTestFakeKeyEvent.argtypes = [Display, KeyCode, ctypes.c_int, ctypes.c_ulong]
    libXtst.XTestFakeKeyEvent.restype = ctypes.c_int

class X11Keyboard:
    def __init__(self):
        if not libX11:
            raise RuntimeError("X11 libraries not available")
        
        self.display = libX11.XOpenDisplay(None)
        if not self.display:
            raise RuntimeError("Could not open X Display")
            
        self.lock = threading.Lock()

    def __del__(self):
        if self.display:
            libX11.XCloseDisplay(self.display)

    def _get_keycode(self, char):
        # Handle some special characters manually if needed, 
        # but XStringToKeysym handles most standard ASCII
        
        # Mapping for special keys if needed (simplified)
        key_map = {
            '\n': 'Return',
            '\t': 'Tab',
            ' ': 'space',
        }
        
        keysym_str = key_map.get(char, char)
        
        # For single characters that are not in the map, we need to be careful.
        # XStringToKeysym works well for single characters.
        # But we need to handle shifted characters (e.g., 'A' vs 'a', '!' vs '1') manually
        # implies sending Shift down/up. This basic implementation focuses on direct mapping.
        # NOTE: A robust implementation requires handling modifiers (Shift).
        
        # Quick hack: standard XKeysymToKeycode might give the keycode for the key locally.
        # If 'A' is passed, XStringToKeysym returns XK_A.
        
        c_str = keysym_str.encode('utf-8')
        keysym = libX11.XStringToKeysym(c_str)
        
        if keysym == 0:
            return None, False
            
        keycode = libX11.XKeysymToKeycode(self.display, keysym)
        
        # Check if we need shift.
        # This is a simplification. A real impl needs to query the keymap.
        # For now, we assume if it's an uppercase char or special symbols, we might need shift?
        # Actually, let's try a simpler approach: XTestFakeKeyEvent sends the keycode.
        # If we send the keycode for 'a', it types 'a'. If Shift is held, it types 'A'.
        # We need to manually toggle shift for uppercase.
        
        needs_shift = char.isupper() or char in '!@#$%^&*()_+{}|:"<>?~'
        
        return keycode, needs_shift

    def press_key(self, keycode):
        libXtst.XTestFakeKeyEvent(self.display, keycode, True, 0)
        libX11.XFlush(self.display)

    def release_key(self, keycode):
        libXtst.XTestFakeKeyEvent(self.display, keycode, False, 0)
        libX11.XFlush(self.display)
        
    def type_char(self, char):
        with self.lock:
            keycode, needs_shift = self._get_keycode(char)
            
            if not keycode:
                # Fallback for chars X11 doesn't recognize easily without more logic
                return
            
            # Get Shift keycode (usually 50 or 62 but simpler to look it up)
            shift_sym = libX11.XStringToKeysym(b"Shift_L")
            shift_code = libX11.XKeysymToKeycode(self.display, shift_sym)
            
            if needs_shift:
                self.press_key(shift_code)
                
            self.press_key(keycode)
            self.release_key(keycode)
            
            if needs_shift:
                self.release_key(shift_code)

    def type_string(self, text, interval=0.01, stop_event=None):
        for char in text:
            if stop_event and stop_event.is_set():
                break
            self.type_char(char)
            time.sleep(interval)

