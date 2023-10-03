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


#region Import Modules #############################################################
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, uic
from PyQt5.Qt import Qt

#endregion
#region Global Variables ###########################################################
EXTENSION_ID = 'pykrita_pigment_o_extension'

#endregion


class Pigmento_Extension( Extension ):
    """
    Extension Shortcuts.
    """
    SIGNAL_COLOR = QtCore.pyqtSignal( int )
    SIGNAL_KEY_1 = QtCore.pyqtSignal( int )
    SIGNAL_KEY_2 = QtCore.pyqtSignal( int )
    SIGNAL_KEY_3 = QtCore.pyqtSignal( int )
    SIGNAL_KEY_4 = QtCore.pyqtSignal( int )    
    SIGNAL_LOCK = QtCore.pyqtSignal( str )

    #region Initialize #############################################################

    def __init__( self, parent ):
        super().__init__( parent )
    def setup( self ):
        pass

    #endregion
    #region Actions ################################################################

    def createActions( self, window ):
        # Main Menu
        action_pigmento = window.createAction( "pigment_o", "Pigment.O", "tools/scripts" )
        menu_color = QtWidgets.QMenu( "pigment_o", window.qwindow() )
        menu_key   = QtWidgets.QMenu( "pigment_o", window.qwindow() )
        menu_lock  = QtWidgets.QMenu( "pigment_o", window.qwindow() )

        # Sub Menu
        action_color = window.createAction( "color", "Color", "tools/scripts/pigment_o" )
        action_key   = window.createAction( "key",   "Key",   "tools/scripts/pigment_o" )
        action_lock  = window.createAction( "lock",  "Lock",  "tools/scripts/pigment_o" )
        action_pigmento.setMenu( menu_color )
        action_pigmento.setMenu( menu_key )
        action_pigmento.setMenu( menu_lock )

        menu_color = QtWidgets.QMenu( "color", window.qwindow() )
        menu_key   = QtWidgets.QMenu( "key", window.qwindow() )
        menu_lock  = QtWidgets.QMenu( "lock", window.qwindow() )
        action_color.setMenu( menu_color )
        action_key.setMenu( menu_key )
        action_lock.setMenu( menu_lock )

        # Color Actions
        action_color_00 = window.createAction( "pigment_o_color_00", "Color 0",  "tools/scripts/pigment_o/color" )
        action_color_01 = window.createAction( "pigment_o_color_01", "Color 1",  "tools/scripts/pigment_o/color" )
        action_color_02 = window.createAction( "pigment_o_color_02", "Color 2",  "tools/scripts/pigment_o/color" )
        action_color_03 = window.createAction( "pigment_o_color_03", "Color 3",  "tools/scripts/pigment_o/color" )
        action_color_04 = window.createAction( "pigment_o_color_04", "Color 4",  "tools/scripts/pigment_o/color" )
        action_color_05 = window.createAction( "pigment_o_color_05", "Color 5",  "tools/scripts/pigment_o/color" )
        action_color_06 = window.createAction( "pigment_o_color_06", "Color 6",  "tools/scripts/pigment_o/color" )
        action_color_07 = window.createAction( "pigment_o_color_07", "Color 7",  "tools/scripts/pigment_o/color" )
        action_color_08 = window.createAction( "pigment_o_color_08", "Color 8",  "tools/scripts/pigment_o/color" )
        action_color_09 = window.createAction( "pigment_o_color_09", "Color 9",  "tools/scripts/pigment_o/color" )
        action_color_10 = window.createAction( "pigment_o_color_10", "Color 10", "tools/scripts/pigment_o/color" )
        # Color Connections
        action_color_00.triggered.connect( self.COLOR_00 )
        action_color_01.triggered.connect( self.COLOR_01 )
        action_color_02.triggered.connect( self.COLOR_02 )
        action_color_03.triggered.connect( self.COLOR_03 )
        action_color_04.triggered.connect( self.COLOR_04 )
        action_color_05.triggered.connect( self.COLOR_05 )
        action_color_06.triggered.connect( self.COLOR_06 )
        action_color_07.triggered.connect( self.COLOR_07 )
        action_color_08.triggered.connect( self.COLOR_08 )
        action_color_09.triggered.connect( self.COLOR_09 )
        action_color_10.triggered.connect( self.COLOR_10 )

        # Key Actions
        action_key_1_minus = window.createAction( "pigment_o_key_1_minus", "Key 1 Minus", "tools/scripts/pigment_o/key" )
        action_key_1_plus  = window.createAction( "pigment_o_key_1_plus",  "Key 1 Plus",  "tools/scripts/pigment_o/key" )
        action_key_2_minus = window.createAction( "pigment_o_key_2_minus", "Key 2 Minus", "tools/scripts/pigment_o/key" )
        action_key_2_plus  = window.createAction( "pigment_o_key_2_plus",  "Key 2 Plus",  "tools/scripts/pigment_o/key" )
        action_key_3_minus = window.createAction( "pigment_o_key_3_minus", "Key 3 Minus", "tools/scripts/pigment_o/key" )
        action_key_3_plus  = window.createAction( "pigment_o_key_3_plus",  "Key 3 Plus",  "tools/scripts/pigment_o/key" )
        action_key_4_minus = window.createAction( "pigment_o_key_4_minus", "Key 4 Minus", "tools/scripts/pigment_o/key" )
        action_key_4_plus  = window.createAction( "pigment_o_key_4_plus",  "Key 4 Plus",  "tools/scripts/pigment_o/key" )
        # Key Connections
        action_key_1_minus.triggered.connect( self.KEY_1_Minus )
        action_key_1_plus.triggered.connect( self.KEY_1_Plus )
        action_key_2_minus.triggered.connect( self.KEY_2_Minus )
        action_key_2_plus.triggered.connect( self.KEY_2_Plus )
        action_key_3_minus.triggered.connect( self.KEY_3_Minus )
        action_key_3_plus.triggered.connect( self.KEY_3_Plus )
        action_key_4_minus.triggered.connect( self.KEY_4_Minus )
        action_key_4_plus.triggered.connect( self.KEY_4_Plus )

        # Lock Actions
        action_lock_cmyk = window.createAction( "pigment_o_lock_cmyk", "Lock CMYK",   "tools/scripts/pigment_o/lock" )
        action_lock_kkk  = window.createAction( "pigment_o_lock_kkk",  "Lock Kelvin", "tools/scripts/pigment_o/lock" )
        # Lock Connections
        action_lock_cmyk.triggered.connect( self.LOCK_CMYK )
        action_lock_kkk.triggered.connect( self.LOCK_KKK )

    #endregion
    #region COLOR ##################################################################

    def COLOR_00( self ):
        self.SIGNAL_COLOR.emit( 0 )
    def COLOR_01( self ):
        self.SIGNAL_COLOR.emit( 1 )
    def COLOR_02( self ):
        self.SIGNAL_COLOR.emit( 2 )
    def COLOR_03( self ):
        self.SIGNAL_COLOR.emit( 3 )
    def COLOR_04( self ):
        self.SIGNAL_COLOR.emit( 4 )
    def COLOR_05( self ):
        self.SIGNAL_COLOR.emit( 5 )
    def COLOR_06( self ):
        self.SIGNAL_COLOR.emit( 6 )
    def COLOR_07( self ):
        self.SIGNAL_COLOR.emit( 7 )
    def COLOR_08( self ):
        self.SIGNAL_COLOR.emit( 8 )
    def COLOR_09( self ):
        self.SIGNAL_COLOR.emit( 9 )
    def COLOR_10( self ):
        self.SIGNAL_COLOR.emit( 10 )

    #endregion
    #region KEY ####################################################################

    def KEY_1_Minus( self ):
        self.SIGNAL_KEY_1.emit( -1 )
    def KEY_1_Plus( self ):
        self.SIGNAL_KEY_1.emit( 1 )

    def KEY_2_Minus( self ):
        self.SIGNAL_KEY_2.emit( -1 )
    def KEY_2_Plus( self ):
        self.SIGNAL_KEY_2.emit( 1 )

    def KEY_3_Minus( self ):
        self.SIGNAL_KEY_3.emit( -1 )
    def KEY_3_Plus( self ):
        self.SIGNAL_KEY_3.emit( 1 )

    def KEY_4_Minus( self ):
        self.SIGNAL_KEY_4.emit( -1 )
    def KEY_4_Plus( self ):
        self.SIGNAL_KEY_4.emit( 1 )

    #endregion
    #region LOCK ###################################################################

    def LOCK_CMYK( self ):
        self.SIGNAL_LOCK.emit( "CMYK" )
    def LOCK_KKK( self ):
        self.SIGNAL_LOCK.emit( "KKK" )

    #endregion
