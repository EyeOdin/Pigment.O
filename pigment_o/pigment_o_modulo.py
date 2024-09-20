# Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer.
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

# Python Modules
import os
import math
import time
import subprocess
import zipfile
# Krita Module
from krita import *
# PyQt5 Modules
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# Pigment.O Modules
from .pigment_o_constants import *
from .pigment_o_calculations import ( 
    Geometry,
    Convert,
 )

#endregion

#region Shared

# ZIP
def Read_Zip( self, location, tan_range, space, shape ):
    try:
        qpixmap_list = []
        if zipfile.is_zipfile( location ):
            archive = zipfile.ZipFile( location, "r" )
            for i in range( 0, tan_range+1 ):
                # Mode Sensitive
                name = f"{ space }_{ shape }_{ str( i ).zfill( 3 ) }.png"
                # Read File
                archive_open = archive.open( name )
                archive_read = archive_open.read()
                # Image
                image = QImage()
                image.loadFromData( archive_read )
                qpixmap = QPixmap().fromImage( image )
                qpixmap_list.append( qpixmap )
        return qpixmap_list
    except:
        try:QtCore.qDebug( f"Pigment.O | ERROR Zip failed" )
        except:pass

# Region
def Circles( self, painter ):
    # Circle 0 ( Everything )
    v0a = 0
    v0b = 1 - ( 2*v0a )
    circle_0 = QPainterPath()
    circle_0.addEllipse( int( self.px + self.side * v0a ), int( self.py + self.side * v0a ), int( self.side * v0b ), int( self.side * v0b ) )
    # Circle 1 ( Outter Most Region )
    v1a = 0.025
    v1b = 1 - ( 2*v1a )
    circle_1 = QPainterPath()
    circle_1.addEllipse( int( self.px + self.side * v1a ), int( self.py + self.side * v1a ), int( self.side * v1b ), int( self.side * v1b ) )
    # Circle 2 ( Inner Most Region )
    v2a = 0.068
    v2b = 1 - ( 2*v2a )
    circle_2 = QPainterPath()
    circle_2.addEllipse( int( self.px + self.side * v2a ), int( self.py + self.side * v2a ), int( self.side * v2b ), int( self.side * v2b ) )
    # Circle 3 ( Central Dot )
    v3a = 0.13
    v3b = 1 - ( 2*v3a )
    circle_3 = QPainterPath()
    circle_3.addEllipse( int( self.px + self.side * v3a ), int( self.py + self.side * v3a ), int( self.side * v3b ), int( self.side * v3b ) )

    # Return
    return circle_0, circle_1, circle_2, circle_3
# Cursor
def Cursor_Normal( self, painter, size ):
    # Variables
    w = 2
    # Mask
    mask = QPainterPath()
    mask.addEllipse( 
        int( self.ex - size ),
        int( self.ey - size ),
        int( size * 2 ),
        int( size * 2 ),
        )
    mask.addEllipse( 
        int( self.ex - size + w * 2 ),
        int( self.ey - size + w * 2 ),
        int( size * 2 - w * 4 ),
        int( size * 2 - w * 4 ),
        )
    painter.setClipPath( mask )
    # Black Circle
    painter.setPen( QtCore.Qt.NoPen )
    painter.setBrush( QBrush( QColor( "#000000" ) ) )
    painter.drawEllipse( 
        int( self.ex - size ),
        int( self.ey - size ),
        int( size * 2 ),
        int( size * 2 ),
        )
    # White Circle
    painter.setPen( QtCore.Qt.NoPen )
    painter.setBrush( QBrush( QColor( "#ffffff" ) ) )
    painter.drawEllipse( 
        int( self.ex - size + w ),
        int( self.ey - size + w ),
        int( size * 2 - w * 2 ),
        int( size * 2 - w * 2 ),
        )
def Cursor_Zoom( self, painter, zoom_size, margin_size ):
    # Border
    painter.setPen( QtCore.Qt.NoPen )
    painter.setBrush( QBrush( QColor( "#000000" ) ) )
    painter.drawEllipse( 
        int( self.ex - zoom_size ),
        int( self.ey - zoom_size ),
        int( zoom_size * 2 ),
        int( zoom_size * 2 ),
        )
    # Hex Color
    painter.setBrush( QBrush( self.hex_color ) )
    painter.drawEllipse( 
        int( self.ex - zoom_size + margin_size ),
        int( self.ey - zoom_size + margin_size ),
        int( zoom_size * 2 - margin_size * 2 ),
        int( zoom_size * 2 - margin_size * 2 ),
        )

#endregion
#region Header

class Color_Header( QWidget ):
    SIGNAL_SWAP = QtCore.pyqtSignal( int )
    SIGNAL_SHIFT = QtCore.pyqtSignal( bool )
    SIGNAL_RANDOM = QtCore.pyqtSignal( int )
    SIGNAL_COMP = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Color_Header, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    def Variables( self ):
        # Widget
        self.ww = 100
        self.hh = 40

        # Variables
        self.mode_ab = True
        self.progress_bar = 0

        # Other
        self.other_show = False
        self.ui_k = 80
        self.other_a = self.ui_k
        self.other_b = self.ww - self.ui_k

        # Colors HEX
        self.kac_1 = QColor( '#000000' )
        self.kac_2 = QColor( '#323232' )
        self.kbc_1 = QColor( '#ffffff' )
        self.kbc_2 = QColor( '#cbcbcb' )

        # Modules
        self.geometry = Geometry()

    # Relay
    def Set_Mode_AB( self, mode_ab ):
        self.mode_ab = mode_ab
        self.update()
    def Set_Size( self, ww, hh ):
        # widget
        self.ww = ww
        self.hh = hh
        # Limits
        if ww <= 200:
            self.other_a = ww * 0.4
            self.other_b = ww * 0.7
        else:
            self.other_a = self.ui_k
            self.other_b = ww - self.ui_k
        # Update
        self.resize( ww, hh )
    def Set_Color_A1( self, kac_1 ):
        self.kac_1 = QColor( kac_1 )
        self.update()
    def Set_Color_A2( self, kac_2 ):
        self.kac_2 = QColor( kac_2 )
        self.update()
    def Set_Color_B1( self, kbc_1 ):
        self.kbc_1 = QColor( kbc_1 )
        self.update()
    def Set_Color_B2( self, kbc_2 ):
        self.kbc_2 = QColor( kbc_2 )
        self.update()
    def Set_Progress( self, progress_bar ):
        self.progress_bar = progress_bar
        self.update()

    # Mouse Interaction
    def mousePressEvent( self, event ):
        self.update()
    def mouseMoveEvent( self, event ):
        self.update()
    def mouseReleaseEvent( self, event ):
        self.update()

    # Context Menu Event
    def contextMenuEvent( self, event ):
        # Variables
        if self.mode_ab == True:
            side = "BG"
        else:
            side = "FG"

        # Menu
        if event.modifiers() == QtCore.Qt.NoModifier:
            qmenu = QMenu( self )
            # Actions
            qmenu_swap = qmenu.addAction( "FG-BG Swap" )
            qmenu_active = qmenu.addAction( side + " Active" )
            qmenu_random = qmenu.addAction( "Random" )
            qmenu_complementary = qmenu.addAction( "Complementary" )
            # Map
            action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
            # Triggers
            if action == qmenu_swap:
                self.SIGNAL_SWAP.emit( 0 )
            if action == qmenu_active:
                self.mode_ab = not self.mode_ab
                self.SIGNAL_SHIFT.emit( self.mode_ab )
            if action == qmenu_random:
                self.SIGNAL_RANDOM.emit( 0 )
            if action == qmenu_complementary:
                self.SIGNAL_COMP.emit( 0 )

    # Interaction
    def enterEvent( self, event ):
        self.other_show = True
        self.update()
    def leaveEvent( self, event ):
        self.other_show = False
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

        # Mode FG
        if self.mode_ab == True:
            # FG Active
            painter.setBrush( QBrush( self.kac_1 ) )
            painter.drawRect( int( 0 ), int( 0 ), int( w2 ), int( self.hh ) )
            # FG Previous
            painter.setBrush( QBrush( self.kac_2 ) )
            painter.drawRect( int( w2 ), int( 0 ), int( w2 ), int( self.hh ) )

            # BG over FG
            painter.setBrush( QBrush( self.kbc_1 ) )
            if self.other_show == True:
                point = w1 - self.other_a
                painter.drawRect( int( point ), int( 0 ), int( self.other_a ), int( self.hh ) )
        # Mode BG
        if self.mode_ab == False:
            # BG Active
            painter.setBrush( QBrush( self.kbc_1 ) )
            painter.drawRect( int( 0 ), int( 0 ), int( w2 ), int( self.hh ) )
            # BG Previous
            painter.setBrush( QBrush( self.kbc_2 ) )
            painter.drawRect( int( w2 ), int( 0 ), int( w2 ), int( self.hh ) )

            # FG over BG
            painter.setBrush( QBrush( self.kac_1 ) )
            if self.other_show == True:
                painter.drawRect( int( 0 ), int( 0 ), int( self.other_a ), int( self.hh ) )

class Harmony_Swatch( QWidget ):
    SIGNAL_RULE = QtCore.pyqtSignal( str )
    SIGNAL_EDIT = QtCore.pyqtSignal( bool )
    SIGNAL_INDEX = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Harmony_Swatch, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        # Index
        self.harmony_rule = "Analogous" # "Monochromatic" "Complementary" "Analogous" "Triadic" "Tetradic"
        self.harmony_edit = False
        self.harmony_index = 0
        self.harmony_parts = 5
        self.harmony_color = [ "#000000", "#000000", "#000000", "#000000", "#000000" ]
        # Modules
        self.geometry = Geometry()
        # Colors
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )

    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.resize( ww, hh )
    def Set_Harmony_Rule( self, harmony_rule ):
        self.harmony_rule = harmony_rule
        self.update()
    def Set_Harmony_Parts( self, har_parts, har_color ):
        self.harmony_parts = har_parts
        self.harmony_color = har_color
        self.update()
    def Set_WheelSpace( self, wheel_space ):
        self.wheel_space = wheel_space
        self.update()

    # Update
    def Update_Harmony( self, harmony_rule, harmony_edit, harmony_index ):
        self.harmony_rule = harmony_rule
        self.harmony_edit = harmony_edit
        self.harmony_index = harmony_index
        self.update()
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
        self.ex = self.geometry.Limit_Range( event.x(), 0, self.ww )
        percentage = self.ex / self.ww
        self.harmony_index = self.geometry.Limit_Range( int( percentage * self.harmony_parts ), 0, self.harmony_parts - 1 ) + 1
        self.SIGNAL_INDEX.emit( self.harmony_index )
        self.update()

    # Context
    def contextMenuEvent( self, event ):
        # Menu
        qmenu = QMenu( self )

        # Actions Harmony Rule
        qmenu_rule = qmenu.addMenu( "Harmony Rule" )
        qmenu_rule_m = qmenu_rule.addAction( "Monochromatic" )
        qmenu_rule_c = qmenu_rule.addAction( "Complementary" )
        qmenu_rule_a = qmenu_rule.addAction( "Analogous" )
        qmenu_rule_tri = qmenu_rule.addAction( "Triadic" )
        qmenu_rule_tet = qmenu_rule.addAction( "Tetradic" )
        qmenu_rule_m.setCheckable( True )
        qmenu_rule_c.setCheckable( True )
        qmenu_rule_a.setCheckable( True )
        qmenu_rule_tri.setCheckable( True )
        qmenu_rule_tet.setCheckable( True )
        qmenu_rule_m.setChecked( self.harmony_rule == "Monochromatic" )
        qmenu_rule_c.setChecked( self.harmony_rule == "Complementary" )
        qmenu_rule_a.setChecked( self.harmony_rule == "Analogous" )
        qmenu_rule_tri.setChecked( self.harmony_rule == "Triadic" )
        qmenu_rule_tet.setChecked( self.harmony_rule == "Tetradic" )
        # Actions Edit
        qmenu_edit = qmenu.addAction( "Edit" )
        qmenu_edit.setCheckable( True )
        qmenu_edit.setChecked( self.harmony_edit )

        action = qmenu.exec_( self.mapToGlobal( event.pos() ) )

        # Triggers
        if action == qmenu_rule_m:
            self.harmony_rule = "Monochromatic"
            self.SIGNAL_RULE.emit( self.harmony_rule )
        if action == qmenu_rule_c:
            self.harmony_rule = "Complementary"
            self.SIGNAL_RULE.emit( self.harmony_rule )
        if action == qmenu_rule_a:
            self.harmony_rule = "Analogous"
            self.SIGNAL_RULE.emit( self.harmony_rule )
        if action == qmenu_rule_tri:
            self.harmony_rule = "Triadic"
            self.SIGNAL_RULE.emit( self.harmony_rule )
        if action == qmenu_rule_tet:
            self.harmony_rule = "Tetradic"
            self.SIGNAL_RULE.emit( self.harmony_rule )
        if action == qmenu_edit:
            self.harmony_edit = not self.harmony_edit
            self.SIGNAL_EDIT.emit( self.harmony_edit )

    # Paint
    def paintEvent( self, event ):
        # Start Qpainter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Correct Variable Range
        if self.harmony_index > self.harmony_parts:
            self.harmony_index = 0

        # Swatch
        points = []
        painter.setPen( QtCore.Qt.NoPen )
        width = int( self.ww / self.harmony_parts + 1 )
        for i in range( 0, self.harmony_parts ):
            # Variables
            px = ( self.ww / self.harmony_parts ) * i
            # Color
            painter.setBrush( QBrush( QColor( self.harmony_color[i] ) ) )
            painter.drawRect( int( px ), int( 0 ), int( width ), int( self.hh ) )
            # Stops
            points.append( px )
        points.append( self.ww )

        # Index Cursor
        if self.harmony_index != 0:
            height = 8
            px = points[ self.harmony_index - 1 ]
            py = self.hh - height
            pw = points[ self.harmony_index ]
            width = pw - px
            painter.setBrush( QBrush( self.color_2 ) )
            painter.drawRect( int( px ), int( py ), int( width ), int( height ) )
            painter.setBrush( QBrush( self.color_1 ) )
            painter.drawRect( int( px + 1 ), int( py + 1 ), int( width - 2 ), int( height - 2 ) )
class Harmony_Spread( QWidget ):
    SIGNAL_SPAN = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Harmony_Spread, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        # Range
        self.harmony_span = 0.2
        self.harmony_rule = "Analogous" # "Monochromatic" "Complementary" "Analogous" "Triadic" "Tetradic"
        self.no_span = ["Monochromatic", "Complementary"] # Have no span
        # Modules
        self.geometry = Geometry()
        # Colors
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
        self.color_alpha = QColor( 0, 0, 0, 50 )

    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.w2 = int( ww * 0.5 )
        self.resize( ww, hh )
    def Set_Rule( self, rule ):
        self.harmony_rule = rule
        self.update()

    # Update
    def Update_Span( self, harmony_span ):
        # range 0-1
        self.harmony_span = harmony_span
        self.update()

    # Mouse Interaction
    def mousePressEvent( self, event ):
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Range_Width( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Range_Pin( event )
    def mouseMoveEvent( self, event ):
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Range_Width( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Range_Pin( event )
    def mouseDoubleClickEvent( self, event ):
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Range_Width( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Range_Pin( event )
    def mouseReleaseEvent( self, event ):
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Range_Width( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Range_Pin( event )
        self.SIGNAL_RELEASE.emit( 0 )

    # Signals
    def Range_Width( self, event ):
        # Read
        event_x = event.x()
        # Consider Widget Size
        value = self.geometry.Limit_Range( event_x, 0, self.ww )
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
            self.harmony_span = 0
        else:
            self.harmony_span = delta / self.ww
        self.SIGNAL_SPAN.emit( self.harmony_span )
        self.update()
    def Range_Pin( self, event ):
        # Read
        event_x = event.x()
        # Consider Widget Size
        value = self.geometry.Limit_Range( event_x, 0, self.ww )
        # Pin
        stops = 72
        unit = self.ww / stops
        distances = []
        for i in range( 0, stops+1 ):
            dist = self.geometry.Trig_2D_Points_Distance( value, 0, ( unit * i ), 0 )
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
            self.harmony_span = 0
        else:
            self.harmony_span = delta / self.ww
        self.SIGNAL_SPAN.emit( self.harmony_span )
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Start Qpainter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Background Hover
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_alpha ) )
        painter.drawRect( 0, 0, self.ww, self.hh )

        # Variables
        if self.harmony_rule in self.no_span:
            px = int( self.w2 )
            width = 1
        else:
            px = int( self.w2 - ( self.harmony_span * self.ww * 0.5 ) )
            width = int( self.ww * self.harmony_span )
            if width <= 1:
                width = 1

        # Harmony Angle
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_2 ) )
        painter.drawRect( int( px ), int( 1 ), int( width ), int( 8 ) )
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_1 ) )
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
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        # Display
        self.hex_color = QColor( "#000000" )

    # Set
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.resize( ww, hh )

    # Updates
    def Update_Panel( self, color ):
        self.hex_color = QColor( color["hex6_d"] )
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Draw Pixmaps
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.hex_color ) )
        painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( self.hh ) )

class Panel_Square( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( dict )
    SIGNAL_TAN = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( dict )

    # Init
    def __init__( self, parent ):
        super( Panel_Square, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.origin_x = 0
        self.origin_y = 0
        self.origin_tan_axis = 0
        self.ex = 0
        self.ey = 0
        self.press = False
        self.pressure = 0
        self.input_pressure = 0.5

        # Display
        self.zoom = False
        self.tan_axis = 0 # 0-360 because of background index
        self.tan_range = None # 360 255
        self.qpixmap_list = []

        # Format
        self.directory = None # Path
        self.d_cm = None # "A" "RGB" "CMYK" "YUV" "XYZ" "LAB"
        self.shape = None # "3" "4" "R"
        self.chan = None # "hsv" "hsl" "hcy" "ard" / "yuv"
        # Wheel
        self.wheel_space = None # "HSV" "HSL" "HCY" "ARD"

        # Colors
        self.color = None
        self.hex_color = QColor( "#000000" )
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
        self.color_theme = QColor( "#31363b" )
        # Harmony Colors
        self.harmony_rule = None
        self.harmony_index = None
        self.harmony_list = None
        # Pinned Colors
        self.pin_index = None
        self.pin_list = None
        # Analyse Colors
        self.analyse = None

        # YUV primaries
        self.CR = [ 1, 0, 0 ]
        self.CY = [ 1, 1, 0 ]
        self.CG = [ 0, 1, 0 ]
        self.CC = [ 0, 1, 1 ]
        self.CB = [ 0, 0, 1 ]
        self.CM = [ 1, 0, 1 ]

        # Modules
        self.geometry = Geometry()
        self.convert = None
    def Init_Convert( self, convert ):
        self.convert = convert
        self.update()

    # Set
    def Set_ColorModel( self, d_cm ):
        self.d_cm = d_cm
        self.Set_ColorSpace_inDocument( self.directory, self.d_cm, self.wheel_space, self.shape )
        self.update()
    def Set_WheelSpace( self, wheel_space ):
        self.wheel_space = wheel_space
        self.Set_ColorSpace_inDocument( self.directory, self.d_cm, self.wheel_space, self.shape )
        self.update()
    def Set_Tangent_Range( self, tan_range ):
        self.tan_range = tan_range
        self.update()
    def Set_ColorSpace_inDocument( self, directory, d_cm, wheel_space, shape ):
        # Variables
        self.directory = directory
        self.d_cm = d_cm
        self.wheel_space = wheel_space
        self.shape = shape
        self.chan = self.wheel_space.lower()

        # Cursor
        if self.color != None:
            if self.shape == "3":
                cx = self.color["hsl_2"]
                cy = 1 - self.color["hsl_3"]
                inter = self.Triangle_Inter( cy, 1, 1 )
                self.ex = self.geometry.Limit_Range( cx * inter * self.ww, 0, self.ww )
                self.ey = self.geometry.Limit_Range( cy * self.hh, 0, self.hh )
            if self.shape == "4":
                self.ex = self.geometry.Limit_Range( self.color[f"{self.chan}_2"] * self.ww, 0, self.ww )
                self.ey = self.geometry.Limit_Range( self.color[f"{self.chan}_3"] * self.hh, 0, self.hh )
            if self.shape == "R":
                cx = self.color["hsl_2"]
                cy = 1 - self.color["hsl_3"]
                mini, maxi, delta = self.Diamond_Inter( cy, 1, 1 )
                value = mini + cx * delta
                self.ex = self.geometry.Limit_Range( value * self.ww, mini * self.ww, maxi * self.ww )
                self.ey = self.geometry.Limit_Range( cy * self.hh, 0, self.hh )
        # Primaries
        if self.wheel_space == "YUV":
            self.CR = self.convert.rgb_to_yuv( 1, 0, 0 )
            self.CY = self.convert.rgb_to_yuv( 1, 1, 0 )
            self.CG = self.convert.rgb_to_yuv( 0, 1, 0 )
            self.CC = self.convert.rgb_to_yuv( 0, 1, 1 )
            self.CB = self.convert.rgb_to_yuv( 0, 0, 1 )
            self.CM = self.convert.rgb_to_yuv( 1, 0, 1 )

        # Read Zip File
        location = os.path.join( self.directory, panel )
        location = os.path.join( location, f"{ self.d_cm }_{ self.wheel_space }_{ self.shape }.zip" )
        self.qpixmap_list = Read_Zip( self, location, self.tan_range, self.wheel_space, self.shape )

        # Update
        self.update()
    def Set_Size( self, ww, hh ):
        # Variables
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        # Mask ( slightly bigger than color display )
        if self.shape == "3":
            polygon = QPolygon( [
                QPoint( int( -1 ), int( -1 ) ),
                QPoint( int( self.ww + 1 ), int( self.hh * 0.5 ) ),
                QPoint( int( -1 ), int( self.hh + 1 ) ),
                ] )
            triangle = QRegion( polygon, Qt.OddEvenFill )
            self.setMask( triangle )
        if self.shape == "4":
            polygon = QPolygon( [
                QPoint( int( -1 ), int( -1 ) ),
                QPoint( int( self.ww + 1 ), int( -1 ) ),
                QPoint( int( self.ww + 1 ), int( self.hh + 1 ) ),
                QPoint( int( -1 ), int( self.hh + 1 ) ),
                ] )
            square = QRegion( polygon, Qt.OddEvenFill )
            self.setMask( square )
        if self.shape == "R":
            polygon = QPolygon( [
                QPoint( int( self.ww * 0.5 ), int( -1 ) ),
                QPoint( int( self.ww + 1 ), int( self.hh * 0.5 ) ),
                QPoint( int( self.ww * 0.5 ), int( self.hh + 1 ) ),
                QPoint( int( -1 ), int( self.hh * 0.5 ) ),
                ] )
            diamond = QRegion( polygon, Qt.OddEvenFill )
            self.setMask( diamond )
        # Update
        self.resize( ww, hh )
    def Set_Zoom( self, boolean ):
        self.press = boolean
        self.zoom = boolean
        self.update()

    # Updates
    def Update_Panel( self, color ):
        # Variables
        self.color = color
        # Display
        self.hex_color = QColor( color["hex6"] )
        if self.shape == "3":
            # Variables
            cx = color["hsl_2"]
            cy = 1 - color["hsl_3"]
            inter = self.Triangle_Inter( cy, 1, 1 )
            # Values
            self.tan_axis = color["hsl_1"]
            self.ex = self.geometry.Limit_Range( cx * inter * self.ww, 0, self.ww )
            self.ey = self.geometry.Limit_Range( cy * self.hh, 0, self.hh )
        if self.shape == "4":
            # Values
            self.tan_axis = color[f"{self.chan}_1"]
            self.ex = color[f"{self.chan}_2"] * self.ww
            self.ey = ( 1 - color[f"{self.chan}_3"] ) * self.hh
        if self.shape == "R":
            # Variables
            cx = color["hsl_2"]
            cy = 1 - color["hsl_3"]
            mini, maxi, delta = self.Diamond_Inter( cy, 1, 1 )
            value = mini + cx * delta
            # Values
            self.tan_axis = color["hsl_1"]
            self.ex = self.geometry.Limit_Range( value * self.ww, mini * self.ww, maxi * self.ww )
            self.ey = self.geometry.Limit_Range( cy * self.hh, 0, self.hh )

        # Update
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse ):
        self.analyse = analyse
        self.update()

    # Panel Modifiers
    def Triangle_Inter ( self, y, px, py ):
        if y <= 0*py:
            inter = 0
        elif ( y >= 0*py and y <= 0.5*py ):
            inter = self.geometry.Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0*px, 0*py, 1*px, 0.5*py )[0]
        elif y == 0.5*py:
            inter = 1
        elif ( y >= 0.5*py and y <= 1*py ):
            inter = self.geometry.Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0*px, 1*py, 1*px, 0.5*py )[0]
        elif y >= 1*py:
            inter = 0
        return inter
    def Diamond_Inter( self, y, px, py ):
        if y <= 0*py:
            mini = 0.5 * px
            maxi = 0.5 * py
            delta = 0
        elif ( y >= 0*py and y <= 0.5*py ):
            mini = self.geometry.Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 0*py, 0*px, 0.5*py )[0]
            maxi = self.geometry.Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 0*py, 1*px, 0.5*py )[0]
            delta = abs( maxi - mini )
        elif y == 0.5*py:
            mini = 0
            maxi = py
            delta = py
        elif ( y >= 0.5*py and y <= 1*py ):
            mini = self.geometry.Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 1*py, 0*px, 0.5*py )[0]
            maxi = self.geometry.Trig_2D_Points_Lines_Intersection( 0*px, y, 1*px, y, 0.5*px, 1*py, 1*px, 0.5*py )[0]
            delta = abs( maxi - mini )
        elif y >= 1*py:
            mini = 0.5 * px
            maxi = 0.5 * py
            delta = 0
        return mini, maxi, delta

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # Variables
        self.press = True
        self.origin_x = ex
        self.origin_y = ey
        self.origin_tan_axis = self.tan_axis

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )


        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Snap( ex, ey )

        self.update()
    def mouseMoveEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Position( ex, ey )

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Position( ex, ey )

        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.press = False
        self.zoom = False
        self.pressure = 0
        self.origin_tan_axis = 0
        self.pin_index = None
        # Updates
        self.SIGNAL_RELEASE.emit( 0 )
        self.update()

    # Mouse Event
    def Cursor_Position( self, ex, ey ):
        # Variables
        ww = self.ww
        wh = self.hh

        # Input
        if self.shape == "3":
            # Cursor
            inter = self.Triangle_Inter( ey, ww, wh )
            self.ex = self.geometry.Limit_Range( ex, 0, inter )
            self.ey = self.geometry.Limit_Range( ey, 0, self.hh )
            # Color
            if inter == 0:px = 0
            else:px = self.ex / inter
            py = ( wh - self.ey ) / wh
        if self.shape == "4":
            # Cursor
            self.ex = self.geometry.Limit_Range( ex, 0, ww )
            self.ey = self.geometry.Limit_Range( ey, 0, wh )
            # Color
            px =  self.ex / ww
            py = ( wh - self.ey ) / wh
        if self.shape == "R":
            # Cursor
            mini, maxi, delta = self.Diamond_Inter( ey, ww, wh )
            self.ex = self.geometry.Limit_Range( ex, mini, maxi )
            self.ey = self.geometry.Limit_Range( ey, 0, self.hh )
            # Color
            if delta == 0:px = 0
            else:px = ( self.ex - mini ) / delta
            py = ( wh - self.ey ) / wh

        # Variables
        if self.shape == "3":
            mode = "HSL"
            inter = self.Triangle_Inter( ey, self.ww, self.hh )
            if inter == 0:c2 = 0
            else:c2 = ex / inter
        if self.shape == "4":
            mode = self.wheel_space
            c2 = ex / self.ww
        if self.shape == "R":
            mode = "HSL"
            mini, maxi, delta = self.Diamond_Inter( ey, self.ww, self.hh )
            if delta == 0:c2 = 0
            else:c2 = ( ex - mini ) / delta
        c3 = ( self.hh - ey ) / self.hh

        # Limit
        c2 = self.geometry.Limit_Float( c2 )
        c3 = self.geometry.Limit_Float( c3 )

        # Signals
        dictionary = { "mode" : self.wheel_space, "c2" : c2, "c3" : c3, "pin_index" : self.pin_index }
        self.SIGNAL_VALUE.emit( dictionary )
        if self.pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( dictionary )
    def Cursor_Tangent( self, ex ):
        # Hue
        delta_hue = ( ( ex - self.origin_x ) / self.ww )
        angle = self.origin_tan_axis + delta_hue
        if self.wheel_space == "YUV":
            self.tan_axis = self.geometry.Limit_Float( angle )
        else:
            self.tan_axis = self.geometry.Limit_Looper( angle, 1 )
        # Update
        self.SIGNAL_TAN.emit( self.tan_axis )
    def Cursor_Snap( self, ex, ey ):
        if self.pin_list != None:
            distance = []
            for i in range( 0, len( self.pin_list ) ):
                if self.pin_list[i]["active"] == True:
                    px = self.pin_list[i][f"{self.chan}_2"] * self.ww
                    py = ( 1 - self.pin_list[i][f"{self.chan}_3"] ) * self.hh
                    dist = self.geometry.Trig_2D_Points_Distance( ex, ey, px, py )
                    distance.append( ( dist, i ) )
            if len( distance ) > 0:
                distance.sort()
                pin_index = distance[0][1]
                if pin_index < 20:
                    self.pin_index = pin_index
                    self.SIGNAL_PIN_INDEX.emit( self.pin_index )

    # Tablet Interaction
    def tabletEvent( self, event ):
        self.pressure = event.pressure()
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Draw Gradient
        if len( self.qpixmap_list ) > 0:
            try:
                # Draw Masks
                if self.shape == "3":
                    triangle = QPainterPath()
                    triangle.moveTo( int( 0 ), int( 1 ) )
                    triangle.lineTo( int( self.ww ), int( self.h2 ) )
                    triangle.lineTo( int( 0 ), int( self.hh ) )
                    painter.setClipPath( triangle )
                if self.shape == "R":
                    diamond = QPainterPath()
                    diamond.moveTo( int( self.w2 ), int( 0 ) )
                    diamond.lineTo( int( self.ww ), int( self.h2 ) )
                    diamond.lineTo( int( self.w2 ), int( self.hh ) )
                    diamond.lineTo( int( 0 ), int( self.h2 ) )
                    painter.setClipPath( diamond )

                # Draw Pixmaps
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( QtCore.Qt.NoBrush )
                index = int( self.tan_axis * self.tan_range )
                qpixmap = self.qpixmap_list[index]
                if qpixmap.isNull() == False:
                    render = qpixmap.scaled( self.ww, self.hh, Qt.IgnoreAspectRatio, Qt.FastTransformation )
                else:
                    render = qpixmap
                painter.drawPixmap( int( 0 ), int( 0 ), render )
            except:
                pass

        # YUV Line
        if self.wheel_space == "YUV":
            # Variables
            line_size = 2
            w1 = int( self.ww )
            h1 = int( self.hh )
            w2 = int( w1 * 0.5 )
            h2 = int( h1 * 0.5 )
            # Painter
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            # Draw Cross
            painter.drawLine( int( w2 ), int( 0 ), int( w2 ), int( h1 ) )
            painter.drawLine( int( 0 ), int( h2 ), int( w1 ), int( h2 ) )
            # Draw Primaries
            painter.drawLine( int( self.CR[1] * w1 ), int( ( 1-self.CR[2] ) * h1 ), int( self.CM[1] * w1 ), int( ( 1-self.CM[2] ) * h1 ) )
            painter.drawLine( int( self.CM[1] * w1 ), int( ( 1-self.CM[2] ) * h1 ), int( self.CB[1] * w1 ), int( ( 1-self.CB[2] ) * h1 ) )
            painter.drawLine( int( self.CB[1] * w1 ), int( ( 1-self.CB[2] ) * h1 ), int( self.CC[1] * w1 ), int( ( 1-self.CC[2] ) * h1 ) )
            painter.drawLine( int( self.CC[1] * w1 ), int( ( 1-self.CC[2] ) * h1 ), int( self.CG[1] * w1 ), int( ( 1-self.CG[2] ) * h1 ) )
            painter.drawLine( int( self.CG[1] * w1 ), int( ( 1-self.CG[2] ) * h1 ), int( self.CY[1] * w1 ), int( ( 1-self.CY[2] ) * h1 ) )
            painter.drawLine( int( self.CY[1] * w1 ), int( ( 1-self.CY[2] ) * h1 ), int( self.CR[1] * w1 ), int( ( 1-self.CR[2] ) * h1 ) )

        # Analyse Colors
        if self.analyse != None:
            # Variables
            dot = 5
            line_size = 2
            length = len( self.analyse )

            # Draw
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            for i in range( 0, length ):
                color = self.analyse[i]
                if int( self.tan_axis * 360 ) == int( color[f"{self.chan}_1"] * 360 ):
                    px = color[f"{self.chan}_2"] * self.ww
                    py = ( 1 - color[f"{self.chan}_3"] ) * self.hh
                    painter.drawEllipse( int( px - dot ), int( py - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Pinned Colors
        if ( self.color != None and self.pin_list != None ):
            # Variables
            pin_size = 5
            line_size = 2
            length = len( self.pin_list )

            # Draw
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            for i in range( 0, length ):
                if self.pin_list[i]["active"] == True:
                    if self.shape == "3":
                        cx = self.pin_list[i]["hsl_2"]
                        cy = ( 1 - self.pin_list[i]["hsl_3"] )
                        inter = self.Triangle_Inter( cy, 1, 1 )
                        painter.drawEllipse( 
                            int( ( cx * inter * self.ww ) - pin_size ),
                            int( ( cy * self.hh ) - pin_size ),
                            int( pin_size * 2 ),
                            int( pin_size * 2 )
                            )
                    if self.shape == "4":
                        painter.drawEllipse( 
                            int( ( self.pin_list[i][f"{self.chan}_2"] * self.ww ) - pin_size ),
                            int( ( ( 1-self.pin_list[i][f"{self.chan}_3"] ) * self.hh ) - pin_size ),
                            int( pin_size * 2 ),
                            int( pin_size * 2 )
                            )
                    if self.shape == "R":
                        cx = self.pin_list[i]["hsl_2"]
                        cy = ( 1 - self.pin_list[i]["hsl_3"] )
                        mini, maxi, delta = self.Diamond_Inter( cy, 1, 1 )
                        value = mini + cx * delta
                        painter.drawEllipse( 
                            int( ( value * self.ww ) - pin_size ),
                            int( ( cy * self.hh ) - pin_size ),
                            int( pin_size * 2 ),
                            int( pin_size * 2 )
                            )

        # Harmony Colors
        if ( self.color != None and self.harmony_list != None ):
            # Variables
            line_size = 2
            radius = 5

            # Parsing
            points = []
            for i in range( 0, len( self.harmony_list ) ):
                if self.shape == "3":
                    cx = self.harmony_list[i]["hsl_2"]
                    cy = ( 1 - self.harmony_list[i]["hsl_3"] )
                    inter = self.Triangle_Inter( cy, 1, 1 )
                    har_x = cx * inter * self.ww
                    har_y = cy * self.hh
                if self.shape == "4":
                    chan = self.wheel_space.lower()
                    har_x = self.harmony_list[i][f"{chan}_2"] * self.ww
                    har_y = ( 1 - self.harmony_list[i][f"{chan}_3"] ) * self.hh
                if self.shape == "R":
                    cx = self.harmony_list[i]["hsl_2"]
                    cy = ( 1 - self.harmony_list[i]["hsl_3"] )
                    mini, maxi, delta = self.Diamond_Inter( cy, 1, 1 )
                    value = mini + cx * delta
                    har_x = value * self.ww
                    har_y = cy * self.hh
                points.append( ( har_x, har_y ) )
            length = len( points )

            # Draw Line
            painter.setPen( QPen( self.color_1, line_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( points[i-1][0] ), int( points[i-1][1] ), int( points[i][0] ), int( points[i][1] ) )
            if self.harmony_rule in [ "Triadic", "Tetradic" ]:
                painter.drawLine( int( points[0][0] ), int( points[0][1] ), int( points[length-1][0] ), int( points[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( points[i][0] - radius ), int( points[i][1] - radius ), int( radius * 2 ), int( radius * 2 ) )

        # Cursor
        size = 10
        zoom_size = 100
        margin_size = 10
        if ( self.press == True and self.zoom == True ):
            size = zoom_size
            Cursor_Zoom( self, painter, size, margin_size )
        elif( self.pressure > self.input_pressure ):
            size = zoom_size * self.pressure
            Cursor_Zoom( self, painter, size, margin_size )
        else:
            Cursor_Normal( self, painter, size )

class Panel_HueCircle( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )
    SIGNAL_SUBPANEL = QtCore.pyqtSignal( str )

    # Init
    def __init__( self, parent ):
        super( Panel_HueCircle, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.press = False
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.px = 0
        self.py = 0
        self.side = 0
        # Variables
        self.wheel_mode = "DIGITAL" # "DIGITAL" "ANALOG"
        self.wheel_space = "HSV" # "HSV" "HSL" "HCY" "ARD"
        self.huecircle_shape = "None" # "None" "Triangle" "Square" "Diamond"

        # Color
        self.color = None
        self.hex_color = QColor( "#000000" )
        self.colors = [
            [1, 0, 0],   # Index = 0 > red
            [1, 0.5, 0], # Index = 1 > orange
            [1, 1, 0],   # Index = 2 > yellow
            [0, 1, 0],   # Index = 3 > green
            [0, 1, 1],   # Index = 4 > cyan
            [0, 0, 1],   # Index = 5 > blue
            [1, 0, 1],   # Index = 6 > magenta
            ]
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
        self.color_theme = QColor( "#31363b" )

        # Hue
        self.digital = [ 0, 60, 120, 180, 240, 300, 360 ]
        self.analog = [ 0, 122, 165, 218, 275, 330, 360 ]

        # Harmony Colors
        self.harmony_rule = None # "Monochromatic" "Complementary" "Analogous" "Triadic" "Tetradic"
        self.harmony_index = None
        self.harmony_list = None
        self.harmony_span = 0

        # Modules
        self.geometry = Geometry()
        self.convert = None
    def Init_Convert( self, convert ):
        self.convert = convert
        self.update()

    # Set
    def Set_WheelMode( self, wheel_mode ):
        self.wheel_mode = wheel_mode
        self.update()
    def Set_WheelSpace( self, wheel_space ):
        self.wheel_space = wheel_space
        self.update()
    def Set_Shape( self, huecircle_shape ):
        self.huecircle_shape = huecircle_shape
        self.update()
    def Set_Size( self, ww, hh, subpanel_shape ):
        # Widget
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        # Frame
        if self.ww >= self.hh:
            self.side = self.hh
            self.px = self.w2 - ( self.side * 0.5 )
            self.py = 0
        else:
            self.side = self.ww
            self.px = 0
            self.py = self.h2 - ( self.side * 0.5 )

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
        if subpanel_shape == "None":
            mask_region = widget_square
        if subpanel_shape == "Triangle":
            x = 0.28
            y = 0.13
            k = 0.07
            t = 1 - k - x
            polygon = QPolygon( [
                # Top
                QPoint( int( self.px + x * self.side - pad ),       int( self.py + y * self.side ) ),
                QPoint( int( self.px + x * self.side ),             int( self.py + y * self.side - pad ) ),
                # Right
                QPoint( int( self.px + self.side - k * self.side ), int( self.h2 - pad ) ),
                QPoint( int( self.px + self.side - k * self.side ), int( self.h2 + pad ) ),
                # Bot
                QPoint( int( self.px + x * self.side ),             int( self.py + self.side - y * self.side + pad ) ),
                QPoint( int( self.px + x * self.side - pad ),       int( self.py + self.side - y * self.side ) ),
                ] )
            triangle = QRegion( polygon, Qt.OddEvenFill )
            mask_region = widget_square.subtracted( triangle )
        if subpanel_shape == "Square":
            k = 0.2
            square = QRegion(
                int( self.px + self.side * k - pad ),
                int( self.py + self.side * k - pad ),
                int( self.side - ( 2 * k * self.side ) + ( 2 * pad ) ),
                int( self.side - ( 2 * k * self.side ) + ( 2 * pad ) ),
                QRegion.Rectangle
                )
            mask_region = widget_square.subtracted( square )
        if subpanel_shape == "Diamond":
            k = 0.07
            kk = ( 1 - k * 2 ) / 2
            polygon = QPolygon( [
                    QPoint( int( self.w2 ),                         int( self.h2 - self.side * kk - pad ) ),
                    QPoint( int( self.w2 + self.side * kk + pad ),  int( self.h2 ) ),
                    QPoint( int( self.w2 ),                         int( self.h2 + self.side * kk + pad ) ),
                    QPoint( int( self.w2 - self.side * kk - pad ),  int( self.h2 ) ),
                    ] )
            diamond = QRegion( polygon, Qt.OddEvenFill )
            mask_region = widget_square.subtracted( diamond )
        # Mask
        self.setMask( mask_region )

        # Update
        self.resize( ww, hh )
    def Set_Theme( self, color_1, color_2, color_theme ):
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_theme = color_theme
        self.update()

    # Update
    def Update_Panel( self, color ):
        self.color = color
        self.update()
    def Update_Colors( self, colors ):
        self.colors = colors
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Span( self, harmony_span ):
        self.harmony_span = harmony_span
        self.update()

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Variables
        self.press = True

        # LMB Neutral
        if event.buttons() == QtCore.Qt.LeftButton:
            self.Cursor_Angle( event )
        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.press = False
            self.Context_Menu( event )
        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # LMB Neutral
        if event.buttons() == QtCore.Qt.LeftButton:
            self.Cursor_Angle( event )
        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # Update
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # LMB Neutral
        if event.buttons() == QtCore.Qt.LeftButton:
            self.Cursor_Angle( event )
        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.press = False
        # Update
        self.SIGNAL_RELEASE.emit( 0 )
        self.update()

    def Cursor_Angle( self, event ):
        # Variables
        ex = event.x()
        ey = self.hh - event.y()
        # Angle Measure
        if self.wheel_mode == "DIGITAL":
            angle = self.geometry.Trig_2D_Points_Lines_Angle( ex, ey, self.w2, self.h2, 0, self.h2 )
            if event.modifiers() == QtCore.Qt.ShiftModifier:
                angle = int( angle )
            if event.modifiers() == QtCore.Qt.ControlModifier:
                angle = self.geometry.Limit_Angle( angle, 2.5 )
            value = angle / 360
        if self.wheel_mode == "ANALOG":
            px = self.w2 - ( self.side * 0.5 )
            py = self.h2 - ( self.side * 0.314 ) # Inverted for the formula
            angle = self.geometry.Trig_2D_Points_Lines_Angle( ex, ey, self.w2, self.h2, px, py )
            if event.modifiers() == QtCore.Qt.ShiftModifier:
                angle = int( angle )
            if event.modifiers() == QtCore.Qt.ControlModifier:
                angle = self.geometry.Limit_Angle( angle, 2.5 )
            value = self.convert.huea_to_hued( self.geometry.Limit_Looper( angle, 360 ) / 360 )
        # Emit Values
        self.SIGNAL_VALUE.emit( value )

    # Context
    def Context_Menu( self, event ):
        if self.press == False:
            # Menu
            qmenu = QMenu( self )

            # Action 
            qmenu_sn = qmenu.addAction( "None" )
            qmenu_st = qmenu.addAction( "Triangle" )
            qmenu_ss = qmenu.addAction( "Square" )
            qmenu_sd = qmenu.addAction( "Diamond" )
            qmenu_sn.setCheckable( True )
            qmenu_st.setCheckable( True )
            qmenu_ss.setCheckable( True )
            qmenu_sd.setCheckable( True )
            qmenu_sn.setChecked( self.huecircle_shape == "None" )
            qmenu_st.setChecked( self.huecircle_shape == "Triangle" )
            qmenu_ss.setChecked( self.huecircle_shape == "Square" )
            qmenu_sd.setChecked( self.huecircle_shape == "Diamond" )

            action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
            # Triggers
            if action == qmenu_sn:
                self.huecircle_shape = "None"
                self.SIGNAL_SUBPANEL.emit( self.huecircle_shape )
            if action == qmenu_st:
                self.huecircle_shape = "Triangle"
                self.SIGNAL_SUBPANEL.emit( self.huecircle_shape )
            if action == qmenu_ss:
                self.huecircle_shape = "Square"
                self.SIGNAL_SUBPANEL.emit( self.huecircle_shape )
            if action == qmenu_sd:
                self.huecircle_shape = "Diamond"
                self.SIGNAL_SUBPANEL.emit( self.huecircle_shape )

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        line_width = 4
        circle_0, circle_1, circle_2, circle_3 = Circles( self, painter )

        # Hue
        if self.wheel_mode == "DIGITAL":
            index = "hue_d"
        if self.wheel_mode == "ANALOG":
            index = "hue_a"
        # Circle Points
        radius = 0.5
        circle_points = []
        if self.harmony_rule != None:
            for i in range( 0, len( self.harmony_list ) ):
                if self.wheel_mode == "DIGITAL":
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, self.harmony_list[i][index] * 360 )
                if self.wheel_mode == "ANALOG":
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, ( self.harmony_list[i][index] * 360 ) - hue_a )
                circle_points.append( [ px, py ] )
        else:
            if self.wheel_mode == "DIGITAL":
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, self.color[index] * 360 )
            if self.wheel_mode == "ANALOG":
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, ( self.color[index] * 360 ) - hue_a )
            circle_points.append( [ px, py ] )
        length = len( circle_points )
        # Divisions
        div = []
        margin = 0.01
        if self.wheel_mode == "DIGITAL":
            for i in range( 0, len( self.digital ) ):
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, self.digital[i] )
                div.append( [ px, py ] )
        if self.wheel_mode == "ANALOG":
            for i in range( 0, len( self.analog ) ):
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius - margin, self.analog[i] - hue_a )
                div.append( [ px, py ] )

        # Dark Border
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_theme ) )
        circle_02 = circle_0.subtracted( circle_2 )
        painter.drawPath( circle_02 )
        # Dark Lines Color Reference
        painter.setPen( QPen( self.color_theme, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        s1 = self.side
        s2 = self.side * 0.5
        if self.wheel_mode == "DIGITAL":
            for i in range( 0, len( self.digital ) ):
                painter.drawLine( int( div[i][0] ), int( div[i][1] ), int( self.w2 ), int( self.h2 ) )
        if self.wheel_mode == "ANALOG":
            for i in range( 0, len( self.analog ) ):
                painter.drawLine( int( div[i][0] ), int( div[i][1] ), int( self.w2 ), int( self.h2 ) )

        # Light Line
        painter.setPen( QPen( self.color_1, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        circle_13 = circle_1.subtracted( circle_3 )
        if length > 0:
            line_gray = QPainterPath()
            for i in range( 0, length ):
                # Variables
                px = circle_points[i][0]
                py = circle_points[i][1]
                # Draw
                line_gray.moveTo( int( self.w2 ), int( self.h2 ) )
                line_gray.lineTo( int( px ), int( py ) )
            painter.setClipPath( circle_13 )
            painter.drawPath( line_gray )
        # Hue Gradient
        painter.setPen( QtCore.Qt.NoPen )
        d = 255
        if self.wheel_mode == "DIGITAL":
            hue = QConicalGradient( QPoint( int( self.w2 ), int( self.h2 ) ), 180 )
            hue.setColorAt( 0.000, QColor( int( self.colors[0][0] * d ), int( self.colors[0][1] * d ), int( self.colors[0][2] * d ) ) ) # RED
            hue.setColorAt( 0.166, QColor( int( self.colors[6][0] * d ), int( self.colors[6][1] * d ), int( self.colors[6][2] * d ) ) ) # MAGENTA
            hue.setColorAt( 0.333, QColor( int( self.colors[5][0] * d ), int( self.colors[5][1] * d ), int( self.colors[5][2] * d ) ) ) # BLUE
            hue.setColorAt( 0.500, QColor( int( self.colors[4][0] * d ), int( self.colors[4][1] * d ), int( self.colors[4][2] * d ) ) ) # CYAN
            hue.setColorAt( 0.666, QColor( int( self.colors[3][0] * d ), int( self.colors[3][1] * d ), int( self.colors[3][2] * d ) ) ) # GREEN
            hue.setColorAt( 0.833, QColor( int( self.colors[2][0] * d ), int( self.colors[2][1] * d ), int( self.colors[2][2] * d ) ) ) # YELLOW
            hue.setColorAt( 1.000, QColor( int( self.colors[0][0] * d ), int( self.colors[0][1] * d ), int( self.colors[0][2] * d ) ) ) # RED
        if self.wheel_mode == "ANALOG":
            hue = QConicalGradient( QPoint( int( self.w2 ), int( self.h2 ) ), 210 )
            hue.setColorAt( 0.000, QColor( int( self.colors[0][0] * d ), int( self.colors[0][1] * d ), int( self.colors[0][2] * d ) ) ) # RED
            hue.setColorAt( 0.083, QColor( int( self.colors[6][0] * d ), int( self.colors[6][1] * d ), int( self.colors[6][2] * d ) ) ) # MAGENTA
            hue.setColorAt( 0.236, QColor( int( self.colors[5][0] * d ), int( self.colors[5][1] * d ), int( self.colors[5][2] * d ) ) ) # BLUE
            hue.setColorAt( 0.394, QColor( int( self.colors[4][0] * d ), int( self.colors[4][1] * d ), int( self.colors[4][2] * d ) ) ) # CYAN
            hue.setColorAt( 0.541, QColor( int( self.colors[3][0] * d ), int( self.colors[3][1] * d ), int( self.colors[3][2] * d ) ) ) # GREEN
            hue.setColorAt( 0.661, QColor( int( self.colors[2][0] * d ), int( self.colors[2][1] * d ), int( self.colors[2][2] * d ) ) ) # YELLOW
            hue.setColorAt( 0.833, QColor( int( self.colors[1][0] * d ), int( self.colors[1][1] * d ), int( self.colors[1][2] * d ) ) ) # ORANGE
            hue.setColorAt( 1.000, QColor( int( self.colors[0][0] * d ), int( self.colors[0][1] * d ), int( self.colors[0][2] * d ) ) ) # RED
        painter.setBrush( QBrush( hue ) )
        circle_01 = circle_0.subtracted( circle_1 )
        painter.setClipPath( circle_01 )
        painter.drawRect( int( self.px ), int( self.py ), int( self.side ), int( self.side ) )
        # Dark Line over Hue
        painter.setPen( QPen( self.color_theme, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        circle_01 = circle_0.subtracted( circle_1 )
        painter.setClipPath( circle_01 )
        for i in range( 0, length ):
            painter.drawLine( int( circle_points[i][0] ), int( circle_points[i][1] ), int( self.w2 ), int( self.h2 ) )

class Panel_Gamut( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( dict )
    SIGNAL_TAN = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )
    SIGNAL_MASK = QtCore.pyqtSignal( str )
    SIGNAL_PROFILE = QtCore.pyqtSignal( list )
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( dict )

    # Init
    def __init__( self, parent ):
        super( Panel_Gamut, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.press = False
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.ex = 0
        self.ey = 0
        self.origin_x = 0
        self.origin_y = 0
        self.origin_tan_axis = 0
        self.origin_angle = 0
        self.origin_dist = 0
        self.previous_dist = 0
        self.px = 0
        self.py = 0
        self.side = 0
        self.pressure = 0
        self.input_pressure = 0.5
        self.region = None # "RING" "DISK"

        # Disk
        self.disk_var = 0.068
        self.disk_radius = 0.5 * ( 1 - ( 2 * self.disk_var ) ) # 0.432
        self.disk_x = 0
        self.disk_y = 0
        self.disk_side = 0

        # Display
        self.zoom = False
        self.tan_axis = 0 # 0-255 because of background index
        self.tan_range = 255

        # Format
        self.directory = None # Path
        self.shape = None # "CD" "CA"
        self.d_cm = None # "A" "RGB" "CMYK" "YUV" "XYZ" "LAB"
        self.chan = None # "hsv" "hsl" "hcy" "ard"
        # Wheel
        self.wheel_mode = "DIGITAL" # "DIGITAL" "ANALOG"
        self.wheel_space = "HSV" # "HSV" "HSL" "HCY" "ARD"

        # Color
        self.color = None
        self.hex_color = QColor( "#000000" )
        self.white = self.color_1 = QColor( "#e5e5e5" )
        self.black = self.color_2 = QColor( "#191919" )
        self.color_theme = QColor( "#31363b" )
        # Harmony Colors
        self.harmony_index = None
        self.harmony_list = None
        # Pinned Colors
        self.pin_index = None
        self.pin_list = None
        # Analyse Colors
        self.analyse = None

        # Hue
        self.digital = [ 0, 60, 120, 180, 240, 300, 360 ]
        self.analog = [ 0, 122, 165, 218, 275, 330, 360 ]
        # Harmony Colors
        self.harmony_rule = None # "Monochromatic" "Complementary" "Analogous" "Triadic" "Tetradic"
        self.harmony_index = None
        self.harmony_list = None
        self.harmony_span = 0

        # Gamut
        self.gamut_mask = "None" # "None" "Triangle" "Square" "Circle" "2 Circle" "3 Pie" "Reset"
        self.gamut_index = None
        self.gamut_rotation = None
        # Gamut Neutral
        self.neutral_1tri = [ ( 0.5, 0.5 ), ( 0.5, 0.1 ), ( 0.84641, 0.7 ), ( 0.15359, 0.7 ) ] # Centroid + Polygon
        self.neutral_1squ = [ ( 0.5, 0.5 ), ( 0.5, 0.1 ), ( 0.9, 0.5 ), ( 0.5, 0.9 ), ( 0.1, 0.5 ) ] # Centroid + Polygon
        self.neutral_1cir = [ ( 0.5, 0.5 ), ( 0.5, 0.1 ), ( 0.9, 0.5 ), ( 0.5, 0.9 ), ( 0.1, 0.5 ) ] # Centroid + Polygon
        self.neutral_2cir = [ ( 0.5, 0.275 ), ( 0.5, 0.1 ), ( 0.675, 0.275 ), ( 0.5, 0.45 ), ( 0.325, 0.275 ), # Circle 1  ( Centroid + Polygon )
                            ( 0.5, 0.725 ), ( 0.5, 0.55 ), ( 0.675, 0.725 ), ( 0.5, 0.9 ), ( 0.325, 0.725 ) ]  # Circle 2  ( Centroid + Polygon )
        self.neutral_3pie = [ ( 0.5, 0.5 ), ( 0.5, 0.15359 ), ( 0.8, 0.32679 ), ( 0.8, 0.67321 ), ( 0.5, 0.84641 ), ( 0.2, 0.67321 ), ( 0.2, 0.32679 ) ] # Centroid + Polygon
        # Gamut Lists
        self.gamut_1tri = self.neutral_1tri.copy()
        self.gamut_1squ = self.neutral_1squ.copy()
        self.gamut_1cir = self.neutral_1cir.copy()
        self.gamut_2cir = self.neutral_2cir.copy()
        self.gamut_3pie = self.neutral_3pie.copy()

        # Modules
        self.geometry = Geometry()
        self.convert = None
    def Init_Convert( self, convert ):
        self.convert = convert
        self.update()

    # Set
    def Set_ColorModel( self, d_cm ):
        self.d_cm = d_cm
        self.Set_ColorSpace_inDocument( self.directory, self.d_cm, self.wheel_space, self.shape )
        self.update()
    def Set_WheelMode( self, wheel_mode ):
        self.wheel_mode = wheel_mode
        if self.wheel_mode == "DIGITAL":
            self.shape = "D"
        if self.wheel_mode == "ANALOG":
            self.shape = "A"
        self.Set_ColorSpace_inDocument( self.directory, self.d_cm, self.wheel_space, self.shape )
        self.update()
    def Set_WheelSpace( self, wheel_space ):
        self.wheel_space = wheel_space
        self.Set_ColorSpace_inDocument( self.directory, self.d_cm, self.wheel_space, self.shape )
        self.update()
    def Set_ColorSpace_inDocument( self, directory, d_cm, wheel_space, shape ):
        # Variables
        self.directory = directory
        self.d_cm = d_cm
        self.wheel_space = wheel_space
        self.shape = shape
        self.chan = self.wheel_space.lower()

        # Cursor
        if self.color != None:
            self.ex, self.ey = self.Update_Cursor( self.color )

        # Read Zip File
        location = os.path.join( self.directory, panel )
        location = os.path.join( location, f"{ self.d_cm }_{ self.wheel_space }_{ self.shape }.zip" )
        self.qpixmap_list = Read_Zip( self, location, self.tan_range, self.wheel_space, self.shape )

        # Update
        self.update()
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
    def Set_Size( self, ww, hh ):
        # Widget
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        # Frame
        if self.ww >= self.hh:
            self.side = self.hh
            self.px = self.w2 - ( self.side * 0.5 )
            self.py = 0
        else:
            self.side = self.ww
            self.px = 0
            self.py = self.h2 - ( self.side * 0.5 )
        # Disk Coordinates
        self.disk_x = self.px + self.disk_var * self.side
        self.disk_y = self.py + self.disk_var * self.side
        self.disk_side = ( 1 - 2 * self.disk_var ) * self.side

        # Update
        self.resize( ww, hh )
    def Set_Theme( self, color_1, color_2, color_theme ):
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_theme = color_theme
        self.update()

    # Update
    def Update_Panel( self, color ):
        # Variables
        self.color = color
        self.hex_color = QColor( color["hex6"] )

        # Location of Cursor
        self.ex, self.ey = self.Update_Cursor( self.color )
        self.previous_dist = self.geometry.Trig_2D_Points_Distance( self.ex, self.ey, self.w2, self.h2 )

        # Update
        self.update()
    def Update_Cursor( self, color ):
        # Angle
        if self.wheel_mode == "DIGITAL":
            angle = color["hue_d"] * 360
        if self.wheel_mode == "ANALOG":
            angle = color["hue_a"] * 360 - hue_a
        # Radius
        radius = color[f"{ self.chan }_2"]
        self.tan_axis = color[f"{ self.chan }_3"]
        # Location
        ex, ey = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side * 0.5, radius, angle )
        return ex, ey
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse ):
        self.analyse = analyse
        self.update()
    def Update_Mask( self, gamut_mask ):
        self.gamut_mask = gamut_mask
        self.update()
    def Update_Profile( self, gamut_profile ):
        self.gamut_1tri = gamut_profile[0]
        self.gamut_1squ = gamut_profile[1]
        self.gamut_1cir = gamut_profile[2]
        self.gamut_2cir = gamut_profile[3]
        self.gamut_3pie = gamut_profile[4]
        self.update()

    # Emit
    def Signal_Profile( self ):
        profile = [ self.gamut_1tri, self.gamut_1squ, self.gamut_1cir, self.gamut_2cir, self.gamut_3pie ]
        self.SIGNAL_PROFILE.emit( profile )

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # Variables
        self.press = True
        self.origin_x = ex
        self.origin_y = ey
        self.origin_tan_axis = self.tan_axis
        self.origin_angle = self.geometry.Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
        self.origin_dist = self.geometry.Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
        self.region = self.geometry.Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 ) <= ( self.side * self.disk_radius )

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, False )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey, False )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex, ey )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.press = False
            self.Context_Menu( event )
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Snap( ex, ey )

        # Rotate
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) ):
            self.gamut_rotation = self.Gamut_Rotation()

        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, False )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey, False )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex, ey )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            # self.Cursor_Move( ex, ey )
            self.Cursor_Position( ex, ey, False )

        # Rotate
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) ):
            self.Cursor_Rotation( ex, ey )

        # Update
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, False )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey, False )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex, ey )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            # self.Cursor_Move( ex, ey )
            self.Cursor_Position( ex, ey, False )

        # Rotate
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) ):
            self.Cursor_Rotation( ex, ey )

        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Previous
        self.previous_dist = self.geometry.Trig_2D_Points_Distance( self.ex, self.ey, self.w2, self.h2 )
        # Variables
        self.press = False
        self.zoom = False
        self.pressure = 0
        self.region = None
        self.origin_x = 0
        self.origin_y = 0
        self.origin_angle = 0
        self.origin_dist = 0
        # Gamut
        self.gamut_index = None
        self.gamut_rotation = None
        # Pin
        self.pin_index = None
        # Updates
        self.SIGNAL_RELEASE.emit( 0 )
        self.update()

    def Cursor_Position( self, ex, ey, clip ):
        # Hue
        angle = self.geometry.Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
        if clip == True:
            angle = self.geometry.Limit_Angle( angle, 2.5 )
        if self.wheel_mode == "DIGITAL":
            hue = angle / 360
        if self.wheel_mode == "ANALOG":
            angle = self.geometry.Limit_Looper( angle + hue_a, 360 )
            hue = self.convert.huea_to_hued( angle / 360 )
        # Saturation
        distance = 0
        radius = self.side * self.disk_radius
        if self.region == False: # Ring
            distance = self.previous_dist
            self.ex, self.ey = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side, distance, angle )
        if self.region == True: # Disk
            distance = self.geometry.Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
            if distance >= radius:
                distance = radius
                self.ex, self.ey = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side, 0.5, angle )
            else:
                self.ex = ex
                self.ey = ey

        # Variables
        c1 = hue
        c2 = distance / radius

        # Edit Dot
        if self.gamut_index != None:
            # Move
            mx = ( self.ex - self.disk_x ) / self.disk_side
            my = ( self.ey - self.disk_y ) / self.disk_side
            # Apply
            lista = self.Gamut_List( self.gamut_mask )
            if ( self.gamut_mask != "2 Circle" and self.gamut_index != 0 ):
                lista[self.gamut_index] = ( mx, my )
            if ( self.gamut_mask == "2 Circle" and self.gamut_index != 0 and self.gamut_index != 5 ):
                lista[self.gamut_index] = ( mx, my )
        elif self.pin_index != None:
            pin = { "pin_index" : self.pin_index, "c1" : c1, "c2" : c2 }
            self.SIGNAL_PIN_EDIT.emit( pin )

        # Emition
        value = { "c1" : c1, "c2" : c2 }
        self.SIGNAL_VALUE.emit( value )

        # Update Centroids
        self.Gamut_Centroid( self.gamut_mask )
    def Cursor_Tangent( self, ex, ey ):
        if self.region == False: # Ring
            self.Cursor_Position( ex, ey, True )
        if self.region == True: # Disk
            # Hue
            delta_hue = ( ( ex - self.origin_x ) / self.ww )
            self.tan_axis = self.geometry.Limit_Float( self.origin_tan_axis + delta_hue )
            # Update
            self.SIGNAL_TAN.emit( self.tan_axis )
    def Cursor_Snap( self, ex, ey ):
        if self.region == True:
            # Gamut Profile
            lista = self.Gamut_List( self.gamut_mask )
            points = self.Gamut_Points( ex, ey, lista )

            # Pins
            points = self.Pin_Points( ex, ey, points )

            # Position
            if len( points ) > 0:
                points.sort( key = lambda row: row[0] )
                check_gamut = points[0][3] # gamut_index
                check_pin = points[0][4] # pin_index
                if check_gamut != None:
                    self.gamut_index = check_gamut
                    self.Cursor_Position( points[0][1], points[0][2], False )
                elif check_pin != None:
                    self.pin_index = check_pin
                    self.SIGNAL_PIN_INDEX.emit( check_pin )
    def Cursor_Rotation( self, ex, ey ):
        lista = self.Gamut_List( self.gamut_mask )
        ang_new = self.geometry.Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, ex, ey )
        delta = self.geometry.Limit_Looper( ang_new - self.origin_angle, 360 )
        for i in range( 0, len( lista ) ):
            # Read
            dis = self.gamut_rotation[i][0]
            angle = self.gamut_rotation[i][1]
            if dis != 0:
                radius = dis / self.disk_side
                angle = self.geometry.Limit_Looper( angle + delta, 360 )
                dx, dy = self.geometry.Trig_2D_Angle_Circle( 0.5, 0.5, 1, radius, angle )
                lista[i] = ( dx, dy )

        # Update Centroids
        self.Gamut_Centroid( self.gamut_mask )

    # Gamut
    def Gamut_List( self, mode ):
        if mode == "None":
            lista = []
        if mode == "Triangle":
            lista = self.gamut_1tri
        if mode == "Square":
            lista = self.gamut_1squ
        if mode == "Circle":
            lista = self.gamut_1cir
        if mode == "2 Circle":
            lista = self.gamut_2cir
        if mode == "3 Pie":
            lista = self.gamut_3pie
        return lista
    def Gamut_Rotation( self ):
        lista = self.Gamut_List( self.gamut_mask )
        rotation = []
        for i in range( 0, len( lista ) ):
            px = self.disk_x + lista[i][0] * self.disk_side
            py = self.disk_y + lista[i][1] * self.disk_side
            dist = self.geometry.Trig_2D_Points_Distance( px, py, self.w2, self.h2 )
            angle = self.geometry.Trig_2D_Points_Lines_Angle( 0, self.h2, self.w2, self.h2, px, py )
            rotation.append( ( dist, angle ) )
        return rotation
    def Gamut_Centroid( self, mode ):
        # Update Centroid
        if mode == "Triangle":
            p = self.gamut_1tri
            c = self.geometry.Trig_2D_Centroid_Triangle( p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1] )
            self.gamut_1tri[0] = ( c[0], c[1] )
        if mode == "Square":
            p = self.gamut_1squ
            c = self.geometry.Trig_2D_Centroid_Square( p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1], p[4][0], p[4][1] )
            self.gamut_1squ[0] = ( c[0], c[1] )
        if mode == "Circle":
            p = self.gamut_1cir
            c = self.geometry.Trig_2D_Centroid_Square( p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1], p[4][0], p[4][1] )
            self.gamut_1cir[0] = ( c[0], c[1] )
        if mode == "2 Circle":
            # Circle 1
            p = self.gamut_2cir[0:5]
            c = self.geometry.Trig_2D_Centroid_Square( p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1], p[4][0], p[4][1] )
            self.gamut_2cir[0] = ( c[0], c[1] )
            # Circle 2
            p = self.gamut_2cir[5:10]
            c = self.geometry.Trig_2D_Centroid_Square( p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1], p[4][0], p[4][1] )
            self.gamut_2cir[5] = ( c[0], c[1] )
        # Save Profile
        self.Signal_Profile()

    # Points
    def Gamut_Points( self, ex, ey, lista ):
        points = []
        for i in range( 0, len( lista ) ):
            px = self.disk_x + lista[i][0] * self.disk_side
            py = self.disk_y + lista[i][1] * self.disk_side
            distance = self.geometry.Trig_2D_Points_Distance( ex, ey, px, py )
            points.append( ( distance, px, py, i, None ) ) # dist px py gamut_index, pin_index
        return points
    def Pin_Points( self, ex, ey, points ):
        if self.pin_list != None:
            for i in range( 0, len( self.pin_list ) - 1 ):
                if self.pin_list[i]["active"] == True:
                    if self.wheel_mode == "DIGITAL":
                        angle = self.pin_list[i]["hue_d"] * 360
                    if self.wheel_mode == "ANALOG":
                        angle = self.pin_list[i]["hue_a"] * 360 - hue_a
                    radius = self.pin_list[i][f"{self.chan}_2"]
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side * 0.5, radius, angle )
                    distance = self.geometry.Trig_2D_Points_Distance( ex, ey, px, py )
                    points.append( ( distance, px, py, None, i ) ) # dist px py gamut_index, pin_index
        return points

    # Context
    def Context_Menu( self, event ):
        if self.press == False:
            # Menu
            qmenu = QMenu( self )
            # Action 
            qmenu_gn = qmenu.addAction( "None" )
            qmenu_gt = qmenu.addAction( "Triangle" )
            qmenu_gs = qmenu.addAction( "Square" )
            qmenu_g1c = qmenu.addAction( "Circle" )
            qmenu_g2c = qmenu.addAction( "2 Circle" )
            qmenu_g3p = qmenu.addAction( "3 Pie" )
            qmenu_gr = qmenu.addAction( "Reset" )
            qmenu_gn.setCheckable( True )
            qmenu_gt.setCheckable( True )
            qmenu_gs.setCheckable( True )
            qmenu_g1c.setCheckable( True )
            qmenu_g2c.setCheckable( True )
            qmenu_g3p.setCheckable( True )
            qmenu_gn.setChecked( self.gamut_mask == "None" )
            qmenu_gt.setChecked( self.gamut_mask == "Triangle" )
            qmenu_gs.setChecked( self.gamut_mask == "Square" )
            qmenu_g1c.setChecked( self.gamut_mask == "Circle" )
            qmenu_g2c.setChecked( self.gamut_mask == "2 Circle" )
            qmenu_g3p.setChecked( self.gamut_mask == "3 Pie" )
            # Mapping
            action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
            # Triggers
            if action == qmenu_gn:
                self.gamut_mask = "None"
                self.SIGNAL_MASK.emit( self.gamut_mask )
            if action == qmenu_gt:
                self.gamut_mask = "Triangle"
                self.SIGNAL_MASK.emit( self.gamut_mask )
            if action == qmenu_gs:
                self.gamut_mask = "Square"
                self.SIGNAL_MASK.emit( self.gamut_mask )
            if action == qmenu_g1c:
                self.gamut_mask = "Circle"
                self.SIGNAL_MASK.emit( self.gamut_mask )
            if action == qmenu_g2c:
                self.gamut_mask = "2 Circle"
                self.SIGNAL_MASK.emit( self.gamut_mask )
            if action == qmenu_g3p:
                self.gamut_mask = "3 Pie"
                self.SIGNAL_MASK.emit( self.gamut_mask )
            if action == qmenu_gr:
                if self.gamut_mask == "Triangle":
                    self.gamut_1tri = self.neutral_1tri.copy()
                if self.gamut_mask == "Square":
                    self.gamut_1squ = self.neutral_1squ.copy()
                if self.gamut_mask == "Circle":
                    self.gamut_1cir = self.neutral_1cir.copy()
                if self.gamut_mask == "2 Circle":
                    self.gamut_2cir = self.neutral_2cir.copy()
                if self.gamut_mask == "3 Pie":
                    self.gamut_3pie = self.neutral_3pie.copy()
                self.update()
                self.Signal_Profile()

    # Tablet Interaction
    def tabletEvent( self, event ):
        self.pressure = event.pressure()
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        line_width = 5
        circle_0, circle_1, circle_2, circle_3 = Circles( self, painter )

        # Hue
        if self.wheel_mode == "DIGITAL":
            hue_index = "hue_d"
        if self.wheel_mode == "ANALOG":
            hue_index = "hue_a"
        # Circle Points
        radius = 0.5
        circle_points = []
        if self.harmony_rule != None:
            for i in range( 0, len( self.harmony_list ) ):
                if self.wheel_mode == "DIGITAL":
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, self.harmony_list[i][hue_index] * 360 )
                if self.wheel_mode == "ANALOG":
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, ( self.harmony_list[i][hue_index] * 360 ) - hue_a )
                circle_points.append( [ px, py ] )
        else:
            if self.wheel_mode == "DIGITAL":
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, self.color[hue_index] * 360 )
            if self.wheel_mode == "ANALOG":
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, ( self.color[hue_index] * 360 ) - hue_a )
            circle_points.append( [ px, py ] )
        length = len( circle_points )
        # Divisions
        div = []
        if self.wheel_mode == "DIGITAL":
            for i in range( 0, len( self.digital ) ):
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, self.digital[i] )
                div.append( [ px, py ] )
        if self.wheel_mode == "ANALOG":
            for i in range( 0, len( self.analog ) ):
                px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, self.analog[i] - hue_a )
                div.append( [ px, py ] )

        # Outter Mask
        outline = QPainterPath()
        outline.addEllipse( int( 0 ), int( 0 ), int( self.ww ), int( self.hh ) )
        painter.setClipPath( circle_0 )

        # Dark Border
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_theme ) )
        circle_02 = circle_0.subtracted( circle_2 )
        painter.drawPath( circle_02 )
        # Dark Lines
        painter.setPen( QPen( self.color_theme, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        if self.wheel_mode == "DIGITAL":
            for i in range( 0, len( self.digital ) ):
                painter.drawLine( int( div[i][0] ), int( div[i][1] ), int( self.w2 ), int( self.h2 ) )
        if self.wheel_mode == "ANALOG":
            for i in range( 0, len( self.analog ) ):
                painter.drawLine( int( div[i][0] ), int( div[i][1] ), int( self.w2 ), int( self.h2 ) )

        # Line Gray
        painter.setPen( QPen( self.color_1, line_width, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
        painter.setBrush( QtCore.Qt.NoBrush )
        circle_02 = circle_0.subtracted( circle_2 )
        if length > 0:
            line_gray = QPainterPath()
            for i in range( 0, length ):
                # Variables
                px = circle_points[i][0]
                py = circle_points[i][1]
                # Draw
                line_gray.moveTo( int( self.w2 ), int( self.h2 ) )
                line_gray.lineTo( int( px ), int( py ) )
            painter.setClipPath( circle_02 )
            painter.drawPath( line_gray )

        # Reset Mask
        square = QPainterPath()
        square.moveTo( int( 0 ), int( 0 ) )
        square.lineTo( int( self.ww ), int( 0 ) )
        square.lineTo( int( self.ww ), int( self.hh ) )
        square.lineTo( int( 0 ), int( self.hh ) )
        painter.setClipPath( square )

        # Draw Gradient
        if len( self.qpixmap_list ) > 0:
            try:
                # Pixmaps
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( QtCore.Qt.NoBrush )
                tan_index = int( self.tan_axis * self.tan_range )
                qpixmap = self.qpixmap_list[tan_index]
                # Brush
                qbrush = QBrush( qpixmap )
                if qpixmap.isNull() == False:
                    qtransform = QTransform()
                    qtransform.translate( int( self.disk_x ), int( self.disk_y ) )
                    qtransform.scale( int( self.disk_side ) / 256, int( self.disk_side ) / 256 )
                    qbrush.setTransform( qtransform )
                # Painter
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( qbrush )
            except:
                pass
        # Polygon
        dot = 5
        line_size = 2
        key = self.gamut_mask
        gdx = self.disk_x
        gdy = self.disk_y
        gds = self.disk_side
        if self.gamut_mask == "None":
            painter.setPen( QtCore.Qt.NoPen )
            painter.drawEllipse( int( gdx ), int( gdy ), int( gds ), int( gds ) )
        if self.gamut_mask == "Triangle":
            # Polygon
            painter.setPen( QtCore.Qt.NoPen )
            poly = QPolygon( [
                QPoint( int( gdx + gds * self.gamut_1tri[1][0] ), int( gdy + gds * self.gamut_1tri[1][1] ) ),
                QPoint( int( gdx + gds * self.gamut_1tri[2][0] ), int( gdy + gds * self.gamut_1tri[2][1] ) ),
                QPoint( int( gdx + gds * self.gamut_1tri[3][0] ), int( gdy + gds * self.gamut_1tri[3][1] ) ),
                ] )
            painter.drawPolygon( poly )
            # Display Subjective Primaries
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1tri[0][0] - dot ), int( gdy + gds * self.gamut_1tri[0][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1tri[1][0] - dot ), int( gdy + gds * self.gamut_1tri[1][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1tri[2][0] - dot ), int( gdy + gds * self.gamut_1tri[2][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1tri[3][0] - dot ), int( gdy + gds * self.gamut_1tri[3][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
        if self.gamut_mask == "Square":
            # Polygon
            painter.setPen( QtCore.Qt.NoPen )
            poly = QPolygon( [
                QPoint( int( gdx + gds * self.gamut_1squ[1][0] ), int( gdy + gds * self.gamut_1squ[1][1] ) ),
                QPoint( int( gdx + gds * self.gamut_1squ[2][0] ), int( gdy + gds * self.gamut_1squ[2][1] ) ),
                QPoint( int( gdx + gds * self.gamut_1squ[3][0] ), int( gdy + gds * self.gamut_1squ[3][1] ) ),
                QPoint( int( gdx + gds * self.gamut_1squ[4][0] ), int( gdy + gds * self.gamut_1squ[4][1] ) ),
                ] )
            painter.drawPolygon( poly )
            # Display Subjective Primaries
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1squ[0][0] - dot ), int( gdy + gds * self.gamut_1squ[0][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1squ[1][0] - dot ), int( gdy + gds * self.gamut_1squ[1][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1squ[2][0] - dot ), int( gdy + gds * self.gamut_1squ[2][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1squ[3][0] - dot ), int( gdy + gds * self.gamut_1squ[3][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_1squ[4][0] - dot ), int( gdy + gds * self.gamut_1squ[4][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
        if self.gamut_mask == "Circle":
            # Profile Points
            path, P0, P1, P2, P3, P4 = self.Render_Circle( gdx, gdy, gds, self.gamut_1cir, circle_2 )

            # Polygon
            painter.setPen( QtCore.Qt.NoPen )
            painter.drawPath( path )
            # Display Subjective Primaries
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            painter.drawEllipse( int( P0[0] - dot ), int( P0[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P1[0] - dot ), int( P1[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P2[0] - dot ), int( P2[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P3[0] - dot ), int( P3[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P4[0] - dot ), int( P4[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
        if self.gamut_mask == "2 Circle":
            # Profile Points
            path_0, P0_0, P1_0, P2_0, P3_0, P4_0 = self.Render_Circle( gdx, gdy, gds, self.gamut_2cir[0:5], circle_2 )
            path_1, P0_1, P1_1, P2_1, P3_1, P4_1 = self.Render_Circle( gdx, gdy, gds, self.gamut_2cir[5:10], circle_2 )

            # Polygon
            painter.setPen( QtCore.Qt.NoPen )
            painter.drawPath( path_0 )
            painter.drawPath( path_1 )
            # Display Subjective Primaries
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            # Circle 0
            painter.drawEllipse( int( P0_0[0] - dot ), int( P0_0[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P1_0[0] - dot ), int( P1_0[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P2_0[0] - dot ), int( P2_0[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P3_0[0] - dot ), int( P3_0[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P4_0[0] - dot ), int( P4_0[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            # Circle 1
            painter.drawEllipse( int( P0_1[0] - dot ), int( P0_1[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P1_1[0] - dot ), int( P1_1[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P2_1[0] - dot ), int( P2_1[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P3_1[0] - dot ), int( P3_1[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( P4_1[0] - dot ), int( P4_1[1] - dot ), int( dot * 2 ), int( dot * 2 ) )
        if self.gamut_mask == "3 Pie":
            # Variables
            rect = QRect( int( gdx ), int( gdy ), int( gds ), int( gds ) )
            ang_a1 = 16 * self.geometry.Trig_2D_Points_Lines_Angle(
                gdx + self.gamut_3pie[1][0] * gds, gdy + self.gamut_3pie[1][1] * gds,
                self.w2, self.h2,
                self.ww, self.h2,
                )
            ang_a2 = -16 * self.geometry.Trig_2D_Points_Lines_Angle(
                gdx + self.gamut_3pie[1][0] * gds, gdy + self.gamut_3pie[1][1] * gds,
                self.w2, self.h2,
                gdx + self.gamut_3pie[2][0] * gds, gdy + self.gamut_3pie[2][1] * gds,
                )
            ang_b1 = 16 * self.geometry.Trig_2D_Points_Lines_Angle(
                gdx + self.gamut_3pie[3][0] * gds, gdy + self.gamut_3pie[3][1] * gds,
                self.w2, self.h2,
                self.ww, self.h2,
                )
            ang_b2 = -16 * self.geometry.Trig_2D_Points_Lines_Angle(
                gdx + self.gamut_3pie[3][0] * gds, gdy + self.gamut_3pie[3][1] * gds,
                self.w2, self.h2,
                gdx + self.gamut_3pie[4][0] * gds, gdy + self.gamut_3pie[4][1] * gds,
                )
            ang_c1 = 16 * self.geometry.Trig_2D_Points_Lines_Angle(
                gdx + self.gamut_3pie[5][0] * gds, gdy + self.gamut_3pie[5][1] * gds,
                self.w2, self.h2,
                self.ww, self.h2,
                )
            ang_c2 = -16 * self.geometry.Trig_2D_Points_Lines_Angle(
                gdx + self.gamut_3pie[5][0] * gds, gdy + self.gamut_3pie[5][1] * gds,
                self.w2, self.h2,
                gdx + self.gamut_3pie[6][0] * gds, gdy + self.gamut_3pie[6][1] * gds,
                )

            # Polygon
            painter.setPen( QtCore.Qt.NoPen )
            painter.drawPie( rect, int( ang_a1 ), int( ang_a2 ) )
            painter.drawPie( rect, int( ang_b1 ), int( ang_b2 ) )
            painter.drawPie( rect, int( ang_c1 ), int( ang_c2 ) )
            # Display Subjective Primaries
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[0][0] - dot ), int( gdy + gds * self.gamut_3pie[0][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[1][0] - dot ), int( gdy + gds * self.gamut_3pie[1][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[2][0] - dot ), int( gdy + gds * self.gamut_3pie[2][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[3][0] - dot ), int( gdy + gds * self.gamut_3pie[3][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[4][0] - dot ), int( gdy + gds * self.gamut_3pie[4][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[5][0] - dot ), int( gdy + gds * self.gamut_3pie[5][1] - dot ), int( dot * 2 ), int( dot * 2 ) )
            painter.drawEllipse( int( gdx + gds * self.gamut_3pie[6][0] - dot ), int( gdy + gds * self.gamut_3pie[6][1] - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Analyse Colors
        if self.analyse != None:
            # Variables
            dot = 5
            line_size = 2
            length = len( self.analyse )

            # Draw
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            for i in range( 0, length ):
                color = self.analyse[i]
                if int( self.tan_axis * 255 ) == int( color[f"{self.chan}_3"] * 255 ):
                    if self.wheel_mode == "DIGITAL":
                        angle = color[hue_index] * 360
                    if self.wheel_mode == "ANALOG":
                        angle = color[hue_index] * 360 - hue_a
                    radius = color[f"{self.chan}_2"]
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side * 0.5, radius, angle )
                    painter.drawEllipse( int( px - dot ), int( py - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Pinned Colors
        if ( self.color != None and self.pin_list != None ):
            # Variables
            dot = 5
            line_size = 2
            length = len( self.pin_list )

            # Draw
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.white ) )
            for i in range( 0, length ):
                if self.pin_list[i]["active"] == True:
                    if self.wheel_mode == "DIGITAL":
                        angle = self.pin_list[i][hue_index] * 360
                    if self.wheel_mode == "ANALOG":
                        angle = self.pin_list[i][hue_index] * 360 - hue_a
                    radius = self.pin_list[i][f"{self.chan}_2"]
                    px, py = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side * 0.5, radius, angle )
                    painter.drawEllipse( int( px - dot ), int( py - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Harmony Colors
        if ( self.color != None and self.harmony_list != None ):
            # Variables
            line_size = 2
            dot = 5

            # Parsing
            points = []
            for i in range( 0, len( self.harmony_list ) ):
                if self.wheel_mode == "DIGITAL":
                    angle = self.harmony_list[i][hue_index] * 360
                if self.wheel_mode == "ANALOG":
                    angle = self.harmony_list[i][hue_index] * 360 - hue_a
                radius = self.harmony_list[i][f"{self.chan}_2"]
                har_x, har_y = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.disk_side * 0.5, radius, angle )
                points.append( ( har_x, har_y ) )
            length = len( points )

            # Draw Line
            painter.setPen( QPen( self.white, line_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( points[i-1][0] ), int( points[i-1][1] ), int( points[i][0] ), int( points[i][1] ) )
            if self.harmony_rule in [ "Triadic", "Tetradic" ]:
                painter.drawLine( int( points[0][0] ), int( points[0][1] ), int( points[length-1][0] ), int( points[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.black, line_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.white ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( points[i][0] - dot ), int( points[i][1] - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Cursor
        size = 10
        zoom_size = 100
        margin_size = 10
        if ( self.press == True and self.zoom == True ):
            size = zoom_size
            Cursor_Zoom( self, painter, size, margin_size )
        elif( self.pressure > self.input_pressure ):
            size = zoom_size * self.pressure
            Cursor_Zoom( self, painter, size, margin_size )
        else:
            Cursor_Normal( self, painter, size )
    def Render_Circle( self, px, py, side, points, circle ):
        # Points from User
        P0 = [ px + points[0][0] * side, py + points[0][1] * side ]
        P1 = [ px + points[1][0] * side, py + points[1][1] * side ]
        P2 = [ px + points[2][0] * side, py + points[2][1] * side ]
        P3 = [ px + points[3][0] * side, py + points[3][1] * side ]
        P4 = [ px + points[4][0] * side, py + points[4][1] * side ]
        # Angles from the Points
        O1 = self.geometry.Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P1[0],P1[1] )
        O2 = self.geometry.Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P2[0],P2[1] )
        O3 = self.geometry.Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P3[0],P3[1] )
        O4 = self.geometry.Trig_2D_Points_Lines_Angle( px, P0[1], P0[0],P0[1], P4[0],P4[1] )
        # Order Angles in Sequence
        order = [ ( O1, P1 ), ( O2, P2 ), ( O3, P3 ), ( O4, P4 ) ]
        order.sort()
        A1 = order[0][1]
        A2 = order[1][1]
        A3 = order[2][1]
        A4 = order[3][1]
        # Bridge Points
        B12 = [ self.geometry.Lerp_1D( 0.5, A1[0], A2[0] ), self.geometry.Lerp_1D( 0.5, A1[1], A2[1] ) ]
        B23 = [ self.geometry.Lerp_1D( 0.5, A2[0], A3[0] ), self.geometry.Lerp_1D( 0.5, A2[1], A3[1] ) ]
        B34 = [ self.geometry.Lerp_1D( 0.5, A3[0], A4[0] ), self.geometry.Lerp_1D( 0.5, A3[1], A4[1] ) ]
        B41 = [ self.geometry.Lerp_1D( 0.5, A4[0], A1[0] ), self.geometry.Lerp_1D( 0.5, A4[1], A1[1] ) ]
        # Bridge Components
        dist_B12 = self.geometry.Trig_2D_Ortogonal_Components( P0[0], P0[1], B12[0], B12[1] )
        dist_B23 = self.geometry.Trig_2D_Ortogonal_Components( P0[0], P0[1], B23[0], B23[1] )
        dist_B34 = self.geometry.Trig_2D_Ortogonal_Components( P0[0], P0[1], B34[0], B34[1] )
        dist_B41 = self.geometry.Trig_2D_Ortogonal_Components( P0[0], P0[1], B41[0], B41[1] )
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
            QPoint( int( self.geometry.Lerp_1D( a, A1[0], P12[0] ) ), int( self.geometry.Lerp_1D( a, A1[1], P12[1] ) ) ),
            QPoint( int( self.geometry.Lerp_1D( b, P12[0], A2[0] ) ), int( self.geometry.Lerp_1D( b, P12[1], A2[1] ) ) ),
            QPoint( int( A2[0] ), int( A2[1] ) ) )
        path.cubicTo(
            QPoint( int( self.geometry.Lerp_1D( a, A2[0], P23[0] ) ), int( self.geometry.Lerp_1D( a, A2[1], P23[1] ) ) ),
            QPoint( int( self.geometry.Lerp_1D( b, P23[0], A3[0] ) ), int( self.geometry.Lerp_1D( b, P23[1], A3[1] ) ) ),
            QPoint( int( A3[0] ), int( A3[1] ) ) )
        path.cubicTo(
            QPoint( int( self.geometry.Lerp_1D( a, A3[0], P34[0] ) ), int( self.geometry.Lerp_1D( a, A3[1], P34[1] ) ) ),
            QPoint( int( self.geometry.Lerp_1D( b, P34[0], A4[0] ) ), int( self.geometry.Lerp_1D( b, P34[1], A4[1] ) ) ),
            QPoint( int( A4[0] ), int( A4[1] ) ) )
        path.cubicTo(
            QPoint( int( self.geometry.Lerp_1D( a, A4[0], P41[0] ) ), int( self.geometry.Lerp_1D( a, A4[1], P41[1] ) ) ),
            QPoint( int( self.geometry.Lerp_1D( b, P41[0], A1[0] ) ), int( self.geometry.Lerp_1D( b, P41[1], A1[1] ) ) ),
            QPoint( int( A1[0] ), int( A1[1] ) ) )
        path = path.intersected( circle )
        # Return
        return path, P0, P1, P2, P3, P4

class Panel_Hexagon( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( dict )
    SIGNAL_TAN = QtCore.pyqtSignal( float )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )
    SIGNAL_PIN_INDEX = QtCore.pyqtSignal( int )
    SIGNAL_PIN_EDIT = QtCore.pyqtSignal( dict )

    # Init
    def __init__( self, parent ):
        super( Panel_Hexagon, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.origin_x = 0
        self.origin_y = 0
        self.origin_tan_axis = 0
        self.ex = 0
        self.ey = 0
        self.press = False
        self.pressure = 0
        self.input_pressure = 0.5
        self.px = 0
        self.py = 0
        self.side = 0

        # Display
        self.zoom = False
        self.tan_axis = 0 # 0-360 because of background index
        self.tan_range = 255
        self.qpixmap_list = []

        # Format
        self.directory = None # Path
        self.d_cm = None # "A" "RGB" "CMYK" "YUV" "XYZ" "LAB"
        # Wheel
        self.wheel_mode = "DIGITAL" # "DIGITAL" "ANALOG"
        self.wheel_space = "HSV" # "HSV" "HSL" "HCY" "ARD"

        # Geometry
        self.O1 = None
        self.O2 = None
        self.O3 = None
        self.O4 = None
        self.O5 = None
        self.O6 = None
        self.C61 = None

        # Colors
        self.color = None
        self.hex_color = QColor( "#000000" )
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
        # Harmony Colors
        self.harmony_rule = None
        self.harmony_index = None
        self.harmony_list = None
        # Pinned Colors
        self.pin_index = None
        self.pin_list = None
        # Analyse Colors
        self.analyse = None

        # Modules
        self.geometry = Geometry()
        self.convert = None
    def Init_Convert( self, convert ):
        self.convert = convert
        self.update()

    # Set
    def Set_ColorModel( self, d_cm ):
        self.d_cm = d_cm
        self.Set_ColorSpace_inDocument( self.directory, self.d_cm )
        self.update()
    def Set_Wheel( self, wheel_mode, wheel_space ):
        self.wheel_mode = wheel_mode
        self.wheel_space = wheel_space
        self.update()
    def Set_ColorSpace_inDocument( self, directory, d_cm ):
        # Variables
        self.directory = directory
        self.d_cm = d_cm

        # Cursor
        if self.color != None:
            self.ex = self.geometry.Limit_Range( self.color[f"uvd_1"] * self.ww, 0, self.ww )
            self.ey = self.geometry.Limit_Range( self.color[f"uvd_2"] * self.hh, 0, self.hh )

        # Read Zip File
        location = os.path.join( self.directory, panel )
        location = os.path.join( location, f"{ self.d_cm }_UVD_4.zip" )
        self.qpixmap_list = Read_Zip( self, location, self.tan_range, "UVD", "4" )

        # Update
        self.update()
    def Set_Size( self, ww, hh ):
        # Variables
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        # Frame
        if self.ww >= self.hh:
            self.side = self.hh
            self.px = self.w2 - ( self.side * 0.5 )
            self.py = 0
        else:
            self.side = self.ww
            self.px = 0
            self.py = self.h2 - ( self.side * 0.5 )
        # Origin Points
        self.O1, self.O2, self.O3, self.O4, self.O5, self.O6, C12, C23, C34, C45, C56, self.C61 = self.convert.uvd_hexagon( self.tan_axis, 0.5, 0.5, -1 )
        # Update
        self.resize( ww, hh )
    def Set_Zoom( self, boolean ):
        self.press = boolean
        self.zoom = boolean
        self.update()

    # Updates
    def Update_Panel( self, color ):
        # Variables
        self.color = color
        # Display
        self.hex_color = QColor( color["hex6"] )
        # Values
        self.ex = self.px + ( 0.5 + color["uvd_1"] * 0.5 ) * self.side
        self.ey = self.py + ( 0.5 - color["uvd_2"] * 0.5 ) * self.side
        self.tan_axis = color["uvd_3"]
        # Origin Points
        self.O1, self.O2, self.O3, self.O4, self.O5, self.O6, C12, C23, C34, C45, C56, self.C61 = self.convert.uvd_hexagon( self.tan_axis, 0.5, 0.5, -1 )
        # Update
        self.update()
    def Update_Harmony( self, harmony_rule, harmony_index, harmony_list ):
        self.harmony_rule = harmony_rule
        self.harmony_index = harmony_index
        self.harmony_list = harmony_list
        self.update()
    def Update_Pin( self, pin_list ):
        self.pin_list = pin_list
        self.update()
    def Update_Analyse( self, analyse ):
        self.analyse = analyse
        self.update()

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # Variables
        self.origin_x = ex
        self.origin_y = ey
        self.origin_tan_axis = self.tan_axis
        self.press = True

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, None )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey, None )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Snap( ex, ey )

        self.update()
    def mouseMoveEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, None )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey, None )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Position( ex, ey, self.pin_index )

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( ex, ey, None )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( ex, ey, None )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Tangent( ex )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Snap( ex, ey )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.Cursor_Position( ex, ey, self.pin_index )

        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.press = False
        self.zoom = False
        self.pressure = 0
        self.pin_index = None
        # Updates
        self.SIGNAL_RELEASE.emit( 0 )
        self.update()

    # Mouse Event
    def Cursor_Position( self, ex, ey, pin_index ):
        # Calculation
        if ( self.tan_axis <= 0 or self.tan_axis >= 1 ):
            self.ex = self.w2
            self.ey = self.h2
        else:
            self.ex, self.ey = self.Hexagon_Inter( ex, ey, self.tan_axis)
        u = 2 * ( ( self.ex - self.px ) / self.side ) - 1
        v = -2 * ( ( self.ey - self.py ) / self.side ) + 1

        # Signal
        values = { "c1" : u, "c2" : v, "pin_index" : pin_index }
        self.SIGNAL_VALUE.emit( values )
        if pin_index != None:
            self.SIGNAL_PIN_EDIT.emit( values )
    def Cursor_Tangent( self, ex ):
        # Hue
        delta_hue = ( ( ex - self.origin_x ) / self.ww )
        self.tan_axis = self.geometry.Limit_Float( self.origin_tan_axis + delta_hue )
        # Update
        self.SIGNAL_TAN.emit( self.tan_axis )
    def Cursor_Snap( self, ex, ey ):
        if self.pin_list != None:
            distance = []
            for i in range( 0, len( self.pin_list ) ):
                if self.pin_list[i]["active"] == True:
                    px = self.px + ( 0.5 + self.pin_list[i]["uvd_1"] * 0.5 ) * self.side
                    py = self.py + ( 0.5 - self.pin_list[i]["uvd_2"] * 0.5 ) * self.side
                    dist = self.geometry.Trig_2D_Points_Distance( ex, ey, px, py )
                    distance.append( ( dist, i ) )
            if len( distance ) > 0:
                distance.sort()
                pin_index = distance[0][1]
                if pin_index < 20:
                    self.pin_index = pin_index
                    self.SIGNAL_PIN_INDEX.emit( self.pin_index )

    # Panel Modifiers
    def Hexagon_Inter( self, ex, ey, d ):
        # Variables
        red_x = self.px + self.C61[0] * self.side
        red_y = self.py + self.C61[1] * self.side
        o1_x = self.px + self.O1[0] * self.side
        o1_y = self.py + self.O1[1] * self.side
        o2_x = self.px + self.O2[0] * self.side
        o2_y = self.py + self.O2[1] * self.side
        o3_x = self.px + self.O3[0] * self.side
        o3_y = self.py + self.O3[1] * self.side
        o4_x = self.px + self.O4[0] * self.side
        o4_y = self.py + self.O4[1] * self.side
        o5_x = self.px + self.O5[0] * self.side
        o5_y = self.py + self.O5[1] * self.side
        o6_x = self.px + self.O6[0] * self.side
        o6_y = self.py + self.O6[1] * self.side

        # Single Points
        di = round( d * 3, 14 )
        if ( di <= 0 or di >= 3 ):
            ex = self.w2
            ey = self.h2
        else:
            # Angles
            angle = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, ex, ey )
            a1 = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o1_x, o1_y )
            a2 = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o2_x, o2_y )
            a3 = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o3_x, o3_y )
            a4 = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o4_x, o4_y )
            a5 = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o5_x, o5_y )
            a6 = self.geometry.Trig_2D_Points_Lines_Angle( red_x, red_y, self.w2, self.h2, o6_x, o6_y )
            if a6 == 0:
                a6 = 360

            # Limit
            if angle <= a1:
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( red_x, red_y, o1_x, o1_y, ex, ey, self.w2, self.h2 )
            elif ( angle >= a1 and angle <= a2 ):
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( o1_x, o1_y, o2_x, o2_y, ex, ey, self.w2, self.h2 )
            elif ( angle >= a2 and angle <= a3 ):
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( o2_x, o2_y, o3_x, o3_y, ex, ey, self.w2, self.h2 )
            elif ( angle >= a3 and angle <= a4 ):
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( o3_x, o3_y, o4_x, o4_y, ex, ey, self.w2, self.h2 )
            elif ( angle >= a4 and angle <= a5 ):
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( o4_x, o4_y, o5_x, o5_y, ex, ey, self.w2, self.h2 )
            elif ( angle >= a5 and angle <= a6 ):
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( o5_x, o5_y, o6_x, o6_y, ex, ey, self.w2, self.h2 )
            elif angle >= a6:
                lx, ly = self.geometry.Trig_2D_Points_Lines_Intersection( o6_x, o6_y, red_x, red_y, ex, ey, self.w2, self.h2 )
            else:
                radius = self.geometry.Trig_2D_Points_Distance( o1_x, o1_y, self.w2, self.h2 )
                lx, ly = self.geometry.Trig_2D_Angle_Circle( self.w2, self.h2, self.side, radius, angle )

            # Distance
            event_dist = self.geometry.Trig_2D_Points_Distance( ex, ey, self.w2, self.h2 )
            limit_dist = self.geometry.Trig_2D_Points_Distance( lx, ly, self.w2, self.h2 )
            if event_dist >= limit_dist:
                ex = lx
                ey = ly
        # Return
        return ex, ey

    # Tablet Interaction
    def tabletEvent( self, event ):
        self.pressure = event.pressure()
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Draw Gradient
        if len( self.qpixmap_list ) > 0:
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
            index = int( self.tan_axis * self.tan_range )
            qpixmap = self.qpixmap_list[index]
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

        # Analyse Colors
        if self.analyse != None:
            # Variables
            dot = 5
            line_size = 2
            length = len( self.analyse )

            # Draw
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            for i in range( 0, length ):
                color = self.analyse[i]
                if int( self.tan_axis * 255 ) == int( color[f"uvd_3"] * 255 ):
                    px = self.px + ( 0.5 + color["uvd_1"] * 0.5 ) * self.side
                    py = self.py + ( 0.5 - color["uvd_2"] * 0.5 ) * self.side
                    painter.drawEllipse( int( px - dot ), int( py - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Pinned Colors
        if ( self.color != None and self.pin_list != None ):
            # Variables
            pin_size = 5
            line_size = 2
            length = len( self.pin_list )

            # Draw
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            for i in range( 0, length ):
                if self.pin_list[i]["active"] == True:
                    cx = self.px + ( 0.5 + self.pin_list[i]["uvd_1"] * 0.5 ) * self.side
                    cy = self.py + ( 0.5 - self.pin_list[i]["uvd_2"] * 0.5 ) * self.side
                    painter.drawEllipse( int( cx - pin_size ), int( cy - pin_size ), int( pin_size * 2 ), int( pin_size * 2 ) )

        # Harmony Colors
        if ( self.color != None and self.harmony_list != None ):
            # Variables
            line_size = 2
            dot = 5

            # Parsing
            points = []
            for i in range( 0, len( self.harmony_list ) ):
                har_x = self.px + ( 0.5 + self.harmony_list[i]["uvd_1"] * 0.5 ) * self.side
                har_y = self.py + ( 0.5 - self.harmony_list[i]["uvd_2"] * 0.5 ) * self.side
                points.append( ( har_x, har_y ) )
            length = len( points )

            # Draw Line
            painter.setPen( QPen( self.color_1, line_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            for i in range( 1, length ):
                painter.drawLine( int( points[i-1][0] ), int( points[i-1][1] ), int( points[i][0] ), int( points[i][1] ) )
            if self.harmony_rule in [ "Triadic", "Tetradic" ]:
                painter.drawLine( int( points[0][0] ), int( points[0][1] ), int( points[length-1][0] ), int( points[length-1][1] ) )
            # Draw Points
            painter.setPen( QPen( self.color_2, line_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin ) )
            painter.setBrush( QBrush( self.color_1 ) )
            for i in range( 0, length ):
                painter.drawEllipse( int( points[i][0] - dot ), int( points[i][1] - dot ), int( dot * 2 ), int( dot * 2 ) )

        # Cursor
        size = 10
        zoom_size = 100
        margin_size = 10
        if ( self.press == True and self.zoom == True ):
            size = zoom_size
            Cursor_Zoom( self, painter, size, margin_size )
        elif( self.pressure > self.input_pressure ):
            size = zoom_size * self.pressure
            Cursor_Zoom( self, painter, size, margin_size )
        else:
            Cursor_Normal( self, painter, size )

class Panel_Dot( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )
    SIGNAL_INTERPOLATION = QtCore.pyqtSignal( str )
    SIGNAL_DIMENSION = QtCore.pyqtSignal( int )
    SIGNAL_EDIT = QtCore.pyqtSignal( bool )
    SIGNAL_ZORN = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Panel_Dot, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.press = False
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.press = False
        self.zoom = False
        self.pressure = 0
        self.input_pressure = 0.5

        # Events
        self.ex = 0
        self.ey = 0
        self.dot_x = 0
        self.dot_y = 0

        # Settings
        self.dot_interpolation = "RGB"
        self.dot_dimension = 11
        self.dot_edit = True
        self.dot_matrix = None
        self.unit = 24
        self.margin = 5
        self.shape = "CIRCLE" # SQUARE CIRCLE
        self.Update_Side()
        self.Cursor_Move( self.dot_x, self.dot_y )

        # Context Menu Checks
        self.dot_interpolation = "RGB"
        self.dot_dimension = 11

        # Color
        self.hex_color = QColor( "#000000" )
        self.color_black = QColor( "#000000")
        self.color_white = QColor( "#ffffff")

        # Modules
        self.geometry = Geometry()
        self.convert = None
    def Init_Convert( self, convert ):
        self.convert = convert
        self.update()

    # Relay
    def Set_Size( self, ww, hh ):
        # Widget Size
        self.ww = ww
        self.hh = hh
        self.w2 = int( ww * 0.5 )
        self.h2 = int( hh * 0.5 )
        # Cursor Move
        self.Cursor_Move( self.dot_x, self.dot_y )
        self.resize( ww, hh )
    def Set_Interpolation( self, string ):
        self.dot_interpolation = string
        self.update()
    def Set_Dimension( self, number ):
        self.dot_dimension = number
        self.Update_Side()
        self.update()
    def Set_Edit( self, boolean ):
        self.dot_edit = boolean
        self.update()

    # Update
    def Update_Color( self, dot_matrix ):
        self.dot_matrix = dot_matrix
        self.update()
    def Update_Side( self ):
        self.side = ( self.unit * self.dot_dimension ) + ( self.margin * ( self.dot_dimension - 1 ) )

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Input
        self.origin_x = event.x()
        self.origin_y = event.y()
        self.press = True

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( event )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.press = False
            self.Context_Menu( event )
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass

        self.update()
    def mouseMoveEvent( self, event ):
        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( event )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Position( event )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Position( event )

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass

        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.press = False
        self.zoom = False
        self.pressure = 0
        # Updates
        self.SIGNAL_RELEASE.emit( 0 )
        self.update()

    # Mouse Event
    def Cursor_Move( self, dot_x, dot_y ):
        if self.dot_matrix != None:
            self.ex = int( self.w2 - ( self.side * 0.5 ) + ( self.unit*dot_x + self.margin*( dot_x-1 ) ) + ( self.unit * 0.5 ) )
            self.ey = int( self.h2 - ( self.side * 0.5 ) + ( self.unit*dot_y + self.margin*( dot_y-1 ) ) + ( self.unit * 0.5 ) )
    def Cursor_Position( self, event ):
        # Read
        ex = event.x()
        ey = event.y()

        if self.dot_matrix != None:
            # Points
            points = []
            for y in range( 0, self.dot_dimension ):
                for x in range( 0, self.dot_dimension ):
                    px = int( self.w2 - ( self.side * 0.5 ) + ( self.unit*x + self.margin*( x-1 ) ) + ( self.unit * 0.5 ) )
                    py = int( self.h2 - ( self.side * 0.5 ) + ( self.unit*y + self.margin*( y-1 ) ) + ( self.unit * 0.5 ) )
                    dist = self.geometry.Trig_2D_Points_Distance( px, py, ex, ey )
                    hex_code = self.dot_matrix[y][x]
                    points.append( [dist, px, py, hex_code, x, y] )
            points.sort()

            # Input
            self.ex = points[0][1]
            self.ey = points[0][2]
            # Lock
            self.dot_x = points[0][4]
            self.dot_y = points[0][5]
            # Signal
            hex_code = points[0][3]
            self.Hex_Color( hex_code )
    def Hex_Color( self, hex_code ):
        self.hex_color = QColor( hex_code )
        self.SIGNAL_VALUE.emit( hex_code )
        self.update()

    # Context
    def Context_Menu( self, event ):
        if self.press == False:
            # Menu
            qmenu = QMenu( self )
            # Interpolation
            qmenu_interpolation = qmenu.addMenu( "Interpolation" )
            qmenu_int_rgb = qmenu_interpolation.addAction( "RGB" )
            qmenu_int_cmyk = qmenu_interpolation.addAction( "CMYK" )
            qmenu_int_ryb = qmenu_interpolation.addAction( "RYB" )
            qmenu_int_yuv = qmenu_interpolation.addAction( "YUV" )
            qmenu_int_hsv = qmenu_interpolation.addAction( "HSV" )
            qmenu_int_hsl = qmenu_interpolation.addAction( "HSL" )
            qmenu_int_hcy = qmenu_interpolation.addAction( "HCY" )
            qmenu_int_ard = qmenu_interpolation.addAction( "ARD" )
            qmenu_int_rgb.setCheckable( True )
            qmenu_int_cmyk.setCheckable( True )
            qmenu_int_ryb.setCheckable( True )
            qmenu_int_yuv.setCheckable( True )
            qmenu_int_hsv.setCheckable( True )
            qmenu_int_hsl.setCheckable( True )
            qmenu_int_hcy.setCheckable( True )
            qmenu_int_ard.setCheckable( True )
            qmenu_int_rgb.setChecked( self.dot_interpolation == "RGB" )
            qmenu_int_cmyk.setChecked( self.dot_interpolation == "CMYK" )
            qmenu_int_ryb.setChecked( self.dot_interpolation == "RYB" )
            qmenu_int_yuv.setChecked( self.dot_interpolation == "YUV" )
            qmenu_int_hsv.setChecked( self.dot_interpolation == "HSV" )
            qmenu_int_hsl.setChecked( self.dot_interpolation == "HSL" )
            qmenu_int_hcy.setChecked( self.dot_interpolation == "HCY" )
            qmenu_int_ard.setChecked( self.dot_interpolation == "ARD" )
            # Dimension
            qmenu_dimension = qmenu.addMenu( "Dimension" )
            qmenu_dim_3 = qmenu_dimension.addAction( "3 x 3" )
            qmenu_dim_5 = qmenu_dimension.addAction( "5 x 5" )
            qmenu_dim_7 = qmenu_dimension.addAction( "7 x 7" )
            qmenu_dim_9 = qmenu_dimension.addAction( "9 x 9" )
            qmenu_dim_11 = qmenu_dimension.addAction( "11 x 11" )
            qmenu_dim_13 = qmenu_dimension.addAction( "13 x 13" )
            qmenu_dim_15 = qmenu_dimension.addAction( "15 x 15" )
            qmenu_dim_17 = qmenu_dimension.addAction( "17 x 17" )
            qmenu_dim_19 = qmenu_dimension.addAction( "19 x 19" )
            qmenu_dim_21 = qmenu_dimension.addAction( "21 x 21" )
            qmenu_dim_3.setCheckable( True )
            qmenu_dim_5.setCheckable( True )
            qmenu_dim_7.setCheckable( True )
            qmenu_dim_9.setCheckable( True )
            qmenu_dim_11.setCheckable( True )
            qmenu_dim_13.setCheckable( True )
            qmenu_dim_15.setCheckable( True )
            qmenu_dim_17.setCheckable( True )
            qmenu_dim_19.setCheckable( True )
            qmenu_dim_21.setCheckable( True )
            qmenu_dim_3.setChecked( self.dot_dimension == "3 x 3" )
            qmenu_dim_5.setChecked( self.dot_dimension == "5 x 5" )
            qmenu_dim_7.setChecked( self.dot_dimension == "7 x 7" )
            qmenu_dim_9.setChecked( self.dot_dimension == "9 x 9" )
            qmenu_dim_11.setChecked( self.dot_dimension == "11 x 11" )
            qmenu_dim_13.setChecked( self.dot_dimension == "13 x 13" )
            qmenu_dim_15.setChecked( self.dot_dimension == "15 x 15" )
            qmenu_dim_17.setChecked( self.dot_dimension == "17 x 17" )
            qmenu_dim_19.setChecked( self.dot_dimension == "19 x 19" )
            qmenu_dim_21.setChecked( self.dot_dimension == "21 x 21" )
            # Edit
            qmenu_edit = qmenu.addAction( "Edit" )
            qmenu_edit.setCheckable( True )
            qmenu_edit.setChecked( self.dot_edit )
            # Reset
            qmenu_zorn = qmenu.addAction( "Zorn Palette" )

            # Actions
            action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
            # Triggers
            if action == qmenu_int_rgb:
                self.dot_interpolation = "RGB"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_cmyk:
                self.dot_interpolation = "CMYK"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_ryb:
                self.dot_interpolation = "RYB"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_yuv:
                self.dot_interpolation = "YUV"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_hsv:
                self.dot_interpolation = "HSV"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_hsl:
                self.dot_interpolation = "HSL"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_hcy:
                self.dot_interpolation = "HCY"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_int_ard:
                self.dot_interpolation = "ARD"
                self.SIGNAL_INTERPOLATION.emit( self.dot_interpolation )
            if action == qmenu_dim_3:
                self.dot_dimension = 3
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_5:
                self.dot_dimension = 5
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_7:
                self.dot_dimension = 7
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_9:
                self.dot_dimension = 9
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_11:
                self.dot_dimension = 11
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_13:
                self.dot_dimension = 13
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_15:
                self.dot_dimension = 15
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_17:
                self.dot_dimension = 17
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_19:
                self.dot_dimension = 19
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_dim_21:
                self.dot_dimension = 21
                self.SIGNAL_DIMENSION.emit( self.dot_dimension )
            if action == qmenu_edit:
                self.SIGNAL_EDIT.emit( not self.dot_edit )
            if action == qmenu_zorn:
                self.SIGNAL_ZORN.emit( 0 )

    # Tablet Interaction
    def tabletEvent( self, event ):
        self.pressure = event.pressure()
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Dots
        if self.dot_matrix != None:
            painter.setPen( QtCore.Qt.NoPen )
            for y in range( 0, self.dot_dimension ):
                for x in range( 0, self.dot_dimension ):
                    try:
                        hex6 = self.dot_matrix[y][x]
                    except:
                        hex6 = "#000000"
                    painter.setBrush( QBrush( QColor( hex6 ) ) )
                    point_x = int( self.w2 - ( self.side * 0.5 ) + ( self.unit * x + self.margin * x ) )
                    point_y = int( self.h2 - ( self.side * 0.5 ) + ( self.unit * y + self.margin * y ) )
                    if self.shape == "CIRCLE":
                        painter.drawEllipse( int( point_x ), int( point_y ), int( self.unit ), int( self.unit ) )
                    elif self.shape == "SQUARE":
                        painter.drawRect( int( point_x ), int( point_y ), int( self.unit ), int( self.unit ) )

        # Cursor
        zoom_size = 100
        margin_size = 10
        size = 10
        s2 = int( size * 0.5 )
        if ( self.press == True and self.zoom == True ):
            size = zoom_size
            self.Cursor_Zoom( painter, size, margin_size, s2 )
        elif( self.pressure > self.input_pressure ):
            size = zoom_size * self.pressure
            self.Cursor_Zoom( painter, size, margin_size, s2 )
        else:
            self.Cursor_Normal( painter, size, s2 )
    # Cursor
    def Cursor_Normal( self, painter, size, s2 ):
        # Variables
        w = 2
        # Mask
        mask = QPainterPath()
        mask.addEllipse( 
            int( self.ex - s2 ),
            int( self.ey - s2 ),
            int( size * 2 ),
            int( size * 2 ),
            )
        mask.addEllipse( 
            int( self.ex - s2 + w * 2 ),
            int( self.ey - s2 + w * 2 ),
            int( size * 2 - w * 4 ),
            int( size * 2 - w * 4 ),
            )
        painter.setClipPath( mask )
        # Black Circle
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_black ) )
        painter.drawEllipse( 
            int( self.ex - s2 ),
            int( self.ey - s2 ),
            int( size * 2 ),
            int( size * 2 ),
            )
        # White Circle
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_white ) )
        painter.drawEllipse( 
            int( self.ex - s2 + w ),
            int( self.ey - s2 + w ),
            int( size * 2 - w * 2 ),
            int( size * 2 - w * 2 ),
            )
    def Cursor_Zoom( self, painter, zoom_size, margin_size, s2 ):
        # Border
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_black ) )
        painter.drawEllipse( 
            int( self.ex - zoom_size + s2 ),
            int( self.ey - zoom_size + s2 ),
            int( zoom_size * 2 ),
            int( zoom_size * 2 ),
            )
        # Hex Color
        painter.setBrush( QBrush( self.hex_color ) )
        painter.drawEllipse( 
            int( self.ex - zoom_size + margin_size + s2 ),
            int( self.ey - zoom_size + margin_size + s2 ),
            int( zoom_size * 2 - margin_size * 2 ),
            int( zoom_size * 2 - margin_size * 2 ),
            )

class Panel_Mask( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( str )
    SIGNAL_RELEASE = QtCore.pyqtSignal( int )
    SIGNAL_MASKSET = QtCore.pyqtSignal( str )
    SIGNAL_EDIT = QtCore.pyqtSignal( bool )
    SIGNAL_RESET = QtCore.pyqtSignal( bool )
    SIGNAL_LIVE_OFF = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Panel_Mask, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
            # Widget
        self.press = False
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        self.press = False
        self.zoom = False
        self.pressure = 0
        self.input_pressure = 0.5

        # Events
        self.origin_x = -10
        self.origin_y = -10
        self.ex = -10
        self.ey = -10

        # Mask
        self.mask_edit = True

        # Path
        self.directory = None
        self.file_format = ".png"
        self.files = [
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

        # Masks
        self.mask_path = []
        self.mask_color = {
            "b1" : "#7f7f7f",
            "b2" : "#000000",
            "b3" : "#000000",
            "d1" : "#231402",
            "d2" : "#543713",
            "d3" : "#fe9f0e",
            "d4" : "#ffca32",
            "d5" : "#000000",
            "d6" : "#000000",
            "f1" : "#000000",
            "f2" : "#ffff96",
            "f3" : "#ffffff",
            }
        self.mask_alpha = {
            "b1" : 0.0,
            "b2" : 1.0,
            "b3" : 1.0,
            "d1" : 1.0,
            "d2" : 1.0,
            "d3" : 1.0,
            "d4" : 1.0,
            "d5" : 0.0,
            "d6" : 0.0,
            "f1" : 1.0,
            "f2" : 1.0,
            "f3" : 1.0,
            }
        self.mask_qpixmaps = None

        # Color
        self.hex_color = QColor( "#000000" )

        # Modules
        self.geometry = Geometry()

        # Image
        self.qimage = QImage()

    # Set
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        self.ex = -10
        self.ey = -10
        self.resize( ww, hh )
    def Set_Directory( self, directory ):
        # Variables
        self.directory = directory
        # Update
        self.Update_Path( os.path.join( self.directory, "SPHERE" ) )
        self.update()
    def Set_Edit( self, boolean ):
        self.mask_edit = boolean
        self.update()
    # Update
    def Update_Path( self, mask_set ):
        self.mask_path = []
        for i in range( 0, len( self.files ) ):
            path = os.path.join( str( mask_set ), self.files[i] + self.file_format )
            qpixmap = QPixmap( path )
            if qpixmap.isNull() == False:
                self.mask_path.append( path )
            else:
                self.mask_path.append( None )
        if None not in self.mask_path:
            self.mask_qpixmaps = self.Pixmap_Composite( self.mask_path, self.mask_color, self.mask_alpha )
        else:
            self.mask_qpixmaps = None
        self.update()
    def Update_Color( self, mask_color, mask_alpha ):
        self.mask_color = mask_color
        self.mask_alpha = mask_alpha
        self.mask_qpixmaps = self.Pixmap_Composite( self.mask_path, self.mask_color, self.mask_alpha )
        self.update()

    # Calculations
    def Pixmap_Composite( self, mask_path, mask_color, mask_alpha ):
        # Pre Compose pixmaps to display
        qpixmaps = []
        for i in range( 0, len( mask_path ) ):
            # Color
            color = QColor( self.mask_color[ self.files[i] ] )
            color.setAlphaF( self.mask_alpha[ self.files[i] ] )
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
        # Return
        return qpixmaps

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Input
        ex = event.x()
        ey = event.y()
        self.origin_x = ex
        self.origin_y = ey
        self.press = True
        self.qimage = self.grab().toImage()

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.SIGNAL_LIVE_OFF.emit( 0 )
            self.Cursor_Color( ex, ey, self.qimage )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Color( ex, ey, self.qimage )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.press = False
            self.Context_Menu( event )
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass

        self.update()
    def mouseMoveEvent( self, event ):
        # Input
        ex = event.x()
        ey = event.y()
        self.ex = ex
        self.ey = ey
        self.press = True

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Color( ex, ey, self.qimage )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Color( ex, ey, self.qimage )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Input
        ex = event.x()
        ey = event.y()
        self.ex = ex
        self.ey = ey
        self.press = True

        # LMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.Cursor_Color( ex, ey, self.qimage )
        # LMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.zoom = True
            self.Cursor_Color( ex, ey, self.qimage )
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            pass

        # RMB Neutral
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        # RMB Modifiers
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            pass

        self.update()
    def mouseReleaseEvent( self, event ):
        # Input
        self.ex = event.x()
        self.ey = event.y()

        # Variables
        self.press = False
        self.zoom = False
        self.pressure = 0
        # Updates
        self.SIGNAL_RELEASE.emit( 0 )
        self.update()

    def Cursor_Color( self, ex, ey, qimage ):
        # Pixel Color
        pixel = qimage.pixelColor( ex, ey )
        code = pixel.name()
        self.hex_color = QColor( code )
        # Emit
        self.SIGNAL_VALUE.emit( code )

    # Context
    def Context_Menu( self, event ):
        # Variables
        sub_folder = os.listdir( self.directory )

        # Menu
        if self.press == False:
            # Menu
            qmenu = QMenu( self )

            # Mask Sets
            qmenu_maps = qmenu.addMenu( "Maps" )
            actions = {}
            for i in range( 0, len( sub_folder ) ):
                actions[i] = qmenu_maps.addAction( sub_folder[i] )
            # Edit
            qmenu_edit = qmenu.addAction( "Edit" )
            qmenu_edit.setCheckable( True )
            qmenu_edit.setChecked( self.mask_edit )
            # Reset
            qmenu_reset = qmenu.addAction( "Reset" )

            # Actions
            action = qmenu.exec_( self.mapToGlobal( event.pos() ) )
            # Triggers
            for i in range( 0, len( sub_folder ) ):
                if action == actions[i]:
                    path = os.path.join( self.directory, sub_folder[i] )
                    self.Update_Path( path )
                    self.SIGNAL_MASKSET.emit( path )
                    break
            if action == qmenu_edit:
                self.SIGNAL_EDIT.emit( not self.mask_edit )
            if action == qmenu_reset:
                self.SIGNAL_RESET.emit( True )

    # Tablet Interaction
    def tabletEvent( self, event ):
        self.pressure = event.pressure()
        self.update()

    # Paint
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Background
        painter.setPen( QtCore.Qt.NoPen )
        bw = QLinearGradient( int( 0 ), int( 0 ), int( 0 ), int( self.hh ) )
        bw.setColorAt( 0.000, QColor( 0, 0, 0, 0 ) ) # White
        bw.setColorAt( 1.000, QColor( 0, 0, 0, 50 ) ) # Black
        painter.setBrush( QBrush( bw ) )
        painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( self.hh ) )

        # Draw Pixmaps
        if self.mask_qpixmaps != None:
            for i in range( 0, len( self.mask_qpixmaps ) ):
                qpixmap = self.mask_qpixmaps[i]
                if qpixmap.isNull() == False:
                    render = qpixmap.scaled( self.ww, self.hh, Qt.KeepAspectRatio, Qt.FastTransformation )
                    w = render.width()
                    h = render.height()
                    px = int( self.w2 - w * 0.5 )
                    py = int( self.h2 - h * 0.5 )
                    painter.drawPixmap( int( px ), int( py ), render )

        # Cursor
        size = 10
        zoom_size = 100
        margin_size = 10
        if ( self.press == True and self.zoom == True ):
            size = zoom_size
            Cursor_Zoom( self, painter, size, margin_size )
        elif( self.pressure > self.input_pressure ):
            size = zoom_size * self.pressure
            Cursor_Zoom( self, painter, size, margin_size )
        else:
            Cursor_Normal( self, painter, size )

class Panel_Sample_List( QWidget ):
    SIGNAL_INDEX = QtCore.pyqtSignal( [ int, bool ] )

    # Init
    def __init__( self, parent ):
        super( Panel_Sample_List, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        # Event
        self.ex = 0
        self.ey = 0
        # Colors
        self.color_alpha = QColor( 0, 0, 0, 150 )
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
        # Display
        self.list_qpixmap = None
        self.list_text = None
        # Constants
        self.operation = None
        self.origin = 0
        self.oy = 0
        self.oh = 0
        self.height = 0
        self.margin = 5
        self.thumb = 120 - 2 * self.margin
        # Modules
        self.geometry = Geometry()

    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.Thumb_Center()
        self.resize( ww, hh )
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
        self.update()
    def Set_Display( self, lista ):
        if lista == None:
            self.list_qpixmap = None
            self.list_text = None
        else:
            self.list_qpixmap = []
            self.list_text = []
            for item in lista:
                qpixmap = item["render"].scaledToWidth( int( self.thumb ), Qt.FastTransformation )
                self.height = qpixmap.height() + self.margin
                self.list_qpixmap.append( qpixmap )
                self.list_text.append( item["text"] )
            self.oh = self.height * len( lista )
            self.Thumb_Center()
        self.update()

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()
        self.Cursor_Position( ex, ey )
        # Inputs
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = "index"
            self.Cursor_Index( False )
        if ( event.modifiers() != QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ) or ( event.buttons() == QtCore.Qt.RightButton ):
            self.operation = "move"
            self.origin = ey
            self.Thumb_Move( ex, ey )
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()
        self.Cursor_Position( ex, ey )
        # Inputs
        if self.operation == "index":
            self.Cursor_Index( False )
        if self.operation == "move":
            self.Thumb_Move( ex, ey )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()
        self.Cursor_Position( ex, ey )
        # Input
        self.Cursor_Index( True )
        self.update()
    def mouseReleaseEvent( self, event ):
        self.ex = 0
        self.ey = 0
        self.operation = None
        self.update()

    # Mouse Event
    def Cursor_Position( self, ex, ey ):
        self.ex = self.geometry.Limit_Range( ex, 0, self.ww )
        self.ey = self.geometry.Limit_Range( ey, 0, self.hh )
    def Cursor_Index( self, boolean ):
        if ( self.list_qpixmap != None and self.list_text != None ):
            if ( self.ey >= self.oy and self.ey <= ( self.oy + self.height * len( self.list_qpixmap ) ) ):
                index = int( self.geometry.Limit_Range( int( ( self.ey - self.oy ) / self.height ), 0, len( self.list_qpixmap ) - 1 ) )
                self.SIGNAL_INDEX.emit( index, boolean )

    # Wheel Events
    def wheelEvent( self, event ):
        if self.oh > self.hh:
            # Variables
            num = 0
            factor = 10
            # Read
            delta_y = event.angleDelta().y()
            if delta_y > 20:
                num = -1
            if delta_y < -20:
                num = 1
            # Offset
            if num != 0:
                self.oy += num * factor
                self.oy = self.geometry.Limit_Range( self.oy, ( self.hh - self.oh + self.margin ), 0 )
                self.update()
        else:
            self.Thumb_Center()

    # Thumbnail
    def Thumb_Move( self, ex, ey ):
        factor = 10
        delta = ey - self.origin
        if self.oh > self.hh:
            if delta <= -factor or delta >= factor:
                self.oy = self.geometry.Limit_Range( self.oy + delta, ( self.hh - self.oh + self.margin ), 0 )
                self.origin = ey
        else:
            self.Thumb_Center()
        self.update()
    def Thumb_Center( self ):
        self.oy = ( self.hh * 0.5 ) - ( self.oh * 0.5 )
        self.update()

    # Painter Event
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        family = "Ubuntu Mono"
        size = 12
        # Render
        try:
            if ( self.list_qpixmap != None and self.list_text != None ):
                for i in range( 0, len( self.list_qpixmap ) ):
                    # Parsing
                    qpixmap = self.list_qpixmap[i]
                    text = self.list_text[i]
                    # Image
                    sh = self.height * i + self.oy
                    painter.drawPixmap( int( self.margin ), int( sh ), qpixmap )
                    # Text
                    check_x = ( self.ex >= self.margin ) and ( self.ex <= self.ww - self.margin )
                    check_y = ( self.ey >= sh ) and ( self.ey <= sh + self.height )
                    if ( check_x == True and check_y == True ):
                        # Variables
                        qrect = QRect( int( self.margin ), int( sh ), int( self.thumb ), int( self.height - self.margin ) )
                        # Contrast
                        painter.setPen( QtCore.Qt.NoPen )
                        painter.setBrush( QBrush( QColor( self.color_alpha ) ) )
                        painter.drawRect( qrect )
                        # Text
                        painter.setPen( self.color_1 )
                        painter.setFont( QFont( family, size ) )
                        painter.drawText( qrect, Qt.AlignCenter, text )
        except:
            pass
class Panel_Sample_Image( QWidget ):
    SIGNAL_POSITION = QtCore.pyqtSignal( [ QPoint ] )

    # Init
    def __init__( self, parent ):
        super( Panel_Sample_Image, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, render_height )
    def Variables( self ):
        # Widget
        self.ww = 0
        self.hh = 0
        self.w2 = 0
        self.h2 = 0
        # Event
        self.ex = 0
        self.ey = 0
        # Colors
        self.color_alpha = QColor( 0, 0, 0, 50 )
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
        # Display
        self.qpixmap = None
        self.background = self.color_alpha
        # Interaction
        self.press = False
        self.operation = None
        self.zoom = False
        self.pressure = 0
        self.input_pressure = 0.5
        # Modules
        self.geometry = Geometry()

    # Set
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        self.resize( ww, hh )
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
        self.update()
    def Set_Display( self, qpixmap, cor ):
        self.qpixmap = qpixmap
        if cor == False:
            self.background = self.color_alpha
        else:
            self.background = QColor( 255, 0, 0, 50 )
        self.update()

    # Mouse Interaction
    def mousePressEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # Variables
        self.press = True

        # Operation
        if event.buttons() == QtCore.Qt.LeftButton:
            if event.modifiers() == QtCore.Qt.NoModifier:
                self.operation = "cursor"
                self.Cursor_Position( ex, ey )
            else:
                self.operation = "zoom"
                self.zoom = True
                self.Cursor_Position( ex, ey )
        if event.buttons() == QtCore.Qt.RightButton:
            self.SIGNAL_POSITION.emit( event.pos() )
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()

        # Operation
        if self.operation == "cursor":
            self.Cursor_Position( ex, ey )
        elif self.operation == "zoom":
            self.zoom = True
            self.Cursor_Position( ex, ey )
        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Events
        ex = event.x()
        ey = event.y()

        # Operation
        if self.operation == "cursor":
            self.Cursor_Position( ex, ey )
        elif self.operation == "zoom":
            self.zoom = True
            self.Cursor_Position( ex, ey )
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.press = False
        self.operation = None
        self.zoom = False
        self.pressure = 0
        # Updates
        self.update()

    # Mouse Event
    def Cursor_Position( self, ex, ey ):
        self.ex = self.geometry.Limit_Range( ex, 0, self.ww )
        self.ey = self.geometry.Limit_Range( ey, 0, self.hh )

    # Tablet Interaction
    def tabletEvent( self, event ):
        self.pressure = event.pressure()
        self.update()

    # Painter Event
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Background Hover
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( QColor( self.background ) ) )
        painter.drawRect( 0, 0, self.ww, self.hh )

        # Render
        try:
            if self.qpixmap != None:
                painter.setPen( QtCore.Qt.NoPen )
                painter.setBrush( QtCore.Qt.NoBrush )
                if self.qpixmap.isNull() == False:
                    # Image
                    render = self.qpixmap.scaled( int( self.ww ), int( self.hh ), Qt.KeepAspectRatio, Qt.FastTransformation )
                    rw = render.width()
                    rh = render.height()
                    px = int( ( self.ww * 0.5 ) - ( rw * 0.5 ) )
                    py = int( ( self.hh * 0.5 ) - ( rh * 0.5 ) )
                    painter.drawPixmap( int( px ), int( py ), render )

                    # Zoom Cursor
                    size = 10
                    ms1 = 10
                    ms2 = 2 * ms1
                    image = False
                    if ( self.press == True and self.zoom == True ):
                        image = True
                        p = 1
                    elif( self.pressure > self.input_pressure ):
                        image = True
                        p = self.pressure
                    if image == True:
                        # Variables
                        zs1 = 100 * p
                        zs2 = 2 * zs1

                        # Border
                        painter.setPen( QtCore.Qt.NoPen )
                        painter.setBrush( QBrush( QColor( "#000000" ) ) )
                        painter.drawEllipse( 
                            int( self.ex - zs1 ),
                            int( self.ey - zs1 ),
                            int( zs2 ),
                            int( zs2 ),
                            )

                        # Variables
                        dd = - zs1 + ms1
                        cx = self.ex + dd
                        cy = self.ey + dd
                        cs = zs2 - ms2
                        # Factor
                        fx = self.qpixmap.width() / rw
                        fy = self.qpixmap.height() / rh
                        # Zoom Position
                        zx = ( self.ex - px ) * fx + dd
                        zy = ( self.ey - py ) * fy + dd
                        # Zoom Image
                        zoom = self.qpixmap.copy( int( zx ), int( zy ), int( cs ), int( cs ) )
                        zw = zoom.width()
                        zh = zoom.height()
                        # Out of Bounds
                        if ( zw > cs or zh > cs ):
                            zoom = QPixmap( int( zs1 ), int( zs1 ) )
                            zoom.fill( Qt.transparent )
                        # Offset
                        ox = 0
                        oy = 0
                        if ( zw < cs and self.ex < self.w2 ):
                            ox = cs - zw
                        if ( zh < cs and self.ey < self.h2 ):
                            oy = cs - zh
                        # Mask
                        circle = QPainterPath()
                        circle.addEllipse( int( cx ), int( cy ), int( cs ), int( cs ) )
                        painter.setClipPath( circle, Qt.ReplaceClip )
                        # Render
                        painter.drawPixmap( int( cx + ox ), int( cy + oy ), zoom )
        except:
            pass

#endregion
#region Channels

class Channel_Slider( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( dict )
    SIGNAL_RELEASE = QtCore.pyqtSignal( bool )
    SIGNAL_STOPS = QtCore.pyqtSignal( int )
    SIGNAL_TEXT = QtCore.pyqtSignal( str )

    # Init
    def __init__( self, parent ):
        super( Channel_Slider, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    def Variables( self ):
        # Modules
        self.geometry = Geometry()
        # Widget
        self.ww = 1
        self.hh = 1
        # Display
        self.origin_x = 0
        self.origin_stops = 0
        # Variables
        self.mode = "LINEAR" # "LINEAR" "CIRCULAR" "MIXER"
        self.minimum = 0
        self.half = 0.5
        self.maximum = 1
        self.stops = 1
        self.value = 0
        self.colors = None
        self.alpha = 1
        self.index = None
        # Colors
        self.color_black = QColor( "#000000")
        self.color_white = QColor( "#ffffff")
        self.color_alpha = QColor( 0, 0, 0, 50 )
        self.color_1 = QColor( "#191919" )
        self.color_2 = QColor( "#e5e5e5" )

    # Relay
    def Set_Mode( self, mode ):
        self.mode = mode
        self.update()
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.resize( ww, hh )
    def Set_Limits( self, minimum, half, maximum ):
        self.minimum = minimum
        self.half = half
        self.maximum = maximum
        self.update()
    def Set_Colors( self, colors, alpha ):
        self.colors = colors
        self.alpha = alpha
        self.update()
    def Set_Stops( self, stops ):
        self.stops = stops
        self.update()
    def Set_Value( self, value ):
        self.value = value * self.ww
        self.update()
    def Set_Index( self, index ):
        self.index = index
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
        self.update()

    # Interaction
    def mousePressEvent( self, event ):
        # Start Event
        self.origin_x = event.x()
        self.origin_stops = self.stops
        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Emit_Value_Linear( event )
        # LMB Modifier
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ):
            pass
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Snap_Stop( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier ):
            self.Stops_Shift( event )

        self.update()
    def mouseMoveEvent( self, event ):
        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Emit_Value_Linear( event )
        # LMB Modifier
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ):
            pass
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Snap_Stop( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier ):
            self.Stops_Shift( event )

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Emit_Value_Linear( event )
        # LMB Modifier
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ):
            pass
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Snap_Half( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier ):
            self.Stops_Reset()

        self.update()
    def mouseReleaseEvent( self, event ):
        # Update
        self.SIGNAL_TEXT.emit( "" )
        self.SIGNAL_RELEASE.emit( True )
        self.update()

    # Functions
    def Mouse_Position( self, event ):
        # Event read
        pos_x = event.pos().x()
        # Calculations
        if ( self.mode == "LINEAR" or self.mode == "MIXER" ):
            value = self.geometry.Limit_Range( pos_x, 0, self.ww )
        if self.mode == "CIRCULAR":
            value = self.Loop_Hue( pos_x, self.ww )
        return value
    def Loop_Hue( self, value, limit ):
        if value < 0:
            delta = value - limit
            units = abs( int( delta / limit ) )
            value = value + ( limit*units )
        if value > limit:
            units = abs( int( value / limit ) )
            value = value - ( limit*units )
        return value

    # Value
    def Emit_Value_Linear( self, event ):
        # Mouse
        self.value = self.Mouse_Position( event )
        # Calculations
        percent = self.value / self.ww
        text = str( round( percent*100,2 ) ) + " %"
        # Emission
        self.SIGNAL_VALUE.emit( { "index":self.index, "value":percent } )
        self.SIGNAL_TEXT.emit( text )

    # Snap
    def Snap_Half( self, event ):
        self.value = self.half * self.ww
        self.SIGNAL_VALUE.emit( { "index":self.index, "value":self.half } )
        self.SIGNAL_TEXT.emit( "50 %" )
    def Snap_Stop( self, event ):
        # Mouse
        value = self.Mouse_Position( event )
        # Calculations
        unit = self.ww / self.stops
        distances = []
        for i in range( 0, self.stops+1 ):
            dist = self.geometry.Trig_2D_Points_Distance( value, 0, ( unit * i ), 0 )
            distances.append( dist )
        value_min = min( distances )
        index = distances.index( value_min )
        self.value = unit * index
        percent = self.value / self.ww
        text = str( round( percent*100,2 ) ) + " %"
        # Emission
        self.SIGNAL_VALUE.emit( { "index":self.index, "value":percent } )
        self.SIGNAL_TEXT.emit( text )
    # Stops
    def Stops_Shift( self, event ):
        # Variables
        minimum = 2
        divisions = 100
        unit = 50
        # Calculations
        delta = event.x() - self.origin_x
        value = int( delta / unit )
        self.stops = self.geometry.Limit_Range( self.origin_stops + value, minimum, divisions )
        # Emission
        self.SIGNAL_STOPS.emit( self.stops )
        self.SIGNAL_TEXT.emit( "snap " + str( self.stops ) )
    def Stops_Reset( self ):
        # Set Number
        if self.mode == "LINEAR":
            self.stops = 4
        if self.mode == "CIRCULAR":
            self.stops = 6
        if self.mode == "MIXER":
            self.stops = 2
        # Emission
        self.SIGNAL_STOPS.emit( self.stops )

    # Wheel Events
    def wheelEvent( self, event ):
        delta_y = event.angleDelta().y()
        if delta_y > 20:
            num = 1
        if delta_y < -20:
            num = -1
        # Calculate
        if ( self.mode == "LINEAR" or self.mode == "MIXER" ):
            self.value = self.geometry.Limit_Range( self.value + num, 0, self.ww )
        if self.mode == "CIRCULAR":
            self.value = self.Loop_Hue( self.value + num, self.ww )
        percent = self.value / self.ww
        text = str( round( percent*100,2 ) ) + " %"
        # Emit
        self.SIGNAL_VALUE.emit( { "index":self.index, "value":percent } )
        self.SIGNAL_TEXT.emit( text )
        self.update()

    # Paint Style
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        ww = self.ww
        hh = self.hh
        w1 = ww - 1
        w2 = ww - 2
        h1 = hh - 1
        h4 = hh - 4

        # Background Style
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_alpha ) )
        painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( self.hh ) )

        # Stops
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_1 ) )
        if self.stops <= 0 :
            painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( 1 ) )
        else:
            for i in range( 0, self.stops ):
                percent = self.ww * ( i / self.stops )
                painter.drawRect( int( percent ), int( 0 ), int( 1 ), int( 1 ) )
            painter.drawRect( int( self.ww * 1 - 1 ), int( 0 ), int( 1 ), int( 1 ) )

        # Draw Colors Gradient
        if self.colors != None:
            try:
                painter.setPen( QtCore.Qt.NoPen )
                grad = QLinearGradient( int( 0 ), int( 0 ), int( self.ww ), int( 0 ) )

                number = len( self.colors )
                for i in range( 0, number ):
                    grad.setColorAt( round( i / number, 3 ), QColor( int( self.colors[i][0] * 255 ), int( self.colors[i][1] * 255 ), int( self.colors[i][2] * 255 ), int( self.alpha * 255 ) ) )

                painter.setBrush( QBrush( grad ) )
                square = QPolygon( [
                    QPoint( int( 1 ),  int( 1 ) ),
                    QPoint( int( w1 ), int( 1 ) ),
                    QPoint( int( w1 ), int( h1 ) ),
                    QPoint( int( 1 ),  int( h1 ) ),
                    ] )
                painter.drawPolygon( square )
            except Exception as e:
                QtCore.qDebug( f"error = { e }" )

        # Cursor
        value = int( self.value )
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
        painter.setBrush( QBrush( self.color_black ) )
        black = QPolygon( [
            QPoint( int( bl ), int( top1 ) ),
            QPoint( int( bl ), int( bot1 ) ),
            QPoint( int( br ), int( bot1 ) ),
            QPoint( int( br ), int( top1 ) ),
            ] )
        painter.drawPolygon( black )
        # White Square
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_white ) )
        white = QPolygon( [
            QPoint( int( wl ), int( top2 ) ),
            QPoint( int( wl ), int( bot2 ) ),
            QPoint( int( wr ), int( bot2 ) ),
            QPoint( int( wr ), int( top2 ) ),
            ] )
        painter.drawPolygon( white )

class Channel_Selection( QWidget ):
    SIGNAL_VALUE = QtCore.pyqtSignal( dict )
    SIGNAL_RELEASE = QtCore.pyqtSignal( bool )
    SIGNAL_RESET = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Channel_Selection, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( render_width, 100 )
    def Variables( self ):
        # Modules
        self.geometry = Geometry()
        # Widget
        self.ww = 1
        self.hh = 1

        # Variables
        self.mode = "LINEAR" # "LINEAR" "CIRCULAR"
        self.value = 0
        self.colors = None
        self.alpha = 1
        self.sele = None
        self.sele_origin = None
        self.marker = None

        # Colors
        self.color_black = QColor( "#000000")
        self.color_white = QColor( "#ffffff")
        self.color_alpha = QColor( 0, 0, 0, 50 )
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )

    # Relay
    def Set_Mode( self, mode ):
        self.mode = mode
        self.update()
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.resize( ww, hh )

    # Update
    def Update_Value( self, value ):
        self.value = value
        self.update()
    def Update_Colors( self, colors, alpha ):
        self.colors = colors
        self.alpha = alpha
        self.update()
    def Update_Selection( self, sele ):
        self.sele = sele
        self.update()

    # Interaction
    def mousePressEvent( self, event ):
        # Event
        ex = event.x()

        # Variables
        self.sele_origin = self.sele

        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.marker = self.Marker_Index( ex, "ALL" )
            self.Cursor_Position( ex )
        # LMB Modifier
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ):
            self.marker = self.Marker_Index( ex, "1" )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.marker = self.Marker_Index( ex, "0" )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier ):
            pass

        # Reset
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) ):
            self.Cursor_Reset()

        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()

        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Cursor_Position( ex )
        # LMB Modifier
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ):
            self.Cursor_Position( ex )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Cursor_Position( ex )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier ):
            pass

        # Reset
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) ):
            self.Cursor_Reset()

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # Event
        ex = event.x()

        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Cursor_Position( ex )
        # LMB Modifier
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ShiftModifier ):
            self.Cursor_Position( ex )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.ControlModifier ):
            self.Cursor_Position( ex )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.AltModifier ):
            pass

        # Reset
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) ):
            self.Cursor_Reset()

        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.marker = None
        # Update
        self.SIGNAL_RELEASE.emit( True )
        self.update()
    # Cursor
    def Cursor_Position( self, ex ):
        if ( self.mode != None ):
            # Interaction
            limit = 20
            if self.marker[0] <= limit:
                # Variables
                index = self.marker[1]
                ww = self.ww
                vv = self.value * ww
                # Markers Normal
                l0 = vv - self.sele_origin["l0"] * ww
                l1 = vv - self.sele_origin["l1"] * ww
                r1 = vv + self.sele_origin["r1"] * ww
                r0 = vv + self.sele_origin["r0"] * ww
                # Markers Negative
                n_l0 = vv - self.sele_origin["l0"] * ww + ww
                n_l1 = vv - self.sele_origin["l1"] * ww + ww
                n_r1 = vv + self.sele_origin["r1"] * ww - ww
                n_r0 = vv + self.sele_origin["r0"] * ww - ww

                # Calculations
                if index == "l0":
                    delta = ex - l0
                    value = l0 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, n_r0, l1  )
                    else:
                        value = self.geometry.Limit_Range( value, 0, l1  )
                    percentage = ( vv - value ) / self.ww
                    self.sele["l0"] = percentage
                if index == "l1":
                    delta = ex - l1
                    value = l1 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, l0, vv  )
                    else:
                        value = self.geometry.Limit_Range( value, l0, vv  )
                    percentage = ( vv - value ) / self.ww
                    self.sele["l1"] = percentage
                if index == "r1":
                    delta = ex - r1
                    value = r1 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, vv, r0  )
                    else:
                        value = self.geometry.Limit_Range( value, vv, r0  )
                    percentage = ( value - vv ) / self.ww
                    self.sele["r1"] = percentage
                if index == "r0":
                    delta = ex - r0
                    value = r0 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, r1, n_l0  )
                    else:
                        value = self.geometry.Limit_Range( value, r1, ww  )
                    percentage = ( value - vv ) / self.ww
                    self.sele["r0"] = percentage

                if index == "n_l0":
                    delta = ex - l0
                    value = l0 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, n_r0, l1  ) - ww
                    else:
                        value = self.geometry.Limit_Range( value, 0, l1  ) - ww
                    percentage = ( vv - value - ww ) / self.ww
                    self.sele["l0"] = percentage
                if index == "n_l1":
                    delta = ex - l1
                    value = l1 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, l0, vv  ) - ww
                    else:
                        value = self.geometry.Limit_Range( value, l0, vv  ) - ww
                    percentage = ( vv - value - ww ) / self.ww
                    self.sele["l1"] = percentage
                if index == "n_r1":
                    delta = ex - r1
                    value = r1 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, vv, r0  ) + ww
                    else:
                        value = self.geometry.Limit_Range( value, vv, r0  ) + ww
                    percentage = ( value - vv - ww ) / self.ww
                    self.sele["r1"] = percentage
                if index == "n_r0":
                    delta = ex - r0
                    value = r0 + delta
                    if self.mode == "CIRCULAR":
                        value = self.geometry.Limit_Range( value, r1, n_l0  ) + ww
                    else:
                        value = self.geometry.Limit_Range( value, r1, ww  ) + ww
                    percentage = ( value - vv - ww ) / self.ww
                    self.sele["r0"] = percentage

                self.SIGNAL_VALUE.emit( self.sele )
                self.update()
    def Cursor_Reset( self ):
        if self.mode != None:
            self.SIGNAL_RESET.emit( 0 )
    # Marker
    def Marker_Index( self, ex, mode ):
        # Markers Normal
        ww = self.ww
        vv = self.value * ww
        l0 = vv - self.sele["l0"] * ww
        l1 = vv - self.sele["l1"] * ww
        r1 = vv + self.sele["r1"] * ww
        r0 = vv + self.sele["r0"] * ww
        # Markers Negative
        n_l0 = vv - self.sele["l0"] * ww + ww
        n_l1 = vv - self.sele["l1"] * ww + ww
        n_r1 = vv + self.sele["r1"] * ww - ww
        n_r0 = vv + self.sele["r0"] * ww - ww
        # Distance
        d_ml0 = abs( ex - l0 )
        d_ml1 = abs( ex - l1 )
        d_mr1 = abs( ex - r1 )
        d_mr0 = abs( ex - r0 )
        d_n_ml0 = abs( ex - n_l0 )
        d_n_ml1 = abs( ex - n_l1 )
        d_n_mr1 = abs( ex - n_r1 )
        d_n_mr0 = abs( ex - n_r0 )
        # Index
        if mode == "ALL":
            distance = [ ( d_n_ml0, "n_l0" ), ( d_n_ml1, "n_l1" ), ( d_ml0, "l0" ), ( d_ml1, "l1" ), ( d_mr1, "r1" ), ( d_mr0, "r0" ), ( d_n_mr1, "n_r1" ), ( d_n_mr0, "n_r0" ) ]
        elif mode == "1":
            distance = [ ( d_n_ml1, "n_l1" ), ( d_ml1, "l1" ), ( d_mr1, "r1" ), ( d_n_mr1, "n_r1" ) ]
        elif mode == "0":
            distance = [ ( d_n_ml0, "n_l0" ), ( d_ml0, "l0" ), ( d_mr0, "r0" ), ( d_n_mr0, "n_r0" ) ]
        distance.sort()
        marker = distance[0]
        # Return
        return marker

    # Paint Style
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Variables
        ww = self.ww
        hh = self.hh
        w1 = ww - 1
        w2 = ww - 2
        h1 = hh - 1
        h4 = hh - 4
        h5 = hh - 5
        h6 = hh - 6

        # Slider
        if ( self.value != None and self.sele != None ):
            # Variables 1
            vv = self.value * self.ww
            l0 = vv - self.sele["l0"] * self.ww
            l1 = vv - self.sele["l1"] * self.ww
            r1 = vv + self.sele["r1"] * self.ww
            r0 = vv + self.sele["r0"] * self.ww
            # Variables 2
            l0i = l0 + 1
            l1i = l1 + 1
            r1i = r1 - 1
            r0i = r0 - 1

            # Background Style
            painter.setPen( QtCore.Qt.NoPen )

            painter.setBrush( QBrush( self.color_alpha ) )
            painter.drawRect( int( 0 ), int( h5 ), int( self.ww ), int( 5 ) )

            # Markers Range
            left_full = QPolygon( [
                QPoint( int( vv ),  int( 1 )  ),
                QPoint( int( vv ),  int( 2 )  ),
                QPoint( int( l1i ), int( 2 )  ),
                QPoint( int( l1i ), int( h6 ) ),
                QPoint( int( vv ),  int( h6 ) ),
                QPoint( int( vv ),  int( h5 ) ),
                QPoint( int( l1 ),  int( h5 ) ),
                QPoint( int( l1 ),  int( 1 )  ),
                ] )
            right_full = QPolygon( [
                QPoint( int( vv ),  int( 1 )  ),
                QPoint( int( vv ),  int( 2 )  ),
                QPoint( int( r1i ), int( 2 )  ),
                QPoint( int( r1i ), int( h6 ) ),
                QPoint( int( vv ),  int( h6 ) ),
                QPoint( int( vv ),  int( h5 ) ),
                QPoint( int( r1 ),  int( h5 ) ),
                QPoint( int( r1 ),  int( 1 )  ),
                ] )
            left_tri = QPolygon( [
                QPoint( int( l1 ), int( 1 )  ),
                QPoint( int( l1 ), int( h5 ) ),
                QPoint( int( l0 ), int( h5 ) ),
                QPoint( int( l0 ), int( 1 )  ),
                ] )
            right_tri = QPolygon( [
                QPoint( int( r1 ), int( 1 )  ),
                QPoint( int( r1 ), int( h5 ) ),
                QPoint( int( r0 ), int( h5 ) ),
                QPoint( int( r0 ), int( 1 )  ),
                ] )
            left_cap = QPolygon( [
                QPoint( int( l0 ),  int( 1 )  ),
                QPoint( int( l0 ),  int( h5 ) ),
                QPoint( int( l0i ), int( h5 ) ),
                QPoint( int( l0i ), int( 1 )  ),
                ] )
            right_cap = QPolygon( [
                QPoint( int( r0 ),  int( 1 )  ),
                QPoint( int( r0 ),  int( h5 ) ),
                QPoint( int( r0i ), int( h5 ) ),
                QPoint( int( r0i ), int( 1 )  ),
                ] )

            painter.setPen( QtCore.Qt.NoPen )

            painter.setBrush( QBrush( QColor( self.color_1 ) ) )
            painter.drawPolygon( left_full )
            painter.drawPolygon( right_full )

            painter.setBrush( QBrush( QColor( self.color_1 ), Qt.BDiagPattern ) )
            painter.drawPolygon( left_tri )
            painter.setBrush( QBrush( QColor( self.color_1 ), Qt.FDiagPattern ) )
            painter.drawPolygon( right_tri )

            painter.setBrush( QBrush( QColor( self.color_1 ) ) )
            painter.drawPolygon( left_cap )
            painter.setBrush( QBrush( QColor( self.color_1 ) ) )
            painter.drawPolygon( right_cap )


            if self.mode == "CIRCULAR":
                # Polygons
                neg_left_full = QPolygon( [
                    QPoint( int( vv - ww ),  int( 1 )  ),
                    QPoint( int( vv - ww ),  int( 2 )  ),
                    QPoint( int( r1i - ww ), int( 2 )  ),
                    QPoint( int( r1i - ww ), int( h6 ) ),
                    QPoint( int( vv - ww ),  int( h6 ) ),
                    QPoint( int( vv - ww ),  int( h5 ) ),
                    QPoint( int( r1 - ww ),  int( h5 ) ),
                    QPoint( int( r1 - ww ),  int( 1 )  ),
                    ] )
                neg_right_full = QPolygon( [
                    QPoint( int( vv + ww ),  int( 1 )  ),
                    QPoint( int( vv + ww ),  int( 2 )  ),
                    QPoint( int( l1i + ww ), int( 2 )  ),
                    QPoint( int( l1i + ww ), int( h6 ) ),
                    QPoint( int( vv + ww ),  int( h6 ) ),
                    QPoint( int( vv + ww ),  int( h5 ) ),
                    QPoint( int( l1 + ww ),  int( h5 ) ),
                    QPoint( int( l1 + ww ),  int( 1 )  ),
                    ] )
                neg_left_tri = QPolygon( [
                    QPoint( int( r1 - ww ), int( 1 )  ),
                    QPoint( int( r1 - ww ), int( h5 ) ),
                    QPoint( int( r0 - ww ), int( h5 ) ),
                    QPoint( int( r0 - ww ), int( 1 )  ),
                    ] )
                neg_right_tri = QPolygon( [
                    QPoint( int( l1 + ww ), int( 1 )  ),
                    QPoint( int( l1 + ww ), int( h5 ) ),
                    QPoint( int( l0 + ww ), int( h5 ) ),
                    QPoint( int( l0 + ww ), int( 1 )  ),
                    ] )
                neg_left_cap = QPolygon( [
                    QPoint( int( r0 - ww ),  int( 1 )  ),
                    QPoint( int( r0 - ww ),  int( h5 ) ),
                    QPoint( int( r0i - ww ), int( h5 ) ),
                    QPoint( int( r0i - ww ), int( 1 )  ),
                    ] )
                neg_right_cap = QPolygon( [
                    QPoint( int( l0 + ww ),  int( 1 )  ),
                    QPoint( int( l0 + ww ),  int( h5 ) ),
                    QPoint( int( l0i + ww ), int( h5 ) ),
                    QPoint( int( l0i + ww ), int( 1 )  ),
                    ] )

                # Draw
                painter.setPen( QtCore.Qt.NoPen )

                painter.setBrush( QBrush( QColor( self.color_1 ) ) )
                painter.drawPolygon( neg_left_full )
                painter.drawPolygon( neg_right_full )

                painter.setBrush( QBrush( QColor( self.color_1 ), Qt.FDiagPattern ) )
                painter.drawPolygon( neg_left_tri )
                painter.setBrush( QBrush( QColor( self.color_1 ), Qt.BDiagPattern ) )
                painter.drawPolygon( neg_right_tri )

                painter.setBrush( QBrush( QColor( self.color_1 ) ) )
                painter.drawPolygon( neg_left_cap )
                painter.setBrush( QBrush( QColor( self.color_1 ) ) )
                painter.drawPolygon( neg_right_cap )

        # Draw Colors Gradient
        if self.colors != None:
            painter.setPen( QtCore.Qt.NoPen )
            grad = QLinearGradient( int( 0 ), int( 0 ), int( self.ww ), int( 0 ) )
            number = len( self.colors )
            for i in range( 0, number ):
                grad.setColorAt( round( i / number, 3 ), QColor( int( self.colors[i][0] * 255 ), int( self.colors[i][1] * 255 ), int( self.colors[i][2] * 255 ), int( self.alpha * 255 ) ) )
            painter.setBrush( QBrush( grad ) )
            square = QPolygon( [
                QPoint( int( 1 ),  int( h4 ) ),
                QPoint( int( w1 ), int( h4 ) ),
                QPoint( int( w1 ), int( h1 ) ),
                QPoint( int( 1 ),  int( h1 ) ),
                ] )
            painter.drawPolygon( square )

        # Cursor
        if self.value != None:
            vv = int( self.value * self.ww )
            bl = vv - 3
            br = vv + 3
            wl = vv - 1
            wr = vv + 1
            top1 = 0
            bot1 = self.hh
            top2 = 1
            bot2 = self.hh - 1
            # Black Square
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( self.color_black ) )
            black = QPolygon( [
                QPoint( int( bl ), int( top1 ) ),
                QPoint( int( bl ), int( bot1 ) ),
                QPoint( int( br ), int( bot1 ) ),
                QPoint( int( br ), int( top1 ) ),
                ] )
            painter.drawPolygon( black )
            # White Square
            painter.setPen( QtCore.Qt.NoPen )
            painter.setBrush( QBrush( self.color_white ) )
            white = QPolygon( [
                QPoint( int( wl ), int( top2 ) ),
                QPoint( int( wl ), int( bot2 ) ),
                QPoint( int( wr ), int( bot2 ) ),
                QPoint( int( wr ), int( top2 ) ),
                ] )
            painter.drawPolygon( white )

#endregion
#region Pin

class Pin_Color( QWidget ):
    SIGNAL_APPLY = QtCore.pyqtSignal( int )
    SIGNAL_SAVE = QtCore.pyqtSignal( int )
    SIGNAL_CLEAN = QtCore.pyqtSignal( int )
    SIGNAL_ALPHA = QtCore.pyqtSignal( float )
    SIGNAL_TEXT = QtCore.pyqtSignal( str )

    # Init
    def __init__( self, parent ):
        super( Pin_Color, self ).__init__( parent )
        self.Variables()
    def sizeHint( self ):
        return QtCore.QSize( 500, 500 )
    def Variables( self ):
        # Widget
        self.ww = 1
        self.hh = 1

        # Events
        self.ex = 0
        self.ey = 0

        # States
        self.press = False
        self.active = False
        self.index = None

        # Color
        self.color = None  # None == no color
        self.alpha = None  # None == no alpha
        self.color_1 = QColor( "#191919" )
        self.color_2 = QColor( "#e5e5e5" )
        self.color_alpha = QColor( 0, 0, 0, 50 )

        # Modifier Keys
        self.mod_1 = [ QtCore.Qt.ShiftModifier, QtCore.Qt.ControlModifier, QtCore.Qt.AltModifier ]
        self.mod_3 = ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier )

        # Modules
        self.geometry = Geometry()

    # Relay
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.resize( ww, hh )
    def Set_Index( self, index ):
        self.index = index
    def Set_Active( self, active ):
        self.active = active
        self.update()
    def Set_Color( self, color ):
        self.color = QColor( color )
        self.update()
    def Set_Clean( self ):
        self.color = None
        self.update()
    def Set_Alpha( self, alpha ):
        self.alpha = alpha
        self.update()

    # Interaction
    def mousePressEvent( self, event ):
        # Variables
        self.press = True

        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.press = "operation"
            self.Swipe_String( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() in self.mod_1 ):
            self.press = "alpha"
            self.Swipe_Alpha( event )
        # RMB Neutral
        if ( event.buttons() == QtCore.Qt.RightButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.press = False
            self.Context_Menu( event )

        # Clean
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == self.mod_3 ):
            self.press = True
            self.SIGNAL_CLEAN.emit( self.index )

        self.update()
    def mouseMoveEvent( self, event ):
        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Swipe_String( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() in self.mod_1 ):
            self.Swipe_Alpha( event )
        # RMB Neutral
        if ( event.buttons() == QtCore.Qt.RightButton and event.modifiers() == QtCore.Qt.NoModifier ):
            pass

        # Clean
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == self.mod_3 ):
            pass

        self.update()
    def mouseDoubleClickEvent( self, event ):
        # LMB Neutral
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == QtCore.Qt.NoModifier ):
            self.Swipe_String( event )
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() in self.mod_1 ):
            self.Swipe_Alpha( event )
        # RMB Neutral
        if ( event.buttons() == QtCore.Qt.RightButton and event.modifiers() == QtCore.Qt.NoModifier ):
            pass

        # Clean
        if ( event.buttons() == QtCore.Qt.LeftButton and event.modifiers() == self.mod_3 ):
            pass

        self.update()
    def mouseReleaseEvent( self, event ):
        # Input
        self.Swipe_Operation( event )
        self.press = False
        # Update
        self.update()

    # Swipe Operations
    def Swipe_String( self, event ):
        if self.press == "operation":
            # Input
            ex = event.x()
            ey = event.y()
            # Signals
            if ( ( ex >= 0 and ex <= self.ww ) and ey <= 0 ):
                self.SIGNAL_TEXT.emit( "APPLY" )
            elif ( ( ex >= 0 and ex <= self.ww ) and ey >= self.hh ):
                self.SIGNAL_TEXT.emit( "SAVE" )
            else:
                self.SIGNAL_TEXT.emit( "" )
    def Swipe_Operation( self, event ):
        if self.press == "operation":
            # Input
            ex = event.x()
            ey = event.y()
            # Signals
            if ( ( ex >= 0 and ex <= self.ww ) and ey <= 0 ):
                self.SIGNAL_APPLY.emit( self.index )
            elif ( ( ex >= 0 and ex <= self.ww ) and ey >= self.hh ):
                self.SIGNAL_SAVE.emit( self.index )
            self.SIGNAL_TEXT.emit( "" )
    def Swipe_Alpha( self, event ):
        if ( self.press == "alpha" and self.alpha != None ):
            # Input
            ex = event.x()
            ex = self.geometry.Limit_Range( ex, 0, self.ww )
            # Signals
            if self.ww != 0:
                self.alpha = ex / self.ww
                self.SIGNAL_ALPHA.emit( self.alpha )
            self.update()
    # Context
    def Context_Menu( self, event ):
        if self.press == False:
            # Menu
            qmenu = QMenu( self )
            # Actions
            qmenu_apply = qmenu.addAction( "APPLY" )
            qmenu_save = qmenu.addAction( "SAVE" )
            qmenu_clean = qmenu.addAction( "CLEAN" )
            action = qmenu.exec_( self.mapToGlobal( QPoint( 10,5 ) ) )
            # Triggers
            if action == qmenu_apply:
                self.SIGNAL_APPLY.emit( self.index )
            if action == qmenu_save:
                self.SIGNAL_SAVE.emit( self.index )
            if action == qmenu_clean:
                self.SIGNAL_CLEAN.emit( self.index )

    # Paint Style
    def paintEvent( self, event ):
        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Background
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( self.color_alpha ) )
        painter.drawRect( int( 0 ), int( 0 ), int( self.ww ), int( self.hh ) )

        # Active
        if self.active == True:
            # Dot
            w1 = 1
            w3 = self.ww-2
            # Color
            h2 = 2
            h4 = self.hh-3
        else:
            # Dot
            w1 = 0
            w3 = 1
            # Color
            h2 = 1
            h4 = self.hh-2
        if self.alpha == None:
            a1 = 0
        else:
            a1 = 2
        # Dot
        painter.setPen( QtCore.Qt.NoPen )
        painter.setBrush( QBrush( QColor( self.color_1 ) ) )
        painter.drawRect( int( w1 ), int( 0 ), int( w3 ), int( 1 ) )

        # Color
        painter.setPen( QtCore.Qt.NoPen )
        if self.color != None:
            qcolor = self.color
            if self.alpha != None:
                qcolor.setAlphaF( self.alpha )
            painter.setBrush( QBrush( qcolor ) )
            painter.drawRect( QRect( int( 1 ), int( h2 ), int( self.ww - 2 ), int( h4 - a1 ) ) )

        # Alpha
        if self.alpha != None:
            painter.setPen( QtCore.Qt.NoPen )
            # Background
            painter.setBrush( QBrush( self.color_1 ) )
            painter.drawRect( QRect( int( 1 ), int( self.hh - a1 ), int( self.ww - 2 ), int( a1 ) ) )
            # Slider
            painter.setBrush( QBrush( self.color_2 ) )
            painter.drawRect( QRect( int( 1 ), int( self.hh - a1 ), int( ( self.ww * self.alpha ) - 2 ), int( a1 ) ) )

#endregion
