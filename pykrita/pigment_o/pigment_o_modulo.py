from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg
import math


class Channel_Linear(QWidget):
    SIGNAL_VALUE = QtCore.pyqtSignal(float)
    SIGNAL_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)
    SIGNAL_HALF = QtCore.pyqtSignal(int)
    SIGNAL_MINUS = QtCore.pyqtSignal(int)
    SIGNAL_PLUS = QtCore.pyqtSignal(int)

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
        self.cursor_width = 6
        self.value_x = 0
        # Theme for the Buttons
        self.color_transparent = QColor(Qt.transparent)
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')

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
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.Emit_Value_Unit(event)
        else:
            self.Emit_Value(event)
    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.Emit_Value(event)
    def mouseDoubleClickEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.Emit_Value(event)
    def mouseReleaseEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.Emit_Value_Half(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.Emit_Value_Pin(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            pass
        else:
            self.Emit_Value(event)
        self.SIGNAL_RELEASE.emit(0)
        self.SIGNAL_ZOOM.emit(0)

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
        # Zoom PanelColor
        if event.buttons() == QtCore.Qt.RightButton:
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.SIGNAL_ZOOM.emit(0)
    def Emit_Value_Half(self, event): # SHIFT
        self.SIGNAL_HALF.emit(1)
    def Emit_Value_Pin(self, event): # CTRL
        # Confirm 10 Percentil Values
        position = event.pos().x()
        # Channel Discrimination
        if (self.mode == "HUE" or self.mode == "ARD3"):
            # Pin to 7
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
            # Pin to 11
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
        # Zoom PanelColor
        if event.buttons() == QtCore.Qt.RightButton:
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.SIGNAL_ZOOM.emit(0)
    def Emit_Value_Unit(self, event): # ALT
        if event.x() <= (self.channel_width*0.5):
            self.SIGNAL_MINUS.emit(1)
        else:
            self.SIGNAL_PLUS.emit(1)

    # Paint Style
    def paintEvent(self, event):
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
        half_height = channel_height / 2
        h2 = half_height - 1.5
        h3 = half_height + 1.5
        # Cursor
        if self.value_x is not None:
            if self.mode == "NEU":
                top = 0
                bot = channel_height
                # Square
                polygon = QPolygon([
                    QPoint(self.value_x, top),
                    QPoint(0, top),
                    QPoint(0, bot),
                    QPoint(self.value_x, bot)
                    ])
            else:
                # Diamonds
                diamond_dist = 7
                left = self.value_x - diamond_dist
                right = self.value_x + diamond_dist
                top = channel_middle - diamond_dist
                bot = channel_middle + diamond_dist
                polygon = QPolygon([
                    QPoint(self.value_x, top),
                    QPoint(left, channel_middle),
                    QPoint(self.value_x, bot),
                    QPoint(right, channel_middle)
                    ])
            # Draw
            painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.setBrush(QBrush(self.color_light))
            painter.drawPolygon(polygon)
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
    def Setup_SOF(self, size, opacity, flow):
        self.cond = "TIP"
        self.size = size
        self.opacity = opacity
        self.flow = flow
    def sizeHint(self):
        return QtCore.QSize(1000,1000)

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
            self.text = (
                "S_"+str(round(self.size,0))+"\n"+
                "O_"+str(round(self.opacity*100,0))+"\n"+
                "F_"+str(round(self.flow*100,0))
                )
            self.drawColors(event)
    def drawColors(self, event):
        # QPainter Start
        painter = QPainter()
        painter.begin(self)
        # Background
        brush = QBrush(QColor(0, 0, 0, 0), Qt.NoBrush)
        painter.setBrush(brush)
        painter.drawRect(-5, -5, 100, 100)
        # Letters
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Monospace', 5))
        painter.drawText(event.rect(), Qt.AlignHCenter|Qt.AlignVCenter, self.text)
        # Finish
        painter.end()


class Apply_RGB(QWidget):
    SIGNAL_APPLY = QtCore.pyqtSignal(list)

    # Init
    def __init__(self, parent):
        super(Apply_RGB, self).__init__(parent)

    # Relay
    def Setup(self, value_1, value_2, value_3):
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3
    def sizeHint(self):
        return QtCore.QSize(1000,1000)

    # Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.SIGNAL_APPLY.emit([self.value_1, self.value_2, self.value_3])
    def mouseDoubleClickEvent(self, event):
        self.SIGNAL_APPLY.emit([self.value_1, self.value_2, self.value_3])


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
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')

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
        channel_height = event.rect().height()
        channel_pad = self.channel_padding / 2
        channel_tri = channel_height + channel_pad
        # Cursor
        if self.value_x is not None:
            # cursor_point = self.value_x
            tri = 8
            cursor_left = self.value_x - tri
            cursor_right = self.value_x + tri
            # Polygons
            triangle = QPolygon([
                QPoint(self.value_x, (channel_height - tri)),
                QPoint(cursor_left, channel_height),
                QPoint(cursor_right, channel_height)])
            # Draw
            painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine))
            painter.setBrush(QBrush(self.color_light))
            painter.drawPolygon(triangle)
        # Finish QPainter
        painter.end()
    def sizeHint(self):
        return QtCore.QSize(16777215,15)


class Harmony(QWidget):
    SIGNAL_ACTIVE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Harmony, self).__init__(parent)
        self.width = 0
        self.height = 0
        self.active = False
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
    def sizeHint(self):
        return QtCore.QSize(1000,1000)

    # Relay
    def Update(self, width, height):
        self.width = width
        self.height = height
    def Active(self, active):
        self.active = active

    # Interaction
    def mousePressEvent(self, event):
        self.SIGNAL_ACTIVE.emit(0)

    # Paint Style
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QPen(self.color_dark, 1, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        painter.setBrush(QBrush(self.color_light))
        # Polygon
        if self.active == True:
            square = QPolygon([
                QPoint(self.width*0.3, self.height*0.8),
                QPoint(self.width*0.7, self.height*0.8),
                QPoint(self.width*0.7, self.height*1.0),
                QPoint(self.width*0.3, self.height*1.0)
                ])
            painter.drawPolygon(square)
        # Finish QPainter
        painter.end()
        self.update()


class Panel_UVD(QWidget):
    SIGNAL_UVD_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_UVD_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_UVD, self).__init__(parent)
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        # Variables
        self.value_x = None
        self.value_y = None
        self.limit_x = None
        self.limit_y = None
        self.angle_input = 0
        self.delta = 1
        self.percentage = None
        # Theme for the Buttons
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # RMB SVG Cursor
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Setup(self, render):
        self.render = render
    def Update_Panel(self, aaa, uuu, vvv, ddd, pcc, p1, p2, p3, p4, p5, p6, p12, p23, p34, p45, p56, p61, width, height, hex, zoom):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Change value range to slider range
        self.aaa = aaa
        self.value_x = 0.5 * ((self.panel_width) + (uuu * self.panel_width))
        self.value_y = 0.5 * ((self.panel_height) + (vvv * self.panel_height))
        self.diagonal = ddd * 3
        # Points
        self.PCC = pcc
        self.P1 = p1
        self.P2 = p2
        self.P3 = p3
        self.P4 = p4
        self.P5 = p5
        self.P6 = p6
        self.P12 = p12
        self.P23 = p23
        self.P34 = p34
        self.P45 = p45
        self.P56 = p56
        self.P61 = p61
        # Move Cursor
        try:
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width()/2), self.value_y-(self.cursor_lmb.height()/2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width()/2), self.value_y-(self.cursor_rmb.height()/2))
        except:
            self.cursor_lmb.move(self.panel_width / 2, self.panel_height / 2)
            self.cursor_rmb.move(self.panel_width / 2, self.panel_height / 2)
        # Zoom
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
        self.cursorzoom(0)
        self.SIGNAL_UVD_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.event_x = event.x()
        self.event_y = event.y()
        self.half_x = self.panel_width / 2
        self.half_y = self.panel_height / 2
        # Angles of Input
        self.angle_input = self.Math_2D_Points_Lines_Angle(self.event_x, self.event_y, self.PCC[0], self.PCC[1], self.PCC[0], -1)
        # Widget Constraint
        if self.diagonal <= 0:
            self.Mouse_Distance_Null()
        elif (self.diagonal > 0 and self.diagonal <= 1):
            # Certain
            if (self.angle_input == 0 or self.angle_input ==360):
                self.Mouse_Distance_Point(self.P61[0], self.P61[1])
            elif self.angle_input == 120:
                self.Mouse_Distance_Point(self.P45[0], self.P45[1])
            elif self.angle_input == 240:
                self.Mouse_Distance_Point(self.P23[0], self.P23[1])
            # Intervals
            elif (self.angle_input > 0 and self.angle_input < 120):
                self.Mouse_Distance_Line(self.P5[0], self.P5[1], self.P6[0], self.P6[1])
            elif (self.angle_input > 120 and self.angle_input < 240):
                self.Mouse_Distance_Line(self.P3[0], self.P3[1], self.P4[0], self.P4[1])
            elif (self.angle_input > 240 and self.angle_input < 360):
                self.Mouse_Distance_Line(self.P1[0], self.P1[1], self.P2[0], self.P2[1])
        elif (self.diagonal > 1 and self.diagonal < 2):
            # Angles
            A1 = self.Math_2D_Points_Lines_Angle(self.P1[0], self.P1[1], self.PCC[0], self.PCC[1], self.PCC[0], -1)
            A2 = self.Math_2D_Points_Lines_Angle(self.P2[0], self.P2[1], self.PCC[0], self.PCC[1], self.PCC[0], -1)
            A3 = self.Math_2D_Points_Lines_Angle(self.P3[0], self.P3[1], self.PCC[0], self.PCC[1], self.PCC[0], -1)
            A4 = self.Math_2D_Points_Lines_Angle(self.P4[0], self.P4[1], self.PCC[0], self.PCC[1], self.PCC[0], -1)
            A5 = self.Math_2D_Points_Lines_Angle(self.P5[0], self.P5[1], self.PCC[0], self.PCC[1], self.PCC[0], -1)
            A6 = self.Math_2D_Points_Lines_Angle(self.P6[0], self.P6[1], self.PCC[0], self.PCC[1], self.PCC[0], -1)
            # Certain
            if self.angle_input == A1:
                self.Mouse_Distance_Point(self.P1[0], self.P1[1])
            elif self.angle_input == A2:
                self.Mouse_Distance_Point(self.P2[0], self.P2[1])
            elif self.angle_input == A3:
                self.Mouse_Distance_Point(self.P3[0], self.P3[1])
            elif self.angle_input == A4:
                self.Mouse_Distance_Point(self.P4[0], self.P4[1])
            elif self.angle_input == A5:
                self.Mouse_Distance_Point(self.P5[0], self.P5[1])
            elif self.angle_input == A6:
                self.Mouse_Distance_Point(self.P6[0], self.P6[1])
            # Intervals
            elif (self.angle_input < A1 and self.angle_input > A2):
                self.Mouse_Distance_Line(self.P1[0], self.P1[1], self.P2[0], self.P2[1])
            elif (self.angle_input < A2 and self.angle_input > A3):
                self.Mouse_Distance_Line(self.P2[0], self.P2[1], self.P3[0], self.P3[1])
            elif (self.angle_input < A3 and self.angle_input > A4):
                self.Mouse_Distance_Line(self.P3[0], self.P3[1], self.P4[0], self.P4[1])
            elif (self.angle_input < A4 and self.angle_input > A5):
                self.Mouse_Distance_Line(self.P4[0], self.P4[1], self.P5[0], self.P5[1])
            elif (self.angle_input < A5 and self.angle_input > A6):
                self.Mouse_Distance_Line(self.P5[0], self.P5[1], self.P6[0], self.P6[1])
            elif (self.angle_input < A6 or self.angle_input > A1):
                self.Mouse_Distance_Line(self.P6[0], self.P6[1], self.P1[0], self.P1[1])
        elif (self.diagonal >= 2 and self.diagonal < 3):
            # Certain
            if self.angle_input == 60:
                self.Mouse_Distance_Point(self.P45[0], self.P45[1])
            elif self.angle_input == 180:
                self.Mouse_Distance_Point(self.P34[0], self.P34[1])
            elif self.angle_input == 300:
                self.Mouse_Distance_Point(self.P12[0], self.P12[1])
            # Intervals
            elif (self.angle_input < 60 or self.angle_input > 300):
                self.Mouse_Distance_Line(self.P1[0], self.P1[1], self.P6[0], self.P6[1])
            elif (self.angle_input > 60 and self.angle_input < 180):
                self.Mouse_Distance_Line(self.P4[0], self.P4[1], self.P5[0], self.P5[1])
            elif (self.angle_input > 180 and self.angle_input < 300):
                self.Mouse_Distance_Line(self.P2[0], self.P2[1], self.P3[0], self.P3[1])
        elif self.diagonal >= 3:
            self.Mouse_Distance_Null()
        # Cursor Value
        self.value_x = self.limit_x - self.half_x
        self.value_y = self.limit_y - self.half_y
        # Correct Cursor
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width()/2), self.value_y-(self.cursor_lmb.height()/2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width()/2), self.value_y-(self.cursor_rmb.height()/2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        # Emit Values
        try:
            values = ["UV", (2 * self.value_x) / self.panel_width, (2 * self.value_y) / self.panel_height, 0]
        except:
            values = ["UV", 0, 0, 0]
        self.SIGNAL_UVD_VALUE.emit(values)
    def cursorzoom(self, zoom):
        if zoom == 1:
            # Scale Cursor for Display
            self.cursor_rmb.resize(self.scale_factor, self.scale_factor) # 60 = max tilt value
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width()/2), self.value_y-(self.cursor_lmb.height()/2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width()/2), self.value_y-(self.cursor_rmb.height()/2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.cursor_rmb.resize(0, 0)
            self.SIGNAL_ZOOM.emit(0)
    def mouseHue(self, event):
        # Delta
        self.delta_x = event.x()
        # Distance to Origin
        self.distance = (self.delta_x - self.origin_x) / self.panel_width
        if self.distance <= -1:
            self.distance = -1
        elif self.distance >= 1:
            self.distance = 1
        # Emit
        values = ["D", 0, 0, self.distance]
        self.SIGNAL_UVD_VALUE.emit(values)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.render == "COLOR":
            # Painter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gradient Variables
            if self.diagonal <= 0:
                # RED
                gradient_red = QLinearGradient(self.P45[0],self.P45[1], self.P12[0],self.P12[1])
                gradient_red.setColorAt(0.0, QColor(0,0,0,255))
                gradient_red.setColorAt(1.0, QColor(0,0,0,0))
                # GREEN
                gradient_green = QLinearGradient(self.P23[0],self.P23[1], self.P56[0],self.P56[1])
                gradient_green.setColorAt(0.0, QColor(0,0,0,255))
                gradient_green.setColorAt(1.0, QColor(0,0,0,0))
                # BLUE
                gradient_blue = QLinearGradient(self.P61[0],self.P61[1], self.P34[0],self.P34[1])
                gradient_blue.setColorAt(0.0, QColor(0,0,0,255))
                gradient_blue.setColorAt(1.0, QColor(0,0,0,0))
            if (self.diagonal > 0 and self.diagonal < 1):
                var = self.diagonal * 255
                # RED
                gradient_red = QLinearGradient(self.P45[0],self.P45[1], self.P12[0],self.P12[1])
                gradient_red.setColorAt(0.0, QColor(var,0,0,255))
                gradient_red.setColorAt(1.0, QColor(0,0,0,255))
                # GREEN
                gradient_green = QLinearGradient(self.P23[0],self.P23[1], self.P56[0],self.P56[1])
                gradient_green.setColorAt(0.0, QColor(0,var,0,255))
                gradient_green.setColorAt(1.0, QColor(0,0,0,255))
                # BLUE
                gradient_blue = QLinearGradient(self.P61[0],self.P61[1], self.P34[0],self.P34[1])
                gradient_blue.setColorAt(0.0, QColor(0,0,var,255))
                gradient_blue.setColorAt(1.0, QColor(0,0,0,255))
            if (self.diagonal >= 1 and self.diagonal <= 2):
                # RED
                gradient_red = QLinearGradient(self.P45[0],self.P45[1], self.P12[0],self.P12[1])
                gradient_red.setColorAt(0.0, QColor(255,0,0,255))
                gradient_red.setColorAt(1.0, QColor(0,0,0,0))
                # GREEN
                gradient_green = QLinearGradient(self.P23[0],self.P23[1], self.P56[0],self.P56[1])
                gradient_green.setColorAt(0.0, QColor(0,255,0,255))
                gradient_green.setColorAt(1.0, QColor(0,0,0,0))
                # BLUE
                gradient_blue = QLinearGradient(self.P61[0],self.P61[1], self.P34[0],self.P34[1])
                gradient_blue.setColorAt(0.0, QColor(0,0,255,255))
                gradient_blue.setColorAt(1.0, QColor(0,0,0,0))
            if (self.diagonal > 2 and self.diagonal < 3):
                var = (self.diagonal-2) * 255
                # RED
                gradient_red = QLinearGradient(self.P45[0],self.P45[1], self.P12[0],self.P12[1])
                gradient_red.setColorAt(0.0, QColor(255,0,0,255))
                gradient_red.setColorAt(1.0, QColor(var,0,0,255))
                # GREEN
                gradient_green = QLinearGradient(self.P23[0],self.P23[1], self.P56[0],self.P56[1])
                gradient_green.setColorAt(0.0, QColor(0,255,0,255))
                gradient_green.setColorAt(1.0, QColor(0,var,0,255))
                # BLUE
                gradient_blue = QLinearGradient(self.P61[0],self.P61[1], self.P34[0],self.P34[1])
                gradient_blue.setColorAt(0.0, QColor(0,0,255,255))
                gradient_blue.setColorAt(1.0, QColor(0,0,var,255))
            if self.diagonal >= 3:
                # RED
                gradient_red = QLinearGradient(self.P45[0],self.P45[1], self.P12[0],self.P12[1])
                gradient_red.setColorAt(0.0, QColor(255,255,255,255))
                gradient_red.setColorAt(1.0, QColor(0,0,0,0))
                # GREEN
                gradient_green = QLinearGradient(self.P23[0],self.P23[1], self.P56[0],self.P56[1])
                gradient_green.setColorAt(0.0, QColor(255,255,255,255))
                gradient_green.setColorAt(1.0, QColor(0,0,0,0))
                # BLUE
                gradient_blue = QLinearGradient(self.P61[0],self.P61[1], self.P34[0],self.P34[1])
                gradient_blue.setColorAt(0.0, QColor(255,255,255,255))
                gradient_blue.setColorAt(1.0, QColor(0,0,0,0))
            # Paint the Gradients
            painter.setBrush(QBrush(QColor(0,0,0)))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            painter.setCompositionMode(QPainter.CompositionMode_Plus)
            painter.setBrush(QBrush(gradient_red))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            painter.setBrush(QBrush(gradient_green))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            painter.setBrush(QBrush(gradient_blue))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # End the Painter
            painter.end()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gray
            painter.setBrush(QBrush(QColor(self.aaa*255, self.aaa*255, self.aaa*255)))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "NONE":
            pass
        self.update()

    # Limits
    def Mouse_Distance_Null(self):
        self.limit_x = self.half_x
        self.limit_y = self.half_y
    def Mouse_Distance_Point(self, x1, y1):
        # Distance of Input
        self.D_input = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.PCC[0], self.PCC[1])
        self.D_intersection = self.Math_2D_Points_Distance(x1, y1, self.PCC[0], self.PCC[1])
        # Distance Limit
        if self.D_input >= self.D_intersection:
            self.limit_x = x1
            self.limit_y = y1
        else:
            self.limit_x = self.event_x
            self.limit_y = self.event_y
    def Mouse_Distance_Line(self, x1, y1, x2, y2):
        # Intersecction of lines
        self.intersection = list(self.Math_2D_Points_Lines_Intersection(self.event_x, self.event_y, self.PCC[0], self.PCC[1],x1, y1, x2, y2))
        # Distance of Input
        self.D_input = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.PCC[0], self.PCC[1])
        self.D_intersection = self.Math_2D_Points_Distance(self.intersection[0], self.intersection[1], self.PCC[0], self.PCC[1])
        # Maintain Percentage (Used in Mouse_Stand_Line)
        self.percentage = self.D_input / self.D_intersection
        # Distance Limit
        if self.D_input >= self.D_intersection:
            self.limit_x = self.intersection[0]
            self.limit_y = self.intersection[1]
        else:
            self.limit_x = self.event_x
            self.limit_y = self.event_y

    # Trignometry
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle


class Panel_ARD(QWidget):
    SIGNAL_ARD_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_ARD_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_ARD, self).__init__(parent)
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        # Variables
        self.value_x = None
        self.value_y = None
        self.limit_x = None
        self.angle_input = 0
        self.delta = 1
        self.origin_x = None
        self.origin_y = None
        self.delta_x = None
        self.delta_y = None
        self.distance = None
        # Theme for the Buttons
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # RMB SVG Cursor
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Setup(self, render):
        self.render = render
    def Update_Panel(self, aaa, hue, rrr, ddd, t1, t2, t3, cross, width, height, hex, zoom):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.half_x = self.panel_width / 3
        self.half_y = self.panel_height / 2
        self.hex = str(hex)
        # Points
        self.T1 = [t1[0]*width, t1[1]*height]
        self.T2 = [t2[0]*width, t2[1]*height]
        self.T3 = [t3[0]*width, t3[1]*height]
        self.cross = cross
        # Change value range to slider range
        self.aaa = aaa
        self.hue = [hue[0], hue[1], hue[2]]
        self.value_x = (rrr * cross[0]) * self.panel_width
        self.value_y = (1 - ddd) * self.panel_height
        self.diagonal = ddd
        self.cross_x = cross[0]
        self.cross_y = cross[1]
        # Move Cursor
        try:
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width()/2), self.value_y-(self.cursor_lmb.height()/2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width()/2), self.value_y-(self.cursor_rmb.height()/2))
        except:
            self.cursor_lmb.move(0, self.panel_height)
            self.cursor_rmb.move(0, self.panel_height)
        # Zoom
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
        self.SIGNAL_ARD_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.event_x = event.x()
        self.event_y = event.y()
        # Cursor Value
        self.value_x = self.event_x
        self.value_y = self.event_y
        # Angles of Input
        self.angle_input = self.Math_2D_Points_Lines_Angle(self.event_x, self.event_y, self.half_x, self.half_y, 0, 0)
        self.angle_T1 = 0
        self.angle_T2 = self.Math_2D_Points_Lines_Angle(self.T2[0], self.T2[1], self.half_x, self.half_y, 0, 0)
        self.angle_T3 = self.Math_2D_Points_Lines_Angle(self.T3[0], self.T3[1], self.half_x, self.half_y, 0, 0)
        # Widget Constraint
        if self.angle_input == self.angle_T1:
            self.Mouse_Distance_Point(self.T1[0], self.T1[1])
        if self.angle_input == self.angle_T2:
            self.Mouse_Distance_Point(self.T2[0], self.T2[1])
        if self.angle_input == self.angle_T3:
            self.Mouse_Distance_Point(self.T3[0], self.T3[1])
        if (self.angle_input < self.angle_T2):
            self.Mouse_Distance_Line(self.T1[0], self.T1[1], self.T2[0], self.T2[1])
        if (self.angle_input > self.angle_T2 and self.angle_input < self.angle_T3):
            self.Mouse_Distance_Line(self.T2[0], self.T2[1], self.T3[0], self.T3[1])
        if (self.angle_input > self.angle_T3):
            self.Mouse_Distance_Line(self.T1[0], self.T1[1], self.T3[0], self.T3[1])
        # Horizontal Triangle Limit
        if self.value_y <= self.T3[1]:
            self.limit_x = list(self.Math_2D_Points_Lines_Intersection(
                0,0,
                self.T3[0],self.T3[1],
                0,self.value_y,
                self.panel_width,self.value_y,
                ))
        if self.value_y > self.T3[1]:
            self.limit_x = list(self.Math_2D_Points_Lines_Intersection(
                self.T2[0],self.T2[1],
                self.T3[0],self.T3[1],
                0,self.value_y,
                self.panel_width,self.value_y,
                ))
        # Correct Cursor
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton or event.type() == QtCore.QEvent.MouseButtonDblClick):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width()/2), self.value_y-(self.cursor_lmb.height()/2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width()/2), self.value_y-(self.cursor_rmb.height()/2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.cursorzoom(0)
            self.SIGNAL_ARD_RELEASE.emit(0)
        # Emit Values
        try:
            values = ["RD", 0, (self.value_x) / self.limit_x[0], 1 - (self.value_y / self.panel_height)]
            if self.value_y == 0:
                values = ["RD", 0, 0, 0]
            elif self.value_y == 1:
                values = ["RD", 0, 0, 1]
        except:
            values = ["RD", 0, 0, 0]
        self.SIGNAL_ARD_VALUE.emit(values)
    def cursorzoom(self, zoom):
        if zoom == 1:
            # Scale Cursor for Display
            self.cursor_rmb.resize(self.scale_factor, self.scale_factor) # 60 = max tilt value
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width()/2), self.value_y-(self.cursor_lmb.height()/2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width()/2), self.value_y-(self.cursor_rmb.height()/2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.cursor_rmb.resize(0, 0)
            self.SIGNAL_ZOOM.emit(0)
    def mouseHue(self, event):
        # Delta
        self.delta_x = event.x()
        # Distance to Origin
        self.distance = (self.delta_x - self.origin_x) / self.panel_width
        if self.distance <= -1:
            self.distance = -1
        elif self.distance >= 1:
            self.distance = 1
        # Emit
        values = ["A", self.distance, 0, 0]
        self.SIGNAL_ARD_VALUE.emit(values)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gradient BW
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)); # White Invisiable
            bw.setColorAt(1.000, QColor(0, 0, 0)); # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Gradient Color
            cor = QLinearGradient(0, 0, self.panel_width, 0)
            cor.setColorAt(0.000, QColor(255, 255, 255, 0)) # White
            cor.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255, 255)) # Color
            painter.setBrush(QBrush(cor))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gray
            painter.setBrush(QBrush(QColor(self.aaa*255, self.aaa*255, self.aaa*255)))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "NONE":
            pass
        self.update()

    # Limits
    def Mouse_Distance_Point(self, x1, y1):
        # Distance of Input
        self.input = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.half_x, self.half_y)
        self.point = self.Math_2D_Points_Distance(x1, y1, self.half_x, self.half_y)
        # Distance Limit
        if self.input >= self.point:
            self.value_x = x1
            self.value_y = y1
        else:
            self.value_x = self.event_x
            self.value_y = self.event_y
    def Mouse_Distance_Line(self, x1, y1, x2, y2):
        # Intersecction of lines
        self.intersection = list(self.Math_2D_Points_Lines_Intersection(self.event_x, self.event_y, self.half_x, self.half_y, x1, y1, x2, y2))
        # Distance of Input
        self.input = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.half_x, self.half_y)
        self.point = self.Math_2D_Points_Distance(self.intersection[0], self.intersection[1], self.half_x, self.half_y)
        # Distance Limit
        if self.input >= self.point:
            self.value_x = self.intersection[0]
            self.value_y = self.intersection[1]
        else:
            self.value_x = self.event_x
            self.value_y = self.event_y
    # Trignometry
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle


class Panel_HSV_4(QWidget):
    SIGNAL_HSV_4_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSV_4_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSV_4, self).__init__(parent)
        # Variables
        self.render = "COLOR"
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # RMB SVG Cursor
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Render(self, render):
        self.render = render
    def Update_Panel(self, aaa, hsv, hue, width, height, hex, zoom):
        # Colors
        self.aaa = aaa
        self.hsv = [hsv[0], hsv[1], hsv[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Change value range to slider range
        self.value_x = self.hsv[1] * self.panel_width
        self.value_y = self.panel_height - (self.hsv[2] * self.panel_height)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Zoom
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
        self.cursorzoom(0)
        self.SIGNAL_HSV_4_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        event_x = event.x()
        event_y = event.y()
        # Limit Position
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
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        # Emit Values
        try:
            list = ["SL", 0, (self.value_x / self.panel_width), ((self.panel_height - self.value_y) / self.panel_height)]
        except:
            list = ["SL", 0, 0, 0]
        self.SIGNAL_HSV_4_VALUE.emit(list)
    def cursorzoom(self, zoom):
        if zoom == 1:
            # Scale Cursor for Display
            self.cursor_rmb.resize(self.scale_factor, self.scale_factor) # 60 = max tilt value
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.cursor_rmb.resize(0, 0)
            self.SIGNAL_ZOOM.emit(0)
    def mouseHue(self, event):
        # Delta
        self.delta_x = event.x()
        # Distance to Origin
        self.distance = (self.delta_x - self.origin_x) / self.panel_width
        if self.distance <= -1:
            self.distance = -1
        elif self.distance >= 1:
            self.distance = 1
        # Emit
        list = ["H", self.distance, 0, 0]
        self.SIGNAL_HSV_4_VALUE.emit(list)

    # Tablet Interaction
    def tabletEvent(self, event):
        self.tabletCursor(event)
    def tabletCursor(self, event):
        if ((event.type() == QtCore.QEvent.TabletPress or event.type() == QtCore.QEvent.TabletMove) and event.PointerType() == 3):
            self.cursorzoom(1)
        elif event.type() == QtCore.QEvent.TabletRelease:
            self.cursorzoom(0)
            self.SIGNAL_HSV_4_RELEASE.emit(0)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gradient Color
            cor = QLinearGradient(0, 0, self.panel_width, 0)
            cor.setColorAt(0.000, QColor(255, 255, 255, 255)) # White
            cor.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255, 255)) # Color
            painter.setBrush(QBrush(cor))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Gradient BW
            painter.setCompositionMode(QPainter.CompositionMode_Multiply)
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)); # White Invisiable
            bw.setColorAt(1.000, QColor(0, 0, 0)); # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gray
            painter.setBrush(QBrush(QColor(self.aaa*255, self.aaa*255, self.aaa*255)))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "NONE":
            pass
        self.update()


class Panel_HSL_3(QWidget):
    SIGNAL_HSL_3_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSL_3_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSL_3, self).__init__(parent)
        # Variables
        self.render = "COLOR"
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # RMB SVG Cursor
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Render(self, render):
        self.render = render
    def Update_Panel(self, aaa, hsl, hue, width, height, hex, zoom):
        # Colors
        self.aaa = aaa
        self.hsl = [hsl[0], hsl[1], hsl[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Change value range to slider range
        self.value_y = self.panel_height - (self.hsl[2] * self.panel_height)
        if self.value_y == self.panel_height*0:
            self.value_x = 0
        if (self.value_y >= self.panel_height*0 and self.value_y <= self.panel_height*0.5):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.value_y, self.panel_width,self.value_y,
                0,0, self.panel_width,self.panel_height/2
                )
            self.value_x = self.hsl[1] * intersection[0]
        if self.value_y == self.panel_height*0.5:
            self.value_x = self.hsl[1] * self.panel_width
        if (self.value_y >= self.panel_height*0.5 and self.value_y <= self.panel_height*1):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.value_y, self.panel_width,self.value_y,
                0,self.panel_height, self.panel_width,self.panel_height/2
                )
            self.value_x = self.hsl[1] * intersection[0]
        if self.value_y == self.panel_height*1:
            self.value_x = 0
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Zoom
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
        self.cursorzoom(0)
        self.SIGNAL_HSL_3_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.value_x = event.x()
        self.value_y = event.y()
        # Consider Triangle
        if self.value_y <= self.panel_height*0:
            distance = 1
            self.value_x = 0
            self.value_y = 0
        if (self.value_y > self.panel_height*0 and self.value_y < self.panel_height*0.5):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.value_y, self.panel_width,self.value_y,
                0,0, self.panel_width,self.panel_height/2
                )
            distance = intersection[0]
            if self.value_x <= 0:
                self.value_x = 0
            if self.value_x >= intersection[0]:
                self.value_x = intersection[0]
        if self.value_y == self.panel_height*0.5:
            distance = self.panel_width
            if self.value_x <= 0:
                self.value_x = 0
            if self.value_x >= self.panel_width:
                self.value_x = self.panel_width
        if (self.value_y > self.panel_height*0.5 and self.value_y < self.panel_height*1):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.value_y, self.panel_width,self.value_y,
                0,self.panel_height, self.panel_width,self.panel_height/2
                )
            distance = intersection[0]
            if self.value_x <= 0:
                self.value_x = 0
            if self.value_x >= intersection[0]:
                self.value_x = intersection[0]
        if self.value_y >= self.panel_height*1:
            distance = 1
            self.value_x = 0
            self.value_y = self.panel_height
        # Correct Cursor
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        if event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        # Emit Values
        try:
            list = ["SL", 0, (self.value_x / distance), ((self.panel_height - self.value_y) / self.panel_height)]
        except:
            list = ["SL", 0, 0, 0]
        self.SIGNAL_HSL_3_VALUE.emit(list)
    def cursorzoom(self, zoom):
        if zoom == 1:
            # Scale Cursor for Display
            self.cursor_rmb.resize(self.scale_factor, self.scale_factor) # 60 = max tilt value
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.cursor_rmb.resize(0, 0)
            self.SIGNAL_ZOOM.emit(0)
    def mouseHue(self, event):
        # Delta
        self.delta_x = event.x()
        # Distance to Origin
        self.distance = (self.delta_x - self.origin_x) / self.panel_width
        if self.distance <= -1:
            self.distance = -1
        elif self.distance >= 1:
            self.distance = 1
        # Emit
        list = ["H", self.distance, 0, 0]
        self.SIGNAL_HSL_3_VALUE.emit(list)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gradient Color
            cor1 = QConicalGradient (QPointF(0, 0), 0)
            cor1.setColorAt(0.750, QColor(127,127,127))
            cor1.setColorAt(0.917, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            painter.setBrush(QBrush(cor1))
            painter.drawRect(0,0, self.panel_width, self.panel_height/2)
            cor2 = QConicalGradient (QPointF(0, self.panel_height), 0)
            cor2.setColorAt(0.083, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor2.setColorAt(0.250, QColor(127,127,127))
            painter.setBrush(QBrush(cor2))
            painter.drawRect(0,self.panel_height/2, self.panel_width, self.panel_height)
            # Gradient BW
            painter.setCompositionMode(QPainter.CompositionMode_HardLight)
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gray
            painter.setBrush(QBrush(QColor(self.aaa*255, self.aaa*255, self.aaa*255)))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "NONE":
            pass
        self.update()

    # Trignometry
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle
class Panel_HSL_4(QWidget):
    SIGNAL_HSL_4_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSL_4_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSL_4, self).__init__(parent)
        # Variables
        self.render = "COLOR"
        # Start
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # RMB SVG Cursor
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Render(self, render):
        self.render = render
    def Update_Panel(self, aaa, hsl, hue, width, height, hex, zoom):
        # Colors
        self.aaa = aaa
        self.hsl = [hsl[0], hsl[1], hsl[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Change value range to slider range
        self.value_x = self.hsl[1] * self.panel_width
        self.value_y = self.panel_height - (self.hsl[2] * self.panel_height)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Zoom
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
        self.cursorzoom(0)
        self.SIGNAL_HSL_4_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        event_x = event.x()
        event_y = event.y()
        # Limit Position
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
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        if event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        # Emit Values
        try:
            list = ["SL", 0, (self.value_x / self.panel_width), ((self.panel_height - self.value_y) / self.panel_height)]
        except:
            list = ["SL", 0, 0, 0]
        self.SIGNAL_HSL_4_VALUE.emit(list)
    def cursorzoom(self, zoom):
        if zoom == 1:
            # Scale Cursor for Display
            self.cursor_rmb.resize(self.scale_factor, self.scale_factor) # 60 = max tilt value
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.cursor_rmb.resize(0, 0)
            self.SIGNAL_ZOOM.emit(0)
    def mouseHue(self, event):
        # Delta
        self.delta_x = event.x()
        # Distance to Origin
        self.distance = (self.delta_x - self.origin_x) / self.panel_width
        if self.distance <= -1:
            self.distance = -1
        elif self.distance >= 1:
            self.distance = 1
        # Emit
        list = ["H", self.distance, 0, 0]
        self.SIGNAL_HSL_4_VALUE.emit(list)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gradient BW
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Color
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Gradient COLOR
            painter.setCompositionMode(QPainter.CompositionMode_Overlay)
            cor = QLinearGradient(0, 0, self.panel_width, 0)
            cor.setColorAt(0.000, QColor(0, 0, 0, 0)) # White Invisiable
            cor.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255, 255)) # Black
            painter.setBrush(QBrush(cor))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gray
            painter.setBrush(QBrush(QColor(self.aaa*255, self.aaa*255, self.aaa*255)))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "NONE":
            pass
        self.update()
class Panel_HSL_4D(QWidget):
    SIGNAL_HSL_4D_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSL_4D_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSL_4D, self).__init__(parent)
        # Module Style
        self.style = Style()
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Variables(self):
        # Variables
        self.hex = '#000000'
        self.render = "COLOR"
        self.angle = 0
        self.circle_x = 0
        self.circle_y = 0
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
        self.margin = 5
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Cursor(self):
        # Variables
        self.hex = '#000000'
        # Module Style
        self.style = Style()
        # LMB SVG Cursor
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        # RMB SVG Cursor
        self.cursor_rmb = QtSvg.QSvgWidget(self)
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Style SVG Cursors
        self.cursor_size = 20
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_rmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        self.cursor_rmb.setStyleSheet(self.unseen)
        # Cursor Scale
        self.scale_factor = 180

    # Relay
    def Render(self, render):
        self.render = render
    def Update_Panel(self, aaa, hsl, hue, width, height, hex, zoom):
        # Colors
        self.aaa = aaa
        self.hsl = [hsl[0], hsl[1], hsl[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Change value range to slider range
        if self.hsl[2] <= 0:
            self.value_x = self.panel_width/2
            self.value_y = self.panel_height
        if (self.hsl[2] > 0 and self.hsl[2] < 0.5):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.hsl[2]*self.panel_height, self.panel_width,self.hsl[2]*self.panel_height,
                0,self.panel_height/2, self.panel_width/2,0)
            distance = self.panel_width - (2*intersection[0])
            self.value_x = intersection[0] + (self.hsl[1] * distance)
            self.value_y = self.panel_height - (self.hsl[2] * self.panel_height)
        if self.hsl[2] == 0.5:
            self.value_x = self.hsl[1] * self.panel_width
            self.value_y = self.panel_height/2
        if (self.hsl[2] > 0.5 and self.hsl[2] < 1):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.hsl[2]*self.panel_height, self.panel_width,self.hsl[2]*self.panel_height,
                0,self.panel_height/2, self.panel_width/2,self.panel_height)
            distance = self.panel_width - (2*intersection[0])
            self.value_x = intersection[0] + (self.hsl[1] * distance)
            self.value_y = self.panel_height - (self.hsl[2] * self.panel_height)
        if self.hsl[2] >= 1:
            self.value_x = self.panel_width/2
            self.value_y = 0
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Zoom
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.mouseHue(event)
        else:
            self.mouseCursor(event)
        self.cursorzoom(0)
        self.SIGNAL_HSL_4D_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Position
        if self.value_y <= self.panel_height*0:
            self.value_x = self.panel_width/2
            self.value_y = 0
            list = ["SL", 0, 0, 1]
        if (self.value_y > self.panel_height*0 and self.value_y < self.panel_height*0.5):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.value_y, self.panel_width,self.value_y,
                0,self.panel_height/2, self.panel_width/2,0)
            distance = self.panel_width - (2*intersection[0])
            if self.value_x <= intersection[0]:
                self.value_x = intersection[0]
            if self.value_x >= (self.panel_width-intersection[0]):
                self.value_x = (self.panel_width-intersection[0])
            list = ["SL", 0, ((self.value_x - intersection[0]) / distance), ((self.panel_height - self.value_y) / self.panel_height)]
        if self.value_y == self.panel_height*0.5:
            distance = self.panel_width
            if self.value_x <= 0:
                self.value_x = 0
            if self.value_x >= self.panel_width:
                self.value_x = self.panel_width
            list = ["SL", 0, (self.value_x / distance), ((self.panel_height - self.value_y) / self.panel_height)]
        if (self.value_y > self.panel_height*0.5 and self.value_y < self.panel_height*1):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,self.value_y, self.panel_width,self.value_y,
                0,self.panel_height/2, self.panel_width/2,self.panel_height)
            distance = self.panel_width - (2*intersection[0])
            if self.value_x <= intersection[0]:
                self.value_x = intersection[0]
            if self.value_x >= (self.panel_width-intersection[0]):
                self.value_x = (self.panel_width-intersection[0])
            list = ["SL", 0, ((self.value_x - intersection[0]) / distance), ((self.panel_height - self.value_y) / self.panel_height)]
        if self.value_y >= self.panel_height*1:
            self.value_x = self.panel_width/2
            self.value_y = self.panel_height
            list = ["SL", 0, 0, 0]
        # Correct Cursor
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        # Emit Values
        self.SIGNAL_HSL_4D_VALUE.emit(list)
    def cursorzoom(self, zoom):
        if zoom == 1:
            # Scale Cursor for Display
            self.cursor_rmb.resize(self.scale_factor, self.scale_factor) # 60 = max tilt value
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
            self.SIGNAL_ZOOM.emit(1)
        else:
            self.cursor_rmb.resize(0, 0)
            self.SIGNAL_ZOOM.emit(0)
    def mouseHue(self, event):
        # Delta
        self.delta_x = event.x()
        # Distance to Origin
        self.distance = (self.delta_x - self.origin_x) / self.panel_width
        if self.distance <= -1:
            self.distance = -1
        elif self.distance >= 1:
            self.distance = 1
        # Emit
        list = ["H", self.distance, 0, 0]
        self.SIGNAL_HSL_4D_VALUE.emit(list)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gradient Color 1
            cor1 = QConicalGradient (QPointF(self.panel_width/2, 0), 225)
            cor1.setColorAt(0.000, QColor(127,127,127))
            cor1.setColorAt(0.250, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            painter.setBrush(QBrush(cor1))
            painter.drawRect(0,0, self.panel_width, self.panel_height/2)
            # Gradient Color 2
            cor2 = QConicalGradient (QPointF(self.panel_width/2, self.panel_height), 45)
            cor2.setColorAt(0.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor2.setColorAt(0.250, QColor(127,127,127))
            cor2.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            painter.setBrush(QBrush(cor2))
            painter.drawRect(0,self.panel_height/2, self.panel_width, self.panel_height)
            # Gradient BW
            painter.setCompositionMode(QPainter.CompositionMode_HardLight)
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Gray
            painter.setBrush(QBrush(QColor(self.aaa*255, self.aaa*255, self.aaa*255)))
            painter.drawRect(0,0, self.panel_width, self.panel_height)
            # Finish QPainter
            painter.end()
        if self.render == "NONE":
            pass
        self.update()

    # Trignometry
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle


class Panel_HUE_Circle(QWidget):
    SIGNAL_HUE_C_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HUE_C_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_HUE_C_HARMONY_ACTIVE = QtCore.pyqtSignal(int)
    SIGNAL_HUE_C_HARMONY_DELTA = QtCore.pyqtSignal(list)

    # Init
    def __init__(self, parent):
        super(Panel_HUE_Circle, self).__init__(parent)
        # Module Style
        self.style = Style()
        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Variables(self):
        # Variables
        self.hex = '#000000'
        self.render = "COLOR"
        self.angle = 0
        self.circle_x = 0
        self.circle_y = 0
        self.color_dark = QColor('#383838')
        self.color_gray = QColor('#666666')
        self.harmony = "COLOR"
        self.line_1 = 5
        self.line_2 = 12
        # Angle
        self.har_radius = 0.5
        self.har_radius_poly = 0.5 - ( 2 * 0.035 )
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)

    # Relay
    def Render(self, render):
        self.render = render
    def Harmony(self, harmony_index):
        self.harmony_index = harmony_index
    def Active(self, harmony_active):
        self.harmony_active = harmony_active

    # Update Normal
    def Update_Panel(self, angle, hue, width, height, gray_natural, gray_contrast):
        # Color
        self.angle = angle * 360  # Angle of Color
        self.hue = [hue[0], hue[1], hue[2]]  # Pure Hue Color
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        # Location in XY
        self.radius = 0.50
        try:
            self.circle_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(self.angle)))
            self.circle_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(self.angle)))
        except:
            self.circle_x = 0
            self.circle_y = 0
        self.event_x = self.circle_x
        self.event_y = self.circle_y
    # Update Harmony
    def Update_Harmony_1(self, angle, color, width, height, gray_natural, gray_contrast):
        # Hue Color in RGB
        self.h1_angle = angle * 360
        self.h1_hue = [color[0], color[1], color[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        try:
            self.h1_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius) * math.cos(math.radians(self.h1_angle)))
            self.h1_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius) * math.sin(math.radians(self.h1_angle)))
            self.h1p_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius_poly) * math.cos(math.radians(self.h1_angle)))
            self.h1p_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius_poly) * math.sin(math.radians(self.h1_angle)))
        except:
            self.h1_circle_x = 0
            self.h1_circle_y = 0
            self.h1p_circle_x = 0
            self.h1p_circle_y = 0
        self.h1_event_x = self.h1_circle_x
        self.h1_event_y = self.h1_circle_y
    def Update_Harmony_2(self, angle, color, width, height, gray_natural, gray_contrast):
        # Hue Color in RGB
        self.h2_angle = angle * 360
        self.h2_hue = [color[0], color[1], color[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        try:
            self.h2_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius) * math.cos(math.radians(self.h2_angle)))
            self.h2_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius) * math.sin(math.radians(self.h2_angle)))
            self.h2p_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius_poly) * math.cos(math.radians(self.h2_angle)))
            self.h2p_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius_poly) * math.sin(math.radians(self.h2_angle)))
        except:
            self.h2_circle_x = 0
            self.h2_circle_y = 0
            self.h2p_circle_x = 0
            self.h2p_circle_y = 0
        self.h2_event_x = self.h2_circle_x
        self.h2_event_y = self.h2_circle_y
    def Update_Harmony_3(self, angle, color, width, height, gray_natural, gray_contrast):
        # Hue Color in RGB
        self.h3_angle = angle * 360
        self.h3_hue = [color[0], color[1], color[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        try:
            self.h3_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius) * math.cos(math.radians(self.h3_angle)))
            self.h3_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius) * math.sin(math.radians(self.h3_angle)))
            self.h3p_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius_poly) * math.cos(math.radians(self.h3_angle)))
            self.h3p_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius_poly) * math.sin(math.radians(self.h3_angle)))
        except:
            self.h3_circle_x = 0
            self.h3_circle_y = 0
            self.h3p_circle_x = 0
            self.h3p_circle_y = 0
        self.h3_event_x = self.h3_circle_x
        self.h3_event_y = self.h3_circle_y
    def Update_Harmony_4(self, angle, color, width, height, gray_natural, gray_contrast):
        # Hue Color in RGB
        self.h4_angle = angle * 360
        self.h4_hue = [color[0], color[1], color[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        try:
            self.h4_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius) * math.cos(math.radians(self.h4_angle)))
            self.h4_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius) * math.sin(math.radians(self.h4_angle)))
            self.h4p_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius_poly) * math.cos(math.radians(self.h4_angle)))
            self.h4p_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius_poly) * math.sin(math.radians(self.h4_angle)))
        except:
            self.h4_circle_x = 0
            self.h4_circle_y = 0
            self.h4p_circle_x = 0
            self.h4p_circle_y = 0
        self.h4_event_x = self.h4_circle_x
        self.h4_event_y = self.h4_circle_y
    def Update_Harmony_5(self, angle, color, width, height, gray_natural, gray_contrast):
        # Hue Color in RGB
        self.h5_angle = angle * 360
        self.h5_hue = [color[0], color[1], color[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        try:
            self.h5_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius) * math.cos(math.radians(self.h5_angle)))
            self.h5_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius) * math.sin(math.radians(self.h5_angle)))
            self.h5p_circle_x = (self.panel_width*0.5) - ((self.panel_width*self.har_radius_poly) * math.cos(math.radians(self.h5_angle)))
            self.h5p_circle_y = (self.panel_height*0.5) - ((self.panel_height*self.har_radius_poly) * math.sin(math.radians(self.h5_angle)))
        except:
            self.h5_circle_x = 0
            self.h5_circle_y = 0
            self.h5p_circle_x = 0
            self.h5p_circle_y = 0
        self.h5_event_x = self.h5_circle_x
        self.h5_event_y = self.h5_circle_y

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.CloserTo(event)
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.mouseCursor(event)
        self.SIGNAL_HUE_C_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Circle Values
        self.event_x = event.x()
        self.event_y = self.panel_height - event.y()
        self.angle = self.Math_2D_Points_Lines_Angle(
            self.event_x, self.event_y,
            self.panel_width/2,self.panel_height/2,
            0,self.panel_height/2)
        self.radius = 0.465
        self.circle_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(self.angle)))
        self.circle_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(self.angle)))
        # Emit Values
        list = [self.angle/360]
        self.SIGNAL_HUE_C_VALUE.emit(list)
    def CloserTo(self, event):
        if self.render == "HARMONY":
            if self.harmony_index == "Monochromatic":
                # Calculate Distances
                h3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h3_event_x,self.h3_event_y)
                # Confirm to whom it belongs and Emit Signal
                self.harmony_active = 3
                self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(3)
            if self.harmony_index == "Complemantary":
                # Calculate Distances
                h3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h3_event_x,self.h3_event_y)
                h5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h5_event_x,self.h5_event_y)
                # Verify what is the closest Value
                min_dist = min(h3, h5)
                if min_dist < 50:
                    # Confirm to whom it belongs and Emit Signal
                    if min_dist == h5:
                        self.harmony_active = 5
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(5)
                    if min_dist == h3:
                        self.harmony_active = 3
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(3)
            if self.harmony_index == "Analogous":
                # Calculate Distances
                h1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h1_event_x,self.h1_event_y)
                h2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h2_event_x,self.h2_event_y)
                h3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h3_event_x,self.h3_event_y)
                h4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h4_event_x,self.h4_event_y)
                h5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h5_event_x,self.h5_event_y)
                # Verify what is the closest Value
                min_dist = min(h1, h2, h3, h4, h5)
                if min_dist < 50:
                    # Confirm to whom it belongs and Emit Signal
                    if min_dist == h1:
                        self.harmony_active = 1
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(1)
                    if min_dist == h5:
                        self.harmony_active = 5
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(5)
                    if min_dist == h2:
                        self.harmony_active = 2
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(2)
                    if min_dist == h4:
                        self.harmony_active = 4
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(4)
                    if min_dist == h3:
                        self.harmony_active = 3
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(3)
            if self.harmony_index == "Split Complemantary":
                # Calculate Distances
                h1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h1_event_x,self.h1_event_y)
                h3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h3_event_x,self.h3_event_y)
                h5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h5_event_x,self.h5_event_y)
                # Verify what is the closest Value
                min_dist = min(h1, h3, h5)
                if min_dist < 50:
                    # Confirm to whom it belongs and Emit Signal
                    if min_dist == h1:
                        self.harmony_active = 1
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(1)
                    if min_dist == h5:
                        self.harmony_active = 5
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(5)
                    if min_dist == h3:
                        self.harmony_active = 3
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(3)
            if self.harmony_index == "Double Split Complemantary":
                # Calculate Distances
                h1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h1_event_x,self.h1_event_y)
                h2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h2_event_x,self.h2_event_y)
                h3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h3_event_x,self.h3_event_y)
                h4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h4_event_x,self.h4_event_y)
                h5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h5_event_x,self.h5_event_y)
                # Verify what is the closest Value
                min_dist = min(h1, h2, h3, h4, h5)
                if min_dist < 50:
                    # Confirm to whom it belongs and Emit Signal
                    if min_dist == h1:
                        self.harmony_active = 1
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(1)
                    if min_dist == h5:
                        self.harmony_active = 5
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(5)
                    if min_dist == h2:
                        self.harmony_active = 2
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(2)
                    if min_dist == h4:
                        self.harmony_active = 4
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(4)
                    if min_dist == h3:
                        self.harmony_active = 3
                        self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(3)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
        self.update()
    def drawColors(self, event):
        if self.render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            # Regions
            region0 = QRegion(0,0, self.panel_width,self.panel_height) # Everything
            value1a = 0.068
            value1b = 1 - (2*value1a)
            region1 = QRegion(self.panel_width*value1a,self.panel_height*value1a, self.panel_width*value1b,self.panel_height*value1b, QRegion.Ellipse) # Inner Most Region
            value2a = 0.03
            value2b = 1 - (2*value2a)
            region2 = QRegion(self.panel_width*value2a,self.panel_height*value2a, self.panel_width*value2b,self.panel_height*value2b, QRegion.Ellipse) # Outter Most Region
            value3a = 0.35
            value3b = 1 - (2*value3a)
            region3 = QRegion(self.panel_width*value3a,self.panel_height*value3a, self.panel_width*value3b,self.panel_height*value3b, QRegion.Ellipse)
            # Dark Border
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            region01 = region0.subtracted(region1)
            painter.setClipRegion(region01)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Gray
            painter.setPen(QPen(QColor(self.gray_contrast), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            region23 = region2.subtracted(region3)
            painter.setClipRegion(region23)
            painter.drawLine(self.circle_x,self.circle_y, self.panel_width*0.5,self.panel_height*0.5)
            # Hue Gradient
            painter.setPen(QtCore.Qt.NoPen)
            hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 240)
            hue.setColorAt(0.000, QColor(255, 0, 255)) # MAGENTA
            hue.setColorAt(0.166, QColor(0, 0, 255)) # BLUE
            hue.setColorAt(0.333, QColor(0, 255, 255)) # CYAN
            hue.setColorAt(0.500, QColor(0, 255, 0)) # GREEN
            hue.setColorAt(0.666, QColor(255, 255, 0)) # YELLOW
            hue.setColorAt(0.833, QColor(255, 0, 0)) # RED
            hue.setColorAt(1.000, QColor(255, 0, 255)) # MAGENTA
            painter.setBrush(QBrush(hue))
            region04 = region0.subtracted(region2)
            painter.setClipRegion(region04)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Dark over Hue
            painter.setPen(QPen(QColor(self.gray_natural), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            region04 = region0.subtracted(region2)
            painter.setClipRegion(region04)
            painter.drawLine(self.circle_x,self.circle_y, self.panel_width*0.5,self.panel_height*0.5)
            # Finish QPainter
            painter.end()
            self.update()
        if self.render == "GRAY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            # Regions
            region0 = QRegion(0,0, self.panel_width,self.panel_height) # Everything
            value1a = 0.068
            value1b = 1 - (2*value1a)
            region1 = QRegion(self.panel_width*value1a,self.panel_height*value1a, self.panel_width*value1b,self.panel_height*value1b, QRegion.Ellipse) # Inner Most Region
            value2a = 0.03
            value2b = 1 - (2*value2a)
            region2 = QRegion(self.panel_width*value2a,self.panel_height*value2a, self.panel_width*value2b,self.panel_height*value2b, QRegion.Ellipse) # Outter Most Region
            value3a = 0.35
            value3b = 1 - (2*value3a)
            region3 = QRegion(self.panel_width*value3a,self.panel_height*value3a, self.panel_width*value3b,self.panel_height*value3b, QRegion.Ellipse)
            # Dark Border
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            region01 = region0.subtracted(region1)
            painter.setClipRegion(region01)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Gray
            painter.setPen(QPen(QColor(self.gray_contrast), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            region23 = region2.subtracted(region3)
            painter.setClipRegion(region23)
            painter.drawLine(self.circle_x,self.circle_y, self.panel_width*0.5,self.panel_height*0.5)
            # Hue Gradient
            painter.setPen(QtCore.Qt.NoPen)
            hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 240)
            hue.setColorAt(0.000, QColor(163, 163, 163)) # MAGENTA
            hue.setColorAt(0.166, QColor(86, 86, 86)) # BLUE
            hue.setColorAt(0.333, QColor(213, 213, 213)) # CYAN
            hue.setColorAt(0.500, QColor(195, 195, 195)) # GREEN
            hue.setColorAt(0.666, QColor(240, 240, 240)) # YELLOW
            hue.setColorAt(0.833, QColor(139, 139, 139)) # RED
            hue.setColorAt(1.000, QColor(163, 163, 163)) # MAGENTA
            painter.setBrush(QBrush(hue))
            region04 = region0.subtracted(region2)
            painter.setClipRegion(region04)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Dark over Hue
            painter.setPen(QPen(QColor(self.gray_natural), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            region04 = region0.subtracted(region2)
            painter.setClipRegion(region04)
            painter.drawLine(self.circle_x,self.circle_y, self.panel_width*0.5,self.panel_height*0.5)
            # Finish QPainter
            painter.end()
            self.update()
        if self.render == "NONE":
            pass
        if self.render == "HARMONY":
            # Start Qpainter
            painter = QPainter(self)
            painter.begin(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            # Regions
            region0 = QRegion(0,0, self.panel_width,self.panel_height) # Everything
            value1a = 0.03
            value1b = 1 - (2*value1a)
            region1 = QRegion(self.panel_width*value1a,self.panel_height*value1a, self.panel_width*value1b,self.panel_height*value1b, QRegion.Ellipse) # Outter Most Region
            value2a = 0.068
            value2b = 1 - (2*value2a)
            region2 = QRegion(self.panel_width*value2a,self.panel_height*value2a, self.panel_width*value2b,self.panel_height*value2b, QRegion.Ellipse) # Inner Most Region
            value3a = 0.35
            value3b = 1 - (2*value3a)
            region3 = QRegion(self.panel_width*value3a,self.panel_height*value3a, self.panel_width*value3b,self.panel_height*value3b, QRegion.Ellipse) # Central Dot

            # Harmony Gray SPAN Area
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            # Considering the Harmony set Choosen
            if (self.harmony_index == "Monochromatic" or self.harmony_index == "Complemantary" or self.harmony_index == "Analogous"):
                # Start Angle (PyQt5 Angle Space)
                pie_angle_5 = 180 - self.h5_angle
                if pie_angle_5 < 0:
                    pie_angle_5 = pie_angle_5 + 360
                if pie_angle_5 > 360:
                    pie_angle_5 = pie_angle_5 - 360
                # Span Angle (Pigmento Angle Space)
                if self.h5_angle < self.h1_angle:
                    span_angle = self.h5_angle + (360 - self.h1_angle)
                else:
                    span_angle = self.h5_angle - self.h1_angle
                # Draw Pie Shape
                painter.drawPie(0,0, self.panel_width,self.panel_height, pie_angle_5*16, span_angle*16)
                # Polygon
                polygon = QPolygon([
                    QPoint(0, 0),
                    QPoint(0, 0),
                    QPoint(0, 0)
                    ])
                painter.drawPolygon(polygon)
            if self.harmony_index == "Split Complemantary":
                # Triangle
                polygon = QPolygon([
                    QPoint(self.h1p_circle_x, self.h1p_circle_y),
                    QPoint(self.h3p_circle_x, self.h3p_circle_y),
                    QPoint(self.h5p_circle_x, self.h5p_circle_y)
                    ])
                painter.drawPolygon(polygon)
            if self.harmony_index == "Double Split Complemantary":
                # Square
                polygon = QPolygon([
                    QPoint(self.h1p_circle_x, self.h1p_circle_y),
                    QPoint(self.h2p_circle_x, self.h2p_circle_y),
                    QPoint(self.h4p_circle_x, self.h4p_circle_y),
                    QPoint(self.h5p_circle_x, self.h5p_circle_y)
                    ])
                painter.drawPolygon(polygon)

            # Dark Border
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            region02 = region0.subtracted(region2)
            painter.setClipRegion(region02)
            painter.drawRect(0,0, self.panel_width,self.panel_height)

            # Line Gray
            painter.setBrush(QBrush(QColor(self.gray_contrast)))
            region23 = region2.subtracted(region3)
            painter.setClipRegion(region23)

            painter.setPen(QPen(QColor(self.gray_contrast), 4, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h1_circle_x,self.h1_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.setPen(QPen(QColor(self.gray_contrast), 4, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h5_circle_x,self.h5_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            painter.setPen(QPen(QColor(self.gray_contrast), 4, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h2_circle_x,self.h2_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.setPen(QPen(QColor(self.gray_contrast), 4, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h4_circle_x,self.h4_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            painter.setPen(QPen(QColor(self.gray_contrast), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h3_circle_x,self.h3_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            # Hue Gradient
            painter.setPen(QtCore.Qt.NoPen)
            hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 240)
            hue.setColorAt(0.000, QColor(255, 0, 255)) # MAGENTA
            hue.setColorAt(0.166, QColor(0, 0, 255)) # BLUE
            hue.setColorAt(0.333, QColor(0, 255, 255)) # CYAN
            hue.setColorAt(0.500, QColor(0, 255, 0)) # GREEN
            hue.setColorAt(0.666, QColor(255, 255, 0)) # YELLOW
            hue.setColorAt(0.833, QColor(255, 0, 0)) # RED
            hue.setColorAt(1.000, QColor(255, 0, 255)) # MAGENTA
            painter.setBrush(QBrush(hue))
            region01 = region0.subtracted(region1)
            painter.setClipRegion(region01)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Dark over Hue
            region01 = region0.subtracted(region1)
            painter.setClipRegion(region01)
            painter.setPen(QPen(QColor(self.gray_natural), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))

            painter.drawLine(self.h1_circle_x,self.h1_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.h2_circle_x,self.h2_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.h3_circle_x,self.h3_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.h4_circle_x,self.h4_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.h5_circle_x,self.h5_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            # Harmony Color Edit over Dark Stripe
            region12 = region1.subtracted(region2)
            painter.setClipRegion(region12)

            painter.setPen(QPen(QColor(self.h1_hue[0]*255, self.h1_hue[1]*255, self.h1_hue[2]*255), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h1_circle_x,self.h1_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.setPen(QPen(QColor(self.h5_hue[0]*255, self.h5_hue[1]*255, self.h5_hue[2]*255), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h5_circle_x,self.h5_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            painter.setPen(QPen(QColor(self.h2_hue[0]*255, self.h2_hue[1]*255, self.h2_hue[2]*255), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h2_circle_x,self.h2_circle_y, self.panel_width*0.5,self.panel_height*0.5)
            painter.setPen(QPen(QColor(self.h4_hue[0]*255, self.h4_hue[1]*255, self.h4_hue[2]*255), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h4_circle_x,self.h4_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            painter.setPen(QPen(QColor(self.h3_hue[0]*255, self.h3_hue[1]*255, self.h3_hue[2]*255), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.h3_circle_x,self.h3_circle_y, self.panel_width*0.5,self.panel_height*0.5)

            # Finish QPainter
            painter.end()
            self.update()

    # Trignometry
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle


class Panel_DOT(QWidget):
    # works in 0-255 color range
    SIGNAL_DOT_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_DOT_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_DOT_LOCATION = QtCore.pyqtSignal(list)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_DOT, self).__init__(parent)
        self.Variables()
    def sizeHint(self):
        return QtCore.QSize(5000,5000)
    def Variables(self):
        # Variables
        self.value_x = 0
        self.value_y = 0
        self.panel_width = 0
        self.panel_height = 0
        self.cursor_size = 20
        # SVG Cursor
        self.style = Style()
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_lmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)
        # Dots
        self.size = 15
        self.margin = 5
        self.max_colors = 20
        self.max_white = 10
        self.max_black = 10

    # Relay
    def Location(self, location_x, location_y, width, height):
        # Input
        self.value_x = (width*0.5) + location_x
        self.value_y = (height*0.5) + location_y
        self.panel_width = width
        self.panel_height = height
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))
        self.update()
    def Update_Panel(self, dot_1, dot_2, dot_3, dot_4, width, height):
        # Dot Colors
        self.dot_1 = [dot_1[0], dot_1[1]*255, dot_1[2]*255, dot_1[3]*255]
        self.dot_2 = [dot_2[0], dot_2[1]*255, dot_2[2]*255, dot_2[3]*255]
        self.dot_3 = [dot_3[0], dot_3[1]*255, dot_3[2]*255, dot_3[3]*255]
        self.dot_4 = [dot_4[0], dot_4[1]*255, dot_4[2]*255, dot_4[3]*255]
        # Panel Size
        self.panel_width = width
        self.panel_height = height
    def Reset(self):
        self.cursor_lmb.resize(0, 0)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.scale = 0
        self.mouseSelect(event)
    def mouseMoveEvent(self, event):
        self.scale = 0
        self.mouseSelect(event)
    def mouseDoubleClickEvent(self, event):
        self.scale = 0
        self.mouseSelect(event)
    def mouseReleaseEvent(self, event):
        self.scale = 20
        self.mouseSelect(event)
        self.SIGNAL_DOT_RELEASE.emit(0)

    def mouseSelect(self, event):
        # Event
        self.value_x = event.x()
        self.value_y = event.y()
        # Mouse Position
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))
        self.cursor_lmb.resize(self.scale, self.scale)
        # Emit values
        self.SIGNAL_DOT_VALUE.emit([self.value_x, self.value_y])
        self.SIGNAL_DOT_LOCATION.emit([self.value_x - (self.panel_width*0.5), self.value_y - (self.panel_height*0.5)])

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # Clipping Mask
        region0 = QRegion(0,0, self.panel_width,self.panel_height) # Everything
        painter.setClipRegion(region0)
        # Circle
        painter.setPen(QtCore.Qt.NoPen)
        origin_x = (self.panel_width * 0.5) - (((self.max_colors+1) * self.size) + ((self.max_colors) * self.margin)) * 0.5
        origin_y = (self.panel_height * 0.5) - (((self.max_colors+1) * self.size) + ((self.max_colors) * self.margin)) * 0.5

        for i in range(self.max_colors+1):
            rgb = self.Color_Transform(i, self.max_colors, [self.dot_1[1], self.dot_1[2], self.dot_1[3]], [self.dot_2[1], self.dot_2[2], self.dot_2[3]])
            painter.setBrush(QBrush(QColor(rgb[0], rgb[1], rgb[2])))
            point_x = origin_x + (i*self.size + i*self.margin)
            point_y = (self.panel_height*0.5 - self.size*0.5)
            painter.drawRect(point_x,point_y, self.size,self.size)
            # Black
            for b in range(1, self.max_black+1):
                black = self.Color_Transform(b, self.max_black, [rgb[0], rgb[1], rgb[2]], [self.dot_3[1], self.dot_3[2], self.dot_3[3]])
                painter.setBrush(QBrush(QColor(black[0], black[1], black[2])))
                black_y = point_y + (b*self.size + b*self.margin)
                painter.drawRect(point_x,black_y, self.size,self.size)
            # White
            for w in range(1, self.max_white+1):
                white = self.Color_Transform(w, self.max_white, [rgb[0], rgb[1], rgb[2]], [self.dot_4[1], self.dot_4[2], self.dot_4[3]])
                painter.setBrush(QBrush(QColor(white[0], white[1], white[2])))
                white_y = point_y - (w*self.size + w*self.margin)
                painter.drawRect(point_x,white_y, self.size,self.size)

        # Finish QPainter
        painter.end()
        self.update()
    def Color_Transform(self, i, max, color_left, color_right):
        # Red
        if color_left[0] < color_right[0]:
            unit_r = (color_right[0] - color_left[0]) / max
            red = color_left[0] + (i*unit_r)
        elif color_left[0] >= color_right[0]:
            unit_r = (color_left[0] - color_right[0]) / max
            red = color_left[0] - (i*unit_r)
        # Green
        if color_left[1] < color_right[1]:
            unit_g = (color_right[1] - color_left[1]) / max
            green = color_left[1] + (i*unit_g)
        elif color_left[1] >= color_right[1]:
            unit_g = (color_left[1] - color_right[1]) / max
            green = color_left[1] - (i*unit_g)
        # Blue
        if color_left[2] < color_right[2]:
            unit_b = (color_right[2] - color_left[2]) / max
            blue = color_left[2] + (i*unit_b)
        elif color_left[2] >= color_right[2]:
            unit_b = (color_left[2] - color_right[2]) / max
            blue = color_left[2] - (i*unit_b)

        # Return StyleSheet String
        return [red, green, blue]


class Panel_OBJ(QWidget):
    SIGNAL_OBJ_PRESS = QtCore.pyqtSignal(list)
    SIGNAL_OBJ_RELEASE = QtCore.pyqtSignal(list)
    SIGNAL_OBJ_LOCATION = QtCore.pyqtSignal(list)

    # Init
    def __init__(self, parent):
        super(Panel_OBJ, self).__init__(parent)

        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000,5000)
    def Variables(self):
        # Variables
        self.value_x = 0
        self.value_y = 0
        self.panel_width = 0
        self.panel_height = 0
        self.cursor_size = 20
        # SVG Cursor
        self.style = Style()
        self.cursor_lmb = QtSvg.QSvgWidget(self)
        self.array_lmb = self.style.SVG_Cursor_LMB()
        self.cursor_lmb.load(self.array_lmb)
        self.cursor_half = self.cursor_size / 2
        self.cursor_lmb.setGeometry(QtCore.QRect(-self.cursor_half, -self.cursor_half, self.cursor_size, self.cursor_size))
        self.cursor_lmb.resize(0, 0)
        self.unseen = self.style.Transparent()
        self.cursor_lmb.setStyleSheet(self.unseen)

    # Relay
    def Location(self, location_x, location_y, width, height):
        # Input
        self.value_x = (width*0.5) + location_x
        self.value_y = (height*0.5) + location_y
        self.panel_width = width
        self.panel_height = height
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))
        self.update()

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.scale = 0
        self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        self.scale = 0
        self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        self.scale = 0
        self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        self.scale = 20
        self.mouseCursor(event)
        self.SIGNAL_OBJ_RELEASE.emit([self.value_x, self.value_y])

    def mouseCursor(self, event):
        # Event
        self.value_x = event.x()
        self.value_y = event.y()
        # Mouse Position
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))
        self.cursor_lmb.resize(self.scale, self.scale)
        # Emit values
        self.SIGNAL_OBJ_PRESS.emit([self.value_x, self.value_y])
        self.SIGNAL_OBJ_LOCATION.emit([self.value_x - (self.panel_width*0.5), self.value_y - (self.panel_height*0.5)])


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
    def SVG_Cursor_NODE(self, color):
        string_cursor_node = str(
        "<svg width=\"64\" height=\"64\" viewBox=\"0 0 48.000002 48.000002\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <circle \n" +
        "     style=\"fill:"+color+";stroke-width:0.0;stroke:none\" \n" +
        "     id=\"path831\" \n" +
        "     cx=\"24.000002\" \n" +
        "     cy=\"24.000002\" \n" +
        "     r=\"24.000002\" /> \n" +
        "</svg>"
        )
        array_cursor_node = bytearray(string_cursor_node, encoding='utf-8')
        return array_cursor_node
    def SVG_Cursor_POINT(self, color1, color2):
        string_cursor_point = str(
        "<svg width=\"64\" height=\"64\" viewBox=\"0 0 48.000002 48.000002\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     id=\"path834\" \n" +
        "     style=\"fill:"+color1+";fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "     d=\"M 32,0 0,32 32,64 64,32 Z M 32,14 50,32 32,50 13.999999,32 Z\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"OUT\" \n" +
        "     sodipodi:nodetypes=\"cccccccccc\" /> \n" +
        "  <path \n" +
        "     style=\"fill:"+color2+";fill-opacity:1;stroke:none;stroke-width:0.75px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "     d=\"M 24.000001,10.5 10.5,24.000001 24.000001,37.500002 37.500002,24.000001\" \n" +
        "     id=\"path845\" \n" +
        "     sodipodi:nodetypes=\"cccc\" \n" +
        "     inkscape:label=\"IN\" /> \n" +
        "</svg> "
        )
        array_cursor_point = bytearray(string_cursor_point, encoding='utf-8')
        return array_cursor_point
    def Transparent(self):
        transparent = "background-color: rgba(0, 0, 0, 0); border: 1px solid rgba(0, 0, 0, 0) ;"
        return transparent
