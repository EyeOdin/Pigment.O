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

# Python Modules
import math
import random
import os
import time
import sys
import webbrowser
import datetime
import shutil
import re
# Krita Modules
from krita import *
# PyQt5 Modules
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# Pigment.O Modules
from .pigment_o_names import *
from .pigment_o_constants import *
from .pigment_o_calculations import Geometry, Convert
from .pigment_o_extension import Pigmento_Extension
from .pigment_o_modulo import ( 
    # Header
    Color_Header,
    Harmony_Swatch,
    Harmony_Spread,
    # Panels
    Panel_Fill,
    Panel_Square,
    Panel_HueCircle,
    Panel_Gamut,
    Panel_Hexagon,
    Panel_Dot,
    Panel_Mask,
    # Sliders
    Channel_Slider,
    Channel_Selection,
    # Mixer
    Pin_Color,
    # Maps
    Sample_Map,
    )

#endregion
#region Global Variables ###########################################################

DOCKER_NAME_1 = "Pigment.O"
DOCKER_NAME_2 = "Pigment.S"
pigment_o_version = "2023_10_01"

#endregion


class PigmentO_Docker( DockWidget ):
    """
    Color Picker and Mixer
    """

    #region Initialize #############################################################

    def __init__( self ):
        super( PigmentO_Docker, self ).__init__()

        # Construct
        self.Variables()
        self.User_Interface()
        self.Connections()
        self.Modules()
        self.Style()
        self.Timer()
        self.Extension()
        self.Settings()
        self.Loader()

    def Variables( self ):
        # Widget
        self.mode_index = 0
        self.inbound = False
        self.mode_ab = True
        self.cor = kac
        self.widget_press = False # cursor pressing widget
        self.slider_height = 15
        self.depth_previous = 0
        # Document
        self.doc = self.Current_Document()
        self.fill = False

        # Harmony
        self.harmony_rule = "Analogous" # "Monochromatic" "Complementary" "Analogous" "Triadic" "Tetradic"
        self.harmony_edit = False
        self.harmony_index = 0
        self.harmony_span = 0.2

        # Panels
        self.zoom = False
        # Color Wheel
        self.wheel_mode = "DIGITAL" # "DIGITAL" "ANALOG"
        self.wheel_space = "HSV" # "HSV" "HSL" "HSY" "ARD"
        # Hue
        self.huecircle_shape = "None" # "None" "Triangle" "Square" "Diamond"
        # Gamut
        self.gamut_mask = "None" # "None" "Triangle" "Square" "1 Circle" "2 Circle" "3 Pie" "Reset"
        self.gamut_profile = [
            [ ( 0.5, 0.5 ), ( 0.5, 0.1 ), ( 0.84641, 0.7 ), ( 0.15359, 0.7 ) ],
            [ ( 0.5, 0.5 ), ( 0.5, 0.1 ), ( 0.9, 0.5 ), ( 0.5, 0.9 ), ( 0.1, 0.5 ) ],
            [ ( 0.5, 0.5 ), ( 0.5, 0.1 ), ( 0.9, 0.5 ), ( 0.5, 0.9 ), ( 0.1, 0.5 ) ],
            [ ( 0.5, 0.275 ), ( 0.5, 0.1 ), ( 0.675, 0.275 ), ( 0.5, 0.45 ), ( 0.325, 0.275 ), ( 0.5, 0.725 ), ( 0.5, 0.55 ), ( 0.675, 0.725 ), ( 0.5, 0.9 ), ( 0.325, 0.725 ) ],
            [ ( 0.5, 0.5 ), ( 0.5, 0.15359 ), ( 0.8, 0.32679 ), ( 0.8, 0.67321 ), ( 0.5, 0.84641 ), ( 0.2, 0.67321 ), ( 0.2, 0.32679 ) ],
            ]

        # Dots
        self.dot_interpolation = "RGB"
        self.dot_dimension = 11
        self.dot_edit = False
        self.dot_1 = color_false.copy()
        self.dot_2 = color_false.copy()
        self.dot_3 = color_false.copy()
        self.dot_4 = color_false.copy()
        # Mask
        self.mask_set = None
        self.mask_live = {
            "b1" : False,
            "b2" : False,
            "b3" : False,
            "d1" : False,
            "d2" : False,
            "d3" : False,
            "d4" : False,
            "d5" : False,
            "d6" : False,
            "f1" : False,
            "f2" : False,
            "f3" : False,
            }
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
        self.mask_edit = False
        self.mask_write = False

        # UI
        self.ui_harmony = False
        self.ui_channel = False
        self.ui_mixer = False
        self.ui_pin = False
        self.ui_history = False

        # Panels
        self.panel_index = None
        # Mixers
        self.mixer_space = "RGB" # mix method
        self.mixer_count = 1
        self.mixer_widget = None
        self.mixer_module = None
        self.mixer_colors = [ {
            "l" : color_false.copy(),
            "m" : 0,
            "r" : color_false.copy(),
            } ]
        # Pins
        self.pin_widget = []
        self.pin_module = []
        self.pin_cor = []

        # Channels
        self.chan_aaa = False
        self.chan_rgb = False
        self.chan_cmy = False
        self.chan_cmyk = False
        self.chan_ryb = False
        self.chan_yuv = False
        self.chan_hsv = False
        self.chan_hsl = False
        self.chan_hsy = False
        self.chan_ard = False
        self.chan_xyz = False
        self.chan_xyy = False
        self.chan_lab = False
        self.chan_lch = False
        # Non Color
        self.chan_kkk = False
        self.chan_sele = False
        self.sele_mode = "RGB"
        self.chan_hex = False
        self.hex_sum = False
        # Locks
        self.lock_cmyk_4 = False
        self.lock_kkk_1 = False

        # Channel Format
        self.hue_shine = False
        self.disp_values = False
        self.hex_copy_paste = False

        # Shortcut
        self.key_1_chan = "[KEY 1]"
        self.key_2_chan = "[KEY 2]"
        self.key_3_chan = "[KEY 3]"
        self.key_4_chan = "[KEY 4]"
        self.key_1_factor = 1
        self.key_2_factor = 1
        self.key_3_factor = 1
        self.key_4_factor = 1

        # Annotations
        self.annotation_kra = False
        self.annotation_file = False
        # Performance
        self.performance_release = False
        self.performance_inaccurate = False

        # Analyse
        self.analyse_display = False
        self.analyse_collection = None

        # Style Sheets
        self.bg_alpha = str( "background-color: rgba( 0, 0, 0, 50 );" )
    def User_Interface( self ):
        # Window
        self.setWindowTitle( DOCKER_NAME_1 )

        # Operating System
        self.OS = str( QSysInfo.kernelType() ) # WINDOWS=winnt & LINUX=linux
        if self.OS == "winnt": # Unlocks icons in Krita for Menu Mode
            QApplication.setAttribute( Qt.AA_DontShowIconsInMenus, False )

        # Path Name
        self.directory_plugin = str( os.path.dirname( os.path.realpath( __file__ ) ) )

        # Widget Docker
        self.layout = uic.loadUi( os.path.join( self.directory_plugin, "pigment_o_docker.ui" ), QWidget( self ) )
        self.setWidget( self.layout )

        # Settings
        self.dialog = uic.loadUi( os.path.join( self.directory_plugin, "pigment_o_settings.ui" ), QDialog( self ) )
        self.dialog.setWindowTitle( "Pigment.O : Settings" )
        self.dialog.accept() # Hides the Dialog

        # Mixer Layout
        self.mixer_widget = [ {
            "l" : self.layout.mixer_l_000,
            "m" : self.layout.mixer_m_000,
            "r" : self.layout.mixer_r_000,
            } ]
    def Connections( self ):
        #region Panel Dot

        self.layout.dot_swap.clicked.connect( self.Dot_Swap )

        #endregion
        #region Panel Mask

        self.layout.fg_3_live.toggled.connect( self.Mask_Live_F3 )
        self.layout.fg_2_live.toggled.connect( self.Mask_Live_F2 )
        self.layout.fg_1_live.toggled.connect( self.Mask_Live_F1 )

        self.layout.dif_6_live.toggled.connect( self.Mask_Live_D6 )
        self.layout.dif_5_live.toggled.connect( self.Mask_Live_D5 )
        self.layout.dif_4_live.toggled.connect( self.Mask_Live_D4 )
        self.layout.dif_3_live.toggled.connect( self.Mask_Live_D3 )
        self.layout.dif_2_live.toggled.connect( self.Mask_Live_D2 )
        self.layout.dif_1_live.toggled.connect( self.Mask_Live_D1 )

        self.layout.bg_3_live.toggled.connect( self.Mask_Live_B3 )
        self.layout.bg_2_live.toggled.connect( self.Mask_Live_B2 )
        self.layout.bg_1_live.toggled.connect( self.Mask_Live_B1 )
        
        #endregion
        #region Locks

        self.layout.cmyk_4_label.toggled.connect( self.Lock_CMYK_4 )
        self.layout.kkk_1_label.toggled.connect( self.Lock_KKK_1 )

        #endregion
        #region Channels Ranges

        # AAA
        self.layout.aaa_1_value.setMinimum( 0 )
        self.layout.aaa_1_value.setMaximum( krange["aaa_1"] )
        # RGB
        self.layout.rgb_1_value.setMinimum( 0 )
        self.layout.rgb_2_value.setMinimum( 0 )
        self.layout.rgb_3_value.setMinimum( 0 )
        self.layout.rgb_1_value.setMaximum( krange["rgb_1"] )
        self.layout.rgb_2_value.setMaximum( krange["rgb_2"] )
        self.layout.rgb_3_value.setMaximum( krange["rgb_3"] )
        # CMY
        self.layout.cmy_1_value.setMinimum( 0 )
        self.layout.cmy_2_value.setMinimum( 0 )
        self.layout.cmy_3_value.setMinimum( 0 )
        self.layout.cmy_1_value.setMaximum( krange["cmy_1"] )
        self.layout.cmy_2_value.setMaximum( krange["cmy_2"] )
        self.layout.cmy_3_value.setMaximum( krange["cmy_3"] )
        # CMYK
        self.layout.cmyk_1_value.setMinimum( 0 )
        self.layout.cmyk_2_value.setMinimum( 0 )
        self.layout.cmyk_3_value.setMinimum( 0 )
        self.layout.cmyk_4_value.setMinimum( 0 )
        self.layout.cmyk_1_value.setMaximum( krange["cmyk_1"] )
        self.layout.cmyk_2_value.setMaximum( krange["cmyk_2"] )
        self.layout.cmyk_3_value.setMaximum( krange["cmyk_3"] )
        self.layout.cmyk_4_value.setMaximum( krange["cmyk_4"] )
        # RYB
        self.layout.ryb_1_value.setMinimum( 0 )
        self.layout.ryb_2_value.setMinimum( 0 )
        self.layout.ryb_3_value.setMinimum( 0 )
        self.layout.ryb_1_value.setMaximum( krange["ryb_1"] )
        self.layout.ryb_2_value.setMaximum( krange["ryb_2"] )
        self.layout.ryb_3_value.setMaximum( krange["ryb_3"] )
        # YUV
        self.layout.yuv_1_value.setMinimum( 0 )
        self.layout.yuv_2_value.setMinimum( 0 )
        self.layout.yuv_3_value.setMinimum( 0 )
        self.layout.yuv_1_value.setMaximum( krange["yuv_1"] )
        self.layout.yuv_2_value.setMaximum( krange["yuv_2"] )
        self.layout.yuv_3_value.setMaximum( krange["yuv_3"] )

        # HSV
        self.layout.hsv_1_value.setMinimum( 0 )
        self.layout.hsv_2_value.setMinimum( 0 )
        self.layout.hsv_3_value.setMinimum( 0 )
        self.layout.hsv_1_value.setMaximum( krange["hsv_1"] )
        self.layout.hsv_2_value.setMaximum( krange["hsv_2"] )
        self.layout.hsv_3_value.setMaximum( krange["hsv_3"] )
        # HSL
        self.layout.hsl_1_value.setMinimum( 0 )
        self.layout.hsl_2_value.setMinimum( 0 )
        self.layout.hsl_3_value.setMinimum( 0 )
        self.layout.hsl_1_value.setMaximum( krange["hsl_1"] )
        self.layout.hsl_2_value.setMaximum( krange["hsl_2"] )
        self.layout.hsl_3_value.setMaximum( krange["hsl_3"] )
        # HSY
        self.layout.hsy_1_value.setMinimum( 0 )
        self.layout.hsy_2_value.setMinimum( 0 )
        self.layout.hsy_3_value.setMinimum( 0 )
        self.layout.hsy_1_value.setMaximum( krange["hsy_1"] )
        self.layout.hsy_2_value.setMaximum( krange["hsy_2"] )
        self.layout.hsy_3_value.setMaximum( krange["hsy_3"] )
        # ARD
        self.layout.ard_1_value.setMinimum( 0 )
        self.layout.ard_2_value.setMinimum( 0 )
        self.layout.ard_3_value.setMinimum( 0 )
        self.layout.ard_1_value.setMaximum( krange["ard_1"] )
        self.layout.ard_2_value.setMaximum( krange["ard_2"] )
        self.layout.ard_3_value.setMaximum( krange["ard_3"] )

        # XYZ
        self.layout.xyz_1_value.setMinimum( 0 )
        self.layout.xyz_2_value.setMinimum( 0 )
        self.layout.xyz_3_value.setMinimum( 0 )
        self.layout.xyz_1_value.setMaximum( krange["xyz_1"] )
        self.layout.xyz_2_value.setMaximum( krange["xyz_2"] )
        self.layout.xyz_3_value.setMaximum( krange["xyz_3"] )
        # XYY
        self.layout.xyy_1_value.setMinimum( 0 )
        self.layout.xyy_2_value.setMinimum( 0 )
        self.layout.xyy_3_value.setMinimum( 0 )
        self.layout.xyy_1_value.setMaximum( krange["xyy_1"] )
        self.layout.xyy_2_value.setMaximum( krange["xyy_2"] )
        self.layout.xyy_3_value.setMaximum( krange["xyy_3"] )
        # LAB
        self.layout.lab_1_value.setMinimum( 0 )
        self.layout.lab_2_value.setMinimum( 0 )
        self.layout.lab_3_value.setMinimum( 0 )
        self.layout.lab_1_value.setMaximum( krange["lab_1"] )
        self.layout.lab_2_value.setMaximum( krange["lab_2"] )
        self.layout.lab_3_value.setMaximum( krange["lab_3"] )

        # LCH
        self.layout.lch_1_value.setMinimum( 0 )
        self.layout.lch_2_value.setMinimum( 0 )
        self.layout.lch_3_value.setMinimum( 0 )
        self.layout.lch_1_value.setMaximum( krange["lch_1"] )
        self.layout.lch_2_value.setMaximum( krange["lch_2"] )
        self.layout.lch_3_value.setMaximum( krange["lch_3"] )

        #endregion
        #region Channels Connections

        # AAA
        self.layout.aaa_1_value.valueChanged.connect( self.Channels_AAA_1_Value )
        # RGB
        self.layout.rgb_1_value.valueChanged.connect( self.Channels_RGB_1_Value )
        self.layout.rgb_2_value.valueChanged.connect( self.Channels_RGB_2_Value )
        self.layout.rgb_3_value.valueChanged.connect( self.Channels_RGB_3_Value )
        # CMY
        self.layout.cmy_1_value.valueChanged.connect( self.Channels_CMY_1_Value )
        self.layout.cmy_2_value.valueChanged.connect( self.Channels_CMY_2_Value )
        self.layout.cmy_3_value.valueChanged.connect( self.Channels_CMY_3_Value )
        # CMYK
        self.layout.cmyk_1_value.valueChanged.connect( self.Channels_CMYK_1_Value )
        self.layout.cmyk_2_value.valueChanged.connect( self.Channels_CMYK_2_Value )
        self.layout.cmyk_3_value.valueChanged.connect( self.Channels_CMYK_3_Value )
        self.layout.cmyk_4_value.valueChanged.connect( self.Channels_CMYK_4_Value )
        # RYB
        self.layout.ryb_1_value.valueChanged.connect( self.Channels_RYB_1_Value )
        self.layout.ryb_2_value.valueChanged.connect( self.Channels_RYB_2_Value )
        self.layout.ryb_3_value.valueChanged.connect( self.Channels_RYB_3_Value )
        # YUV
        self.layout.yuv_1_value.valueChanged.connect( self.Channels_YUV_1_Value )
        self.layout.yuv_2_value.valueChanged.connect( self.Channels_YUV_2_Value )
        self.layout.yuv_3_value.valueChanged.connect( self.Channels_YUV_3_Value )

        # HSV
        self.layout.hsv_1_value.valueChanged.connect( self.Channels_HSV_1_Value )
        self.layout.hsv_2_value.valueChanged.connect( self.Channels_HSV_2_Value )
        self.layout.hsv_3_value.valueChanged.connect( self.Channels_HSV_3_Value )
        # HSL
        self.layout.hsl_1_value.valueChanged.connect( self.Channels_HSL_1_Value )
        self.layout.hsl_2_value.valueChanged.connect( self.Channels_HSL_2_Value )
        self.layout.hsl_3_value.valueChanged.connect( self.Channels_HSL_3_Value )
        # HSY
        self.layout.hsy_1_value.valueChanged.connect( self.Channels_HSY_1_Value )
        self.layout.hsy_2_value.valueChanged.connect( self.Channels_HSY_2_Value )
        self.layout.hsy_3_value.valueChanged.connect( self.Channels_HSY_3_Value )
        # ARD
        self.layout.ard_1_value.valueChanged.connect( self.Channels_ARD_1_Value )
        self.layout.ard_2_value.valueChanged.connect( self.Channels_ARD_2_Value )
        self.layout.ard_3_value.valueChanged.connect( self.Channels_ARD_3_Value )

        # XYZ
        self.layout.xyz_1_value.valueChanged.connect( self.Channels_XYZ_1_Value )
        self.layout.xyz_2_value.valueChanged.connect( self.Channels_XYZ_2_Value )
        self.layout.xyz_3_value.valueChanged.connect( self.Channels_XYZ_3_Value )
        # XYY
        self.layout.xyy_1_value.valueChanged.connect( self.Channels_XYY_1_Value )
        self.layout.xyy_2_value.valueChanged.connect( self.Channels_XYY_2_Value )
        self.layout.xyy_3_value.valueChanged.connect( self.Channels_XYY_3_Value )
        # LAB*
        self.layout.lab_1_value.valueChanged.connect( self.Channels_LAB_1_Value )
        self.layout.lab_2_value.valueChanged.connect( self.Channels_LAB_2_Value )
        self.layout.lab_3_value.valueChanged.connect( self.Channels_LAB_3_Value )

        # LCH
        self.layout.lch_1_value.valueChanged.connect( self.Channels_LCH_1_Value )
        self.layout.lch_2_value.valueChanged.connect( self.Channels_LCH_2_Value )
        self.layout.lch_3_value.valueChanged.connect( self.Channels_LCH_3_Value )

        # KKK
        self.layout.kkk_1_value.valueChanged.connect( self.Channels_KKK_1_Value )

        # Sele 1
        self.layout.sele_1_l0.valueChanged.connect( self.Channels_SELE_1_L0_Value )
        self.layout.sele_1_l1.valueChanged.connect( self.Channels_SELE_1_L1_Value )
        self.layout.sele_1_r1.valueChanged.connect( self.Channels_SELE_1_R1_Value )
        self.layout.sele_1_r0.valueChanged.connect( self.Channels_SELE_1_R0_Value )
        # Sele 2
        self.layout.sele_2_l0.valueChanged.connect( self.Channels_SELE_2_L0_Value )
        self.layout.sele_2_l1.valueChanged.connect( self.Channels_SELE_2_L1_Value )
        self.layout.sele_2_r1.valueChanged.connect( self.Channels_SELE_2_R1_Value )
        self.layout.sele_2_r0.valueChanged.connect( self.Channels_SELE_2_R0_Value )
        # Sele 3
        self.layout.sele_3_l0.valueChanged.connect( self.Channels_SELE_3_L0_Value )
        self.layout.sele_3_l1.valueChanged.connect( self.Channels_SELE_3_L1_Value )
        self.layout.sele_3_r1.valueChanged.connect( self.Channels_SELE_3_R1_Value )
        self.layout.sele_3_r0.valueChanged.connect( self.Channels_SELE_3_R0_Value )
        # Sele 4
        self.layout.sele_4_l0.valueChanged.connect( self.Channels_SELE_4_L0_Value )
        self.layout.sele_4_l1.valueChanged.connect( self.Channels_SELE_4_L1_Value )
        self.layout.sele_4_r1.valueChanged.connect( self.Channels_SELE_4_R1_Value )
        self.layout.sele_4_r0.valueChanged.connect( self.Channels_SELE_4_R0_Value )

        # HEX
        self.layout.hex_string.returnPressed.connect( lambda: self.Color_HEX( self.layout.hex_string.text() ) )

        #endregion
        #region History

        self.layout.history_list.clicked.connect( self.History_APPLY )

        #endregion
        #region Footer

        self.layout.fill.toggled.connect( self.Menu_FILL )
        self.layout.selection.clicked.connect( self.Selection_APPLY )
        self.layout.settings.clicked.connect( self.Menu_Settings )

        #endregion
        #region Dialog Header

        self.dialog.harmony.toggled.connect( self.Menu_Harmony )
        self.dialog.channel.toggled.connect( self.Menu_Channel )
        self.dialog.mixer.toggled.connect( self.Menu_Mixer )
        self.dialog.pin.toggled.connect( self.Menu_Pin )
        self.dialog.history.toggled.connect( self.Menu_History )

        #endregion
        #region Dialog Option

        # Panels
        self.dialog.panel_index.currentTextChanged.connect( self.Panel_Index )
        # Wheel
        self.dialog.wheel_mode.currentTextChanged.connect( self.Wheel_Mode )
        self.dialog.wheel_space.currentTextChanged.connect( self.Wheel_Space )
        # Analyse
        self.dialog.analyse_display.toggled.connect( self.Analyse_Display )
        # Mixers
        self.dialog.mixer_space.currentTextChanged.connect( self.Mixer_Space )
        self.dialog.mixer_count.valueChanged.connect( self.Mixer_Count )

        #endregion
        #region Dialog Color

        # Channels
        self.dialog.chan_aaa.toggled.connect( self.Channel_AAA )
        self.dialog.chan_rgb.toggled.connect( self.Channel_RGB )
        self.dialog.chan_cmy.toggled.connect( self.Channel_CMY )
        self.dialog.chan_cmyk.toggled.connect( self.Channel_CMYK )
        self.dialog.chan_ryb.toggled.connect( self.Channel_RYB )
        self.dialog.chan_yuv.toggled.connect( self.Channel_YUV )
        self.dialog.chan_hsv.toggled.connect( self.Channel_HSV )
        self.dialog.chan_hsl.toggled.connect( self.Channel_HSL )
        self.dialog.chan_hsy.toggled.connect( self.Channel_HSY )
        self.dialog.chan_ard.toggled.connect( self.Channel_ARD )
        self.dialog.chan_xyz.toggled.connect( self.Channel_XYZ )
        self.dialog.chan_xyy.toggled.connect( self.Channel_XYY )
        self.dialog.chan_lab.toggled.connect( self.Channel_LAB )
        self.dialog.chan_lch.toggled.connect( self.Channel_LCH )

        # Ranges
        self.dialog.range_aaa.valueChanged.connect( self.Range_AAA )
        self.dialog.range_rgb.valueChanged.connect( self.Range_RGB )
        self.dialog.range_cmy.valueChanged.connect( self.Range_CMY )
        self.dialog.range_cmyk.valueChanged.connect( self.Range_CMYK )
        self.dialog.range_ryb.valueChanged.connect( self.Range_RYB )
        self.dialog.range_yuv.valueChanged.connect( self.Range_YUV )
        self.dialog.range_hue.valueChanged.connect( self.Range_HUE )
        self.dialog.range_hsv.valueChanged.connect( self.Range_HSV )
        self.dialog.range_hsl.valueChanged.connect( self.Range_HSL )
        self.dialog.range_hsy.valueChanged.connect( self.Range_HSY )
        self.dialog.range_ard.valueChanged.connect( self.Range_ARD )
        self.dialog.range_xyz.valueChanged.connect( self.Range_XYZ )
        self.dialog.range_xyy.valueChanged.connect( self.Range_XYY )
        self.dialog.range_lab.valueChanged.connect( self.Range_LAB )
        self.dialog.range_lch.valueChanged.connect( self.Range_LCH )

        # Resets
        self.dialog.reset_aaa.clicked.connect( self.Reset_AAA )
        self.dialog.reset_rgb.clicked.connect( self.Reset_RGB )
        self.dialog.reset_cmy.clicked.connect( self.Reset_CMY )
        self.dialog.reset_cmyk.clicked.connect( self.Reset_CMYK )
        self.dialog.reset_ryb.clicked.connect( self.Reset_RYB )
        self.dialog.reset_yuv.clicked.connect( self.Reset_YUV )
        self.dialog.reset_hue.clicked.connect( self.Reset_HUE )
        self.dialog.reset_hsv.clicked.connect( self.Reset_HSV )
        self.dialog.reset_hsl.clicked.connect( self.Reset_HSL )
        self.dialog.reset_hsy.clicked.connect( self.Reset_HSY )
        self.dialog.reset_ard.clicked.connect( self.Reset_ARD )
        self.dialog.reset_xyz.clicked.connect( self.Reset_XYZ )
        self.dialog.reset_xyy.clicked.connect( self.Reset_XYY )
        self.dialog.reset_lab.clicked.connect( self.Reset_LAB )
        self.dialog.reset_lch.clicked.connect( self.Reset_LCH )

        # Non Color Kelvin
        self.dialog.chan_kkk.toggled.connect( self.Channel_KKK )
        # Non Color Selection
        self.dialog.chan_sele.toggled.connect( self.Channel_SELE )
        self.dialog.sele_mode.currentTextChanged.connect( self.Selection_Mode )
        # Non Color Hex
        self.dialog.chan_hex.toggled.connect( self.Channel_Hex )
        self.dialog.hex_sum.toggled.connect( self.Hex_Sum )

        # Format
        self.dialog.hue_shine.toggled.connect( self.Hue_Shine )
        self.dialog.disp_values.toggled.connect( self.Display_Values )
        self.dialog.hex_copy_paste.toggled.connect( self.Hex_CopyPaste )

        # Reference
        self.dialog.name_display.clicked.connect( self.Color_Name )
        self.dialog.names_closest.clicked.connect( self.HEX_Closest )

        # Shortcuts
        self.dialog.key_1_chan.currentTextChanged.connect( self.Key_1_Channel )
        self.dialog.key_2_chan.currentTextChanged.connect( self.Key_2_Channel )
        self.dialog.key_3_chan.currentTextChanged.connect( self.Key_3_Channel )
        self.dialog.key_4_chan.currentTextChanged.connect( self.Key_4_Channel )
        self.dialog.key_1_factor.valueChanged.connect( self.Key_1_Factor )
        self.dialog.key_2_factor.valueChanged.connect( self.Key_2_Factor )
        self.dialog.key_3_factor.valueChanged.connect( self.Key_3_Factor )
        self.dialog.key_4_factor.valueChanged.connect( self.Key_4_Factor )

        #endregion
        #region Dialog System

        # Color Space
        self.dialog.cs_luminosity.currentTextChanged.connect( self.CS_Luminosity )
        self.dialog.cs_matrix.currentTextChanged.connect( lambda: self.CS_Matrix( self.dialog.cs_matrix.currentText(), self.dialog.cs_illuminant.currentText() ) )
        self.dialog.cs_illuminant.currentTextChanged.connect( lambda: self.CS_Matrix( self.dialog.cs_matrix.currentText(), self.dialog.cs_illuminant.currentText() ) )

        # Annotations
        self.dialog.annotation_kra_save.toggled.connect( self.AutoSave_KRA )
        self.dialog.annotation_kra_load.clicked.connect( self.Annotation_KRA_Load )
        self.dialog.annotation_file_save.toggled.connect( self.AutoSave_File )
        self.dialog.annotation_file_load.clicked.connect( self.Annotation_FILE_Load )

        # Performance
        self.dialog.performance_release.toggled.connect( self.Performace_Release )
        self.dialog.performance_inaccurate.toggled.connect( self.Performace_Inaccurate )

        #endregion
        #region Dialog Footer

        self.dialog.manual.clicked.connect( self.Menu_Manual )
        self.dialog.license.clicked.connect( self.Menu_License )

        #endregion
        #region Event Filter

        # Panel
        self.layout.panel_set.installEventFilter( self )
        self.layout.edit_dot.installEventFilter( self )
        self.layout.edit_mask.installEventFilter( self )
        # Channel
        self.layout.aaa_slider.installEventFilter( self )
        self.layout.rgb_slider.installEventFilter( self )
        self.layout.cmy_slider.installEventFilter( self )
        self.layout.cmyk_slider.installEventFilter( self )
        self.layout.ryb_slider.installEventFilter( self )
        self.layout.yuv_slider.installEventFilter( self )
        self.layout.hsv_slider.installEventFilter( self )
        self.layout.hsl_slider.installEventFilter( self )
        self.layout.hsy_slider.installEventFilter( self )
        self.layout.ard_slider.installEventFilter( self )
        self.layout.xyz_slider.installEventFilter( self )
        self.layout.xyy_slider.installEventFilter( self )
        self.layout.lab_slider.installEventFilter( self )
        self.layout.lch_slider.installEventFilter( self )
        self.layout.kkk_slider.installEventFilter( self )
        # Mixer
        self.layout.mixer_set.installEventFilter( self )
        # Footer
        self.layout.mode.installEventFilter( self ) # Mode Index
        self.layout.history_list.installEventFilter( self ) # History Clear

        #endregion
    def Modules( self ):
        #region Notifier

        self.notifier = Krita.instance().notifier()
        self.notifier.applicationClosing.connect( self.Application_Closing )
        self.notifier.configurationChanged.connect( self.Configuration_Changed )
        self.notifier.imageClosed.connect( self.Image_Closed )
        self.notifier.imageCreated.connect( self.Image_Created )
        self.notifier.imageSaved.connect( self.Image_Saved )
        self.notifier.viewClosed.connect( self.View_Closed )
        self.notifier.viewCreated.connect( self.View_Created )
        self.notifier.windowCreated.connect( self.Window_Created )
        self.notifier.windowIsBeingCreated.connect( self.Window_IsBeingCreated )

        #endregion
        #region Geometry

        self.geometry = Geometry()

        #endregion
        #region Conversions

        self.convert = Convert()
        self.convert.Set_Document( "RGB", "U8", "sRGB-elle-V2-srgtrc.icc" )
        self.convert.Set_Hue( zero )
        self.convert.Set_Luminosity( "ITU-R BT.709" )
        self.convert.Set_Gamma( gamma_y, gamma_l )
        self.convert.Set_Matrix( "sRGB", "D65" )

        #endregion
        #region Path

        # Panel
        mask_set = os.path.join( self.directory_plugin, "MASK" )
        self.mask_set = os.path.join( mask_set, "SPHERE" )

        #endregion
        #region Header

        self.color_header = Color_Header( self.layout.color_header )
        self.color_header.Set_Mode_AB( True ) # FG
        self.color_header.Set_Progress( 1 )
        self.color_header.SIGNAL_SHIFT.connect( self.Header_Shift )
        self.color_header.SIGNAL_SWAP.connect( self.Header_Swap )
        self.color_header.SIGNAL_RANDOM.connect( self.Color_Random )
        self.color_header.SIGNAL_COMP.connect( self.Color_Complementary )
        self.color_header.SIGNAL_ANALYSE.connect( self.Color_AnalyseDocument )

        #endregion
        #region Harmony

        self.harmony_swatch = Harmony_Swatch( self.layout.harmony_swatch )
        self.harmony_swatch.SIGNAL_RULE.connect( self.Harmony_Rule )
        self.harmony_swatch.SIGNAL_EDIT.connect( self.Harmony_Edit )
        self.harmony_swatch.SIGNAL_INDEX.connect( self.Harmony_Index )

        self.harmony_spread = Harmony_Spread( self.layout.harmony_spread )
        self.harmony_spread.SIGNAL_SPAN.connect( self.Harmony_Spread )
        self.harmony_spread.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )

        #endregion
        #region Panel FGC

        self.panel_fill = Panel_Fill( self.layout.panel_fill )

        #endregion
        #region Panel Square

        self.panel_square = Panel_Square( self.layout.panel_square )
        self.panel_square.Init_Convert( self.convert )
        self.panel_square.Set_Tangent_Range( 360 )
        self.panel_square.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", self.wheel_space, "4" ) # Square
        
        self.panel_square.SIGNAL_VALUE.connect( self.Square_Value )
        self.panel_square.SIGNAL_TAN.connect( self.Square_Tangent )
        self.panel_square.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_square.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_square.SIGNAL_PIN_EDIT.connect( self.Square_Pin )

        #endregion
        #region Panel HUE

        self.panel_huecircle = Panel_HueCircle( self.layout.panel_hue )
        self.panel_huecircle.Init_Convert( self.convert )
        self.panel_huecircle.SIGNAL_VALUE.connect( self.HueCircle_Value )
        self.panel_huecircle.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_huecircle.SIGNAL_SUBPANEL.connect( self.HueCircle_SubPanel )

        self.panel_huesubpanel = Panel_Square( self.layout.panel_huesubpanel )
        self.panel_huesubpanel.Init_Convert( self.convert )
        self.panel_huesubpanel.Set_Tangent_Range( 360 )
        self.panel_huesubpanel.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", self.wheel_space, "4" ) # Square
        self.panel_huesubpanel.SIGNAL_VALUE.connect( self.Square_Value )
        self.panel_huesubpanel.SIGNAL_TAN.connect( self.Square_Tangent )
        self.panel_huesubpanel.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_huesubpanel.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_huesubpanel.SIGNAL_PIN_EDIT.connect( self.Square_Pin )

        #endregion
        #region Panel Gamut

        self.panel_gamut = Panel_Gamut( self.layout.panel_gamut )
        self.panel_gamut.Init_Convert( self.convert )
        self.panel_gamut.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", self.wheel_space, "D" ) # DIGITAL
        self.panel_gamut.SIGNAL_VALUE.connect( self.Gamut_Value )
        self.panel_gamut.SIGNAL_TAN.connect( self.Gamut_Tangent )
        self.panel_gamut.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_gamut.SIGNAL_MASK.connect( self.Gamut_Mask )
        self.panel_gamut.SIGNAL_PROFILE.connect( self.Gamut_Profile )
        self.panel_gamut.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_gamut.SIGNAL_PIN_EDIT.connect( self.Gamut_Pin )

        #endregion
        #region Panel Hexagon

        self.panel_hexagon = Panel_Hexagon( self.layout.panel_hexagon )
        self.panel_hexagon.Init_Convert( self.convert )
        self.panel_hexagon.Set_ColorSpace_inDocument( self.directory_plugin, "RGB" )

        self.panel_hexagon.SIGNAL_VALUE.connect( self.Hexagon_Value )
        self.panel_hexagon.SIGNAL_TAN.connect( self.Hexagon_Depth )
        self.panel_hexagon.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_hexagon.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_hexagon.SIGNAL_PIN_EDIT.connect( self.Hexagon_Pin )

        #endregion
        #region Panel Luma

        self.panel_luma = Panel_Square( self.layout.panel_luma )
        self.panel_luma.Init_Convert( self.convert )
        self.panel_luma.Set_Tangent_Range( 255 )
        self.panel_luma.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", "YUV", "4" ) # Square

        self.panel_luma.SIGNAL_VALUE.connect( self.Luma_Value )
        self.panel_luma.SIGNAL_TAN.connect( self.Luma_Tangent )
        self.panel_luma.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_luma.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_luma.SIGNAL_PIN_EDIT.connect( self.Luma_Pin )

        #endregion
        #region Panel Dot

        self.panel_dot = Panel_Dot( self.layout.panel_dot )
        self.panel_dot.Init_Convert( self.convert )
        self.panel_dot.SIGNAL_VALUE.connect( self.Dot_Value )
        self.panel_dot.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_dot.SIGNAL_INTERPOLATION.connect( self.Dot_Interpolation )
        self.panel_dot.SIGNAL_DIMENSION.connect( self.Dot_Dimension )
        self.panel_dot.SIGNAL_EDIT.connect( self.Dot_Edit )
        self.panel_dot.SIGNAL_ZORN.connect( self.Dot_Zorn )

        #endregion
        #region Dot Pins

        self.pin_d1 = Pin_Color( self.layout.dot_1 )
        self.pin_d1.SIGNAL_APPLY.connect( self.Dot_Apply_1 )
        self.pin_d1.SIGNAL_SAVE.connect( self.Dot_Save_1 )
        self.pin_d1.SIGNAL_CLEAN.connect( self.Dot_Clean_1 )
        self.pin_d1.SIGNAL_TEXT.connect( self.Label_String )

        self.pin_d2 = Pin_Color( self.layout.dot_2 )
        self.pin_d2.SIGNAL_APPLY.connect( self.Dot_Apply_2 )
        self.pin_d2.SIGNAL_SAVE.connect( self.Dot_Save_2 )
        self.pin_d2.SIGNAL_CLEAN.connect( self.Dot_Clean_2 )
        self.pin_d2.SIGNAL_TEXT.connect( self.Label_String )

        self.pin_d3 = Pin_Color( self.layout.dot_3 )
        self.pin_d3.SIGNAL_APPLY.connect( self.Dot_Apply_3 )
        self.pin_d3.SIGNAL_SAVE.connect( self.Dot_Save_3 )
        self.pin_d3.SIGNAL_CLEAN.connect( self.Dot_Clean_3 )
        self.pin_d3.SIGNAL_TEXT.connect( self.Label_String )

        self.pin_d4 = Pin_Color( self.layout.dot_4 )
        self.pin_d4.SIGNAL_APPLY.connect( self.Dot_Apply_4 )
        self.pin_d4.SIGNAL_SAVE.connect( self.Dot_Save_4 )
        self.pin_d4.SIGNAL_CLEAN.connect( self.Dot_Clean_4 )
        self.pin_d4.SIGNAL_TEXT.connect( self.Label_String )

        #endregion
        #region Panel Mask

        self.panel_mask = Panel_Mask( self.layout.panel_mask )
        self.panel_mask.Set_Directory( os.path.join( self.directory_plugin, "MASK" ) )
        self.panel_mask.SIGNAL_VALUE.connect( self.Mask_Value )
        self.panel_mask.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.panel_mask.SIGNAL_MASKSET.connect( self.Mask_Set )
        self.panel_mask.SIGNAL_EDIT.connect( self.Mask_Edit )
        self.panel_mask.SIGNAL_RESET.connect( self.Mask_Read )

        #endregion
        #region Mask Pins

        self.mask_f3 = Pin_Color( self.layout.fg_3_color )
        self.mask_f2 = Pin_Color( self.layout.fg_2_color )
        self.mask_f1 = Pin_Color( self.layout.fg_1_color )
        self.mask_d6 = Pin_Color( self.layout.dif_6_color )
        self.mask_d5 = Pin_Color( self.layout.dif_5_color )
        self.mask_d4 = Pin_Color( self.layout.dif_4_color )
        self.mask_d3 = Pin_Color( self.layout.dif_3_color )
        self.mask_d2 = Pin_Color( self.layout.dif_2_color )
        self.mask_d1 = Pin_Color( self.layout.dif_1_color )
        self.mask_b3 = Pin_Color( self.layout.bg_3_color )
        self.mask_b2 = Pin_Color( self.layout.bg_2_color )
        self.mask_b1 = Pin_Color( self.layout.bg_1_color )

        self.mask_f3.Set_Alpha( 1.0 )
        self.mask_f2.Set_Alpha( 1.0 )
        self.mask_f1.Set_Alpha( 1.0 )
        self.mask_d6.Set_Alpha( 1.0 )
        self.mask_d5.Set_Alpha( 1.0 )
        self.mask_d4.Set_Alpha( 1.0 )
        self.mask_d3.Set_Alpha( 1.0 )
        self.mask_d2.Set_Alpha( 1.0 )
        self.mask_d1.Set_Alpha( 1.0 )
        self.mask_b3.Set_Alpha( 1.0 )
        self.mask_b2.Set_Alpha( 1.0 )
        self.mask_b1.Set_Alpha( 1.0 )

        self.mask_f3.SIGNAL_APPLY.connect( self.Mask_Apply_F3 )
        self.mask_f2.SIGNAL_APPLY.connect( self.Mask_Apply_F2 )
        self.mask_f1.SIGNAL_APPLY.connect( self.Mask_Apply_F1 )
        self.mask_d6.SIGNAL_APPLY.connect( self.Mask_Apply_D6 )
        self.mask_d5.SIGNAL_APPLY.connect( self.Mask_Apply_D5 )
        self.mask_d4.SIGNAL_APPLY.connect( self.Mask_Apply_D4 )
        self.mask_d3.SIGNAL_APPLY.connect( self.Mask_Apply_D3 )
        self.mask_d2.SIGNAL_APPLY.connect( self.Mask_Apply_D2 )
        self.mask_d1.SIGNAL_APPLY.connect( self.Mask_Apply_D1 )
        self.mask_b3.SIGNAL_APPLY.connect( self.Mask_Apply_B3 )
        self.mask_b2.SIGNAL_APPLY.connect( self.Mask_Apply_B2 )
        self.mask_b1.SIGNAL_APPLY.connect( self.Mask_Apply_B1 )

        self.mask_f3.SIGNAL_SAVE.connect( self.Mask_Save_F3 )
        self.mask_f2.SIGNAL_SAVE.connect( self.Mask_Save_F2 )
        self.mask_f1.SIGNAL_SAVE.connect( self.Mask_Save_F1 )
        self.mask_d6.SIGNAL_SAVE.connect( self.Mask_Save_D6 )
        self.mask_d5.SIGNAL_SAVE.connect( self.Mask_Save_D5 )
        self.mask_d4.SIGNAL_SAVE.connect( self.Mask_Save_D4 )
        self.mask_d3.SIGNAL_SAVE.connect( self.Mask_Save_D3 )
        self.mask_d2.SIGNAL_SAVE.connect( self.Mask_Save_D2 )
        self.mask_d1.SIGNAL_SAVE.connect( self.Mask_Save_D1 )
        self.mask_b3.SIGNAL_SAVE.connect( self.Mask_Save_B3 )
        self.mask_b2.SIGNAL_SAVE.connect( self.Mask_Save_B2 )
        self.mask_b1.SIGNAL_SAVE.connect( self.Mask_Save_B1 )

        self.mask_f3.SIGNAL_CLEAN.connect( self.Mask_Clean_F3 )
        self.mask_f2.SIGNAL_CLEAN.connect( self.Mask_Clean_F2 )
        self.mask_f1.SIGNAL_CLEAN.connect( self.Mask_Clean_F1 )
        self.mask_d6.SIGNAL_CLEAN.connect( self.Mask_Clean_D6 )
        self.mask_d5.SIGNAL_CLEAN.connect( self.Mask_Clean_D5 )
        self.mask_d4.SIGNAL_CLEAN.connect( self.Mask_Clean_D4 )
        self.mask_d3.SIGNAL_CLEAN.connect( self.Mask_Clean_D3 )
        self.mask_d2.SIGNAL_CLEAN.connect( self.Mask_Clean_D2 )
        self.mask_d1.SIGNAL_CLEAN.connect( self.Mask_Clean_D1 )
        self.mask_b3.SIGNAL_CLEAN.connect( self.Mask_Clean_B3 )
        self.mask_b2.SIGNAL_CLEAN.connect( self.Mask_Clean_B2 )
        self.mask_b1.SIGNAL_CLEAN.connect( self.Mask_Clean_B1 )

        self.mask_f3.SIGNAL_ALPHA.connect( self.Mask_Alpha_F3 )
        self.mask_f2.SIGNAL_ALPHA.connect( self.Mask_Alpha_F2 )
        self.mask_f1.SIGNAL_ALPHA.connect( self.Mask_Alpha_F1 )
        self.mask_d6.SIGNAL_ALPHA.connect( self.Mask_Alpha_D6 )
        self.mask_d5.SIGNAL_ALPHA.connect( self.Mask_Alpha_D5 )
        self.mask_d4.SIGNAL_ALPHA.connect( self.Mask_Alpha_D4 )
        self.mask_d3.SIGNAL_ALPHA.connect( self.Mask_Alpha_D3 )
        self.mask_d2.SIGNAL_ALPHA.connect( self.Mask_Alpha_D2 )
        self.mask_d1.SIGNAL_ALPHA.connect( self.Mask_Alpha_D1 )
        self.mask_b3.SIGNAL_ALPHA.connect( self.Mask_Alpha_B3 )
        self.mask_b2.SIGNAL_ALPHA.connect( self.Mask_Alpha_B2 )
        self.mask_b1.SIGNAL_ALPHA.connect( self.Mask_Alpha_B1 )

        self.mask_f3.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_f2.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_f1.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_d6.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_d5.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_d4.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_d3.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_d2.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_d1.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_b3.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_b2.SIGNAL_TEXT.connect( self.Label_String )
        self.mask_b1.SIGNAL_TEXT.connect( self.Label_String )

        #endregion
        #region Sliders Module

        # AAA
        self.aaa_1_slider = Channel_Slider( self.layout.aaa_1_slider )
        self.aaa_1_slider.Set_Mode( "LINEAR" )
        self.aaa_1_slider.Set_Limits( 0, 0.5, 1 )
        self.aaa_1_slider.Set_Stops( stops["aaa_1"] )
        # RGB
        self.rgb_1_slider = Channel_Slider( self.layout.rgb_1_slider )
        self.rgb_2_slider = Channel_Slider( self.layout.rgb_2_slider )
        self.rgb_3_slider = Channel_Slider( self.layout.rgb_3_slider )
        self.rgb_1_slider.Set_Mode( "LINEAR" )
        self.rgb_2_slider.Set_Mode( "LINEAR" )
        self.rgb_3_slider.Set_Mode( "LINEAR" )
        self.rgb_1_slider.Set_Limits( 0, 0.5, 1 )
        self.rgb_2_slider.Set_Limits( 0, 0.5, 1 )
        self.rgb_3_slider.Set_Limits( 0, 0.5, 1 )
        self.rgb_1_slider.Set_Stops( stops["rgb_1"] )
        self.rgb_2_slider.Set_Stops( stops["rgb_2"] )
        self.rgb_3_slider.Set_Stops( stops["rgb_3"] )
        # CMY
        self.cmy_1_slider = Channel_Slider( self.layout.cmy_1_slider )
        self.cmy_2_slider = Channel_Slider( self.layout.cmy_2_slider )
        self.cmy_3_slider = Channel_Slider( self.layout.cmy_3_slider )
        self.cmy_1_slider.Set_Mode( "LINEAR" )
        self.cmy_2_slider.Set_Mode( "LINEAR" )
        self.cmy_3_slider.Set_Mode( "LINEAR" )
        self.cmy_1_slider.Set_Limits( 0, 0.5, 1 )
        self.cmy_2_slider.Set_Limits( 0, 0.5, 1 )
        self.cmy_3_slider.Set_Limits( 0, 0.5, 1 )
        self.cmy_1_slider.Set_Stops( stops["cmy_1"] )
        self.cmy_2_slider.Set_Stops( stops["cmy_2"] )
        self.cmy_3_slider.Set_Stops( stops["cmy_3"] )
        # CMYK
        self.cmyk_1_slider = Channel_Slider( self.layout.cmyk_1_slider )
        self.cmyk_2_slider = Channel_Slider( self.layout.cmyk_2_slider )
        self.cmyk_3_slider = Channel_Slider( self.layout.cmyk_3_slider )
        self.cmyk_4_slider = Channel_Slider( self.layout.cmyk_4_slider )
        self.cmyk_1_slider.Set_Mode( "LINEAR" )
        self.cmyk_2_slider.Set_Mode( "LINEAR" )
        self.cmyk_3_slider.Set_Mode( "LINEAR" )
        self.cmyk_4_slider.Set_Mode( "LINEAR" )
        self.cmyk_1_slider.Set_Limits( 0, 0.5, 1 )
        self.cmyk_2_slider.Set_Limits( 0, 0.5, 1 )
        self.cmyk_3_slider.Set_Limits( 0, 0.5, 1 )
        self.cmyk_4_slider.Set_Limits( 0, 0.5, 1 )
        self.cmyk_1_slider.Set_Stops( stops["cmyk_1"] )
        self.cmyk_2_slider.Set_Stops( stops["cmyk_2"] )
        self.cmyk_3_slider.Set_Stops( stops["cmyk_3"] )
        self.cmyk_4_slider.Set_Stops( stops["cmyk_4"] )
        # RYB
        self.ryb_1_slider = Channel_Slider( self.layout.ryb_1_slider )
        self.ryb_2_slider = Channel_Slider( self.layout.ryb_2_slider )
        self.ryb_3_slider = Channel_Slider( self.layout.ryb_3_slider )
        self.ryb_1_slider.Set_Mode( "LINEAR" )
        self.ryb_2_slider.Set_Mode( "LINEAR" )
        self.ryb_3_slider.Set_Mode( "LINEAR" )
        self.ryb_1_slider.Set_Limits( 0, 0.5, 1 )
        self.ryb_2_slider.Set_Limits( 0, 0.5, 1 )
        self.ryb_3_slider.Set_Limits( 0, 0.5, 1 )
        self.ryb_1_slider.Set_Stops( stops["ryb_1"] )
        self.ryb_2_slider.Set_Stops( stops["ryb_2"] )
        self.ryb_3_slider.Set_Stops( stops["ryb_3"] )
        # YUV
        self.yuv_1_slider = Channel_Slider( self.layout.yuv_1_slider )
        self.yuv_2_slider = Channel_Slider( self.layout.yuv_2_slider )
        self.yuv_3_slider = Channel_Slider( self.layout.yuv_3_slider )
        self.yuv_1_slider.Set_Mode( "LINEAR" )
        self.yuv_2_slider.Set_Mode( "LINEAR" )
        self.yuv_3_slider.Set_Mode( "LINEAR" )
        self.yuv_1_slider.Set_Limits( 0, 0.5, 1 )
        self.yuv_2_slider.Set_Limits( 0, 0.5, 1 )
        self.yuv_3_slider.Set_Limits( 0, 0.5, 1 )
        self.yuv_1_slider.Set_Stops( stops["yuv_1"] )
        self.yuv_2_slider.Set_Stops( stops["yuv_2"] )
        self.yuv_3_slider.Set_Stops( stops["yuv_3"] )

        # HSV
        self.hsv_1_slider = Channel_Slider( self.layout.hsv_1_slider )
        self.hsv_2_slider = Channel_Slider( self.layout.hsv_2_slider )
        self.hsv_3_slider = Channel_Slider( self.layout.hsv_3_slider )
        self.hsv_1_slider.Set_Mode( "CIRCULAR" )
        self.hsv_2_slider.Set_Mode( "LINEAR" )
        self.hsv_3_slider.Set_Mode( "LINEAR" )
        self.hsv_1_slider.Set_Limits( 0, 0.5, 1 )
        self.hsv_2_slider.Set_Limits( 0, 0.5, 1 )
        self.hsv_3_slider.Set_Limits( 0, 0.5, 1 )
        self.hsv_1_slider.Set_Stops( stops["hsv_1"] )
        self.hsv_2_slider.Set_Stops( stops["hsv_2"] )
        self.hsv_3_slider.Set_Stops( stops["hsv_3"] )
        # HSL
        self.hsl_1_slider = Channel_Slider( self.layout.hsl_1_slider )
        self.hsl_2_slider = Channel_Slider( self.layout.hsl_2_slider )
        self.hsl_3_slider = Channel_Slider( self.layout.hsl_3_slider )
        self.hsl_1_slider.Set_Mode( "CIRCULAR" )
        self.hsl_2_slider.Set_Mode( "LINEAR" )
        self.hsl_3_slider.Set_Mode( "LINEAR" )
        self.hsl_1_slider.Set_Limits( 0, 0.5, 1 )
        self.hsl_2_slider.Set_Limits( 0, 0.5, 1 )
        self.hsl_3_slider.Set_Limits( 0, 0.5, 1 )
        self.hsl_1_slider.Set_Stops( stops["hsl_1"] )
        self.hsl_2_slider.Set_Stops( stops["hsl_2"] )
        self.hsl_3_slider.Set_Stops( stops["hsl_3"] )
        # HSY
        self.hsy_1_slider = Channel_Slider( self.layout.hsy_1_slider )
        self.hsy_2_slider = Channel_Slider( self.layout.hsy_2_slider )
        self.hsy_3_slider = Channel_Slider( self.layout.hsy_3_slider )
        self.hsy_1_slider.Set_Mode( "CIRCULAR" )
        self.hsy_2_slider.Set_Mode( "LINEAR" )
        self.hsy_3_slider.Set_Mode( "LINEAR" )
        self.hsy_1_slider.Set_Limits( 0, 0.5, 1 )
        self.hsy_2_slider.Set_Limits( 0, 0.5, 1 )
        self.hsy_3_slider.Set_Limits( 0, 0.5, 1 )
        self.hsy_1_slider.Set_Stops( stops["hsy_1"] )
        self.hsy_2_slider.Set_Stops( stops["hsy_2"] )
        self.hsy_3_slider.Set_Stops( stops["hsy_3"] )
        # ARD
        self.ard_1_slider = Channel_Slider( self.layout.ard_1_slider )
        self.ard_2_slider = Channel_Slider( self.layout.ard_2_slider )
        self.ard_3_slider = Channel_Slider( self.layout.ard_3_slider )
        self.ard_1_slider.Set_Mode( "CIRCULAR" )
        self.ard_2_slider.Set_Mode( "LINEAR" )
        self.ard_3_slider.Set_Mode( "LINEAR" )
        self.ard_1_slider.Set_Limits( 0, 0.5, 1 )
        self.ard_2_slider.Set_Limits( 0, 0.5, 1 )
        self.ard_3_slider.Set_Limits( 0, 0.5, 1 )
        self.ard_1_slider.Set_Stops( stops["ard_1"] )
        self.ard_2_slider.Set_Stops( stops["ard_2"] )
        self.ard_3_slider.Set_Stops( stops["ard_3"] )

        # XYZ
        self.xyz_1_slider = Channel_Slider( self.layout.xyz_1_slider )
        self.xyz_2_slider = Channel_Slider( self.layout.xyz_2_slider )
        self.xyz_3_slider = Channel_Slider( self.layout.xyz_3_slider )
        self.xyz_1_slider.Set_Mode( "LINEAR" )
        self.xyz_2_slider.Set_Mode( "LINEAR" )
        self.xyz_3_slider.Set_Mode( "LINEAR" )
        self.xyz_1_slider.Set_Limits( 0, 0.5, 1 )
        self.xyz_2_slider.Set_Limits( 0, 0.5, 1 )
        self.xyz_3_slider.Set_Limits( 0, 0.5, 1 )
        self.xyz_1_slider.Set_Stops( stops["xyz_1"] )
        self.xyz_2_slider.Set_Stops( stops["xyz_2"] )
        self.xyz_3_slider.Set_Stops( stops["xyz_3"] )
        # XYY
        self.xyy_1_slider = Channel_Slider( self.layout.xyy_1_slider )
        self.xyy_2_slider = Channel_Slider( self.layout.xyy_2_slider )
        self.xyy_3_slider = Channel_Slider( self.layout.xyy_3_slider )
        self.xyy_1_slider.Set_Mode( "LINEAR" )
        self.xyy_2_slider.Set_Mode( "LINEAR" )
        self.xyy_3_slider.Set_Mode( "LINEAR" )
        self.xyy_1_slider.Set_Limits( 0, 0.5, 1 )
        self.xyy_2_slider.Set_Limits( 0, 0.5, 1 )
        self.xyy_3_slider.Set_Limits( 0, 0.5, 1 )
        self.xyy_1_slider.Set_Stops( stops["xyy_1"] )
        self.xyy_2_slider.Set_Stops( stops["xyy_2"] )
        self.xyy_3_slider.Set_Stops( stops["xyy_3"] )
        # LAB
        self.lab_1_slider = Channel_Slider( self.layout.lab_1_slider )
        self.lab_2_slider = Channel_Slider( self.layout.lab_2_slider )
        self.lab_3_slider = Channel_Slider( self.layout.lab_3_slider )
        self.lab_1_slider.Set_Mode( "LINEAR" )
        self.lab_2_slider.Set_Mode( "LINEAR" )
        self.lab_3_slider.Set_Mode( "LINEAR" )
        self.lab_1_slider.Set_Limits( 0, 0.5, 1 )
        self.lab_2_slider.Set_Limits( 0, 0.5, 1 )
        self.lab_3_slider.Set_Limits( 0, 0.5, 1 )
        self.lab_1_slider.Set_Stops( stops["lab_1"] )
        self.lab_2_slider.Set_Stops( stops["lab_2"] )
        self.lab_3_slider.Set_Stops( stops["lab_3"] )

        # LCH
        self.lch_1_slider = Channel_Slider( self.layout.lch_1_slider )
        self.lch_2_slider = Channel_Slider( self.layout.lch_2_slider )
        self.lch_3_slider = Channel_Slider( self.layout.lch_3_slider )
        self.lch_1_slider.Set_Mode( "LINEAR" )
        self.lch_2_slider.Set_Mode( "LINEAR" )
        self.lch_3_slider.Set_Mode( "CIRCULAR" )
        self.lch_1_slider.Set_Limits( 0, 0.5, 1 )
        self.lch_2_slider.Set_Limits( 0, 0.5, 1 )
        self.lch_3_slider.Set_Limits( 0, 0.5, 1 )
        self.lch_1_slider.Set_Stops( stops["lch_1"] )
        self.lch_2_slider.Set_Stops( stops["lch_2"] )
        self.lch_3_slider.Set_Stops( stops["lch_3"] )

        #endregion
        #region Sliders Connects

        # AAA 1
        self.aaa_1_slider.SIGNAL_VALUE.connect( self.Channels_AAA_1_Slider )
        self.aaa_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.aaa_1_slider.SIGNAL_STOPS.connect( self.Channels_AAA_1_Stops )
        self.aaa_1_slider.SIGNAL_TEXT.connect( self.Label_String )

        # RGB 1
        self.rgb_1_slider.SIGNAL_VALUE.connect( self.Channels_RGB_1_Slider )
        self.rgb_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.rgb_1_slider.SIGNAL_STOPS.connect( self.Channels_RGB_1_Stops )
        self.rgb_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # RGB 2
        self.rgb_2_slider.SIGNAL_VALUE.connect( self.Channels_RGB_2_Slider )
        self.rgb_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.rgb_2_slider.SIGNAL_STOPS.connect( self.Channels_RGB_2_Stops )
        self.rgb_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # RGB 3
        self.rgb_3_slider.SIGNAL_VALUE.connect( self.Channels_RGB_3_Slider )
        self.rgb_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.rgb_3_slider.SIGNAL_STOPS.connect( self.Channels_RGB_3_Stops )
        self.rgb_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # CMY 1
        self.cmy_1_slider.SIGNAL_VALUE.connect( self.Channels_CMY_1_Slider )
        self.cmy_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmy_1_slider.SIGNAL_STOPS.connect( self.Channels_CMY_1_Stops )
        self.cmy_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # CMY 2
        self.cmy_2_slider.SIGNAL_VALUE.connect( self.Channels_CMY_2_Slider )
        self.cmy_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmy_2_slider.SIGNAL_STOPS.connect( self.Channels_CMY_2_Stops )
        self.cmy_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # CMY 3
        self.cmy_3_slider.SIGNAL_VALUE.connect( self.Channels_CMY_3_Slider )
        self.cmy_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmy_3_slider.SIGNAL_STOPS.connect( self.Channels_CMY_3_Stops )
        self.cmy_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # CMYK 1
        self.cmyk_1_slider.SIGNAL_VALUE.connect( self.Channels_CMYK_1_Slider )
        self.cmyk_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmyk_1_slider.SIGNAL_STOPS.connect( self.Channels_CMYK_1_Stops )
        self.cmyk_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # CMYK 2
        self.cmyk_2_slider.SIGNAL_VALUE.connect( self.Channels_CMYK_2_Slider )
        self.cmyk_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmyk_2_slider.SIGNAL_STOPS.connect( self.Channels_CMYK_2_Stops )
        self.cmyk_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # CMYK 3
        self.cmyk_3_slider.SIGNAL_VALUE.connect( self.Channels_CMYK_3_Slider )
        self.cmyk_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmyk_3_slider.SIGNAL_STOPS.connect( self.Channels_CMYK_3_Stops )
        self.cmyk_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        # CMYK 4
        self.cmyk_4_slider.SIGNAL_VALUE.connect( self.Channels_CMYK_4_Slider )
        self.cmyk_4_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.cmyk_4_slider.SIGNAL_STOPS.connect( self.Channels_CMYK_4_Stops )
        self.cmyk_4_slider.SIGNAL_TEXT.connect( self.Label_String )

        # RYB 1
        self.ryb_1_slider.SIGNAL_VALUE.connect( self.Channels_RYB_1_Slider )
        self.ryb_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.ryb_1_slider.SIGNAL_STOPS.connect( self.Channels_RYB_1_Stops )
        self.ryb_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # RYB 2
        self.ryb_2_slider.SIGNAL_VALUE.connect( self.Channels_RYB_2_Slider )
        self.ryb_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.ryb_2_slider.SIGNAL_STOPS.connect( self.Channels_RYB_2_Stops )
        self.ryb_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # RYB 3
        self.ryb_3_slider.SIGNAL_VALUE.connect( self.Channels_RYB_3_Slider )
        self.ryb_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.ryb_3_slider.SIGNAL_STOPS.connect( self.Channels_RYB_3_Stops )
        self.ryb_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # YUV 1
        self.yuv_1_slider.SIGNAL_VALUE.connect( self.Channels_YUV_1_Slider )
        self.yuv_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.yuv_1_slider.SIGNAL_STOPS.connect( self.Channels_YUV_1_Stops )
        self.yuv_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # YUV 2
        self.yuv_2_slider.SIGNAL_VALUE.connect( self.Channels_YUV_2_Slider )
        self.yuv_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.yuv_2_slider.SIGNAL_STOPS.connect( self.Channels_YUV_2_Stops )
        self.yuv_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # YUV 3
        self.yuv_3_slider.SIGNAL_VALUE.connect( self.Channels_YUV_3_Slider )
        self.yuv_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.yuv_3_slider.SIGNAL_STOPS.connect( self.Channels_YUV_3_Stops )
        self.yuv_3_slider.SIGNAL_TEXT.connect( self.Label_String )


        # HSV 1
        self.hsv_1_slider.SIGNAL_VALUE.connect( self.Channels_HSV_1_Slider )
        self.hsv_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsv_1_slider.SIGNAL_STOPS.connect( self.Channels_HSV_1_Stops )
        self.hsv_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # HSV 2
        self.hsv_2_slider.SIGNAL_VALUE.connect( self.Channels_HSV_2_Slider )
        self.hsv_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsv_2_slider.SIGNAL_STOPS.connect( self.Channels_HSV_2_Stops )
        self.hsv_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # HSV 3
        self.hsv_3_slider.SIGNAL_VALUE.connect( self.Channels_HSV_3_Slider )
        self.hsv_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsv_3_slider.SIGNAL_STOPS.connect( self.Channels_HSV_3_Stops )
        self.hsv_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # HSL 1
        self.hsl_1_slider.SIGNAL_VALUE.connect( self.Channels_HSL_1_Slider )
        self.hsl_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsl_1_slider.SIGNAL_STOPS.connect( self.Channels_HSL_1_Stops )
        self.hsl_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # HSL 2
        self.hsl_2_slider.SIGNAL_VALUE.connect( self.Channels_HSL_2_Slider )
        self.hsl_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsl_2_slider.SIGNAL_STOPS.connect( self.Channels_HSL_2_Stops )
        self.hsl_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # HSL 3
        self.hsl_3_slider.SIGNAL_VALUE.connect( self.Channels_HSL_3_Slider )
        self.hsl_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsl_3_slider.SIGNAL_STOPS.connect( self.Channels_HSL_3_Stops )
        self.hsl_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # HSY 1
        self.hsy_1_slider.SIGNAL_VALUE.connect( self.Channels_HSY_1_Slider )
        self.hsy_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsy_1_slider.SIGNAL_STOPS.connect( self.Channels_HSY_1_Stops )
        self.hsy_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # HSY 2
        self.hsy_2_slider.SIGNAL_VALUE.connect( self.Channels_HSY_2_Slider )
        self.hsy_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsy_2_slider.SIGNAL_STOPS.connect( self.Channels_HSY_2_Stops )
        self.hsy_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # HSY 3
        self.hsy_3_slider.SIGNAL_VALUE.connect( self.Channels_HSY_3_Slider )
        self.hsy_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.hsy_3_slider.SIGNAL_STOPS.connect( self.Channels_HSY_3_Stops )
        self.hsy_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # ARD 1
        self.ard_1_slider.SIGNAL_VALUE.connect( self.Channels_ARD_1_Slider )
        self.ard_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.ard_1_slider.SIGNAL_STOPS.connect( self.Channels_ARD_1_Stops )
        self.ard_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # ARD 2
        self.ard_2_slider.SIGNAL_VALUE.connect( self.Channels_ARD_2_Slider )
        self.ard_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.ard_2_slider.SIGNAL_STOPS.connect( self.Channels_ARD_2_Stops )
        self.ard_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # ARD 3
        self.ard_3_slider.SIGNAL_VALUE.connect( self.Channels_ARD_3_Slider )
        self.ard_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.ard_3_slider.SIGNAL_STOPS.connect( self.Channels_ARD_3_Stops )
        self.ard_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # XYZ 1
        self.xyz_1_slider.SIGNAL_VALUE.connect( self.Channels_XYZ_1_Slider )
        self.xyz_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.xyz_1_slider.SIGNAL_STOPS.connect( self.Channels_XYZ_1_Stops )
        self.xyz_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # XYZ 2
        self.xyz_2_slider.SIGNAL_VALUE.connect( self.Channels_XYZ_2_Slider )
        self.xyz_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.xyz_2_slider.SIGNAL_STOPS.connect( self.Channels_XYZ_2_Stops )
        self.xyz_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # XYZ 3
        self.xyz_3_slider.SIGNAL_VALUE.connect( self.Channels_XYZ_3_Slider )
        self.xyz_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.xyz_3_slider.SIGNAL_STOPS.connect( self.Channels_XYZ_3_Stops )
        self.xyz_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # XYY 1
        self.xyy_1_slider.SIGNAL_VALUE.connect( self.Channels_XYY_1_Slider )
        self.xyy_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.xyy_1_slider.SIGNAL_STOPS.connect( self.Channels_XYY_1_Stops )
        self.xyy_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # XYY 2
        self.xyy_2_slider.SIGNAL_VALUE.connect( self.Channels_XYY_2_Slider )
        self.xyy_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.xyy_2_slider.SIGNAL_STOPS.connect( self.Channels_XYY_2_Stops )
        self.xyy_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # XYY 3
        self.xyy_3_slider.SIGNAL_VALUE.connect( self.Channels_XYY_3_Slider )
        self.xyy_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.xyy_3_slider.SIGNAL_STOPS.connect( self.Channels_XYY_3_Stops )
        self.xyy_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # LAB 1
        self.lab_1_slider.SIGNAL_VALUE.connect( self.Channels_LAB_1_Slider )
        self.lab_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.lab_1_slider.SIGNAL_STOPS.connect( self.Channels_LAB_1_Stops )
        self.lab_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # LAB 2
        self.lab_2_slider.SIGNAL_VALUE.connect( self.Channels_LAB_2_Slider )
        self.lab_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.lab_2_slider.SIGNAL_STOPS.connect( self.Channels_LAB_2_Stops )
        self.lab_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # LAB 3
        self.lab_3_slider.SIGNAL_VALUE.connect( self.Channels_LAB_3_Slider )
        self.lab_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.lab_3_slider.SIGNAL_STOPS.connect( self.Channels_LAB_3_Stops )
        self.lab_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        # LCH 1
        self.lch_1_slider.SIGNAL_VALUE.connect( self.Channels_LCH_1_Slider )
        self.lch_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.lch_1_slider.SIGNAL_STOPS.connect( self.Channels_LCH_1_Stops )
        self.lch_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        # LCH 2
        self.lch_2_slider.SIGNAL_VALUE.connect( self.Channels_LCH_2_Slider )
        self.lch_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.lch_2_slider.SIGNAL_STOPS.connect( self.Channels_LCH_2_Stops )
        self.lch_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        # LCH 3
        self.lch_3_slider.SIGNAL_VALUE.connect( self.Channels_LCH_3_Slider )
        self.lch_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.lch_3_slider.SIGNAL_STOPS.connect( self.Channels_LCH_3_Stops )
        self.lch_3_slider.SIGNAL_TEXT.connect( self.Label_String )

        #endregion
        #region Sliders Non Color

        # Kelvin
        self.kkk_1_slider = Channel_Slider( self.layout.kkk_1_slider )
        self.kkk_1_slider.Set_Mode( "LINEAR" )
        self.kkk_1_slider.Set_Limits( 0, 0.5, 1 )
        self.kkk_1_slider.Set_Stops( 4 )
        self.kkk_1_slider.SIGNAL_VALUE.connect( self.Channels_KKK_1_Slider )
        self.kkk_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.kkk_1_slider.SIGNAL_STOPS.connect( self.Channels_KKK_1_Stops )
        self.kkk_1_slider.SIGNAL_TEXT.connect( self.Label_String )

        # SELE 1
        self.sele_1_slider = Channel_Selection( self.layout.sele_1_slider )
        self.sele_1_slider.SIGNAL_VALUE.connect( self.Channels_SELE_1_Slider )
        self.sele_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.sele_1_slider.SIGNAL_RESET.connect( self.Channels_SELE_1_Reset )
        # SELE 2
        self.sele_2_slider = Channel_Selection( self.layout.sele_2_slider )
        self.sele_2_slider.SIGNAL_VALUE.connect( self.Channels_SELE_2_Slider )
        self.sele_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.sele_2_slider.SIGNAL_RESET.connect( self.Channels_SELE_2_Reset )
        # SELE 3
        self.sele_3_slider = Channel_Selection( self.layout.sele_3_slider )
        self.sele_3_slider.SIGNAL_VALUE.connect( self.Channels_SELE_3_Slider )
        self.sele_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.sele_3_slider.SIGNAL_RESET.connect( self.Channels_SELE_3_Reset )
        # SELE 4
        self.sele_4_slider = Channel_Selection( self.layout.sele_4_slider )
        self.sele_4_slider.SIGNAL_VALUE.connect( self.Channels_SELE_4_Slider )
        self.sele_4_slider.SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.sele_4_slider.SIGNAL_RESET.connect( self.Channels_SELE_4_Reset )

        #endregion
        #region Mixer

        self.mixer_module = [ {
            "l" : Pin_Color( self.mixer_widget[0]["l"] ),
            "m" : Channel_Slider( self.mixer_widget[0]["m"] ),
            "r" : Pin_Color( self.mixer_widget[0]["r"] ),
            } ]

        # Left
        self.mixer_module[0]["l"].Set_Index( 0 )
        self.mixer_module[0]["l"].SIGNAL_APPLY.connect( self.Mixer_Apply_L )
        self.mixer_module[0]["l"].SIGNAL_SAVE.connect( self.Mixer_Save_L )
        self.mixer_module[0]["l"].SIGNAL_CLEAN.connect( self.Mixer_Clean_L )
        self.mixer_module[0]["l"].SIGNAL_TEXT.connect( self.Label_String )

        # Gradient
        self.mixer_module[0]["m"].Set_Index( 0 )
        self.mixer_module[0]["m"].Set_Mode( "MIXER" )
        self.mixer_module[0]["m"].Set_Limits( 0, 0.5, 1 )
        self.mixer_module[0]["m"].Set_Stops( 2 )
        self.mixer_module[0]["m"].SIGNAL_VALUE.connect( self.Mixer_Slider_M )
        self.mixer_module[0]["m"].SIGNAL_STOPS.connect( self.Mixer_Stops_M )
        self.mixer_module[0]["m"].SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
        self.mixer_module[0]["m"].SIGNAL_TEXT.connect( self.Label_String )

        # Right
        self.mixer_module[0]["r"].Set_Index( 0 )
        self.mixer_module[0]["r"].SIGNAL_APPLY.connect( self.Mixer_Apply_R )
        self.mixer_module[0]["r"].SIGNAL_SAVE.connect( self.Mixer_Save_R )
        self.mixer_module[0]["r"].SIGNAL_CLEAN.connect( self.Mixer_Clean_R )
        self.mixer_module[0]["r"].SIGNAL_TEXT.connect( self.Label_String )

        #endregion
        #region Pin

        self.pin_widget = [
            self.layout.pin_00,
            self.layout.pin_01,
            self.layout.pin_02,
            self.layout.pin_03,
            self.layout.pin_04,
            self.layout.pin_05,
            self.layout.pin_06,
            self.layout.pin_07,
            self.layout.pin_08,
            self.layout.pin_09,
            self.layout.pin_10,
            ]
        length = len( self.pin_widget )
        for i in range( 0, length ):
            self.pin_module.append( Pin_Color( self.pin_widget[i] ) )
        for i in range( 0, length ):
            self.pin_module[i].Set_Index( i )
            self.pin_module[i].SIGNAL_APPLY.connect( self.Pin_Apply )
            self.pin_module[i].SIGNAL_SAVE.connect( self.Pin_Save )
            self.pin_module[i].SIGNAL_CLEAN.connect( self.Pin_Clean )
            self.pin_module[i].SIGNAL_TEXT.connect( self.Label_String )
        for i in range( 0, length ):
            self.pin_cor.append( color_false.copy() )

        #endregion
    def Style( self ):
        # Icons
        qicon_swap = Krita.instance().icon( "fileLayer" )
        self.qicon_on = Krita.instance().icon( "showColoring" )
        self.qicon_write = Krita.instance().icon( "media-playback-start" )
        self.qicon_read = Krita.instance().icon( "system-help" )
        self.qicon_off = Krita.instance().icon( "showColoringOff" )
        qicon_fill = Krita.instance().icon( "folder-documents" )
        qicon_selection = Krita.instance().icon( "local-selection-inactive" )
        qicon_settings = Krita.instance().icon( "settings-button" )
        self.qicon_lock_layout = Krita.instance().icon( "layer-locked" )
        self.qicon_lock_dialog = Krita.instance().icon( "docker_lock_b" )
        self.qicon_none = QIcon()

        # Widgets
        self.layout.dot_swap.setIcon( qicon_swap )
        self.layout.mode.setIcon( self.qicon_on )
        self.layout.fill.setIcon( qicon_fill )
        self.layout.selection.setIcon( qicon_selection )
        self.layout.settings.setIcon( qicon_settings )

        # Tool Tips
        self.layout.mode.setToolTip( "Mode" )
        self.layout.fill.setToolTip( "Fill Pixel" )
        self.layout.selection.setToolTip( "Color Selection" )
        self.layout.hex_string.setToolTip( "Hex Code" )
        self.layout.settings.setToolTip( "Settings" )

        # Style Sheets Layout
        self.layout.panel_fill.setStyleSheet( "#panel_fill{background-color: rgba( 0, 0, 0, 50 );}" )
        self.layout.panel_square.setStyleSheet( "#panel_square{background-color: rgba( 0, 0, 0, 50 );}" )
        self.layout.panel_hue.setStyleSheet( "#panel_hue{background-color: rgba( 0, 0, 0, 50 );}" )
        self.layout.panel_gamut.setStyleSheet( "#panel_gamut{background-color: rgba( 0, 0, 0, 50 );}" )
        self.layout.panel_hexagon.setStyleSheet( "#panel_hexagon{background-color: rgba( 0, 0, 0, 50 );}" )
        self.layout.panel_dot.setStyleSheet( "#panel_dot{background-color: rgba( 0, 0, 0, 50 );}" )
        # Style Sheets Dialog
        self.dialog.scroll_area_contents_option.setStyleSheet( "#scroll_area_contents_option{background-color: rgba( 0, 0, 0, 20 );}" )
        self.dialog.scroll_area_contents_color.setStyleSheet( "#scroll_area_contents_color{background-color: rgba( 0, 0, 0, 20 );}" )
        self.dialog.scroll_area_contents_system.setStyleSheet( "#scroll_area_contents_system{background-color: rgba( 0, 0, 0, 20 );}" )

        # Combobox
        qpixmap_fill = QPixmap( 100, 100 )
        qpixmap_fill.fill( QColor( "#000000" ) )

        icon_path = "\\ICON\\"
        path_square =  self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "SQUARE.png" )
        path_hue =     self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "HUE.png" )
        path_gamut =   self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "GAMUT.png" )
        path_hexagon = self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "HEXAGON.png" )
        path_luma =    self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "LUMA.png" )
        path_dot =     self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "DOT.png" )
        path_mask =    self.convert.Path_Os( self.OS, self.directory_plugin + icon_path + "MASK.png" )

        self.dialog.panel_index.blockSignals( True )
        self.dialog.panel_index.setItemIcon( 0, QIcon( qpixmap_fill ) )
        self.dialog.panel_index.setItemIcon( 1, QIcon( path_square ) )
        self.dialog.panel_index.setItemIcon( 2, QIcon( path_hue ) )
        self.dialog.panel_index.setItemIcon( 3, QIcon( path_gamut ) )
        self.dialog.panel_index.setItemIcon( 4, QIcon( path_hexagon ) )
        self.dialog.panel_index.setItemIcon( 5, QIcon( path_luma ) )
        self.dialog.panel_index.setItemIcon( 6, QIcon( path_dot ) )
        self.dialog.panel_index.setItemIcon( 7, QIcon( path_mask ) )
        self.dialog.panel_index.blockSignals( False )
    def Timer( self ):
        #region QTimer

        if check_timer >= 30:
            self.timer_pulse = QtCore.QTimer( self )
            self.timer_pulse.timeout.connect( self.Krita_to_Pigmento )

        #endregion
        #region Randomizer Seed

        today = datetime.date.today()
        y = str( today )[0:4]
        m = str( today )[5:7]
        d = str( today )[8:10]
        seed = int( str( y + m + d ) )
        random.seed( seed )

        #endregion
    def Extension( self ):
        # Install Extension for Pigmento Docker
        extension = Pigmento_Extension( parent = Krita.instance() )
        Krita.instance().addExtension( extension )
        # Connect Extension Signals
        extension.SIGNAL_COLOR.connect( self.Extension_COR )
        extension.SIGNAL_KEY_1.connect( self.Extension_KEY_1 )
        extension.SIGNAL_KEY_2.connect( self.Extension_KEY_2 )
        extension.SIGNAL_KEY_3.connect( self.Extension_KEY_3 )
        extension.SIGNAL_KEY_4.connect( self.Extension_KEY_4 )
        extension.SIGNAL_LOCK.connect( self.Extension_LOCK )
    def Settings( self ):
        #region Dictionaries

        self.Dict_Copy( krange, self.Set_Read( "EVAL", "krange", krange ) )
        self.Dict_Copy( stops, self.Set_Read( "EVAL", "stops", stops ) )
        self.Dict_Copy( kac, self.Set_Read( "EVAL", "kac", kac ) )
        self.Dict_Copy( kbc, self.Set_Read( "EVAL", "kbc", kbc ) )

        #endregion
        #region Dictionaries Pin

        self.pin_cor = self.Set_Read( "EVAL", "pin_cor", self.pin_cor )

        #endregion
        #region Harmony

        # Colors
        self.Dict_Copy( har_01, self.Set_Read( "EVAL", "har_01", har_01 ) )
        self.Dict_Copy( har_02, self.Set_Read( "EVAL", "har_02", har_02 ) )
        self.Dict_Copy( har_03, self.Set_Read( "EVAL", "har_03", har_03 ) )
        self.Dict_Copy( har_04, self.Set_Read( "EVAL", "har_04", har_04 ) )
        self.Dict_Copy( har_05, self.Set_Read( "EVAL", "har_05", har_05 ) )

        # Variables
        self.harmony_rule = self.Set_Read( "STR", "harmony_rule", self.harmony_rule )
        self.harmony_edit = self.Set_Read( "EVAL", "harmony_edit", self.harmony_edit )
        self.harmony_index = self.Set_Read( "EVAL", "harmony_index", self.harmony_index )
        self.harmony_span = self.Set_Read( "EVAL", "harmony_span", self.harmony_span )

        # Modules
        self.harmony_swatch.Update_Harmony( self.harmony_rule, self.harmony_edit, self.harmony_index )
        self.harmony_spread.Update_Span( self.harmony_span )

        #endregion
        #region Panel HUE

        # Variables
        self.huecircle_shape = self.Set_Read( "STR", "huecircle_shape", self.huecircle_shape )
        # # Module
        self.panel_huecircle.Set_Shape( self.huecircle_shape )
        self.HueCircle_SubPanel( self.huecircle_shape )

        #endregion
        #region Panel Gamut

        # Variables
        self.gamut_mask = self.Set_Read( "STR", "gamut_mask", self.gamut_mask )
        self.gamut_profile = self.Set_Read( "EVAL", "gamut_profile", self.gamut_profile )

        # Module
        self.panel_gamut.Update_Mask( self.gamut_mask )
        self.panel_gamut.Update_Profile( self.gamut_profile )

        #endregion
        #region Panel DOT

        # Variables
        self.dot_interpolation = self.Set_Read( "STR", "dot_interpolation", self.dot_interpolation )
        self.dot_dimension = self.Set_Read( "EVAL", "dot_dimension", self.dot_dimension )
        self.dot_edit = self.Set_Read( "EVAL", "dot_edit", self.dot_edit )

        # Modules
        self.panel_dot.Set_Interpolation( self.dot_interpolation )
        self.panel_dot.Set_Dimension( self.dot_dimension )
        self.panel_dot.Set_Edit( self.dot_edit )
        self.Dot_Widget( self.dot_edit )

        # Colors
        self.dot_1 = self.Set_Read( "EVAL", "dot_1", self.Color_Convert( "HEX", "#edb525", 0, 0, 0, self.dot_1 ) )
        self.dot_2 = self.Set_Read( "EVAL", "dot_2", self.Color_Convert( "HEX", "#b72e35", 0, 0, 0, self.dot_2 ) )
        self.dot_3 = self.Set_Read( "EVAL", "dot_3", self.Color_Convert( "HEX", "#edf0ec", 0, 0, 0, self.dot_3 ) )
        self.dot_4 = self.Set_Read( "EVAL", "dot_4", self.Color_Convert( "HEX", "#292421", 0, 0, 0, self.dot_4 ) )

        # Update
        self.Update_Panel_Dot()
        self.Update_Edit_Dot()

        #endregion
        #region Panel Mask

        self.mask_set = self.Set_Read( "STR", "mask_set", self.mask_set )
        self.mask_edit = self.Set_Read( "EVAL", "mask_edit", self.mask_edit )
        self.panel_mask.Set_Edit( self.mask_edit )
        self.Mask_Widget( self.mask_edit )

        #endregion
        #region Mixer

        self.mixer_colors = self.Set_Read( "EVAL", "mixer_colors", self.mixer_colors )

        #endregion
        #region Dialog Option

        # Panels
        self.dialog.panel_index.setCurrentText( self.Set_Read( "STR", "panel_index", "Square" ) )
        self.dialog.wheel_mode.setCurrentText( self.Set_Read( "STR", "wheel_mode", "DIGITAL" ) )
        self.dialog.wheel_space.setCurrentText( self.Set_Read( "STR", "wheel_space", "HSV" ) )
        self.dialog.analyse_display.setChecked( self.Set_Read( "EVAL", "analyse_display", False ) )
        # Mixers
        self.dialog.mixer_space.setCurrentText( self.Set_Read( "STR", "mixer_space", "HSV" ) )

        #endregion
        #region Dialog Color

        # Color Space
        self.dialog.chan_aaa.setChecked( self.Set_Read( "EVAL", "chan_aaa", False ) )
        self.dialog.chan_rgb.setChecked( self.Set_Read( "EVAL", "chan_rgb", False ) )
        self.dialog.chan_cmy.setChecked( self.Set_Read( "EVAL", "chan_cmy", False ) )
        self.dialog.chan_cmyk.setChecked( self.Set_Read( "EVAL", "chan_cmyk", False ) )
        self.dialog.chan_ryb.setChecked( self.Set_Read( "EVAL", "chan_ryb", False ) )
        self.dialog.chan_yuv.setChecked( self.Set_Read( "EVAL", "chan_yuv", False ) )
        self.dialog.chan_hsv.setChecked( self.Set_Read( "EVAL", "chan_hsv", True ) )
        self.dialog.chan_hsl.setChecked( self.Set_Read( "EVAL", "chan_hsl", False ) )
        self.dialog.chan_hsy.setChecked( self.Set_Read( "EVAL", "chan_hsy", False ) )
        self.dialog.chan_ard.setChecked( self.Set_Read( "EVAL", "chan_ard", False ) )
        self.dialog.chan_xyz.setChecked( self.Set_Read( "EVAL", "chan_xyz", False ) )
        self.dialog.chan_xyy.setChecked( self.Set_Read( "EVAL", "chan_xyy", False ) )
        self.dialog.chan_lab.setChecked( self.Set_Read( "EVAL", "chan_lab", False ) )
        self.dialog.chan_lch.setChecked( self.Set_Read( "EVAL", "chan_lch", False ) )
        # Non Color
        self.dialog.chan_kkk.setChecked( self.Set_Read( "EVAL", "chan_kkk", False ) )
        self.dialog.chan_sele.setChecked( self.Set_Read( "EVAL", "chan_sele", False ) )
        self.dialog.sele_mode.setCurrentText( self.Set_Read( "STR", "sele_mode", "HSV" ) )
        self.dialog.chan_hex.setChecked( self.Set_Read( "EVAL", "chan_hex", False ) )
        self.dialog.hex_sum.setChecked( self.Set_Read( "EVAL", "hex_sum", False ) )

        # Format
        self.dialog.hue_shine.setChecked( self.Set_Read( "EVAL", "hue_shine", False ) )
        self.dialog.disp_values.setChecked( self.Set_Read( "EVAL", "disp_values", False ) )
        self.dialog.hex_copy_paste.setChecked( self.Set_Read( "EVAL", "hex_copy_paste", False ) )

        # Shortcuts
        self.dialog.key_1_chan.setCurrentText( self.Set_Read( "STR", "key_1_chan", "[KEY 1]" ) )
        self.dialog.key_2_chan.setCurrentText( self.Set_Read( "STR", "key_2_chan", "[KEY 2]" ) )
        self.dialog.key_3_chan.setCurrentText( self.Set_Read( "STR", "key_3_chan", "[KEY 3]" ) )
        self.dialog.key_4_chan.setCurrentText( self.Set_Read( "STR", "key_4_chan", "[KEY 4]" ) )
        self.dialog.key_1_factor.setValue( self.Set_Read( "INT", "key_1_factor", 1 ) )
        self.dialog.key_2_factor.setValue( self.Set_Read( "INT", "key_2_factor", 1 ) )
        self.dialog.key_3_factor.setValue( self.Set_Read( "INT", "key_3_factor", 1 ) )
        self.dialog.key_4_factor.setValue( self.Set_Read( "INT", "key_4_factor", 1 ) )

        #endregion
        #region Dialog System

        # Color Space
        self.dialog.cs_luminosity.setCurrentText( self.Set_Read( "STR", "cs_luminosity", "ITU-R BT.709" ) )
        self.dialog.cs_matrix.setCurrentText( self.Set_Read( "STR", "cs_matrix", "sRGB" ) )
        self.dialog.cs_illuminant.setCurrentText( self.Set_Read( "STR", "cs_illuminant", "D65" ) )

        # Annotations
        self.dialog.annotation_kra_save.setChecked( self.Set_Read( "EVAL", "annotation_kra", False ) )
        self.dialog.annotation_file_save.setChecked( self.Set_Read( "EVAL", "annotation_file", False ) )

        # Performance
        self.dialog.performance_release.setChecked( self.Set_Read( "EVAL", "performance_release", False ) )
        self.dialog.performance_inaccurate.setChecked( self.Set_Read( "EVAL", "performance_inaccurate", False ) )

        #endregion
        #region Dialog Header

        self.dialog.harmony.setChecked( self.Set_Read( "EVAL", "ui_harmony", False ) )
        self.dialog.channel.setChecked( self.Set_Read( "EVAL", "ui_channel", True ) )
        self.dialog.mixer.setChecked( self.Set_Read( "EVAL", "ui_mixer", False ) )
        self.dialog.pin.setChecked( self.Set_Read( "EVAL", "ui_pin", False ) )
        self.dialog.history.setChecked( self.Set_Read( "EVAL", "ui_history", False ) )

        #endregion
    def Loader( self ):
        # Dictionaries
        self.Range_Load( krange )
        self.Sliders_Stops_Load( stops )
        # Panel
        self.Mask_Load()
        # Channel Color
        self.Channel_AAA( self.dialog.chan_aaa.isChecked() )
        self.Channel_RGB( self.dialog.chan_rgb.isChecked() )
        self.Channel_CMY( self.dialog.chan_cmy.isChecked() )
        self.Channel_CMYK( self.dialog.chan_cmyk.isChecked() )
        self.Channel_RYB( self.dialog.chan_ryb.isChecked() )
        self.Channel_YUV( self.dialog.chan_yuv.isChecked() )
        self.Channel_HSV( self.dialog.chan_hsv.isChecked() )
        self.Channel_HSL( self.dialog.chan_hsl.isChecked() )
        self.Channel_HSY( self.dialog.chan_hsy.isChecked() )
        self.Channel_ARD( self.dialog.chan_ard.isChecked() )
        self.Channel_XYZ( self.dialog.chan_xyz.isChecked() )
        self.Channel_XYY( self.dialog.chan_xyy.isChecked() )
        self.Channel_LAB( self.dialog.chan_lab.isChecked() )
        self.Channel_LCH( self.dialog.chan_lch.isChecked() )
        # Channels Non Color
        self.Channel_KKK( self.dialog.chan_kkk.isChecked() )
        self.Channel_SELE( self.dialog.chan_sele.isChecked() )
        self.Selection_Mode( self.dialog.sele_mode.currentText() )
        self.Channel_Hex( self.dialog.chan_hex.isChecked() )
        self.Hex_Sum( self.dialog.hex_sum.isChecked() )
        # Mixer
        self.Mixer_LOAD()
        # Pin
        self.Pin_LOAD()

        # Dialog Option
        self.Panel_Index( self.dialog.panel_index.currentText() )
        self.Wheel_Mode( self.dialog.wheel_mode.currentText() )
        self.Wheel_Space( self.dialog.wheel_space.currentText() )
        self.Mixer_Space( self.dialog.mixer_space.currentText() )
        # Dialog Color
        self.Hue_Shine( self.dialog.hue_shine.isChecked() )
        self.Display_Values( self.dialog.disp_values.isChecked() )
        self.Hex_CopyPaste( self.dialog.hex_copy_paste.isChecked() )
        # UI Layout
        self.Menu_Harmony( self.dialog.harmony.isChecked() )
        self.Menu_Channel( self.dialog.channel.isChecked() )
        self.Menu_Mixer( self.dialog.mixer.isChecked() )
        self.Menu_Pin( self.dialog.pin.isChecked() )
        self.Menu_History( self.dialog.history.isChecked() )

        # Sync
        self.Pigmento_RELEASE()
        self.Harmony_Update()

    def Set_Read( self, mode, entry, default ):
        setting = Krita.instance().readSetting( "Pigment.O", entry, "" )
        if setting == "":
            read = default
            Krita.instance().writeSetting( "Pigment.O", entry, str( default ) )
        else:
            read = setting
            if mode == "EVAL":
                read = eval( read )
            elif mode == "STR":
                read = str( read )
            elif mode == "INT":
                read = int( read )
        return read

    #endregion
    #region Menu Displays ##########################################################

    # Mode Index
    def Mode_Index( self, index ):
        self.mode_index = index
        if index == 0: # On
            self.layout.mode.setIcon( self.qicon_on )
            self.timer_pulse.start( check_timer )
        if index == 1: # Write
            self.layout.mode.setIcon( self.qicon_write )
            self.timer_pulse.stop()
        if index == 2: # Read
            self.layout.mode.setIcon( self.qicon_read )
            self.timer_pulse.start( check_timer )
        if index == 3: # Off
            self.layout.mode.setIcon( self.qicon_off )
            self.timer_pulse.stop()

    # Extra Functions
    def Menu_FILL( self, boolean ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            # Variables
            fill["active"] = boolean
            # UI
            if boolean == True:
                fill["node_name"] = Krita.instance().activeDocument().activeNode().name()
                fill["alphalock_before"] = Krita.instance().activeDocument().activeNode().alphaLocked()
                self.layout.fill.setIcon( Krita.instance().icon( "fillLayer" ) )
                Krita.instance().activeDocument().activeNode().setAlphaLocked( boolean )
            else:
                try:Krita.instance().activeDocument().nodeByName( fill["node_name"] ).setAlphaLocked( fill["alphalock_before"] )
                except:pass
                self.layout.fill.setIcon( Krita.instance().icon( "folder-documents" ) )
                fill["alphalock_before"] = None
                fill["node_name"] = None
        else:
            self.Fill_None()

    # UI Toggle
    def Menu_Harmony( self, boolean ):
        # Variables
        if boolean == True:
            # Variables
            text = "[HARMONY]"
            a = 10
            b = 20
            c = 10
            # Modules
            self.Harmony_Index( self.harmony_index )
            self.harmony_swatch.Update_Index( self.harmony_index )
        else:
            # Variables
            text = "HARMONY"
            a = 30
            b = 0
            c = 0
            # Modules
            self.Harmony_Index( 0 )
            self.harmony_swatch.Update_Index( 0 )
        # UI
        self.dialog.harmony.setText( text )
        self.layout.color_header.setMinimumHeight( a )
        self.layout.color_header.setMaximumHeight( a )
        self.layout.harmony_swatch.setMinimumHeight( b )
        self.layout.harmony_swatch.setMaximumHeight( b )
        self.layout.harmony_spread.setMinimumHeight( c )
        self.layout.harmony_spread.setMaximumHeight( c )
        # Update
        if self.ui_harmony != boolean:
            self.ui_harmony = boolean
        # Save
        Krita.instance().writeSetting( "Pigment.O", "ui_harmony", str( self.ui_harmony ) )
    def Menu_Channel( self, boolean ):
        # Variables
        if boolean == True:
            text_c = "[CHANNEL]"
            sc = 16777215
        else:
            text_c = "CHANNEL"
            sc = 0
        # UI
        self.dialog.channel.setText( text_c )
        self.layout.channel_set.setMinimumHeight( sc )
        self.layout.channel_set.setMaximumHeight( sc )
        # layout
        self.layout.channel_set.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Fixed )
        # Update
        if self.ui_channel != boolean:
            self.ui_channel = boolean
        self.Channel_Active()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "ui_channel", str( self.ui_channel ) )
    def Menu_Mixer( self, boolean ):
        # Variables
        if boolean == True:
            text = "[MIXER]"
            horz = 0
            vert = 1
            a = 10
            b = max_val
        else:
            text = "MIXER"
            horz = 0
            vert = 0
            a = 0
            b = 0
        # UI
        self.dialog.mixer.setText( text )
        self.layout.mixer_set.setMinimumHeight( a )
        self.layout.mixer_set.setMaximumHeight( b )
        # layout
        self.layout.mixer_set_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.mixer_set_layout.setVerticalSpacing( vert )
        # Update
        if self.ui_mixer != boolean:
            self.ui_mixer = boolean
        # Save
        Krita.instance().writeSetting( "Pigment.O", "ui_mixer", str( self.ui_mixer ) )
    def Menu_Pin( self, boolean ):
        # Variables
        if boolean == True:
            text = "[PIN]"
            horz = 0
            vert = 1
            a = 10
            b = 20
        else:
            text = "PIN"
            horz = 0
            vert = 0
            a = 0
            b = 0
        # UI
        self.dialog.pin.setText( text )
        self.layout.pin_set.setMinimumHeight( a )
        self.layout.pin_set.setMaximumHeight( b )
        # layout
        self.layout.pin_set_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.pin_set_layout.setVerticalSpacing( vert )
        # Update
        if self.ui_pin != boolean:
            self.ui_pin = boolean
        # Save
        Krita.instance().writeSetting( "Pigment.O", "ui_pin", str( self.ui_pin ) )
    def Menu_History( self, boolean ):
        # Variables
        if boolean == True:
            text = "[HISTORY]"
            horz = 0
            vert = 1
            a = 10
            b = 20
        else:
            text = "HISTORY"
            horz = 0
            vert = 0
            a = 0
            b = 0
        # UI
        self.dialog.history.setText( text )
        self.layout.history_set.setMinimumHeight( a )
        self.layout.history_set.setMaximumHeight( b )
        # layout
        self.layout.history_set_layout.setContentsMargins( horz, vert, horz, vert )
        # Update
        if self.ui_history != boolean:
            self.ui_history = boolean
        # Save
        Krita.instance().writeSetting( "Pigment.O", "ui_history", str( self.ui_history ) )

    # Panels
    def Panel_Index( self, index ):
        # UI
        if index == "Fill":
            self.layout.panel_set.setCurrentIndex( 0 )
        if index == "Square":
            self.layout.panel_set.setCurrentIndex( 1 )
        if index == "Hue":
            self.layout.panel_set.setCurrentIndex( 2 )
        if index == "Gamut":
            self.layout.panel_set.setCurrentIndex( 3 )
        if index == "Hexagon":
            self.layout.panel_set.setCurrentIndex( 4 )
        if index == "Luma":
            self.layout.panel_set.setCurrentIndex( 5 )
        if index == "Dot":
            self.layout.panel_set.setCurrentIndex( 6 )
        if index == "Mask":
            self.layout.panel_set.setCurrentIndex( 7 )
        # Update
        if self.panel_index != index:
            self.panel_index = index
            self.Update_Size()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "panel_index", str( self.panel_index ) )
    # Wheel
    def Wheel_Mode( self, wheel_mode ):
        # Variables
        self.wheel_mode = wheel_mode
        # UI display
        if self.dialog.wheel_mode.currentText() != self.wheel_mode:
            self.dialog.wheel_mode.setCurrentText( self.wheel_mode )
        # Modules
        self.panel_huecircle.Set_WheelMode( self.wheel_mode )
        self.panel_gamut.Set_WheelMode( self.wheel_mode )
        # Save
        Krita.instance().writeSetting( "Pigment.O", "wheel_mode", str( self.wheel_mode ) )
    def Wheel_Space( self, wheel_space ):
        # Variables
        self.wheel_space = wheel_space

        # UI display
        if self.dialog.wheel_space.currentText() != self.wheel_space:
            self.dialog.wheel_space.setCurrentText( self.wheel_space )

        # Panel Square
        self.panel_square.Set_WheelSpace( self.wheel_space )
        # Panel Hue
        self.panel_huecircle.Set_WheelSpace( self.wheel_space )
        if self.huecircle_shape == "Triangle":
            self.panel_huesubpanel.Set_WheelSpace( "HSL" )
        if self.huecircle_shape == "Square":
            self.panel_huesubpanel.Set_WheelSpace( self.wheel_space )
        if self.huecircle_shape == "Diamond":
            self.panel_huesubpanel.Set_WheelSpace( "HSL" )
        # Panel Gamut
        self.panel_gamut.Set_WheelSpace( self.wheel_space )

        # Save
        Krita.instance().writeSetting( "Pigment.O", "wheel_space", str( self.wheel_space ) )
    # Analyse
    def Analyse_Display( self, boolean ):
        # Variables
        self.analyse_display = boolean
        # Update
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "analyse_display", str( self.analyse_display ) )

    # Mixer
    def Mixer_Space( self, mixer_space ):
        self.mixer_space = mixer_space
        self.Mixers_Set_Style()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_space", str( self.mixer_space ) )
    def Mixer_Count( self, mixer_count ):
        # Construct
        if self.mixer_count < mixer_count:
            self.Count_Construct( self.mixer_count, mixer_count )
        # Clear
        elif self.mixer_count > mixer_count:
            self.Count_Clear( mixer_count, self.mixer_count )

        # Variables
        self.mixer_count = mixer_count
        # Update
        self.Update_Size()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_count", str( self.mixer_count ) )
    def Count_Construct( self, old, new ):
        for i in range( old, new ):
            # Widegts
            left = QWidget()
            middle = QWidget()
            right = QWidget()
            # Dimensions
            left = self.Count_Square( left, i )
            middle = self.Count_Slider( middle, i )
            right = self.Count_Square( right, i )
            # Layout
            self.layout.mixer_set_layout.addWidget( left, i, 0 )
            self.layout.mixer_set_layout.addWidget( middle, i, 1 )
            self.layout.mixer_set_layout.addWidget( right, i, 2 )

            # Variables
            self.mixer_widget.append( { "l" : left, "m" : middle, "r" : right } )
            self.mixer_module.append( { "l" : Pin_Color( left ), "m" : Channel_Slider( middle ), "r" : Pin_Color( right ) } )
            self.mixer_colors.append( { "l" : color_false.copy(), "m" : 0, "r" : color_false.copy() } )

            # Left
            self.mixer_module[i]["l"].Set_Index( i )
            self.mixer_module[i]["l"].SIGNAL_APPLY.connect( self.Mixer_Apply_L )
            self.mixer_module[i]["l"].SIGNAL_SAVE.connect( self.Mixer_Save_L )
            self.mixer_module[i]["l"].SIGNAL_CLEAN.connect( self.Mixer_Clean_L )
            self.mixer_module[i]["l"].SIGNAL_TEXT.connect( self.Label_String )
            # Gradient
            self.mixer_module[i]["m"].Set_Index( i )
            self.mixer_module[i]["m"].Set_Mode( "MIXER" )
            self.mixer_module[i]["m"].Set_Limits( 0, 0.5, 1 )
            self.mixer_module[i]["m"].Set_Stops( 2 )
            self.mixer_module[i]["m"].Set_Value( 0 )
            self.mixer_module[i]["m"].SIGNAL_VALUE.connect( self.Mixer_Slider_M )
            self.mixer_module[i]["m"].SIGNAL_STOPS.connect( self.Mixer_Stops_M )
            self.mixer_module[i]["m"].SIGNAL_RELEASE.connect( self.Pigmento_RELEASE )
            self.mixer_module[i]["m"].SIGNAL_TEXT.connect( self.Label_String )
            # Right
            self.mixer_module[i]["r"].Set_Index( i )
            self.mixer_module[i]["r"].SIGNAL_APPLY.connect( self.Mixer_Apply_R )
            self.mixer_module[i]["r"].SIGNAL_SAVE.connect( self.Mixer_Save_R )
            self.mixer_module[i]["r"].SIGNAL_CLEAN.connect( self.Mixer_Clean_R )
            self.mixer_module[i]["r"].SIGNAL_TEXT.connect( self.Label_String )

            # Delete Objects
            del left
            del middle
            del right
    def Count_Square( self, square, r ):
        # Dimensions
        square.setMinimumHeight( 15 )
        square.setMaximumHeight( 20 )
        square.setMaximumWidth( 20 )
        # Size Policy
        square.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Preferred )
        # Return
        return square
    def Count_Slider( self, slider, r ):
        # Geometry
        width = self.layout.mixer_m_000.width()
        slider.setGeometry( 0, 0, width, 20)
        # Dimensions
        slider.setMinimumHeight( 15 )
        slider.setMaximumHeight( 20 )
        # Size Policy
        slider.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Preferred )
        # Return
        return slider
    def Count_Clear( self, old, new ):
        for i in range( old, new ):
            # Widgets
            self.layout.mixer_set_layout.removeWidget( self.mixer_widget[-1]["l"] )
            self.layout.mixer_set_layout.removeWidget( self.mixer_widget[-1]["m"] )
            self.layout.mixer_set_layout.removeWidget( self.mixer_widget[-1]["r"] )
            # Delete Entries
            self.mixer_colors.pop( -1 )
            self.mixer_module.pop( -1 )
            self.mixer_widget.pop( -1 )

    # Selection
    def Selection_Mode( self, sele_mode ):
        # Variable
        self.sele_mode = sele_mode
        # Mode for Sliders
        if self.sele_mode == "A":
            self.sele_1_slider.Set_Mode( "LINEAR" )
            self.sele_2_slider.Set_Mode( None )
            self.sele_3_slider.Set_Mode( None )
            self.sele_4_slider.Set_Mode( None )
        if self.sele_mode in [ "RGB", "CMY", "RYB", "YUV", "XYZ", "XYY", "LAB", "LCH" ]:
            self.sele_1_slider.Set_Mode( "LINEAR" )
            self.sele_2_slider.Set_Mode( "LINEAR" )
            self.sele_3_slider.Set_Mode( "LINEAR" )
            self.sele_4_slider.Set_Mode( None )
        if self.sele_mode in [ "HSV", "HSL", "HSY", "ARD" ]:
            self.sele_1_slider.Set_Mode( "CIRCULAR" )
            self.sele_2_slider.Set_Mode( "LINEAR" )
            self.sele_3_slider.Set_Mode( "LINEAR" )
            self.sele_4_slider.Set_Mode( None )
        if self.sele_mode == "CMYK":
            self.sele_1_slider.Set_Mode( "LINEAR" )
            self.sele_2_slider.Set_Mode( "LINEAR" )
            self.sele_3_slider.Set_Mode( "LINEAR" )
            self.sele_4_slider.Set_Mode( "LINEAR" )
        # Update
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "sele_mode", str( self.sele_mode ) )

    # Space Channels UI
    def Channel_Active( self ):
        # Check UI
        chan_aaa = self.dialog.chan_aaa.isChecked()
        chan_rgb = self.dialog.chan_rgb.isChecked()
        chan_cmy = self.dialog.chan_cmy.isChecked()
        chan_cmyk = self.dialog.chan_cmyk.isChecked()
        chan_ryb = self.dialog.chan_ryb.isChecked()
        chan_yuv = self.dialog.chan_yuv.isChecked()
        chan_hsv = self.dialog.chan_hsv.isChecked()
        chan_hsl = self.dialog.chan_hsl.isChecked()
        chan_hsy = self.dialog.chan_hsy.isChecked()
        chan_ard = self.dialog.chan_ard.isChecked()
        chan_xyz = self.dialog.chan_xyz.isChecked()
        chan_xyy = self.dialog.chan_xyy.isChecked()
        chan_lab = self.dialog.chan_lab.isChecked()
        chan_lch = self.dialog.chan_lch.isChecked()
        chan_kkk = self.dialog.chan_kkk.isChecked()

        # Activate Corresponding
        self.Channel_AAA( chan_aaa )
        self.Channel_RGB( chan_rgb )
        self.Channel_CMY( chan_cmy )
        self.Channel_CMYK( chan_cmyk )
        self.Channel_RYB( chan_ryb )
        self.Channel_YUV( chan_yuv )

        self.Channel_HSV( chan_hsv )
        self.Channel_HSL( chan_hsl )
        self.Channel_HSY( chan_hsy )
        self.Channel_ARD( chan_ard )

        self.Channel_XYZ( chan_xyz )
        self.Channel_XYY( chan_xyy )
        self.Channel_LAB( chan_lab )

        self.Channel_LCH( chan_lch )

        self.Channel_KKK( chan_kkk )
    def Channel_AAA( self, boolean ):
        self.chan_aaa = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.aaa_label.setMaximumHeight( maxi )
        self.layout.aaa_slider.setMaximumHeight( maxi )
        self.layout.aaa_value.setMaximumHeight( maxi )
        self.layout.aaa_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.aaa_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.aaa_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_aaa", str( self.chan_aaa ) )
    def Channel_RGB( self, boolean ):
        self.chan_rgb = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.rgb_label.setMaximumHeight( maxi )
        self.layout.rgb_slider.setMaximumHeight( maxi )
        self.layout.rgb_value.setMaximumHeight( maxi )
        self.layout.rgb_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.rgb_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.rgb_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_rgb", str( self.chan_rgb ) )
    def Channel_CMY( self, boolean ):
        self.chan_cmy = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.cmy_label.setMaximumHeight( maxi )
        self.layout.cmy_slider.setMaximumHeight( maxi )
        self.layout.cmy_value.setMaximumHeight( maxi )
        self.layout.cmy_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.cmy_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.cmy_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_cmy", str( self.chan_cmy ) )
    def Channel_CMYK( self, boolean ):
        self.chan_cmyk = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.cmyk_label.setMaximumHeight( maxi )
        self.layout.cmyk_slider.setMaximumHeight( maxi )
        self.layout.cmyk_value.setMaximumHeight( maxi )
        self.layout.cmyk_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.cmyk_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.cmyk_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_cmyk", str( self.chan_cmyk ) )
    def Channel_RYB( self, boolean ):
        self.chan_ryb = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.ryb_label.setMaximumHeight( maxi )
        self.layout.ryb_slider.setMaximumHeight( maxi )
        self.layout.ryb_value.setMaximumHeight( maxi )
        self.layout.ryb_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.ryb_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.ryb_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_ryb", str( self.chan_ryb ) )
    def Channel_YUV( self, boolean ):
        self.chan_yuv = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.yuv_label.setMaximumHeight( maxi )
        self.layout.yuv_slider.setMaximumHeight( maxi )
        self.layout.yuv_value.setMaximumHeight( maxi )
        self.layout.yuv_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.yuv_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.yuv_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_yuv", str( self.chan_yuv ) )
    def Channel_HSV( self, boolean ):
        self.chan_hsv = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.hsv_label.setMaximumHeight( maxi )
        self.layout.hsv_slider.setMaximumHeight( maxi )
        self.layout.hsv_value.setMaximumHeight( maxi )
        self.layout.hsv_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hsv_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hsv_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_hsv", str( self.chan_hsv ) )
    def Channel_HSL( self, boolean ):
        self.chan_hsl = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.hsl_label.setMaximumHeight( maxi )
        self.layout.hsl_slider.setMaximumHeight( maxi )
        self.layout.hsl_value.setMaximumHeight( maxi )
        self.layout.hsl_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hsl_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hsl_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_hsl", str( self.chan_hsl ) )
    def Channel_HSY( self, boolean ):
        self.chan_hsy = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.hsy_label.setMaximumHeight( maxi )
        self.layout.hsy_slider.setMaximumHeight( maxi )
        self.layout.hsy_value.setMaximumHeight( maxi )
        self.layout.hsy_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hsy_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hsy_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_hsy", str( self.chan_hsy ) )
    def Channel_ARD( self, boolean ):
        self.chan_ard = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.ard_label.setMaximumHeight( maxi )
        self.layout.ard_slider.setMaximumHeight( maxi )
        self.layout.ard_value.setMaximumHeight( maxi )
        self.layout.ard_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.ard_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.ard_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_ard", str( self.chan_ard ) )
    def Channel_XYZ( self, boolean ):
        self.chan_xyz = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.xyz_label.setMaximumHeight( maxi )
        self.layout.xyz_slider.setMaximumHeight( maxi )
        self.layout.xyz_value.setMaximumHeight( maxi )
        self.layout.xyz_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.xyz_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.xyz_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_xyz", str( self.chan_xyz ) )
    def Channel_XYY( self, boolean ):
        self.chan_xyy = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.xyy_label.setMaximumHeight( maxi )
        self.layout.xyy_slider.setMaximumHeight( maxi )
        self.layout.xyy_value.setMaximumHeight( maxi )
        self.layout.xyy_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.xyy_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.xyy_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_xyy", str( self.chan_xyy ) )
    def Channel_LAB( self, boolean ):
        self.chan_lab = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.lab_label.setMaximumHeight( maxi )
        self.layout.lab_slider.setMaximumHeight( maxi )
        self.layout.lab_value.setMaximumHeight( maxi )
        self.layout.lab_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lab_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lab_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_lab", str( self.chan_lab ) )
    def Channel_LCH( self, boolean ):
        self.chan_lch = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.lch_label.setMaximumHeight( maxi )
        self.layout.lch_slider.setMaximumHeight( maxi )
        self.layout.lch_value.setMaximumHeight( maxi )
        self.layout.lch_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lch_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lch_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_lch", str( self.chan_lch ) )
    def Channel_KKK( self, boolean ):
        self.chan_kkk = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.kkk_label.setMaximumHeight( maxi )
        self.layout.kkk_slider.setMaximumHeight( maxi )
        self.layout.kkk_value.setMaximumHeight( maxi )
        self.layout.kkk_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.kkk_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.kkk_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_kkk", str( self.chan_kkk ) )
    def Channel_SELE( self, boolean ):
        self.chan_sele = boolean
        if ( boolean == True and self.ui_channel == True ):
            maxi = max_val
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0

        # layout
        self.layout.sele_label.setMaximumHeight( maxi )
        self.layout.sele_slider.setMaximumHeight( maxi )
        self.layout.sele_value.setMaximumHeight( maxi )
        self.layout.sele_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.sele_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.sele_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_sele", str( self.chan_sele ) )
    def Channel_Hex( self, boolean ):
        # Variables
        self.chan_hex = boolean
        if boolean == True:
            self.layout.hex_string.setMaximumWidth( 180 )
        else:
            self.layout.hex_string.setMaximumWidth( zero )

        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "chan_hex", str( self.chan_hex ) )

    # Space Range Load
    def Range_Load( self, dict ):
        # Dialog Range
        self.Range_Block( True )
        self.Range_Maximum( dict )
        self.Range_Set( dict )
        self.Range_Block( False )
    def Range_Block( self, boolean ):
        self.dialog.range_aaa.blockSignals( boolean )
        self.dialog.range_rgb.blockSignals( boolean )
        self.dialog.range_cmy.blockSignals( boolean )
        self.dialog.range_cmyk.blockSignals( boolean )
        self.dialog.range_ryb.blockSignals( boolean )
        self.dialog.range_yuv.blockSignals( boolean )

        self.dialog.range_hue.blockSignals( boolean )
        self.dialog.range_hsv.blockSignals( boolean )
        self.dialog.range_hsl.blockSignals( boolean )
        self.dialog.range_hsy.blockSignals( boolean )
        self.dialog.range_ard.blockSignals( boolean )

        self.dialog.range_xyz.blockSignals( boolean )
        self.dialog.range_xyy.blockSignals( boolean )
        self.dialog.range_lab.blockSignals( boolean )

        self.dialog.range_lch.blockSignals( boolean )
    def Range_Maximum( self, dict ):
        self.layout.aaa_1_value.setMaximum( dict["aaa_1"] )
        self.layout.rgb_1_value.setMaximum( dict["rgb_1"] )
        self.layout.rgb_2_value.setMaximum( dict["rgb_2"] )
        self.layout.rgb_3_value.setMaximum( dict["rgb_3"] )
        self.layout.cmy_1_value.setMaximum( dict["cmy_1"] )
        self.layout.cmy_2_value.setMaximum( dict["cmy_2"] )
        self.layout.cmy_3_value.setMaximum( dict["cmy_3"] )
        self.layout.cmyk_1_value.setMaximum( dict["cmyk_1"] )
        self.layout.cmyk_2_value.setMaximum( dict["cmyk_2"] )
        self.layout.cmyk_3_value.setMaximum( dict["cmyk_3"] )
        self.layout.cmyk_4_value.setMaximum( dict["cmyk_4"] )
        self.layout.ryb_1_value.setMaximum( dict["ryb_1"] )
        self.layout.ryb_2_value.setMaximum( dict["ryb_2"] )
        self.layout.ryb_3_value.setMaximum( dict["ryb_3"] )
        self.layout.yuv_1_value.setMaximum( dict["yuv_1"] )
        self.layout.yuv_2_value.setMaximum( dict["yuv_2"] )
        self.layout.yuv_3_value.setMaximum( dict["yuv_3"] )

        self.layout.hsv_1_value.setMaximum( dict["hsv_1"] )
        self.layout.hsv_2_value.setMaximum( dict["hsv_2"] )
        self.layout.hsv_3_value.setMaximum( dict["hsv_3"] )
        self.layout.hsl_1_value.setMaximum( dict["hsl_1"] )
        self.layout.hsl_2_value.setMaximum( dict["hsl_2"] )
        self.layout.hsl_3_value.setMaximum( dict["hsl_3"] )
        self.layout.hsy_1_value.setMaximum( dict["hsy_1"] )
        self.layout.hsy_2_value.setMaximum( dict["hsy_2"] )
        self.layout.hsy_3_value.setMaximum( dict["hsy_3"] )
        self.layout.ard_1_value.setMaximum( dict["ard_1"] )
        self.layout.ard_2_value.setMaximum( dict["ard_2"] )
        self.layout.ard_3_value.setMaximum( dict["ard_3"] )

        self.layout.xyz_1_value.setMaximum( dict["xyz_1"] )
        self.layout.xyz_2_value.setMaximum( dict["xyz_2"] )
        self.layout.xyz_3_value.setMaximum( dict["xyz_3"] )
        self.layout.xyy_1_value.setMaximum( dict["xyy_1"] )
        self.layout.xyy_2_value.setMaximum( dict["xyy_2"] )
        self.layout.xyy_3_value.setMaximum( dict["xyy_3"] )
        self.layout.lab_1_value.setMaximum( dict["lab_1"] )
        self.layout.lab_2_value.setMaximum( dict["lab_2"] )
        self.layout.lab_3_value.setMaximum( dict["lab_3"] )

        self.layout.lch_1_value.setMaximum( dict["lch_1"] )
        self.layout.lch_2_value.setMaximum( dict["lch_2"] )
        self.layout.lch_3_value.setMaximum( dict["lch_3"] )
    def Range_Set( self, dict ):
        self.dialog.range_aaa.setValue( dict["aaa_1"] )
        self.dialog.range_rgb.setValue( dict["rgb_1"] )
        self.dialog.range_cmy.setValue( dict["cmy_1"] )
        self.dialog.range_cmyk.setValue( dict["cmyk_1"] )
        self.dialog.range_ryb.setValue( dict["ryb_1"] )
        self.dialog.range_yuv.setValue( dict["yuv_1"] )
        self.dialog.range_hue.setValue( dict["hsv_1"] )
        self.dialog.range_hsv.setValue( dict["hsv_2"] )
        self.dialog.range_hsl.setValue( dict["hsl_2"] )
        self.dialog.range_hsy.setValue( dict["hsy_2"] )
        self.dialog.range_ard.setValue( dict["ard_2"] )
        self.dialog.range_xyz.setValue( dict["xyz_1"] )
        self.dialog.range_xyy.setValue( dict["xyy_1"] )
        self.dialog.range_lab.setValue( dict["lab_1"] )
        self.dialog.range_lch.setValue( dict["lch_1"] )

    # Space Range Value
    def Range_AAA( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["aaa_1"] = range
        self.layout.aaa_1_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_RGB( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["rgb_1"] = range
        krange["rgb_2"] = range
        krange["rgb_3"] = range
        self.layout.rgb_1_value.setMaximum( range )
        self.layout.rgb_2_value.setMaximum( range )
        self.layout.rgb_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_CMY( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["cmy_1"] = range
        krange["cmy_2"] = range
        krange["cmy_3"] = range
        self.layout.cmy_1_value.setMaximum( range )
        self.layout.cmy_2_value.setMaximum( range )
        self.layout.cmy_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_CMYK( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["cmyk_1"] = range
        krange["cmyk_2"] = range
        krange["cmyk_3"] = range
        krange["cmyk_4"] = range
        self.layout.cmyk_1_value.setMaximum( range )
        self.layout.cmyk_2_value.setMaximum( range )
        self.layout.cmyk_3_value.setMaximum( range )
        self.layout.cmyk_4_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_RYB( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["ryb_1"] = range
        krange["ryb_2"] = range
        krange["ryb_3"] = range
        self.layout.ryb_1_value.setMaximum( range )
        self.layout.ryb_2_value.setMaximum( range )
        self.layout.ryb_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_YUV( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["yuv_1"] = range
        krange["yuv_2"] = range
        krange["yuv_3"] = range
        self.layout.yuv_1_value.setMaximum( range )
        self.layout.yuv_2_value.setMaximum( range )
        self.layout.yuv_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_HUE( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["hsv_1"] = range
        krange["hsl_1"] = range
        krange["hsy_1"] = range
        krange["ard_1"] = range
        self.layout.hsv_1_value.setMaximum( range )
        self.layout.hsl_1_value.setMaximum( range )
        self.layout.hsy_1_value.setMaximum( range )
        self.layout.ard_1_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_HSV( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["hsv_2"] = range
        krange["hsv_3"] = range
        self.layout.hsv_2_value.setMaximum( range )
        self.layout.hsv_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_HSL( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["hsl_2"] = range
        krange["hsl_3"] = range
        self.layout.hsl_2_value.setMaximum( range )
        self.layout.hsl_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_HSY( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["hsy_2"] = range
        krange["hsy_3"] = range
        self.layout.hsy_2_value.setMaximum( range )
        self.layout.hsy_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_ARD( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["ard_2"] = range
        krange["ard_3"] = range
        self.layout.ard_2_value.setMaximum( range )
        self.layout.ard_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_XYZ( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["xyz_1"] = range
        krange["xyz_2"] = range
        krange["xyz_3"] = range
        self.layout.xyz_1_value.setMaximum( range )
        self.layout.xyz_2_value.setMaximum( range )
        self.layout.xyz_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_XYY( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["xyy_1"] = range
        krange["xyy_2"] = range
        krange["xyy_3"] = range
        self.layout.xyy_1_value.setMaximum( range )
        self.layout.xyy_2_value.setMaximum( range )
        self.layout.xyy_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_LAB( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["lab_1"] = range
        krange["lab_2"] = range
        krange["lab_3"] = range
        self.layout.lab_1_value.setMaximum( range )
        self.layout.lab_2_value.setMaximum( range )
        self.layout.lab_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    def Range_LCH( self, range ):
        range = int( self.geometry.Limit_Unit( range ) )
        krange["lch_1"] = range
        krange["lch_2"] = range
        krange["lch_3"] = range
        self.layout.lch_1_value.setMaximum( range )
        self.layout.lch_2_value.setMaximum( range )
        self.layout.lch_3_value.setMaximum( range )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "krange", str( krange ) )
    # Space Range Reset
    def Reset_AAA( self ):
        self.dialog.range_aaa.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_RGB( self ):
        self.dialog.range_rgb.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_CMY( self ):
        self.dialog.range_cmy.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_CMYK( self ):
        self.dialog.range_cmyk.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_RYB( self ):
        self.dialog.range_ryb.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_YUV( self ):
        self.dialog.range_yuv.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_HUE( self ):
        self.dialog.range_hue.setValue( 360 )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_HSV( self ):
        self.dialog.range_hsv.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_HSL( self ):
        self.dialog.range_hsl.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_HSY( self ):
        self.dialog.range_hsy.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_ARD( self ):
        self.dialog.range_ard.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_XYZ( self ):
        self.dialog.range_xyz.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_XYY( self ):
        self.dialog.range_xyy.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_LAB( self ):
        self.dialog.range_lab.setValue( self.doc["depth"]+1 )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    def Reset_LCH( self ):
        self.dialog.range_lch.setValue( self.doc["depth"] )
        self.Pigmento_RELEASE()
        self.Reset_UnFocus()
    # Reset Focus
    def Reset_UnFocus( self ):
        self.dialog.range_aaa.clearFocus()
        self.dialog.range_rgb.clearFocus()
        self.dialog.range_cmy.clearFocus()
        self.dialog.range_cmyk.clearFocus()
        self.dialog.range_ryb.clearFocus()
        self.dialog.range_yuv.clearFocus()

        self.dialog.range_hue.clearFocus()
        self.dialog.range_hsv.clearFocus()
        self.dialog.range_hsl.clearFocus()
        self.dialog.range_hsy.clearFocus()
        self.dialog.range_ard.clearFocus()

        self.dialog.range_xyz.clearFocus()
        self.dialog.range_xyy.clearFocus()
        self.dialog.range_lab.clearFocus()

        self.dialog.range_lch.clearFocus()

    # Non Color
    def Hex_Sum( self, boolean ):
        self.hex_sum = boolean
        self.Update_Values()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "hex_sum", str( self.hex_sum ) )

    # Locks
    def Lock_CMYK_4( self, boolean ):
        # UI
        if boolean == True:
            self.layout.cmyk_4_label.setText( "" ) # LOCKED
            self.layout.cmyk_4_label.setIcon( self.qicon_lock_layout )
            self.dialog.chan_cmyk.setIcon( self.qicon_lock_dialog )
        else:
            self.layout.cmyk_4_label.setText( "K" ) # Unlocked
            self.layout.cmyk_4_label.setIcon( self.qicon_none )
            self.dialog.chan_cmyk.setIcon( self.qicon_none )
        # Variables
        self.lock_cmyk_4 = boolean
        self.update()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "lock_cmyk_4", str( self.lock_cmyk_4 ) )
    def Lock_KKK_1( self, boolean ):
        # Variables
        self.lock_kkk_1 = boolean
        # State
        if boolean == True:
            self.layout.kkk_1_label.setText( "" ) # LOCKED
            self.layout.kkk_1_label.setIcon( self.qicon_lock_layout )
            self.dialog.chan_kkk.setIcon( self.qicon_lock_dialog )
            self.Pigmento_APPLY( "KKK", 0, 0, 0, 0, self.cor ) # Update to Kelvin influence
        else:
            self.layout.kkk_1_label.setText( "K" ) # Unlocked
            self.layout.kkk_1_label.setIcon( self.qicon_none )
            self.dialog.chan_kkk.setIcon( self.qicon_none )
            self.Pigmento_APPLY( "RGB", self.cor["rgb_1"], self.cor["rgb_2"], self.cor["rgb_3"], 0, self.cor ) # Recover previous RGB
        # Save
        Krita.instance().writeSetting( "Pigment.O", "lock_kkk_1", str( self.lock_kkk_1 ) )

    # Format
    def Hue_Shine( self, boolean ):
        self.hue_shine = boolean
        self.Channels_Set_Style()
        Krita.instance().writeSetting( "Pigment.O", "hue_shine", str( self.hue_shine ) )
    def Display_Values( self, boolean ):
        # Variables
        self.disp_values = boolean
        if boolean == True:
            a = 20
            b = 100
            c = 1
        else:
            a = 0
            b = 0
            c = 0

        # AAA
        self.layout.aaa_label.setMaximumWidth( a )
        self.layout.aaa_value.setMaximumWidth( b )
        # RGB
        self.layout.rgb_label.setMaximumWidth( a )
        self.layout.rgb_value.setMaximumWidth( b )
        # CMY
        self.layout.cmy_label.setMaximumWidth( a )
        self.layout.cmy_value.setMaximumWidth( b )
        # CMYK
        self.layout.cmyk_label.setMaximumWidth( a )
        self.layout.cmyk_value.setMaximumWidth( b )
        # RYB
        self.layout.ryb_label.setMaximumWidth( a )
        self.layout.ryb_value.setMaximumWidth( b )
        # YUV
        self.layout.yuv_label.setMaximumWidth( a )
        self.layout.yuv_value.setMaximumWidth( b )
        # HSV
        self.layout.hsv_label.setMaximumWidth( a )
        self.layout.hsv_value.setMaximumWidth( b )
        # HSL
        self.layout.hsl_label.setMaximumWidth( a )
        self.layout.hsl_value.setMaximumWidth( b )
        # HSY
        self.layout.hsy_label.setMaximumWidth( a )
        self.layout.hsy_value.setMaximumWidth( b )
        # HSV
        self.layout.ard_label.setMaximumWidth( a )
        self.layout.ard_value.setMaximumWidth( b )
        # XYZ
        self.layout.xyz_label.setMaximumWidth( a )
        self.layout.xyz_value.setMaximumWidth( b )
        # XYY
        self.layout.xyy_label.setMaximumWidth( a )
        self.layout.xyy_value.setMaximumWidth( b )
        # LAB
        self.layout.lab_label.setMaximumWidth( a )
        self.layout.lab_value.setMaximumWidth( b )
        # LCH
        self.layout.lch_label.setMaximumWidth( a )
        self.layout.lch_value.setMaximumWidth( b )
        # KKK
        self.layout.kkk_label.setMaximumWidth( a )
        self.layout.kkk_value.setMaximumWidth( b )
        # SELE
        self.layout.sele_label.setMaximumWidth( a )
        self.layout.sele_value.setMaximumWidth( b )

        # Channel Set
        self.layout.channel_set_layout.setHorizontalSpacing( c )
        # Update
        self.Update_Size()

        # Save
        Krita.instance().writeSetting( "Pigment.O", "disp_values", str( self.disp_values ) )
    def Hex_CopyPaste( self, boolean ):
        self.hex_copy_paste = boolean
        Krita.instance().writeSetting( "Pigment.O", "hex_copy_paste", str( self.hex_copy_paste ) )

    # Shortcuts Channel
    def Key_1_Channel( self ):
        self.key_1_chan = self.dialog.key_1_chan.currentText()
        Krita.instance().writeSetting( "Pigment.O", "key_1_chan", str( self.key_1_chan ) )
    def Key_2_Channel( self ):
        self.key_2_chan = self.dialog.key_2_chan.currentText()
        Krita.instance().writeSetting( "Pigment.O", "key_2_chan", str( self.key_2_chan ) )
    def Key_3_Channel( self ):
        self.key_3_chan = self.dialog.key_3_chan.currentText()
        Krita.instance().writeSetting( "Pigment.O", "key_3_chan", str( self.key_3_chan ) )
    def Key_4_Channel( self ):
        self.key_4_chan = self.dialog.key_4_chan.currentText()
        Krita.instance().writeSetting( "Pigment.O", "key_4_chan", str( self.key_4_chan ) )
    # Shortcuts Factor
    def Key_1_Factor( self, factor ):
        self.key_1_factor = factor
        Krita.instance().writeSetting( "Pigment.O", "key_1_factor", str( self.key_1_factor ) )
    def Key_2_Factor( self, factor ):
        self.key_2_factor = factor
        Krita.instance().writeSetting( "Pigment.O", "key_2_factor", str( self.key_2_factor ) )
    def Key_3_Factor( self, factor ):
        self.key_3_factor = factor
        Krita.instance().writeSetting( "Pigment.O", "key_3_factor", str( self.key_3_factor ) )
    def Key_4_Factor( self, factor ):
        self.key_4_factor = factor
        Krita.instance().writeSetting( "Pigment.O", "key_4_factor", str( self.key_4_factor ) )

    # Reference
    def Color_Name( self ):
        color_name = self.dialog.name_display.text()
        if color_name != "":
            hc = QApplication.clipboard()
            hc.clear()
            hc.setText( color_name )
            self.Label_String( "NAME COPY" )

    # Colors Spaces
    def CS_Luminosity( self, cs_luminosity ):
        self.convert.Set_Luminosity( cs_luminosity )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "cs_luminosity", str( cs_luminosity ) )
    def CS_Matrix( self, cs_matrix, cs_illuminant ):
        self.convert.Set_Matrix( cs_matrix, cs_illuminant )
        # Update
        self.update()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "cs_matrix", str( cs_matrix ) )
        Krita.instance().writeSetting( "Pigment.O", "cs_illuminant", str( cs_illuminant ) )

    # Performance
    def Performace_Release( self, boolean ):
        self.performance_release = boolean
        Krita.instance().writeSetting( "Pigment.O", "performance_release", str( self.performance_release ) )
    def Performace_Inaccurate( self, boolean ):
        self.performance_inaccurate = boolean
        Krita.instance().writeSetting( "Pigment.O", "performance_inaccurate", str( self.performance_inaccurate ) )

    # Dialogs
    def Menu_Settings( self ):
        # Display
        self.dialog.show()
        # Resize Geometry
        qmw = Krita.instance().activeWindow().qwindow()
        px = qmw.x()
        py = qmw.y()
        w2 = qmw.width() * 0.5
        h2 = qmw.height() * 0.5
        size = 500
        self.dialog.setGeometry( int( px + w2 - size * 0.5 ), int( py + h2 - size * 0.5 ), int( size ), int( size ) )
    def Menu_Manual( self ):
        url = "https://github.com/EyeOdin/Pigment.O/wiki"
        webbrowser.open_new( url )
    def Menu_License( self ):
        url = "https://github.com/EyeOdin/Pigment.O/blob/master/LICENSE"
        webbrowser.open_new( url )

    # Event Filter
    def Menu_Context_History( self, event ):
        # Menu
        cmenu = QMenu( self )
        cmenu_clear = cmenu.addAction( "CLEAR" )
        # Execute
        widget = self.layout.history_set.mapToGlobal( self.layout.history_list.geometry().topLeft() )
        mouse = event.pos()
        qpoint = QPoint( widget.x()+mouse.x(), widget.y()+mouse.y() )
        action = cmenu.exec_( qpoint )
        # Triggers
        if action == cmenu_clear:
            self.History_CLEAR()
    def Menu_Mode_Press( self, event ):
        # Menu
        cmenu = QMenu( self )
        # Actions
        cmenu_on = cmenu.addAction( "ON" )
        cmenu_write = cmenu.addAction( "WRITE" )
        cmenu_read = cmenu.addAction( "READ" )
        cmenu_off = cmenu.addAction( "OFF" )
        # Icons
        cmenu_on.setIcon( self.qicon_on )
        cmenu_write.setIcon( self.qicon_write )
        cmenu_read.setIcon( self.qicon_read )
        cmenu_off.setIcon( self.qicon_off )

        # Execute
        geo = self.layout.mode.geometry()
        qpoint = geo.bottomLeft()
        position = self.layout.footer_widget.mapToGlobal( qpoint )
        action = cmenu.exec_( position )
        # Triggers
        if action == cmenu_on:
            self.Mode_Index( 0 )
        elif action == cmenu_write:
            self.Mode_Index( 1 )
        elif action == cmenu_read:
            self.Mode_Index( 2 )
        elif action == cmenu_off:
            self.Mode_Index( 3 )
    def Menu_Mode_Wheel( self, event ):
        delta = event.angleDelta()
        if event.modifiers() == QtCore.Qt.NoModifier:
            delta_y = delta.y()
            value = 0
            if delta_y > 20:
                value = -1
            if delta_y < -20:
                value = 1
            if ( value == -1 or value == 1 ):
                new_index = self.geometry.Limit_Range( self.mode_index + value, 0, 3 )
                if self.mode_index != new_index:
                    self.Mode_Index( new_index )

    #endregion
    #region Management #############################################################

    # Document
    def Current_Document( self ):
        # Active Node Type
        # type_layer = ["paintlayer", "grouplayer", "clonelayer", "vectorlayer", "filterlayer", "filllayer", "filelayer"]
        # type_mask = ["transparencymask", "filtermask", "colorizemask", "transformmask", "selectionmask"]
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            try:
                # Instance
                ad = Krita.instance().activeDocument()
                vc = Krita.instance().activeWindow().activeView().canvas()

                # active document
                d_nt = ad.activeNode().type()
                d_nn = ad.activeNode().name()

                # document color
                d_cm = ad.colorModel()
                d_cd = ad.colorDepth()
                d_cp = ad.colorProfile()
                # Vector Layers
                vi = self.Vector_Index()

                # Colors
                fgc = Krita.instance().activeWindow().activeView().foregroundColor()
                bgc = Krita.instance().activeWindow().activeView().backgroundColor()
                # view color settings
                fgc_cm = fgc.colorModel()
                fgc_cd = fgc.colorDepth()
                fgc_cp = fgc.colorProfile()
                bgc_cm = bgc.colorModel()
                bgc_cd = bgc.colorDepth()
                bgc_cp = bgc.colorProfile()

                # Color Model
                if ( d_cm == "A" or d_cm == "GRAYA" ):
                    d_cm = "A"
                elif ( d_cm == "RGBA" or d_cm == None ):
                    d_cm = "RGB"
                elif d_cm == "CMYKA":
                    d_cm = "CMYK"
                elif d_cm == "YCbCr":
                    d_cm = "YUV"
                elif d_cm == "XYZA":
                    d_cm = "XYZ"
                elif d_cm == "LABA":
                    d_cm = "LAB"

                # Biggest value for Bit Depth Document
                if d_cd == "U16":
                    depth = 65535
                elif ( d_cd == "F16" or d_cd == "F32" ):
                    depth = 1
                else:
                    depth = 255

                # Create List
                document = {
                    "ad" : ad,
                    "vc" : vc,
                    "d_nt" : d_nt,
                    "d_nn" : d_nn,
                    "d_cm" : d_cm,
                    "d_cd" : d_cd,
                    "d_cp" : d_cp,
                    "vi" : vi,
                    "fgc" : fgc,
                    "bgc" : bgc,
                    "fgc_cm" : fgc_cm,
                    "fgc_cd" : fgc_cd,
                    "fgc_cp" : fgc_cp,
                    "bgc_cm" : bgc_cm,
                    "bgc_cd" : bgc_cd,
                    "bgc_cp" : bgc_cp,
                    "depth" : depth,
                    }
            except:
                document = self.Document_None()
        else:
            document = self.Document_None()
        return document
    def Document_None( self ):
        document = {
            "ad" : None,
            "vc" : None,
            "d_nt" : None,
            "d_nn" : None,
            "d_cm" : None,
            "d_cd" : None,
            "d_cp" : None,
            "vi" : None,
            "fgc" : None,
            "bgc" : None,
            "fgc_cm" : None,
            "fgc_cd" : None,
            "fgc_cp" : None,
            "bgc_cm" : None,
            "bgc_cd" : None,
            "bgc_cp" : None,
            "depth" : 255,
            }
        return document
    def Panel_inSpace( self, d_cm ):
        # Document
        if d_cm != "CMYK":
            d_cm = "RGB"

        # Panels
        self.panel_square.Set_ColorModel( d_cm )
        self.panel_huesubpanel.Set_ColorModel( d_cm )
        self.panel_gamut.Set_ColorModel( d_cm )
        self.panel_hexagon.Set_ColorModel( d_cm )
        self.panel_luma.Set_ColorModel( d_cm )

    # Resize Event
    def Update_Size( self ):
        #region Header

        self.color_header.Set_Size( self.layout.color_header.width(), self.layout.color_header.height() )
        self.harmony_swatch.Set_Size( self.layout.harmony_swatch.width(), self.layout.harmony_swatch.height() )
        self.harmony_spread.Set_Size( self.layout.harmony_spread.width(), self.layout.harmony_spread.height() )

        #endregion
        #region Panels

        # Fill
        self.panel_fill.Set_Size( self.layout.panel_fill.width(), self.layout.panel_fill.height() )
        # Square
        self.panel_square.Set_Size( self.layout.panel_square.width(), self.layout.panel_square.height() )
        # Hue
        self.panel_huecircle.Set_Size( self.layout.panel_hue.width(), self.layout.panel_hue.height(), self.huecircle_shape )
        self.HueCircle_Geo( self.layout.panel_hue.width(), self.layout.panel_hue.height() )
        # Gamut
        self.panel_gamut.Set_Size( self.layout.panel_gamut.width(), self.layout.panel_gamut.height() )
        # Hexagon
        self.panel_hexagon.Set_Size( self.layout.panel_hexagon.width(), self.layout.panel_hexagon.height() )
        # Yuv
        self.panel_luma.Set_Size( self.layout.panel_luma.width(), self.layout.panel_luma.height() )
        # Dot
        self.panel_dot.Set_Size( self.layout.panel_dot.width(), self.layout.panel_dot.height() )
        self.pin_d1.Set_Size( self.layout.dot_1.width(), self.layout.dot_1.height() )
        self.pin_d2.Set_Size( self.layout.dot_2.width(), self.layout.dot_2.height() )
        self.pin_d3.Set_Size( self.layout.dot_3.width(), self.layout.dot_3.height() )
        self.pin_d4.Set_Size( self.layout.dot_4.width(), self.layout.dot_4.height() )
        # Mask
        self.panel_mask.Set_Size( self.layout.panel_mask.width(), self.layout.panel_mask.height() )
        self.mask_f3.Set_Size( self.layout.fg_3_color.width(), self.layout.fg_3_color.height() )
        self.mask_f2.Set_Size( self.layout.fg_2_color.width(), self.layout.fg_2_color.height() )
        self.mask_f1.Set_Size( self.layout.fg_1_color.width(), self.layout.fg_1_color.height() )
        self.mask_d6.Set_Size( self.layout.dif_6_color.width(), self.layout.dif_6_color.height() )
        self.mask_d5.Set_Size( self.layout.dif_5_color.width(), self.layout.dif_5_color.height() )
        self.mask_d4.Set_Size( self.layout.dif_4_color.width(), self.layout.dif_4_color.height() )
        self.mask_d3.Set_Size( self.layout.dif_3_color.width(), self.layout.dif_3_color.height() )
        self.mask_d2.Set_Size( self.layout.dif_2_color.width(), self.layout.dif_2_color.height() )
        self.mask_d1.Set_Size( self.layout.dif_1_color.width(), self.layout.dif_1_color.height() )
        self.mask_b3.Set_Size( self.layout.bg_3_color.width(), self.layout.bg_3_color.height() )
        self.mask_b2.Set_Size( self.layout.bg_2_color.width(), self.layout.bg_2_color.height() )
        self.mask_b1.Set_Size( self.layout.bg_1_color.width(), self.layout.bg_1_color.height() )

        self.Panels_Set_Value()

        #endregion
        #region Channels

        # AAA
        self.aaa_1_slider.Set_Size( self.layout.aaa_1_slider.width(), self.layout.aaa_1_slider.height() )
        # RGB
        self.rgb_1_slider.Set_Size( self.layout.rgb_1_slider.width(), self.layout.rgb_1_slider.height() )
        self.rgb_2_slider.Set_Size( self.layout.rgb_2_slider.width(), self.layout.rgb_2_slider.height() )
        self.rgb_3_slider.Set_Size( self.layout.rgb_3_slider.width(), self.layout.rgb_3_slider.height() )
        # CMY
        self.cmy_1_slider.Set_Size( self.layout.cmy_1_slider.width(), self.layout.cmy_1_slider.height() )
        self.cmy_2_slider.Set_Size( self.layout.cmy_2_slider.width(), self.layout.cmy_2_slider.height() )
        self.cmy_3_slider.Set_Size( self.layout.cmy_3_slider.width(), self.layout.cmy_3_slider.height() )
        # CMYK
        self.cmyk_1_slider.Set_Size( self.layout.cmyk_1_slider.width(), self.layout.cmyk_1_slider.height() )
        self.cmyk_2_slider.Set_Size( self.layout.cmyk_2_slider.width(), self.layout.cmyk_2_slider.height() )
        self.cmyk_3_slider.Set_Size( self.layout.cmyk_3_slider.width(), self.layout.cmyk_3_slider.height() )
        self.cmyk_4_slider.Set_Size( self.layout.cmyk_4_slider.width(), self.layout.cmyk_4_slider.height() )
        # RYB
        self.ryb_1_slider.Set_Size( self.layout.ryb_1_slider.width(), self.layout.ryb_1_slider.height() )
        self.ryb_2_slider.Set_Size( self.layout.ryb_2_slider.width(), self.layout.ryb_2_slider.height() )
        self.ryb_3_slider.Set_Size( self.layout.ryb_3_slider.width(), self.layout.ryb_3_slider.height() )
        # YUV
        self.yuv_1_slider.Set_Size( self.layout.yuv_1_slider.width(), self.layout.yuv_1_slider.height() )
        self.yuv_2_slider.Set_Size( self.layout.yuv_2_slider.width(), self.layout.yuv_2_slider.height() )
        self.yuv_3_slider.Set_Size( self.layout.yuv_3_slider.width(), self.layout.yuv_3_slider.height() )

        # HSV
        self.hsv_1_slider.Set_Size( self.layout.hsv_1_slider.width(), self.layout.hsv_1_slider.height() )
        self.hsv_2_slider.Set_Size( self.layout.hsv_2_slider.width(), self.layout.hsv_2_slider.height() )
        self.hsv_3_slider.Set_Size( self.layout.hsv_3_slider.width(), self.layout.hsv_3_slider.height() )
        # HSL
        self.hsl_1_slider.Set_Size( self.layout.hsl_1_slider.width(), self.layout.hsl_1_slider.height() )
        self.hsl_2_slider.Set_Size( self.layout.hsl_2_slider.width(), self.layout.hsl_2_slider.height() )
        self.hsl_3_slider.Set_Size( self.layout.hsl_3_slider.width(), self.layout.hsl_3_slider.height() )
        # HSY
        self.hsy_1_slider.Set_Size( self.layout.hsy_1_slider.width(), self.layout.hsy_1_slider.height() )
        self.hsy_2_slider.Set_Size( self.layout.hsy_2_slider.width(), self.layout.hsy_2_slider.height() )
        self.hsy_3_slider.Set_Size( self.layout.hsy_3_slider.width(), self.layout.hsy_3_slider.height() )
        # ARD
        self.ard_1_slider.Set_Size( self.layout.ard_1_slider.width(), self.layout.ard_1_slider.height() )
        self.ard_2_slider.Set_Size( self.layout.ard_2_slider.width(), self.layout.ard_2_slider.height() )
        self.ard_3_slider.Set_Size( self.layout.ard_3_slider.width(), self.layout.ard_3_slider.height() )

        # XYZ
        self.xyz_1_slider.Set_Size( self.layout.xyz_1_slider.width(), self.layout.xyz_1_slider.height() )
        self.xyz_2_slider.Set_Size( self.layout.xyz_2_slider.width(), self.layout.xyz_2_slider.height() )
        self.xyz_3_slider.Set_Size( self.layout.xyz_3_slider.width(), self.layout.xyz_3_slider.height() )
        # XYY
        self.xyy_1_slider.Set_Size( self.layout.xyy_1_slider.width(), self.layout.xyy_1_slider.height() )
        self.xyy_2_slider.Set_Size( self.layout.xyy_2_slider.width(), self.layout.xyy_2_slider.height() )
        self.xyy_3_slider.Set_Size( self.layout.xyy_3_slider.width(), self.layout.xyy_3_slider.height() )
        # LAB
        self.lab_1_slider.Set_Size( self.layout.lab_1_slider.width(), self.layout.lab_1_slider.height() )
        self.lab_2_slider.Set_Size( self.layout.lab_2_slider.width(), self.layout.lab_2_slider.height() )
        self.lab_3_slider.Set_Size( self.layout.lab_3_slider.width(), self.layout.lab_3_slider.height() )

        # LCH
        self.lch_1_slider.Set_Size( self.layout.lch_1_slider.width(), self.layout.lch_1_slider.height() )
        self.lch_2_slider.Set_Size( self.layout.lch_2_slider.width(), self.layout.lch_2_slider.height() )
        self.lch_3_slider.Set_Size( self.layout.lch_3_slider.width(), self.layout.lch_3_slider.height() )

        # KKK
        self.kkk_1_slider.Set_Size( self.layout.kkk_1_slider.width(), self.layout.kkk_1_slider.height() )

        # SELE
        self.sele_1_slider.Set_Size( self.layout.sele_1_slider.width(), self.layout.sele_1_slider.height() )
        self.sele_2_slider.Set_Size( self.layout.sele_2_slider.width(), self.layout.sele_2_slider.height() )
        self.sele_3_slider.Set_Size( self.layout.sele_3_slider.width(), self.layout.sele_3_slider.height() )
        self.sele_4_slider.Set_Size( self.layout.sele_4_slider.width(), self.layout.sele_4_slider.height() )

        # Adjust Handles
        self.Update_Values()

        #endregion
        #region Mixer

        # Mixer 000
        for i in range( 0, len( self.mixer_module) ):
            self.mixer_module[i]["l"].Set_Size( self.mixer_widget[i]["l"].width(), self.mixer_widget[i]["l"].height() )
            self.mixer_module[i]["m"].Set_Size( self.mixer_widget[i]["m"].width(), self.mixer_widget[i]["m"].height() )
            self.mixer_module[i]["r"].Set_Size( self.mixer_widget[i]["r"].width(), self.mixer_widget[i]["r"].height() )

        #endregion
        #region Pin

        for i in range( 0, len( self.pin_module ) ):
            self.pin_module[i].Set_Size( self.pin_widget[i].width(), self.pin_widget[i].height() )

        #endregion

        self.update()
    def Resize_Print( self, event ):
        # Used doing a photoshoot
        width = self.width()
        height = self.height()
        QtCore.qDebug( "size = " + str( width ) + " x "  + str( height ) )

    # Leave Event
    def Clear_Focus( self ):
        # AAA
        self.layout.aaa_1_value.clearFocus()
        # RGB
        self.layout.rgb_1_value.clearFocus()
        self.layout.rgb_2_value.clearFocus()
        self.layout.rgb_3_value.clearFocus()
        # CMY
        self.layout.cmy_1_value.clearFocus()
        self.layout.cmy_2_value.clearFocus()
        self.layout.cmy_3_value.clearFocus()
        # CMYK
        self.layout.cmyk_1_value.clearFocus()
        self.layout.cmyk_2_value.clearFocus()
        self.layout.cmyk_3_value.clearFocus()
        self.layout.cmyk_4_value.clearFocus()
        # RYB
        self.layout.ryb_1_value.clearFocus()
        self.layout.ryb_2_value.clearFocus()
        self.layout.ryb_3_value.clearFocus()
        # YUV
        self.layout.yuv_1_value.clearFocus()
        self.layout.yuv_2_value.clearFocus()
        self.layout.yuv_3_value.clearFocus()

        # HSV
        self.layout.hsv_1_value.clearFocus()
        self.layout.hsv_2_value.clearFocus()
        self.layout.hsv_3_value.clearFocus()
        # HSL
        self.layout.hsl_1_value.clearFocus()
        self.layout.hsl_2_value.clearFocus()
        self.layout.hsl_3_value.clearFocus()
        # HSY
        self.layout.hsy_1_value.clearFocus()
        self.layout.hsy_2_value.clearFocus()
        self.layout.hsy_3_value.clearFocus()
        # ARD
        self.layout.ard_1_value.clearFocus()
        self.layout.ard_2_value.clearFocus()
        self.layout.ard_3_value.clearFocus()

        # XYZ
        self.layout.xyz_1_value.clearFocus()
        self.layout.xyz_2_value.clearFocus()
        self.layout.xyz_3_value.clearFocus()
        # XYY
        self.layout.xyy_1_value.clearFocus()
        self.layout.xyy_2_value.clearFocus()
        self.layout.xyy_3_value.clearFocus()
        # LAB
        self.layout.lab_1_value.clearFocus()
        self.layout.lab_2_value.clearFocus()
        self.layout.lab_3_value.clearFocus()

        # LCH
        self.layout.lch_1_value.clearFocus()
        self.layout.lch_2_value.clearFocus()
        self.layout.lch_3_value.clearFocus()

        # KKK
        self.layout.kkk_1_value.clearFocus()

        # SELE 1
        self.layout.sele_1_l0.clearFocus()
        self.layout.sele_1_l1.clearFocus()
        self.layout.sele_1_r1.clearFocus()
        self.layout.sele_1_r0.clearFocus()
        # SELE 2
        self.layout.sele_2_l0.clearFocus()
        self.layout.sele_2_l1.clearFocus()
        self.layout.sele_2_r1.clearFocus()
        self.layout.sele_2_r0.clearFocus()
        # SELE 3
        self.layout.sele_3_l0.clearFocus()
        self.layout.sele_3_l1.clearFocus()
        self.layout.sele_3_r1.clearFocus()
        self.layout.sele_3_r0.clearFocus()
        # SELE 4
        self.layout.sele_4_l0.clearFocus()
        self.layout.sele_4_l1.clearFocus()
        self.layout.sele_4_r1.clearFocus()
        self.layout.sele_4_r0.clearFocus()

        # HEX
        self.layout.hex_string.clearFocus()

    # Modules variables
    def Label_String( self, text ):
        self.layout.label.setText( str( text ) )

    # Dictionanries
    def Dict_Copy( self, active, load ):
        keys = list( active.keys() )
        for i in range( 0, len( active ) ):
            try:
                active[keys[i]] = load[keys[i]]
            except:
                pass

    # Hue
    def Hue_Index( self, mode ):
        c1 = f"{ mode.lower() }_1"
        c2 = f"{ mode.lower() }_2"
        c3 = f"{ mode.lower() }_3"
        return c1, c2, c3

    # Vector
    def Vector_Index( self ):
        node = Krita.instance().activeDocument().activeNode()
        if node.type() == "vectorlayer":
            index = []
            shapes = node.shapes()
            for i in range( 0, len( shapes ) ):
                if shapes[i].isSelected():
                    index.append( i )
            if len( index ) == 0:
                index = None
        else:
            index = None
        return index

    # Stops
    def Sliders_Stops_Load( self, dictionary ):
        # AAA
        self.aaa_1_slider.Set_Stops( dictionary["aaa_1"] )
        # RGB
        self.rgb_1_slider.Set_Stops( dictionary["rgb_1"] )
        self.rgb_2_slider.Set_Stops( dictionary["rgb_2"] )
        self.rgb_3_slider.Set_Stops( dictionary["rgb_3"] )
        # CMY
        self.cmy_1_slider.Set_Stops( dictionary["cmy_1"] )
        self.cmy_2_slider.Set_Stops( dictionary["cmy_2"] )
        self.cmy_3_slider.Set_Stops( dictionary["cmy_3"] )
        # CMYK
        self.cmyk_1_slider.Set_Stops( dictionary["cmyk_1"] )
        self.cmyk_2_slider.Set_Stops( dictionary["cmyk_2"] )
        self.cmyk_3_slider.Set_Stops( dictionary["cmyk_3"] )
        self.cmyk_4_slider.Set_Stops( dictionary["cmyk_4"] )
        # RYB
        self.ryb_1_slider.Set_Stops( dictionary["ryb_1"] )
        self.ryb_2_slider.Set_Stops( dictionary["ryb_2"] )
        self.ryb_3_slider.Set_Stops( dictionary["ryb_3"] )
        # YUV
        self.yuv_1_slider.Set_Stops( dictionary["yuv_1"] )
        self.yuv_2_slider.Set_Stops( dictionary["yuv_2"] )
        self.yuv_3_slider.Set_Stops( dictionary["yuv_3"] )

        # HSV
        self.hsv_1_slider.Set_Stops( dictionary["hsv_1"] )
        self.hsv_2_slider.Set_Stops( dictionary["hsv_2"] )
        self.hsv_3_slider.Set_Stops( dictionary["hsv_3"] )
        # HSL
        self.hsl_1_slider.Set_Stops( dictionary["hsl_1"] )
        self.hsl_2_slider.Set_Stops( dictionary["hsl_2"] )
        self.hsl_3_slider.Set_Stops( dictionary["hsl_3"] )
        # HSY
        self.hsy_1_slider.Set_Stops( dictionary["hsy_1"] )
        self.hsy_2_slider.Set_Stops( dictionary["hsy_2"] )
        self.hsy_3_slider.Set_Stops( dictionary["hsy_3"] )
        # ARD
        self.ard_1_slider.Set_Stops( dictionary["ard_1"] )
        self.ard_2_slider.Set_Stops( dictionary["ard_2"] )
        self.ard_3_slider.Set_Stops( dictionary["ard_3"] )

        # XYZ
        self.xyz_1_slider.Set_Stops( dictionary["xyz_1"] )
        self.xyz_2_slider.Set_Stops( dictionary["xyz_2"] )
        self.xyz_3_slider.Set_Stops( dictionary["xyz_3"] )
        # XYY
        self.xyy_1_slider.Set_Stops( dictionary["xyy_1"] )
        self.xyy_2_slider.Set_Stops( dictionary["xyy_2"] )
        self.xyy_3_slider.Set_Stops( dictionary["xyy_3"] )
        # LAB
        self.lab_1_slider.Set_Stops( dictionary["lab_1"] )
        self.lab_2_slider.Set_Stops( dictionary["lab_2"] )
        self.lab_3_slider.Set_Stops( dictionary["lab_3"] )

        # LCH
        self.lch_1_slider.Set_Stops( dictionary["lch_1"] )
        self.lch_2_slider.Set_Stops( dictionary["lch_2"] )
        self.lch_3_slider.Set_Stops( dictionary["lch_3"] )

        # KKK
        self.kkk_1_slider.Set_Stops( dictionary["kkk_1"] )

        # Mixers
        for i in range( 0, len( self.mixer_widget ) ):
            self.mixer_module[i]["m"].Set_Stops( dictionary["mixer"] )

    # Label
    def Warn_Message( self, string ):
        QMessageBox.information( QWidget(), i18n( "Warnning" ), i18n( string ) )

    #endregion
    #region Pigmento & Krita #######################################################

    def Krita_to_Pigmento( self ):
        # Current Document
        doc = self.Current_Document()
        if self.doc["d_cm"] != doc["d_cm"]:
            # QtCore.qDebug( f'self.doc["d_cm"] = { self.doc["d_cm"] }' )
            # QtCore.qDebug( f'doc["d_cm"] = { doc["d_cm"] }' )
            self.Panel_inSpace( doc["d_cm"] )
            # self.doc["d_cm"] = doc["d_cm"]
        d_cm = doc["d_cm"]
        d_cd = doc["d_cd"]
        d_cp = doc["d_cp"]
        d = doc["depth"]

        # Canvas
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            # Read Color
            try:
                if ( self.mode_index == 0 and ( self.widget_press == False or self.doc != doc ) ):
                    # Check Eraser Mode ON or OFF
                    eraser = Krita.instance().action( "erase_action" )
                    # Current Krita Active Colors
                    color_fg = Krita.instance().activeWindow().activeView().foregroundColor()
                    color_bg = Krita.instance().activeWindow().activeView().backgroundColor()
                    order_fg = color_fg.componentsOrdered()
                    order_bg = color_bg.componentsOrdered()

                    # Variables
                    len_fg = len( order_fg )
                    len_bg = len( order_bg )

                    # Depth
                    self.depth_previous = self.cor["uvd_3"]

                    # Harmony
                    if self.harmony_index == 1:
                        a = har_01
                    elif self.harmony_index == 2:
                        a = har_02
                    elif self.harmony_index == 3:
                        a = har_03
                    elif self.harmony_index == 4:
                        a = har_04
                    elif self.harmony_index == 5:
                        a = har_05
                    else:
                        a = kac
                    b = kbc

                    # Read if Colors Differs
                    if doc["vi"] == None: # Pixel Read
                        if ( d_cm == "A" or len_fg == 2 ):
                            # Foreground and Background Colors ( Krita is in AAA )
                            kac_1 = order_fg[0]
                            kbc_1 = order_bg[0]

                            # Range
                            if ( d_cd == "U8" or d_cd == "U16" ):
                                c_fg_1 = ( kac_1 < ( ( int( a["aaa_d1"] * d ) ) / d ) ) or ( kac_1 >= ( ( int( a["aaa_d1"] * d ) + 1 ) / d ) )
                                c_bg_1 = ( kbc_1 < ( ( int( b["aaa_d1"] * d ) ) / d ) ) or ( kbc_1 >= ( ( int( b["aaa_d1"] * d ) + 1 ) / d ) )
                            if ( d_cd == "F16" or d_cd == "F32" ):
                                c_fg_1 = kac_1 != a["aaa_d1"]
                                c_bg_1 = kbc_1 != b["aaa_d1"]

                            # Operation
                            if c_fg_1 == True:
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "A", kac_1, 0, 0, 0, a )
                            if c_bg_1 == True:
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "A", kbc_1, 0, 0, 0, b )
                        elif ( d_cm == "RGB" or d_cm == None ):
                            # Foreground and Background Colors ( Krita is in RGB )
                            kac_1 = order_fg[0] # Red
                            kac_2 = order_fg[1] # Green
                            kac_3 = order_fg[2] # Blue
                            kbc_1 = order_bg[0]
                            kbc_2 = order_bg[1]
                            kbc_3 = order_bg[2]

                            # Range
                            if ( d_cd == "U8" or d_cd == "U16" ):
                                c_fg_1 = ( kac_1 < ( ( int( a["rgb_d1"] * d ) ) / d ) ) or ( kac_1 >= ( ( int( a["rgb_d1"] * d ) + 1 ) / d ) )
                                c_fg_2 = ( kac_2 < ( ( int( a["rgb_d2"] * d ) ) / d ) ) or ( kac_2 >= ( ( int( a["rgb_d2"] * d ) + 1 ) / d ) )
                                c_fg_3 = ( kac_3 < ( ( int( a["rgb_d3"] * d ) ) / d ) ) or ( kac_3 >= ( ( int( a["rgb_d3"] * d ) + 1 ) / d ) )
                                c_bg_1 = ( kbc_1 < ( ( int( b["rgb_d1"] * d ) ) / d ) ) or ( kbc_1 >= ( ( int( b["rgb_d1"] * d ) + 1 ) / d ) )
                                c_bg_2 = ( kbc_2 < ( ( int( b["rgb_d2"] * d ) ) / d ) ) or ( kbc_2 >= ( ( int( b["rgb_d2"] * d ) + 1 ) / d ) )
                                c_bg_3 = ( kbc_3 < ( ( int( b["rgb_d3"] * d ) ) / d ) ) or ( kbc_3 >= ( ( int( b["rgb_d3"] * d ) + 1 ) / d ) )
                            if ( d_cd == "F16" or d_cd == "F32" ):
                                c_fg_1 = kac_1 != a["rgb_d1"]
                                c_fg_2 = kac_2 != a["rgb_d2"]
                                c_fg_3 = kac_3 != a["rgb_d3"]
                                c_bg_1 = kbc_1 != b["rgb_d1"]
                                c_bg_2 = kbc_2 != b["rgb_d2"]
                                c_bg_3 = kbc_3 != b["rgb_d3"]

                            # Operation
                            if ( c_fg_1 == True or c_fg_2 == True or c_fg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "RGB", kac_1, kac_2, kac_3, 0, a )
                            if ( c_bg_1 == True or c_bg_2 == True or c_bg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "RGB", kbc_1, kbc_2, kbc_3, 0, b )
                        elif d_cm == "CMYK":
                            # Foreground and Background Colors ( Krita is in CMYK )
                            kac_1 = order_fg[0]
                            kac_2 = order_fg[1]
                            kac_3 = order_fg[2]
                            kac_4 = order_fg[3]
                            kbc_1 = order_bg[0]
                            kbc_2 = order_bg[1]
                            kbc_3 = order_bg[2]
                            kbc_4 = order_bg[3]

                            # Range
                            if ( d_cd == "U8" or d_cd == "U16" ):
                                c_fg_1 = ( kac_1 < ( ( int( a["cmyk_d1"] * d ) ) / d ) ) or ( kac_1 >= ( ( math.ceil( a["cmyk_d1"] * d ) + 1 ) / d ) )
                                c_fg_2 = ( kac_2 < ( ( int( a["cmyk_d2"] * d ) ) / d ) ) or ( kac_2 >= ( ( math.ceil( a["cmyk_d2"] * d ) + 1 ) / d ) )
                                c_fg_3 = ( kac_3 < ( ( int( a["cmyk_d3"] * d ) ) / d ) ) or ( kac_3 >= ( ( math.ceil( a["cmyk_d3"] * d ) + 1 ) / d ) )
                                c_fg_4 = ( kac_4 < ( ( int( a["cmyk_d4"] * d ) ) / d ) ) or ( kac_4 >= ( ( math.ceil( a["cmyk_d4"] * d ) + 1 ) / d ) )
                                c_bg_1 = ( kbc_1 < ( ( int( b["cmyk_d1"] * d ) ) / d ) ) or ( kbc_1 >= ( ( math.ceil( b["cmyk_d1"] * d ) + 1 ) / d ) )
                                c_bg_2 = ( kbc_2 < ( ( int( b["cmyk_d2"] * d ) ) / d ) ) or ( kbc_2 >= ( ( math.ceil( b["cmyk_d2"] * d ) + 1 ) / d ) )
                                c_bg_3 = ( kbc_3 < ( ( int( b["cmyk_d3"] * d ) ) / d ) ) or ( kbc_3 >= ( ( math.ceil( b["cmyk_d3"] * d ) + 1 ) / d ) )
                                c_bg_4 = ( kbc_4 < ( ( int( b["cmyk_d4"] * d ) ) / d ) ) or ( kbc_4 >= ( ( math.ceil( b["cmyk_d4"] * d ) + 1 ) / d ) )
                            if ( d_cd == "F16" or d_cd == "F32" ):
                                c_fg_1 = kac_1 != a["cmyk_d1"]
                                c_fg_2 = kac_2 != a["cmyk_d2"]
                                c_fg_3 = kac_3 != a["cmyk_d3"]
                                c_fg_4 = kac_4 != a["cmyk_d4"]
                                c_bg_1 = kbc_1 != b["cmyk_d1"]
                                c_bg_2 = kbc_2 != b["cmyk_d2"]
                                c_bg_3 = kbc_3 != b["cmyk_d3"]
                                c_bg_4 = kbc_4 != b["cmyk_d4"]

                            # Operation
                            if ( c_fg_1 == True or c_fg_2 == True or c_fg_3 == True or c_fg_4 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "CMYK", kac_1, kac_2, kac_3, kac_4, a )
                            if ( c_bg_1 == True or c_bg_2 == True or c_bg_3 == True or c_bg_4 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "CMYK", kbc_1, kbc_2, kbc_3, kbc_4, b )
                        elif d_cm == "YUV":
                            # Foreground and Background Colors ( Krita is in YUV )
                            kac_1 = order_fg[0]
                            kac_2 = order_fg[1]
                            kac_3 = order_fg[2]
                            kbc_1 = order_bg[0]
                            kbc_2 = order_bg[1]
                            kbc_3 = order_bg[2]

                            # Range
                            if ( d_cd == "U8" or d_cd == "U16" ):
                                c_fg_1 = ( kac_1 < ( ( int( a["yuv_d1"] * d ) ) / d ) ) or ( kac_1 >= ( ( int( a["yuv_d1"] * d ) + 1 ) / d ) )
                                c_fg_2 = ( kac_2 < ( ( int( a["yuv_d2"] * d ) ) / d ) ) or ( kac_2 >= ( ( int( a["yuv_d2"] * d ) + 1 ) / d ) )
                                c_fg_3 = ( kac_3 < ( ( int( a["yuv_d3"] * d ) ) / d ) ) or ( kac_3 >= ( ( int( a["yuv_d3"] * d ) + 1 ) / d ) )
                                c_bg_1 = ( kbc_1 < ( ( int( b["yuv_d1"] * d ) ) / d ) ) or ( kbc_1 >= ( ( int( b["yuv_d1"] * d ) + 1 ) / d ) )
                                c_bg_2 = ( kbc_2 < ( ( int( b["yuv_d2"] * d ) ) / d ) ) or ( kbc_2 >= ( ( int( b["yuv_d2"] * d ) + 1 ) / d ) )
                                c_bg_3 = ( kbc_3 < ( ( int( b["yuv_d3"] * d ) ) / d ) ) or ( kbc_3 >= ( ( int( b["yuv_d3"] * d ) + 1 ) / d ) )
                            if ( d_cd == "F16" or d_cd == "F32" ):
                                c_fg_1 = kac_1 != a["yuv_d1"]
                                c_fg_2 = kac_2 != a["yuv_d2"]
                                c_fg_3 = kac_3 != a["yuv_d3"]
                                c_bg_1 = kbc_1 != b["yuv_d1"]
                                c_bg_2 = kbc_2 != b["yuv_d2"]
                                c_bg_3 = kbc_3 != b["yuv_d3"]

                            # Operation
                            if ( c_fg_1 == True or c_fg_2 == True or c_fg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "YUV", kac_1, kac_2, kac_3, 0, a )
                            if ( c_bg_1 == True or c_bg_2 == True or c_bg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "YUV", kbc_1, kbc_2, kbc_3, 0, b )
                        elif d_cm == "XYZ":
                            # Foreground and Background Colors ( Krita is in XYZ )
                            kac_1 = order_fg[0]
                            kac_2 = order_fg[1]
                            kac_3 = order_fg[2]
                            kbc_1 = order_bg[0]
                            kbc_2 = order_bg[1]
                            kbc_3 = order_bg[2]

                            # Range
                            if ( d_cd == "U8" or d_cd == "U16" ):
                                c_fg_1 = ( kac_1 < ( ( int( a["xyz_d1"] * d ) ) / d ) ) or ( kac_1 >= ( ( int( a["xyz_d1"] * d ) + 1 ) / d ) )
                                c_fg_2 = ( kac_2 < ( ( int( a["xyz_d2"] * d ) ) / d ) ) or ( kac_2 >= ( ( int( a["xyz_d2"] * d ) + 1 ) / d ) )
                                c_fg_3 = ( kac_3 < ( ( int( a["xyz_d3"] * d ) ) / d ) ) or ( kac_3 >= ( ( int( a["xyz_d3"] * d ) + 1 ) / d ) )
                                c_bg_1 = ( kbc_1 < ( ( int( b["xyz_d1"] * d ) ) / d ) ) or ( kbc_1 >= ( ( int( b["xyz_d1"] * d ) + 1 ) / d ) )
                                c_bg_2 = ( kbc_2 < ( ( int( b["xyz_d2"] * d ) ) / d ) ) or ( kbc_2 >= ( ( int( b["xyz_d2"] * d ) + 1 ) / d ) )
                                c_bg_3 = ( kbc_3 < ( ( int( b["xyz_d3"] * d ) ) / d ) ) or ( kbc_3 >= ( ( int( b["xyz_d3"] * d ) + 1 ) / d ) )
                            if ( d_cd == "F16" or d_cd == "F32" ):
                                c_fg_1 = kac_1 != a["xyz_d1"]
                                c_fg_2 = kac_2 != a["xyz_d2"]
                                c_fg_3 = kac_3 != a["xyz_d3"]
                                c_bg_1 = kbc_1 != b["xyz_d1"]
                                c_bg_2 = kbc_2 != b["xyz_d2"]
                                c_bg_3 = kbc_3 != b["xyz_d3"]

                            # Operation
                            if ( c_fg_1 == True or c_fg_2 == True or c_fg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "XYZ", kac_1, kac_2, kac_3, 0, a )
                            if ( c_bg_1 == True or c_bg_2 == True or c_bg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "XYZ", kbc_1, kbc_2, kbc_3, 0, b )
                        elif d_cm == "LAB":
                            # Foreground and Background Colors ( Krita is in LAB )
                            kac_1 = order_fg[0]
                            kac_2 = order_fg[1]
                            kac_3 = order_fg[2]
                            kbc_1 = order_bg[0]
                            kbc_2 = order_bg[1]
                            kbc_3 = order_bg[2]

                            # Range
                            if ( d_cd == "U8" or d_cd == "U16" ):
                                c_fg_1 = ( kac_1 < ( ( int( a["lab_d1"] * d ) ) / d ) ) or ( kac_1 >= ( ( int( a["lab_d1"] * d ) + 1 ) / d ) )
                                c_fg_2 = ( kac_2 < ( ( int( a["lab_d2"] * d ) ) / d ) ) or ( kac_2 >= ( ( int( a["lab_d2"] * d ) + 1 ) / d ) )
                                c_fg_3 = ( kac_3 < ( ( int( a["lab_d3"] * d ) ) / d ) ) or ( kac_3 >= ( ( int( a["lab_d3"] * d ) + 1 ) / d ) )
                                c_bg_1 = ( kbc_1 < ( ( int( b["lab_d1"] * d ) ) / d ) ) or ( kbc_1 >= ( ( int( b["lab_d1"] * d ) + 1 ) / d ) )
                                c_bg_2 = ( kbc_2 < ( ( int( b["lab_d2"] * d ) ) / d ) ) or ( kbc_2 >= ( ( int( b["lab_d2"] * d ) + 1 ) / d ) )
                                c_bg_3 = ( kbc_3 < ( ( int( b["lab_d3"] * d ) ) / d ) ) or ( kbc_3 >= ( ( int( b["lab_d3"] * d ) + 1 ) / d ) )
                            if ( d_cd == "F16" or d_cd == "F32" ):
                                c_fg_1 = kac_1 != a["lab_d1"]
                                c_fg_2 = kac_2 != a["lab_d2"]
                                c_fg_3 = kac_3 != a["lab_d3"]
                                c_bg_1 = kbc_1 != b["lab_d1"]
                                c_bg_2 = kbc_2 != b["lab_d2"]
                                c_bg_3 = kbc_3 != b["lab_d3"]

                            # Operation
                            if ( c_fg_1 == True or c_fg_2 == True or c_fg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "LAB", kac_1, kac_2, kac_3, 0, a )
                            if ( c_bg_1 == True or c_bg_2 == True or c_bg_3 == True ):
                                if not eraser.isChecked():
                                    self.Pigmento_READ( "LAB", kbc_1, kbc_2, kbc_3, 0, b )
                    else: # Vector Read
                        # Variables
                        v = 255

                        # Foreground Color
                        fgc_canvas = doc["fgc"].colorForCanvas( doc["vc"] )
                        kac_1 = fgc_canvas.red() / v
                        kac_2 = fgc_canvas.green() / v
                        kac_3 = fgc_canvas.blue() / v
                        # Background Color
                        bgc_canvas = doc["bgc"].colorForCanvas( doc["vc"] )
                        kbc_1 = bgc_canvas.red() / v
                        kbc_2 = bgc_canvas.green() / v
                        kbc_3 = bgc_canvas.blue() / v

                        # Range
                        c_fg_1 = ( kac_1 < ( ( int( a["rgb_d1"] * v ) ) / v ) ) or ( kac_1 >= ( ( int( a["rgb_d1"] * v ) + 1 ) / v ) )
                        c_fg_2 = ( kac_2 < ( ( int( a["rgb_d2"] * v ) ) / v ) ) or ( kac_2 >= ( ( int( a["rgb_d2"] * v ) + 1 ) / v ) )
                        c_fg_3 = ( kac_3 < ( ( int( a["rgb_d3"] * v ) ) / v ) ) or ( kac_3 >= ( ( int( a["rgb_d3"] * v ) + 1 ) / v ) )
                        c_bg_1 = ( kbc_1 < ( ( int( b["rgb_d1"] * v ) ) / v ) ) or ( kbc_1 >= ( ( int( b["rgb_d1"] * v ) + 1 ) / v ) )
                        c_bg_2 = ( kbc_2 < ( ( int( b["rgb_d2"] * v ) ) / v ) ) or ( kbc_2 >= ( ( int( b["rgb_d2"] * v ) + 1 ) / v ) )
                        c_bg_3 = ( kbc_3 < ( ( int( b["rgb_d3"] * v ) ) / v ) ) or ( kbc_3 >= ( ( int( b["rgb_d3"] * v ) + 1 ) / v ) )

                        # Operation
                        if ( c_fg_1 == True or c_fg_2 == True or c_fg_3 == True ):
                            self.Pigmento_READ( "RGB", kac_1, kac_2, kac_3, 0, a )
                        if ( c_bg_1 == True or c_bg_2 == True or c_bg_3 == True ):
                            self.Pigmento_READ( "RGB", kbc_1, kbc_2, kbc_3, 0, b )
                elif self.mode_index == 2:
                    self.Read_Only()
            except:
                pass

            # Fill Check ( case active node changes )
            if self.Fill_Check( doc ) == False:
                self.Fill_None()
        else:
            self.Fill_None()

        # Variables for next Cycle
        if self.doc != doc:
            self.doc = doc
            self.convert.Set_Document( d_cm, d_cd, d_cp )
    def Pigmento_to_Krita( self, release ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            if ( self.mode_index in ( 0 , 1 ) and release == True ):
                # Check Eraser Mode ON or OFF
                eraser = Krita.instance().action( "erase_action" )
                # Current Document
                doc = self.Current_Document()
                d_cm = doc["d_cm"]
                d_cd = doc["d_cd"]
                d_cp = doc["d_cp"]
                vc = doc["vc"]

                # Managed Color
                if self.ui_harmony == True:
                    if self.harmony_index == 1:
                        self.Color_Managed( d_cm, d_cd, d_cp, vc, "FG", har_01 )
                    if self.harmony_index == 2:
                        self.Color_Managed( d_cm, d_cd, d_cp, vc, "FG", har_02 )
                    if self.harmony_index == 3:
                        self.Color_Managed( d_cm, d_cd, d_cp, vc, "FG", har_03 )
                    if self.harmony_index == 4:
                        self.Color_Managed( d_cm, d_cd, d_cp, vc, "FG", har_04 )
                    if self.harmony_index == 5:
                        self.Color_Managed( d_cm, d_cd, d_cp, vc, "FG", har_05 )
                else:
                    self.Color_Managed( d_cm, d_cd, d_cp, vc, "FG", kac )
                    self.Color_Managed( d_cm, d_cd, d_cp, vc, "BG", kbc )

                # Save
                Krita.instance().writeSetting( "Pigment.O", "kac", str( kac ) )
                Krita.instance().writeSetting( "Pigment.O", "kbc", str( kbc ) )

                # If Eraser was true, set it ON again
                if eraser.isChecked():
                    eraser.trigger()

                # Fill with Foreground Color
                if self.Fill_Check( doc ) == True:
                    Krita.instance().action( "fill_selection_foreground_color_opacity" ).trigger()
                else:
                    self.Fill_None()

    def Read_Only( self ):
        # Variables
        c1 = 255
        c2 = 255
        c3 = 255

        # Foreground Color
        color_fg = Krita.instance().activeWindow().activeView().foregroundColor()
        order_fg = color_fg.componentsOrdered()
        fg_1 = int( order_fg[0] * c1 )
        fg_2 = int( order_fg[1] * c2 )
        fg_3 = int( order_fg[2] * c3 )

        # Foreground Color
        color_bg = Krita.instance().activeWindow().activeView().backgroundColor()
        order_bg = color_bg.componentsOrdered()
        bg_1 = int( order_bg[0] * c1 )
        bg_2 = int( order_bg[1] * c2 )
        bg_3 = int( order_bg[2] * c3 )

        # Print Debug
        QtCore.qDebug( "---------------------" )
        QtCore.qDebug( "fg_1 = " + str( fg_1 ) )
        QtCore.qDebug( "fg_2 = " + str( fg_2 ) )
        QtCore.qDebug( "fg_3 = " + str( fg_3 ) )
        QtCore.qDebug( "" )
        QtCore.qDebug( "bg_1 = " + str( bg_1 ) )
        QtCore.qDebug( "bg_2 = " + str( bg_2 ) )
        QtCore.qDebug( "bg_3 = " + str( bg_3 ) )
        QtCore.qDebug( "" )

    #endregion
    #region Pigmento Paths #########################################################

    def Pigmento_READ( self, mode, var_1, var_2, var_3, var_4, color ):
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( False, True, True )
    def Pigmento_APPLY( self, mode, var_1, var_2, var_3, var_4, color ):
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( True, True, True )
    def Pigmento_PRESS( self, mode, var_1, var_2, var_3, var_4, color ):
        self.widget_press = True
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( not self.performance_release, True, False )
    def Pigmento_RELEASE( self ):
        self.widget_press = False
        self.Sync_Elements( True, True, True )

    #endregion
    #region Pigmento & Scripts #####################################################

    def Script_Request_FG( self ):
        return kac
    def Script_Request_BG( self ):
        return kbc
    def Script_Color_Name( self, hex ):
        name = self.convert.hex6_to_name( hex, color_names )
        return name
    def Script_Convert_Color( self, mode, var_1, var_2, var_3, var_4, color ):
        convert = self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        return convert

    def Script_Input_Preview( self, mode, var_1, var_2, var_3, var_4 ):
        self.widget_press = True
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, self.cor )
        self.Sync_Elements( False, True, False )
        return self.cor
    def Script_Input_Apply( self, mode, var_1, var_2, var_3, var_4 ):
        self.widget_press = False
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, self.cor )
        self.Sync_Elements( True, True, True )
        return self.cor

    def Script_Printer( self, mode, geo, directory, render, start_from, max_val ):
        """
        mode - color space of the map
        geo - geometric shape of the map
        directory - location to save zip file
        render - location to render images. This folder is deleted and recreated after a cycle
        start_from - start from given given number. Default is zero but if non zero nothing will be deleted.
        max_val - finish at given number.

        notes - YUV=255 UVD=255 HSV=360 HSL=360 HSY=360 CD_CA=255
        """

        # Variables
        size = 256
        s2 = size * 0.5
        wtri = 0.5 * math.sqrt( 3 ) * size
        cda = [ "D", "A" ]

        # Range
        if start_from == None:
            start_from = 0
        if max_val == None:
            if geo in cda:
                max_val = 255
            else:
                max_val = 360

        # Document Modifier
        doc = self.Current_Document()
        d_cm = doc["d_cm"]
        d_cd = doc["d_cd"]
        d_cp = doc["d_cp"]
        vc = doc["vc"]

        # Temporary Folder
        zipname = f"{ d_cm }_{ mode }_{ geo }"
        temporary = os.path.join( render, zipname )
        os.mkdir( temporary, 0o666 )

        # Third Axis Loop
        for h in range( start_from, max_val+1 ):
            # Base Image to Edit
            qpixmap = QPixmap( size, size )
            qpixmap.fill( QColor( 0, 0, 0, 255 ) )
            qimage = qpixmap.toImage()

            # Calculate Pixels
            for y in range( 0, size ):
                for x in range( 0, size ):
                    # Variables
                    if geo in [ "3", "4", "R" ]:
                        # Hue
                        hue = h / max_val
                        # Hsx
                        inv_y = size-y
                        hsx = inv_y / size
                    if geo in cda:
                        # Hsx
                        hsx = h / max_val

                    # Geometry influence
                    if geo == "3":
                        if y >= 0 and y <= size * 0.5:
                            ix, iy = self.geometry.Trig_2D_Points_Lines_Intersection( 0, y, size, y, 1, 0, wtri + 1, size * 0.5 )
                        elif y > size * 0.5 and y <= size:
                            ix, iy = self.geometry.Trig_2D_Points_Lines_Intersection( 0, y, size, y, wtri + 1, size * 0.5, 1, size )
                        sat = self.geometry.Limit_Float( x / ix )
                    if geo == "4":
                        sat = x / size
                    if geo == "R":
                        if y >= 0 and y <= size * 0.5:
                            lix, liy = self.geometry.Trig_2D_Points_Lines_Intersection( 0, y, size, y, 0,    size * 0.5, size * 0.5, 0 )
                            rix, riy = self.geometry.Trig_2D_Points_Lines_Intersection( 0, y, size, y, size, size * 0.5, size * 0.5, 0 )
                        elif y > size*0.5 and y <= size:
                            lix, liy = self.geometry.Trig_2D_Points_Lines_Intersection( 0, y, size, y, 0,    size * 0.5, size * 0.5, size )
                            rix, riy = self.geometry.Trig_2D_Points_Lines_Intersection( 0, y, size, y, size, size * 0.5, size * 0.5, size )
                        dist = abs( rix - lix )
                        margin = abs( ( size - dist ) * 0.5 )
                        dx = x - margin
                        if ( dx > 0 and dist > 0 ):
                            sat = self.geometry.Limit_Range( dx / dist, 0, 1 )
                        else:
                            sat = 0
                    if geo in cda:
                        # Geometry
                        dist = self.geometry.Trig_2D_Points_Distance( x, y, s2, s2 )
                        if geo == "D":
                            angle = self.geometry.Trig_2D_Points_Lines_Angle( 0, s2, s2, s2, x, y ) / 360
                        if geo == "A":
                            hhh = self.geometry.Limit_Looper( self.geometry.Trig_2D_Points_Lines_Angle( 0, s2, s2, s2, x, y ) + hue_a, 360 )
                            angle = self.convert.huea_to_hued( hhh / 360 )
                        # Values
                        hue = angle
                        sat = self.geometry.Limit_Range( dist / s2, 0, 1 )

                    # Color Spaces to RGB
                    if mode == "YUV":
                        rgb = self.convert.yuv_to_rgb( h / max_val, x / 255, inv_y / 255 )
                    if mode == "UVD":
                        rgb = self.convert.uvd_to_rgb( x / 127.5 - 1, inv_y / 127.5 - 1, h / max_val )
                    if mode == "HSV":
                        rgb = self.convert.hsv_to_rgb( hue, sat, hsx )
                    if mode == "HSL":
                        rgb = self.convert.hsl_to_rgb( hue, sat, hsx )
                    if mode == "HSY":
                        rgb = self.convert.hsy_to_rgb( hue, sat, hsx )
                    if mode == "ARD":
                        rgb = self.convert.ard_to_rgb( hue, sat, hsx )

                    # Document Modifier
                    if d_cm == None:
                        color = rgb
                    if d_cm == "A":
                        aaa = self.convert.rgb_to_aaa( rgb[0], rgb[1], rgb[2] )
                        color = self.Color_Display( d_cm, d_cd, d_cp, vc, aaa )
                    if d_cm == "RGB":
                        color = self.Color_Display( d_cm, d_cd, d_cp, vc, rgb )
                    if d_cm == "CMYK":
                        cmyk = self.convert.rgb_to_cmyk( rgb[0], rgb[1], rgb[2], None )
                        color = self.Color_Display( d_cm, d_cd, d_cp, vc, cmyk )
                    if d_cm == "YUV":
                        yuv = self.convert.rgb_to_yuv( rgb[0], rgb[1], rgb[2] )
                        color = self.Color_Display( d_cm, d_cd, d_cp, vc, yuv )

                    # Write Pixels
                    qimage.setPixelColor( x, y, QColor( color[0]*255, color[1]*255, color[2]*255 ) )

            # Save Image to File
            qpixmap = QPixmap().fromImage( qimage )
            filename = mode + "_" + geo + "_" + str( h ).zfill( 3 ) + ".png"
            location = os.path.join( temporary, filename )
            qpixmap.save( location )

        if start_from == 0:
            # Create Zip File
            basename = os.path.join( directory, zipname )
            shutil.make_archive( basename, "zip", temporary )

            # Delete all Render Files
            shutil.rmtree( temporary )

    def Pigmento_Sample_Script( self ):
        # Import Pigment.O reference object
        """
        import krita

        pigmento_pyid = "pykrita_pigment_o"
        dockers = Krita.instance().dockers()
        for i in range( 0, len( dockers ) ):
            if dockers[i].objectName() == pigmento_pyid:
                pigment_o = dockers[i]
        """

        # Print Maps
        """
        space = [ "HSV", "HSL", "HSY" ]
        geo = [ "3", "4", "R" ]
        directory = "C:\\Users\\EyeOd\\Desktop\\pigmento\\Directory" # path to finished zip folder
        render = "C:\\Users\\EyeOd\\Desktop\\pigmento\\Render" # path to temporary render folder
        for g in range( 0, len( geo ) ):
            for s in range( 0, len( space ) ):
                pigment_o.Script_Printer( space[s], geo[g], directory, render, None, None )
        """

        # Apply Color
        """
        pigment_o.Script_Input_FG( "RGB", 0.25, 0.50, 0.75, 0 )
        """
    def Krita_Sample_Script( self ):
        # Read Color
        """
        from krita import *

        color_fg = Krita.instance().activeWindow().activeView().foregroundColor()
        order_fg = color_fg.componentsOrdered()
        r = order_fg[0]
        g = order_fg[1]
        b = order_fg[2]

        print( "red " + str( r ) )
        print( "green " + str( g ) )
        print( "blue " + str( b ) )
        """

        # Write Color
        """
        from krita import *

        d_cm = Krita.instance().activeDocument().colorModel()
        d_cd = Krita.instance().activeDocument().colorDepth()
        d_cp = Krita.instance().activeDocument().colorProfile()

        managed_color = ManagedColor( d_cm, d_cd, d_cp )
        comp = managed_color.components()
        red   = 0.4
        green = 0.5
        blue  = 0.6
        alpha = 1
        comp = [blue, green, red, alpha]
        managed_color.setComponents( comp )
        Krita.instance().activeWindow().activeView().setForeGroundColor( managed_color )
        """

    def Script_Image_Analyse( self, path ):
        exists = os.path.exists( path )
        null = QImage( path ).isNull()
        if ( exists == True and null == False ):
            self.Color_Analyse( path )

    #endregion
    #region Color ##################################################################

    def Color_Convert( self, mode, var_1, var_2, var_3, var_4, color ):
        # cmyk calculation uses self.lock_cmyk_4
        # hue calculation uses self.wheel_mode
        # kkk calculation uses self.lock_kkk_1

        #region Adjustments

        if mode == "KKK":
            color["kkk_percent"] = var_1
            color["kkk_scale"] = var_2
            self.Kelvin_Class( var_2 )

        #endregion
        #region Convert to RGB+XYZ

        if mode == "A":
            aaa = [var_1]
            rgb = [aaa[0], aaa[0], aaa[0]]
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = 0
        if mode == "RGB":
            rgb = [var_1, var_2, var_3]
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( var_1, var_2, var_3 )
        if mode == "UVD":
            uvd = [var_1, var_2, var_3]
            rgb = self.convert.uvd_to_rgb( uvd[0], uvd[1], uvd[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "CMY":
            cmy = [var_1, var_2, var_3]
            rgb = self.convert.cmy_to_rgb( cmy[0], cmy[1], cmy[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "CMYK":
            cmyk = [var_1, var_2, var_3, var_4]
            rgb = self.convert.cmyk_to_rgb( cmyk[0], cmyk[1], cmyk[2], cmyk[3] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "RYB":
            ryb = [var_1, var_2, var_3]
            rgb = self.convert.ryb_to_rgb( ryb[0], ryb[1], ryb[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "YUV":
            yuv = [var_1, var_2, var_3]
            rgb = self.convert.yuv_to_rgb( yuv[0], yuv[1], yuv[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )

        if mode == "HSV":
            hue_d = var_1
            hsv = [var_1, var_2, var_3]
            rgb = self.convert.hsv_to_rgb( hsv[0], hsv[1], hsv[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        if mode == "HSL":
            hue_d = var_1
            hsl = [var_1, var_2, var_3]
            rgb = self.convert.hsl_to_rgb( hsl[0], hsl[1], hsl[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        if mode == "HSY":
            hue_d = var_1
            hsy = [var_1, var_2, var_3]
            rgb = self.convert.hsy_to_rgb( hsy[0], hsy[1], hsy[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        if mode == "ARD":
            hue_d = var_1
            ard = [var_1, var_2, var_3]
            rgb = self.convert.ard_to_rgb( ard[0], ard[1], ard[2] )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )

        if mode == "XYZ":
            xyz = [var_1, var_2, var_3]
            rgb = self.convert.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "XYY":
            xyy = [var_1, var_2, var_3]
            xyz = self.convert.xyy_to_xyz( xyy[0], xyy[1], xyy[2] )
            rgb = self.convert.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "LAB":
            lab = [var_1, var_2, var_3]
            xyz = self.convert.lab_to_xyz( lab[0], lab[1], lab[2] )
            rgb = self.convert.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )

        if mode == "LCH":
            lch = [var_1, var_2, var_3]
            lab = self.convert.lch_to_lab( lch[0], lch[1], lch[2] )
            xyz = self.convert.lab_to_xyz( lab[0], lab[1], lab[2] )
            rgb = self.convert.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )

        if mode == "KKK":
            if self.lock_kkk_1 == False:
                kkk = self.convert.kkk_to_rgb( color["kkk_scale"], kelvin_rgb )
                rgb = ( color["rgb_1"], color["rgb_2"], color["rgb_3"] )
            else: # False
                kkk = [1, 1, 1]
                rgb = self.convert.kkk_to_rgb( color["kkk_scale"], kelvin_rgb )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
        if mode == "HEX":
            rgb = self.convert.hex6_to_rgb( var_1 )
            xyz = self.convert.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
            hue_d = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )


        #endregion
        #region Convert RGB+XYZ into Other

        # HUE
        self.convert.Set_Hue( hue_d )
        hue_a = self.convert.hued_to_huea( hue_d )

        if mode != "A":
            aaa = self.convert.rgb_to_aaa( rgb[0], rgb[1], rgb[2] )
        if mode != "RGB":
            pass
        if mode != "UVD":
            uvd = self.convert.rgb_to_uvd( rgb[0], rgb[1], rgb[2] )
        if mode != "CMY":
            cmy = self.convert.rgb_to_cmy( rgb[0], rgb[1], rgb[2] )
        if mode != "CMYK":
            key = lambda k: None if k==False else color["cmyk_4"]
            cmyk = self.convert.rgb_to_cmyk( rgb[0], rgb[1], rgb[2], key( self.lock_cmyk_4 ) )
        if mode != "RYB":
            ryb = self.convert.rgb_to_ryb( rgb[0], rgb[1], rgb[2] )
        if mode != "YUV":
            yuv = self.convert.rgb_to_yuv( rgb[0], rgb[1], rgb[2] )

        if mode != "HSV":
            hsv = self.convert.rgb_to_hsv( rgb[0], rgb[1], rgb[2] )
        if mode != "HSL":
            hsl = self.convert.rgb_to_hsl( rgb[0], rgb[1], rgb[2] )
        if mode != "HSY":
            hsy = self.convert.rgb_to_hsy( rgb[0], rgb[1], rgb[2] )
        if mode != "ARD":
            ard = self.convert.rgb_to_ard( rgb[0], rgb[1], rgb[2] )

        if mode != "XYZ":
            pass
        if mode != "XYY":
            xyy = self.convert.xyz_to_xyy( xyz[0], xyz[1], xyz[2] )
        if mode != "LAB":
            lab = self.convert.xyz_to_lab( xyz[0], xyz[1], xyz[2] )

        if mode != "LCH":
            lch = self.convert.lab_to_lch( lab[0], lab[1], lab[2] )

        if mode != "KKK":
            if self.lock_kkk_1 == False:
                kkk = self.convert.kkk_to_rgb( color["kkk_scale"], kelvin_rgb )
            else:
                kkk = [1, 1, 1]

        #endregion
        #region Variables

        # HEX
        hex_code = self.convert.rgb_to_hex6( rgb[0], rgb[1], rgb[2] )
        name = self.convert.hex6_to_name( hex_code, color_names )
        color["hex6"] = hex_code
        color["name"] = name
        # RGB Depth Error Correction
        checkdepth = uvd[2] - self.depth_previous
        if (checkdepth >= -( 1 / krange["uvd_3"] ) and checkdepth <= ( 1 / krange["uvd_3"] ) ):
            uvd[2] = self.depth_previous
            ard[2] = self.depth_previous

        # AAA
        color["aaa_1"] = aaa[0]
        # RGB
        color["rgb_1"] = rgb[0]
        color["rgb_2"] = rgb[1]
        color["rgb_3"] = rgb[2]
        # UVD
        color["uvd_1"] = uvd[0]
        color["uvd_2"] = uvd[1]
        color["uvd_3"] = uvd[2]
        # CMY
        color["cmy_1"] = cmy[0]
        color["cmy_2"] = cmy[1]
        color["cmy_3"] = cmy[2]
        # CMYK
        color["cmyk_1"] = cmyk[0]
        color["cmyk_2"] = cmyk[1]
        color["cmyk_3"] = cmyk[2]
        color["cmyk_4"] = cmyk[3]
        # RYB
        color["ryb_1"] = ryb[0]
        color["ryb_2"] = ryb[1]
        color["ryb_3"] = ryb[2]
        # YUV
        color["yuv_1"] = yuv[0]
        color["yuv_2"] = yuv[1]
        color["yuv_3"] = yuv[2]

        # HUE
        color["hue_d"] = hue_d
        color["hue_a"] = hue_a
        # HSV
        color["hsv_1"] = hue_d
        color["hsv_2"] = hsv[1]
        color["hsv_3"] = hsv[2]
        # HSL
        color["hsl_1"] = hue_d
        color["hsl_2"] = hsl[1]
        color["hsl_3"] = hsl[2]
        # HSY
        color["hsy_1"] = hue_d
        color["hsy_2"] = hsy[1]
        color["hsy_3"] = hsy[2]
        # ARD
        color["ard_1"] = hue_d
        color["ard_2"] = ard[1]
        color["ard_3"] = ard[2]

        # XYZ
        color["xyz_1"] = xyz[0]
        color["xyz_2"] = xyz[1]
        color["xyz_3"] = xyz[2]
        # XYY
        color["xyy_1"] = xyy[0]
        color["xyy_2"] = xyy[1]
        color["xyy_3"] = xyy[2]
        # LAB
        color["lab_1"] = lab[0]
        color["lab_2"] = lab[1]
        color["lab_3"] = lab[2]

        # LCH
        color["lch_1"] = lch[0]
        color["lch_2"] = lch[1]
        color["lch_3"] = lch[2]

        #endregion
        #region Finish

        # Kelvin Multiplication
        kr = rgb[0] * kkk[0]
        kg = rgb[1] * kkk[1]
        kb = rgb[2] * kkk[2]
        display = [kr, kg, kb]
        color["rgb_d1"] = kr
        color["rgb_d2"] = kg
        color["rgb_d3"] = kb

        # Display
        doc = self.Current_Document()
        d_cm = doc["d_cm"]
        if d_cm == "A":
            kaaa = self.convert.rgb_to_aaa( kr, kg, kb )
            color["aaa_d1"] = kaaa[0]
            display = kaaa
        if d_cm == "CMYK":
            key = lambda k: None if k==False else self.convert.rgb_to_k( kr, kg, kb )
            kcmyk = self.convert.rgb_to_cmyk( kr, kg, kb, key( self.lock_cmyk_4 ) )
            color["cmyk_d1"] = kcmyk[0]
            color["cmyk_d2"] = kcmyk[1]
            color["cmyk_d3"] = kcmyk[2]
            color["cmyk_d4"] = kcmyk[3]
            display = kcmyk
        if d_cm == "YUV":
            kyuv = self.convert.rgb_to_yuv( kr, kg, kb )
            color["yuv_d1"] = kyuv[0]
            color["yuv_d2"] = kyuv[1]
            color["yuv_d3"] = kyuv[2]
            display = kyuv
        if d_cm == "XYZ":
            kxyz = self.convert.rgb_to_xyz( kr, kg, kb )
            color["xyz_d1"] = kxyz[0]
            color["xyz_d2"] = kxyz[1]
            color["xyz_d3"] = kxyz[2]
            display = kxyz
        if d_cm == "LAB":
            klab = self.convert.rgb_to_lab( kr, kg, kb )
            color["lab_d1"] = klab[0]
            color["lab_d2"] = klab[1]
            color["lab_d3"] = klab[2]
            display = klab
        # HEX
        disp_rgb = self.Color_Display( doc["d_cm"], doc["d_cd"], doc["d_cp"], doc["vc"], display )
        color["hex6_d"] = self.convert.rgb_to_hex6( disp_rgb[0], disp_rgb[1], disp_rgb[2] )

        #endregion

        # Return
        return color
    def Color_Harmony( self, span, hue_1, hue_2, hue_3, hue_4, hue_5 ):
        try:
            # Variables
            comp = 0.5

            # Wheel
            if self.wheel_mode == "DIGITAL":index = "hue_d"
            if self.wheel_mode == "ANALOG":index = "hue_a"
            # Director Angle
            if self.harmony_index == 1:angulus = hue_1[ index ]
            if self.harmony_index == 2:angulus = hue_2[ index ]
            if self.harmony_index == 3:angulus = hue_3[ index ]
            if self.harmony_index == 4:angulus = hue_4[ index ]
            if self.harmony_index == 5:angulus = hue_5[ index ]

            # Rules
            if self.harmony_rule == "Monochromatic":
                if self.harmony_index in ( 1, 2, 3, 4, 5 ):
                    angle_1 = angulus
                    angle_2 = angulus
                    angle_3 = angulus
                    angle_4 = angulus
                    angle_5 = angulus
            if self.harmony_rule == "Complementary":
                if self.harmony_index in ( 1, 2, 3 ):
                    angle_1 = angulus
                    angle_2 = angulus
                    angle_3 = angulus
                    angle_4 = self.geometry.Limit_Looper( angulus + comp , 1 )
                    angle_5 = self.geometry.Limit_Looper( angulus + comp , 1 )
                if self.harmony_index in ( 4, 5 ):
                    angle_1 = self.geometry.Limit_Looper( angulus - comp , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus - comp , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus - comp , 1 )
                    angle_4 = angulus
                    angle_5 = angulus
            if self.harmony_rule == "Analogous":
                if self.harmony_index == 1:
                    angle_1 = angulus
                    angle_2 = self.geometry.Limit_Looper( angulus + span * 0.25 , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus + span * 0.50 , 1 )
                    angle_4 = self.geometry.Limit_Looper( angulus + span * 0.75 , 1 )
                    angle_5 = self.geometry.Limit_Looper( angulus + span * 1.00 , 1 )
                if self.harmony_index == 2:
                    angle_1 = self.geometry.Limit_Looper( angulus - span * 0.25 , 1 )
                    angle_2 = angulus
                    angle_3 = self.geometry.Limit_Looper( angulus + span * 0.25 , 1 )
                    angle_4 = self.geometry.Limit_Looper( angulus + span * 0.50 , 1 )
                    angle_5 = self.geometry.Limit_Looper( angulus + span * 0.75 , 1 )
                if self.harmony_index == 3:
                    angle_1 = self.geometry.Limit_Looper( angulus - span * 0.50 , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus - span * 0.25 , 1 )
                    angle_3 = angulus
                    angle_4 = self.geometry.Limit_Looper( angulus + span * 0.25 , 1 )
                    angle_5 = self.geometry.Limit_Looper( angulus + span * 0.50 , 1 )
                if self.harmony_index == 4:
                    angle_1 = self.geometry.Limit_Looper( angulus - span * 0.75 , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus - span * 0.50 , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus - span * 0.25 , 1 )
                    angle_4 = angulus
                    angle_5 = self.geometry.Limit_Looper( angulus + span * 0.25 , 1 )
                if self.harmony_index == 5:
                    angle_1 = self.geometry.Limit_Looper( angulus - span * 1.00 , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus - span * 0.75 , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus - span * 0.50 , 1 )
                    angle_4 = self.geometry.Limit_Looper( angulus - span * 0.25 , 1 )
                    angle_5 = angulus
            if self.harmony_rule == "Triadic":
                if self.harmony_index == 1:
                    angle_1 = angulus
                    angle_2 = self.geometry.Limit_Looper( angulus + comp - span * 0.50 , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus + comp + span * 0.50 , 1 )
                if self.harmony_index == 2:
                    angle_1 = self.geometry.Limit_Looper( angulus + comp + span * 0.50 , 1 )
                    angle_2 = angulus
                    angle_3 = self.geometry.Limit_Looper( angulus + span * 1.00        , 1 )
                if self.harmony_index == 3:
                    angle_1 = self.geometry.Limit_Looper( angulus + comp - span * 0.50 , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus - span * 1.00        , 1 )
                    angle_3 = angulus
                angle_4 = 0
                angle_5 = 0
            if self.harmony_rule == "Tetradic":
                if self.harmony_index == 1:
                    angle_1 = angulus
                    angle_2 = self.geometry.Limit_Looper( angulus + span        , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus + comp        , 1 )
                    angle_4 = self.geometry.Limit_Looper( angulus + comp + span , 1 )
                if self.harmony_index == 2:
                    angle_1 = self.geometry.Limit_Looper( angulus - span        , 1 )
                    angle_2 = angulus
                    angle_3 = self.geometry.Limit_Looper( angulus + comp - span , 1 )
                    angle_4 = self.geometry.Limit_Looper( angulus + comp        , 1 )
                if self.harmony_index == 3:
                    angle_1 = self.geometry.Limit_Looper( angulus + comp        , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus + comp + span , 1 )
                    angle_3 = angulus
                    angle_4 = self.geometry.Limit_Looper( angulus + span        , 1 )
                if self.harmony_index == 4:
                    angle_1 = self.geometry.Limit_Looper( angulus + comp - span , 1 )
                    angle_2 = self.geometry.Limit_Looper( angulus + comp        , 1 )
                    angle_3 = self.geometry.Limit_Looper( angulus - span        , 1 )
                    angle_4 = angulus
                angle_5 = 0

            if self.wheel_mode == "ANALOG":
                angle_1 = self.convert.huea_to_hued( angle_1 )
                angle_2 = self.convert.huea_to_hued( angle_2 )
                angle_3 = self.convert.huea_to_hued( angle_3 )
                angle_4 = self.convert.huea_to_hued( angle_4 )
                angle_5 = self.convert.huea_to_hued( angle_5 )

            # Wheel Mode
            mode = self.wheel_space
            if self.panel_index == "Hexagon":
                mode = "ARD"
            if self.panel_index == "Luma":
                mode = "YUV"
            # Channels
            c1, c2, c3 = self.Hue_Index( mode )

            if self.panel_index == "Luma":
                # Angulus no Edit
                if self.harmony_edit == False:
                    y1, u1, v1 = self.convert.yuv_to_angle( self.cor[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_1 - angulus , 1 ) )
                    y2, u2, v2 = self.convert.yuv_to_angle( self.cor[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_2 - angulus , 1 ) )
                    y3, u3, v3 = self.convert.yuv_to_angle( self.cor[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_3 - angulus , 1 ) )
                    y4, u4, v4 = self.convert.yuv_to_angle( self.cor[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_4 - angulus , 1 ) )
                    y5, u5, v5 = self.convert.yuv_to_angle( self.cor[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_5 - angulus , 1 ) )
                # Angulus with Edit
                if self.harmony_edit == True:
                    y1, u1, v1 = self.convert.yuv_to_angle( har_01[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_1 - angulus , 1 ) )
                    y2, u2, v2 = self.convert.yuv_to_angle( har_02[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_2 - angulus , 1 ) )
                    y3, u3, v3 = self.convert.yuv_to_angle( har_03[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_3 - angulus , 1 ) )
                    y4, u4, v4 = self.convert.yuv_to_angle( har_04[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_4 - angulus , 1 ) )
                    y5, u5, v5 = self.convert.yuv_to_angle( har_05[c1], self.cor[c2], self.cor[c3], self.geometry.Limit_Looper( angle_5 - angulus , 1 ) )
                # Harmony
                self.Color_Convert( mode, y1, u1, v1, 0, har_01 )
                self.Color_Convert( mode, y2, u2, v2, 0, har_02 )
                self.Color_Convert( mode, y3, u3, v3, 0, har_03 )
                self.Color_Convert( mode, y4, u4, v4, 0, har_04 )
                self.Color_Convert( mode, y5, u5, v5, 0, har_05 )
            else:
                # Angulus no Edit
                if self.harmony_edit == False:
                    self.Color_Convert( mode, angle_1, self.cor[c2], self.cor[c3], 0, har_01 )
                    self.Color_Convert( mode, angle_2, self.cor[c2], self.cor[c3], 0, har_02 )
                    self.Color_Convert( mode, angle_3, self.cor[c2], self.cor[c3], 0, har_03 )
                    self.Color_Convert( mode, angle_4, self.cor[c2], self.cor[c3], 0, har_04 )
                    self.Color_Convert( mode, angle_5, self.cor[c2], self.cor[c3], 0, har_05 )
                # Angulus with Edit
                if self.harmony_edit == True:
                    self.Color_Convert( mode, angle_1, har_01[c2], har_01[c3], 0, har_01 )
                    self.Color_Convert( mode, angle_2, har_02[c2], har_02[c3], 0, har_02 )
                    self.Color_Convert( mode, angle_3, har_03[c2], har_03[c3], 0, har_03 )
                    self.Color_Convert( mode, angle_4, har_04[c2], har_04[c3], 0, har_04 )
                    self.Color_Convert( mode, angle_5, har_05[c2], har_05[c3], 0, har_05 )

            # Save
            Krita.instance().writeSetting( "Pigment.O", "har_01", str( har_01 ) )
            Krita.instance().writeSetting( "Pigment.O", "har_02", str( har_02 ) )
            Krita.instance().writeSetting( "Pigment.O", "har_03", str( har_03 ) )
            Krita.instance().writeSetting( "Pigment.O", "har_04", str( har_04 ) )
            Krita.instance().writeSetting( "Pigment.O", "har_05", str( har_05 ) )
        except:
            pass
    def Color_HEX( self, hex_code ):
        try:
            # Variables
            check_null = ( hex_code == None or hex_code == "" )
            check_hex6 = self.HEX_Valid( hex_code, 6 )
            check_hex3 = self.HEX_Valid( hex_code, 3 )
            space = list( filter( None, re.findall( r"(GRAY|CMYK|AAA|RGB|CMY|RYB|YUV|HSV|HSL|HSY|XYZ|XYY|LAB|LCH)+", hex_code.upper() ) ) )
            if len( space ) > 0:
                color_space = space[0].upper()
            else:
                color_space = None
            values = list( filter( None, re.findall( r"[0-9\.0-9]*", hex_code) ) )
            vector = len( values )

            # Logic
            if check_null == True: # Null == Black (r=0, g=0, b=0)
                self.Color_Convert( "RGB", 0, 0, 0, 0, self.cor )
                self.Sync_Elements( True, True, True )
            elif ( check_hex6 == True or check_hex3 == True ): # HEX format
                if hex_code.startswith( "#" ) == False: # correct nomenclature
                    hex_code = "#" + hex_code
                if ( check_hex6 == True and len( hex_code ) == 7 ): #123456
                    rgb = self.convert.hex6_to_rgb( hex_code )
                    self.Color_Convert( "RGB", rgb[0], rgb[1], rgb[2], 0, self.cor )
                    self.Sync_Elements( True, True, True )
                if ( check_hex3 == True and len( hex_code ) == 4 ): #123
                    rgb = self.convert.hex3_to_rgb( hex_code )
                    self.Color_Convert( "RGB", rgb[0], rgb[1], rgb[2], 0, self.cor )
                    self.Sync_Elements( True, True, True )
            elif ( color_space in [ "A", "GRAY" ] and vector == 1 ): # GRAY(100)
                self.Color_Convert(
                    color_space,
                    int( values[0] ) / 255,
                    0,
                    0,
                    0,
                    self.cor
                    )
                self.Sync_Elements( True, True, True )
            elif ( color_space in [ "RGB", "CMY", "RYB", "YUV", "XYZ", "XYY", "LAB", "LCH" ] and vector == 3 ): # RGB(100, 100, 100)
                self.Color_Convert(
                    color_space,
                    int( values[0] ) / 255,
                    int( values[1] ) / 255,
                    int( values[2] ) / 255,
                    0,
                    self.cor
                    )
                self.Sync_Elements( True, True, True )
            elif ( color_space in [ "CMYK" ] and vector == 4 ): # CMYK(100, 100, 100, 100)
                self.Color_Convert(
                    color_space,
                    int( values[0] ) / 255,
                    int( values[1] ) / 255,
                    int( values[2] ) / 255,
                    int( values[3] ) / 255,
                    self.cor
                    )
                self.Sync_Elements( True, True, True )
            elif ( color_space in [ "HSV", "HSL","HSY" ] and vector == 3 ): #HSV(100, 100, 100)
                self.Color_Convert(
                    color_space,
                    int( values[0] ) / 360,
                    int( values[1] ) / 100,
                    int( values[2] ) / 100,
                    0,
                    self.cor
                    )
                self.Sync_Elements( True, True, True )
            else:# Red Green Blue
                # Variables
                name = hex_code.lower()
                item = list( color_names.items() )

                # Search Dictionary with color names
                for i in range( 0, len( item ) ):
                    key_i = item[i][0]
                    value_i = item[i][1]
                    for j in range( 0, len( value_i ) ):
                        value_ij = value_i[j].lower()
                        if value_ij == name:
                            self.Color_Convert( "HEX", key_i, 0, 0, 0, self.cor )
                            self.Sync_Elements( True, True, True )
                            break
        except Exception as e:
            try:QtCore.qDebug( "Pigment.O ERROR | " + str( e ) )
            except:pass

    def Color_Managed( self, d_cm, d_cd, d_cp, vc, side, color ):
        #region Color Management
        color_model = Krita.instance().activeDocument().colorModel()
        managed_color = ManagedColor( color_model, d_cd, d_cp )
        comp = managed_color.components()
        if d_cm == "A":
            kac_1 = color["aaa_d1"]
            comp = [kac_1, 1]
        if ( d_cm == "RGB" or d_cm == None ):
            kac_1 = color["rgb_d1"]
            kac_2 = color["rgb_d2"]
            kac_3 = color["rgb_d3"]
            if ( d_cd == "U8" or d_cd == "U16" ):
                comp = [kac_3, kac_2, kac_1, 1]
            if ( d_cd == "F16" or d_cd == "F32" ):
                comp = [kac_1, kac_2, kac_3, 1]
        if d_cm == "CMYK":
            kac_1 = color["cmyk_d1"]
            kac_2 = color["cmyk_d2"]
            kac_3 = color["cmyk_d3"]
            kac_4 = color["cmyk_d4"]
            comp = [kac_1, kac_2, kac_3, kac_4, 1]
        if d_cm == "YUV":
            kac_1 = color["yuv_d1"]
            kac_2 = color["yuv_d2"]
            kac_3 = color["yuv_d3"]
            comp = [kac_1, kac_2, kac_3, 1]
        if d_cm == "XYZ":
            kac_1 = color["xyz_d1"]
            kac_2 = color["xyz_d2"]
            kac_3 = color["xyz_d3"]
            comp = [kac_1, kac_2, kac_3, 1]
        if d_cm == "LAB":
            kac_1 = color["lab_d1"]
            kac_2 = color["lab_d2"]
            kac_3 = color["lab_d3"]
            comp = [kac_1, kac_2, kac_3, 1]
        managed_color.setComponents( comp )

        #endregion
        #region Color for Canvas

        if ( self.performance_inaccurate == False or side == "RETURN" ):
            display = managed_color.colorForCanvas( vc )
            r = display.redF()
            g = display.greenF()
            b = display.blueF()
        else:
            r = color["rgb_1"]
            g = color["rgb_2"]
            b = color["rgb_3"]
        color["hex6_d"] = self.convert.rgb_to_hex6( r, g, b )

        #endregion
        #region Operation

        if side == "FG":
            Krita.instance().activeWindow().activeView().setForeGroundColor( managed_color )
        if side == "BG":
            Krita.instance().activeWindow().activeView().setBackGroundColor( managed_color )

        #endregion
    def Color_Display( self, d_cm, d_cd, d_cp, vc, color ):
        if ( self.performance_inaccurate == False and ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            color_model = Krita.instance().activeDocument().colorModel()
            mc = ManagedColor( color_model, d_cd, d_cp )
            if d_cm == "A":
                mc.setComponents( [color[0], 1.0] )
            if ( d_cm == "RGB" or d_cm == None ):
                if ( d_cd == "U8" or d_cd == "U16" ):
                    mc.setComponents( [color[2], color[1], color[0], 1.0] )
                if ( d_cd == "F16" or d_cd == "F32" ):
                    mc.setComponents( [color[0], color[1], color[2], 1.0] )
            if d_cm == "CMYK":
                mc.setComponents( [color[0], color[1], color[2], color[3], 1.0] )
            if d_cm == "YUV":
                mc.setComponents( [color[0], color[1], color[2], 1.0] )
            if d_cm == "XYZ":
                mc.setComponents( [color[0], color[1], color[2], 1.0] )
            if d_cm == "LAB":
                mc.setComponents( [color[0], color[1], color[2], 1.0] )
            color_canvas = mc.colorForCanvas( vc )
            r = color_canvas.redF()
            g = color_canvas.greenF()
            b = color_canvas.blueF()
        else:
            r = color[0]
            g = color[1]
            b = color[2]
        # Return
        return [r, g, b]

    def Color_Interpolate( self, mode, color_a, color_b, factor ):
        # Parse
        color_a = self.convert.color_vector( mode, color_a )
        color_b = self.convert.color_vector( mode, color_b )
        # Interpolation
        channels = len( color_a )
        lerp = self.convert.color_lerp( mode, channels, color_a, color_b, factor )
        # Conversion
        color = color_true.copy()
        if mode == "A":
            color = self.Color_Convert( mode, lerp[0], 0, 0, 0, color )
        elif ( mode == "CMYK" or mode == "CMYK" ):
            color = self.Color_Convert( mode, lerp[0], lerp[1], lerp[2], lerp[3], color )
        else:
            color = self.Color_Convert( mode, lerp[0], lerp[1], lerp[2], 0, color )
        # Return
        return color

    def Color_Swap( self ):
        # Transfer Dict
        ab = color_true.copy()
        ba = color_true.copy()
        # Copy Swap
        self.Dict_Copy( ab, kac )
        self.Dict_Copy( ba, kbc )
        self.Dict_Copy( kac, ba )
        self.Dict_Copy( kbc, ab )
    def Color_Random( self ):
        r = random.randrange( 0,255,1 ) / 255
        g = random.randrange( 0,255,1 ) / 255
        b = random.randrange( 0,255,1 ) / 255
        self.Pigmento_APPLY( "RGB", r, g, b, 0, self.cor )
    def Color_Complementary( self ):
        # Wheel Influence
        if self.wheel_mode == "DIGITAL":
            hue = self.geometry.Limit_Looper( self.cor["hue_d"] + 0.5, 1 )
        if self.wheel_mode == "ANALOG":
            hue = self.convert.huea_to_hued( self.geometry.Limit_Looper( self.cor["hue_a"] + 0.5, 1 ) )

        # Color Space Influence
        if self.wheel_space == "HSV":
            self.Pigmento_APPLY( "HSV", hue, self.cor["hsv_2"], self.cor["hsv_3"], 0, self.cor )
        if self.wheel_space == "HSL":
            self.Pigmento_APPLY( "HSL", hue, self.cor["hsl_2"], self.cor["hsl_3"], 0, self.cor )
        if self.wheel_space == "HSY":
            self.Pigmento_APPLY( "HSY", hue, self.cor["hsy_2"], self.cor["hsy_3"], 0, self.cor )
        if self.wheel_space == "ARD":
            self.Pigmento_APPLY( "ARD", hue, self.cor["ard_2"], self.cor["ard_3"], 0, self.cor )

    def Color_AnalyseDocument( self ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            path = Krita.instance().activeDocument().fileName()
            self.Color_Analyse( path )
        else:
            self.analyse_collection = None
    def Color_Analyse( self, path ):
        # Variables
        size = 100

        # Construct
        qimage = QImage( path )
        width = qimage.width()
        height = qimage.height()
        if ( width >= size and height >= size ):
            qimage = qimage.scaled( size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation )
            width = qimage.width()
            height = qimage.height()

        # Pixel Check
        p = list()
        for h in range( 0, height ):
            # Progress bar
            percent = round( ( h + 1 ) / height, 4 )
            self.color_header.Set_Progress( percent )
            QApplication.processEvents()
            # Rox of Pixels
            for w in range( 0, width ):
                # RGB
                pixel = qimage.pixelColor( w,h )
                r = pixel.redF()
                g = pixel.greenF()
                b = pixel.blueF()
                rgb = [ r, g, b ]
                if rgb not in p:
                    p.append( rgb )
        # Color
        len_p = len( p )
        analyse_collection = list()
        for i in range( 0, len_p ):
            c = color_neutral.copy()
            color = self.Color_Convert( "RGB", p[i][0], p[i][1], p[i][2], 0, c )
            analyse_collection.append( color )
        self.analyse_collection = analyse_collection

        # UI
        self.color_header.Set_Progress( 1 )
        self.Pigmento_RELEASE()
        # System
        QtCore.qDebug( "Pigment.O | Analyse Complete" )

    #endregion
    #region Syncronization  ########################################################

    def Sync_Elements( self, p2k, color_active, color_previous ):
        # Signals
        self.Block_Channels( True )

        # Layout
        self.Pigmento_to_Krita( p2k )
        self.Harmony_Header( har_01, har_02, har_03, har_04, har_05 )
        self.Update_Header( color_active, color_previous )
        self.Panels_Set_Value()
        self.Update_Values()
        self.Channels_Set_Style()
        self.Mixers_Set_Style()
        self.Pin_Active()
        self.History_List( self.cor["rgb_d1"], self.cor["rgb_d2"], self.cor["rgb_d3"] )

        # Signals
        self.Block_Channels( False )

        # Dialog
        self.Reference_Name()

        # Save
        Krita.instance().writeSetting( "Pigment.O", "kac", str( kac ) )
        Krita.instance().writeSetting( "Pigment.O", "kbc", str( kbc ) )

    def Block_Channels( self, boolean ):
        # AAA
        self.layout.aaa_1_slider.blockSignals( boolean )
        self.layout.aaa_1_value.blockSignals( boolean )
        # RGB
        self.layout.rgb_1_slider.blockSignals( boolean )
        self.layout.rgb_2_slider.blockSignals( boolean )
        self.layout.rgb_3_slider.blockSignals( boolean )
        self.layout.rgb_1_value.blockSignals( boolean )
        self.layout.rgb_2_value.blockSignals( boolean )
        self.layout.rgb_3_value.blockSignals( boolean )
        # CMY
        self.layout.cmy_1_slider.blockSignals( boolean )
        self.layout.cmy_2_slider.blockSignals( boolean )
        self.layout.cmy_3_slider.blockSignals( boolean )
        self.layout.cmy_1_value.blockSignals( boolean )
        self.layout.cmy_2_value.blockSignals( boolean )
        self.layout.cmy_3_value.blockSignals( boolean )
        # CMYK
        self.layout.cmyk_1_slider.blockSignals( boolean )
        self.layout.cmyk_2_slider.blockSignals( boolean )
        self.layout.cmyk_3_slider.blockSignals( boolean )
        self.layout.cmyk_4_slider.blockSignals( boolean )
        self.layout.cmyk_1_value.blockSignals( boolean )
        self.layout.cmyk_2_value.blockSignals( boolean )
        self.layout.cmyk_3_value.blockSignals( boolean )
        self.layout.cmyk_4_value.blockSignals( boolean )
        # RYB
        self.layout.ryb_1_slider.blockSignals( boolean )
        self.layout.ryb_2_slider.blockSignals( boolean )
        self.layout.ryb_3_slider.blockSignals( boolean )
        self.layout.ryb_1_value.blockSignals( boolean )
        self.layout.ryb_2_value.blockSignals( boolean )
        self.layout.ryb_3_value.blockSignals( boolean )
        # YUV
        self.layout.yuv_1_slider.blockSignals( boolean )
        self.layout.yuv_2_slider.blockSignals( boolean )
        self.layout.yuv_3_slider.blockSignals( boolean )
        self.layout.yuv_1_value.blockSignals( boolean )
        self.layout.yuv_2_value.blockSignals( boolean )
        self.layout.yuv_3_value.blockSignals( boolean )

        # HSV
        self.layout.hsv_1_slider.blockSignals( boolean )
        self.layout.hsv_2_slider.blockSignals( boolean )
        self.layout.hsv_3_slider.blockSignals( boolean )
        self.layout.hsv_1_value.blockSignals( boolean )
        self.layout.hsv_2_value.blockSignals( boolean )
        self.layout.hsv_3_value.blockSignals( boolean )
        # HSL
        self.layout.hsl_1_slider.blockSignals( boolean )
        self.layout.hsl_2_slider.blockSignals( boolean )
        self.layout.hsl_3_slider.blockSignals( boolean )
        self.layout.hsl_1_value.blockSignals( boolean )
        self.layout.hsl_2_value.blockSignals( boolean )
        self.layout.hsl_3_value.blockSignals( boolean )
        # HSY
        self.layout.hsy_1_slider.blockSignals( boolean )
        self.layout.hsy_2_slider.blockSignals( boolean )
        self.layout.hsy_3_slider.blockSignals( boolean )
        self.layout.hsy_1_value.blockSignals( boolean )
        self.layout.hsy_2_value.blockSignals( boolean )
        self.layout.hsy_3_value.blockSignals( boolean )
        # ARD
        self.layout.ard_1_slider.blockSignals( boolean )
        self.layout.ard_2_slider.blockSignals( boolean )
        self.layout.ard_3_slider.blockSignals( boolean )
        self.layout.ard_1_value.blockSignals( boolean )
        self.layout.ard_2_value.blockSignals( boolean )
        self.layout.ard_3_value.blockSignals( boolean )

        # XYZ
        self.layout.xyz_1_slider.blockSignals( boolean )
        self.layout.xyz_2_slider.blockSignals( boolean )
        self.layout.xyz_3_slider.blockSignals( boolean )
        self.layout.xyz_1_value.blockSignals( boolean )
        self.layout.xyz_2_value.blockSignals( boolean )
        self.layout.xyz_3_value.blockSignals( boolean )
        # XYY
        self.layout.xyy_1_slider.blockSignals( boolean )
        self.layout.xyy_2_slider.blockSignals( boolean )
        self.layout.xyy_3_slider.blockSignals( boolean )
        self.layout.xyy_1_value.blockSignals( boolean )
        self.layout.xyy_2_value.blockSignals( boolean )
        self.layout.xyy_3_value.blockSignals( boolean )
        # LAB
        self.layout.lab_1_slider.blockSignals( boolean )
        self.layout.lab_2_slider.blockSignals( boolean )
        self.layout.lab_3_slider.blockSignals( boolean )
        self.layout.lab_1_value.blockSignals( boolean )
        self.layout.lab_2_value.blockSignals( boolean )
        self.layout.lab_3_value.blockSignals( boolean )

        # LCH
        self.layout.lch_1_slider.blockSignals( boolean )
        self.layout.lch_2_slider.blockSignals( boolean )
        self.layout.lch_3_slider.blockSignals( boolean )
        self.layout.lch_1_value.blockSignals( boolean )
        self.layout.lch_2_value.blockSignals( boolean )
        self.layout.lch_3_value.blockSignals( boolean )

        # KKK
        self.layout.kkk_1_slider.blockSignals( boolean )
        self.layout.kkk_1_value.blockSignals( boolean )
    def Harmony_Header( self, har_01, har_02, har_03, har_04, har_05 ):
        # Variables
        self.Color_Harmony( self.harmony_span, har_01, har_02, har_03, har_04, har_05 )
        # Update
        self.Harmony_Update()
        self.harmony_spread.Update_Span( self.harmony_span )
    def Update_Header( self, active, previous ):
        # Left
        if self.harmony_index == 0:
            if self.mode_ab == True:
                if active == True:
                    self.color_header.Set_Color_A1( kac["hex6_d"] )
                if previous == True:
                    self.color_header.Set_Color_B1( kbc["hex6_d"] )
            if self.mode_ab == False:
                if active == True:
                    self.color_header.Set_Color_B1( kbc["hex6_d"] )
                if previous == True:
                    self.color_header.Set_Color_A1( kac["hex6_d"] )
        if self.harmony_index == 1:
            self.color_header.Set_Color_A1( har_01["hex6_d"] )
        if self.harmony_index == 2:
            self.color_header.Set_Color_A1( har_02["hex6_d"] )
        if self.harmony_index == 3:
            self.color_header.Set_Color_A1( har_03["hex6_d"] )
        if self.harmony_index == 4:
            self.color_header.Set_Color_A1( har_04["hex6_d"] )
        if self.harmony_index == 5:
            self.color_header.Set_Color_A1( har_05["hex6_d"] )

        # Right
        if ( active == True and previous == True ):
            if self.harmony_index == 0:
                self.color_header.Set_Color_A2( kac["hex6_d"] )
                self.color_header.Set_Color_B2( kbc["hex6_d"] )
            if self.harmony_index == 1:
                self.color_header.Set_Color_A1( har_01["hex6_d"] )
                self.color_header.Set_Color_A2( har_01["hex6_d"] )
            if self.harmony_index == 2:
                self.color_header.Set_Color_A1( har_02["hex6_d"] )
                self.color_header.Set_Color_A2( har_02["hex6_d"] )
            if self.harmony_index == 3:
                self.color_header.Set_Color_A1( har_03["hex6_d"] )
                self.color_header.Set_Color_A2( har_03["hex6_d"] )
            if self.harmony_index == 4:
                self.color_header.Set_Color_A1( har_04["hex6_d"] )
                self.color_header.Set_Color_A2( har_04["hex6_d"] )
            if self.harmony_index == 5:
                self.color_header.Set_Color_A1( har_05["hex6_d"] )
                self.color_header.Set_Color_A2( har_05["hex6_d"] )
            self.zoom = False
            # Label
            self.Label_String( "" )
    def Panels_Set_Value( self ):
        # Place Cursor
        if self.panel_index == "Fill":
            self.Update_Panel_Fill()
        if self.panel_index == "Square":
            self.Update_Panel_Square()
        if self.panel_index == "Hue":
            self.Update_Panel_HueCircle()
        if self.panel_index == "Gamut":
            self.Update_Panel_Gamut()
        if self.panel_index == "Hexagon":
            self.Update_Panel_Hexagon()
        if self.panel_index == "Luma":
            self.Update_Panel_Luma()
        if self.panel_index == "Dot":
            pass # only changes when the dot color changes
        if self.panel_index == "Mask":
            self.Mask_Live_Update()
    def Update_Values( self ):
        # AAA
        if self.chan_aaa == True:
            self.aaa_1_slider.Set_Value( self.cor["aaa_1"] )
            self.layout.aaa_1_value.setValue( self.cor["aaa_1"] * krange["aaa_1"] )
        # RGB
        if self.chan_rgb == True:
            self.rgb_1_slider.Set_Value( self.cor["rgb_1"] )
            self.rgb_2_slider.Set_Value( self.cor["rgb_2"] )
            self.rgb_3_slider.Set_Value( self.cor["rgb_3"] )
            self.layout.rgb_1_value.setValue( self.cor["rgb_1"] * krange["rgb_1"] )
            self.layout.rgb_2_value.setValue( self.cor["rgb_2"] * krange["rgb_2"] )
            self.layout.rgb_3_value.setValue( self.cor["rgb_3"] * krange["rgb_3"] )
        # CMY
        if self.chan_cmy == True:
            self.cmy_1_slider.Set_Value( self.cor["cmy_1"] )
            self.cmy_2_slider.Set_Value( self.cor["cmy_2"] )
            self.cmy_3_slider.Set_Value( self.cor["cmy_3"] )
            self.layout.cmy_1_value.setValue( self.cor["cmy_1"] * krange["cmy_1"] )
            self.layout.cmy_2_value.setValue( self.cor["cmy_2"] * krange["cmy_2"] )
            self.layout.cmy_3_value.setValue( self.cor["cmy_3"] * krange["cmy_3"] )
        # CMYK
        if self.chan_cmyk == True:
            self.cmyk_1_slider.Set_Value( self.cor["cmyk_1"] )
            self.cmyk_2_slider.Set_Value( self.cor["cmyk_2"] )
            self.cmyk_3_slider.Set_Value( self.cor["cmyk_3"] )
            self.cmyk_4_slider.Set_Value( self.cor["cmyk_4"] )
            self.layout.cmyk_1_value.setValue( self.cor["cmyk_1"] * krange["cmyk_1"] )
            self.layout.cmyk_2_value.setValue( self.cor["cmyk_2"] * krange["cmyk_2"] )
            self.layout.cmyk_3_value.setValue( self.cor["cmyk_3"] * krange["cmyk_3"] )
            self.layout.cmyk_4_value.setValue( self.cor["cmyk_4"] * krange["cmyk_4"] )
        # RYB
        if self.chan_ryb == True:
            self.ryb_1_slider.Set_Value( self.cor["ryb_1"] )
            self.ryb_2_slider.Set_Value( self.cor["ryb_2"] )
            self.ryb_3_slider.Set_Value( self.cor["ryb_3"] )
            self.layout.ryb_1_value.setValue( self.cor["ryb_1"] * krange["ryb_1"] )
            self.layout.ryb_2_value.setValue( self.cor["ryb_2"] * krange["ryb_2"] )
            self.layout.ryb_3_value.setValue( self.cor["ryb_3"] * krange["ryb_3"] )
        # YUV
        if self.chan_yuv == True:
            self.yuv_1_slider.Set_Value( self.cor["yuv_1"] )
            self.yuv_2_slider.Set_Value( self.cor["yuv_2"] )
            self.yuv_3_slider.Set_Value( self.cor["yuv_3"] )
            self.layout.yuv_1_value.setValue( self.cor["yuv_1"] * krange["yuv_1"] )
            self.layout.yuv_2_value.setValue( self.cor["yuv_2"] * krange["yuv_2"] )
            self.layout.yuv_3_value.setValue( self.cor["yuv_3"] * krange["yuv_3"] )

        # HSV
        if self.chan_hsv == True:
            self.hsv_1_slider.Set_Value( self.cor["hsv_1"] )
            self.hsv_2_slider.Set_Value( self.cor["hsv_2"] )
            self.hsv_3_slider.Set_Value( self.cor["hsv_3"] )
            self.layout.hsv_1_value.setValue( self.cor["hsv_1"] * krange["hsv_1"] )
            self.layout.hsv_2_value.setValue( self.cor["hsv_2"] * krange["hsv_2"] )
            self.layout.hsv_3_value.setValue( self.cor["hsv_3"] * krange["hsv_3"] )
        # HSL
        if self.chan_hsl == True:
            self.hsl_1_slider.Set_Value( self.cor["hsl_1"] )
            self.hsl_2_slider.Set_Value( self.cor["hsl_2"] )
            self.hsl_3_slider.Set_Value( self.cor["hsl_3"] )
            self.layout.hsl_1_value.setValue( self.cor["hsl_1"] * krange["hsl_1"] )
            self.layout.hsl_2_value.setValue( self.cor["hsl_2"] * krange["hsl_2"] )
            self.layout.hsl_3_value.setValue( self.cor["hsl_3"] * krange["hsl_3"] )
        # HSY
        if self.chan_hsy == True:
            self.hsy_1_slider.Set_Value( self.cor["hsy_1"] )
            self.hsy_2_slider.Set_Value( self.cor["hsy_2"] )
            self.hsy_3_slider.Set_Value( self.cor["hsy_3"] )
            self.layout.hsy_1_value.setValue( self.cor["hsy_1"] * krange["hsy_1"] )
            self.layout.hsy_2_value.setValue( self.cor["hsy_2"] * krange["hsy_2"] )
            self.layout.hsy_3_value.setValue( self.cor["hsy_3"] * krange["hsy_3"] )
        # ARD
        if self.chan_ard == True:
            self.ard_1_slider.Set_Value( self.cor["ard_1"] )
            self.ard_2_slider.Set_Value( self.cor["ard_2"] )
            self.ard_3_slider.Set_Value( self.cor["ard_3"] )
            self.layout.ard_1_value.setValue( self.cor["ard_1"] * krange["ard_1"] )
            self.layout.ard_2_value.setValue( self.cor["ard_2"] * krange["ard_2"] )
            self.layout.ard_3_value.setValue( self.cor["ard_3"] * krange["ard_3"] )

        # XYZ
        if self.chan_xyz == True:
            self.xyz_1_slider.Set_Value( self.cor["xyz_1"] )
            self.xyz_2_slider.Set_Value( self.cor["xyz_2"] )
            self.xyz_3_slider.Set_Value( self.cor["xyz_3"] )
            self.layout.xyz_1_value.setValue( self.cor["xyz_1"] * krange["xyz_1"] )
            self.layout.xyz_2_value.setValue( self.cor["xyz_2"] * krange["xyz_2"] )
            self.layout.xyz_3_value.setValue( self.cor["xyz_3"] * krange["xyz_3"] )
        # XYY
        if self.chan_xyy == True:
            self.xyy_1_slider.Set_Value( self.cor["xyy_1"] )
            self.xyy_2_slider.Set_Value( self.cor["xyy_2"] )
            self.xyy_3_slider.Set_Value( self.cor["xyy_3"] )
            self.layout.xyy_1_value.setValue( self.cor["xyy_1"] * krange["xyy_1"] )
            self.layout.xyy_2_value.setValue( self.cor["xyy_2"] * krange["xyy_2"] )
            self.layout.xyy_3_value.setValue( self.cor["xyy_3"] * krange["xyy_3"] )
        # LAB
        if self.chan_lab == True:
            self.lab_1_slider.Set_Value( self.cor["lab_1"] )
            self.lab_2_slider.Set_Value( self.cor["lab_2"] )
            self.lab_3_slider.Set_Value( self.cor["lab_3"] )
            self.layout.lab_1_value.setValue( self.cor["lab_1"] * krange["lab_1"] )
            self.layout.lab_2_value.setValue( self.cor["lab_2"] * krange["lab_2"] )
            self.layout.lab_3_value.setValue( self.cor["lab_3"] * krange["lab_3"] )

        # LCH
        if self.chan_lch == True:
            self.lch_1_slider.Set_Value( self.cor["lch_1"] )
            self.lch_2_slider.Set_Value( self.cor["lch_2"] )
            self.lch_3_slider.Set_Value( self.cor["lch_3"] )
            self.layout.lch_1_value.setValue( self.cor["lch_1"] * krange["lch_1"] )
            self.layout.lch_2_value.setValue( self.cor["lch_2"] * krange["lch_2"] )
            self.layout.lch_3_value.setValue( self.cor["lch_3"] * krange["lch_3"] )

        # KKK
        if self.chan_kkk == True:
            self.kkk_1_slider.Set_Value( self.cor["kkk_percent"] )
            self.layout.kkk_1_value.setValue( self.cor["kkk_scale"] )

        # SELE
        if self.chan_sele == True:
            # Sliders
            if self.sele_mode == "A":
                self.sele_1_slider.Update_Value( self.cor["aaa_1"] )
                self.sele_2_slider.Update_Value( None )
                self.sele_3_slider.Update_Value( None )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "RGB":
                self.sele_1_slider.Update_Value( self.cor["rgb_1"] )
                self.sele_2_slider.Update_Value( self.cor["rgb_2"] )
                self.sele_3_slider.Update_Value( self.cor["rgb_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "CMY":
                self.sele_1_slider.Update_Value( self.cor["cmy_1"] )
                self.sele_2_slider.Update_Value( self.cor["cmy_2"] )
                self.sele_3_slider.Update_Value( self.cor["cmy_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "CMYK":
                self.sele_1_slider.Update_Value( self.cor["cmyk_1"] )
                self.sele_2_slider.Update_Value( self.cor["cmyk_2"] )
                self.sele_3_slider.Update_Value( self.cor["cmyk_3"] )
                self.sele_4_slider.Update_Value( self.cor["cmyk_4"] )
            if self.sele_mode == "RYB":
                self.sele_1_slider.Update_Value( self.cor["ryb_1"] )
                self.sele_2_slider.Update_Value( self.cor["ryb_2"] )
                self.sele_3_slider.Update_Value( self.cor["ryb_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "YUV":
                self.sele_1_slider.Update_Value( self.cor["yuv_1"] )
                self.sele_2_slider.Update_Value( self.cor["yuv_2"] )
                self.sele_3_slider.Update_Value( self.cor["yuv_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "HSV":
                self.sele_1_slider.Update_Value( self.cor["hsv_1"] )
                self.sele_2_slider.Update_Value( self.cor["hsv_2"] )
                self.sele_3_slider.Update_Value( self.cor["hsv_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "HSL":
                self.sele_1_slider.Update_Value( self.cor["hsl_1"] )
                self.sele_2_slider.Update_Value( self.cor["hsl_2"] )
                self.sele_3_slider.Update_Value( self.cor["hsl_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "HSY":
                self.sele_1_slider.Update_Value( self.cor["hsy_1"] )
                self.sele_2_slider.Update_Value( self.cor["hsy_2"] )
                self.sele_3_slider.Update_Value( self.cor["hsy_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "ARD":
                self.sele_1_slider.Update_Value( self.cor["ard_1"] )
                self.sele_2_slider.Update_Value( self.cor["ard_2"] )
                self.sele_3_slider.Update_Value( self.cor["ard_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "XYZ":
                self.sele_1_slider.Update_Value( self.cor["xyz_1"] )
                self.sele_2_slider.Update_Value( self.cor["xyz_2"] )
                self.sele_3_slider.Update_Value( self.cor["xyz_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "XYY":
                self.sele_1_slider.Update_Value( self.cor["xyy_1"] )
                self.sele_2_slider.Update_Value( self.cor["xyy_2"] )
                self.sele_3_slider.Update_Value( self.cor["xyy_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "LAB":
                self.sele_1_slider.Update_Value( self.cor["lab_1"] )
                self.sele_2_slider.Update_Value( self.cor["lab_2"] )
                self.sele_3_slider.Update_Value( self.cor["lab_3"] )
                self.sele_4_slider.Update_Value( None )
            if self.sele_mode == "LCH":
                self.sele_1_slider.Update_Value( self.cor["lch_1"] )
                self.sele_2_slider.Update_Value( self.cor["lch_2"] )
                self.sele_3_slider.Update_Value( self.cor["lch_3"] )
                self.sele_4_slider.Update_Value( None )
            # Values 1
            self.layout.sele_1_l0.setValue( sele_1_var["l0"] * 100 )
            self.layout.sele_1_l1.setValue( sele_1_var["l1"] * 100 )
            self.layout.sele_1_r1.setValue( sele_1_var["r1"] * 100 )
            self.layout.sele_1_r0.setValue( sele_1_var["r0"] * 100 )
            # Values 2
            self.layout.sele_2_l0.setValue( sele_2_var["l0"] * 100 )
            self.layout.sele_2_l1.setValue( sele_2_var["l1"] * 100 )
            self.layout.sele_2_r1.setValue( sele_2_var["r1"] * 100 )
            self.layout.sele_2_r0.setValue( sele_2_var["r0"] * 100 )
            # Values 3
            self.layout.sele_3_l0.setValue( sele_3_var["l0"] * 100 )
            self.layout.sele_3_l1.setValue( sele_3_var["l1"] * 100 )
            self.layout.sele_3_r1.setValue( sele_3_var["r1"] * 100 )
            self.layout.sele_3_r0.setValue( sele_3_var["r0"] * 100 )
            # Values 4
            self.layout.sele_4_l0.setValue( sele_4_var["l0"] * 100 )
            self.layout.sele_4_l1.setValue( sele_4_var["l1"] * 100 )
            self.layout.sele_4_r1.setValue( sele_4_var["r1"] * 100 )
            self.layout.sele_4_r0.setValue( sele_4_var["r0"] * 100 )
            # Selection
            self.sele_1_slider.Update_Selection( sele_1_var )
            self.sele_2_slider.Update_Selection( sele_2_var )
            self.sele_3_slider.Update_Selection( sele_3_var )
            self.sele_4_slider.Update_Selection( sele_4_var )

        # Mixers
        if self.ui_mixer == True:
            for i in range( 0, len( self.mixer_colors ) ):
                try:self.mixer_module[i]["m"].Set_Value( self.mixer_colors[i]["m"] )
                except:pass

        # HEX
        if self.chan_hex == True:
            hex_text = self.cor["hex6_d"]
            if self.hex_sum == True:
                percentage = self.convert.cmyk_to_tic( self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"] )
                hex_text += " Σ" + str( percentage ).zfill(3)
            self.layout.hex_string.setText( hex_text )
    def Channels_Set_Style( self ):
        # Variables
        linear = 20 # 4 stops
        circular = 18 # 6 stops
        # Channels Update
        if self.chan_aaa == True:
            aaa_1 = self.Gradient_Style( "A", False, linear, [0], [1] )
            self.aaa_1_slider.Set_Colors( aaa_1, 1 )
        if self.chan_rgb == True:
            rgb_1 = self.Gradient_Style( "RGB", False, linear, [0, self.cor["rgb_2"], self.cor["rgb_3"]], [1, self.cor["rgb_2"], self.cor["rgb_3"]] )
            rgb_2 = self.Gradient_Style( "RGB", False, linear, [self.cor["rgb_1"], 0, self.cor["rgb_3"]], [self.cor["rgb_1"], 1, self.cor["rgb_3"]] )
            rgb_3 = self.Gradient_Style( "RGB", False, linear, [self.cor["rgb_1"], self.cor["rgb_2"], 0], [self.cor["rgb_1"], self.cor["rgb_2"], 1] )
            self.rgb_1_slider.Set_Colors( rgb_1, 1 )
            self.rgb_2_slider.Set_Colors( rgb_2, 1 )
            self.rgb_3_slider.Set_Colors( rgb_3, 1 )
        if self.chan_cmy == True:
            cmy_1 = self.Gradient_Style( "CMY", False, linear, [0, self.cor["cmy_2"], self.cor["cmy_3"]], [1, self.cor["cmy_2"], self.cor["cmy_3"]] )
            cmy_2 = self.Gradient_Style( "CMY", False, linear, [self.cor["cmy_1"], 0, self.cor["cmy_3"]], [self.cor["cmy_1"], 1, self.cor["cmy_3"]] )
            cmy_3 = self.Gradient_Style( "CMY", False, linear, [self.cor["cmy_1"], self.cor["cmy_2"], 0], [self.cor["cmy_1"], self.cor["cmy_2"], 1] )
            self.cmy_1_slider.Set_Colors( cmy_1, 1 )
            self.cmy_2_slider.Set_Colors( cmy_2, 1 )
            self.cmy_3_slider.Set_Colors( cmy_3, 1 )
        if self.chan_cmyk == True:
            cmyk_1 = self.Gradient_Style( "CMYK", False, linear, [0, self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"]], [1, self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"]] )
            cmyk_2 = self.Gradient_Style( "CMYK", False, linear, [self.cor["cmyk_1"], 0, self.cor["cmyk_3"], self.cor["cmyk_4"]], [self.cor["cmyk_1"], 1, self.cor["cmyk_3"], self.cor["cmyk_4"]] )
            cmyk_3 = self.Gradient_Style( "CMYK", False, linear, [self.cor["cmyk_1"], self.cor["cmyk_2"], 0, self.cor["cmyk_4"]], [self.cor["cmyk_1"], self.cor["cmyk_2"], 1, self.cor["cmyk_4"]] )
            cmyk_4 = self.Gradient_Style( "CMYK", False, linear, [self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], 0], [self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], 1] )
            self.cmyk_1_slider.Set_Colors( cmyk_1, 1 )
            self.cmyk_2_slider.Set_Colors( cmyk_2, 1 )
            self.cmyk_3_slider.Set_Colors( cmyk_3, 1 )
            self.cmyk_4_slider.Set_Colors( cmyk_4, 1 )
        if self.chan_ryb == True:
            ryb_1 = self.Gradient_Style( "RYB", False, linear, [0, self.cor["ryb_2"], self.cor["ryb_3"]], [1, self.cor["ryb_2"], self.cor["ryb_3"]] )
            ryb_2 = self.Gradient_Style( "RYB", False, linear, [self.cor["ryb_1"], 0, self.cor["ryb_3"]], [self.cor["ryb_1"], 1, self.cor["ryb_3"]] )
            ryb_3 = self.Gradient_Style( "RYB", False, linear, [self.cor["ryb_1"], self.cor["ryb_2"], 0], [self.cor["ryb_1"], self.cor["ryb_2"], 1] )
            self.ryb_1_slider.Set_Colors( ryb_1, 1 )
            self.ryb_2_slider.Set_Colors( ryb_2, 1 )
            self.ryb_3_slider.Set_Colors( ryb_3, 1 )
        if self.chan_yuv == True:
            yuv_1 = self.Gradient_Style( "YUV", False, linear, [0, self.cor["yuv_2"], self.cor["yuv_3"]], [1, self.cor["yuv_2"], self.cor["yuv_3"]] )
            yuv_2 = self.Gradient_Style( "YUV", False, linear, [self.cor["yuv_1"], 0, self.cor["yuv_3"]], [self.cor["yuv_1"], 1, self.cor["yuv_3"]] )
            yuv_3 = self.Gradient_Style( "YUV", False, linear, [self.cor["yuv_1"], self.cor["yuv_2"], 0], [self.cor["yuv_1"], self.cor["yuv_2"], 1] )
            self.yuv_1_slider.Set_Colors( yuv_1, 1 )
            self.yuv_2_slider.Set_Colors( yuv_2, 1 )
            self.yuv_3_slider.Set_Colors( yuv_3, 1 )

        if self.chan_hsv == True:
            if self.hue_shine == True:
                hsv_1 = self.Gradient_Style( "HSV", False, circular, [0, 1, 1], [1, 1, 1] )
            else:
                hsv_1 = self.Gradient_Style( "HSV", False, circular, [0, self.cor["hsv_2"], self.cor["hsv_3"]], [1, self.cor["hsv_2"], self.cor["hsv_3"]] )
            hsv_2 = self.Gradient_Style( "HSV", False, linear, [self.cor["hsv_1"], 0, self.cor["hsv_3"]], [self.cor["hsv_1"], 1, self.cor["hsv_3"]] )
            hsv_3 = self.Gradient_Style( "HSV", False, linear, [self.cor["hsv_1"], self.cor["hsv_2"], 0], [self.cor["hsv_1"], self.cor["hsv_2"], 1] )
            self.hsv_1_slider.Set_Colors( hsv_1, 1 )
            self.hsv_2_slider.Set_Colors( hsv_2, 1 )
            self.hsv_3_slider.Set_Colors( hsv_3, 1 )
        if self.chan_hsl == True:
            if self.hue_shine == True:
                hsl_1 = self.Gradient_Style( "HSV", False, circular, [0, 1, 1], [1, 1, 1] )
            else:
                hsl_1 = self.Gradient_Style( "HSL", False, circular, [0, self.cor["hsl_2"], self.cor["hsl_3"]], [1, self.cor["hsl_2"], self.cor["hsl_3"]] )
            hsl_2 = self.Gradient_Style( "HSL", False, linear, [self.cor["hsl_1"], 0, self.cor["hsl_3"]], [self.cor["hsl_1"], 1, self.cor["hsl_3"]] )
            hsl_3 = self.Gradient_Style( "HSL", False, linear, [self.cor["hsl_1"], self.cor["hsl_2"], 0], [self.cor["hsl_1"], self.cor["hsl_2"], 1] )
            self.hsl_1_slider.Set_Colors( hsl_1, 1 )
            self.hsl_2_slider.Set_Colors( hsl_2, 1 )
            self.hsl_3_slider.Set_Colors( hsl_3, 1 )
        if self.chan_hsy == True:
            if self.hue_shine == True:
                hsy_1 = self.Gradient_Style( "HSV", False, circular, [0, 1, 1], [1, 1, 1] )
            else:
                hsy_1 = self.Gradient_Style( "HSY", False, circular, [0, self.cor["hsy_2"], self.cor["hsy_3"]], [1, self.cor["hsy_2"], self.cor["hsy_3"]] )
            hsy_2 = self.Gradient_Style( "HSY", False, linear, [self.cor["hsy_1"], 0, self.cor["hsy_3"]], [self.cor["hsy_1"], 1, self.cor["hsy_3"]] )
            hsy_3 = self.Gradient_Style( "HSY", False, linear, [self.cor["hsy_1"], self.cor["hsy_2"], 0], [self.cor["hsy_1"], self.cor["hsy_2"], 1] )
            self.hsy_1_slider.Set_Colors( hsy_1, 1 )
            self.hsy_2_slider.Set_Colors( hsy_2, 1 )
            self.hsy_3_slider.Set_Colors( hsy_3, 1 )
        if self.chan_ard == True:
            if self.hue_shine == True:
                ard_1 = self.Gradient_Style( "HSV", False, circular, [0, 1, 1], [1, 1, 1] )
            else:
                ard_1 = self.Gradient_Style( "ARD", False, circular, [0, self.cor["ard_2"], self.cor["ard_3"]], [1, self.cor["ard_2"], self.cor["ard_3"]] )
            ard_2 = self.Gradient_Style( "ARD", False, linear, [self.cor["ard_1"], 0, self.cor["ard_3"]], [self.cor["ard_1"], 1, self.cor["ard_3"]] )
            ard_3 = self.Gradient_Style( "ARD", False, linear, [self.cor["ard_1"], self.cor["ard_2"], 0], [self.cor["ard_1"], self.cor["ard_2"], 1] )
            self.ard_1_slider.Set_Colors( ard_1, 1 )
            self.ard_2_slider.Set_Colors( ard_2, 1 )
            self.ard_3_slider.Set_Colors( ard_3, 1 )

        if self.chan_xyz == True:
            xyz_1 = self.Gradient_Style( "XYZ", False, linear, [0, self.cor["xyz_2"], self.cor["xyz_3"]], [1, self.cor["xyz_2"], self.cor["xyz_3"]] )
            xyz_2 = self.Gradient_Style( "XYZ", False, linear, [self.cor["xyz_1"], 0, self.cor["xyz_3"]], [self.cor["xyz_1"], 1, self.cor["xyz_3"]] )
            xyz_3 = self.Gradient_Style( "XYZ", False, linear, [self.cor["xyz_1"], self.cor["xyz_2"], 0], [self.cor["xyz_1"], self.cor["xyz_2"], 1] )
            self.xyz_1_slider.Set_Colors( xyz_1, 1 )
            self.xyz_2_slider.Set_Colors( xyz_2, 1 )
            self.xyz_3_slider.Set_Colors( xyz_3, 1 )
        if self.chan_xyy == True:
            xyy_1 = self.Gradient_Style( "XYY", False, linear, [0, self.cor["xyy_2"], self.cor["xyy_3"]], [1, self.cor["xyy_2"], self.cor["xyy_3"]] )
            xyy_2 = self.Gradient_Style( "XYY", False, linear, [self.cor["xyy_1"], 0, self.cor["xyy_3"]], [self.cor["xyy_1"], 1, self.cor["xyy_3"]] )
            xyy_3 = self.Gradient_Style( "XYY", False, linear, [self.cor["xyy_1"], self.cor["xyy_2"], 0], [self.cor["xyy_1"], self.cor["xyy_2"], 1] )
            self.xyy_1_slider.Set_Colors( xyy_1, 1 )
            self.xyy_2_slider.Set_Colors( xyy_2, 1 )
            self.xyy_3_slider.Set_Colors( xyy_3, 1 )
        if self.chan_lab == True:
            lab_1 = self.Gradient_Style( "LAB", False, linear, [0, self.cor["lab_2"], self.cor["lab_3"]], [1, self.cor["lab_2"], self.cor["lab_3"]] )
            lab_2 = self.Gradient_Style( "LAB", False, linear, [self.cor["lab_1"], 0, self.cor["lab_3"]], [self.cor["lab_1"], 1, self.cor["lab_3"]] )
            lab_3 = self.Gradient_Style( "LAB", False, linear, [self.cor["lab_1"], self.cor["lab_2"], 0], [self.cor["lab_1"], self.cor["lab_2"], 1] )
            self.lab_1_slider.Set_Colors( lab_1, 1 )
            self.lab_2_slider.Set_Colors( lab_2, 1 )
            self.lab_3_slider.Set_Colors( lab_3, 1 )

        if self.chan_lch == True:
            lch_1 = self.Gradient_Style( "LCH", False, linear, [0, self.cor["lch_2"], self.cor["lch_3"]], [1, self.cor["lch_2"], self.cor["lch_3"]] )
            lch_2 = self.Gradient_Style( "LCH", False, linear, [self.cor["lch_1"], 0, self.cor["lch_3"]], [self.cor["lch_1"], 1, self.cor["lch_3"]] )
            lch_3 = self.Gradient_Style( "LCH", False, linear, [self.cor["lch_1"], self.cor["lch_2"], 0], [self.cor["lch_1"], self.cor["lch_2"], 1] )
            self.lch_1_slider.Set_Colors( lch_1, 1 )
            self.lch_2_slider.Set_Colors( lch_2, 1 )
            self.lch_3_slider.Set_Colors( lch_3, 1 )

        if self.chan_kkk == True:
            kkk_1 = self.Gradient_Kelvin( self.lock_kkk_1, linear, self.cor["rgb_1"], self.cor["rgb_2"], self.cor["rgb_3"] )
            self.kkk_1_slider.Set_Colors( kkk_1, 1 )

        if self.chan_sele == True:
            if self.sele_mode == "A":
                sele_1 = self.Gradient_Style( "A", False, linear, [0], [1] )
                sele_2 = None
                sele_3 = None
                sele_4 = None
            if self.sele_mode == "RGB":
                sele_1 = self.Gradient_Style( "RGB", False, linear, [0, self.cor["rgb_2"], self.cor["rgb_3"]], [1, self.cor["rgb_2"], self.cor["rgb_3"]] )
                sele_2 = self.Gradient_Style( "RGB", False, linear, [self.cor["rgb_1"], 0, self.cor["rgb_3"]], [self.cor["rgb_1"], 1, self.cor["rgb_3"]] )
                sele_3 = self.Gradient_Style( "RGB", False, linear, [self.cor["rgb_1"], self.cor["rgb_2"], 0], [self.cor["rgb_1"], self.cor["rgb_2"], 1] )
                sele_4 = None
            if self.sele_mode == "CMY":
                sele_1 = self.Gradient_Style( "CMY", False, linear, [0, self.cor["cmy_2"], self.cor["cmy_3"]], [1, self.cor["cmy_2"], self.cor["cmy_3"]] )
                sele_2 = self.Gradient_Style( "CMY", False, linear, [self.cor["cmy_1"], 0, self.cor["cmy_3"]], [self.cor["cmy_1"], 1, self.cor["cmy_3"]] )
                sele_3 = self.Gradient_Style( "CMY", False, linear, [self.cor["cmy_1"], self.cor["cmy_2"], 0], [self.cor["cmy_1"], self.cor["cmy_2"], 1] )
                sele_4 = None
            if self.sele_mode == "CMYK":
                sele_1 = self.Gradient_Style( "CMYK", False, linear, [0, self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"]], [1, self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"]] )
                sele_2 = self.Gradient_Style( "CMYK", False, linear, [self.cor["cmyk_1"], 0, self.cor["cmyk_3"], self.cor["cmyk_4"]], [self.cor["cmyk_1"], 1, self.cor["cmyk_3"], self.cor["cmyk_4"]] )
                sele_3 = self.Gradient_Style( "CMYK", False, linear, [self.cor["cmyk_1"], self.cor["cmyk_2"], 0, self.cor["cmyk_4"]], [self.cor["cmyk_1"], self.cor["cmyk_2"], 1, self.cor["cmyk_4"]] )
                sele_4 = self.Gradient_Style( "CMYK", False, linear, [self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], 0], [self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], 1] )
            if self.sele_mode == "RYB":
                sele_1 = self.Gradient_Style( "RYB", False, linear, [0, self.cor["ryb_2"], self.cor["ryb_3"]], [1, self.cor["ryb_2"], self.cor["ryb_3"]] )
                sele_2 = self.Gradient_Style( "RYB", False, linear, [self.cor["ryb_1"], 0, self.cor["ryb_3"]], [self.cor["ryb_1"], 1, self.cor["ryb_3"]] )
                sele_3 = self.Gradient_Style( "RYB", False, linear, [self.cor["ryb_1"], self.cor["ryb_2"], 0], [self.cor["ryb_1"], self.cor["ryb_2"], 1] )
                sele_4 = None
            if self.sele_mode == "YUV":
                sele_1 = self.Gradient_Style( "YUV", False, linear, [0, self.cor["yuv_2"], self.cor["yuv_3"]], [1, self.cor["yuv_2"], self.cor["yuv_3"]] )
                sele_2 = self.Gradient_Style( "YUV", False, linear, [self.cor["yuv_1"], 0, self.cor["yuv_3"]], [self.cor["yuv_1"], 1, self.cor["yuv_3"]] )
                sele_3 = self.Gradient_Style( "YUV", False, linear, [self.cor["yuv_1"], self.cor["yuv_2"], 0], [self.cor["yuv_1"], self.cor["yuv_2"], 1] )
                sele_4 = None
            if self.sele_mode == "HSV":
                if self.hue_shine == True:
                    sele_1 = self.Gradient_Style( "HSV", False, circular, [0, 1, 1], [1, 1, 1] )
                else:
                    sele_1 = self.Gradient_Style( "HSV", False, circular, [0, self.cor["hsv_2"], self.cor["hsv_3"]], [1, self.cor["hsv_2"], self.cor["hsv_3"]] )
                sele_2 = self.Gradient_Style( "HSV", False, linear, [self.cor["hsv_1"], 0, self.cor["hsv_3"]], [self.cor["hsv_1"], 1, self.cor["hsv_3"]] )
                sele_3 = self.Gradient_Style( "HSV", False, linear, [self.cor["hsv_1"], self.cor["hsv_2"], 0], [self.cor["hsv_1"], self.cor["hsv_2"], 1] )
                sele_4 = None
            if self.sele_mode == "HSL":
                if self.hue_shine == True:
                    sele_1 = self.Gradient_Style( "HSL", False, circular, [0, 1, 0.5], [1, 1, 0.5] )
                else:
                    sele_1 = self.Gradient_Style( "HSL", False, circular, [0, self.cor["hsl_2"], self.cor["hsl_3"]], [1, self.cor["hsl_2"], self.cor["hsl_3"]] )
                sele_2 = self.Gradient_Style( "HSL", False, linear, [self.cor["hsl_1"], 0, self.cor["hsl_3"]], [self.cor["hsl_1"], 1, self.cor["hsl_3"]] )
                sele_3 = self.Gradient_Style( "HSL", False, linear, [self.cor["hsl_1"], self.cor["hsl_2"], 0], [self.cor["hsl_1"], self.cor["hsl_2"], 1] )
                sele_4 = None
            if self.sele_mode == "HSY":
                if self.hue_shine == True:
                    sele_1 = self.Gradient_Style( "HSV", False, circular, [0, 1, 1], [1, 1, 1] )
                else:
                    sele_1 = self.Gradient_Style( "HSY", False, circular, [0, self.cor["hsy_2"], self.cor["hsy_3"]], [1, self.cor["hsy_2"], self.cor["hsy_3"]] )
                sele_2 = self.Gradient_Style( "HSY", False, linear, [self.cor["hsy_1"], 0, self.cor["hsy_3"]], [self.cor["hsy_1"], 1, self.cor["hsy_3"]] )
                sele_3 = self.Gradient_Style( "HSY", False, linear, [self.cor["hsy_1"], self.cor["hsy_2"], 0], [self.cor["hsy_1"], self.cor["hsy_2"], 1] )
                sele_4 = None
            if self.sele_mode == "ARD":
                if self.hue_shine == True:
                    sele_1 = self.Gradient_Style( "ARD", False, circular, [0, 1, 1], [1, 1, 1] )
                else:
                    sele_1 = self.Gradient_Style( "ARD", False, circular, [0, self.cor["ard_2"], self.cor["ard_3"]], [1, self.cor["ard_2"], self.cor["ard_3"]] )
                sele_2 = self.Gradient_Style( "ARD", False, linear, [self.cor["ard_1"], 0, self.cor["ard_3"]], [self.cor["ard_1"], 1, self.cor["ard_3"]] )
                sele_3 = self.Gradient_Style( "ARD", False, linear, [self.cor["ard_1"], self.cor["ard_2"], 0], [self.cor["ard_1"], self.cor["ard_2"], 1] )
                sele_4 = None
            if self.sele_mode == "XYZ":
                sele_1 = self.Gradient_Style( "XYZ", False, linear, [0, self.cor["xyz_2"], self.cor["xyz_3"]], [1, self.cor["xyz_2"], self.cor["xyz_3"]] )
                sele_2 = self.Gradient_Style( "XYZ", False, linear, [self.cor["xyz_1"], 0, self.cor["xyz_3"]], [self.cor["xyz_1"], 1, self.cor["xyz_3"]] )
                sele_3 = self.Gradient_Style( "XYZ", False, linear, [self.cor["xyz_1"], self.cor["xyz_2"], 0], [self.cor["xyz_1"], self.cor["xyz_2"], 1] )
                sele_4 = None
            if self.sele_mode == "XYY":
                sele_1 = self.Gradient_Style( "XYY", False, linear, [0, self.cor["xyy_2"], self.cor["xyy_3"]], [1, self.cor["xyy_2"], self.cor["xyy_3"]] )
                sele_2 = self.Gradient_Style( "XYY", False, linear, [self.cor["xyy_1"], 0, self.cor["xyy_3"]], [self.cor["xyy_1"], 1, self.cor["xyy_3"]] )
                sele_3 = self.Gradient_Style( "XYY", False, linear, [self.cor["xyy_1"], self.cor["xyy_2"], 0], [self.cor["xyy_1"], self.cor["xyy_2"], 1] )
                sele_4 = None
            if self.sele_mode == "LAB":
                sele_1 = self.Gradient_Style( "LAB", False, linear, [0, self.cor["lab_2"], self.cor["lab_3"]], [1, self.cor["lab_2"], self.cor["lab_3"]] )
                sele_2 = self.Gradient_Style( "LAB", False, linear, [self.cor["lab_1"], 0, self.cor["lab_3"]], [self.cor["lab_1"], 1, self.cor["lab_3"]] )
                sele_3 = self.Gradient_Style( "LAB", False, linear, [self.cor["lab_1"], self.cor["lab_2"], 0], [self.cor["lab_1"], self.cor["lab_2"], 1] )
                sele_4 = None
            if self.sele_mode == "LCH":
                sele_1 = self.Gradient_Style( "LCH", False, linear, [0, self.cor["lch_2"], self.cor["lch_3"]], [1, self.cor["lch_2"], self.cor["lch_3"]] )
                sele_2 = self.Gradient_Style( "LCH", False, linear, [self.cor["lch_1"], 0, self.cor["lch_3"]], [self.cor["lch_1"], 1, self.cor["lch_3"]] )
                sele_3 = self.Gradient_Style( "LCH", False, linear, [self.cor["lch_1"], self.cor["lch_2"], 0], [self.cor["lch_1"], self.cor["lch_2"], 1] )
                sele_4 = None
            self.sele_1_slider.Update_Colors( sele_1, 1 )
            self.sele_2_slider.Update_Colors( sele_2, 1 )
            self.sele_3_slider.Update_Colors( sele_3, 1 )
            self.sele_4_slider.Update_Colors( sele_4, 1 )
    def Mixers_Set_Style( self ):
        for i in range( 0, len( self.mixer_colors ) ):
            try:
                # Variables
                mode = self.mixer_space
                short = True
                stops = 20
                ll = self.mixer_colors[i]["l"]
                rr = self.mixer_colors[i]["r"]

                # Active
                al = ll["active"]
                ar = rr["active"]
                # Render Colors
                if ( al == True and ar == True ):
                    # Variables
                    if mode == "A":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["aaa_1"] ], [ rr["aaa_1"] ] )
                    elif ( mode == "RGB" or mode == None ):
                        mixed = self.Gradient_Style( "RGB", short, stops, [ ll["rgb_1"], ll["rgb_2"], ll["rgb_3"] ], [ rr["rgb_1"], rr["rgb_2"], rr["rgb_3"] ] )
                    elif mode == "CMY":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["cmy_1"], ll["cmy_2"], ll["cmy_3"] ], [ rr["cmy_1"], rr["cmy_2"], rr["cmy_3"] ] )
                    elif mode == "CMYK":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["cmyk_1"], ll["cmyk_2"], ll["cmyk_3"], ll["cmyk_4"] ], [ rr["cmyk_1"], rr["cmyk_2"], rr["cmyk_3"], rr["cmyk_4"] ] )
                    elif mode == "RYB":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["ryb_1"], ll["ryb_2"], ll["ryb_3"] ], [ rr["ryb_1"], rr["ryb_2"], rr["ryb_3"] ] )
                    elif mode == "YUV":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["yuv_1"], ll["yuv_2"], ll["yuv_3"] ], [ rr["yuv_1"], rr["yuv_2"], rr["yuv_3"] ] )
                    elif mode == "HSV":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["hsv_1"], ll["hsv_2"], ll["hsv_3"] ], [ rr["hsv_1"], rr["hsv_2"], rr["hsv_3"] ] )
                    elif mode == "HSL":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["hsl_1"], ll["hsl_2"], ll["hsl_3"] ], [ rr["hsl_1"], rr["hsl_2"], rr["hsl_3"] ] )
                    elif mode == "HSY":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["hsy_1"], ll["hsy_2"], ll["hsy_3"] ], [ rr["hsy_1"], rr["hsy_2"], rr["hsy_3"] ] )
                    elif mode == "ARD":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["ard_1"], ll["ard_2"], ll["ard_3"] ], [ rr["ard_1"], rr["ard_2"], rr["ard_3"] ] )
                    elif mode == "XYZ":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["xyz_1"], ll["xyz_2"], ll["xyz_3"] ], [ rr["xyz_1"], rr["xyz_2"], rr["xyz_3"] ] )
                    elif mode == "XYY":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["xyy_1"], ll["xyy_2"], ll["xyy_3"] ], [ rr["xyy_1"], rr["xyy_2"], rr["xyy_3"] ] )
                    elif mode == "LAB":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["lab_1"], ll["lab_2"], ll["lab_3"] ], [ rr["lab_1"], rr["lab_2"], rr["lab_3"] ] )
                    elif mode == "LCH":
                        mixed = self.Gradient_Style( mode, short, stops, [ ll["lch_1"], ll["lch_2"], ll["lch_3"] ], [ rr["lch_1"], rr["lch_2"], rr["lch_3"] ] )
                    # Render
                    self.mixer_module[i]["m"].Set_Colors( mixed, 1 )
                else:
                    self.mixer_module[i]["m"].Set_Colors( None, 1 )
            except:
                pass
    def Pin_Active( self ):
        # Variables
        rgb_cor = self.cor["hex6"]

        # Activate Pin
        for i in range( 0, len( self.pin_module ) ):
            if ( self.pin_cor[i]["active"] == True and self.pin_cor[i]["hex6"] == rgb_cor ):
                self.pin_module[i].Set_Active( True )
            else:
                self.pin_module[i].Set_Active( False )

    def Reference_Name( self ):
        self.dialog.name_display.setText( self.cor["name"] )
        self.dialog.kelvin_class.setText( kelvin["class"] )
        self.dialog.kelvin_discription.setText( kelvin["description"] )

    #endregion
    #region Gradients ##############################################################

    def Gradient_Style( self, mode, short, stops, left, right ):
        # mode = color space
        # short = straight ahead or shortest distance
        # stops = amount of divisions
        # left and right = colors in 0-1 format

        # Variables
        hue = [ "HSV", "HSL", "HSY", "ARD" ]

        # Length
        len_left = len( left )
        len_right = len( right )
        if len_left == len_right:
            # Size
            length = len_left

            # Round Left to 0.000
            l1 = round( left[0],3 )
            if length >= 3:
                l2 = round( left[1],3 )
                l3 = round( left[2],3 )
            if length >= 4:
                l4 = round( left[3],3 )
            # Round Right to 0.000
            r1 = round( right[0],3 )
            if length >= 3:
                r2 = round( right[1],3 )
                r3 = round( right[2],3 )
            if length >= 4:
                r4 = round( right[3],3 )

            # delta
            if ( mode in hue and short == True ):
                dist_a = r1 - l1
                if l1 < r1:
                    dist_b = ( r1 - 1 ) - l1
                    unit = - 1 / 360
                else:
                    dist_b = ( r1 + 1 ) - l1
                    unit = 1 / 360
                dist = [ ( abs( dist_a ), dist_a ), ( abs( dist_b + unit ), dist_b ) ]
                d1 = sorted( dist )[0][1] / stops
            else:
                d1 = ( r1 - l1 ) / stops
            if length >= 3:
                d2 = ( r2 - l2 ) / stops
                d3 = ( r3 - l3 ) / stops
            if length >= 4:
                d4 = ( r4 - l4 ) / stops

            # Output
            output = []
            for i in range( 0, stops+1 ):
                # Value Interpolated
                stop_i = [ self.geometry.Limit_Looper( l1 + ( d1 * i ), 1 ) ]
                if length >= 3:
                    stop_i.append( l2 + ( d2 * i ) )
                    stop_i.append( l3 + ( d3 * i ) )
                if length >= 4:
                    stop_i.append( l4 + ( d4 * i ) )

                # Calculate RGB
                if mode == "A":
                    rgb = self.convert.aaa_to_rgb( *stop_i )
                if mode == "RGB":
                    rgb = stop_i
                if mode == "CMY":
                    rgb = self.convert.cmy_to_rgb( *stop_i )
                if mode == "CMYK":
                    rgb = self.convert.cmyk_to_rgb( *stop_i )
                if mode == "RYB":
                    rgb = self.convert.ryb_to_rgb( *stop_i )
                if mode == "YUV":
                    rgb = self.convert.yuv_to_rgb( *stop_i )

                if mode == "HSV":
                    rgb = self.convert.hsv_to_rgb( *stop_i )
                if mode == "HSL":
                    rgb = self.convert.hsl_to_rgb( *stop_i )
                if mode == "HSY":
                    rgb = self.convert.hsy_to_rgb( *stop_i )
                if mode == "ARD":
                    rgb = self.convert.ard_to_rgb( *stop_i )

                if mode == "XYZ":
                    rgb = self.convert.xyz_to_rgb( *stop_i )
                if mode == "XYY":
                    rgb = self.convert.xyy_to_rgb( *stop_i )
                if mode == "LAB":
                    rgb = self.convert.lab_to_rgb( *stop_i )

                if mode == "LCH":
                    rgb = self.convert.lch_to_rgb( *stop_i )

                # Display


                # Output
                output.append( rgb )
            # Return
            return output
    def Gradient_Kelvin( self, lock, stops, red, green, blue ):
        # Variables
        delta = kkk_delta / stops
        # Calculations
        output = []
        for i in range( 0, stops+1 ):
            # Temperature
            temp = kkk_min_scale + ( delta * i )
            rgb = self.convert.kkk_to_rgb( temp, kelvin_rgb )
            # Lock
            if self.lock_kkk_1 == False:
                rgb = [rgb[0] * red, rgb[1] * green, rgb[2] * blue]
            # Display

            # Output
            output.append( rgb )
        # Return
        return output

    #endregion
    #region Header #################################################################

    def Header_Shift( self, SIGNAL_SHIFT ):
        # Shift Foreground and Background
        if SIGNAL_SHIFT == True:
            self.cor = kac
        if SIGNAL_SHIFT == False:
            self.cor = kbc

        # Save Mode
        self.mode_ab = SIGNAL_SHIFT
        self.Pigmento_RELEASE()
    def Header_Swap( self ):
        self.Color_Swap()
        self.Pigmento_RELEASE()

    #endregion
    #region Harmony ################################################################

    # Context Menu
    def Harmony_Rule( self, harmony_rule ):
        self.harmony_rule = harmony_rule
        self.harmony_spread.Set_Rule( self.harmony_rule )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "harmony_rule", str( self.harmony_rule ) )
    def Harmony_Edit( self, harmony_edit ):
        self.harmony_edit = harmony_edit
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "harmony_edit", str( self.harmony_edit ) )
    def Harmony_Index( self, harmony_index ):
        self.harmony_index = harmony_index
        self.Cor_Number( self.harmony_index )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "har_index", str( self.harmony_index ) )
    def Harmony_Spread( self, harmony_span ):
        self.harmony_span = harmony_span
        self.Pigmento_RELEASE()
        self.Label_String( f"{ round( self.harmony_span * 360, 2 )}º" )
        Krita.instance().writeSetting( "Pigment.O", "harmony_span", str( self.harmony_span ) )

    # Interaction
    def Cor_Number( self, number ):
        if self.harmony_index == 0:
            if self.mode_ab == True:
                self.cor = kac
            if self.mode_ab == False:
                self.cor = kbc
        if self.harmony_index == 1:
            self.cor = har_01
        if self.harmony_index == 2:
            self.cor = har_02
        if self.harmony_index == 3:
            self.cor = har_03
        if self.harmony_index == 4:
            self.cor = har_04
        if self.harmony_index == 5:
            self.cor = har_05

    # Send
    def Harmony_Update( self ):
        if self.harmony_rule == "Triadic":
            parts = 3
            colors = [ har_01["hex6"], har_02["hex6"], har_03["hex6"] ]
        elif self.harmony_rule == "Tetradic":
            parts = 4
            colors = [ har_01["hex6"], har_02["hex6"], har_03["hex6"], har_04["hex6"] ]
        else:
            parts = 5
            colors = [ har_01["hex6"], har_02["hex6"], har_03["hex6"], har_04["hex6"], har_05["hex6"] ]
        self.harmony_swatch.Set_Harmony_Parts( parts, colors )

    #endregion
    #region Panel Fill #############################################################

    def Update_Panel_Fill( self ):
        # Foreground Color
        self.panel_fill.Update_Panel( self.cor )

    #endregion
    #region Panel Square ###########################################################

    # Send
    def Update_Panel_Square( self ):
        # Cor
        self.panel_square.Update_Panel( self.cor )
        # Harmony
        if self.ui_harmony == True:
            if self.harmony_rule == "Triadic":
                harmony_list = [har_01, har_02, har_03]
            elif self.harmony_rule == "Tetradic":
                harmony_list = [har_01, har_02, har_03, har_04]
            else:
                harmony_list = [har_01, har_02, har_03, har_04, har_05]
            self.panel_square.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_square.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True:
            self.panel_square.Update_Pin( self.pin_cor )
        else:
            self.panel_square.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:
            self.panel_square.Update_Analyse( self.analyse_collection )
        else:
            self.panel_square.Update_Analyse( None )
    # Recieve
    def Square_Value( self, value ):
        self.widget_press = True
        c1, c2, c3 = self.Hue_Index( value["mode"] )
        self.Color_Convert( value["mode"], self.cor[c1], value["c2"], value["c3"], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Square_Tangent( self, tangent ):
        self.widget_press = True
        c1, c2, c3 = self.Hue_Index( self.wheel_space )
        self.Color_Convert( self.wheel_space, tangent, self.cor[c2], self.cor[c3], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Square_Pin( self, pin ):
        # Variables
        mode = pin["mode"]
        index = pin["pin_index"]
        # Color
        color = self.Color_Convert( mode, self.cor[f"{ mode.lower() }_1"], pin["c2"], pin["c3"], 0, self.pin_cor[index] )
        self.Dict_Copy( self.pin_cor[index], color )
        self.pin_module[index].Set_Color( self.pin_cor[index]["hex6"] )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "pin_cor", str( self.pin_cor ) )

    #endregion
    #region Panel Hue ##############################################################

    # Send
    def Update_Panel_HueCircle( self ):
        # Cor
        self.panel_huecircle.Update_Panel( self.cor )
        # Harmony
        if self.ui_harmony == True:
            if self.harmony_rule == "Triadic":
                harmony_list = [har_01, har_02, har_03]
            elif self.harmony_rule == "Tetradic":
                harmony_list = [har_01, har_02, har_03, har_04]
            else:
                harmony_list = [har_01, har_02, har_03, har_04, har_05]
            self.panel_huecircle.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_huecircle.Update_Harmony( None, None, None )

        # Subpanel
        self.panel_huesubpanel.Update_Panel( self.cor )
        # Harmony
        if self.ui_harmony == True:
            if self.harmony_rule == "Triadic":
                harmony = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == "Tetradic":
                harmony = [ har_01, har_02, har_03, har_04 ]
            else:
                harmony = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_huesubpanel.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_huesubpanel.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True:
            self.panel_huesubpanel.Update_Pin( self.pin_cor )
        else:
            self.panel_huesubpanel.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:
            self.panel_huesubpanel.Update_Analyse( self.analyse_collection )
        else:
            self.panel_huesubpanel.Update_Analyse( None )

    # Recieve
    def HueCircle_Value( self, angle ):
        self.widget_press = True
        c1, c2, c3 = self.Hue_Index( self.wheel_space )
        self.Color_Convert( self.wheel_space, angle, self.cor[c2], self.cor[c3], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def HueCircle_SubPanel( self, huecircle_shape ):
        # Variable
        self.huecircle_shape = huecircle_shape
        # Modules
        if self.huecircle_shape == "Triangle":
            self.panel_huesubpanel.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", "HSL", "3" ) # Triangle
        if self.huecircle_shape == "Square":
            self.panel_huesubpanel.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", self.wheel_space, "4" ) # Square
        if self.huecircle_shape == "Diamond":
            self.panel_huesubpanel.Set_ColorSpace_inDocument( self.directory_plugin, "RGB", "HSL", "R" ) # Diamond
        # Modules
        self.Update_Size() # Updates Mask
        # Save
        Krita.instance().writeSetting( "Pigment.O", "huecircle_shape", str( self.huecircle_shape ) )
    def HueCircle_Geo( self, width, height ):
        # Widget
        w2 = int( width * 0.5 )
        h2 = int( height * 0.5 )
        # Frame
        if width >= height:
            side = height
            px = int( w2 - ( side * 0.5 ) )
            py = 0
        else:
            side = width
            px = 0
            py = int( h2 - ( side * 0.5 ) )

        # Variables
        if self.huecircle_shape == "None":
            index = 0
            px = -10
            py = -10
            w = 10
            h = 10
        if self.huecircle_shape == "Triangle":
            index = 0
            k = 0.07
            x = 0.28
            y1 = 0.13
            y2 = 2 * y1
            px = int( px + x * side )
            py = int( py + y1 * side + 1 )
            w = int( side - x * side - k * side )
            h = int( side - y2 * side )
        if self.huecircle_shape == "Square":
            index = 1
            k1 = 0.2
            k2 = 2 * k1
            px = int( px + k1 * side )
            py = int( py + k1 * side )
            w = int( side - k2 * side )
            h = int( side - k2 * side )
        if self.huecircle_shape == "Diamond":
            index = 2
            k1 = 0.07
            k2 = 2 * k1
            px = int( px + k1 * side )
            py = int( py + k1 * side + 1 )
            w = int( side - k2 * side )
            h = int( side - k2 * side )
            
        # Geometry
        self.layout.panel_huesubpanel.setGeometry( px, py, w, h )
        self.panel_huesubpanel.Set_Size( w, h )

    #endregion
    #region Panel Gamut ############################################################

    # Send
    def Update_Panel_Gamut( self ):
        # Cor
        self.panel_gamut.Update_Panel( self.cor )
        # Harmony
        if self.ui_harmony == True:
            if self.harmony_rule == "Triadic":
                harmony_list = [har_01, har_02, har_03]
            elif self.harmony_rule == "Tetradic":
                harmony_list = [har_01, har_02, har_03, har_04]
            else:
                harmony_list = [har_01, har_02, har_03, har_04, har_05]
            self.panel_gamut.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_gamut.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True:
            self.panel_gamut.Update_Pin( self.pin_cor )
        else:
            self.panel_gamut.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:
            self.panel_gamut.Update_Analyse( self.analyse_collection )
        else:
            self.panel_gamut.Update_Analyse( None )
    # Recieve
    def Gamut_Value( self, value ):
        self.widget_press = True
        mode = self.wheel_space
        self.Color_Convert( mode, value["c1"], value["c2"], self.cor[f"{ mode.lower() }_3"], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Gamut_Tangent( self, tangent ):
        self.widget_press = True
        index = self.wheel_space.lower()
        self.Color_Convert( self.wheel_space, self.cor[f"{index}_1"], self.cor[f"{index}_2"], tangent, 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Gamut_Mask( self, gamut_mask ):
        self.gamut_mask = gamut_mask
        Krita.instance().writeSetting( "Pigment.O", "gamut_mask", str( self.gamut_mask ) )
    def Gamut_Profile( self, gamut_profile ):
        self.gamut_profile = gamut_profile
        Krita.instance().writeSetting( "Pigment.O", "gamut_profile", str( self.gamut_profile ) )
    def Gamut_Pin( self, pin ):
        # Variables
        mode = self.wheel_space
        index = pin["pin_index"]
        # Color
        color = self.Color_Convert( mode, pin["c1"], pin["c2"], self.cor[f"{ mode.lower() }_3"], 0, self.pin_cor[index] )
        self.Dict_Copy( self.pin_cor[index], color )
        self.pin_module[index].Set_Color( self.pin_cor[index]["hex6"] )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "pin_cor", str( self.pin_cor ) )

    #endregion
    #region Panel Hexagon ##########################################################

    # Send
    def Update_Panel_Hexagon( self ):
        # Cor
        self.panel_hexagon.Update_Panel( self.cor )
        # Harmony
        if self.ui_harmony == True:
            if self.harmony_rule == "Triadic":
                harmony_list = [har_01, har_02, har_03]
            elif self.harmony_rule == "Tetradic":
                harmony_list = [har_01, har_02, har_03, har_04]
            else:
                harmony_list = [har_01, har_02, har_03, har_04, har_05]
            self.panel_hexagon.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_hexagon.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True:
            self.panel_hexagon.Update_Pin( self.pin_cor )
        else:
            self.panel_hexagon.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:
            self.panel_hexagon.Update_Analyse( self.analyse_collection )
        else:
            self.panel_hexagon.Update_Analyse( None )
    # Recieve
    def Hexagon_Value( self, value ):
        self.widget_press = True
        self.Color_Convert( "UVD", value["c1"], value["c2"], self.cor["uvd_3"], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Hexagon_Depth( self, depth ):
        self.widget_press = True
        self.Color_Convert( "ARD", self.cor["ard_1"], self.cor["ard_2"], depth, 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Hexagon_Pin( self, pin ):
        index = pin["pin_index"]
        color = self.Color_Convert( "UVD", pin["c1"], pin["c2"], self.cor["uvd_3"], 0, self.pin_cor[index] )
        self.Dict_Copy( self.pin_cor[index], color )
        self.pin_module[index].Set_Color( self.pin_cor[index]["hex6"] )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "pin_cor", str( self.pin_cor ) )

    #endregion
    #region Panel Luma #############################################################

    # Send
    def Update_Panel_Luma( self ):
        # Cor
        self.panel_luma.Update_Panel( self.cor )
        # Harmony
        if self.ui_harmony == True:
            if self.harmony_rule == "Triadic":
                harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == "Tetradic":
                harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:
                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_luma.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_luma.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True:
            self.panel_luma.Update_Pin( self.pin_cor )
        else:
            self.panel_luma.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:
            self.panel_luma.Update_Analyse( self.analyse_collection )
        else:
            self.panel_luma.Update_Analyse( None )
    # Recieve
    def Luma_Value( self, value ):
        self.widget_press = True
        c1, c2, c3 = self.Hue_Index( value["mode"] )
        self.Color_Convert( value["mode"], self.cor[c1], value["c2"], value["c3"], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Luma_Tangent( self, tangent ):
        self.widget_press = True
        self.Color_Convert( "YUV", tangent, self.cor["yuv_2"], self.cor["yuv_3"], 0, self.cor )
        self.Sync_Elements( not self.performance_release, True, False )
    def Luma_Pin( self, pin ):
        # Variables
        index = pin["pin_index"]
        # Color
        color = self.Color_Convert( "YUV", self.cor[f"yuv_1"], pin["c2"], pin["c3"], 0, self.pin_cor[index] )
        self.Dict_Copy( self.pin_cor[index], color )
        self.pin_module[index].Set_Color( self.pin_cor[index]["hex6"] )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "pin_cor", str( self.pin_cor ) )

    #endregion
    #region Panel DOT ##############################################################

    # UI
    def Dot_Widget( self, boolean ):
        if boolean == True:
            horz = 5
            vert = 2
            mini = 5
            maxi = 120
        else:
            horz = 0
            vert = 0
            mini = 0
            maxi = 0
        self.layout.edit_dot.setMinimumWidth( mini )
        self.layout.edit_dot.setMaximumWidth( maxi )
        self.layout.edit_dot_layout.setContentsMargins( horz, vert, horz, vert )

    # Send
    def Dot_Update( self ):
        self.Update_Panel_Dot()
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "dot_1", str( self.dot_1 ) )
        Krita.instance().writeSetting( "Pigment.O", "dot_2", str( self.dot_2 ) )
        Krita.instance().writeSetting( "Pigment.O", "dot_3", str( self.dot_3 ) )
        Krita.instance().writeSetting( "Pigment.O", "dot_4", str( self.dot_4 ) )
    def Update_Panel_Dot( self ):
        # Color Lines
        line_top = []
        for i in range( 0, self.dot_dimension ):
            line_top.append( self.dot_3 )
        line_mid = []
        for i in range( 0, self.dot_dimension ):
            if i == self.dot_dimension:
                color = dot_2
            else:
                factor = i / ( self.dot_dimension-1 )
                color = self.Color_Interpolate( self.dot_interpolation, self.dot_1, self.dot_2, factor )
            line_mid.append( color )
        line_bot = []
        for i in range( 0, self.dot_dimension ):
            line_bot.append( self.dot_4 )

        # Color Matrix
        dot_matrix = []
        value_top = 0
        value_mid = int( self.dot_dimension * 0.5 )
        value_bot = self.dot_dimension - 1
        for y in range( 0, self.dot_dimension ):
            line = []
            for x in range( 0, self.dot_dimension ):
                if y == value_top:
                    line.append( line_top[x]["hex6"] )
                if ( y > value_top and y < value_mid ):
                    factor = y / value_mid
                    color_a = line_top[x]
                    color_b = line_mid[x]
                    color = self.Color_Interpolate( self.dot_interpolation, color_a, color_b, factor )
                    line.append( color["hex6"] )
                if y == value_mid:
                    line.append( line_mid[x]["hex6"] )
                if ( y > value_mid and y < value_bot ):
                    factor = ( y-value_mid ) / value_mid
                    color_a = line_mid[x]
                    color_b = line_bot[x]
                    color = self.Color_Interpolate( self.dot_interpolation, color_a, color_b, factor )
                    line.append( color["hex6"] )
                if y == value_bot:
                    line.append( line_bot[x]["hex6"] )
            dot_matrix.append( line )
        if len( dot_matrix ) == 0:
            dot_matrix = None

        # Update
        self.panel_dot.Update_Color( dot_matrix )
    def Update_Edit_Dot( self ):
        self.pin_d1.Set_Color( self.dot_1["hex6"] )
        self.pin_d2.Set_Color( self.dot_2["hex6"] )
        self.pin_d3.Set_Color( self.dot_3["hex6"] )
        self.pin_d4.Set_Color( self.dot_4["hex6"] )
    # Recieve
    def Dot_Value( self, SIGNAL_VALUE ):
        self.widget_press = True
        hex_code = SIGNAL_VALUE
        valid_code = self.HEX_Valid( hex_code, 6 )
        if valid_code == True:
            rgb = self.convert.hex6_to_rgb( SIGNAL_VALUE )
            self.Color_Convert( "RGB", rgb[0], rgb[1], rgb[2], 0, self.cor )
            self.Sync_Elements( not self.performance_release, True, True )
    def Dot_Interpolation( self, SIGNAL_INTERPOLATION ):
        self.dot_interpolation = SIGNAL_INTERPOLATION
        self.panel_dot.Set_Interpolation( SIGNAL_INTERPOLATION )
        self.Update_Panel_Dot()
        Krita.instance().writeSetting( "Pigment.O", "dot_interpolation", str( self.dot_interpolation ) )
    def Dot_Dimension( self, SIGNAL_DIMENSION ):
        self.dot_dimension = SIGNAL_DIMENSION
        self.panel_dot.Set_Dimension( SIGNAL_DIMENSION )
        self.Update_Panel_Dot()
        Krita.instance().writeSetting( "Pigment.O", "dot_dimension", str( self.dot_dimension ) )
    def Dot_Edit( self, SIGNAL_EDIT ):
        # Signals
        self.dot_edit = SIGNAL_EDIT
        self.panel_dot.Set_Edit( SIGNAL_EDIT )
        self.Dot_Widget( SIGNAL_EDIT )
        self.Update_Panel_Dot()
        # Size
        self.Update_Size()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "dot_edit", str( self.dot_edit ) )
    def Dot_Zorn( self, SIGNAL_ZORN ):
        # Variables
        self.dot_1 = self.Color_Convert( "HEX", "#edb525", 0, 0, 0, self.dot_1 )
        self.dot_2 = self.Color_Convert( "HEX", "#b72e35", 0, 0, 0, self.dot_2 )
        self.dot_3 = self.Color_Convert( "HEX", "#edf0ec", 0, 0, 0, self.dot_3 )
        self.dot_4 = self.Color_Convert( "HEX", "#292421", 0, 0, 0, self.dot_4 )
        self.dot_1["active"] = True
        self.dot_2["active"] = True
        self.dot_3["active"] = True
        self.dot_4["active"] = True
        # Update
        self.Update_Panel_Dot()
        # Pins
        self.pin_d1.Set_Color( self.dot_1["hex6"] )
        self.pin_d2.Set_Color( self.dot_2["hex6"] )
        self.pin_d3.Set_Color( self.dot_3["hex6"] )
        self.pin_d4.Set_Color( self.dot_4["hex6"] )
        # Save
        Krita.instance().writeSetting( "Pigment.O", "dot_1", str( self.dot_1 ) )
        Krita.instance().writeSetting( "Pigment.O", "dot_2", str( self.dot_2 ) )
        Krita.instance().writeSetting( "Pigment.O", "dot_3", str( self.dot_3 ) )
        Krita.instance().writeSetting( "Pigment.O", "dot_4", str( self.dot_4 ) )

    # Button
    def Dot_Swap( self ):
        # Initial Swap
        a = self.dot_1.copy()
        b = self.dot_2.copy()
        c = self.dot_3.copy()
        d = self.dot_4.copy()
        # Final Swap
        self.dot_1 = c.copy()
        self.dot_2 = d.copy()
        self.dot_3 = a.copy()
        self.dot_4 = b.copy()
        # Functions
        self.pin_d1.Set_Color( self.dot_1["hex6"] )
        self.pin_d2.Set_Color( self.dot_2["hex6"] )
        self.pin_d3.Set_Color( self.dot_3["hex6"] )
        self.pin_d4.Set_Color( self.dot_4["hex6"] )
        # Update
        self.Update_Panel_Dot()

    # Apply
    def Dot_Apply_1( self, SIGNAL_APPLY ):
        if self.dot_1["active"] == True:
            self.Color_Convert( "HEX", self.dot_1["hex6"], 0, 0, 0, self.cor )
            self.Pigmento_RELEASE()
    def Dot_Apply_2( self, SIGNAL_APPLY ):
        if self.dot_2["active"] == True:
            self.Color_Convert( "HEX", self.dot_2["hex6"], 0, 0, 0, self.cor )
            self.Pigmento_RELEASE()
    def Dot_Apply_3( self, SIGNAL_APPLY ):
        if self.dot_3["active"] == True:
            self.Color_Convert( "HEX", self.dot_3["hex6"], 0, 0, 0, self.cor )
            self.Pigmento_RELEASE()
    def Dot_Apply_4( self, SIGNAL_APPLY ):
        if self.dot_4["active"] == True:
            self.Color_Convert( "HEX", self.dot_4["hex6"], 0, 0, 0, self.cor )
            self.Pigmento_RELEASE()
    # Save
    def Dot_Save_1( self, SIGNAL_SAVE ):
        self.dot_1["active"] = True
        self.Dict_Copy( self.dot_1, self.cor )
        self.pin_d1.Set_Color( self.dot_1["hex6"] )
        self.Dot_Update()
    def Dot_Save_2( self, SIGNAL_SAVE ):
        self.dot_2["active"] = True
        self.Dict_Copy( self.dot_2, self.cor )
        self.pin_d2.Set_Color( self.dot_2["hex6"] )
        self.Dot_Update()
    def Dot_Save_3( self, SIGNAL_SAVE ):
        self.dot_3["active"] = True
        self.Dict_Copy( self.dot_3, self.cor )
        self.pin_d3.Set_Color( self.dot_3["hex6"] )
        self.Dot_Update()
    def Dot_Save_4( self, SIGNAL_SAVE ):
        self.dot_4["active"] = True
        self.Dict_Copy( self.dot_4, self.cor )
        self.pin_d4.Set_Color( self.dot_4["hex6"] )
        self.Dot_Update()
    # Clean
    def Dot_Clean_1( self, SIGNAL_CLEAN ):
        self.dot_1["active"] = False
        self.Dict_Copy( self.dot_1, color_false )
        self.pin_d1.Set_Color( None )
        self.Dot_Update()
    def Dot_Clean_2( self, SIGNAL_CLEAN ):
        self.dot_2["active"] = False
        self.Dict_Copy( self.dot_2, color_false )
        self.pin_d2.Set_Color( None )
        self.Dot_Update()
    def Dot_Clean_3( self, SIGNAL_CLEAN ):
        self.dot_3["active"] = False
        self.Dict_Copy( self.dot_3, color_false )
        self.pin_d3.Set_Color( None )
        self.Dot_Update()
    def Dot_Clean_4( self, SIGNAL_CLEAN ):
        self.dot_4["active"] = False
        self.Dict_Copy( self.dot_4, color_false )
        self.pin_d4.Set_Color( None )
        self.Dot_Update()

    #endregion
    #region Panel MASK #############################################################

    # UI
    def Mask_Widget( self, boolean ):
        if boolean == True:
            horz = 5
            vert = 2
            mini = 5
            maxi = 120
        else:
            horz = 0
            vert = 0
            mini = 0
            maxi = 0
        self.layout.edit_mask.setMinimumWidth( mini )
        self.layout.edit_mask.setMaximumWidth( maxi )
        self.layout.edit_mask_layout.setContentsMargins( horz, vert, horz, vert )

    # Send
    def Update_Panel_Mask( self ):
        self.panel_mask.Update_Color( self.mask_color, self.mask_alpha )
    # Recieve
    def Mask_Value( self, SIGNAL_VALUE ):
        self.Pigmento_APPLY( "HEX", SIGNAL_VALUE, 0, 0, 0, self.cor )
    def Mask_Set( self, SIGNAL_MASKSET ):
        self.mask_set = SIGNAL_MASKSET
        self.Mask_Read( False )
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mask_set", str( self.mask_set ) )
        self.Mask_Write()
    def Mask_Edit( self, SIGNAL_EDIT ):
        # Signals
        self.mask_edit = SIGNAL_EDIT
        self.panel_mask.Set_Edit( SIGNAL_EDIT )
        self.Mask_Widget( SIGNAL_EDIT )
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mask_edit", str( self.mask_edit ) )

    # Operators
    def Mask_Load( self ):
        # Open File
        path = os.path.join( self.mask_set, "color.eo" )
        exists = os.path.exists( path )
        if exists == True:
            with open( path, "r" ) as color:
                data = color.readlines()

                for i in range( len( data ) ):
                    index = data[i]
                    if index.startswith( "mask_color=" ) == True:
                        line = index.replace( "mask_color=", "" )
                        self.mask_color = eval( line )
                    if index.startswith( "mask_alpha=" ) == True:
                        line = index.replace( "mask_alpha=", "" )
                        self.mask_alpha = eval( line )

                # Update
                self.Update_Panel_Mask()
                # Pins
                self.Mask_Pin_Color( self.mask_color )
                self.Mask_Pin_Alpha( self.mask_alpha )
    def Mask_Read( self, SIGNAL_RESET ):
        if self.panel_index == "Mask":
            # Open File
            path = os.path.join( self.mask_set, "color.eo" )
            with open( path, "r" ) as color:
                data = color.readlines()

                for i in range( len( data ) ):
                    index = data[i]
                    if SIGNAL_RESET == True:
                        if index.startswith( "default_color=" ) == True:
                            line = index.replace( "default_color=", "" )
                            self.mask_color = eval( line )
                        if index.startswith( "default_alpha=" ) == True:
                            line = index.replace( "default_alpha=", "" )
                            self.mask_alpha = eval( line )
                    else:
                        if index.startswith( "mask_color=" ) == True:
                            line = index.replace( "mask_color=", "" )
                            self.mask_color = eval( line )
                        if index.startswith( "mask_alpha=" ) == True:
                            line = index.replace( "mask_alpha=", "" )
                            self.mask_alpha = eval( line )

                # Update
                self.Update_Panel_Mask()
                # Pins
                self.Mask_Pin_Color( self.mask_color )
                self.Mask_Pin_Alpha( self.mask_alpha )
    def Mask_Write( self ):
        if ( self.panel_index == "Mask" and self.mask_write == False ):
            # Variables
            self.mask_write = True
            path = os.path.join( self.mask_set, "color.eo" )

            # Read
            with open( path, "r" ) as note:
                read = note.readlines()

            # Edit
            edit = ""
            for i in range( len( read ) ):
                index = read[i]
                if index.startswith( "mask_color=" ) == True:
                    line = "mask_color=" + str( self.mask_color ) + "\n"
                    index = line
                if index.startswith( "mask_alpha=" ) == True:
                    line = "mask_alpha=" + str( self.mask_alpha ) + "\n"
                    index = line
                edit += index

                # Write
                with open( path, "w" ) as note:
                    note.write( edit )
            
            # Variables
            self.mask_write = False

    # Pin
    def Mask_Pin_Color( self, mask_color ):
        # Background
        self.mask_b1.Set_Color( mask_color["b1"] )
        self.mask_b2.Set_Color( mask_color["b2"] )
        self.mask_b3.Set_Color( mask_color["b3"] )
        # Diffuse
        self.mask_d1.Set_Color( mask_color["d1"] )
        self.mask_d2.Set_Color( mask_color["d2"] )
        self.mask_d3.Set_Color( mask_color["d3"] )
        self.mask_d4.Set_Color( mask_color["d4"] )
        self.mask_d5.Set_Color( mask_color["d5"] )
        self.mask_d6.Set_Color( mask_color["d6"] )
        # Foreground
        self.mask_f1.Set_Color( mask_color["f1"] )
        self.mask_f2.Set_Color( mask_color["f2"] )
        self.mask_f3.Set_Color( mask_color["f3"] )
    def Mask_Pin_Alpha( self, mask_alpha ):
        # Background
        self.mask_b1.Set_Alpha( mask_alpha["b1"] )
        self.mask_b2.Set_Alpha( mask_alpha["b2"] )
        self.mask_b3.Set_Alpha( mask_alpha["b3"] )
        # Diffuse
        self.mask_d1.Set_Alpha( mask_alpha["d1"] )
        self.mask_d2.Set_Alpha( mask_alpha["d2"] )
        self.mask_d3.Set_Alpha( mask_alpha["d3"] )
        self.mask_d4.Set_Alpha( mask_alpha["d4"] )
        self.mask_d5.Set_Alpha( mask_alpha["d5"] )
        self.mask_d6.Set_Alpha( mask_alpha["d6"] )
        # Foreground
        self.mask_f1.Set_Alpha( mask_alpha["f1"] )
        self.mask_f2.Set_Alpha( mask_alpha["f2"] )
        self.mask_f3.Set_Alpha( mask_alpha["f3"] )
    # Live
    def Mask_Live_Update( self ):
        # Live
        if self.mask_live["b1"] == True:
            self.Mask_Save_B1( 0 )
        if self.mask_live["b2"] == True:
            self.Mask_Save_B2( 0 )
        if self.mask_live["b3"] == True:
            self.Mask_Save_B3( 0 )
        if self.mask_live["d1"] == True:
            self.Mask_Save_D1( 0 )
        if self.mask_live["d2"] == True:
            self.Mask_Save_D2( 0 )
        if self.mask_live["d3"] == True:
            self.Mask_Save_D3( 0 )
        if self.mask_live["d4"] == True:
            self.Mask_Save_D4( 0 )
        if self.mask_live["d5"] == True:
            self.Mask_Save_D5( 0 )
        if self.mask_live["d6"] == True:
            self.Mask_Save_D6( 0 )
        if self.mask_live["f1"] == True:
            self.Mask_Save_F1( 0 )
        if self.mask_live["f2"] == True:
            self.Mask_Save_F2( 0 )
        if self.mask_live["f3"] == True:
            self.Mask_Save_F3( 0 )

        # Update
        if True in self.mask_live:
            self.Update_Panel_Mask()
    def Mask_Live_Uncheck( self, item ):
        if item != "b1":
            self.layout.bg_1_live.setChecked( False )
        if item != "b2":
            self.layout.bg_2_live.setChecked( False )
        if item != "b3":
            self.layout.bg_3_live.setChecked( False )
        if item != "d1":
            self.layout.dif_1_live.setChecked( False )
        if item != "d2":
            self.layout.dif_2_live.setChecked( False )
        if item != "d3":
            self.layout.dif_3_live.setChecked( False )
        if item != "d4":
            self.layout.dif_4_live.setChecked( False )
        if item != "d5":
            self.layout.dif_5_live.setChecked( False )
        if item != "d6":
            self.layout.dif_6_live.setChecked( False )
        if item != "f1":
            self.layout.fg_1_live.setChecked( False )
        if item != "f2":
            self.layout.fg_2_live.setChecked( False )
        if item != "f3":
            self.layout.fg_3_live.setChecked( False )

    # Live
    def Mask_Live_B1( self, boolean ):
        self.mask_live["b1"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "b1" )
            self.Pigmento_APPLY( "HEX", self.mask_color["b1"], 0, 0, 0, self.cor )
    def Mask_Live_B2( self, boolean ):
        self.mask_live["b2"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "b2" )
            self.Pigmento_APPLY( "HEX", self.mask_color["b2"], 0, 0, 0, self.cor )
    def Mask_Live_B3( self, boolean ):
        self.mask_live["b3"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "b3" )
            self.Pigmento_APPLY( "HEX", self.mask_color["b3"], 0, 0, 0, self.cor )
    def Mask_Live_D1( self, boolean ):
        self.mask_live["d1"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "d1" )
            self.Pigmento_APPLY( "HEX", self.mask_color["d1"], 0, 0, 0, self.cor )
    def Mask_Live_D2( self, boolean ):
        self.mask_live["d2"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "d2" )
            self.Pigmento_APPLY( "HEX", self.mask_color["d2"], 0, 0, 0, self.cor )
    def Mask_Live_D3( self, boolean ):
        self.mask_live["d3"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "d3" )
            self.Pigmento_APPLY( "HEX", self.mask_color["d3"], 0, 0, 0, self.cor )
    def Mask_Live_D4( self, boolean ):
        self.mask_live["d4"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "d4" )
            self.Pigmento_APPLY( "HEX", self.mask_color["d4"], 0, 0, 0, self.cor )
    def Mask_Live_D5( self, boolean ):
        self.mask_live["d5"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "d5" )
            self.Pigmento_APPLY( "HEX", self.mask_color["d5"], 0, 0, 0, self.cor )
    def Mask_Live_D6( self, boolean ):
        self.mask_live["d6"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "d6" )
            self.Pigmento_APPLY( "HEX", self.mask_color["d6"], 0, 0, 0, self.cor )
    def Mask_Live_F1( self, boolean ):
        self.mask_live["f1"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "f1" )
            self.Pigmento_APPLY( "HEX", self.mask_color["f1"], 0, 0, 0, self.cor )
    def Mask_Live_F2( self, boolean ):
        self.mask_live["f2"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "f2" )
            self.Pigmento_APPLY( "HEX", self.mask_color["f2"], 0, 0, 0, self.cor )
    def Mask_Live_F3( self, boolean ):
        self.mask_live["f3"] = boolean
        if boolean == True:
            self.Mask_Live_Uncheck( "f3" )
            self.Pigmento_APPLY( "HEX", self.mask_color["f3"], 0, 0, 0, self.cor )
    # Apply
    def Mask_Apply_B1( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["b1"], 0, 0, 0, self.cor )
    def Mask_Apply_B2( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["b2"], 0, 0, 0, self.cor )
    def Mask_Apply_B3( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["b3"], 0, 0, 0, self.cor )
    def Mask_Apply_D1( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["d1"], 0, 0, 0, self.cor )
    def Mask_Apply_D2( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["d2"], 0, 0, 0, self.cor )
    def Mask_Apply_D3( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["d3"], 0, 0, 0, self.cor )
    def Mask_Apply_D4( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["d4"], 0, 0, 0, self.cor )
    def Mask_Apply_D5( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["d5"], 0, 0, 0, self.cor )
    def Mask_Apply_D6( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["d6"], 0, 0, 0, self.cor )
    def Mask_Apply_F1( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["f1"], 0, 0, 0, self.cor )
    def Mask_Apply_F2( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["f2"], 0, 0, 0, self.cor )
    def Mask_Apply_F3( self, SIGNAL_APPLY ):
        self.Pigmento_APPLY( "HEX", self.mask_color["f3"], 0, 0, 0, self.cor )
    # Save
    def Mask_Save_B1( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["b1"] = cor
        self.mask_b1.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_B2( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["b2"] = cor
        self.mask_b2.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_B3( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["b3"] = cor
        self.mask_b3.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_D1( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["d1"] = cor
        self.mask_d1.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_D2( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["d2"] = cor
        self.mask_d2.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_D3( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["d3"] = cor
        self.mask_d3.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_D4( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["d4"] = cor
        self.mask_d4.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_D5( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["d5"] = cor
        self.mask_d5.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_D6( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["d6"] = cor
        self.mask_d6.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_F1( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["f1"] = cor
        self.mask_f1.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_F2( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["f2"] = cor
        self.mask_f2.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    def Mask_Save_F3( self, SIGNAL_SAVE ):
        cor = self.cor["hex6"]
        self.mask_color["f3"] = cor
        self.mask_f3.Set_Color( cor )
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
    # Clean
    def Mask_Clean_B1( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["b1"] = cor
        self.mask_alpha["b1"] = 0
        self.mask_b1.Set_Color( cor )
        self.mask_b1.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_B2( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["b2"] = cor
        self.mask_alpha["b2"] = 0
        self.mask_b2.Set_Color( cor )
        self.mask_b2.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_B3( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["b3"] = cor
        self.mask_alpha["b3"] = 0
        self.mask_b3.Set_Color( cor )
        self.mask_b3.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_D1( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["d1"] = cor
        self.mask_alpha["d1"] = 0
        self.mask_d1.Set_Color( cor )
        self.mask_d1.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_D2( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["d2"] = cor
        self.mask_alpha["d2"] = 0
        self.mask_d2.Set_Color( cor )
        self.mask_d2.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_D3( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["d3"] = cor
        self.mask_alpha["d3"] = 0
        self.mask_d3.Set_Color( cor )
        self.mask_d3.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_D4( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["d4"] = cor
        self.mask_alpha["d4"] = 0
        self.mask_d4.Set_Color( cor )
        self.mask_d4.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_D5( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["d5"] = cor
        self.mask_alpha["d5"] = 0
        self.mask_d5.Set_Color( cor )
        self.mask_d5.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_D6( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["d6"] = cor
        self.mask_alpha["d6"] = 0
        self.mask_d6.Set_Color( cor )
        self.mask_d6.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_F1( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["f1"] = cor
        self.mask_alpha["f1"] = 0
        self.mask_f1.Set_Color( cor )
        self.mask_f1.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_F2( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["f2"] = cor
        self.mask_alpha["f2"] = 0
        self.mask_f2.Set_Color( cor )
        self.mask_f2.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Clean_F3( self, SIGNAL_CLEAN ):
        cor = "#000000"
        self.mask_color["f3"] = cor
        self.mask_alpha["f3"] = 0
        self.mask_f3.Set_Color( cor )
        self.mask_f3.Set_Alpha( 0 )
        Krita.instance().writeSetting( "Pigment.O", "mask_color", str( self.mask_color ) )
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    # Alpha
    def Mask_Alpha_B1( self, SIGNAL_ALPHA ):
        self.mask_alpha["b1"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_B2( self, SIGNAL_ALPHA ):
        self.mask_alpha["b2"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_B3( self, SIGNAL_ALPHA ):
        self.mask_alpha["b3"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_D1( self, SIGNAL_ALPHA ):
        self.mask_alpha["d1"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_D2( self, SIGNAL_ALPHA ):
        self.mask_alpha["d2"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_D3( self, SIGNAL_ALPHA ):
        self.mask_alpha["d3"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_D4( self, SIGNAL_ALPHA ):
        self.mask_alpha["d4"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_D5( self, SIGNAL_ALPHA ):
        self.mask_alpha["d5"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_D6( self, SIGNAL_ALPHA ):
        self.mask_alpha["d6"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_F1( self, SIGNAL_ALPHA ):
        self.mask_alpha["f1"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_F2( self, SIGNAL_ALPHA ):
        self.mask_alpha["f2"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )
    def Mask_Alpha_F3( self, SIGNAL_ALPHA ):
        self.mask_alpha["f3"] = SIGNAL_ALPHA
        self.Update_Panel_Mask()
        Krita.instance().writeSetting( "Pigment.O", "mask_alpha", str( self.mask_alpha ) )

    #endregion
    #region Channel Sliders ########################################################

    # AAA
    def Channels_AAA_1_Slider( self, sv ):
        self.Pigmento_PRESS( "A", sv["value"], 0, 0, 0, self.cor )
    # RGB
    def Channels_RGB_1_Slider( self, sv ):
        self.Pigmento_PRESS( "RGB", sv["value"], self.cor["rgb_2"], self.cor["rgb_3"], 0, self.cor )
    def Channels_RGB_2_Slider( self, sv ):
        self.Pigmento_PRESS( "RGB", self.cor["rgb_1"], sv["value"], self.cor["rgb_3"], 0, self.cor )
    def Channels_RGB_3_Slider( self, sv ):
        self.Pigmento_PRESS( "RGB", self.cor["rgb_1"], self.cor["rgb_2"], sv["value"], 0, self.cor )
    # CMY
    def Channels_CMY_1_Slider( self, sv ):
        self.Pigmento_PRESS( "CMY", sv["value"], self.cor["cmy_2"], self.cor["cmy_3"], 0, self.cor )
    def Channels_CMY_2_Slider( self, sv ):
        self.Pigmento_PRESS( "CMY", self.cor["cmy_1"], sv["value"], self.cor["cmy_3"], 0, self.cor )
    def Channels_CMY_3_Slider( self, sv ):
        self.Pigmento_PRESS( "CMY", self.cor["cmy_1"], self.cor["cmy_2"], sv["value"], 0, self.cor )
    # CMYK
    def Channels_CMYK_1_Slider( self, sv ):
        self.Pigmento_PRESS( "CMYK", sv["value"], self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"], self.cor )
    def Channels_CMYK_2_Slider( self, sv ):
        self.Pigmento_PRESS( "CMYK", self.cor["cmyk_1"], sv["value"], self.cor["cmyk_3"], self.cor["cmyk_4"], self.cor )
    def Channels_CMYK_3_Slider( self, sv ):
        self.Pigmento_PRESS( "CMYK", self.cor["cmyk_1"], self.cor["cmyk_2"], sv["value"], self.cor["cmyk_4"], self.cor )
    def Channels_CMYK_4_Slider( self, sv ):
        self.Pigmento_PRESS( "CMYK", self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], sv["value"], self.cor )
    # RYB
    def Channels_RYB_1_Slider( self, sv ):
        self.Pigmento_PRESS( "RYB", sv["value"], self.cor["ryb_2"], self.cor["ryb_3"], 0, self.cor )
    def Channels_RYB_2_Slider( self, sv ):
        self.Pigmento_PRESS( "RYB", self.cor["ryb_1"], sv["value"], self.cor["ryb_3"], 0, self.cor )
    def Channels_RYB_3_Slider( self, sv ):
        self.Pigmento_PRESS( "RYB", self.cor["ryb_1"], self.cor["ryb_2"], sv["value"], 0, self.cor )
    # YUV
    def Channels_YUV_1_Slider( self, sv ):
        self.Pigmento_PRESS( "YUV", sv["value"], self.cor["yuv_2"], self.cor["yuv_3"], 0, self.cor )
    def Channels_YUV_2_Slider( self, sv ):
        self.Pigmento_PRESS( "YUV", self.cor["yuv_1"], sv["value"], self.cor["yuv_3"], 0, self.cor )
    def Channels_YUV_3_Slider( self, sv ):
        self.Pigmento_PRESS( "YUV", self.cor["yuv_1"], self.cor["yuv_2"], sv["value"], 0, self.cor )

    # HSV
    def Channels_HSV_1_Slider( self, sv ):
        self.Pigmento_PRESS( "HSV", sv["value"], self.cor["hsv_2"], self.cor["hsv_3"], 0, self.cor )
    def Channels_HSV_2_Slider( self, sv ):
        self.Pigmento_PRESS( "HSV", self.cor["hsv_1"], sv["value"], self.cor["hsv_3"], 0, self.cor )
    def Channels_HSV_3_Slider( self, sv ):
        self.Pigmento_PRESS( "HSV", self.cor["hsv_1"], self.cor["hsv_2"], sv["value"], 0, self.cor )
    # HSL
    def Channels_HSL_1_Slider( self, sv ):
        self.Pigmento_PRESS( "HSL", sv["value"], self.cor["hsl_2"], self.cor["hsl_3"], 0, self.cor )
    def Channels_HSL_2_Slider( self, sv ):
        self.Pigmento_PRESS( "HSL", self.cor["hsl_1"], sv["value"], self.cor["hsl_3"], 0, self.cor )
    def Channels_HSL_3_Slider( self, sv ):
        self.Pigmento_PRESS( "HSL", self.cor["hsl_1"], self.cor["hsl_2"], sv["value"], 0, self.cor )
    # HSY
    def Channels_HSY_1_Slider( self, sv ):
        self.Pigmento_PRESS( "HSY", sv["value"], self.cor["hsy_2"], self.cor["hsy_3"], 0, self.cor )
    def Channels_HSY_2_Slider( self, sv ):
        self.Pigmento_PRESS( "HSY", self.cor["hsy_1"], sv["value"], self.cor["hsy_3"], 0, self.cor )
    def Channels_HSY_3_Slider( self, sv ):
        self.Pigmento_PRESS( "HSY", self.cor["hsy_1"], self.cor["hsy_2"], sv["value"], 0, self.cor )
    # ARD
    def Channels_ARD_1_Slider( self, sv ):
        self.Pigmento_PRESS( "ARD", sv["value"], self.cor["ard_2"], self.cor["ard_3"], 0, self.cor )
    def Channels_ARD_2_Slider( self, sv ):
        self.Pigmento_PRESS( "ARD", self.cor["ard_1"], sv["value"], self.cor["ard_3"], 0, self.cor )
    def Channels_ARD_3_Slider( self, sv ):
        self.Pigmento_PRESS( "ARD", self.cor["ard_1"], self.cor["ard_2"], sv["value"], 0, self.cor )

    # XYZ
    def Channels_XYZ_1_Slider( self, sv ):
        self.Pigmento_PRESS( "XYZ", sv["value"], self.cor["xyz_2"], self.cor["xyz_3"], 0, self.cor )
    def Channels_XYZ_2_Slider( self, sv ):
        self.Pigmento_PRESS( "XYZ", self.cor["xyz_1"], sv["value"], self.cor["xyz_3"], 0, self.cor )
    def Channels_XYZ_3_Slider( self, sv ):
        self.Pigmento_PRESS( "XYZ", self.cor["xyz_1"], self.cor["xyz_2"], sv["value"], 0, self.cor )
    # XYY
    def Channels_XYY_1_Slider( self, sv ):
        self.Pigmento_PRESS( "XYY", sv["value"], self.cor["xyy_2"], self.cor["xyy_3"], 0, self.cor )
    def Channels_XYY_2_Slider( self, sv ):
        self.Pigmento_PRESS( "XYY", self.cor["xyy_1"], sv["value"], self.cor["xyy_3"], 0, self.cor )
    def Channels_XYY_3_Slider( self, sv ):
        self.Pigmento_PRESS( "XYY", self.cor["xyy_1"], self.cor["xyy_2"], sv["value"], 0, self.cor )
    # LAB
    def Channels_LAB_1_Slider( self, sv ):
        self.Pigmento_PRESS( "LAB", sv["value"], self.cor["lab_2"], self.cor["lab_3"], 0, self.cor )
    def Channels_LAB_2_Slider( self, sv ):
        self.Pigmento_PRESS( "LAB", self.cor["lab_1"], sv["value"], self.cor["lab_3"], 0, self.cor )
    def Channels_LAB_3_Slider( self, sv ):
        self.Pigmento_PRESS( "LAB", self.cor["lab_1"], self.cor["lab_2"], sv["value"], 0, self.cor )

    # LCH
    def Channels_LCH_1_Slider( self, sv ):
        self.Pigmento_PRESS( "LCH", sv["value"], self.cor["lch_2"], self.cor["lch_3"], 0, self.cor )
    def Channels_LCH_2_Slider( self, sv ):
        self.Pigmento_PRESS( "LCH", self.cor["lch_1"], sv["value"], self.cor["lch_3"], 0, self.cor )
    def Channels_LCH_3_Slider( self, sv ):
        self.Pigmento_PRESS( "LCH", self.cor["lch_1"], self.cor["lch_2"], sv["value"], 0, self.cor )

    #endregion
    #region Channel Stops ##########################################################

    # AAA
    def Channels_AAA_1_Stops( self, ss ):
        stops["aaa_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # RGB
    def Channels_RGB_1_Stops( self, ss ):
        stops["rgb_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_RGB_2_Stops( self, ss ):
        stops["rgb_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_RGB_3_Stops( self, ss ):
        stops["rgb_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # CMY
    def Channels_CMY_1_Stops( self, ss ):
        stops["cmy_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_CMY_2_Stops( self, ss ):
        stops["cmy_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_CMY_3_Stops( self, ss ):
        stops["cmy_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # CMYK
    def Channels_CMYK_1_Stops( self, ss ):
        stops["cmyk_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_CMYK_2_Stops( self, ss ):
        stops["cmyk_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_CMYK_3_Stops( self, ss ):
        stops["cmyk_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_CMYK_4_Stops( self, ss ):
        stops["cmyk_4"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # RYB
    def Channels_RYB_1_Stops( self, ss ):
        stops["ryb_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_RYB_2_Stops( self, ss ):
        stops["ryb_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_RYB_3_Stops( self, ss ):
        stops["ryb_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # YUV
    def Channels_YUV_1_Stops( self, ss ):
        stops["yuv_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_YUV_2_Stops( self, ss ):
        stops["yuv_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_YUV_3_Stops( self, ss ):
        stops["yuv_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )

    # HSV
    def Channels_HSV_1_Stops( self, ss ):
        stops["hsv_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_HSV_2_Stops( self, ss ):
        stops["hsv_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_HSV_3_Stops( self, ss ):
        stops["hsv_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # HSL
    def Channels_HSL_1_Stops( self, ss ):
        stops["hsl_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_HSL_2_Stops( self, ss ):
        stops["hsl_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_HSL_3_Stops( self, ss ):
        stops["hsl_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # HSY
    def Channels_HSY_1_Stops( self, ss ):
        stops["hsy_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_HSY_2_Stops( self, ss ):
        stops["hsy_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_HSY_3_Stops( self, ss ):
        stops["hsy_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # ARD
    def Channels_ARD_1_Stops( self, ss ):
        stops["ard_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_ARD_2_Stops( self, ss ):
        stops["ard_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_ARD_3_Stops( self, ss ):
        stops["ard_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )

    # XYZ
    def Channels_XYZ_1_Stops( self, ss ):
        stops["xyz_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_XYZ_2_Stops( self, ss ):
        stops["xyz_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_XYZ_3_Stops( self, ss ):
        stops["xyz_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # XYY
    def Channels_XYY_1_Stops( self, ss ):
        stops["xyy_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_XYY_2_Stops( self, ss ):
        stops["xyy_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_XYY_3_Stops( self, ss ):
        stops["xyy_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    # LAB
    def Channels_LAB_1_Stops( self, ss ):
        stops["lab_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_LAB_2_Stops( self, ss ):
        stops["lab_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_LAB_3_Stops( self, ss ):
        stops["lab_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )

    # LCH
    def Channels_LCH_1_Stops( self, ss ):
        stops["lch_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_LCH_2_Stops( self, ss ):
        stops["lch_2"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_LCH_3_Stops( self, ss ):
        stops["lch_3"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )

    #endregion
    #region Channel Values #########################################################

    # AAA
    def Channels_AAA_1_Value( self, sv ):
        value = sv / krange["aaa_1"]
        self.Pigmento_PRESS( "A", value, 0, 0, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # RGB
    def Channels_RGB_1_Value( self, sv ):
        value = sv / krange["rgb_1"]
        self.Pigmento_PRESS( "RGB", value, self.cor["rgb_2"], self.cor["rgb_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_RGB_2_Value( self, sv ):
        value = sv / krange["rgb_2"]
        self.Pigmento_PRESS( "RGB", self.cor["rgb_1"], value, self.cor["rgb_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_RGB_3_Value( self, sv ):
        value = sv / krange["rgb_3"]
        self.Pigmento_PRESS( "RGB", self.cor["rgb_1"], self.cor["rgb_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # CMY
    def Channels_CMY_1_Value( self, sv ):
        value = sv / krange["cmy_1"]
        self.Pigmento_PRESS( "CMY", value, self.cor["cmy_2"], self.cor["cmy_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_CMY_2_Value( self, sv ):
        value = sv / krange["cmy_2"]
        self.Pigmento_PRESS( "CMY", self.cor["cmy_1"], value, self.cor["cmy_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_CMY_3_Value( self, sv ):
        value = sv / krange["cmy_3"]
        self.Pigmento_PRESS( "CMY", self.cor["cmy_1"], self.cor["cmy_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # CMYK
    def Channels_CMYK_1_Value( self, sv ):
        value = sv / krange["cmyk_1"]
        self.Pigmento_PRESS( "CMYK", value, self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"], self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_CMYK_2_Value( self, sv ):
        value = sv / krange["cmyk_2"]
        self.Pigmento_PRESS( "CMYK", self.cor["cmyk_1"], value, self.cor["cmyk_3"], self.cor["cmyk_4"], self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_CMYK_3_Value( self, sv ):
        value = sv / krange["cmyk_3"]
        self.Pigmento_PRESS( "CMYK", self.cor["cmyk_1"], self.cor["cmyk_2"], value, self.cor["cmyk_4"], self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_CMYK_4_Value( self, sv ):
        value = sv / krange["cmyk_4"]
        self.Pigmento_PRESS( "CMYK", self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], value, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # RYB
    def Channels_RYB_1_Value( self, sv ):
        value = sv / krange["ryb_1"]
        self.Pigmento_PRESS( "RYB", value, self.cor["ryb_2"], self.cor["ryb_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_RYB_2_Value( self, sv ):
        value = sv / krange["ryb_2"]
        self.Pigmento_PRESS( "RYB", self.cor["ryb_1"], value, self.cor["ryb_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_RYB_3_Value( self, sv ):
        value = sv / krange["ryb_3"]
        self.Pigmento_PRESS( "RYB", self.cor["ryb_1"], self.cor["ryb_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # YUV
    def Channels_YUV_1_Value( self, sv ):
        value = sv / krange["yuv_1"]
        self.Pigmento_PRESS( "YUV", value, self.cor["yuv_2"], self.cor["yuv_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_YUV_2_Value( self, sv ):
        value = sv / krange["yuv_2"]
        self.Pigmento_PRESS( "YUV", self.cor["yuv_1"], value, self.cor["yuv_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_YUV_3_Value( self, sv ):
        value = sv / krange["yuv_3"]
        self.Pigmento_PRESS( "YUV", self.cor["yuv_1"], self.cor["yuv_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )

    # HSV
    def Channels_HSV_1_Value( self, sv ):
        value = sv / krange["hsv_1"]
        self.Pigmento_PRESS( "HSV", value, self.cor["hsv_2"], self.cor["hsv_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_HSV_2_Value( self, sv ):
        value = sv / krange["hsv_2"]
        self.Pigmento_PRESS( "HSV", self.cor["hsv_1"], value, self.cor["hsv_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_HSV_3_Value( self, sv ):
        value = sv / krange["hsv_3"]
        self.Pigmento_PRESS( "HSV", self.cor["hsv_1"], self.cor["hsv_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # HSL
    def Channels_HSL_1_Value( self, sv ):
        value = sv / krange["hsl_1"]
        self.Pigmento_PRESS( "HSL", value, self.cor["hsl_2"], self.cor["hsl_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_HSL_2_Value( self, sv ):
        value = sv / krange["hsl_2"]
        self.Pigmento_PRESS( "HSL", self.cor["hsl_1"], value, self.cor["hsl_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_HSL_3_Value( self, sv ):
        value = sv / krange["hsl_3"]
        self.Pigmento_PRESS( "HSL", self.cor["hsl_1"], self.cor["hsl_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # HSY
    def Channels_HSY_1_Value( self, sv ):
        value = sv / krange["hsy_1"]
        self.Pigmento_PRESS( "HSY", value, self.cor["hsy_2"], self.cor["hsy_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_HSY_2_Value( self, sv ):
        value = sv / krange["hsy_2"]
        self.Pigmento_PRESS( "HSY", self.cor["hsy_1"], value, self.cor["hsy_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_HSY_3_Value( self, sv ):
        value = sv / krange["hsy_3"]
        self.Pigmento_PRESS( "HSY", self.cor["hsy_1"], self.cor["hsy_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # ARD
    def Channels_ARD_1_Value( self, sv ):
        value = sv / krange["ard_1"]
        self.Pigmento_PRESS( "ARD", value, self.cor["ard_2"], self.cor["ard_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_ARD_2_Value( self, sv ):
        value = sv / krange["ard_2"]
        self.Pigmento_PRESS( "ARD", self.cor["ard_1"], value, self.cor["ard_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_ARD_3_Value( self, sv ):
        value = sv / krange["ard_3"]
        self.Pigmento_PRESS( "ARD", self.cor["ard_1"], self.cor["ard_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )

    # XYZ
    def Channels_XYZ_1_Value( self, sv ):
        value = sv / krange["xyz_1"]
        self.Pigmento_PRESS( "XYZ", value, self.cor["xyz_2"], self.cor["xyz_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_XYZ_2_Value( self, sv ):
        value = sv / krange["xyz_2"]
        self.Pigmento_PRESS( "XYZ", self.cor["xyz_1"], value, self.cor["xyz_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_XYZ_3_Value( self, sv ):
        value = sv / krange["xyz_3"]
        self.Pigmento_PRESS( "XYZ", self.cor["xyz_1"], self.cor["xyz_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # XYY
    def Channels_XYY_1_Value( self, sv ):
        value = sv / krange["xyy_1"]
        self.Pigmento_PRESS( "XYY", value, self.cor["xyy_2"], self.cor["xyy_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_XYY_2_Value( self, sv ):
        value = sv / krange["xyy_2"]
        self.Pigmento_PRESS( "XYY", self.cor["xyy_1"], value, self.cor["xyy_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_XYY_3_Value( self, sv ):
        value = sv / krange["xyy_3"]
        self.Pigmento_PRESS( "XYY", self.cor["xyy_1"], self.cor["xyy_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # LAB
    def Channels_LAB_1_Value( self, sv ):
        value = sv / krange["lab_1"]
        self.Pigmento_PRESS( "LAB", value, self.cor["lab_2"], self.cor["lab_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_LAB_2_Value( self, sv ):
        value = sv / krange["lab_2"]
        self.Pigmento_PRESS( "LAB", self.cor["lab_1"], value, self.cor["lab_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_LAB_3_Value( self, sv ):
        value = sv / krange["lab_3"]
        self.Pigmento_PRESS( "LAB", self.cor["lab_1"], self.cor["lab_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )

    # LCH
    def Channels_LCH_1_Value( self, sv ):
        value = sv / krange["lch_1"]
        self.Pigmento_PRESS( "LCH", value, self.cor["lch_2"], self.cor["lch_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_LCH_2_Value( self, sv ):
        value = sv / krange["lch_2"]
        self.Pigmento_PRESS( "LCH", self.cor["lch_1"], value, self.cor["lch_3"], 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channels_LCH_3_Value( self, sv ):
        value = sv / krange["lch_3"]
        self.Pigmento_PRESS( "LCH", self.cor["lch_1"], self.cor["lch_2"], value, 0, self.cor )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )

    #endregion
    #region Channel Non Color ######################################################

    # KKK
    def Channels_KKK_1_Slider( self, sv ):
        percent = sv["value"]
        scale = self.convert.kkk_percent_to_scale( sv["value"] )
        self.Pigmento_PRESS( "KKK", percent, scale, 0, 0, self.cor )
    def Channels_KKK_1_Stops( self, ss ):
        stops["kkk_1"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )
    def Channels_KKK_1_Value( self, sv ):
        percent = self.convert.kkk_scale_to_percent( sv )
        scale = sv
        self.Pigmento_PRESS( "KKK", percent, scale, 0, 0, self.cor )
        self.Label_String( str( round( percent*100, 2 ) ) + " %" )

    def Kelvin_Class( self, scale ):
        # Variables
        cd = self.convert.kkk_to_cd( scale, kelvin_illuminants )
        # Write
        kelvin["class"] = cd[0]
        kelvin["description"] = cd[1]

    #endregion
    #region Mixer ##################################################################

    # Load
    def Mixer_LOAD( self ):
        # Clean Non Active Rows
        length = len( self.mixer_colors )
        to_pop = []
        for i in range( 1, length ):
            try:al = self.mixer_colors[i]["l"]["active"]
            except:al = False
            try:ar = self.mixer_colors[i]["r"]["active"]
            except:ar = False
            check = ( al == False and ar == False )
            if check == True:
                to_pop.append( i )
        to_pop.sort(reverse=True)
        for i in range( 0, len( to_pop ) ):
            self.mixer_colors.pop( to_pop[i] )

        # Widgets
        self.mixer_count = len( self.mixer_colors )
        self.dialog.mixer_count.setValue( self.mixer_count )
        self.Count_Construct( 1, self.mixer_count )

        # Render
        for i in range( 0, len( self.mixer_colors ) ):
            # Variables
            al = self.mixer_colors[i]["l"]["active"]
            ar = self.mixer_colors[i]["r"]["active"]
            if al == True:
                try:self.mixer_module[i]["l"].Set_Color( self.mixer_colors[i]["l"]["hex6"] )
                except:pass
            if ar == True:
                try:self.mixer_module[i]["r"].Set_Color( self.mixer_colors[i]["r"]["hex6"] )
                except:pass
            try:self.mixer_module[i]["m"].Set_Value( self.mixer_colors[i]["m"] )
            except:pass

    # Pin LEFT
    def Mixer_Apply_L( self, index ):
        if self.mixer_colors[index]["l"]["active"] == True:
            self.Dict_Copy( self.cor, self.mixer_colors[index]["l"] )
            self.Pigmento_RELEASE()
    def Mixer_Save_L( self, index ):
        self.Dict_Copy( self.mixer_colors[index]["l"], self.cor )
        self.mixer_module[index]["l"].Set_Color( self.cor["hex6"] )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_colors", str( self.mixer_colors ) )
    def Mixer_Clean_L( self, index ):
        self.Dict_Copy( self.mixer_colors[index]["l"], color_false )
        self.mixer_module[index]["l"].Set_Clean()
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_colors", str( self.mixer_colors ) )
    # Pin RIGHT
    def Mixer_Apply_R( self, index ):
        if self.mixer_colors[index]["r"]["active"] == True:
            self.Dict_Copy( self.cor, self.mixer_colors[index]["r"] )
            self.Pigmento_RELEASE()
    def Mixer_Save_R( self, index ):
        self.Dict_Copy( self.mixer_colors[index]["r"], self.cor )
        self.mixer_module[index]["r"].Set_Color( self.cor["hex6"] )
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_colors", str( self.mixer_colors ) )
    def Mixer_Clean_R( self, index ):
        self.Dict_Copy( self.mixer_colors[index]["r"], color_false )
        self.mixer_module[index]["r"].Set_Clean()
        self.Pigmento_RELEASE()
        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_colors", str( self.mixer_colors ) )
    # Slider
    def Mixer_Slider_M( self, sv ):
        # Variables
        index = sv["index"]
        value = sv["value"]
        mode = self.mixer_space

        # Write
        self.mixer_colors[index]["m"] = value

        # Active
        al = self.mixer_colors[index]["l"]["active"]
        ar = self.mixer_colors[index]["r"]["active"]
        if ( al == True and ar == True ):
            # Color Apply
            color = self.Color_Interpolate( mode, self.mixer_colors[index]["l"], self.mixer_colors[index]["r"], value )
            if mode == "A":
                self.Pigmento_PRESS( mode, color["aaa_1"], 0, 0, 0, self.cor )
            if mode == "RGB":
                self.Pigmento_PRESS( mode, color["rgb_1"], color["rgb_2"], color["rgb_3"], 0, self.cor )
            if mode == "CMY":
                self.Pigmento_PRESS( mode, color["cmy_1"], color["cmy_2"], color["cmy_3"], 0, self.cor )
            if mode == "CMYK":
                self.Pigmento_PRESS( mode, color["cmyk_1"], color["cmyk_2"], color["cmyk_3"], color["cmyk_4"], self.cor )
            if mode == "RYB":
                self.Pigmento_PRESS( mode, color["ryb_1"], color["ryb_2"], color["ryb_3"], 0, self.cor )
            if mode == "YUV":
                self.Pigmento_PRESS( mode, color["yuv_1"], color["yuv_2"], color["yuv_3"], 0, self.cor )
            if mode == "HSV":
                self.Pigmento_PRESS( mode, color["hsv_1"], color["hsv_2"], color["hsv_3"], 0, self.cor )
            if mode == "HSL":
                self.Pigmento_PRESS( mode, color["hsl_1"], color["hsl_2"], color["hsl_3"], 0, self.cor )
            if mode == "HSY":
                self.Pigmento_PRESS( mode, color["hsy_1"], color["hsy_2"], color["hsy_3"], 0, self.cor )
            if mode == "ARD":
                self.Pigmento_PRESS( mode, color["ard_1"], color["ard_2"], color["ard_3"], 0, self.cor )
            if mode == "XYZ":
                self.Pigmento_PRESS( mode, color["xyz_1"], color["xyz_2"], color["xyz_3"], 0, self.cor )
            if mode == "XYY":
                self.Pigmento_PRESS( mode, color["xyy_1"], color["xyy_2"], color["xyy_3"], 0, self.cor )
            if mode == "LAB":
                self.Pigmento_PRESS( mode, color["lab_1"], color["lab_2"], color["lab_3"], 0, self.cor )
            if mode == "LCH":
                self.Pigmento_PRESS( mode, color["lch_1"], color["lch_2"], color["lch_3"], 0, self.cor )

        # Save
        Krita.instance().writeSetting( "Pigment.O", "mixer_colors", str( self.mixer_colors ) )
    def Mixer_Stops_M( self, ss ):
        stops["mixer"] = ss
        Krita.instance().writeSetting( "Pigment.O", "stops", str( stops ) )

    #endregion
    #region Pin ####################################################################

    def Pin_LOAD( self ):
        for i in range( 0, len( self.pin_cor ) ):
            if self.pin_cor[i]["active"] == True:
                self.pin_module[i].Set_Color( self.pin_cor[i]["hex6"] )
            else:
                self.pin_module[i].Set_Clean()
    def Pin_Apply( self, index ):
        if index in range( 0, len( self.pin_cor ) ):
            if self.pin_cor[index]["active"] == True:
                self.Dict_Copy( self.cor, self.pin_cor[index] )
                self.Pigmento_RELEASE()
    def Pin_Save( self, index ):
        self.Dict_Copy( self.pin_cor[index], self.cor )
        self.pin_module[index].Set_Color( self.pin_cor[index]["hex6"] )
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "pin_cor", str( self.pin_cor ) )
    def Pin_Clean( self, index ):
        self.Dict_Copy( self.pin_cor[index], color_false )
        self.pin_module[index].Set_Clean()
        self.Pigmento_RELEASE()
        Krita.instance().writeSetting( "Pigment.O", "pin_cor", str( self.pin_cor ) )

    #endregion
    #region History ################################################################

    def History_List( self, red, green, blue ):
        # Last Entry
        last_item = self.layout.history_list.item( 0 )
        if last_item == None:
            self.History_Add( red, green, blue )
        else:
            if ( self.widget_press == False and self.inbound == False ):
                # Input Color
                input_red = int( red * 255 )
                input_green = int( green * 255 )
                input_blue = int( blue * 255 )
                # Last Colors
                last_color = last_item.background().color()
                last_red = int( last_color.red() )
                last_green = int( last_color.green() )
                last_blue = int( last_color.blue() )

                # Apply Colors Values
                if ( ( input_red != last_red ) or ( input_green != last_green ) or ( input_blue != last_blue ) ):
                    self.History_Add( red, green, blue )
    def History_Add( self, red, green, blue ):
        color = QColor( int(red * 255), int(green * 255), int(blue * 255) )
        pixmap = QPixmap( 10,20 )
        pixmap.fill( color )
        item = QListWidgetItem()
        item.setIcon( QIcon( pixmap ) )
        item.setBackground( QBrush( color ) )
        self.layout.history_list.insertItem( 0, item )
    def History_APPLY( self ):
        current = self.layout.history_list.currentItem()
        color = current.background().color()
        red = color.red() / 255
        green = color.green() / 255
        blue = color.blue() / 255
        self.Pigmento_APPLY( "RGB", red, green, blue, 0, self.cor )
    def History_CLEAR( self ):
        self.layout.history_list.clear()

    #endregion
    #region Fill Pixels ############################################################

    def Fill_Check( self, doc ):
        try:
            check_alpha = Krita.instance().activeDocument().nodeByName( fill["node_name"] ).alphaLocked()
            check_fill = fill["active"] == True and fill["node_name"] == doc["d_nn"] and check_alpha == True
        except:
            check_fill = False
        return check_fill
    def Fill_None( self ):
        # Layers
        try:
            try:Krita.instance().activeDocument().nodeByName( fill["node_name"] ).setAlphaLocked( fill["alphalock_before"] )
            except:Krita.instance().activeDocument().nodeByName( fill["node_name"] ).setAlphaLocked( False )
        except:
            pass
        # Variables
        fill["active"] = False
        fill["node_name"] = None
        fill["alphalock_before"] = None
        # UI
        self.layout.fill.blockSignals( True )
        self.layout.fill.setIcon( Krita.instance().icon( "folder-documents" ) )
        self.layout.fill.setChecked( False )
        self.layout.fill.blockSignals( False )

    #endregion
    #region Selection ##############################################################

    # Value Slider
    def Channels_SELE_1_Slider( self, value ):
        sele_1_var["l0"] = value["l0"]
        sele_1_var["l1"] = value["l1"]
        sele_1_var["r1"] = value["r1"]
        sele_1_var["r0"] = value["r0"]
        self.Update_Values()
        self.update()
    def Channels_SELE_2_Slider( self, value ):
        sele_2_var["l0"] = value["l0"]
        sele_2_var["l1"] = value["l1"]
        sele_2_var["r1"] = value["r1"]
        sele_2_var["r0"] = value["r0"]
        self.Update_Values()
        self.update()
    def Channels_SELE_3_Slider( self, value ):
        sele_3_var["l0"] = value["l0"]
        sele_3_var["l1"] = value["l1"]
        sele_3_var["r1"] = value["r1"]
        sele_3_var["r0"] = value["r0"]
        self.Update_Values()
        self.update()
    def Channels_SELE_4_Slider( self, value ):
        sele_4_var["l0"] = value["l0"]
        sele_4_var["l1"] = value["l1"]
        sele_4_var["r1"] = value["r1"]
        sele_4_var["r0"] = value["r0"]
        self.Update_Values()
        self.update()
    # Reset Slider
    def Channels_SELE_1_Reset( self, reset ):
        self.Dict_Copy( sele_1_var, selection )
        self.update()
    def Channels_SELE_2_Reset( self, reset ):
        self.Dict_Copy( sele_2_var, selection )
        self.update()
    def Channels_SELE_3_Reset( self, reset ):
        self.Dict_Copy( sele_3_var, selection )
        self.update()
    def Channels_SELE_4_Reset( self, reset ):
        self.Dict_Copy( sele_4_var, selection )
        self.update()

    # Values 1
    def Channels_SELE_1_L0_Value( self, value ):
        sele_1_var["l0"] = value / 100
        self.update()
    def Channels_SELE_1_L1_Value( self, value ):
        sele_1_var["l1"] = value / 100
        self.update()
    def Channels_SELE_1_R1_Value( self, value ):
        sele_1_var["r1"] = value / 100
        self.update()
    def Channels_SELE_1_R0_Value( self, value ):
        sele_1_var["r0"] = value / 100
        self.update()
    # Values 2
    def Channels_SELE_2_L0_Value( self, value ):
        sele_2_var["l0"] = value / 100
        self.update()
    def Channels_SELE_2_L1_Value( self, value ):
        sele_2_var["l1"] = value / 100
        self.update()
    def Channels_SELE_2_R1_Value( self, value ):
        sele_2_var["r1"] = value / 100
        self.update()
    def Channels_SELE_2_R0_Value( self, value ):
        sele_2_var["r0"] = value / 100
        self.update()
    # Values 3
    def Channels_SELE_3_L0_Value( self, value ):
        sele_3_var["l0"] = value / 100
        self.update()
    def Channels_SELE_3_L1_Value( self, value ):
        sele_3_var["l1"] = value / 100
        self.update()
    def Channels_SELE_3_R1_Value( self, value ):
        sele_3_var["r1"] = value / 100
        self.update()
    def Channels_SELE_3_R0_Value( self, value ):
        sele_3_var["r0"] = value / 100
        self.update()
    # Values 4
    def Channels_SELE_4_L0_Value( self, value ):
        sele_4_var["l0"] = value / 100
        self.update()
    def Channels_SELE_4_L1_Value( self, value ):
        sele_4_var["l1"] = value / 100
        self.update()
    def Channels_SELE_4_R1_Value( self, value ):
        sele_4_var["r1"] = value / 100
        self.update()
    def Channels_SELE_4_R0_Value( self, value ):
        sele_4_var["r0"] = value / 100
        self.update()

    def Selection_APPLY( self ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            # Variables
            type_layer = ["paintlayer", "grouplayer", "clonelayer", "vectorlayer", "filterlayer", "filllayer", "filelayer"]

            # Document
            doc = self.Current_Document()
            d_cm = doc["d_cm"]
            d_cd = doc["d_cd"]
            ad = doc["ad"]
            d_nt = ad.activeNode().type()

            if d_nt in type_layer:
                # Place Text
                Krita.instance().activeWindow().activeView().showFloatingMessage( "Pigment.O Read | Source", Krita.instance().icon( "local-selection-active" ), 5000, 0 )
                Krita.instance().activeDocument().waitForDone()

                # Size
                width = ad.width()
                height = ad.height()

                # Depth Constants
                if d_cd == "U16":
                    depth = 65535
                elif d_cd == "F16":
                    depth = 65535
                elif d_cd == "F32":
                    depth = 4294836225
                else:
                    depth = 255
                k = 255

                # Source
                ss = ad.selection()
                if ss == None:
                    dx = 0
                    dy = 0
                    dw = width
                    dh = height
                else:
                    dx = ss.x()
                    dy = ss.y()
                    dw = ss.width()
                    dh = ss.height()

                # Color
                cor = self.convert.color_vector( self.sele_mode, self.cor )
                length = len( cor )
                if length == 1:
                    c0 = cor[0]
                if length == 3:
                    c0 = cor[0]
                    c1 = cor[1]
                    c2 = cor[2]
                if length == 4:
                    c0 = cor[0]
                    c1 = cor[1]
                    c2 = cor[2]
                    c3 = cor[3]

                # Pixel DAta
                byte_array = ad.pixelData( dx, dy, dw, dh )
                num_array = Bytes_to_Integer( self, byte_array, d_cd )

                # Calculation
                hue_rgb = [ "HSV", "HSL", "HSY", "ARD" ]
                hue_xyz = [ "LCH" ]
                index = 0
                sel_pixels = []
                for y in range( 0, dh ):
                    for x in range( 0, dw ):
                        # Read Bytes
                        num = Numbers_on_Pixel( self, d_cm, d_cd, index, num_array )

                        # Convert
                        if d_cm == "A":
                            conv = self.convert.color_convert( d_cm, self.sele_mode, [num[0]/depth] )
                        if ( d_cm == "RGB" or d_cm == None ):
                            conv = self.convert.color_convert( d_cm, self.sele_mode, [num[0]/depth, num[1]/depth, num[2]/depth] )
                        if d_cm == "CMYK":
                            conv = self.convert.color_convert( d_cm, self.sele_mode, [num[0]/depth, num[1]/depth, num[2]/depth, num[3]/depth] )

                        # Variables
                        if length == 1:
                            # Parse
                            n0 = conv[0]
                            # Variables
                            sel_0 = self.Selector_Linear( n0, c0, sele_1_var["l0"], sele_1_var["l1"], sele_1_var["r1"], sele_1_var["r0"] )
                            # Selection
                            sel_factor = sel_0
                        elif length == 3:
                            # Parse
                            n0 = conv[0]
                            n1 = conv[1]
                            n2 = conv[2]
                            # Variables
                            if self.sele_mode in hue_rgb: sel_0 = self.Selector_Circular( n0, c0, sele_1_var["l0"], sele_1_var["l1"], sele_1_var["r1"], sele_1_var["r0"] )
                            else:                         sel_0 = self.Selector_Linear( n0, c0, sele_1_var["l0"], sele_1_var["l1"], sele_1_var["r1"], sele_1_var["r0"] )
                            sel_1 = self.Selector_Linear( n1, c1, sele_2_var["l0"], sele_2_var["l1"], sele_2_var["r1"], sele_2_var["r0"] )
                            if self.sele_mode in hue_xyz: sel_2 = self.Selector_Circular( n2, c2, sele_3_var["l0"], sele_3_var["l1"], sele_3_var["r1"], sele_3_var["r0"] )
                            else:                         sel_2 = self.Selector_Linear( n2, c2, sele_3_var["l0"], sele_3_var["l1"], sele_3_var["r1"], sele_3_var["r0"] )
                            # Selection
                            sel_factor = sel_0 * sel_1 * sel_2
                            # sel_factor = ( sel_0 + sel_1 + sel_2 ) / 3
                        elif length == 4:
                            # Parse
                            n0 = conv[0]
                            n1 = conv[1]
                            n2 = conv[2]
                            n3 = conv[3]
                            # Variables
                            sel_0 = self.Selector_Linear( n0, c0, sele_1_var["l0"], sele_1_var["l1"], sele_1_var["r1"], sele_1_var["r0"] )
                            sel_1 = self.Selector_Linear( n1, c1, sele_2_var["l0"], sele_2_var["l1"], sele_2_var["r1"], sele_2_var["r0"] )
                            sel_2 = self.Selector_Linear( n2, c2, sele_3_var["l0"], sele_3_var["l1"], sele_3_var["r1"], sele_3_var["r0"] )
                            sel_3 = self.Selector_Linear( n3, c3, sele_4_var["l0"], sele_4_var["l1"], sele_4_var["r1"], sele_4_var["r0"] )
                            # Selection
                            sel_factor = sel_0 * sel_1 * sel_2 * sel_3

                        # Apply Selection
                        sel_pixels.append( int( sel_factor * k ) )
                        # Cycle
                        index += 1

                # Selection
                if len( sel_pixels ) > 0:
                    Insert_Selection( self, sel_pixels, dx, dy, dw, dh )
                else:
                    self.Warn_Message( f"Pigment.O ERROR | Model {d_cm} and/or Depth {d_cd} not supported" )
            else:
                self.Warn_Message( f"Pigment.O ERROR | Layer Type {d_nt} not supported" )
    def Selector_Circular( self, num, cor, l0, l1, r1, r0 ):
        # Distances
        cnl0 = cor - l0
        cnl1 = cor - l1
        cnr1 = cor + r1
        cnr0 = cor + r0
        cal0 = cnl0 - 1
        cal1 = cnl1 - 1
        car1 = cnr1 - 1
        car0 = cnr0 - 1
        cbl0 = cnl0 + 1
        cbl1 = cnl1 + 1
        cbr1 = cnr1 + 1
        cbr0 = cnr0 + 1

        # Intervals
        i1n = num >= cnl1 and num <= cnr1
        i1a = num >= cal1 and num <= car1
        i1b = num >= cbl1 and num <= cbr1
        i2n = num >= cnl0 and num < cnl1
        i2b = num >= cbl0 and num < cbl1
        i3n = num <= cnr0 and num > cnr1
        i3a = num <= car0 and num > car1

        # Logic
        if ( i1n == True or i1a == True or i1b == True ):
            select = 1
        elif ( i2n == True or i2b == True ):
            if i2n == True:
                dt = abs( cnl1 - cnl0 )
                db = abs( num - cnl0 )
            if i2b == True:
                dt = abs( cbl1 - cbl0 )
                db = abs( num - cbl0 )
            if dt == 0:
                select = 1
            elif db == 0:
                select = 0
            else:
                select = db / dt
        elif ( i3n == True or i3a == True ):
            if i3n == True:
                dt = abs( cnr1 - cnr0 )
                db = abs( num - cnr0 )
            if i3a == True:
                dt = abs( car1 - car0 )
                db = abs( num - car0 )
            if dt == 0:
                select = 1
            elif db == 0:
                select = 0
            else:
                select = db / dt
        else:
            select = 0

        # Return
        return select
    def Selector_Linear( self, num, cor, l0, l1, r1, r0 ):
        # Distances
        cnl0 = cor - l0
        cnl1 = cor - l1
        cnr1 = cor + r1
        cnr0 = cor + r0

        # Intervals
        i1 = num >= cnl1 and num <= cnr1
        ia = num >= cnl0 and num < cnl1
        ib = num <= cnr0 and num > cnr1
        # Logic
        if i1 == True:
            select = 1
        elif ia == True:
            dt = abs( cnl1 - cnl0 )
            da = abs( num - cnl0 )
            if da > 0:
                select = da / dt
            else:
                select = 0
        elif ib == True:
            dt = abs( cnr1 - cnr0 )
            db = abs( num - cnr0 )
            if db > 0:
                select = db / dt
            else:
                select = 0
        else:
            select = 0
        # Return
        return select

    #endregion
    #region HEX Codes ##############################################################

    # Copy-Paste
    def HEX_Copy( self ):
        hc = QApplication.clipboard()
        hc.clear()
        hc.setText( str( self.cor["hex6"] ) )
        self.Label_String( "HEX COPY" )
    def HEX_Paste( self ):
        array = [6, 7]
        hc = QApplication.clipboard()
        hex_code = hc.text()
        self.Color_HEX( hex_code )
        self.Label_String( "HEX PASTE" )

    # Operators
    def HEX_Valid( self, hex_code, length ):
        if ( hex_code == "" or hex_code == None ):
            return False
        else:
            # Variables
            valid = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"]
            
            # Checks
            checks = []
            if hex_code[0] == "#":
                hex_code = hex_code[1:]
                checks.append( True )
            if len( hex_code ) == length:
                for i in range( 0, len( hex_code ) ):
                    if hex_code[i] in valid:
                        checks.append( True )
                    else:
                        checks.append( False )
            else:
                checks.append( False )

            # Validity
            valid = True
            for i in range( 0, len( checks ) ):
                if checks[i] == False:
                    valid = False
                    break

            # Return
            return valid
    def HEX_Closest( self ):
        # Original HEX Point
        hex_start = self.cor["hex6"]
        ps = self.convert.hex6_to_rgb( hex_start )
        # Calculate Distances
        lista = list( color_names )
        index = [0,5]
        for i in range( len( lista ) ):
            pe = self.convert.hex6_to_rgb( lista[i] )
            d = self.geometry.Trig_3D_Points_Distance( ps[0], ps[1], ps[2], pe[0], pe[1], pe[2] )
            if d < index[1]:
                index = [i , d]
        # Final Color
        rgb = self.convert.hex6_to_rgb( lista[index[0]] )
        # Move Location to Closest Point
        self.Pigmento_APPLY( "RGB", rgb[0], rgb[1], rgb[2], 0, self.cor )

    #endregion
    #region Extension ##############################################################

    # COR
    def Extension_COR( self, SIGNAL_COLOR ):
        if SIGNAL_COLOR == 0:self.Pin_Apply_00( 0 )
        if SIGNAL_COLOR == 1:self.Pin_Apply_01( 0 )
        if SIGNAL_COLOR == 2:self.Pin_Apply_02( 0 )
        if SIGNAL_COLOR == 3:self.Pin_Apply_03( 0 )
        if SIGNAL_COLOR == 4:self.Pin_Apply_04( 0 )
        if SIGNAL_COLOR == 5:self.Pin_Apply_05( 0 )
        if SIGNAL_COLOR == 6:self.Pin_Apply_06( 0 )
        if SIGNAL_COLOR == 7:self.Pin_Apply_07( 0 )
        if SIGNAL_COLOR == 8:self.Pin_Apply_08( 0 )
        if SIGNAL_COLOR == 9:self.Pin_Apply_09( 0 )
        if SIGNAL_COLOR == 10:self.Pin_Apply_10( 0 )
    # KEYs
    def Extension_KEY_1( self, SIGNAL_KEY_1 ):
        self.Extension_KEY_Apply( self.key_1_chan, SIGNAL_KEY_1 * self.key_1_factor )
    def Extension_KEY_2( self, SIGNAL_KEY_2 ):
        self.Extension_KEY_Apply( self.key_2_chan, SIGNAL_KEY_2 * self.key_2_factor )
    def Extension_KEY_3( self, SIGNAL_KEY_3 ):
        self.Extension_KEY_Apply( self.key_3_chan, SIGNAL_KEY_3 * self.key_3_factor )
    def Extension_KEY_4( self, SIGNAL_KEY_4 ):
        self.Extension_KEY_Apply( self.key_4_chan, SIGNAL_KEY_4 * self.key_4_factor )
    def Extension_KEY_Apply( self, key, delta ):
        # AAA
        if key == "A 1":
            value = self.geometry.Limit_Float( self.cor["aaa_1"] + delta / krange["aaa_1"] )
            self.Pigmento_APPLY( "A", value, 0, 0, 0, self.cor )
        # RGB
        if key == "RGB 1":
            value = self.geometry.Limit_Float( self.cor["rgb_1"] + delta / krange["rgb_1"] )
            self.Pigmento_APPLY( "RGB", value, self.cor["rgb_2"], self.cor["rgb_3"], 0, self.cor )
        if key == "RGB 2":
            value = self.geometry.Limit_Float( self.cor["rgb_2"] + delta / krange["rgb_2"] )
            self.Pigmento_APPLY( "RGB", self.cor["rgb_1"], value, self.cor["rgb_3"], 0, self.cor )
        if key == "RGB 3":
            value = self.geometry.Limit_Float( self.cor["rgb_3"] + delta / krange["rgb_3"] )
            self.Pigmento_APPLY( "RGB", self.cor["rgb_1"], self.cor["rgb_2"], value, 0, self.cor )
        # CMY
        if key == "CMY 1":
            value = self.geometry.Limit_Float( self.cor["cmy_1"] + delta / krange["cmy_1"] )
            self.Pigmento_APPLY( "CMY", value, self.cor["cmy_2"], self.cor["cmy_3"], 0, self.cor )
        if key == "CMY 2":
            value = self.geometry.Limit_Float( self.cor["cmy_2"] + delta / krange["cmy_2"] )
            self.Pigmento_APPLY( "CMY", self.cor["cmy_1"], value, self.cor["cmy_3"], 0, self.cor )
        if key == "CMY 3":
            value = self.geometry.Limit_Float( self.cor["cmy_3"] + delta / krange["cmy_3"] )
            self.Pigmento_APPLY( "CMY", self.cor["cmy_1"], self.cor["cmy_2"], value, 0, self.cor )
        # CMYK
        if key == "CMYK 1":
            value = self.geometry.Limit_Float( self.cor["cmyk_1"] + delta / krange["cmyk_1"] )
            self.Pigmento_APPLY( "CMYK", value, self.cor["cmyk_2"], self.cor["cmyk_3"], self.cor["cmyk_4"], self.cor )
        if key == "CMYK 2":
            value = self.geometry.Limit_Float( self.cor["cmyk_2"] + delta / krange["cmyk_2"] )
            self.Pigmento_APPLY( "CMYK", self.cor["cmyk_1"], value, self.cor["cmyk_3"], self.cor["cmyk_4"], self.cor )
        if key == "CMYK 3":
            value = self.geometry.Limit_Float( self.cor["cmyk_3"] + delta / krange["cmyk_3"] )
            self.Pigmento_APPLY( "CMYK", self.cor["cmyk_1"], self.cor["cmyk_2"], value, self.cor["cmyk_4"], self.cor )
        if key == "CMYK 4":
            value = self.geometry.Limit_Float( self.cor["cmyk_4"] + delta / krange["cmyk_4"] )
            self.Pigmento_APPLY( "CMYK", self.cor["cmyk_1"], self.cor["cmyk_2"], self.cor["cmyk_3"], value, self.cor )
        # RYB
        if key == "RYB 1":
            value = self.geometry.Limit_Float( self.cor["ryb_1"] + delta / krange["ryb_1"] )
            self.Pigmento_APPLY( "RYB", value, self.cor["ryb_2"], self.cor["ryb_3"], 0, self.cor )
        if key == "RYB 2":
            value = self.geometry.Limit_Float( self.cor["ryb_2"] + delta / krange["ryb_2"] )
            self.Pigmento_APPLY( "RYB", self.cor["ryb_1"], value, self.cor["ryb_3"], 0, self.cor )
        if key == "RYB 3":
            value = self.geometry.Limit_Float( self.cor["ryb_3"] + delta / krange["ryb_3"] )
            self.Pigmento_APPLY( "RYB", self.cor["ryb_1"], self.cor["ryb_2"], value, 0, self.cor )
        # YUV
        if key == "YUV 1":
            value = self.geometry.Limit_Float( self.cor["yuv_1"] + delta / krange["yuv_1"] )
            self.Pigmento_APPLY( "YUV", value, self.cor["yuv_2"], self.cor["yuv_3"], 0, self.cor )
        if key == "YUV 2":
            value = self.geometry.Limit_Float( self.cor["yuv_2"] + delta / krange["yuv_2"] )
            self.Pigmento_APPLY( "YUV", self.cor["yuv_1"], value, self.cor["yuv_3"], 0, self.cor )
        if key == "YUV 3":
            value = self.geometry.Limit_Float( self.cor["yuv_3"] + delta / krange["yuv_3"] )
            self.Pigmento_APPLY( "YUV", self.cor["yuv_1"], self.cor["yuv_2"], value, 0, self.cor )

        # HSV
        if key == "HSV 1":
            value = self.geometry.Limit_Looper( self.cor["hsv_1"] + delta / krange["hsv_1"], 1 )
            self.Pigmento_APPLY( "HSV", value, self.cor["hsv_2"], self.cor["hsv_3"], 0, self.cor )
        if key == "HSV 2":
            value = self.geometry.Limit_Float( self.cor["hsv_2"] + delta / krange["hsv_2"] )
            self.Pigmento_APPLY( "HSV", self.cor["hsv_1"], value, self.cor["hsv_3"], 0, self.cor )
        if key == "HSV 3":
            value = self.geometry.Limit_Float( self.cor["hsv_3"] + delta / krange["hsv_3"] )
            self.Pigmento_APPLY( "HSV", self.cor["hsv_1"], self.cor["hsv_2"], value, 0, self.cor )
        # HSL
        if key == "HSL 1":
            value = self.geometry.Limit_Looper( self.cor["hsl_1"] + delta / krange["hsl_1"], 1 )
            self.Pigmento_APPLY( "HSL", value, self.cor["hsl_2"], self.cor["hsl_3"], 0, self.cor )
        if key == "HSL 2":
            value = self.geometry.Limit_Float( self.cor["hsl_2"] + delta / krange["hsl_2"] )
            self.Pigmento_APPLY( "HSL", self.cor["hsl_1"], value, self.cor["hsl_3"], 0, self.cor )
        if key == "HSL 3":
            value = self.geometry.Limit_Float( self.cor["hsl_3"] + delta / krange["hsl_3"] )
            self.Pigmento_APPLY( "HSL", self.cor["hsl_1"], self.cor["hsl_2"], value, 0, self.cor )
        # HSY
        if key == "HSY 1":
            value = self.geometry.Limit_Looper( self.cor["hsy_1"] + delta / krange["hsy_1"], 1 )
            self.Pigmento_APPLY( "HSY", value, self.cor["hsy_2"], self.cor["hsy_3"], 0, self.cor )
        if key == "HSY 2":
            value = self.geometry.Limit_Float( self.cor["hsy_2"] + delta / krange["hsy_2"] )
            self.Pigmento_APPLY( "HSY", self.cor["hsy_1"], value, self.cor["hsy_3"], 0, self.cor )
        if key == "HSY 3":
            value = self.geometry.Limit_Float( self.cor["hsy_3"] + delta / krange["hsy_3"] )
            self.Pigmento_APPLY( "HSY", self.cor["hsy_1"], self.cor["hsy_2"], value, 0, self.cor )
        # ARD
        if key == "ARD 1":
            value = self.geometry.Limit_Looper( self.cor["ard_1"] + delta / krange["ard_1"], 1 )
            self.Pigmento_APPLY( "ARD", value, self.cor["ard_2"], self.cor["ard_3"], 0, self.cor )
        if key == "ARD 2":
            value = self.geometry.Limit_Float( self.cor["ard_2"] + delta / krange["ard_2"] )
            self.Pigmento_APPLY( "ARD", self.cor["ard_1"], value, self.cor["ard_3"], 0, self.cor )
        if key == "ARD 3":
            value = self.geometry.Limit_Float( self.cor["ard_3"] + delta / krange["ard_3"] )
            self.Pigmento_APPLY( "ARD", self.cor["ard_1"], self.cor["ard_2"], value, 0, self.cor )

        # XYZ
        if key == "XYZ 1":
            value = self.geometry.Limit_Float( self.cor["xyz_1"] + delta / krange["xyz_1"] )
            self.Pigmento_APPLY( "XYZ", value, self.cor["xyz_2"], self.cor["xyz_3"], 0, self.cor )
        if key == "XYZ 2":
            value = self.geometry.Limit_Float( self.cor["xyz_2"] + delta / krange["xyz_2"] )
            self.Pigmento_APPLY( "XYZ", self.cor["xyz_1"], value, self.cor["xyz_3"], 0, self.cor )
        if key == "XYZ 3":
            value = self.geometry.Limit_Float( self.cor["xyz_3"] + delta / krange["xyz_3"] )
            self.Pigmento_APPLY( "XYZ", self.cor["xyz_1"], self.cor["xyz_2"], value, 0, self.cor )
        # XYY
        if key == "XYY 1":
            value = self.geometry.Limit_Float( self.cor["xyy_1"] + delta / krange["xyy_1"] )
            self.Pigmento_APPLY( "XYY", value, self.cor["xyy_2"], self.cor["xyy_3"], 0, self.cor )
        if key == "XYY 2":
            value = self.geometry.Limit_Float( self.cor["xyy_2"] + delta / krange["xyy_2"] )
            self.Pigmento_APPLY( "XYY", self.cor["xyy_1"], value, self.cor["xyy_3"], 0, self.cor )
        if key == "XYY 3":
            value = self.geometry.Limit_Float( self.cor["xyy_3"] + delta / krange["xyy_3"] )
            self.Pigmento_APPLY( "XYY", self.cor["xyy_1"], self.cor["xyy_2"], value, 0, self.cor )
        # LAB
        if key == "LAB 1":
            value = self.geometry.Limit_Float( self.cor["lab_1"] + delta / krange["lab_1"] )
            self.Pigmento_APPLY( "LAB", value, self.cor["lab_2"], self.cor["lab_3"], 0, self.cor )
        if key == "LAB 2":
            value = self.geometry.Limit_Float( self.cor["lab_2"] + delta / krange["lab_2"] )
            self.Pigmento_APPLY( "LAB", self.cor["lab_1"], value, self.cor["lab_3"], 0, self.cor )
        if key == "LAB 3":
            value = self.geometry.Limit_Float( self.cor["lab_3"] + delta / krange["lab_3"] )
            self.Pigmento_APPLY( "LAB", self.cor["lab_1"], self.cor["lab_2"], value, 0, self.cor )

        # LCH
        if key == "LCH 1":
            value = self.geometry.Limit_Float( self.cor["lch_1"] + delta / krange["lch_1"] )
            self.Pigmento_APPLY( "LCH", value, self.cor["lch_2"], self.cor["lch_3"], 0, self.cor )
        if key == "LCH 2":
            value = self.geometry.Limit_Float( self.cor["lch_2"] + delta / krange["lch_2"] )
            self.Pigmento_APPLY( "LCH", self.cor["lch_1"], value, self.cor["lch_3"], 0, self.cor )
        if key == "LCH 3":
            value = self.geometry.Limit_Float( self.cor["lch_3"] + delta / krange["lch_3"] )
            self.Pigmento_APPLY( "LCH", self.cor["lch_1"], self.cor["lch_2"], value, 0, self.cor )

        # KKK
        if key == "K 1":
            scale = int( self.geometry.Limit_Range( self.cor["kkk_scale"] + delta * 10, kkk_min_scale, kkk_max_scale ) )
            percent = self.convert.kkk_scale_to_percent( scale )
            self.Pigmento_APPLY( "KKK", percent, scale, 0, 0, self.cor )
    # LOCKs
    def Extension_LOCK( self, SIGNAL_LOCK ):
        if SIGNAL_LOCK == "CMYK":
            if self.layout.cmyk_4_label.isChecked():
                self.layout.cmyk_4_label.setChecked( False )
            else:
                self.layout.cmyk_4_label.setChecked( True )
        if SIGNAL_LOCK == "KKK":
            if self.layout.kkk_1_label.isChecked():
                self.layout.kkk_1_label.setChecked( False )
            else:
                self.layout.kkk_1_label.setChecked( True )

    #endregion
    #region Annotations ############################################################

    # Autosave
    def AutoSave_KRA( self, boolean ):
        self.annotation_kra = boolean
        Krita.instance().writeSetting( "Pigment.O", "annotation_kra", str( self.annotation_kra ) )
    def AutoSave_File( self, boolean ):
        self.annotation_file = boolean
        Krita.instance().writeSetting( "Pigment.O", "annotation_file", str( self.annotation_file ) )
    # LOAD
    def Annotation_KRA_Load( self ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            try:
                # Active Document
                self.doc = self.Current_Document()

                # Annotations
                annotation = self.doc["ad"].annotation( "Pigment.O" )
                an_string = str( annotation )
                an_replace = an_string[:-3].replace( "b\"", "" )
                an_split = an_replace.split( "\\n" )
                self.Variables_Load( an_split )
            except:
                pass
    def Annotation_FILE_Load( self ):
        file_dialog = QFileDialog( QWidget( self ) )
        file_dialog.setFileMode( QFileDialog.AnyFile )
        directory_path = file_dialog.getOpenFileName( self, "Select *.pigment_o.eo File", "", str( "*.pigment_o.eo" ) )
        directory_path = directory_path[0]
        if ( directory_path != "" and directory_path != "." ):
            # Read
            note = open( directory_path, "r" )
            data = note.readlines()
            self.Variables_Load( data )
    def Variables_Load( self, lista ):
        # lista = [str, str, str, ...]

        try:
            plugin = str( lista[0] ).replace( "\n", "", 1 )
            if plugin  == "pigment_o":
                # Read
                for i in range( 1, len( lista ) ):
                    lista_i = lista[i]
                    # Colors
                    if lista_i.startswith( "krange=" ) == True:
                        self.Dict_Copy( krange, eval( str( lista_i ).replace( "krange=", "", 1 ) ) )
                    if lista_i.startswith( "kac=" ) == True:
                        self.Dict_Copy( kac, eval( str( lista_i ).replace( "kac=", "", 1 ) ) )
                    if lista_i.startswith( "kbc=" ) == True:
                        self.Dict_Copy( kbc, eval( str( lista_i ).replace( "kbc=", "", 1 ) ) )
                    # Harmony
                    if lista_i.startswith( "har_01=" ) == True:
                        self.Dict_Copy( har_01, eval( str( lista_i ).replace( "har_01=", "", 1 ) ) )
                    if lista_i.startswith( "har_02=" ) == True:
                        self.Dict_Copy( har_02, eval( str( lista_i ).replace( "har_02=", "", 1 ) ) )
                    if lista_i.startswith( "har_03=" ) == True:
                        self.Dict_Copy( har_03, eval( str( lista_i ).replace( "har_03=", "", 1 ) ) )
                    if lista_i.startswith( "har_04=" ) == True:
                        self.Dict_Copy( har_04, eval( str( lista_i ).replace( "har_04=", "", 1 ) ) )
                    if lista_i.startswith( "har_05=" ) == True:
                        self.Dict_Copy( har_05, eval( str( lista_i ).replace( "har_05=", "", 1 ) ) )
                    # Pin
                    if lista_i.startswith( "pin_00=" ) == True:
                        self.Dict_Copy( pin_00, eval( str( lista_i ).replace( "pin_00=", "", 1 ) ) )
                    if lista_i.startswith( "pin_01=" ) == True:
                        self.Dict_Copy( pin_01, eval( str( lista_i ).replace( "pin_01=", "", 1 ) ) )
                    if lista_i.startswith( "pin_02=" ) == True:
                        self.Dict_Copy( pin_02, eval( str( lista_i ).replace( "pin_02=", "", 1 ) ) )
                    if lista_i.startswith( "pin_03=" ) == True:
                        self.Dict_Copy( pin_03, eval( str( lista_i ).replace( "pin_03=", "", 1 ) ) )
                    if lista_i.startswith( "pin_04=" ) == True:
                        self.Dict_Copy( pin_04, eval( str( lista_i ).replace( "pin_04=", "", 1 ) ) )
                    if lista_i.startswith( "pin_05=" ) == True:
                        self.Dict_Copy( pin_05, eval( str( lista_i ).replace( "pin_05=", "", 1 ) ) )
                    if lista_i.startswith( "pin_06=" ) == True:
                        self.Dict_Copy( pin_06, eval( str( lista_i ).replace( "pin_06=", "", 1 ) ) )
                    if lista_i.startswith( "pin_07=" ) == True:
                        self.Dict_Copy( pin_07, eval( str( lista_i ).replace( "pin_07=", "", 1 ) ) )
                    if lista_i.startswith( "pin_08=" ) == True:
                        self.Dict_Copy( pin_08, eval( str( lista_i ).replace( "pin_08=", "", 1 ) ) )
                    if lista_i.startswith( "pin_09=" ) == True:
                        self.Dict_Copy( pin_09, eval( str( lista_i ).replace( "pin_09=", "", 1 ) ) )
                    if lista_i.startswith( "pin_10=" ) == True:
                        self.Dict_Copy( pin_10, eval( str( lista_i ).replace( "pin_10=", "", 1 ) ) )
                # Write
                self.Pin_LOAD()
                self.Sync_Elements( True, True, True )
        except:
            pass
    # SAVE
    def Annotation_Save( self ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            try:
                # Document
                self.doc = self.Current_Document()

                # Data to be Saved
                data = ( 
                    # Plugin
                    f"pigment_o\n"+
                    # Colors
                    f"krange={ krange }\n"+
                    f"kac={ kac }\n"+
                    f"kbc={ kbc }\n"+
                    # Harmony
                    f"har_01={ har_01 }\n"+
                    f"har_02={ har_02 }\n"+
                    f"har_03={ har_03 }\n"+
                    f"har_04={ har_04 }\n"+
                    f"har_05={ har_05 }\n"+
                    # Pin
                    f"pin_00={ pin_00 }\n"+
                    f"pin_01={ pin_01 }\n"+
                    f"pin_02={ pin_02 }\n"+
                    f"pin_03={ pin_03 }\n"+
                    f"pin_04={ pin_04 }\n"+
                    f"pin_05={ pin_05 }\n"+
                    f"pin_06={ pin_06 }\n"+
                    f"pin_07={ pin_07 }\n"+
                    f"pin_08={ pin_08 }\n"+
                    f"pin_09={ pin_09 }\n"+
                    f"pin_10={ pin_10 }\n"+
                    # Other
                    ""
                    )

                # Save Method
                if self.doc["ad"] != None:
                    if self.annotation_kra == True:
                        # Save to active Document
                        self.doc["ad"].setAnnotation( "Pigment.O", "Document", QByteArray( data.encode() ) )
                    if self.annotation_file == True:
                        # Variables
                        file_path = self.doc["ad"].fileName()
                        base_name = os.path.basename( file_path )
                        extension = os.path.splitext( file_path )[1]
                        directory = file_path[:-len( base_name )]
                        name = base_name[:-len( extension )]
                        save_path = directory + name + ".pigment_o.eo"

                        # Save to TXT file
                        if ( file_path != "" and file_path != "." ):
                            with open( save_path, "w" ) as note:
                                note.write( data )
            except:
                pass

    #endregion
    #region Notifier ###############################################################

    def Application_Closing( self ):
        pass
    def Configuration_Changed( self ):
        pass
    def Image_Closed( self ):
        pass
    def Image_Created( self ):
        pass
    def Image_Saved( self ):
        pass
    def View_Closed( self ):
        pass
    def View_Created( self ):
        pass
    def Window_Created( self ):
        pass
    def Window_IsBeingCreated( self ):
        pass

    #endregion
    #region Window #################################################################

    def Window_Connect( self ):
        # Window
        self.window = Krita.instance().activeWindow()
        if self.window != None:
            self.window.activeViewChanged.connect( self.View_Changed )
            self.window.themeChanged.connect( self.Theme_Changed )
            self.window.windowClosed.connect( self.Window_Closed )

    def View_Changed( self ):
        pass
    def Theme_Changed( self ):
        # Krita Theme
        theme_value = QApplication.palette().color( QPalette.Window ).value()
        # Calculations
        rgb = self.convert.hsv_to_rgb( 0, 0, theme_value )
        hex6 = self.convert.rgb_to_hex6( rgb[0], rgb[1], rgb[2] )
        # Update Pigmento
        self.panel_huecircle.Set_Theme( hex6 )
        self.panel_gamut.Set_Theme( hex6 )
    def Window_Closed( self ):
        pass

    #endregion
    #region Widget Events ##########################################################

    def showEvent( self, event ):
        # UI
        self.Update_Size()
        # Window
        self.Window_Connect()
        # QTimer
        if check_timer >= 30:
            self.timer_pulse.start( check_timer )
    def resizeEvent( self, event ):
        # self.Resize_Print( event )
        self.Update_Size()
    def enterEvent( self, event ):
        # Variables
        self.inbound = True
        # Check Krita/Clipboard Once before editing Pigmento
        if self.hex_copy_paste == True:
            self.HEX_Paste()
        if ( self.hex_copy_paste == False and self.mode_index == 0 ):
            self.Pigmento_RELEASE()
    def leaveEvent( self, event ):
        # Variables
        self.inbound = False
        # Widgets
        self.Pigmento_RELEASE()
        self.Clear_Focus()
        # Hex Copy
        if self.hex_copy_paste == True:
            self.HEX_Copy()
        # Save
        self.Annotation_Save()
        self.Mask_Write()
    def closeEvent( self, event ):
        # QTimer
        self.timer_pulse.stop()
        # Save
        self.Annotation_Save()

    def eventFilter( self, source, event ):
        # Panels
        panels = [
            self.layout.panel_set,
            self.layout.edit_dot,
            self.layout.edit_mask,

            self.layout.aaa_slider,
            self.layout.rgb_slider,
            self.layout.cmy_slider,
            self.layout.cmyk_slider,
            self.layout.ryb_slider,
            self.layout.yuv_slider,
            self.layout.hsv_slider,
            self.layout.hsl_slider,
            self.layout.hsy_slider,
            self.layout.ard_slider,
            self.layout.xyz_slider,
            self.layout.xyy_slider,
            self.layout.lab_slider,
            self.layout.lch_slider,
            self.layout.kkk_slider,

            self.layout.mixer_set,
            ]
        if ( event.type() == QEvent.Resize and source in panels ):
            self.Update_Size()
            return True

        # History
        if ( event.type() == QEvent.ContextMenu and source is self.layout.history_list ):
            self.Menu_Context_History( event )
            return True

        # Mode
        if ( event.type() == QEvent.MouseButtonPress and source is self.layout.mode ):
            self.Menu_Mode_Press( event )
            return True
        if ( event.type() == QEvent.Wheel and source is self.layout.mode ):
            self.Menu_Mode_Wheel( event )
            return True



        return super().eventFilter( source, event )

    #endregion
    #region Canvas #################################################################

    def canvasChanged( self, canvas ):
        pass

    #endregion
    #region Notes ##################################################################

    """
    # Label Message
    self.layout.label.setText( "message" )

    # Pop Up Message
    QMessageBox.information( QWidget(), i18n( "Warnning" ), i18n( "message" ) )

    # Log Viewer Message
    QtCore.qDebug( f"value = { value }" )
    QtCore.qDebug( "message" )
    QtCore.qWarning( "message" )
    QtCore.qCritical( "message" )

    # qimage = QImage( byte_array, width, height, QImage.Format_RGBA8888 )

    # convert QPixmap to bytes
    ba = QtCore.QByteArray()
    buff = QtCore.QBuffer(ba)
    buff.open(QtCore.QIODevice.WriteOnly) 
    ok = pixmap.save(buff, "PNG")
    assert ok
    pixmap_bytes = ba.data()
    print(type(pixmap_bytes))

    # convert bytes to QPixmap
    ba = QtCore.QByteArray(pixmap_bytes)
    pixmap = QtGui.QPixmap()
    ok = pixmap.loadFromData(ba, "PNG")
    assert ok
    print(type(pixmap))
    """

    #endregion


class PigmentS_Docker( DockWidget ):
    """
    Color Samples
    """

    #region Initialize #############################################################

    def __init__( self ):
        super( PigmentS_Docker, self ).__init__()
        # Construct
        self.Variables()
        self.User_Interface()
        self.Connections()
        self.Modules()
        self.Style()
        self.Settings()
        self.Loader()

    def Variables( self ):
        # Sample
        self.sample_mode = "RGB"
        self.sample_limit = 300
        self.sample_index = None
        self.sample_data = []

        # Samples
        self.invert_cmyk = False

        # Profile File
        self.profile_file = None
        self.black_point_file = None
        self.white_point_file = None
        # Profile Krita
        self.profile_krita = None
        self.black_point_krita = None
        self.white_point_krita = None

        # Colors
        self.color_alpha = QColor( 0, 0, 0, 0 )
    def User_Interface( self ):
        # Window
        self.setWindowTitle( DOCKER_NAME_2 )

        # Operating System
        self.OS = str( QSysInfo.kernelType() ) # WINDOWS=winnt & LINUX=linux

        # Path Name
        self.directory_plugin = str( os.path.dirname( os.path.realpath( __file__ ) ) )

        # Widget Docker
        self.layout = uic.loadUi( os.path.join( self.directory_plugin, "pigment_s_docker.ui" ), QWidget( self ) )
        self.setWidget( self.layout )
    def Connections( self ):
        # Lists
        self.layout.sample_list.itemClicked.connect( self.Sample_Display )
        self.layout.sample_list.itemDoubleClicked.connect( self.Sample_Insert )
        self.layout.split_sample.splitterMoved.connect( self.Update_Size )

        # Buttons
        self.layout.sample_mode.currentTextChanged.connect( self.Sample_Mode )
        self.layout.sample_generate.clicked.connect( self.Sample_Generate )
        self.layout.sample_slider.valueChanged.connect( self.Sample_Slider )
        self.layout.sample_value.valueChanged.connect( self.Sample_Value )

        # Profile
        # self.layout.profile_file.clicked.connect( self.Profile_File )
        # self.layout.profile_krita.clicked.connect( self.Profile_Krita )
        # self.layout.profile_tint.clicked.connect( self.Profile_Tint )
    def Modules( self ):
        #region Geometry

        self.geometry = Geometry()

        #endregion
        #region Conversions

        self.convert = Convert()
        self.convert.Set_Document( "RGB", "U8", "sRGB-elle-V2-srgtrc.icc" )
        self.convert.Set_Hue( zero )
        self.convert.Set_Luminosity( "ITU-R BT.709" )
        self.convert.Set_Gamma( gamma_y, gamma_l )
        self.convert.Set_Matrix( "sRGB", "D65" )

        #endregion
        #region Notifier

        self.notifier = Krita.instance().notifier()
        self.notifier.applicationClosing.connect( self.Application_Closing )
        self.notifier.configurationChanged.connect( self.Configuration_Changed )
        self.notifier.imageClosed.connect( self.Image_Closed )
        self.notifier.imageCreated.connect( self.Image_Created )
        self.notifier.imageSaved.connect( self.Image_Saved )
        self.notifier.viewClosed.connect( self.View_Closed )
        self.notifier.viewCreated.connect( self.View_Created )
        self.notifier.windowCreated.connect( self.Window_Created )
        self.notifier.windowIsBeingCreated.connect( self.Window_IsBeingCreated )

        #endregion
        #region Sample

        self.sample_display = Sample_Map( self.layout.sample_display )
        self.sample_display.SIGNAL_INDEX.connect( self.Sample_Insert )

        #endregion
    def Style( self ):
        # Icon
        qicon_gen = Krita.instance().icon( "all-layers" )
        # Widgets
        self.layout.sample_generate.setIcon( qicon_gen )
        # Style Sheet
        self.layout.progress_bar.setStyleSheet( "#progress_bar{background-color: rgba( 0, 0, 0, 50 );}" )
    def Settings( self ):
        # Settings
        self.sample_mode = self.Set_Read( "STR", "sample_mode", self.sample_mode )
        self.sample_limit = self.Set_Read( "INT", "sample_limit", self.sample_limit )
    def Loader( self ):
        self.Sample_Block( True )
        self.layout.sample_mode.setCurrentText( self.sample_mode )
        self.layout.sample_slider.setValue( self.sample_limit )
        self.layout.sample_value.setValue( self.sample_limit )
        self.Sample_Block( False )

    def Set_Read( self, mode, entry, default ):
        setting = Krita.instance().readSetting( "Pigment.O", entry, "" )
        if setting == "":
            read = default
            Krita.instance().writeSetting( "Pigment.O", entry, str( default ) )
        else:
            read = setting
            if mode == "EVAL":
                read = eval( read )
            elif mode == "STR":
                read = str( read )
            elif mode == "INT":
                read = int( read )
        return read

    #endregion
    #region Menu ###################################################################

    def Sample_Mode( self, sample_mode ):
        self.sample_mode = sample_mode
        Krita.instance().writeSetting( "Pigment.O", "sample_mode", str( self.sample_mode ) )
    def Sample_Limit( self, sample_limit ):
        self.sample_limit = sample_limit
        Krita.instance().writeSetting( "Pigment.O", "sample_limit", str( self.sample_limit ) )

    #endregion
    #region Management #############################################################

    def Update_Size( self ):
        self.sample_display.Set_Size( self.layout.sample_display.width(), self.layout.sample_display.height() )
        self.update()
    def Sample_Block( self, boolean ):
        self.layout.sample_mode.blockSignals( boolean )
        self.layout.sample_slider.blockSignals( boolean )
        self.layout.sample_value.blockSignals( boolean )
    def Clear_Focus( self ):
        self.layout.sample_slider.clearFocus()
        self.layout.sample_value.clearFocus()

    def Text_Index( self, mode ):
        # Variables
        chan_0 = ""
        chan_1 = ""
        chan_2 = ""
        chan_3 = ""

        # Parsing
        if mode == "A":
            chan_0 = "Gray"
        if mode == "RGB":
            chan_0 = "Red"
            chan_1 = "Green"
            chan_2 = "Blue"
        if mode == "CMY":
            chan_0 = "Cyan"
            chan_1 = "Magenta"
            chan_2 = "Yellow"
        if mode == "CMYK":
            chan_0 = "Cyan"
            chan_1 = "Magenta"
            chan_2 = "Yellow"
            chan_3 = "Key"
        if mode == "RYB":
            chan_0 = "Red"
            chan_1 = "Yellow"
            chan_2 = "Blue"
        if mode == "YUV":
            chan_0 = "Luma"
            chan_1 = "Comp Blue"
            chan_2 = "Comp Red"
        if mode == "HSV":
            chan_0 = "Hue"
            chan_1 = "Saturation"
            chan_2 = "Value"
        if mode == "HSL":
            chan_0 = "Hue"
            chan_1 = "Saturation"
            chan_2 = "Lightness"
        if mode == "HSY":
            chan_0 = "Hue"
            chan_1 = "Saturation"
            chan_2 = "Luma"
        if mode == "ARD":
            chan_0 = "Angle"
            chan_1 = "Ratio"
            chan_2 = "Depth"
        if mode == "XYZ":
            chan_0 = "XYZ X"
            chan_1 = "XYZ Y"
            chan_2 = "XYZ Z"
        if mode == "XYY":
            chan_0 = "xyY x"
            chan_1 = "xyY y"
            chan_2 = "xyY Y"
        if mode == "LAB":
            chan_0 = "LAB L*"
            chan_1 = "LAB A*"
            chan_2 = "LAB B*"
        if mode == "LCH":
            chan_0 = "Luminosity"
            chan_1 = "Chroma"
            chan_2 = "Hue"

        # Return
        return chan_0, chan_1, chan_2, chan_3

    #endregion
    #region Slider #################################################################

    def Sample_Slider( self, value ):
        # Widgets
        self.Sample_Block( True )
        self.layout.sample_value.setValue( value )
        self.Sample_Block( False )
        # Variables
        self.Sample_Limit( value )
    def Sample_Value( self, value ):
        # Widgets
        self.Sample_Block( True )
        self.layout.sample_slider.setValue( value )
        self.Sample_Block( False )
        # Variables
        self.Sample_Limit( value )

    #endregion
    #region Samples ################################################################

    def Sample_Generate( self ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            # Instance
            ad = Krita.instance().activeDocument()
            # document color
            d_cm = ad.colorModel()
            d_cd = ad.colorDepth()
            # Color Model
            if ( d_cm == "A" or d_cm == "GRAYA" ):
                d_cm = "A"
            elif ( d_cm == "RGBA" or d_cm == None ):
                d_cm = "RGB"
            elif d_cm == "CMYKA":
                d_cm = "CMYK"
            elif d_cm == "YCbCr":
                d_cm = "YUV"
            elif d_cm == "XYZA":
                d_cm = "XYZ"
            elif d_cm == "LABA":
                d_cm = "LAB"
            # Depth Constants
            if d_cd == "U16":
                depth = 65535
            elif d_cd == "F16":
                depth = 65535
            elif d_cd == "F32":
                depth = 4294836225
            else:
                depth = 255
            k = 255

            # Variables
            index = 0
            c0 = 0.75
            c1 = 0.25
            c2 = 0.25
            cor = False
            hue_rgb = [ "HSV", "HSL", "HSY", "ARD" ]
            hue_xyz = [ "LCH" ]

            # Document
            width = ad.width()
            height = ad.height()

            # Channels
            if self.sample_mode == "A":
                channels = 1
                extra = 2
            elif self.sample_mode == "CMYK":
                channels = 4
                extra = 2
            elif self.sample_mode in hue_rgb:
                channels = 3
                extra = 1
            else:
                channels = 3
                extra = 2
            # Item Selection
            try:
                previous = self.geometry.Limit_Range( self.layout.sample_list.currentRow(), 0, channels + extra - 1 )
            except:
                previous = 0
            # Channel names
            chan_0, chan_1, chan_2, chan_3 = self.Text_Index( self.sample_mode )

            # Source
            ss = ad.selection()
            if ss == None:
                dx = 0
                dy = 0
                dw = width
                dh = height
            else:
                dx = ss.x()
                dy = ss.y()
                dw = ss.width()
                dh = ss.height()

            # Bytes Selection
            byte_array = ad.pixelData( dx, dy, dw, dh )

            # Convert to Number List
            num_array = Bytes_to_Integer( self, byte_array, d_cd )

            # Progress bar
            self.layout.progress_bar.setMaximum( height )
            self.layout.progress_bar.setValue( 0 )

            # Lists
            byte_0_r = []
            byte_1_r = []
            byte_2_r = []
            byte_3_r = []
            byte_t_r = []
            byte_a_r = []

            byte_0_m = []
            byte_1_m = []
            byte_2_m = []
            byte_3_m = []
            byte_t_m = []
            byte_a_m = []

            # Document
            for y in range( 0, dh ):
                if ( ( y + 1 ) % 5 ) == 0:self.layout.progress_bar.setValue( y + 1 )
                QApplication.processEvents()
                for x in range( 0, dw ):
                    # Read Byte
                    num = Numbers_on_Pixel( self, d_cm, d_cd, index, num_array )

                    # Convert
                    if d_cm == "A":
                        # Variables
                        n0 = num[0] / depth
                        na = num[1] / depth
                        # Convert
                        conv = self.convert.color_convert( d_cm, self.sample_mode, [ n0 ] )
                        # Variables
                        cmyk = self.convert.rgb_to_cmyk( n0, n0, n0, None )
                        bw = 1 - cmyk[3]
                    elif ( d_cm == "RGB" or d_cm == None ):
                        # Variables
                        n0 = num[0] / depth
                        n1 = num[1] / depth
                        n2 = num[2] / depth
                        na = num[3] / depth
                        # Convert
                        conv = self.convert.color_convert( d_cm, self.sample_mode, [ n0, n1, n2 ] )
                        # Variables
                        cmyk = self.convert.rgb_to_cmyk( n0, n1, n2, None )
                        bw = 1 - cmyk[3]
                    elif d_cm == "CMYK":
                        # Variables
                        n0 = num[0] / depth
                        n1 = num[1] / depth
                        n2 = num[2] / depth
                        n3 = num[3] / depth
                        na = num[4] / depth
                        # Convert
                        conv = self.convert.color_convert( d_cm, self.sample_mode, [ n0, n1, n2, n3 ] )
                        # Variables
                        cmyk = [ n0, n1, n2, n3 ]
                        bw = 1 - n3

                    # Length
                    length = len( conv )

                    # Channels
                    if length == 1:
                        s0 = int( self.geometry.Limit_Float( conv[0] ) * k )
                    elif length == 3:
                        if self.sample_mode in hue_rgb:
                            hrgb = self.convert.hue_to_rgb( conv[0] )
                            hue0 = int( hrgb[0] * k )
                            hue1 = int( hrgb[1] * k )
                            hue2 = int( hrgb[2] * k )
                        if self.sample_mode in hue_xyz:
                            rgb = self.convert.lch_to_rgb( conv[0], conv[1], conv[2] )
                            h = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
                            hrgb = self.convert.hsv_to_rgb( h, 1, 1 )
                            hue0 = int( hrgb[0] * k )
                            hue1 = int( hrgb[1] * k )
                            hue2 = int( hrgb[2] * k )
                        s0 = int( self.geometry.Limit_Float( conv[0] ) * k )
                        s1 = int( self.geometry.Limit_Float( conv[1] ) * k )
                        s2 = int( self.geometry.Limit_Float( conv[2] ) * k )
                    elif length == 4:
                        if self.invert_cmyk == True:
                            s0 = int( self.geometry.Limit_Float( 1 - conv[0] ) * k )
                            s1 = int( self.geometry.Limit_Float( 1 - conv[1] ) * k )
                            s2 = int( self.geometry.Limit_Float( 1 - conv[2] ) * k )
                            s3 = int( self.geometry.Limit_Float( 1 - conv[3] ) * k )
                        else:
                            s0 = int( self.geometry.Limit_Float( conv[0] ) * k )
                            s1 = int( self.geometry.Limit_Float( conv[1] ) * k )
                            s2 = int( self.geometry.Limit_Float( conv[2] ) * k )
                            s3 = int( self.geometry.Limit_Float( conv[3] ) * k )
                    # Total Ink Cove_rage
                    if self.sample_mode not in hue_rgb:
                        tic = self.convert.cmyk_to_tic( cmyk[0], cmyk[1], cmyk[2], cmyk[3] )
                        t0, t1, t2, tw, cor = self.Total_Ink_Coverage( tic, self.sample_limit, c0, c1, c2, bw, cor )
                        t0 = int( t0 * k )
                        t1 = int( t1 * k )
                        t2 = int( t2 * k )
                        tw = int( tw * k )
                    # Alpha
                    na = int( na * k )

                    # Images
                    if length == 1:
                        byte_0_r.extend( [ s0, s0, s0, na ] )
                    elif length == 3:
                        if self.sample_mode in hue_rgb:
                            byte_0_r.extend( [ hue0, hue1, hue2, na ] )
                        else:
                            byte_0_r.extend( [ s0, s0, s0, na ] )
                        byte_1_r.extend( [ s1, s1, s1, na ] )
                        if self.sample_mode in hue_xyz:
                            byte_2_r.extend( [ hue0, hue1, hue2, na ] )
                        else:
                            byte_2_r.extend( [ s2, s2, s2, na ] )
                    elif length == 4:
                        byte_0_r.extend( [ s0, s0, s0, na ] )
                        byte_1_r.extend( [ s1, s1, s1, na ] )
                        byte_2_r.extend( [ s2, s2, s2, na ] )
                        byte_3_r.extend( [ s3, s3, s3, na ] )
                    if self.sample_mode not in hue_rgb:
                        byte_t_r.extend( [ t0, t1, t2, na ] )
                    byte_a_r.extend( [ na, na, na, k ] )

                    # Maps
                    if length == 1:
                        byte_0_m.append( s0 )
                    elif length == 3:
                        byte_0_m.append( s0 )
                        byte_1_m.append( s1 )
                        byte_2_m.append( s2 )
                    elif length == 4:
                        byte_0_m.append( s0 )
                        byte_1_m.append( s1 )
                        byte_2_m.append( s2 )
                        byte_3_m.append( s3 )
                    if self.sample_mode not in hue_rgb:
                        byte_t_m.append( tw )
                    byte_a_m.append( na )

                    # Cycle
                    index += 1

            # Check
            if len( byte_0_m ) > 0:
                # Render
                self.sample_data = []
                if length >= 1:
                    self.sample_data.append( { "index" : 0, "render" : byte_0_r, "map" : byte_0_m, "dx" : dx, "dy" : dy, "dw" : dw, "dh" : dh, "text" : chan_0, "cor" : False } )
                if length >= 3:
                    self.sample_data.append( { "index" : 1, "render" : byte_1_r, "map" : byte_1_m, "dx" : dx, "dy" : dy, "dw" : dw, "dh" : dh, "text" : chan_1, "cor" : False } )
                    self.sample_data.append( { "index" : 2, "render" : byte_2_r, "map" : byte_2_m, "dx" : dx, "dy" : dy, "dw" : dw, "dh" : dh, "text" : chan_2, "cor" : False } )
                if length == 4:
                    self.sample_data.append( { "index" : 3, "render" : byte_3_r, "map" : byte_3_m, "dx" : dx, "dy" : dy, "dw" : dw, "dh" : dh, "text" : chan_3, "cor" : False } )
                if self.sample_mode not in hue_rgb:
                    self.sample_data.append( { "index" : "TIC", "render" : byte_t_r, "map" : byte_t_m, "dx" : dx, "dy" : dy, "dw" : dw, "dh" : dh, "text" : "TIC", "cor" : cor } )
                self.sample_data.append( { "index" : "Alpha", "render" : byte_a_r, "map" : byte_a_m, "dx" : dx, "dy" : dy, "dw" : dw, "dh" : dh, "text" : "Alpha", "cor" : False } )

                # Select Previous
                item = self.sample_data[previous]
                qimage = QImage( bytes( item["render"] ), dw, dh, QImage.Format_RGBA8888 )
                qpixmap = QPixmap().fromImage( qimage )
                self.sample_display.Set_Sample( item["index"], qpixmap, item["cor"] )

                # Create List
                self.layout.sample_list.clear()
                for i in range( 0, len( self.sample_data ) ):
                    # item
                    item = QListWidgetItem()
                    size = 100
                    # Thumbnail
                    bg = QPixmap( size, size )
                    bg.fill( self.color_alpha )
                    sd = self.sample_data[i]
                    img = QImage( bytes( sd["render"] ), sd["dw"], sd["dh"], QImage.Format_RGBA8888 )
                    pix = QPixmap().fromImage( img )
                    pix = pix.scaled( size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation )
                    # Variables
                    w = pix.width()
                    h = pix.height()
                    px = int( ( size * 0.5 ) - ( w * 0.5 ) )
                    py = int( ( size * 0.5 ) - ( h * 0.5 ) )
                    # Composed Image
                    painter = QPainter( bg )
                    painter.drawPixmap( px, py, pix )
                    painter.end()
                    # Item
                    qicon = QIcon( bg )
                    item.setIcon( qicon )
                    item.setToolTip( self.sample_data[i]["text"] )
                    self.layout.sample_list.addItem( item )
                self.layout.sample_list.setCurrentRow( previous )
            else:
                self.Sample_Clean()
                self.Warn_Message( f"Pigment.O ERROR | Model {d_cm} and/or Depth {d_cd} not supported" )

            # Progress bar
            self.layout.progress_bar.setMaximum( 1 )
            self.layout.progress_bar.setValue( 0 )
    def Total_Ink_Coverage( self, tic, limit, c0, c1, c2, bw, cor ):
        if tic > limit:
            value = ( tic - limit ) / ( 400 - limit )
            cor = True
            t0 = c0
            t1 = c1
            t2 = c2
            tw = value
        else:
            t0 = bw
            t1 = bw
            t2 = bw
            tw = 0
        return t0, t1, t2, tw, cor

    def Sample_Display( self ):
        # Variables
        index = self.layout.sample_list.currentRow()
        item = self.sample_data[index]
        # Render
        qimage = QImage( bytes( item["render"] ), item["dw"], item["dh"], QImage.Format_RGBA8888 )
        qpixmap = QPixmap().fromImage( qimage )
        self.sample_display.Set_Sample( index, qpixmap, item["cor"] )
    def Sample_Insert( self, index ):
        # Variables
        index = self.layout.sample_list.currentRow()
        item = self.sample_data[index]
        # Selection
        Insert_Selection( self, item["map"], item["dx"], item["dy"], item["dw"], item["dh"] )
    def Sample_Clean( self ):
        self.sample_data = []
        self.layout.sample_list.clear()
        self.sample_display.Set_Sample( None, None, False )
        self.update()

    #endregion
    #region Profiles ###############################################################

    def Profile_Run( self ):
        try:
            self.Profile_File()
            self.Profile_Krita()
            self.Profile_Tint()
        except:
            pass

    def Profile_File( self ):
        # Path
        path_source = "C:\\Users\\EyeOd\\Desktop\\SOURCE\\s.jpg"
        path_destination = "C:\\Users\\EyeOd\\Desktop\\SOURCE\\destination.jpg"

        # Drive
        qimage = QImage( path_source )
        depth = 255

        if qimage.isNull() == False:
            self.profile_file, self.black_point_file, self.white_point_file = self.Profile_Generate( qimage, depth )
            for i in range( 0, len( self.profile_file ) ):
                QtCore.qDebug( f"source {i} = { self.profile_file[i] }" )
    def Profile_Krita( self ):
        # Krita Document
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            # Instance
            ad = Krita.instance().activeDocument()
            # document color
            d_cm = ad.colorModel()
            d_cd = ad.colorDepth()
            # Depth Constants
            if d_cd == "U16":
                depth = 65535
            elif d_cd == "F16":
                depth = 65535
            elif d_cd == "F32":
                depth = 4294836225
            else:
                depth = 256
            # QImage
            qimage = ad.thumbnail( ad.width(), ad.height() )
            if qimage.isNull() == False:
                self.profile_krita, self.black_point_krita, self.white_point_krita = self.Profile_Generate( qimage, depth )
                for i in range( 0, len( self.profile_krita ) ):
                    QtCore.qDebug( f"destination {i} = { self.profile_krita[i] }" )
    def Profile_Tint( self ):
        if ( self.profile_file != None and self.profile_krita != None ):
            if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
                # Instance
                ad = Krita.instance().activeDocument()
                width = ad.width()
                height = ad.height()
                # document color
                d_cm = ad.colorModel()
                d_cd = ad.colorDepth()
                # Depth Constants
                if d_cd == "U16":
                    depth = 65535
                elif d_cd == "F16":
                    depth = 65535
                elif d_cd == "F32":
                    depth = 4294836225
                else:
                    depth = 256
                k = 255

                # QImage
                qimage = ad.thumbnail( width, height )
                if qimage.isNull() == False:
                    # Progress bar
                    self.layout.progress_bar.setMaximum( height )
                    self.layout.progress_bar.setValue( 0 )

                    # Pixels
                    percent = []
                    num_array = []
                    for h in range( 0, height ):
                        if ( ( h + 1 ) % 5 ) == 0:self.layout.progress_bar.setValue( h + 1 )
                        QApplication.processEvents()
                        for w in range( 0, width ):
                            # RGB
                            pixel = qimage.pixelColor( w, h )
                            r = pixel.redF()
                            g = pixel.greenF()
                            b = pixel.blueF()
                            alpha = pixel.alphaF()
                            # UVD
                            uvd = self.convert.rgb_to_uvd( r, g, b )
                            u = uvd[0]
                            v = uvd[1]
                            d = uvd[2]
                            # ARD
                            # ard = self.convert.rgb_to_ard( r, g, b )
                            # a = ard[0]
                            # r = ard[1]
                            # d = ard[2]
                            # depth
                            d_depth = int( d * k )

                            # Profile
                            krita_lim = self.profile_krita[d_depth]
                            min_ku = krita_lim[0]
                            max_ku = krita_lim[1]
                            min_kv = krita_lim[2]
                            max_kv = krita_lim[3]
                            # Percent
                            du = max_ku - min_ku
                            dv = max_kv - min_kv
                            if du == 0: pu = 0 
                            else:       pu = ( u - min_ku ) / ( du )
                            if dv == 0: pv = 0
                            else:       pv = ( v - min_kv ) / ( dv )
                            percent.append( [ pu, pv, d ] )

                            # Depth Point
                            per_d = ( d_depth - self.black_point_krita ) / ( self.white_point_krita - self.black_point_krita )
                            lerp = self.geometry.Lerp_1D( per_d, self.black_point_file, self.white_point_file )
                            new_d = int( self.geometry.Limit_Range( lerp, 0, k ) )

                            # File
                            file_lim = self.profile_file[ d_depth ]
                            # file_lim = self.profile_file[ new_d ]
                            min_fu = file_lim[0]
                            max_fu = file_lim[1]
                            min_fv = file_lim[2]
                            max_fv = file_lim[3]
                            new_u = self.geometry.Lerp_1D( pu, min_fu, max_fu )
                            new_v = self.geometry.Lerp_1D( pv, min_fv, max_fv )

                            new_rgb = self.convert.uvd_to_rgb( new_u, new_v, d )
                            # uvd_rgb = self.convert.uvd_to_rgb( new_u, new_v, d )
                            # angle = self.convert.rgb_to_hue( uvd_rgb[0], uvd_rgb[1], uvd_rgb[2] )
                            # new_rgb = self.convert.ard_to_rgb( angle, r, d )

                            r = int( self.geometry.Limit_Float( new_rgb[0] ) * k )
                            g = int( self.geometry.Limit_Float( new_rgb[1] ) * k )
                            b = int( self.geometry.Limit_Float( new_rgb[2] ) * k )
                            a = int( alpha * k )

                            # Number Array
                            num_array.extend( [ b, g, r, a ] )

                    # Byte Conversion
                    byte_array = Integer_to_Bytes( self, num_array, d_cd )

                    # Node
                    self.Wait( ad )
                    # New Node
                    node = ad.activeNode()
                    name = "Pigment.S Tint"
                    new_node = ad.createNode( name, "paintLayer" )
                    ad.activeNode().parentNode().addChildNode( new_node, node )
                    ad.setActiveNode( new_node )
                    self.Wait( ad )
                    # Paste
                    px = 0
                    py = 0
                    pw = width
                    ph = height
                    new_node.setPixelData( byte_array, px, py, pw, ph )
                    self.Wait( ad )

                    # Progress bar
                    self.layout.progress_bar.setMaximum( 1 )
                    self.layout.progress_bar.setValue( 0 )

    def Profile_Generate( self, qimage, depth ):
        # QImage
        size = 100
        # Image
        img_scale = qimage.scaled( size, size, Qt.KeepAspectRatio, Qt.FastTransformation ) #Qt.SmoothTransformation
        img_width = img_scale.width()
        img_height = img_scale.height()

        # Progress bar
        self.layout.progress_bar.setMaximum( img_height )
        self.layout.progress_bar.setValue( 0 )
        # RGB Pixels
        rgb_col = []
        for h in range( 0, img_height ):
            if ( ( h + 1 ) % 5 ) == 0:self.layout.progress_bar.setValue( h + 1 )
            QApplication.processEvents()
            for w in range( 0, img_width ):
                pixel_s = img_scale.pixelColor( w, h )
                r = pixel_s.redF()
                g = pixel_s.greenF()
                b = pixel_s.blueF()
                rgb = [ r, g, b ]
                if rgb not in rgb_col:
                    rgb_col.append( rgb )
        # Progress bar
        self.layout.progress_bar.setMaximum( 1 )
        self.layout.progress_bar.setValue( 0 )

        # UVD Dictionary
        uvd_col = {}
        for i in range( 0, depth ):
            uvd_col[i] = []
        len_rgb = len( rgb_col )
        if len_rgb > 0:
            for i in range( 0, len_rgb ):
                rgb = rgb_col[i]
                uvd = self.convert.rgb_to_uvd( rgb[0], rgb[1], rgb[2] )
                di = int( uvd[2] * depth )
                uvd_col[di].append( uvd )

        # Profile
        len_uvd = len( uvd_col )
        if len_uvd > 0:
            # Black Point
            for i in range( 0, len_uvd ):
                if len( uvd_col[i] ) > 0:
                    black_point = i
                    break
            # White Point
            for i in range( len_uvd, 0, -1 ):
                index = i - 1
                if len( uvd_col[index] ) > 0:
                    white_point = index
                    break

            # Profile
            profile = []
            for i in range( 0, len_uvd ):
                px = []
                py = []
                for d in range( 0, len( uvd_col[i] ) ):
                    px.append( uvd_col[i][d][0] )
                    py.append( uvd_col[i][d][1] )
                if ( len( px ) > 0 and len( py ) > 0 ):
                    mini_u = min( px )
                    maxi_u = max( px )
                    mini_v = min( py )
                    maxi_v = max( py )
                    profile.append( [ mini_u, maxi_u, mini_v, maxi_v ] )
                else:
                    profile.append( None )
            # Caps
            if profile[0] == None:
                profile[0] = [ 0, 0, 0, 0 ]
            if profile[depth-1] == None:
                profile[depth-1] = [ 0, 0, 0, 0 ]
            # Correction
            for i in range( 0, len( profile ) ):
                item = profile[i]
                if item == None:
                    # Left
                    for l in range( 0, depth ):
                        index_left = i-l
                        left = profile[index_left]
                        if left != None:
                            break
                    # Right
                    for r in range( 0, depth ):
                        index_right = i+r
                        right = profile[index_right]
                        if right != None:
                            break
                    # Percentage
                    percent = ( i - index_left ) / ( index_right - index_left )
                    # Lerp
                    lerp = self.geometry.Lerp_List( percent, left, right )
                    profile[i] = lerp
            # Return
            return profile, black_point, white_point

    def Wait( self, active_document ):
        active_document.waitForDone()
        active_document.refreshProjection()

    #endregion
    #region Notifier ###############################################################

    def Application_Closing( self ):
        pass
    def Configuration_Changed( self ):
        pass
    def Image_Closed( self ):
        pass
    def Image_Created( self ):
        pass
    def Image_Saved( self ):
        pass
    def View_Closed( self ):
        self.Sample_Clean()
    def View_Created( self ):
        pass
    def Window_Created( self ):
        pass
    def Window_IsBeingCreated( self ):
        pass

    #endregion
    #region Widget Events ##########################################################

    def showEvent( self, event ):
        # UI
        self.layout.split_sample.moveSplitter( int( self.layout.display_body.width() * 0.5 ), 1 )
        self.Update_Size()
    def resizeEvent( self, event ):
        self.Update_Size()
    def enterEvent( self, event ):
        pass
    def leaveEvent( self, event ):
        self.Clear_Focus()
    def closeEvent( self, event ):
        pass

    #endregion
    #region Canvas #################################################################

    def canvasChanged( self, canvas ):
        pass

    #endregion


# Bytes
def Bytes_to_Integer( self, byte_array, d_cd ):
    # converts byte data to numerical data
    # byte_data - information read from a document
    # d_cd - document color depth

    # Byte Order
    byte_order = sys.byteorder
    # Bit Depth
    if d_cd == "U8":
        k = 1
    elif ( d_cd == "U16" or d_cd == "F16" ):
        k = 2
    elif d_cd == "F32":
        k = 4
    # Conversion to INTEGER
    num_array = []
    for i in range( 0, len( byte_array ), k ):
        byte = byte_array[ i : i+k ]
        num = int.from_bytes( byte, byte_order )
        num_array.append( num )
    return num_array
def Integer_to_Bytes( self, num_array, d_cd ):
    # converts numbers to byte data
    # num_data - information previously calculated
    # d_cd - document color depth

    # Byte Order
    byte_order = sys.byteorder
    # Bit Depth
    if d_cd == "U8":
        k = 1
    elif ( d_cd == "U16" or d_cd == "F16" ):
        k = 2
    elif d_cd == "F32":
        k = 4

    # Conversion to Bytes
    byte_array = bytearray( num_array )
    return byte_array
# Pixels
def Numbers_on_Pixel( self, d_cm, d_cd, index, num_array ):
    # reads the numerical data from a pixel with a given index

    # Variables
    if d_cd == "U8": # BGR
        k = 255
    elif d_cd == "U16":
        k = 65535
    elif d_cd == "F16":
        # k = 65535
        k = 15360
    elif d_cd == "F32":
        # k = 4294836225
        k = 1065353216
    # Color Model and Depth
    byte_list = []
    if d_cm == "A":
        pixel = index * 2
        if d_cd == "U8":
            n0 = num_array[pixel + 0] # Gray
            n1 = num_array[pixel + 1] # Alpha
        if d_cd == "U16":
            n0 = num_array[pixel + 0] # Gray
            n1 = num_array[pixel + 1] # Alpha
        if d_cd == "F16":
            pass
        if d_cd == "F32":
            pass
        byte_list = [n0, n1]
    elif ( d_cm == "RGB" or d_cm == None ):
        pixel = index * 4
        if d_cd == "U8": # BGR
            n0 = num_array[pixel + 2] # Red
            n1 = num_array[pixel + 1] # Green
            n2 = num_array[pixel + 0] # Blue
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "U16": # BGR
            n0 = num_array[pixel + 2] # Red
            n1 = num_array[pixel + 1] # Green
            n2 = num_array[pixel + 0] # Blue
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "F16":
            pass
        if d_cd == "F32":
            pass
        byte_list = [n0, n1, n2, n3]
    elif d_cm == "CMYK":
        pixel = index * 5
        if d_cd == "U8":
            n0 = num_array[pixel + 0] # Cyan
            n1 = num_array[pixel + 1] # Magenta
            n2 = num_array[pixel + 2] # Yellow
            n3 = num_array[pixel + 3] # Key
            n4 = num_array[pixel + 4] # Alpha
        if d_cd == "U16":
            n0 = num_array[pixel + 0] # Cyan
            n1 = num_array[pixel + 1] # Magenta
            n2 = num_array[pixel + 2] # Yellow
            n3 = num_array[pixel + 3] # Key
            n4 = num_array[pixel + 4] # Alpha
        if d_cd == "F32":
            pass
        byte_list = [n0, n1, n2, n3, n4]
    elif d_cm == "YUV":
        pixel = index * 4
        if d_cd == "U8":
            n0 = num_array[pixel + 0] # Luma
            n1 = num_array[pixel + 1] # Cb
            n2 = num_array[pixel + 2] # Cr
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "U16":
            n0 = num_array[pixel + 0] # Luma
            n1 = num_array[pixel + 1] # Cb
            n2 = num_array[pixel + 2] # Cr
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "F32":
            pass
        byte_list = [n0, n1, n2, n3]
    elif d_cm == "XYZ":
        pixel = index * 4
        if d_cd == "U8":
            n0 = num_array[pixel + 0] # X
            n1 = num_array[pixel + 1] # Y
            n2 = num_array[pixel + 2] # Z
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "U16":
            n0 = num_array[pixel + 0] # X
            n1 = num_array[pixel + 1] # Y
            n2 = num_array[pixel + 2] # Z
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "F16":
            pass
        if d_cd == "F32":
            pass
        byte_list = [n0, n1, n2, n3]
    elif d_cm == "LAB":
        pixel = index * 4
        if d_cd == "U8":
            n0 = num_array[pixel + 0] # Lightness*
            n1 = num_array[pixel + 1] # A*
            n2 = num_array[pixel + 2] # 1*
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "U16":
            n0 = num_array[pixel + 0] # Lightness*
            n1 = num_array[pixel + 1] # A*
            n2 = num_array[pixel + 2] # 1*
            n3 = num_array[pixel + 3] # Alpha
        if d_cd == "F32":
            pass
        byte_list = [n0, n1, n2, n3]
    return byte_list
# Selection
def Insert_Selection( self, num_array, px, py, width, height ):
    # num_array - list of integer numbers, represents each pixels channels. RGB U8 > [ B,G,R,A, B,G,R,A, B,G,R,A, ... ]
    if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
        # Variables
        ki = Krita.instance()
        ad = ki.activeDocument()
        nt = ad.activeNode().type()

        # Place selection on good parent node
        if nt in ["paintlayer", "grouplayer"]:
            # Deselect all
            ki.action( "deselect" ).trigger()

            # Place Text
            ki.activeWindow().activeView().showFloatingMessage( "Pigment.O Insert | Selection", Krita.instance().icon( "local-selection-active" ), 5000, 0 )

            # Selection
            sel = Selection()
            sel.setPixelData( bytes( num_array ), px, py, width, height )
            ad.setSelection( sel )

            # Document Response Time
            ad.waitForDone()
            ad.refreshProjection()

            # Make Selection
            ki.action( "add_new_selection_mask" ).trigger()
            ki.action( "invert_selection" ).trigger()
            ki.action( "invert_selection" ).trigger()
        else:
            QMessageBox.information( QWidget(), i18n( "Warnning" ), i18n( f"Pigment.O ERROR | Please select valid layer for selection mask" ) )


"""
Krita Bugs:
- Byte data of a U16 document is not in RGB like on the API notes but it is in BGR.

To Do:
- Sample (Bit Depth + Color model )
    O U8
    O U16
    - F16
    - F32
- Profile UVD / ARD LUTs


Investigate Krita
- YUV / YCbCr color conversion formula - YUV formula is RED and Blue inverted ? or is it Krita ?

"""
