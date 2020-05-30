from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui
import threading

class Mixer_Color(QWidget):
    SIGNAL_MIXER_COLOR = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Mixer_Color, self).__init__(parent)
        self.save = None

    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier):
            self.SIGNAL_MIXER_COLOR.emit("SAVE")
            self.update()
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.SIGNAL_MIXER_COLOR.emit("CLEAN")
            self.update()
        else:
            self.SIGNAL_MIXER_COLOR.emit("APPLY")
            self.update()

class Mixer_Gradient(QWidget):
    SIGNAL_MIXER_GRADIENT = QtCore.pyqtSignal(int)
    SIGNAL_RELEASE = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Mixer_Gradient, self).__init__(parent)
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # Variables
        self.channel_padding = 2
        self.cursor_width = 6
        self.value_x = None
        # Theme for the Buttons
        self.color_bg = QColor('#383838')
        self.color_cursor = QColor('#d4d4d4')

        # Thread Creation
        self.thread_size_hint = threading.Thread(target=self.sizeHint, daemon=True)
        self.thread_paint_event = threading.Thread(target=self.paintEvent, daemon=True)
        self.thread_draw_cursor = threading.Thread(target=self.drawCursor, daemon=True)
        self.thread_mouse_press_event = threading.Thread(target=self.mousePressevent, daemon=True)
        self.thread_mouse_move_event = threading.Thread(target=self.mouseMoveEvent, daemon=True)
        self.thread_mouse_double_click_event = threading.Thread(target=self.mouseDoubleClickEvent, daemon=True)
        self.thread_mouse_release_event = threading.Thread(target=self.mouseReleaseEvent, daemon=True)
        self.thread_emit_value = threading.Thread(target=self.Emit_Value, daemon=True)
        self.thread_emit_value_pin = threading.Thread(target=self.Emit_Value_Pin, daemon=True)
        self.thread_update = threading.Thread(target=self.Update, daemon=True)
        # Thread Creation
        self.thread_size_hint.start()
        self.thread_paint_event.start()
        self.thread_draw_cursor.start()
        self.thread_mouse_press_event.start()
        self.thread_mouse_move_event.start()
        self.thread_mouse_double_click_event.start()
        self.thread_mouse_release_event.start()
        self.thread_emit_value.start()
        self.thread_emit_value_pin.start()
        self.thread_update.start()

    def sizeHint(self):
        return QtCore.QSize(16777215,15)

    def paintEvent(self, event):
        # Limit for the Limit Range
        self.channel_width = event.rect().width()
        # Draw Elements
        self.drawCursor(event)

    def drawCursor(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Available Space Calculations
        self.channel_width = event.rect().width()
        channel_height = event.rect().height()
        channel_pad = self.channel_padding / 2
        # channel_crop = channel_height - channel_pad
        channel_tri = channel_height + channel_pad
        tri = 5
        # Cursor
        if self.value_x is not None:
            # cursor_point = self.value_x
            cursor_left = self.value_x - self.cursor_width
            cursor_right = self.value_x + self.cursor_width
            # Polygons
            triangle = QPolygon([
                QPoint(self.value_x, (channel_height - tri)),
                QPoint(cursor_left, channel_tri),
                QPoint(cursor_right, channel_tri)])
            # Draw
            painter.setPen(QPen(self.color_bg, 1, Qt.SolidLine))
            painter.setBrush(QBrush(self.color_cursor))
            painter.drawPolygon(triangle)
        # Finish QPainter
        painter.end()
        self.update()

    def mousePressevent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
        self.update()
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
        self.update()
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
        self.update()
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
        self.SIGNAL_RELEASE.emit("RELEASE")
        self.update()

    def Emit_Value(self, event):
        # Convert Value to Percentage
        position = event.pos().x()
        if position < 0:
            position = 0
        elif position > self.channel_width:
            position = self.channel_width
        else:
            position = position
        self.value_x = position
        self.SIGNAL_MIXER_GRADIENT.emit(self.value_x)

    def Emit_Value_Pin(self, event):
        # Confirm 10 Percentil Values
        position = event.pos().x()
        pp = self.channel_width / 20
        # Pin to 10 Percentil Near
        if (position >= 0 and position < (pp*1)):
            self.value_x = 0
        elif (position >= (pp*1) and position < (pp*3)):
            self.value_x = pp*2
        elif (position >= (pp*3) and position < (pp*5)):
            self.value_x = pp*4
        elif (position >= (pp*5) and position < (pp*7)):
            self.value_x = pp*6
        elif (position >= (pp*7) and position < (pp*9)):
            self.value_x = pp*8
        elif (position >= (pp*9) and position < (pp*11)):
            self.value_x = pp*10
        elif (position >= (pp*11) and position < (pp*13)):
            self.value_x = pp*12
        elif (position >= (pp*13) and position < (pp*15)):
            self.value_x = pp*14
        elif (position >= (pp*15) and position < (pp*17)):
            self.value_x = pp*16
        elif (position >= (pp*17) and position < (pp*19)):
            self.value_x = pp*18
        elif (position >= (pp*19) and position < (pp*20)):
            self.value_x = pp*20
        # Emit
        self.SIGNAL_MIXER_GRADIENT.emit(self.value_x)

    def Update(self, value, width):
        # Update the variables
        self.channel_width = width
        # Spin value range to slider range
        self.value_x = value * self.channel_width
        # Redraw everything
        self.update()
