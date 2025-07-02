import time
import win32gui
import win32process
import ctypes
import json

with open("layouts.json", "r", encoding="utf-8") as f:
	layouts = json.load(f)

def get_activate_window():
	hwnd = win32gui.GetForegroundWindow()
	if hwnd != 0:
		return hwnd, win32gui.GetWindowText(hwnd)
	return None

def get_current_keyboard_layout(hwnd):
    thread_id = win32process.GetWindowThreadProcessId(hwnd)[0]
    layout = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    lang_id = layout & 0xFFFF
    return hex(lang_id)

def main():
	last_window = None
	while True:
		hwnd, window_title = get_activate_window()
		if hwnd and window_title != last_window:
			layout = get_current_keyboard_layout(hwnd)
			layout_name = layouts.get(layout, f"Unknown ({layout})")
			print(f"[+] Window: {window_title} | Layout: {layout_name}")
			last_window = window_title
		time.sleep(1)

if __name__ == "__main__":
	main()