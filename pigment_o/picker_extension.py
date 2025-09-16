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


#region Import Modules

from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, uic

#endregion
#region Global Variables

EXTENSION_ID = 'pykrita_pigment_o_picker_extension'

#endregion


class Picker_Extension( Extension ):
    SIGNAL_PIN = QtCore.pyqtSignal( int )
    SIGNAL_KEY_1 = QtCore.pyqtSignal( int )
    SIGNAL_KEY_2 = QtCore.pyqtSignal( int )
    SIGNAL_KEY_3 = QtCore.pyqtSignal( int )
    SIGNAL_KEY_4 = QtCore.pyqtSignal( int )
    SIGNAL_LOCK = QtCore.pyqtSignal( str )

    #region Initialize

    def __init__( self, parent ):
        super().__init__( parent )
    def setup( self ):
        pass

    #endregion
    #region Actions

    def createActions( self, window ):
        # Main Menu
        menu_pigment_o = QtWidgets.QMenu( "pigment_o_menu", window.qwindow() )
        action_pigment_o = window.createAction( "pigment_o_menu", "Pigment.O", "tools/scripts" )
        action_pigment_o.setMenu( menu_pigment_o )

        # Sub Menus
        menu_pin = QtWidgets.QMenu( "pin_menu", window.qwindow() )
        action_pin = window.createAction( "pin_menu", "Pin", "tools/scripts/pigment_o_menu" )
        action_pin.setMenu( menu_pin )

        menu_key = QtWidgets.QMenu( "key_menu", window.qwindow() )
        action_key = window.createAction( "key_menu", "Key", "tools/scripts/pigment_o_menu" )
        action_key.setMenu( menu_key )

        menu_lock = QtWidgets.QMenu( "lock_menu", window.qwindow() )
        action_lock = window.createAction( "lock_menu", "Lock", "tools/scripts/pigment_o_menu" )
        action_lock.setMenu( menu_lock )

        # Pin Actions
        action_pin_00 = window.createAction( "pigment_o_picker_pin_00", "Pin 00", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_01 = window.createAction( "pigment_o_picker_pin_01", "Pin 01", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_02 = window.createAction( "pigment_o_picker_pin_02", "Pin 02", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_03 = window.createAction( "pigment_o_picker_pin_03", "Pin 03", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_04 = window.createAction( "pigment_o_picker_pin_04", "Pin 04", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_05 = window.createAction( "pigment_o_picker_pin_05", "Pin 05", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_06 = window.createAction( "pigment_o_picker_pin_06", "Pin 06", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_07 = window.createAction( "pigment_o_picker_pin_07", "Pin 07", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_08 = window.createAction( "pigment_o_picker_pin_08", "Pin 08", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_09 = window.createAction( "pigment_o_picker_pin_09", "Pin 09", "tools/scripts/pigment_o_menu/pin_menu" )
        action_pin_10 = window.createAction( "pigment_o_picker_pin_10", "Pin 10", "tools/scripts/pigment_o_menu/pin_menu" )
        # Pin Connections
        action_pin_00.triggered.connect( self.PIN_00 )
        action_pin_01.triggered.connect( self.PIN_01 )
        action_pin_02.triggered.connect( self.PIN_02 )
        action_pin_03.triggered.connect( self.PIN_03 )
        action_pin_04.triggered.connect( self.PIN_04 )
        action_pin_05.triggered.connect( self.PIN_05 )
        action_pin_06.triggered.connect( self.PIN_06 )
        action_pin_07.triggered.connect( self.PIN_07 )
        action_pin_08.triggered.connect( self.PIN_08 )
        action_pin_09.triggered.connect( self.PIN_09 )
        action_pin_10.triggered.connect( self.PIN_10 )

        # Key Actions
        action_key_1_minus = window.createAction( "pigment_o_picker_key_1_minus", "Key 1 Minus", "tools/scripts/pigment_o_menu/key_menu" )
        action_key_1_plus  = window.createAction( "pigment_o_picker_key_1_plus",  "Key 1 Plus",  "tools/scripts/pigment_o_menu/key_menu" )
        action_key_2_minus = window.createAction( "pigment_o_picker_key_2_minus", "Key 2 Minus", "tools/scripts/pigment_o_menu/key_menu" )
        action_key_2_plus  = window.createAction( "pigment_o_picker_key_2_plus",  "Key 2 Plus",  "tools/scripts/pigment_o_menu/key_menu" )
        action_key_3_minus = window.createAction( "pigment_o_picker_key_3_minus", "Key 3 Minus", "tools/scripts/pigment_o_menu/key_menu" )
        action_key_3_plus  = window.createAction( "pigment_o_picker_key_3_plus",  "Key 3 Plus",  "tools/scripts/pigment_o_menu/key_menu" )
        action_key_4_minus = window.createAction( "pigment_o_picker_key_4_minus", "Key 4 Minus", "tools/scripts/pigment_o_menu/key_menu" )
        action_key_4_plus  = window.createAction( "pigment_o_picker_key_4_plus",  "Key 4 Plus",  "tools/scripts/pigment_o_menu/key_menu" )
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
        action_lock_cmyk = window.createAction( "pigment_o_picker_lock_cmyk", "Lock CMYK",   "tools/scripts/pigment_o_menu/lock_menu" )
        action_lock_kkk  = window.createAction( "pigment_o_picker_lock_kkk",  "Lock Kelvin", "tools/scripts/pigment_o_menu/lock_menu" )
        # Lock Connections
        action_lock_cmyk.triggered.connect( self.LOCK_CMYK )
        action_lock_kkk.triggered.connect( self.LOCK_KKK )

    #endregion
    #region PIN

    def PIN_00( self ):
        self.SIGNAL_PIN.emit( 0 )
    def PIN_01( self ):
        self.SIGNAL_PIN.emit( 1 )
    def PIN_02( self ):
        self.SIGNAL_PIN.emit( 2 )
    def PIN_03( self ):
        self.SIGNAL_PIN.emit( 3 )
    def PIN_04( self ):
        self.SIGNAL_PIN.emit( 4 )
    def PIN_05( self ):
        self.SIGNAL_PIN.emit( 5 )
    def PIN_06( self ):
        self.SIGNAL_PIN.emit( 6 )
    def PIN_07( self ):
        self.SIGNAL_PIN.emit( 7 )
    def PIN_08( self ):
        self.SIGNAL_PIN.emit( 8 )
    def PIN_09( self ):
        self.SIGNAL_PIN.emit( 9 )
    def PIN_10( self ):
        self.SIGNAL_PIN.emit( 10 )

    #endregion
    #region KEY

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
    #region LOCK

    def LOCK_CMYK( self ):
        self.SIGNAL_LOCK.emit( "CMYK" )
    def LOCK_KKK( self ):
        self.SIGNAL_LOCK.emit( "KKK" )

    #endregion
