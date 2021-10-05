# Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer.
# Copyright (C) 2020  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#\\ Import Modules #############################################################
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt
import math
#//


class Color_Header(QWidget):
    SIGNAL_COLOR_LUMALOCK = QtCore.pyqtSignal(int)
    SIGNAL_COLOR_COMPLEMENTARY = QtCore.pyqtSignal(int)
    SIGNAL_COLOR_SWAP = QtCore.pyqtSignal(int)
    SIGNAL_COLOR_SHOW = QtCore.pyqtSignal(int)
    SIGNAL_COLOR_HIDE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Color_Header, self).__init__(parent)
        self.aaa_lock = False
        self.color = '#000000'
        self.gray_natural = '#383838'
        self.gray_contrast = '#d4d4d4'
        self.width = 0
        self.height = 0
    def sizeHint(self):
        return QtCore.QSize(5000,100)

    # Relay
    def Update_1(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height
    def Update_2(self, color, aaa_lock, gray_natural, gray_contrast, width, height):
        self.color = color
        self.aaa_lock = aaa_lock
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        self.width = width
        self.height = height
    def Setup(self, side):
        self.side = side

    # Interaction
    def mousePressEvent(self, event):
        if (self.side == 1 or self.side == 2):
            if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier):
                self.SIGNAL_COLOR_LUMALOCK.emit(0)
            if event.modifiers() == QtCore.Qt.AltModifier:
                self.SIGNAL_COLOR_COMPLEMENTARY.emit(0)
        if self.side == 3:
            self.SIGNAL_COLOR_SWAP.emit(0)
    def enterEvent(self, event):
        self.SIGNAL_COLOR_SHOW.emit(0)
    def leaveEvent(self, event):
        self.SIGNAL_COLOR_HIDE.emit(0)

    # Paint Style
    def paintEvent(self, event):
        if (self.side == 1 or self.side == 3):
            # Start Painter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Active Color
            painter.setBrush(QBrush(QColor(self.color)))
            painter.drawRect(0, 0, self.width, self.height)
        if self.side == 2:
            # Start Painter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            if self.aaa_lock == True:
                painter.setBrush(QBrush(QColor(self.gray_natural)))
                painter.drawRect(0, 0, self.width, self.height)
                painter.setBrush(QBrush(QColor(self.gray_contrast)))
                painter.drawRect(self.width*0.7, 0, self.width*0.20, self.height)
            if self.aaa_lock == False:
                painter.setBrush(QBrush(QColor(self.color)))
                painter.drawRect(0, 0, self.width, self.height)


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
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QPen(self.color_dark, 1, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        painter.setBrush(QBrush(self.color_light))
        # Polygon
        if self.active == True:
            square = QPolygon([
                QPoint(self.width*0.3, self.height*0.75),
                QPoint(self.width*0.7, self.height*0.75),
                QPoint(self.width*0.7, self.height*1.0),
                QPoint(self.width*0.3, self.height*1.0)
                ])
            painter.drawPolygon(square)


class Apply_RGB(QWidget):
    SIGNAL_APPLY = QtCore.pyqtSignal(list)

    # Init
    def __init__(self, parent):
        super(Apply_RGB, self).__init__(parent)
    def sizeHint(self):
        return QtCore.QSize(1000,1000)

    # Relay
    def Setup(self, value_1, value_2, value_3):
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3

    # Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.SIGNAL_APPLY.emit([self.value_1, self.value_2, self.value_3])
    def mouseDoubleClickEvent(self, event):
        self.SIGNAL_APPLY.emit([self.value_1, self.value_2, self.value_3])


class Panel_UVD(QWidget):
    SIGNAL_UVD_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_UVD_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_UVD, self).__init__(parent)
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
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
    def Update_Panel(self, uuu, vvv, ddd, pcc, p1, p2, p3, p4, p5, p6, p12, p23, p34, p45, p56, p61, width, height, hex, zoom):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.w2 = self.panel_width*0.5
        self.h2 = self.panel_height*0.5
        if self.panel_width >= self.panel_height:
            self.side = self.h2
        if self.panel_height > self.panel_width:
            self.side = self.w2
        self.hex = str(hex)
        # Change value range to slider range
        self.value_x = self.w2 + uuu * self.side
        self.value_y = self.h2 + vvv * self.side
        self.diagonal = round(ddd * 3, 9)
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
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        # Angles of Input
        self.angle_input = self.Math_2D_Points_Lines_Angle(self.event_x, self.event_y, self.PCC[0], self.PCC[1], self.PCC[0], -1)
        # Widget Constraint
        if self.diagonal <= 0:
            self.Mouse_Distance_Null(event)
        elif (self.diagonal > 0 and self.diagonal <= 1):
            # Certain
            if (self.angle_input == 0 or self.angle_input ==360):
                self.Mouse_Distance_Point(event, self.P61[0], self.P61[1])
            elif self.angle_input == 120:
                self.Mouse_Distance_Point(event, self.P45[0], self.P45[1])
            elif self.angle_input == 240:
                self.Mouse_Distance_Point(event, self.P23[0], self.P23[1])
            # Intervals
            elif (self.angle_input > 0 and self.angle_input < 120):
                self.Mouse_Distance_Line(event, self.P5[0], self.P5[1], self.P6[0], self.P6[1])
            elif (self.angle_input > 120 and self.angle_input < 240):
                self.Mouse_Distance_Line(event, self.P3[0], self.P3[1], self.P4[0], self.P4[1])
            elif (self.angle_input > 240 and self.angle_input < 360):
                self.Mouse_Distance_Line(event, self.P1[0], self.P1[1], self.P2[0], self.P2[1])
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
                self.Mouse_Distance_Point(event, self.P1[0], self.P1[1])
            elif self.angle_input == A2:
                self.Mouse_Distance_Point(event, self.P2[0], self.P2[1])
            elif self.angle_input == A3:
                self.Mouse_Distance_Point(event, self.P3[0], self.P3[1])
            elif self.angle_input == A4:
                self.Mouse_Distance_Point(event, self.P4[0], self.P4[1])
            elif self.angle_input == A5:
                self.Mouse_Distance_Point(event, self.P5[0], self.P5[1])
            elif self.angle_input == A6:
                self.Mouse_Distance_Point(event, self.P6[0], self.P6[1])
            # Intervals
            elif (self.angle_input < A1 and self.angle_input > A2):
                self.Mouse_Distance_Line(event, self.P1[0], self.P1[1], self.P2[0], self.P2[1])
            elif (self.angle_input < A2 and self.angle_input > A3):
                self.Mouse_Distance_Line(event, self.P2[0], self.P2[1], self.P3[0], self.P3[1])
            elif (self.angle_input < A3 and self.angle_input > A4):
                self.Mouse_Distance_Line(event, self.P3[0], self.P3[1], self.P4[0], self.P4[1])
            elif (self.angle_input < A4 and self.angle_input > A5):
                self.Mouse_Distance_Line(event, self.P4[0], self.P4[1], self.P5[0], self.P5[1])
            elif (self.angle_input < A5 and self.angle_input > A6):
                self.Mouse_Distance_Line(event, self.P5[0], self.P5[1], self.P6[0], self.P6[1])
            elif (self.angle_input < A6 or self.angle_input > A1):
                self.Mouse_Distance_Line(event, self.P6[0], self.P6[1], self.P1[0], self.P1[1])
        elif (self.diagonal >= 2 and self.diagonal < 3):
            # Certain
            if self.angle_input == 60:
                self.Mouse_Distance_Point(event, self.P45[0], self.P45[1])
            elif self.angle_input == 180:
                self.Mouse_Distance_Point(event, self.P34[0], self.P34[1])
            elif self.angle_input == 300:
                self.Mouse_Distance_Point(event, self.P12[0], self.P12[1])
            # Intervals
            elif (self.angle_input < 60 or self.angle_input > 300):
                self.Mouse_Distance_Line(event, self.P1[0], self.P1[1], self.P6[0], self.P6[1])
            elif (self.angle_input > 60 and self.angle_input < 180):
                self.Mouse_Distance_Line(event, self.P4[0], self.P4[1], self.P5[0], self.P5[1])
            elif (self.angle_input > 180 and self.angle_input < 300):
                self.Mouse_Distance_Line(event, self.P2[0], self.P2[1], self.P3[0], self.P3[1])
        elif self.diagonal >= 3:
            self.Mouse_Distance_Null(event)
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
        if self.diagonal <= 0:
            values = ["UV", 0, 0, 0]
        elif self.diagonal >= 3:
            values = ["UV", 0, 0, 0]
        else:
            values = ["UV", self.value_x / self.side, self.value_y / self.side, 0]
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
        # Painter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        # Masking
        hexagon = QPainterPath()
        hexagon.moveTo(self.P1[0], self.P1[1])
        hexagon.lineTo(self.P2[0], self.P2[1])
        hexagon.lineTo(self.P3[0], self.P3[1])
        hexagon.lineTo(self.P4[0], self.P4[1])
        hexagon.lineTo(self.P5[0], self.P5[1])
        hexagon.lineTo(self.P6[0], self.P6[1])
        painter.setClipPath(hexagon)
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

    # Limits
    def Mouse_Distance_Null(self, event):
        self.value_x = 0
        self.value_y = 0
    def Mouse_Distance_Point(self, event, x1, y1):
        # Distance of Input
        self.D_input = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.PCC[0], self.PCC[1])
        self.D_intersection = self.Math_2D_Points_Distance(x1, y1, self.PCC[0], self.PCC[1])
        # Distance Limit
        if self.D_input >= self.D_intersection:
            self.value_x = x1 - self.w2
            self.value_y = y1 - self.h2
        else:
            self.value_x = event.x() - self.w2
            self.value_y = event.y() - self.h2
    def Mouse_Distance_Line(self, event, x1, y1, x2, y2):
        # Intersecction of lines
        self.intersection = list(self.Math_2D_Points_Lines_Intersection(self.event_x, self.event_y, self.PCC[0], self.PCC[1],x1, y1, x2, y2))
        # Distance of Input
        self.D_input = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.PCC[0], self.PCC[1])
        self.D_intersection = self.Math_2D_Points_Distance(self.intersection[0], self.intersection[1], self.PCC[0], self.PCC[1])
        # Maintain Percentage (Used in Mouse_Stand_Line)
        self.percentage = self.D_input / self.D_intersection
        # Distance Limit
        if self.D_input >= self.D_intersection:
            self.value_x = self.intersection[0] - self.w2
            self.value_y = self.intersection[1] - self.h2
        else:
            self.value_x = event.x() - self.w2
            self.value_y = event.y() - self.h2

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


class Panel_YUV(QWidget):
    SIGNAL_YUV_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_YUV_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_YUV, self).__init__(parent)
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
        # Colors
        self.yuv = [0, 0, 0]
        # Left Colors
        self.cor1 = QColor(0, 0, 0)
        self.cor2 = QColor(0, 0, 0)
        self.cor3 = QColor(0, 0, 0)
        # Right Colors
        self.cor4 = QColor(0, 0, 0)
        self.cor5 = QColor(0, 0, 0)
        self.cor6 = QColor(0, 0, 0)
        # Panel
        self.panel_width = 0
        self.panel_height = 0
        # Panel Colors
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
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
    def Update_Panel(self, yuv, cor1, cor2, cor3, cor4, cor5, cor6, width, height, hex, zoom):
        # Colors
        self.yuv = [yuv[0], yuv[1], yuv[2]]
        # Left Colors
        self.cor1 = QColor(cor1)
        self.cor2 = QColor(cor2)
        self.cor3 = QColor(cor3)
        # Right Colors
        self.cor4 = QColor(cor4)
        self.cor5 = QColor(cor5)
        self.cor6 = QColor(cor6)

        # Change value range to slider range
        self.value_x = self.yuv[1] * self.panel_width
        self.value_y = self.panel_height - (self.yuv[2] * self.panel_height)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))

        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        self.SIGNAL_YUV_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Position
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.panel_width:
            self.value_x = self.panel_width
        if self.value_y <= 0:
            self.value_y = 0
        if self.value_y >= self.panel_height:
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
            list = ["UV", 0, (self.value_x / self.panel_width), ((self.panel_height - self.value_y) / self.panel_height)]
        except:
            list = ["UV", 0, 0, 0]
        self.SIGNAL_YUV_VALUE.emit(list)
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
        list = ["Y", self.distance, 0, 0]
        self.SIGNAL_YUV_VALUE.emit(list)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # gradient on left side, color top to color bottom
        gradientL = QLinearGradient(0,0, 0,self.panel_height)
        gradientL.setColorAt(0, self.cor1)
        gradientL.setColorAt(0.5, self.cor2)
        gradientL.setColorAt(1, self.cor3)

        # gradient on right side, color top to color bottom
        gradientR = QLinearGradient(0,0, 0,self.panel_height)
        gradientR.setColorAt(0, self.cor4)
        gradientR.setColorAt(0.5, self.cor5)
        gradientR.setColorAt(1, self.cor6)

        # gradient to define transparency, from left (opaque) to right (transparent)
        gradientTransparencyLR = QLinearGradient(0,0, self.panel_width,0)
        gradientTransparencyLR.setColorAt(0, QColor(Qt.black))
        gradientTransparencyLR.setColorAt(1, QColor(Qt.transparent))


        # create a first pixmap, color left, set it as transparent (because composition mode works on transparent pixels only)
        pixmapLeft = QPixmap(self.panel_width, self.panel_height)
        pixmapLeft.fill(Qt.transparent)
        canvas1 = QPainter()
        canvas1.begin(pixmapLeft)

        # first, prepare pixmap with opaque>transparent gradient
        canvas1.setPen(Qt.NoPen)
        canvas1.setBrush(gradientTransparencyLR)
        canvas1.drawRect(QRect(0,0, self.panel_width, self.panel_height))

        # and paint left color gradient on it:
        # result: left side is opaque with gradient from top left to bottom left
        canvas1.setCompositionMode(QPainter.CompositionMode_SourceIn)
        canvas1.setBrush(gradientL)
        canvas1.drawRect(QRect(0,0, self.panel_width, self.panel_height))
        canvas1.end()

        # create a new pixmap
        pixmap = QPixmap(self.panel_width, self.panel_height)
        canvas2 = QPainter(self)
        canvas2.begin(pixmap)

        # paint right top to bottom gradient (fill all area)
        canvas2.setPen(Qt.NoPen)
        canvas2.setBrush(gradientR)
        canvas2.drawRect(QRect(0,0, self.panel_width, self.panel_height))

        # draw pixmap of left side gradient
        canvas2.drawPixmap(0,0,pixmapLeft)
        canvas2.end()

        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)

        # Lines
        painter.setPen(QPen(QColor(self.color_light), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        lines = QPainterPath()
        lines.moveTo(self.panel_width*0.5, 0)
        lines.lineTo(self.panel_width*0.5, self.panel_height)
        lines.moveTo(0, self.panel_height*0.5)
        lines.lineTo(self.panel_width, self.panel_height*0.5)
        painter.drawPath(lines)
        painter.end()


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
        self.limit = None
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
    def Update_Panel(self, hue, rrr, ddd, t1, t2, t3, cross, width, height, hex, zoom):
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        # Points
        self.T1 = [t1[0]*width, t1[1]*height]
        self.T2 = [t2[0]*width, t2[1]*height]
        self.T3 = [t3[0]*width, t3[1]*height]
        self.cross = cross
        # Change value range to slider range
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
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        # Cursor Value
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Inputs
        if self.value_y <= 0:
            self.value_x = self.T1[0]
            self.value_y = self.T1[1]
        elif self.value_y >= self.panel_height:
            self.value_x = self.T2[0]
            self.value_y = self.T2[1]
        elif (self.value_y > 0 and self.value_y < self.panel_height):
            # Vertical Limits
            if self.value_y < self.T3[1]:
                self.limit = list(self.Math_2D_Points_Lines_Intersection(
                    0,0,
                    self.T3[0],self.T3[1],
                    0,self.value_y,
                    self.panel_width,self.value_y,
                    ))
            elif self.value_y == self.T3[1]:
                self.limit = self.panel_width
            elif self.value_y > self.T3[1]:
                self.limit = list(self.Math_2D_Points_Lines_Intersection(
                    self.T2[0],self.T2[1],
                    self.T3[0],self.T3[1],
                    0,self.value_y,
                    self.panel_width,self.value_y,
                    ))
            # Horizontal Limits
            if self.value_x <= 0:
                self.value_x = 0
            if self.value_x >= self.limit[0]:
                self.value_x = self.limit[0]
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
            values = ["RD", 0, (self.value_x) / self.limit[0], 1 - (self.value_y / self.panel_height)]
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
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        # Masking
        triangle = QPainterPath()
        triangle.moveTo(0, 0)
        triangle.lineTo(self.T1[0], self.T1[1])
        triangle.lineTo(self.T2[0], self.T2[1])
        triangle.lineTo(self.T3[0], self.T3[1])
        painter.setClipPath(triangle)
        # Gradient BW
        bw = QLinearGradient(0, 0, 0, self.panel_height)
        bw.setColorAt(0.000, QColor(255, 255, 255)) # White Invisiable
        bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
        painter.setBrush(QBrush(bw))
        painter.drawRect(0,0, self.panel_width,self.panel_height)
        # Gradient Color
        cor = QLinearGradient(0, 0, self.panel_width, 0)
        cor.setColorAt(0.000, QColor(255, 255, 255, 0)) # White
        cor.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255, 255)) # Color
        painter.setBrush(QBrush(cor))
        painter.drawRect(0,0, self.panel_width, self.panel_height)

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
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
        self.render = "COLOR"
        self.har_spot = 5
        self.har_line = 2
        self.panel_width = 0
        self.panel_height = 0
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
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
    def Update_Panel(self, hsv, hue, harmony_render, harmony_edit, har_1, har_2, har_3, har_4, har_5, width, height, hex, zoom):
        # Colors
        self.hsv = [hsv[0], hsv[1], hsv[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Change value range to slider range
        self.value_x = self.hsv[1] * self.panel_width
        self.value_y = self.panel_height - (self.hsv[2] * self.panel_height)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Harmony
        self.harmony_render = harmony_render
        self.harmony_edit = harmony_edit
        self.har_1 = [har_1[0], har_1[1], har_1[2]]
        self.har_2 = [har_2[0], har_2[1], har_2[2]]
        self.har_3 = [har_3[0], har_3[1], har_3[2]]
        self.har_4 = [har_4[0], har_4[1], har_4[2]]
        self.har_5 = [har_5[0], har_5[1], har_5[2]]
        self.har_1x = self.har_1[1] * self.panel_width
        self.har_2x = self.har_2[1] * self.panel_width
        self.har_3x = self.har_3[1] * self.panel_width
        self.har_4x = self.har_4[1] * self.panel_width
        self.har_5x = self.har_5[1] * self.panel_width
        self.har_1y = self.panel_height - (self.har_1[2] * self.panel_height)
        self.har_2y = self.panel_height - (self.har_2[2] * self.panel_height)
        self.har_3y = self.panel_height - (self.har_3[2] * self.panel_height)
        self.har_4y = self.panel_height - (self.har_4[2] * self.panel_height)
        self.har_5y = self.panel_height - (self.har_5[2] * self.panel_height)
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Position
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.panel_width:
            self.value_x = self.panel_width
        if self.value_y <= 0:
            self.value_y = 0
        if self.value_y >= self.panel_height:
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
            list = ["SV", 0, (self.value_x / self.panel_width), ((self.panel_height - self.value_y) / self.panel_height)]
        except:
            list = ["SV", 0, 0, 0]
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
        if self.harmony_render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
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
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White Invisiable
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
        if self.harmony_render == "HARMONY":
            # Start Qpainter
            painter = QPainter(self)
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
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White Invisiable
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Harmony Marks
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(self.color_light), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.har_1x, self.har_1y, self.har_2x, self.har_2y)
            painter.drawLine(self.har_2x, self.har_2y, self.har_3x, self.har_3y)
            painter.drawLine(self.har_3x, self.har_3y, self.har_4x, self.har_4y)
            painter.drawLine(self.har_4x, self.har_4y, self.har_5x, self.har_5y)
            painter.setBrush(QBrush(QColor(self.color_light)))
            # Harmoney Line
            painter.setPen(QPen(QColor(self.color_dark), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawEllipse(self.har_1x-self.har_spot, self.har_1y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_2x-self.har_spot, self.har_2y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_3x-self.har_spot, self.har_3y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_4x-self.har_spot, self.har_4y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_5x-self.har_spot, self.har_5y-self.har_spot, self.har_spot*2, self.har_spot*2)


class Panel_HSL_3(QWidget):
    SIGNAL_HSL_3_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HSL_3_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HSL_3, self).__init__(parent)
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
        self.render = "COLOR"
        self.har_spot = 5
        self.har_line = 2
        self.panel_width = 0
        self.panel_height = 0
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
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
    def Update_Panel(self, hsl, hue, harmony_render, harmony_edit, har_1, har_2, har_3, har_4, har_5, width, height, hex, zoom):
        # Colors
        self.hsl = [hsl[0], hsl[1], hsl[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Change value range to slider range
        self.value_y = self.panel_height - (self.hsl[2] * self.panel_height)
        self.value_x = self.Panel_Triangle(self.hsl[1], self.value_y)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Harmony
        self.harmony_render = harmony_render
        self.harmony_edit = harmony_edit
        self.har_1 = [har_1[0], har_1[1], har_1[2]]
        self.har_2 = [har_2[0], har_2[1], har_2[2]]
        self.har_3 = [har_3[0], har_3[1], har_3[2]]
        self.har_4 = [har_4[0], har_4[1], har_4[2]]
        self.har_5 = [har_5[0], har_5[1], har_5[2]]
        self.har_1y = self.panel_height - (self.har_1[2] * self.panel_height)
        self.har_2y = self.panel_height - (self.har_2[2] * self.panel_height)
        self.har_3y = self.panel_height - (self.har_3[2] * self.panel_height)
        self.har_4y = self.panel_height - (self.har_4[2] * self.panel_height)
        self.har_5y = self.panel_height - (self.har_5[2] * self.panel_height)
        self.har_1x = self.Panel_Triangle(self.har_1[1], self.har_1y)
        self.har_2x = self.Panel_Triangle(self.har_2[1], self.har_2y)
        self.har_3x = self.Panel_Triangle(self.har_3[1], self.har_3y)
        self.har_4x = self.Panel_Triangle(self.har_4[1], self.har_4y)
        self.har_5x = self.Panel_Triangle(self.har_5[1], self.har_5y)
        # Update the variables
        self.hex = str(hex)
        self.cursorzoom(zoom)
    def Panel_Triangle (self, horizontal, vertical):
        if vertical <= self.panel_height*0:
            value_x = 0
        if (vertical >= self.panel_height*0 and vertical <= self.panel_height*0.5):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,vertical, self.panel_width,vertical,
                0,0, self.panel_width,self.panel_height/2
                )
            value_x = horizontal * intersection[0]
        if vertical == self.panel_height*0.5:
            value_x = horizontal * self.panel_width
        if (vertical >= self.panel_height*0.5 and vertical <= self.panel_height*1):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,vertical, self.panel_width,vertical,
                0,self.panel_height, self.panel_width,self.panel_height/2
                )
            value_x = horizontal * intersection[0]
        if vertical >= self.panel_height*1:
            value_x = 0
        return value_x

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        if self.harmony_render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Masking
            triangle = QPainterPath()
            triangle.moveTo(0, 1)
            triangle.lineTo(0, self.panel_height-1)
            triangle.lineTo(self.panel_width-1, self.panel_height*0.5)
            painter.setClipPath(triangle)
            # Gradient Color
            cor1 = QConicalGradient (QPointF(0, 0), 0)
            cor1.setColorAt(0.000, QColor(127,127,127))
            cor1.setColorAt(0.750, QColor(127,127,127))
            cor1.setColorAt(0.917, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor1.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            painter.setBrush(QBrush(cor1))
            painter.drawRect(0,0, self.panel_width, self.panel_height*0.5)
            cor2 = QConicalGradient (QPointF(0, self.panel_height), 0)
            cor2.setColorAt(0.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor2.setColorAt(0.082, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor2.setColorAt(0.250, QColor(127,127,127))
            cor2.setColorAt(1.000, QColor(127,127,127))
            painter.setBrush(QBrush(cor2))
            painter.drawRect(0,self.panel_height*0.5, self.panel_width, self.panel_height)
            # Gradient BW
            painter.setCompositionMode(QPainter.CompositionMode_HardLight)
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
        if self.harmony_render == "HARMONY":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Masking
            triangle = QPainterPath()
            triangle.moveTo(0, 1)
            triangle.lineTo(0, self.panel_height-1)
            triangle.lineTo(self.panel_width-1, self.panel_height*0.5)
            painter.setClipPath(triangle)
            # Gradient Color
            cor1 = QConicalGradient (QPointF(0, 0), 0)
            cor1.setColorAt(0.000, QColor(127,127,127))
            cor1.setColorAt(0.750, QColor(127,127,127))
            cor1.setColorAt(0.917, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor1.setColorAt(1.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            painter.setBrush(QBrush(cor1))
            painter.drawRect(0,0, self.panel_width, self.panel_height*0.5)
            cor2 = QConicalGradient (QPointF(0, self.panel_height), 0)
            cor2.setColorAt(0.000, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor2.setColorAt(0.082, QColor(self.hue[0]*255, self.hue[1]*255, self.hue[2]*255)) # Color
            cor2.setColorAt(0.250, QColor(127,127,127))
            cor2.setColorAt(1.000, QColor(127,127,127))
            painter.setBrush(QBrush(cor2))
            painter.drawRect(0,self.panel_height*0.5, self.panel_width, self.panel_height)
            # Gradient BW
            painter.setCompositionMode(QPainter.CompositionMode_HardLight)
            bw = QLinearGradient(0, 0, 0, self.panel_height)
            bw.setColorAt(0.000, QColor(255, 255, 255)) # White
            bw.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Harmony Marks
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(self.color_light), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.har_1x, self.har_1y, self.har_2x, self.har_2y)
            painter.drawLine(self.har_2x, self.har_2y, self.har_3x, self.har_3y)
            painter.drawLine(self.har_3x, self.har_3y, self.har_4x, self.har_4y)
            painter.drawLine(self.har_4x, self.har_4y, self.har_5x, self.har_5y)
            painter.setBrush(QBrush(QColor(self.color_light)))
            # Harmoney Line
            painter.setPen(QPen(QColor(self.color_dark), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawEllipse(self.har_1x-self.har_spot, self.har_1y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_2x-self.har_spot, self.har_2y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_3x-self.har_spot, self.har_3y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_4x-self.har_spot, self.har_4y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_5x-self.har_spot, self.har_5y-self.har_spot, self.har_spot*2, self.har_spot*2)

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
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
        self.render = "COLOR"
        self.har_spot = 5
        self.har_line = 2
        self.panel_width = 0
        self.panel_height = 0
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
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
    def Update_Panel(self, hsl, hue, harmony_render, harmony_edit, har_1, har_2, har_3, har_4, har_5, width, height, hex, zoom):
        # Colors
        self.hsl = [hsl[0], hsl[1], hsl[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Change value range to slider range
        self.value_x = self.hsl[1] * self.panel_width
        self.value_y = self.panel_height - (self.hsl[2] * self.panel_height)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Harmony
        self.harmony_render = harmony_render
        self.harmony_edit = harmony_edit
        self.har_1 = [har_1[0], har_1[1], har_1[2]]
        self.har_2 = [har_2[0], har_2[1], har_2[2]]
        self.har_3 = [har_3[0], har_3[1], har_3[2]]
        self.har_4 = [har_4[0], har_4[1], har_4[2]]
        self.har_5 = [har_5[0], har_5[1], har_5[2]]
        self.har_1x = self.har_1[1] * self.panel_width
        self.har_2x = self.har_2[1] * self.panel_width
        self.har_3x = self.har_3[1] * self.panel_width
        self.har_4x = self.har_4[1] * self.panel_width
        self.har_5x = self.har_5[1] * self.panel_width
        self.har_1y = self.panel_height - (self.har_1[2] * self.panel_height)
        self.har_2y = self.panel_height - (self.har_2[2] * self.panel_height)
        self.har_3y = self.panel_height - (self.har_3[2] * self.panel_height)
        self.har_4y = self.panel_height - (self.har_4[2] * self.panel_height)
        self.har_5y = self.panel_height - (self.har_5[2] * self.panel_height)
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Position
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.panel_width:
            self.value_x = self.panel_width
        if self.value_y <= 0:
            self.value_y = 0
        if self.value_y >= self.panel_height:
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
        if self.harmony_render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
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
        if self.harmony_render == "HARMONY":
            # Start Qpainter
            painter = QPainter(self)
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
            # Harmony Marks
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(self.color_light), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.har_1x, self.har_1y, self.har_2x, self.har_2y)
            painter.drawLine(self.har_2x, self.har_2y, self.har_3x, self.har_3y)
            painter.drawLine(self.har_3x, self.har_3y, self.har_4x, self.har_4y)
            painter.drawLine(self.har_4x, self.har_4y, self.har_5x, self.har_5y)
            painter.setBrush(QBrush(QColor(self.color_light)))
            # Harmoney Line
            painter.setPen(QPen(QColor(self.color_dark), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawEllipse(self.har_1x-self.har_spot, self.har_1y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_2x-self.har_spot, self.har_2y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_3x-self.har_spot, self.har_3y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_4x-self.har_spot, self.har_4y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_5x-self.har_spot, self.har_5y-self.har_spot, self.har_spot*2, self.har_spot*2)
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
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
        self.render = "COLOR"
        self.har_spot = 5
        self.har_line = 2
        self.panel_width = 0
        self.panel_height = 0
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
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
    def Update_Panel(self, hsl, hue, harmony_render, harmony_edit, har_1, har_2, har_3, har_4, har_5, width, height, hex, zoom):
        # Colors
        self.hsl = [hsl[0], hsl[1], hsl[2]]
        self.hue = [hue[0], hue[1], hue[2]]
        # Panel Geometry
        self.panel_width = width
        self.panel_height = height
        # Change value range to slider range
        self.value_x, self.value_y = self.Panel_Diamond(self.hsl[1], self.hsl[2])
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Harmony
        self.harmony_render = harmony_render
        self.harmony_edit = harmony_edit
        self.har_1 = [har_1[0], har_1[1], har_1[2]]
        self.har_2 = [har_2[0], har_2[1], har_2[2]]
        self.har_3 = [har_3[0], har_3[1], har_3[2]]
        self.har_4 = [har_4[0], har_4[1], har_4[2]]
        self.har_5 = [har_5[0], har_5[1], har_5[2]]
        self.har_1x, self.har_1y = self.Panel_Diamond(self.har_1[1], self.har_1[2])
        self.har_2x, self.har_2y = self.Panel_Diamond(self.har_2[1], self.har_2[2])
        self.har_3x, self.har_3y = self.Panel_Diamond(self.har_3[1], self.har_3[2])
        self.har_4x, self.har_4y = self.Panel_Diamond(self.har_4[1], self.har_4[2])
        self.har_5x, self.har_5y = self.Panel_Diamond(self.har_5[1], self.har_5[2])
        # Update the variables
        self.hex = str(hex)
        self.cursorzoom(zoom)
    def Panel_Diamond(self, horizontal, vertical):
        if vertical <= 0:
            value_x = self.panel_width/2
            value_y = self.panel_height
        if (vertical > 0 and vertical < 0.5):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,vertical*self.panel_height, self.panel_width,vertical*self.panel_height,
                0,self.panel_height/2, self.panel_width/2,0)
            distance = self.panel_width - (2*intersection[0])
            value_x = intersection[0] + (horizontal * distance)
            value_y = self.panel_height - (vertical * self.panel_height)
        if vertical == 0.5:
            value_x = horizontal * self.panel_width
            value_y = self.panel_height/2
        if (vertical > 0.5 and vertical < 1):
            intersection = self.Math_2D_Points_Lines_Intersection(
                0,vertical*self.panel_height, self.panel_width,vertical*self.panel_height,
                0,self.panel_height/2, self.panel_width/2,self.panel_height)
            distance = self.panel_width - (2*intersection[0])
            value_x = intersection[0] + (horizontal * distance)
            value_y = self.panel_height - (vertical * self.panel_height)
        if vertical >= 1:
            value_x = self.panel_width/2
            value_y = 0
        return [value_x, value_y]

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        if self.harmony_render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Masking
            triangle = QPainterPath()
            triangle.moveTo(self.panel_width*0.5, 1)
            triangle.lineTo(self.panel_width-1, self.panel_height*0.5)
            triangle.lineTo(self.panel_width*0.5, self.panel_height-1)
            triangle.lineTo(1, self.panel_height*0.5)
            painter.setClipPath(triangle)
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
        if self.harmony_render == "HARMONY":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)
            # Masking
            triangle = QPainterPath()
            triangle.moveTo(self.panel_width*0.5, 1)
            triangle.lineTo(self.panel_width-1, self.panel_height*0.5)
            triangle.lineTo(self.panel_width*0.5, self.panel_height-1)
            triangle.lineTo(1, self.panel_height*0.5)
            painter.setClipPath(triangle)
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
            # Harmony Marks
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(self.color_light), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawLine(self.har_1x, self.har_1y, self.har_2x, self.har_2y)
            painter.drawLine(self.har_2x, self.har_2y, self.har_3x, self.har_3y)
            painter.drawLine(self.har_3x, self.har_3y, self.har_4x, self.har_4y)
            painter.drawLine(self.har_4x, self.har_4y, self.har_5x, self.har_5y)
            painter.setBrush(QBrush(QColor(self.color_light)))
            # Harmoney Line
            painter.setPen(QPen(QColor(self.color_dark), self.har_line, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawEllipse(self.har_1x-self.har_spot, self.har_1y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_2x-self.har_spot, self.har_2y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_3x-self.har_spot, self.har_3y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_4x-self.har_spot, self.har_4y-self.har_spot, self.har_spot*2, self.har_spot*2)
            painter.drawEllipse(self.har_5x-self.har_spot, self.har_5y-self.har_spot, self.har_spot*2, self.har_spot*2)

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


class Panel_HCY_4(QWidget):
    SIGNAL_HCY_4_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HCY_4_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_HCY_4, self).__init__(parent)
        # Start
        self.Variables()
        self.Cursor()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)
    def Variables(self):
        self.render = "COLOR"
        self.har_spot = 5
        self.har_line = 2
        self.panel_width = 0
        self.panel_height = 0
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
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
    def Update_Panel(self,
    hcy,

    cor_00,
    cor_01,
    cor_02,
    cor_03,
    cor_04,
    cor_05,
    cor_06,
    cor_07,
    cor_08,
    cor_09,
    cor_10,

    harmony_render, harmony_edit,
    #har_1, har_2, har_3, har_4, har_5,
    width, height, hex, zoom):
        # Colors
        self.hcy = [hcy[0], hcy[1], hcy[2]]

        self.cor_00 = [cor_00[0], cor_00[1], cor_00[2]]
        self.cor_01 = [cor_01[0], cor_01[1], cor_01[2]]
        self.cor_02 = [cor_02[0], cor_02[1], cor_02[2]]
        self.cor_03 = [cor_03[0], cor_03[1], cor_03[2]]
        self.cor_04 = [cor_04[0], cor_04[1], cor_04[2]]
        self.cor_05 = [cor_05[0], cor_05[1], cor_05[2]]
        self.cor_06 = [cor_06[0], cor_06[1], cor_06[2]]
        self.cor_07 = [cor_07[0], cor_07[1], cor_07[2]]
        self.cor_08 = [cor_08[0], cor_08[1], cor_08[2]]
        self.cor_09 = [cor_09[0], cor_09[1], cor_09[2]]
        self.cor_10 = [cor_10[0], cor_10[1], cor_10[2]]

        # Change value range to slider range
        self.value_x = self.hcy[1] * self.panel_width
        self.value_y = self.panel_height - (self.hcy[2] * self.panel_height)
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # # Harmony
        self.harmony_render = harmony_render
        self.harmony_edit = harmony_edit
        # self.har_1 = [har_1[0], har_1[1], har_1[2]]
        # self.har_2 = [har_2[0], har_2[1], har_2[2]]
        # self.har_3 = [har_3[0], har_3[1], har_3[2]]
        # self.har_4 = [har_4[0], har_4[1], har_4[2]]
        # self.har_5 = [har_5[0], har_5[1], har_5[2]]
        # self.har_1x = self.har_1[1] * self.panel_width
        # self.har_2x = self.har_2[1] * self.panel_width
        # self.har_3x = self.har_3[1] * self.panel_width
        # self.har_4x = self.har_4[1] * self.panel_width
        # self.har_5x = self.har_5[1] * self.panel_width
        # self.har_1y = self.panel_height - (self.har_1[2] * self.panel_height)
        # self.har_2y = self.panel_height - (self.har_2[2] * self.panel_height)
        # self.har_3y = self.panel_height - (self.har_3[2] * self.panel_height)
        # self.har_4y = self.panel_height - (self.har_4[2] * self.panel_height)
        # self.har_5y = self.panel_height - (self.har_5[2] * self.panel_height)
        # Update the variables
        self.panel_width = width
        self.panel_height = height
        self.hex = str(hex)
        self.cursorzoom(zoom)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
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
        self.SIGNAL_HCY_4_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.value_x = event.x()
        self.value_y = event.y()
        # Limit Position
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.panel_width:
            self.value_x = self.panel_width
        if self.value_y <= 0:
            self.value_y = 0
        if self.value_y >= self.panel_height:
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
            list = ["CY", 0, (self.value_x / self.panel_width), ((self.panel_height - self.value_y) / self.panel_height)]
        except:
            list = ["CY", 0, 0, 0]
        self.SIGNAL_HCY_4_VALUE.emit(list)
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
        self.SIGNAL_HCY_4_VALUE.emit(list)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        if self.harmony_render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setPen(QtCore.Qt.NoPen)

            # Gradient BW
            bw1 = QLinearGradient(0, 0, 0, self.panel_height)
            bw1.setColorAt(0.000, QColor(255, 255, 255)) # White
            bw1.setColorAt(1.000, QColor(0, 0, 0)) # Black
            painter.setBrush(QBrush(bw1))
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            painter.end()


            gradientTransparencyLR = QLinearGradient(0,0, self.panel_width,0)
            gradientTransparencyLR.setColorAt(0, QColor(Qt.black))
            gradientTransparencyLR.setColorAt(1, QColor(Qt.transparent))

            pixmapLeft = QPixmap(self.panel_width, self.panel_height)
            pixmapLeft.fill(Qt.transparent)
            canvas1 = QPainter(self)
            canvas1.begin(pixmapLeft)

            canvas1.setPen(Qt.NoPen)
            canvas1.setBrush(gradientTransparencyLR)
            canvas1.drawRect(QRect(0,0, self.panel_width, self.panel_height))

            canvas1.setCompositionMode(QPainter.CompositionMode_SourceIn)
            # canvas1.setBrush(gradientL)
            # canvas1.drawRect(QRect(0,0, self.panel_width, self.panel_height))
            # canvas1.end()


            # Gradient Color (Source)
            cor = QLinearGradient(0, 0, 0, self.panel_height)
            cor.setColorAt(0.000, QColor(self.cor_00[0]*255, self.cor_00[1]*255, self.cor_00[2]*255, 255))
            cor.setColorAt(0.100, QColor(self.cor_01[0]*255, self.cor_01[1]*255, self.cor_01[2]*255, 255))
            cor.setColorAt(0.200, QColor(self.cor_02[0]*255, self.cor_02[1]*255, self.cor_02[2]*255, 255))
            cor.setColorAt(0.300, QColor(self.cor_03[0]*255, self.cor_03[1]*255, self.cor_03[2]*255, 255))
            cor.setColorAt(0.400, QColor(self.cor_04[0]*255, self.cor_04[1]*255, self.cor_04[2]*255, 255))
            cor.setColorAt(0.500, QColor(self.cor_05[0]*255, self.cor_05[1]*255, self.cor_05[2]*255, 255))
            cor.setColorAt(0.600, QColor(self.cor_06[0]*255, self.cor_06[1]*255, self.cor_06[2]*255, 255))
            cor.setColorAt(0.700, QColor(self.cor_07[0]*255, self.cor_07[1]*255, self.cor_07[2]*255, 255))
            cor.setColorAt(0.800, QColor(self.cor_08[0]*255, self.cor_08[1]*255, self.cor_08[2]*255, 255))
            cor.setColorAt(0.900, QColor(self.cor_09[0]*255, self.cor_09[1]*255, self.cor_09[2]*255, 255))
            cor.setColorAt(1.000, QColor(self.cor_10[0]*255, self.cor_10[1]*255, self.cor_10[2]*255, 255))
            canvas1.setBrush(QBrush(cor))
            canvas1.drawRect(0,0, self.panel_width, self.panel_height)
            canvas1.end()

            # # Gradient BW (Destination)
            # painter.setCompositionMode(QPainter.CompositionMode_Lighten)
            # bw2 = QLinearGradient(0, 0, self.panel_width, 0)
            # bw2.setColorAt(0.000, QColor(255, 255, 255, 0))
            # bw2.setColorAt(1.000, QColor(0, 0, 0, 255))
            # painter.setBrush(QBrush(bw2))
            # painter.drawRect(0,0, self.panel_width,self.panel_height)
        if self.harmony_render == "HARMONY":
            pass


class Panel_HUE_Circle(QWidget):
    SIGNAL_HUE_C_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_HUE_C_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_HUE_C_HARMONY_ACTIVE = QtCore.pyqtSignal(int)

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
        self.valid = False
        self.wheel = "CMY"
        self.harmony_render ="COLOR"
        self.harmony_rule = "Analogous"
        self.angle = 0
        self.red = [0, 0, 0]
        self.mag = [0, 0, 0]
        self.blu = [0, 0, 0]
        self.cya = [0, 0, 0]
        self.gre = [0, 0, 0]
        self.yel = [0, 0, 0]
        self.ora = [0, 0, 0]
        self.circle_x = 0
        self.circle_y = 0
        self.hex = '#000000'
        self.color_dark = QColor('#383838')
        self.color_gray = QColor('#666666')
        self.har_radius = 0.5
        self.har_radius_poly = 0.5 - ( 2 * 0.035 )

        self.h1_angle = 0
        self.h2_angle = 0
        self.h3_angle = 0
        self.h4_angle = 0
        self.h5_angle = 0
        self.h1_circle_x = 0
        self.h1_circle_y = 0
        self.h2_circle_x = 0
        self.h2_circle_y = 0
        self.h3_circle_x = 0
        self.h3_circle_y = 0
        self.h4_circle_x = 0
        self.h4_circle_y = 0
        self.h5_circle_x = 0
        self.h5_circle_y = 0
        self.h1_hue = [0, 0, 0]
        self.h2_hue = [0, 0, 0]
        self.h3_hue = [0, 0, 0]
        self.h4_hue = [0, 0, 0]
        self.h5_hue = [0, 0, 0]
        self.h1_event_x = 0
        self.h1_event_y = 0
        self.h2_event_x = 0
        self.h2_event_y = 0
        self.h3_event_x = 0
        self.h3_event_y = 0
        self.h4_event_x = 0
        self.h4_event_y = 0
        self.h5_event_x = 0
        self.h5_event_y = 0
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)

    # Relay
    def Active(self, harmony_active):
        self.harmony_active = harmony_active

    # Update Normal
    def Update_Panel(self, wheel, harmony_render, harmony_rule, angle, hue, width, height, gray_natural, gray_contrast):
        # Color
        self.wheel = wheel # CMY RYB
        if self.wheel == "CMY":
            self.angle = angle * 360
        if self.wheel == "RYB":
            self.angle = (angle * 360) - 30
        self.harmony_render = harmony_render # COLOR HARMONY
        self.harmony_rule = harmony_rule # Monochromatic Complemantary Analogous Split Complemantary Double Split Complemantary
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
    def Update_Harmony_1(self, wheel, harmony_render, harmony_rule, angle, color, width, height, gray_natural, gray_contrast):
        # Color
        self.wheel = wheel # CMY RYB
        # Harmony
        self.harmony_render = harmony_render # COLOR HARMONY
        self.harmony_rule = harmony_rule # Monochromatic Complemantary Analogous Split Complemantary Double Split Complemantary
        # Hue Color in RGB
        if self.wheel == "CMY":
            self.h1_angle = angle * 360
        if self.wheel == "RYB":
            self.h1_angle = (angle * 360) - 30
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
    def Update_Harmony_2(self, wheel, harmony_render, harmony_rule, angle, color, width, height, gray_natural, gray_contrast):
        # Color
        self.wheel = wheel # CMY RYB
        # Harmony
        self.harmony_render = harmony_render # COLOR HARMONY
        self.harmony_rule = harmony_rule # Monochromatic Complemantary Analogous Split Complemantary Double Split Complemantary
        # Hue Color in RGB
        if self.wheel == "CMY":
            self.h2_angle = angle * 360
        if self.wheel == "RYB":
            self.h2_angle = (angle * 360) - 30
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
    def Update_Harmony_3(self, wheel, harmony_render, harmony_rule, angle, color, width, height, gray_natural, gray_contrast):
        # Color
        self.wheel = wheel # CMY RYB
        # Harmony
        self.harmony_render = harmony_render # COLOR HARMONY
        self.harmony_rule = harmony_rule # Monochromatic Complemantary Analogous Split Complemantary Double Split Complemantary
        # Hue Color in RGB
        if self.wheel == "CMY":
            self.h3_angle = angle * 360
        if self.wheel == "RYB":
            self.h3_angle = (angle * 360) - 30
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
    def Update_Harmony_4(self, wheel, harmony_render, harmony_rule, angle, color, width, height, gray_natural, gray_contrast):
        # Color
        self.wheel = wheel # CMY RYB
        # Harmony
        self.harmony_render = harmony_render # COLOR HARMONY
        self.harmony_rule = harmony_rule # Monochromatic Complemantary Analogous Split Complemantary Double Split Complemantary
        # Hue Color in RGB
        if self.wheel == "CMY":
            self.h4_angle = angle * 360
        if self.wheel == "RYB":
            self.h4_angle = (angle * 360) - 30
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
    def Update_Harmony_5(self, wheel, harmony_render, harmony_rule, angle, color, width, height, gray_natural, gray_contrast):
        # Color
        self.wheel = wheel # CMY RYB
        # Harmony
        self.harmony_render = harmony_render # COLOR HARMONY
        self.harmony_rule = harmony_rule # Monochromatic Complemantary Analogous Split Complemantary Double Split Complemantary
        # Hue Color in RGB
        if self.wheel == "CMY":
            self.h5_angle = angle * 360
        if self.wheel == "RYB":
            self.h5_angle = (angle * 360) - 30
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
    def Update_Ring(self, red, mag, blu, cya, gre, yel, ora):
        # Ring Colors
        self.red = [red[0]*255, red[1]*255, red[2]*255]
        self.mag = [mag[0]*255, mag[1]*255, mag[2]*255]
        self.blu = [blu[0]*255, blu[1]*255, blu[2]*255]
        self.cya = [cya[0]*255, cya[1]*255, cya[2]*255]
        self.gre = [gre[0]*255, gre[1]*255, gre[2]*255]
        self.yel = [yel[0]*255, yel[1]*255, yel[2]*255]
        self.ora = [ora[0]*255, ora[1]*255, ora[2]*255]

    # Mouse Interaction
    def mousePressEvent(self, event):
        dist = math.sqrt( math.pow((event.x() - self.panel_width*0.5),2) + math.pow((event.y() - self.panel_height*0.5),2) )
        if dist <= self.panel_width*0.5:
            self.valid = True
        if self.valid == True:
            self.CloserTo(event)
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if self.valid == True:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if self.valid == True:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if self.valid == True:
            self.mouseCursor(event)
            self.SIGNAL_HUE_C_RELEASE.emit(0)
            self.valid = False

    def mouseCursor(self, event):
        # Circle Values
        self.event_x = event.x()
        self.event_y = self.panel_height - event.y()
        # Angle
        if self.wheel == "CMY":
            self.angle = self.Math_2D_Points_Lines_Angle(
                self.event_x, self.event_y,
                self.panel_width*0.5,self.panel_height*0.5,
                0,self.panel_height*0.5)
        if self.wheel == "RYB":
            self.angle = self.Math_2D_Points_Lines_Angle(
                self.event_x, self.event_y,
                self.panel_width*0.5,self.panel_height*0.5,
                0,self.panel_height*0.211325)
        self.radius = 0.465
        self.circle_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(self.angle)))
        self.circle_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(self.angle)))
        # Constraint for Modifier Keys
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier):
            if (self.angle < 5 or self.angle >= 355): # Red
                self.angle = 0
            if (self.angle >= 5 and self.angle < 15):
                self.angle = 10
            if (self.angle >= 15 and self.angle < 25):
                self.angle = 20
            if (self.angle >= 25 and self.angle < 35):
                self.angle = 30
            if (self.angle >= 35 and self.angle < 45):
                self.angle = 40
            if (self.angle >= 45 and self.angle < 55):
                self.angle = 50
            if (self.angle >= 55 and self.angle < 65): # Yellow
                self.angle = 60
            if (self.angle >= 65 and self.angle < 75):
                self.angle = 70
            if (self.angle >= 75 and self.angle < 85):
                self.angle = 80
            if (self.angle >= 85 and self.angle < 95):
                self.angle = 90
            if (self.angle >= 95 and self.angle < 105):
                self.angle = 100
            if (self.angle >= 105 and self.angle < 115):
                self.angle = 110
            if (self.angle >= 115 and self.angle < 125): # Green
                self.angle = 120
            if (self.angle >= 125 and self.angle < 135):
                self.angle = 130
            if (self.angle >= 135 and self.angle < 145):
                self.angle = 140
            if (self.angle >= 145 and self.angle < 155):
                self.angle = 150
            if (self.angle >= 155 and self.angle < 165):
                self.angle = 160
            if (self.angle >= 165 and self.angle < 175):
                self.angle = 170
            if (self.angle >= 175 and self.angle < 185): # Cyan
                self.angle = 180
            if (self.angle >= 185 and self.angle < 195):
                self.angle = 190
            if (self.angle >= 195 and self.angle < 205):
                self.angle = 200
            if (self.angle >= 205 and self.angle < 215):
                self.angle = 210
            if (self.angle >= 215 and self.angle < 225):
                self.angle = 220
            if (self.angle >= 225 and self.angle < 235):
                self.angle = 230
            if (self.angle >= 235 and self.angle < 245): # Blue
                self.angle = 240
            if (self.angle >= 245 and self.angle < 255):
                self.angle = 250
            if (self.angle >= 255 and self.angle < 265):
                self.angle = 260
            if (self.angle >= 265 and self.angle < 275):
                self.angle = 270
            if (self.angle >= 275 and self.angle < 285):
                self.angle = 280
            if (self.angle >= 285 and self.angle < 295):
                self.angle = 290
            if (self.angle >= 295 and self.angle < 305): # Magenta
                self.angle = 300
            if (self.angle >= 305 and self.angle < 315):
                self.angle = 310
            if (self.angle >= 315 and self.angle < 325):
                self.angle = 320
            if (self.angle >= 325 and self.angle < 335):
                self.angle = 330
            if (self.angle >= 335 and self.angle < 345):
                self.angle = 340
            if (self.angle >= 345 and self.angle < 355):
                self.angle = 350
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.SIGNAL_HUE_C_VALUE.emit([0])
        # Emit Values within Area
        list = [self.angle/360]
        self.SIGNAL_HUE_C_VALUE.emit(list)
    def CloserTo(self, event):
        if self.harmony_render == "HARMONY":
            if self.harmony_rule == "Monochromatic":
                # Calculate Distances
                h3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.h3_event_x,self.h3_event_y)
                # Confirm to whom it belongs and Emit Signal
                self.harmony_active = 3
                self.SIGNAL_HUE_C_HARMONY_ACTIVE.emit(3)
            if self.harmony_rule == "Complemantary":
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
            if self.harmony_rule == "Analogous":
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
            if self.harmony_rule == "Split Complemantary":
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
            if self.harmony_rule == "Double Split Complemantary":
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
    def drawColors(self, event):
        if self.harmony_render == "COLOR":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            # Path Regions
            outline0 = QPainterPath() # Everything
            outline0.addEllipse(0,0, self.panel_width,self.panel_height)
            value1a = 0.03
            value1b = 1 - (2*value1a)
            outline1 = QPainterPath() # Outter Most Region
            outline1.addEllipse(self.panel_width*value1a,self.panel_height*value1a, self.panel_width*value1b,self.panel_height*value1b)
            value2a = 0.068
            value2b = 1 - (2*value2a)
            outline2 = QPainterPath() # Inner Most Region
            outline2.addEllipse(self.panel_width*value2a,self.panel_height*value2a, self.panel_width*value2b,self.panel_height*value2b)
            value3a = 0.35
            value3b = 1 - (2*value3a)
            outline3 = QPainterPath() # Central Dot
            outline3.addEllipse(self.panel_width*value3a,self.panel_height*value3a, self.panel_width*value3b,self.panel_height*value3b)
            # Dark Border
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            outline02 = outline0.subtracted(outline2)
            painter.drawPath(outline02)
            # Line Gray
            painter.setPen(QPen(QColor(self.gray_contrast), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            line_gray = QPainterPath()
            line_gray.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            line_gray.lineTo(self.circle_x, self.circle_y)
            outline13 = outline1.subtracted(outline3)
            painter.setClipPath(outline13)
            painter.drawPath(line_gray)
            # Hue Gradient
            painter.setPen(QtCore.Qt.NoPen)
            if self.wheel == "CMY":
                hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 180)
                hue.setColorAt(0.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
                hue.setColorAt(0.166, QColor(self.mag[0], self.mag[1], self.mag[2])) # MAGENTA
                hue.setColorAt(0.333, QColor(self.blu[0], self.blu[1], self.blu[2])) # BLUE
                hue.setColorAt(0.500, QColor(self.cya[0], self.cya[1], self.cya[2])) # CYAN
                hue.setColorAt(0.666, QColor(self.gre[0], self.gre[1], self.gre[2])) # GREEN
                hue.setColorAt(0.833, QColor(self.yel[0], self.yel[1], self.yel[2])) # YELLOW
                hue.setColorAt(1.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
            if self.wheel == "RYB":
                hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 210)
                hue.setColorAt(0.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
                hue.setColorAt(0.083, QColor(self.mag[0], self.mag[1], self.mag[2])) # MAGENTA
                hue.setColorAt(0.236, QColor(self.blu[0], self.blu[1], self.blu[2])) # BLUE
                hue.setColorAt(0.394, QColor(self.cya[0], self.cya[1], self.cya[2])) # CYAN
                hue.setColorAt(0.541, QColor(self.gre[0], self.gre[1], self.gre[2])) # GREEN
                hue.setColorAt(0.661, QColor(self.yel[0], self.yel[1], self.yel[2])) # YELLOW
                hue.setColorAt(0.833, QColor(self.ora[0], self.ora[1], self.ora[2])) # ORANGE
                hue.setColorAt(1.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
            painter.setBrush(QBrush(hue))
            outline01 = outline0.subtracted(outline1)
            painter.setClipPath(outline01)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Dark over Hue
            painter.setPen(QPen(QColor(self.gray_natural), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            outline01 = outline0.subtracted(outline1)
            painter.setClipPath(outline01)
            painter.drawLine(self.circle_x,self.circle_y, self.panel_width*0.5,self.panel_height*0.5)
        if self.harmony_render == "HARMONY":
            # Start Qpainter
            painter = QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            # Path Regions
            outline0 = QPainterPath() # Everything
            outline0.addEllipse(0,0, self.panel_width,self.panel_height)
            value1a = 0.03
            value1b = 1 - (2*value1a)
            outline1 = QPainterPath() # Outter Most Region
            outline1.addEllipse(self.panel_width*value1a,self.panel_height*value1a, self.panel_width*value1b,self.panel_height*value1b)
            value2a = 0.068
            value2b = 1 - (2*value2a)
            outline2 = QPainterPath() # Inner Most Region
            outline2.addEllipse(self.panel_width*value2a,self.panel_height*value2a, self.panel_width*value2b,self.panel_height*value2b)
            value3a = 0.35
            value3b = 1 - (2*value3a)
            outline3 = QPainterPath() # Central Dot
            outline3.addEllipse(self.panel_width*value3a,self.panel_height*value3a, self.panel_width*value3b,self.panel_height*value3b)
            # Harmony Gray SPAN Area
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            # Considering the Harmony set Choosen
            if (self.harmony_rule == "Monochromatic" or self.harmony_rule == "Complemantary" or self.harmony_rule == "Analogous"):
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
            if self.harmony_rule == "Split Complemantary":
                # Triangle
                polygon = QPolygon([
                    QPoint(self.h1p_circle_x, self.h1p_circle_y),
                    QPoint(self.h3p_circle_x, self.h3p_circle_y),
                    QPoint(self.h5p_circle_x, self.h5p_circle_y)
                    ])
                painter.drawPolygon(polygon)
            if self.harmony_rule == "Double Split Complemantary":
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
            outline02 = outline0.subtracted(outline2)
            painter.drawPath(outline02)
            # Line Gray
            outline23 = outline2.subtracted(outline3)
            painter.setClipPath(outline23)
            painter.setPen(QPen(QColor(self.gray_contrast), 4, Qt.DotLine, Qt.SquareCap, Qt.MiterJoin))
            line_dots = QPainterPath()
            line_dots.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            line_dots.lineTo(self.h1_circle_x,self.h1_circle_y)
            line_dots.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            line_dots.lineTo(self.h5_circle_x,self.h5_circle_y)
            line_dots.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            line_dots.lineTo(self.h2_circle_x,self.h2_circle_y)
            line_dots.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            line_dots.lineTo(self.h4_circle_x,self.h4_circle_y)
            painter.drawPath(line_dots)
            painter.setPen(QPen(QColor(self.gray_contrast), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            line_gray = QPainterPath()
            line_gray.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            line_gray.lineTo(self.h3_circle_x,self.h3_circle_y)
            painter.drawPath(line_gray)
            # Hue Gradient
            painter.setPen(QtCore.Qt.NoPen)
            if self.wheel == "CMY":
                hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 180)
                hue.setColorAt(0.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
                hue.setColorAt(0.166, QColor(self.mag[0], self.mag[1], self.mag[2])) # MAGENTA
                hue.setColorAt(0.333, QColor(self.blu[0], self.blu[1], self.blu[2])) # BLUE
                hue.setColorAt(0.500, QColor(self.cya[0], self.cya[1], self.cya[2])) # CYAN
                hue.setColorAt(0.666, QColor(self.gre[0], self.gre[1], self.gre[2])) # GREEN
                hue.setColorAt(0.833, QColor(self.yel[0], self.yel[1], self.yel[2])) # YELLOW
                hue.setColorAt(1.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
            if self.wheel == "RYB":
                hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 210)
                hue.setColorAt(0.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
                hue.setColorAt(0.083, QColor(self.mag[0], self.mag[1], self.mag[2])) # MAGENTA
                hue.setColorAt(0.236, QColor(self.blu[0], self.blu[1], self.blu[2])) # BLUE
                hue.setColorAt(0.394, QColor(self.cya[0], self.cya[1], self.cya[2])) # CYAN
                hue.setColorAt(0.541, QColor(self.gre[0], self.gre[1], self.gre[2])) # GREEN
                hue.setColorAt(0.661, QColor(self.yel[0], self.yel[1], self.yel[2])) # YELLOW
                hue.setColorAt(0.833, QColor(self.ora[0], self.ora[1], self.ora[2])) # ORANGE
                hue.setColorAt(1.000, QColor(self.red[0], self.red[1], self.red[2])) # RED
            painter.setBrush(QBrush(hue))
            outline01 = outline0.subtracted(outline1)
            painter.setClipPath(outline01)
            painter.drawRect(0,0, self.panel_width,self.panel_height)
            # Line Dark over Hue
            outline01 = outline0.subtracted(outline1)
            painter.setClipPath(outline01)
            painter.setPen(QPen(QColor(self.gray_natural), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            dark_line = QPainterPath()
            dark_line.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            dark_line.lineTo(self.h1_circle_x,self.h1_circle_y)
            dark_line.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            dark_line.lineTo(self.h2_circle_x,self.h2_circle_y)
            dark_line.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            dark_line.lineTo(self.h3_circle_x,self.h3_circle_y)
            dark_line.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            dark_line.lineTo(self.h4_circle_x,self.h4_circle_y)
            dark_line.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            dark_line.lineTo(self.h5_circle_x,self.h5_circle_y)
            painter.drawPath(dark_line)
            # Harmony Color Edit over Dark Stripe
            outline12 = outline1.subtracted(outline2)
            painter.setClipPath(outline12)
            cs1 = QPainterPath()
            cs1.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            cs1.lineTo(self.h1_circle_x,self.h1_circle_y)
            cs2 = QPainterPath()
            cs2.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            cs2.lineTo(self.h2_circle_x,self.h2_circle_y)
            cs3 = QPainterPath()
            cs3.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            cs3.lineTo(self.h3_circle_x,self.h3_circle_y)
            cs4 = QPainterPath()
            cs4.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            cs4.lineTo(self.h4_circle_x,self.h4_circle_y)
            cs5 = QPainterPath()
            cs5.moveTo(self.panel_width*0.5, self.panel_height*0.5)
            cs5.lineTo(self.h5_circle_x,self.h5_circle_y)
            painter.setPen(QPen(QColor(self.h1_hue[0]*255, self.h1_hue[1]*255, self.h1_hue[2]*255), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawPath(cs1)
            painter.setPen(QPen(QColor(self.h5_hue[0]*255, self.h5_hue[1]*255, self.h5_hue[2]*255), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawPath(cs5)
            painter.setPen(QPen(QColor(self.h2_hue[0]*255, self.h2_hue[1]*255, self.h2_hue[2]*255), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawPath(cs2)
            painter.setPen(QPen(QColor(self.h4_hue[0]*255, self.h4_hue[1]*255, self.h4_hue[2]*255), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawPath(cs4)
            painter.setPen(QPen(QColor(self.h3_hue[0]*255, self.h3_hue[1]*255, self.h3_hue[2]*255), 4, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.drawPath(cs3)

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


class Panel_GAM_Circle(QWidget):
    SIGNAL_GAM_C_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_GAM_C_RELEASE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_GAM_Circle, self).__init__(parent)
        # Module Style
        self.style = Style()
        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Variables(self):
        # Variables
        self.valid = False
        self.input_start = 0
        self.input_var = 0
        self.angle = 0
        self.P1_S1 = []
        self.P1_S3 = []
        self.P1_S4 = []
        self.circle_x = 0
        self.circle_y = 0
        self.panel_width = 0
        self.panel_height = 0
        self.gray_natural = "#000000"
        self.gray_contrast = "#000000"
    def sizeHint(self):
        return QtCore.QSize(5000, 5000)

    # Relay
    def Update_Panel(self,
    gamut_angle,
    P1_S1,
    P1_S3,
    P1_S4,
    P2_S1,
    P3_S3,
    panel_width, panel_height,
    gray_natural, gray_contrast):
        # Points Input (0-1) and Output (0-1)
        self.P1_S1 = [P1_S1[0],P1_S1[1], P1_S1[2],P1_S1[3], P1_S1[4],P1_S1[5], P1_S1[6],P1_S1[7]]
        self.P1_S3 = [P1_S3[0],P1_S3[1], P1_S3[2],P1_S3[3], P1_S3[4],P1_S3[5]]
        self.P1_S4 = [P1_S4[0],P1_S4[1], P1_S4[2],P1_S4[3], P1_S4[4],P1_S4[5], P1_S4[6],P1_S4[7]]
        self.P2_S1 = [
            P2_S1[0],P2_S1[1], P2_S1[2],P2_S1[3], P2_S1[4],P2_S1[5], P2_S1[6],P2_S1[7],
            P2_S1[8],P2_S1[9], P2_S1[10],P2_S1[11], P2_S1[12],P2_S1[13], P2_S1[14],P2_S1[15]]
        self.P3_S3 = [
            P3_S3[0],P3_S3[1],
            P3_S3[2],P3_S3[3], P3_S3[4],P3_S3[5],
            P3_S3[6],P3_S3[7], P3_S3[8],P3_S3[9],
            P3_S3[10],P3_S3[11], P3_S3[12],P3_S3[13]]

        # Angle Rotation
        self.radius = 0.50
        # Panel Geometry
        self.panel_width = panel_width
        self.panel_height = panel_height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        # Compose for Display
        try:
            self.circle_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(gamut_angle)))
            self.circle_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(gamut_angle)))
        except:
            self.circle_x = 0
            self.circle_y = 0

    # Mouse Interaction
    def mousePressEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):
            self.input_start = [event.x(),event.y()]
            dist = math.sqrt( math.pow((self.input_start[0] - self.panel_width*0.5),2) + math.pow((self.input_start[1] - self.panel_height*0.5),2) )
            if dist <= self.panel_width*0.5:
                self.valid = True
            if self.valid == True:
                self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if self.valid == True:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if self.valid == True:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if self.valid == True:
            self.mouseCursor(event)
            self.SIGNAL_GAM_C_RELEASE.emit(0)
            self.valid = False

    def mouseCursor(self, event):
        # Calculations
        self.event_x = event.x()
        self.event_y = event.y()
        # Angles
        self.angle = self.Math_2D_Points_Lines_Angle(
            0,self.panel_height*0.5,
            self.panel_width*0.5,self.panel_height*0.5,
            self.event_x,self.event_y)
        self.input_var = self.Math_2D_Points_Lines_Angle(
            self.input_start[0],self.input_start[1],
            self.panel_width*0.5,self.panel_height*0.5,
            self.event_x,self.event_y)
        # Angle Mofifier Keys
        if event.modifiers() == QtCore.Qt.AltModifier:
            self.angle = 0
        # Masks
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier):
            # Circle
            c1 = [
                ((self.P1_S1[0]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S1[1]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S1[0]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S1[1]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            c2 = [
                ((self.P1_S1[2]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S1[3]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S1[2]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S1[3]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            c3 = [
                ((self.P1_S1[4]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S1[5]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S1[4]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S1[5]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            c4 = [
                ((self.P1_S1[6]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S1[7]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S1[6]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S1[7]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            self.P1_S1 = [
                c1[0],c1[1],
                c2[0],c2[1],
                c3[0],c3[1],
                c4[0],c4[1]]
            # Triangle
            t1 = [
                ((self.P1_S3[0]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S3[1]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S3[0]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S3[1]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            t2 = [
                ((self.P1_S3[2]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S3[3]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S3[2]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S3[3]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            t3 = [
                ((self.P1_S3[4]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S3[5]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S3[4]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S3[5]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            self.P1_S3 = [
                t1[0],t1[1],
                t2[0],t2[1],
                t3[0],t3[1]]
            # Square
            s1 = [
                ((self.P1_S4[0]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S4[1]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S4[0]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S4[1]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            s2 = [
                ((self.P1_S4[2]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S4[3]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S4[2]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S4[3]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            s3 = [
                ((self.P1_S4[4]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S4[5]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S4[4]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S4[5]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            s4 = [
                ((self.P1_S4[6]-0.5)*math.cos(math.radians(self.input_var)) - (self.P1_S4[7]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P1_S4[6]-0.5)*math.sin(math.radians(self.input_var)) + (self.P1_S4[7]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            self.P1_S4 = [
                s1[0],s1[1],
                s2[0],s2[1],
                s3[0],s3[1],
                s4[0],s4[1]]
            # 2 Circles
            cc1 = [
                ((self.P2_S1[0]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[1]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[0]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[1]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc2 = [
                ((self.P2_S1[2]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[3]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[2]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[3]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc3 = [
                ((self.P2_S1[4]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[5]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[4]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[5]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc4 = [
                ((self.P2_S1[6]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[7]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[6]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[7]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc5 = [
                ((self.P2_S1[8]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[9]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[8]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[9]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc6 = [
                ((self.P2_S1[10]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[11]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[10]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[11]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc7 = [
                ((self.P2_S1[12]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[13]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[12]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[13]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            cc8 = [
                ((self.P2_S1[14]-0.5)*math.cos(math.radians(self.input_var)) - (self.P2_S1[15]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P2_S1[14]-0.5)*math.sin(math.radians(self.input_var)) + (self.P2_S1[15]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            self.P2_S1 = [
                cc1[0],cc1[1], cc2[0],cc2[1], cc3[0],cc3[1], cc4[0],cc4[1],
                cc5[0],cc5[1], cc6[0],cc6[1], cc7[0],cc7[1], cc8[0],cc8[1]]
            # 3 Triangles
            ttt1 = [
                ((self.P3_S3[0]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[1]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[0]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[1]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            ttt2 = [
                ((self.P3_S3[2]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[3]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[2]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[3]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            ttt3 = [
                ((self.P3_S3[4]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[5]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[4]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[5]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            ttt4 = [
                ((self.P3_S3[6]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[7]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[6]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[7]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            ttt5 = [
                ((self.P3_S3[8]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[9]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[8]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[9]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            ttt6 = [
                ((self.P3_S3[10]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[11]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[10]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[11]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            ttt7 = [
                ((self.P3_S3[12]-0.5)*math.cos(math.radians(self.input_var)) - (self.P3_S3[13]-0.5)*math.sin(math.radians(self.input_var)))+0.5,
                ((self.P3_S3[12]-0.5)*math.sin(math.radians(self.input_var)) + (self.P3_S3[13]-0.5)*math.cos(math.radians(self.input_var)))+0.5]
            self.P3_S3 = [
                ttt1[0],ttt1[1],
                ttt2[0],ttt2[1], ttt3[0],ttt3[1],
                ttt4[0],ttt4[1], ttt5[0],ttt5[1],
                ttt6[0],ttt6[1], ttt7[0],ttt7[1]]
        # Emit
        self.SIGNAL_GAM_C_VALUE.emit([self.angle, self.P1_S1, self.P1_S3, self.P1_S4, self.P2_S1, self.P3_S3])
        # Compose Line for Widget Display
        try:
            self.circle_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(self.angle)))
            self.circle_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(self.angle)))
        except:
            self.circle_x = 0
            self.circle_y = 0

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # Masking
        value1a = 0.05
        value1b = 1 - (2*value1a)
        circle = QPainterPath()
        circle.addEllipse(0, 0, self.panel_width, self.panel_height)
        circle.addEllipse(self.panel_width*value1a, self.panel_height*value1a, self.panel_width*value1b, self.panel_height*value1b)
        painter.setClipPath(circle)
        # Dark Border
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.gray_natural)))
        painter.drawRect(0,0, self.panel_width,self.panel_height)
        # Line Gray
        painter.setPen(QPen(QColor(self.gray_contrast), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        painter.drawLine(self.circle_x,self.circle_y, self.panel_width*0.5,self.panel_height*0.5)

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
class Panel_GAM_Polygon(QWidget):
    SIGNAL_GAM_P_POINTS = QtCore.pyqtSignal(list)
    SIGNAL_GAM_P_VALUE = QtCore.pyqtSignal(list)
    SIGNAL_GAM_P_RELEASE = QtCore.pyqtSignal(int)
    SIGNAL_GAM_P_COLORS = QtCore.pyqtSignal(list)
    SIGNAL_ZOOM = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Panel_GAM_Polygon, self).__init__(parent)
        # Module Style
        self.style = Style()
        # Start
        self.Cursor()
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def Variables(self):
        # Variables
        self.wheel = "CMY"
        self.modifier = False
        self.nearby = 50
        self.circle = 5
        self.cmy_step = [0, 35/360, 60/360, 120/360, 180/360, 240/360, 300/360, 1]
        self.ryb_step = [0, 60/360, 122/360, 165/360, 218/360, 275/360, 330/360, 1]
        # Colors
        self.cgg = [0,0,0]
        self.c00 = [0,0,0]
        self.c01 = [0,0,0]
        self.c02 = [0,0,0]
        self.c03 = [0,0,0]
        self.c04 = [0,0,0]
        self.c05 = [0,0,0]
        self.c06 = [0,0,0]
        self.c07 = [0,0,0]
        self.c08 = [0,0,0]
        self.c09 = [0,0,0]
        self.c10 = [0,0,0]
        self.c11 = [0,0,0]
        self.c12 = [0,0,0]
        self.c13 = [0,0,0]
        self.c14 = [0,0,0]
        self.c15 = [0,0,0]
        self.c16 = [0,0,0]
        self.c17 = [0,0,0]
        self.c18 = [0,0,0]
        self.c19 = [0,0,0]
        self.c20 = [0,0,0]
        self.c21 = [0,0,0]
        self.c22 = [0,0,0]
        self.c23 = [0,0,0]
        self.c24 = [0,0,0]
        self.c25 = [0,0,0]
        self.c26 = [0,0,0]
        self.c27 = [0,0,0]
        self.c28 = [0,0,0]
        self.c29 = [0,0,0]
        self.c30 = [0,0,0]
        self.c31 = [0,0,0]
        self.c32 = [0,0,0]
        self.c33 = [0,0,0]
        self.c34 = [0,0,0]
        self.c35 = [0,0,0]
        self.c36 = [0,0,0]
        # Gamut Shape
        self.gamut_shape = "None"
        self.P1_S1 = [0,0, 0,0, 0,0, 0,0]
        self.P1_S3 = [0,0, 0,0, 0,0]
        self.P1_S4 = [0,0, 0,0, 0,0, 0,0]
        self.P2_S1 = [0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0,]
        self.P3_S3 = [0,0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0,]
        self.centroid_1 = [0, 0]
        self.centroid_2 = [0, 0]
        # Widget
        self.panel_width = 0
        self.panel_height = 0
        self.hex = '#000000'
        self.gray_natural = "#000000"
        self.gray_contrast = "#000000"
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
    def Update_Panel(self, angle, radius, wheel, cgg, c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c34, c35, c36, gamut_shape, P1_S1, P1_S3, P1_S4, P2_S1, P3_S3, panel_width, panel_height, gray_natural, gray_contrast, hex, zoom):
        # Values
        self.angle = angle * 360
        self.radius = radius
        # Hue Circle Wheel
        self.wheel = wheel
        if self.wheel == "RYB":
            self.angle -= 30
        # Base Colors
        self.cgg = [cgg[0]*255, cgg[1]*255, cgg[2]*255]
        self.c00 = [c00[0]*255, c00[1]*255, c00[2]*255]
        self.c01 = [c01[0]*255, c01[1]*255, c01[2]*255]
        self.c02 = [c02[0]*255, c02[1]*255, c02[2]*255]
        self.c03 = [c03[0]*255, c03[1]*255, c03[2]*255]
        self.c04 = [c04[0]*255, c04[1]*255, c04[2]*255]
        self.c05 = [c05[0]*255, c05[1]*255, c05[2]*255]
        self.c06 = [c06[0]*255, c06[1]*255, c06[2]*255]
        self.c07 = [c07[0]*255, c07[1]*255, c07[2]*255]
        self.c08 = [c08[0]*255, c08[1]*255, c08[2]*255]
        self.c09 = [c09[0]*255, c09[1]*255, c09[2]*255]
        self.c10 = [c10[0]*255, c10[1]*255, c10[2]*255]
        self.c11 = [c11[0]*255, c11[1]*255, c11[2]*255]
        self.c12 = [c12[0]*255, c12[1]*255, c12[2]*255]
        self.c13 = [c13[0]*255, c13[1]*255, c13[2]*255]
        self.c14 = [c14[0]*255, c14[1]*255, c14[2]*255]
        self.c15 = [c15[0]*255, c15[1]*255, c15[2]*255]
        self.c16 = [c16[0]*255, c16[1]*255, c16[2]*255]
        self.c17 = [c17[0]*255, c17[1]*255, c17[2]*255]
        self.c18 = [c18[0]*255, c18[1]*255, c18[2]*255]
        self.c19 = [c19[0]*255, c19[1]*255, c19[2]*255]
        self.c20 = [c20[0]*255, c20[1]*255, c20[2]*255]
        self.c21 = [c21[0]*255, c21[1]*255, c21[2]*255]
        self.c22 = [c22[0]*255, c22[1]*255, c22[2]*255]
        self.c23 = [c23[0]*255, c23[1]*255, c23[2]*255]
        self.c24 = [c24[0]*255, c24[1]*255, c24[2]*255]
        self.c25 = [c25[0]*255, c25[1]*255, c25[2]*255]
        self.c26 = [c26[0]*255, c26[1]*255, c26[2]*255]
        self.c27 = [c27[0]*255, c27[1]*255, c27[2]*255]
        self.c28 = [c28[0]*255, c28[1]*255, c28[2]*255]
        self.c29 = [c29[0]*255, c29[1]*255, c29[2]*255]
        self.c30 = [c30[0]*255, c30[1]*255, c30[2]*255]
        self.c31 = [c31[0]*255, c31[1]*255, c31[2]*255]
        self.c32 = [c32[0]*255, c32[1]*255, c32[2]*255]
        self.c33 = [c33[0]*255, c33[1]*255, c33[2]*255]
        self.c34 = [c34[0]*255, c34[1]*255, c34[2]*255]
        self.c35 = [c35[0]*255, c35[1]*255, c35[2]*255]
        self.c36 = [c36[0]*255, c36[1]*255, c36[2]*255]
        # Polygon
        self.gamut_shape = gamut_shape
        if self.gamut_shape == "None":
            pass
        if self.gamut_shape == "P1_S1":
            self.P1_S1 = [
                P1_S1[0]*panel_width, P1_S1[1]*panel_height,
                P1_S1[2]*panel_width, P1_S1[3]*panel_height,
                P1_S1[4]*panel_width, P1_S1[5]*panel_height,
                P1_S1[6]*panel_width, P1_S1[7]*panel_height]
            self.centroid_1 = self.Math_2D_Centroid_Square(
                P1_S1[0]*panel_width, P1_S1[1]*panel_height,
                P1_S1[2]*panel_width, P1_S1[3]*panel_height,
                P1_S1[4]*panel_width, P1_S1[5]*panel_height,
                P1_S1[6]*panel_width, P1_S1[7]*panel_height)
        if self.gamut_shape == "P1_S3":
            self.P1_S3 = [
                P1_S3[0]*panel_width, P1_S3[1]*panel_height,
                P1_S3[2]*panel_width, P1_S3[3]*panel_height,
                P1_S3[4]*panel_width, P1_S3[5]*panel_height]
            self.centroid_1 = self.Math_2D_Centroid_Triangle(
                P1_S3[0]*panel_width, P1_S3[1]*panel_height,
                P1_S3[2]*panel_width, P1_S3[3]*panel_height,
                P1_S3[4]*panel_width, P1_S3[5]*panel_height)
        if self.gamut_shape == "P1_S4":
            self.P1_S4 = [
                P1_S4[0]*panel_width, P1_S4[1]*panel_height,
                P1_S4[2]*panel_width, P1_S4[3]*panel_height,
                P1_S4[4]*panel_width, P1_S4[5]*panel_height,
                P1_S4[6]*panel_width, P1_S4[7]*panel_height]
            self.centroid_1 = self.Math_2D_Centroid_Square(
                P1_S4[0]*panel_width, P1_S4[1]*panel_height,
                P1_S4[2]*panel_width, P1_S4[3]*panel_height,
                P1_S4[4]*panel_width, P1_S4[5]*panel_height,
                P1_S4[6]*panel_width, P1_S4[7]*panel_height)
        if self.gamut_shape == "P2_S1":
            self.P2_S1 = [
                # 1
                P2_S1[0]*panel_width, P2_S1[1]*panel_height,
                P2_S1[2]*panel_width, P2_S1[3]*panel_height,
                P2_S1[4]*panel_width, P2_S1[5]*panel_height,
                P2_S1[6]*panel_width, P2_S1[7]*panel_height,
                # 2
                P2_S1[8]*panel_width, P2_S1[9]*panel_height,
                P2_S1[10]*panel_width, P2_S1[11]*panel_height,
                P2_S1[12]*panel_width, P2_S1[13]*panel_height,
                P2_S1[14]*panel_width, P2_S1[15]*panel_height]
            self.centroid_1 = self.Math_2D_Centroid_Square(
                P2_S1[0]*panel_width, P2_S1[1]*panel_height,
                P2_S1[2]*panel_width, P2_S1[3]*panel_height,
                P2_S1[4]*panel_width, P2_S1[5]*panel_height,
                P2_S1[6]*panel_width, P2_S1[7]*panel_height)
            self.centroid_2 = self.Math_2D_Centroid_Square(
                P2_S1[8]*panel_width, P2_S1[9]*panel_height,
                P2_S1[10]*panel_width, P2_S1[11]*panel_height,
                P2_S1[12]*panel_width, P2_S1[13]*panel_height,
                P2_S1[14]*panel_width, P2_S1[15]*panel_height)
        if self.gamut_shape == "P3_S3":
            self.P3_S3 = [
                # Center
                P3_S3[0]*panel_width, P3_S3[1]*panel_height,
                # Hexagon
                P3_S3[2]*panel_width, P3_S3[3]*panel_height,
                P3_S3[4]*panel_width, P3_S3[5]*panel_height,
                P3_S3[6]*panel_width, P3_S3[7]*panel_height,
                P3_S3[8]*panel_width, P3_S3[9]*panel_height,
                P3_S3[10]*panel_width, P3_S3[11]*panel_height,
                P3_S3[12]*panel_width, P3_S3[13]*panel_height]
            self.centroid_1 = (P3_S3[0]*panel_width, P3_S3[1]*panel_height)
        # Panel Geometry
        self.panel_width = panel_width
        self.panel_height = panel_height
        # Contrast Value
        self.gray_natural = gray_natural
        self.gray_contrast = gray_contrast
        # Hex
        self.hex = str(hex)
        # Zoom
        self.cursorzoom(zoom)
        # Cursor Location
        try:
            self.value_x = (self.panel_width*0.5) - ((self.panel_width*self.radius*0.5) * math.cos(math.radians(self.angle)))
            self.value_y = (self.panel_height*0.5) - ((self.panel_height*self.radius*0.5) * math.sin(math.radians(self.angle)))
        except:
            self.value_x = 0
            self.value_y = 0
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() / 2), self.value_y-(self.cursor_lmb.height() / 2))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() / 2), self.value_y-(self.cursor_rmb.height() / 2))
        # Change Color
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)

    # Mouse Interaction
    def mousePressEvent(self, event):
        self.origin_x = event.x()
        self.origin_y = event.y()
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.modifier = True
            self.CloserTo(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.mouseHue(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.PinTo(event)
        else:
            self.mouseCursor(event)
    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.modifier = True
            self.CloserTo(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.mouseHue(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.PinTo(event)
        else:
            self.mouseCursor(event)
    def mouseDoubleClickEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.modifier = True
            self.CloserTo(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.mouseHue(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.PinTo(event)
        else:
            self.mouseCursor(event)
    def mouseReleaseEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            self.modifier = True
            self.CloserTo(event)
        elif event.modifiers() == QtCore.Qt.ControlModifier:
            self.mouseHue(event)
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.PinTo(event)
        else:
            self.mouseCursor(event)
        self.modifier = False
        self.cursorzoom(0)
        self.SIGNAL_GAM_P_RELEASE.emit(0)

    def mouseCursor(self, event):
        # Mouse Position
        self.event_x = event.x()
        self.event_y = event.y()
        # Angle
        self.angle = self.Angulus(event, self.event_x, self.event_y)
        # Radius
        self.radius = self.Math_2D_Points_Distance(self.event_x, self.event_y, self.panel_width*0.5, self.panel_height*0.5)
        # Limit Position
        if self.radius <= 0:
            self.angle = 0
            self.radius = 0
        if self.radius >= self.panel_width*0.5:
            self.radius = self.panel_width*0.5
        # Calculate Cursor
        self.value_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(self.angle)))
        self.value_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(self.angle)))
        # Correct Cursor
        if (event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton):
            # Move Cursor
            self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() * 0.5), self.value_y-(self.cursor_lmb.height() * 0.5))
            self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() * 0.5), self.value_y-(self.cursor_rmb.height() * 0.5))
            # Change Color
            self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
            self.cursor_rmb.load(self.array_rmb)
        elif event.buttons() == QtCore.Qt.RightButton:
            self.cursorzoom(1)
        # Emit Values
        try:
            list = ["12", self.angle/360, self.radius/(self.panel_width*0.5), 0]
        except:
            list = ["12", 0, 0, 0]
        self.SIGNAL_GAM_P_VALUE.emit(list)
    def Angulus(self, event, x1, y1):
        if self.wheel == "CMY":
            angulus = 360 - self.Math_2D_Points_Lines_Angle(
                x1, y1,
                self.panel_width*0.5,self.panel_height*0.5,
                0,self.panel_height*0.5)
        if self.wheel == "RYB":
            angulus = 360 - self.Math_2D_Points_Lines_Angle(
                x1, y1,
                self.panel_width*0.5,self.panel_height*0.5,
                0,self.panel_height*0.788675)
        return angulus
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
        values = ["3", 0, 0, self.distance]
        self.SIGNAL_GAM_P_VALUE.emit(values)
    def CloserTo(self, event):
        # Point of Event
        event_x = event.x()
        event_y = event.y()
        # Limit the distance
        distance = self.Math_2D_Points_Distance(self.panel_width*0.5,self.panel_height*0.5, event.x(),event.y())
        if (distance >= self.panel_width * 0.5 or distance >= self.panel_height * 0.5):
            angle = self.Math_2D_Points_Lines_Angle(
                0, self.panel_height * 0.5,
                self.panel_width * 0.5, self.panel_height * 0.5,
                event.x(),event.y())
            event_x = (self.panel_width*0.5) - ((self.panel_width*0.5) * math.cos(math.radians(angle)))
            event_y = (self.panel_height*0.5) - ((self.panel_height*0.5) * math.sin(math.radians(angle)))
        # Point Index of Closest Node
        if self.gamut_shape == "None":
            pass
        if self.gamut_shape == "P1_S1":
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[0],self.P1_S1[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[2],self.P1_S1[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[4],self.P1_S1[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[6],self.P1_S1[7])
            min_dist = min(p1, p2, p3, p4)
            if min_dist < self.nearby:
                if min_dist == p1:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S1", 1, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p2:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S1", 2, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p3:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S1", 3, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p4:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S1", 4, event_x/self.panel_width, event_y/self.panel_height])
        if self.gamut_shape == "P1_S3":
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S3[0],self.P1_S3[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S3[2],self.P1_S3[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S3[4],self.P1_S3[5])
            min_dist = min(p1, p2, p3)
            if min_dist < self.nearby:
                if min_dist == p1:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S3", 1, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p2:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S3", 2, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p3:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S3", 3, event_x/self.panel_width, event_y/self.panel_height])
        if self.gamut_shape == "P1_S4":
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[0],self.P1_S4[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[2],self.P1_S4[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[4],self.P1_S4[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[6],self.P1_S4[7])
            min_dist = min(p1, p2, p3, p4)
            if min_dist < self.nearby:
                if min_dist == p1:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S4", 1, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p2:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S4", 2, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p3:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S4", 3, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p4:
                    self.SIGNAL_GAM_P_POINTS.emit(["P1_S4", 4, event_x/self.panel_width, event_y/self.panel_height])
        if self.gamut_shape == "P2_S1":
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[0],self.P2_S1[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[2],self.P2_S1[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[4],self.P2_S1[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[6],self.P2_S1[7])
            p5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[8],self.P2_S1[9])
            p6 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[10],self.P2_S1[11])
            p7 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[12],self.P2_S1[13])
            p8 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[14],self.P2_S1[15])
            min_dist = min(p1, p2, p3, p4, p5, p6, p7, p8)
            if min_dist < self.nearby:
                if min_dist == p1:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 1, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p2:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 2, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p3:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 3, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p4:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 4, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p5:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 5, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p6:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 6, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p7:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 7, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p8:
                    self.SIGNAL_GAM_P_POINTS.emit(["P2_S1", 8, event_x/self.panel_width, event_y/self.panel_height])
        if self.gamut_shape == "P3_S3":
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[0],self.P3_S3[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[2],self.P3_S3[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[4],self.P3_S3[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[6],self.P3_S3[7])
            p5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[8],self.P3_S3[9])
            p6 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[10],self.P3_S3[11])
            p7 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[12],self.P3_S3[13])
            min_dist = min(p1, p2, p3, p4, p5, p6, p7)
            if min_dist < self.nearby:
                if min_dist == p1:
                    pass
                if min_dist == p2:
                    self.SIGNAL_GAM_P_POINTS.emit(["P3_S3", 2, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p3:
                    self.SIGNAL_GAM_P_POINTS.emit(["P3_S3", 3, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p4:
                    self.SIGNAL_GAM_P_POINTS.emit(["P3_S3", 4, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p5:
                    self.SIGNAL_GAM_P_POINTS.emit(["P3_S3", 5, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p6:
                    self.SIGNAL_GAM_P_POINTS.emit(["P3_S3", 6, event_x/self.panel_width, event_y/self.panel_height])
                if min_dist == p7:
                    self.SIGNAL_GAM_P_POINTS.emit(["P3_S3", 7, event_x/self.panel_width, event_y/self.panel_height])
    def PinTo(self, event):
        # Point of Event
        event_x = event.x()
        event_y = event.y()
        # Gamut Shape
        if self.gamut_shape == "None":
            pass
        if self.gamut_shape == "P1_S1":
            c1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.centroid_1[0], self.centroid_1[1])
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[0],self.P1_S1[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[2],self.P1_S1[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[4],self.P1_S1[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S1[6],self.P1_S1[7])
            min_dist = min(c1, p1, p2, p3, p4)
            if min_dist < self.nearby:
                if min_dist == c1:
                    self.angle = self.Angulus(event, self.centroid_1[0], self.centroid_1[1])
                    self.radius = self.Math_2D_Points_Distance(self.centroid_1[0], self.centroid_1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p1:
                    self.angle = self.Angulus(event, self.P1_S1[0], self.P1_S1[1])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S1[0], self.P1_S1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p2:
                    self.angle = self.Angulus(event, self.P1_S1[2], self.P1_S1[3])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S1[2], self.P1_S1[3], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p3:
                    self.angle = self.Angulus(event, self.P1_S1[4], self.P1_S1[5])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S1[4], self.P1_S1[5], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p4:
                    self.angle = self.Angulus(event, self.P1_S1[6], self.P1_S1[7])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S1[6], self.P1_S1[7], self.panel_width*0.5, self.panel_height*0.5)
        if self.gamut_shape == "P1_S3":
            c1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.centroid_1[0], self.centroid_1[1])
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S3[0],self.P1_S3[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S3[2],self.P1_S3[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S3[4],self.P1_S3[5])
            min_dist = min(c1, p1, p2, p3)
            if min_dist < self.nearby:
                if min_dist == c1:
                    self.angle = self.Angulus(event, self.centroid_1[0], self.centroid_1[1])
                    self.radius = self.Math_2D_Points_Distance(self.centroid_1[0], self.centroid_1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p1:
                    self.angle = self.Angulus(event, self.P1_S3[0], self.P1_S3[1])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S3[0], self.P1_S3[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p2:
                    self.angle = self.Angulus(event, self.P1_S3[2], self.P1_S3[3])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S3[2], self.P1_S3[3], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p3:
                    self.angle = self.Angulus(event, self.P1_S3[4], self.P1_S3[5])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S3[4], self.P1_S3[5], self.panel_width*0.5, self.panel_height*0.5)
        if self.gamut_shape == "P1_S4":
            c1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.centroid_1[0], self.centroid_1[1])
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[0],self.P1_S4[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[2],self.P1_S4[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[4],self.P1_S4[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P1_S4[6],self.P1_S4[7])
            min_dist = min(c1, p1, p2, p3, p4)
            if min_dist < self.nearby:
                if min_dist == c1:
                    self.angle = self.Angulus(event, self.centroid_1[0], self.centroid_1[1])
                    self.radius = self.Math_2D_Points_Distance(self.centroid_1[0], self.centroid_1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p1:
                    self.angle = self.Angulus(event, self.P1_S4[0], self.P1_S4[1])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S4[0], self.P1_S4[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p2:
                    self.angle = self.Angulus(event, self.P1_S4[2], self.P1_S4[3])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S4[2], self.P1_S4[3], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p3:
                    self.angle = self.Angulus(event, self.P1_S4[4], self.P1_S4[5])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S4[4], self.P1_S4[5], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p4:
                    self.angle = self.Angulus(event, self.P1_S4[6], self.P1_S4[7])
                    self.radius = self.Math_2D_Points_Distance(self.P1_S4[6], self.P1_S4[7], self.panel_width*0.5, self.panel_height*0.5)
        if self.gamut_shape == "P2_S1":
            c1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.centroid_1[0], self.centroid_1[1])
            c2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.centroid_2[0], self.centroid_2[1])
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[0],self.P2_S1[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[2],self.P2_S1[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[4],self.P2_S1[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[6],self.P2_S1[7])
            p5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[8],self.P2_S1[9])
            p6 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[10],self.P2_S1[11])
            p7 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[12],self.P2_S1[13])
            p8 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P2_S1[14],self.P2_S1[15])
            min_dist = min(c1, c2, p1, p2, p3, p4, p5, p6, p7, p8)
            if min_dist < self.nearby:
                if min_dist == c1:
                    self.angle = self.Angulus(event, self.centroid_1[0], self.centroid_1[1])
                    self.radius = self.Math_2D_Points_Distance(self.centroid_1[0], self.centroid_1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == c2:
                    self.angle = self.Angulus(event, self.centroid_2[0], self.centroid_2[1])
                    self.radius = self.Math_2D_Points_Distance(self.centroid_2[0], self.centroid_2[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p1:
                    self.angle = self.Angulus(event, self.P2_S1[0], self.P2_S1[1])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[0], self.P2_S1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p2:
                    self.angle = self.Angulus(event, self.P2_S1[2], self.P2_S1[3])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[2], self.P2_S1[3], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p3:
                    self.angle = self.Angulus(event, self.P2_S1[4], self.P2_S1[5])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[4], self.P2_S1[5], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p4:
                    self.angle = self.Angulus(event, self.P2_S1[6], self.P2_S1[7])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[6], self.P2_S1[7], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p5:
                    self.angle = self.Angulus(event, self.P2_S1[8], self.P2_S1[9])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[8], self.P2_S1[9], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p6:
                    self.angle = self.Angulus(event, self.P2_S1[10], self.P2_S1[11])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[10], self.P2_S1[11], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p7:
                    self.angle = self.Angulus(event, self.P2_S1[12], self.P2_S1[13])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[12], self.P2_S1[13], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p8:
                    self.angle = self.Angulus(event, self.P2_S1[14], self.P2_S1[15])
                    self.radius = self.Math_2D_Points_Distance(self.P2_S1[14], self.P2_S1[15], self.panel_width*0.5, self.panel_height*0.5)
        if self.gamut_shape == "P3_S3":
            c1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.centroid_1[0], self.centroid_1[1])
            p1 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[0],self.P3_S3[1])
            p2 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[2],self.P3_S3[3])
            p3 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[4],self.P3_S3[5])
            p4 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[6],self.P3_S3[7])
            p5 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[8],self.P3_S3[9])
            p6 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[10],self.P3_S3[11])
            p7 = self.Math_2D_Points_Distance(event.x(),event.y(), self.P3_S3[12],self.P3_S3[13])
            min_dist = min(c1, p1, p2, p3, p4, p5, p6, p7)
            if min_dist < self.nearby:
                if min_dist == c1:
                    self.angle = self.Angulus(event, self.centroid_1[0], self.centroid_1[1])
                    self.radius = self.Math_2D_Points_Distance(self.centroid_1[0], self.centroid_1[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p1:
                    self.angle = self.Angulus(event, self.P3_S3[0], self.P3_S3[1])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[0], self.P3_S3[1], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p2:
                    self.angle = self.Angulus(event, self.P3_S3[2], self.P3_S3[3])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[2], self.P3_S3[3], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p3:
                    self.angle = self.Angulus(event, self.P3_S3[4], self.P3_S3[5])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[4], self.P3_S3[5], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p4:
                    self.angle = self.Angulus(event, self.P3_S3[6], self.P3_S3[7])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[6], self.P3_S3[7], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p5:
                    self.angle = self.Angulus(event, self.P3_S3[8], self.P3_S3[9])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[8], self.P3_S3[9], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p6:
                    self.angle = self.Angulus(event, self.P3_S3[10], self.P3_S3[11])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[10], self.P3_S3[11], self.panel_width*0.5, self.panel_height*0.5)
                if min_dist == p7:
                    self.angle = self.Angulus(event, self.P3_S3[12], self.P3_S3[13])
                    self.radius = self.Math_2D_Points_Distance(self.P3_S3[12], self.P3_S3[13], self.panel_width*0.5, self.panel_height*0.5)
        # Calculate Cursor
        self.value_x = (self.panel_width*0.5) - ((self.panel_width*self.radius) * math.cos(math.radians(self.angle)))
        self.value_y = (self.panel_height*0.5) - ((self.panel_height*self.radius) * math.sin(math.radians(self.angle)))
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_lmb.width() * 0.5), self.value_y-(self.cursor_lmb.height() * 0.5))
        self.cursor_rmb.move(self.value_x-(self.cursor_rmb.width() * 0.5), self.value_y-(self.cursor_rmb.height() * 0.5))
        # Change Color
        self.array_rmb = self.style.SVG_Cursor_RMB(self.hex)
        self.cursor_rmb.load(self.array_rmb)
        # Emit Values
        list = ["12", self.angle/360, self.radius/(self.panel_width*0.5), 0]
        self.SIGNAL_GAM_P_VALUE.emit(list)

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        # Outter Limit Circle
        outline = QPainterPath()
        outline.addEllipse(0, 0, self.panel_width, self.panel_height)
        painter.setClipPath(outline)

        # Draw Lines for center reference
        painter.setPen(QPen(QColor(self.gray_natural), 5, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        if self.wheel == "CMY":
            lines = QPainterPath()
            lines.moveTo(self.panel_width*0,self.panel_height*0.5)
            lines.lineTo(self.panel_width*1,self.panel_height*0.5)

            lines.moveTo(self.panel_width*0.21132,self.panel_height*0)
            lines.lineTo(self.panel_width*0.78868,self.panel_height*1)

            lines.moveTo(self.panel_width*0.78868,self.panel_height*0)
            lines.lineTo(self.panel_width*0.21132,self.panel_height*1)

            painter.drawPath(lines)
        if self.wheel == "RYB":
            painter.drawLine(self.panel_width*0,self.panel_height*0.78868, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.panel_width*0.51781,self.panel_height*0, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.panel_width*1,self.panel_height*0.00417, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.panel_width*1,self.panel_height*0.57169, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.panel_width*0.73273,self.panel_height*1, self.panel_width*0.5,self.panel_height*0.5)
            painter.drawLine(self.panel_width*0.20993,self.panel_height*1, self.panel_width*0.5,self.panel_height*0.5)

        # Edit Graphical Signal
        if self.modifier == True:
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural),Qt.Dense3Pattern))
            painter.drawRect(0,0, self.panel_width,self.panel_height)

        # Hue Gradient Colors
        painter.setPen(QtCore.Qt.NoPen)
        if self.wheel == "CMY":
            hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 180)
            hue.setColorAt(0.000, QColor(self.c36[0], self.c36[1], self.c36[2])) # RED
            hue.setColorAt(0.027, QColor(self.c35[0], self.c35[1], self.c35[2]))
            hue.setColorAt(0.055, QColor(self.c34[0], self.c34[1], self.c34[2]))
            hue.setColorAt(0.083, QColor(self.c33[0], self.c33[1], self.c33[2]))
            hue.setColorAt(0.111, QColor(self.c32[0], self.c32[1], self.c32[2]))
            hue.setColorAt(0.138, QColor(self.c31[0], self.c31[1], self.c31[2]))
            hue.setColorAt(0.166, QColor(self.c30[0], self.c30[1], self.c30[2])) # Magenta
            hue.setColorAt(0.194, QColor(self.c29[0], self.c29[1], self.c29[2]))
            hue.setColorAt(0.222, QColor(self.c28[0], self.c28[1], self.c28[2]))
            hue.setColorAt(0.250, QColor(self.c27[0], self.c27[1], self.c27[2]))
            hue.setColorAt(0.277, QColor(self.c26[0], self.c26[1], self.c26[2]))
            hue.setColorAt(0.305, QColor(self.c25[0], self.c25[1], self.c25[2]))
            hue.setColorAt(0.333, QColor(self.c24[0], self.c24[1], self.c24[2])) # Blue
            hue.setColorAt(0.361, QColor(self.c23[0], self.c23[1], self.c23[2]))
            hue.setColorAt(0.388, QColor(self.c22[0], self.c22[1], self.c22[2]))
            hue.setColorAt(0.416, QColor(self.c21[0], self.c21[1], self.c21[2]))
            hue.setColorAt(0.444, QColor(self.c20[0], self.c20[1], self.c20[2]))
            hue.setColorAt(0.472, QColor(self.c19[0], self.c19[1], self.c19[2]))
            hue.setColorAt(0.500, QColor(self.c18[0], self.c18[1], self.c18[2])) # Cyan
            hue.setColorAt(0.527, QColor(self.c17[0], self.c17[1], self.c17[2]))
            hue.setColorAt(0.555, QColor(self.c16[0], self.c16[1], self.c16[2]))
            hue.setColorAt(0.583, QColor(self.c15[0], self.c15[1], self.c15[2]))
            hue.setColorAt(0.611, QColor(self.c14[0], self.c14[1], self.c14[2]))
            hue.setColorAt(0.638, QColor(self.c13[0], self.c13[1], self.c13[2]))
            hue.setColorAt(0.666, QColor(self.c12[0], self.c12[1], self.c12[2])) # Green
            hue.setColorAt(0.694, QColor(self.c11[0], self.c11[1], self.c11[2]))
            hue.setColorAt(0.722, QColor(self.c10[0], self.c10[1], self.c10[2]))
            hue.setColorAt(0.750, QColor(self.c09[0], self.c09[1], self.c09[2]))
            hue.setColorAt(0.777, QColor(self.c08[0], self.c08[1], self.c08[2]))
            hue.setColorAt(0.805, QColor(self.c07[0], self.c07[1], self.c07[2]))
            hue.setColorAt(0.833, QColor(self.c06[0], self.c06[1], self.c06[2])) # Yellow
            hue.setColorAt(0.861, QColor(self.c05[0], self.c05[1], self.c05[2]))
            hue.setColorAt(0.888, QColor(self.c04[0], self.c04[1], self.c04[2]))
            hue.setColorAt(0.916, QColor(self.c03[0], self.c03[1], self.c03[2]))
            hue.setColorAt(0.944, QColor(self.c02[0], self.c02[1], self.c02[2]))
            hue.setColorAt(0.972, QColor(self.c01[0], self.c01[1], self.c01[2]))
            hue.setColorAt(1.000, QColor(self.c00[0], self.c00[1], self.c00[2])) # Red
        if self.wheel == "RYB":
            hue = QConicalGradient(QPoint(self.panel_width/2, self.panel_height/2), 210)
            hue.setColorAt(0.000, QColor(self.c36[0], self.c36[1], self.c36[2])) # RED
            hue.setColorAt(0.027, QColor(self.c35[0], self.c35[1], self.c35[2]))
            hue.setColorAt(0.055, QColor(self.c34[0], self.c34[1], self.c34[2]))
            hue.setColorAt(0.083, QColor(self.c33[0], self.c33[1], self.c33[2]))
            hue.setColorAt(0.111, QColor(self.c32[0], self.c32[1], self.c32[2]))
            hue.setColorAt(0.138, QColor(self.c31[0], self.c31[1], self.c31[2]))
            hue.setColorAt(0.166, QColor(self.c30[0], self.c30[1], self.c30[2])) # Magenta
            hue.setColorAt(0.194, QColor(self.c29[0], self.c29[1], self.c29[2]))
            hue.setColorAt(0.222, QColor(self.c28[0], self.c28[1], self.c28[2]))
            hue.setColorAt(0.250, QColor(self.c27[0], self.c27[1], self.c27[2]))
            hue.setColorAt(0.277, QColor(self.c26[0], self.c26[1], self.c26[2]))
            hue.setColorAt(0.305, QColor(self.c25[0], self.c25[1], self.c25[2]))
            hue.setColorAt(0.333, QColor(self.c24[0], self.c24[1], self.c24[2])) # Blue
            hue.setColorAt(0.361, QColor(self.c23[0], self.c23[1], self.c23[2]))
            hue.setColorAt(0.388, QColor(self.c22[0], self.c22[1], self.c22[2]))
            hue.setColorAt(0.416, QColor(self.c21[0], self.c21[1], self.c21[2]))
            hue.setColorAt(0.444, QColor(self.c20[0], self.c20[1], self.c20[2]))
            hue.setColorAt(0.472, QColor(self.c19[0], self.c19[1], self.c19[2]))
            hue.setColorAt(0.500, QColor(self.c18[0], self.c18[1], self.c18[2])) # Cyan
            hue.setColorAt(0.527, QColor(self.c17[0], self.c17[1], self.c17[2]))
            hue.setColorAt(0.555, QColor(self.c16[0], self.c16[1], self.c16[2]))
            hue.setColorAt(0.583, QColor(self.c15[0], self.c15[1], self.c15[2]))
            hue.setColorAt(0.611, QColor(self.c14[0], self.c14[1], self.c14[2]))
            hue.setColorAt(0.638, QColor(self.c13[0], self.c13[1], self.c13[2]))
            hue.setColorAt(0.666, QColor(self.c12[0], self.c12[1], self.c12[2])) # Green
            hue.setColorAt(0.694, QColor(self.c11[0], self.c11[1], self.c11[2]))
            hue.setColorAt(0.722, QColor(self.c10[0], self.c10[1], self.c10[2]))
            hue.setColorAt(0.750, QColor(self.c09[0], self.c09[1], self.c09[2]))
            hue.setColorAt(0.777, QColor(self.c08[0], self.c08[1], self.c08[2]))
            hue.setColorAt(0.805, QColor(self.c07[0], self.c07[1], self.c07[2]))
            hue.setColorAt(0.833, QColor(self.c06[0], self.c06[1], self.c06[2])) # Yellow
            hue.setColorAt(0.861, QColor(self.c05[0], self.c05[1], self.c05[2]))
            hue.setColorAt(0.888, QColor(self.c04[0], self.c04[1], self.c04[2]))
            hue.setColorAt(0.916, QColor(self.c03[0], self.c03[1], self.c03[2]))
            hue.setColorAt(0.944, QColor(self.c02[0], self.c02[1], self.c02[2]))
            hue.setColorAt(0.972, QColor(self.c01[0], self.c01[1], self.c01[2]))
            hue.setColorAt(1.000, QColor(self.c00[0], self.c00[1], self.c00[2])) # Red
        painter.setBrush(QBrush(hue))
        # HUE Gradient Paint Colors
        if self.gamut_shape == "None":
            circle = QPainterPath()
            circle.addEllipse(1, 1, self.panel_width-1, self.panel_height-1)
            # painter.setClipPath(circle)
            painter.drawPath(circle)
        if self.gamut_shape == "P1_S1":
            # Points from User
            P1 = [self.P1_S1[0], self.P1_S1[1]]
            P2 = [self.P1_S1[2], self.P1_S1[3]]
            P3 = [self.P1_S1[4], self.P1_S1[5]]
            P4 = [self.P1_S1[6], self.P1_S1[7]]
            # Angles from the Points
            O1 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P1[0],P1[1])
            O2 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P2[0],P2[1])
            O3 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P3[0],P3[1])
            O4 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P4[0],P4[1])
            # Order Angles in Sequence
            order = [O1, O2, O3, O4]
            angle_order = sorted(order)
            if angle_order[0] == O1:
                AO1 = [P1[0],P1[1]]
                if angle_order[1] == O2:
                    AO2 = [P2[0],P2[1]]
                    if angle_order[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P3[0],P3[1]]
                if angle_order[1] == O3:
                    AO2 = [P3[0],P3[1]]
                    if angle_order[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P2[0],P2[1]]
                if angle_order[1] == O4:
                    AO2 = [P4[0],P4[1]]
                    if angle_order[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P2[0],P2[1]]
            if angle_order[0] == O2:
                AO1 = [P2[0],P2[1]]
                if angle_order[1] == O1:
                    AO2 = [P1[0],P1[1]]
                    if angle_order[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P3[0],P3[1]]
                if angle_order[1] == O3:
                    AO2 = [P3[0],P3[1]]
                    if angle_order[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P1[0],P1[1]]
                if angle_order[1] == O4:
                    AO2 = [P4[0],P4[1]]
                    if angle_order[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P1[0],P1[1]]
            if angle_order[0] == O3:
                AO1 = [P3[0],P3[1]]
                if angle_order[1] == O1:
                    AO2 = [P1[0],P1[1]]
                    if angle_order[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P2[0],P2[1]]
                if angle_order[1] == O2:
                    AO2 = [P2[0],P2[1]]
                    if angle_order[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P1[0],P1[1]]
                if angle_order[1] == O4:
                    AO2 = [P4[0],P4[1]]
                    if angle_order[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P2[0],P2[1]]
                    if angle_order[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P1[0],P1[1]]
            if angle_order[0] == O4:
                AO1 = [P4[0],P4[1]]
                if angle_order[1] == O1:
                    AO2 = [P1[0],P1[1]]
                    if angle_order[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P2[0],P2[1]]
                if angle_order[1] == O2:
                    AO2 = [P2[0],P2[1]]
                    if angle_order[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P1[0],P1[1]]
                if angle_order[1] == O3:
                    AO2 = [P3[0],P3[1]]
                    if angle_order[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P2[0],P2[1]]
                    if angle_order[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P1[0],P1[1]]
            order_correct = [AO1, AO2, AO3, AO4]
            # Point of the Centroid
            PM = self.Math_2D_Points_Lines_Intersection(AO1[0],AO1[1], AO3[0],AO3[1], AO2[0],AO2[1], AO4[0],AO4[1])
            # Bridge Points
            B12 = [self.Math_1D_Lerp(AO1[0],AO2[0],0.5), self.Math_1D_Lerp(AO1[1],AO2[1],0.5)]
            B23 = [self.Math_1D_Lerp(AO2[0],AO3[0],0.5), self.Math_1D_Lerp(AO2[1],AO3[1],0.5)]
            B34 = [self.Math_1D_Lerp(AO3[0],AO4[0],0.5), self.Math_1D_Lerp(AO3[1],AO4[1],0.5)]
            B41 = [self.Math_1D_Lerp(AO4[0],AO1[0],0.5), self.Math_1D_Lerp(AO4[1],AO1[1],0.5)]
            # Bridge Components
            dist_B12 = self.Math_2D_Ortogonal_Components(PM[0],PM[1], B12[0],B12[1])
            dist_B23 = self.Math_2D_Ortogonal_Components(PM[0],PM[1], B23[0],B23[1])
            dist_B34 = self.Math_2D_Ortogonal_Components(PM[0],PM[1], B34[0],B34[1])
            dist_B41 = self.Math_2D_Ortogonal_Components(PM[0],PM[1], B41[0],B41[1])
            # Intermediate Points
            scalar = 2
            P12 = [PM[0]+scalar*dist_B12[0], PM[1]+scalar*dist_B12[1]]
            P23 = [PM[0]+scalar*dist_B23[0], PM[1]+scalar*dist_B23[1]]
            P34 = [PM[0]+scalar*dist_B34[0], PM[1]+scalar*dist_B34[1]]
            P41 = [PM[0]+scalar*dist_B41[0], PM[1]+scalar*dist_B41[1]]
            # Painter Path Object
            path = QPainterPath()
            a = 0.551915024494
            b = 1 - 0.551915024494
            path.moveTo(AO1[0], AO1[1])
            path.cubicTo(
                QPoint( self.Math_1D_Lerp(AO1[0],P12[0],a), self.Math_1D_Lerp(AO1[1],P12[1],a) ),
                QPoint( self.Math_1D_Lerp(P12[0],AO2[0],b), self.Math_1D_Lerp(P12[1],AO2[1],b) ),
                QPoint(AO2[0],AO2[1]))
            path.cubicTo(
                QPoint( self.Math_1D_Lerp(AO2[0],P23[0],a), self.Math_1D_Lerp(AO2[1],P23[1],a) ),
                QPoint( self.Math_1D_Lerp(P23[0],AO3[0],b), self.Math_1D_Lerp(P23[1],AO3[1],b) ),
                QPoint(AO3[0],AO3[1]))
            path.cubicTo(
                QPoint( self.Math_1D_Lerp(AO3[0],P34[0],a), self.Math_1D_Lerp(AO3[1],P34[1],a) ),
                QPoint( self.Math_1D_Lerp(P34[0],AO4[0],b), self.Math_1D_Lerp(P34[1],AO4[1],b) ),
                QPoint(AO4[0],AO4[1]))
            path.cubicTo(
                QPoint( self.Math_1D_Lerp(AO4[0],P41[0],a), self.Math_1D_Lerp(AO4[1],P41[1],a) ),
                QPoint( self.Math_1D_Lerp(P41[0],AO1[0],b), self.Math_1D_Lerp(P41[1],AO1[1],b) ),
                QPoint(AO1[0],AO1[1]))
            painter.drawPath(path)
        if self.gamut_shape == "P1_S3":
            poly = QPolygon([
                QPoint(self.P1_S3[0],self.P1_S3[1]),
                QPoint(self.P1_S3[2],self.P1_S3[3]),
                QPoint(self.P1_S3[4],self.P1_S3[5])
                ])
            painter.drawPolygon(poly)
        if self.gamut_shape == "P1_S4":
            poly = QPolygon([
                QPoint(self.P1_S4[0],self.P1_S4[1]),
                QPoint(self.P1_S4[2],self.P1_S4[3]),
                QPoint(self.P1_S4[4],self.P1_S4[5]),
                QPoint(self.P1_S4[6],self.P1_S4[7])
                ])
            painter.drawPolygon(poly)
        if self.gamut_shape == "P2_S1":
            # Polygon 1
            P1 = [self.P2_S1[0], self.P2_S1[1]]
            P2 = [self.P2_S1[2], self.P2_S1[3]]
            P3 = [self.P2_S1[4], self.P2_S1[5]]
            P4 = [self.P2_S1[6], self.P2_S1[7]]
            # Polygon 2
            P5 = [self.P2_S1[8], self.P2_S1[9]]
            P6 = [self.P2_S1[10], self.P2_S1[11]]
            P7 = [self.P2_S1[12], self.P2_S1[13]]
            P8 = [self.P2_S1[14], self.P2_S1[15]]
            # Angles from Polygon 1
            O1 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P1[0],P1[1])
            O2 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P2[0],P2[1])
            O3 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P3[0],P3[1])
            O4 = self.Math_2D_Points_Lines_Angle(0,self.centroid_1[1], self.centroid_1[0],self.centroid_1[1], P4[0],P4[1])
            # Angles from Polygon 2
            O5 = self.Math_2D_Points_Lines_Angle(0,self.centroid_2[1], self.centroid_2[0],self.centroid_2[1], P5[0],P5[1])
            O6 = self.Math_2D_Points_Lines_Angle(0,self.centroid_2[1], self.centroid_2[0],self.centroid_2[1], P6[0],P6[1])
            O7 = self.Math_2D_Points_Lines_Angle(0,self.centroid_2[1], self.centroid_2[0],self.centroid_2[1], P7[0],P7[1])
            O8 = self.Math_2D_Points_Lines_Angle(0,self.centroid_2[1], self.centroid_2[0],self.centroid_2[1], P8[0],P8[1])
            # order Angles in Sequence for Polygon 1
            order_p1 = [O1, O2, O3, O4]
            angle_order_p1 = sorted(order_p1)
            if angle_order_p1[0] == O1:
                AO1 = [P1[0],P1[1]]
                if angle_order_p1[1] == O2:
                    AO2 = [P2[0],P2[1]]
                    if angle_order_p1[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P3[0],P3[1]]
                if angle_order_p1[1] == O3:
                    AO2 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P2[0],P2[1]]
                if angle_order_p1[1] == O4:
                    AO2 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P2[0],P2[1]]
            if angle_order_p1[0] == O2:
                AO1 = [P2[0],P2[1]]
                if angle_order_p1[1] == O1:
                    AO2 = [P1[0],P1[1]]
                    if angle_order_p1[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P3[0],P3[1]]
                if angle_order_p1[1] == O3:
                    AO2 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P1[0],P1[1]]
                if angle_order_p1[1] == O4:
                    AO2 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P1[0],P1[1]]
            if angle_order_p1[0] == O3:
                AO1 = [P3[0],P3[1]]
                if angle_order_p1[1] == O1:
                    AO2 = [P1[0],P1[1]]
                    if angle_order_p1[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P2[0],P2[1]]
                if angle_order_p1[1] == O2:
                    AO2 = [P2[0],P2[1]]
                    if angle_order_p1[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O4:
                        AO3 = [P4[0],P4[1]]
                        AO4 = [P1[0],P1[1]]
                if angle_order_p1[1] == O4:
                    AO2 = [P4[0],P4[1]]
                    if angle_order_p1[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P2[0],P2[1]]
                    if angle_order_p1[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P1[0],P1[1]]
            if angle_order_p1[0] == O4:
                AO1 = [P4[0],P4[1]]
                if angle_order_p1[1] == O1:
                    AO2 = [P1[0],P1[1]]
                    if angle_order_p1[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P2[0],P2[1]]
                if angle_order_p1[1] == O2:
                    AO2 = [P2[0],P2[1]]
                    if angle_order_p1[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O3:
                        AO3 = [P3[0],P3[1]]
                        AO4 = [P1[0],P1[1]]
                if angle_order_p1[1] == O3:
                    AO2 = [P3[0],P3[1]]
                    if angle_order_p1[2] == O1:
                        AO3 = [P1[0],P1[1]]
                        AO4 = [P2[0],P2[1]]
                    if angle_order_p1[2] == O2:
                        AO3 = [P2[0],P2[1]]
                        AO4 = [P1[0],P1[1]]
            order_correct_p1 = [AO1, AO2, AO3, AO4]
            # order Angles in Sequence for Polygon 2
            order_p2 = [O5, O6, O7, O8]
            angle_order_p2 = sorted(order_p2)
            if angle_order_p2[0] == O5:
                AO5 = [P5[0],P5[1]]
                if angle_order_p2[1] == O6:
                    AO6 = [P6[0],P6[1]]
                    if angle_order_p2[2] == O7:
                        AO7 = [P7[0],P7[1]]
                        AO8 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O8:
                        AO7 = [P8[0],P8[1]]
                        AO8 = [P7[0],P7[1]]
                if angle_order_p2[1] == O7:
                    AO6 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O6:
                        AO7 = [P6[0],P6[1]]
                        AO8 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O8:
                        AO7 = [P8[0],P8[1]]
                        AO8 = [P6[0],P6[1]]
                if angle_order_p2[1] == O8:
                    AO6 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O6:
                        AO7 = [P6[0],P6[1]]
                        AO8 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O7:
                        AO7 = [P7[0],P7[1]]
                        AO8 = [P6[0],P6[1]]
            if angle_order_p2[0] == O6:
                AO5 = [P6[0],P6[1]]
                if angle_order_p2[1] == O5:
                    AO6 = [P5[0],P5[1]]
                    if angle_order_p2[2] == O7:
                        AO7 = [P7[0],P7[1]]
                        AO8 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O8:
                        AO7 = [P8[0],P8[1]]
                        AO8 = [P7[0],P7[1]]
                if angle_order_p2[1] == O7:
                    AO6 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O5:
                        AO7 = [P5[0],P5[1]]
                        AO8 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O8:
                        AO7 = [P8[0],P8[1]]
                        AO8 = [P5[0],P5[1]]
                if angle_order_p2[1] == O8:
                    AO6 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O5:
                        AO7 = [P5[0],P5[1]]
                        AO8 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O7:
                        AO7 = [P7[0],P7[1]]
                        AO8 = [P5[0],P5[1]]
            if angle_order_p2[0] == O7:
                AO5 = [P7[0],P7[1]]
                if angle_order_p2[1] == O5:
                    AO6 = [P5[0],P5[1]]
                    if angle_order_p2[2] == O6:
                        AO7 = [P6[0],P6[1]]
                        AO8 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O8:
                        AO7 = [P8[0],P8[1]]
                        AO8 = [P6[0],P6[1]]
                if angle_order_p2[1] == O6:
                    AO6 = [P6[0],P6[1]]
                    if angle_order_p2[2] == O5:
                        AO7 = [P5[0],P5[1]]
                        AO8 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O8:
                        AO7 = [P8[0],P8[1]]
                        AO8 = [P5[0],P5[1]]
                if angle_order_p2[1] == O8:
                    AO6 = [P8[0],P8[1]]
                    if angle_order_p2[2] == O5:
                        AO7 = [P5[0],P5[1]]
                        AO8 = [P6[0],P6[1]]
                    if angle_order_p2[2] == O6:
                        AO7 = [P6[0],P6[1]]
                        AO8 = [P5[0],P5[1]]
            if angle_order_p2[0] == O8:
                AO5 = [P8[0],P8[1]]
                if angle_order_p2[1] == O5:
                    AO6 = [P5[0],P5[1]]
                    if angle_order_p2[2] == O6:
                        AO7 = [P6[0],P6[1]]
                        AO8 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O7:
                        AO7 = [P7[0],P7[1]]
                        AO8 = [P6[0],P6[1]]
                if angle_order_p2[1] == O6:
                    AO6 = [P6[0],P6[1]]
                    if angle_order_p2[2] == O5:
                        AO7 = [P5[0],P5[1]]
                        AO8 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O7:
                        AO7 = [P7[0],P7[1]]
                        AO8 = [P5[0],P5[1]]
                if angle_order_p2[1] == O7:
                    AO6 = [P7[0],P7[1]]
                    if angle_order_p2[2] == O5:
                        AO7 = [P5[0],P5[1]]
                        AO8 = [P6[0],P6[1]]
                    if angle_order_p2[2] == O6:
                        AO7 = [P6[0],P6[1]]
                        AO8 = [P5[0],P5[1]]
            order_correct_p2 = [AO5, AO6, AO7, AO8]
            # Point of the Centroid 1
            PM1 = self.Math_2D_Points_Lines_Intersection(AO1[0],AO1[1], AO3[0],AO3[1], AO2[0],AO2[1], AO4[0],AO4[1])
            # Point of the Centroid 2
            PM2 = self.Math_2D_Points_Lines_Intersection(AO5[0],AO5[1], AO7[0],AO7[1], AO6[0],AO6[1], AO8[0],AO8[1])
            # Bridge Points of Polygon 1
            B12 = [self.Math_1D_Lerp(AO1[0],AO2[0],0.5), self.Math_1D_Lerp(AO1[1],AO2[1],0.5)]
            B23 = [self.Math_1D_Lerp(AO2[0],AO3[0],0.5), self.Math_1D_Lerp(AO2[1],AO3[1],0.5)]
            B34 = [self.Math_1D_Lerp(AO3[0],AO4[0],0.5), self.Math_1D_Lerp(AO3[1],AO4[1],0.5)]
            B41 = [self.Math_1D_Lerp(AO4[0],AO1[0],0.5), self.Math_1D_Lerp(AO4[1],AO1[1],0.5)]
            # Bridge Points of Polygon 2
            B56 = [self.Math_1D_Lerp(AO5[0],AO6[0],0.5), self.Math_1D_Lerp(AO5[1],AO6[1],0.5)]
            B67 = [self.Math_1D_Lerp(AO6[0],AO7[0],0.5), self.Math_1D_Lerp(AO6[1],AO7[1],0.5)]
            B78 = [self.Math_1D_Lerp(AO7[0],AO8[0],0.5), self.Math_1D_Lerp(AO7[1],AO8[1],0.5)]
            B85 = [self.Math_1D_Lerp(AO8[0],AO5[0],0.5), self.Math_1D_Lerp(AO8[1],AO5[1],0.5)]
            # Bridge Components Polygon 1
            dist_B12 = self.Math_2D_Ortogonal_Components(PM1[0],PM1[1], B12[0],B12[1])
            dist_B23 = self.Math_2D_Ortogonal_Components(PM1[0],PM1[1], B23[0],B23[1])
            dist_B34 = self.Math_2D_Ortogonal_Components(PM1[0],PM1[1], B34[0],B34[1])
            dist_B41 = self.Math_2D_Ortogonal_Components(PM1[0],PM1[1], B41[0],B41[1])
            # Bridge Components Polygon 1
            dist_B56 = self.Math_2D_Ortogonal_Components(PM2[0],PM2[1], B56[0],B56[1])
            dist_B67 = self.Math_2D_Ortogonal_Components(PM2[0],PM2[1], B67[0],B67[1])
            dist_B78 = self.Math_2D_Ortogonal_Components(PM2[0],PM2[1], B78[0],B78[1])
            dist_B85 = self.Math_2D_Ortogonal_Components(PM2[0],PM2[1], B85[0],B85[1])
            # Intermediate Points for Polygon 1
            scalar = 2
            P12 = [PM1[0]+scalar*dist_B12[0], PM1[1]+scalar*dist_B12[1]]
            P23 = [PM1[0]+scalar*dist_B23[0], PM1[1]+scalar*dist_B23[1]]
            P34 = [PM1[0]+scalar*dist_B34[0], PM1[1]+scalar*dist_B34[1]]
            P41 = [PM1[0]+scalar*dist_B41[0], PM1[1]+scalar*dist_B41[1]]
            # Intermediate Points for Polygon 2
            scalar = 2
            P56 = [PM2[0]+scalar*dist_B56[0], PM2[1]+scalar*dist_B56[1]]
            P67 = [PM2[0]+scalar*dist_B67[0], PM2[1]+scalar*dist_B67[1]]
            P78 = [PM2[0]+scalar*dist_B78[0], PM2[1]+scalar*dist_B78[1]]
            P85 = [PM2[0]+scalar*dist_B85[0], PM2[1]+scalar*dist_B85[1]]
            # Painter Path Object for Polygon 1
            path_p1 = QPainterPath()
            a = 0.551915024494
            b = 1 - 0.551915024494
            path_p1.moveTo(AO1[0], AO1[1])
            path_p1.cubicTo(
                QPoint( self.Math_1D_Lerp(AO1[0],P12[0],a), self.Math_1D_Lerp(AO1[1],P12[1],a) ),
                QPoint( self.Math_1D_Lerp(P12[0],AO2[0],b), self.Math_1D_Lerp(P12[1],AO2[1],b) ),
                QPoint(AO2[0],AO2[1]))
            path_p1.cubicTo(
                QPoint( self.Math_1D_Lerp(AO2[0],P23[0],a), self.Math_1D_Lerp(AO2[1],P23[1],a) ),
                QPoint( self.Math_1D_Lerp(P23[0],AO3[0],b), self.Math_1D_Lerp(P23[1],AO3[1],b) ),
                QPoint(AO3[0],AO3[1]))
            path_p1.cubicTo(
                QPoint( self.Math_1D_Lerp(AO3[0],P34[0],a), self.Math_1D_Lerp(AO3[1],P34[1],a) ),
                QPoint( self.Math_1D_Lerp(P34[0],AO4[0],b), self.Math_1D_Lerp(P34[1],AO4[1],b) ),
                QPoint(AO4[0],AO4[1]))
            path_p1.cubicTo(
                QPoint( self.Math_1D_Lerp(AO4[0],P41[0],a), self.Math_1D_Lerp(AO4[1],P41[1],a) ),
                QPoint( self.Math_1D_Lerp(P41[0],AO1[0],b), self.Math_1D_Lerp(P41[1],AO1[1],b) ),
                QPoint(AO1[0],AO1[1]))
            # Painter Path Object for Polygon 2
            path_p2 = QPainterPath()
            a = 0.551915024494
            b = 1 - 0.551915024494
            path_p2.moveTo(AO5[0], AO5[1])
            path_p2.cubicTo(
                QPoint( self.Math_1D_Lerp(AO5[0],P56[0],a), self.Math_1D_Lerp(AO5[1],P56[1],a) ),
                QPoint( self.Math_1D_Lerp(P56[0],AO6[0],b), self.Math_1D_Lerp(P56[1],AO6[1],b) ),
                QPoint(AO6[0],AO6[1]))
            path_p2.cubicTo(
                QPoint( self.Math_1D_Lerp(AO6[0],P67[0],a), self.Math_1D_Lerp(AO6[1],P67[1],a) ),
                QPoint( self.Math_1D_Lerp(P67[0],AO7[0],b), self.Math_1D_Lerp(P67[1],AO7[1],b) ),
                QPoint(AO7[0],AO7[1]))
            path_p2.cubicTo(
                QPoint( self.Math_1D_Lerp(AO7[0],P78[0],a), self.Math_1D_Lerp(AO7[1],P78[1],a) ),
                QPoint( self.Math_1D_Lerp(P78[0],AO8[0],b), self.Math_1D_Lerp(P78[1],AO8[1],b) ),
                QPoint(AO8[0],AO8[1]))
            path_p2.cubicTo(
                QPoint( self.Math_1D_Lerp(AO8[0],P85[0],a), self.Math_1D_Lerp(AO8[1],P85[1],a) ),
                QPoint( self.Math_1D_Lerp(P85[0],AO5[0],b), self.Math_1D_Lerp(P85[1],AO5[1],b) ),
                QPoint(AO5[0],AO5[1]))
            # Draw Paths
            painter.drawPath(path_p1)
            painter.drawPath(path_p2)
        if self.gamut_shape == "P3_S3":
            rect = QRect(0,0,self.panel_width,self.panel_height)
            ang_a1 = 16 * self.Math_2D_Points_Lines_Angle(
                self.P3_S3[2], self.P3_S3[3],
                self.panel_width*0.5, self.panel_height*0.5,
                self.panel_width, self.panel_height*0.5
                )
            ang_a2 = -16 * self.Math_2D_Points_Lines_Angle(
                self.P3_S3[2], self.P3_S3[3],
                self.panel_width*0.5, self.panel_height*0.5,
                self.P3_S3[4], self.P3_S3[5]
                )
            ang_b1 = 16 * self.Math_2D_Points_Lines_Angle(
                self.P3_S3[6], self.P3_S3[7],
                self.panel_width*0.5, self.panel_height*0.5,
                self.panel_width, self.panel_height*0.5
                )
            ang_b2 = -16 * self.Math_2D_Points_Lines_Angle(
                self.P3_S3[6], self.P3_S3[7],
                self.panel_width*0.5, self.panel_height*0.5,
                self.P3_S3[8], self.P3_S3[9]
                )
            ang_c1 = 16 * self.Math_2D_Points_Lines_Angle(
                self.P3_S3[10], self.P3_S3[11],
                self.panel_width*0.5, self.panel_height*0.5,
                self.panel_width, self.panel_height*0.5
                )
            ang_c2 = -16 * self.Math_2D_Points_Lines_Angle(
                self.P3_S3[10], self.P3_S3[11],
                self.panel_width*0.5, self.panel_height*0.5,
                self.P3_S3[12], self.P3_S3[13]
                )
            # Pies
            painter.drawPie(rect, ang_a1, ang_a2)
            painter.drawPie(rect, ang_b1, ang_b2)
            painter.drawPie(rect, ang_c1, ang_c2)

        # Inner Gray And Mask Primeries Colors
        painter.setPen(QtCore.Qt.NoPen)
        gray = QRadialGradient(QPointF(self.panel_width/2, self.panel_height/2), self.panel_width/2)
        gray.setColorAt(0.000, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 255))

        # gray.setColorAt(0.100, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 253))
        # gray.setColorAt(0.200, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 247))
        # gray.setColorAt(0.300, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 236))
        # gray.setColorAt(0.400, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 221))
        # gray.setColorAt(0.500, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 199))
        # gray.setColorAt(0.600, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 172))
        # gray.setColorAt(0.700, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 138))
        # gray.setColorAt(0.800, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 98))
        # gray.setColorAt(0.900, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 52))

        gray.setColorAt(1.000, QColor(self.cgg[0], self.cgg[1], self.cgg[2], 0))
        painter.setBrush(QBrush(gray))

        # Render new



        # Gamut Shapes
        if self.gamut_shape == "None":
            mask = QPolygon([
                QPoint(0, 0),
                QPoint(self.panel_width, 0),
                QPoint(self.panel_width, self.panel_height),
                QPoint(0, self.panel_height)
                ])
            painter.drawPolygon(mask)
        if self.gamut_shape == "P1_S1":
            # Grey Polygon
            painter.drawPath(path)
            # Display Subjective Primaries
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            painter.drawEllipse(self.centroid_1[0]-self.circle, self.centroid_1[1]-self.circle, self.circle*2,self.circle*2)
            painter.setBrush(QBrush(QColor(self.gray_contrast)))
            painter.drawEllipse(self.P1_S1[0]-self.circle, self.P1_S1[1]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S1[2]-self.circle, self.P1_S1[3]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S1[4]-self.circle, self.P1_S1[5]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S1[6]-self.circle, self.P1_S1[7]-self.circle, self.circle*2,self.circle*2)
        if self.gamut_shape == "P1_S3":
            # Grey Polygon
            painter.drawPolygon(poly)
            # Display Subjective Primaries
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            painter.drawEllipse(self.centroid_1[0]-self.circle, self.centroid_1[1]-self.circle, self.circle*2,self.circle*2)
            painter.setBrush(QBrush(QColor(self.gray_contrast)))
            painter.drawEllipse(self.P1_S3[0]-self.circle, self.P1_S3[1]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S3[2]-self.circle, self.P1_S3[3]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S3[4]-self.circle, self.P1_S3[5]-self.circle, self.circle*2,self.circle*2)
        if self.gamut_shape == "P1_S4":
            # Grey Polygon
            painter.drawPolygon(poly)
            # Display Subjective Primaries
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            painter.drawEllipse(self.centroid_1[0]-self.circle, self.centroid_1[1]-self.circle, self.circle*2,self.circle*2)
            painter.setBrush(QBrush(QColor(self.gray_contrast)))
            painter.drawEllipse(self.P1_S4[0]-self.circle, self.P1_S4[1]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S4[2]-self.circle, self.P1_S4[3]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S4[4]-self.circle, self.P1_S4[5]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P1_S4[6]-self.circle, self.P1_S4[7]-self.circle, self.circle*2,self.circle*2)
        if self.gamut_shape == "P2_S1":
            # Grey Polygon
            painter.drawPath(path_p1)
            painter.drawPath(path_p2)
            # Display Subjective Primaries
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            painter.drawEllipse(self.centroid_1[0]-self.circle, self.centroid_1[1]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.centroid_2[0]-self.circle, self.centroid_2[1]-self.circle, self.circle*2,self.circle*2)
            painter.setBrush(QBrush(QColor(self.gray_contrast)))
            painter.drawEllipse(self.P2_S1[0]-self.circle, self.P2_S1[1]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[2]-self.circle, self.P2_S1[3]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[4]-self.circle, self.P2_S1[5]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[6]-self.circle, self.P2_S1[7]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[8]-self.circle, self.P2_S1[9]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[10]-self.circle, self.P2_S1[11]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[12]-self.circle, self.P2_S1[13]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P2_S1[14]-self.circle, self.P2_S1[15]-self.circle, self.circle*2,self.circle*2)
        if self.gamut_shape == "P3_S3":
            # Grey Polygon
            painter.drawPie(rect, ang_a1, ang_a2)
            painter.drawPie(rect, ang_b1, ang_b2)
            painter.drawPie(rect, ang_c1, ang_c2)
            # Display Subjective Primaries Polygon 1
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.gray_natural)))
            painter.drawEllipse(self.P3_S3[0]-self.circle, self.P3_S3[1]-self.circle, self.circle*2,self.circle*2)
            painter.setBrush(QBrush(QColor(self.gray_contrast)))
            painter.drawEllipse(self.P3_S3[2]-self.circle, self.P3_S3[3]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P3_S3[4]-self.circle, self.P3_S3[5]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P3_S3[6]-self.circle, self.P3_S3[7]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P3_S3[8]-self.circle, self.P3_S3[9]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P3_S3[10]-self.circle, self.P3_S3[11]-self.circle, self.circle*2,self.circle*2)
            painter.drawEllipse(self.P3_S3[12]-self.circle, self.P3_S3[13]-self.circle, self.circle*2,self.circle*2)

    # Trignometry
    def Math_1D_Loop(self, var):
        if var <= 0:
            var += 1
        if var >= 1:
            var -= 1
        return var
    def Math_1D_Lerp(self, v0, v1, t):
        return (v0+t*(v1-v0))
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
    def Math_2D_Centroid_Triangle(self, a1, a2, b1, b2, c1, c2):
        cx = (a1+b1+c1)/3
        cy = (a2+b2+c2)/3
        return [cx, cy]
    def Math_2D_Centroid_Square(self, a1, a2, b1, b2, c1, c2, d1, d2):
        cx = (a1+b1+c1+d1)/4
        cy = (a2+b2+c2+d2)/4
        return [cx, cy]
    def Math_2D_Ortogonal_Components(self, x1, y1, x2, y2):
        # x1,y1 is the origin
        delta_x = x2 - x1
        delta_y = y2 - y1
        return [delta_x, delta_y]


class Panel_DOT(QWidget):
    # works in 0-255 color range
    SIGNAL_DOT_COLOR = QtCore.pyqtSignal(list)
    SIGNAL_DOT_CURSOR = QtCore.pyqtSignal(list)
    SIGNAL_DOT_RELEASE = QtCore.pyqtSignal(int)

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
        # Dots (20 x 20)
        self.size = 15
        self.margin = 5
        self.max_colors = 20 # 20
        self.max_white = 10 # 10
        self.max_black = 10 # 10

    # Relay
    def Location(self, location_x, location_y, width, height):
        # Input
        self.value_x = (width*0.5) + location_x
        self.value_y = (height*0.5) + location_y
        self.panel_width = width
        self.panel_height = height
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))
    def Update_Panel(self, dot_1, dot_2, dot_3, dot_4, dim_hor, dim_ver, width, height):
        # Dot Colors
        self.dot_1 = [dot_1[0], dot_1[1]*255, dot_1[2]*255, dot_1[3]*255]
        self.dot_2 = [dot_2[0], dot_2[1]*255, dot_2[2]*255, dot_2[3]*255]
        self.dot_3 = [dot_3[0], dot_3[1]*255, dot_3[2]*255, dot_3[3]*255]
        self.dot_4 = [dot_4[0], dot_4[1]*255, dot_4[2]*255, dot_4[3]*255]
        # Dot Dimensions
        self.max_colors = dim_hor
        self.max_white = dim_ver
        self.max_black = dim_ver
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
        self.SIGNAL_DOT_COLOR.emit([self.value_x, self.value_y])
        self.SIGNAL_DOT_CURSOR.emit([self.value_x - (self.panel_width*0.5), self.value_y - (self.panel_height*0.5)])

    # Paint
    def paintEvent(self, event):
        self.drawColors(event)
    def drawColors(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        # Clipping Mask
        region0 = QRegion(0,0, self.panel_width,self.panel_height) # Everything
        painter.setClipRegion(region0)
        # Circle
        painter.setPen(QtCore.Qt.NoPen)
        origin_x = (self.panel_width * 0.5) - (((self.max_colors+1) * self.size) + ((self.max_colors) * self.margin)) * 0.5
        origin_y = (self.panel_height * 0.5) - (((self.max_colors+1) * self.size) + ((self.max_colors) * self.margin)) * 0.5
        # Color Gradient
        for i in range(self.max_colors+1):
            rgb = self.Color_Transform(i, self.max_colors, [self.dot_1[1], self.dot_1[2], self.dot_1[3]], [self.dot_2[1], self.dot_2[2], self.dot_2[3]])
            painter.setBrush(QBrush(QColor(rgb[0], rgb[1], rgb[2])))
            point_x = origin_x + (i*self.size + i*self.margin)
            point_y = (self.panel_height*0.5 - self.size*0.5)
            painter.drawRect(point_x,point_y, self.size,self.size)
            # Black Gradient
            for b in range(1, self.max_black+1):
                black = self.Color_Transform(b, self.max_black, [rgb[0], rgb[1], rgb[2]], [self.dot_3[1], self.dot_3[2], self.dot_3[3]])
                painter.setBrush(QBrush(QColor(black[0], black[1], black[2])))
                black_y = point_y + (b*self.size + b*self.margin)
                painter.drawRect(point_x,black_y, self.size,self.size)
            # White Gradient
            for w in range(1, self.max_white+1):
                white = self.Color_Transform(w, self.max_white, [rgb[0], rgb[1], rgb[2]], [self.dot_4[1], self.dot_4[2], self.dot_4[3]])
                painter.setBrush(QBrush(QColor(white[0], white[1], white[2])))
                white_y = point_y - (w*self.size + w*self.margin)
                painter.drawRect(point_x,white_y, self.size,self.size)
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
    SIGNAL_OBJ_COLOR = QtCore.pyqtSignal(list)
    SIGNAL_OBJ_CURSOR = QtCore.pyqtSignal(list)
    SIGNAL_OBJ_RELEASE = QtCore.pyqtSignal(list)

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
        self.SIGNAL_OBJ_COLOR.emit([self.value_x, self.value_y])
        self.SIGNAL_OBJ_CURSOR.emit([self.value_x - (self.panel_width*0.5), self.value_y - (self.panel_height*0.5)])


class Panel_IMG(QWidget):
    SIGNAL_IMG_COLOR = QtCore.pyqtSignal(list)
    SIGNAL_IMG_CLEAN = QtCore.pyqtSignal(int)
    SIGNAL_IMG_RELEASE = QtCore.pyqtSignal(list)
    SIGNAL_IMG_DRAGDROP = QtCore.pyqtSignal(list)

    # Init
    def __init__(self, parent):
        super(Panel_IMG, self).__init__(parent)

        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        # Accept Drops
        self.setAcceptDrops(True)
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
        self.value_x = location_x
        self.value_y = location_y
        self.panel_width = width
        self.panel_height = height
        # Move Cursor
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))

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
        self.SIGNAL_IMG_RELEASE.emit([self.value_x, self.value_y])

    def mouseCursor(self, event):
        # Event
        self.value_x = event.x()
        self.value_y = event.y()
        # Mouse Position
        self.cursor_lmb.move(self.value_x-(self.cursor_size / 2), self.value_y-(self.cursor_size / 2))
        self.cursor_lmb.resize(self.scale, self.scale)
        # Emit values
        self.SIGNAL_IMG_COLOR.emit([self.value_x, self.value_y])
        # Clean Image to Default
        if ((event.buttons() == QtCore.Qt.LeftButton or event.buttons() == QtCore.Qt.MiddleButton or event.buttons() == QtCore.Qt.RightButton) and (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier)):
            self.SIGNAL_IMG_CLEAN.emit(0)

    # Drag and Drop Interaction
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            self.SIGNAL_IMG_DRAGDROP.emit(["ENTER", 0])
            event.accept()
        else:
            event.ignore()
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            self.SIGNAL_IMG_DRAGDROP.emit(["MOVE", 0])
            event.accept()
        else:
            event.ignore()
    def dragLeaveEvent(self, event):
        self.SIGNAL_IMG_DRAGDROP.emit(["LEAVE", 0])
        event.accept()
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.SIGNAL_IMG_DRAGDROP.emit(["DROP", file_path])
            event.accept()
        else:
            event.ignore()


class Channel_Percent(QWidget):

    def __init__(self, parent):
        super(Channel_Percent, self).__init__(parent)
        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000,20)
    def Variables(self):
        # Theme for the Buttons
        self.gray_contrast = QColor('#d4d4d4')
        # Values
        self.render = False

        self.aaa_1 = [False, 0]
        self.rgb_1 = [False, 0]
        self.rgb_2 = [False, 0]
        self.rgb_3 = [False, 0]
        self.cmy_1 = [False, 0]
        self.cmy_2 = [False, 0]
        self.cmy_3 = [False, 0]
        self.cmyk_1 = [False, 0]
        self.cmyk_2 = [False, 0]
        self.cmyk_3 = [False, 0]
        self.cmyk_4 = [False, 0]
        self.ryb_1 = [False, 0]
        self.ryb_2 = [False, 0]
        self.ryb_3 = [False, 0]
        self.yuv_1 = [False, 0]
        self.yuv_2 = [False, 0]
        self.yuv_3 = [False, 0]
        self.kkk_1 = [False, 0]

        self.ard_1 = [False, 0]
        self.ard_2 = [False, 0]
        self.ard_3 = [False, 0]
        self.hsv_1 = [False, 0]
        self.hsv_2 = [False, 0]
        self.hsv_3 = [False, 0]
        self.hsl_1 = [False, 0]
        self.hsl_2 = [False, 0]
        self.hsl_3 = [False, 0]
        self.hcy_1 = [False, 0]
        self.hcy_2 = [False, 0]
        self.hcy_3 = [False, 0]

        self.xyz_1 = [False, 0]
        self.xyz_2 = [False, 0]
        self.xyz_3 = [False, 0]
        self.xyy_1 = [False, 0]
        self.xyy_2 = [False, 0]
        self.xyy_3 = [False, 0]
        self.lab_1 = [False, 0]
        self.lab_2 = [False, 0]
        self.lab_3 = [False, 0]

    # Relay
    def Setup(self, render):
        self.render = render
    def Update(self, aaa_1, rgb_1,rgb_2,rgb_3, cmy_1,cmy_2,cmy_3, cmyk_1,cmyk_2,cmyk_3,cmyk_4, ryb_1,ryb_2,ryb_3, yuv_1,yuv_2,yuv_3, kkk_1, ard_1,ard_2,ard_3, hsv_1,hsv_2,hsv_3, hsl_1,hsl_2,hsl_3, hcy_1,hcy_2,hcy_3, xyz_1,xyz_2,xyz_3, xyy_1,xyy_2,xyy_3, lab_1,lab_2,lab_3, gray_contrast,channel_width):
        # Update the variables (Bolean, Value)
        self.aaa_1 = [aaa_1[0], aaa_1[1]]

        self.rgb_1 = [rgb_1[0], rgb_1[1]]
        self.rgb_2 = [rgb_2[0], rgb_2[1]]
        self.rgb_3 = [rgb_3[0], rgb_3[1]]

        self.cmy_1 = [cmy_1[0], cmy_1[1]]
        self.cmy_2 = [cmy_2[0], cmy_2[1]]
        self.cmy_3 = [cmy_3[0], cmy_3[1]]

        self.cmyk_1 = [cmyk_1[0], cmyk_1[1]]
        self.cmyk_2 = [cmyk_2[0], cmyk_2[1]]
        self.cmyk_3 = [cmyk_3[0], cmyk_3[1]]
        self.cmyk_4 = [cmyk_4[0], cmyk_4[1]]

        self.ryb_1 = [ryb_1[0], ryb_1[1]]
        self.ryb_2 = [ryb_2[0], ryb_2[1]]
        self.ryb_3 = [ryb_3[0], ryb_3[1]]

        self.yuv_1 = [yuv_1[0], yuv_1[1]]
        self.yuv_2 = [yuv_2[0], yuv_2[1]]
        self.yuv_3 = [yuv_3[0], yuv_3[1]]

        self.kkk_1 = [kkk_1[0], kkk_1[1]]

        self.ard_1 = [ard_1[0], ard_1[1]]
        self.ard_2 = [ard_2[0], ard_2[1]]
        self.ard_3 = [ard_3[0], ard_3[1]]

        self.hsv_1 = [hsv_1[0], hsv_1[1]]
        self.hsv_2 = [hsv_2[0], hsv_2[1]]
        self.hsv_3 = [hsv_3[0], hsv_3[1]]

        self.hsl_1 = [hsl_1[0], hsl_1[1]]
        self.hsl_2 = [hsl_2[0], hsl_2[1]]
        self.hsl_3 = [hsl_3[0], hsl_3[1]]

        self.hcy_1 = [hcy_1[0], hcy_1[1]]
        self.hcy_2 = [hcy_2[0], hcy_2[1]]
        self.hcy_3 = [hcy_3[0], hcy_3[1]]

        self.xyz_1 = [xyz_1[0], xyz_1[1]]
        self.xyz_2 = [xyz_2[0], xyz_2[1]]
        self.xyz_3 = [xyz_3[0], xyz_3[1]]

        self.xyy_1 = [xyy_1[0], xyy_1[1]]
        self.xyy_2 = [xyy_2[0], xyy_2[1]]
        self.xyy_3 = [xyy_3[0], xyy_3[1]]

        self.lab_1 = [lab_1[0], lab_1[1]]
        self.lab_2 = [lab_2[0], lab_2[1]]
        self.lab_3 = [lab_3[0], lab_3[1]]

        self.gray_contrast = QColor(gray_contrast)
        self.channel_width = channel_width

    # Paint Style
    def paintEvent(self, event):
        self.drawCursor(event)
    def drawCursor(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Pen
        painter.setPen(QPen(self.gray_contrast, 1, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        # Cursors
        if self.render == True:
            if self.aaa_1[0] == True:
                value_x = self.aaa_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.rgb_1[0] == True:
                value_x = self.rgb_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.rgb_1[0] == True:
                value_x = self.rgb_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.rgb_1[0] == True:
                value_x = self.rgb_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.cmy_1[0] == True:
                value_x = self.cmy_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.cmy_1[0] == True:
                value_x = self.cmy_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.cmy_1[0] == True:
                value_x = self.cmy_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.cmyk_1[0] == True:
                value_x = self.cmyk_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.cmyk_1[0] == True:
                value_x = self.cmyk_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.cmyk_1[0] == True:
                value_x = self.cmyk_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.cmyk_4[0] == True:
                value_x = self.cmyk_4[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.ryb_1[0] == True:
                value_x = self.ryb_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.ryb_1[0] == True:
                value_x = self.ryb_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.ryb_1[0] == True:
                value_x = self.ryb_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.yuv_1[0] == True:
                value_x = self.yuv_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.yuv_1[0] == True:
                value_x = self.yuv_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.yuv_1[0] == True:
                value_x = self.yuv_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.kkk_1[0] == True:
                value_x = self.kkk_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)


            if self.ard_1[0] == True:
                value_x = self.ard_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.ard_1[0] == True:
                value_x = self.ard_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.ard_1[0] == True:
                value_x = self.ard_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.hsv_1[0] == True:
                value_x = self.hsv_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.hsv_1[0] == True:
                value_x = self.hsv_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.hsv_1[0] == True:
                value_x = self.hsv_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.hsl_1[0] == True:
                value_x = self.hsl_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.hsl_1[0] == True:
                value_x = self.hsl_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.hsl_1[0] == True:
                value_x = self.hsl_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.hcy_1[0] == True:
                value_x = self.hcy_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.hcy_1[0] == True:
                value_x = self.hcy_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.hcy_1[0] == True:
                value_x = self.hcy_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)


            if self.xyz_1[0] == True:
                value_x = self.xyz_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.xyz_1[0] == True:
                value_x = self.xyz_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.xyz_1[0] == True:
                value_x = self.xyz_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.xyy_1[0] == True:
                value_x = self.xyy_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.xyy_1[0] == True:
                value_x = self.xyy_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.xyy_1[0] == True:
                value_x = self.xyy_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)

            if self.lab_1[0] == True:
                value_x = self.lab_1[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.lab_1[0] == True:
                value_x = self.lab_2[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
            if self.lab_1[0] == True:
                value_x = self.lab_3[1] * self.channel_width
                painter.drawLine(value_x, -10, value_x, 35)
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
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000,20)
    def Variables(self):
        # Variables
        self.width = 1
        self.channel_padding = 2
        self.cursor_width = 6
        self.value_x = 0
        self.valid = True
        # Theme for the Buttons
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
        # Colors
        self.s00 = [0*255, 0*255, 0*255]
        self.s05 = [0.05*255, 0.05*255, 0.05*255]
        self.s10 = [0.10*255, 0.10*255, 0.10*255]
        self.s15 = [0.15*255, 0.15*255, 0.15*255]
        self.s20 = [0.20*255, 0.20*255, 0.20*255]
        self.s25 = [0.25*255, 0.25*255, 0.25*255]
        self.s30 = [0.30*255, 0.30*255, 0.30*255]
        self.s35 = [0.35*255, 0.35*255, 0.35*255]
        self.s40 = [0.40*255, 0.40*255, 0.40*255]
        self.s45 = [0.45*255, 0.45*255, 0.45*255]
        self.s50 = [0.50*255, 0.50*255, 0.50*255]
        self.s55 = [0.55*255, 0.55*255, 0.55*255]
        self.s60 = [0.60*255, 0.60*255, 0.60*255]
        self.s65 = [0.65*255, 0.65*255, 0.65*255]
        self.s70 = [0.70*255, 0.70*255, 0.70*255]
        self.s75 = [0.75*255, 0.75*255, 0.75*255]
        self.s80 = [0.80*255, 0.80*255, 0.80*255]
        self.s85 = [0.85*255, 0.85*255, 0.85*255]
        self.s90 = [0.90*255, 0.90*255, 0.90*255]
        self.s95 = [0.95*255, 0.95*255, 0.95*255]
        self.sAA = [1*255, 1*255, 1*255]
        # Hues
        self.red = [1*255, 0*255, 0*255]
        self.yellow = [1*255, 1*255, 0*255]
        self.green = [0*255, 1*255, 0*255]
        self.cyan = [0*255, 1*255, 1*255]
        self.blue = [0*255, 0*255, 1*255]
        self.magenta = [1*255, 0*255, 1*255]
        self.red2 = [1*255, 0*255, 0*255]
        # SetUp
        self.mode = None
        self.blocks = 4
        self.cursor = "DIAMOND_1"

    # Relay
    def Setup(self, mode, blocks, cursor):
        self.mode = mode
        self.blocks = blocks
        self.cursor = cursor
    def Update(self, value, channel_width):
        # Update the variables
        self.channel_width = channel_width
        self.value_x = value * self.channel_width
        # Limit Range
        if self.value_x <= 0:
            self.value_x = 0
        if self.value_x >= self.channel_width:
            self.value_x = self.channel_width
    def Colors(self, stops):
        # Slider Background
        self.s00 = [stops[0][0]*255, stops[0][1]*255, stops[0][2]*255]
        self.s05 = [stops[1][0]*255, stops[1][1]*255, stops[1][2]*255]
        self.s10 = [stops[2][0]*255, stops[2][1]*255, stops[2][2]*255]
        self.s15 = [stops[3][0]*255, stops[3][1]*255, stops[3][2]*255]
        self.s20 = [stops[4][0]*255, stops[4][1]*255, stops[4][2]*255]
        self.s25 = [stops[5][0]*255, stops[5][1]*255, stops[5][2]*255]
        self.s30 = [stops[6][0]*255, stops[6][1]*255, stops[6][2]*255]
        self.s35 = [stops[7][0]*255, stops[7][1]*255, stops[7][2]*255]
        self.s40 = [stops[8][0]*255, stops[8][1]*255, stops[8][2]*255]
        self.s45 = [stops[9][0]*255, stops[9][1]*255, stops[9][2]*255]
        self.s50 = [stops[10][0]*255, stops[10][1]*255, stops[10][2]*255]
        self.s55 = [stops[11][0]*255, stops[11][1]*255, stops[11][2]*255]
        self.s60 = [stops[12][0]*255, stops[12][1]*255, stops[12][2]*255]
        self.s65 = [stops[13][0]*255, stops[13][1]*255, stops[13][2]*255]
        self.s70 = [stops[14][0]*255, stops[14][1]*255, stops[14][2]*255]
        self.s75 = [stops[15][0]*255, stops[15][1]*255, stops[15][2]*255]
        self.s80 = [stops[16][0]*255, stops[16][1]*255, stops[16][2]*255]
        self.s85 = [stops[17][0]*255, stops[17][1]*255, stops[17][2]*255]
        self.s90 = [stops[18][0]*255, stops[18][1]*255, stops[18][2]*255]
        self.s95 = [stops[19][0]*255, stops[19][1]*255, stops[19][2]*255]
        self.sAA = [stops[20][0]*255, stops[20][1]*255, stops[20][2]*255]
    def Hues(self, red, yellow, green, cyan, blue, magenta, red2):
        self.red = [red[0]*255, red[1]*255, red[2]*255]
        self.yellow = [yellow[0]*255, yellow[1]*255, yellow[2]*255]
        self.green = [green[0]*255, green[1]*255, green[2]*255]
        self.cyan = [cyan[0]*255, cyan[1]*255, cyan[2]*255]
        self.blue = [blue[0]*255, blue[1]*255, blue[2]*255]
        self.magenta = [magenta[0]*255, magenta[1]*255, magenta[2]*255]
        self.red2 = [red2[0]*255, red2[1]*255, red2[2]*255]
    def Valid(self, valid):
        self.valid = valid

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
        self.drawCursor(event)
    def drawCursor(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Available Space Calculations
        self.width = event.rect().width()
        channel_height = event.rect().height()
        channel_middle = (channel_height / 2)

        # Background
        if self.mode != "NEU":
            # Backdrop Gray
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.color_dark)))
            painter.drawRect(0,0, self.width, channel_height)

            # Gradient Display
            painter.setPen(QtCore.Qt.NoPen)
            grad = QLinearGradient(0, 0, self.width, 0)
            if (self.blocks == "4" or self.blocks == "6"):
                grad.setColorAt(0.000, QColor(self.s00[0], self.s00[1], self.s00[2], 255)) # Color Left
                grad.setColorAt(0.050, QColor(self.s05[0], self.s05[1], self.s05[2], 255))
                grad.setColorAt(0.100, QColor(self.s10[0], self.s10[1], self.s10[2], 255))
                grad.setColorAt(0.150, QColor(self.s15[0], self.s15[1], self.s15[2], 255))
                grad.setColorAt(0.200, QColor(self.s20[0], self.s20[1], self.s20[2], 255))
                grad.setColorAt(0.250, QColor(self.s25[0], self.s25[1], self.s25[2], 255))
                grad.setColorAt(0.300, QColor(self.s30[0], self.s30[1], self.s30[2], 255))
                grad.setColorAt(0.350, QColor(self.s35[0], self.s35[1], self.s35[2], 255))
                grad.setColorAt(0.400, QColor(self.s40[0], self.s40[1], self.s40[2], 255))
                grad.setColorAt(0.450, QColor(self.s45[0], self.s45[1], self.s45[2], 255))
                grad.setColorAt(0.500, QColor(self.s50[0], self.s50[1], self.s50[2], 255))
                grad.setColorAt(0.550, QColor(self.s55[0], self.s55[1], self.s55[2], 255))
                grad.setColorAt(0.600, QColor(self.s60[0], self.s60[1], self.s60[2], 255))
                grad.setColorAt(0.650, QColor(self.s65[0], self.s65[1], self.s65[2], 255))
                grad.setColorAt(0.700, QColor(self.s70[0], self.s70[1], self.s70[2], 255))
                grad.setColorAt(0.750, QColor(self.s75[0], self.s75[1], self.s75[2], 255))
                grad.setColorAt(0.800, QColor(self.s80[0], self.s80[1], self.s80[2], 255))
                grad.setColorAt(0.850, QColor(self.s85[0], self.s85[1], self.s85[2], 255))
                grad.setColorAt(0.900, QColor(self.s90[0], self.s90[1], self.s90[2], 255))
                grad.setColorAt(0.950, QColor(self.s95[0], self.s95[1], self.s95[2], 255))
                grad.setColorAt(1.000, QColor(self.sAA[0], self.sAA[1], self.sAA[2], 255)) # Color Right
            if self.blocks == "HUE":
                grad.setColorAt(0.000, QColor(self.red[0], self.red[1], self.red[2], 255)) # Color Left
                grad.setColorAt(0.166, QColor(self.yellow[0], self.yellow[1], self.yellow[2], 255))
                grad.setColorAt(0.333, QColor(self.green[0], self.green[1], self.green[2], 255))
                grad.setColorAt(0.500, QColor(self.cyan[0], self.cyan[1], self.cyan[2], 255))
                grad.setColorAt(0.666, QColor(self.blue[0], self.blue[1], self.blue[2], 255))
                grad.setColorAt(0.833, QColor(self.magenta[0], self.magenta[1], self.magenta[2], 255))
                grad.setColorAt(1.000, QColor(self.red2[0], self.red2[1], self.red2[2], 255)) # Color Right
            painter.setBrush(QBrush(grad))
            painter.drawRect(1,1, self.width-2, channel_height-2)

        # value if it is out of scope
        if self.valid == False:
            painter.setBrush(QBrush(QColor('#a10820')))
            painter.drawRect(0, 0, self.channel_width, 30)

        # Draw Cursor
        if self.cursor == "NEU":
            # Cursor Amount Square
            top = 0
            bot = channel_height
            polygon = QPolygon([
                QPoint(self.value_x, top),
                QPoint(0, top),
                QPoint(0, bot),
                QPoint(self.value_x, bot)
                ])
            # Brush and Pen
            painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.setBrush(QBrush(self.color_light))
            painter.drawPolygon(polygon)
        if self.cursor == "DIAMOND_1":
            # Cursor Diamond
            diamond_dist = 7
            left = self.value_x - diamond_dist
            right = self.value_x + diamond_dist
            top = channel_middle - diamond_dist
            bot = channel_middle + diamond_dist
            mid = channel_middle
            polygon = QPolygon([
                QPoint(self.value_x, top),
                QPoint(left, mid),
                QPoint(self.value_x, bot),
                QPoint(right, mid)
                ])
            # Brush and Pen
            painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.setBrush(QBrush(self.color_light))
            painter.drawPolygon(polygon)
        if self.cursor == "DIAMOND_2": # urzeye
            # Cursor Diamond
            diamond_dist = 8
            left = self.value_x - diamond_dist
            right = self.value_x + diamond_dist
            top = channel_middle - diamond_dist
            bot = channel_middle + diamond_dist
            mid = channel_middle
            polygon = QPolygon([
                QPoint(self.value_x, top),
                QPoint(left, mid),
                QPoint(self.value_x, bot),
                QPoint(right, mid)
                ])
            # Brush and Pen
            painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPolygon(polygon)
        if self.cursor == "LINE":
            # Cursor Diamond
            dist = 2
            left = self.value_x - dist
            right = self.value_x + dist
            top = 0
            bot = channel_height
            polygon = QPolygon([
                QPoint(left, top),
                QPoint(left, bot),
                QPoint(right, bot),
                QPoint(right, top),
                ])
            # Brush and Pen
            painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
            painter.setBrush(QBrush(self.color_light))
            painter.drawPolygon(polygon)


class Clicks(QWidget):
    SIGNAL_APPLY = QtCore.pyqtSignal(int)
    SIGNAL_SAVE = QtCore.pyqtSignal(int)
    SIGNAL_CLEAN = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Clicks, self).__init__(parent)
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
    def mouseDoubleClickEvent(self, event):
        self.SIGNAL_APPLY.emit(0)


class Mixer_Linear(QWidget):
    SIGNAL_MIXER_VALUE = QtCore.pyqtSignal(int)
    SIGNAL_MIXER_RELEASE = QtCore.pyqtSignal(int)

    # Init
    def __init__(self, parent):
        super(Mixer_Linear, self).__init__(parent)
        # Start
        self.Variables()
        # Size Hint Expand
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
    def sizeHint(self):
        return QtCore.QSize(5000,15)
    def Variables(self):
        # Variables
        self.value_x = None
        # Theme for the Buttons
        self.color_dark = QColor('#383838')
        self.color_light = QColor('#d4d4d4')
        # Colors
        self.s00 = [0*255, 0*255, 0*255]
        self.s05 = [0.05*255, 0.05*255, 0.05*255]
        self.s10 = [0.10*255, 0.10*255, 0.10*255]
        self.s15 = [0.15*255, 0.15*255, 0.15*255]
        self.s20 = [0.20*255, 0.20*255, 0.20*255]
        self.s25 = [0.25*255, 0.25*255, 0.25*255]
        self.s30 = [0.30*255, 0.30*255, 0.30*255]
        self.s35 = [0.35*255, 0.35*255, 0.35*255]
        self.s40 = [0.40*255, 0.40*255, 0.40*255]
        self.s45 = [0.45*255, 0.45*255, 0.45*255]
        self.s50 = [0.50*255, 0.50*255, 0.50*255]
        self.s55 = [0.55*255, 0.55*255, 0.55*255]
        self.s60 = [0.60*255, 0.60*255, 0.60*255]
        self.s65 = [0.65*255, 0.65*255, 0.65*255]
        self.s70 = [0.70*255, 0.70*255, 0.70*255]
        self.s75 = [0.75*255, 0.75*255, 0.75*255]
        self.s80 = [0.80*255, 0.80*255, 0.80*255]
        self.s85 = [0.85*255, 0.85*255, 0.85*255]
        self.s90 = [0.90*255, 0.90*255, 0.90*255]
        self.s95 = [0.95*255, 0.95*255, 0.95*255]
        self.sAA = [1*255, 1*255, 1*255]
        # Color Display
        self.color = True

    # Relay
    def Update(self, value, width):
        # Update the variables
        self.channel_width = width
        # Spin value range to slider range
        self.value_x = value * self.channel_width
    def Colors(self, color, stops):
        self.color = color
        if self.color == True:
            self.s00 = [stops[0][0]*255, stops[0][1]*255, stops[0][2]*255]
            self.s05 = [stops[1][0]*255, stops[1][1]*255, stops[1][2]*255]
            self.s10 = [stops[2][0]*255, stops[2][1]*255, stops[2][2]*255]
            self.s15 = [stops[3][0]*255, stops[3][1]*255, stops[3][2]*255]
            self.s20 = [stops[4][0]*255, stops[4][1]*255, stops[4][2]*255]
            self.s25 = [stops[5][0]*255, stops[5][1]*255, stops[5][2]*255]
            self.s30 = [stops[6][0]*255, stops[6][1]*255, stops[6][2]*255]
            self.s35 = [stops[7][0]*255, stops[7][1]*255, stops[7][2]*255]
            self.s40 = [stops[8][0]*255, stops[8][1]*255, stops[8][2]*255]
            self.s45 = [stops[9][0]*255, stops[9][1]*255, stops[9][2]*255]
            self.s50 = [stops[10][0]*255, stops[10][1]*255, stops[10][2]*255]
            self.s55 = [stops[11][0]*255, stops[11][1]*255, stops[11][2]*255]
            self.s60 = [stops[12][0]*255, stops[12][1]*255, stops[12][2]*255]
            self.s65 = [stops[13][0]*255, stops[13][1]*255, stops[13][2]*255]
            self.s70 = [stops[14][0]*255, stops[14][1]*255, stops[14][2]*255]
            self.s75 = [stops[15][0]*255, stops[15][1]*255, stops[15][2]*255]
            self.s80 = [stops[16][0]*255, stops[16][1]*255, stops[16][2]*255]
            self.s85 = [stops[17][0]*255, stops[17][1]*255, stops[17][2]*255]
            self.s90 = [stops[18][0]*255, stops[18][1]*255, stops[18][2]*255]
            self.s95 = [stops[19][0]*255, stops[19][1]*255, stops[19][2]*255]
            self.sAA = [stops[20][0]*255, stops[20][1]*255, stops[20][2]*255]

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
        else:
            self.Emit_Value(event)
        self.SIGNAL_MIXER_RELEASE.emit(0)

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
        self.width = event.rect().width()
        # Draw Elements
        self.drawCursor(event)
    def drawCursor(self, event):
        # Start Qpainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.color == True:
            # Backdrop Gray
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QBrush(QColor(self.color_dark)))
            painter.drawRect(0,0, self.width, 15)

            # Gradient Display
            painter.setPen(QtCore.Qt.NoPen)
            grad = QLinearGradient(0, 0, self.width, 0)
            grad.setColorAt(0.000, QColor(self.s00[0], self.s00[1], self.s00[2], 255)) # Color Left
            grad.setColorAt(0.050, QColor(self.s05[0], self.s05[1], self.s05[2], 255))
            grad.setColorAt(0.100, QColor(self.s10[0], self.s10[1], self.s10[2], 255))
            grad.setColorAt(0.150, QColor(self.s15[0], self.s15[1], self.s15[2], 255))
            grad.setColorAt(0.200, QColor(self.s20[0], self.s20[1], self.s20[2], 255))
            grad.setColorAt(0.250, QColor(self.s25[0], self.s25[1], self.s25[2], 255))
            grad.setColorAt(0.300, QColor(self.s30[0], self.s30[1], self.s30[2], 255))
            grad.setColorAt(0.350, QColor(self.s35[0], self.s35[1], self.s35[2], 255))
            grad.setColorAt(0.400, QColor(self.s40[0], self.s40[1], self.s40[2], 255))
            grad.setColorAt(0.450, QColor(self.s45[0], self.s45[1], self.s45[2], 255))
            grad.setColorAt(0.500, QColor(self.s50[0], self.s50[1], self.s50[2], 255))
            grad.setColorAt(0.550, QColor(self.s55[0], self.s55[1], self.s55[2], 255))
            grad.setColorAt(0.600, QColor(self.s60[0], self.s60[1], self.s60[2], 255))
            grad.setColorAt(0.650, QColor(self.s65[0], self.s65[1], self.s65[2], 255))
            grad.setColorAt(0.700, QColor(self.s70[0], self.s70[1], self.s70[2], 255))
            grad.setColorAt(0.750, QColor(self.s75[0], self.s75[1], self.s75[2], 255))
            grad.setColorAt(0.800, QColor(self.s80[0], self.s80[1], self.s80[2], 255))
            grad.setColorAt(0.850, QColor(self.s85[0], self.s85[1], self.s85[2], 255))
            grad.setColorAt(0.900, QColor(self.s90[0], self.s90[1], self.s90[2], 255))
            grad.setColorAt(0.950, QColor(self.s95[0], self.s95[1], self.s95[2], 255))
            grad.setColorAt(1.000, QColor(self.sAA[0], self.sAA[1], self.sAA[2], 255)) # Color Right
            painter.setBrush(QBrush(grad))
            painter.drawRect(1,1, self.width-2, 15-2)

        # Cursor
        tri = 8
        bot = 15-3
        top = bot - tri
        left = self.value_x - tri
        right = self.value_x + tri
        triangle = QPolygon([
            QPoint(self.value_x, top),
            QPoint(left, bot),
            QPoint(right, bot)])
        painter.setPen(QPen(self.color_dark, 2, Qt.SolidLine))
        painter.setBrush(QBrush(self.color_light))
        painter.drawPolygon(triangle)


class Dialog_UI(QDialog):

    def __init__(self, parent):
        super(Dialog_UI, self).__init__(parent)
        # Load UI for Dialog
        self.dir_name = str(os.path.dirname(os.path.realpath(__file__)))
        uic.loadUi(self.dir_name + '/pigment_o_settings.ui', self)


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
