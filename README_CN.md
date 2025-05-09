# DeskTime 桌面悬浮时钟

[English Version](./README.md) | [中文版](./README_CN.md)

![GitHub stars](https://img.shields.io/github/stars/spcity/desktime?style=social)
![GitHub forks](https://img.shields.io/github/forks/spcity/desktime?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/spcity/desktime)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fspcity%2Fdesktime&countColor=%23263759&style=flat)](https://github.com/spcity/desktime)

> 🕒 一款美观、极简、可自定义的 Windows 桌面悬浮时钟工具

---

## ✨ 项目特点

- 🖥️ **始终置顶**：窗口始终悬浮在所有应用之上，自动避让任务栏
- 🎨 **自定义外观**：支持设置背景色、文字色、闪烁色、圆角、透明度
- 🕹️ **自由缩放**：窗口右下角可拖动调整大小
- 🖱️ **右键菜单**：一键全屏、退出全屏、设置透明度、颜色、显示秒/毫秒、退出等功能
- ⏰ **整点/半点闪烁提醒**：每到整点或半点自动闪烁提示
- 🪟 **智能避让任务栏**：自动避免被任务栏遮挡
- 🌙 **极简美观**：无边框、圆角、半透明，适合各种桌面风格

---

## 🚀 使用方法

### 1. 下载与运行

1. [点击下载最新版本 exe文件](https://github.com/spcity/desktime/releases/tag/v1)
2. 解压后双击 `desktime v1.exe` 即可运行（无需安装）

### 2. 自定义设置

- **右键点击时钟窗口**，弹出功能菜单：
  - `设置背景颜色`：自定义背景色
  - `设置闪烁颜色`：自定义整点/半点闪烁色
  - `设置透明度`：滑块实时调整窗口透明度
  - `显示秒`/`显示毫秒`：可选显示到秒或毫秒
  - `一键全屏/退出全屏`：全屏显示或恢复
  - `退出`：关闭程序

- **拖动窗口**：按住窗口任意位置拖动
- **缩放窗口**：拖动右下角三角形调整大小

### 3. 打包与自定义图标

如需自行打包或更换图标，请参考 [打包说明](#打包说明)。

---

## 🛠️ 打包说明

1. 安装依赖：
   ```sh
   pip install pyinstaller pyqt5
   ```
2. 准备 `clock.ico` 图标文件
3. 打包命令：
   ```sh
   pyinstaller --noconsole --onefile --icon=clock.ico timedesk\ v1.py
   ```
4. 生成的 exe 在 `dist/` 目录下

---

## 📷 截图

![screenshot](https://raw.githubusercontent.com/yourusername/desktime/main/screenshot.png)

---

## 📄 License

MIT License

---
