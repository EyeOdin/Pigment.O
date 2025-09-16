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

# Krita
from krita import *
# PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui, uic

#endregion


#region Panels

class Display_Map( QWidget ):
    SIGNAL_INSERT = QtCore.pyqtSignal( int )
    SIGNAL_CLEAN = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Display_Map, self ).__init__( parent )
        self.Variables()
    def Variables( self ):
        # Widget
        self.ww = 1
        self.hh = 1
        self.w2 = 0.5
        self.h2 = 0.5

        # Event
        self.ox = 0
        self.oy = 0
        self.ex = 0
        self.ey = 0

        # State
        self.state_press = False
        self.operation = None

        # Display
        self.qpixmap_display = None
        self.scale_method = Qt.FastTransformation

        # Interaction
        self.operation = None
        # Camera
        self.pcmx = 0
        self.pcmy = 0
        self.pcz = 1
        self.cmx = 0 # Moxe X
        self.cmy = 0 # Move Y
        self.cz = 1 # Zoom
        self.display = False
        self.background = False # Background Color

        # Colors
        self.color_1 = QColor( "#ffffff" )
        self.color_2 = QColor( "#000000" )
        self.color_alpha = QColor( 0, 0, 0, 50 )
        self.color_clip = QColor( 0, 0, 0, 100 )
        self.color_red = QColor( 84, 43, 43 )
    def sizeHint( self ):
        return QtCore.QSize( 5000,5000 )

    # Relay
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        self.resize( ww, hh )
    def Set_Display( self, qpixmap ):
        self.qpixmap_display = qpixmap
        self.update()
    def Set_Background( self, background ):
        self.background = background
        self.update()

    # Draw
    def Draw_Render( self, qpixmap ):
        # QPixmap
        if self.display == False:
            draw = qpixmap.scaled( int( self.ww * self.cz ), int( self.hh * self.cz ), Qt.KeepAspectRatio, self.scale_method )
        else:
            ww = qpixmap.width()
            hh = qpixmap.height()
            draw = qpixmap.scaled( int( ww * self.cz ), int( hh * self.cz ), Qt.KeepAspectRatio, self.scale_method )
        self.bw = draw.width()
        self.bh = draw.height()
        # Variables
        self.bl = self.w2 - ( self.bw * 0.5 ) + ( self.cmx * self.cz )
        self.bt = self.h2 - ( self.bh * 0.5 ) + ( self.cmy * self.cz )
        self.br = self.bl + self.bw
        self.bb = self.bt + self.bh
        # Return
        return draw

    # Camera
    def Camera_Reset( self ):
        self.cmx = 0
        self.cmy = 0
        self.cz = 1
    def Camera_Previous( self ):
        self.pcmx = self.cmx
        self.pcmy = self.cmy
        self.pcz = self.cz
    def Camera_Move( self, ex, ey ):
        if self.cz != 0:
            self.cmx = self.pcmx + ( ( ex - self.ox ) / self.cz )
            self.cmy = self.pcmy + ( ( ey - self.oy ) / self.cz )
    def Camera_Scale( self, ex, ey ):
        factor = 200
        self.cz = self.Limit_Range( self.pcz - ( ( ey - self.oy ) / factor ), 0, 100 )
    def Limit_Range( self, value, minimum, maximum ):
        if value <= minimum:
            value = minimum
        if value >= maximum:
            value = maximum
        return value

    # Context Menu
    def Context_Menu( self, event ):
        #region Menu

        # Menu
        qmenu = QMenu( self )

        # General
        action_mask = qmenu.addAction( "Insert" )
        action_clean = qmenu.addAction( "Clean" )

        #endregion
        #region Action

        # Mapping
        action = qmenu.exec_( self.mapToGlobal( event.pos() ) )

        # General
        if action == action_mask:
            self.SIGNAL_INSERT.emit( 0 )
        if action == action_clean:
            self.SIGNAL_CLEAN.emit( 0 )

        #endregion

    # Mouse Events
    def mousePressEvent( self, event ):
        # Variable
        self.state_press = True

        # Event
        ex = event.x()
        ey = event.y()
        self.ox = ex
        self.oy = ey
        self.ex = ex
        self.ey = ey

        # LMB
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = None
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = "camera_move"
            self.Camera_Previous()
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = None
            self.Camera_Reset()
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = None

        # MMB
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.MiddleButton ):
            self.operation = "camera_move"
            self.Camera_Previous()

        # RMB
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.operation = None
            self.Context_Menu( event )
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.operation = "camera_scale"
            self.Camera_Previous()
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.operation = None
            self.Camera_Reset()
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.RightButton ):
            self.operation = None

        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()
        self.ex = ex
        self.ey = ey

        # Camera
        if self.operation == "camera_move":
            self.Camera_Move( ex, ey )
        if self.operation == "camera_scale":
            self.Camera_Scale( ex, ey )

        # Update
        self.update()
    def mouseDoubleClickEvent( self, event ):
        pass
    def mouseReleaseEvent( self, event ):
        # Variables
        self.state_press = False
        self.operation = None
        # Update
        self.update()
    # Wheel Event
    def wheelEvent( self, event ):
        delta_y = event.angleDelta().y()
        angle = 5
        if delta_y >= angle:
            pass
        if delta_y <= -angle:
            pass

    # Widget
    def enterEvent( self, event ):
        pass
    def leaveEvent( self, event ):
        pass
    # Painter
    def paintEvent( self, event ):
        # Variables
        ww = self.ww
        hh = self.hh
        w2 = self.w2
        h2 = self.h2
        if ww < hh: side = ww
        else:       side = hh

        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Background Hover
        painter.setPen( QtCore.Qt.NoPen )
        if self.background == True:
            painter.setBrush( QBrush( self.color_red ) )
        else:
            painter.setBrush( QBrush( self.color_alpha ) )
        painter.drawRect( 0, 0, ww, hh )

        # Mask
        painter.setClipRect( QRect( int( 0 ), int( 0 ), int( ww ), int( hh ) ), Qt.ReplaceClip )

        # Render Image
        qpixmap = self.qpixmap_display
        render = True
        if qpixmap in [ None, False, True ]:
            render = False
        if render == True:
            # Draw Pixmap
            draw = self.Draw_Render( qpixmap )
            painter.drawPixmap( int( self.bl ), int( self.bt ), draw )

class Channel_Select( QWidget ):
    SIGNAL_INDEX = QtCore.pyqtSignal( int )

    # Init
    def __init__( self, parent ):
        super( Channel_Select, self ).__init__( parent )
        self.Variables()
    def Variables( self ):
        # Widget
        self.ww = 1
        self.hh = 1
        self.w2 = 0.5
        self.h2 = 0.5
        self.start_x = 0

        # Event
        self.ex = 0
        self.ey = 0

        # Channels
        self.channel_number = 5
        self.channel_index = 0
        self.channel_maps = []

        # State
        self.state_press = False
        self.operation = None

        #Button
        self.bw = 20
        self.bh = 10
        self.bi = 6
        self.bb = self.bw + self.bi

        # Colors
        self.color_1 = QColor( "#ffffff" )
        self.color_2 = QColor( "#000000" )
        self.color_neutral = QColor( 127, 127, 127 )
        self.color_alpha = QColor( 0, 0, 0, 20 )
        self.color_clip = QColor( 0, 0, 0, 100 )

        # Icons
        self.margin = 5
        self.total_width = 0
        self.item_width = 0
    def sizeHint( self ):
        return QtCore.QSize( 5000, 100 )

    # Relay
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
    def Set_Size( self, ww, hh ):
        self.ww = ww
        self.hh = hh
        self.w2 = ww * 0.5
        self.h2 = hh * 0.5
        self.Start_Pixel()
        self.resize( ww, hh )
    def Set_ChannelNumber( self, channel_number ):
        self.channel_number = channel_number
        self.update()
    def Set_Display( self, channel_maps ):
        # Variables
        self.channel_maps = channel_maps
        # Sizes
        if self.channel_maps != None:
            self.total_width = 0
            for item in channel_maps:
                width = item["width"]
                self.total_width += width
            self.total_width += self.margin * ( len( channel_maps ) - 1 )
            self.item_width = width
            self.Start_Pixel()
        # Update
        self.update()

    # Calculate
    def Start_Pixel( self ):
        self.start_x = int( self.w2 - ( self.total_width * 0.5 ) )

    # Mouse Events
    def mousePressEvent( self, event ):
        # Variable
        self.state_press = True

        # Event
        ex = event.x()
        ey = event.y()
        self.ex = ex
        self.ey = ey

        # LMB
        if ( event.modifiers() == QtCore.Qt.NoModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = "channel_select"
            self.Channel_Select( ex, ey )
        if ( event.modifiers() == QtCore.Qt.ShiftModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = None
        if ( event.modifiers() == QtCore.Qt.ControlModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = None
        if ( event.modifiers() == QtCore.Qt.AltModifier and event.buttons() == QtCore.Qt.LeftButton ):
            self.operation = None

        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()
        self.ex = ex
        self.ey = ey

        # Operations
        if self.operation == "channel_select":
            self.Channel_Select( ex, ey )

        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Variables
        self.state_press = False
        self.operation = None
        # Update
        self.update()
    # Wheel Event
    def wheelEvent( self, event ):
        delta_y = event.angleDelta().y()
        angle = 5
        if delta_y >= angle:
            self.Channel_Wheel( +1 )
        if delta_y <= -angle:
            self.Channel_Wheel( -1 )

    # Operation
    def Channel_Select( self, ex, ey ):
        if self.channel_maps != None:
            for i in range( 0, len( self.channel_maps ) ):
                px = self.start_x + ( self.item_width * i ) + ( self.margin * i )
                pw = px + self.item_width
                if ( ( ex >= px ) and ( ex <= pw ) ):
                    self.channel_index = i
                    self.Channel_Signal( self.channel_index )
                    break
        self.update()
    def Channel_Wheel( self, value ):
        # Variables
        index = self.channel_index + value
        if index <= 0:
            index = 0
        if index >= self.channel_number - 1:
            index = self.channel_number - 1
        # Send
        self.channel_index = int( index )
        self.Channel_Signal( self.channel_index )
        self.update()
    def Channel_Signal( self, index ):
        self.SIGNAL_INDEX.emit( index )


    # Widget
    def enterEvent( self, event ):
        pass
    def leaveEvent( self, event ):
        pass
    # Painter
    def paintEvent( self, event ):
        # Variables
        ww = self.ww
        hh = self.hh
        w2 = self.w2
        h2 = self.h2
        sw = w2 - ( self.bw * 0.5 )
        sh = h2 - ( self.bh * 0.5 )
        
        # Values
        fw = self.channel_number * self.bb
        start = w2 - ( fw * 0.5 )

        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        painter.setBrush( QBrush( self.color_alpha ) )
        painter.setPen( QtCore.Qt.NoPen )
        painter.drawRect( int( 0 ), int( 0 ), int( ww ), int( hh ) )

        # Paint Images
        if self.channel_maps != None:
            for i in range( 0, len( self.channel_maps ) ):
                # Variables
                item = self.channel_maps[i]
                qpixmap = item["render"]
                width = item["width"]
                height = item["height"]
                text = item["text"]
                # Calculation
                px = self.start_x + ( width * i ) + ( self.margin * i )
                py = self.h2 - height * 0.5
                # Pixmaps
                render = True
                if qpixmap in [ None, False, True ]:
                    render = False
                if render == True:
                    painter.drawPixmap( int( px ), int( py ), qpixmap )
                # Text
                if ( i == self.channel_index and self.state_press == True ):
                    # Variables
                    cor = self.color_2
                    cor.setAlpha( 200 )

                    # Bounding Box
                    box = QRect( int( px ), int( py ), int( width ), int( height ) )
                    # Highlight
                    painter.setPen( QtCore.Qt.NoPen )
                    painter.setBrush( QBrush( cor ) )
                    painter.drawRect( box )
                    # String
                    painter.setBrush( QtCore.Qt.NoBrush )
                    painter.setPen( QPen( self.color_1, 1, Qt.SolidLine ) )
                    qfont = QFont( "Consolas", 10 )
                    painter.setFont( qfont )
                    painter.drawText( box, Qt.AlignCenter, text )

class Channel_Slider( QWidget ):
    SIGNAL_PA = QtCore.pyqtSignal( float )
    SIGNAL_PB = QtCore.pyqtSignal( float )
    SIGNAL_PC = QtCore.pyqtSignal( float )
    SIGNAL_PD = QtCore.pyqtSignal( float )

    # Init
    def __init__( self, parent ):
        super( Channel_Slider, self ).__init__( parent )
        self.Variables()
    def Variables( self ):
        # Widget
        self.ww = 1
        self.hh = 1
        self.w2 = 0.5
        self.h2 = 0.5

        # Original
        self.ex_oa = 0.3
        self.ex_ob = 0.4
        self.ex_oc = 0.6
        self.ex_od = 0.7
        # Event
        self.ex_pa = 0.3
        self.ex_pb = 0.4
        self.ex_pc = 0.6
        self.ex_pd = 0.7
        self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
        self.delta_cd_n = abs( self.ex_pd - self.ex_pc )

        # State
        self.slider_mode = "LINEAR"  # "LINEAR" "CIRCULAR"
        self.slider_cor = None
        self.slider_order = "ABCD" # "ABCD" "BCDA" "CDAB" "DABC"
        self.state_press = False
        self.node = None

        # Colors
        self.color_1 = QColor( "#ffffff" )
        self.color_2 = QColor( "#000000" )
        self.color_neutral = QColor( 127, 127, 127 )
        self.color_alpha = QColor( 0, 0, 0, 50 )
        self.color_clip = QColor( 0, 0, 0, 100 )
        # Display
        self.gradient = None
    def sizeHint( self ):
        return QtCore.QSize( 5000, 50 )

    # Relay
    def Set_Theme( self, color_1, color_2 ):
        self.color_1 = color_1
        self.color_2 = color_2
    def Set_Size( self, ww, hh ):
        self.ww = int( ww )
        self.hh = int( hh )
        self.h2 = int( hh * 0.5 )
        self.resize( ww, hh )
    def Set_Gradient( self, gradient ):
        self.gradient = gradient
        self.update()
    def Set_Mode( self, slider_mode ):
        self.slider_mode = slider_mode
        self.update()
    def Set_Cor( self, slider_cor ):
        self.slider_cor = slider_cor
        self.update()

    # Geometry
    def Limit_Range( self, value, minimum, maximum ):
        if value <= minimum:
            value = minimum
        if value >= maximum:
            value = maximum
        return value
    def Limit_Cycle( self, value, minimum, maximum ):
        delta = abs( maximum - minimum )
        if value < minimum:
            value += delta
        if value > maximum:
            value -= delta
        return value

    # Mouse Events
    def mousePressEvent( self, event ):
        # Variable
        self.state_press = True
        # Event
        ex = event.x()
        ey = event.y()
        # LMB
        self.node = self.Channel_Node( ex, ey )
        # Reset
        if ( event.modifiers() == ( QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier ) and event.buttons() == QtCore.Qt.LeftButton ):
            self.Channel_Reset()
        # Update
        self.update()
    def mouseMoveEvent( self, event ):
        # Event
        ex = event.x()
        ey = event.y()
        # Operations
        self.Channel_Move( ex, ey )
        # Update
        self.update()
    def mouseReleaseEvent( self, event ):
        # Channel Fix
        self.Channel_Cycle()
        # Variables
        self.state_press = False
        self.node = None
        # Update
        self.update()

    # Operation
    def Channel_Reset( self ):
        # Variables
        self.ex_pa = 0.3
        self.ex_pb = 0.4
        self.ex_pc = 0.6
        self.ex_pd = 0.7
        self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
        self.delta_cd_n = abs( self.ex_pd - self.ex_pc )
        # Signals
        self.SIGNAL_PA.emit( self.ex_pa )
        self.SIGNAL_PB.emit( self.ex_pb )
        self.SIGNAL_PC.emit( self.ex_pc )
        self.SIGNAL_PD.emit( self.ex_pd )
    def Channel_Node( self, ex, ey ):
        # Variable
        node = None
        dist = 20

        # Distance
        k_pa = int( self.ex_pa * self.ww )
        k_pb = int( self.ex_pb * self.ww )
        k_pc = int( self.ex_pc * self.ww )
        k_pd = int( self.ex_pd * self.ww )

        d_pa_n = abs( k_pa - ex )
        d_pb_n = abs( k_pb - ex )
        d_pc_n = abs( k_pc - ex )
        d_pd_n = abs( k_pd - ex )

        d_pa_l = abs( ( k_pa - self.ww ) - ex )
        d_pb_l = abs( ( k_pb - self.ww ) - ex )
        d_pc_l = abs( ( k_pc - self.ww ) - ex )
        d_pd_l = abs( ( k_pd - self.ww ) - ex )

        d_pa_r = abs( ( k_pa + self.ww ) - ex )
        d_pb_r = abs( ( k_pb + self.ww ) - ex )
        d_pc_r = abs( ( k_pc + self.ww ) - ex )
        d_pd_r = abs( ( k_pd + self.ww ) - ex )

        min_pa = min( d_pa_n, d_pa_l, d_pa_r )
        min_pb = min( d_pb_n, d_pb_l, d_pb_r )
        min_pc = min( d_pc_n, d_pc_l, d_pc_r )
        min_pd = min( d_pd_n, d_pd_l, d_pd_r )

        # Controller
        if ey <= self.h2: # TOP SIDE
            if self.slider_order in [ "ABCD", "BCDA", "DABC" ]: # BC order
                if   ( min_pb <= dist and ( min_pb < min_pc or ex < k_pb ) ): node = "ex_pb"
                elif ( min_pc <= dist and ( min_pc < min_pb or ex > k_pc ) ): node = "ex_pc"
            else: # CB order
                if   ( min_pb <= dist and ( min_pb < min_pc or ex > k_pb ) ): node = "ex_pb"
                elif ( min_pc <= dist and ( min_pc < min_pb or ex < k_pc ) ): node = "ex_pc"
        else: # BOTTOM SIDE
            if self.slider_order == "ABCD": # AD order
                if   ( min_pa <= dist and ( min_pa < min_pd or ex < k_pa ) ): node = "ex_pa"
                elif ( min_pd <= dist and ( min_pd < min_pa or ex > k_pd ) ): node = "ex_pd"
            else: # DA order
                if   ( min_pa <= dist and ( min_pa < min_pd or ex > k_pa ) ): node = "ex_pa"
                elif ( min_pd <= dist and ( min_pd < min_pa or ex < k_pd ) ): node = "ex_pd"

        return node
    def Channel_Move( self, ex, ey ):
        # Variables
        value = ex / self.ww
        # Interaction
        if self.slider_mode == "LINEAR":
            if self.node == "ex_pa":
                self.ex_pa = value
                self.ex_pa = self.Limit_Range( self.ex_pa, 0, self.ex_pb )
            elif self.node == "ex_pb":
                self.ex_pa = value - self.delta_ab_n
                self.ex_pb = value
                self.ex_pa = self.Limit_Range( self.ex_pa, 0, self.ex_pc )
                self.ex_pb = self.Limit_Range( self.ex_pb, 0, self.ex_pc )
            elif self.node == "ex_pc":
                self.ex_pc = value
                self.ex_pd = value + self.delta_cd_n
                self.ex_pc = self.Limit_Range( self.ex_pc, self.ex_pb, 1 )
                self.ex_pd = self.Limit_Range( self.ex_pd, self.ex_pb, 1 )
            elif self.node == "ex_pd":
                self.ex_pd = value
                self.ex_pd = self.Limit_Range( self.ex_pd, self.ex_pc, 1 )
            # Deltas
            self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
            self.delta_cd_n = abs( self.ex_pd - self.ex_pc )
        if self.slider_mode == "CIRCULAR":
            # Neutral
            ex_pa_n = self.ex_pa
            ex_pb_n = self.ex_pb
            ex_pc_n = self.ex_pc
            ex_pd_n = self.ex_pd
            # Left
            ex_pa_l = ex_pa_n - 1
            ex_pb_l = ex_pb_n - 1
            ex_pc_l = ex_pc_n - 1
            ex_pd_l = ex_pd_n - 1
            # Right
            ex_pa_r = ex_pa_n + 1
            ex_pb_r = ex_pb_n + 1
            ex_pc_r = ex_pc_n + 1
            ex_pd_r = ex_pd_n + 1

            # Movement Limits
            if self.slider_order == "ABCD":
                if   self.node == "ex_pa":
                    self.ex_pa = value
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_l, ex_pb_n )
                elif self.node == "ex_pb":
                    self.ex_pb = value
                    self.ex_pa = value - self.delta_ab_n
                    self.ex_pb = self.Limit_Range( self.ex_pb, ex_pd_l, ex_pc_n )
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_l, ex_pc_n )
                elif self.node == "ex_pc":
                    self.ex_pc = value
                    self.ex_pd = value + self.delta_cd_n
                    self.ex_pc = self.Limit_Range( self.ex_pc, ex_pb_n, ex_pa_r )
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pb_n, ex_pa_r )
                elif self.node == "ex_pd":
                    self.ex_pd = value
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pc_n, ex_pa_r )
                self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
                self.delta_cd_n = abs( self.ex_pd - self.ex_pc )
            if self.slider_order == "BCDA":
                if   self.node == "ex_pa":
                    self.ex_pa = value
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_n, ex_pb_r )
                elif self.node == "ex_pb":
                    self.ex_pb = value
                    self.ex_pa = value + self.delta_ab_n
                    self.ex_pb = self.Limit_Range( self.ex_pb, ex_pd_l, ex_pc_n )
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_n, ex_pc_r )
                elif self.node == "ex_pc":
                    self.ex_pc = value
                    self.ex_pd = value + self.delta_cd_n
                    self.ex_pc = self.Limit_Range( self.ex_pc, ex_pb_n, ex_pa_n )
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pb_n, ex_pa_n )
                elif self.node == "ex_pd":
                    self.ex_pd = value
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pc_n, ex_pa_n )
                self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
                self.delta_cd_n = abs( self.ex_pd - self.ex_pc )
            if self.slider_order == "CDAB":
                if   self.node == "ex_pa":
                    self.ex_pa = value
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_n, ex_pb_n )
                elif self.node == "ex_pb":
                    self.ex_pb = value
                    self.ex_pa = value - self.delta_ab_n
                    self.ex_pb = self.Limit_Range( self.ex_pb, ex_pd_n, ex_pc_r )
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_n, ex_pc_r )
                elif self.node == "ex_pc":
                    self.ex_pc = value
                    self.ex_pd = value + self.delta_cd_n
                    self.ex_pc = self.Limit_Range( self.ex_pc, ex_pb_l, ex_pa_n )
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pb_l, ex_pa_n )
                elif self.node == "ex_pd":
                    self.ex_pd = value
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pc_n, ex_pa_n )
                self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
                self.delta_cd_n = abs( self.ex_pd - self.ex_pc )
            if self.slider_order == "DABC":
                if   self.node == "ex_pa":
                    self.ex_pa = value
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_n, ex_pb_n )
                elif self.node == "ex_pb":
                    self.ex_pb = value
                    self.ex_pa = value - self.delta_ab_n
                    self.ex_pb = self.Limit_Range( self.ex_pb, ex_pd_n, ex_pc_n )
                    self.ex_pa = self.Limit_Range( self.ex_pa, ex_pd_n, ex_pc_n )
                elif self.node == "ex_pc":
                    self.ex_pc = value
                    self.ex_pd = value - self.delta_cd_n
                    self.ex_pc = self.Limit_Range( self.ex_pc, ex_pb_n, ex_pa_r )
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pb_l, ex_pa_n )
                elif self.node == "ex_pd":
                    self.ex_pd = value
                    self.ex_pd = self.Limit_Range( self.ex_pd, ex_pc_l, ex_pa_n )
                self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
                self.delta_cd_n = abs( self.ex_pd - self.ex_pc )

        # Emit
        self.SIGNAL_PA.emit( self.ex_pa )
        self.SIGNAL_PB.emit( self.ex_pb )
        self.SIGNAL_PC.emit( self.ex_pc )
        self.SIGNAL_PD.emit( self.ex_pd )
    def Channel_Cycle( self ):
        # Position
        self.ex_pa = self.Limit_Cycle( self.ex_pa, 0, 1 )
        self.ex_pb = self.Limit_Cycle( self.ex_pb, 0, 1 )
        self.ex_pc = self.Limit_Cycle( self.ex_pc, 0, 1 )
        self.ex_pd = self.Limit_Cycle( self.ex_pd, 0, 1 )
        self.delta_ab_n = abs( self.ex_pa - self.ex_pb )
        self.delta_cd_n = abs( self.ex_pd - self.ex_pc )

        # Point Order
        self.slider_order = self.Slider_Order()

        # Emit
        self.SIGNAL_PA.emit( self.ex_pa )
        self.SIGNAL_PB.emit( self.ex_pb )
        self.SIGNAL_PC.emit( self.ex_pc )
        self.SIGNAL_PD.emit( self.ex_pd )
    def Slider_Order( self ):
        # Neutral
        ex_pa_n = round( self.ex_pa, 6 )
        ex_pb_n = round( self.ex_pb, 6 )
        ex_pc_n = round( self.ex_pc, 6 )
        ex_pd_n = round( self.ex_pd, 6 )
        # Left
        ex_pa_l = round( ex_pa_n - 1.0, 6 )
        ex_pb_l = round( ex_pb_n - 1.0, 6 )
        ex_pc_l = round( ex_pc_n - 1.0, 6 )
        ex_pd_l = round( ex_pd_n - 1.0, 6 )
        # Right
        ex_pa_r = round( ex_pa_n + 1.0, 6 )
        ex_pb_r = round( ex_pb_n + 1.0, 6 )
        ex_pc_r = round( ex_pc_n + 1.0, 6 )
        ex_pd_r = round( ex_pd_n + 1.0, 6 )

        # Sorting
        l = [ ( ex_pa_n, "A" ), ( ex_pb_n, "B" ), ( ex_pc_n, "C" ), ( ex_pd_n, "D" ) ]
        l.sort()
        so = l[0][1] + l[1][1] + l[2][1] + l[3][1]
        # Fix Sort Errors
        if so not in [ "ABCD", "BCDA", "CDAB", "DABC" ]:
            # Variables
            ca = ex_pa_n in [ ex_pb_l,ex_pc_l,ex_pd_l, ex_pb_n,ex_pc_n,ex_pd_n, ex_pb_r,ex_pc_r,ex_pd_r ]
            cb = ex_pb_n in [ ex_pa_l,ex_pc_l,ex_pd_l, ex_pa_n,ex_pc_n,ex_pd_n, ex_pa_r,ex_pc_r,ex_pd_r ]
            cc = ex_pc_n in [ ex_pa_l,ex_pb_l,ex_pd_l, ex_pa_n,ex_pb_n,ex_pd_n, ex_pa_r,ex_pb_r,ex_pd_r ]
            cd = ex_pd_n in [ ex_pa_l,ex_pb_l,ex_pc_l, ex_pa_n,ex_pb_n,ex_pc_n, ex_pa_r,ex_pb_r,ex_pc_r ]

            # 4 letters ( reset )
            if   ( ca == cb == cc == cd == True ):
                so = "ABCD"
            # 3 letters
            elif ( ca == False ):
                if so[0] == "A": so = "ABCD"
                if so[1] == "A": so = "DABC"
                if so[2] == "A": so = "CDAB"
                if so[3] == "A": so = "BCDA"
            elif ( cb == False ):
                if so[0] == "B": so = "BCDA"
                if so[1] == "B": so = "ABCD"
                if so[2] == "B": so = "DABC"
                if so[3] == "B": so = "CDAB"
            elif ( cc == False ):
                if so[0] == "C": so = "CDAB"
                if so[1] == "C": so = "BCDA"
                if so[2] == "C": so = "ABCD"
                if so[3] == "C": so = "DABC"
            elif ( cd == False ):
                if so[0] == "D": so = "DABC"
                if so[1] == "D": so = "CDAB"
                if so[2] == "D": so = "BCDA"
                if so[3] == "D": so = "ABCD"
        return so

    # Widget
    def enterEvent( self, event ):
        pass
    def leaveEvent( self, event ):
        pass
    # Painter
    def paintEvent( self, event ):
        # Variables
        ww = self.ww
        hh = self.hh
        h2 = self.h2
        d = 3
        h2t = h2 - d
        h2b = h2 + d
        delta = 4
        k = 255
        line_size = 2
        # Points
        px = int( 0 )
        py = int( 8 )
        dw = int( self.ww )
        dh = int( 4 )

        # Markers Neutral
        ex_pa_n = int( self.ex_pa * ww )
        ex_pb_n = int( self.ex_pb * ww )
        ex_pc_n = int( self.ex_pc * ww )
        ex_pd_n = int( self.ex_pd * ww )
        check_full = ex_pa_n == ex_pb_n == ex_pc_n == ex_pd_n
        if self.slider_mode == "CIRCULAR":
            # Markers Left
            ex_pa_l = int( ex_pa_n - ww )
            ex_pb_l = int( ex_pb_n - ww )
            ex_pc_l = int( ex_pc_n - ww )
            ex_pd_l = int( ex_pd_n - ww )
            # Markers Right
            ex_pa_r = int( ex_pa_n + ww )
            ex_pb_r = int( ex_pb_n + ww )
            ex_pc_r = int( ex_pc_n + ww )
            ex_pd_r = int( ex_pd_n + ww )

        # Painter
        painter = QPainter( self )
        painter.setRenderHint( QtGui.QPainter.Antialiasing, True )

        # Channels
        if self.gradient != None:
            painter.setPen( QPen( self.color_1, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )

            # Lines
            if self.slider_mode == "LINEAR":
                painter.drawLine( ex_pa_n, h2b, ex_pb_n, h2b )
                painter.drawLine( ex_pb_n, h2t, ex_pc_n, h2t )
                painter.drawLine( ex_pc_n, h2b, ex_pd_n, h2b )
            if self.slider_mode == "CIRCULAR":
                if self.slider_order == "ABCD":
                    if check_full == True:
                        painter.drawLine( 0, h2t, ww, h2t )
                        painter.drawLine( 0, h2b, ww, h2b )
                    else:
                        painter.drawLine( ex_pb_l, h2t, ex_pc_l, h2t )
                        painter.drawLine( ex_pc_l, h2b, ex_pd_l, h2b )

                        painter.drawLine( ex_pa_n, h2b, ex_pb_n, h2b )
                        painter.drawLine( ex_pb_n, h2t, ex_pc_n, h2t )
                        painter.drawLine( ex_pc_n, h2b, ex_pd_n, h2b )

                        painter.drawLine( ex_pa_r, h2b, ex_pb_r, h2b )
                        painter.drawLine( ex_pb_r, h2t, ex_pc_r, h2t )
                if self.slider_order == "BCDA":
                    painter.drawLine( ex_pa_l, h2b, ex_pb_n, h2b )
                    painter.drawLine( ex_pb_n, h2t, ex_pc_n, h2t )
                    painter.drawLine( ex_pc_n, h2b, ex_pd_n, h2b )

                    painter.drawLine( ex_pa_n, h2b, ex_pb_r, h2b )
                    painter.drawLine( ex_pb_r, h2t, ex_pc_r, h2t )
                if self.slider_order == "CDAB":
                    painter.drawLine( ex_pa_l, h2b, ex_pb_l, h2b )
                    painter.drawLine( ex_pb_l, h2t, ex_pc_n, h2t )
                    painter.drawLine( ex_pc_n, h2b, ex_pd_n, h2b )

                    painter.drawLine( ex_pa_n, h2b, ex_pb_n, h2b )
                    painter.drawLine( ex_pb_n, h2t, ex_pc_r, h2t )
                    painter.drawLine( ex_pc_r, h2b, ex_pd_r, h2b )
                if self.slider_order == "DABC":
                    painter.drawLine( ex_pb_l, h2t, ex_pc_l, h2t )
                    painter.drawLine( ex_pc_l, h2b, ex_pd_n, h2b )

                    painter.drawLine( ex_pa_n, h2b, ex_pb_n, h2b )
                    painter.drawLine( ex_pb_n, h2t, ex_pc_n, h2t )
                    painter.drawLine( ex_pc_n, h2b, ex_pd_r, h2b )

                    painter.drawLine( ex_pa_r, h2b, ex_pb_r, h2b )
                    painter.drawLine( ex_pb_r, h2t, ex_pc_r, h2t )

            # Mark
            painter.setPen( QPen( self.color_1, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
            painter.setBrush( QtCore.Qt.NoBrush )
            # Markers Neutral
            painter.drawLine( ex_pa_n, h2, ex_pa_n, hh )
            painter.drawLine( ex_pb_n, 0,  ex_pb_n, h2 )
            painter.drawLine( ex_pc_n, 0,  ex_pc_n, h2 )
            painter.drawLine( ex_pd_n, h2, ex_pd_n, hh )
            if self.slider_mode == "CIRCULAR":
                # Markers Left
                painter.drawLine( ex_pa_l, h2, ex_pa_l, hh )
                painter.drawLine( ex_pb_l, 0,  ex_pb_l, h2 )
                painter.drawLine( ex_pc_l, 0,  ex_pc_l, h2 )
                painter.drawLine( ex_pd_l, h2, ex_pd_l, hh )
                # Markers Right
                painter.drawLine( ex_pa_r, h2, ex_pa_r, hh )
                painter.drawLine( ex_pb_r, 0,  ex_pb_r, h2 )
                painter.drawLine( ex_pc_r, 0,  ex_pc_r, h2 )
                painter.drawLine( ex_pd_r, h2, ex_pd_r, hh )
            
            # Gradient
            grad = QLinearGradient( px, py, dw, dh )
            num = len( self.gradient )
            for i in range( 0, num ):
                loc = round( i / ( num - 1 ), 3 )
                r = int( self.gradient[i][0] * k )
                g = int( self.gradient[i][1] * k )
                b = int( self.gradient[i][2] * k )
                color = QColor( r, g, b, k )
                grad.setColorAt( loc, color )
            painter.setBrush( QBrush( grad ) )
            painter.setPen( QtCore.Qt.NoPen )
            square = QPolygon( [
                QPoint( int( px ),  int( py ) ),
                QPoint( int( dw ), int( py ) ),
                QPoint( int( dw ), int( py+dh ) ),
                QPoint( int( px ),  int( py+dh ) ),
                ] )
            painter.drawPolygon( square )

            # Marker for Color
            if self.slider_cor != None:
                sc = self.slider_cor * ww
                painter.setPen( QPen( self.color_1, line_size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin ) )
                painter.setBrush( QtCore.Qt.NoBrush )
                painter.drawLine( int( sc ), int( 0 ), int( sc ), int( hh ) )

#endregion
