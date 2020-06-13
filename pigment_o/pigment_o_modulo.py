from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg

class Channel_Linear(QWidget):
    SIGNAL_VALUE = QtCore.pyqtSignal(float)
    SIGNAL_RELEASE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Channel_Linear, self).__init__(parent)

        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Variables(self):
        # Variables
        self.channel_padding = 2
        self.value_x = None
        # Theme for the Buttons
        self.color_bg = QColor('#383838')
        self.color_cursor = QColor('#d4d4d4')

    # Relay
    def Setup(self, mode):
        self.mode = mode
    def Update(self, value, width):
        # Update the variables
        self.channel_width = width
        self.value_x = value * self.channel_width
        # Limit Range
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.channel_width:
            self.value_x = self.channel_width
    def sizeHint(self):
        return QtCore.QSize(5000,20)

    # Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
        else:
            self.Emit_Value(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.Emit_Value_Pin(event)
            self.SIGNAL_RELEASE.emit(0)
        else:
            self.Emit_Value(event)
            self.SIGNAL_RELEASE.emit(0)

    # Emission
    def Emit_Value(self, event):
        # Limit Value inside Range
        self.value_x = event.pos().x()
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.channel_width:
            self.value_x = self.channel_width
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        self.SIGNAL_VALUE.emit(percentage)
    def Emit_Value_Pin(self, event):
        # Confirm 10 Percentil Values
        position = event.pos().x()
        # Channel Discrimination
        if self.mode == "HUE":
            # Pin to 6
            pp = self.channel_width / 12
            if (position >= 0 and position < (pp*1)):
                self.value_x = 0
            if (position >= (pp*1) and position < (pp*3)):
                self.value_x = pp*2
            if (position >= (pp*3) and position < (pp*5)):
                self.value_x = pp*4
            if (position >= (pp*5) and position < (pp*7)):
                self.value_x = pp*6
            if (position >= (pp*7) and position < (pp*9)):
                self.value_x = pp*8
            if (position >= (pp*9) and position < (pp*11)):
                self.value_x = pp*10
            if (position >= (pp*11) and position < (pp*12)):
                self.value_x = pp*12
        else:
            # Pin to 10
            pp = self.channel_width / 20
            if (position >= 0 and position < (pp*1)):
                self.value_x = 0
            if (position >= (pp*1) and position < (pp*3)):
                self.value_x = pp*2
            if (position >= (pp*3) and position < (pp*5)):
                self.value_x = pp*4
            if (position >= (pp*5) and position < (pp*7)):
                self.value_x = pp*6
            if (position >= (pp*7) and position < (pp*9)):
                self.value_x = pp*8
            if (position >= (pp*9) and position < (pp*11)):
                self.value_x = pp*10
            if (position >= (pp*11) and position < (pp*13)):
                self.value_x = pp*12
            if (position >= (pp*13) and position < (pp*15)):
                self.value_x = pp*14
            if (position >= (pp*15) and position < (pp*17)):
                self.value_x = pp*16
            if (position >= (pp*17) and position < (pp*19)):
                self.value_x = pp*18
            if (position >= (pp*19) and position < (pp*20)):
                self.value_x = pp*20
        # Convert Value to Range
        percentage = self.value_x / self.channel_width
        self.SIGNAL_VALUE.emit(percentage)

    # Paint Style
    def paintEvent(self, event):
        # Limit for the Limit Range
        self.channel_width = event.rect().width()
        # Draw Elements
        self.drawCursor(event)
    def drawCursor(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.begin(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # Available Space Calculations
        self.channel_width = event.rect().width()
        channel_height = event.rect().height()
        channel_middle = channel_height / 2
        diamond_dist = 5
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


class Clicks(QWidget):
    SIGNAL_APPLY = QtCore.pyqtSignal(int)
    SIGNAL_SAVE = QtCore.pyqtSignal(int)
    SIGNAL_CLEAN = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Clicks, self).__init__(parent)
        self.cond = None

    # Relay
    def Setup(self, size, opacity, flow):
        self.cond = "TIP"
        self.size = size
        self.opacity = opacity
        self.flow = flow

    # Interaction
    def mousePressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.SIGNAL_APPLY.emit(0)
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.SIGNAL_SAVE.emit(1)
        if event.modifiers() == QtCore.Qt.AltModifier:
            self.SIGNAL_CLEAN.emit(2)
        self.update()
    def mouseDoubleClickEvent(self, event):
        self.SIGNAL_APPLY.emit(0)
        self.update()

    # Paint Style
    def paintEvent(self, event):
        if self.cond == "TIP":
            # Text
            self.text = str(self.size)+"\n"+str(round(self.opacity*100,0))+"\n"+str(round(self.flow*100,0))
            # QPainter Start
            qp = QPainter()
            qp.begin(self)
            # Background
            brush = QBrush(QColor(0, 0, 0, 50), Qt.SolidPattern)
            qp.setBrush(brush)
            qp.drawRect(-5, -5, 50, 50)
            # Letters
            qp.setPen(QColor(255, 255, 255))
            qp.setFont(QFont('Monospace', 5))
            qp.drawText(event.rect(), Qt.AlignCenter|Qt.AlignVCenter, self.text)
            # Finish
            qp.end()


class Mixer_Gradient(QWidget):
    SIGNAL_MIXER_VALUE = QtCore.pyqtSignal(int)
    SIGNAL_MIXER_RELEASE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Mixer_Gradient, self).__init__(parent)
        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Variables(self):
        # Variables
        self.channel_padding = 2
        self.cursor_width = 6
        self.value_x = None
        # Theme for the Buttons
        self.color_bg = QColor('#383838')
        self.color_cursor = QColor('#d4d4d4')

    # Relay
    def Update(self, value, width):
        # Update the variables
        self.channel_width = width
        # Spin value range to slider range
        self.value_x = value * self.channel_width
        # Redraw everything
        self.update()

    # Interaction
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
        else:
            self.Emit_Value(event)
        self.SIGNAL_MIXER_RELEASE.emit(0)
        self.update()

    # Emission
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
        self.SIGNAL_MIXER_VALUE.emit(self.value_x)
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
        self.SIGNAL_MIXER_VALUE.emit(self.value_x)

    # Paint Style
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
    def sizeHint(self):
        return QtCore.QSize(16777215,15)


class Panel_HSV(QWidget):
    SIGNAL_HSV_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSV_RELEASE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSV, self).__init__(parent)
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
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
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 2

    # Relay
    def Update_Panel(self, percent_sat, percent_val, width, height, hex):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Spin value range to slider range
        self.value_x = percent_sat * self.panel_width
        self.value_y = self.panel_height - (percent_val * self.panel_height)
        # Move Icons
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)
        self.SIGNAL_HSV_RELEASE.emit(0)
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
        # Correct Cursor
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton or event.type() == QtCore.QEvent.MouseButtonDblClick):
            # Move Icons
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            # Scale Cursor for Display
            self.cursor_rmb.resize(60*self.scale_factor, 60*self.scale_factor) # 60 = max tilt value
            # Move Icons
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.cursor_rmb.resize(0, 0)
        # Emit Values
        list = [((self.value_x / self.panel_width)), (((self.panel_height - self.value_y) / self.panel_height))]
        self.SIGNAL_HSV_VALUE.emit(list)

    # Tablet Interaction
    def tabletEvent(self, event):
        self.tabletCursor(event)
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
                tilt_y = event.yTilt() * self.scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            elif event.yTilt() < -30: # Y Tilt Up
                tilt_y = event.yTilt() * -self.scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            else: # Y Tilt Neutral
                self.cursor_rmb.resize(0, 0)
        elif ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.buttons() == QtCore.Qt.RightButton):
            pass
        elif event.type() == QtCore.QEvent.TabletRelease:
            self.cursor_rmb.resize(0, 0)


class Panel_HSL(QWidget):
    SIGNAL_HSL_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSL_RELEASE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSL, self).__init__(parent)
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
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
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 2

    # Relay
    def Update_Panel(self, percent_sat, percent_val, width, height, hex):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Spin value range to slider range
        self.value_x = percent_sat * self.panel_width
        self.value_y = self.panel_height - (percent_val * self.panel_height)
        # Move Icons
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)
        self.SIGNAL_HSL_RELEASE.emit(0)
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
            self.cursor_rmb.resize(60*self.scale_factor, 60*self.scale_factor) # 60 = max tilt value
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
        list = [((self.value_x / self.panel_width)), (((self.panel_height - self.value_y) / self.panel_height))]
        self.SIGNAL_HSL_VALUE.emit(list)

    # Tablet Interaction
    def tabletEvent(self, event):
        self.tabletCursor(event)
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
                tilt_y = event.yTilt() * self.scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            elif event.yTilt() < -30: # Y Tilt Up
                tilt_y = event.yTilt() * -self.scale_factor
                self.cursor_rmb.resize(tilt_y, tilt_y)
            else: # Y Tilt Neutral
                self.cursor_rmb.resize(0, 0)
        elif ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.buttons() == QtCore.Qt.RightButton):
            pass
        elif event.type() == QtCore.QEvent.TabletRelease:
            self.cursor_rmb.resize(0, 0)


class Style(QWidget):
    def SVG_Cursor_LMB(self):
        string_cursor_lmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#ffffff;fill-opacity:1;stroke:none;stroke-width:1.29929912\" \n" +
        "     d=\"M 50,6 A 43.999998,43.999998 0 0 0 6,50 43.999998,43.999998 0 0 0 50,94 43.999998,43.999998 0 0 0 94,50 43.999998,43.999998 0 0 0 50,6 Z m 0,6.5 A 37.500001,37.500001 0 0 1 87.5,50 37.500001,37.500001 0 0 1 50,87.5 37.500001,37.500001 0 0 1 12.5,50 37.500001,37.500001 0 0 1 50,12.5 Z\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     id=\"circle821\" \n" +
        "     inkscape:label=\"White\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "</svg> "
        )
        array_cursor_lmb = bytearray(string_cursor_lmb, encoding='utf-8')
        return array_cursor_lmb
    def SVG_Cursor_RMB(self, color):
        color = str(color)
        string_cursor_rmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <circle \n" +
        "     style=\"display:inline;fill:"+color+";fill-opacity:1;stroke:none;stroke-width:0.97447437\" \n" +
        "     id=\"circle816\" \n" +
        "     cx=\"37.5\" \n" +
        "     cy=\"37.500004\" \n" +
        "     inkscape:label=\"Color\" \n" +
        "     r=\"33\" /> \n" +
        "</svg> "
        )
        array_cursor_rmb = bytearray(string_cursor_rmb, encoding='utf-8')
        return array_cursor_rmb
    def Transparent(self):
        transparent = "background-color: rgba(0, 0, 0, 0); border: 1px solid rgba(0, 0, 0, 0) ;"
        return transparent
