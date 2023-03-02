import pyautogui
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
import os
import keyboard
WINDOW_UI = r".\window.ui"


class Pointer(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        uic.loadUi(WINDOW_UI, self)

        pointer_timer = QtCore.QTimer(self)
        pointer_timer.timeout.connect(self.update_coordinates)
        pointer_timer.timeout.connect(self.update_rgb)
        pointer_timer.start(100)

        self.point_watcher_timer = QtCore.QTimer(self)
        self.point_watcher_timer.timeout.connect(self.check_point_changed)

        self.shutdown_activated = False
        self.point_is_selected = False
        self.selected_point = None
        self.selected_rgb = None

        self.trigger_shutdown_btn.clicked.connect(self.toggle_watcher)
        self.setFixedSize(358,88)
        self.update_coordinates()
        self.update_rgb()

    def eventFilter(self, object, event):
        if object == self.view and event.type() == QtCore.QEvent.MouseButtonPress:
            print('mouse pressed inside view')
            return True
        return super().eventFilter(object, event)

    def update_coordinates(self):
        pos = pyautogui.position()
        self.x_spot_label.setText(str(pos[0]))
        self.y_spot_label.setText(str(pos[1]))

    def check_point_changed(self):
        img = pyautogui.screenshot()
        rgb = img.getpixel(self.selected_point)
        if rgb != self.selected_rgb:
            self.infolabel.setText("point changed")
            self.point_watcher_timer.stop()
            os.system("shutdown /s /t 10")

    def set_point_to_watch(self):
        pos = pyautogui.position()
        self.selected_point = pyautogui.Point(pos[0], pos[1] - 3)
        img = pyautogui.screenshot()
        self.selected_rgb = img.getpixel(self.selected_point)
        self.point_is_selected = True
        self.infolabel.setText(f"watching at {pos[0]},{pos[1] - 3}")
        self.point_watcher_timer.start(10000)

    def toggle_watcher(self):
        if self.shutdown_activated:
            self.point_watcher_timer.stop()
            self.point_is_selected = False
            self.selected_point = None
            self.infolabel.setText("")
            self.trigger_shutdown_btn.setText("auto shutdown")
            self.shutdown_activated = False
        else:
            self.shutdown_activated = True
            self.point_is_selected = False
            self.infolabel.setText("hover over point + ENTER")
            self.trigger_shutdown_btn.setText("Cancel")

    def update_rgb(self):
        position = pyautogui.position()
        rgb = pyautogui.pixel(position[0], position[1])
        self.rgb_value.setText(str(rgb))

        self.pallete.setStyleSheet(
            f"background-color: rgb{rgb}; border-radius: 10px;")

        if self.shutdown_activated and not self.point_is_selected:
            if keyboard.is_pressed("enter"):
                self.set_point_to_watch()

        if self.shutdown_activated and self.point_is_selected:
            if keyboard.is_pressed("Esc"):
                self.toggle_watcher()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Pointer()
    window.show()
    app.exec_()
