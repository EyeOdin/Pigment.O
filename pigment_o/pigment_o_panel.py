from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
import threading
from .pigment_o_constants import Constants
from .pigment_o_style import Style

# Color Space Factors
constant1 = Constants().Krita()
factorAAA = constant1[0]
factorRGB = constant1[1]
factorHUE = constant1[2]
factorSVL = constant1[3]
factorCMYK = constant1[4]
# Variables
scale_factor = 2

class PanelHsv(QWidget):
    SIGNAL_HSV_NEW = QtCore.pyqtSignal(list)
    SIGNAL_RELEASE = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(PanelHsv, self).__init__(parent)
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        # Module Style
        self.style = Style()

        # Variables
        self.hex = '#000000'
        # LMB SVG Cursors
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # MMB SVG Cursors
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 12
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.alpha = self.style.Alpha()
        self.cursor_lmb.setStyleSheet(self.alpha)
        self.cursor_rmb.setStyleSheet(self.alpha)

        # Thread Creation
        self.thread_size_hint = threading.Thread(target=self.sizeHint, daemon=True)
        self.thread_mouse_press_event = threading.Thread(target=self.mousePressEvent, daemon=True)
        self.thread_mouse_move_event = threading.Thread(target=self.mouseMoveEvent, daemon=True)
        self.thread_mouse_double_click_event = threading.Thread(target=self.mouseDoubleClickEvent, daemon=True)
        self.thread_mouse_release_event = threading.Thread(target=self.mouseReleaseEvent, daemon=True)
        self.thread_tablet_event = threading.Thread(target=self.tabletEvent, daemon=True)
        self.thread_mouse_cursor = threading.Thread(target=self.mouseCursor, daemon=True)
        self.thread_tablet_cursor = threading.Thread(target=self.tabletCursor, daemon=True)
        self.thread_update_panel = threading.Thread(target=self.Update_Panel, daemon=True)
        # Thread Start
        self.thread_size_hint.start()
        self.thread_mouse_press_event.start()
        self.thread_mouse_move_event.start()
        self.thread_mouse_double_click_event.start()
        self.thread_mouse_release_event.start()
        self.thread_tablet_event.start()
        self.thread_mouse_cursor.start()
        self.thread_tablet_cursor.start()
        self.thread_update_panel.start()

        # Update
        self.update()

    def sizeHint(self):
        return QtCore.QSize(16777215, 16777215)

    def mousePressEvent(self, event):
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)
        self.SIGNAL_RELEASE.emit("Release")

    def tabletEvent(self, event):
        self.tabletCursor(event)

    def mouseCursor(self, event):
        # Mouse Position
        event_x = event.x()
        event_y = event.y()
        # Make Object Move XY
        if (event_x >= 0 and event_x <= self.panel_width):
            self.value_x = event_x
        elif event_x < 0:
            self.value_x = 0
        elif event_x > self.panel_width:
            self.value_x = self.panel_width
        if  (event_y >= 0 and event_y <= self.panel_height):
            self.value_y = event_y
        elif event_y < 0:
            self.value_y = 0
        elif event_y > self.panel_height:
            self.value_y = self.panel_height

        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton or event.type() == QtCore.QEvent.MouseButtonDblClick):
            # Move Icons
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            # Scale Cursor for Display
            self.cursor_rmb.resize(60*scale_factor, 60*scale_factor) # 60 = max tilt value
            # Move Icons
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.cursor_rmb.resize(0, 0)
            pass
        # Emit Values
        list = [((self.value_x / self.panel_width) * factorSVL), (((self.panel_height - self.value_y) / self.panel_height) * factorSVL)]
        self.SIGNAL_HSV_NEW.emit(list)
        self.update()

    def tabletCursor(self, event):
        if ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.buttons() == QtCore.Qt.LeftButton):
            # Tilt XY
            if event.xTilt() > 30: # X Tilt Right
                pass
            elif event.xTilt() < -30: # X Tilt Left
                pass
            else: # X Tilt Neutral
                pass
            if event.yTilt() > 30: # Y Tilt Down
                tilt_y = event.yTilt() * scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            elif event.yTilt() < -30: # Y Tilt Up
                tilt_y = event.yTilt() * -scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            else: # Y Tilt Neutral
                self.cursor_rmb.resize(0, 0)
        elif ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.buttons() == QtCore.Qt.RightButton):
            pass
        elif event.type() == QtCore.QEvent.TabletRelease:
            self.cursor_rmb.resize(0, 0)

    def Update_Panel(self, sat, val, width, height, hex):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Spin value range to slider range
        percent_sat = sat / factorSVL
        percent_val = val / factorSVL
        self.value_x = percent_sat * self.panel_width
        self.value_y = self.panel_height - (percent_val * self.panel_height)
        # Move Icons
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        self.update()

class PanelHsl(QWidget):
    SIGNAL_HSL_NEW = QtCore.pyqtSignal(list)
    SIGNAL_RELEASE = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(PanelHsl, self).__init__(parent)
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        # Module Style
        self.style = Style()

        # Variables
        self.hex = '#000000'
        # LMB SVG Cursors
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # MMB SVG Cursors
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 12
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.alpha = self.style.Alpha()
        self.cursor_lmb.setStyleSheet(self.alpha)
        self.cursor_rmb.setStyleSheet(self.alpha)

        # Thread Creation
        self.thread_size_hint = threading.Thread(target=self.sizeHint, daemon=True)
        self.thread_mouse_press_event = threading.Thread(target=self.mousePressEvent, daemon=True)
        self.thread_mouse_move_event = threading.Thread(target=self.mouseMoveEvent, daemon=True)
        self.thread_mouse_double_click_event = threading.Thread(target=self.mouseDoubleClickEvent, daemon=True)
        self.thread_mouse_release_event = threading.Thread(target=self.mouseReleaseEvent, daemon=True)
        self.thread_tablet_event = threading.Thread(target=self.tabletEvent, daemon=True)
        self.thread_mouse_cursor = threading.Thread(target=self.mouseCursor, daemon=True)
        self.thread_tablet_cursor = threading.Thread(target=self.tabletCursor, daemon=True)
        self.thread_update_panel = threading.Thread(target=self.Update_Panel, daemon=True)
        # Thread Start
        self.thread_size_hint.start()
        self.thread_mouse_press_event.start()
        self.thread_mouse_move_event.start()
        self.thread_mouse_double_click_event.start()
        self.thread_mouse_release_event.start()
        self.thread_tablet_event.start()
        self.thread_mouse_cursor.start()
        self.thread_tablet_cursor.start()
        self.thread_update_panel.start()

        # Update
        self.update()

    def sizeHint(self):
        return QtCore.QSize(16777215, 16777215)

    def mousePressEvent(self, event):
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)
        self.SIGNAL_RELEASE.emit("Release")

    def tabletEvent(self, event):
        self.tabletCursor(event)

    def mouseCursor(self, event):
        # Mouse Position
        event_x = event.x()
        event_y = event.y()
        # Make Object Move XY
        if (event_x >= 0 and event_x <= self.panel_width):
            self.value_x = event_x
        elif event_x < 0:
            self.value_x = 0
        elif event_x > self.panel_width:
            self.value_x = self.panel_width
        if  (event_y >= 0 and event_y <= self.panel_height):
            self.value_y = event_y
        elif event_y < 0:
            self.value_y = 0
        elif event_y > self.panel_height:
            self.value_y = self.panel_height

        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton or event.type() == QtCore.QEvent.MouseButtonDblClick):
            # Move Icons
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            # Scale Cursor for Display
            self.cursor_rmb.resize(60*scale_factor, 60*scale_factor) # 60 = max tilt value
            # Move Icons
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.cursor_rmb.resize(0, 0)
            pass
        # Emit Values
        list = [((self.value_x / self.panel_width) * factorSVL), (((self.panel_height - self.value_y) / self.panel_height) * factorSVL)]
        self.SIGNAL_HSL_NEW.emit(list)
        self.update()

    def tabletCursor(self, event):
        if ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.buttons() == QtCore.Qt.LeftButton):
            # Tilt XY
            if event.xTilt() > 30: # X Tilt Right
                pass
            elif event.xTilt() < -30: # X Tilt Left
                pass
            else: # X Tilt Neutral
                pass
            if event.yTilt() > 30: # Y Tilt Down
                tilt_y = event.yTilt() * scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            elif event.yTilt() < -30: # Y Tilt Up
                tilt_y = event.yTilt() * -scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            else: # Y Tilt Neutral
                self.cursor_rmb.resize(0, 0)
        elif ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.buttons() == QtCore.Qt.RightButton):
            pass
        elif event.type() == QtCore.QEvent.TabletRelease:
            self.cursor_rmb.resize(0, 0)

    def Update_Panel(self, sat, val, width, height, hex):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Spin value range to slider range
        percent_sat = sat / factorSVL
        percent_val = val / factorSVL
        self.value_x = percent_sat * self.panel_width
        self.value_y = self.panel_height - (percent_val * self.panel_height)
        # Move Icons
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        self.update()
