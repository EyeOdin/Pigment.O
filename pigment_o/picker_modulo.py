# Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer and Color Sampler.
# Copyright ( C ) 2020  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# ( at your option ) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#region Imports

# Krita Module
from krita import *
# PyQt5 Modules
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# Picker
from .engine_constants import *
from .engine_calculations import *

#endregion
#region Variables

cursor_black = QColor( "#000000" )
cursor_white = QColor( "#ffffff" )

#endregion


#region Shared

# Region
def Circles( px, py, side ):
    # Circle 0 ( Everything )
    v0a = 0.01
    v0b = 1 - ( 2*v0a )
    circle_0 = QPainterPath()
    circle_0.addEllipse( int( px + side * v0a ), int( py + side * v0a ), int( side * v0b ), int( side * v0b ) )
    # Circle 1 ( Outter Most Region )
    v1a = 0.033
    v1b = 1 - ( 2*v1a )
    circle_1 = QPainterPath()
    circle_1.addEllipse( int( px + side * v1a ), int( py + side * v1a ), int( side * v1b ), int( side * v1b ) )
    # Circle 2 ( Inner Most Region )
    v2a = 0.066
    v2b = 1 - ( 2*v2a )
    circle_2 = QPainterPath()
    circle_2.addEllipse( int( px + side * v2a ), int( py + side * v2a ), int( side * v2b ), int( side * v2b ) )
    # Circle 3 ( Central Dot )
    v3a = 0.13
    v3b = 1 - ( 2*v3a )
    circle_3 = QPainterPath()
    circle_3.addEllipse( int( px + side * v3a ), int( py + side * v3a ), int( side * v3b ), int( side * v3b ) )
    # Return
    return circle_0, circle_1, circle_2, circle_3
# Cursor
def Cursor_Display( self, painter ):
    # Variables
    size_normal = 10
    size_zoom = 100
    margin_size = 10
    # Switch
    if self.zoom == True:   Cursor_Zoom( painter, int( self.ex ), int( self.ey ), size_zoom, margin_size, self.hex_code )
    else:                   Cursor_Normal( painter, int( self.ex ), int( self.ey ), size_normal )
def Cursor_Normal( painter, ex, ey, size1 ):
    # Variables
    w1 = 2
    w2 = int( w1 * 2 )
    w4 = int( w1 * 4 )
    size2 = int( size1 * 2 )
    # Mask
    mask = QPainterPath()
    mask.addEllipse( 
        int( ex - size1 ),
        int( ey - size1 ),
        int( size2 ),
        int( size2 ),
        )
    mask.addEllipse( 
        int( ex - size1 + w2 ),
        int( ey - size1 + w2 ),
        int( size2 - w4 ),
        int( size2 - w4 ),
        )
    painter.setClipPath( mask )
    # Black Circle
    painter.setPen( QtCore.Qt.NoPen )
    painter.setBrush( QBrush( cursor_black ) )
    painter.drawEllipse( 
        int( ex - size1 ),
        int( ey - size1 ),
        int( size2 ),
        int( size2 ),
        )
    # White Circle
    painter.setPen( QtCore.Qt.NoPen )
    painter.setBrush( QBrush( cursor_white ) )
    painter.drawEllipse( 
        int( ex - size1 + w1 ),
        int( ey - size1 + w1 ),
        int( size2 - w2 ),
        int( size2 - w2 ),
        )
def Cursor_Zoom( painter, ex, ey, size_zoom, margin_size, hex_code ):
    # Border
    painter.setPen( QtCore.Qt.NoPen )
    painter.setBrush( QBrush( cursor_black ) )
    painter.drawEllipse( 
        int( ex - size_zoom ),
        int( ey - size_zoom ),
        int( size_zoom * 2 ),
        int( size_zoom * 2 ),
        )
    # Hex Color
    painter.setBrush( QBrush( QColor( hex_code ) ) )
    painter.drawEllipse( 
        int( ex - size_zoom + margin_size ),
        int( ey - size_zoom + margin_size ),
        int( size_zoom * 2 - margin_size * 2 ),
        int( size_zoom * 2 - margin_size * 2 ),
        )
# Wheel
def Wheel_Angle( mode, color ):
    if mode == "DIGITAL":   angle = color["hue_d"] * 360
    if mode == "ANALOG":    angle = color["hue_a"] * 360 - hue_a
    return angle

#endregion
#region Header

class Color_Header( QWidget ):
    SIGNAL_SWAP = QtCore.pyqtSignal()
    SIGNAL_SHOW = QtCore.pyqtSignal( str )
    SIGNAL_RANDOM = QtCore.pyqtSignal()
    SIGNAL_COMP = QtCore.pyqtSignal()

    # Init
    def __init__( self, parent ):
        super( Color_Header, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 100
        self.hh = 40
        # Variables
        self.mode = "FG" # "FG" "BG"
        self.progress_bar = 1
        # Other
        self.state_other = False
        self.state_vector = 0
        self.other_ui = 80
        self.other_a = self.other_ui
        self.other_b = self.ww - self.other_ui
        # Colors HEX
        self.f1 = QBrush( QColor( '#000000' ) )
        self.f2 = QBrush( QColor( '#000000' ) )
        self.b1 = QBrush( QColor( '#ffffff' ) )
        self.b2 = QBrush( QColor( '#ffffff' ) )
        self.pen = QColor( '#000000' )
        self.brush = QColor( '#ffffff' )
    # Relay
    def Set_Size( self, ww, hh ):
        # widget
        self.ww = ww
        self.hh = hh
        # Limits
        if ww <= 200:
            self.other_a = ww * 0.4
            self.other_b = ww * 0.7
        else:
            self.other_a = self.other_ui
            self.other_b = ww - self.other_ui
        # Update
        self.resize( ww, hh )
    def Set_Color_F1( self, f1 ):
        self.f1 = QBrush( QColor( f1 ) )
        self.brush = QColor( f1 )
        self.update()
    def Set_Color_F2( self, f2 ):
        self.f2 = QBrush( QColor( f2 ) )
        self.update()
    def Set_Color_B1( self, b1 ):
        self.b1 = QBrush( QColor( b1 ) )
        self.pen = QColor( b1 )
        self.update()
    def Set_Color_B2( self, b2 ):
        self.b2 = QBrush( QColor( b2 ) )
        self.update()
    def Set_Vector( self, state_vector ):
        self.state_vector = state_vector
        self.update()
    def Set_Progress( self, progress_bar ):
        self.progress_bar = progress_bar
        self.update()
    def Set_Mode( self, mode ):
        self.mode = mode
        self.update()
    # Context Menu Event
    def contextMenuEvent( self, event ):
        if   self.mode == "FG": mode_opposite = "BG"
        elif self.mode == "BG": mode_opposite = "FG"

        # Menu
        qmenu = QMenu( self )
        # Actions
        qmenu_swap = qmenu.addAction( "FG-BG Swap" )
        qmenu_active = qmenu.addAction( f"Show { mode_opposite }" )
        qmenu_random = qmenu.addAction( "Random" )
        qmenu_complementary = qmenu.addAction( "Complementary" )
        # Map
        action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
        # Triggers
        if action == qmenu_swap:
            self.SIGNAL_SWAP.emit()
        if action == qmenu_active:
            self.mode = mode_opposite
            self.SIGNAL_SHOW.emit( self.mode )
        if action == qmenu_random:
            self.SIGNAL_RANDOM.emit()
        if action == qmenu_complementary:
            self.SIGNAL_COMP.emit()
    # Interaction
    def enterEvent( self, event ):
        self.state_other = True
        self.update()
    def leaveEvent( self, event ):
        self.state_other = False
        self.update()
    # Paint Style
    def paintEvent( self, event ):
        # Start Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )
        painter.setPen( QtCore.Qt.NoPen )

        # Variable
        w1 = self.ww + 1
        w2 = int( w1 * 0.5 )

        # Progress Bar Mask
        mask = QPainterPath()
        mask.addRect( int( 0 ), int( 0 ), int( self.ww * self.progress_bar ), int( self.hh ) )
        painter.setClipPath( mask )

        # Colors
        if self.state_vector == 0:
            # Colors
            if self.mode == "FG":
                cor1 = self.f1
                cor2 = self.f2
                cor3 = self.b1
            elif self.mode == "BG":
                cor1 = self.b1
                cor2 = self.b2
                cor3 = self.f1
            # FG Active
            painter.setBrush( cor1 )
            painter.drawRect( int( 0 ), int( 0 ), int( w2 ), int( self.hh ) )
            # FG Previous
            painter.setBrush( cor2 )
            painter.drawRect( int( w2 ), int( 0 ), int( w2 ), int( self.hh ) )
            # Other
            if self.state_other == True:
                painter.setBrush( cor3 )
                if self.mode == "FG":
                    point = w1 - self.other_a
                    painter.drawRect( int( point ), int( 0 ), int( self.other_a ), int( self.hh ) )
                elif self.mode == "BG":
                    painter.drawRect( int( 0 ), int( 0 ), int( self.other_a ), int( self.hh ) )
        else:
            painter.setBrush( QBrush( self.brush ) )
            painter.setPen( QPen( self.pen, 15, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.drawRect( int( 0 ), int( 0 ), int( w1 ), int( self.hh ) )

class Harmony_Swatch( QWidget ):
    SIGNAL_HARMONY_INDEX = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Harmony_Swatch, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        # Index
        self.harmony_rule = harmony_5 # harmony_1 harmony_2 harmony_3 harmony_4 harmony_5
        self.harmony_edit = False
        self.harmony_index = 0
        self.harmony_parts = 5
        self.harmony_color = [ "#000000", "#000000", "#000000", "#000000", "#000000" ]
        # Colors
        self.c_black = QColor( "#000000" )
        self.c_white = QColor( "#ffffff" )
    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        self.resize( ww, hh )
    def Set_WheelSpace( self, wheel_space ):
        self.wheel_space = wheel_space
        self.update()
    def Set_Harmony_Rule( self, harmony_rule ):
        self.harmony_rule = harmony_rule
        self.update()
    def Set_Harmony_Parts( self, harmony_parts, harmony_color ):
        self.harmony_parts = harmony_parts
        self.harmony_color = harmony_color
        self.update()
    # Update
    def Update_Index( self, harmony_index ):
        self.harmony_index = harmony_index
        self.update()
    # Mouse Interaction
    def mousePressEvent( self, event ):
        self.Index_Signal( event )
        self.update()
    def mouseMoveEvent( self, event ):
        self.Index_Signal( event )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        self.Index_Signal( event )
        self.update()
    def mouseReleaseEvent( self, event ):
        self.Index_Signal( event )
        self.update()
    # Signals
    def Index_Signal( self, event ):
        self.ex = Limit_Range( event.x(), 0, self.ww )
        percentage = self.ex / self.ww
        self.harmony_index = Limit_Range( int( percentage * self.harmony_parts ), 0, self.harmony_parts - 1 ) + 1
        self.SIGNAL_HARMONY_INDEX.emit( self.harmony_index )
        self.update()
    # Paint
    def paintEvent( self, event ):
        # Start Qpainter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Correct Variable Range
        self.harmony_index = Limit_Range( self.harmony_index, 0, self.harmony_parts )

        # Swatch
        points = list()
        painter.setPen( QtCore.Qt.NoPen )
        unit = int( self.ww / self.harmony_parts ) + 1
        for i in range( 0, self.harmony_parts ):
            # Variables
            px = int( unit * i )
            # Color
            painter.setBrush( QBrush( QColor( self.harmony_color[i] ) ) )
            painter.drawRect( int( px ), int( 0 ), int( unit ), int( self.hh ) )
            # Stops
            points.append( px )
        points.append( self.ww )

        # Index Cursor
        if self.harmony_index != 0:
            px = int( points[ self.harmony_index - 1 ] + unit * 0.5 )
            painter.setBrush( QtCore.Qt.NoBrush )
            painter.setPen( QPen( self.c_black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
            painter.drawLine( px - 5, self.h2, px + 5, self.h2 )
            painter.setPen( QPen( self.c_white, 2, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
            painter.drawLine( px - 4, self.h2, px + 4, self.h2 )
class Harmony_Span( QWidget ):
    SIGNAL_SPAN = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Harmony_Span, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        # Range
        self.harmony_amplitude = 0.2
        self.harmony_rule = harmony_5 # harmony_1 harmony_2 "ANALGOUS" harmony_3 harmony_4
        self.no_span = [ harmony_1, harmony_2 ] # Have no span
        # Colors
        self.c_black = QColor( "#000000" )
        self.c_white = QColor( "#ffffff" )
    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.resize( ww, hh )
    def Set_Rule( self, rule ):
        self.harmony_rule = rule
        self.update()
    # Update
    def Update_Amplitude( self, harmony_amplitude ):
        # range 0-1
        self.harmony_amplitude = harmony_amplitude
        self.update()
    # Mouse Interaction
    def mousePressEvent( self, event ):
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):
            self.Range_Width( ex )
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):
            self.Range_Pin( ex )
    def mouseMoveEvent( self, event ):
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):
            self.Range_Width( ex )
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):
            self.Range_Pin( ex )
    def mouseDoubleClickEvent( self, event ):
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):
            self.Range_Width( ex )
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):
            self.Range_Pin( ex )
    def mouseReleaseEvent( self, event ):
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):
            self.Range_Width( ex )
        if ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):
            self.Range_Pin( ex )
        self.SIGNAL_RELEASE.emit( 0 )
    # Signals
    def Range_Width( self, ex ):
        # Consider Widget Size
        value = Limit_Range( ex, 0, self.ww )
        # Sides
        if value >= self.w2:
            span_right = value
            span_left = self.ww - value
        else:
            span_left = value
            span_right = self.ww - value
        # Normalize Values
        delta = span_right - span_left
        if self.ww == 0:
            self.harmony_amplitude = 0
        else:
            self.harmony_amplitude = delta / self.ww
        self.SIGNAL_SPAN.emit( self.harmony_amplitude )
        self.update()
    def Range_Pin( self, ex ):
        # Consider Widget Size
        value = Limit_Range( ex, 0, self.ww )
        # Pin
        stops = 72
        unit = self.ww / stops
        distances = list()
        for i in range( 0, stops+1 ):
            dist = Trig_2D_Points_Distance( value, 0, ( unit * i ), 0 )
            distances.append( dist )
        value_min = min( distances )
        index = distances.index( value_min )
        value = unit * index
        percent = value / self.ww
        # Sides
        if value >= self.w2:
            span_right = value
            span_left = self.ww - value
        else:
            span_left = value
            span_right = self.ww - value
        # Normalize Values
        delta = span_right - span_left
        if self.ww == 0:
            self.harmony_amplitude = 0
        else:
            self.harmony_amplitude = delta / self.ww
        self.SIGNAL_SPAN.emit( self.harmony_amplitude )
        self.update()
    # Paint
    def paintEvent( self, event ):
        # Start Qpainter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        if self.harmony_rule in self.no_span:
            px = int( self.w2 )
            width = 1
        else:
            px = int( self.w2 - ( self.harmony_amplitude * self.ww * 0.5 ) )
            width = int( self.ww * self.harmony_amplitude )
            if width <= 1:
                width = 1

        # Harmony Angle
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_black ) )
        painter.drawRect( int( px ), int( 1 ), int( width ), int( 8 ) )
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_white ) )
        painter.drawRect( int( px + 1 ), int( 2 ), int( width - 2 ), int( 6 ) )

#endregion
#region Panels

class Panel_Fill( QWidget ):

    # Init
    def __init__( self, parent ):
        super( Panel_Fill, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        # Display
        self.hex_code = QColor( "#000000" )
    # Set
    def Set_Size( self, ww, hh ):
        self.ww = int( ww )
        self.hh = int( hh )
        self.resize( ww, hh )
    # Updates
    def Update_Gradient( self, hex_code ):
        self.hex_code = QColor( hex_code )
        self.update()
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )
        # Draw Pixmaps
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.hex_code ) )
        painter.drawRect( 0, 0, self.ww, self.hh )

class Panel_Square( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str, float, float, float )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( str, float, float, float, int )

    # Init
    def __init__( self, parent ):
        super( Panel_Square, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Varibles
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        # Event
        self.ex = 0
        self.ey = 0
        self.ox = 0
        self.oy = 0
        self.ot = 0
        # State
        self.zoom = False
        self.axis = 0 # 360 255
        # Panel
        self.wheel_space = "HSV"
        self.hue_shape = "SQUARE" # "TRIANGLE" "SQUARE" "DIAMOND"
        self.gradient = None
        self.id1 = "hsv_1"
        self.id2 = "hsv_2"
        self.id3 = "hsv_3"
        self.v1 = 0 # 0-360 event tangent
        self.v2 = 0
        self.v3 = 0
        # Colors
        self.c_white = QColor( "#ffffff" )
        self.c_gray = QColor( "#b0b0b0" )
        self.c_black = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
        self.color_index = None
        # Harmony
        self.harmony_rule = None
        self.harmony_index = None
        self.harmony_list = None
        # Pin
        self.pin_list = None
        self.pin_index = None
        # Analyse
        self.analyse_list = None
    # Set
    def Set_Size( self, ww, hh ):
        # Variables
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Mask ( slightly bigger than color display )
        if self.hue_shape == "TRIANGLE":
            polygon = QPolygon( [
                QPoint( -1, -1 ),
                QPoint( self.ww + 1, self.h2 ),
                QPoint( -1, self.hh + 1 ),
                ] )
            triangle = QRegion( polygon, Qt.OddEvenFill )
            self.setMask( triangle )
        if self.hue_shape == "SQUARE":
            polygon = QPolygon( [
                QPoint( -1, -1 ),
                QPoint( self.ww + 1, -1 ),
                QPoint( self.ww + 1, self.hh + 1 ),
                QPoint( -1, self.hh + 1 ),
                ] )
            square = QRegion( polygon, Qt.OddEvenFill )
            self.setMask( square )
        if self.hue_shape == "DIAMOND":
            polygon = QPolygon( [
                QPoint( self.w2, -1 ),
                QPoint( self.ww + 1, self.h2 ),
                QPoint( self.w2, self.hh + 1 ),
                QPoint( -1, self.h2 ),
                ] )
            diamond = QRegion( polygon, Qt.OddEvenFill )
            self.setMask( diamond )
        # Update
        self.resize( ww, hh )
    def Set_Zoom( self, boolean ):
        self.zoom = boolean
        self.update()
    # Updates
    def Update_Color( self, wheel_space, hue_shape, color_index ):
        # Variables
        self.wheel_space = wheel_space
        self.hue_shape = hue_shape
        self.color_index = color_index
        self.hex_code = QColor( self.color_index["display"] )
        # self.chan = wheel_space.lower()
        self.id1, self.id2, self.id3 = Space_Index( self.wheel_space )
        # Shape
        if self.hue_shape == "TRIANGLE":
            # Variables
            cx = self.color_index[ "hsl_2" ]
            cy = 1 - self.color_index[ "hsl_3" ]
            lerp = self.Triangle_Lerp( cy, 1, 1 )
            # Values
            self.v1 = self.color_index[ "hsl_1" ]
            self.ex = Limit_Range( cx * lerp * self.ww, 0, self.ww )
            self.ey = Limit_Range( cy * self.hh, 0, self.hh )
        if self.hue_shape == "SQUARE":
            # Values
            self.v1 = self.color_index[ self.id1 ]
            self.ex = self.color_index[ self.id2 ] * self.ww
            self.ey = ( 1 - self.color_index[ self.id3 ] ) * self.hh
        if self.hue_shape == "DIAMOND":
            # Variables
            cx = self.color_index[ "hsl_2" ]
            cy = 1 - self.color_index[ "hsl_3" ]
            mini, maxi, delta = self.Diamond_Lerp( cy, 1, 1 )
            value = mini + cx * delta
            # Values
            self.v1 = self.color_index[ "hsl_1" ]
            self.ex = Limit_Range( value * self.ww, mini * self.ww, maxi * self.ww )
            self.ey = Limit_Range( cy * self.hh, 0, self.hh )
        # Update
        self.update()
    def Update_Gradient( self, gradient ):
        self.gradient = gradient
        self.axis = len( gradient ) - 1
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse_list ):
        self.analyse_list = analyse_list
        self.update()
    # Panel Modifiers
    def Triangle_Lerp( self, y, px, py ):
        if y <= 0:
            lerp = 0
        elif ( y > 0 ) and ( y < 0.5 * py ):
            lerp = Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0*px, 0*py, 1*px, 0.5*py )[0]
        elif y == 0.5 * py:
            lerp = 1
        elif ( y > 0.5 * py ) and ( y < py ):
            lerp = Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0*px, 1*py, 1*px, 0.5*py )[0]
        elif y >= py:
            lerp = 0
        return lerp
    def Diamond_Lerp( self, y, px, py ):
        if y <= 0 * py:
            mini = 0.5 * px
            maxi = 0.5 * py
            delta = 0
        elif ( y > 0 ) and ( y < 0.5 * py ):
            mini = Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 0*py, 0*px, 0.5*py )[0]
            maxi = Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 0*py, 1*px, 0.5*py )[0]
            delta = abs( maxi - mini )
        elif y == 0.5 * py:
            mini = 0
            maxi = py
            delta = py
        elif ( y > 0.5 * py ) and ( y < py ):
            mini = Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 1*py, 0*px, 0.5*py )[0]
            maxi = Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 1*py, 1*px, 0.5*py )[0]
            delta = abs( maxi - mini )
        elif y >= 1 * py:
            mini = 0.5 * px
            maxi = 0.5 * py
            delta = 0
        return mini, maxi, delta
    # Mouse Event
    def mousePressEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # Variables
        self.ox = ex
        self.oy = ey
        self.ot = self.v1
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  pass
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Snap( ex, ey )
        self.update()
    def mouseMoveEvent( self, event ):
        # Events
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Position( ex, ey, False )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Position( ex, ey, False )
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.zoom = False
        self.ot = 0
        self.pin_index = None
        # Updates
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Mouse Function
    def Cursor_Position( self, ex, ey, zoom ):
        # Variables
        self.zoom = zoom
        # Input
        if self.hue_shape == "TRIANGLE":
            # Cursor
            lerp = self.Triangle_Lerp( ey, self.ww, self.hh )
            self.ex = Limit_Range( ex, 0, lerp )
            self.ey = Limit_Range( ey, 0, self.hh )
            # Color
            if lerp == 0:  px = 0
            else:           px = self.ex / lerp
            py = ( self.hh - self.ey ) / self.hh
        if self.hue_shape == "SQUARE":
            # Cursor
            self.ex = Limit_Range( ex, 0, self.ww )
            self.ey = Limit_Range( ey, 0, self.hh )
            # Color
            px =  self.ex / self.ww
            py = ( self.hh - self.ey ) / self.hh
        if self.hue_shape == "DIAMOND":
            # Cursor
            mini, maxi, delta = self.Diamond_Lerp( ey, self.ww, self.hh )
            self.ex = Limit_Range( ex, mini, maxi )
            self.ey = Limit_Range( ey, 0, self.hh )
            # Color
            if delta == 0:  px = 0
            else:           px = ( self.ex - mini ) / delta
            py = ( self.hh - self.ey ) / self.hh
        # Variables
        if self.hue_shape == "TRIANGLE":
            mode = "HSL"
            lerp = self.Triangle_Lerp( ey, self.ww, self.hh )
            if lerp == 0:  v2 = 0
            else:           v2 = ex / lerp
        if self.hue_shape == "SQUARE":
            mode = self.wheel_space
            v2 = ex / self.ww
        if self.hue_shape == "DIAMOND":
            mode = "HSL"
            mini, maxi, delta = self.Diamond_Lerp( ey, self.ww, self.hh )
            if delta == 0:  v2 = 0
            else:           v2 = ( ex - mini ) / delta
        v3 = ( self.hh - ey ) / self.hh
        # Limit
        self.v2 = Limit_Float( v2 )
        self.v3 = Limit_Float( v3 )
        # Signals
        self.SIGNAL_VALUE.emit( self.wheel_space, self.v1, self.v2, self.v3 )
        if self.pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( self.wheel_space, self.v1, self.v2, self.v3, self.pin_index )
    def Cursor_Tangent( self, ex ):
        # Hue
        delta_hue = ( ( ex - self.ox ) / self.ww )
        angle = self.ot + delta_hue
        self.v1 = Limit_Looper( angle, 1 )
        # Signals
        self.SIGNAL_VALUE.emit( self.wheel_space, self.v1, self.v2, self.v3 )
    def Cursor_Snap( self, ex, ey ):
        if self.pin_list != None:
            distance = list()
            for i in range( 0, len( self.pin_list ) ):
                if self.pin_list[i]["active"] == True:
                    if self.hue_shape == "TRIANGLE":
                        # Variables
                        cx = self.pin_list[i]["hsl_2"]
                        cy = 1 - self.pin_list[i]["hsl_3"]
                        lerp = self.Triangle_Lerp( cy, 1, 1 )
                        # Values
                        px = Limit_Range( cx * lerp * self.ww, 0, self.ww )
                        py = Limit_Range( cy * self.hh, 0, self.hh )
                    if self.hue_shape == "SQUARE":
                        px = self.pin_list[i][ self.id2 ] * self.ww
                        py = ( 1 - self.pin_list[i][ self.id3 ] ) * self.hh
                    if self.hue_shape == "DIAMOND":
                        # Variables
                        cx = self.pin_list[i]["hsl_2"]
                        cy = 1 - self.pin_list[i]["hsl_3"]
                        mini, maxi, delta = self.Diamond_Lerp( cy, 1, 1 )
                        value = mini + cx * delta
                        # Values
                        px = Limit_Range( value * self.ww, mini * self.ww, maxi * self.ww )
                        py = Limit_Range( cy * self.hh, 0, self.hh )
                    dist = Trig_2D_Points_Distance( ex, ey, px, py )
                    distance.append( ( dist, i ) )
            if len( distance ) > 0:
                distance.sort()
                pin_index = distance[0][1]
                if pin_index <= pin_range:
                    self.pin_index = pin_index
                    self.SIGNAL_PIN_INDEX.emit( self.pin_index )
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        dot1 = 5
        dot2 = 10
        line_poly = 2

        # Draw Gradient
        if self.gradient != None and self.axis > 0:
            # Draw Masks
            if self.hue_shape == "TRIANGLE":
                triangle = QPainterPath()
                triangle.moveTo( 0 , 0 )
                triangle.lineTo( self.ww, self.h2 )
                triangle.lineTo( 0 , self.hh )
                painter.setClipPath( triangle )
            if self.hue_shape == "DIAMOND":
                diamond = QPainterPath()
                diamond.moveTo( self.w2, 0 )
                diamond.lineTo( self.ww, self.h2 )
                diamond.lineTo( self.w2, self.hh )
                diamond.lineTo( 0, self.h2 )
                painter.setClipPath( diamond )
            try:
                # Draw Pixmaps
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( QtCore.Qt.NoBrush )
                index = int( self.v1 * self.axis )
                qpixmap = self.gradient[index]
                render = qpixmap.scaled( self.ww, self.hh, Qt.IgnoreAspectRatio, Qt.FastTransformation )
                painter.drawPixmap( 0, 0, render )
            except:
                pass

        # Analyse Colors
        if self.analyse_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_gray ) )
            hue = int( self.v1 * 360 )
            if hue == 360:
                hue = 0
            for color in self.analyse_list:
                if int( color[ self.id1 ] * 360 ) == hue:
                    if self.hue_shape == "TRIANGLE":
                        cx = color["hsl_2"]
                        cy = ( 1 - color["hsl_3"] )
                        lerp = self.Triangle_Lerp( cy, 1, 1 )
                        painter.drawEllipse( int( ( cx * lerp * self.ww ) - dot1 ), int( ( cy * self.hh ) - dot1 ), dot2, dot2 )
                    if self.hue_shape == "SQUARE":
                        px = color[ self.id2 ] * self.ww
                        py = ( 1 - color[ self.id3 ] ) * self.hh
                        painter.drawEllipse( int( px - dot1 ), int( py - dot1 ), dot2, dot2 )
                    if self.hue_shape == "DIAMOND":
                        cx = color["hsl_2"]
                        cy = ( 1 - color["hsl_3"] )
                        mini, maxi, delta = self.Diamond_Lerp( cy, 1, 1 )
                        value = mini + cx * delta
                        painter.drawEllipse( int( ( value * self.ww ) - dot1 ), int( ( cy * self.hh ) - dot1 ), dot2, dot2 )

        # Pinned Colors
        if self.pin_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for pin in self.pin_list:
                if pin["active"] == True:
                    if self.hue_shape == "TRIANGLE":
                        cx = pin["hsl_2"]
                        cy = ( 1 - pin["hsl_3"] )
                        lerp = self.Triangle_Lerp( cy, 1, 1 )
                        painter.drawEllipse( int( ( cx * lerp * self.ww ) - dot1 ), int( ( cy * self.hh ) - dot1 ), dot2, dot2 )
                    if self.hue_shape == "SQUARE":
                        px = pin[ self.id2 ] * self.ww
                        py = ( 1 - pin[ self.id3 ] ) * self.hh
                        painter.drawEllipse( int( px - dot1 ), int( py - dot1 ), dot2, dot2 )
                    if self.hue_shape == "DIAMOND":
                        cx = pin["hsl_2"]
                        cy = ( 1 - pin["hsl_3"] )
                        mini, maxi, delta = self.Diamond_Lerp( cy, 1, 1 )
                        value = mini + cx * delta
                        painter.drawEllipse( int( ( value * self.ww ) - dot1 ), int( ( cy * self.hh ) - dot1 ), dot2, dot2 )

        # Harmony Colors
        if self.harmony_list != None:
            # Parsing
            points = list()
            for harmony in self.harmony_list:
                if self.hue_shape == "TRIANGLE":
                    cx = harmony["hsl_2"]
                    cy = ( 1 - harmony["hsl_3"] )
                    inter = self.Triangle_Lerp( cy, 1, 1 )
                    har_x = cx * inter * self.ww
                    har_y = cy * self.hh
                if self.hue_shape == "SQUARE":
                    har_x = harmony[ self.id2 ] * self.ww
                    har_y = ( 1 - harmony[ self.id3 ] ) * self.hh
                if self.hue_shape == "DIAMOND":
                    cx = harmony["hsl_2"]
                    cy = ( 1 - harmony["hsl_3"] )
                    mini, maxi, delta = self.Diamond_Lerp( cy, 1, 1 )
                    value = mini + cx * delta
                    har_x = value * self.ww
                    har_y = cy * self.hh
                points.append( [ har_x, har_y ] )
            length = len( points )
            # Draw Line
            painter.setPen( QPen( self.c_white, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( points[i-1][0] ), int( points[i-1][1] ), int( points[i][0] ), int( points[i][1] ) )
            if self.harmony_rule in [ harmony_3, harmony_4 ]:
                painter.drawLine( int( points[0][0] ), int( points[0][1] ), int( points[length-1][0] ), int( points[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( points[i][0] - dot1 ), int( points[i][1] - dot1 ), int( dot2 ), int( dot2 ) )

        # Cursor
        Cursor_Display( self, painter )

class Panel_Hue_Circle( QWidget ):
    SIGNAL_ANGLE = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_HARMONY_INDEX = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Panel_Hue_Circle, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        # Variables
        self.px = 0
        self.py = 0
        self.pw = 1
        self.ph = 1
        self.ax = 0
        self.ay = 0
        self.side = 0
        # Wheel
        self.wheel_mode = "DIGITAL" # "DIGITAL" "ANALOG"
        self.wheel_space = "HSV" # "HSV" "HSL" "HCY" "ARD"
        self.hue_shine = None
        self.hue_tone = None
        self.gradient = None
        self.amplitude = 0.008
        # Color
        self.c_lite = QColor( "#ffffff" )
        self.c_dark = QColor( "#000000" )
        self.c_white = QColor( "#ffffff" )
        self.c_black = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
        self.color_index = None
        # Harmony Colors
        self.harmony_rule = None # harmony_1 harmony_2 harmony_3 harmony_4 harmony_5
        self.harmony_index = None
        self.harmony_list = None
        # Pinned Colors
        self.pin_list = None
    # Set
    def Set_Size( self, ww, hh, hue_shape ):
        # Widget
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Frame
        self.side = min( self.ww, self.hh )
        side2 = self.side * 0.5
        self.px = int( self.w2 - side2 )
        self.py = int( self.h2 - side2 )
        self.ax = int( self.w2 - side2 )
        self.ay = int( self.h2 - ( self.side * delta_a ) ) # Inverted for the formula
        # Circles
        self.circle_0, self.circle_1, self.circle_2, self.circle_3 = Circles( self.px, self.py, self.side )
        self.circle_01 = self.circle_0.subtracted( self.circle_1 )
        self.circle_02 = self.circle_0.subtracted( self.circle_2 )
        self.circle_12 = self.circle_1.subtracted( self.circle_2 )
        self.circle_13 = self.circle_1.subtracted( self.circle_3 )

        # Variables
        pad = 5
        # Regions
        widget_square = QRegion(
            int( 0 ),
            int( 0 ),
            int( self.ww ),
            int( self.hh ),
            QRegion.Rectangle
            )
        if hue_shape == "None":
            mask_region = widget_square
        if hue_shape == "TRIANGLE":
            tx = 0.28
            ty = 0.13
            tk = 0.07
            # t = 1 - k - x
            polygon = QPolygon( [
                # Top
                QPoint( int( self.px + tx * self.side - pad ),       int( self.py + ty * self.side ) ),
                QPoint( int( self.px + tx * self.side ),             int( self.py + ty * self.side - pad ) ),
                # Right
                QPoint( int( self.px + self.side - tk * self.side ), int( self.h2 - pad ) ),
                QPoint( int( self.px + self.side - tk * self.side ), int( self.h2 + pad ) ),
                # Bot
                QPoint( int( self.px + tx * self.side ),             int( self.py + self.side - ty * self.side + pad ) ),
                QPoint( int( self.px + tx * self.side - pad ),       int( self.py + self.side - ty * self.side ) ),
                ] )
            triangle = QRegion( polygon, Qt.OddEvenFill )
            mask_region = widget_square.subtracted( triangle )
        if hue_shape == "SQUARE":
            sk = 0.2
            square = QRegion(
                int( self.px + self.side * sk - pad ),
                int( self.py + self.side * sk - pad ),
                int( self.side - ( 2 * sk * self.side ) + ( 2 * pad ) ),
                int( self.side - ( 2 * sk * self.side ) + ( 2 * pad ) ),
                QRegion.Rectangle
                )
            mask_region = widget_square.subtracted( square )
        if hue_shape == "DIAMOND":
            k = 0.07
            dk = ( 1 - k * 2 ) / 2
            polygon = QPolygon( [
                    QPoint( int( self.w2 ),                         int( self.h2 - self.side * dk - pad ) ),
                    QPoint( int( self.w2 + self.side * dk + pad ),  int( self.h2 ) ),
                    QPoint( int( self.w2 ),                         int( self.h2 + self.side * dk + pad ) ),
                    QPoint( int( self.w2 - self.side * dk - pad ),  int( self.h2 ) ),
                    ] )
            diamond = QRegion( polygon, Qt.OddEvenFill )
            mask_region = widget_square.subtracted( diamond )

        # Mask
        mask_circle = QRegion( int( self.px ), int( self.py ), int( self.side ), int( self.side ), QRegion.Ellipse )
        mask = mask_circle.intersected( mask_region )
        self.setMask( mask )

        # Gradient
        self.Conical_Gradient( self.w2, self.h2 )

        # Update
        self.resize( ww, hh )
    def Set_Theme( self, c_lite, c_dark ):
        self.c_lite = QColor( c_lite )
        self.c_dark = QColor( c_dark )
        self.update()
    # Update
    def Update_Color( self, wheel_mode, wheel_space, color_index ):
        self.wheel_mode = wheel_mode
        self.wheel_space = wheel_space
        self.color_index = color_index
        self.update()
    def Update_Gradient( self, gradient ):
        self.gradient = gradient
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    # Gradients
    def Conical_Gradient( self, w2, h2 ):
        shine = [
            [ 255, 000, 000 ], # Index = 0 > red
            [ 255, 127, 000 ], # Index = 1 > orange
            [ 255, 255, 000 ], # Index = 2 > yellow
            [ 000, 255, 000 ], # Index = 3 > green
            [ 000, 255, 255 ], # Index = 4 > cyan
            [ 000, 000, 255 ], # Index = 5 > blue
            [ 255, 000, 255 ], # Index = 6 > magenta
            ]
        if self.wheel_mode == "DIGITAL":
            hue_shine = QConicalGradient( QPoint( w2, h2 ), 180 )
            hue_shine.setColorAt( 0.000, QColor( shine[0][0], shine[0][1], shine[0][2] ) ) # RED
            hue_shine.setColorAt( 0.166, QColor( shine[6][0], shine[6][1], shine[6][2] ) ) # MAGENTA
            hue_shine.setColorAt( 0.333, QColor( shine[5][0], shine[5][1], shine[5][2] ) ) # BLUE
            hue_shine.setColorAt( 0.500, QColor( shine[4][0], shine[4][1], shine[4][2] ) ) # CYAN
            hue_shine.setColorAt( 0.666, QColor( shine[3][0], shine[3][1], shine[3][2] ) ) # GREEN
            hue_shine.setColorAt( 0.833, QColor( shine[2][0], shine[2][1], shine[2][2] ) ) # YELLOW
            hue_shine.setColorAt( 1.000, QColor( shine[0][0], shine[0][1], shine[0][2] ) ) # RED
        if self.wheel_mode == "ANALOG":
            hue_shine = QConicalGradient( QPoint( w2, h2 ), 210 )
            hue_shine.setColorAt( 0.000, QColor( shine[0][0], shine[0][1], shine[0][2] ) ) # RED
            hue_shine.setColorAt( 0.083, QColor( shine[6][0], shine[6][1], shine[6][2] ) ) # MAGENTA
            hue_shine.setColorAt( 0.236, QColor( shine[5][0], shine[5][1], shine[5][2] ) ) # BLUE
            hue_shine.setColorAt( 0.394, QColor( shine[4][0], shine[4][1], shine[4][2] ) ) # CYAN
            hue_shine.setColorAt( 0.541, QColor( shine[3][0], shine[3][1], shine[3][2] ) ) # GREEN
            hue_shine.setColorAt( 0.661, QColor( shine[2][0], shine[2][1], shine[2][2] ) ) # YELLOW
            hue_shine.setColorAt( 0.833, QColor( shine[1][0], shine[1][1], shine[1][2] ) ) # ORANGE
            hue_shine.setColorAt( 1.000, QColor( shine[0][0], shine[0][1], shine[0][2] ) ) # RED
        return hue_shine
    # Mouse Interaction
    def mousePressEvent( self, event ):
        if event.buttons() == QtCore.Qt.LeftButton:
            angle = self.Cursor_Angle( event )
            if self.harmony_list != None:
                self.Cursor_Harmony( angle )
            self.Cursor_Signal( angle )
        self.update()
    def mouseMoveEvent( self, event ):
        if event.buttons() == QtCore.Qt.LeftButton:
            angle = self.Cursor_Angle( event )
            self.Cursor_Signal( angle )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        if event.buttons() == QtCore.Qt.LeftButton:
            angle = self.Cursor_Angle( event )
            self.Cursor_Signal( angle )
        self.update()
    def mouseReleaseEvent( self, event ):
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Cursor
    def Cursor_Angle( self, event ):
        # Variables
        em = event.modifiers()
        ex = event.x()
        ey = self.hh - event.y()
        limit = 2.5
        # Angle Measure
        if self.wheel_mode == "DIGITAL":
            angle = Trig_2D_Points_Lines_Angle( ex, ey, self.w2, self.h2, 0, self.h2 )
            if em == QtCore.Qt.ShiftModifier:   angle = int( angle )
            if em == QtCore.Qt.ControlModifier: angle = Limit_Angle( angle, limit )
            angle = angle / 360
        elif self.wheel_mode == "ANALOG":
            angle = Trig_2D_Points_Lines_Angle( ex, ey, self.w2, self.h2, self.ax, self.ay )
            if em == QtCore.Qt.ShiftModifier:   angle = int( angle )
            if em == QtCore.Qt.ControlModifier: angle = Limit_Angle( angle, limit )
            angle = Limit_Looper( angle, 360 ) / 360
        return angle
    def Cursor_Harmony( self, angle ):
        list_dist = list()
        for i in range( 0, len( self.harmony_list ) ):
            index = i + 1
            if   self.wheel_mode == "DIGITAL":  har_angle = self.harmony_list[i]["hue_d"]
            elif self.wheel_mode == "ANALOG":   har_angle = self.harmony_list[i]["hue_a"]
            delta = Trig_2d_Angle_Delta( angle, har_angle )
            list_dist.append( [ delta, index ] )
        list_dist.sort()
        self.harmony_index = list_dist[0][1]
        self.SIGNAL_HARMONY_INDEX.emit( self.harmony_index )
    def Cursor_Signal( self, angle ):
        self.SIGNAL_ANGLE.emit( angle )
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        line_width = 4
        radius = 0.5
        margin = 0.05

        # Circle Points
        list_point = list()
        if self.harmony_rule != None:
            for harmony in self.harmony_list:
                px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, Wheel_Angle( self.wheel_mode, harmony ) )
                list_point.append( [ px, py ] )
        else:
            px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, Wheel_Angle( self.wheel_mode, self.color_index ) )
            list_point.append( [ px, py ] )
        length = len( list_point )
        # Pin Points
        list_pin = list()
        if self.pin_list != None:
            for pin in self.pin_list:
                if pin["active"] == True:
                    px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, Wheel_Angle( self.wheel_mode, pin ) )
                    list_pin.append( [ px, py ] )

        # Dark Border
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_dark ) )
        painter.drawPath( self.circle_02 )
        # Dark Lines Color Reference
        painter.setPen( QPen( self.c_dark, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        if self.wheel_mode == "DIGITAL":
            for digital in circle_digital:
                px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, digital )
                painter.drawLine( int( px ), int( py ), int( self.w2 ), int( self.h2 ) )
        if self.wheel_mode == "ANALOG":
            for analog in circle_analog:
                px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, analog - hue_a )
                painter.drawLine( int( px ), int( py ), int( self.w2 ), int( self.h2 ) )

        # Gradients
        hue_shine = self.Conical_Gradient( self.w2, self.h2 )
        # Hue Gradient
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( hue_shine ) )
        painter.setClipPath( self.circle_01 )
        painter.drawRect( int( self.px ), int( self.py ), int( self.side ), int( self.side ) )

        # Light Line
        painter.setPen( QPen( self.c_lite, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        if length > 0:
            line_gray = QPainterPath()
            for point in list_point:
                line_gray.moveTo( int( self.w2 ), int( self.h2 ) )
                line_gray.lineTo( int( point[0] ), int( point[1] ) )
            painter.setClipPath( self.circle_13 )
            painter.drawPath( line_gray )
        # Pinned Colors
        if self.pin_list != None:
            painter.setPen( QPen( self.c_lite, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            line_gray = QPainterPath()
            for pin in list_pin:
                line_gray.moveTo( int( self.w2 ), int( self.h2 ) )
                line_gray.lineTo( int( pin[0] ), int( pin[1] ) )
            painter.setClipPath( self.circle_12 )
            painter.drawPath( line_gray )
        # Dark Line over Hue
        painter.setPen( QPen( self.c_dark, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        painter.setClipPath( self.circle_01 )
        for point in list_point:
            painter.drawLine( int( point[0] ), int( point[1] ), int( self.w2 ), int( self.h2 ) )

class Panel_Gamut( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str, float, float, float )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_PROFILE = QtCore.pyqtSignal( list )
    SIGNAL_HARMONY_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( str, float, float, float, int )

    # Init
    def __init__( self, parent ):
        super( Panel_Gamut, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.side = 0
        # Point
        self.px = 0
        self.py = 0
        self.pz = 0
        # Analog
        self.ax = 0
        self.ay = 0
        # Event
        self.ex = 0
        self.ey = 0
        self.ox = 0
        self.oy = 0
        self.oz = 0
        self.oa = 0
        # State
        self.zoom = False
        self.axis = 0 # 360 255
        self.region = False # Ring=False and Disk=True
        # Panel
        self.wheel_mode = "DIGITAL"
        self.wheel_space = "HSV"
        self.gradient = None
        self.id1 = "hsv_1"
        self.id2 = "hsv_2"
        self.id3 = "hsv_3"
        self.v1 = 0 # 0-360 event tangent
        self.v2 = 0
        self.v3 = 0
        self.mod_3 = QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier
        self.previous_distance = 0
        self.previous_rotation = 0

        # Disk
        self.disk_var = 0.060 #v2a - variable
        self.disk_rad = 0.5 * ( 1 - ( 2 * self.disk_var ) ) # 0.432 - radius
        self.disk_px = 0
        self.disk_py = 0
        self.disk_s1 = 0 # side1
        self.disk_s2 = ( self.disk_s1 * 0.5 ) # side2 ( half )

        # Gamut
        self.gamut_mask = "NONE" # "FULL" "TRIANGLE" "SQUARE" "HEXAGON" "CIRCLE_1" "CIRCLE_2" "NONE"
        self.gamut_index = None
        self.gamut_list = None

        # Gamut Neutral ( X, Y )
        self.Set_Reset( "TRIANGLE" )
        self.Set_Reset( "SQUARE" )
        self.Set_Reset( "HEXAGON" )
        self.Set_Reset( "CIRCLE_1" )
        self.Set_Reset( "CIRCLE_2" )

        # Color
        self.c_lite = QColor( "#ffffff" )
        self.c_dark = QColor( "#000000" )
        self.c_white = QColor( "#ffffff" )
        self.c_gray = QColor( "#b0b0b0" )
        self.c_black = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
        self.color_index = None
        # Harmony
        self.harmony_rule = None
        self.harmony_index = None
        self.harmony_list = None
        # Pin
        self.pin_list = None
        self.pin_index = None
        # Analyse
        self.analyse_list = None
    # Set
    def Set_Size( self, ww, hh ):
        # Widget
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Frame
        self.side = min( self.ww, self.hh )
        side2 = self.side * 0.5
        self.px = int( self.w2 - side2 )
        self.py = int( self.h2 - side2 )
        self.ax = int( self.w2 - side2 )
        self.ay = int( self.h2 - ( self.side * delta_a ) ) # Inverted for the formula
        # Circles
        self.circle_0, self.circle_1, self.circle_2, self.circle_3 = Circles( self.px, self.py, self.side )
        self.circle_02 = self.circle_0.subtracted( self.circle_2 )
        self.circle_12 = self.circle_1.subtracted( self.circle_2 )
        # Disk Coordinates
        self.disk_px = self.px + self.disk_var * self.side
        self.disk_py = self.py + self.disk_var * self.side
        self.disk_s1 = ( 1 - 2 * self.disk_var ) * self.side
        self.disk_s2 = self.disk_s1 * 0.5
        # Update
        self.resize( ww, hh )
    def Set_Theme( self, c_lite, c_dark ):
        self.c_lite = QColor( c_lite )
        self.c_dark = QColor( c_dark )
        self.update()
    def Set_Mask( self, gamut_mask ):
        self.gamut_mask = gamut_mask
        self.update()
    def Set_Reset( self, mode ):
        if mode == "TRIANGLE": self.gi_t1 = [ [ 0.50000, 0.50000 ], [ 0.50000, 0.10000 ], [ 0.84641, 0.70000 ], [ 0.15359, 0.70000 ] ]
        if mode == "SQUARE":   self.gi_s1 = [ [ 0.50000, 0.50000 ], [ 0.50000, 0.10000 ], [ 0.90000, 0.50000 ], [ 0.50000, 0.90000 ], [ 0.10000, 0.50000 ] ]
        if mode == "HEXAGON":  self.gi_h1 = [ [ 0.50000, 0.50000 ], [ 0.15359, 0.30000 ], [ 0.50000, 0.10000 ], [ 0.84641, 0.30000 ], [ 0.84641, 0.70000 ], [ 0.50000, 0.90000 ], [ 0.15359, 0.70000 ] ]
        if mode == "CIRCLE_1": self.gi_c1 = [ [ 0.50000, 0.50000 ], [ 0.50000, 0.10000 ], [ 0.90000, 0.50000 ], [ 0.50000, 0.90000 ], [ 0.10000, 0.50000 ] ]
        if mode == "CIRCLE_2": self.gi_c2 = [ [ 0.50000, 0.27500 ], [ 0.50000, 0.10000 ], [ 0.67500, 0.27500 ], [ 0.50000, 0.45000 ], [ 0.32500, 0.27500 ],
                                              [ 0.50000, 0.72500 ], [ 0.50000, 0.55000 ], [ 0.67500, 0.72500 ], [ 0.50000, 0.90000 ], [ 0.32500, 0.72500 ] ]
        self.update()
    def Set_Profile( self, profile ):
        if profile[0] != None:  self.gi_t1 = profile[0]
        if profile[1] != None:  self.gi_s1 = profile[1]
        if profile[2] != None:  self.gi_h1 = profile[2]
        if profile[3] != None:  self.gi_c1 = profile[3]
        if profile[4] != None:  self.gi_c2 = profile[4]
    # Update
    def Update_Color( self, wheel_mode, wheel_space, color_index ):
        # Variables
        self.wheel_mode = wheel_mode
        self.wheel_space = wheel_space
        self.color_index = color_index
        self.hex_code = QColor( self.color_index[ "display" ] )
        self.id1, self.id2, self.id3 = Space_Index( self.wheel_space )
        # Angle
        if self.wheel_mode == "DIGITAL": angle = self.color_index[ "hue_d" ] * 360
        if self.wheel_mode == "ANALOG":  angle = self.color_index[ "hue_a" ] * 360 - hue_a
        # Channels
        self.v1 = self.color_index[ self.id1 ]
        self.v2 = self.color_index[ self.id2 ]
        self.v3 = self.color_index[ self.id3 ]
        # Location
        self.ex, self.ey = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s2, self.color_index[ self.id2 ], angle )
        self.previous_distance = Trig_2D_Points_Distance( self.ex, self.ey, self.w2, self.h2 )
        # Update
        self.update()
    def Update_Gradient( self, gradient ):
        self.gradient = gradient
        self.axis = len( gradient ) - 1
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse_list ):
        self.analyse_list = analyse_list
        self.update()
    # Mouse
    def mousePressEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # Variables
        self.ox = ex
        self.oy = ey
        angle = Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
        distance = Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
        limit = self.side * self.disk_rad
        # Checks
        self.oz = self.v3
        self.oa = angle
        self.region = distance <= limit # Disk==True and Ring==False
        self.mask = distance > self.side * 0.5
        self.gamut_list = self.Gamut_List()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, em, True )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == True:    self.zoom = True
            self.Cursor_Position( ex, ey, em )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == False:    self.Cursor_Position( ex, ey, em )
            if self.region == True:     self.Disk_Tangent( ex, ey )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == False:    pass
            if self.region == True:     self.Disk_Snap( ex, ey )
        if ( eb == QtCore.Qt.LeftButton and em == self.mod_3 ):
            if self.region == False:    pass
            if self.region == True:     self.previous_rotation = self.Previous_Rotation()
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):
            if self.region == False:    pass
            if self.region == True:     self.Disk_Snap( ex, ey )
        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, em )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == True:    self.zoom = True
            self.Cursor_Position( ex, ey, em )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == False:    self.Cursor_Position( ex, ey, em )
            if self.region == True:     self.Disk_Tangent( ex, ey )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == False:    pass
            if self.region == True:     self.Disk_Snap( ex, ey )
        if ( eb == QtCore.Qt.LeftButton and em == self.mod_3 ):
            if self.region == False:    pass
            if self.region == True:     self.Disk_Rotation( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):
            if self.region == False:    pass
            if self.region == True:     self.Cursor_Position( ex, ey, em )
        # Update
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, em )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == True:    self.zoom = True
            self.Cursor_Position( ex, ey, em )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == False:    self.Cursor_Position( ex, ey, em )
            if self.region == True:     self.Disk_Tangent( ex, ey )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):
            if self.region == False:    pass
            if self.region == True:     self.Disk_Snap( ex, ey )
        if ( eb == QtCore.Qt.LeftButton and em == self.mod_3 ):
            if self.region == False:    pass
            if self.region == True:     self.Disk_Rotation( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):
            if self.region == False:    pass
            if self.region == True:     self.Cursor_Position( ex, ey, em )
        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Previous
        self.previous_distance = Trig_2D_Points_Distance( self.ex, self.ey, self.w2, self.h2 )
        # Variables
        self.ox = 0
        self.oy = 0
        self.oa = 0
        self.zoom = False
        # Disk
        self.region = None
        self.previous_rotation = None
        self.gamut_index = None
        self.pin_index = None
        # Updates
        self.Gamut_Profile()
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Interaction
    def Cursor_Position( self, ex, ey, em, harmony=False ):
        if self.mask == False:
            # Hue
            angle = Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
            if em == QtCore.Qt.ShiftModifier:   angle = int( angle)
            if em == QtCore.Qt.ControlModifier: angle = Limit_Angle( angle, 2.5 )
            if self.wheel_mode == "DIGITAL":    hue = angle / 360
            if self.wheel_mode == "ANALOG":     hue = Limit_Looper( angle + hue_a, 360 ) / 360
            # Saturation
            distance = 0
            radius = self.side * self.disk_rad
            if self.region == False: # Ring
                distance = self.previous_distance
                self.ex, self.ey = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s1, distance, angle )
            elif self.region == True: # Disk
                distance = Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
                if distance >= radius:
                    distance = radius
                    self.ex, self.ey = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s1, 0.5, angle )
                else:
                    self.ex = ex
                    self.ey = ey
            # Variables
            self.v1 = hue
            self.v2 = distance / radius
            # Update
            if harmony == True and self.region == False and self.harmony_list != None:
                self.Ring_Harmony( hue )
            self.SIGNAL_VALUE.emit( self.wheel_space, self.v1, self.v2, self.v3 )
            self.Point_Move()
    def Previous_Rotation( self ):
        rotation = list()
        for item in self.gamut_list:
            px = self.disk_px + item[0] * self.disk_s1
            py = self.disk_py + item[1] * self.disk_s1
            dist = Trig_2D_Points_Distance( px, py, self.w2, self.h2 )
            angle = Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, px, py ) # angle in degrees
            rotation.append( [ dist, angle ] )
        return rotation
    # Ring
    def Ring_Harmony( self, angle ):
        list_dist = list()
        for i in range( 0, len( self.harmony_list ) ):
            index = i + 1
            if   self.wheel_mode == "DIGITAL":  har_angle = self.harmony_list[i]["hue_d"]
            elif self.wheel_mode == "ANALOG":   har_angle = self.harmony_list[i]["hue_a"]
            delta = Trig_2d_Angle_Delta( angle, har_angle )
            list_dist.append( [ delta, index ] )
        list_dist.sort()
        self.harmony_index = list_dist[0][1]
        self.SIGNAL_HARMONY_INDEX.emit( self.harmony_index )
    # Disk
    def Disk_Tangent( self, ex, ey ):
        delta_hue = ( ex - self.ox ) / self.ww
        self.v3 = Limit_Float( self.oz + delta_hue )
        self.SIGNAL_VALUE.emit( self.wheel_space, self.v1, self.v2, self.v3 )
    def Disk_Rotation( self, ex, ey ):
        ang_new = Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
        delta = Limit_Looper( ang_new - self.oa, 360 )
        for i in range( 0, len( self.previous_rotation ) ):
            # Read
            dis = self.previous_rotation[i][0]
            angle = self.previous_rotation[i][1]
            if dis != 0:
                radius = dis / self.disk_s1
                angle = Limit_Looper( angle + delta, 360 )
                dx, dy = Trig_2D_Angle_Circle( 0.5, 0.5, 1, radius, angle )
                item = [ dx, dy ]
                self.gamut_list[i] = item
    def Disk_Snap( self, ex, ey ):
        list_point = list()
        list_point = self.Point_Gamut( ex, ey, list_point )
        list_point = self.Point_Pin( ex, ey, list_point )
        if len( list_point ) > 0:
            list_point.sort( key = lambda row: row[0] )
            gamut_index = list_point[0][3] # gamut_index
            pin_index = list_point[0][4] # pin_index
            if gamut_index != None:
                self.gamut_index = gamut_index
                self.Cursor_Position( list_point[0][1], list_point[0][2], False )
            elif pin_index != None:
                self.pin_index = pin_index
                self.SIGNAL_PIN_INDEX.emit( self.pin_index )
    # Gamut
    def Gamut_List( self ):
        lista = list()
        if   self.gamut_mask == "TRIANGLE": lista = self.gi_t1
        elif self.gamut_mask == "SQUARE":   lista = self.gi_s1
        elif self.gamut_mask == "HEXAGON":  lista = self.gi_h1
        elif self.gamut_mask == "CIRCLE_1": lista = self.gi_c1
        elif self.gamut_mask == "CIRCLE_2": lista = self.gi_c2
        return lista
    def Gamut_Centroid( self, mode ):
        if   mode == "TRIANGLE":
            p = self.gi_t1
            c = Trig_2D_Centroid( [ p[1][0], p[2][0], p[3][0] ], [ p[1][1], p[2][1], p[3][1] ] )
            p[0] = [ c[0], c[1] ]
        elif mode == "SQUARE":
            p = self.gi_s1
            c = Trig_2D_Centroid( [ p[1][0], p[2][0], p[3][0], p[4][0] ], [ p[1][1], p[2][1], p[3][1], p[4][1] ] )
            p[0] = [ c[0], c[1] ]
        elif mode == "HEXAGON":
            p = self.gi_h1
            c = Trig_2D_Centroid( [ p[1][0], p[2][0], p[3][0], p[4][0], p[5][0], p[6][0] ], [ p[1][1], p[2][1], p[3][1], p[4][1], p[5][1], p[6][1] ] )
            p[0] = [ c[0], c[1] ]
        elif mode == "CIRCLE_1":
            p = self.gi_c1
            c = Trig_2D_Centroid( [ p[1][0], p[2][0], p[3][0], p[4][0] ], [ p[1][1], p[2][1], p[3][1], p[4][1] ] )
            p[0] = [ c[0], c[1] ]
        elif mode == "CIRCLE_2":
            # Circle 1
            p1 = self.gi_c2
            v1 = Trig_2D_Centroid( [ p1[1][0], p1[2][0], p1[3][0], p1[4][0] ], [ p1[1][1], p1[2][1], p1[3][1], p1[4][1] ] )
            self.gi_c2[0] = [ v1[0], v1[1] ]
            # Circle 2
            p2 = self.gi_c2
            v2 = Trig_2D_Centroid( [ p2[6][0], p2[7][0], p2[8][0], p2[9][0] ], [ p2[6][1], p2[7][1], p2[8][1], p2[9][1] ] )
            self.gi_c2[5] = [ v2[0], v2[1] ]
    def Gamut_Profile( self ):
        profile = [ self.gi_t1, self.gi_s1, self.gi_h1, self.gi_c1, self.gi_c2 ]
        self.SIGNAL_PROFILE.emit( profile )
    # Points
    def Point_Gamut( self, ex, ey, list_point ):
        for i in range( 0, len( self.gamut_list ) ):
            px = self.disk_px + self.gamut_list[i][0] * self.disk_s1
            py = self.disk_py + self.gamut_list[i][1] * self.disk_s1
            distance = Trig_2D_Points_Distance( ex, ey, px, py )
            list_point.append( [ distance, px, py, i, None ] ) # dist px py gamut_index, pin_index
        return list_point
    def Point_Pin( self, ex, ey, list_point ):
        if self.pin_list != None:
            for i in range( 0, len( self.pin_list ) - 1 ):
                pin = self.pin_list[i]
                if pin["active"] == True:
                    if self.wheel_mode == "DIGITAL": angle = pin["hue_d"] * 360
                    if self.wheel_mode == "ANALOG":  angle = pin["hue_a"] * 360 - hue_a
                    radius = pin[ self.id2 ]
                    px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s1 * 0.5, radius, angle )
                    distance = Trig_2D_Points_Distance( ex, ey, px, py )
                    list_point.append( [ distance, px, py, None, i ] ) # dist px py gamut_index, pin_index
        return list_point
    def Point_Move( self ):
        # Points
        if self.gamut_index != None:
            mx = ( self.ex - self.disk_px ) / self.disk_s1
            my = ( self.ey - self.disk_py ) / self.disk_s1
            lista = self.Gamut_List()
            lista[self.gamut_index] = [ mx, my ]
            self.Gamut_Centroid( self.gamut_mask )
        elif self.pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( self.wheel_space, self.v1, self.v2, self.v3, self.pin_index )
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        line_width = 5
        line_poly = 2
        radius = 0.5
        margin = 0.05
        dot1 = 5
        dot2 = 10

        # Circle Points
        list_point = list()
        if self.harmony_rule != None:
            for harmony in self.harmony_list:
                px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, Wheel_Angle( self.wheel_mode, harmony ) )
                list_point.append( [ px, py ] )
        else:
            px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, Wheel_Angle( self.wheel_mode, self.color_index ) )
            list_point.append( [ px, py ] )
        length = len( list_point )
        # Pin Points
        list_pin = list()
        if self.pin_list != None:
            for pin in self.pin_list:
                if pin["active"] == True:
                    px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, Wheel_Angle( self.wheel_mode, pin ) )
                    list_pin.append( [ px, py ] )

        # Dark Border
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_dark ) )
        painter.drawPath( self.circle_02 )
        # Dark Lines
        painter.setPen( QPen( self.c_dark, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        if self.wheel_mode == "DIGITAL":
            for digital in circle_digital:
                px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, digital )
                painter.drawLine( int( px ), int( py ), int( self.w2 ), int( self.h2 ) )
        if self.wheel_mode == "ANALOG":
            for analog in circle_analog:
                px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, analog - hue_a )
                painter.drawLine( int( px ), int( py ), int( self.w2 ), int( self.h2 ) )

        # Line Gray
        painter.setPen( QPen( self.c_lite, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        if length > 0:
            line_gray = QPainterPath()
            for point in list_point:
                line_gray.moveTo( int( self.w2 ), int( self.h2 ) )
                line_gray.lineTo( int( point[0] ), int( point[1] ) )
            painter.setClipPath( self.circle_02 )
            painter.drawPath( line_gray )

        # Ring Pin Points
        if self.pin_list != None:
            painter.setPen( QPen( self.c_lite, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            line_gray = QPainterPath()
            for pin in list_pin:
                line_gray.moveTo( int( self.w2 ), int( self.h2 ) )
                line_gray.lineTo( int( pin[0] ), int( pin[1] ) )
            painter.setClipPath( self.circle_12 )
            painter.drawPath( line_gray )
        # Reset Mask
        painter.setClipRect( 0, 0, self.ww, self.hh )

        # Draw Gradient
        if self.gamut_mask != "NONE":
            if self.gradient != None and self.axis > 0:
                try:
                    # Draw Pixmaps
                    painter.setPen( QtCore.Qt.NoPen )
                    painter.setBrush( QtCore.Qt.NoBrush )
                    index = int( self.v3 * self.axis )
                    qpixmap = self.gradient[index]
                    qbrush = QBrush( qpixmap )
                    if qpixmap.isNull() == False:
                        qtransform = QTransform()
                        qtransform.translate( int( self.disk_px ), int( self.disk_py ) )
                        qtransform.scale( int( self.disk_s1 ) / 255, int( self.disk_s1 ) / 255 )
                        qbrush.setTransform( qtransform )
                    # Painter
                    painter.setPen( QtCore.Qt.NoPen )
                    painter.setBrush( qbrush )
                except:
                    pass
            # Polygon
            gdx = self.disk_px
            gdy = self.disk_py
            gds = self.disk_s1
            if self.gamut_mask == "FULL":
                painter.setPen( QtCore.Qt.NoPen )
                painter.drawEllipse( int( gdx ), int( gdy ), int( gds ), int( gds ) )
            elif self.gamut_mask == "TRIANGLE":
                # Polygon
                painter.setPen( QtCore.Qt.NoPen )
                poly = QPolygon( [
                    QPoint( int( gdx + gds * self.gi_t1[1][0] ), int( gdy + gds * self.gi_t1[1][1] ) ),
                    QPoint( int( gdx + gds * self.gi_t1[2][0] ), int( gdy + gds * self.gi_t1[2][1] ) ),
                    QPoint( int( gdx + gds * self.gi_t1[3][0] ), int( gdy + gds * self.gi_t1[3][1] ) ),
                    ] )
                painter.drawPolygon( poly )
                # Display Subjective Primaries
                painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QBrush( self.c_white ) )
                painter.drawEllipse( int( gdx + gds * self.gi_t1[0][0] - dot1 ), int( gdy + gds * self.gi_t1[0][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_t1[1][0] - dot1 ), int( gdy + gds * self.gi_t1[1][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_t1[2][0] - dot1 ), int( gdy + gds * self.gi_t1[2][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_t1[3][0] - dot1 ), int( gdy + gds * self.gi_t1[3][1] - dot1 ), int( dot2 ), int( dot2 ) )
            elif self.gamut_mask == "SQUARE":
                # Polygon
                painter.setPen( QtCore.Qt.NoPen )
                poly = QPolygon( [
                    QPoint( int( gdx + gds * self.gi_s1[1][0] ), int( gdy + gds * self.gi_s1[1][1] ) ),
                    QPoint( int( gdx + gds * self.gi_s1[2][0] ), int( gdy + gds * self.gi_s1[2][1] ) ),
                    QPoint( int( gdx + gds * self.gi_s1[3][0] ), int( gdy + gds * self.gi_s1[3][1] ) ),
                    QPoint( int( gdx + gds * self.gi_s1[4][0] ), int( gdy + gds * self.gi_s1[4][1] ) ),
                    ] )
                painter.drawPolygon( poly )
                # Display Subjective Primaries
                painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QBrush( self.c_white ) )
                painter.drawEllipse( int( gdx + gds * self.gi_s1[0][0] - dot1 ), int( gdy + gds * self.gi_s1[0][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_s1[1][0] - dot1 ), int( gdy + gds * self.gi_s1[1][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_s1[2][0] - dot1 ), int( gdy + gds * self.gi_s1[2][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_s1[3][0] - dot1 ), int( gdy + gds * self.gi_s1[3][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_s1[4][0] - dot1 ), int( gdy + gds * self.gi_s1[4][1] - dot1 ), int( dot2 ), int( dot2 ) )
            elif self.gamut_mask == "HEXAGON":
                # Polygon
                painter.setPen( QtCore.Qt.NoPen )
                poly = QPolygon( [
                    QPoint( int( gdx + gds * self.gi_h1[1][0] ), int( gdy + gds * self.gi_h1[1][1] ) ),
                    QPoint( int( gdx + gds * self.gi_h1[2][0] ), int( gdy + gds * self.gi_h1[2][1] ) ),
                    QPoint( int( gdx + gds * self.gi_h1[3][0] ), int( gdy + gds * self.gi_h1[3][1] ) ),
                    QPoint( int( gdx + gds * self.gi_h1[4][0] ), int( gdy + gds * self.gi_h1[4][1] ) ),
                    QPoint( int( gdx + gds * self.gi_h1[5][0] ), int( gdy + gds * self.gi_h1[5][1] ) ),
                    QPoint( int( gdx + gds * self.gi_h1[6][0] ), int( gdy + gds * self.gi_h1[6][1] ) ),
                    ] )
                painter.drawPolygon( poly )
                # Display Subjective Primaries
                painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QBrush( self.c_white ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[0][0] - dot1 ), int( gdy + gds * self.gi_h1[0][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[1][0] - dot1 ), int( gdy + gds * self.gi_h1[1][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[2][0] - dot1 ), int( gdy + gds * self.gi_h1[2][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[3][0] - dot1 ), int( gdy + gds * self.gi_h1[3][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[4][0] - dot1 ), int( gdy + gds * self.gi_h1[4][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[5][0] - dot1 ), int( gdy + gds * self.gi_h1[5][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_h1[6][0] - dot1 ), int( gdy + gds * self.gi_h1[6][1] - dot1 ), int( dot2 ), int( dot2 ) )
            elif self.gamut_mask == "CIRCLE_1":
                # Profile Points
                path, P0, P1, P2, P3, P4 = self.Render_Circle( gdx, gdy, gds, self.gi_c1, self.circle_2 )
                # Polygon
                painter.setPen( QtCore.Qt.NoPen )
                painter.drawPath( path )
                # Display Subjective Primaries
                painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QBrush( self.c_white ) )
                painter.drawEllipse( int( P0[0] - dot1 ), int( P0[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P1[0] - dot1 ), int( P1[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P2[0] - dot1 ), int( P2[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P3[0] - dot1 ), int( P3[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P4[0] - dot1 ), int( P4[1] - dot1 ), int( dot2 ), int( dot2 ) )
            elif self.gamut_mask == "CIRCLE_2":
                # Profile Points
                path_0, P0_0, P1_0, P2_0, P3_0, P4_0 = self.Render_Circle( gdx, gdy, gds, self.gi_c2[0:5], self.circle_2 )
                path_1, P0_1, P1_1, P2_1, P3_1, P4_1 = self.Render_Circle( gdx, gdy, gds, self.gi_c2[5:10], self.circle_2 )
                # Polygon
                painter.setPen( QtCore.Qt.NoPen )
                painter.drawPath( path_0 )
                painter.drawPath( path_1 )
                # Display Subjective Primaries
                painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QBrush( self.c_white ) )
                # Circle 0
                painter.drawEllipse( int( P0_0[0] - dot1 ), int( P0_0[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P1_0[0] - dot1 ), int( P1_0[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P2_0[0] - dot1 ), int( P2_0[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P3_0[0] - dot1 ), int( P3_0[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P4_0[0] - dot1 ), int( P4_0[1] - dot1 ), int( dot2 ), int( dot2 ) )
                # Circle 1
                painter.drawEllipse( int( P0_1[0] - dot1 ), int( P0_1[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P1_1[0] - dot1 ), int( P1_1[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P2_1[0] - dot1 ), int( P2_1[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P3_1[0] - dot1 ), int( P3_1[1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( P4_1[0] - dot1 ), int( P4_1[1] - dot1 ), int( dot2 ), int( dot2 ) )
            """
            elif self.gamut_mask == "PIE_3":
                # Variables
                rect = QRect( int( gdx ), int( gdy ), int( gds ), int( gds ) )
                ang_a1 = +16 * Trig_2D_Points_Lines_Angle(
                    gdx + self.gi_p3[1][0] * gds, gdy + self.gi_p3[1][1] * gds,
                    self.w2, self.h2,
                    self.ww, self.h2,
                    )
                ang_a2 = -16 * Trig_2D_Points_Lines_Angle(
                    gdx + self.gi_p3[1][0] * gds, gdy + self.gi_p3[1][1] * gds,
                    self.w2, self.h2,
                    gdx + self.gi_p3[2][0] * gds, gdy + self.gi_p3[2][1] * gds,
                    )
                ang_b1 = +16 * Trig_2D_Points_Lines_Angle(
                    gdx + self.gi_p3[3][0] * gds, gdy + self.gi_p3[3][1] * gds,
                    self.w2, self.h2,
                    self.ww, self.h2,
                    )
                ang_b2 = -16 * Trig_2D_Points_Lines_Angle(
                    gdx + self.gi_p3[3][0] * gds, gdy + self.gi_p3[3][1] * gds,
                    self.w2, self.h2,
                    gdx + self.gi_p3[4][0] * gds, gdy + self.gi_p3[4][1] * gds,
                    )
                ang_c1 = +16 * Trig_2D_Points_Lines_Angle(
                    gdx + self.gi_p3[5][0] * gds, gdy + self.gi_p3[5][1] * gds,
                    self.w2, self.h2,
                    self.ww, self.h2,
                    )
                ang_c2 = -16 * Trig_2D_Points_Lines_Angle(
                    gdx + self.gi_p3[5][0] * gds, gdy + self.gi_p3[5][1] * gds,
                    self.w2, self.h2,
                    gdx + self.gi_p3[6][0] * gds, gdy + self.gi_p3[6][1] * gds,
                    )

                # Polygon
                painter.setPen( QtCore.Qt.NoPen )
                painter.drawPie( rect, int( ang_a1 ), int( ang_a2 ) )
                painter.drawPie( rect, int( ang_b1 ), int( ang_b2 ) )
                painter.drawPie( rect, int( ang_c1 ), int( ang_c2 ) )
                # Display Subjective Primaries
                painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QBrush( self.c_white ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[0][0] - dot1 ), int( gdy + gds * self.gi_p3[0][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[1][0] - dot1 ), int( gdy + gds * self.gi_p3[1][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[2][0] - dot1 ), int( gdy + gds * self.gi_p3[2][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[3][0] - dot1 ), int( gdy + gds * self.gi_p3[3][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[4][0] - dot1 ), int( gdy + gds * self.gi_p3[4][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[5][0] - dot1 ), int( gdy + gds * self.gi_p3[5][1] - dot1 ), int( dot2 ), int( dot2 ) )
                painter.drawEllipse( int( gdx + gds * self.gi_p3[6][0] - dot1 ), int( gdy + gds * self.gi_p3[6][1] - dot1 ), int( dot2 ), int( dot2 ) )
            """

        # Analyse Colors
        if self.analyse_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_gray ) )
            tone = int( self.v3 * 255 )
            for color in self.analyse_list:
                if int( color[ self.id3 ] * 255 ) == tone:
                    angle = Wheel_Angle( self.wheel_mode, color )
                    radius = color[ self.id2 ]
                    px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s2, radius, angle )
                    painter.drawEllipse( int( px - dot1 ), int( py - dot1 ), int( dot2 ), int( dot2 ) )

        # Pinned Colors
        if self.pin_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for pin in self.pin_list:
                if pin["active"] == True:
                    angle = Wheel_Angle( self.wheel_mode, pin )
                    radius = pin[ self.id2 ]
                    px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s2, radius, angle )
                    painter.drawEllipse( int( px - dot1 ), int( py - dot1 ), int( dot2 ), int( dot2 ) )

        # Harmony Colors
        if ( self.color_index != None and self.harmony_list != None ):
            # Parsing
            list_harmony = list()
            for harmony in self.harmony_list:
                angle = Wheel_Angle( self.wheel_mode, harmony )
                radius = harmony[ self.id2 ]
                har_x, har_y = Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_s2, radius, angle )
                list_harmony.append( [ har_x, har_y ] )
            length = len( list_harmony )
            # Draw Line
            painter.setPen( QPen( self.c_white, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( list_harmony[i-1][0] ), int( list_harmony[i-1][1] ), int( list_harmony[i][0] ), int( list_harmony[i][1] ) )
            if self.harmony_rule in [ harmony_3, harmony_4 ]:
                painter.drawLine( int( list_harmony[0][0] ), int( list_harmony[0][1] ), int( list_harmony[length-1][0] ), int( list_harmony[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( list_harmony[i][0] - dot1 ), int( list_harmony[i][1] - dot1 ), int( dot2 ), int( dot2 ) )

        # Cursor
        Cursor_Display( self, painter )
    def Render_Circle( self, px, py, side, points, circle ):
        # Points from User
        P0 = [ px + points[0][0] * side, py + points[0][1] * side ]
        P1 = [ px + points[1][0] * side, py + points[1][1] * side ]
        P2 = [ px + points[2][0] * side, py + points[2][1] * side ]
        P3 = [ px + points[3][0] * side, py + points[3][1] * side ]
        P4 = [ px + points[4][0] * side, py + points[4][1] * side ]
        # Angles from the Points
        O1 = Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P1[0],P1[1] )
        O2 = Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P2[0],P2[1] )
        O3 = Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P3[0],P3[1] )
        O4 = Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P4[0],P4[1] )
        # Order Angles in Sequence
        order = [ ( O1, P1 ), ( O2, P2 ), ( O3, P3 ), ( O4, P4 ) ]
        order.sort()
        A1 = order[0][1]
        A2 = order[1][1]
        A3 = order[2][1]
        A4 = order[3][1]
        # Bridge Points
        B12 = [ Lerp_1D( 0.5, A1[0], A2[0] ), Lerp_1D( 0.5, A1[1], A2[1] ) ]
        B23 = [ Lerp_1D( 0.5, A2[0], A3[0] ), Lerp_1D( 0.5, A2[1], A3[1] ) ]
        B34 = [ Lerp_1D( 0.5, A3[0], A4[0] ), Lerp_1D( 0.5, A3[1], A4[1] ) ]
        B41 = [ Lerp_1D( 0.5, A4[0], A1[0] ), Lerp_1D( 0.5, A4[1], A1[1] ) ]
        # Bridge Components
        dist_B12 = Trig_2D_Ortogonal_Components( P0[0], P0[1], B12[0], B12[1] )
        dist_B23 = Trig_2D_Ortogonal_Components( P0[0], P0[1], B23[0], B23[1] )
        dist_B34 = Trig_2D_Ortogonal_Components( P0[0], P0[1], B34[0], B34[1] )
        dist_B41 = Trig_2D_Ortogonal_Components( P0[0], P0[1], B41[0], B41[1] )
        # Intermediate Points
        scalar = 2
        P12 = [ P0[0] + scalar * dist_B12[0], P0[1] + scalar * dist_B12[1] ]
        P23 = [ P0[0] + scalar * dist_B23[0], P0[1] + scalar * dist_B23[1] ]
        P34 = [ P0[0] + scalar * dist_B34[0], P0[1] + scalar * dist_B34[1] ]
        P41 = [ P0[0] + scalar * dist_B41[0], P0[1] + scalar * dist_B41[1] ]
        # Painter Path Object
        path = QPainterPath()
        a = 0.551915024494
        b = 1 - 0.551915024494
        path.moveTo( A1[0], A1[1] )
        path.cubicTo(
            QPoint( int( Lerp_1D( a, A1[0], P12[0] ) ), int( Lerp_1D( a, A1[1], P12[1] ) ) ),
            QPoint( int( Lerp_1D( b, P12[0], A2[0] ) ), int( Lerp_1D( b, P12[1], A2[1] ) ) ),
            QPoint( int( A2[0] ), int( A2[1] ) ) )
        path.cubicTo(
            QPoint( int( Lerp_1D( a, A2[0], P23[0] ) ), int( Lerp_1D( a, A2[1], P23[1] ) ) ),
            QPoint( int( Lerp_1D( b, P23[0], A3[0] ) ), int( Lerp_1D( b, P23[1], A3[1] ) ) ),
            QPoint( int( A3[0] ), int( A3[1] ) ) )
        path.cubicTo(
            QPoint( int( Lerp_1D( a, A3[0], P34[0] ) ), int( Lerp_1D( a, A3[1], P34[1] ) ) ),
            QPoint( int( Lerp_1D( b, P34[0], A4[0] ) ), int( Lerp_1D( b, P34[1], A4[1] ) ) ),
            QPoint( int( A4[0] ), int( A4[1] ) ) )
        path.cubicTo(
            QPoint( int( Lerp_1D( a, A4[0], P41[0] ) ), int( Lerp_1D( a, A4[1], P41[1] ) ) ),
            QPoint( int( Lerp_1D( b, P41[0], A1[0] ) ), int( Lerp_1D( b, P41[1], A1[1] ) ) ),
            QPoint( int( A1[0] ), int( A1[1] ) ) )
        path = path.intersected( circle )
        # Return
        return path, P0, P1, P2, P3, P4

class Panel_Hexagon( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str, float, float, float )
    SIGNAL_DEPTH = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( str, float, float, float, int )

    # Init
    def __init__( self, parent ):
        super( Panel_Hexagon, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.side = 0
        # Event
        self.ex = 0
        self.ey = 0
        self.ox = 0
        self.oy = 0
        self.oz = 0
        self.od = 0
        # Point
        self.px = 0
        self.py = 0
        # State
        self.zoom = False
        self.axis = 0 # 360 255
        # Panel
        self.gradient = None
        self.id1 = "uvd_1"
        self.id2 = "uvd_2"
        self.id3 = "uvd_3"
        self.v1 = 0
        self.v2 = 0
        self.v3 = 0

        # Color
        self.c_lite = QColor( "#ffffff" )
        self.c_dark = QColor( "#000000" )
        self.c_white = QColor( "#ffffff" )
        self.c_gray = QColor( "#b0b0b0" )
        self.c_black = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
        self.color_index = None
        # Harmony
        self.harmony_rule = None
        self.harmony_index = None
        self.harmony_list = None
        # Pin
        self.pin_list = None
        self.pin_index = None
        # Analyse
        self.analyse_list = None
    # Set
    def Set_Size( self, ww, hh, point ):
        # Variables
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Frame
        self.side = min( self.ww, self.hh )
        if self.ww >= self.hh:
            self.px = self.w2 - self.h2
            self.py = 0
        else:
            self.px = 0
            self.py = self.h2 - self.w2
        # Origin Points
        self.O1 = point[0]
        self.O2 = point[1]
        self.O3 = point[2]
        self.O4 = point[3]
        self.O5 = point[4]
        self.O6 = point[5]
        self.C61 = point[11]
        # Circles
        self.circle_0, self.circle_1, self.circle_2, self.circle_3 = Circles( self.px, self.py, self.side )
        self.circle_02 = self.circle_0.subtracted( self.circle_2 )
        # Update
        self.resize( ww, hh )
    def Set_Theme( self, c_lite, c_dark ):
        self.c_lite = QColor( c_lite )
        self.c_dark = QColor( c_dark )
        self.update()
    # Updates
    def Update_Color( self, color_index, point ):
        # Variables
        self.color_index = color_index
        self.hex_code = QColor( self.color_index[ "display" ] )
        # Values
        self.v1 = self.color_index["uvd_1"]
        self.v2 = self.color_index["uvd_2"]
        self.v3 = self.color_index["uvd_3"]
        self.ex = self.px + ( 0.5 + self.v1 * 0.5 ) * self.side
        self.ey = self.py + ( 0.5 - self.v2 * 0.5 ) * self.side
        # Origin Points
        self.O1 = point[0]
        self.O2 = point[1]
        self.O3 = point[2]
        self.O4 = point[3]
        self.O5 = point[4]
        self.O6 = point[5]
        self.C61 = point[11]
        # Update
        self.update()
    def Update_Gradient( self, gradient ):
        self.gradient = gradient
        self.axis = len( gradient ) - 1
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse_list ):
        self.analyse_list = analyse_list
        self.update()
    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # Variables
        self.ox = ex
        self.oy = ey
        self.oz = self.v3
        self.od = Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey ); self.zoom = True
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.RightButton ): self.Cursor_Gamma( ex, ey )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Snap( ex, ey )
        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey ); self.zoom = True
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.RightButton ): self.Cursor_Gamma( ex, ey )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Position( ex, ey )
        # Update
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey ); self.zoom = True
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.RightButton ): self.Cursor_Gamma( ex, ey )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Position( ex, ey )
        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.zoom = False
        self.pin_index = None
        # Updates
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Interaction
    def Cursor_Position( self, ex, ey ):
        # Calculation
        if ( self.v3 <= 0 or self.v3 >= 1 ):
            self.ex = self.w2
            self.ey = self.h2
        else:
            self.ex, self.ey = self.Hexagon_Intersection( ex, ey, self.v3 )
        self.v1 = +2 * ( ( self.ex - self.px ) / self.side ) - 1
        self.v2 = -2 * ( ( self.ey - self.py ) / self.side ) + 1
        # Signal
        self.SIGNAL_VALUE.emit( "UVD", self.v1, self.v2, self.v3 )
        if self.pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( "UVD", self.v1, self.v2, self.v3, self.pin_index )
    def Cursor_Tangent( self, ex ):
        delta_hue = ( ex - self.ox ) / self.ww
        self.v3 = Limit_Float( self.oz + delta_hue )
        self.SIGNAL_DEPTH.emit( self.v3 )
    def Cursor_Gamma( self, ex, ey ):
        # Variables
        angle = Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
        ex, ey = Trig_2D_Points_Rotate( self.w2, self.h2, self.od, angle )
        self.ex, self.ey = self.Hexagon_Intersection( ex, ey, self.v3 )
        self.v1 = +2 * ( ( self.ex - self.px ) / self.side ) - 1
        self.v2 = -2 * ( ( self.ey - self.py ) / self.side ) + 1
        # Signal
        self.SIGNAL_VALUE.emit( "UVD", self.v1, self.v2, self.v3 )
        if self.pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( "UVD", self.v1, self.v2, self.v3, self.pin_index )
    def Cursor_Snap( self, ex, ey ):
        if self.pin_list != None:
            distance = list()
            for i in range( 0, len( self.pin_list ) ):
                pin = self.pin_list[i]
                if pin["active"] == True:
                    px = self.px + ( 0.5 + pin["uvd_1"] * 0.5 ) * self.side
                    py = self.py + ( 0.5 - pin["uvd_2"] * 0.5 ) * self.side
                    dist = Trig_2D_Points_Distance( ex, ey, px, py )
                    distance.append( ( dist, i ) )
            if len( distance ) > 0:
                distance.sort()
                pin_index = distance[0][1]
                if pin_index <= pin_range:
                    self.pin_index = pin_index
                    self.SIGNAL_PIN_INDEX.emit( self.pin_index )
    # Panel Modifiers
    def Hexagon_Intersection( self, ex, ey, d ):
        # Variables
        red_x = self.px + self.C61[0] * self.side; red_y = self.py + self.C61[1] * self.side
        o1_x  = self.px + self.O1[0]  * self.side; o1_y  = self.py + self.O1[1]  * self.side
        o2_x  = self.px + self.O2[0]  * self.side; o2_y  = self.py + self.O2[1]  * self.side
        o3_x  = self.px + self.O3[0]  * self.side; o3_y  = self.py + self.O3[1]  * self.side
        o4_x  = self.px + self.O4[0]  * self.side; o4_y  = self.py + self.O4[1]  * self.side
        o5_x  = self.px + self.O5[0]  * self.side; o5_y  = self.py + self.O5[1]  * self.side
        o6_x  = self.px + self.O6[0]  * self.side; o6_y  = self.py + self.O6[1]  * self.side
        # Single Points
        di = round( d * 3, 14 )
        if ( di <= 0 or di >= 3 ):
            ex = self.w2
            ey = self.h2
        else:
            # Angles
            a0 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, ex, ey )
            a1 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o1_x, o1_y )
            a2 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o2_x, o2_y )
            a3 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o3_x, o3_y )
            a4 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o4_x, o4_y )
            a5 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o5_x, o5_y )
            a6 = Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o6_x, o6_y )
            if a6 == 0: a6 = 360
            # Limit
            if a0 <= a1:                    lx, ly = Trig_2D_Points_Lines_Intersection( red_x, red_y, o1_x, o1_y, ex, ey, self.w2, self.h2 )
            elif ( a0 >= a1 and a0 <= a2 ): lx, ly = Trig_2D_Points_Lines_Intersection( o1_x, o1_y, o2_x, o2_y, ex, ey, self.w2, self.h2 )
            elif ( a0 >= a2 and a0 <= a3 ): lx, ly = Trig_2D_Points_Lines_Intersection( o2_x, o2_y, o3_x, o3_y, ex, ey, self.w2, self.h2 )
            elif ( a0 >= a3 and a0 <= a4 ): lx, ly = Trig_2D_Points_Lines_Intersection( o3_x, o3_y, o4_x, o4_y, ex, ey, self.w2, self.h2 )
            elif ( a0 >= a4 and a0 <= a5 ): lx, ly = Trig_2D_Points_Lines_Intersection( o4_x, o4_y, o5_x, o5_y, ex, ey, self.w2, self.h2 )
            elif ( a0 >= a5 and a0 <= a6 ): lx, ly = Trig_2D_Points_Lines_Intersection( o5_x, o5_y, o6_x, o6_y, ex, ey, self.w2, self.h2 )
            elif a0 >= a6:                  lx, ly = Trig_2D_Points_Lines_Intersection( o6_x, o6_y, red_x, red_y, ex, ey, self.w2, self.h2 )
            else:                           lx, ly = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, Trig_2D_Points_Distance( o1_x, o1_y, self.w2, self.h2 ), a0 )
            # Distance
            event_dist = Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
            limit_dist = Trig_2D_Points_Distance( lx, ly, self.w2, self.h2 )
            if event_dist >= limit_dist:
                ex = lx
                ey = ly
        # Return
        return ex, ey
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        line_width = 5
        line_poly = 2
        radius = 0.5
        margin = 0.05
        dot1 = 5
        dot2 = 10

        # Dark Border
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_dark ) )
        painter.drawPath( self.circle_02 )
        # Dark Lines Color Reference
        painter.setPen( QPen( self.c_dark, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        for hexagon in circle_hexagon:
            px, py = Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, hexagon )
            painter.drawLine( int( px ), int( py ), int( self.w2 ), int( self.h2 ) )

        # Draw Gradient
        if self.axis > 0:
            try:
                # Draw Masks
                hexagon = QPainterPath()
                hexagon.moveTo( int( self.px + self.O1[0] * self.side ), int( self.py + self.O1[1] * self.side ) )
                hexagon.lineTo( int( self.px + self.O2[0] * self.side ), int( self.py + self.O2[1] * self.side ) )
                hexagon.lineTo( int( self.px + self.O3[0] * self.side ), int( self.py + self.O3[1] * self.side ) )
                hexagon.lineTo( int( self.px + self.O4[0] * self.side ), int( self.py + self.O4[1] * self.side ) )
                hexagon.lineTo( int( self.px + self.O5[0] * self.side ), int( self.py + self.O5[1] * self.side ) )
                hexagon.lineTo( int( self.px + self.O6[0] * self.side ), int( self.py + self.O6[1] * self.side ) )
                painter.setClipPath( hexagon )

                # Draw Pixmaps
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( QtCore.Qt.NoBrush )
                index = int( self.v3 * self.axis )
                qpixmap = self.gradient[index]
                if qpixmap.isNull() == False:
                    render = qpixmap.scaled( self.side, self.side, Qt.IgnoreAspectRatio, Qt.FastTransformation )
                    painter.drawPixmap( int( self.px ), int( self.py ), render )

                # Reset Mask
                square = QPainterPath()
                square.moveTo( int( 0 ), int( 0 ) )
                square.lineTo( int( self.ww ), int( 0 ) )
                square.lineTo( int( self.ww ), int( self.hh ) )
                square.lineTo( int( 0 ), int( self.hh ) )
                painter.setClipPath( square )
            except:
                pass

        # Analyse Colors
        if self.analyse_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_gray ) )
            gamma = int( self.v3 * 360 )
            for color in self.analyse_list:
                if int( color[ self.id3 ] * 360 ) == gamma:
                    px = self.px + ( 0.5 + color["uvd_1"] * 0.5 ) * self.side
                    py = self.py + ( 0.5 - color["uvd_2"] * 0.5 ) * self.side
                    painter.drawEllipse( int( px - dot1 ), int( py - dot1 ), dot2, dot2 )

        # Pinned Colors
        if self.pin_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for pin in self.pin_list:
                if pin["active"] == True:
                    cx = self.px + ( 0.5 + pin["uvd_1"] * 0.5 ) * self.side
                    cy = self.py + ( 0.5 - pin["uvd_2"] * 0.5 ) * self.side
                    painter.drawEllipse( int( cx - dot1 ), int( cy - dot1 ), int( dot2 ), int( dot2 ) )

        # Harmony Colors
        if self.harmony_list != None:
            # Parsing
            points = list()
            for harmony in self.harmony_list:
                har_x = self.px + ( 0.5 + harmony["uvd_1"] * 0.5 ) * self.side
                har_y = self.py + ( 0.5 - harmony["uvd_2"] * 0.5 ) * self.side
                points.append( [ har_x, har_y ] )
            length = len( points )
            # Draw Line
            painter.setPen( QPen( self.c_white, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( points[i-1][0] ), int( points[i-1][1] ), int( points[i][0] ), int( points[i][1] ) )
            if self.harmony_rule in [ harmony_3, harmony_4 ]:
                painter.drawLine( int( points[0][0] ), int( points[0][1] ), int( points[length-1][0] ), int( points[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( points[i][0] - dot1 ), int( points[i][1] - dot1 ), int( dot2 ), int( dot2 ) )

        # Cursor
        Cursor_Display( self, painter )

class Panel_Luma( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str, float, float, float )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( str, float, float, float, int )

    # Init
    def __init__( self, parent ):
        super( Panel_Luma, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Varibles
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        # Event
        self.ex = 0
        self.ey = 0
        self.ox = 0
        self.oy = 0
        self.ot = 0
        # State
        self.zoom = False
        self.axis = 0 # 360 255
        # Panel
        self.gradient = None
        self.id1 = "yuv_1"
        self.id2 = "yuv_2"
        self.id3 = "yuv_3"
        self.v1 = 0 # 0-360 event tangent
        self.v2 = 0
        self.v3 = 0
        # Colors
        self.c_white = QColor( "#ffffff" )
        self.c_gray = QColor( "#b0b0b0" )
        self.c_black = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
        self.color_index = None
        # Harmony
        self.harmony_rule = None
        self.harmony_index = None
        self.harmony_list = None
        # Pin
        self.pin_list = None
        self.pin_index = None
        # Analyse
        self.analyse_list = None
    # Set
    def Set_Size( self, ww, hh ):
        # Variables
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Mask ( slightly bigger than color display )
        polygon = QPolygon( [
            QPoint( -1, -1 ),
            QPoint( self.ww + 1, -1 ),
            QPoint( self.ww + 1, self.hh + 1 ),
            QPoint( -1, self.hh + 1 ),
            ] )
        square = QRegion( polygon, Qt.OddEvenFill )
        self.setMask( square )
        # Update
        self.resize( ww, hh )
    def Set_Zoom( self, boolean ):
        self.zoom = boolean
        self.update()
    # Updates
    def Update_Color( self, color_index ):
        # Variables
        self.color_index = color_index
        self.hex_code = QColor( self.color_index["display"] )
        # Values
        self.v1 = self.color_index[ self.id1 ]
        self.ex = self.color_index[ self.id2 ] * self.ww
        self.ey = ( 1 - self.color_index[ self.id3 ] ) * self.hh
        # Update
        self.update()
    def Update_Gradient( self, gradient ):
        self.gradient = gradient
        self.axis = len( gradient ) - 1
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse_list ):
        self.analyse_list = analyse_list
        self.update()
    # Mouse Event
    def mousePressEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # Variables
        self.ox = ex
        self.oy = ey
        self.ot = self.v1
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  pass
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Snap( ex, ey )
        self.update()
    def mouseMoveEvent( self, event ):
        # Events
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Position( ex, ey, False )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Tangent( ex )
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Snap( ex, ey )
        # RMB
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.RightButton ):     self.Cursor_Position( ex, ey, False )
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.zoom = False
        self.ot = 0
        self.pin_index = None
        # Updates
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Mouse Function
    def Cursor_Position( self, ex, ey, zoom ):
        # Variables
        self.zoom = zoom
        # Cursor
        self.ex = Limit_Range( ex, 0, self.ww )
        self.ey = Limit_Range( ey, 0, self.hh )
        # Color
        px =  self.ex / self.ww
        py = ( self.hh - self.ey ) / self.hh
        # Variables
        v2 = ex / self.ww
        v3 = ( self.hh - ey ) / self.hh
        # Limit
        self.v2 = Limit_Float( v2 )
        self.v3 = Limit_Float( v3 )
        # Signals
        self.SIGNAL_VALUE.emit( "YUV", self.v1, self.v2, self.v3 )
        if self.pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( "YUV", self.v1, self.v2, self.v3, self.pin_index )
    def Cursor_Tangent( self, ex ):
        # Hue
        delta_hue = ( ( ex - self.ox ) / self.ww )
        angle = self.ot + delta_hue
        self.v1 = Limit_Range( angle, 0, 1 )
        # Signals
        self.SIGNAL_VALUE.emit( "YUV", self.v1, self.v2, self.v3 )
    def Cursor_Snap( self, ex, ey ):
        if self.pin_list != None:
            distance = list()
            for i in range( 0, len( self.pin_list ) ):
                if self.pin_list[i]["active"] == True:
                    px = self.pin_list[i][ self.id2 ] * self.ww
                    py = ( 1 - self.pin_list[i][ self.id3 ] ) * self.hh
                    dist = Trig_2D_Points_Distance( ex, ey, px, py )
                    distance.append( ( dist, i ) )
            if len( distance ) > 0:
                distance.sort()
                pin_index = distance[0][1]
                if pin_index <= pin_range:
                    self.pin_index = pin_index
                    self.SIGNAL_PIN_INDEX.emit( self.pin_index )
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        line_width = 2
        line_poly = 2
        dot1 = 5
        dot2 = 10

        # Draw Gradient
        if self.gradient != None and self.axis > 0:
            try:
                # Draw Pixmaps
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( QtCore.Qt.NoBrush )
                index = int( self.v1 * self.axis )
                qpixmap = self.gradient[index]
                render = qpixmap.scaled( self.ww, self.hh, Qt.IgnoreAspectRatio, Qt.FastTransformation )
                painter.drawPixmap( 0, 0, render )
            except:
                pass

        # Lines
        painter.setPen( QPen( self.c_black, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        painter.drawLine( int( 0 ), int( self.h2 ), int( self.ww ), int( self.h2 ) )
        painter.drawLine( int( self.w2 ), int( 0 ), int( self.w2 ), int( self.hh ) )

        # Analyse Colors
        if self.analyse_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_gray ) )
            hue = int( self.v1 * 360 )
            for color in self.analyse_list:
                if int( color[ self.id1 ] * 360 ) == hue:
                    px = color[ self.id2 ] * self.ww
                    py = ( 1 - color[ self.id3 ] ) * self.hh
                    painter.drawEllipse( int( px - dot1 ), int( py - dot1 ), dot2, dot2 )

        # Pinned Colors
        if self.pin_list != None:
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for pin in self.pin_list:
                if pin["active"] == True:
                    painter.drawEllipse( 
                        int( ( pin[ self.id2 ] * self.ww ) - dot1 ),
                        int( ( ( 1 - pin[ self.id3 ] ) * self.hh ) - dot1 ),
                        dot2,
                        dot2,
                        )

        # Harmony Colors
        if self.harmony_list != None:
            # Parsing
            points = list()
            for harmony in self.harmony_list:
                har_x = harmony[ self.id2 ] * self.ww
                har_y = ( 1 - harmony[ self.id3 ] ) * self.hh
                points.append( [ har_x, har_y ] )
            length = len( points )
            # Draw Line
            painter.setPen( QPen( self.c_white, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( points[i-1][0] ), int( points[i-1][1] ), int( points[i][0] ), int( points[i][1] ) )
            if self.harmony_rule in [ harmony_3, harmony_4 ]:
                painter.drawLine( int( points[0][0] ), int( points[0][1] ), int( points[length-1][0] ), int( points[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.c_black, line_poly, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.c_white ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( points[i][0] - dot1 ), int( points[i][1] - dot1 ), int( dot2 ), int( dot2 ) )

        # Cursor
        Cursor_Display( self, painter )

class Panel_Plane( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_SWAP = QtCore.pyqtSignal( int, int )
    SIGNAL_RANDOM = QtCore.pyqtSignal()
    SIGNAL_RESET = QtCore.pyqtSignal()

    # Init
    def __init__( self, parent ):
        super( Panel_Plane, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        # Event
        self.ex = 0
        self.ey = 0
        self.ox = 0
        self.oy = 0
        # State
        self.zoom = False
        self.state_box = False
        self.state_tl = False
        self.state_tr = False
        self.state_bl = False
        self.state_br = False
        # Plane
        self.plane_matrix = None
        self.plane_margin = 0
        self.plane_split = 0
        self.plane_dx = 0
        self.plane_dy = 0
        self.plane_index = None
        self.plane_swap = [ None, None ]
        # Colors
        self.c_dark = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
    # Set
    def Set_Size( self, ww, hh ):
        # Variables
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Update
        self.resize( ww, hh )
    def Set_Theme( self, c_dark ):
        self.c_dark = QColor( c_dark )
        self.update()
    # Update
    def Update_Gradient( self, ww, hh, plane_matrix, plane_margin, plane_split ):
        # Size
        self.Set_Size( ww, hh )
        # Variables
        self.plane_matrix = plane_matrix
        self.plane_margin = int( plane_margin )
        self.plane_split = int( plane_split )
        self.plane_dx = len( self.plane_matrix[0] )
        self.plane_dy = len( self.plane_matrix )
        self.ex = -100
        self.ey = -100
        # Update
        self.update()
    # Mouse Event
    def mousePressEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        self.ox = ex
        self.oy = ey
        # Variables
        self.Cursor_Location( ex, ey )
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  self.Cursor_Index()
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Source( ex, ey )
        # RMB
        if em == QtCore.Qt.NoModifier and eb == QtCore.Qt.RightButton:
            self.operation = None
            self.Context_Menu( event )
        self.update()
    def mouseMoveEvent( self, event ):
        # Events
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Position( ex, ey, False )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Position( ex, ey, True )
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  pass
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      self.Cursor_Swap( ex, ey )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # Variables
        self.Cursor_Location( ex, ey )
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Index()
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Index()
        if ( em == QtCore.Qt.ControlModifier and eb == QtCore.Qt.LeftButton ):  pass
        if ( em == QtCore.Qt.AltModifier and eb == QtCore.Qt.LeftButton ):      pass
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.zoom = False
        self.state_box = False
        self.state_tl = False
        self.state_tr = False
        self.state_bl = False
        self.state_br = False
        self.plane_index = None
        # Swap
        if self.plane_swap[0] != None and self.plane_swap[1] != None:
            self.SIGNAL_SWAP.emit( self.plane_swap[0], self.plane_swap[1] )
            self.plane_swap = [ None, None ]
        # Updates
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Mouse Function
    def Cursor_Location( self, ex, ey ):
        if self.plane_matrix != None:
            # Variables
            pm = self.plane_margin
            wm = self.ww - self.plane_margin
            hm = self.hh - self.plane_margin
            # Read
            tl = self.plane_matrix[0][0]
            tr = self.plane_matrix[0][-1]
            bl = self.plane_matrix[-1][0]
            br = self.plane_matrix[-1][-1]
            tl_hc, tl_px, tl_py, tl_pw, tl_ph, tl_pr, tl_pb = tl[0], tl[1], tl[2], tl[3], tl[4], tl[5], tl[6]
            tr_hc, tr_px, tr_py, tr_pw, tr_ph, tr_pr, tr_pb = tr[0], tr[1], tr[2], tr[3], tr[4], tr[5], tr[6]
            bl_hc, bl_px, bl_py, bl_pw, bl_ph, bl_pr, bl_pb = bl[0], bl[1], bl[2], bl[3], bl[4], bl[5], bl[6]
            br_hc, br_px, br_py, br_pw, br_ph, br_pr, br_pb = br[0], br[1], br[2], br[3], br[4], br[5], br[6]
            # Check Color
            check_box = ( tl_px < ex < wm ) and ( tl_py < ey < hm )
            check_tl = ( ex <= tl_pr ) and ( ey <= tl_pb )
            check_tr = ( ex >= tr_px ) and ( ey <= tr_pb )
            check_bl = ( ex <= bl_pr ) and ( ey >= bl_pb )
            check_br = ( ex >= br_px ) and ( ey >= br_pb )
            # Check Color
            if   check_box == True: self.plane_index = None; self.state_box = True
            elif check_tl == True:  self.plane_index = 0;    self.state_tl = True
            elif check_tr == True:  self.plane_index = 1;    self.state_tr = True
            elif check_bl == True:  self.plane_index = 2;    self.state_bl = True
            elif check_br == True:  self.plane_index = 3;    self.state_br = True
    def Cursor_Position( self, ex, ey, zoom ):
        # Variables
        self.zoom = zoom
        # Input
        if self.plane_matrix != None and self.state_box == True:
            # Search Y
            for y in range( 0, self.plane_dy ):
                line = self.plane_matrix[y][0]
                py, pb = line[2], line[6]
                if py <= ey <= pb:
                    # Search X
                    for x in range( 0, self.plane_dx ):
                        column = self.plane_matrix[y][x]
                        px, pr = column[1], column[5]
                        if px <= ex <= pr:
                            item = self.plane_matrix[y][x]
                            self.hex_code, px, py, pw, ph = item[0], item[1], item[2], item[3], item[4]
                            self.ex = int( px + 0.5 * pw )
                            self.ey = int( py + 0.5 * ph )
                            self.SIGNAL_VALUE.emit( self.hex_code )
    def Cursor_Index( self ):
        if self.plane_index != None:
            self.SIGNAL_INDEX.emit( self.plane_index )
    def Cursor_Source( self, ex, ey ):
        if   ( ex < self.w2 and ey < self.h2 ): self.plane_swap[0] = 0
        elif ( ex > self.w2 and ey < self.h2 ): self.plane_swap[0] = 1
        elif ( ex < self.w2 and ey > self.h2 ): self.plane_swap[0] = 2
        elif ( ex > self.w2 and ey > self.h2 ): self.plane_swap[0] = 3
        else:                                   self.plane_swap[0] = None
    def Cursor_Swap( self, ex, ey ):
        if   ( ex < self.w2 and ey < self.h2 ):
            self.plane_swap[1] = 0
            self.state_tl = True
            self.state_tr = False
            self.state_bl = False
            self.state_br = False
        elif ( ex > self.w2 and ey < self.h2 ):
            self.plane_swap[1] = 1
            self.state_tl = False
            self.state_tr = True
            self.state_bl = False
            self.state_br = False
        elif ( ex < self.w2 and ey > self.h2 ):
            self.plane_swap[1] = 2
            self.state_tl = False
            self.state_tr = False
            self.state_bl = True
            self.state_br = False
        elif ( ex > self.w2 and ey > self.h2 ):
            self.plane_swap[1] = 3
            self.state_tl = False
            self.state_tr = False
            self.state_bl = False
            self.state_br = True
        else:
            self.plane_swap[1] = None
    # Menu
    def Context_Menu( self, event ):
        # Menu
        qmenu = QMenu( self )
        # General
        action_random = qmenu.addAction( "Random" )
        action_reset = qmenu.addAction( "Reset" )
        # Mapping
        action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
        # General
        if action == action_random: self.SIGNAL_RANDOM.emit()
        if action == action_reset:  self.SIGNAL_RESET.emit()
    # Paint
    def paintEvent( self, event ):
        # Variables
        m = self.plane_margin
        s = self.plane_split
        mm = m + m
        ss = s + s
        ms = m + s
        wm = self.ww - mm + ss
        hm = self.hh - mm + ss

        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Dots
        if self.plane_matrix != None:
            # Read
            tl = self.plane_matrix[0][0]
            tr = self.plane_matrix[0][-1]
            bl = self.plane_matrix[-1][0]
            br = self.plane_matrix[-1][-1]
            tl_hc, tl_px, tl_py, tl_pw, tl_ph, tl_pr, tl_pb = tl[0], tl[1], tl[2], tl[3], tl[4], tl[5], tl[6]
            tr_hc, tr_px, tr_py, tr_pw, tr_ph, tr_pr, tr_pb = tr[0], tr[1], tr[2], tr[3], tr[4], tr[5], tr[6]
            bl_hc, bl_px, bl_py, bl_pw, bl_ph, bl_pr, bl_pb = bl[0], bl[1], bl[2], bl[3], bl[4], bl[5], bl[6]
            br_hc, br_px, br_py, br_pw, br_ph, br_pr, br_pb = br[0], br[1], br[2], br[3], br[4], br[5], br[6]
            # Rectangles
            qrect_tl = QRect( 0,     0,     tl_pw+m, tl_ph+m )
            qrect_tr = QRect( tr_px, 0,     tr_pw+m, tr_ph+m )
            qrect_bl = QRect( 0,     bl_py, bl_pw+m, bl_ph+m )
            qrect_br = QRect( br_px, br_py, br_pw+m, br_ph+m )
            qrect_tl_bg = QRect( 0,       0,       tl_pw+ms, tl_ph+ms )
            qrect_tr_bg = QRect( tr_px-s, 0,       tr_pw+ms, tr_ph+ms )
            qrect_bl_bg = QRect( 0,       bl_py-s, bl_pw+ms, bl_ph+ms )
            qrect_br_bg = QRect( br_px-s, br_py-s, br_pw+ms, br_ph+ms )

            # Mask
            mask = QPainterPath()
            mask.addRect( 1, 1, self.ww-1, self.hh-1 )
            mask.addRect( m-s, m-s, br_px+br_pw-m+ss, br_py+br_ph-m+ss )
            painter.setClipPath( mask )

            # Background Squares
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( QColor( self.c_dark ) ) )
            painter.drawRect( qrect_tl_bg )
            painter.drawRect( qrect_tr_bg )
            painter.drawRect( qrect_bl_bg )
            painter.drawRect( qrect_br_bg )

            # Top Left
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( QColor( tl_hc ) ) )
            painter.drawRect( qrect_tl )
            # Top Right
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( QColor( tr_hc ) ) )
            painter.drawRect( qrect_tr )
            # Bottom Left
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( QColor( bl_hc ) ) )
            painter.drawRect( qrect_bl )
            # Bottom Right
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( QColor( br_hc ) ) )
            painter.drawRect( qrect_br )

            # Clean Mask
            painter.setClipping( False )

            # Interpolation
            painter.setPen( QtCore.Qt.NoPen )
            for y in range( 0, self.plane_dy ):
                for x in range( 0, self.plane_dx ):
                    # Read
                    item = self.plane_matrix[y][x]
                    hex_code, px, py, pw, ph = item[0], item[1], item[2], item[3], item[4]
                    # Draw
                    painter.setBrush( QBrush( QColor( hex_code ) ) )
                    painter.drawRect( px, py, pw, ph )

            # Regions
            painter.setPen( QtCore.Qt.NoPen )
            if self.state_tl == True:
                painter.setBrush( QBrush( self.c_dark, Qt.FDiagPattern ) )
                painter.drawRect( 0, 0, self.w2, self.h2 )
            if self.state_tr == True:
                painter.setBrush( QBrush( self.c_dark, Qt.BDiagPattern ) )
                painter.drawRect( self.w2, 0, self.w2, self.h2 )
            if self.state_bl == True:
                painter.setBrush( QBrush( self.c_dark, Qt.BDiagPattern ) )
                painter.drawRect( 0, self.h2, self.w2, self.h2 )
            if self.state_br == True:
                painter.setBrush( QBrush( self.c_dark, Qt.FDiagPattern ) )
                painter.drawRect( self.w2, self.h2, self.w2, self.h2 )

            # Cursor
            Cursor_Display( self, painter )

class Panel_Mask( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_LIVE_OFF = QtCore.pyqtSignal( str )

    # Init
    def __init__( self, parent ):
        super( Panel_Mask, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.side = 0
        # Event
        self.ex = -10
        self.ey = -10
        self.ox = -10
        self.oy = -10
        # State
        self.zoom = False
        self.qimage = None
        # Mask
        self.mask_path = list()
        self.mask_file = [
            "b1",
            "b2",
            "b3",
            "d1",
            "d2",
            "d3",
            "d4",
            "d5",
            "d6",
            "f1",
            "f2",
            "f3",
            ]
        self.mask_color = None
        self.mask_alpha = None
        self.mask_qpixmap = None
        # Color
        self.color_index = None
        self.c_lite = QColor( "#ffffff" )
        self.c_dark = QColor( "#000000" )
        self.c_white = QColor( "#ffffff" )
        self.c_gray = QColor( "#b0b0b0" )
        self.c_black = QColor( "#000000" )
        self.hex_code = QColor( "#000000" )
    # Set
    def Set_Size( self, ww, hh ):
        self.ww = int( ww )
        self.hh = int( hh )
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        self.ex = -10
        self.ey = -10
        self.resize( ww, hh )
    def Set_Theme( self, c_lite, c_dark ):
        self.c_lite = QColor( c_lite )#; self.c_lite.setAlphaF( 0.5 )
        self.c_dark = QColor( c_dark )#; self.c_dark.setAlphaF( 0.5 )
        self.update()
    # Update
    def Update_Path( self, mask_url ):
        self.mask_path = list()
        for name in self.mask_file:
            path = os.path.join( mask_url, f"{ name }.png" )
            reader = QImageReader( path )
            if reader.canRead() == True:    self.mask_path.append( path )
            else:                           self.mask_path.append( None )
        if None not in self.mask_path:  self.mask_qpixmap = self.Pixmap_Composite( self.mask_path, self.mask_color, self.mask_alpha )
        else:                           self.mask_qpixmap = None
        self.update()
    def Update_Gradient( self, mask_color, mask_alpha ):
        self.mask_color = mask_color
        self.mask_alpha = mask_alpha
        self.mask_qpixmap = self.Pixmap_Composite( self.mask_path, self.mask_color, self.mask_alpha )
        self.update()
    # Calculations
    def Pixmap_Composite( self, mask_path, mask_color, mask_alpha ):
        qpixmaps = list()
        for i in range( 0, len( mask_path ) ):
            # Color
            color = QColor( str( self.mask_color[i] ) )
            color.setAlphaF( self.mask_alpha[i] )
            # Images
            img_path = QImage( mask_path[i] )
            img_color = QImage( img_path.width(), img_path.height(), QImage.Format_RGBA8888 )
            img_color.fill( color )
            # Painter
            painter = QPainter()
            painter.begin( img_path )
            painter.setCompositionMode( QPainter.CompositionMode_SourceIn )
            painter.drawImage( 0, 0, img_color )
            painter.end()
            del painter
            # List
            qpixmaps.append( QPixmap.fromImage( img_path ) )
        return qpixmaps
    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Screenshot
        self.Cursor_Screenshot()
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        self.ox = ex
        self.oy = ey
        self.press = True
        self.SIGNAL_LIVE_OFF.emit( None )
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Color( ex, ey, self.qimage )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Color( ex, ey, self.qimage ); self.zoom = True
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Color( ex, ey, self.qimage )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Color( ex, ey, self.qimage ); self.zoom = True
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        em = event.modifiers()
        eb = event.buttons()
        ex = event.x()
        ey = event.y()
        # LMB
        if ( em == QtCore.Qt.NoModifier and eb == QtCore.Qt.LeftButton ):       self.Cursor_Color( ex, ey, self.qimage )
        if ( em == QtCore.Qt.ShiftModifier and eb == QtCore.Qt.LeftButton ):    self.Cursor_Color( ex, ey, self.qimage ); self.zoom = True
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.press = False
        self.zoom = False
        # Updates
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Operator
    def Cursor_Screenshot( self ):
        self.ex = -20
        self.ey = -20
        self.update()
        self.qimage = self.grab().toImage()
        # Preview_Screenshot( QPixmap().fromImage( self.qimage ) )
    def Cursor_Color( self, ex, ey, qimage ):
        self.ex = Limit_Range( ex, 0, self.ww )
        self.ey = Limit_Range( ey, 0, self.hh )
        pixel = qimage.pixelColor( self.ex, self.ey )
        hex_code = pixel.name()
        self.hex_code = QColor( hex_code )
        self.SIGNAL_VALUE.emit( hex_code )
    def Cursor_Move( self, ex, ey ):
        dx = ex - self.ox
        dy = ey - self.oy
        self.ex = self.w2 + dx
        self.ey = self.h2 + dy
    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )
        # Background
        painter.setPen( QtCore.Qt.NoPen )
        bw = QLinearGradient( int( 0 ), int( 0 ), int( 0 ), int( self.hh ) )
        bw.setColorAt( 0.000, self.c_lite )
        bw.setColorAt( 1.000, self.c_dark )
        painter.setBrush( QBrush( bw ) )
        painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( self.hh ) )
        # Draw Pixmaps
        if self.mask_qpixmap != None:
            for qpixmap in self.mask_qpixmap:
                if qpixmap.isNull() == False:
                    render = qpixmap.scaled( self.ww, self.hh, Qt.KeepAspectRatio, Qt.FastTransformation )
                    px = int( self.w2 - render.width() * 0.5 )
                    py = int( self.h2 - render.height() * 0.5 )
                    painter.drawPixmap( int( px ), int( py ), render )
        # Cursor
        Cursor_Display( self, painter )

#endregion
#region Channels & Pin

class Channel_Slider( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( float )
    SIGNAL_INCREMENT = QtCore.pyqtSignal( int )
    SIGNAL_MARK = QtCore.pyqtSignal( int )
    SIGNAL_RELEASE = QtCore.pyqtSignal()
    SIGNAL_TEXT = QtCore.pyqtSignal( str )

    # Init
    def __init__( self, parent ):
        super( Channel_Slider, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 1
        self.hh = 1
        # Event
        self.ox = 0
        self.ex = 0
        # Variables
        self.mode = "LINEAR" # "LINEAR" "CIRCULAR" "MIXER" "KELVIN" "POLE" "DEPTH"
        self.patch = False
        self.mo = 0
        self.mv = 4
        # Colors
        self.gradient = None
        self.alpha = None
        self.c_white = QColor( "#ffffff" )
        self.c_black = QColor( "#000000" )
        self.brush_black = QBrush( QColor( "#000000" ) )
        self.brush_white = QBrush( QColor( "#ffffff" ) )
    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = int( ww )
        self.hh = int( hh )
        self.resize( ww, hh )
    def Set_Theme( self, c_white, c_black ):
        self.c_white = QColor( c_white )
        self.c_black = QColor( c_black )
        self.update()
    def Set_Mode( self, mode ):
        self.mode = mode
        self.update()
    def Set_Value( self, ex ):
        self.ex = ex * self.ww
        self.update()
    def Set_Mark( self, mark ):
        self.mv = mark
        self.update()
    def Set_Gradient( self, gradient, alpha ):
        self.gradient = gradient
        self.alpha = alpha
        self.update()
    # Mouse Events
    def mousePressEvent( self, event ):
        # Event
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        # Start Event
        self.ox = ex
        self.mo = self.mv
        # LMB
        if   ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.NoModifier ):
            if   self.patch == False:   self.Emit_Value_Linear( ex )
            elif self.patch == True:    self.Snap_Mark( ex )
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):      self.Snap_Half()
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):    self.Snap_Mark( ex )
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.AltModifier ):        self.Mark_Shift( ex )
        # RMB
        elif ( eb == QtCore.Qt.RightButton and em == QtCore.Qt.NoModifier ):        self.Patch_Mode()
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        # LMB
        if   ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.NoModifier ):
            if   self.patch == False:   self.Emit_Value_Linear( ex )
            elif self.patch == True:    self.Snap_Mark( ex )
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):      self.Snap_Half()
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):    self.Snap_Mark( ex )
        # RMB
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.AltModifier ):        self.Mark_Shift( ex )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        # LMB
        if   ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.NoModifier ):
            if   self.patch == False:   self.Emit_Value_Linear( ex )
            elif self.patch == True:    self.Snap_Mark( ex )
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ShiftModifier ):      self.Snap_Half()
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.ControlModifier ):    self.Snap_Mark( ex )
        elif ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.AltModifier ):        self.Mark_Reset()
        self.update()
    def mouseReleaseEvent( self, event ):
        self.SIGNAL_TEXT.emit( "" )
        self.SIGNAL_RELEASE.emit()
        self.update()
    # Value
    def Emit_Value_Linear( self, ex ):
        # Variables
        self.ex = self.Mouse_Position( ex )
        percent, text = self.Request_Percent( self.ex, self.ww )
        if self.mode == "KELVIN":text = self.Request_Kelvin( percent )
        # Emission
        self.SIGNAL_VALUE.emit( percent )
        self.SIGNAL_TEXT.emit( text )
    # Snap
    def Snap_Half( self ):
        # Variables
        percent = 0.5
        self.ex = percent * self.ww
        text = "50 %"
        if self.mode == "KELVIN":text = self.Request_Kelvin( percent )
        # Signals
        self.SIGNAL_VALUE.emit( percent )
        self.SIGNAL_TEXT.emit( text )
    def Snap_Mark( self, ex ):
        # Mouse
        value = self.Mouse_Position( ex )
        # Calculations
        unit = self.ww / self.mv
        distances = list()
        for i in range( 0, self.mv+1 ):
            dist = Trig_2D_Points_Distance( value, 0, ( unit * i ), 0 )
            distances.append( dist )
        value_min = min( distances )
        index = distances.index( value_min )
        self.ex = unit * index
        percent, text = self.Request_Percent( self.ex, self.ww )
        if self.mode == "KELVIN":text = self.Request_Kelvin( percent )
        # Emission
        self.SIGNAL_VALUE.emit( percent )
        self.SIGNAL_TEXT.emit( text )
    # Mark
    def Mark_Shift( self, ex ):
        # Variables
        minimum = 2
        divisions = 100
        unit = 50
        # Calculations
        delta = ex - self.ox
        value = int( delta / unit )
        if self.mode in [ "KELVIN", "POLE" ]:value = int( 2 * value )
        self.mv = Limit_Range( self.mo + value, minimum, divisions )
        # Emission
        self.SIGNAL_MARK.emit( self.mv )
        self.SIGNAL_TEXT.emit( f"snap { self.mv }" )
    def Mark_Reset( self ):
        if self.mode in [ "CIRCULAR", "DEPTH" ]:    self.mv = 6
        else:                                       self.mv = 4
        self.SIGNAL_MARK.emit( self.mv )
    # Patch
    def Patch_Mode( self ):
        self.patch = not self.patch
        self.update()
    # Functions
    def Mouse_Position( self, ex ):
        if self.mode == "CIRCULAR": value = self.Loop_Hue( ex, 0, self.ww )
        else:                       value = Limit_Range( ex, 0, self.ww )
        return value
    def Loop_Hue( self, value, mini, maxi ):
        if value < mini:
            delta = value - maxi
            units = abs( int( delta / maxi ) )
            value = value + ( maxi * units )
        if value > maxi:
            units = abs( int( value / maxi ) )
            value -= maxi * units
        return value
    def Request_Percent( self, value, width ):
        percent = value / width
        text = f"{ round( percent * 100, 2 ) } %"
        return percent, text
    def Request_Kelvin( self, percent ): 
        kelvin = int( percent * kelvin_delta ) + kelvin_min
        text = f"{ kelvin } K"
        return text
    # Wheel Events
    def wheelEvent( self, event ):
        delta_y = event.angleDelta().y()
        if delta_y > 20:    num = +1
        if delta_y < -20:   num = -1
        self.SIGNAL_INCREMENT.emit( num )
    # Paint Style
    def paintEvent( self, event ):
        # Variables
        ww = self.ww
        hh = self.hh
        w1 = ww - 1
        w2 = ww - 2
        h1 = hh - 1

        # Painter
        painter = QPainter( self )

        # Background
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_black ) )
        painter.drawRect( 0, 0, self.ww, self.hh )

        # Mark
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.c_white ) )
        if self.mv <= 0 :
            painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( 1 ) )
        else:
            for i in range( 0, self.mv ):
                percent = self.ww * ( i / self.mv )
                painter.drawRect( int( percent ), int( 0 ), int( 1 ), int( 1 ) )
            painter.drawRect( int( self.ww * 1 - 1 ), int( 0 ), int( 1 ), int( 1 ) )

        # Draw Elements
        if self.gradient != None and self.patch == False:
            # Gradient
            painter.setPen( QtCore.Qt.NoPen )
            gradient = QLinearGradient( int( 0 ), int( 0 ), int( self.ww ), int( 0 ) )
            count = len( self.gradient ) - 1
            for i in range( 0, count + 1 ):
                index = i / count
                red   = int( self.gradient[i][0] * 255 )
                green = int( self.gradient[i][1] * 255 )
                blue  = int( self.gradient[i][2] * 255 )
                alpha = int( self.alpha * 255 )
                qcolor = QColor( red, green, blue, alpha )
                gradient.setColorAt( index, qcolor )
            painter.setBrush( QBrush( gradient ) )
            rectangle = QPolygon( [
                QPoint( int( 1 ),  int( 1 ) ),
                QPoint( int( w1 ), int( 1 ) ),
                QPoint( int( w1 ), int( h1 ) ),
                QPoint( int( 1 ),  int( h1 ) ),
                ] )
            painter.drawPolygon( rectangle )

            # Cursor
            value = int( self.ex )
            bl = value - 3
            br = value + 3
            wl = value - 1
            wr = value + 1
            top1 = 0
            bot1 = self.hh
            top2 = 1
            bot2 = self.hh - 1
            # Black Square
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( self.brush_black )
            black = QPolygon( [
                QPoint( int( bl ), int( top1 ) ),
                QPoint( int( bl ), int( bot1 ) ),
                QPoint( int( br ), int( bot1 ) ),
                QPoint( int( br ), int( top1 ) ),
                ] )
            painter.drawPolygon( black )
            # White Square
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( self.brush_white )
            square = QPolygon( [
                QPoint( int( wl ), int( top2 ) ),
                QPoint( int( wl ), int( bot2 ) ),
                QPoint( int( wr ), int( bot2 ) ),
                QPoint( int( wr ), int( top2 ) ),
                ] )
            painter.drawPolygon( square )
        elif self.gradient != None and self.patch == True:
            # Clip Mask
            slider = QRect( int( 1 ), int( 1 ), int( w2 ), int( h1 ) )
            painter.setClipRect( slider, Qt.ReplaceClip )
            # Gradient
            painter.setPen( QtCore.Qt.NoPen )
            count = len( self.gradient )
            for i in range( 0, count ):
                # Geometry
                pa = ( i - 1 ) / self.mv
                pb = i / self.mv
                pu = pb - pa
                unit = self.ww * pu
                half = self.ww * pu * 0.5
                px = self.ww * pb - half
                pw = self.ww * pu + 1
                # Color
                red   = int( self.gradient[i][0] * 255 )
                green = int( self.gradient[i][1] * 255 )
                blue  = int( self.gradient[i][2] * 255 )
                alpha = int( self.alpha * 255 )
                qcolor = QColor( red, green, blue, alpha )
                painter.setBrush( QBrush( qcolor ) )
                # Draw
                painter.drawRect( int( px ), int( 1 ), int( pw ), int( self.hh-2 ) )
            # Variables
            cx = self.ex - half
            cw = unit

            # Cursor
            r0 = QRegion( 1, 0, w2, self.hh )
            r1 = QRegion( int( cx + 3 ), int( 2 ), int( cw - 6 ), int( self.hh - 4 ) )
            region = r0.subtracted( r1 )
            painter.setClipRegion( region )
            # Colors
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( self.brush_black )
            painter.drawRect( int( cx ), int( 0 ), int( cw ), int( self.hh ) )
            painter.setBrush( self.brush_white )
            painter.drawRect( int( cx + 2 ), int( 1 ), int( cw - 4 ), int( self.hh - 2 ) )

class Pin_Color( QWidget ):
    SIGNAL_APPLY = QtCore.pyqtSignal( int )
    SIGNAL_SAVE  = QtCore.pyqtSignal( int )
    SIGNAL_CLEAN = QtCore.pyqtSignal( int )
    SIGNAL_ALPHA = QtCore.pyqtSignal( int, float )
    SIGNAL_TEXT  = QtCore.pyqtSignal( str )

    # Init
    def __init__( self, parent ):
        super( Pin_Color, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( 500, 500 )
    # Variables
    def Variables( self ):
        # Widget
        self.ww = 2
        self.hh = 2
        self.w2 = 1
        self.h2 = 1
        # Events
        self.ex = 0
        self.ey = 0
        # States
        self.state_active = False
        self.state_alpha = False
        # Pin
        self.operation = None
        self.menu = [ "APPLY", "SAVE", "CLEAN" ]
        self.index = None
        # Color
        self.qcolor = None  # None == no color
        self.alpha = 1
        self.c_white = QColor( "#ffffff" )
        self.c_gray = QColor( "#b0b0b0" )
        self.c_black = QColor( "#000000" )
        # Modifier Keys
        self.mod_1 = [ QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier, QtCore.Qt.AltModifier ]
        self.mod_3 = ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier )
    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        self.resize( ww, hh )
    def Set_Index( self, index ):
        self.index = index
    def Set_Menu( self, menu ):
        self.menu = menu
    def Set_Active( self, boolean ):
        self.state_active = boolean
        self.update()
    def Set_Alpha( self, boolean ):
        self.state_alpha = boolean
        self.update()
    # Update
    def Update_Color( self, qcolor, alpha ):
        self.qcolor = QColor( qcolor )
        self.alpha = alpha
        self.update()
    def Update_Clean( self ):
        self.qcolor = QColor( "#000000" )
        self.alpha = 0
        self.update()
    # Interaction
    def mousePressEvent( self, event ):
        # Variables
        eb = event.buttons()
        em = event.modifiers()
        ex = event.x()
        ey = event.y()
        # LMB Neutral
        if   ( eb == QtCore.Qt.LeftButton and em == QtCore.Qt.NoModifier ): self.Swipe_String( ex, ey );    self.operation = "swipe"
        elif ( eb == QtCore.Qt.LeftButton and em in self.mod_1 ):           self.Swipe_Transparency( ex );  self.operation = "alpha"
        elif ( eb == QtCore.Qt.LeftButton and em == self.mod_3 ):           self.SIGNAL_CLEAN.emit( self.index )
        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()
        # Operation
        if self.operation == "swipe":   self.Swipe_String( ex, ey )
        if self.operation == "alpha":   self.Swipe_Transparency( ex )
        # Update
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()
        # Operation
        if self.operation == "swipe":   self.Swipe_String( ex, ey )
        if self.operation == "alpha":   self.Swipe_Transparency( ex )
        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()
        # Operation
        if self.operation == "swipe":   self.Swipe_Operation( ex, ey )
        if self.operation == "alpha":   self.Swipe_Transparency( ex )
        # Update
        self.operation = None
        self.update()
    # Swipe Operations
    def Swipe_String( self, ex, ey ):
        if   ( 0 <= ex <= self.ww ) and ( ey <= 0 ):        self.SIGNAL_TEXT.emit( "APPLY" )
        elif ( 0 <= ex <= self.ww ) and ( ey >= self.hh ):  self.SIGNAL_TEXT.emit( "SAVE" )
        else:                                               self.SIGNAL_TEXT.emit( "" )
    def Swipe_Operation( self, ex, ey ):
        if   ( 0 <= ex <= self.ww ) and ( ey <= 0 ):        self.SIGNAL_APPLY.emit( self.index )
        elif ( 0 <= ex <= self.ww ) and ( ey >= self.hh ):  self.SIGNAL_SAVE.emit( self.index )
        self.SIGNAL_TEXT.emit( "" )
    def Swipe_Transparency( self, ex ):
        if self.state_alpha == True:
            value = Limit_Float( ex / self.ww )
            self.alpha = value
            self.SIGNAL_ALPHA.emit( self.index, self.alpha )
    # Context
    def contextMenuEvent( self, event ):
        # Menu
        qmenu = QMenu( self )
        # Actions
        if self.menu[0] != None:    qmenu_apply = qmenu.addAction( self.menu[0] )
        if self.menu[1] != None:    qmenu_save = qmenu.addAction( self.menu[1] )
        if self.menu[2] != None:    qmenu_clean = qmenu.addAction( self.menu[2] )
        action = qmenu.exec_( self.mapToGlobal( QPoint( 0, 18 ) ) )
        # Triggers
        if self.menu[0] != None and action == qmenu_apply:  self.SIGNAL_APPLY.emit( self.index )
        if self.menu[1] != None and action == qmenu_save:   self.SIGNAL_SAVE.emit(  self.index )
        if self.menu[2] != None and action == qmenu_clean:  self.SIGNAL_CLEAN.emit( self.index )
    # Paint Style
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        # Null Marker
        nn = 2
        painter.setBrush( QtCore.Qt.NoBrush )
        painter.setPen( QPen( self.c_gray, 2, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
        painter.drawLine( self.w2 - nn, self.h2, self.w2 + nn, self.h2 )
        # Color
        if self.qcolor != None:
            # Color
            if self.alpha != 1:
                self.qcolor.setAlphaF( self.alpha )
            painter.setBrush( QBrush( self.qcolor ) )
            painter.setPen( QtCore.Qt.NoPen )
            painter.drawRect( QRect( 1, 1, self.ww - 2, self.hh - 2 ) )
            # Alpha Bar
            if self.state_alpha == True:
                # Variable
                bar = 3
                line = 1
                width = Limit_Range( ( self.ww * self.alpha ) - 1 , 0, self.ww )
                # Slider
                painter.setBrush( QBrush( self.c_white ) )
                painter.setPen( QPen( self.c_black, line, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
                painter.drawRect( QRect( int( 0 ), int( self.hh - bar - line ), int( width ), int( bar ) ) )
        # Active
        if self.state_active == True:
            painter.setBrush( QtCore.Qt.NoBrush )
            painter.setPen( QtCore.Qt.NoPen )
            painter.setPen( QPen( self.c_black, 6, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
            painter.drawLine( self.w2 - 3, self.h2, self.w2 + 3, self.h2 )
            painter.setPen( QPen( self.c_white, 2, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
            painter.drawLine( self.w2 - 2, self.h2, self.w2 + 2, self.h2 )

#endregion
#region Footer

class SampleScreen_Button( QWidget ):
    SIGNAL_PRESS = QtCore.pyqtSignal()
    SIGNAL_MOVE = QtCore.pyqtSignal()
    SIGNAL_RELEASE = QtCore.pyqtSignal()

    # Initilization
    def __init__( self, parent ):
        super( SampleScreen_Button, self ).__init__( parent )
        pass

    # Mouse Events
    def mousePressEvent( self, event ):
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.SIGNAL_PRESS.emit()
            QApplication.setOverrideCursor( Qt.CrossCursor )
    def mouseMoveEvent( self, event ):
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.SIGNAL_MOVE.emit()
    def mouseReleaseEvent( self, event ):
        self.SIGNAL_RELEASE.emit()
        QApplication.restoreOverrideCursor()

#endregion

