import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QMenu, QAction, 
                             QColorDialog, QFontDialog, QInputDialog, QSlider, QDialog, QVBoxLayout, QPushButton, QDesktopWidget)
from PyQt5.QtCore import Qt, QTimer, QPoint, QTime, QDate, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QIcon
import ctypes
import ctypes.wintypes

class FloatingClock(QWidget):
    def __init__(self):
        super().__init__()
        self.is_fullscreen = False  # 必须最先定义，防止resizeEvent提前触发
        self.clock_font = QFont("Arial", 24)  # 必须提前定义，防止resizeEvent提前触发
        self.default_font_size = 24
        self.fullscreen_font_size = 48  # 全屏时固定大字体
        self.clock_color = QColor(255, 255, 255)
        self.bg_color = QColor(30, 30, 30, 180)
        self.blink_color = QColor(255, 0, 0)  # 默认闪烁颜色为红色
        self._original_bg_color = self.bg_color  # 用于闪烁时恢复
        self.resizing = False
        self.resize_margin = 10  # 右下角缩放区域大小
        self.opacity = 3.0  # 当前透明度
        self.time_label = QLabel(self)  # 必须提前定义，防止resizeEvent提前触发
        self.clock_radius = 10  # 必须提前定义，防止paintEvent提前触发
        self.time_label.setAlignment(Qt.AlignCenter)  # 保证居中
        
        # 窗口设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.show()  # 应用置顶
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(150, 60)
        
        # 初始化变量
        self.drag_pos = QPoint()
        self.blink_count = 0
        self.is_blinking = False
        self.last_triggered = -1  # 记录上次触发时间
        self.show_seconds = False  # 是否显示秒
        self.show_milliseconds = False  # 是否显示毫秒
        
        self.update_style()
        
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        
        # 初始时间显示
        self.update_time()
        
        # 设置上下文菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        self.resize(320, 120)  # 启动时设置更大的初始窗口大小
        self.set_always_on_top()  # 强制最顶层
    
    def update_style(self):
        # 更新时钟样式
        self.time_label.setFont(self.clock_font)
        self.time_label.setStyleSheet(f"color: {self.clock_color.name()};")
        self.time_label.resize(self.size())
        self.time_label.setAlignment(Qt.AlignCenter)  # 保证每次样式更新都居中
        self.update()
    
    def update_time(self):
        current_time = QTime.currentTime()
        if self.show_milliseconds:
            time_text = current_time.toString("hh:mm:ss:zzz")
        elif self.show_seconds:
            time_text = current_time.toString("hh:mm:ss")
        else:
            time_text = current_time.toString("hh:mm")
        self.time_label.setText(time_text)
        # 检查是否为整点或半点
        minutes = current_time.minute()
        seconds = current_time.second()
        # 只在整点或半点时触发一次闪烁
        if (minutes == 0 or minutes == 30) and seconds == 0 and self.last_triggered != minutes:
            self.last_triggered = minutes
            self.start_blink()
    
    def start_blink(self):
        self.is_blinking = True
        self.blink_count = 0
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.do_blink)
        self.blink_timer.start(500)  # 每500毫秒闪烁一次
    
    def do_blink(self):
        if self.blink_count < 6:  # 闪烁3次（显示/隐藏各算一次）
            if self.blink_count % 2 == 0:
                self.setWindowOpacity(1.0)
                self.bg_color = self.blink_color  # 闪烁时切换为闪烁颜色
            else:
                self.setWindowOpacity(1.0)
                self.bg_color = self._original_bg_color  # 恢复原背景色
            self.update()
            self.blink_count += 1
        else:
            self.blink_timer.stop()
            self.setWindowOpacity(1.0)
            self.bg_color = self._original_bg_color
            self.update()
            self.is_blinking = False
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆角背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.bg_color))
        painter.drawRoundedRect(self.rect(), self.clock_radius, self.clock_radius)
        
        # 绘制右下角缩放三角
        margin = self.resize_margin
        w, h = self.width(), self.height()
        points = [QPoint(w - margin, h), QPoint(w, h - margin), QPoint(w, h)]
        painter.setBrush(QBrush(QColor(180, 180, 180, 180)))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(*points)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_in_resize_area(event.pos()):
                self.resizing = True
                self.resize_start_pos = event.globalPos()
                self.resize_start_size = self.size()
                event.accept()
            else:
                self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'resizing') and self.resizing:
            diff = event.globalPos() - self.resize_start_pos
            new_width = max(100, self.resize_start_size.width() + diff.x())
            new_height = max(40, self.resize_start_size.height() + diff.y())
            self.resize(new_width, new_height)
            self.update_style()
            self.time_label.setAlignment(Qt.AlignCenter)  # 保证每次resize都居中
            event.accept()
        elif event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
        else:
            if self.is_in_resize_area(event.pos()):
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def mouseReleaseEvent(self, event):
        if hasattr(self, 'resizing') and self.resizing:
            self.resizing = False
            event.accept()
    
    def is_in_resize_area(self, pos):
        return pos.x() >= self.width() - self.resize_margin and pos.y() >= self.height() - self.resize_margin
    
    def resizeEvent(self, event):
        # 字体大小逻辑调整
        if self.is_fullscreen:
            self.clock_font.setPointSize(self.fullscreen_font_size)
        else:
            self.clock_font.setPointSize(self.default_font_size)
        self.update_style()
        self.time_label.setAlignment(Qt.AlignCenter)  # 保证每次resize都居中
        self.set_always_on_top()
        super().resizeEvent(event)
    
    def show_context_menu(self, pos):
        menu = QMenu(self)
        # 美化右键菜单
        menu.setStyleSheet("""
            QMenu {
                background-color: #23272e;
                color: #fff;
                border-radius: 10px;
                font-size: 18px;
                min-width: 180px;
                padding: 8px 0;
            }
            QMenu::item {
                padding: 10px 28px 10px 28px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: #4e9cff;
                color: #fff;
            }
            QMenu::separator {
                height: 1px;
                background: #444;
                margin: 4px 0;
            }
        """)
        bg_color_action = menu.addAction("设置背景颜色")
        blink_color_action = menu.addAction("设置闪烁颜色")
        opacity_action = menu.addAction("设置透明度")
        show_seconds_action = menu.addAction("显示秒")
        show_seconds_action.setCheckable(True)
        show_seconds_action.setChecked(self.show_seconds)
        show_milliseconds_action = menu.addAction("显示毫秒")
        show_milliseconds_action.setCheckable(True)
        show_milliseconds_action.setChecked(self.show_milliseconds)
        fullscreen_action = None
        exit_fullscreen_action = None
        if not self.is_fullscreen:
            fullscreen_action = menu.addAction("一键全屏")
        else:
            exit_fullscreen_action = menu.addAction("退出全屏")
        exit_action = menu.addAction("退出")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == bg_color_action:
            color = QColorDialog.getColor(self.bg_color, self, "选择背景颜色")
            if color.isValid():
                self.bg_color = color
                self._original_bg_color = color
                self.update()
        elif action == blink_color_action:
            color = QColorDialog.getColor(self.blink_color, self, "选择闪烁颜色")
            if color.isValid():
                self.blink_color = color
        elif action == opacity_action:
            self.set_opacity_dialog()
        elif action == show_seconds_action:
            self.show_seconds = not self.show_seconds
            if self.show_seconds:
                self.show_milliseconds = False
            self.update_time()
        elif action == show_milliseconds_action:
            self.show_milliseconds = not self.show_milliseconds
            if self.show_milliseconds:
                self.show_seconds = False
            self.update_time()
        elif fullscreen_action and action == fullscreen_action:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.showFullScreen()
            self.is_fullscreen = True
            self.clock_font.setPointSize(self.fullscreen_font_size)
            self.update_style()
            self.show()  # 应用置顶
            self.set_always_on_top()
        elif exit_fullscreen_action and action == exit_fullscreen_action:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.showNormal()
            self.is_fullscreen = False
            self.clock_font.setPointSize(self.default_font_size)
            self.update_style()
            self.show()  # 应用置顶
            self.set_always_on_top()
        elif action == exit_action:
            self.close()
            QApplication.quit()
    
    def set_opacity_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置透明度")
        dialog.setFixedWidth(380)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(22)
        label = QLabel(f"当前透明度: {int(self.windowOpacity()*100)}%", dialog)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 22px; font-weight: bold;")
        slider = QSlider(Qt.Horizontal, dialog)
        slider.setMinimum(30)
        slider.setMaximum(100)
        slider.setValue(int(self.windowOpacity()*100))
        slider.setTickInterval(1)
        slider.setStyleSheet("QSlider { min-height: 32px; } QSlider::handle:horizontal { width: 32px; height: 32px; }")
        layout.addWidget(label)
        layout.addWidget(slider)
        btn = QPushButton("确定", dialog)
        btn.setStyleSheet("font-size: 20px; min-height: 36px; border-radius: 8px;")
        layout.addWidget(btn)
        def on_value_change(val):
            self.setWindowOpacity(val/100)
            label.setText(f"当前透明度: {val}%")
        slider.valueChanged.connect(on_value_change)
        btn.clicked.connect(dialog.accept)
        dialog.exec_()

    def set_always_on_top(self):
        # 仅在Windows下有效
        try:
            hwnd = int(self.winId())
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_SHOWWINDOW = 0x0040
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        except Exception as e:
            pass

    def showEvent(self, event):
        super().showEvent(event)
        self.set_always_on_top()

    def moveEvent(self, event):
        super().moveEvent(event)
        self.set_always_on_top()
        self.avoid_taskbar()

    def avoid_taskbar(self):
        # 获取可用屏幕区域（不含任务栏）
        screen = self.screen() if hasattr(self, 'screen') else QApplication.primaryScreen()
        available_rect = screen.availableGeometry() if screen else QDesktopWidget().availableGeometry(self)
        geo = self.geometry()
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()
        # 如果窗口底部超出可用区域，则上移
        if y + h > available_rect.bottom():
            y = available_rect.bottom() - h
            if y < available_rect.top():
                y = available_rect.top()
            self.move(x, y)
        # 如果窗口右侧超出可用区域，也左移
        if x + w > available_rect.right():
            x = available_rect.right() - w
            if x < available_rect.left():
                x = available_rect.left()
            self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("clock.ico"))  # 这行确保任务栏图标
    clock = FloatingClock()
    clock.show()
    sys.exit(app.exec_())