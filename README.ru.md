[![License: Custom MIT](https://img.shields.io/badge/license-Custom%20MIT-orange.svg)](./LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/RimZotik/binding-lang-to-window?label=release)](https://github.com/RimZotik/binding-lang-to-window/releases)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
[![GitHub stars](https://img.shields.io/github/stars/RimZotik/binding-lang-to-window?style=social)](https://github.com/RimZotik/binding-lang-to-window/stargazers)

# 🧠 Привязка раскладки клавиатуры к окнам на Windows

> 🇺🇸 [Read in English](./README.md)

## 📌 Описание проекта

Это небольшая утилита для Windows, реализующая поведение привязки раскладки клавиатуры к каждому окну — аналогично тому, как это работает на macOS.

При переключении между окнами программа автоматически сохраняет и восстанавливает последнюю использованную раскладку клавиатуры для каждого конкретного окна, делая работу с мультиязычными приложениями более комфортной.

---

## ⚙️ Установка

1. Перейдите на вкладку [Releases](https://github.com/RimZotik/binding-lang-to-window/releases) и скачайте последнюю сборку `*.exe`.

2. Добавьте скачанный `.exe` файл в автозагрузку:
   - Нажмите `Win + R`, введите `shell:startup` и нажмите Enter.
   - Скопируйте ярлык `.exe` файла в открывшуюся папку.

Программа запускается в фоне и не требует взаимодействия — просто включите и забудьте.

---

## 💡 Как работает

- Каждые `0.2` секунды программа проверяет текущее активное окно (`GetForegroundWindow`).
- Когда активное окно меняется:
  - Сохраняется текущая раскладка (через `GetKeyboardLayout`) для предыдущего окна.
  - Если для нового окна уже была сохранена раскладка, она восстанавливается с помощью `SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, hkl)`.

Названия раскладок берутся из файла `layouts.json`, который можно легко расширять.

### Используемые технологии:

- `pywin32` — взаимодействие с окнами Windows (WinAPI)
- `ctypes` — вызов `GetKeyboardLayout` через WinAPI
- `PyInstaller` — упаковка проекта в `.exe`
- `json` — хранение и расширение поддерживаемых языков

---

## 📁 Расширение `layouts.json`

Файл `layouts.json` содержит сопоставление кодов раскладок (HKL и `lang_id`) с читаемыми названиями языков.

Пример:

```json
{
  "0x409": "English (United States)",
  "0x419": "Russian"
}
```

## 📜 Лицензия

Проект распространяется под кастомной лицензией MIT, запрещающей коммерческое использование. Это означает:

- ✅ Разрешено использование в личных целях
- ✅ Разрешено модифицировать и распространять
- ❌ Запрещено использовать в коммерческих продуктах и проектах
