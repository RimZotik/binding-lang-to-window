[![License: Custom MIT](https://img.shields.io/badge/license-Custom%20MIT-orange.svg)](./LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/RimZotik/binding-lang-to-window?label=release)](https://github.com/RimZotik/binding-lang-to-window/releases)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
[![GitHub stars](https://img.shields.io/github/stars/RimZotik/binding-lang-to-window?style=social)](https://github.com/RimZotik/binding-lang-to-window/stargazers)

# 🧠 Binding keyboard layout to windows on Windows

> 🇷🇺 [Читать на русском](./README.ru.md)

## 📌 Project Description

This is a small Windows utility that implements the behavior of binding the keyboard layout to each window, similar to how it works on macOS.

When switching between windows, the program automatically saves and restores the last used keyboard layout for each specific window, making working with multilingual applications more comfortable.

---

## ⚙️ Installation

1. Go to the tab [Releases](https://github.com/RimZotik/RimZotikbinding-lang-to-window/releases) and download the latest build. `*.exe`.

2. Add the downloaded '.exe` file to the startup:
   - Press `Win + R', type `shell:startup` and press Enter.
   - Copy the shortcut of the `.exe' file to the folder that opens.

The program runs in the background and requires no interaction — just turn it on and forget it.

---

## 💡 How it works

- Every `0.2` seconds, the program checks the currently active window ('GetForegroundWindow').
- When the active window changes:
  - The current layout is saved (via 'GetKeyboardLayout') for the previous window.
  - If the layout has already been saved for the new window, it is restored using `SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, hkl)`.

The names of the layouts are taken from the `layouts' file.json`, which can be easily expanded.

### Technologies used:

- `pywin32' — interaction with Windows windows (WinAPI)
- `ctypes' — calling `GetKeyboardLayout' via WinAPI
- `PyInstaller' — packaging the project in `.exe`
- 'json' — storage and extension of supported languages

---

## 📁 Expansion `layouts.json`

The `layouts' file.json` contains a mapping of layout codes (HKL and `lang_id`) with readable language names.

Example:

```json
{
  "0x409": "English (United States)",
  "0x419": "Russian"
}
```

## 📜 License

The project is distributed under a custom MIT license that prohibits commercial use. It means:

- ✅ Allowed use for personal purposes
- ✅ Allowed to modify and distribute
- ❌ It is forbidden to use it in commercial products and projects
