from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui
import threading
from .pigment_o_constants import Constants

# Color Space Factors
constant1 = Constants().Krita()
factorAAA = constant1[0]
factorRGB = constant1[1]
factorHUE = constant1[2]
factorSVL = constant1[3]
factorCMYK = constant1[4]

class Channel_Linear(QWidget):
    SIGNAL_VALUE = QtCore.pyqtSignal(int)
    SIGNAL_RELEASE = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Channel_Linear, self).__init__(parent)
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # Variables
        self.channel_padding = 2
        self.value_x = None
        # Theme for the Buttons
        self.color_bg = QColor('#383838')
        self.color_cursor = QColor('#d4d4d4')

        # Thread Creation
        self.thread_setup = threading.Thread(target=self.Setup, daemon=True)
        self.thread_size_hint = threading.Thread(target=self.sizeHint, daemon=True)
        self.thread_paint_event = threading.Thread(target=self.paintEvent, daemon=True)
        self.thread_draw_cursor = threading.Thread(target=self.drawCursor, daemon=True)
        self.thread_mouse_press_event = threading.Thread(target=self.mousePressEvent, daemon=True)
        self.thread_mouse_move_event = threading.Thread(target=self.mouseMoveEvent, daemon=True)
        self.thread_mouse_double_click_event = threading.Thread(target=self.mouseDoubleClickEvent, daemon=True)
        self.thread_mouse_release_event = threading.Thread(target=self.mouseReleaseEvent, daemon=True)
        self.thread_emit_value = threading.Thread(target=self.Emit_Value, daemon=True)
        self.thread_emit_value_pin = threading.Thread(target=self.Emit_Value_Pin, daemon=True)
        self.thread_limit_range = threading.Thread(target=self.Limit_Range, daemon=True)
        self.thread_update = threading.Thread(target=self.Update, daemon=True)
        # Thread Start
        self.thread_setup.start()
        self.thread_size_hint.start()
        self.thread_paint_event.start()
        self.thread_draw_cursor.start()
        self.thread_mouse_press_event.start()
        self.thread_mouse_move_event.start()
        self.thread_mouse_double_click_event.start()
        self.thread_mouse_release_event.start()
        self.thread_emit_value.start()
        self.thread_emit_value_pin.start()
        self.thread_limit_range.start()
        self.thread_update.start()

    def Setup(self, mode):
        self.mode = mode

    def sizeHint(self):
        return QtCore.QSize(16777215,20)

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
        channel_middle = channel_height / 2
        diamond_dist = 4
        left = self.value_x - diamond_dist
        right = self.value_x + diamond_dist
        top = channel_middle - diamond_dist
        bot = channel_middle + diamond_dist
        # Cursor
        if self.value_x is not None:
            # Diamonds
            diamond = QPolygon([
                QPoint(self.value_x, top),
                QPoint(left, channel_middle),
                QPoint(self.value_x, bot),
                QPoint(right, channel_middle)
                ])
            # Draw
            painter.setPen(QPen(self.color_bg, 1, Qt.SolidLine))
            painter.setBrush(QBrush(self.color_cursor))
            painter.drawPolygon(diamond)
        # Finish QPainter
        painter.end()
        self.update()

    def mousePressEvent(self, event):
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
            self.SIGNAL_RELEASE.emit("Release")
        else:
            self.Emit_Value(event)
            self.SIGNAL_RELEASE.emit("Release")
        self.update()

    def Emit_Value(self, event):
        # Limit Value inside Range
        self.value_x = self.Limit_Range(event)
        # Range Consideration
        if self.mode == "AAA":
            range = factorAAA
        elif self.mode == "RGB":
            range = factorRGB
        elif self.mode == "HUE":
            range = factorHUE
        elif self.mode == "SVL":
            range = factorSVL
        elif self.mode == "CMYK":
            range = factorCMYK
        elif self.mode == "XYZ":
            range = factorXYZ
        elif self.mode == "LLL":
            range = factorLLL
        # elif self.mode == "AB":
        #     range = factorAB
        elif self.mode == "YYY":
            range = factorYYY
        # elif self.mode == "CBCR":
        #     range = factorCBCR
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        value = percentage * range
        self.SIGNAL_VALUE.emit(value)

    def Emit_Value_Pin(self, event):
        # Confirm 10 Percentil Values
        position = event.pos().x()
        # Channel Discrimination
        if self.mode == "HUE":
            # Pin to 6
            pp = self.channel_width / 12
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
            elif (position >= (pp*11) and position < (pp*12)):
                self.value_x = pp*12
        else:
            # Pin to 10
            pp = self.channel_width / 20
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
        # Range Consideration
        if self.mode == "AAA":
            range = factorAAA
        elif self.mode == "RGB":
            range = factorRGB
        elif self.mode == "HUE":
            range = factorHUE
        elif self.mode == "SVL":
            range = factorSVL
        elif self.mode == "CMYK":
            range = factorCMYK
        elif self.mode == "XYZ":
            range = factorXYZ
        elif self.mode == "LLL":
            range = factorLLL
        elif self.mode == "AB":
            range = factorAB
        elif self.mode == "YYY":
            range = factorYYY
        elif self.mode == "CBCR":
            range = factorCBCR
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        value = percentage * range
        self.SIGNAL_VALUE.emit(value)

    def Limit_Range(self, event):
        position = event.pos().x()
        if position <= 0:
            x = 0
        elif position >= self.channel_width:
            x = self.channel_width
        else:
            x = position
        return x

    def Update(self, value, range, width):
        # Update the variables
        self.range = range
        self.channel_width = width
        # Spin value range to slider range
        percent = value / self.range
        self.value_x = percent * self.channel_width
        # Limit Range
        if self.value_x <= 0:
            self.value_x = 0
        elif self.value_x >= self.channel_width:
            self.value_x = self.channel_width
        # Redraw everything
        self.update()
