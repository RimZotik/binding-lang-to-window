import time
import win32gui

def get_activate_window():
	hwnd = win32gui.GetForegroundWindow()
	if hwnd != 0:
		return win32gui.GetWindowText(hwnd)
	return None

def main():
	last_window = None
	while True:
		current_window = get_activate_window()
		if current_window != last_window:
			print(current_window)
			last_window = current_window
		time.sleep(1)

if __name__ == "__main__":
	main()