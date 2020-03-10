from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg

from .pigment_o_style import Style

class PanelHsv(QWidget):

    SIGNAL_HSV_X = QtCore.pyqtSignal(int)
    SIGNAL_HSV_Y = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        super(PanelHsv, self).__init__(parent)
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # Variables
        self.value_x = None
        self.value_y = None
        # Theme for the Buttons
        self.color_bg = QColor('#383838')
        self.color_cursor = QColor('#d4d4d4')

        # Module Style
        self.style = Style()

        # LMB SVG Cursors
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_LMB('#000000')
        self.cursor_lmb.load(self.array_lmb)
        # MMB SVG Cursors
        self.cursor_select = QtSvg.QSvgWidget(self)
        self.array_select = self.style.SVG_Select('#000000')
        self.cursor_select.load(self.array_select)
        # Style SVG Cursors
        self.cursor_lmb.setGeometry(QtCore.QRect(6,6,12,12))
        self.cursor_select.setGeometry(QtCore.QRect(6,6,12,12))
        self.cursor_select.resize(0, 0)
        self.alpha = self.style.Alpha()
        self.cursor_lmb.setStyleSheet(self.alpha)
        self.cursor_select.setStyleSheet(self.alpha)

    def sizeHint(self):
        return QtCore.QSize(16777215,16777215)

    def paintEvent(self, event):
        # Limit for the Limit Range
        self.panel_width = event.rect().width()
        self.panel_height = event.rect().height()
        # Draw Elements
        self.drawCircle(event)
        self.drawDot(event)

    def drawCircle(self, event):
        pass

    def drawDot(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Cursor
        if (self.value_x is not None and self.value_y is not None):
            # Dot Shape
            dot = QPolygon([
                QPoint(self.value_x+0.0, self.value_y+3.3499),
                QPoint(self.value_x+0.45441, self.value_y+3.319),
                QPoint(self.value_x+0.8902, self.value_y+3.2295),
                QPoint(self.value_x+1.3035, self.value_y+3.0859),
                QPoint(self.value_x+1.6905, self.value_y+2.8921),
                QPoint(self.value_x+2.0471, self.value_y+2.6517),
                QPoint(self.value_x+2.369, self.value_y+2.3685),
                QPoint(self.value_x+2.6521, self.value_y+2.0466),
                QPoint(self.value_x+2.8924, self.value_y+1.69),
                QPoint(self.value_x+3.0861, self.value_y+1.3031),
                QPoint(self.value_x+3.2296, self.value_y+0.88985),
                QPoint(self.value_x+3.319, self.value_y+0.45422),

                QPoint(self.value_x+3.3499, self.value_y+0),
                QPoint(self.value_x+3.319, self.value_y-0.45422),
                QPoint(self.value_x+3.2296, self.value_y-0.88985),
                QPoint(self.value_x+3.0861, self.value_y-1.3031),
                QPoint(self.value_x+2.8924, self.value_y-1.69),
                QPoint(self.value_x+2.6521, self.value_y-2.0466),
                QPoint(self.value_x+2.369, self.value_y-2.3685),
                QPoint(self.value_x+2.0471, self.value_y-2.6517),
                QPoint(self.value_x+1.6905, self.value_y-2.8921),
                QPoint(self.value_x+1.3035, self.value_y-3.0859),
                QPoint(self.value_x+0.8902, self.value_y-3.2295),
                QPoint(self.value_x+0.45441, self.value_y-3.319),

                QPoint(self.value_x+0, self.value_y-3.3499),
                QPoint(self.value_x-0.45441, self.value_y-3.319),
                QPoint(self.value_x-0.8902, self.value_y-3.2295),
                QPoint(self.value_x-1.3035, self.value_y-3.0859),
                QPoint(self.value_x-1.6905, self.value_y-2.8921),
                QPoint(self.value_x-2.0471, self.value_y-2.6517),
                QPoint(self.value_x-2.369, self.value_y-2.3685),
                QPoint(self.value_x-2.6521, self.value_y-2.0466),
                QPoint(self.value_x-2.8924, self.value_y-1.69),
                QPoint(self.value_x-3.0861, self.value_y-1.3031),
                QPoint(self.value_x-3.2296, self.value_y-0.88985),
                QPoint(self.value_x-3.319, self.value_y-0.45422),

                QPoint(self.value_x-3.3499, self.value_y+0),
                QPoint(self.value_x-3.319, self.value_y+0.45422),
                QPoint(self.value_x-3.2296, self.value_y+0.88985),
                QPoint(self.value_x-3.0861, self.value_y+1.3031),
                QPoint(self.value_x-2.8924, self.value_y+1.69),
                QPoint(self.value_x-2.6521, self.value_y+2.0466),
                QPoint(self.value_x-2.369, self.value_y+2.3685),
                QPoint(self.value_x-2.0471, self.value_y+2.6517),
                QPoint(self.value_x-1.6905, self.value_y+2.8921),
                QPoint(self.value_x-1.3035, self.value_y+3.0859),
                QPoint(self.value_x-0.8902, self.value_y+3.2295),
                QPoint(self.value_x-0.45441, self.value_y+3.319)
                ])
            square = QPolygon([
                QPoint(self.value_x-5,self.value_y-5),
                QPoint(self.value_x+5,self.value_y-5),
                QPoint(self.value_x+5,self.value_y+5),
                QPoint(self.value_x-5,self.value_y+5)
                ])
            circle = QPolygon([
                QPoint(self.value_x+0, self.value_y+3.3651),
                QPoint(self.value_x+0.86732, self.value_y+3.2555),
                QPoint(self.value_x+1.6763, self.value_y+2.9253),
                QPoint(self.value_x+2.3721, self.value_y+2.3972),
                QPoint(self.value_x+2.9076, self.value_y+1.707),
                QPoint(self.value_x+3.2463, self.value_y+0.90155),
                QPoint(self.value_x+3.3651, self.value_y+0),
                QPoint(self.value_x+3.2555, self.value_y-0.83191),
                QPoint(self.value_x+2.9253, self.value_y-1.6409),
                QPoint(self.value_x+2.3972, self.value_y-2.3367),
                QPoint(self.value_x+1.707, self.value_y-2.8722),
                QPoint(self.value_x+0.90155, self.value_y-3.2109),

                QPoint(self.value_x+0, self.value_y-3.3297),
                QPoint(self.value_x-0.83192, self.value_y-3.2201),
                QPoint(self.value_x-1.6409, self.value_y-2.8899),
                QPoint(self.value_x-2.3367, self.value_y-2.3618),
                QPoint(self.value_x-2.8722, self.value_y-1.6716),
                QPoint(self.value_x-3.2109, self.value_y-0.86615),
                QPoint(self.value_x-3.3297, self.value_y-0),
                QPoint(self.value_x-3.2201, self.value_y+0.86731),
                QPoint(self.value_x-2.8899, self.value_y+1.6763),
                QPoint(self.value_x-2.3618, self.value_y+2.3721),
                QPoint(self.value_x-1.6716, self.value_y+2.9076),
                QPoint(self.value_x-0.86615, self.value_y+3.2463)
                ])
            diamond = QPolygon([
                QPoint(self.value_x+4, self.value_y+6),
                QPoint(self.value_x+6, self.value_y+4),
                QPoint(self.value_x+6, self.value_y-4),
                QPoint(self.value_x+4, self.value_y-6),
                QPoint(self.value_x-4, self.value_y-6),
                QPoint(self.value_x-6, self.value_y-4),
                QPoint(self.value_x-6, self.value_y+4),
                QPoint(self.value_x-4, self.value_y+6),
                ])
            # Draw 1
            painter.setPen(QPen(self.color_bg, 0, Qt.NoPen))
            painter.setBrush(QBrush(self.color_bg))
            # painter.drawPolygon(diamond)
            # painter.drawEllipse(self.value_x-50, self.value_y-50, 100, 100)
        # Finish QPainter
        painter.end()
        self.update()

    def mousePressEvent(self, event):
        self.Emit_Value(event)
        self.update()
    def mouseMoveEvent(self, event):
        self.Emit_Value(event)
        self.update()
    def mouseReleaseEvent(self, event):
        self.Emit_Value(event)
        self.update()
    def mouseDoubleClickEvent(self, event):
        self.Emit_Value(event)
        self.update()

    def Emit_Value(self, event):
        # Limit Value inside Range
        self.value_x = self.Limit_Range_X(event)
        self.value_y = self.Limit_Range_Y(event)
        # Range Consideration
        range = 100
        # Convert Value to Range
        percentage_x = self.value_x / self.panel_width
        percentage_y = self.value_y / self.panel_height
        value_xx = percentage_x * range
        value_yy = percentage_y * range
        # Emit Signals
        self.SIGNAL_HSV_X.emit(value_xx)
        self.SIGNAL_HSV_Y.emit(value_yy)

    # def tabletEvent(self, tabletEvent):
    #     self.pen_x = tabletEvent.globalX()
    #     self.pen_y = tabletEvent.globalY()
    #     self.pen_pressure = int(tabletEvent.pressure() * 100)
    #     if tabletEvent.type() == QTabletEvent.TabletPress:
    #         self.pen_is_down = True
    #         self.text = "TabletPress event"
    #     elif tabletEvent.type() == QTabletEvent.TabletMove:
    #         self.pen_is_down = True
    #         self.text = "TabletMove event"
    #     elif tabletEvent.type() == QTabletEvent.TabletRelease:
    #         self.pen_is_down = False
    #         self.text = "TabletRelease event"
    #     self.text += " at x={0}, y={1}, pressure={2}%,".format(self.pen_x, self.pen_y, self.pen_pressure)
    #     if self.pen_is_down:
    #         self.text += " Pen is down."
    #     else:
    #         self.text += " Pen is up."
    #     tabletEvent.accept()
    #     self.update()

    def Limit_Range_X(self, event):
        # Axis X Limits
        pos_x = event.pos().x()
        if pos_x <= 0:
            x = 0
        elif pos_x >= self.panel_width:
            x = self.panel_width
        else:
            x = pos_x
        return x

    def Limit_Range_Y(self, event):
        # Axis Y Limits
        pos_y = event.pos().y()
        if pos_y <= 0:
            y = 0
        elif pos_y >= self.panel_height:
            y = self.panel_height
        else:
            y = pos_y
        return y

    def Update(self, mode, sat, val, width, height):
        # Update the variables
        self.mode = mode
        self.panel_width = width
        self.panel_height = height
        if self.mode == "RGBA":
            pass
        elif self.mode == "HSVA":
            pass
        # Spin value range to slider range
        percent = value / self.range
        self.value_x = percent * self.channel_width
        # Redraw everything
        self.update()

    def Cursor_Update_Color(self, color):
        # Change Color
        self.array_select = self.ss.SVG_Select(str(self.layout.lineEdit_hex.text()))
        self.cursor_select.load(self.array_select)
