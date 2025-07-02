import time
import win32gui

def get_activate_window():
	hwnd = win32gui.GetForegroundWindow()
	if hwnd != 0:
		return win32gui.GetWindowText(hwnd)
	return None

def main():
	while True:
		current_window = get_activate_window()
		if current_window != None:
			print(current_window)
		time.sleep(1)

if __name__ == "__main__":
	main()