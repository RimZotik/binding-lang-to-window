import win32gui
import win32api
import ctypes
import win32process
import sys
import os
import json
import time

def load_layouts():
    """Load layouts.json, works both from source and from PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle: layouts.The json is in the exe folder.
        base_path = sys._MEIPASS
    else:
        # Starting from source
        base_path = os.path.abspath(".")

    path = os.path.join(base_path, "layouts.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

layouts = load_layouts()

window_langs = {}

def get_activate_window():
    """
    @return: tuple (hwnd: int, window_title: str) or (None, None)
    
    Get the handle (HWND) of the currently active (foreground) window,
    and its window title text.
    Uses win32gui.GetForegroundWindow() to retrieve the HWND of the active window,
    then win32gui.GetWindowText() to get the window's title string.
    Returns (None, None) if no active window found.
    """
    hwnd = win32gui.GetForegroundWindow()
    if hwnd != 0:
        return hwnd, win32gui.GetWindowText(hwnd)
    return None, None

def get_current_keyboard_layout(hwnd):
    """
    @param hwnd: int
        Handle to a window.
    @return: tuple (layout: int, lang_id: int)
        Retrieves the current keyboard layout (HKL) for the thread
        that created the specified window.
        
    Calls win32process.GetWindowThreadProcessId(hwnd) to get the thread ID owning the window.
    Calls Windows API GetKeyboardLayout(thread_id) via ctypes to get HKL.
    lang_id extracts lower 16 bits (language ID) from HKL.
    """
    thread_id = win32process.GetWindowThreadProcessId(hwnd)[0]
    layout = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    lang_id = layout & 0xFFFF
    return layout, lang_id

def switch_keyboard_layout(hwnd, hkl):
    """
    @param hwnd: int
        Handle to the target window whose keyboard layout should be changed.
    @param hkl: int
        The input locale identifier (HKL) to set as the new keyboard layout.
        
    Sends the Windows message WM_INPUTLANGCHANGEREQUEST (0x0050) to the specified window,
    requesting it to change its input language to the provided HKL.
    Uses win32api.SendMessage for inter-window messaging.
    """
    WM_INPUTLANGCHANGEREQUEST = 0x0050
    win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, hkl)

def main():
    """
    Main loop that:
    - Monitors the currently active window in a loop.
    - Detects when the active window changes.
    - Saves the keyboard layout of the window that lost focus.
    - Restores the saved keyboard layout for the newly active window, if known.
    - Prints informative messages about saving/restoring layouts.
    - Gracefully exits on KeyboardInterrupt (Ctrl+C).
    """
    last_window = None
    try:
        while True:
            hwnd, window_title = get_activate_window()
            if hwnd and window_title != last_window:
                # When leaving the previous window, save its current keyboard layout
                if last_window is not None:
                    prev_hwnd = win32gui.GetForegroundWindow()
                    prev_layout, prev_lang_id = get_current_keyboard_layout(prev_hwnd)
                    window_langs[last_window] = prev_layout
                    prev_layout_hex = hex(prev_lang_id)
                    prev_layout_name = layouts.get(prev_layout_hex, f"Unknown ({prev_layout_hex})")
                    print(f"[+] Saved layout {prev_layout_name} for window '{last_window}'")

                # Restore the saved keyboard layout for the new active window if available
                if window_title in window_langs:
                    saved_layout = window_langs[window_title]
                    switch_keyboard_layout(hwnd, saved_layout)
                    print(f"[+] Restored layout for window '{window_title}'")
                else:
                    # If it's a new window, save its current layout
                    layout_full, lang_id = get_current_keyboard_layout(hwnd)
                    window_langs[window_title] = layout_full
                    layout_hex = hex(lang_id)
                    layout_name = layouts.get(layout_hex, f"Unknown ({layout_hex})")
                    print(f"[+] Saved layout {layout_name} for new window '{window_title}'")

                last_window = window_title

            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n[+] Program terminated by user.")

if __name__ == "__main__":
    main()
