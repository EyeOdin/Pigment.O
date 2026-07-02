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

# Python
import copy
import os
import random
import time
import webbrowser
import re
import math
import zipfile
import shutil
# Krita
from krita import *
# PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# Engine
from .engine_name import *
from .engine_constants import *
from .engine_calculations import *
# Picker
from .picker_modulo import *
from .picker_extension import *

#endregion


class Picker_Docker( DockWidget ):
    """
    Color Picker and Mixer
    """

    #region Initialize

    def __init__( self ):
        super( Picker_Docker, self ).__init__()

        # Construct
        self.Interface()
        self.Module()
        self.Style()
        self.Variable()
        self.Setting()
        self.Connection()
        self.Extension()
        self.Updater()

    def Interface( self ):
        # Window
        self.setWindowTitle( DOCKER_PICKER )
        # Path Name
        self.directory_plugin = str( os.path.dirname( os.path.realpath( __file__ ) ) )
        # Widget Docker
        self.layout = uic.loadUi( os.path.join( self.directory_plugin, "picker_docker.ui" ), QWidget( self ) )
        self.setWidget( self.layout )
        # Settings
        self.dialog = uic.loadUi( os.path.join( self.directory_plugin, "picker_settings.ui" ), QDialog( self ) )
        self.dialog.setWindowTitle( f"{ DOCKER_PICKER } : Settings" )
        self.dialog.accept() # Hides the Dialog
    def Module( self ):
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
        #region Calculations

        # Convert
        self.convert = Convert()
        # Analyse
        self.analyse = Analyse()

        #endregion
        #region Header

        self.color_header = Color_Header( self.layout.color_header )
        self.color_header.SIGNAL_SWAP.connect( self.Header_Swap )
        self.color_header.SIGNAL_SHOW.connect( self.Header_Show )
        self.color_header.SIGNAL_RANDOM.connect( self.Header_Random )
        self.color_header.SIGNAL_COMP.connect( self.Header_Complementary )

        #endregion
        #region Harmony

        self.harmony_swatch = Harmony_Swatch( self.layout.harmony_swatch )
        self.harmony_swatch.SIGNAL_HARMONY_INDEX.connect( self.Harmony_Index )

        self.harmony_span = Harmony_Span( self.layout.harmony_span )
        self.harmony_span.SIGNAL_SPAN.connect( self.Harmony_Span )
        self.harmony_span.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )

        #endregion
        #region Panel View

        # Panel Fill
        self.panel_fill = Panel_Fill( self.layout.panel_fill )

        # Panel Square
        self.panel_square = Panel_Square( self.layout.panel_square )
        self.panel_square.SIGNAL_VALUE.connect( self.Panel_Square_Value )
        self.panel_square.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_square.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_square.SIGNAL_PIN_EDIT.connect( self.Pin_Panel )

        # Panel Hue Circle
        self.panel_hue_circle = Panel_Hue_Circle( self.layout.panel_hue_circle )
        self.panel_hue_circle.SIGNAL_ANGLE.connect( self.Panel_Hue_Circle_Angle )
        self.panel_hue_circle.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_hue_circle.SIGNAL_HARMONY_INDEX.connect( self.Harmony_Panel )
        # Panel Hue Shape
        self.panel_hue_shape = Panel_Square( self.layout.panel_hue_shape )
        self.panel_hue_shape.SIGNAL_VALUE.connect( self.Panel_Hue_Shape_Value )
        self.panel_hue_shape.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_hue_shape.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_hue_shape.SIGNAL_PIN_EDIT.connect( self.Pin_Panel )

        # Panel Gamut
        self.panel_gamut = Panel_Gamut( self.layout.panel_gamut )
        self.panel_gamut.SIGNAL_VALUE.connect( self.Panel_Gamut_Value )
        self.panel_gamut.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_gamut.SIGNAL_PROFILE.connect( self.Panel_Gamut_Profile )
        self.panel_gamut.SIGNAL_HARMONY_INDEX.connect( self.Harmony_Panel )
        self.panel_gamut.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_gamut.SIGNAL_PIN_EDIT.connect( self.Pin_Panel )

        # Panel Hexagon
        self.panel_hexagon = Panel_Hexagon( self.layout.panel_hexagon )
        self.panel_hexagon.SIGNAL_VALUE.connect( self.Panel_Hexagon_Value )
        self.panel_hexagon.SIGNAL_DEPTH.connect( self.Panel_Hexagon_Depth )
        self.panel_hexagon.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_hexagon.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_hexagon.SIGNAL_PIN_EDIT.connect( self.Pin_Panel )

        # Panel Luma
        self.panel_luma = Panel_Luma( self.layout.panel_luma )
        self.panel_luma.SIGNAL_VALUE.connect( self.Panel_Luma_Value )
        self.panel_luma.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_luma.SIGNAL_PIN_INDEX.connect( self.Pin_Apply )
        self.panel_luma.SIGNAL_PIN_EDIT.connect( self.Pin_Panel )

        # Panel Plane
        self.panel_plane = Panel_Plane( self.layout.panel_plane )
        self.panel_plane.SIGNAL_VALUE.connect( self.Panel_Plane_Value )
        self.panel_plane.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_plane.SIGNAL_INDEX.connect( self.Panel_Plane_Index )
        self.panel_plane.SIGNAL_SWAP.connect( self.Panel_Plane_Swap )
        self.panel_plane.SIGNAL_RANDOM.connect( self.Panel_Plane_Random )
        self.panel_plane.SIGNAL_RESET.connect( self.Panel_Plane_Reset )

        # Panel Mask View
        self.panel_mask = Panel_Mask( self.layout.panel_mask )
        self.panel_mask.SIGNAL_VALUE.connect( self.Panel_Mask_Value )
        self.panel_mask.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.panel_mask.SIGNAL_LIVE_OFF.connect( self.Mask_Close )

        #endregion
        #region Panel Pins

        # Panel Mask Pins
        self.mask_widget = [
            self.layout.b1_color,
            self.layout.b2_color,
            self.layout.b3_color,
            self.layout.d1_color,
            self.layout.d2_color,
            self.layout.d3_color,
            self.layout.d4_color,
            self.layout.d5_color,
            self.layout.d6_color,
            self.layout.f1_color,
            self.layout.f2_color,
            self.layout.f3_color,
            ]
        self.mask_module = list()
        count = len( self.mask_widget )
        for i in range( 0, count ):
            self.mask_module.append( Pin_Color( self.mask_widget[i] ) )
            self.mask_module[i].Set_Index( i )
            self.mask_module[i].Set_Alpha( True )
            self.mask_module[i].SIGNAL_APPLY.connect( self.Mask_Apply )
            self.mask_module[i].SIGNAL_SAVE.connect( self.Mask_Save )
            self.mask_module[i].SIGNAL_CLEAN.connect( self.Mask_Clean )
            self.mask_module[i].SIGNAL_ALPHA.connect( self.Mask_Alpha )
            self.mask_module[i].SIGNAL_TEXT.connect( self.Label_String )

        #endregion
        #region Channel

        # GRAY 1
        self.gray_1_slider = Channel_Slider( self.layout.gray_1_slider )
        self.gray_1_slider.SIGNAL_VALUE.connect( self.Channel_GRAY_1_Slider )
        self.gray_1_slider.SIGNAL_INCREMENT.connect( self.Channel_GRAY_1_Increment )
        self.gray_1_slider.SIGNAL_MARK.connect( self.Channel_GRAY_1_Mark )
        self.gray_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.gray_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.gray_1_slider.Set_Mode( "LINEAR" )
        # SRGB 1
        self.srgb_1_slider = Channel_Slider( self.layout.srgb_1_slider )
        self.srgb_1_slider.SIGNAL_VALUE.connect( self.Channel_SRGB_1_Slider )
        self.srgb_1_slider.SIGNAL_INCREMENT.connect( self.Channel_SRGB_1_Increment )
        self.srgb_1_slider.SIGNAL_MARK.connect( self.Channel_SRGB_1_Mark )
        self.srgb_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.srgb_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.srgb_1_slider.Set_Mode( "LINEAR" )
        # SRGB 2
        self.srgb_2_slider = Channel_Slider( self.layout.srgb_2_slider )
        self.srgb_2_slider.SIGNAL_VALUE.connect( self.Channel_SRGB_2_Slider )
        self.srgb_2_slider.SIGNAL_INCREMENT.connect( self.Channel_SRGB_2_Increment )
        self.srgb_2_slider.SIGNAL_MARK.connect( self.Channel_SRGB_2_Mark )
        self.srgb_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.srgb_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.srgb_2_slider.Set_Mode( "LINEAR" )
        # SRGB 3
        self.srgb_3_slider = Channel_Slider( self.layout.srgb_3_slider )
        self.srgb_3_slider.SIGNAL_VALUE.connect( self.Channel_SRGB_3_Slider )
        self.srgb_3_slider.SIGNAL_INCREMENT.connect( self.Channel_SRGB_3_Increment )
        self.srgb_3_slider.SIGNAL_MARK.connect( self.Channel_SRGB_3_Mark )
        self.srgb_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.srgb_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.srgb_3_slider.Set_Mode( "LINEAR" )
        # LRGB 1
        self.lrgb_1_slider = Channel_Slider( self.layout.lrgb_1_slider )
        self.lrgb_1_slider.SIGNAL_VALUE.connect( self.Channel_LRGB_1_Slider )
        self.lrgb_1_slider.SIGNAL_INCREMENT.connect( self.Channel_LRGB_1_Increment )
        self.lrgb_1_slider.SIGNAL_MARK.connect( self.Channel_LRGB_1_Mark )
        self.lrgb_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lrgb_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lrgb_1_slider.Set_Mode( "LINEAR" )
        # LRGB 2
        self.lrgb_2_slider = Channel_Slider( self.layout.lrgb_2_slider )
        self.lrgb_2_slider.SIGNAL_VALUE.connect( self.Channel_LRGB_2_Slider )
        self.lrgb_2_slider.SIGNAL_INCREMENT.connect( self.Channel_LRGB_2_Increment )
        self.lrgb_2_slider.SIGNAL_MARK.connect( self.Channel_LRGB_2_Mark )
        self.lrgb_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lrgb_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lrgb_2_slider.Set_Mode( "LINEAR" )
        # LRGB 3
        self.lrgb_3_slider = Channel_Slider( self.layout.lrgb_3_slider )
        self.lrgb_3_slider.SIGNAL_VALUE.connect( self.Channel_LRGB_3_Slider )
        self.lrgb_3_slider.SIGNAL_INCREMENT.connect( self.Channel_LRGB_3_Increment )
        self.lrgb_3_slider.SIGNAL_MARK.connect( self.Channel_LRGB_3_Mark )
        self.lrgb_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lrgb_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lrgb_3_slider.Set_Mode( "LINEAR" )
        # CMYK 1
        self.cmyk_1_slider = Channel_Slider( self.layout.cmyk_1_slider )
        self.cmyk_1_slider.SIGNAL_VALUE.connect( self.Channel_CMYK_1_Slider )
        self.cmyk_1_slider.SIGNAL_INCREMENT.connect( self.Channel_CMYK_1_Increment )
        self.cmyk_1_slider.SIGNAL_MARK.connect( self.Channel_CMYK_1_Mark )
        self.cmyk_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.cmyk_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.cmyk_1_slider.Set_Mode( "LINEAR" )
        # CMYK 2
        self.cmyk_2_slider = Channel_Slider( self.layout.cmyk_2_slider )
        self.cmyk_2_slider.SIGNAL_VALUE.connect( self.Channel_CMYK_2_Slider )
        self.cmyk_2_slider.SIGNAL_INCREMENT.connect( self.Channel_CMYK_2_Increment )
        self.cmyk_2_slider.SIGNAL_MARK.connect( self.Channel_CMYK_2_Mark )
        self.cmyk_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.cmyk_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.cmyk_2_slider.Set_Mode( "LINEAR" )
        # CMYK 3
        self.cmyk_3_slider = Channel_Slider( self.layout.cmyk_3_slider )
        self.cmyk_3_slider.SIGNAL_VALUE.connect( self.Channel_CMYK_3_Slider )
        self.cmyk_3_slider.SIGNAL_INCREMENT.connect( self.Channel_CMYK_3_Increment )
        self.cmyk_3_slider.SIGNAL_MARK.connect( self.Channel_CMYK_3_Mark )
        self.cmyk_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.cmyk_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.cmyk_3_slider.Set_Mode( "LINEAR" )
        # CMYK 4
        self.cmyk_4_slider = Channel_Slider( self.layout.cmyk_4_slider )
        self.cmyk_4_slider.SIGNAL_VALUE.connect( self.Channel_CMYK_4_Slider )
        self.cmyk_4_slider.SIGNAL_INCREMENT.connect( self.Channel_CMYK_4_Increment )
        self.cmyk_4_slider.SIGNAL_MARK.connect( self.Channel_CMYK_4_Mark )
        self.cmyk_4_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.cmyk_4_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.cmyk_4_slider.Set_Mode( "LINEAR" )
        # RYB 1
        self.ryb_1_slider = Channel_Slider( self.layout.ryb_1_slider )
        self.ryb_1_slider.SIGNAL_VALUE.connect( self.Channel_RYB_1_Slider )
        self.ryb_1_slider.SIGNAL_INCREMENT.connect( self.Channel_RYB_1_Increment )
        self.ryb_1_slider.SIGNAL_MARK.connect( self.Channel_RYB_1_Mark )
        self.ryb_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.ryb_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.ryb_1_slider.Set_Mode( "LINEAR" )
        # RYB 2
        self.ryb_2_slider = Channel_Slider( self.layout.ryb_2_slider )
        self.ryb_2_slider.SIGNAL_VALUE.connect( self.Channel_RYB_2_Slider )
        self.ryb_2_slider.SIGNAL_INCREMENT.connect( self.Channel_RYB_2_Increment )
        self.ryb_2_slider.SIGNAL_MARK.connect( self.Channel_RYB_2_Mark )
        self.ryb_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.ryb_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.ryb_2_slider.Set_Mode( "LINEAR" )
        # RYB 3
        self.ryb_3_slider = Channel_Slider( self.layout.ryb_3_slider )
        self.ryb_3_slider.SIGNAL_VALUE.connect( self.Channel_RYB_3_Slider )
        self.ryb_3_slider.SIGNAL_INCREMENT.connect( self.Channel_RYB_3_Increment )
        self.ryb_3_slider.SIGNAL_MARK.connect( self.Channel_RYB_3_Mark )
        self.ryb_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.ryb_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.ryb_3_slider.Set_Mode( "LINEAR" )
        # YUV 1
        self.yuv_1_slider = Channel_Slider( self.layout.yuv_1_slider )
        self.yuv_1_slider.SIGNAL_VALUE.connect( self.Channel_YUV_1_Slider )
        self.yuv_1_slider.SIGNAL_INCREMENT.connect( self.Channel_YUV_1_Increment )
        self.yuv_1_slider.SIGNAL_MARK.connect( self.Channel_YUV_1_Mark )
        self.yuv_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.yuv_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.yuv_1_slider.Set_Mode( "LINEAR" )
        # YUV 2
        self.yuv_2_slider = Channel_Slider( self.layout.yuv_2_slider )
        self.yuv_2_slider.SIGNAL_VALUE.connect( self.Channel_YUV_2_Slider )
        self.yuv_2_slider.SIGNAL_INCREMENT.connect( self.Channel_YUV_2_Increment )
        self.yuv_2_slider.SIGNAL_MARK.connect( self.Channel_YUV_2_Mark )
        self.yuv_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.yuv_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.yuv_2_slider.Set_Mode( "LINEAR" )
        # YUV 3
        self.yuv_3_slider = Channel_Slider( self.layout.yuv_3_slider )
        self.yuv_3_slider.SIGNAL_VALUE.connect( self.Channel_YUV_3_Slider )
        self.yuv_3_slider.SIGNAL_INCREMENT.connect( self.Channel_YUV_3_Increment )
        self.yuv_3_slider.SIGNAL_MARK.connect( self.Channel_YUV_3_Mark )
        self.yuv_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.yuv_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.yuv_3_slider.Set_Mode( "LINEAR" )
        # HSV 1
        self.hsv_1_slider = Channel_Slider( self.layout.hsv_1_slider )
        self.hsv_1_slider.SIGNAL_VALUE.connect( self.Channel_HSV_1_Slider )
        self.hsv_1_slider.SIGNAL_INCREMENT.connect( self.Channel_HSV_1_Increment )
        self.hsv_1_slider.SIGNAL_MARK.connect( self.Channel_HSV_1_Mark )
        self.hsv_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hsv_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hsv_1_slider.Set_Mode( "CIRCULAR" )
        # HSV 2
        self.hsv_2_slider = Channel_Slider( self.layout.hsv_2_slider )
        self.hsv_2_slider.SIGNAL_VALUE.connect( self.Channel_HSV_2_Slider )
        self.hsv_2_slider.SIGNAL_INCREMENT.connect( self.Channel_HSV_2_Increment )
        self.hsv_2_slider.SIGNAL_MARK.connect( self.Channel_HSV_2_Mark )
        self.hsv_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hsv_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hsv_2_slider.Set_Mode( "LINEAR" )
        # HSV 3
        self.hsv_3_slider = Channel_Slider( self.layout.hsv_3_slider )
        self.hsv_3_slider.SIGNAL_VALUE.connect( self.Channel_HSV_3_Slider )
        self.hsv_3_slider.SIGNAL_INCREMENT.connect( self.Channel_HSV_3_Increment )
        self.hsv_3_slider.SIGNAL_MARK.connect( self.Channel_HSV_3_Mark )
        self.hsv_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hsv_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hsv_3_slider.Set_Mode( "LINEAR" )
        # HSL 1
        self.hsl_1_slider = Channel_Slider( self.layout.hsl_1_slider )
        self.hsl_1_slider.SIGNAL_VALUE.connect( self.Channel_HSL_1_Slider )
        self.hsl_1_slider.SIGNAL_INCREMENT.connect( self.Channel_HSL_1_Increment )
        self.hsl_1_slider.SIGNAL_MARK.connect( self.Channel_HSL_1_Mark )
        self.hsl_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hsl_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hsl_1_slider.Set_Mode( "CIRCULAR" )
        # HSL 2
        self.hsl_2_slider = Channel_Slider( self.layout.hsl_2_slider )
        self.hsl_2_slider.SIGNAL_VALUE.connect( self.Channel_HSL_2_Slider )
        self.hsl_2_slider.SIGNAL_INCREMENT.connect( self.Channel_HSL_2_Increment )
        self.hsl_2_slider.SIGNAL_MARK.connect( self.Channel_HSL_2_Mark )
        self.hsl_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hsl_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hsl_2_slider.Set_Mode( "LINEAR" )
        # HSL 3
        self.hsl_3_slider = Channel_Slider( self.layout.hsl_3_slider )
        self.hsl_3_slider.SIGNAL_VALUE.connect( self.Channel_HSL_3_Slider )
        self.hsl_3_slider.SIGNAL_INCREMENT.connect( self.Channel_HSL_3_Increment )
        self.hsl_3_slider.SIGNAL_MARK.connect( self.Channel_HSL_3_Mark )
        self.hsl_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hsl_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hsl_3_slider.Set_Mode( "LINEAR" )
        # HCY 1
        self.hcy_1_slider = Channel_Slider( self.layout.hcy_1_slider )
        self.hcy_1_slider.SIGNAL_VALUE.connect( self.Channel_HCY_1_Slider )
        self.hcy_1_slider.SIGNAL_INCREMENT.connect( self.Channel_HCY_1_Increment )
        self.hcy_1_slider.SIGNAL_MARK.connect( self.Channel_HCY_1_Mark )
        self.hcy_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hcy_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hcy_1_slider.Set_Mode( "CIRCULAR" )
        # HCY 2
        self.hcy_2_slider = Channel_Slider( self.layout.hcy_2_slider )
        self.hcy_2_slider.SIGNAL_VALUE.connect( self.Channel_HCY_2_Slider )
        self.hcy_2_slider.SIGNAL_INCREMENT.connect( self.Channel_HCY_2_Increment )
        self.hcy_2_slider.SIGNAL_MARK.connect( self.Channel_HCY_2_Mark )
        self.hcy_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hcy_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hcy_2_slider.Set_Mode( "LINEAR" )
        # HCY 3
        self.hcy_3_slider = Channel_Slider( self.layout.hcy_3_slider )
        self.hcy_3_slider.SIGNAL_VALUE.connect( self.Channel_HCY_3_Slider )
        self.hcy_3_slider.SIGNAL_INCREMENT.connect( self.Channel_HCY_3_Increment )
        self.hcy_3_slider.SIGNAL_MARK.connect( self.Channel_HCY_3_Mark )
        self.hcy_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.hcy_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.hcy_3_slider.Set_Mode( "LINEAR" )
        # ARD 1
        self.ard_1_slider = Channel_Slider( self.layout.ard_1_slider )
        self.ard_1_slider.SIGNAL_VALUE.connect( self.Channel_ARD_1_Slider )
        self.ard_1_slider.SIGNAL_INCREMENT.connect( self.Channel_ARD_1_Increment )
        self.ard_1_slider.SIGNAL_MARK.connect( self.Channel_ARD_1_Mark )
        self.ard_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.ard_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.ard_1_slider.Set_Mode( "CIRCULAR" )
        # ARD 2
        self.ard_2_slider = Channel_Slider( self.layout.ard_2_slider )
        self.ard_2_slider.SIGNAL_VALUE.connect( self.Channel_ARD_2_Slider )
        self.ard_2_slider.SIGNAL_INCREMENT.connect( self.Channel_ARD_2_Increment )
        self.ard_2_slider.SIGNAL_MARK.connect( self.Channel_ARD_2_Mark )
        self.ard_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.ard_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.ard_2_slider.Set_Mode( "LINEAR" )
        # ARD 3
        self.ard_3_slider = Channel_Slider( self.layout.ard_3_slider )
        self.ard_3_slider.SIGNAL_VALUE.connect( self.Channel_ARD_3_Slider )
        self.ard_3_slider.SIGNAL_INCREMENT.connect( self.Channel_ARD_3_Increment )
        self.ard_3_slider.SIGNAL_MARK.connect( self.Channel_ARD_3_Mark )
        self.ard_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.ard_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.ard_3_slider.Set_Mode( "DEPTH" )
        # XYZ 1
        self.xyz_1_slider = Channel_Slider( self.layout.xyz_1_slider )
        self.xyz_1_slider.SIGNAL_VALUE.connect( self.Channel_XYZ_1_Slider )
        self.xyz_1_slider.SIGNAL_INCREMENT.connect( self.Channel_XYZ_1_Increment )
        self.xyz_1_slider.SIGNAL_MARK.connect( self.Channel_XYZ_1_Mark )
        self.xyz_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.xyz_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.xyz_1_slider.Set_Mode( "LINEAR" )
        # XYZ 2
        self.xyz_2_slider = Channel_Slider( self.layout.xyz_2_slider )
        self.xyz_2_slider.SIGNAL_VALUE.connect( self.Channel_XYZ_2_Slider )
        self.xyz_2_slider.SIGNAL_INCREMENT.connect( self.Channel_XYZ_2_Increment )
        self.xyz_2_slider.SIGNAL_MARK.connect( self.Channel_XYZ_2_Mark )
        self.xyz_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.xyz_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.xyz_2_slider.Set_Mode( "LINEAR" )
        # XYZ 3
        self.xyz_3_slider = Channel_Slider( self.layout.xyz_3_slider )
        self.xyz_3_slider.SIGNAL_VALUE.connect( self.Channel_XYZ_3_Slider )
        self.xyz_3_slider.SIGNAL_INCREMENT.connect( self.Channel_XYZ_3_Increment )
        self.xyz_3_slider.SIGNAL_MARK.connect( self.Channel_XYZ_3_Mark )
        self.xyz_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.xyz_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.xyz_3_slider.Set_Mode( "LINEAR" )
        # XYY 1
        self.xyy_1_slider = Channel_Slider( self.layout.xyy_1_slider )
        self.xyy_1_slider.SIGNAL_VALUE.connect( self.Channel_XYY_1_Slider )
        self.xyy_1_slider.SIGNAL_INCREMENT.connect( self.Channel_XYY_1_Increment )
        self.xyy_1_slider.SIGNAL_MARK.connect( self.Channel_XYY_1_Mark )
        self.xyy_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.xyy_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.xyy_1_slider.Set_Mode( "LINEAR" )
        # XYY 2
        self.xyy_2_slider = Channel_Slider( self.layout.xyy_2_slider )
        self.xyy_2_slider.SIGNAL_VALUE.connect( self.Channel_XYY_2_Slider )
        self.xyy_2_slider.SIGNAL_INCREMENT.connect( self.Channel_XYY_2_Increment )
        self.xyy_2_slider.SIGNAL_MARK.connect( self.Channel_XYY_2_Mark )
        self.xyy_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.xyy_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.xyy_2_slider.Set_Mode( "LINEAR" )
        # XYY 3
        self.xyy_3_slider = Channel_Slider( self.layout.xyy_3_slider )
        self.xyy_3_slider.SIGNAL_VALUE.connect( self.Channel_XYY_3_Slider )
        self.xyy_3_slider.SIGNAL_INCREMENT.connect( self.Channel_XYY_3_Increment )
        self.xyy_3_slider.SIGNAL_MARK.connect( self.Channel_XYY_3_Mark )
        self.xyy_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.xyy_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.xyy_3_slider.Set_Mode( "LINEAR" )
        # LAB 1
        self.lab_1_slider = Channel_Slider( self.layout.lab_1_slider )
        self.lab_1_slider.SIGNAL_VALUE.connect( self.Channel_LAB_1_Slider )
        self.lab_1_slider.SIGNAL_INCREMENT.connect( self.Channel_LAB_1_Increment )
        self.lab_1_slider.SIGNAL_MARK.connect( self.Channel_LAB_1_Mark )
        self.lab_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lab_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lab_1_slider.Set_Mode( "LINEAR" )
        # LAB 2
        self.lab_2_slider = Channel_Slider( self.layout.lab_2_slider )
        self.lab_2_slider.SIGNAL_VALUE.connect( self.Channel_LAB_2_Slider )
        self.lab_2_slider.SIGNAL_INCREMENT.connect( self.Channel_LAB_2_Increment )
        self.lab_2_slider.SIGNAL_MARK.connect( self.Channel_LAB_2_Mark )
        self.lab_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lab_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lab_2_slider.Set_Mode( "LINEAR" )
        # LAB 3
        self.lab_3_slider = Channel_Slider( self.layout.lab_3_slider )
        self.lab_3_slider.SIGNAL_VALUE.connect( self.Channel_LAB_3_Slider )
        self.lab_3_slider.SIGNAL_INCREMENT.connect( self.Channel_LAB_3_Increment )
        self.lab_3_slider.SIGNAL_MARK.connect( self.Channel_LAB_3_Mark )
        self.lab_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lab_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lab_3_slider.Set_Mode( "LINEAR" )
        # LCH 1
        self.lch_1_slider = Channel_Slider( self.layout.lch_1_slider )
        self.lch_1_slider.SIGNAL_VALUE.connect( self.Channel_LCH_1_Slider )
        self.lch_1_slider.SIGNAL_INCREMENT.connect( self.Channel_LCH_1_Increment )
        self.lch_1_slider.SIGNAL_MARK.connect( self.Channel_LCH_1_Mark )
        self.lch_1_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lch_1_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lch_1_slider.Set_Mode( "LINEAR" )
        # LCH 2
        self.lch_2_slider = Channel_Slider( self.layout.lch_2_slider )
        self.lch_2_slider.SIGNAL_VALUE.connect( self.Channel_LCH_2_Slider )
        self.lch_2_slider.SIGNAL_INCREMENT.connect( self.Channel_LCH_2_Increment )
        self.lch_2_slider.SIGNAL_MARK.connect( self.Channel_LCH_2_Mark )
        self.lch_2_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lch_2_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lch_2_slider.Set_Mode( "LINEAR" )
        # LCH 3
        self.lch_3_slider = Channel_Slider( self.layout.lch_3_slider )
        self.lch_3_slider.SIGNAL_VALUE.connect( self.Channel_LCH_3_Slider )
        self.lch_3_slider.SIGNAL_INCREMENT.connect( self.Channel_LCH_3_Increment )
        self.lch_3_slider.SIGNAL_MARK.connect( self.Channel_LCH_3_Mark )
        self.lch_3_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.lch_3_slider.SIGNAL_TEXT.connect( self.Label_String )
        self.lch_3_slider.Set_Mode( "CIRCULAR" )

        #endregion
        #region Mixer

        # Kelvin Pin Left
        self.kelvin_pin_l = Pin_Color( self.layout.kelvin_pin_l )
        self.kelvin_pin_l.Set_Menu( [ "APPLY", None, None ] )
        self.kelvin_pin_l.Set_Index( 0 )
        self.kelvin_pin_l.SIGNAL_APPLY.connect( self.Kelvin_Apply )
        self.kelvin_pin_l.SIGNAL_TEXT.connect( self.Label_String )
        # Kelvin Pin Right
        self.kelvin_pin_r = Pin_Color( self.layout.kelvin_pin_r )
        self.kelvin_pin_r.Set_Menu( [ "APPLY", None, None ] )
        self.kelvin_pin_r.Set_Index( 1 )
        self.kelvin_pin_r.SIGNAL_APPLY.connect( self.Kelvin_Apply )
        self.kelvin_pin_r.SIGNAL_TEXT.connect( self.Label_String )
        # Kelvin Slider
        self.kelvin_slider = Channel_Slider( self.layout.kelvin_slider )
        self.kelvin_slider.Set_Mode( "KELVIN" )
        self.kelvin_slider.Set_Value( 0.5 )
        self.kelvin_slider.SIGNAL_VALUE.connect( self.Kelvin_Slider )
        self.kelvin_slider.SIGNAL_MARK.connect( self.Kelvin_Mark )
        self.kelvin_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.kelvin_slider.SIGNAL_TEXT.connect( self.Label_String )

        # Pole Pin Left
        self.pole_pin_l = Pin_Color( self.layout.pole_pin_l )
        self.pole_pin_l.Set_Index( 0 )
        self.pole_pin_l.SIGNAL_APPLY.connect( self.Pole_Apply )
        self.pole_pin_l.SIGNAL_SAVE.connect( self.Pole_Save )
        self.pole_pin_l.SIGNAL_CLEAN.connect( self.Pole_Clean )
        self.pole_pin_l.SIGNAL_TEXT.connect( self.Label_String )
        # Pole Pin Right
        self.pole_pin_r = Pin_Color( self.layout.pole_pin_r )
        self.pole_pin_r.Set_Index( 1 )
        self.pole_pin_r.SIGNAL_APPLY.connect( self.Pole_Apply )
        self.pole_pin_r.SIGNAL_SAVE.connect( self.Pole_Save )
        self.pole_pin_r.SIGNAL_CLEAN.connect( self.Pole_Clean )
        self.pole_pin_r.SIGNAL_TEXT.connect( self.Label_String )
        # Pole Slider
        self.pole_slider = Channel_Slider( self.layout.pole_slider )
        self.pole_slider.Set_Mode( "POLE" )
        self.pole_slider.Set_Value( 0.5 )
        self.pole_slider.SIGNAL_VALUE.connect( self.Pole_Slider )
        self.pole_slider.SIGNAL_MARK.connect( self.Pole_Mark )
        self.pole_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.pole_slider.SIGNAL_TEXT.connect( self.Label_String )

        # Linear Pin Left
        self.linear_pin_l = Pin_Color( self.layout.linear_pin_l )
        self.linear_pin_l.Set_Index( 0 )
        self.linear_pin_l.SIGNAL_APPLY.connect( self.Linear_Apply )
        self.linear_pin_l.SIGNAL_SAVE.connect( self.Linear_Save )
        self.linear_pin_l.SIGNAL_CLEAN.connect( self.Linear_Clean )
        self.linear_pin_l.SIGNAL_TEXT.connect( self.Label_String )
        # Linear Pin Right
        self.linear_pin_r = Pin_Color( self.layout.linear_pin_r )
        self.linear_pin_r.Set_Index( 1 )
        self.linear_pin_r.SIGNAL_APPLY.connect( self.Linear_Apply )
        self.linear_pin_r.SIGNAL_SAVE.connect( self.Linear_Save )
        self.linear_pin_r.SIGNAL_CLEAN.connect( self.Linear_Clean )
        self.linear_pin_r.SIGNAL_TEXT.connect( self.Label_String )
        # Linear Slider
        self.linear_slider = Channel_Slider( self.layout.linear_slider )
        self.linear_slider.Set_Mode( "LINEAR" )
        self.linear_slider.Set_Value( 0 )
        self.linear_slider.SIGNAL_VALUE.connect( self.Linear_Slider )
        self.linear_slider.SIGNAL_MARK.connect( self.Linear_Mark )
        self.linear_slider.SIGNAL_RELEASE.connect( self.Pigmento_SYNC )
        self.linear_slider.SIGNAL_TEXT.connect( self.Label_String )

        #endregion
        #region Pin

        # Variables
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
        self.pin_module = list()
        self.pin_color = list()
        # Pins
        count = len( self.pin_widget )
        for i in range( 0, count ):
            self.pin_module.append( Pin_Color( self.pin_widget[i] ) )
            self.pin_module[i].Set_Index( i )
            self.pin_module[i].SIGNAL_APPLY.connect( self.Pin_Apply )
            self.pin_module[i].SIGNAL_SAVE.connect( self.Pin_Save )
            self.pin_module[i].SIGNAL_CLEAN.connect( self.Pin_Clean )
            self.pin_module[i].SIGNAL_TEXT.connect( self.Label_String )
            self.pin_color.append( color_false.copy() )

        #endregion
        #region Sample

        self.sample_screen = SampleScreen_Button( self.layout.sample_screen )
        self.sample_screen.SIGNAL_PRESS.connect( self.SampleScreen_Press )
        self.sample_screen.SIGNAL_MOVE.connect( self.SampleScreen_Move )
        self.sample_screen.SIGNAL_RELEASE.connect( self.SampleScreen_Release )

        #endregion
    def Style( self ):
        # Style
        self.Style_Icon()
        self.Style_Tooltip()
        self.Style_Theme()

        # Combobox Panel Entries
        self.dialog.panel_mode.addItem( panel_fill )
        self.dialog.panel_mode.addItem( panel_square )
        self.dialog.panel_mode.addItem( panel_hue )
        self.dialog.panel_mode.addItem( panel_gamut )
        self.dialog.panel_mode.addItem( panel_hexagon )
        self.dialog.panel_mode.addItem( panel_luma )
        self.dialog.panel_mode.addItem( panel_plane )
        self.dialog.panel_mode.addItem( panel_mask )
        # Panel Icons
        qpixmap_fill = QPixmap( 100, 100 )
        qpixmap_fill.fill( QColor( "#000000" ) )
        icon_path       = os.path.join( self.directory_plugin, "ICON" )
        path_square     = os.path.join( icon_path, "SQUARE.png" )
        path_hue        = os.path.join( icon_path, "HUE.png" )
        path_gamut      = os.path.join( icon_path, "GAMUT.png" )
        path_hexagon    = os.path.join( icon_path, "HEXAGON.png" )
        path_luma       = os.path.join( icon_path, "LUMA.png" )
        path_plane      = os.path.join( icon_path, "PLANE.png" )
        path_mask       = os.path.join( icon_path, "MASK.png" )
        self.dialog.panel_mode.setItemIcon( 0, QIcon( qpixmap_fill ) )
        self.dialog.panel_mode.setItemIcon( 1, QIcon( path_square ) )
        self.dialog.panel_mode.setItemIcon( 2, QIcon( path_hue ) )
        self.dialog.panel_mode.setItemIcon( 3, QIcon( path_gamut ) )
        self.dialog.panel_mode.setItemIcon( 4, QIcon( path_hexagon ) )
        self.dialog.panel_mode.setItemIcon( 5, QIcon( path_luma ) )
        self.dialog.panel_mode.setItemIcon( 6, QIcon( path_plane ) )
        self.dialog.panel_mode.setItemIcon( 7, QIcon( path_mask ) )

        # Panel Mask Entries
        self.mask_path = os.path.normpath( os.path.join( self.directory_plugin, "MASK" ) )
        self.mask_list = os.listdir( self.mask_path )
        for folder in self.mask_list:
            self.dialog.mask_folder.addItem( folder )
        if len( self.mask_list ) > 0:   self.mask_url = os.path.normpath( os.path.join( self.mask_path, self.mask_list[0] ) )
        else:                           self.mask_url = self.mask_path
    def Variable( self ):
        #region Pigment.O

        # Color Picker Module
        self.pigmento_sampler = None
        self.pigmento_sampler_pyid = "pykrita_pigment_o_sampler_docker"

        #endregion
        #region Colors

        # Url
        self.url_panel = os.path.normpath( os.path.join( self.directory_plugin, "PANEL" ) )

        # Krita
        self.kdocument = self.Document_None()
        self.kcanvas = None
        self.kview = None
        self.kdepth = 255
        self.kmodel = None
        self.kwrite = False

        # Colors
        self.color_index = kfc
        self.mix_index = mix
        self.depth_previous = 0
        self.fgc = None
        self.bgc = None
        self.hue = 0
        self.hex_code = "#000000"
        self.lock_cmyk_4 = False

        # Mixer Variables
        self.mix_p    = 0.5
        self.kelvin_k = 6500
        self.kelvin_p = 0.5
        self.pole_p   = 0.5
        self.linear_p = 0

        # Color
        self.color_view  = Kritarc_Read( DOCKER_PICKER, "color_view",  color_view,  eval )
        self.color_mark  = Kritarc_Read( DOCKER_PICKER, "color_mark",  color_mark,  eval )
        self.color_range = Kritarc_Read( DOCKER_PICKER, "color_range", color_range, eval )

        # Monochrome
        self.color_b  = self.Color_Convert( "HEX", "#000000", 0, 0, 0, color_true.copy() )
        self.color_g  = self.Color_Convert( "HEX", "#7f7f7f", 0, 0, 0, color_true.copy() )
        self.color_w  = self.Color_Convert( "HEX", "#ffffff", 0, 0, 0, color_true.copy() )
        # Zorn
        self.zorn_y = self.Color_Convert( "HEX", "#edb525", 0, 0, 0, color_true.copy() )
        self.zorn_r = self.Color_Convert( "HEX", "#b72e35", 0, 0, 0, color_true.copy() )
        self.zorn_w = self.Color_Convert( "HEX", "#edf0ec", 0, 0, 0, color_true.copy() )
        self.zorn_b = self.Color_Convert( "HEX", "#292421", 0, 0, 0, color_true.copy() )
        # Kelvin
        self.kelvin_l = self.Color_Convert( "HEX", "#ff4300", 0, 0, 0, color_true.copy() )
        self.kelvin_r = self.Color_Convert( "HEX", "#bfd3ff", 0, 0, 0, color_true.copy() )
        # Read Mixer Pole
        self.pole_l = Kritarc_Read( DOCKER_PICKER, "pole_l", self.color_b, eval )
        self.pole_r = Kritarc_Read( DOCKER_PICKER, "pole_r", self.color_w, eval )
        # Read Mixer Linear
        self.linear_l = Kritarc_Read( DOCKER_PICKER, "linear_l", self.color_b, eval )
        self.linear_r = Kritarc_Read( DOCKER_PICKER, "linear_r", self.color_w, eval )

        #endregion
        #region Layout

        # Header
        self.header_mode = "FG" # "FG" "BG"

        # Harmony
        self.harmony_index = 1
        self.harmony_amplitude = 0.2

        # Panel Gamut
        gamut_profile = [
            [ [0.5, 0.5], [0.5, 0.1], [0.84641, 0.7], [0.15359, 0.7] ],
            [ [0.5, 0.5], [0.5, 0.1], [0.9, 0.5], [0.5, 0.9], [0.1, 0.5] ],
            [ [0.5, 0.5], [0.15359, 0.3], [0.5, 0.1], [0.84641, 0.3], [0.84641, 0.7], [0.5, 0.9], [0.15359, 0.7] ],
            [ [0.5, 0.5], [0.5, 0.1], [0.9, 0.5], [0.5, 0.9], [0.1, 0.5] ],
            [ [0.5, 0.275], [0.5, 0.1], [0.675, 0.275], [0.5, 0.45], [0.325, 0.275], [0.5, 0.725], [0.5, 0.55], [0.675, 0.725], [0.5, 0.9], [0.325, 0.725] ]
            ]
        self.gamut_profile = Kritarc_Read( DOCKER_PICKER, "gamut_profile", gamut_profile, eval )

        # Panel Plane
        plane_color = [ self.zorn_w.copy(), self.zorn_y.copy(), self.zorn_r.copy(), self.zorn_b.copy() ]
        self.plane_color = Kritarc_Read( DOCKER_PICKER, "plane_color", plane_color, eval )
        self.plane_matrix = None
        self.plane_margin = 10
        self.plane_split = 2
        self.plane_unit = 22 # square size pixels
        self.plane_dx = 0
        self.plane_dy = 0
        self.plane_ux = self.plane_unit
        self.plane_uy = self.plane_unit
        self.plane_ww = 1
        self.plane_hh = 1

        # Panel Mask
        self.mask_file = None # URL
        self.mask_live = None # index
        self.mask_color = [
            "#7f7f7f", # b1
            "#000000", # b2
            "#000000", # b3
            "#231402", # d1
            "#543713", # d2
            "#fe9f0e", # d3
            "#ffca32", # d4
            "#000000", # d5
            "#000000", # d6
            "#000000", # f1
            "#ffff96", # f2
            "#ffffff", # f3
            ]
        self.mask_alpha = [
            0.0, # b1
            1.0, # b2
            1.0, # b3
            1.0, # d1
            1.0, # d2
            1.0, # d3
            1.0, # d4
            0.0, # d5
            0.0, # d6
            1.0, # f1
            1.0, # f2
            1.0, # f3
            ]

        # Pin
        self.pin_color = Kritarc_Read( DOCKER_PICKER, "pin_color", self.pin_color, eval )

        # History
        self.cursor_inside = None

        # Footer
        self.mode_index = 0

        # Fill
        self.fill_pixel = { "active" : False, "node_uid" : None, "alpha_lock" : False }

        # Timer
        self.qtimer_pulse = None

        #endregion
        #region Docker Header

        # Docker User interface
        self.ui_harmony = Kritarc_Read( DOCKER_PICKER, "ui_harmony", False, eval )
        self.ui_channel = Kritarc_Read( DOCKER_PICKER, "ui_channel", True,  eval )
        self.ui_mixer   = Kritarc_Read( DOCKER_PICKER, "ui_mixer",   False, eval )
        self.ui_pin     = Kritarc_Read( DOCKER_PICKER, "ui_pin",     False, eval )
        self.ui_history = Kritarc_Read( DOCKER_PICKER, "ui_history", False, eval )

        #endregion
        #region Dialog Interface

        # Harmony
        self.harmony_rule  = Kritarc_Read( DOCKER_PICKER, "harmony_rule",  harmony_5,    str )
        self.harmony_edit  = Kritarc_Read( DOCKER_PICKER, "harmony_edit",  False,        eval )
        # Panel
        self.panel_mode    = Kritarc_Read( DOCKER_PICKER, "panel_mode",    panel_square, str )
        self.wheel_mode    = Kritarc_Read( DOCKER_PICKER, "wheel_mode",    "DIGITAL",    str ) # "DIGITAL" "ANALOG"
        self.wheel_space   = Kritarc_Read( DOCKER_PICKER, "wheel_space",   "HSV",        str ) # "HSV" "HSL" "HCY" "ARD"
        # Panel Options
        self.hue_shape     = Kritarc_Read( DOCKER_PICKER, "hue_shape",     "TRIANGLE",   str ) # "None" "TRIANGLE" "SQUARE" "DIAMOND"
        self.gamut_mask    = Kritarc_Read( DOCKER_PICKER, "gamut_mask",    "FULL",       str ) # "FULL" "TRIANGLE" "SQUARE" "HEXAGON" "CIRCLE_1" "CIRCLE_2" "NONE"
        self.mask_folder   = Kritarc_Read( DOCKER_PICKER, "mask_folder",   "SPHERE",     str ) # "SPHERE" "USER"
        self.mask_edit     = Kritarc_Read( DOCKER_PICKER, "mask_edit",     False,        eval )
        # Mixer
        self.mixer_space   = Kritarc_Read( DOCKER_PICKER, "mixer_space",   "LRGB",       str )

        #endregion
        #region Dialog Color

        # Channel Format
        self.format_index    = Kritarc_Read( DOCKER_PICKER, "format_index",    False, eval )
        self.format_value    = Kritarc_Read( DOCKER_PICKER, "format_value",    False, eval )
        self.format_hueshine = Kritarc_Read( DOCKER_PICKER, "format_hueshine", False, eval )

        #endregion
        #region Dialog Extras

        # Analyse
        self.analyse_list = None
        self.analyse_display = Kritarc_Read( DOCKER_PICKER, "analyse_display", False, eval )

        # Shortcuts
        self.key_1_mode = Kritarc_Read( DOCKER_PICKER, "key_1_mode", "CMYK_1", str )
        self.key_2_mode = Kritarc_Read( DOCKER_PICKER, "key_2_mode", "CMYK_2", str )
        self.key_3_mode = Kritarc_Read( DOCKER_PICKER, "key_3_mode", "CMYK_3", str )
        self.key_4_mode = Kritarc_Read( DOCKER_PICKER, "key_4_mode", "CMYK_4", str )
        self.key_1_unit = Kritarc_Read( DOCKER_PICKER, "key_1_unit", 1, int )
        self.key_2_unit = Kritarc_Read( DOCKER_PICKER, "key_2_unit", 1, int )
        self.key_3_unit = Kritarc_Read( DOCKER_PICKER, "key_3_unit", 1, int )
        self.key_4_unit = Kritarc_Read( DOCKER_PICKER, "key_4_unit", 1, int )

        #endregion
        #region Dialog System

        # Color Space
        self.cs_luminosity = Kritarc_Read( DOCKER_PICKER, "cs_luminosity", "Rec.709", str )
        self.cs_matrix = Kritarc_Read( DOCKER_PICKER, "cs_matrix", "sRGB (D50)", str )
        # Performance
        self.performance_release = Kritarc_Read( DOCKER_PICKER, "performance_release", False, eval )

        #endregion
    def Setting( self ):
        # Harmony
        self.Color_Harmony( self.harmony_amplitude, har_01, har_02, har_03, har_04, har_05 )
        self.harmony_swatch.Update_Index( self.harmony_index )

        # Panel Gamut
        self.panel_gamut.Set_Profile( self.gamut_profile )

        # Panel Mask
        self.Mask_Load( self.mask_url )

        # Channel
        self.Channel_Mark()
        self.Channel_Range()
        self.Mixer_Mark()

        # Mixer Loads
        self.Kelvin_Load()
        self.Pole_Load()
        self.Linear_Load()

        # Pin
        self.Pin_Load( self.pin_color )
    def Connection( self ):
        #region Layout

        # Panel Mask
        self.layout.f3_live.toggled.connect( self.Live_F3 )
        self.layout.f2_live.toggled.connect( self.Live_F2 )
        self.layout.f1_live.toggled.connect( self.Live_F1 )
        self.layout.d6_live.toggled.connect( self.Live_D6 )
        self.layout.d5_live.toggled.connect( self.Live_D5 )
        self.layout.d4_live.toggled.connect( self.Live_D4 )
        self.layout.d3_live.toggled.connect( self.Live_D3 )
        self.layout.d2_live.toggled.connect( self.Live_D2 )
        self.layout.d1_live.toggled.connect( self.Live_D1 )
        self.layout.b3_live.toggled.connect( self.Live_B3 )
        self.layout.b2_live.toggled.connect( self.Live_B2 )
        self.layout.b1_live.toggled.connect( self.Live_B1 )
        self.layout.mask_reset.clicked.connect( self.Mask_Reset )

        # GRAY
        self.layout.gray_1_value.valueChanged.connect( self.Channel_GRAY_1_Value )
        # RGB
        self.layout.srgb_1_value.valueChanged.connect( self.Channel_SRGB_1_Value )
        self.layout.srgb_2_value.valueChanged.connect( self.Channel_SRGB_2_Value )
        self.layout.srgb_3_value.valueChanged.connect( self.Channel_SRGB_3_Value )
        # LRGB
        self.layout.lrgb_1_value.valueChanged.connect( self.Channel_LRGB_1_Value )
        self.layout.lrgb_2_value.valueChanged.connect( self.Channel_LRGB_2_Value )
        self.layout.lrgb_3_value.valueChanged.connect( self.Channel_LRGB_3_Value )
        # CMYK
        self.layout.cmyk_1_value.valueChanged.connect( self.Channel_CMYK_1_Value )
        self.layout.cmyk_2_value.valueChanged.connect( self.Channel_CMYK_2_Value )
        self.layout.cmyk_3_value.valueChanged.connect( self.Channel_CMYK_3_Value )
        self.layout.cmyk_4_value.valueChanged.connect( self.Channel_CMYK_4_Value )
        # RYB
        self.layout.ryb_1_value.valueChanged.connect( self.Channel_RYB_1_Value )
        self.layout.ryb_2_value.valueChanged.connect( self.Channel_RYB_2_Value )
        self.layout.ryb_3_value.valueChanged.connect( self.Channel_RYB_3_Value )
        # YUV
        self.layout.yuv_1_value.valueChanged.connect( self.Channel_YUV_1_Value )
        self.layout.yuv_2_value.valueChanged.connect( self.Channel_YUV_2_Value )
        self.layout.yuv_3_value.valueChanged.connect( self.Channel_YUV_3_Value )
        # HSV
        self.layout.hsv_1_value.valueChanged.connect( self.Channel_HSV_1_Value )
        self.layout.hsv_2_value.valueChanged.connect( self.Channel_HSV_2_Value )
        self.layout.hsv_3_value.valueChanged.connect( self.Channel_HSV_3_Value )
        # HSL
        self.layout.hsl_1_value.valueChanged.connect( self.Channel_HSL_1_Value )
        self.layout.hsl_2_value.valueChanged.connect( self.Channel_HSL_2_Value )
        self.layout.hsl_3_value.valueChanged.connect( self.Channel_HSL_3_Value )
        # HCY
        self.layout.hcy_1_value.valueChanged.connect( self.Channel_HCY_1_Value )
        self.layout.hcy_2_value.valueChanged.connect( self.Channel_HCY_2_Value )
        self.layout.hcy_3_value.valueChanged.connect( self.Channel_HCY_3_Value )
        # ARD
        self.layout.ard_1_value.valueChanged.connect( self.Channel_ARD_1_Value )
        self.layout.ard_2_value.valueChanged.connect( self.Channel_ARD_2_Value )
        self.layout.ard_3_value.valueChanged.connect( self.Channel_ARD_3_Value )
        # XYZ
        self.layout.xyz_1_value.valueChanged.connect( self.Channel_XYZ_1_Value )
        self.layout.xyz_2_value.valueChanged.connect( self.Channel_XYZ_2_Value )
        self.layout.xyz_3_value.valueChanged.connect( self.Channel_XYZ_3_Value )
        # XYY
        self.layout.xyy_1_value.valueChanged.connect( self.Channel_XYY_1_Value )
        self.layout.xyy_2_value.valueChanged.connect( self.Channel_XYY_2_Value )
        self.layout.xyy_3_value.valueChanged.connect( self.Channel_XYY_3_Value )
        # LAB*
        self.layout.lab_1_value.valueChanged.connect( self.Channel_LAB_1_Value )
        self.layout.lab_2_value.valueChanged.connect( self.Channel_LAB_2_Value )
        self.layout.lab_3_value.valueChanged.connect( self.Channel_LAB_3_Value )
        # LCH
        self.layout.lch_1_value.valueChanged.connect( self.Channel_LCH_1_Value )
        self.layout.lch_2_value.valueChanged.connect( self.Channel_LCH_2_Value )
        self.layout.lch_3_value.valueChanged.connect( self.Channel_LCH_3_Value )
        # HEX
        self.layout.hex_string.returnPressed.connect( lambda: self.Color_HEX( self.layout.hex_string.text() ) )
        # Locks
        self.layout.cmyk_4_label.toggled.connect( self.Lock_CMYK_4 )

        # History
        self.layout.history_list.clicked.connect( self.History_Apply )

        # Footer
        self.layout.fill_pixel.toggled.connect( self.Menu_Fill )
        self.layout.settings.clicked.connect( self.Menu_Settings )

        #endregion
        #region Dialog Header

        self.dialog.ui_harmony.toggled.connect( self.UI_Harmony );  self.dialog.ui_harmony.setChecked( self.ui_harmony ); self.UI_Harmony( self.ui_harmony )
        self.dialog.ui_channel.toggled.connect( self.UI_Channel );  self.dialog.ui_channel.setChecked( self.ui_channel ); self.UI_Channel( self.ui_channel )
        self.dialog.ui_mixer.toggled.connect( self.UI_Mixer );      self.dialog.ui_mixer.setChecked( self.ui_mixer );     self.UI_Mixer( self.ui_mixer )
        self.dialog.ui_pin.toggled.connect( self.UI_Pin );          self.dialog.ui_pin.setChecked( self.ui_pin );         self.UI_Pin( self.ui_pin )
        self.dialog.ui_history.toggled.connect( self.UI_History );  self.dialog.ui_history.setChecked( self.ui_history ); self.UI_History( self.ui_history )

        #endregion
        #region Dialog Interface

        # Harmony
        self.dialog.harmony_rule.currentTextChanged.connect( self.Harmony_Rule ); self.dialog.harmony_rule.setCurrentText( self.harmony_rule ); self.Harmony_Rule( self.harmony_rule )
        self.dialog.harmony_edit.toggled.connect( self.Harmony_Edit );            self.dialog.harmony_edit.setChecked( self.harmony_edit );     self.Harmony_Edit( self.harmony_edit )
        # Panel
        self.dialog.panel_mode.currentTextChanged.connect( self.Panel_Mode );     self.dialog.panel_mode.setCurrentText( self.panel_mode );     self.Panel_Mode( self.panel_mode )
        self.dialog.wheel_mode.currentTextChanged.connect( self.Wheel_Mode );     self.dialog.wheel_mode.setCurrentText( self.wheel_mode );     self.Wheel_Mode( self.wheel_mode )
        self.dialog.wheel_space.currentTextChanged.connect( self.Wheel_Space );   self.dialog.wheel_space.setCurrentText( self.wheel_space );   self.Wheel_Space( self.wheel_space )
        self.dialog.hue_shape.currentTextChanged.connect( self.Hue_Shape );       self.dialog.hue_shape.setCurrentText( self.hue_shape );       self.Hue_Shape( self.hue_shape )
        self.dialog.gamut_mask.currentTextChanged.connect( self.Gamut_Mask );     self.dialog.gamut_mask.setCurrentText( self.gamut_mask );     self.Gamut_Mask( self.gamut_mask )
        self.dialog.gamut_reset.clicked.connect( self.Gamut_Reset )
        self.dialog.mask_folder.currentTextChanged.connect( self.Mask_Folder );   self.dialog.mask_folder.setCurrentText( self.mask_folder );   self.Mask_Folder( self.mask_folder )
        self.dialog.mask_edit.toggled.connect( self.Mask_Edit );                  self.dialog.mask_edit.setChecked( self.mask_edit );           self.Mask_Edit( self.mask_edit )
        # Mixer
        self.dialog.mixer_space.currentTextChanged.connect( self.Mixer_Space );   self.dialog.mixer_space.setCurrentText( self.mixer_space );   self.Mixer_Space( self.mixer_space )

        #endregion
        #region Dialog Color

        # Channel
        self.dialog.chan_gray.toggled.connect( self.Channel_GRAY_Display ); self.dialog.chan_gray.setChecked( self.color_view["gray"] ); self.Channel_GRAY_Display( self.color_view["gray"] )
        self.dialog.chan_srgb.toggled.connect( self.Channel_SRGB_Display ); self.dialog.chan_srgb.setChecked( self.color_view["srgb"] ); self.Channel_SRGB_Display( self.color_view["srgb"] )
        self.dialog.chan_lrgb.toggled.connect( self.Channel_LRGB_Display ); self.dialog.chan_lrgb.setChecked( self.color_view["lrgb"] ); self.Channel_LRGB_Display( self.color_view["lrgb"] )
        self.dialog.chan_cmyk.toggled.connect( self.Channel_CMYK_Display ); self.dialog.chan_cmyk.setChecked( self.color_view["cmyk"]);  self.Channel_CMYK_Display( self.color_view["cmyk"] )
        self.dialog.chan_ryb.toggled.connect( self.Channel_RYB_Display );   self.dialog.chan_ryb.setChecked( self.color_view["ryb"] );   self.Channel_RYB_Display( self.color_view["ryb"] )
        self.dialog.chan_yuv.toggled.connect( self.Channel_YUV_Display );   self.dialog.chan_yuv.setChecked( self.color_view["yuv"] );   self.Channel_YUV_Display( self.color_view["yuv"] )
        self.dialog.chan_hsv.toggled.connect( self.Channel_HSV_Display );   self.dialog.chan_hsv.setChecked( self.color_view["hsv"] );   self.Channel_HSV_Display( self.color_view["hsv"] )
        self.dialog.chan_hsl.toggled.connect( self.Channel_HSL_Display );   self.dialog.chan_hsl.setChecked( self.color_view["hsl"] );   self.Channel_HSL_Display( self.color_view["hsl"] )
        self.dialog.chan_hcy.toggled.connect( self.Channel_HCY_Display );   self.dialog.chan_hcy.setChecked( self.color_view["hcy"] );   self.Channel_HCY_Display( self.color_view["hcy"] )
        self.dialog.chan_ard.toggled.connect( self.Channel_ARD_Display );   self.dialog.chan_ard.setChecked( self.color_view["ard"] );   self.Channel_ARD_Display( self.color_view["ard"] )
        self.dialog.chan_xyz.toggled.connect( self.Channel_XYZ_Display );   self.dialog.chan_xyz.setChecked( self.color_view["xyz"] );   self.Channel_XYZ_Display( self.color_view["xyz"] )
        self.dialog.chan_xyy.toggled.connect( self.Channel_XYY_Display );   self.dialog.chan_xyy.setChecked( self.color_view["xyy"] );   self.Channel_XYY_Display( self.color_view["xyy"] )
        self.dialog.chan_lab.toggled.connect( self.Channel_LAB_Display );   self.dialog.chan_lab.setChecked( self.color_view["lab"] );   self.Channel_LAB_Display( self.color_view["lab"] )
        self.dialog.chan_lch.toggled.connect( self.Channel_LCH_Display );   self.dialog.chan_lch.setChecked( self.color_view["lch"] );   self.Channel_LCH_Display( self.color_view["lch"] )
        # Mixer
        self.dialog.mix_kelvin.toggled.connect( self.Mixer_KELVIN_Display ); self.dialog.mix_kelvin.setChecked( self.color_view["kelvin"] ); self.Mixer_KELVIN_Display( self.color_view["kelvin"] )
        self.dialog.mix_pole.toggled.connect( self.Mixer_POLE_Display );     self.dialog.mix_pole.setChecked( self.color_view["pole"] );     self.Mixer_POLE_Display( self.color_view["pole"] )
        self.dialog.mix_linear.toggled.connect( self.Mixer_LINEAR_Display ); self.dialog.mix_linear.setChecked( self.color_view["linear"] ); self.Mixer_LINEAR_Display( self.color_view["linear"] )

        # Ranges & Resets
        self.dialog.range_gray.valueChanged.connect( self.Channel_GRAY_Range ); self.dialog.reset_gray.clicked.connect( self.Channel_GRAY_Reset )
        self.dialog.range_srgb.valueChanged.connect( self.Channel_SRGB_Range ); self.dialog.reset_srgb.clicked.connect( self.Channel_SRGB_Reset )
        self.dialog.range_lrgb.valueChanged.connect( self.Channel_LRGB_Range ); self.dialog.reset_lrgb.clicked.connect( self.Channel_LRGB_Reset )
        self.dialog.range_cmyk.valueChanged.connect( self.Channel_CMYK_Range ); self.dialog.reset_cmyk.clicked.connect( self.Channel_CMYK_Reset )
        self.dialog.range_ryb.valueChanged.connect( self.Channel_RYB_Range );   self.dialog.reset_ryb.clicked.connect( self.Channel_RYB_Reset )
        self.dialog.range_yuv.valueChanged.connect( self.Channel_YUV_Range );   self.dialog.reset_yuv.clicked.connect( self.Channel_YUV_Reset )
        self.dialog.range_hue.valueChanged.connect( self.Channel_HUE_Range );   self.dialog.reset_hue.clicked.connect( self.Channel_HUE_Reset )
        self.dialog.range_hsv.valueChanged.connect( self.Channel_HSV_Range );   self.dialog.reset_hsv.clicked.connect( self.Channel_HSV_Reset )
        self.dialog.range_hsl.valueChanged.connect( self.Channel_HSL_Range );   self.dialog.reset_hsl.clicked.connect( self.Channel_HSL_Reset )
        self.dialog.range_hcy.valueChanged.connect( self.Channel_HCY_Range );   self.dialog.reset_hcy.clicked.connect( self.Channel_HCY_Reset )
        self.dialog.range_ard.valueChanged.connect( self.Channel_ARD_Range );   self.dialog.reset_ard.clicked.connect( self.Channel_ARD_Reset )
        self.dialog.range_xyz.valueChanged.connect( self.Channel_XYZ_Range );   self.dialog.reset_xyz.clicked.connect( self.Channel_XYZ_Reset )
        self.dialog.range_xyy.valueChanged.connect( self.Channel_XYY_Range );   self.dialog.reset_xyy.clicked.connect( self.Channel_XYY_Reset )
        self.dialog.range_lab.valueChanged.connect( self.Channel_LAB_Range );   self.dialog.reset_lab.clicked.connect( self.Channel_LAB_Reset )
        self.dialog.range_lch.valueChanged.connect( self.Channel_LCH_Range );   self.dialog.reset_lch.clicked.connect( self.Channel_LCH_Reset )

        # Format
        self.dialog.format_index.toggled.connect( self.Format_Label );       self.dialog.format_index.setChecked( self.format_index );       self.Format_Label( self.format_index )
        self.dialog.format_value.toggled.connect( self.Format_Value );       self.dialog.format_value.setChecked( self.format_value );       self.Format_Value( self.format_value )
        self.dialog.format_hueshine.toggled.connect( self.Format_Hueshine ); self.dialog.format_hueshine.setChecked( self.format_hueshine ); self.Format_Hueshine( self.format_hueshine)
        # Code
        self.dialog.code_hex.toggled.connect( self.Code_HEX_Display ); self.dialog.code_hex.setChecked( self.color_view["hex6"] ); self.Code_HEX_Display( self.color_view["hex6"] )
        self.dialog.code_sum.toggled.connect( self.Code_SUM_Display ); self.dialog.code_sum.setChecked( self.color_view["sum4"] ); self.Code_SUM_Display( self.color_view["sum4"] )

        #endregion
        #region Dialog Extras

        # Analyse
        self.dialog.analyse_document.clicked.connect( self.Analyse_Document )
        self.dialog.analyse_display.toggled.connect( self.Analyse_Display );  self.dialog.analyse_display.setChecked( self.analyse_display ); self.Analyse_Display( self.analyse_display )
        # Shortcut
        self.dialog.key_1_mode.currentTextChanged.connect( self.Key_1_Mode ); self.dialog.key_1_mode.setCurrentText( self.key_1_mode ); self.Key_1_Mode( self.key_1_mode )
        self.dialog.key_2_mode.currentTextChanged.connect( self.Key_2_Mode ); self.dialog.key_2_mode.setCurrentText( self.key_2_mode ); self.Key_2_Mode( self.key_2_mode )
        self.dialog.key_3_mode.currentTextChanged.connect( self.Key_3_Mode ); self.dialog.key_3_mode.setCurrentText( self.key_3_mode ); self.Key_3_Mode( self.key_3_mode )
        self.dialog.key_4_mode.currentTextChanged.connect( self.Key_4_Mode ); self.dialog.key_4_mode.setCurrentText( self.key_4_mode ); self.Key_4_Mode( self.key_4_mode )
        self.dialog.key_1_unit.valueChanged.connect( self.Key_1_Unit );       self.dialog.key_1_unit.setValue( self.key_1_unit );       self.Key_1_Unit( self.key_1_unit )
        self.dialog.key_2_unit.valueChanged.connect( self.Key_2_Unit );       self.dialog.key_2_unit.setValue( self.key_2_unit );       self.Key_2_Unit( self.key_2_unit )
        self.dialog.key_3_unit.valueChanged.connect( self.Key_3_Unit );       self.dialog.key_3_unit.setValue( self.key_3_unit );       self.Key_3_Unit( self.key_3_unit )
        self.dialog.key_4_unit.valueChanged.connect( self.Key_4_Unit );       self.dialog.key_4_unit.setValue( self.key_4_unit );       self.Key_4_Unit( self.key_4_unit )
        # Reference
        self.dialog.name_display.clicked.connect( self.Name_Display );
        self.dialog.name_closest.clicked.connect( self.Name_Closest )

        #endregion
        #region Dialog System

        # Color Space
        self.dialog.cs_luminosity.currentTextChanged.connect( self.CS_Luminosity ); self.dialog.cs_luminosity.setCurrentText( self.cs_luminosity ); self.CS_Luminosity( self.cs_luminosity )
        self.dialog.cs_matrix.currentTextChanged.connect( self.CS_Matrix ); self.dialog.cs_matrix.setCurrentText( self.cs_matrix ); self.CS_Matrix( self.cs_matrix )
        # Print
        self.dialog.printer.clicked.connect( self.Print_Button )
        # Performance
        self.dialog.performance_release.toggled.connect( self.Performace_Release ); self.dialog.performance_release.setChecked( self.performance_release ); self.Performace_Release( self.performance_release )
        # Notices
        self.dialog.manual.clicked.connect( self.Menu_Manual )
        self.dialog.license.clicked.connect( self.Menu_License )

        #endregion
        #region Instal Event Filter

        # Panel
        self.layout.panel_set.installEventFilter( self )
        self.layout.panel_mask.installEventFilter( self )
        # Channel
        self.layout.gray_slider.installEventFilter( self )
        self.layout.srgb_slider.installEventFilter( self )
        self.layout.lrgb_slider.installEventFilter( self )
        self.layout.cmyk_slider.installEventFilter( self )
        self.layout.ryb_slider.installEventFilter( self )
        self.layout.yuv_slider.installEventFilter( self )
        self.layout.hsv_slider.installEventFilter( self )
        self.layout.hsl_slider.installEventFilter( self )
        self.layout.hcy_slider.installEventFilter( self )
        self.layout.ard_slider.installEventFilter( self )
        self.layout.xyz_slider.installEventFilter( self )
        self.layout.xyy_slider.installEventFilter( self )
        self.layout.lab_slider.installEventFilter( self )
        self.layout.lch_slider.installEventFilter( self )
        # Sets
        self.layout.mixer_set.installEventFilter( self )
        self.layout.pin_set.installEventFilter( self )
        self.layout.history_set.installEventFilter( self )
        # History
        self.layout.history_list.installEventFilter( self )
        # Footer
        self.layout.mode.installEventFilter( self ) # Mode Index
        self.layout.settings.installEventFilter( self ) # Photoshoot

        #endregion
    def Extension( self ):
        # Install Extension for Pigmento Docker
        extension = Picker_Extension( parent = Krita.instance() )
        Krita.instance().addExtension( extension )
        # Connect Extension Signals
        extension.SIGNAL_PIN.connect( self.Extension_PIN )
        extension.SIGNAL_KEY.connect( self.Extension_KEY )
        extension.SIGNAL_LOCK.connect( self.Extension_LOCK )
    def Updater( self ):
        # QTimer
        self.qtimer_pulse = QtCore.QTimer( self )
        self.qtimer_pulse.timeout.connect( self.Krita_Read )
        # Mode
        self.Mode_Index( self.mode_index )

    #endregion
    #region Managment

    # Pigmento
    def Import_Sampler( self ):
        # Variables
        self.pigmento_sampler = None
        # Search Dockers
        docker_list = Krita.instance().dockers()
        for docker in docker_list:
            try: # Module Picker
                if docker.objectName() == self.pigmento_sampler_pyid:
                    self.pigmento_sampler = docker
                    break
            except:
                pass

    # Dictionanries
    def Dict_Copy( self, active, load ):
        keys = list( active.keys() )
        for k in keys:
            active[k] = load[k]
    # ZIP
    def Read_Zip( self, url ):
        list_qpixmap = list()
        try:
            if zipfile.is_zipfile( url ):
                archive = zipfile.ZipFile( url, "r" )
                name_list = archive.namelist()
                name_list.sort()
                for name in name_list:
                    # Archive
                    extract = archive.open( name )
                    image_data = extract.read()
                    # Buffer
                    byte_array = QByteArray( image_data )
                    buffer = QBuffer()
                    buffer.setData( byte_array )
                    buffer.open( QIODevice.OpenModeFlag.ReadOnly )
                    # Image
                    reader = QImageReader( buffer )
                    qpixmap = QPixmap().fromImageReader( reader )
                    list_qpixmap.append( qpixmap )
        except Exception as e:
            Message_Log( "ERROR", f"\n{ e }" )
        return list_qpixmap

    # Focus Event
    def Focus_Clear( self ):
        # GRAY
        self.layout.gray_1_value.clearFocus()
        # SRGB
        self.layout.srgb_1_value.clearFocus()
        self.layout.srgb_2_value.clearFocus()
        self.layout.srgb_3_value.clearFocus()
        # LRGB
        self.layout.lrgb_1_value.clearFocus()
        self.layout.lrgb_2_value.clearFocus()
        self.layout.lrgb_3_value.clearFocus()
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
        # HCY
        self.layout.hcy_1_value.clearFocus()
        self.layout.hcy_2_value.clearFocus()
        self.layout.hcy_3_value.clearFocus()
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
        # HEX
        self.layout.hex_string.clearFocus()
        self.layout.sum_string.clearFocus()

    # Resize Event
    def Size_Print( self ):
        widget = self
        width = widget.width()
        height = widget.height()
        Message_Log( "SIZE", f"{ width } x { height }" )
    def Size_Standard( self ):
        if self.isFloating() == True:
            self.resize( QSize( 500, 500 ) )
            self.Size_Update()
    def Size_Update( self ):
        # Size
        self.Header_Size()
        self.Panel_Size()
        self.Channel_Size()
        self.Mixer_Size()
        self.Pin_Size()
        # Cursor
        self.Sync_Elements( False, False, False )

    # Style
    def Style_Icon( self ):
        # Variables
        ki = Krita.instance()
        # Icons
        self.qicon_on               = ki.icon( "showColoring" )
        self.qicon_write            = ki.icon( "media-playback-start" )
        self.qicon_read             = ki.icon( "system-help" )
        self.qicon_off              = ki.icon( "showColoringOff" )
        self.qicon_fill_off         = ki.icon( "folder-documents" )
        self.qicon_fill_on          = ki.icon( "fillLayer" )
        self.qicon_sample_screen    = ki.icon( "sample-screen" )
        self.qicon_sampling_point   = ki.icon( "pivot-point" )
        self.qicon_settings         = ki.icon( "settings-button" )
        self.qicon_lock_layout      = ki.icon( "layer-locked" )
        self.qicon_lock_dialog      = ki.icon( "docker_lock_b" )
        self.qicon_none             = QIcon()
        # Widgets
        self.layout.fill_pixel.setIcon( self.qicon_fill_off )
        self.layout.sample_screen.setIcon( self.qicon_sample_screen )
        self.layout.settings.setIcon( self.qicon_settings )
    def Style_Tooltip( self ):
        # Tool Tips
        self.layout.mode.setToolTip( "Mode" )
        self.layout.fill_pixel.setToolTip( "Fill Pixel" )
        self.layout.sample_screen.setToolTip( "Sample Screen" )
        self.layout.hex_string.setToolTip( "Hex Code" )
        self.layout.settings.setToolTip( "Settings" )
    def Style_Theme( self ):
        """
        Theme Breeze Dark
        w_alternate     = #31363b
        w_base          = #232629
        w_button        = #31363b
        w_dark          = #1d2023
        w_light         = #464d54
        w_mid           = #2b3034
        w_midlight      = #3c4248
        w_shadow        = #151719
        w_tool_tip      = #31363b
        w_window        = #31363b
        t_bright        = #ffffff
        t_button        = #eff0f1
        t_highlighted   = #eff0f1
        t_placeholder   = #eff0f1
        t_text          = #eff0f1
        t_tool_tip      = #eff0f1
        t_window        = #eff0f1
        c_highlight     = #3daee9
        c_link          = #2980b9
        c_visited       = #7f8c8d

        Theme Breeze Ligh
        w_alternate     = #f8f7f6
        w_base          = #fcfcfc
        w_button        = #eff0f1
        w_dark          = #888e93
        w_light         = #ffffff
        w_mid           = #c4c8cc
        w_midlight      = #f6f7f7
        w_shadow        = #474a4c
        w_tool_tip      = #fcfcfc
        w_window        = #eff0f1
        t_bright        = #ffffff
        t_button        = #31363b
        t_highlighted   = #fcfcfc
        t_placeholder   = #31363b
        t_text          = #31363b
        t_tool_tip      = #31363b
        t_window        = #31363b
        c_highlight     = #3daee9
        c_link          = #0057ae
        c_visited       = #452886
        """

        # Read
        palette = QApplication.palette()
        # Window
        w_alternate   = palette.alternateBase().color().name()
        w_base        = palette.base().color().name()
        w_button      = palette.button().color().name()
        w_dark        = palette.dark().color().name()
        w_light       = palette.light().color().name()
        w_mid         = palette.mid().color().name()
        w_midlight    = palette.midlight().color().name()
        w_shadow      = palette.shadow().color().name()
        w_tool_tip    = palette.toolTipBase().color().name()
        w_window      = palette.window().color().name()
        # Text
        t_bright      = palette.brightText().color().name()
        t_button      = palette.buttonText().color().name()
        t_highlighted = palette.highlightedText().color().name()
        t_placeholder = palette.placeholderText().color().name()
        t_text        = palette.text().color().name()
        t_tool_tip    = palette.toolTipText().color().name()
        t_window      = palette.windowText().color().name()
        # Color
        c_highlight   = palette.highlight().color().name()
        c_link        = palette.link().color().name()
        c_visited     = palette.linkVisited().color().name()
        # c_accent      = palette.accent().color().name() # qt6

        # Colors
        win = palette.window().color().getHsvF()
        hue = palette.highlight().color().getHsvF()
        m2 = +0.03; m3 = -0.03
        if win[2] > 0.5:    d2 = +0.20; d3 = -0.05 # Light Theme
        else:               d2 = +0.10; d3 = +0.10 # Dark Theme
        backdrop = QColor().fromHsvF( win[0], win[1] + 0,  win[2] - 0.05 ).name()
        menu     = QColor().fromHsvF( hue[0], win[1] + m2, win[2] + m3 ).name()
        dim      = QColor().fromHsvF( hue[0], win[1] + d2, win[2] + d3 ).name()

        # Harmony
        self.layout.color_header.setStyleSheet( "#color_header{ background-color: " + backdrop + "; }" )
        self.layout.harmony_swatch.setStyleSheet( "#harmony_swatch{ background-color: " + backdrop + "; }" )
        self.layout.harmony_span.setStyleSheet( "#harmony_span{ background-color: " + backdrop + "; }" )

        # Panels
        self.panel_hue_circle.Set_Theme( t_window, w_window )
        self.panel_gamut.Set_Theme( t_window, w_window )
        self.panel_hexagon.Set_Theme( t_window, w_window )
        self.panel_plane.Set_Theme( dim )
        self.panel_mask.Set_Theme( w_midlight, w_dark )

        # Panel Backgrounds
        self.layout.panel_fill.setStyleSheet( "#panel_fill{ background-color: " + backdrop + "; }" )
        self.layout.panel_square.setStyleSheet( "#panel_square{ background-color: " + backdrop + "; }" )
        self.layout.panel_hue_circle.setStyleSheet( "#panel_hue_circle{ background-color: " + backdrop + "; }" )
        self.layout.panel_gamut.setStyleSheet( "#panel_gamut{ background-color: " + backdrop + "; }" )
        self.layout.panel_hexagon.setStyleSheet( "#panel_hexagon{ background-color: " + backdrop + "; }" )
        self.layout.panel_luma.setStyleSheet( "#panel_luma{ background-color: " + backdrop + "; }" )
        self.layout.panel_mask.setStyleSheet( "#panel_mask{ background-color: " + backdrop + "; }" )
        self.layout.panel_plane.setStyleSheet( "#panel_plane{ background-color: " + backdrop + "; }" )

        # GRAY
        self.gray_1_slider.Set_Theme( t_window, backdrop )
        # SRGB
        self.srgb_1_slider.Set_Theme( t_window, backdrop )
        self.srgb_2_slider.Set_Theme( t_window, backdrop )
        self.srgb_3_slider.Set_Theme( t_window, backdrop )
        # LRGB
        self.lrgb_1_slider.Set_Theme( t_window, backdrop )
        self.lrgb_2_slider.Set_Theme( t_window, backdrop )
        self.lrgb_3_slider.Set_Theme( t_window, backdrop )
        # CMYK
        self.cmyk_1_slider.Set_Theme( t_window, backdrop )
        self.cmyk_2_slider.Set_Theme( t_window, backdrop )
        self.cmyk_3_slider.Set_Theme( t_window, backdrop )
        self.cmyk_4_slider.Set_Theme( t_window, backdrop )
        # RYB
        self.ryb_1_slider.Set_Theme( t_window, backdrop )
        self.ryb_2_slider.Set_Theme( t_window, backdrop )
        self.ryb_3_slider.Set_Theme( t_window, backdrop )
        # YUV
        self.yuv_1_slider.Set_Theme( t_window, backdrop )
        self.yuv_2_slider.Set_Theme( t_window, backdrop )
        self.yuv_3_slider.Set_Theme( t_window, backdrop )
        # HSV
        self.hsv_1_slider.Set_Theme( t_window, backdrop )
        self.hsv_2_slider.Set_Theme( t_window, backdrop )
        self.hsv_3_slider.Set_Theme( t_window, backdrop )
        # HSL
        self.hsl_1_slider.Set_Theme( t_window, backdrop )
        self.hsl_2_slider.Set_Theme( t_window, backdrop )
        self.hsl_3_slider.Set_Theme( t_window, backdrop )
        # HCY
        self.hcy_1_slider.Set_Theme( t_window, backdrop )
        self.hcy_2_slider.Set_Theme( t_window, backdrop )
        self.hcy_3_slider.Set_Theme( t_window, backdrop )
        # ARD
        self.ard_1_slider.Set_Theme( t_window, backdrop )
        self.ard_2_slider.Set_Theme( t_window, backdrop )
        self.ard_3_slider.Set_Theme( t_window, backdrop )
        # XYZ
        self.xyz_1_slider.Set_Theme( t_window, backdrop )
        self.xyz_2_slider.Set_Theme( t_window, backdrop )
        self.xyz_3_slider.Set_Theme( t_window, backdrop )
        # XYY
        self.xyy_1_slider.Set_Theme( t_window, backdrop )
        self.xyy_2_slider.Set_Theme( t_window, backdrop )
        self.xyy_3_slider.Set_Theme( t_window, backdrop )
        # LAB
        self.lab_1_slider.Set_Theme( t_window, backdrop )
        self.lab_2_slider.Set_Theme( t_window, backdrop )
        self.lab_3_slider.Set_Theme( t_window, backdrop )
        # LCH
        self.lch_1_slider.Set_Theme( t_window, backdrop )
        self.lch_2_slider.Set_Theme( t_window, backdrop )
        self.lch_3_slider.Set_Theme( t_window, backdrop )

        # Kelvin
        self.kelvin_slider.Set_Theme( t_window, backdrop )
        self.pole_slider.Set_Theme( t_window, backdrop )
        self.linear_slider.Set_Theme( t_window, backdrop )

        # Pin
        for widget in self.pin_widget:
            widget.setStyleSheet( "#" + widget.objectName() + "{background-color: " + backdrop + ";}" )

        # History
        self.layout.history_list.setStyleSheet( "#history_list{background-color: " + backdrop + ";}" )

        # Icons
        self.layout.fill_pixel.setStyleSheet( "#fill_pixel::checked{ background-color : " + w_light + "; }" )
        self.layout.sample_screen.setStyleSheet( "#sample_screen::clicked{ background-color : " + w_light + "; }" )

        # Dialog Header
        self.dialog.ui_harmony.setStyleSheet( "#ui_harmony::checked{ background-color : " + dim + "; }" )
        self.dialog.ui_channel.setStyleSheet( "#ui_channel::checked{ background-color : " + dim + "; }" )
        self.dialog.ui_mixer.setStyleSheet( "#ui_mixer::checked{ background-color : " + dim + "; }" )
        self.dialog.ui_pin.setStyleSheet( "#ui_pin::checked{ background-color : " + dim + "; }" )
        self.dialog.ui_history.setStyleSheet( "#ui_history::checked{ background-color : " + dim + "; }" )

        # Style Sheets Dialog
        self.dialog.scroll_area_contents_interface.setStyleSheet( "#scroll_area_contents_interface{background-color: " + menu + ";}" )
        self.dialog.scroll_area_contents_color.setStyleSheet( "#scroll_area_contents_color{background-color: " + menu + ";}" )
        self.dialog.scroll_area_contents_extra.setStyleSheet( "#scroll_area_contents_extra{background-color: " + menu + ";}" )
        self.dialog.scroll_area_contents_system.setStyleSheet( "#scroll_area_contents_system{background-color: " + menu + ";}" )
        # Progressbar
        progress_style_sheet = self.Style_ProgressBar( c_highlight, "#00000000" )
        self.layout.progress_bar.setStyleSheet( progress_style_sheet )
        self.dialog.progress_bar.setStyleSheet( progress_style_sheet )
    def Style_ProgressBar( self, percentage, background ):
        style_sheet = str()
        style_sheet += "QProgressBar { background-color: " + background + "; border-radius: 0px; }"
        style_sheet += "QProgressBar::chunk { background-color: " + percentage + "; }"
        return style_sheet

    # Random
    def Random_Channels( self ):
        time_seed = time.time()
        random.seed( time_seed )
        c1 = random.randrange( 0, 255, 1 ) / 255
        c2 = random.randrange( 0, 255, 1 ) / 255
        c3 = random.randrange( 0, 255, 1 ) / 255
        return c1, c2, c3

    #endregion
    #region API

    # Read
    def API_Request_FG( self ):
        self.Update_WhenInvisible()
        return kfc
    def API_Request_BG( self ):
        self.Update_WhenInvisible()
        return kbc
    def API_Request_Wheel_Space( self ):
        self.Update_WhenInvisible()
        return self.wheel_space
    def Update_WhenInvisible( self ):
        if self.layout.isVisible() == False:
            self.Krita_Read()

    # Convert
    def API_Color_Name( self, hex_code ):
        name = self.convert.hex6_to_name( hex_code, color_name )
        return name
    def API_Color_Convert( self, mode, var_1, var_2, var_3, var_4, color ):
        convert = self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        return convert
    def API_Color_Interpolate( self, mode, color_l, color_r, factor ):
        # requires a pigmento color object
        interpolate = self.Color_Interpolate_2( mode, mode, color_l, color_r, factor )
        return interpolate
    # Write
    def API_Input_Preview( self, mode, var_1, var_2, var_3, var_4 ):
        # mode : color space
        # var : 0-1
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, self.color_index )
        self.Sync_Elements( False, True, False )
        return self.color_index
    def API_Input_Apply( self, mode, var_1, var_2, var_3, var_4 ):
        # mode : color space
        # var : 0-1
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, self.color_index )
        self.Sync_Elements( True, True, True )
        return self.color_index
    def API_Image_Analyse( self, qimage ):
        try:
            report = True
            self.Analyse_Pixel( qimage )
        except:
            report = False
        return report

    # Script Examples
    def Krita_Sample_Script( self ):
        # Read Color
        """
        from krita import *

        color_fg = Krita.instance().activeWindow().activeView().foregroundColor()
        vfg = color_fg.componentsOrdered()
        r = vfg[0]
        g = vfg[1]
        b = vfg[2]

        print( "red " + str( r ) )
        print( "green " + str( g ) )
        print( "blue " + str( b ) )
        """

        # Write Color
        """
        from krita import *

        n_cm = Krita.instance().activeDocument().colorModel()
        n_cd = Krita.instance().activeDocument().colorDepth()
        n_cp = Krita.instance().activeDocument().colorProfile()

        managed_color = ManagedColor( n_cm, n_cd, n_cp )
        comp = managed_color.components()
        red   = 0.4
        green = 0.5
        blue  = 0.6
        alpha = 1
        comp = [blue, green, red, alpha]
        managed_color.setComponents( comp )
        Krita.instance().activeWindow().activeView().setForeGroundColor( managed_color )
        """

    #endregion
    #region ENGINE

    # Document
    def Document_Active( self ):
        # Active Node Types
        # type_layer = ["paintlayer", "grouplayer", "clonelayer", "vectorlayer", "filterlayer", "filllayer", "filelayer"]
        # type_mask = ["transparencymask", "filtermask", "colorizemask", "transformmask", "selectionmask"]
        try:
            # Instance
            ki = Krita.instance()
            aw = ki.activeWindow()
            av = aw.activeView()
            ad = ki.activeDocument()
            an = ad.activeNode()
            # Node
            n_cm = an.colorModel()
            n_cd = an.colorDepth()
            n_cp = an.colorProfile()
            n_uid = an.uniqueId()
            # Colors
            fgc = av.foregroundColor() # ManagedColor
            bgc = av.backgroundColor() # ManagedColor
            # Others
            vc = av.canvas()
            vi = self.Vector_Index( an )
            cmodel = self.Color_Model_Index( n_cm )
            # Create List
            document = {
                "n_cm"      : n_cm,
                "n_cd"      : n_cd,
                "n_cp"      : n_cp,
                "n_uid"     : n_uid,
                "fgc"       : fgc,
                "bgc"       : bgc,
                "vc"        : vc,
                "vi"        : vi,
                "cmodel"    : cmodel,
                }
        except:
            document = self.Document_None()
        return document
    def Document_None( self ):
        document = {
            "n_cm"      : "SRGB",
            "n_cd"      : "U8",
            "n_cp"      : None,
            "n_uid"     : None,
            "fgc"       : None,
            "bgc"       : None,
            "vc"        : None,
            "vi"        : 0,
            "cmodel"    : "SRGB",
            }
        return document
    def Vector_Index( self, node ):
        count = 0
        if node.type() == "vectorlayer":
            list_shape = node.shapes()
            for i in range( 0, len( list_shape ) ):
                if list_shape[i].isSelected():
                    count += 1
        return count
    def Color_Model_Index( self, mode ):
        color_model = "SRGB"
        if   mode == "A":                           color_model = "A"       # alpha
        elif mode == "GRAYA":                       color_model = "GRAY"    # grayscale
        elif mode == "RGBA" and self.kdepth == 255: color_model = "SRGB"
        elif mode == "RGBA" and self.kdepth != 255: color_model = "LRGB"
        elif mode == "CMYKA":                       color_model = "CMYK"
        elif mode == "YCbCrA":                      color_model = "YUV"
        elif mode == "XYZA":                        color_model = "XYZ"
        elif mode == "LABA":                        color_model = "LAB"
        return color_model

    # Krita and Pigmento
    def Krita_Read( self ):
        if self.kwrite == False:
            # Document
            kdocument = self.Document_Active()
            cmodel = kdocument["cmodel"]
            if self.kdocument != kdocument:
                self.kdocument = kdocument
                self.convert.Set_Document( cmodel, kdocument["n_cd"], kdocument["n_cp"] )
                self.color_header.Set_Vector( self.kdocument["vi"] )
            # Canvas
            if ( self.kcanvas != None ) and ( self.kview != None ):
                if ( self.mode_index == 0 ) or ( self.kdocument != kdocument ): self.Read_Color( kdocument )
                elif self.mode_index == 2:                                      self.Read_Only( kdocument )
                if self.Fill_Check( kdocument ) == False:                       self.Fill_None()
            else:
                self.kdepth = 255
                self.Fill_None()
    def Krita_Write( self, release ):
        if ( self.kcanvas != None ) and ( self.kview != None ):
            if self.mode_index in ( 0 , 1 ) and release == True:
                # Control
                self.kwrite = True
                # Check Eraser Mode ON or OFF
                eraser = Krita.instance().action( "erase_action" )
                # Current Document
                kdocument = self.Document_Active()
                n_cm   = kdocument["n_cm"]
                n_cd   = kdocument["n_cd"]
                n_cp   = kdocument["n_cp"]
                vc     = kdocument["vc"]
                cmodel = kdocument["cmodel"]
                # Managed Color
                if   self.ui_harmony == False:                              write = kfc
                elif self.ui_harmony == True and self.harmony_index == 1:   write = har_01
                elif self.ui_harmony == True and self.harmony_index == 2:   write = har_02
                elif self.ui_harmony == True and self.harmony_index == 3:   write = har_03
                elif self.ui_harmony == True and self.harmony_index == 4:   write = har_04
                elif self.ui_harmony == True and self.harmony_index == 5:   write = har_05
                self.Write_Color( cmodel, n_cm, n_cd, n_cp, vc, write, "FG" )
                self.Write_Color( cmodel, n_cm, n_cd, n_cp, vc, kbc, "BG" )
                # If Eraser was true, set it ON again
                if eraser.isChecked():
                    eraser.trigger()
                # Fill with Foreground Color
                if self.Fill_Check( kdocument ) == True: Krita.instance().action( "fill_selection_foreground_color_opacity" ).trigger()
                else:                                    self.Fill_None()
                # Control
                self.kwrite = False

    # Channel Read
    def Read_Color( self, kdocument, update=False ):
        if self.cursor_inside == False:
            # Pigment.o Colors
            pf = kfc
            pb = kbc
            if self.ui_harmony == True:
                if self.harmony_index == 1: pf = har_01
                if self.harmony_index == 2: pf = har_02
                if self.harmony_index == 3: pf = har_03
                if self.harmony_index == 4: pf = har_04
                if self.harmony_index == 5: pf = har_05
            # Depth
            self.depth_previous = self.color_index["uvd_3"]
            # Variables
            ki = Krita.instance()
            # Document
            cmodel = kdocument["cmodel"]
            n_cd   = kdocument["n_cd"]
            n_cp   = kdocument["n_cp"]
            fgc    = kdocument["fgc"]
            bgc    = kdocument["bgc"]
            vc     = kdocument["vc"]
            vi     = kdocument["vi"]
            # Check Eraser Mode ON or OFF
            eraser = ki.action( "erase_action" )

            # Krita Foreground Color
            if ( self.fgc != fgc != None ) and ( vi == 0 ) or ( update == True ):
                # Variables
                self.fgc = fgc
                fcm = self.Color_Model_Index( fgc.colorModel() )
                fgs = fgc.toQString().split()
                # Color Model
                if fcm == "A":
                    # Colors
                    k1 = float( fgs[1] ) # does not display range so it is inhereted
                    cf1, kf1 = self.Read_Channel( k1, pf["gray_1"], self.kdepth )
                    m1 = self.mix_index["gray_1"]
                    # Operation
                    if ( cf1 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( "GRAY", kf1, 0, 0, 0, pf )
                        self.Mixer_Neutral()
                        if kf1 != m1:
                            self.Mixer_Read()
                elif fcm == "GRAY":
                    # Colors
                    k1, self.kdepth = float( fgs[1] ), int( fgs[3] )
                    cf1, kf1 = self.Read_Channel( k1, pf["gray_1"], self.kdepth )
                    m1 = self.mix_index["gray_1"]
                    # Operation
                    if ( cf1 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( "GRAY", kf1, 0, 0, 0, pf )
                        self.Mixer_Neutral()
                        if kf1 != m1:
                            self.Mixer_Read()
                elif fcm == "CMYK":
                    # Colors
                    k1, k2, k3, k4, self.kdepth = float( fgs[1] ), float( fgs[3] ), float( fgs[5] ), float( fgs[7] ), int( fgs[9] )
                    cf1, kf1 = self.Read_Channel( k1, pf["cmyk_1"], self.kdepth )
                    cf2, kf2 = self.Read_Channel( k2, pf["cmyk_2"], self.kdepth )
                    cf3, kf3 = self.Read_Channel( k3, pf["cmyk_3"], self.kdepth )
                    cf4, kf4 = self.Read_Channel( k4, pf["cmyk_4"], self.kdepth )
                    m1 = self.mix_index["cmyk_1"]
                    m2 = self.mix_index["cmyk_2"]
                    m3 = self.mix_index["cmyk_3"]
                    m4 = self.mix_index["cmyk_4"]
                    # Operation
                    if ( cf1 == True ) or ( cf2 == True ) or ( cf3 == True ) or ( cf4 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( "CMYK", kf1, kf2, kf3, kf4, pf )
                        self.Mixer_Neutral()
                        if kf1 != m1 or kf2 != m2 or kf3 != m3 or kf4 != m4:
                            self.Mixer_Read()
                elif fcm in [ "SRGB", "LRGB", "YUV", "XYZ", "LAB" ]:
                    # Variables
                    if   fcm == "SRGB": s1, s2, s3 = "srgb_1", "srgb_2", "srgb_3"
                    elif fcm == "LRGB": s1, s2, s3 = "lrgb_1", "lrgb_2", "lrgb_3"
                    elif fcm == "YUV":  s1, s2, s3 = "yuv_1",  "yuv_2",  "yuv_3"
                    elif fcm == "XYZ":  s1, s2, s3 = "xyz_1",  "xyz_2",  "xyz_3"
                    elif fcm == "LAB":  s1, s2, s3 = "lab_1",  "lab_2",  "lab_3"
                    # Colors
                    k1, k2, k3, self.kdepth = float( fgs[1] ), float( fgs[3] ), float( fgs[5] ), int( fgs[7] )
                    cf1, kf1 = self.Read_Channel( k1, pf[s1], self.kdepth )
                    cf2, kf2 = self.Read_Channel( k2, pf[s2], self.kdepth )
                    cf3, kf3 = self.Read_Channel( k3, pf[s3], self.kdepth )
                    m1 = self.mix_index[s1]
                    m2 = self.mix_index[s2]
                    m3 = self.mix_index[s3]
                    # Operation
                    if ( cf1 == True ) or ( cf2 == True ) or ( cf3 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( fcm, kf1, kf2, kf3, 0, pf )
                        self.Mixer_Neutral()
                        if kf1 != m1 or kf2 != m2 or kf3 != m3:
                            self.Mixer_Read()
            # Krita Background Color
            elif ( self.bgc != bgc != None ) and ( vi == 0 ) or ( update == True ):
                # Variables
                self.bgc = bgc
                bcm = self.Color_Model_Index( bgc.colorModel() )
                bgs = bgc.toQString().split()
                # Color Model
                if bcm == "A":
                    # Colors
                    k1 = float( bgs[1] ) # does not display range so it is inhereted
                    cb1, kb1 = self.Read_Channel( k1, pb["gray_1"], self.kdepth )
                    # Operation
                    if ( cb1 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( "GRAY", kb1, 0, 0, 0, pb )
                elif bcm == "GRAY":
                    # Colors
                    k1, ka = float( bgs[1] ), int( bgs[3] )
                    cb1, kb1 = self.Read_Channel( k1, pb["gray_1"], ka )
                    # Operation
                    if ( cb1 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( "GRAY", kb1, 0, 0, 0, pb )
                elif bcm == "CMYK":
                    # Colors
                    k1, k2, k3, k4, ka = float( bgs[1] ), float( bgs[3] ), float( bgs[5] ), float( bgs[7] ), int( bgs[9] )
                    cb1, kb1 = self.Read_Channel( k1, pb["cmyk_1"], ka )
                    cb2, kb2 = self.Read_Channel( k2, pb["cmyk_2"], ka )
                    cb3, kb3 = self.Read_Channel( k3, pb["cmyk_3"], ka )
                    cb4, kb4 = self.Read_Channel( k4, pb["cmyk_4"], ka )
                    # Operation
                    if ( cb1 == True ) or ( cb2 == True ) or ( cb3 == True ) or ( cb4 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( "CMYK", kb1, kb2, kb3, kb4, pb )
                elif bcm in [ "SRGB", "LRGB", "YUV", "XYZ", "LAB" ]:
                    # Variables
                    if bcm == "SRGB":
                        s1 = "srgb_1"
                        s2 = "srgb_2"
                        s3 = "srgb_3"
                    elif bcm == "LRGB":
                        s1 = "lrgb_1"
                        s2 = "lrgb_2"
                        s3 = "lrgb_3"
                    elif bcm == "YUV":
                        s1 = "yuv_1"
                        s2 = "yuv_2"
                        s3 = "yuv_3"
                    elif bcm == "XYZ":
                        s1 = "xyz_1"
                        s2 = "xyz_2"
                        s3 = "xyz_3"
                    elif bcm == "LAB":
                        s1 = "lab_1"
                        s2 = "lab_2"
                        s3 = "lab_3"
                    # Colors
                    k1, k2, k3, ka = float( bgs[1] ), float( bgs[3] ), float( bgs[5] ), int( bgs[7] )
                    cb1, kb1 = self.Read_Channel( k1, pb[s1], ka )
                    cb2, kb2 = self.Read_Channel( k2, pb[s2], ka )
                    cb3, kb3 = self.Read_Channel( k3, pb[s3], ka )
                    # Operation
                    if ( cb1 == True ) or ( cb2 == True ) or ( cb3 == True ) or ( update == True ):
                        if not eraser.isChecked():
                            self.Pigmento_READ( bcm, kb1, kb2, kb3, 0, pb )
            # Krita Vector Color
            elif ( vi > 0 ) or ( update == True ):
                # Variables
                v = 255
                # Foreground Color
                vfg = fgc.colorForCanvas( vc )
                kf1 = vfg.redF()
                kf2 = vfg.greenF()
                kf3 = vfg.blueF()
                self.kdepth = vfg.alpha()
                # Background Color
                vbg = bgc.colorForCanvas( vc )
                kb1 = vbg.redF()
                kb2 = vbg.greenF()
                kb3 = vbg.blueF()
                # Range
                cf1 = kf1 != pf["srgb_1"]
                cf2 = kf2 != pf["srgb_2"]
                cf3 = kf3 != pf["srgb_3"]
                cb1 = kb1 != pb["srgb_1"]
                cb2 = kb2 != pb["srgb_2"]
                cb3 = kb3 != pb["srgb_3"]
                # Operation
                if ( cf1 == True ) or ( cf2 == True ) or ( cf3 == True ) or ( update == True ):
                    self.Pigmento_READ( cmodel, kf1, kf2, kf3, 0, pf )
                if ( cb1 == True ) or ( cb2 == True ) or ( cb3 == True ) or ( update == True ):
                    self.Pigmento_READ( cmodel, kb1, kb2, kb3, 0, pb )
    def Read_Only( self, kdocument ):
        # Variables
        fgc = kdocument["fgc"]
        bgc = kdocument["bgc"]
        k  = self.color_range["srgb_1"]
        # Document
        fcd = fgc.colorDepth()
        fcm = fgc.colorModel()
        fcp = fgc.colorProfile()
        fcc = fgc.colorForCanvas( self.kcanvas )
        bcd = fgc.colorDepth()
        bcm = fgc.colorModel()
        bcp = fgc.colorProfile()
        bcc = fgc.colorForCanvas( self.kcanvas )
        # Foreground Color
        vfg = fgc.componentsOrdered()
        len_vfg = len( vfg )
        if len_vfg == 2:
            f1 = vfg[0] * k
            f2 = vfg[1] * k
        if len_vfg == 4:
            f1 = vfg[0] * k
            f2 = vfg[1] * k
            f3 = vfg[2] * k
            f4 = vfg[3] * k
        if len_vfg == 5:
            f1 = vfg[0] * k
            f2 = vfg[1] * k
            f3 = vfg[2] * k
            f4 = vfg[3] * k
            f5 = vfg[4] * k
        # Background Color
        vbg = bgc.componentsOrdered()
        len_vbg = len( vbg )
        if len_vbg == 2:
            b1 = vbg[0] * k
            b2 = vbg[1] * k
        if len_vbg == 4:
            b1 = vbg[0] * k
            b2 = vbg[1] * k
            b3 = vbg[2] * k
            b4 = vbg[3] * k
        if len_vbg == 5:
            b1 = vbg[0] * k
            b2 = vbg[1] * k
            b3 = vbg[2] * k
            b4 = vbg[3] * k
            b5 = vbg[4] * k
        # String
        fstr = fgc.toQString()
        bstr = bgc.toQString()
        # XML
        fxml = str( fgc.toXML() )[:-1]
        bxml = str( bgc.toXML() )[:-1]
        # Print Debug
        try:
            QtCore.qDebug( f"KRITA COLOR ( { k } )" )
            # Document
            QtCore.qDebug( f"Document = { fcd } { fcm } { fcp } { fcc }" )
            QtCore.qDebug( f"Document = { bcd } { bcm } { bcp } { bcc }" )
            # Components Ordered
            if len_vfg == 2: QtCore.qDebug( f"f1 = { f1 }\nf2 = { f2 }" )
            if len_vfg == 4: QtCore.qDebug( f"f1 = { f1 }\nf2 = { f2 }\nf3 = { f3 }\nf4 = { f4 }" )
            if len_vfg == 5: QtCore.qDebug( f"f1 = { f1 }\nf2 = { f2 }\nf3 = { f3 }\nf4 = { f4 }\nf5 = { f5 }" )
            if len_vfg == 2: QtCore.qDebug( f"b1 = { b1 }\nb2 = { b2 }" )
            if len_vfg == 4: QtCore.qDebug( f"b1 = { b1 }\nb2 = { b2 }\nb3 = { b3 }\nb4 = { b4 }" )
            if len_vfg == 5: QtCore.qDebug( f"b1 = { b1 }\nb2 = { b2 }\nb3 = { b3 }\nb4 = { b4 }\nb5 = { b5 }" )
            # String
            QtCore.qDebug( f"fstr = { fstr }" )
            QtCore.qDebug( f"bstr = { bstr }" )
            # XML
            QtCore.qDebug( f"fxml = { fxml }" )
            QtCore.qDebug( f"bxml = { bxml }" )
            QtCore.qDebug( f"" )
        except:
            pass
    def Read_Channel( self, ki, pi, depth ):
        if depth < 1:
            check = False
            value = 0
        elif depth == 1:
            check = ki != pi
            value = ki
        elif depth > 1:
            check = ( ki < int( pi * depth ) ) or ( ki >= ( int( pi * depth ) + 1 ) )
            value = ki / depth
        return check, value
    # Channel Write
    def Write_Color( self, cmodel, n_cm, n_cd, n_cp, vc, color, side ):
        # Managed Colors
        managed_color, hex_display = self.Color_Managed( cmodel, n_cm, n_cd, n_cp, vc, color )
        # Color for Canvas
        color["display"] = hex_display
        # Operation
        if side == "FG":    Krita.instance().activeWindow().activeView().setForeGroundColor( managed_color )
        if side == "BG":    Krita.instance().activeWindow().activeView().setBackGroundColor( managed_color )

    # Mixer
    def Mixer_Neutral( self ):
        if self.kelvin_p != 0.5:    self.Kelvin_Reset()
        if self.pole_p   != 0.5:    self.Pole_Reset()
    def Mixer_Read( self ):
        if self.cursor_inside == False:
            self.Dict_Copy( self.mix_index, self.color_index )
            self.Mixer_Gradient()

    #endregion
    #region Path

    def Pigmento_SHOW( self, mode, var_1, var_2, var_3, var_4, color ):
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( False, True, False )
    def Pigmento_READ( self, mode, var_1, var_2, var_3, var_4, color ):
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( False, True, True )
    def Pigmento_APPLY( self, mode, var_1, var_2, var_3, var_4, color ):
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( True, True, True )
    def Pigmento_PRESS( self, mode, var_1, var_2, var_3, var_4, color ):
        self.Color_Convert( mode, var_1, var_2, var_3, var_4, color )
        self.Sync_Elements( not self.performance_release, True, False )
    def Pigmento_SYNC( self ):
        self.Sync_Elements( True, True, True )

    #endregion
    #region Color

    # Pigmento
    def Color_Harmony( self, span, hue_1, hue_2, hue_3, hue_4, hue_5 ):
        # Variables
        comp = 0.5
        angle_1 = 0
        angle_2 = 0
        angle_3 = 0
        angle_4 = 0
        angle_5 = 0

        # Wheel
        if self.wheel_mode == "DIGITAL": index = "hue_d"
        if self.wheel_mode == "ANALOG" : index = "hue_a"

        # Director Angle
        if self.harmony_index == 1: angulus = hue_1[ index ]
        if self.harmony_index == 2: angulus = hue_2[ index ]
        if self.harmony_index == 3: angulus = hue_3[ index ]
        if self.harmony_index == 4: angulus = hue_4[ index ]
        if self.harmony_index == 5: angulus = hue_5[ index ]

        # Rules
        if self.harmony_rule == harmony_5:
            if self.harmony_index == 1:
                angle_1 = angulus
                angle_2 = Limit_Looper( angulus + span * 0.25 , 1 )
                angle_3 = Limit_Looper( angulus + span * 0.50 , 1 )
                angle_4 = Limit_Looper( angulus + span * 0.75 , 1 )
                angle_5 = Limit_Looper( angulus + span * 1.00 , 1 )
            if self.harmony_index == 2:
                angle_1 = Limit_Looper( angulus - span * 0.25 , 1 )
                angle_2 = angulus
                angle_3 = Limit_Looper( angulus + span * 0.25 , 1 )
                angle_4 = Limit_Looper( angulus + span * 0.50 , 1 )
                angle_5 = Limit_Looper( angulus + span * 0.75 , 1 )
            if self.harmony_index == 3:
                angle_1 = Limit_Looper( angulus - span * 0.50 , 1 )
                angle_2 = Limit_Looper( angulus - span * 0.25 , 1 )
                angle_3 = angulus
                angle_4 = Limit_Looper( angulus + span * 0.25 , 1 )
                angle_5 = Limit_Looper( angulus + span * 0.50 , 1 )
            if self.harmony_index == 4:
                angle_1 = Limit_Looper( angulus - span * 0.75 , 1 )
                angle_2 = Limit_Looper( angulus - span * 0.50 , 1 )
                angle_3 = Limit_Looper( angulus - span * 0.25 , 1 )
                angle_4 = angulus
                angle_5 = Limit_Looper( angulus + span * 0.25 , 1 )
            if self.harmony_index == 5:
                angle_1 = Limit_Looper( angulus - span * 1.00 , 1 )
                angle_2 = Limit_Looper( angulus - span * 0.75 , 1 )
                angle_3 = Limit_Looper( angulus - span * 0.50 , 1 )
                angle_4 = Limit_Looper( angulus - span * 0.25 , 1 )
                angle_5 = angulus
        if self.harmony_rule == harmony_4:
            if self.harmony_index == 1:
                angle_1 = angulus
                angle_2 = Limit_Looper( angulus + span        , 1 )
                angle_3 = Limit_Looper( angulus + comp        , 1 )
                angle_4 = Limit_Looper( angulus + comp + span , 1 )
            if self.harmony_index == 2:
                angle_1 = Limit_Looper( angulus - span        , 1 )
                angle_2 = angulus
                angle_3 = Limit_Looper( angulus + comp - span , 1 )
                angle_4 = Limit_Looper( angulus + comp        , 1 )
            if self.harmony_index == 3:
                angle_1 = Limit_Looper( angulus + comp        , 1 )
                angle_2 = Limit_Looper( angulus + comp + span , 1 )
                angle_3 = angulus
                angle_4 = Limit_Looper( angulus + span        , 1 )
            if self.harmony_index == 4:
                angle_1 = Limit_Looper( angulus + comp - span , 1 )
                angle_2 = Limit_Looper( angulus + comp        , 1 )
                angle_3 = Limit_Looper( angulus - span        , 1 )
                angle_4 = angulus
            angle_5 = 0
        if self.harmony_rule == harmony_3:
            if self.harmony_index == 1:
                angle_1 = angulus
                angle_2 = Limit_Looper( angulus + comp - span * 0.50 , 1 )
                angle_3 = Limit_Looper( angulus + comp + span * 0.50 , 1 )
            if self.harmony_index == 2:
                angle_1 = Limit_Looper( angulus + comp + span * 0.50 , 1 )
                angle_2 = angulus
                angle_3 = Limit_Looper( angulus + span * 1.00        , 1 )
            if self.harmony_index == 3:
                angle_1 = Limit_Looper( angulus + comp - span * 0.50 , 1 )
                angle_2 = Limit_Looper( angulus - span * 1.00        , 1 )
                angle_3 = angulus
            angle_4 = 0
            angle_5 = 0
        if self.harmony_rule == harmony_2:
            if self.harmony_index == 1:
                angle_1 = angulus
                angle_2 = Limit_Looper( angulus + comp , 1 )
            if self.harmony_index == 2:
                angle_1 = Limit_Looper( angulus - comp , 1 )
                angle_2 = angulus
            angle_3 = 0
            angle_4 = 0
            angle_5 = 0
        if self.harmony_rule == harmony_1:
            if self.harmony_index in ( 1, 2, 3, 4, 5 ):
                angle_1 = angulus
                angle_2 = angulus
                angle_3 = angulus
                angle_4 = angulus
                angle_5 = angulus

        if self.wheel_mode == "ANALOG":
            angle_1 = self.convert.huea_to_hued( angle_1 )
            angle_2 = self.convert.huea_to_hued( angle_2 )
            angle_3 = self.convert.huea_to_hued( angle_3 )
            angle_4 = self.convert.huea_to_hued( angle_4 )
            angle_5 = self.convert.huea_to_hued( angle_5 )

        # Wheel Mode
        mode = self.wheel_space
        if self.panel_mode == panel_hexagon:   mode = "ARD"
        if self.panel_mode == panel_luma:      mode = "YUV"
        # Channels
        c1, c2, c3 = Space_Index( mode )

        if self.panel_mode == panel_luma:
            luma = self.color_index[c1]
            # Angulus no Edit
            if self.harmony_edit == False:
                y1, u1, v1 = self.convert.uv_to_hue( self.color_index[c1], self.color_index[c2], self.color_index[c3], angle_1 )
                y2, u2, v2 = self.convert.uv_to_hue( self.color_index[c1], self.color_index[c2], self.color_index[c3], angle_2 )
                y3, u3, v3 = self.convert.uv_to_hue( self.color_index[c1], self.color_index[c2], self.color_index[c3], angle_3 )
                y4, u4, v4 = self.convert.uv_to_hue( self.color_index[c1], self.color_index[c2], self.color_index[c3], angle_4 )
                y5, u5, v5 = self.convert.uv_to_hue( self.color_index[c1], self.color_index[c2], self.color_index[c3], angle_5 )
            # Angulus with Edit
            if self.harmony_edit == True:
                y1, u1, v1 = self.convert.uv_to_hue( har_01[c1], har_01[c2], har_01[c3], angle_1 )
                y2, u2, v2 = self.convert.uv_to_hue( har_02[c1], har_02[c2], har_02[c3], angle_2 )
                y3, u3, v3 = self.convert.uv_to_hue( har_03[c1], har_03[c2], har_03[c3], angle_3 )
                y4, u4, v4 = self.convert.uv_to_hue( har_04[c1], har_04[c2], har_04[c3], angle_4 )
                y5, u5, v5 = self.convert.uv_to_hue( har_05[c1], har_05[c2], har_05[c3], angle_5 )
            # Others
            if self.harmony_index != 1: self.Color_Convert( mode, luma, u1, v1, 0, har_01 )
            if self.harmony_index != 2: self.Color_Convert( mode, luma, u2, v2, 0, har_02 )
            if self.harmony_index != 3: self.Color_Convert( mode, luma, u3, v3, 0, har_03 )
            if self.harmony_index != 4: self.Color_Convert( mode, luma, u4, v4, 0, har_04 )
            if self.harmony_index != 5: self.Color_Convert( mode, luma, u5, v5, 0, har_05 )
            # Active
            if self.harmony_index == 1: self.Color_Convert( mode, luma, u1, v1, 0, har_01 )
            if self.harmony_index == 2: self.Color_Convert( mode, luma, u2, v2, 0, har_02 )
            if self.harmony_index == 3: self.Color_Convert( mode, luma, u3, v3, 0, har_03 )
            if self.harmony_index == 4: self.Color_Convert( mode, luma, u4, v4, 0, har_04 )
            if self.harmony_index == 5: self.Color_Convert( mode, luma, u5, v5, 0, har_05 )
        else:
            # Angulus no Edit
            if self.harmony_edit == False:
                # Others
                if self.harmony_index != 1: self.Color_Convert( mode, angle_1, self.color_index[c2], self.color_index[c3], 0, har_01 )
                if self.harmony_index != 2: self.Color_Convert( mode, angle_2, self.color_index[c2], self.color_index[c3], 0, har_02 )
                if self.harmony_index != 3: self.Color_Convert( mode, angle_3, self.color_index[c2], self.color_index[c3], 0, har_03 )
                if self.harmony_index != 4: self.Color_Convert( mode, angle_4, self.color_index[c2], self.color_index[c3], 0, har_04 )
                if self.harmony_index != 5: self.Color_Convert( mode, angle_5, self.color_index[c2], self.color_index[c3], 0, har_05 )
                # Active
                if self.harmony_index == 1: self.Color_Convert( mode, angle_1, self.color_index[c2], self.color_index[c3], 0, har_01 )
                if self.harmony_index == 2: self.Color_Convert( mode, angle_2, self.color_index[c2], self.color_index[c3], 0, har_02 )
                if self.harmony_index == 3: self.Color_Convert( mode, angle_3, self.color_index[c2], self.color_index[c3], 0, har_03 )
                if self.harmony_index == 4: self.Color_Convert( mode, angle_4, self.color_index[c2], self.color_index[c3], 0, har_04 )
                if self.harmony_index == 5: self.Color_Convert( mode, angle_5, self.color_index[c2], self.color_index[c3], 0, har_05 )
            # Angulus with Edit
            if self.harmony_edit == True:
                # Others
                if self.harmony_index != 1: self.Color_Convert( mode, angle_1, har_01[c2], har_01[c3], 0, har_01 )
                if self.harmony_index != 2: self.Color_Convert( mode, angle_2, har_02[c2], har_02[c3], 0, har_02 )
                if self.harmony_index != 3: self.Color_Convert( mode, angle_3, har_03[c2], har_03[c3], 0, har_03 )
                if self.harmony_index != 4: self.Color_Convert( mode, angle_4, har_04[c2], har_04[c3], 0, har_04 )
                if self.harmony_index != 5: self.Color_Convert( mode, angle_5, har_05[c2], har_05[c3], 0, har_05 )
                # Active
                if self.harmony_index == 1: self.Color_Convert( mode, angle_1, har_01[c2], har_01[c3], 0, har_01 )
                if self.harmony_index == 2: self.Color_Convert( mode, angle_2, har_02[c2], har_02[c3], 0, har_02 )
                if self.harmony_index == 3: self.Color_Convert( mode, angle_3, har_03[c2], har_03[c3], 0, har_03 )
                if self.harmony_index == 4: self.Color_Convert( mode, angle_4, har_04[c2], har_04[c3], 0, har_04 )
                if self.harmony_index == 5: self.Color_Convert( mode, angle_5, har_05[c2], har_05[c3], 0, har_05 )

        # Active ( cleanup )
        har_01[ "active" ] = True
        har_02[ "active" ] = True
        har_03[ "active" ] = True
        har_04[ "active" ] = True
        har_05[ "active" ] = True
    def Color_Convert( self, mode, var_1, var_2, var_3, var_4, color ):
        # cmyk calculation uses self.lock_cmyk_4
        # hue calculation uses self.wheel_mode

        #region Convert to RGB+XYZ

        # RGB Linear
        if mode == "GRAY":
            gray = [ var_1 ]
            srgb = [ gray[0], gray[0], gray[0] ]
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "SRGB":
            srgb = [ var_1, var_2, var_3 ]
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "LRGB":
            lrgb = [ var_1, var_2, var_3 ]
            srgb = self.convert.lrgb_to_srgb( lrgb[0], lrgb[1], lrgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "CMYK":
            cmyk = [ var_1, var_2, var_3, var_4 ]
            srgb = self.convert.cmyk_to_srgb( cmyk[0], cmyk[1], cmyk[2], cmyk[3] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "RYB":
            ryb = [ var_1, var_2, var_3 ]
            srgb = self.convert.ryb_to_srgb( ryb[0], ryb[1], ryb[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "YUV":
            yuv = [ var_1, var_2, var_3 ]
            srgb = self.convert.yuv_to_srgb( yuv[0], yuv[1], yuv[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        # RGB Hue
        if mode == "HSV":
            hsv = [ var_1, var_2, var_3 ]
            srgb = self.convert.hsv_to_srgb( hsv[0], hsv[1], hsv[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "HSL":
            hsl = [ var_1, var_2, var_3 ]
            srgb = self.convert.hsl_to_srgb( hsl[0], hsl[1], hsl[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "HCY":
            hcy = [ var_1, var_2, var_3 ]
            srgb = self.convert.hcy_to_srgb( hcy[0], hcy[1], hcy[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "ARD":
            ard = [ var_1, var_2, var_3 ]
            srgb = self.convert.ard_to_srgb( ard[0], ard[1], ard[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        # XYZ Linear
        if mode == "XYZ":
            xyz = [ var_1, var_2, var_3 ]
            lrgb = self.convert.xyz_to_lrgb( xyz[0], xyz[1], xyz[2] )
            srgb = self.convert.lrgb_to_srgb( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "XYY":
            xyy = [ var_1, var_2, var_3 ]
            xyz = self.convert.xyy_to_xyz( xyy[0], xyy[1], xyy[2] )
            lrgb = self.convert.xyz_to_lrgb( xyz[0], xyz[1], xyz[2] )
            srgb = self.convert.lrgb_to_srgb( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "LAB":
            lab = [ var_1, var_2, var_3 ]
            xyz = self.convert.lab_to_xyz( lab[0], lab[1], lab[2] )
            lrgb = self.convert.xyz_to_lrgb( xyz[0], xyz[1], xyz[2] )
            srgb = self.convert.lrgb_to_srgb( lrgb[0], lrgb[1], lrgb[2] )
        # XYZ Hue
        if mode == "LCH":
            lch = [ var_1, var_2, var_3 ]
            lab = self.convert.lch_to_lab( lch[0], lch[1], lch[2] )
            xyz = self.convert.lab_to_xyz( lab[0], lab[1], lab[2] )
            lrgb = self.convert.xyz_to_lrgb( xyz[0], xyz[1], xyz[2] )
            srgb = self.convert.lrgb_to_srgb( lrgb[0], lrgb[1], lrgb[2] )
        # Non Color
        if mode == "UVD":
            uvd = [ var_1, var_2, var_3 ]
            srgb = self.convert.uvd_to_srgb( uvd[0], uvd[1], uvd[2] )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        if mode == "KELVIN":
            kkk = self.convert.kelvin_to_srgb( var_4 )
            srgb = [ var_1 * kkk[0], var_2 * kkk[1], var_3 * kkk[2] ]
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
        # Hex
        if mode == "HEX":
            srgb = self.convert.hex6_to_srgb( var_1 )
            lrgb = self.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
            xyz = self.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )

        # Hue Digital
        hsx = [ "HSV", "HSL", "HCY", "ARD" ]
        if mode in hsx: hue_d = var_1
        else:           hue_d = self.convert.srgb_to_hue( srgb[0], srgb[1], srgb[2] )
        hue_a = self.convert.hued_to_huea( hue_d )
        self.convert.Set_Hue( hue_d )

        #endregion
        #region Convert RGB+XYZ into Other

        # Others
        if mode != "GRAY":
            gray = self.convert.srgb_to_gray( srgb[0], srgb[1], srgb[2] )
        if mode != "SRGB":
            pass
        if mode != "LRGB":
            pass
        if mode != "CMYK":
            key = None
            if self.lock_cmyk_4 == True:    key = color["cmyk_4"]
            cmyk = self.convert.srgb_to_cmyk( srgb[0], srgb[1], srgb[2], key )
        if mode != "RYB":
            ryb = self.convert.srgb_to_ryb( srgb[0], srgb[1], srgb[2] )
        if mode != "YUV":
            yuv = self.convert.srgb_to_yuv( srgb[0], srgb[1], srgb[2] )
        if mode != "HSV":
            hsv = self.convert.srgb_to_hsv( srgb[0], srgb[1], srgb[2] )
        if mode != "HSL":
            hsl = self.convert.srgb_to_hsl( srgb[0], srgb[1], srgb[2] )
        if mode != "HCY":
            hcy = self.convert.srgb_to_hcy( srgb[0], srgb[1], srgb[2] )
        if mode != "ARD":
            ard = self.convert.srgb_to_ard( srgb[0], srgb[1], srgb[2] )
        if mode != "XYZ":
            pass
        if mode != "XYY":
            xyy = self.convert.xyz_to_xyy( xyz[0], xyz[1], xyz[2] )
        if mode != "LAB":
            lab = self.convert.xyz_to_lab( xyz[0], xyz[1], xyz[2] )
        if mode != "LCH":
            lch = self.convert.lab_to_lch( lab[0], lab[1], lab[2] )
        if mode != "UVD":
            uvd = self.convert.srgb_to_uvd( srgb[0], srgb[1], srgb[2] )

        #endregion
        #region Variables

        # Description
        hex_code = self.convert.srgb_to_hex6( srgb[0], srgb[1], srgb[2] ) # HEX
        sum4 = self.convert.cmyk_to_sum( cmyk[0], cmyk[1], cmyk[2], cmyk[3] ) # Sum ( Total Ink Coverage )
        name = self.convert.hex6_to_name( hex_code, color_name ) # HTML color name
        color[ "hex6" ] = hex_code
        color[ "sum4" ] = sum4
        color[ "name" ] = name

        # RGB Depth Error Correction
        checkdepth = uvd[2] - self.depth_previous
        if ( checkdepth >= -( 1 / self.color_range["uvd_3"] ) and checkdepth <= ( 1 / self.color_range["uvd_3"] ) ):
            uvd[2] = self.depth_previous
            ard[2] = self.depth_previous

        # GRAY
        color[ "gray_1" ] = gray[0]
        # SRGB
        color[ "srgb_1" ] = srgb[0]
        color[ "srgb_2" ] = srgb[1]
        color[ "srgb_3" ] = srgb[2]
        # LRGB
        color[ "lrgb_1" ] = lrgb[0]
        color[ "lrgb_2" ] = lrgb[1]
        color[ "lrgb_3" ] = lrgb[2]
        # CMYK
        color[ "cmyk_1" ] = cmyk[0]
        color[ "cmyk_2" ] = cmyk[1]
        color[ "cmyk_3" ] = cmyk[2]
        color[ "cmyk_4" ] = cmyk[3]
        # RYB
        color[ "ryb_1" ] = ryb[0]
        color[ "ryb_2" ] = ryb[1]
        color[ "ryb_3" ] = ryb[2]
        # YUV
        color[ "yuv_1" ] = yuv[0]
        color[ "yuv_2" ] = yuv[1]
        color[ "yuv_3" ] = yuv[2]
        # HUE
        color[ "hue_d" ] = hue_d
        color[ "hue_a" ] = hue_a
        # HSV
        color[ "hsv_1" ] = hue_d
        color[ "hsv_2" ] = hsv[1]
        color[ "hsv_3" ] = hsv[2]
        # HSL
        color[ "hsl_1" ] = hue_d
        color[ "hsl_2" ] = hsl[1]
        color[ "hsl_3" ] = hsl[2]
        # HCY
        color[ "hcy_1" ] = hue_d
        color[ "hcy_2" ] = hcy[1]
        color[ "hcy_3" ] = hcy[2]
        # ARD
        color[ "ard_1" ] = hue_d
        color[ "ard_2" ] = ard[1]
        color[ "ard_3" ] = ard[2]
        # XYZ
        color[ "xyz_1" ] = xyz[0]
        color[ "xyz_2" ] = xyz[1]
        color[ "xyz_3" ] = xyz[2]
        # XYY
        color[ "xyy_1" ] = xyy[0]
        color[ "xyy_2" ] = xyy[1]
        color[ "xyy_3" ] = xyy[2]
        # LAB
        color[ "lab_1" ] = lab[0]
        color[ "lab_2" ] = lab[1]
        color[ "lab_3" ] = lab[2]
        # LCH
        color[ "lch_1" ] = lch[0]
        color[ "lch_2" ] = lch[1]
        color[ "lch_3" ] = lch[2]
        # UVD
        color[ "uvd_1" ] = uvd[0]
        color[ "uvd_2" ] = uvd[1]
        color[ "uvd_3" ] = uvd[2]

        # Header
        hex_display = color[ "hex6" ]
        if self.kcanvas != None and self.kview != None:
            cmodel = self.kdocument["cmodel"]
            n_cm   = self.kdocument["n_cm"]
            n_cd   = self.kdocument["n_cd"]
            n_cp   = self.kdocument["n_cp"]
            vc     = self.kdocument["vc"]
            managed_color, hex_display = self.Color_Managed( cmodel, n_cm, n_cd, n_cp, vc, color )
            del managed_color
        color["display"] = hex_display

        #endregion
        # Return
        return color
    def Color_HEX( self, hex_code ):
        try:
            # Variables
            check_null = ( hex_code == None or hex_code == "" )
            check_hex6 = self.HEX_Valid( hex_code, 6 )
            check_hex3 = self.HEX_Valid( hex_code, 3 )
            space = list( filter( None, re.findall( r"(GRAY|A|SRGB|LRGB|CMYK|RYB|YUV|HSV|HSL|HCY|ARD|XYZ|XYY|LAB|LCH)+", hex_code.upper() ) ) )
            if len( space ) > 0:    color_space = space[0].upper()
            else:                   color_space = None
            values = list( filter( None, re.findall( r"[0-9\.0-9]*", hex_code) ) )
            vector = len( values )

            # Logic
            if check_null == True: # Null == Black (r=0, g=0, b=0)
                self.Color_Convert( "SRGB", 0, 0, 0, 0, self.color_index )
                self.Sync_Elements( True, True, True )
            elif ( check_hex6 == True or check_hex3 == True ): # HEX format
                if hex_code.startswith( "#" ) == False: # correct nomenclature
                    hex_code = "#" + hex_code
                if ( check_hex6 == True and len( hex_code ) == 7 ): #123456
                    srgb = self.convert.hex6_to_srgb( hex_code )
                    self.Color_Convert( "SRGB", srgb[0], srgb[1], srgb[2], 0, self.color_index )
                    self.Sync_Elements( True, True, True )
                if ( check_hex3 == True and len( hex_code ) == 4 ): #123
                    srgb = self.convert.hex3_to_srgb( hex_code )
                    self.Color_Convert( "SRGB", srgb[0], srgb[1], srgb[2], 0, self.color_index )
                    self.Sync_Elements( True, True, True )
            elif ( vector == 1 and color_space in [ "A", "GRAY" ] ): # GRAY(100)
                self.Color_Convert( "GRAY", int( values[0] ) / 255, 0, 0, 0, self.color_index )
                self.Sync_Elements( True, True, True )
            elif ( vector == 3 and color_space in [ "SRGB", "LRGB", "RYB", "YUV", "XYZ", "XYY", "LAB", "LCH" ] ): # RGB(100, 100, 100)
                self.Color_Convert( color_space, int( values[0] ) / 255, int( values[1] ) / 255, int( values[2] ) / 255, 0, self.color_index )
                self.Sync_Elements( True, True, True )
            elif ( vector == 4 and color_space in [ "CMYK" ] ): # CMYK(100, 100, 100, 100)
                self.Color_Convert( "CMYK", int( values[0] ) / 255, int( values[1] ) / 255, int( values[2] ) / 255, int( values[3] ) / 255, self.color_index )
                self.Sync_Elements( True, True, True )
            elif ( vector == 3 and color_space in [ "HSV", "HSL","HCY", "ARD" ] ): # HSV(100, 100, 100)
                key = self.Color_Vector( color_space, self.color_range ) 
                var0 = int( values[0] ) / key[0]
                var1 = int( values[1] ) / key[1]
                var2 = int( values[2] ) / key[2]
                self.Color_Convert( color_space, var0, var1, var2, 0, self.color_index )
                self.Sync_Elements( True, True, True )
            else:# Red Green Blue
                # Variables
                name = hex_code.lower()
                item = list( color_name.items() )
                # Search Dictionary with color names
                for i in range( 0, len( item ) ):
                    key_i = item[i][0]
                    value_i = item[i][1]
                    for j in range( 0, len( value_i ) ):
                        value_ij = value_i[j].lower()
                        if value_ij == name:
                            self.Color_Convert( "HEX", key_i, 0, 0, 0, self.color_index )
                            self.Sync_Elements( True, True, True )
                            break
        except:
            Message_Log( "ERROR", "input value" )
    # Krita
    def Color_Managed( self, cmodel, n_cm, n_cd, n_cp, vc, index ):
        managed_color = None
        hex_display = "#4287f5"
        if ( self.kcanvas != None and self.kview != None ):
            managed_color = ManagedColor( n_cm, n_cd, n_cp )
            if   cmodel == "A":     components = [ index["gray_1"], 1 ]
            elif cmodel == "GRAY":  components = [ index["gray_1"], 1 ]
            elif cmodel == "SRGB":  components = [ index["srgb_3"], index["srgb_2"], index["srgb_1"], 1 ]
            elif cmodel == "LRGB":
                if n_cd == "U16":   components = [ index["lrgb_3"], index["lrgb_2"], index["lrgb_1"], 1 ]
                else:               components = [ index["lrgb_1"], index["lrgb_2"], index["lrgb_3"], 1 ]
            elif cmodel == "CMYK":  components = [ index["cmyk_1"], index["cmyk_2"], index["cmyk_3"], index["cmyk_4"], 1 ]
            elif cmodel == "YUV":   components = [ index["yuv_1"],  index["yuv_2"],  index["yuv_3"],  1 ] 
            elif cmodel == "XYZ":   components = [ index["xyz_1"],  index["xyz_2"],  index["xyz_3"],  1 ]
            elif cmodel == "LAB":   components = [ index["lab_1"],  index["lab_2"],  index["lab_3"],  1 ]
            managed_color.setComponents( components )
            qcolor = managed_color.colorForCanvas( vc )
            hex_display = qcolor.name()
        return managed_color, hex_display
    # Utility
    def Color_Vector( self, mode, color, pad=False ):
        # RGB Linear
        if mode in [ "A", "GRAY" ]: vector = [ color["gray_1"] ]
        elif mode == "SRGB":        vector = [ color["srgb_1"], color["srgb_2"], color["srgb_3"] ]
        elif mode == "LRGB":        vector = [ color["lrgb_1"], color["lrgb_2"], color["lrgb_3"] ]
        elif mode == "CMYK":        vector = [ color["cmyk_1"], color["cmyk_2"], color["cmyk_3"], color["cmyk_4"] ]
        elif mode == "RYB":         vector = [ color["ryb_1"],  color["ryb_2"],  color["ryb_3"] ]
        elif mode == "YUV":         vector = [ color["yuv_1"],  color["yuv_2"],  color["yuv_3"] ]
        # RGB Hue
        elif mode == "HSV":         vector = [ color["hsv_1"],  color["hsv_2"],  color["hsv_3"] ]
        elif mode == "HSL":         vector = [ color["hsl_1"],  color["hsl_2"],  color["hsl_3"] ]
        elif mode == "HCY":         vector = [ color["hcy_1"],  color["hcy_2"],  color["hcy_3"] ]
        elif mode == "ARD":         vector = [ color["ard_1"],  color["ard_2"],  color["ard_3"] ]
        # XYZ Linear
        elif mode == "XYZ":         vector = [ color["xyz_1"],  color["xyz_2"],  color["xyz_3"] ]
        elif mode == "XYY":         vector = [ color["xyy_1"],  color["xyy_2"],  color["xyy_3"] ]
        elif mode == "LAB":         vector = [ color["lab_1"],  color["lab_2"],  color["lab_3"] ]
        # XYZ Hue
        elif mode == "LCH":         vector = [ color["lch_1"],  color["lch_2"],  color["lch_3"] ]
        # Padding ( helps with color_convert and color_lerp )
        if pad == True and mode != "CMYK":          vector.extend( [ 0 ] )
        if pad == True and mode in [ "A", "GRAY" ]: vector.extend( [ 0, 0 ] )
        # Return
        return vector
    def Color_Interpolate_2( self, mode, color_l, color_r, factor ):
        color_l = self.Color_Vector( mode, color_l, True )
        color_r = self.Color_Vector( mode, color_r, True )
        lerp = self.convert.color_lerp( mode, color_l, color_r, factor )
        color = self.Color_Convert( mode, lerp[0], lerp[1], lerp[2], lerp[3], color_true.copy() )
        return color
    def Color_Interpolate_3( self, mode, color_l, color_n, color_r, factor ):
        # Parse
        color_l = self.Color_Vector( mode, color_l, True )
        color_n = self.Color_Vector( mode, color_n, True )
        color_r = self.Color_Vector( mode, color_r, True )
        if   factor == 0.5: lerp = color_n
        elif factor == 0:   lerp = color_l
        elif factor == 1:   lerp = color_r
        elif factor < 0.5:  lerp = self.convert.color_lerp( mode, color_l, color_n, 2 * factor )
        elif factor > 0.5:  lerp = self.convert.color_lerp( mode, color_n, color_r, 2 * ( factor - 0.5 ) )
        color = self.Color_Convert( mode, lerp[0], lerp[1], lerp[2], lerp[3], color_true.copy() )
        return color

    #endregion
    #region Syncronization

    # Sync
    def Sync_Elements( self, release, color_new, color_old ):
        # Signals
        self.Block_Channel( True )
        # Layout
        self.Krita_Write( release )
        # Header
        self.Header_Normal( color_new, color_old )
        self.Header_Harmony( har_01, har_02, har_03, har_04, har_05 )
        # Panel
        self.Panel_Cursor()
        self.Panel_Document( self.kdocument )        
        # Channel
        self.Channel_Cursor()
        self.Channel_Gradient()
        # Mixer
        self.Mixer_Cursor()
        self.Mixer_Gradient()
        # Pin
        self.Pin_Active()
        # History
        if color_old == True:
            self.History_List( self.color_index["display"] )
            self.HEX_Copy( self.color_index["hex6"] )
        # Code
        self.Code_Cursor()
        self.Reference_Name()
        # Signals
        self.Block_Channel( False )
        # Sampler Update ( only works when picker is visible )
        if self.pigmento_sampler != None:
            self.pigmento_sampler.API_Input_Color_Index( self.color_index )

    # Signals
    def Block_Channel( self, boolean ):
        # GRAY
        self.layout.gray_1_slider.blockSignals( boolean )
        self.layout.gray_1_value.blockSignals( boolean )
        # SRGB
        self.layout.srgb_1_slider.blockSignals( boolean )
        self.layout.srgb_2_slider.blockSignals( boolean )
        self.layout.srgb_3_slider.blockSignals( boolean )
        self.layout.srgb_1_value.blockSignals( boolean )
        self.layout.srgb_2_value.blockSignals( boolean )
        self.layout.srgb_3_value.blockSignals( boolean )
        # LRGB
        self.layout.lrgb_1_slider.blockSignals( boolean )
        self.layout.lrgb_2_slider.blockSignals( boolean )
        self.layout.lrgb_3_slider.blockSignals( boolean )
        self.layout.lrgb_1_value.blockSignals( boolean )
        self.layout.lrgb_2_value.blockSignals( boolean )
        self.layout.lrgb_3_value.blockSignals( boolean )
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
        # HCY
        self.layout.hcy_1_slider.blockSignals( boolean )
        self.layout.hcy_2_slider.blockSignals( boolean )
        self.layout.hcy_3_slider.blockSignals( boolean )
        self.layout.hcy_1_value.blockSignals( boolean )
        self.layout.hcy_2_value.blockSignals( boolean )
        self.layout.hcy_3_value.blockSignals( boolean )
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
    # Header
    def Header_Size( self ):
        self.color_header.Set_Size( self.layout.color_header.width(), self.layout.color_header.height() )
        if self.ui_harmony == True:
            self.harmony_swatch.Set_Size( self.layout.harmony_swatch.width(), self.layout.harmony_swatch.height() )
            self.harmony_span.Set_Size( self.layout.harmony_span.width(), self.layout.harmony_span.height() )
    def Header_Normal( self, new, old ):
        hex_code = "hex6"
        if ( self.kcanvas != None ) and ( self.kview != None ):
            hex_code = "display"
        # Display
        if new == True:
            if self.ui_harmony == True:
                if self.harmony_index == 1: self.color_header.Set_Color_F1( har_01[hex_code] )
                if self.harmony_index == 2: self.color_header.Set_Color_F1( har_02[hex_code] )
                if self.harmony_index == 3: self.color_header.Set_Color_F1( har_03[hex_code] )
                if self.harmony_index == 4: self.color_header.Set_Color_F1( har_04[hex_code] )
                if self.harmony_index == 5: self.color_header.Set_Color_F1( har_05[hex_code] )
            else:
                self.color_header.Set_Color_F1( kfc[ hex_code ] )
            self.color_header.Set_Color_B1( kbc[ hex_code ] )
        if old == True:
            if self.ui_harmony == True:
                if self.harmony_index == 1: self.color_header.Set_Color_F2( har_01[hex_code] )
                if self.harmony_index == 2: self.color_header.Set_Color_F2( har_02[hex_code] )
                if self.harmony_index == 3: self.color_header.Set_Color_F2( har_03[hex_code] )
                if self.harmony_index == 4: self.color_header.Set_Color_F2( har_04[hex_code] )
                if self.harmony_index == 5: self.color_header.Set_Color_F2( har_05[hex_code] )
            else:
                self.color_header.Set_Color_F2( kfc[hex_code] )
            self.color_header.Set_Color_B2( kbc[hex_code] )
        # Update
        if ( new == True ) and ( old == True ):
            self.zoom = False
            self.Label_String( "" )
    def Header_Harmony( self, har_01, har_02, har_03, har_04, har_05 ):
        if self.ui_harmony == True:
            if self.header_mode == "FG":
                self.Color_Harmony( self.harmony_amplitude, har_01, har_02, har_03, har_04, har_05 )
            self.Header_Rule()
            self.Header_Span()
    # Panel
    def Panel_Size( self ):
        if self.panel_mode == panel_fill:
            self.panel_fill.Set_Size( self.layout.panel_fill.width(), self.layout.panel_fill.height() )
        elif self.panel_mode == panel_square:
            self.panel_square.Set_Size( self.layout.panel_square.width(), self.layout.panel_square.height() )
        elif self.panel_mode == panel_hue:
            self.Panel_Hue_Size()
        elif self.panel_mode == panel_gamut:
            self.panel_gamut.Set_Size( self.layout.panel_gamut.width(), self.layout.panel_gamut.height() )
        elif self.panel_mode == panel_hexagon:
            uvd_hexagon = list( self.convert.uvd_hexagon( self.color_index["uvd_3"], 0.5, 0.5, -1 ) )
            self.panel_hexagon.Set_Size( self.layout.panel_hexagon.width(), self.layout.panel_hexagon.height(), uvd_hexagon )
        elif self.panel_mode == panel_luma:
            self.panel_luma.Set_Size( self.layout.panel_luma.width(), self.layout.panel_luma.height() )
        elif self.panel_mode == panel_plane:
            self.Panel_Plane_Gradient()
        elif self.panel_mode == panel_mask:
            self.panel_mask.Set_Size( self.layout.panel_mask.width(), self.layout.panel_mask.height() )
            for i in range( 0, len( self.mask_module ) ):
                self.mask_module[i].Set_Size( self.mask_widget[i].width(), self.mask_widget[i].height() )
    def Panel_Hue_Size( self ):
        # Widget
        width = self.layout.panel_hue_circle.width()
        height = self.layout.panel_hue_circle.height()
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
        if self.hue_shape == "NONE":
            # index = 0
            px = -10
            py = -10
            pw = 10
            ph = 10
        if self.hue_shape == "TRIANGLE":
            # index = 0
            k = 0.07
            x = 0.28
            y1 = 0.13
            y2 = 2 * y1
            px = int( px + x * side )
            py = int( py + y1 * side + 1 )
            pw = int( side - x * side - k * side )
            ph = int( side - y2 * side )
        if self.hue_shape == "SQUARE":
            # index = 1
            k1 = 0.2
            k2 = 2 * k1
            px = int( px + k1 * side )
            py = int( py + k1 * side )
            pw = int( side - k2 * side )
            ph = int( side - k2 * side )
        if self.hue_shape == "DIAMOND":
            # index = 2
            k1 = 0.07
            k2 = 2 * k1
            px = int( px + k1 * side )
            py = int( py + k1 * side + 1 )
            pw = int( side - k2 * side )
            ph = int( side - k2 * side )
        # Geometry
        self.panel_hue_circle.Set_Size( width, height, self.hue_shape )
        self.layout.panel_hue_shape.setGeometry( px, py, pw, ph )
        self.panel_hue_shape.Set_Size( pw, ph )
    def Panel_Cursor( self ):
        # Place Cursor
        if   self.panel_mode == panel_fill:     self.Panel_Fill_Gradient()
        elif self.panel_mode == panel_square:   self.Panel_Square_Color()
        elif self.panel_mode == panel_hue:      self.Panel_Hue_Circle_Color(); self.Panel_Hue_Shape_Color()
        elif self.panel_mode == panel_gamut:    self.Panel_Gamut_Color()
        elif self.panel_mode == panel_hexagon:  self.Panel_Hexagon_Color()
        elif self.panel_mode == panel_luma:     self.Panel_Luma_Color()
        elif self.panel_mode == panel_plane:    pass
        elif self.panel_mode == panel_mask:     self.Panel_Mask_Live()
    def Panel_Document( self, kdocument ):
        kmodel = kdocument[ "cmodel" ]
        if kmodel in [ "A", "GRAY", "LRGB" ]: kmodel = "SRGB"
        if self.kmodel != kmodel:
            self.kmodel = kmodel
            self.Panel_Gradient( self.kmodel )
    def Panel_Gradient( self, kmodel ):
        self.Panel_Fill_Gradient()
        self.Panel_Square_Gradient( kmodel, self.wheel_space )
        self.Panel_Hue_Shape_Gradient( kmodel )
        self.Panel_Gamut_Gradient( kmodel, self.wheel_space, self.wheel_mode )
        self.Panel_Hexagon_Gradient( kmodel )
        self.Panel_Luma_Gradient( kmodel )
        self.Panel_Plane_Gradient()
        self.Panel_Mask_Gradient()
    # Channel
    def Channel_Size( self ):
        if self.ui_channel == True:
            # RGB Linear
            if self.color_view["gray"] == True:
                chan_width = self.layout.gray_1_slider.width()
                chan_height = self.layout.gray_1_slider.height()
                self.gray_1_slider.Set_Size( chan_width, chan_height )
            if self.color_view["srgb"] == True:
                chan_width = self.layout.srgb_1_slider.width()
                chan_height = self.layout.srgb_1_slider.height()
                self.srgb_1_slider.Set_Size( chan_width, chan_height )
                self.srgb_2_slider.Set_Size( chan_width, chan_height )
                self.srgb_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["lrgb"] == True:
                chan_width = self.layout.lrgb_1_slider.width()
                chan_height = self.layout.lrgb_1_slider.height()
                self.lrgb_1_slider.Set_Size( chan_width, chan_height )
                self.lrgb_2_slider.Set_Size( chan_width, chan_height )
                self.lrgb_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["cmyk"] == True:
                chan_width = self.layout.cmyk_1_slider.width()
                chan_height = self.layout.cmyk_1_slider.height()
                self.cmyk_1_slider.Set_Size( chan_width, chan_height )
                self.cmyk_2_slider.Set_Size( chan_width, chan_height )
                self.cmyk_3_slider.Set_Size( chan_width, chan_height )
                self.cmyk_4_slider.Set_Size( chan_width, chan_height )
            if self.color_view["ryb"] == True:
                chan_width = self.layout.ryb_1_slider.width()
                chan_height = self.layout.ryb_1_slider.height()
                self.ryb_1_slider.Set_Size( chan_width, chan_height )
                self.ryb_2_slider.Set_Size( chan_width, chan_height )
                self.ryb_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["yuv"] == True:
                chan_width = self.layout.yuv_1_slider.width()
                chan_height = self.layout.yuv_1_slider.height()
                self.yuv_1_slider.Set_Size( chan_width, chan_height )
                self.yuv_2_slider.Set_Size( chan_width, chan_height )
                self.yuv_3_slider.Set_Size( chan_width, chan_height )
            # RGB Circular
            if self.color_view["hsv"] == True:
                chan_width = self.layout.hsv_1_slider.width()
                chan_height = self.layout.hsv_1_slider.height()
                self.hsv_1_slider.Set_Size( chan_width, chan_height )
                self.hsv_2_slider.Set_Size( chan_width, chan_height )
                self.hsv_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["hsl"] == True:
                chan_width = self.layout.hsl_1_slider.width()
                chan_height = self.layout.hsl_1_slider.height()
                self.hsl_1_slider.Set_Size( chan_width, chan_height )
                self.hsl_2_slider.Set_Size( chan_width, chan_height )
                self.hsl_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["hcy"] == True:
                chan_width = self.layout.hcy_1_slider.width()
                chan_height = self.layout.hcy_1_slider.height()
                self.hcy_1_slider.Set_Size( chan_width, chan_height )
                self.hcy_2_slider.Set_Size( chan_width, chan_height )
                self.hcy_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["ard"] == True:
                chan_width = self.layout.ard_1_slider.width()
                chan_height = self.layout.ard_1_slider.height()
                self.ard_1_slider.Set_Size( chan_width, chan_height )
                self.ard_2_slider.Set_Size( chan_width, chan_height )
                self.ard_3_slider.Set_Size( chan_width, chan_height )
            # XYZ Linear
            if self.color_view["xyz"] == True:
                chan_width = self.layout.xyz_1_slider.width()
                chan_height = self.layout.xyz_1_slider.height()
                self.xyz_1_slider.Set_Size( chan_width, chan_height )
                self.xyz_2_slider.Set_Size( chan_width, chan_height )
                self.xyz_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["xyy"] == True:
                chan_width = self.layout.xyy_1_slider.width()
                chan_height = self.layout.xyy_1_slider.height()
                self.xyy_1_slider.Set_Size( chan_width, chan_height )
                self.xyy_2_slider.Set_Size( chan_width, chan_height )
                self.xyy_3_slider.Set_Size( chan_width, chan_height )
            if self.color_view["lab"] == True:
                chan_width = self.layout.lab_1_slider.width()
                chan_height = self.layout.lab_1_slider.height()
                self.lab_1_slider.Set_Size( chan_width, chan_height )
                self.lab_2_slider.Set_Size( chan_width, chan_height )
                self.lab_3_slider.Set_Size( chan_width, chan_height )
            # XYZ Circular
            if self.color_view["lch"] == True:
                chan_width = self.layout.lch_1_slider.width()
                chan_height = self.layout.lch_1_slider.height()
                self.lch_1_slider.Set_Size( chan_width, chan_height )
                self.lch_2_slider.Set_Size( chan_width, chan_height )
                self.lch_3_slider.Set_Size( chan_width, chan_height )
    def Channel_Cursor( self ):
        if self.ui_channel == True:
            # RGB Linear
            if self.color_view["gray"] == True:
                self.gray_1_slider.Set_Value( self.color_index["gray_1"] )
                self.layout.gray_1_value.setValue( self.color_index["gray_1"] * self.color_range["gray_1"] )
            if self.color_view["srgb"] == True:
                self.srgb_1_slider.Set_Value( self.color_index["srgb_1"] )
                self.srgb_2_slider.Set_Value( self.color_index["srgb_2"] )
                self.srgb_3_slider.Set_Value( self.color_index["srgb_3"] )
                self.layout.srgb_1_value.setValue( self.color_index["srgb_1"] * self.color_range["srgb_1"] )
                self.layout.srgb_2_value.setValue( self.color_index["srgb_2"] * self.color_range["srgb_2"] )
                self.layout.srgb_3_value.setValue( self.color_index["srgb_3"] * self.color_range["srgb_3"] )
            if self.color_view["lrgb"] == True:
                self.lrgb_1_slider.Set_Value( self.color_index["lrgb_1"] )
                self.lrgb_2_slider.Set_Value( self.color_index["lrgb_2"] )
                self.lrgb_3_slider.Set_Value( self.color_index["lrgb_3"] )
                self.layout.lrgb_1_value.setValue( self.color_index["lrgb_1"] * self.color_range["lrgb_1"] )
                self.layout.lrgb_2_value.setValue( self.color_index["lrgb_2"] * self.color_range["lrgb_2"] )
                self.layout.lrgb_3_value.setValue( self.color_index["lrgb_3"] * self.color_range["lrgb_3"] )
            if self.color_view["cmyk"] == True:
                self.cmyk_1_slider.Set_Value( self.color_index["cmyk_1"] )
                self.cmyk_2_slider.Set_Value( self.color_index["cmyk_2"] )
                self.cmyk_3_slider.Set_Value( self.color_index["cmyk_3"] )
                self.cmyk_4_slider.Set_Value( self.color_index["cmyk_4"] )
                self.layout.cmyk_1_value.setValue( self.color_index["cmyk_1"] * self.color_range["cmyk_1"] )
                self.layout.cmyk_2_value.setValue( self.color_index["cmyk_2"] * self.color_range["cmyk_2"] )
                self.layout.cmyk_3_value.setValue( self.color_index["cmyk_3"] * self.color_range["cmyk_3"] )
                self.layout.cmyk_4_value.setValue( self.color_index["cmyk_4"] * self.color_range["cmyk_4"] )
            if self.color_view["ryb"] == True:
                self.ryb_1_slider.Set_Value( self.color_index["ryb_1"] )
                self.ryb_2_slider.Set_Value( self.color_index["ryb_2"] )
                self.ryb_3_slider.Set_Value( self.color_index["ryb_3"] )
                self.layout.ryb_1_value.setValue( self.color_index["ryb_1"] * self.color_range["ryb_1"] )
                self.layout.ryb_2_value.setValue( self.color_index["ryb_2"] * self.color_range["ryb_2"] )
                self.layout.ryb_3_value.setValue( self.color_index["ryb_3"] * self.color_range["ryb_3"] )
            if self.color_view["yuv"] == True:
                self.yuv_1_slider.Set_Value( self.color_index["yuv_1"] )
                self.yuv_2_slider.Set_Value( self.color_index["yuv_2"] )
                self.yuv_3_slider.Set_Value( self.color_index["yuv_3"] )
                self.layout.yuv_1_value.setValue( self.color_index["yuv_1"] * self.color_range["yuv_1"] )
                self.layout.yuv_2_value.setValue( self.color_index["yuv_2"] * self.color_range["yuv_2"] )
                self.layout.yuv_3_value.setValue( self.color_index["yuv_3"] * self.color_range["yuv_3"] )
            # RGB Circular
            if self.color_view["hsv"] == True:
                self.hsv_1_slider.Set_Value( self.color_index["hsv_1"] )
                self.hsv_2_slider.Set_Value( self.color_index["hsv_2"] )
                self.hsv_3_slider.Set_Value( self.color_index["hsv_3"] )
                self.layout.hsv_1_value.setValue( self.color_index["hsv_1"] * self.color_range["hsv_1"] )
                self.layout.hsv_2_value.setValue( self.color_index["hsv_2"] * self.color_range["hsv_2"] )
                self.layout.hsv_3_value.setValue( self.color_index["hsv_3"] * self.color_range["hsv_3"] )
            if self.color_view["hsl"] == True:
                self.hsl_1_slider.Set_Value( self.color_index["hsl_1"] )
                self.hsl_2_slider.Set_Value( self.color_index["hsl_2"] )
                self.hsl_3_slider.Set_Value( self.color_index["hsl_3"] )
                self.layout.hsl_1_value.setValue( self.color_index["hsl_1"] * self.color_range["hsl_1"] )
                self.layout.hsl_2_value.setValue( self.color_index["hsl_2"] * self.color_range["hsl_2"] )
                self.layout.hsl_3_value.setValue( self.color_index["hsl_3"] * self.color_range["hsl_3"] )
            if self.color_view["hcy"] == True:
                self.hcy_1_slider.Set_Value( self.color_index["hcy_1"] )
                self.hcy_2_slider.Set_Value( self.color_index["hcy_2"] )
                self.hcy_3_slider.Set_Value( self.color_index["hcy_3"] )
                self.layout.hcy_1_value.setValue( self.color_index["hcy_1"] * self.color_range["hcy_1"] )
                self.layout.hcy_2_value.setValue( self.color_index["hcy_2"] * self.color_range["hcy_2"] )
                self.layout.hcy_3_value.setValue( self.color_index["hcy_3"] * self.color_range["hcy_3"] )
            if self.color_view["ard"] == True:
                self.ard_1_slider.Set_Value( self.color_index["ard_1"] )
                self.ard_2_slider.Set_Value( self.color_index["ard_2"] )
                self.ard_3_slider.Set_Value( self.color_index["ard_3"] )
                self.layout.ard_1_value.setValue( self.color_index["ard_1"] * self.color_range["ard_1"] )
                self.layout.ard_2_value.setValue( self.color_index["ard_2"] * self.color_range["ard_2"] )
                self.layout.ard_3_value.setValue( self.color_index["ard_3"] * self.color_range["ard_3"] )
            # XYZ Linear
            if self.color_view["xyz"] == True:
                self.xyz_1_slider.Set_Value( self.color_index["xyz_1"] )
                self.xyz_2_slider.Set_Value( self.color_index["xyz_2"] )
                self.xyz_3_slider.Set_Value( self.color_index["xyz_3"] )
                self.layout.xyz_1_value.setValue( self.color_index["xyz_1"] * self.color_range["xyz_1"] )
                self.layout.xyz_2_value.setValue( self.color_index["xyz_2"] * self.color_range["xyz_2"] )
                self.layout.xyz_3_value.setValue( self.color_index["xyz_3"] * self.color_range["xyz_3"] )
            if self.color_view["xyy"] == True:
                self.xyy_1_slider.Set_Value( self.color_index["xyy_1"] )
                self.xyy_2_slider.Set_Value( self.color_index["xyy_2"] )
                self.xyy_3_slider.Set_Value( self.color_index["xyy_3"] )
                self.layout.xyy_1_value.setValue( self.color_index["xyy_1"] * self.color_range["xyy_1"] )
                self.layout.xyy_2_value.setValue( self.color_index["xyy_2"] * self.color_range["xyy_2"] )
                self.layout.xyy_3_value.setValue( self.color_index["xyy_3"] * self.color_range["xyy_3"] )
            if self.color_view["lab"] == True:
                self.lab_1_slider.Set_Value( self.color_index["lab_1"] )
                self.lab_2_slider.Set_Value( self.color_index["lab_2"] )
                self.lab_3_slider.Set_Value( self.color_index["lab_3"] )
                self.layout.lab_1_value.setValue( self.color_index["lab_1"] * self.color_range["lab_1"] )
                self.layout.lab_2_value.setValue( self.color_index["lab_2"] * self.color_range["lab_2"] )
                self.layout.lab_3_value.setValue( self.color_index["lab_3"] * self.color_range["lab_3"] )
            # XYZ Circular
            if self.color_view["lch"] == True:
                self.lch_1_slider.Set_Value( self.color_index["lch_1"] )
                self.lch_2_slider.Set_Value( self.color_index["lch_2"] )
                self.lch_3_slider.Set_Value( self.color_index["lch_3"] )
                self.layout.lch_1_value.setValue( self.color_index["lch_1"] * self.color_range["lch_1"] )
                self.layout.lch_2_value.setValue( self.color_index["lch_2"] * self.color_range["lch_2"] )
                self.layout.lch_3_value.setValue( self.color_index["lch_3"] * self.color_range["lch_3"] )
    def Channel_Gradient( self ):
        if self.ui_channel == True:
            # RGB Linear
            if self.color_view["gray"] == True:
                gray_1 = self.Gradient_2( "GRAY", self.color_mark["gray_1"], [0], [1] )
                self.gray_1_slider.Set_Gradient( gray_1, 1 )
            if self.color_view["srgb"] == True:
                srgb_1 = self.Gradient_2( "SRGB", self.color_mark["srgb_1"], [0, self.color_index["srgb_2"], self.color_index["srgb_3"]], [1, self.color_index["srgb_2"], self.color_index["srgb_3"]] )
                srgb_2 = self.Gradient_2( "SRGB", self.color_mark["srgb_2"], [self.color_index["srgb_1"], 0, self.color_index["srgb_3"]], [self.color_index["srgb_1"], 1, self.color_index["srgb_3"]] )
                srgb_3 = self.Gradient_2( "SRGB", self.color_mark["srgb_3"], [self.color_index["srgb_1"], self.color_index["srgb_2"], 0], [self.color_index["srgb_1"], self.color_index["srgb_2"], 1] )
                self.srgb_1_slider.Set_Gradient( srgb_1, 1 )
                self.srgb_2_slider.Set_Gradient( srgb_2, 1 )
                self.srgb_3_slider.Set_Gradient( srgb_3, 1 )
            if self.color_view["lrgb"] == True:
                lrgb_1 = self.Gradient_2( "LRGB", self.color_mark["lrgb_1"], [0, self.color_index["lrgb_2"], self.color_index["lrgb_3"]], [1, self.color_index["lrgb_2"], self.color_index["lrgb_3"]] )
                lrgb_2 = self.Gradient_2( "LRGB", self.color_mark["lrgb_2"], [self.color_index["lrgb_1"], 0, self.color_index["lrgb_3"]], [self.color_index["lrgb_1"], 1, self.color_index["lrgb_3"]] )
                lrgb_3 = self.Gradient_2( "LRGB", self.color_mark["lrgb_3"], [self.color_index["lrgb_1"], self.color_index["lrgb_2"], 0], [self.color_index["lrgb_1"], self.color_index["lrgb_2"], 1] )
                self.lrgb_1_slider.Set_Gradient( lrgb_1, 1 )
                self.lrgb_2_slider.Set_Gradient( lrgb_2, 1 )
                self.lrgb_3_slider.Set_Gradient( lrgb_3, 1 )
            if self.color_view["cmyk"] == True:
                cmyk_1 = self.Gradient_2( "CMYK", self.color_mark["cmyk_1"], [0, self.color_index["cmyk_2"], self.color_index["cmyk_3"], self.color_index["cmyk_4"]], [1, self.color_index["cmyk_2"], self.color_index["cmyk_3"], self.color_index["cmyk_4"]] )
                cmyk_2 = self.Gradient_2( "CMYK", self.color_mark["cmyk_2"], [self.color_index["cmyk_1"], 0, self.color_index["cmyk_3"], self.color_index["cmyk_4"]], [self.color_index["cmyk_1"], 1, self.color_index["cmyk_3"], self.color_index["cmyk_4"]] )
                cmyk_3 = self.Gradient_2( "CMYK", self.color_mark["cmyk_3"], [self.color_index["cmyk_1"], self.color_index["cmyk_2"], 0, self.color_index["cmyk_4"]], [self.color_index["cmyk_1"], self.color_index["cmyk_2"], 1, self.color_index["cmyk_4"]] )
                cmyk_4 = self.Gradient_2( "CMYK", self.color_mark["cmyk_4"], [self.color_index["cmyk_1"], self.color_index["cmyk_2"], self.color_index["cmyk_3"], 0], [self.color_index["cmyk_1"], self.color_index["cmyk_2"], self.color_index["cmyk_3"], 1] )
                self.cmyk_1_slider.Set_Gradient( cmyk_1, 1 )
                self.cmyk_2_slider.Set_Gradient( cmyk_2, 1 )
                self.cmyk_3_slider.Set_Gradient( cmyk_3, 1 )
                self.cmyk_4_slider.Set_Gradient( cmyk_4, 1 )
            if self.color_view["ryb"] == True:
                ryb_1 = self.Gradient_2( "RYB", self.color_mark["ryb_1"], [0, self.color_index["ryb_2"], self.color_index["ryb_3"]], [1, self.color_index["ryb_2"], self.color_index["ryb_3"]] )
                ryb_2 = self.Gradient_2( "RYB", self.color_mark["ryb_2"], [self.color_index["ryb_1"], 0, self.color_index["ryb_3"]], [self.color_index["ryb_1"], 1, self.color_index["ryb_3"]] )
                ryb_3 = self.Gradient_2( "RYB", self.color_mark["ryb_3"], [self.color_index["ryb_1"], self.color_index["ryb_2"], 0], [self.color_index["ryb_1"], self.color_index["ryb_2"], 1] )
                self.ryb_1_slider.Set_Gradient( ryb_1, 1 )
                self.ryb_2_slider.Set_Gradient( ryb_2, 1 )
                self.ryb_3_slider.Set_Gradient( ryb_3, 1 )
            if self.color_view["yuv"] == True:
                yuv_1 = self.Gradient_2( "YUV", self.color_mark["yuv_1"], [0, self.color_index["yuv_2"], self.color_index["yuv_3"]], [1, self.color_index["yuv_2"], self.color_index["yuv_3"]] )
                yuv_2 = self.Gradient_2( "YUV", self.color_mark["yuv_2"], [self.color_index["yuv_1"], 0, self.color_index["yuv_3"]], [self.color_index["yuv_1"], 1, self.color_index["yuv_3"]] )
                yuv_3 = self.Gradient_2( "YUV", self.color_mark["yuv_3"], [self.color_index["yuv_1"], self.color_index["yuv_2"], 0], [self.color_index["yuv_1"], self.color_index["yuv_2"], 1] )
                self.yuv_1_slider.Set_Gradient( yuv_1, 1 )
                self.yuv_2_slider.Set_Gradient( yuv_2, 1 )
                self.yuv_3_slider.Set_Gradient( yuv_3, 1 )
            # RGB Hue
            if self.color_view["hsv"] == True:
                if self.format_hueshine == True:
                    hsv_1 = self.Gradient_2( "HSV", self.color_mark["hsv_1"], [0, 1, 1], [1, 1, 1] )
                else:
                    hsv_1 = self.Gradient_2( "HSV", self.color_mark["hsv_1"], [0, self.color_index["hsv_2"], self.color_index["hsv_3"]], [1, self.color_index["hsv_2"], self.color_index["hsv_3"]] )
                hsv_2 = self.Gradient_2( "HSV", self.color_mark["hsv_2"], [self.color_index["hsv_1"], 0, self.color_index["hsv_3"]], [self.color_index["hsv_1"], 1, self.color_index["hsv_3"]] )
                hsv_3 = self.Gradient_2( "HSV", self.color_mark["hsv_3"], [self.color_index["hsv_1"], self.color_index["hsv_2"], 0], [self.color_index["hsv_1"], self.color_index["hsv_2"], 1] )
                self.hsv_1_slider.Set_Gradient( hsv_1, 1 )
                self.hsv_2_slider.Set_Gradient( hsv_2, 1 )
                self.hsv_3_slider.Set_Gradient( hsv_3, 1 )
            if self.color_view["hsl"] == True:
                if self.format_hueshine == True:
                    hsl_1 = self.Gradient_2( "HSV", self.color_mark["hsl_1"], [0, 1, 1], [1, 1, 1] )
                else:
                    hsl_1 = self.Gradient_2( "HSL", self.color_mark["hsl_1"], [0, self.color_index["hsl_2"], self.color_index["hsl_3"]], [1, self.color_index["hsl_2"], self.color_index["hsl_3"]] )
                hsl_2 = self.Gradient_2( "HSL", self.color_mark["hsl_2"], [self.color_index["hsl_1"], 0, self.color_index["hsl_3"]], [self.color_index["hsl_1"], 1, self.color_index["hsl_3"]] )
                hsl_3 = self.Gradient_2( "HSL", self.color_mark["hsl_3"], [self.color_index["hsl_1"], self.color_index["hsl_2"], 0], [self.color_index["hsl_1"], self.color_index["hsl_2"], 1] )
                self.hsl_1_slider.Set_Gradient( hsl_1, 1 )
                self.hsl_2_slider.Set_Gradient( hsl_2, 1 )
                self.hsl_3_slider.Set_Gradient( hsl_3, 1 )
            if self.color_view["hcy"] == True:
                if self.format_hueshine == True:
                    hcy_1 = self.Gradient_2( "HSV", self.color_mark["hcy_1"], [0, 1, 1], [1, 1, 1] )
                else:
                    hcy_1 = self.Gradient_2( "HCY", self.color_mark["hcy_1"], [0, self.color_index["hcy_2"], self.color_index["hcy_3"]], [1, self.color_index["hcy_2"], self.color_index["hcy_3"]] )
                hcy_2 = self.Gradient_2( "HCY", self.color_mark["hcy_2"], [self.color_index["hcy_1"], 0, self.color_index["hcy_3"]], [self.color_index["hcy_1"], 1, self.color_index["hcy_3"]] )
                hcy_3 = self.Gradient_2( "HCY", self.color_mark["hcy_3"], [self.color_index["hcy_1"], self.color_index["hcy_2"], 0], [self.color_index["hcy_1"], self.color_index["hcy_2"], 1] )
                self.hcy_1_slider.Set_Gradient( hcy_1, 1 )
                self.hcy_2_slider.Set_Gradient( hcy_2, 1 )
                self.hcy_3_slider.Set_Gradient( hcy_3, 1 )
            if self.color_view["ard"] == True:
                if self.format_hueshine == True:
                    ard_1 = self.Gradient_2( "HSV", self.color_mark["ard_1"], [0, 1, 1], [1, 1, 1] )
                else:
                    ard_1 = self.Gradient_2( "ARD", self.color_mark["ard_1"], [0, self.color_index["ard_2"], self.color_index["ard_3"]], [1, self.color_index["ard_2"], self.color_index["ard_3"]] )
                ard_2 = self.Gradient_2( "ARD", self.color_mark["ard_2"], [self.color_index["ard_1"], 0, self.color_index["ard_3"]], [self.color_index["ard_1"], 1, self.color_index["ard_3"]] )
                ard_3 = self.Gradient_2( "ARD", self.color_mark["ard_3"], [self.color_index["ard_1"], self.color_index["ard_2"], 0], [self.color_index["ard_1"], self.color_index["ard_2"], 1] )
                self.ard_1_slider.Set_Gradient( ard_1, 1 )
                self.ard_2_slider.Set_Gradient( ard_2, 1 )
                self.ard_3_slider.Set_Gradient( ard_3, 1 )
            # XYZ Linear
            if self.color_view["xyz"] == True:
                xyz_1 = self.Gradient_2( "XYZ", self.color_mark["xyz_1"], [0, self.color_index["xyz_2"], self.color_index["xyz_3"]], [1, self.color_index["xyz_2"], self.color_index["xyz_3"]] )
                xyz_2 = self.Gradient_2( "XYZ", self.color_mark["xyz_2"], [self.color_index["xyz_1"], 0, self.color_index["xyz_3"]], [self.color_index["xyz_1"], 1, self.color_index["xyz_3"]] )
                xyz_3 = self.Gradient_2( "XYZ", self.color_mark["xyz_3"], [self.color_index["xyz_1"], self.color_index["xyz_2"], 0], [self.color_index["xyz_1"], self.color_index["xyz_2"], 1] )
                self.xyz_1_slider.Set_Gradient( xyz_1, 1 )
                self.xyz_2_slider.Set_Gradient( xyz_2, 1 )
                self.xyz_3_slider.Set_Gradient( xyz_3, 1 )
            if self.color_view["xyy"] == True:
                xyy_1 = self.Gradient_2( "XYY", self.color_mark["xyy_1"], [0, self.color_index["xyy_2"], self.color_index["xyy_3"]], [1, self.color_index["xyy_2"], self.color_index["xyy_3"]] )
                xyy_2 = self.Gradient_2( "XYY", self.color_mark["xyy_2"], [self.color_index["xyy_1"], 0, self.color_index["xyy_3"]], [self.color_index["xyy_1"], 1, self.color_index["xyy_3"]] )
                xyy_3 = self.Gradient_2( "XYY", self.color_mark["xyy_3"], [self.color_index["xyy_1"], self.color_index["xyy_2"], 0], [self.color_index["xyy_1"], self.color_index["xyy_2"], 1] )
                self.xyy_1_slider.Set_Gradient( xyy_1, 1 )
                self.xyy_2_slider.Set_Gradient( xyy_2, 1 )
                self.xyy_3_slider.Set_Gradient( xyy_3, 1 )
            if self.color_view["lab"] == True:
                lab_1 = self.Gradient_2( "LAB", self.color_mark["lab_1"], [0, self.color_index["lab_2"], self.color_index["lab_3"]], [1, self.color_index["lab_2"], self.color_index["lab_3"]] )
                lab_2 = self.Gradient_2( "LAB", self.color_mark["lab_2"], [self.color_index["lab_1"], 0, self.color_index["lab_3"]], [self.color_index["lab_1"], 1, self.color_index["lab_3"]] )
                lab_3 = self.Gradient_2( "LAB", self.color_mark["lab_3"], [self.color_index["lab_1"], self.color_index["lab_2"], 0], [self.color_index["lab_1"], self.color_index["lab_2"], 1] )
                self.lab_1_slider.Set_Gradient( lab_1, 1 )
                self.lab_2_slider.Set_Gradient( lab_2, 1 )
                self.lab_3_slider.Set_Gradient( lab_3, 1 )
            # XYZ Hue
            if self.color_view["lch"] == True:
                lch_1 = self.Gradient_2( "LCH", self.color_mark["lch_1"], [0, self.color_index["lch_2"], self.color_index["lch_3"]], [1, self.color_index["lch_2"], self.color_index["lch_3"]] )
                lch_2 = self.Gradient_2( "LCH", self.color_mark["lch_2"], [self.color_index["lch_1"], 0, self.color_index["lch_3"]], [self.color_index["lch_1"], 1, self.color_index["lch_3"]] )
                if self.format_hueshine == True:
                    lch_3 = self.Gradient_2( "HSV", self.color_mark["lch_3"], [0, 1, 1], [1, 1, 1] )
                else:
                    lch_3 = self.Gradient_2( "LCH", self.color_mark["lch_3"], [self.color_index["lch_1"], self.color_index["lch_2"], 0], [self.color_index["lch_1"], self.color_index["lch_2"], 1] )
                self.lch_1_slider.Set_Gradient( lch_1, 1 )
                self.lch_2_slider.Set_Gradient( lch_2, 1 )
                self.lch_3_slider.Set_Gradient( lch_3, 1 )
    def Channel_View( self ):
        self.Channel_GRAY_Display( self.color_view["gray"] )
        self.Channel_SRGB_Display( self.color_view["srgb"] )
        self.Channel_LRGB_Display( self.color_view["lrgb"] )
        self.Channel_CMYK_Display( self.color_view["cmyk"] )
        self.Channel_RYB_Display( self.color_view["ryb"] )
        self.Channel_YUV_Display( self.color_view["yuv"] )
        self.Channel_HSV_Display( self.color_view["hsv"] )
        self.Channel_HSL_Display( self.color_view["hsl"] )
        self.Channel_HCY_Display( self.color_view["hcy"] )
        self.Channel_ARD_Display( self.color_view["ard"] )
        self.Channel_XYZ_Display( self.color_view["xyz"] )
        self.Channel_XYY_Display( self.color_view["xyy"] )
        self.Channel_LAB_Display( self.color_view["lab"] )
        self.Channel_LCH_Display( self.color_view["lch"] )
    def Channel_Mark( self ):
        self.gray_1_slider.Set_Mark( self.color_mark["gray_1"] )
        self.srgb_1_slider.Set_Mark( self.color_mark["srgb_1"] )
        self.srgb_2_slider.Set_Mark( self.color_mark["srgb_2"] )
        self.srgb_3_slider.Set_Mark( self.color_mark["srgb_3"] )
        self.lrgb_1_slider.Set_Mark( self.color_mark["lrgb_1"] )
        self.lrgb_2_slider.Set_Mark( self.color_mark["lrgb_2"] )
        self.lrgb_3_slider.Set_Mark( self.color_mark["lrgb_3"] )
        self.cmyk_1_slider.Set_Mark( self.color_mark["cmyk_1"] )
        self.cmyk_2_slider.Set_Mark( self.color_mark["cmyk_2"] )
        self.cmyk_3_slider.Set_Mark( self.color_mark["cmyk_3"] )
        self.cmyk_4_slider.Set_Mark( self.color_mark["cmyk_4"] )
        self.ryb_1_slider.Set_Mark( self.color_mark["ryb_1"] )
        self.ryb_2_slider.Set_Mark( self.color_mark["ryb_2"] )
        self.ryb_3_slider.Set_Mark( self.color_mark["ryb_3"] )
        self.yuv_1_slider.Set_Mark( self.color_mark["yuv_1"] )
        self.yuv_2_slider.Set_Mark( self.color_mark["yuv_2"] )
        self.yuv_3_slider.Set_Mark( self.color_mark["yuv_3"] )
        self.hsv_1_slider.Set_Mark( self.color_mark["hsv_1"] )
        self.hsv_2_slider.Set_Mark( self.color_mark["hsv_2"] )
        self.hsv_3_slider.Set_Mark( self.color_mark["hsv_3"] )
        self.hsl_1_slider.Set_Mark( self.color_mark["hsl_1"] )
        self.hsl_2_slider.Set_Mark( self.color_mark["hsl_2"] )
        self.hsl_3_slider.Set_Mark( self.color_mark["hsl_3"] )
        self.hcy_1_slider.Set_Mark( self.color_mark["hcy_1"] )
        self.hcy_2_slider.Set_Mark( self.color_mark["hcy_2"] )
        self.hcy_3_slider.Set_Mark( self.color_mark["hcy_3"] )
        self.ard_1_slider.Set_Mark( self.color_mark["ard_1"] )
        self.ard_2_slider.Set_Mark( self.color_mark["ard_2"] )
        self.ard_3_slider.Set_Mark( self.color_mark["ard_3"] )
        self.xyz_1_slider.Set_Mark( self.color_mark["xyz_1"] )
        self.xyz_2_slider.Set_Mark( self.color_mark["xyz_2"] )
        self.xyz_3_slider.Set_Mark( self.color_mark["xyz_3"] )
        self.xyy_1_slider.Set_Mark( self.color_mark["xyy_1"] )
        self.xyy_2_slider.Set_Mark( self.color_mark["xyy_2"] )
        self.xyy_3_slider.Set_Mark( self.color_mark["xyy_3"] )
        self.lab_1_slider.Set_Mark( self.color_mark["lab_1"] )
        self.lab_2_slider.Set_Mark( self.color_mark["lab_2"] )
        self.lab_3_slider.Set_Mark( self.color_mark["lab_3"] )
        self.lch_1_slider.Set_Mark( self.color_mark["lch_1"] )
        self.lch_2_slider.Set_Mark( self.color_mark["lch_2"] )
        self.lch_3_slider.Set_Mark( self.color_mark["lch_3"] )
    def Channel_Range( self ):
        self.layout.gray_1_value.setMaximum( self.color_range["gray_1"] )
        self.layout.srgb_1_value.setMaximum( self.color_range["srgb_1"] )
        self.layout.srgb_2_value.setMaximum( self.color_range["srgb_2"] )
        self.layout.srgb_3_value.setMaximum( self.color_range["srgb_3"] )
        self.layout.lrgb_1_value.setMaximum( self.color_range["lrgb_1"] )
        self.layout.lrgb_2_value.setMaximum( self.color_range["lrgb_2"] )
        self.layout.lrgb_3_value.setMaximum( self.color_range["lrgb_3"] )
        self.layout.cmyk_1_value.setMaximum( self.color_range["cmyk_1"] )
        self.layout.cmyk_2_value.setMaximum( self.color_range["cmyk_2"] )
        self.layout.cmyk_3_value.setMaximum( self.color_range["cmyk_3"] )
        self.layout.cmyk_4_value.setMaximum( self.color_range["cmyk_4"] )
        self.layout.ryb_1_value.setMaximum( self.color_range["ryb_1"] )
        self.layout.ryb_2_value.setMaximum( self.color_range["ryb_2"] )
        self.layout.ryb_3_value.setMaximum( self.color_range["ryb_3"] )
        self.layout.yuv_1_value.setMaximum( self.color_range["yuv_1"] )
        self.layout.yuv_2_value.setMaximum( self.color_range["yuv_2"] )
        self.layout.yuv_3_value.setMaximum( self.color_range["yuv_3"] )
        self.layout.hsv_1_value.setMaximum( self.color_range["hsv_1"] )
        self.layout.hsv_2_value.setMaximum( self.color_range["hsv_2"] )
        self.layout.hsv_3_value.setMaximum( self.color_range["hsv_3"] )
        self.layout.hsl_1_value.setMaximum( self.color_range["hsl_1"] )
        self.layout.hsl_2_value.setMaximum( self.color_range["hsl_2"] )
        self.layout.hsl_3_value.setMaximum( self.color_range["hsl_3"] )
        self.layout.hcy_1_value.setMaximum( self.color_range["hcy_1"] )
        self.layout.hcy_2_value.setMaximum( self.color_range["hcy_2"] )
        self.layout.hcy_3_value.setMaximum( self.color_range["hcy_3"] )
        self.layout.ard_1_value.setMaximum( self.color_range["ard_1"] )
        self.layout.ard_2_value.setMaximum( self.color_range["ard_2"] )
        self.layout.ard_3_value.setMaximum( self.color_range["ard_3"] )
        self.layout.xyz_1_value.setMaximum( self.color_range["xyz_1"] )
        self.layout.xyz_2_value.setMaximum( self.color_range["xyz_2"] )
        self.layout.xyz_3_value.setMaximum( self.color_range["xyz_3"] )
        self.layout.xyy_1_value.setMaximum( self.color_range["xyy_1"] )
        self.layout.xyy_2_value.setMaximum( self.color_range["xyy_2"] )
        self.layout.xyy_3_value.setMaximum( self.color_range["xyy_3"] )
        self.layout.lab_1_value.setMaximum( self.color_range["lab_1"] )
        self.layout.lab_2_value.setMaximum( self.color_range["lab_2"] )
        self.layout.lab_3_value.setMaximum( self.color_range["lab_3"] )
        self.layout.lch_1_value.setMaximum( self.color_range["lch_1"] )
        self.layout.lch_2_value.setMaximum( self.color_range["lch_2"] )
        self.layout.lch_3_value.setMaximum( self.color_range["lch_3"] )
    # Mixer
    def Mixer_Size( self ):
        if self.ui_mixer == True:
            if self.color_view["kelvin"] == True:
                self.kelvin_pin_l.Set_Size( self.layout.kelvin_pin_l.width(), self.layout.kelvin_pin_l.height() )
                self.kelvin_pin_r.Set_Size( self.layout.kelvin_pin_r.width(), self.layout.kelvin_pin_r.height() )
                self.kelvin_slider.Set_Size( self.layout.kelvin_slider.width(), self.layout.kelvin_slider.height() )
            if self.color_view["pole"] == True:
                self.pole_pin_l.Set_Size( self.layout.pole_pin_l.width(), self.layout.pole_pin_l.height() )
                self.pole_pin_r.Set_Size( self.layout.pole_pin_r.width(), self.layout.pole_pin_r.height() )
                self.pole_slider.Set_Size( self.layout.pole_slider.width(), self.layout.pole_slider.height() )
            if self.color_view["linear"] == True:
                self.linear_pin_l.Set_Size( self.layout.linear_pin_l.width(), self.layout.linear_pin_l.height() )
                self.linear_pin_r.Set_Size( self.layout.linear_pin_r.width(), self.layout.linear_pin_r.height() )
                self.linear_slider.Set_Size( self.layout.linear_slider.width(), self.layout.linear_slider.height() )
    def Mixer_Cursor( self ):
        if self.ui_mixer == True:
            if self.color_view["kelvin"] == True:
                self.kelvin_slider.Set_Value( self.kelvin_p )
            if self.color_view["pole"] == True:
                self.pole_slider.Set_Value( self.pole_p )
            if self.color_view["linear"] == True:
                self.linear_slider.Set_Value( self.linear_p )
    def Mixer_Gradient( self ):
        if self.ui_mixer == True:
            if self.color_view["kelvin"] == True:
                kelvin = self.Gradient_Kelvin( self.color_mark["kelvin"], self.mix_index["srgb_1"], self.mix_index["srgb_2"], self.mix_index["srgb_3"] )
                self.kelvin_slider.Set_Gradient( kelvin, 1 )
            if self.color_view["pole"] == True:
                pl = self.Color_Vector( self.mixer_space, self.pole_l )
                pn = self.Color_Vector( self.mixer_space, self.mix_index )
                pr = self.Color_Vector( self.mixer_space, self.pole_r )
                pole = self.Gradient_3( self.mixer_space, self.color_mark["pole"], pl, pn, pr, True )
                alpha = int( self.pole_l["active"] * self.mix_index["active"] * self.pole_r["active"] )
                self.pole_slider.Set_Gradient( pole, alpha )
            if self.color_view["linear"] == True:
                ll = self.Color_Vector( self.mixer_space, self.linear_l )
                lr = self.Color_Vector( self.mixer_space, self.linear_r )
                linear = self.Gradient_2( self.mixer_space, self.color_mark["linear"], ll, lr, True )
                alpha = int( self.linear_l["active"] * self.linear_r["active"] )
                self.linear_slider.Set_Gradient( linear, alpha )
    def Mixer_Mark( self ):
        self.kelvin_slider.Set_Mark( self.color_mark["kelvin"] )
        self.pole_slider.Set_Mark( self.color_mark["pole"] )
        self.linear_slider.Set_Mark( self.color_mark["linear"] )
    # Pin
    def Pin_Size( self ):
        for i in range( 0, len( self.pin_module ) ):
            self.pin_module[i].Set_Size( self.pin_widget[i].width(), self.pin_widget[i].height() )
    def Pin_Active( self ):
        srgb_cor = self.color_index["display"]
        for i in range( 0, len( self.pin_color ) ):
            check_active = self.pin_color[i]["active"] == True and self.pin_color[i]["display"] == srgb_cor
            self.pin_module[i].Set_Active( check_active )
    # Code
    def Code_Cursor( self ):
        if self.color_view["hex6"] == True:
            hex_code = self.color_index["hex6"]
            self.layout.hex_string.setText( hex_code )
        if self.color_view["sum4"] == True:
            percentage = round( self.color_index["sum4"] * 100 )
            sum_text = "Σ" + str( percentage ).zfill(3)
            self.layout.sum_string.setText( sum_text )
    def Reference_Name( self ):
        self.dialog.name_display.setText( self.color_index["name"] )

    #endregion
    #region UI LAYOUT Header

    def Header_Swap( self ):
        list_key = list( kfc.keys() )
        for key in list_key:
            # kfc[key], kbc[key] = kbc[key], kfc[key]
            fg = kfc[key]
            bg = kbc[key]
            kfc[key] = bg
            kbc[key] = fg
        self.Pigmento_SYNC()
    def Header_Show( self, active ):
        # Show Foreground or Background Color
        if active == "FG":
            if self.ui_harmony == True:
                if   self.harmony_index == 1:   self.color_index = har_01
                elif self.harmony_index == 2:   self.color_index = har_02
                elif self.harmony_index == 3:   self.color_index = har_03
                elif self.harmony_index == 4:   self.color_index = har_04
                elif self.harmony_index == 5:   self.color_index = har_05
            else:
                self.color_index = kfc
        if active == "BG":
            self.color_index = kbc
        # Save Mode
        self.header_mode = active
        self.Pigmento_SYNC()
    def Header_Random( self ):
        c1, c2, c3 = self.Random_Channels()
        self.Pigmento_APPLY( "SRGB", c1, c2, c3, 0, self.color_index )
    def Header_Complementary( self ):
        # Wheel Mode
        if self.wheel_mode == "DIGITAL":    hue = Limit_Looper( self.color_index["hue_d"] + 0.5, 1 )
        if self.wheel_mode == "ANALOG":     hue = self.convert.huea_to_hued( Limit_Looper( self.color_index["hue_a"] + 0.5, 1 ) )
        # Wheel Space
        if self.wheel_space == "HSV":       self.Pigmento_APPLY( "HSV", hue, self.color_index["hsv_2"], self.color_index["hsv_3"], 0, self.color_index )
        if self.wheel_space == "HSL":       self.Pigmento_APPLY( "HSL", hue, self.color_index["hsl_2"], self.color_index["hsl_3"], 0, self.color_index )
        if self.wheel_space == "HCY":       self.Pigmento_APPLY( "HCY", hue, self.color_index["hcy_2"], self.color_index["hcy_3"], 0, self.color_index )
        if self.wheel_space == "ARD":       self.Pigmento_APPLY( "ARD", hue, self.color_index["ard_2"], self.color_index["ard_3"], 0, self.color_index )

    #endregion
    #region UI LAYOUT HARMONY

    # Signal
    def Harmony_Panel( self, harmony_index ):
        self.harmony_swatch.Update_Index( harmony_index )
        self.Harmony_Index( harmony_index )
    def Harmony_Index( self, harmony_index ):
        self.harmony_index = harmony_index
        if self.header_mode == "FG":
            if self.ui_harmony == True:
                if   self.harmony_index == 1:   self.color_index = har_01
                elif self.harmony_index == 2:   self.color_index = har_02
                elif self.harmony_index == 3:   self.color_index = har_03
                elif self.harmony_index == 4:   self.color_index = har_04
                elif self.harmony_index == 5:   self.color_index = har_05
            else:
                self.color_index = kfc
        if self.header_mode == "BG":
            self.color_index = kbc
        self.Pigmento_SYNC()
    def Harmony_Span( self, harmony_amplitude ):
        self.harmony_amplitude = harmony_amplitude
        self.Pigmento_SYNC()
        self.Label_String( f"{ round( self.harmony_amplitude * 360, 2 )}º" )

    # Dialog Set
    def Header_Rule( self ):
        if   self.harmony_rule == harmony_2: self.harmony_swatch.Set_Harmony_Parts( 2, [ har_01["hex6"], har_02["hex6"] ] )
        elif self.harmony_rule == harmony_3: self.harmony_swatch.Set_Harmony_Parts( 3, [ har_01["hex6"], har_02["hex6"], har_03["hex6"] ] )
        elif self.harmony_rule == harmony_4: self.harmony_swatch.Set_Harmony_Parts( 4, [ har_01["hex6"], har_02["hex6"], har_03["hex6"], har_04["hex6"] ] )
        else:                                self.harmony_swatch.Set_Harmony_Parts( 5, [ har_01["hex6"], har_02["hex6"], har_03["hex6"], har_04["hex6"], har_05["hex6"] ] )
    def Header_Span( self ):
        self.harmony_span.Update_Amplitude( self.harmony_amplitude )

    #endregion
    #region UI LAYOUT PANEL Fill

    # Update
    def Panel_Fill_Gradient( self ):
        self.panel_fill.Update_Gradient( self.color_index["display"] )

    #endregion
    #region UI LAYOUT PANEL Square

    # Update
    def Panel_Square_Color( self ):
        # Cursor
        self.panel_square.Update_Color( self.wheel_space, "SQUARE", self.color_index )
        # Harmony
        if self.ui_harmony == True and self.header_mode == "FG":
            if   self.harmony_rule == harmony_2: harmony_list = [ har_01, har_02 ]
            elif self.harmony_rule == harmony_3: harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == harmony_4: harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:                                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_square.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_square.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True: self.panel_square.Update_Pin( self.pin_color )
        else:                   self.panel_square.Update_Pin( None )
        # Analyze
        if self.analyse_display == True: self.panel_square.Update_Analyse( self.analyse_list )
        else:                            self.panel_square.Update_Analyse( None )
    def Panel_Square_Gradient( self, kmodel, space ):
        url = os.path.join( self.url_panel, f"{ kmodel }_{ space }_S4.zip" )
        list_gradient = self.Read_Zip( url )
        self.panel_square.Update_Gradient( list_gradient )
    # Signals
    def Panel_Square_Value( self, mode, v1, v2, v3 ):
        self.Color_Convert( mode, v1, v2, v3, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )

    #endregion
    #region UI LAYOUT PANEL Hue

    # Update
    def Panel_Hue_Circle_Color( self ):
        # Update
        self.panel_hue_circle.Update_Color( self.wheel_mode, self.wheel_space, self.color_index )
        # Harmony
        if self.ui_harmony == True and self.header_mode == "FG":
            if   self.harmony_rule == harmony_2: harmony_list = [ har_01, har_02 ]
            elif self.harmony_rule == harmony_3: harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == harmony_4: harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:                                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_hue_circle.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_hue_circle.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True: self.panel_hue_circle.Update_Pin( self.pin_color )
        else:                   self.panel_hue_circle.Update_Pin( None )
    def Panel_Hue_Circle_Gradient( self, kmodel ):
        list_gradient = list()
        for angle in range( 0, 360 ):
            if   self.wheel_space == "HSV": srgb = self.convert.hsv_to_srgb( angle/360, self.color_index["hsv_2"], self.color_index["hsv_3"] )
            elif self.wheel_space == "HSL": srgb = self.convert.hsl_to_srgb( angle/360, self.color_index["hsl_2"], self.color_index["hsl_3"] )
            elif self.wheel_space == "HCY": srgb = self.convert.hcy_to_srgb( angle/360, self.color_index["hcy_2"], self.color_index["hcy_3"] )
            elif self.wheel_space == "ARD": srgb = self.convert.ard_to_srgb( angle/360, self.color_index["ard_2"], self.color_index["ard_3"] )
            srgb = [ int( srgb[0] * 255 ), int( srgb[1] * 255 ), int( srgb[2] * 255 ) ]
            list_gradient.append( srgb )
        self.panel_hue_circle.Update_Gradient( list_gradient )
    # Signals
    def Panel_Hue_Circle_Angle( self, angle ):
        if self.wheel_mode == "ANALOG": angle = self.convert.huea_to_hued( angle )
        c1, c2, c3 = Space_Index( self.wheel_space )
        self.Color_Convert( self.wheel_space, angle, self.color_index[c2], self.color_index[c3], 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )

    # Update
    def Panel_Hue_Shape_Color( self ):
        # Variables
        color_space = "HSL"
        if self.hue_shape == "SQUARE":color_space = self.wheel_space
        # Update
        self.panel_hue_shape.Update_Color( color_space, self.hue_shape, self.color_index )
        # Harmony
        if self.ui_harmony == True and self.header_mode == "FG":
            if   self.harmony_rule == harmony_2: harmony_list = [ har_01, har_02 ]
            elif self.harmony_rule == harmony_3: harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == harmony_4: harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:                                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_hue_shape.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_hue_shape.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True: self.panel_hue_shape.Update_Pin( self.pin_color )
        else:                   self.panel_hue_shape.Update_Pin( None )
        # Analyze
        if self.analyse_display == True: self.panel_hue_shape.Update_Analyse( self.analyse_list )
        else:                            self.panel_hue_shape.Update_Analyse( None )
    def Panel_Hue_Shape_Gradient( self, kmodel ):
        if self.hue_shape == "TRIANGLE":
            color_space = "HSL"
            geometry = "S3"
        elif self.hue_shape == "SQUARE":
            color_space = self.wheel_space
            geometry = "S4"
        elif self.hue_shape == "DIAMOND":
            color_space = "HSL"
            geometry = "SD"
        url = os.path.join( self.url_panel, f"{ kmodel }_{ color_space }_{ geometry }.zip" )
        list_gradient = self.Read_Zip( url )
        self.panel_hue_shape.Update_Gradient( list_gradient )
    # Signals
    def Panel_Hue_Shape_Value( self, mode, v1, v2, v3 ):
        self.Color_Convert( mode, v1, v2, v3, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )

    #endregion
    #region UI LAYOUT PANEL Gamut

    # Update
    def Panel_Gamut_Color( self ):
        # Cursor
        self.panel_gamut.Update_Color( self.wheel_mode, self.wheel_space, self.color_index )
        # Harmony
        if self.ui_harmony == True and self.header_mode == "FG":
            if   self.harmony_rule == harmony_2: harmony_list = [ har_01, har_02 ]
            elif self.harmony_rule == harmony_3: harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == harmony_4: harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:                                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_gamut.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_gamut.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True: self.panel_gamut.Update_Pin( self.pin_color )
        else:                   self.panel_gamut.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:    self.panel_gamut.Update_Analyse( self.analyse_list )
        else:                               self.panel_gamut.Update_Analyse( None )
    def Panel_Gamut_Gradient( self, kmodel, space, mode ):
        if mode == "DIGITAL":   geometry = "GD"
        if mode == "ANALOG":    geometry = "GA"
        url = os.path.join( self.url_panel, f"{ kmodel }_{ space }_{ geometry }.zip" )
        list_gradient = self.Read_Zip( url )
        self.panel_gamut.Update_Gradient( list_gradient )
    # Signals
    def Panel_Gamut_Value( self, mode, v1, v2, v3 ):
        if self.wheel_mode == "ANALOG": v1 = self.convert.huea_to_hued( v1 )
        self.Color_Convert( mode, v1, v2, v3, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )
    def Panel_Gamut_Profile( self, gamut_profile ):
        self.gamut_profile = gamut_profile
        Kritarc_Write( DOCKER_PICKER, "gamut_profile", self.gamut_profile )

    #endregion
    #region UI LAYOUT PANEL Hexagon

    # Update
    def Panel_Hexagon_Color( self ):
        # Cursor
        uvd_hexagon = list( self.convert.uvd_hexagon( self.color_index["uvd_3"], 0.5, 0.5, -1 ) )
        self.panel_hexagon.Update_Color( self.color_index, uvd_hexagon )
        # Harmony
        if self.ui_harmony == True and self.header_mode == "FG":
            if   self.harmony_rule == harmony_2: harmony_list = [ har_01, har_02 ]
            elif self.harmony_rule == harmony_3: harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == harmony_4: harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:                                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_hexagon.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_hexagon.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True: self.panel_hexagon.Update_Pin( self.pin_color )
        else:                   self.panel_hexagon.Update_Pin( None )
        # Analyze
        if self.analyse_display == True:    self.panel_hexagon.Update_Analyse( self.analyse_list )
        else:                               self.panel_hexagon.Update_Analyse( None )
    def Panel_Hexagon_Gradient( self, kmodel ):
        url = os.path.join( self.url_panel, f"{ kmodel }_UVD_H6.zip" )
        list_gradient = self.Read_Zip( url )
        self.panel_hexagon.Update_Gradient( list_gradient )
    # Signals
    def Panel_Hexagon_Value( self, mode, v1, v2, v3 ):
        self.Color_Convert( mode, v1, v2, v3, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )
    def Panel_Hexagon_Depth( self, v3 ):
        self.Color_Convert( "ARD", self.color_index["ard_1"], self.color_index["ard_2"], v3, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )

    #endregion
    #region UI LAYOUT PANEL Luma

    # Update
    def Panel_Luma_Color( self ):
        # Cursor
        self.panel_luma.Update_Color( self.color_index )
        # Harmony
        if self.ui_harmony == True and self.header_mode == "FG":
            if   self.harmony_rule == harmony_2: harmony_list = [ har_01, har_02 ]
            elif self.harmony_rule == harmony_3: harmony_list = [ har_01, har_02, har_03 ]
            elif self.harmony_rule == harmony_4: harmony_list = [ har_01, har_02, har_03, har_04 ]
            else:                                harmony_list = [ har_01, har_02, har_03, har_04, har_05 ]
            self.panel_luma.Update_Harmony( self.harmony_rule, self.harmony_index, harmony_list )
        else:
            self.panel_luma.Update_Harmony( None, None, None )
        # Pins
        if self.ui_pin == True: self.panel_luma.Update_Pin( self.pin_color )
        else:                   self.panel_luma.Update_Pin( None )
        # Analyze
        if self.analyse_display == True: self.panel_luma.Update_Analyse( self.analyse_list )
        else:                            self.panel_luma.Update_Analyse( None )
    def Panel_Luma_Gradient( self, kmodel ):
        url = os.path.join( self.url_panel, f"{ kmodel }_YUV_Y4.zip" )
        list_gradient = self.Read_Zip( url )
        self.panel_luma.Update_Gradient( list_gradient )
    # Signals
    def Panel_Luma_Value( self, mode, v1, v2, v3 ):
        self.Color_Convert( mode, v1, v2, v3, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )

    #endregion
    #region UI LAYOUT PANEL Plane

    # Update
    def Panel_Plane_Gradient( self, update=False ):
        # Variable
        mini = 2 # amount of square
        maxi = 30 # amount of squares
        # Range Calculation
        ww = self.layout.panel_plane.width()
        hh = self.layout.panel_plane.height()
        width = ww - 2 * self.plane_margin
        height = hh - 2 * self.plane_margin
        dx = int( width / ( self.plane_unit + self.plane_split ) )
        dy = int( height / ( self.plane_unit + self.plane_split ) )
        plane_dx = Limit_Range( dx, mini, maxi )
        plane_dy = Limit_Range( dy, mini, maxi )
        if dx > maxi:   plane_ux = int( width / ( maxi + self.plane_split ) )
        else:           plane_ux = self.plane_unit
        if dy > maxi:   plane_uy = int( height / ( maxi + self.plane_split ) )
        else:           plane_uy = self.plane_unit

        # Calculation Interpolation of Colors
        check_widget = ( self.plane_ww != ww ) or ( self.plane_hh != hh )
        check_delta = ( self.plane_dx != plane_dx ) or ( self.plane_dy != plane_dy )
        check_unit = ( self.plane_ux != plane_ux ) or ( self.plane_uy != plane_uy )
        if check_widget == True or check_delta == True or check_unit == True or update == True:
            # Variables
            self.plane_ww = ww
            self.plane_hh = hh
            self.plane_dx = plane_dx
            self.plane_dy = plane_dy
            self.plane_ux = plane_ux
            self.plane_uy = plane_uy
            # Left
            plane_left = list()
            for i in range( 0, plane_dy ):
                factor = i / ( plane_dy - 1 )
                color = self.Color_Interpolate_2( self.mixer_space, self.plane_color[0], self.plane_color[2], factor )
                plane_left.append( color )
            # Right
            plane_right = list()
            for i in range( 0, plane_dy ):
                factor = i / ( plane_dy - 1 )
                color = self.Color_Interpolate_2( self.mixer_space, self.plane_color[1], self.plane_color[3], factor )
                plane_right.append( color )
            # Matrix
            self.plane_matrix = list()
            for y in range( 0, plane_dy ):
                line = list()
                for x in range( 0, plane_dx ):
                    factor = x / ( plane_dx - 1 )
                    color = self.Color_Interpolate_2( self.mixer_space, plane_left[y], plane_right[y], factor )
                    line.append( [ color["hex6"] ] )
                self.plane_matrix.append( line )

        # Error correction
        sx = int( 2 * self.plane_margin ) + ( self.plane_ux * self.plane_dx ) + ( self.plane_split * ( self.plane_dx - 1 ) )
        sy = int( 2 * self.plane_margin ) + ( self.plane_uy * self.plane_dy ) + ( self.plane_split * ( self.plane_dy - 1 ) )
        ex = max( ww - sx, 0 )
        ey = max( hh - sy, 0 )
        cx = math.ceil( ex / self.plane_dx )
        cy = math.ceil( ey / self.plane_dy )

        # Geometry
        pr = self.plane_margin
        pd = self.plane_margin
        # Cycle
        for y in range( 0, self.plane_dy ):
            for x in range( 0, self.plane_dx ):
                # Variables
                if x == 0: ox = ex; pr = self.plane_margin
                if y == 0: oy = ey; pd = self.plane_margin
                tx = cx
                ty = cy
                if ox >= 0 and ox < cx: tx = ox
                if oy >= 0 and oy < cy: ty = oy
                # Calculation
                px = int( pr )
                py = int( pd )
                pw = int( self.plane_ux + tx )
                ph = int( self.plane_uy + ty )
                pr = int( px + pw )
                pb = int( py + ph )
                self.plane_matrix[y][x].extend( [ px, py, pw, ph, pr, pb ] )
                # Next Cycle X
                pr = px + pw + self.plane_split
                ox = max( ox - cx, 0 )
            # Next Cycle Y
            pd = py + ph + self.plane_split
            oy = max( oy - cy, 0 )

        # Update
        self.panel_plane.Update_Gradient( ww, hh, self.plane_matrix, self.plane_margin, self.plane_split )
    # Signals
    def Panel_Plane_Value( self, hex_code ):
        self.Color_Convert( "HEX", hex_code, 0, 0, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )
    def Panel_Plane_Index( self, index ):
        self.plane_color[index] = self.color_index.copy()
        self.Panel_Plane_Gradient( True )
        Kritarc_Write( DOCKER_PICKER, "plane_color", self.plane_color )
    def Panel_Plane_Swap( self, ia, ib ):
        self.plane_color[ia], self.plane_color[ib] = self.plane_color[ib], self.plane_color[ia]
        self.Panel_Plane_Gradient( True )
        Kritarc_Write( DOCKER_PICKER, "plane_color", self.plane_color )
    def Panel_Plane_Random( self ):
        # Random
        tl_c1, tl_c2, tl_c3 = self.Random_Channels()
        tr_c1, tr_c2, tr_c3 = self.Random_Channels()
        bl_c1, bl_c2, bl_c3 = self.Random_Channels()
        br_c1, br_c2, br_c3 = self.Random_Channels()
        # Convert
        color_tl = self.Color_Convert( "HEX", "#000000", 0, 0, 0, color_true.copy() )
        color_tr = self.Color_Convert( "HEX", "#000000", 0, 0, 0, color_true.copy() )
        color_bl = self.Color_Convert( "HEX", "#000000", 0, 0, 0, color_true.copy() )
        color_br = self.Color_Convert( "HEX", "#000000", 0, 0, 0, color_true.copy() )
        # Apply
        self.Pigmento_APPLY( "SRGB", tl_c1, tl_c2, tl_c3, 0, color_tl )
        self.Pigmento_APPLY( "SRGB", tr_c1, tr_c2, tr_c3, 0, color_tr )
        self.Pigmento_APPLY( "SRGB", bl_c1, bl_c2, bl_c3, 0, color_bl )
        self.Pigmento_APPLY( "SRGB", br_c1, br_c2, br_c3, 0, color_br )
        # Update
        self.plane_color = [ color_tl, color_tr, color_bl, color_br ]
        self.Panel_Plane_Gradient( True )
        Kritarc_Write( DOCKER_PICKER, "plane_color", self.plane_color )
    def Panel_Plane_Reset( self ):
        self.plane_color = [ self.zorn_w.copy(), self.zorn_y.copy(), self.zorn_r.copy(), self.zorn_b.copy() ]
        self.Panel_Plane_Gradient( True )
        Kritarc_Write( DOCKER_PICKER, "plane_color", self.plane_color )

    #endregion
    #region UI LAYOUT PANEL Mask

    # Update
    def Panel_Mask_Gradient( self ):
        self.panel_mask.Update_Gradient( self.mask_color, self.mask_alpha )
    def Mask_Pin_Color( self, mask_color, mask_alpha ):
        for i in range( 0, len( self.mask_module ) ):
            self.mask_module[i].Update_Color( mask_color[i], mask_alpha[i] )
    # Signals
    def Panel_Mask_Value( self, hex_code ):
        self.Color_Convert( "HEX", hex_code, 0, 0, 0, self.color_index )
        self.Sync_Elements( not self.performance_release, True, False )

    # Live
    def Panel_Mask_Live( self ):
        if self.mask_live != None:
            self.Mask_Save( self.mask_live )
    def Live_B1( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 0
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_B2( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 1
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_B3( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 2
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_D1( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 3
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_D2( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 4
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_D3( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 5
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_D4( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 6
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_D5( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 7
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_D6( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 8
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_F1( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 9
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_F2( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 10
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Live_F3( self, boolean ):
        self.mask_live = None
        if boolean == True:
            index = 11
            self.Mask_Apply( index )
            self.Mask_Close( index )
            self.mask_live = index
    def Mask_Close( self, index ):
        # Background
        if index != 0:  self.layout.b1_live.setChecked( False )
        if index != 1:  self.layout.b2_live.setChecked( False )
        if index != 2:  self.layout.b3_live.setChecked( False )
        # Diffuse
        if index != 3:  self.layout.d1_live.setChecked( False )
        if index != 4:  self.layout.d2_live.setChecked( False )
        if index != 5:  self.layout.d3_live.setChecked( False )
        if index != 6:  self.layout.d4_live.setChecked( False )
        if index != 7:  self.layout.d5_live.setChecked( False )
        if index != 8:  self.layout.d6_live.setChecked( False )
        # Foreground
        if index != 9:  self.layout.f1_live.setChecked( False )
        if index != 10: self.layout.f2_live.setChecked( False )
        if index != 11: self.layout.f3_live.setChecked( False )
    # Pin Edit
    def Mask_Apply( self, index ):
        self.Pigmento_APPLY( "HEX", self.mask_color[index], 0, 0, 0, self.color_index )
        self.Pigmento_SYNC()
    def Mask_Save( self, index ):
        # Variables
        self.mask_color[index] = self.color_index["hex6"]
        self.mask_alpha[index] = 1.0
        # Update
        self.mask_module[index].Update_Color( self.mask_color[index], self.mask_alpha[index] )
        self.Panel_Mask_Gradient()
        # Save
        self.Mask_Write()
    def Mask_Clean( self, index ):
        # Variables
        self.mask_color[index] = "#000000"
        self.mask_alpha[index] = 0.0
        # Update
        self.mask_module[index].Update_Clean()
        self.Panel_Mask_Gradient()
        # Save
        self.Mask_Write()
    def Mask_Alpha( self, index, value ):
        # Variables
        self.mask_alpha[index] = value
        # Update
        self.mask_module[index].Update_Color( self.mask_color[index], self.mask_alpha[index] )
        self.Panel_Mask_Gradient()
        # Save
        self.Mask_Write()
    # Reset
    def Mask_Reset( self ):
        self.Mask_Read( True )
        self.Mask_Write()

    # Operators
    def Mask_Load( self, mask_url ):
        path = os.path.join( mask_url, "color.eo" )
        exists = os.path.exists( path )
        if exists == True:
            with open( path, "r" ) as self.mask_file:
                # Read
                data = self.mask_file.readlines()
                for line in data:
                    if line.startswith( "mask_color=" ) == True:   self.mask_color = eval( line.replace( "mask_color=", "" ) )
                    if line.startswith( "mask_alpha=" ) == True:   self.mask_alpha = eval( line.replace( "mask_alpha=", "" ) )
                # Update
                self.Panel_Mask_Gradient()
                self.Mask_Pin_Color( self.mask_color, self.mask_alpha )
                self.panel_mask.Update_Path( self.mask_url )
        self.mask_file.close()
    def Mask_Read( self, reset ):
        self.Mask_Close( None )
        path = os.path.join( self.mask_url, "color.eo" )
        with open( path, "r" ) as self.mask_file:
            # Read
            data = self.mask_file.readlines()
            for line in data:
                if reset == True:
                    if line.startswith( "default_color=" ) == True: self.mask_color = eval( line.replace( "default_color=", "" ) )
                    if line.startswith( "default_alpha=" ) == True: self.mask_alpha = eval( line.replace( "default_alpha=", "" ) )
                else:
                    if line.startswith( "mask_color=" ) == True:    self.mask_color = eval( line.replace( "mask_color=", "" ) )
                    if line.startswith( "mask_alpha=" ) == True:    self.mask_alpha = eval( line.replace( "mask_alpha=", "" ) )
            # Update
            self.Panel_Mask_Gradient()
            self.Mask_Pin_Color( self.mask_color, self.mask_alpha )
            self.panel_mask.Update_Path( self.mask_url )
        self.mask_file.close()
    def Mask_Write( self ):
        path = os.path.join( self.mask_url, "color.eo" )
        if self.mask_file.closed == True:
            # Read
            with open( path, "r" ) as self.mask_file:
                data = self.mask_file.readlines()
            # Write
            with open( path, "w" ) as self.mask_file:
                edit = str()
                for line in data:
                    if   line.startswith( "mask_color=" ) == True:  line = f"mask_color={ self.mask_color }\n"
                    elif line.startswith( "mask_alpha=" ) == True:  line = f"mask_alpha={ self.mask_alpha }\n"
                    edit += line
                self.mask_file.write( edit )
            # File
            self.mask_file.close()

    #endregion
    #region UI LAYOUT CHANNEL General

    # Locks
    def Lock_CMYK_4( self, boolean ):
        # Variables
        self.lock_cmyk_4 = boolean
        # UI
        if boolean == True:
            self.layout.cmyk_4_label.setText( "" ) # LOCKED
            self.layout.cmyk_4_label.setIcon( self.qicon_lock_layout )
            self.dialog.chan_cmyk.setIcon( self.qicon_lock_dialog )
        else:
            self.layout.cmyk_4_label.setText( "K" ) # Unlocked
            self.layout.cmyk_4_label.setIcon( self.qicon_none )
            self.dialog.chan_cmyk.setIcon( self.qicon_none )
        # Save
        Kritarc_Write( DOCKER_PICKER, "lock_cmyk_4", self.lock_cmyk_4 )

    #endregion
    #region UI LAYOUT CHANNEL Sliders

    # GRAY
    def Channel_GRAY_1_Slider( self, value ):
        self.Pigmento_PRESS( "GRAY", value, 0, 0, 0, self.color_index )
    # SRGB
    def Channel_SRGB_1_Slider( self, value ):
        self.Pigmento_PRESS( "SRGB", value, self.color_index["srgb_2"], self.color_index["srgb_3"], 0, self.color_index )
    def Channel_SRGB_2_Slider( self, value ):
        self.Pigmento_PRESS( "SRGB", self.color_index["srgb_1"], value, self.color_index["srgb_3"], 0, self.color_index )
    def Channel_SRGB_3_Slider( self, value ):
        self.Pigmento_PRESS( "SRGB", self.color_index["srgb_1"], self.color_index["srgb_2"], value, 0, self.color_index )
    # LRGB
    def Channel_LRGB_1_Slider( self, value ):
        self.Pigmento_PRESS( "LRGB", value, self.color_index["lrgb_2"], self.color_index["lrgb_3"], 0, self.color_index )
    def Channel_LRGB_2_Slider( self, value ):
        self.Pigmento_PRESS( "LRGB", self.color_index["lrgb_1"], value, self.color_index["lrgb_3"], 0, self.color_index )
    def Channel_LRGB_3_Slider( self, value ):
        self.Pigmento_PRESS( "LRGB", self.color_index["lrgb_1"], self.color_index["lrgb_2"], value, 0, self.color_index )
    # CMYK
    def Channel_CMYK_1_Slider( self, value ):
        self.Pigmento_PRESS( "CMYK", value, self.color_index["cmyk_2"], self.color_index["cmyk_3"], self.color_index["cmyk_4"], self.color_index )
    def Channel_CMYK_2_Slider( self, value ):
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], value, self.color_index["cmyk_3"], self.color_index["cmyk_4"], self.color_index )
    def Channel_CMYK_3_Slider( self, value ):
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], self.color_index["cmyk_2"], value, self.color_index["cmyk_4"], self.color_index )
    def Channel_CMYK_4_Slider( self, value ):
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], self.color_index["cmyk_2"], self.color_index["cmyk_3"], value, self.color_index )
    # RYB
    def Channel_RYB_1_Slider( self, value ):
        self.Pigmento_PRESS( "RYB", value, self.color_index["ryb_2"], self.color_index["ryb_3"], 0, self.color_index )
    def Channel_RYB_2_Slider( self, value ):
        self.Pigmento_PRESS( "RYB", self.color_index["ryb_1"], value, self.color_index["ryb_3"], 0, self.color_index )
    def Channel_RYB_3_Slider( self, value ):
        self.Pigmento_PRESS( "RYB", self.color_index["ryb_1"], self.color_index["ryb_2"], value, 0, self.color_index )
    # YUV
    def Channel_YUV_1_Slider( self, value ):
        self.Pigmento_PRESS( "YUV", value, self.color_index["yuv_2"], self.color_index["yuv_3"], 0, self.color_index )
    def Channel_YUV_2_Slider( self, value ):
        self.Pigmento_PRESS( "YUV", self.color_index["yuv_1"], value, self.color_index["yuv_3"], 0, self.color_index )
    def Channel_YUV_3_Slider( self, value ):
        self.Pigmento_PRESS( "YUV", self.color_index["yuv_1"], self.color_index["yuv_2"], value, 0, self.color_index )
    # HSV
    def Channel_HSV_1_Slider( self, value ):
        self.Pigmento_PRESS( "HSV", value, self.color_index["hsv_2"], self.color_index["hsv_3"], 0, self.color_index )
    def Channel_HSV_2_Slider( self, value ):
        self.Pigmento_PRESS( "HSV", self.color_index["hsv_1"], value, self.color_index["hsv_3"], 0, self.color_index )
    def Channel_HSV_3_Slider( self, value ):
        self.Pigmento_PRESS( "HSV", self.color_index["hsv_1"], self.color_index["hsv_2"], value, 0, self.color_index )
    # HSL
    def Channel_HSL_1_Slider( self, value ):
        self.Pigmento_PRESS( "HSL", value, self.color_index["hsl_2"], self.color_index["hsl_3"], 0, self.color_index )
    def Channel_HSL_2_Slider( self, value ):
        self.Pigmento_PRESS( "HSL", self.color_index["hsl_1"], value, self.color_index["hsl_3"], 0, self.color_index )
    def Channel_HSL_3_Slider( self, value ):
        self.Pigmento_PRESS( "HSL", self.color_index["hsl_1"], self.color_index["hsl_2"], value, 0, self.color_index )
    # HCY
    def Channel_HCY_1_Slider( self, value ):
        self.Pigmento_PRESS( "HCY", value, self.color_index["hcy_2"], self.color_index["hcy_3"], 0, self.color_index )
    def Channel_HCY_2_Slider( self, value ):
        self.Pigmento_PRESS( "HCY", self.color_index["hcy_1"], value, self.color_index["hcy_3"], 0, self.color_index )
    def Channel_HCY_3_Slider( self, value ):
        self.Pigmento_PRESS( "HCY", self.color_index["hcy_1"], self.color_index["hcy_2"], value, 0, self.color_index )
    # ARD
    def Channel_ARD_1_Slider( self, value ):
        self.Pigmento_PRESS( "ARD", value, self.color_index["ard_2"], self.color_index["ard_3"], 0, self.color_index )
    def Channel_ARD_2_Slider( self, value ):
        self.Pigmento_PRESS( "ARD", self.color_index["ard_1"], value, self.color_index["ard_3"], 0, self.color_index )
    def Channel_ARD_3_Slider( self, value ):
        self.Pigmento_PRESS( "ARD", self.color_index["ard_1"], self.color_index["ard_2"], value, 0, self.color_index )
    # XYZ
    def Channel_XYZ_1_Slider( self, value ):
        self.Pigmento_PRESS( "XYZ", value, self.color_index["xyz_2"], self.color_index["xyz_3"], 0, self.color_index )
    def Channel_XYZ_2_Slider( self, value ):
        self.Pigmento_PRESS( "XYZ", self.color_index["xyz_1"], value, self.color_index["xyz_3"], 0, self.color_index )
    def Channel_XYZ_3_Slider( self, value ):
        self.Pigmento_PRESS( "XYZ", self.color_index["xyz_1"], self.color_index["xyz_2"], value, 0, self.color_index )
    # XYY
    def Channel_XYY_1_Slider( self, value ):
        self.Pigmento_PRESS( "XYY", value, self.color_index["xyy_2"], self.color_index["xyy_3"], 0, self.color_index )
    def Channel_XYY_2_Slider( self, value ):
        self.Pigmento_PRESS( "XYY", self.color_index["xyy_1"], value, self.color_index["xyy_3"], 0, self.color_index )
    def Channel_XYY_3_Slider( self, value ):
        self.Pigmento_PRESS( "XYY", self.color_index["xyy_1"], self.color_index["xyy_2"], value, 0, self.color_index )
    # LAB
    def Channel_LAB_1_Slider( self, value ):
        self.Pigmento_PRESS( "LAB", value, self.color_index["lab_2"], self.color_index["lab_3"], 0, self.color_index )
    def Channel_LAB_2_Slider( self, value ):
        self.Pigmento_PRESS( "LAB", self.color_index["lab_1"], value, self.color_index["lab_3"], 0, self.color_index )
    def Channel_LAB_3_Slider( self, value ):
        self.Pigmento_PRESS( "LAB", self.color_index["lab_1"], self.color_index["lab_2"], value, 0, self.color_index )
    # LCH
    def Channel_LCH_1_Slider( self, value ):
        self.Pigmento_PRESS( "LCH", value, self.color_index["lch_2"], self.color_index["lch_3"], 0, self.color_index )
    def Channel_LCH_2_Slider( self, value ):
        self.Pigmento_PRESS( "LCH", self.color_index["lch_1"], value, self.color_index["lch_3"], 0, self.color_index )
    def Channel_LCH_3_Slider( self, value ):
        self.Pigmento_PRESS( "LCH", self.color_index["lch_1"], self.color_index["lch_2"], value, 0, self.color_index )

    #endregion
    #region UI LAYOUT CHANNEL Increment

    # GRAY
    def Channel_GRAY_1_Increment( self, value ):
        value = Limit_Float( self.color_index["gray_1"] + ( value / self.color_range["gray_1"] ) )
        self.Pigmento_PRESS( "GRAY", value, 0, 0, 0, self.color_index )
    # SRGB
    def Channel_SRGB_1_Increment( self, value ):
        value = Limit_Float( self.color_index["srgb_1"] + ( value / self.color_range["srgb_1"] ) )
        self.Pigmento_PRESS( "SRGB", value, self.color_index["srgb_2"], self.color_index["srgb_3"], 0, self.color_index )
    def Channel_SRGB_2_Increment( self, value ):
        value = Limit_Float( self.color_index["srgb_2"] + ( value / self.color_range["srgb_2"] ) )
        self.Pigmento_PRESS( "SRGB", self.color_index["srgb_1"], value, self.color_index["srgb_3"], 0, self.color_index )
    def Channel_SRGB_3_Increment( self, value ):
        value = Limit_Float( self.color_index["srgb_3"] + ( value / self.color_range["srgb_3"] ) )
        self.Pigmento_PRESS( "SRGB", self.color_index["srgb_1"], self.color_index["srgb_2"], value, 0, self.color_index )
    # LRGB
    def Channel_LRGB_1_Increment( self, value ):
        value = Limit_Float( self.color_index["lrgb_1"] + ( value / self.color_range["lrgb_1"] ) )
        self.Pigmento_PRESS( "LRGB", value, self.color_index["lrgb_2"], self.color_index["lrgb_3"], 0, self.color_index )
    def Channel_LRGB_2_Increment( self, value ):
        value = Limit_Float( self.color_index["lrgb_2"] + ( value / self.color_range["lrgb_2"] ) )
        self.Pigmento_PRESS( "LRGB", self.color_index["lrgb_1"], value, self.color_index["lrgb_3"], 0, self.color_index )
    def Channel_LRGB_3_Increment( self, value ):
        value = Limit_Float( self.color_index["lrgb_3"] + ( value / self.color_range["lrgb_3"] ) )
        self.Pigmento_PRESS( "LRGB", self.color_index["lrgb_1"], self.color_index["lrgb_2"], value, 0, self.color_index )
    # CMYK
    def Channel_CMYK_1_Increment( self, value ):
        value = Limit_Float( self.color_index["cmyk_1"] + ( value / self.color_range["cmyk_1"] ) )
        self.Pigmento_PRESS( "CMYK", value, self.color_index["cmyk_2"], self.color_index["cmyk_3"], self.color_index["cmyk_4"], self.color_index )
    def Channel_CMYK_2_Increment( self, value ):
        value = Limit_Float( self.color_index["cmyk_2"] + ( value / self.color_range["cmyk_2"] ) )
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], value, self.color_index["cmyk_3"], self.color_index["cmyk_4"], self.color_index )
    def Channel_CMYK_3_Increment( self, value ):
        value = Limit_Float( self.color_index["cmyk_3"] + ( value / self.color_range["cmyk_3"] ) )
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], self.color_index["cmyk_2"], value, self.color_index["cmyk_4"], self.color_index )
    def Channel_CMYK_4_Increment( self, value ):
        value = Limit_Float( self.color_index["cmyk_4"] + ( value / self.color_range["cmyk_4"] ) )
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], self.color_index["cmyk_2"], self.color_index["cmyk_3"], value, self.color_index )
    # RYB
    def Channel_RYB_1_Increment( self, value ):
        value = Limit_Float( self.color_index["ryb_1"] + ( value / self.color_range["ryb_1"] ) )
        self.Pigmento_PRESS( "RYB", value, self.color_index["ryb_2"], self.color_index["ryb_3"], 0, self.color_index )
    def Channel_RYB_2_Increment( self, value ):
        value = Limit_Float( self.color_index["ryb_2"] + ( value / self.color_range["ryb_2"] ) )
        self.Pigmento_PRESS( "RYB", self.color_index["ryb_1"], value, self.color_index["ryb_3"], 0, self.color_index )
    def Channel_RYB_3_Increment( self, value ):
        value = Limit_Float( self.color_index["ryb_3"] + ( value / self.color_range["ryb_3"] ) )
        self.Pigmento_PRESS( "RYB", self.color_index["ryb_1"], self.color_index["ryb_2"], value, 0, self.color_index )
    # YUV
    def Channel_YUV_1_Increment( self, value ):
        value = Limit_Float( self.color_index["yuv_1"] + ( value / self.color_range["yuv_1"] ) )
        self.Pigmento_PRESS( "YUV", value, self.color_index["yuv_2"], self.color_index["yuv_3"], 0, self.color_index )
    def Channel_YUV_2_Increment( self, value ):
        value = Limit_Float( self.color_index["yuv_2"] + ( value / self.color_range["yuv_2"] ) )
        self.Pigmento_PRESS( "YUV", self.color_index["yuv_1"], value, self.color_index["yuv_3"], 0, self.color_index )
    def Channel_YUV_3_Increment( self, value ):
        value = Limit_Float( self.color_index["yuv_3"] + ( value / self.color_range["yuv_3"] ) )
        self.Pigmento_PRESS( "YUV", self.color_index["yuv_1"], self.color_index["yuv_2"], value, 0, self.color_index )
    # HSV
    def Channel_HSV_1_Increment( self, value ):
        value = Limit_Float( self.color_index["hsv_1"] + ( value / self.color_range["hsv_1"] ) )
        self.Pigmento_PRESS( "HSV", value, self.color_index["hsv_2"], self.color_index["hsv_3"], 0, self.color_index )
    def Channel_HSV_2_Increment( self, value ):
        value = Limit_Float( self.color_index["hsv_2"] + ( value / self.color_range["hsv_2"] ) )
        self.Pigmento_PRESS( "HSV", self.color_index["hsv_1"], value, self.color_index["hsv_3"], 0, self.color_index )
    def Channel_HSV_3_Increment( self, value ):
        value = Limit_Float( self.color_index["hsv_3"] + ( value / self.color_range["hsv_3"] ) )
        self.Pigmento_PRESS( "HSV", self.color_index["hsv_1"], self.color_index["hsv_2"], value, 0, self.color_index )
    # HSL
    def Channel_HSL_1_Increment( self, value ):
        value = Limit_Float( self.color_index["hsl_1"] + ( value / self.color_range["hsl_1"] ) )
        self.Pigmento_PRESS( "HSL", value, self.color_index["hsl_2"], self.color_index["hsl_3"], 0, self.color_index )
    def Channel_HSL_2_Increment( self, value ):
        value = Limit_Float( self.color_index["hsl_2"] + ( value / self.color_range["hsl_2"] ) )
        self.Pigmento_PRESS( "HSL", self.color_index["hsl_1"], value, self.color_index["hsl_3"], 0, self.color_index )
    def Channel_HSL_3_Increment( self, value ):
        value = Limit_Float( self.color_index["hsl_3"] + ( value / self.color_range["hsl_3"] ) )
        self.Pigmento_PRESS( "HSL", self.color_index["hsl_1"], self.color_index["hsl_2"], value, 0, self.color_index )
    # HCY
    def Channel_HCY_1_Increment( self, value ):
        value = Limit_Float( self.color_index["hcy_1"] + ( value / self.color_range["hcy_1"] ) )
        self.Pigmento_PRESS( "HCY", value, self.color_index["hcy_2"], self.color_index["hcy_3"], 0, self.color_index )
    def Channel_HCY_2_Increment( self, value ):
        value = Limit_Float( self.color_index["hcy_2"] + ( value / self.color_range["hcy_2"] ) )
        self.Pigmento_PRESS( "HCY", self.color_index["hcy_1"], value, self.color_index["hcy_3"], 0, self.color_index )
    def Channel_HCY_3_Increment( self, value ):
        value = Limit_Float( self.color_index["hcy_3"] + ( value / self.color_range["hcy_3"] ) )
        self.Pigmento_PRESS( "HCY", self.color_index["hcy_1"], self.color_index["hcy_2"], value, 0, self.color_index )
    # ARD
    def Channel_ARD_1_Increment( self, value ):
        value = Limit_Float( self.color_index["ard_1"] + ( value / self.color_range["ard_1"] ) )
        self.Pigmento_PRESS( "ARD", value, self.color_index["ard_2"], self.color_index["ard_3"], 0, self.color_index )
    def Channel_ARD_2_Increment( self, value ):
        value = Limit_Float( self.color_index["ard_2"] + ( value / self.color_range["ard_2"] ) )
        self.Pigmento_PRESS( "ARD", self.color_index["ard_1"], value, self.color_index["ard_3"], 0, self.color_index )
    def Channel_ARD_3_Increment( self, value ):
        value = Limit_Float( self.color_index["ard_3"] + ( value / self.color_range["ard_3"] ) )
        self.Pigmento_PRESS( "ARD", self.color_index["ard_1"], self.color_index["ard_2"], value, 0, self.color_index )
    # XYZ
    def Channel_XYZ_1_Increment( self, value ):
        value = Limit_Float( self.color_index["xyz_1"] + ( value / self.color_range["xyz_1"] ) )
        self.Pigmento_PRESS( "XYZ", value, self.color_index["xyz_2"], self.color_index["xyz_3"], 0, self.color_index )
    def Channel_XYZ_2_Increment( self, value ):
        value = Limit_Float( self.color_index["xyz_2"] + ( value / self.color_range["xyz_2"] ) )
        self.Pigmento_PRESS( "XYZ", self.color_index["xyz_1"], value, self.color_index["xyz_3"], 0, self.color_index )
    def Channel_XYZ_3_Increment( self, value ):
        value = Limit_Float( self.color_index["xyz_3"] + ( value / self.color_range["xyz_3"] ) )
        self.Pigmento_PRESS( "XYZ", self.color_index["xyz_1"], self.color_index["xyz_2"], value, 0, self.color_index )
    # XYY
    def Channel_XYY_1_Increment( self, value ):
        value = Limit_Float( self.color_index["xyy_1"] + ( value / self.color_range["xyy_1"] ) )
        self.Pigmento_PRESS( "XYY", value, self.color_index["xyy_2"], self.color_index["xyy_3"], 0, self.color_index )
    def Channel_XYY_2_Increment( self, value ):
        value = Limit_Float( self.color_index["xyy_2"] + ( value / self.color_range["xyy_2"] ) )
        self.Pigmento_PRESS( "XYY", self.color_index["xyy_1"], value, self.color_index["xyy_3"], 0, self.color_index )
    def Channel_XYY_3_Increment( self, value ):
        value = Limit_Float( self.color_index["xyy_3"] + ( value / self.color_range["xyy_3"] ) )
        self.Pigmento_PRESS( "XYY", self.color_index["xyy_1"], self.color_index["xyy_2"], value, 0, self.color_index )
    # LAB
    def Channel_LAB_1_Increment( self, value ):
        value = Limit_Float( self.color_index["lab_1"] + ( value / self.color_range["lab_1"] ) )
        self.Pigmento_PRESS( "LAB", value, self.color_index["lab_2"], self.color_index["lab_3"], 0, self.color_index )
    def Channel_LAB_2_Increment( self, value ):
        value = Limit_Float( self.color_index["lab_2"] + ( value / self.color_range["lab_2"] ) )
        self.Pigmento_PRESS( "LAB", self.color_index["lab_1"], value, self.color_index["lab_3"], 0, self.color_index )
    def Channel_LAB_3_Increment( self, value ):
        value = Limit_Float( self.color_index["lab_3"] + ( value / self.color_range["lab_3"] ) )
        self.Pigmento_PRESS( "LAB", self.color_index["lab_1"], self.color_index["lab_2"], value, 0, self.color_index )
    # LCH
    def Channel_LCH_1_Increment( self, value ):
        value = Limit_Float( self.color_index["lch_1"] + ( value / self.color_range["lch_1"] ) )
        self.Pigmento_PRESS( "LCH", value, self.color_index["lch_2"], self.color_index["lch_3"], 0, self.color_index )
    def Channel_LCH_2_Increment( self, value ):
        value = Limit_Float( self.color_index["lch_2"] + ( value / self.color_range["lch_2"] ) )
        self.Pigmento_PRESS( "LCH", self.color_index["lch_1"], value, self.color_index["lch_3"], 0, self.color_index )
    def Channel_LCH_3_Increment( self, value ):
        value = Limit_Float( self.color_index["lch_3"] + ( value / self.color_range["lch_3"] ) )
        self.Pigmento_PRESS( "LCH", self.color_index["lch_1"], self.color_index["lch_2"], value, 0, self.color_index )

    #endregion
    #region UI LAYOUT CHANNEL Mark

    # GRAY
    def Channel_GRAY_1_Mark( self, mark ):
        self.color_mark["gray_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # SRGB
    def Channel_SRGB_1_Mark( self, mark ):
        self.color_mark["srgb_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_SRGB_2_Mark( self, mark ):
        self.color_mark["srgb_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_SRGB_3_Mark( self, mark ):
        self.color_mark["srgb_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # LRGB
    def Channel_LRGB_1_Mark( self, mark ):
        self.color_mark["lrgb_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_LRGB_2_Mark( self, mark ):
        self.color_mark["lrgb_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_LRGB_3_Mark( self, mark ):
        self.color_mark["lrgb_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # CMYK
    def Channel_CMYK_1_Mark( self, mark ):
        self.color_mark["cmyk_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_CMYK_2_Mark( self, mark ):
        self.color_mark["cmyk_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_CMYK_3_Mark( self, mark ):
        self.color_mark["cmyk_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_CMYK_4_Mark( self, mark ):
        self.color_mark["cmyk_4"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # RYB
    def Channel_RYB_1_Mark( self, mark ):
        self.color_mark["ryb_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_RYB_2_Mark( self, mark ):
        self.color_mark["ryb_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_RYB_3_Mark( self, mark ):
        self.color_mark["ryb_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # YUV
    def Channel_YUV_1_Mark( self, mark ):
        self.color_mark["yuv_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_YUV_2_Mark( self, mark ):
        self.color_mark["yuv_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_YUV_3_Mark( self, mark ):
        self.color_mark["yuv_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # HSV
    def Channel_HSV_1_Mark( self, mark ):
        self.color_mark["hsv_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_HSV_2_Mark( self, mark ):
        self.color_mark["hsv_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_HSV_3_Mark( self, mark ):
        self.color_mark["hsv_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # HSL
    def Channel_HSL_1_Mark( self, mark ):
        self.color_mark["hsl_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_HSL_2_Mark( self, mark ):
        self.color_mark["hsl_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_HSL_3_Mark( self, mark ):
        self.color_mark["hsl_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # HCY
    def Channel_HCY_1_Mark( self, mark ):
        self.color_mark["hcy_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_HCY_2_Mark( self, mark ):
        self.color_mark["hcy_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_HCY_3_Mark( self, mark ):
        self.color_mark["hcy_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # ARD
    def Channel_ARD_1_Mark( self, mark ):
        self.color_mark["ard_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_ARD_2_Mark( self, mark ):
        self.color_mark["ard_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_ARD_3_Mark( self, mark ):
        self.color_mark["ard_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # XYZ
    def Channel_XYZ_1_Mark( self, mark ):
        self.color_mark["xyz_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_XYZ_2_Mark( self, mark ):
        self.color_mark["xyz_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_XYZ_3_Mark( self, mark ):
        self.color_mark["xyz_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # XYY
    def Channel_XYY_1_Mark( self, mark ):
        self.color_mark["xyy_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_XYY_2_Mark( self, mark ):
        self.color_mark["xyy_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_XYY_3_Mark( self, mark ):
        self.color_mark["xyy_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # LAB
    def Channel_LAB_1_Mark( self, mark ):
        self.color_mark["lab_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_LAB_2_Mark( self, mark ):
        self.color_mark["lab_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_LAB_3_Mark( self, mark ):
        self.color_mark["lab_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # LCH
    def Channel_LCH_1_Mark( self, mark ):
        self.color_mark["lch_1"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_LCH_2_Mark( self, mark ):
        self.color_mark["lch_2"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    def Channel_LCH_3_Mark( self, mark ):
        self.color_mark["lch_3"] = mark
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )

    #endregion
    #region UI LAYOUT CHANNEL Values

    # GRAY
    def Channel_GRAY_1_Value( self, value ):
        value = value / self.color_range["gray_1"]
        self.Pigmento_PRESS( "GRAY", value, 0, 0, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # RGB
    def Channel_SRGB_1_Value( self, value ):
        value = value / self.color_range["srgb_1"]
        self.Pigmento_PRESS( "SRGB", value, self.color_index["srgb_2"], self.color_index["srgb_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_SRGB_2_Value( self, value ):
        value = value / self.color_range["srgb_2"]
        self.Pigmento_PRESS( "SRGB", self.color_index["srgb_1"], value, self.color_index["srgb_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_SRGB_3_Value( self, value ):
        value = value / self.color_range["srgb_3"]
        self.Pigmento_PRESS( "SRGB", self.color_index["srgb_1"], self.color_index["srgb_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # LRGB
    def Channel_LRGB_1_Value( self, value ):
        value = value / self.color_range["lrgb_1"]
        self.Pigmento_PRESS( "LRGB", value, self.color_index["lrgb_2"], self.color_index["lrgb_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_LRGB_2_Value( self, value ):
        value = value / self.color_range["lrgb_2"]
        self.Pigmento_PRESS( "LRGB", self.color_index["lrgb_1"], value, self.color_index["lrgb_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_LRGB_3_Value( self, value ):
        value = value / self.color_range["lrgb_3"]
        self.Pigmento_PRESS( "LRGB", self.color_index["lrgb_1"], self.color_index["lrgb_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # CMYK
    def Channel_CMYK_1_Value( self, value ):
        value = value / self.color_range["cmyk_1"]
        self.Pigmento_PRESS( "CMYK", value, self.color_index["cmyk_2"], self.color_index["cmyk_3"], self.color_index["cmyk_4"], self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_CMYK_2_Value( self, value ):
        value = value / self.color_range["cmyk_2"]
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], value, self.color_index["cmyk_3"], self.color_index["cmyk_4"], self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_CMYK_3_Value( self, value ):
        value = value / self.color_range["cmyk_3"]
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], self.color_index["cmyk_2"], value, self.color_index["cmyk_4"], self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_CMYK_4_Value( self, value ):
        value = value / self.color_range["cmyk_4"]
        self.Pigmento_PRESS( "CMYK", self.color_index["cmyk_1"], self.color_index["cmyk_2"], self.color_index["cmyk_3"], value, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # RYB
    def Channel_RYB_1_Value( self, value ):
        value = value / self.color_range["ryb_1"]
        self.Pigmento_PRESS( "RYB", value, self.color_index["ryb_2"], self.color_index["ryb_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_RYB_2_Value( self, value ):
        value = value / self.color_range["ryb_2"]
        self.Pigmento_PRESS( "RYB", self.color_index["ryb_1"], value, self.color_index["ryb_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_RYB_3_Value( self, value ):
        value = value / self.color_range["ryb_3"]
        self.Pigmento_PRESS( "RYB", self.color_index["ryb_1"], self.color_index["ryb_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # YUV
    def Channel_YUV_1_Value( self, value ):
        value = value / self.color_range["yuv_1"]
        self.Pigmento_PRESS( "YUV", value, self.color_index["yuv_2"], self.color_index["yuv_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_YUV_2_Value( self, value ):
        value = value / self.color_range["yuv_2"]
        self.Pigmento_PRESS( "YUV", self.color_index["yuv_1"], value, self.color_index["yuv_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_YUV_3_Value( self, value ):
        value = value / self.color_range["yuv_3"]
        self.Pigmento_PRESS( "YUV", self.color_index["yuv_1"], self.color_index["yuv_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # HSV
    def Channel_HSV_1_Value( self, value ):
        value = value / self.color_range["hsv_1"]
        self.Pigmento_PRESS( "HSV", value, self.color_index["hsv_2"], self.color_index["hsv_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_HSV_2_Value( self, value ):
        value = value / self.color_range["hsv_2"]
        self.Pigmento_PRESS( "HSV", self.color_index["hsv_1"], value, self.color_index["hsv_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_HSV_3_Value( self, value ):
        value = value / self.color_range["hsv_3"]
        self.Pigmento_PRESS( "HSV", self.color_index["hsv_1"], self.color_index["hsv_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # HSL
    def Channel_HSL_1_Value( self, value ):
        value = value / self.color_range["hsl_1"]
        self.Pigmento_PRESS( "HSL", value, self.color_index["hsl_2"], self.color_index["hsl_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_HSL_2_Value( self, value ):
        value = value / self.color_range["hsl_2"]
        self.Pigmento_PRESS( "HSL", self.color_index["hsl_1"], value, self.color_index["hsl_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_HSL_3_Value( self, value ):
        value = value / self.color_range["hsl_3"]
        self.Pigmento_PRESS( "HSL", self.color_index["hsl_1"], self.color_index["hsl_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # HCY
    def Channel_HCY_1_Value( self, value ):
        value = value / self.color_range["hcy_1"]
        self.Pigmento_PRESS( "HCY", value, self.color_index["hcy_2"], self.color_index["hcy_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_HCY_2_Value( self, value ):
        value = value / self.color_range["hcy_2"]
        self.Pigmento_PRESS( "HCY", self.color_index["hcy_1"], value, self.color_index["hcy_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_HCY_3_Value( self, value ):
        value = value / self.color_range["hcy_3"]
        self.Pigmento_PRESS( "HCY", self.color_index["hcy_1"], self.color_index["hcy_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # ARD
    def Channel_ARD_1_Value( self, value ):
        value = value / self.color_range["ard_1"]
        self.Pigmento_PRESS( "ARD", value, self.color_index["ard_2"], self.color_index["ard_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_ARD_2_Value( self, value ):
        value = value / self.color_range["ard_2"]
        self.Pigmento_PRESS( "ARD", self.color_index["ard_1"], value, self.color_index["ard_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_ARD_3_Value( self, value ):
        value = value / self.color_range["ard_3"]
        self.Pigmento_PRESS( "ARD", self.color_index["ard_1"], self.color_index["ard_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # XYZ
    def Channel_XYZ_1_Value( self, value ):
        value = value / self.color_range["xyz_1"]
        self.Pigmento_PRESS( "XYZ", value, self.color_index["xyz_2"], self.color_index["xyz_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_XYZ_2_Value( self, value ):
        value = value / self.color_range["xyz_2"]
        self.Pigmento_PRESS( "XYZ", self.color_index["xyz_1"], value, self.color_index["xyz_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_XYZ_3_Value( self, value ):
        value = value / self.color_range["xyz_3"]
        self.Pigmento_PRESS( "XYZ", self.color_index["xyz_1"], self.color_index["xyz_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # XYY
    def Channel_XYY_1_Value( self, value ):
        value = value / self.color_range["xyy_1"]
        self.Pigmento_PRESS( "XYY", value, self.color_index["xyy_2"], self.color_index["xyy_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_XYY_2_Value( self, value ):
        value = value / self.color_range["xyy_2"]
        self.Pigmento_PRESS( "XYY", self.color_index["xyy_1"], value, self.color_index["xyy_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_XYY_3_Value( self, value ):
        value = value / self.color_range["xyy_3"]
        self.Pigmento_PRESS( "XYY", self.color_index["xyy_1"], self.color_index["xyy_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # LAB
    def Channel_LAB_1_Value( self, value ):
        value = value / self.color_range["lab_1"]
        self.Pigmento_PRESS( "LAB", value, self.color_index["lab_2"], self.color_index["lab_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_LAB_2_Value( self, value ):
        value = value / self.color_range["lab_2"]
        self.Pigmento_PRESS( "LAB", self.color_index["lab_1"], value, self.color_index["lab_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_LAB_3_Value( self, value ):
        value = value / self.color_range["lab_3"]
        self.Pigmento_PRESS( "LAB", self.color_index["lab_1"], self.color_index["lab_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    # LCH
    def Channel_LCH_1_Value( self, value ):
        value = value / self.color_range["lch_1"]
        self.Pigmento_PRESS( "LCH", value, self.color_index["lch_2"], self.color_index["lch_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_LCH_2_Value( self, value ):
        value = value / self.color_range["lch_2"]
        self.Pigmento_PRESS( "LCH", self.color_index["lch_1"], value, self.color_index["lch_3"], 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )
    def Channel_LCH_3_Value( self, value ):
        value = value / self.color_range["lch_3"]
        self.Pigmento_PRESS( "LCH", self.color_index["lch_1"], self.color_index["lch_2"], value, 0, self.color_index )
        self.Label_String( f"{ round( value * 100, 2 ) } %" )

    #endregion
    #region UI LAYOUT CHANNEL Gradient

    # Gradient
    def Gradient_2( self, mode, mark, cl, cr, circle=False ):
        # mode = color space
        # mark = divisions
        # cl, cr = colors left and right in [0-1] range
        # circle = linear or circular

        len_l = len( cl )
        len_r = len( cr )
        if len_l == len_r:
            channel = len_l
            output = self.Gradient_Mark( mode, mark, cl, cr, channel, circle, 0, mark+1 )
            return output
    def Gradient_3( self, mode, mark, cl, cn, cr, circle=False ):
        # mode = color space
        # mark = divisions
        # cl, cn, cr = colors left , neutral and right in [0-1] range
        # circle = linear or circular

        # Variables
        len_l = len( cl )
        len_n = len( cn )
        len_r = len( cr )
        if len_l == len_n == len_r:
            # Size
            channel = len_l
            m2 = int( mark * 0.5 )
            o1 = self.Gradient_Mark( mode, m2, cl, cn, channel, circle, 0, m2 )
            o2 = self.Gradient_Mark( mode, m2, cn, cr, channel, circle, 0, m2+1 )
            # Construct
            output = list()
            for oi in o1:output.append( oi )
            for oi in o2:output.append( oi )
            return output
    def Gradient_Kelvin( self, mark, red, green, blue ):
        output = list()
        unit = kelvin_delta / mark
        for i in range( 0, mark+1 ):
            temp = kelvin_min + ( unit * i )
            srgb = self.convert.kelvin_to_srgb( temp )
            srgb = [ srgb[0] * red, srgb[1] * green, srgb[2] * blue ]
            output.append( srgb )
        return output
    # Colors
    def Gradient_Mark( self, mode, mark, cl, cr, channel, circle, start, end ):
        # Variables
        hue_rgb = [ "HSV", "HSL", "HCY", "ARD" ]
        hue_xyz = [ "LCH" ]
        positive = True
        # Left End
        point = list()
        if channel == 1:
            point.append( cl[0] )
        elif channel == 3:
            point.append( cl[0] )
            point.append( cl[1] )
            point.append( cl[2] )
        elif channel == 4:
            point.append( cl[0] )
            point.append( cl[1] )
            point.append( cl[2] )
            point.append( cl[3] )
        # Delta from Left
        delta = list()
        if channel == 1:
            delta.append( ( cr[0] - cl[0] ) / mark )
        elif channel == 3:
            # Channel 1
            if mode in hue_rgb and circle == True:
                da = cr[0] - cl[0]
                db = cl[0] + ( 1 - cr[0] )
                if da < db:
                    delta.append( da / mark )
                else:
                    delta.append( db / mark )
                    positive = False
            else:
                delta.append( ( cr[0] - cl[0] ) / mark )
            # Channel 2
            delta.append( ( cr[1] - cl[1] ) / mark )
            # Channel 3
            if mode in hue_xyz and circle == True:
                da = cr[2] - cl[2]
                db = cl[2] + ( 1 - cr[2] )
                if da < db:
                    delta.append( da / mark )
                else:
                    delta.append( db / mark )
                    positive = False
            else:
                delta.append( ( cr[2] - cl[2] ) / mark )
        elif channel == 4:
            delta.append( ( cr[0] - cl[0] ) / mark )
            delta.append( ( cr[1] - cl[1] ) / mark )
            delta.append( ( cr[2] - cl[2] ) / mark )
            delta.append( ( cr[3] - cl[3] ) / mark )
        # Cycle
        output = list()
        for i in range( start, end ):
            # Value Interpolated
            vector = list()
            if channel == 1:
                vector.append( point[0] + ( delta[0] * i ) )
            elif channel == 3:
                # Channel 1
                if mode in hue_rgb and positive == False:   vector.append( Limit_Looper( point[0] - ( delta[0] * i ), 1 ) )
                else:                                       vector.append( point[0] + ( delta[0] * i ) )
                # Channel 2
                vector.append( point[1] + ( delta[1] * i ) )
                # Channel 3
                if mode in hue_xyz and positive == False:   vector.append( Limit_Looper( point[2] - ( delta[2] * i ), 1 ) )
                else:                                       vector.append( point[2] + ( delta[2] * i ) )
            elif channel == 4:
                vector.append( point[0] + ( delta[0] * i ) )
                vector.append( point[1] + ( delta[1] * i ) )
                vector.append( point[2] + ( delta[2] * i ) )
                vector.append( point[3] + ( delta[3] * i ) )
            # Calculate RGB Linear
            if mode == "GRAY":  srgb = self.convert.gray_to_srgb( *vector )
            if mode == "SRGB":  srgb = vector
            if mode == "LRGB":  srgb = self.convert.lrgb_to_srgb( *vector )
            if mode == "CMYK":  srgb = self.convert.cmyk_to_srgb( *vector )
            if mode == "RYB":   srgb = self.convert.ryb_to_srgb( *vector )
            if mode == "YUV":   srgb = self.convert.yuv_to_srgb( *vector )
            # Calculate RGB Hue
            if mode == "HSV":   srgb = self.convert.hsv_to_srgb( *vector )
            if mode == "HSL":   srgb = self.convert.hsl_to_srgb( *vector )
            if mode == "HCY":   srgb = self.convert.hcy_to_srgb( *vector )
            if mode == "ARD":   srgb = self.convert.ard_to_srgb( *vector )
            # Calculate XYZ Linear
            if mode == "XYZ":   srgb = self.convert.xyz_to_srgb( *vector )
            if mode == "XYY":   srgb = self.convert.xyy_to_srgb( *vector )
            if mode == "LAB":   srgb = self.convert.lab_to_srgb( *vector )
            # Calculate XYZ Hue
            if mode == "LCH":   srgb = self.convert.lch_to_srgb( *vector )
            # Output
            output.append( srgb )
        return output

    #endregion
    #region UI LAYOUT Mixer Kelvin

    # Kelvin Pin
    def Kelvin_Load( self ):
        self.kelvin_pin_l.Update_Color( self.kelvin_l["display"], 1 )
        self.kelvin_pin_r.Update_Color( self.kelvin_r["display"], 1 )
    def Kelvin_Apply( self, index ):
        self.kelvin_p = index
        if index == 0:  self.Dict_Copy( self.color_index, self.kelvin_l )
        if index == 1:  self.Dict_Copy( self.color_index, self.kelvin_r )
        self.kelvin_slider.Set_Value( self.kelvin_p )
        self.Pigmento_SYNC()
    # Kelvin Slider
    def Kelvin_Slider( self, value ):
        self.Pole_Reset()
        self.kelvin_p = Limit_Float( value )
        self.kelvin_k = int( value * kelvin_delta ) + kelvin_min
        self.Pigmento_PRESS( "KELVIN", self.mix_index["srgb_1"], self.mix_index["srgb_2"], self.mix_index["srgb_3"], self.kelvin_k, self.color_index )
    def Kelvin_Mark( self, mark ):
        self.color_mark["kelvin"] = mark
        self.Mixer_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # Operator
    def Kelvin_Reset( self ):
        if self.kelvin_p != 0.5:
            self.kelvin_p = 0.5
            self.layout.kelvin_slider.blockSignals( True )
            self.kelvin_slider.Set_Value( self.kelvin_p )
            self.layout.kelvin_slider.blockSignals( False )

    #endregion
    #region UI LAYOUT Mixer Pole

    # Pole Pin
    def Pole_Load( self ):
        self.pole_pin_l.Update_Color( self.pole_l["display"], 1 )
        self.pole_pin_r.Update_Color( self.pole_r["display"], 1 )
    def Pole_Apply( self, index ):
        self.pole_p = index
        if index == 0:  self.Dict_Copy( self.color_index, self.pole_l )
        if index == 1:  self.Dict_Copy( self.color_index, self.pole_r )
        self.pole_slider.Set_Value( self.pole_p )
        self.Pigmento_SYNC()
    def Pole_Save( self, index ):
        if index == 0:
            self.Dict_Copy( self.pole_l, self.color_index )
            self.pole_pin_l.Update_Color( self.pole_l["display"], 1 )
        if index == 1:
            self.Dict_Copy( self.pole_r, self.color_index )
            self.pole_pin_r.Update_Color( self.pole_r["display"], 1 )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "pole_l", self.pole_l )
        Kritarc_Write( DOCKER_PICKER, "pole_r", self.pole_r )
    def Pole_Clean( self, index ):
        if index == 0:
            self.Dict_Copy( self.pole_l, color_false )
            self.pole_pin_l.Update_Clean()
        if index == 1:
            self.Dict_Copy( self.pole_r, color_false )
            self.pole_pin_r.Update_Clean()
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "pole_l", self.pole_l )
        Kritarc_Write( DOCKER_PICKER, "pole_r", self.pole_r )
    # Pole Slider
    def Pole_Slider( self, value ):
        self.Kelvin_Reset()
        self.pole_p = Limit_Float( value )
        if ( self.pole_l["active"] == True and self.pole_r["active"] == True ):
            color = self.Color_Interpolate_3( self.mixer_space, self.pole_l, self.mix_index, self.pole_r, self.pole_p )
            vector = self.Color_Vector( self.mixer_space, color, True )
            self.Pigmento_PRESS( self.mixer_space, vector[0], vector[1], vector[2], vector[3], self.color_index )
    def Pole_Mark( self, mark ):
        self.color_mark["pole"] = mark
        self.Mixer_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )
    # Operator
    def Pole_Reset( self ):
        if self.pole_p != 0.5:
            self.pole_p = 0.5
            self.layout.pole_slider.blockSignals( True )
            self.pole_slider.Set_Value( self.pole_p )
            self.layout.pole_slider.blockSignals( False )

    #endregion
    #region UI LAYOUT Mixer Linear

    # Linear Pin
    def Linear_Load( self ):
        self.linear_pin_l.Update_Color( self.linear_l["display"], 1 )
        self.linear_pin_r.Update_Color( self.linear_r["display"], 1 )
    def Linear_Apply( self, index ):
        self.linear_p = index
        if index == 0:  self.Dict_Copy( self.color_index, self.linear_l )
        if index == 1:  self.Dict_Copy( self.color_index, self.linear_r )
        self.linear_slider.Set_Value( self.linear_p )
        self.Pigmento_SYNC()
    def Linear_Save( self, index ):
        if index == 0:
            self.Dict_Copy( self.linear_l, self.color_index )
            self.linear_pin_l.Update_Color( self.linear_l["display"], 1 )
        if index == 1:
            self.Dict_Copy( self.linear_r, self.color_index )
            self.linear_pin_r.Update_Color( self.linear_r["display"], 1 )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "linear_l", self.linear_l )
        Kritarc_Write( DOCKER_PICKER, "linear_r", self.linear_r )
    def Linear_Clean( self, index ):
        if index == 0:
            self.Dict_Copy( self.linear_l, color_false )
            self.linear_pin_l.Update_Clean()
        if index == 1:
            self.Dict_Copy( self.linear_r, color_false )
            self.linear_pin_r.Update_Clean()
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "linear_l", self.linear_l )
        Kritarc_Write( DOCKER_PICKER, "linear_r", self.linear_r )
    # Linear Slider
    def Linear_Slider( self, value ):
        self.Mixer_Neutral()
        self.linear_p = value
        if ( self.linear_l["active"] == True and self.linear_r["active"] == True ):
            color = self.Color_Interpolate_2( self.mixer_space, self.linear_l, self.linear_r, self.linear_p )
            vector = self.Color_Vector( self.mixer_space, color, True )
            self.Pigmento_PRESS( self.mixer_space, vector[0], vector[1], vector[2], vector[3], self.color_index )
    def Linear_Mark( self, mark ):
        self.color_mark["linear"] = mark
        self.Mixer_Gradient()
        Kritarc_Write( DOCKER_PICKER, "color_mark", self.color_mark )

    #endregion
    #region UI LAYOUT PIN

    # Context Menu
    def Pin_Load( self, pin_color ):
        for i in range( 0, len( pin_color ) ):
            if pin_color[i]["active"] == True:  self.pin_module[i].Update_Color( pin_color[i]["display"], 1 )
            else:                               self.pin_module[i].Update_Clean()
    def Pin_Apply( self, index ):
        if self.pin_color[index]["active"] == True:
            self.Dict_Copy( self.color_index, self.pin_color[index] )
            self.Pigmento_SYNC()
    def Pin_Save( self, index ):
        self.Dict_Copy( self.pin_color[index], self.color_index )
        self.pin_module[index].Update_Color( self.pin_color[index]["display"], 1 )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "pin_color", self.pin_color )
    def Pin_Clean( self, index ):
        self.Dict_Copy( self.pin_color[index], color_false )
        self.pin_module[index].Update_Clean()
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "pin_color", self.pin_color )
    # Panel
    def Pin_Panel( self, mode, v1, v2, v3, index ):
        color = self.Color_Convert( mode, v1, v2, v3, 0, self.pin_color[index] )
        self.Dict_Copy( self.pin_color[index], color )
        self.pin_module[index].Update_Color( self.pin_color[index]["display"], 1 )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "pin_color", self.pin_color )

    #endregion
    #region UI LAYOUT HISTORY

    # Context Menu
    def History_Menu( self, event ):
        qmenu = QMenu( self )
        action_clear = qmenu.addAction( "Clear" )
        widget = self.layout.history_set.mapToGlobal( self.layout.history_list.geometry().topLeft() )
        mouse = event.pos()
        qpoint = QPoint( widget.x()+mouse.x(), widget.y()+mouse.y() )
        action = qmenu.exec_( qpoint )
        if action == action_clear:
            self.layout.history_list.clear()

    # Operations
    def History_List( self, hex_code ):
        # Variables
        limit = 100
        remove = list()
        count = self.layout.history_list.count()
        # Remove Cycle
        if self.cursor_inside == False:
            # Remove
            for i in range( 0, count ):
                item = self.layout.history_list.item( i )
                name = item.toolTip()
                if ( i > limit-2 ) or ( hex_code == name ):
                    remove.append( i )
            remove.reverse()
            for i in remove:
                self.layout.history_list.takeItem( i )
            # Add
            self.History_Add( hex_code )
        # User Interface
        self.layout.history_list.clearSelection()
    def History_Add( self, hex_code ):
        color = QColor( hex_code )
        pixmap = QPixmap( 20, 20 )
        pixmap.fill( color )
        item = QListWidgetItem()
        item.setToolTip( hex_code )
        item.setIcon( QIcon( pixmap ) )
        item.setBackground( QBrush( color ) )
        self.layout.history_list.insertItem( 0, item )
        if self.ui_history == True:
            self.layout.history_list.setCurrentRow( 0 )
    def History_Apply( self ):
        current = self.layout.history_list.currentItem()
        color = current.background().color()
        hex_code = color.name()
        self.Pigmento_APPLY( "HEX", hex_code, 0, 0, 0, self.color_index )

    #endregion
    #region UI LAYOUT FOOTER

    # Mode
    def Mode_Index( self, index ):
        self.mode_index = index
        # On
        if index == 0:
            self.layout.mode.setIcon( self.qicon_on )
            self.qtimer_pulse.start( check_timer )
        # Write
        if index == 1:
            self.layout.mode.setIcon( self.qicon_write )
            self.qtimer_pulse.stop()
        # Read
        if index == 2:
            self.layout.mode.setIcon( self.qicon_read )
            self.qtimer_pulse.start( check_timer )
        # Off
        if index == 3:
            self.layout.mode.setIcon( self.qicon_off )
            self.qtimer_pulse.stop()
    def Mode_Press( self, event ):
        # Menu
        qmenu = QMenu( self )
        # Actions
        action_on = qmenu.addAction( "ON" )
        action_write = qmenu.addAction( "WRITE" )
        action_read = qmenu.addAction( "READ" )
        action_off = qmenu.addAction( "OFF" )
        # Icons
        action_on.setIcon( self.qicon_on )
        action_write.setIcon( self.qicon_write )
        action_read.setIcon( self.qicon_read )
        action_off.setIcon( self.qicon_off )

        # Execute
        geo = self.layout.mode.geometry()
        qpoint = geo.bottomLeft()
        position = self.layout.footer.mapToGlobal( qpoint )
        action = qmenu.exec_( position )
        # Triggers
        if action == action_on:
            self.Mode_Index( 0 )
        elif action == action_write:
            self.Mode_Index( 1 )
        elif action == action_read:
            self.Mode_Index( 2 )
        elif action == action_off:
            self.Mode_Index( 3 )
    def Mode_Wheel( self, event ):
        increment = 0
        value = 20
        delta = event.angleDelta()
        delta_y = delta.y()
        if delta_y > +value: increment = -1
        if delta_y < -value: increment = +1
        if increment in [ -1, +1 ]:
            new_index = Limit_Range( self.mode_index + increment, 0, 3 )
            if self.mode_index != new_index:
                self.Mode_Index( new_index )

    # Fill
    def Menu_Fill( self, boolean ):
        if ( self.kcanvas != None ) and ( self.kview != None ):
            # Variables
            ad = Krita.instance().activeDocument()
            an = ad.activeNode()
            # UI
            self.fill_pixel["active"] = boolean
            if boolean == True:
                # Variables
                self.fill_pixel["node_uid"] = an.uniqueId()
                self.fill_pixel["alpha_lock"] = an.alphaLocked()
                # UI
                self.layout.fill_pixel.setIcon( self.qicon_fill_on )
                # Layers
                an.setAlphaLocked( boolean )
            else:
                # Layers
                node_uid = self.fill_pixel["node_uid"]
                alpha_lock = self.fill_pixel["alpha_lock"]
                try:ad.nodeByUniqueID( node_uid ).setAlphaLocked( alpha_lock )
                except:pass
                # UI
                self.layout.fill_pixel.setIcon( self.qicon_fill_off )
                # Variables
                self.fill_pixel["node_uid"] = None
                self.fill_pixel["alpha_lock"] = None
        else:
            self.Fill_None()
    def Fill_Check( self, kdocument ):
        try:
            check_alpha = Krita.instance().activeDocument().nodeByUniqueID( self.fill_pixel["node_uid"] ).alphaLocked()
            check_fill = self.fill_pixel["active"] == True and self.fill_pixel["node_uid"] == kdocument["n_uid"] and check_alpha == True
        except:
            check_fill = False
        return check_fill
    def Fill_None( self ):
        # Layers
        try:
            node = Krita.instance().activeDocument().nodeByUniqueID( self.fill_pixel["node_uid"] )
            try:node.setAlphaLocked( self.fill_pixel["alpha_lock"] )
            except:node.setAlphaLocked( False )
            else:pass
        except:
            pass
        # Variables
        self.fill_pixel["active"] = False
        self.fill_pixel["node_uid"] = None
        self.fill_pixel["alpha_lock"] = None
        # UI
        self.layout.fill_pixel.blockSignals( True )
        self.layout.fill_pixel.setIcon( Krita.instance().icon( "folder-documents" ) )
        self.layout.fill_pixel.setChecked( False )
        self.layout.fill_pixel.blockSignals( False )

    # Sample
    def SampleScreen_Press( self ):
        self.Label_String( "Sample Screen" )
        self.layout.sample_screen.setIcon( self.qicon_sampling_point )
    def SampleScreen_Move( self ):
        self.Label_String( "Sampling" )
    def SampleScreen_Release( self ):
        # Krita Action ( gives wrong colors on everything except the canvas)
        # Krita.instance().action( "sample_screen_color_real_canvas" ).trigger()

        # Screen Shot
        qscreen = self.layout.sample_screen.screen()
        geo = qscreen.geometry()
        qpixmap = qscreen.grabWindow( 0, geo.x(), geo.y(), geo.width(), geo.height() )
        qimage = qpixmap.toImage()
        # Cursor
        qcursor = QCursor()
        qpoint = qcursor.pos()
        # Picker
        qcolor = qimage.pixelColor( qpoint.x(), qpoint.y() )
        red = qcolor.redF()
        green = qcolor.greenF()
        blue = qcolor.blueF()
        # Apply
        self.Pigmento_APPLY( "SRGB", red, green, blue, 0, self.color_index )
        # Icon
        self.layout.sample_screen.setIcon( self.qicon_sample_screen )

    # String
    def Label_String( self, string ):
        self.layout.label.setText( str( string ) )
    # Settings
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

    #endregion
    #region UI DIALOG Geometry

    # Areas
    def UI_Harmony( self, boolean ):
        # Variables
        self.ui_harmony = boolean
        if boolean == True:
            text = "[HARMONY]"
            a = 10
            b = 20
            c = 10
        else:
            text = "HARMONY"
            a = 40
            b = 0
            c = 0
        # UI
        self.dialog.ui_harmony.setText( text )
        self.layout.color_header.setMinimumHeight( a )
        self.layout.color_header.setMaximumHeight( a )
        self.layout.harmony_swatch.setMinimumHeight( b )
        self.layout.harmony_swatch.setMaximumHeight( b )
        self.layout.harmony_span.setMinimumHeight( c )
        self.layout.harmony_span.setMaximumHeight( c )
        self.Harmony_Index( self.harmony_index )
        self.Size_Update()
        # Update
        Kritarc_Write( DOCKER_PICKER, "ui_harmony", self.ui_harmony )
    def UI_Channel( self, boolean ):
        # Variables
        self.ui_channel = boolean
        if boolean == True: text = "[CHANNEL]"
        else:               text = "CHANNEL"
        # UI
        self.dialog.ui_channel.setText( text )
        self.layout.channel_set.setMaximumHeight( int( qt_max * boolean ) )
        self.Size_Update()
        # Update
        Kritarc_Write( DOCKER_PICKER, "ui_channel", self.ui_channel )
    def UI_Mixer( self, boolean ):
        # Variables
        self.ui_mixer = boolean
        if boolean == True: text = "[MIXER]"
        else:               text = "MIXER"
        # UI
        self.dialog.ui_mixer.setText( text )
        self.layout.mixer_set.setMaximumHeight( int( qt_max * boolean ) )
        self.Size_Update()
        # Update
        Kritarc_Write( DOCKER_PICKER, "ui_mixer", self.ui_mixer )
    def UI_Pin( self, boolean ):
        # Variables
        self.ui_pin = boolean
        if boolean == True: text = "[PIN]"
        else:               text = "PIN"
        # UI
        self.dialog.ui_pin.setText( text )
        self.layout.pin_set.setMaximumHeight( int( 20 * boolean ) )
        self.Size_Update()
        # Update
        Kritarc_Write( DOCKER_PICKER, "ui_pin", self.ui_pin )
    def UI_History( self, boolean ):
        # Variables
        self.ui_history = boolean
        if boolean == True: text = "[HISTORY]"
        else:               text = "HISTORY"
        # UI
        self.dialog.ui_history.setText( text )
        self.layout.history_set.setMaximumHeight( int( 20 * boolean ) )
        self.Size_Update()
        # Update
        Kritarc_Write( DOCKER_PICKER, "ui_history", self.ui_history )

    # Layout
    def Edit_Layout( self, widget, boolean ):
        widget.setMinimumWidth( int( 5 * boolean ) )
        widget.setMaximumWidth( int( 120 * boolean ) )
        widget.setContentsMargins( int( 5 * boolean ), int( 2 * boolean ), int( 5 * boolean ), int( 2 * boolean ) )

    #endregion
    #region UI DIALOG Interface

    # Harmony
    def Harmony_Rule( self, harmony_rule ):
        self.harmony_rule = harmony_rule
        self.harmony_span.Set_Rule( self.harmony_rule )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "harmony_rule", self.harmony_rule )
    def Harmony_Edit( self, harmony_edit ):
        self.harmony_edit = harmony_edit
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "harmony_edit", self.harmony_edit )

    # Panels
    def Panel_Mode( self, panel_mode ):
        # UI
        if panel_mode == panel_fill:    self.layout.panel_set.setCurrentIndex( 0 )
        if panel_mode == panel_square:  self.layout.panel_set.setCurrentIndex( 1 )
        if panel_mode == panel_hue:     self.layout.panel_set.setCurrentIndex( 2 )
        if panel_mode == panel_gamut:   self.layout.panel_set.setCurrentIndex( 3 )
        if panel_mode == panel_hexagon: self.layout.panel_set.setCurrentIndex( 4 )
        if panel_mode == panel_luma:    self.layout.panel_set.setCurrentIndex( 5 )
        if panel_mode == panel_plane:   self.layout.panel_set.setCurrentIndex( 6 )
        if panel_mode == panel_mask:    self.layout.panel_set.setCurrentIndex( 7 )
        # Update
        if self.panel_mode != panel_mode:
            self.panel_mode = panel_mode
            self.Size_Update()
            self.Pigmento_SYNC()
        # Save
        Kritarc_Write( DOCKER_PICKER, "panel_mode", self.panel_mode )
    # Wheel
    def Wheel_Mode( self, wheel_mode ):
        self.wheel_mode = wheel_mode
        self.Pigmento_SYNC()
        self.Size_Update()
        self.Panel_Gradient( self.kmodel )
        Kritarc_Write( DOCKER_PICKER, "wheel_mode", self.wheel_mode )
    def Wheel_Space( self, wheel_space ):
        self.wheel_space = wheel_space
        self.Pigmento_SYNC()
        self.Size_Update()
        self.Panel_Gradient( self.kmodel )
        Kritarc_Write( DOCKER_PICKER, "wheel_space", self.wheel_space )

    # Options HUE
    def Hue_Shape( self, hue_shape ):
        self.hue_shape = hue_shape
        self.Pigmento_SYNC()
        self.Size_Update() # Updates Mask
        self.Panel_Gradient( self.kmodel )
        Kritarc_Write( DOCKER_PICKER, "hue_shape", self.hue_shape )
    # Options Gamut
    def Gamut_Mask( self, gamut_mask ):
        self.gamut_mask = gamut_mask
        self.panel_gamut.Set_Mask( self.gamut_mask )
        Kritarc_Write( DOCKER_PICKER, "gamut_mask", self.gamut_mask )
    def Gamut_Reset( self ):
        self.panel_gamut.Set_Reset( self.gamut_mask )
    # Options Mask
    def Mask_Folder( self, folder ):
        self.mask_folder = folder
        self.mask_url = os.path.normpath( os.path.join( self.mask_path, folder ) )
        self.Mask_Read( False )
        self.Panel_Mask_Gradient()
        Kritarc_Write( DOCKER_PICKER, "mask_folder", self.mask_folder )
    def Mask_Edit( self, mask_edit ):
        self.mask_edit = mask_edit
        self.Edit_Layout( self.layout.edit_mask, self.mask_edit )
        self.Size_Update()
        self.Panel_Mask_Gradient()
        Kritarc_Write( DOCKER_PICKER, "mask_edit", self.mask_edit )

    # Mixer
    def Mixer_Space( self, mixer_space ):
        self.mixer_space = mixer_space
        self.Panel_Plane_Gradient( True ) # Panel Plane
        self.Mixer_Gradient() # Kelvin Pole Linear
        Kritarc_Write( DOCKER_PICKER, "mixer_space", self.mixer_space )

    #endregion
    #region UI DIALOG Color

    # Channel Display
    def Channel_GRAY_Display( self, boolean ):
        self.color_view["gray"] = boolean
        if boolean == True:
            maxi = qt_max
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0
        # layout
        self.layout.gray_label.setMaximumHeight( maxi )
        self.layout.gray_slider.setMaximumHeight( maxi )
        self.layout.gray_value.setMaximumHeight( maxi )
        self.layout.gray_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.gray_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.gray_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.gray_label_layout.setSpacing( vert )
        self.layout.gray_slider_layout.setSpacing( vert )
        self.layout.gray_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_SRGB_Display( self, boolean ):
        self.color_view["srgb"] = boolean
        if boolean == True:
            maxi = qt_max
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0
        # layout
        self.layout.srgb_label.setMaximumHeight( maxi )
        self.layout.srgb_slider.setMaximumHeight( maxi )
        self.layout.srgb_value.setMaximumHeight( maxi )
        self.layout.srgb_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.srgb_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.srgb_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.srgb_label_layout.setSpacing( vert )
        self.layout.srgb_slider_layout.setSpacing( vert )
        self.layout.srgb_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_LRGB_Display( self, boolean ):
        self.color_view["lrgb"] = boolean
        if boolean == True:
            maxi = qt_max
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0
        # layout
        self.layout.lrgb_label.setMaximumHeight( maxi )
        self.layout.lrgb_slider.setMaximumHeight( maxi )
        self.layout.lrgb_value.setMaximumHeight( maxi )
        self.layout.lrgb_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lrgb_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lrgb_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.lrgb_label_layout.setSpacing( vert )
        self.layout.lrgb_slider_layout.setSpacing( vert )
        self.layout.lrgb_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_CMYK_Display( self, boolean ):
        self.color_view["cmyk"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.cmyk_label_layout.setSpacing( vert )
        self.layout.cmyk_slider_layout.setSpacing( vert )
        self.layout.cmyk_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_RYB_Display( self, boolean ):
        self.color_view["ryb"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.ryb_label_layout.setSpacing( vert )
        self.layout.ryb_slider_layout.setSpacing( vert )
        self.layout.ryb_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_YUV_Display( self, boolean ):
        self.color_view["yuv"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.yuv_label_layout.setSpacing( vert )
        self.layout.yuv_slider_layout.setSpacing( vert )
        self.layout.yuv_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_HSV_Display( self, boolean ):
        self.color_view["hsv"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.hsv_label_layout.setSpacing( vert )
        self.layout.hsv_slider_layout.setSpacing( vert )
        self.layout.hsv_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_HSL_Display( self, boolean ):
        self.color_view["hsl"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.hsl_label_layout.setSpacing( vert )
        self.layout.hsl_slider_layout.setSpacing( vert )
        self.layout.hsl_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_HCY_Display( self, boolean ):
        self.color_view["hcy"] = boolean
        if boolean == True:
            maxi = qt_max
            horz = 0
            vert = 1
        else:
            maxi = 0
            horz = 0
            vert = 0
        # layout
        self.layout.hcy_label.setMaximumHeight( maxi )
        self.layout.hcy_slider.setMaximumHeight( maxi )
        self.layout.hcy_value.setMaximumHeight( maxi )
        self.layout.hcy_label_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hcy_slider_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hcy_value_layout.setContentsMargins( horz, vert, horz, vert )
        self.layout.hcy_label_layout.setSpacing( vert )
        self.layout.hcy_slider_layout.setSpacing( vert )
        self.layout.hcy_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_ARD_Display( self, boolean ):
        self.color_view["ard"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.ard_label_layout.setSpacing( vert )
        self.layout.ard_slider_layout.setSpacing( vert )
        self.layout.ard_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_XYZ_Display( self, boolean ):
        self.color_view["xyz"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.xyz_label_layout.setSpacing( vert )
        self.layout.xyz_slider_layout.setSpacing( vert )
        self.layout.xyz_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_XYY_Display( self, boolean ):
        self.color_view["xyy"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.xyy_label_layout.setSpacing( vert )
        self.layout.xyy_slider_layout.setSpacing( vert )
        self.layout.xyy_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_LAB_Display( self, boolean ):
        self.color_view["lab"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.lab_label_layout.setSpacing( vert )
        self.layout.lab_slider_layout.setSpacing( vert )
        self.layout.lab_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_LCH_Display( self, boolean ):
        self.color_view["lch"] = boolean
        if boolean == True:
            maxi = qt_max
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
        self.layout.lch_label_layout.setSpacing( vert )
        self.layout.lch_slider_layout.setSpacing( vert )
        self.layout.lch_value_layout.setSpacing( vert )
        # Update
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    # Mixer Display
    def Mixer_KELVIN_Display( self, boolean ):
        self.color_view["kelvin"] = boolean
        if boolean == True:
            maxi = 17
        else:
            maxi = 0
        self.layout.kelvin_set.setMaximumHeight( maxi )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Mixer_POLE_Display( self, boolean ):
        self.color_view["pole"] = boolean
        if boolean == True:
            maxi = 17
        else:
            maxi = 0
        self.layout.pole_set.setMaximumHeight( maxi )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Mixer_LINEAR_Display( self, boolean ):
        self.color_view["linear"] = boolean
        if boolean == True:
            maxi = 17
        else:
            maxi = 0
        self.layout.linear_set.setMaximumHeight( maxi )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    # Code Display
    def Code_HEX_Display( self, boolean ):
        self.color_view["hex6"] = boolean
        self.Channel_HEX_SUM( self.color_view["hex6"], self.color_view["sum4"] )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Code_SUM_Display( self, boolean ):
        self.color_view["sum4"] = boolean
        self.Channel_HEX_SUM( self.color_view["hex6"], self.color_view["sum4"] )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_view", self.color_view )
    def Channel_HEX_SUM( self, code_hex, code_sum ):
        if code_hex == True and code_sum == True:
            self.layout.hex_string.setMaximumWidth( 60 )
            self.layout.sum_string.setMaximumWidth( 60 )
        elif code_hex == True or code_sum == True:
            self.layout.hex_string.setMaximumWidth( int( 120 * code_hex ) )
            self.layout.sum_string.setMaximumWidth( int( 120 * code_sum ) )
        else:
            self.layout.hex_string.setMaximumWidth( 0 )
            self.layout.sum_string.setMaximumWidth( 0 )

    # Channel Range
    def Channel_GRAY_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["gray_1"] = value
        self.layout.gray_1_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_SRGB_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["srgb_1"] = value
        self.color_range["srgb_2"] = value
        self.color_range["srgb_3"] = value
        self.layout.srgb_1_value.setMaximum( value )
        self.layout.srgb_2_value.setMaximum( value )
        self.layout.srgb_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_LRGB_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["lrgb_1"] = value
        self.color_range["lrgb_2"] = value
        self.color_range["lrgb_3"] = value
        self.layout.lrgb_1_value.setMaximum( value )
        self.layout.lrgb_2_value.setMaximum( value )
        self.layout.lrgb_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_CMYK_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["cmyk_1"] = value
        self.color_range["cmyk_2"] = value
        self.color_range["cmyk_3"] = value
        self.color_range["cmyk_4"] = value
        self.layout.cmyk_1_value.setMaximum( value )
        self.layout.cmyk_2_value.setMaximum( value )
        self.layout.cmyk_3_value.setMaximum( value )
        self.layout.cmyk_4_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_RYB_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["ryb_1"] = value
        self.color_range["ryb_2"] = value
        self.color_range["ryb_3"] = value
        self.layout.ryb_1_value.setMaximum( value )
        self.layout.ryb_2_value.setMaximum( value )
        self.layout.ryb_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_YUV_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["yuv_1"] = value
        self.color_range["yuv_2"] = value
        self.color_range["yuv_3"] = value
        self.layout.yuv_1_value.setMaximum( value )
        self.layout.yuv_2_value.setMaximum( value )
        self.layout.yuv_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_HUE_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["hsv_1"] = value
        self.color_range["hsl_1"] = value
        self.color_range["hcy_1"] = value
        self.color_range["ard_1"] = value
        self.color_range["ard_3"] = value # ARD=360
        self.layout.hsv_1_value.setMaximum( value )
        self.layout.hsl_1_value.setMaximum( value )
        self.layout.hcy_1_value.setMaximum( value )
        self.layout.ard_1_value.setMaximum( value )
        self.layout.ard_3_value.setMaximum( value ) # ARD=360
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_HSV_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["hsv_2"] = value
        self.color_range["hsv_3"] = value
        self.layout.hsv_2_value.setMaximum( value )
        self.layout.hsv_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_HSL_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["hsl_2"] = value
        self.color_range["hsl_3"] = value
        self.layout.hsl_2_value.setMaximum( value )
        self.layout.hsl_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_HCY_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["hcy_2"] = value
        self.color_range["hcy_3"] = value
        self.layout.hcy_2_value.setMaximum( value )
        self.layout.hcy_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_ARD_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["ard_2"] = value
        # self.color_range["ard_3"] = value # ARD=255
        self.layout.ard_2_value.setMaximum( value )
        # self.layout.ard_3_value.setMaximum( value ) # ARD=255
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_XYZ_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["xyz_1"] = value
        self.color_range["xyz_2"] = value
        self.color_range["xyz_3"] = value
        self.layout.xyz_1_value.setMaximum( value )
        self.layout.xyz_2_value.setMaximum( value )
        self.layout.xyz_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_XYY_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["xyy_1"] = value
        self.color_range["xyy_2"] = value
        self.color_range["xyy_3"] = value
        self.layout.xyy_1_value.setMaximum( value )
        self.layout.xyy_2_value.setMaximum( value )
        self.layout.xyy_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_LAB_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["lab_1"] = value
        self.color_range["lab_2"] = value
        self.color_range["lab_3"] = value
        self.layout.lab_1_value.setMaximum( value )
        self.layout.lab_2_value.setMaximum( value )
        self.layout.lab_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )
    def Channel_LCH_Range( self, value ):
        value = Limit_Unit( value )
        self.color_range["lch_1"] = value
        self.color_range["lch_2"] = value
        self.color_range["lch_3"] = value
        self.layout.lch_1_value.setMaximum( value )
        self.layout.lch_2_value.setMaximum( value )
        self.layout.lch_3_value.setMaximum( value )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "color_range", self.color_range )

    # Channel Reset
    def Channel_GRAY_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_gray.setValue( value )
        self.Channel_GRAY_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_SRGB_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_srgb.setValue( value )
        self.Channel_SRGB_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_LRGB_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_lrgb.setValue( value )
        self.Channel_LRGB_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_CMYK_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_cmyk.setValue( value )
        self.Channel_CMYK_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_RYB_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_ryb.setValue( value )
        self.Channel_RYB_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_YUV_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_yuv.setValue( value )
        self.Channel_YUV_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_HUE_Reset( self ):
        value = 360
        self.dialog.range_hue.setValue( 360 )
        self.Channel_HUE_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_HSV_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_hsv.setValue( value )
        self.Channel_HSV_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_HSL_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_hsl.setValue( value )
        self.Channel_HSL_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_HCY_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_hcy.setValue( value )
        self.Channel_HCY_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_ARD_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_ard.setValue( value )
        self.Channel_ARD_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_XYZ_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_xyz.setValue( value )
        self.Channel_XYZ_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_XYY_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_xyy.setValue( value )
        self.Channel_XYY_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_LAB_Reset( self ):
        value = int( self.kdepth ) + 1
        self.dialog.range_lab.setValue( value )
        self.Channel_LAB_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    def Channel_LCH_Reset( self ):
        value = int( self.kdepth )
        self.dialog.range_lch.setValue( value )
        self.Channel_LCH_Range( value )
        self.Pigmento_SYNC()
        self.Reset_UnFocus()
    # Reset Focus
    def Reset_UnFocus( self ):
        self.dialog.range_gray.clearFocus()
        self.dialog.range_srgb.clearFocus()
        self.dialog.range_lrgb.clearFocus()
        self.dialog.range_cmyk.clearFocus()
        self.dialog.range_ryb.clearFocus()
        self.dialog.range_yuv.clearFocus()
        self.dialog.range_hue.clearFocus()
        self.dialog.range_hsv.clearFocus()
        self.dialog.range_hsl.clearFocus()
        self.dialog.range_hcy.clearFocus()
        self.dialog.range_ard.clearFocus()
        self.dialog.range_xyz.clearFocus()
        self.dialog.range_xyy.clearFocus()
        self.dialog.range_lab.clearFocus()
        self.dialog.range_lch.clearFocus()

    # Format
    def Format_Label( self, boolean ):
        # Variables
        self.format_index = boolean
        if boolean == True:
            l = 25
        else:
            l = 0
        # UI
        self.layout.gray_label.setMaximumWidth( l )
        self.layout.srgb_label.setMaximumWidth( l )
        self.layout.lrgb_label.setMaximumWidth( l )
        self.layout.cmyk_label.setMaximumWidth( l )
        self.layout.ryb_label.setMaximumWidth( l )
        self.layout.yuv_label.setMaximumWidth( l )
        self.layout.hsv_label.setMaximumWidth( l )
        self.layout.hsl_label.setMaximumWidth( l )
        self.layout.hcy_label.setMaximumWidth( l )
        self.layout.ard_label.setMaximumWidth( l )
        self.layout.xyz_label.setMaximumWidth( l )
        self.layout.xyy_label.setMaximumWidth( l )
        self.layout.lab_label.setMaximumWidth( l )
        self.layout.lch_label.setMaximumWidth( l )
        # Update
        self.Size_Update()
        Kritarc_Write( DOCKER_PICKER, "format_index", self.format_index )
    def Format_Value( self, boolean ):
        # Variables
        self.format_value = boolean
        if boolean == True:
            v = 100
        else:
            v = 0
        # Ui
        self.layout.gray_value.setMaximumWidth( v )
        self.layout.srgb_value.setMaximumWidth( v )
        self.layout.lrgb_value.setMaximumWidth( v )
        self.layout.cmyk_value.setMaximumWidth( v )
        self.layout.ryb_value.setMaximumWidth( v )
        self.layout.yuv_value.setMaximumWidth( v )
        self.layout.hsv_value.setMaximumWidth( v )
        self.layout.hsl_value.setMaximumWidth( v )
        self.layout.hcy_value.setMaximumWidth( v )
        self.layout.ard_value.setMaximumWidth( v )
        self.layout.xyz_value.setMaximumWidth( v )
        self.layout.xyy_value.setMaximumWidth( v )
        self.layout.lab_value.setMaximumWidth( v )
        self.layout.lch_value.setMaximumWidth( v )
        # Update
        self.Size_Update()
        Kritarc_Write( DOCKER_PICKER, "format_value", self.format_value )
    def Format_Hueshine( self, boolean ):
        self.format_hueshine = boolean
        self.Channel_Gradient()
        Kritarc_Write( DOCKER_PICKER, "format_hueshine", self.format_hueshine )

    #endregion
    #region UI DIALOG Extra

    # Analyse
    def Analyse_Document( self ):
        # Variables
        self.analyse_list = None
        # Read
        qimage = self.Analyse_Alpha()
        if qimage != None:
            self.Analyse_Pixel( qimage )
    def Analyse_Alpha( self ):
        qimage = None
        if ( self.kcanvas != None ) and ( self.kview != None ):
            # Variables
            ki = Krita.instance()
            ad = ki.activeDocument()
            n_cd = ad.activeNode().colorDepth()
            k = self.kdepth

            # Source
            ss = ad.selection()
            if ss == None:
                dx = int( 0 )
                dy = int( 0 )
                dw = int( ad.width() )
                dh = int( ad.height() )
            else:
                dx = int( ss.x() )
                dy = int( ss.y() )
                dw = int( ss.width() )
                dh = int( ss.height() )

            # QImage
            qimage = ad.projection( dx, dy, dw, dh )

            # Selection into Alpha
            if ss != None:
                # Selection
                pds = ss.pixelData( dx, dy, dw, dh )
                num_array = self.analyse.Bytes_to_Integer( pds, n_cd )

                # Clip
                counter = 0
                for h in range( 0, dh ):
                    for w in range( 0, dw ):
                        # Variables
                        s = num_array[counter] / k
                        # Read
                        qcolor = qimage.pixelColor( w, h )
                        a = qcolor.alphaF()
                        # Logic
                        var = a * s
                        # Write
                        qcolor.setAlphaF( var )
                        qimage.setPixelColor( w, h, qcolor )
                        # Cycle
                        counter += 1
        return qimage
    def Analyse_Pixel( self, qimage ):
        if qimage.isNull() == False:
            # Scale
            size = 200
            if qimage.width() > size and qimage.height() > size:
                qimage = qimage.scaled( size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation )
            # Variables
            width = qimage.width()
            height = qimage.height()
            # Progress Bar
            self.layout.progress_bar.setValue( 0 )
            self.layout.progress_bar.setMaximum( height )
            # Variables
            list_name = list()
            self.analyse_list = list()
            # Pixel Check
            for h in range( 0, height ):
                # Progress Bar
                h1 = ( h + 1 )
                if h1 % 10 == 0:
                    self.layout.progress_bar.setValue( h1 )
                    QApplication.processEvents()
                for w in range( 0, width ):
                    # Read
                    qcolor = qimage.pixelColor( w, h )
                    name = qcolor.name()
                    alpha = qcolor.alphaF()
                    # List
                    if ( alpha > 0 ) and ( name not in list_name ):
                        list_name.append( name )
                        cor = self.Color_Convert( "HEX", name, 0, 0, 0, color_neutral.copy() )
                        self.analyse_list.append( cor )
            # Update
            self.layout.progress_bar.setValue( 0 )
            self.layout.progress_bar.setMaximum( 1 )
            self.Pigmento_SYNC()
            Message_Log( "ANALYSE", "Complete" )
    def Analyse_Display( self, boolean ):
        self.analyse_display = boolean
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "analyse_display", self.analyse_display )

    # Shortcuts
    def Key_1_Mode( self, mode ):
        self.key_1_mode = mode
        Kritarc_Write( DOCKER_PICKER, "key_1_mode", self.key_1_mode )
    def Key_2_Mode( self, mode ):
        self.key_2_mode = mode
        Kritarc_Write( DOCKER_PICKER, "key_2_mode", self.key_2_mode )
    def Key_3_Mode( self, mode ):
        self.key_3_mode = mode
        Kritarc_Write( DOCKER_PICKER, "key_3_mode", self.key_3_mode )
    def Key_4_Mode( self, mode ):
        self.key_4_mode = mode
        Kritarc_Write( DOCKER_PICKER, "key_4_mode", self.key_4_mode )
    def Key_1_Unit( self, unit ):
        self.key_1_unit = unit
        Kritarc_Write( DOCKER_PICKER, "key_1_unit", self.key_1_unit )
    def Key_2_Unit( self, unit ):
        self.key_2_unit = unit
        Kritarc_Write( DOCKER_PICKER, "key_2_unit", self.key_2_unit )
    def Key_3_Unit( self, unit ):
        self.key_3_unit = unit
        Kritarc_Write( DOCKER_PICKER, "key_3_unit", self.key_3_unit )
    def Key_4_Unit( self, unit ):
        self.key_4_unit = unit
        Kritarc_Write( DOCKER_PICKER, "key_4_unit", self.key_4_unit )

    # Reference
    def Name_Display( self ):
        color_name = self.dialog.name_display.text()
        if color_name != "":
            try:
                hc = QApplication.clipboard()
                hc.clear()
                hc.setText( color_name )
                self.Label_String( "NAME COPY" )
            except:
                pass
    def Name_Closest( self ):
        hex_start = self.color_index["hex6"]
        ps = self.convert.hex6_to_srgb( hex_start )
        list_code = list()
        list_key = color_name.keys()
        for key in color_name:
            pe = self.convert.hex6_to_srgb( key )
            dist = Trig_3D_Points_Distance( ps[0], ps[1], ps[2], pe[0], pe[1], pe[2] )
            list_code.append( [ dist, key ] )
        list_code.sort()
        self.Pigmento_APPLY( "HEX", list_code[0][1], 0, 0, 0, self.color_index )

    #endregion
    #region UI DIALOG System

    # Colors Spaces
    def CS_Luminosity( self, cs_luminosity ):
        self.cs_luminosity = cs_luminosity
        self.convert.Set_Luminosity( self.cs_luminosity )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "cs_luminosity", self.cs_luminosity )
    def CS_Matrix( self, cs_matrix ):
        self.cs_matrix = cs_matrix
        self.convert.Set_Matrix( self.cs_matrix )
        self.Pigmento_SYNC()
        Kritarc_Write( DOCKER_PICKER, "cs_matrix", self.cs_matrix )

    # Performance
    def Performace_Release( self, boolean ):
        self.performance_release = boolean
        Kritarc_Write( DOCKER_PICKER, "performance_release", self.performance_release )

    # Help
    def Menu_Manual( self ):
        url = "https://github.com/EyeOdin/Pigment.O/wiki"
        webbrowser.open_new( url )
    def Menu_License( self ):
        url = "https://github.com/EyeOdin/Pigment.O/blob/master/LICENSE"
        webbrowser.open_new( url )

    #endregion
    #region HEX SUM

    # Hex
    def HEX_Valid( self, hex_code, length ):
        valid = False
        if  hex_code not in [ "", None ]:
            # Variables
            valid = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"]
            # Checks
            checks = list()
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
    def HEX_Copy( self, hex_code ):
        if self.cursor_inside == True:
            try:
                clip_board = QApplication.clipboard()
                clip_board.clear()
                clip_board.setText( hex_code )
            except:
                pass

    #endregion
    #region Extension

    # COR
    def Extension_PIN( self, index ):
        self.Pin_Apply( index )
    # KEYs
    def Extension_KEY( self, index, value ):
        if index == 1:
            mode = self.key_1_mode
            value = self.key_1_unit * value
        if index == 2:
            mode = self.key_2_mode
            value = self.key_2_unit * value
        if index == 3:
            mode = self.key_3_mode
            value = self.key_3_unit * value
        if index == 4:
            mode = self.key_4_mode
            value = self.key_4_unit * value
        self.Extension_KEY_Color( mode, value )
    def Extension_KEY_Color( self, mode, value ):
        # GRAY
        if mode == "GRAY_1":    self.Channel_GRAY_1_Increment( value )
        # RGB
        if mode == "SRGB_1":    self.Channel_SRGB_1_Increment( value )
        if mode == "SRGB_2":    self.Channel_SRGB_2_Increment( value )
        if mode == "SRGB_3":    self.Channel_SRGB_3_Increment( value )
        # LRGB
        if mode == "LRGB_1":    self.Channel_LRGB_1_Increment( value )
        if mode == "LRGB_2":    self.Channel_LRGB_2_Increment( value )
        if mode == "LRGB_3":    self.Channel_LRGB_3_Increment( value )
        # CMYK
        if mode == "CMYK_1":    self.Channel_CMYK_1_Increment( value )
        if mode == "CMYK_2":    self.Channel_CMYK_2_Increment( value )
        if mode == "CMYK_3":    self.Channel_CMYK_3_Increment( value )
        if mode == "CMYK_4":    self.Channel_CMYK_4_Increment( value )
        # RYB
        if mode == "RYB_1":     self.Channel_RYB_1_Increment( value )
        if mode == "RYB_2":     self.Channel_RYB_2_Increment( value )
        if mode == "RYB_3":     self.Channel_RYB_3_Increment( value )
        # YUV
        if mode == "YUV_1":     self.Channel_YUV_1_Increment( value )
        if mode == "YUV_2":     self.Channel_YUV_2_Increment( value )
        if mode == "YUV_3":     self.Channel_YUV_3_Increment( value )
        # HSV
        if mode == "HSV_1":     self.Channel_HSV_1_Increment( value )
        if mode == "HSV_2":     self.Channel_HSV_2_Increment( value )
        if mode == "HSV_3":     self.Channel_HSV_3_Increment( value )
        # HSL
        if mode == "HSL_1":     self.Channel_HSL_1_Increment( value )
        if mode == "HSL_2":     self.Channel_HSL_2_Increment( value )
        if mode == "HSL_3":     self.Channel_HSL_3_Increment( value )
        # HCY
        if mode == "HCY_1":     self.Channel_HCY_1_Increment( value )
        if mode == "HCY_2":     self.Channel_HCY_2_Increment( value )
        if mode == "HCY_3":     self.Channel_HCY_3_Increment( value )
        # ARD
        if mode == "ARD_1":     self.Channel_ARD_1_Increment( value )
        if mode == "ARD_2":     self.Channel_ARD_2_Increment( value )
        if mode == "ARD_3":     self.Channel_ARD_3_Increment( value )
        # XYZ
        if mode == "XYZ_1":     self.Channel_XYZ_1_Increment( value )
        if mode == "XYZ_2":     self.Channel_XYZ_2_Increment( value )
        if mode == "XYZ_3":     self.Channel_XYZ_3_Increment( value )
        # XYY
        if mode == "XYY_1":     self.Channel_XYY_1_Increment( value )
        if mode == "XYY_2":     self.Channel_XYY_2_Increment( value )
        if mode == "XYY_3":     self.Channel_XYY_3_Increment( value )
        # LAB
        if mode == "LAB_1":     self.Channel_LAB_1_Increment( value )
        if mode == "LAB_2":     self.Channel_LAB_2_Increment( value )
        if mode == "LAB_3":     self.Channel_LAB_3_Increment( value )
        # LCH
        if mode == "LCH_1":     self.Channel_LCH_1_Increment( value )
        if mode == "LCH_2":     self.Channel_LCH_2_Increment( value )
        if mode == "LCH_3":     self.Channel_LCH_3_Increment( value )
    # LOCKs
    def Extension_LOCK( self, lock ):
        if lock == "CMYK":  self.layout.cmyk_4_label.setChecked( not self.layout.cmyk_4_label.isChecked() )

    #endregion
    #region Printer

    # Print
    def Print_Button( self ):
        # Color Space
        if self.panel_mode == panel_square:                                 space = self.wheel_space
        if self.panel_mode == panel_hue and self.hue_shape == "TRIANGLE":   space = "HSL"
        if self.panel_mode == panel_hue and self.hue_shape == "SQUARE":     space = self.wheel_space
        if self.panel_mode == panel_hue and self.hue_shape == "DIAMOND":    space = "HSL"
        if self.panel_mode == panel_gamut:                                  space = self.wheel_space
        if self.panel_mode == panel_hexagon:                                space = "UVD"
        if self.panel_mode == panel_luma:                                   space = "YUV"
        # Geometry
        if self.panel_mode == panel_square:                                 geometry = "S4"
        if self.panel_mode == panel_hue and self.hue_shape == "TRIANGLE":   geometry = "S3"
        if self.panel_mode == panel_hue and self.hue_shape == "SQUARE":     geometry = "S4"
        if self.panel_mode == panel_hue and self.hue_shape == "DIAMOND":    geometry = "SD"
        if self.panel_mode == panel_gamut and self.wheel_mode == "DIGITAL": geometry = "GD"
        if self.panel_mode == panel_gamut and self.wheel_mode == "ANALOG":  geometry = "GA"
        if self.panel_mode == panel_hexagon:                                geometry = "H6"
        if self.panel_mode == panel_luma:                                   geometry = "Y4"
        # Operation Confirmation
        message = f"This operation will take a couple of minutes\nCreate { self.kdocument['cmodel'] }_{ space }_{ geometry }.zip ?"
        boolean = QMessageBox.question( QWidget(), DOCKER_PICKER, message, QMessageBox.Yes, QMessageBox.Abort )
        if boolean == QMessageBox.Yes:
            self.Print_Process( space, geometry )
    # Worker
    def Print_Process( self, space, geometry ):
        thread = True
        if thread == False: self.Print_Single( space, geometry )
        if thread == True:  self.Print_Thread( space, geometry )
    def Print_Connect( self ):
        self.print_worker = Worker_Print()
    def Print_Single( self, space, geometry ):
        self.Print_Connect()
        self.print_worker.run( self, space, geometry, False )
    def Print_Thread( self, space, geometry ):
        # Thread
        self.print_qthread = QtCore.QThread()
        # Worker
        self.Print_Connect()
        self.print_worker.moveToThread( self.print_qthread )
        # Thread
        self.print_qthread.started.connect( lambda : self.print_worker.run( self, space, geometry, True ) )
        self.print_qthread.start()

    #endregion
    #region Notifier

    # Notifier
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
        # Module
        ki = Krita.instance()
        self.window = ki.activeWindow()
        # Signals
        self.window.activeViewChanged.connect( self.View_Changed )
        self.window.themeChanged.connect( self.Theme_Changed )
        self.window.windowClosed.connect( self.Window_Closed )
    def Window_IsBeingCreated( self ):
        pass

    # Window
    def View_Changed( self ):
        pass
    def Theme_Changed( self ):
        self.Style_Icon()
        self.Style_Theme()
    def Window_Closed( self ):
        pass

    #endregion
    #region Widget Events

    # QWidget
    def showEvent( self, event ):
        # Sampler
        self.Import_Sampler()
        # UI
        self.Size_Update()
        # QTimer
        self.qtimer_pulse.start( check_timer )
    def resizeEvent( self, event ):
        # self.Size_Print()
        self.Size_Update()
    def enterEvent( self, event ):
        self.cursor_inside = True
    def leaveEvent( self, event ):
        self.cursor_inside = False
        self.Focus_Clear()
        self.Pigmento_SYNC()
    def closeEvent( self, event ):
        try:self.qtimer_pulse.stop()
        except:pass
    # QEventFilter
    def eventFilter( self, source, event ):
        # Event
        et = event.type()
        modifier_all = QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier
        # Panels
        panels = [
            # Panel
            self.layout.panel_set,
            self.layout.panel_mask,
            # Channel
            self.layout.gray_slider,
            self.layout.srgb_slider,
            self.layout.lrgb_slider,
            self.layout.cmyk_slider,
            self.layout.ryb_slider,
            self.layout.yuv_slider,
            self.layout.hsv_slider,
            self.layout.hsl_slider,
            self.layout.hcy_slider,
            self.layout.ard_slider,
            self.layout.xyz_slider,
            self.layout.xyy_slider,
            self.layout.lab_slider,
            self.layout.lch_slider,
            # Sets
            self.layout.mixer_set,
            self.layout.pin_set,
            self.layout.history_set,
            ]
        if ( et == QEvent.Resize and source in panels ):
            self.Size_Update()
        if ( et == QEvent.ContextMenu and source == self.layout.history_list ):
            self.History_Menu( event )
        # Mode
        if ( et == QEvent.MouseButtonPress and source is self.layout.mode ):
            self.Mode_Press( event )
        if ( et == QEvent.Wheel and source is self.layout.mode ):
            self.Mode_Wheel( event )
        # Settings
        if ( et == QEvent.MouseButtonPress and event.modifiers() == modifier_all and source is self.layout.settings ):
            self.Size_Standard()
        return super().eventFilter( source, event )
    # Krita Canvas
    def canvasChanged( self, canvas ):
        # Canvas
        self.kcanvas = canvas
        if canvas == None: self.kview = None
        else:              self.kview = canvas.view()
        # Color Model
        self.kdocument = self.Document_Active()
        self.Panel_Document( self.kdocument )

    #endregion
    #region Notes

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
    """

    """
    # qimage = QImage( byte_array, width, height, QImage.Format_RGBA8888 )
    """

    """
    # Krita Theme
    color_theme = QApplication.palette().color( QPalette.Window )
    if color_theme.value() > 128:
        self.color_1 = QColor( "#191919" )
        self.color_2 = QColor( "#e5e5e5" )
    else:
        self.color_1 = QColor( "#e5e5e5" )
        self.color_2 = QColor( "#191919" )
    """

    """
    def eventFilter( self, source, event ):
        # return super().eventFilter( source, event )
    """

    """
    # Operating System
    self.OS = str( QSysInfo.kernelType() ) # WINDOWS=winnt & LINUX=linux
    if self.OS == "winnt": # Unlocks icons in Krita for Menu Mode
        QApplication.setAttribute( Qt.AA_DontShowIconsInMenus, False )
    """

    """
    # In case Krita is in Linear Format
    if self.n_cd != "U8":
        lsl = self.lrgb_to_srgb( r, g, b )
        r = lsl[0]
        g = lsl[1]
        b = lsl[2]

    # In case Krita is in Linear Format
    if self.n_cd != "U8":
        lsl = self.srgb_to_lrgb( r, g, b )
        r = lsl[0]
        g = lsl[1]
        b = lsl[2]
    """
    #endregion

class Worker_Print( QtCore.QObject ):

    # Run
    def run( self, source, space, geometry, thread ):
        # space - color space of the map
        # document - color managed by document
        # notes - YUV=255 UVD=255 HSV=360 HSL=360 HCY=360 CD_CA=255

        # Variables
        self.source = source
        panel_square = [ "S3", "S4", "SD" ] # "TRIANGLE" "SQUARE" "DIAMOND"
        panel_gamut = [ "GD", "GA" ] # "DIGITAL", "ANALOG"
        panel_hexagon = [ "H6" ]
        panel_luma = [ "Y4" ]

        # Document Modifier
        doc = self.source.Document_Active()
        cmodel = doc["cmodel"]
        n_cm = doc["n_cm"]
        n_cd = doc["n_cd"]
        n_cp = doc["n_cp"]
        vc = doc["vc"]
        # Temporary Folder
        zipname = f"{ cmodel }_{ space }_{ geometry }"
        temporary = os.path.normpath( os.path.join( self.source.url_panel, zipname ) )
        try:shutil.rmtree( temporary )
        except:pass
        os.mkdir( temporary, 0o666 )
        # Save URL File
        save_url = os.path.normpath( os.path.join( self.source.url_panel, zipname ) )
        try:os.remove( save_url )
        except:pass

        # Cycle Geometry
        if geometry in panel_square:
            # Variables
            total = 360 + 1
            depth = 255 + 1
            d2 = depth * 0.5
            qsize = QSize( depth, depth )
            qcolor = QColor( 0, 0, 0, 255 )
            # Progress
            self.source.dialog.progress_bar.setValue( 0 )
            self.source.dialog.progress_bar.setMaximum( total )
            # Cycle
            for t in range( 0, total ):
                # Print
                self.source.dialog.progress_bar.setValue( t+1 )
                QApplication.processEvents()
                # Base Image to Edit
                qimage = QImage( qsize, QImage.Format_RGB32 )
                qimage.fill( qcolor )
                # Range
                for y in range( 0, depth ):
                    for x in range( 0, depth ):
                        # Variables
                        c1 = t
                        c2 = Limit_Range( self.Print_Saturation( geometry, x, y, depth, d2 ), 0, depth )
                        c3 = depth - y
                        # Space
                        if   space == "HSV":    srgb = self.source.convert.hsv_to_srgb( c1/360, c2/depth, c3/depth )
                        elif space == "HSL":    srgb = self.source.convert.hsl_to_srgb( c1/360, c2/depth, c3/depth )
                        elif space == "HSY":    srgb = self.source.convert.hsy_to_srgb( c1/360, c2/depth, c3/depth )
                        elif space == "HCY":    srgb = self.source.convert.hcy_to_srgb( c1/360, c2/depth, c3/depth )
                        elif space == "ARD":    srgb = self.source.convert.ard_to_srgb( c1/360, c2/depth, c3/depth )
                        # Write Pixels
                        component = self.Print_Component( cmodel, n_cd, srgb )
                        qcolor = self.Print_Document( n_cm, n_cd, n_cp, vc, component )
                        qimage.setPixelColor( x, y, qcolor )
                # Save Image to File
                qpixmap = QPixmap().fromImage( qimage )
                filename = space + "_" + geometry + "_" + str( t ).zfill( 3 ) + ".png"
                location = os.path.normpath( os.path.join( temporary, filename ) )
                qpixmap.save( location )
        elif geometry in panel_gamut:
            # Variables
            total = 255 + 1
            depth = 255 + 1
            d2 = depth * 0.5
            qsize = QSize( depth, depth )
            qcolor = QColor( 0, 0, 0, 255 )
            # Progress
            self.source.dialog.progress_bar.setValue( 0 )
            self.source.dialog.progress_bar.setMaximum( total )
            # Cycle
            for t in range( 0, total ):
                # Print
                self.source.dialog.progress_bar.setValue( t+1 )
                QApplication.processEvents()
                # Base Image to Edit
                qimage = QImage( qsize, QImage.Format_RGB32 )
                qimage.fill( qcolor )
                # Range
                for y in range( 0, depth ):
                    for x in range( 0, depth ):
                        # Variables
                        if geometry == "GD":
                            angle = Trig_2D_Points_Lines_Angle( 0,d2, d2,d2, x,y ) / 360
                        if geometry == "GA":
                            angle = Limit_Looper( Trig_2D_Points_Lines_Angle( 0,d2, d2,d2, x,y ) + hue_a, 360 )
                            angle = self.source.convert.huea_to_hued( angle / 360 )
                        c1 = angle
                        c2 = Trig_2D_Points_Distance( x,y, d2,d2 ) / d2
                        c3 = t / depth
                        # Space
                        if   space == "HSV":    srgb = self.source.convert.hsv_to_srgb( c1, c2, c3 )
                        elif space == "HSL":    srgb = self.source.convert.hsl_to_srgb( c1, c2, c3 )
                        elif space == "HSY":    srgb = self.source.convert.hsy_to_srgb( c1, c2, c3 )
                        elif space == "HCY":    srgb = self.source.convert.hcy_to_srgb( c1, c2, c3 )
                        elif space == "ARD":    srgb = self.source.convert.ard_to_srgb( c1, c2, c3 )
                        # Write Pixels
                        component = self.Print_Component( cmodel, n_cd, srgb )
                        qcolor = self.Print_Document( n_cm, n_cd, n_cp, vc, component )
                        qimage.setPixelColor( x, y, qcolor )
                # Save Image to File
                qpixmap = QPixmap().fromImage( qimage )
                filename = space + "_" + geometry + "_" + str( t ).zfill( 3 ) + ".png"
                location = os.path.normpath( os.path.join( temporary, filename ) )
                qpixmap.save( location )
        elif geometry in panel_hexagon:
            # Variables
            total = 360 + 1
            depth = 255 + 1
            d2 = depth * 0.5
            qsize = QSize( depth, depth )
            qcolor = QColor( 0, 0, 0, 255 )
            # Progress
            self.source.dialog.progress_bar.setValue( 0 )
            self.source.dialog.progress_bar.setMaximum( total )
            # Cycle
            for t in range( 0, total ):
                # Print
                self.source.dialog.progress_bar.setValue( t+1 )
                QApplication.processEvents()
                # Base Image to Edit
                qimage = QImage( qsize, QImage.Format_RGB32 )
                qimage.fill( qcolor )
                # Range
                for y in range( 0, depth ):
                    for x in range( 0, depth ):
                        # Variables
                        c1 = ( x / d2 ) - 1
                        c2 = ( ( depth - y ) / d2 ) - 1
                        c3 = t / total
                        # Space
                        srgb = self.source.convert.uvd_to_srgb( c1, c2, c3 )
                        # Write Pixels
                        component = self.Print_Component( cmodel, n_cd, srgb )
                        qcolor = self.Print_Document( n_cm, n_cd, n_cp, vc, component )
                        qimage.setPixelColor( x, y, qcolor )
                # Save Image to File
                qpixmap = QPixmap().fromImage( qimage )
                filename = space + "_" + geometry + "_" + str( t ).zfill( 3 ) + ".png"
                location = os.path.normpath( os.path.join( temporary, filename ) )
                qpixmap.save( location )
        elif geometry in panel_luma:
            # Variables
            total = 255 + 1
            depth = 255 + 1
            d2 = depth * 0.5
            qsize = QSize( depth, depth )
            qcolor = QColor( 0, 0, 0, 255 )
            # Progress
            self.source.dialog.progress_bar.setValue( 0 )
            self.source.dialog.progress_bar.setMaximum( total )
            # Cycle
            for t in range( 0, total ):
                # Print
                self.source.dialog.progress_bar.setValue( t+1 )
                QApplication.processEvents()
                # Base Image to Edit
                qimage = QImage( qsize, QImage.Format_RGB32 )
                qimage.fill( qcolor )
                # Range
                for y in range( 0, depth ):
                    for x in range( 0, depth ):
                        # Variables
                        c1 = t
                        c2 = x
                        c3 = depth - y
                        # Space
                        if space == "YUV": srgb = self.source.convert.yuv_to_srgb( c1/depth, c2/depth, c3/depth )    
                        # Write Pixels
                        component = self.Print_Component( cmodel, n_cd, srgb )
                        qcolor = self.Print_Document( n_cm, n_cd, n_cp, vc, component )
                        qimage.setPixelColor( x, y, qcolor )
                # Save Image to File
                qpixmap = QPixmap().fromImage( qimage )
                filename = space + "_" + geometry + "_" + str( t ).zfill( 3 ) + ".png"
                location = os.path.normpath( os.path.join( temporary, filename ) )
                qpixmap.save( location )

        # Print
        self.source.dialog.progress_bar.setValue( 0 )
        # Create Zip File
        shutil.make_archive( save_url, "zip", temporary )
        # Delete all Render Files
        shutil.rmtree( temporary )
        if thread == True:
            self.source.print_qthread.quit()
        QApplication.beep()
    def Print_Component( self, cmodel, n_cd, srgb ):
        lrgb = self.source.convert.srgb_to_lrgb( srgb[0], srgb[1], srgb[2] )
        # Document
        if cmodel == "A":
            aaa = self.source.convert.srgb_to_gray( srgb[0], srgb[1], srgb[2] )
            component = [ aaa[0], 1 ]
        elif cmodel == "GRAY":
            gray = self.source.convert.srgb_to_gray( srgb[0], srgb[1], srgb[2] )
            component = [ gray[0], 1 ]
        elif cmodel == "SRGB":
            component = [ srgb[2], srgb[1], srgb[0], 1 ]
        elif cmodel == "LRGB":
            if n_cd == "U16":   component = [ lrgb[2], lrgb[1], lrgb[0], 1 ]
            else:               component = [ lrgb[0], lrgb[1], lrgb[2], 1 ]
        elif cmodel == "CMYK":
            cmyk = self.source.convert.srgb_to_cmyk( srgb[0], srgb[1], srgb[2], None )
            component = [ cmyk[0], cmyk[1], cmyk[2], cmyk[3], 1 ]
        elif cmodel == "YUV":
            yuv = self.source.convert.srgb_to_yuv( srgb[0], srgb[1], srgb[2] )
            component = [ yuv[0], yuv[1], yuv[2], 1 ]
        elif cmodel == "XYZ":
            xyz = self.source.convert.lrgb_to_xyz( lrgb[0], lrgb[1], lrgb[2] )
            component = [ xyz[0], xyz[1], xyz[2], 1 ]
        elif cmodel == "LAB":
            lab = self.source.convert.lrgb_to_lab( lrgb[0], lrgb[1], lrgb[2] )
            component = [ lab[0], lab[1], lab[2], 1 ]
        return component
    def Print_Saturation( self, geometry, x, y, depth, d2 ):
        if geometry == "S3":
            if y in [ 0, depth ]:
                c2 = 0
            elif y == d2:
                c2 = x
            elif 0 < y < d2:
                rx, ry = Trig_2D_Points_Lines_Intersection( 0,y, depth,y, 0,0, depth,d2 )
                c2 = Limit_Float( x / rx ) * depth
            elif d2 < y < depth:
                rx, ry = Trig_2D_Points_Lines_Intersection( 0,y, depth,y, depth,d2, 0,depth )
                c2 = Limit_Float( x / rx ) * depth
        if geometry == "S4":
            c2 = x
        if geometry == "SD":
            if y in [ 0, depth ]:
                c2 = 0
            elif y == d2:
                c2 = x
            elif 0 < y < d2:
                lx, ly = Trig_2D_Points_Lines_Intersection( 0,y, depth,y, 0, d2, d2,0 )
                rx, ry = Trig_2D_Points_Lines_Intersection( 0,y, depth,y, depth,d2, d2,0 )
                c2 = self.Print_Limit( x, lx, rx, depth )
            elif d2 < y < depth:
                lx, ly = Trig_2D_Points_Lines_Intersection( 0,y, depth,y, 0, d2, d2,depth )
                rx, ry = Trig_2D_Points_Lines_Intersection( 0,y, depth,y, depth,d2, d2,depth )
                c2 = self.Print_Limit( x, lx, rx, depth )
        return c2
    def Print_Document( self, n_cm, n_cd, n_cp, vc, component ):
        if ( self.source.kcanvas != None and self.source.kview != None ):
            managed_color = ManagedColor( n_cm, n_cd, n_cp )
            managed_color.setComponents( component )
            qcolor = managed_color.colorForCanvas( vc )
            return qcolor
    def Print_Limit( self, x, mini, maxi, depth ):
        if x <= mini:
            value = 0
        elif x >= maxi:
            value = depth
        else:
            dx = x - mini
            dt = maxi - mini
            value = Limit_Range( ( dx / dt ) * depth, 0, depth )
        return value


"""
Krita Bugs:
- Byte data of a U16 document is not in RGB like on the API notes but it is in BGR.

Ideas:
- Sampler ( Bit Depth + Color model )
- Profile UVD / ARD LUTs
- Hexagon have 2 cursors, one for Gamma and another projected in sRGB to correct the conversion

New:
- Panel Dot is now Panel Plane ( more CSP like )

Problems:
- Dialog History has no space
"""
