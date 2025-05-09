# DeskTime - Floating Desktop Clock

[English Version](./README.md) | [中文版](./README_CN.md)

![GitHub stars](https://img.shields.io/github/stars/spcity/desktime?style=social)
![GitHub forks](https://img.shields.io/github/forks/spcity/desktime?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/spcity/desktime)

[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fspcity%2Fdesktime&countColor=%23263759&style=flat)](https://github.com/spcity/desktime)

> 🕒 A beautiful, minimalist, and customizable floating clock for Windows desktop

---

## ✨ Features

- 🖥️ **Always on Top**: The clock always stays above all windows, and automatically avoids the taskbar
- 🎨 **Customizable Appearance**: Set background color, text color, blink color, corner radius, and transparency
- 🕹️ **Resizable**: Drag the bottom-right corner to resize the window
- 🖱️ **Right-Click Menu**: One-click fullscreen, exit fullscreen, set transparency, colors, show seconds/milliseconds, and exit
- ⏰ **Blink Reminder**: Blinks automatically at every hour and half-hour
- 🪟 **Taskbar Avoidance**: Automatically avoids being covered by the Windows taskbar
- 🌙 **Minimal & Elegant**: Frameless, rounded corners, semi-transparent, fits any desktop style

---

## 🚀 Usage

### 1. Download & Run

1. [Download the latest release](https://github.com/spcity/desktime/releases/tag/v1)
2. Unzip and double-click `desktime v1.exe` to run (no installation required)

### 2. Customization

- **Right-click the clock window** to open the menu:
  - `Set Background Color`: Customize background color
  - `Set Blink Color`: Customize the color for hour/half-hour blink
  - `Set Transparency`: Adjust window transparency with a slider
  - `Show Seconds`/`Show Milliseconds`: Optionally display seconds or milliseconds
  - `Fullscreen/Exit Fullscreen`: Toggle fullscreen mode
  - `Exit`: Close the program

- **Drag the window**: Move by dragging anywhere
- **Resize**: Drag the bottom-right triangle to resize

### 3. Packaging & Custom Icon

To package yourself or change the icon, see [Packaging Guide](#packaging-guide).

---

## 🛠️ Packaging Guide

1. Install dependencies:
   ```sh
   pip install pyinstaller pyqt5
   ```
2. Prepare a `clock.ico` icon file
3. Packaging command:
   ```sh
   pyinstaller --noconsole --onefile --icon=clock.ico timedesk\ v1.py
   ```
4. The exe will be in the `dist/` folder

---

## 📷 Screenshot

<video src="desktime show.mp4" controls width="600"></video>

![screenshot](https://raw.githubusercontent.com/yourusername/desktime/main/screenshot.png)

---

## 📄 License

MIT License

---

