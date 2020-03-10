from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui

class Channel(QWidget):

    SIGNALVALUE = QtCore.pyqtSignal(int)
    SIGNALSYNC = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Channel, self).__init__(parent)
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # Variables
        self.channel_padding = 2
        self.value_x = None
        # Theme for the Buttons
        self.color_bg = QColor('#383838')
        self.color_cursor = QColor('#d4d4d4')

    def Setup(self, mode, channel):
        self.mode = mode
        self.channel = channel

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
        self.Emit_Value(event)
        self.SIGNALSYNC.emit("True")
        self.update()
    def mouseMoveEvent(self, event):
        self.Emit_Value(event)
        self.SIGNALSYNC.emit("True")
        self.update()
    def mouseDoubleClickEvent(self, event):
        self.Emit_Value(event)
        self.SIGNALSYNC.emit("True")
        self.update()
    def mouseReleaseEvent(self, event):
        self.Emit_Value(event)
        self.SIGNALSYNC.emit("False")
        self.update()

    def Emit_Value(self, event):
        # Limit Value inside Range
        self.value_x = self.Limit_Range(event)
        # Range Consideration
        if self.mode == "RGB":
            range = 255
        elif self.mode == "HSV":
            if self.channel == 1:
                range = 360
            if self.channel == 2 or self.channel == 3:
                range = 100
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        value = percentage * range
        self.SIGNALVALUE.emit(value)

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
        # Redraw everything
        self.update()
