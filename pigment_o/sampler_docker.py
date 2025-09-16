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
import webbrowser
# Krita
from krita import *
# PyQt5
from PyQt5 import QtWidgets, QtCore, QtGui, uic
# Sampler
from .sampler_modulo import (
    Display_Map,
    Channel_Select,
    Channel_Slider,
    )
# Engine
from .engine_constants import *
from .engine_calculations import Geometry, Convert, Analyse

#endregion
#region Global Variables

DOCKER_NAME = "Pigment.O Sampler"
sample_o_version = "2025_09_16"

#endregion


class Sampler_Docker( DockWidget ):
    """
    Color Sampler
    """

    #region Initialize

    def __init__( self ):
        super( Sampler_Docker, self ).__init__()

        # Construct
        self.User_Interface()
        self.Variables()
        self.Connections()
        self.Modules()
        self.Style()
        self.Settings()
        self.Plugin_Load()

    def User_Interface( self ):
        # Window
        self.setWindowTitle( DOCKER_NAME )

        # Operating System
        self.OS = str( QSysInfo.kernelType() ) # WINDOWS=winnt & LINUX=linux
        if self.OS == "winnt": # Unlocks icons in Krita for Menu Mode
            QApplication.setAttribute( Qt.AA_DontShowIconsInMenus, False )

        # Path Name
        self.directory_plugin = str( os.path.dirname( os.path.realpath( __file__ ) ) )

        # Widget Docker
        self.layout = uic.loadUi( os.path.join( self.directory_plugin, "sampler_docker.ui" ), QWidget( self ) )
        self.setWidget( self.layout )

        # Settings
        self.dialog = uic.loadUi( os.path.join( self.directory_plugin, "sampler_settings.ui" ), QDialog( self ) )
        self.dialog.setWindowTitle( "Pigment.O Sampler : Settings" )
        self.dialog.accept() # Hides the Dialog
    def Variables( self ):
        # Layout
        self.color_space = "RGB"
        self.split_method = "CHANNEL" # "CHANNEL" "RANGE"
        # Dialog
        self.cs_luminosity = "ITU-R BT.709"
        self.cs_matrix = "sRGB"
        self.cs_illuminant = "D65"
        self.tic_display = False
        self.tic_value = 300
        self.invert_tic = False
        self.invert_cmyk = False

        # Display
        self.channel_data = []
        self.channel_index = 0
        self.range_data = []
        self.time = None
        self.qpixmap_logo = QPixmap( os.path.join( self.directory_plugin, "ICON\\SAMPLER.png" ) )

        # Range 1
        self.range_0_pa = 0.3
        self.range_0_pb = 0.4
        self.range_0_pc = 0.6
        self.range_0_pd = 0.7
        # Range 2
        self.range_1_pa = 0.3
        self.range_1_pb = 0.4
        self.range_1_pc = 0.6
        self.range_1_pd = 0.7
        # Range 3
        self.range_2_pa = 0.3
        self.range_2_pb = 0.4
        self.range_2_pc = 0.6
        self.range_2_pd = 0.7
        # Range 4
        self.range_3_pa = 0.3
        self.range_3_pb = 0.4
        self.range_3_pc = 0.6
        self.range_3_pd = 0.7

        # Module
        self.pigment_o_pyid = "pykrita_pigment_o_picker_docker"
        self.pigment_o_module = None # pointer to the module
        self.cor = None # Pigment.o color object
    def Connections( self ):
        #region Footer

        self.layout.color_space.currentTextChanged.connect( self.Mode_Colorspace )
        self.layout.split_method.currentTextChanged.connect( self.Mode_SplitMethod )
        self.layout.run.clicked.connect( self.RUN )
        self.layout.insert.clicked.connect( self.Mask_Insert )
        self.layout.settings.clicked.connect( self.Menu_Settings )

        #endregion
        #region Dialog Footer

        # Color Space
        self.dialog.cs_luminosity.currentTextChanged.connect( self.CS_Luminosity )
        self.dialog.cs_matrix.currentTextChanged.connect( lambda: self.CS_Matrix( self.dialog.cs_matrix.currentText(), self.dialog.cs_illuminant.currentText() ) )
        self.dialog.cs_illuminant.currentTextChanged.connect( lambda: self.CS_Matrix( self.dialog.cs_matrix.currentText(), self.dialog.cs_illuminant.currentText() ) )

        # Options
        self.dialog.tic_display.toggled.connect( self.TIC_Display )
        self.dialog.tic_value.valueChanged.connect( self.TIC_Value )
        self.dialog.invert_tic.toggled.connect( self.Invert_TIC )
        self.dialog.invert_cmyk.toggled.connect( self.Invert_CMYK )

        # Footer
        self.dialog.manual.clicked.connect( self.Menu_Manual )
        self.dialog.license.clicked.connect( self.Menu_License )

        #endregion
    def Modules( self ):
        #region Notifier

        self.notifier = Krita.instance().notifier()
        self.notifier.windowCreated.connect( self.Window_Created )

        #endregion
        #region Calculations

        # Geometry
        self.geometry = Geometry()
        # Convert
        self.convert = Convert()
        self.convert.Set_Document( "RGB", "U8", "sRGB-elle-V2-srgtrc.icc" )
        self.convert.Set_Hue( zero )
        self.convert.Set_Luminosity( "ITU-R BT.709" )
        self.convert.Set_Gamma( gamma_y, gamma_l )
        self.convert.Set_Matrix( "sRGB", "D65" )
        # Analyse
        self.analyse = Analyse()

        #endregion
        #region Modulos

        # Display
        self.display_map = Display_Map( self.layout.display_map )
        self.display_map.SIGNAL_INSERT.connect( self.Mask_Insert )
        self.display_map.SIGNAL_CLEAN.connect( self.Mask_Clean )

        # Controller
        self.channel_select = Channel_Select( self.layout.channel_select )
        self.channel_select.SIGNAL_INDEX.connect( self.Channel_Index )

        # Range 1
        self.range_0 = Channel_Slider( self.layout.range_0 )
        self.range_0.SIGNAL_PA.connect( self.Range_0_PA )
        self.range_0.SIGNAL_PB.connect( self.Range_0_PB )
        self.range_0.SIGNAL_PC.connect( self.Range_0_PC )
        self.range_0.SIGNAL_PD.connect( self.Range_0_PD )
        # Range 2
        self.range_1 = Channel_Slider( self.layout.range_1 )
        self.range_1.SIGNAL_PA.connect( self.Range_1_PA )
        self.range_1.SIGNAL_PB.connect( self.Range_1_PB )
        self.range_1.SIGNAL_PC.connect( self.Range_1_PC )
        self.range_1.SIGNAL_PD.connect( self.Range_1_PD )
        # Range 3
        self.range_2 = Channel_Slider( self.layout.range_2 )
        self.range_2.SIGNAL_PA.connect( self.Range_2_PA )
        self.range_2.SIGNAL_PB.connect( self.Range_2_PB )
        self.range_2.SIGNAL_PC.connect( self.Range_2_PC )
        self.range_2.SIGNAL_PD.connect( self.Range_2_PD )
        # Range 4
        self.range_3 = Channel_Slider( self.layout.range_3 )
        self.range_3.SIGNAL_PA.connect( self.Range_3_PA )
        self.range_3.SIGNAL_PB.connect( self.Range_3_PB )
        self.range_3.SIGNAL_PC.connect( self.Range_3_PC )
        self.range_3.SIGNAL_PD.connect( self.Range_3_PD )

        #endregion
    def Style( self ):
        # Variables
        ki = Krita.instance()
        # Icons
        qicon_run = ki.icon( "animation_play" )
        qicon_settings = ki.icon( "settings-button" )
        self.qicon_insert = "krita_tool_enclose_and_fill"

        # Widgets
        self.layout.run.setIcon( qicon_run )
        self.layout.insert.setIcon( ki.icon( self.qicon_insert ) )
        self.layout.settings.setIcon( qicon_settings )
        # Tool Tips
        self.layout.color_space.setToolTip( "Color Space" )
        self.layout.split_method.setToolTip( "Split Method" )
        self.layout.run.setToolTip( "Run" )
        self.layout.settings.setToolTip( "Settings" )
        # Style Sheets Layout
        self.layout.channel_select.setStyleSheet( "#channel_select{background-color: rgba( 0, 0, 0, 0 );}" )
        self.layout.page_range.setStyleSheet( "#page_range{background-color: rgba( 0, 0, 0, 0 );}" )
        self.layout.progress_bar.setStyleSheet( "#progress_bar{background-color: rgba( 0, 0, 0, 0 );}" )

        # State
        self.Mode_Insert( False )
    def Settings( self ):
        # Layout
        self.layout.color_space.setCurrentText( self.Set_Read( "STR", "color_space", self.color_space ) )
        self.layout.split_method.setCurrentText( self.Set_Read( "STR", "split_method", self.split_method ) )

        # Dialog Color Space
        self.dialog.cs_luminosity.setCurrentText( self.Set_Read( "STR", "cs_luminosity", self.cs_luminosity ) )
        self.dialog.cs_matrix.setCurrentText( self.Set_Read( "STR", "cs_matrix", self.cs_matrix ) )
        self.dialog.cs_illuminant.setCurrentText( self.Set_Read( "STR", "cs_illuminant", self.cs_illuminant ) )

        # Dialog Map
        self.dialog.tic_display.setChecked( self.Set_Read( "EVAL", "tic_display", self.tic_display ) )
        self.dialog.tic_value.setValue( self.Set_Read( "INT", "tic_value", self.tic_value ) )
        self.dialog.invert_tic.setChecked( self.Set_Read( "EVAL", "invert_tic", self.invert_tic ) )
        self.dialog.invert_cmyk.setChecked( self.Set_Read( "EVAL", "invert_cmyk", self.invert_cmyk ) )
    def Plugin_Load( self ):
        try:
            self.Loader()
        except Exception as e:
            self.Message_Warnning( "ERROR", f"Load \n{ e }" )
            self.Variables()
            self.Loader()

    def Loader( self ):
        self.Mode_Colorspace( self.color_space )
        self.Mode_SplitMethod( self.split_method )
    def Set_Read( self, mode, entry, default ):
        setting = Krita.instance().readSetting( DOCKER_NAME, entry, "" )
        if setting == "":
            read = default
        else:
            try:
                if mode == "EVAL":
                    read = eval( setting )
                elif mode == "STR":
                    read = str( setting )
                elif mode == "INT":
                    read = int( setting )
            except:
                read = default
        Krita.instance().writeSetting( DOCKER_NAME, entry, str( read ) )
        return read

    #endregion
    #region Menu

    # Menu
    def Mode_Colorspace( self, color_space ):
        # Variables
        self.color_space = color_space
        bnw = [
            [ 0.0, 0.0, 0.0 ],
            [ 0.5, 0.5, 0.5 ],
            [ 1.0, 1.0, 1.0 ],
            ]
        hue = [
            [ 1.0, 0.0, 0.0 ],
            [ 1.0, 1.0, 0.0 ],
            [ 0.0, 1.0, 0.0 ],
            [ 0.0, 1.0, 1.0 ],
            [ 0.0, 0.0, 1.0 ],
            [ 1.0, 0.0, 1.0 ],
            [ 1.0, 0.0, 0.0 ],
            ]
        # User Interface
        if color_space == "A":
            range_0 = bnw
            range_1 = None
            range_2 = None
            range_3 = None
        if color_space == "RGB":
            range_0 = [
                [ 0.0, 0.0, 0.0 ],
                [ 1.0, 0.0, 0.0 ],
                ]
            range_1 = [
                [ 0.0, 0.0, 0.0 ],
                [ 0.0, 1.0, 0.0 ],
                ]
            range_2 = [
                [ 0.0, 0.0, 0.0 ],
                [ 0.0, 0.0, 1.0 ],
                ]
            range_3 = None
        if color_space == "CMY":
            range_0 = [
                [ 1.0, 1.0, 1.0 ],
                [ 0.0, 1.0, 1.0 ],
                ]
            range_1 = [
                [ 1.0, 1.0, 1.0 ],
                [ 1.0, 0.0, 1.0 ],
                ]
            range_2 = [
                [ 1.0, 1.0, 0.0 ],
                [ 1.0, 1.0, 0.0 ],
                ]
            range_3 = None
        if color_space == "CMYK":
            range_0 = [
                [ 0.0, 0.0, 0.0 ],
                [ 0.0, 1.0, 1.0 ],
                ]
            range_1 = [
                [ 0.0, 0.0, 0.0 ],
                [ 1.0, 0.0, 1.0 ],
                ]
            range_2 = [
                [ 0.0, 0.0, 0.0 ],
                [ 1.0, 1.0, 0.0 ],
                ]
            range_3 = [
                [ 1.0, 1.0, 1.0 ],
                [ 0.0, 0.0, 0.0 ],
                ]
        if color_space == "RYB":
            range_0 = [
                [ 0.0, 0.0, 0.0 ],
                [ 1.0, 0.0, 0.0 ],
                ]
            range_1 = [
                [ 0.0, 0.0, 0.0 ],
                [ 1.0, 1.0, 0.0 ],
                ]
            range_2 = [
                [ 0.0, 0.0, 0.0 ],
                [ 0.0, 0.0, 1.0 ],
                ]
            range_3 = None
        if color_space == "YUV":
            range_0 = bnw
            range_1 = [
                [ 0.50, 0.59, 0.00 ],
                [ 0.50, 0.55, 0.04 ],
                [ 0.50, 0.50, 0.50 ],
                [ 0.50, 0.45, 0.96 ],
                [ 0.50, 0.41, 1.00 ],
                ]
            range_2 = [
                [ 0.00, 0.73, 0.50 ],
                [ 0.11, 0.62, 0.50 ],
                [ 0.50, 0.50, 0.50 ],
                [ 0.89, 0.34, 0.96 ],
                [ 1.00, 0.27, 0.50 ],
                ]
            range_3 = None
        if color_space == "HSV":
            range_0 = hue
            range_1 = [
                [ 1.0, 1.0, 1.0 ],
                [ 1.0, 0.0, 0.0 ],
                ]
            range_2 = bnw
            range_3 = None
        if color_space == "HSL":
            range_0 = hue
            range_1 = [
                [ 0.5, 0.5, 0.5 ],
                [ 1.0, 0.0, 0.0 ],
                ]
            range_2 = [
                [ 0.0, 0.0, 0.0 ],
                [ 1.0, 0.0, 0.0 ],
                [ 1.0, 1.0, 1.0 ],
                ]
            range_3 = None
        if color_space == "HCY":
            range_0 = hue
            range_1 = [
                [ 0.21, 0.21, 0.21 ],
                [ 0.41, 0.16, 0.16 ],
                [ 0.61, 0.11, 0.11 ],
                [ 0.80, 0.05, 0.05 ],
                [ 1.00, 0.00, 0.00 ],
                ]
            range_2 = bnw
            range_3 = None
        if color_space == "ARD":
            range_0 = hue
            range_1 = [
                [ 0.33, 0.33, 0.33 ],
                [ 0.50, 0.25, 0.25 ],
                [ 0.67, 0.17, 0.17 ],
                [ 0.83, 0.08, 0.08 ],
                [ 1.00, 0.00, 0.00 ],
                ]
            range_2 = bnw
            range_3 = None
        if color_space == "XYZ":
            range_0 = [
                [ 0.00, 0.00, 0.00 ],
                [ 0.91, 0.00, 0.12 ],
                [ 1.00, 0.00, 0.18 ],
                [ 1.00, 0.00, 0.23 ],
                [ 1.00, 0.00, 0.26 ],
                ]
            range_1 = [
                [ 0.00, 0.00, 0.00 ],
                [ 0.00, 0.71, 0.00 ],
                [ 0.00, 0.97, 0.00 ],
                [ 0.00, 1.00, 0.00 ],
                [ 0.00, 1.00, 0.00 ],
                ]
            range_2 = [
                [ 0.00, 0.00, 0.00 ],
                [ 0.00, 0.10, 0.55 ],
                [ 0.00, 0.16, 0.75 ],
                [ 0.00, 0.19, 0.90 ],
                [ 0.00, 0.23, 1.00 ],
                ]
            range_3 = None
        if color_space == "XYY":
            range_0 = [
                [ 0.00, 0.68, 0.67 ],
                [ 0.27, 0.54, 0.54 ],
                [ 0.83, 0.33, 0.33 ],
                [ 1.00, 0.00, 0.00 ],
                [ 1.00, 0.00, 0.00 ],
                ]
            range_1 = [
                [ 1.00, 0.00, 1.00 ],
                [ 1.00, 0.00, 0.32 ],
                [ 0.79, 0.40, 0.00 ],
                [ 0.60, 0.50, 0.00 ],
                [ 0.46, 0.55, 0.00 ],
                ]
            range_2 = [
                [ 0.00, 0.00, 0.00 ],
                [ 0.54, 0.54, 0.54 ],
                [ 0.74, 0.74, 0.74 ],
                [ 0.88, 0.88, 0.88 ],
                [ 1.00, 1.00, 1.00 ],
                ]
            range_3 = None
        if color_space == "LAB":
            range_0 = [
                [ 0.00, 0.00, 0.00 ],
                [ 0.23, 0.23, 0.23 ],
                [ 0.47, 0.47, 0.47 ],
                [ 0.72, 0.72, 0.72 ],
                [ 1.00, 1.00, 1.26 ],
                ]
            range_1 = [
                [ 0.00, 0.64, 0.45 ],
                [ 0.00, 0.60, 0.46 ],
                [ 0.47, 0.47, 0.47 ],
                [ 1.00, 0.00, 0.49 ],
                [ 1.00, 0.00, 0.53 ],
                ]
            range_2 = [
                [ 0.00, 0.52, 1.00 ],
                [ 0.00, 0.49, 0.80 ],
                [ 0.47, 0.47, 0.47 ],
                [ 0.55, 0.46, 0.10 ],
                [ 0.57, 0.46, 0.00 ],
                ]
            range_3 = None
        if color_space == "LCH":
            range_0 = [
                [ 0.00, 0.00, 0.00 ],
                [ 0.23, 0.23, 0.23 ],
                [ 0.47, 0.47, 0.47 ],
                [ 0.72, 0.72, 0.72 ],
                [ 1.00, 1.00, 1.00 ],
                ]
            range_1 = [
                [ 0.47, 0.47, 0.47 ],
                [ 0.67, 0.39, 0.32 ],
                [ 0.83, 0.28, 0.17 ],
                [ 0.96, 0.00, 0.00 ],
                [ 1.00, 0.00, 0.00 ],
                ]
            range_2 = [
                [ 1.00, 0.00, 0.53 ],
                [ 1.00, 0.00, 0.00 ],
                [ 0.00, 0.60, 0.00 ],
                [ 0.00, 0.64, 0.45 ],
                [ 0.00, 0.64, 1.00 ],
                [ 0.94, 0.00, 1.00 ],
                [ 1.00, 0.00, 0.53 ],
                ]
            range_3 = None
        # Mode
        hue = ( "HSV", "HSL", "HCY", "ARD" )
        if color_space in hue:
            self.range_0.Set_Mode( "CIRCULAR" )
        else:
            self.range_0.Set_Mode( "LINEAR" )
        self.range_1.Set_Mode( "LINEAR" )
        if color_space == "LCH":
            self.range_2.Set_Mode( "CIRCULAR" )
        else:
            self.range_2.Set_Mode( "LINEAR" )
        self.range_3.Set_Mode( "LINEAR" )
        # Display Gradients
        self.range_0.Set_Gradient( range_0 )
        self.range_1.Set_Gradient( range_1 )
        self.range_2.Set_Gradient( range_2 )
        self.range_3.Set_Gradient( range_3 )
        # Color
        self.Color_READ()
        # Save
        Krita.instance().writeSetting( DOCKER_NAME, "color_space", str( self.color_space ) )
    def Mode_SplitMethod( self, split_method ):
        # Variables
        self.split_method = split_method
        qpixmap = self.qpixmap_logo
        boolean = False
        # Mode
        if self.split_method == "CHANNEL":
            try:
                qpixmap = self.channel_data[self.channel_index]["render"]
                boolean = True
            except:
                pass
            self.layout.stacked_widget.setCurrentIndex( 0 )
        if self.split_method == "RANGE":
            try:
                qpixmap = self.range_data[0]["render"]
                boolean = True
            except:
                pass
            self.layout.stacked_widget.setCurrentIndex( 1 )
            self.Color_READ()
        # User Interface
        self.Map_Display( qpixmap, False )
        self.Mode_Insert( boolean )
        self.Update_Size()
        # Save
        Krita.instance().writeSetting( DOCKER_NAME, "split_method", str( self.split_method ) )
    def Mode_Insert( self, boolean ):
        self.layout.insert.setEnabled( boolean )
        self.layout.insert.setFlat( not boolean )

    # User Interface
    def ProgressBar_Value( self, value ):
        self.layout.progress_bar.setValue( value )

    # Colors Spaces
    def CS_Luminosity( self, cs_luminosity ):
        # Variables
        self.cs_luminosity = cs_luminosity
        self.convert.Set_Luminosity( cs_luminosity )
        # Save
        Krita.instance().writeSetting( DOCKER_NAME, "cs_luminosity", str( self.cs_luminosity ) )
    def CS_Matrix( self, cs_matrix, cs_illuminant ):
        # Variables
        self.cs_matrix = cs_matrix
        self.cs_illuminant = cs_illuminant
        self.convert.Set_Matrix( cs_matrix, cs_illuminant )
        # Save
        Krita.instance().writeSetting( DOCKER_NAME, "cs_matrix", str( self.cs_matrix ) )
        Krita.instance().writeSetting( DOCKER_NAME, "cs_illuminant", str( self.cs_illuminant ) )

    # Maps
    def TIC_Display( self, boolean ):
        self.tic_display = boolean
        Krita.instance().writeSetting( DOCKER_NAME, "tic_display", str( self.tic_display ) )
    def TIC_Value( self, tic_value ):
        self.tic_value = tic_value
        Krita.instance().writeSetting( DOCKER_NAME, "tic_value", str( self.tic_value ) )
    def Invert_TIC( self, boolean ):
        self.invert_tic = boolean
        Krita.instance().writeSetting( DOCKER_NAME, "invert_tic", str( self.invert_tic ) )
    def Invert_CMYK( self, boolean ):
        self.invert_cmyk = boolean
        Krita.instance().writeSetting( DOCKER_NAME, "invert_cmyk", str( self.invert_cmyk ) )

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

    #endregion
    #region Management

    # Communication
    def Message_Label( self, message ):
        self.layout.label.setText( str( message ) )
    def Message_Log( self, operation, message ):
        string = f"Pigment.O Sampler | { operation } { message }"
        try:QtCore.qDebug( string )
        except:pass
    def Message_Warnning( self, operation, message ):
        string = f"Pigment.O Sampler | { operation.upper() } { message }"
        QMessageBox.information( QWidget(), i18n( "Warnning" ), i18n( string ) )
    def Message_Float( self, operation, message, icon ):
        ki = Krita.instance()
        string = f"Pigment.O Sampler | { operation.upper() } { message }"
        ki.activeWindow().activeView().showFloatingMessage( string, ki.icon( icon ), 5000, 0 )

    # Channels
    def Channel_Names( self, mode ):
        chan_0 = ""
        chan_1 = ""
        chan_2 = ""
        chan_3 = ""
        if mode == "A":
            chan_0 = "Gray"
        if mode == "RGB":
            chan_0 = "RGB\nRed"
            chan_1 = "RGB\nGreen"
            chan_2 = "RGB\nBlue"
        if mode == "CMY":
            chan_0 = "CMY\nCyan"
            chan_1 = "CMY\nMagenta"
            chan_2 = "CMY\nYellow"
        if mode == "CMYK":
            chan_0 = "CMYK\nCyan"
            chan_1 = "CMYK\nMagenta"
            chan_2 = "CMYK\nYellow"
            chan_3 = "CMYK\nKey"
        if mode == "RYB":
            chan_0 = "RYB\nRed"
            chan_1 = "RYB\nYellow"
            chan_2 = "RYB\nBlue"
        if mode == "YUV":
            chan_0 = "YUV\nLuma"
            chan_1 = "YUV\nComp Blue"
            chan_2 = "YUV\nComp Red"
        if mode == "HSV":
            chan_0 = "HSV\nHue"
            chan_1 = "HSV\nSaturation"
            chan_2 = "HSV\nValue"
        if mode == "HSL":
            chan_0 = "HSL\nHue"
            chan_1 = "HSL\nSaturation"
            chan_2 = "HSL\nLightness"
        if mode == "HCY":
            chan_0 = "HCY\nHue"
            chan_1 = "HCY\nChroma"
            chan_2 = "HCY\nLuma"
        if mode == "ARD":
            chan_0 = "ARD\nAngle"
            chan_1 = "ARD\nRatio"
            chan_2 = "ARD\nDepth"
        if mode == "XYZ":
            chan_0 = "XYZ\nX"
            chan_1 = "XYZ\nY"
            chan_2 = "XYZ\nZ"
        if mode == "XYY":
            chan_0 = "XYY\nx"
            chan_1 = "XYY\ny"
            chan_2 = "XYY\nY"
        if mode == "LAB":
            chan_0 = "LAB\nL*"
            chan_1 = "LAB\nA*"
            chan_2 = "LAB\nB*"
        if mode == "LCH":
            chan_0 = "LCH\nLuminosity"
            chan_1 = "LCH\nChroma"
            chan_2 = "LCH\nHue"
        return chan_0, chan_1, chan_2, chan_3
    def Channel_Icons( self ):
        # Variables
        margin = 2
        height = self.layout.channel_select.height() - ( 2 * margin )
        # Construct List
        maps = []
        for item in self.channel_data:
            # Variables
            render = item["render"]
            draw = render.scaled( int( height * 1.2 ), int( height ), Qt.KeepAspectRatio, Qt.FastTransformation )
            dw = draw.width()
            dh = draw.height()
            text = item["text"]
            # List construct
            maps.append( { "render" : draw, "width":dw, "height":dh, "text":text } )
        self.channel_select.Set_Display( maps )
    def Channel_Index( self, channel_index ):
        # Variables
        self.channel_index = channel_index
        item = self.channel_data[ self.channel_index ]
        qpixmap = item["render"]
        cor = item["cor"]
        # Map
        self.Map_Display( qpixmap, cor )
    def Map_Display( self, qpixmap, cor ):
        if qpixmap != None:
            self.display_map.Set_Display( qpixmap )
            self.display_map.Set_Background( cor )

    # Color
    def Import_Pigment_O( self ):
        if self.pigment_o_module == None:
            try:
                ki = Krita.instance()
                dockers = ki.dockers()
                for d in dockers:
                    if d.objectName() == self.pigment_o_pyid:
                        self.pigment_o_module = d
                        break
            except:
                pass
    def Color_READ( self ):
        if self.pigment_o_module != None:
            # Read
            cor = self.pigment_o_module.API_Request_FG()
            # Display
            if self.color_space == "A":
                self.range_0.Set_Cor( cor[ "aaa_1" ] )
                self.range_1.Set_Cor( None )
                self.range_2.Set_Cor( None )
                self.range_3.Set_Cor( None )
            if self.color_space == "RGB":
                self.range_0.Set_Cor( cor[ "rgb_1" ] )
                self.range_1.Set_Cor( cor[ "rgb_2" ] )
                self.range_2.Set_Cor( cor[ "rgb_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "CMY":
                self.range_0.Set_Cor( cor[ "cmy_1" ] )
                self.range_1.Set_Cor( cor[ "cmy_2" ] )
                self.range_2.Set_Cor( cor[ "cmy_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "CMYK":
                self.range_0.Set_Cor( cor[ "cmyk_1" ] )
                self.range_1.Set_Cor( cor[ "cmyk_2" ] )
                self.range_2.Set_Cor( cor[ "cmyk_3" ] )
                self.range_3.Set_Cor( cor[ "cmyk_4" ] )
            if self.color_space == "RYB":
                self.range_0.Set_Cor( cor[ "ryb_1" ] )
                self.range_1.Set_Cor( cor[ "ryb_2" ] )
                self.range_2.Set_Cor( cor[ "ryb_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "YUV":
                self.range_0.Set_Cor( cor[ "yuv_1" ] )
                self.range_1.Set_Cor( cor[ "yuv_2" ] )
                self.range_2.Set_Cor( cor[ "yuv_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "HSV":
                self.range_0.Set_Cor( cor[ "hsv_1" ] )
                self.range_1.Set_Cor( cor[ "hsv_2" ] )
                self.range_2.Set_Cor( cor[ "hsv_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "HSL":
                self.range_0.Set_Cor( cor[ "hsl_1" ] )
                self.range_1.Set_Cor( cor[ "hsl_2" ] )
                self.range_2.Set_Cor( cor[ "hsl_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "HCY":
                self.range_0.Set_Cor( cor[ "hcy_1" ] )
                self.range_1.Set_Cor( cor[ "hcy_2" ] )
                self.range_2.Set_Cor( cor[ "hcy_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "ARD":
                self.range_0.Set_Cor( cor[ "ard_1" ] )
                self.range_1.Set_Cor( cor[ "ard_2" ] )
                self.range_2.Set_Cor( cor[ "ard_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "XYZ":
                self.range_0.Set_Cor( cor[ "xyz_1" ] )
                self.range_1.Set_Cor( cor[ "xyz_2" ] )
                self.range_2.Set_Cor( cor[ "xyz_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "XYY":
                self.range_0.Set_Cor( cor[ "xyy_1" ] )
                self.range_1.Set_Cor( cor[ "xyy_2" ] )
                self.range_2.Set_Cor( cor[ "xyy_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "LAB":
                self.range_0.Set_Cor( cor[ "lab_1" ] )
                self.range_1.Set_Cor( cor[ "lab_2" ] )
                self.range_2.Set_Cor( cor[ "lab_3" ] )
                self.range_3.Set_Cor( None )
            if self.color_space == "LCH":
                self.range_0.Set_Cor( cor[ "lch_1" ] )
                self.range_1.Set_Cor( cor[ "lch_2" ] )
                self.range_2.Set_Cor( cor[ "lch_3" ] )
                self.range_3.Set_Cor( None )

    # Widgets
    def Update_Size( self ):
        # Modules
        self.display_map.Set_Size( self.layout.display_map.width(), self.layout.display_map.height() )
        # Channel
        self.channel_select.Set_Size( self.layout.channel_select.width(), self.layout.channel_select.height() )
        # Range
        self.range_0.Set_Size( self.layout.range_0.width(), self.layout.range_0.height() )
        self.range_1.Set_Size( self.layout.range_1.width(), self.layout.range_1.height() )
        self.range_2.Set_Size( self.layout.range_2.width(), self.layout.range_2.height() )
        self.range_3.Set_Size( self.layout.range_3.width(), self.layout.range_3.height() )
        # Update
        self.update()
    def Resize_Print( self, event ):
        # Used doing a photoshoot
        width = self.width()
        height = self.height()
        self.Message_Log( "SIZE", f"{ width } x { height }" )
    def Widgets_Enabled( self, boolean ):
        self.layout.footer_widget.setEnabled( boolean )
        self.dialog.setEnabled( boolean )

    #endregion
    #region Range

    # Range 1
    def Range_0_PA( self, value ):
        self.range_0_pa = value
    def Range_0_PB( self, value ):
        self.range_0_pb = value
    def Range_0_PC( self, value ):
        self.range_0_pc = value
    def Range_0_PD( self, value ):
        self.range_0_pd = value
    # Range 2
    def Range_1_PA( self, value ):
        self.range_1_pa = value
    def Range_1_PB( self, value ):
        self.range_1_pb = value
    def Range_1_PC( self, value ):
        self.range_1_pc = value
    def Range_1_PD( self, value ):
        self.range_1_pd = value
    # Range 3
    def Range_2_PA( self, value ):
        self.range_2_pa = value
    def Range_2_PB( self, value ):
        self.range_2_pb = value
    def Range_2_PC( self, value ):
        self.range_2_pc = value
    def Range_2_PD( self, value ):
        self.range_2_pd = value
    # Range 4
    def Range_3_PA( self, value ):
        self.range_3_pa = value
    def Range_3_PB( self, value ):
        self.range_3_pb = value
    def Range_3_PC( self, value ):
        self.range_3_pc = value
    def Range_3_PD( self, value ):
        self.range_3_pd = value

    #endregion
    #region Samples

    # Generate
    def RUN( self ):
        if ( ( self.canvas() is not None ) and ( self.canvas().view() is not None ) ):
            # Time Watcher
            self.time = QtCore.QDateTime.currentDateTimeUtc()

            # User Interface
            self.Widgets_Enabled( False )

            # Active Document
            ki = Krita.instance()
            ad = ki.activeDocument()
            # Document Color
            d_cm = ad.colorModel()
            d_cd = ad.colorDepth()
            d_cp = ad.colorProfile()
            # d_nt = ad.activeNode().type()

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

            # Place Text
            self.Message_Label( "" )
            self.Message_Float( "GENERATE", self.split_method, "color-adjustment-mode-channels" )
            QApplication.processEvents()

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

            # Pixel Data Colors
            byte_array = ad.pixelData( dx, dy, dw, dh )
            num_array = self.analyse.Bytes_to_Integer( byte_array, d_cd )

            # Pixel Data Selection
            if ss == None:
                num_ss = [ depth ] * len( num_array )
            else:
                byte_ss = ss.pixelData( dx, dy, dw, dh )
                num_ss = self.analyse.Bytes_to_Integer( byte_ss, None )

            # Run mode
            run_variables = ( d_cm, d_cd, depth, k, dx, dy, dw, dh, num_array, num_ss )
            thread = True
            if thread == False: # Local
                if self.split_method == "CHANNEL":
                    Run_Channel( self, *run_variables )
                elif self.split_method == "RANGE":
                    Run_Range( self, *run_variables )
            elif thread == True: # Thread
                # Thread
                self.thread_samples = QThread()
                # self.thread_samples.setPriority( QThread.HighestPriority )
                self.worker_samples = Worker_Samples()
                self.worker_samples.moveToThread( self.thread_samples )
                # Thread
                self.thread_samples.started.connect( lambda : self.worker_samples.run( self, self.split_method, run_variables ) )
                self.thread_samples.start()
        else:
            self.Message_Warnning( "ERROR", "Canvas not Found" )
        # Progress bar
        self.ProgressBar_Value( 0 )
    def Thread_Samples_Quit( self ):
        # Variables
        try:self.thread_samples.quit()
        except:pass
        # User Interface
        self.ProgressBar_Value( 0 )
        self.Widgets_Enabled( True )
        self.update()
        # Time Watcher
        end = QtCore.QDateTime.currentDateTimeUtc()
        delta = self.time.msecsTo( end )
        time = QTime( 0,0 ).addMSecs( delta )
        self.Message_Log( self.split_method, f"{ time.toString( 'hh:mm:ss.zzz' ) }" )
    # Krita Selection
    def Mask_Insert( self ):
        # num_array - list of integer numbers, represents each pixels channels. RGB U8 > [ B,G,R,A, B,G,R,A, B,G,R,A, ... ]

        # Variables
        item = None
        len_cd = len( self.channel_data )
        len_rd = len( self.range_data )
        if len_cd > 0 or len_rd > 0:
            if self.split_method == "CHANNEL":
                item = self.channel_data[ self.channel_index ]
            if self.split_method == "RANGE":
                item = self.range_data[0]
            if item != None:
                # Variables
                num_array = item["map"]
                px = item["dx"]
                py = item["dy"]
                width = item["dw"]
                height = item["dh"]

                # Apply Map
                canvas = self.canvas()
                view = canvas.view()
                if ( ( canvas is not None ) and ( view is not None ) ):
                    # Variables
                    ki = Krita.instance()
                    ad = ki.activeDocument()
                    nt = ad.activeNode().type()

                    # Place selection on good parent node
                    if nt in [ "paintlayer", "grouplayer" ]:
                        # Deselect all
                        ki.action( "deselect" ).trigger()
                        # Place Text
                        self.Message_Float( "INSERT", "Selection", "local-selection-active" )
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
                        self.Message_Float( "ERROR", "Invalid active layer to Insert", self.qicon_insert )
                else:
                    self.Message_Warnning( "ERROR", "Canvas not found" )
        else:
            self.Message_Float( "ERROR", "Map data not found", self.qicon_insert )
    def Mask_Clean( self ):
        # Variables
        if self.split_method == "CHANNEL":
            self.channel_data = []
            self.channel_select.Set_Display( None )
        if self.split_method == "RANGE":
            self.range_data = []
        # User Interface
        self.Map_Display( self.qpixmap_logo, False )
        self.Mode_Insert( False )

    #endregion
    #region Notifier

    # Notifier
    def Window_Created( self ):
        # Module
        self.window = Krita.instance().activeWindow()
        # Signals
        self.window.activeViewChanged.connect( self.View_Changed )
        self.window.themeChanged.connect( self.Theme_Changed )
        self.window.windowClosed.connect( self.Window_Closed )
        # Start Position
        self.Theme_Changed()

    def View_Changed( self ):
        pass
    def Theme_Changed( self ):
        # Krita Theme
        theme_value = QApplication.palette().color( QPalette.Window ).value()
        if theme_value > 128:
            self.color_1 = QColor( "#191919" )
            self.color_2 = QColor( "#e5e5e5" )
        else:
            self.color_1 = QColor( "#e5e5e5" )
            self.color_2 = QColor( "#191919" )
        # Update
        self.display_map.Set_Theme( self.color_1, self.color_2 )
        self.channel_select.Set_Theme( self.color_1, self.color_2 )
        self.range_0.Set_Theme( self.color_1, self.color_2 )
        self.range_1.Set_Theme( self.color_1, self.color_2 )
        self.range_2.Set_Theme( self.color_1, self.color_2 )
        self.range_3.Set_Theme( self.color_1, self.color_2 )
    def Window_Closed( self ):
        pass

    #endregion
    #region Widget Events 

    def showEvent( self, event ):
        self.Import_Pigment_O()
        self.Update_Size()
    def resizeEvent( self, event ):
        # self.Resize_Print( event )
        self.Update_Size()
    def enterEvent( self, event ):
        self.Color_READ()
    def leaveEvent( self, event ):
        pass
    def closeEvent( self, event ):
        pass

    def eventFilter( self, source, event ):
        # Mode
        if ( event.type() == QEvent.MouseButtonPress and source is self.layout.mode ):
            self.Menu_Mode_Press( event )
            return True

        return super().eventFilter( source, event )

    def canvasChanged( self, canvas ):
        pass

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

    # qimage = QImage( byte_array, width, height, QImage.Format_RGBA8888 )
    """

    #endregion

class Worker_Samples( QObject ):

    def run( self, source, split_method, run_variables ):
        source.thread_samples.setPriority( QThread.HighestPriority )
        # Method
        if split_method == "CHANNEL":
            Run_Channel( source, *run_variables )
        elif split_method == "RANGE":
            Run_Range( source, *run_variables )

# Cycles
def Run_Channel( self, d_cm, d_cd, depth, k, dx, dy, dw, dh, num_array, num_ss ):
    # Variables
    index = 0
    c0 = 0.75
    c1 = 0.25
    c2 = 0.25
    cor = False
    hue_rgb = [ "HSV", "HSL", "HCY", "ARD" ]
    hue_xyz = [ "LCH" ]

    # Channels
    if self.color_space == "A":
        channels = 1
    elif self.color_space == "CMYK":
        channels = 4
    else:
        channels = 3
    alpha = 1
    number = channels + alpha + int( self.tic_display )
    self.channel_select.Set_ChannelNumber( number )

    # Item Selection
    try:
        previous = self.geometry.Limit_Range( self.channel_index, 0, number - 1 )
    except:
        previous = 0

    # Channel names
    chan_0, chan_1, chan_2, chan_3 = self.Channel_Names( self.color_space )

    # Lists Render
    byte_0_r = []
    byte_1_r = []
    byte_2_r = []
    byte_3_r = []
    byte_t_r = []
    byte_a_r = []
    # Lists Maps
    byte_0_m = []
    byte_1_m = []
    byte_2_m = []
    byte_3_m = []
    byte_t_m = []
    byte_a_m = []

    # Progress bar
    self.ProgressBar_Value( 0 )
    QApplication.processEvents()

    # Document
    div = int( dh / 100 )
    for y in range( 0, dh ):
        # Progress Bar
        y1 = y + 1
        if ( y1 % div ) == 0:
            percent = int( round( y1 / dh, 4 ) * 100 )
            self.ProgressBar_Value( percent )
            QApplication.processEvents()

        # Pixel
        for x in range( 0, dw ):
            # Read Byte
            num = self.analyse.Numbers_on_Pixel( d_cm, d_cd, index, num_array )
            ssi = num_ss[index] / depth

            # Convert
            if d_cm == "A":
                # Variables
                n0 = num[0] / depth
                na = num[1] / depth
                # Convert
                conv = self.convert.color_convert( d_cm, self.color_space, [ n0 ] )
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
                conv = self.convert.color_convert( d_cm, self.color_space, [ n0, n1, n2 ] )
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
                conv = self.convert.color_convert( d_cm, self.color_space, [ n0, n1, n2, n3 ] )
                # Variables
                cmyk = [ n0, n1, n2, n3 ]
                bw = 1 - n3

            # Length
            length = len( conv )

            # Channels
            occ = na * ssi
            if length == 1:
                s0 = int( self.geometry.Limit_Float( conv[0] ) * occ * k )
            elif length == 3:
                if self.color_space in hue_rgb:
                    hrgb = self.convert.hue_to_rgb( conv[0] )
                    hue0 = int( hrgb[0] * occ * k )
                    hue1 = int( hrgb[1] * occ * k )
                    hue2 = int( hrgb[2] * occ * k )
                if self.color_space in hue_xyz:
                    rgb = self.convert.lch_to_rgb( conv[0], conv[1], conv[2] )
                    hhh = self.convert.rgb_to_hue( rgb[0], rgb[1], rgb[2] )
                    hrgb = self.convert.hue_to_rgb( hhh )
                    hue0 = int( hrgb[0] * occ * k )
                    hue1 = int( hrgb[1] * occ * k )
                    hue2 = int( hrgb[2] * occ * k )
                s0 = int( self.geometry.Limit_Float( conv[0] ) * occ * k )
                s1 = int( self.geometry.Limit_Float( conv[1] ) * occ * k )
                s2 = int( self.geometry.Limit_Float( conv[2] ) * occ * k )
            elif length == 4:
                s0 = int( self.geometry.Limit_Float( conv[0] ) * occ * k )
                s1 = int( self.geometry.Limit_Float( conv[1] ) * occ * k )
                s2 = int( self.geometry.Limit_Float( conv[2] ) * occ * k )
                if self.invert_cmyk == True:
                    s3 = int( self.geometry.Limit_Float( 1 - conv[3] ) * occ * k )
                else:
                    s3 = int( self.geometry.Limit_Float( conv[3] ) * occ * k )
            # Total Ink Cove_rage
            if self.tic_display == True:
                tic = self.convert.cmyk_to_tic( cmyk[0], cmyk[1], cmyk[2], cmyk[3] )
                t0, t1, t2, tw, cor = self.analyse.Total_Ink_Coverage( self.invert_tic, tic, self.tic_value, c0, c1, c2, bw, cor )
                t0 = int( t0 * occ * k )
                t1 = int( t1 * occ * k )
                t2 = int( t2 * occ * k )
                tw = int( tw * occ * k )
            # Alpha
            na = int( na * occ * k )

            # Images
            if length == 1:
                byte_0_r.extend( [ s0, s0, s0, na ] )
            elif length == 3:
                if self.color_space in hue_rgb:
                    byte_0_r.extend( [ hue0, hue1, hue2, na ] )
                else:
                    byte_0_r.extend( [ s0, s0, s0, na ] )
                byte_1_r.extend( [ s1, s1, s1, na ] )
                if self.color_space in hue_xyz:
                    byte_2_r.extend( [ hue0, hue1, hue2, na ] )
                else:
                    byte_2_r.extend( [ s2, s2, s2, na ] )
            elif length == 4:
                byte_0_r.extend( [ s0, s0, s0, na ] )
                byte_1_r.extend( [ s1, s1, s1, na ] )
                byte_2_r.extend( [ s2, s2, s2, na ] )
                byte_3_r.extend( [ s3, s3, s3, na ] )
            byte_a_r.extend( [ na, na, na, k ] )
            if self.tic_display == True:
                byte_t_r.extend( [ t0, t1, t2, na ] )

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
            byte_a_m.append( na )
            if self.tic_display == True:
                byte_t_m.append( tw )

            # Cycle
            index += 1

    # Check
    if len( byte_0_m ) > 0:
        # QPixmap
        qimage_format = QImage.Format_RGBA8888
        if length >= 1:
            pix_0_r = QPixmap().fromImage(   QImage( bytes( byte_0_r ), dw, dh, qimage_format ) )
        if length >= 3:
            pix_1_r = QPixmap().fromImage(   QImage( bytes( byte_1_r ), dw, dh, qimage_format ) )
            pix_2_r = QPixmap().fromImage(   QImage( bytes( byte_2_r ), dw, dh, qimage_format ) )
        if length == 4:
            pix_3_r = QPixmap().fromImage(   QImage( bytes( byte_3_r ), dw, dh, qimage_format ) )
        pix_a_r = QPixmap().fromImage(       QImage( bytes( byte_a_r ), dw, dh, qimage_format ) )
        if self.tic_display == True:
            pix_t_r = QPixmap().fromImage(   QImage( bytes( byte_t_r ), dw, dh, qimage_format ) )

        # Data
        self.channel_data = []
        if length >= 1:
            self.channel_data.append( { "render":pix_0_r, "map":byte_0_m, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":chan_0,  "cor":False } )
        if length >= 3:
            self.channel_data.append( { "render":pix_1_r, "map":byte_1_m, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":chan_1,  "cor":False } )
            self.channel_data.append( { "render":pix_2_r, "map":byte_2_m, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":chan_2,  "cor":False } )
        if length == 4:
            self.channel_data.append( { "render":pix_3_r, "map":byte_3_m, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":chan_3,  "cor":False } )
        self.channel_data.append(     { "render":pix_a_r, "map":byte_a_m, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":"Alpha", "cor":False } )
        if self.tic_display == True:
            self.channel_data.append( { "render":pix_t_r, "map":byte_t_m, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":"TIC",   "cor":cor } )

        # List
        self.Channel_Index( previous )
        self.Channel_Icons()
        self.Mode_Insert( True )
    else:
        self.Message_Warnning( "ERROR", f"Model { d_cm } and/or Depth { d_cd } not supported" )

    # Progress bar
    self.ProgressBar_Value( 100 )

    # Stop Worker
    self.Thread_Samples_Quit()
def Run_Range( self, d_cm, d_cd, depth, k, dx, dy, dw, dh, num_array, num_ss ):
    # Length
    length = 3
    if self.color_space == "A":
        length = 1
    if self.color_space == "CMYK":
        length = 4

    # Points
    r0pa = self.range_0_pa
    r0pb = self.range_0_pb
    r0pc = self.range_0_pc
    r0pd = self.range_0_pd

    r1pa = self.range_1_pa
    r1pb = self.range_1_pb
    r1pc = self.range_1_pc
    r1pd = self.range_1_pd

    r2pa = self.range_2_pa
    r2pb = self.range_2_pb
    r2pc = self.range_2_pc
    r2pd = self.range_2_pd

    r3pa = self.range_3_pa
    r3pb = self.range_3_pb
    r3pc = self.range_3_pc
    r3pd = self.range_3_pd

    # Calculation
    hue_rgb = [ "HSV", "HSL", "HCY", "ARD" ]
    hue_xyz = [ "LCH" ]
    index = 0
    sel_pixels = list()
    draw_pixels = list()
    div = int( dh / 100 )
    for y in range( 0, dh ):
        # Progress bar
        y1 = ( y + 1 )
        if y1 % div == 0:
            percent = int( round( y1 / dh, 4 ) * 100 )
            self.ProgressBar_Value( percent )
            QApplication.processEvents()

        # Pixels
        for x in range( 0, dw ):
            # Read Bytes
            num = self.analyse.Numbers_on_Pixel( d_cm, d_cd, index, num_array )
            ssi = num_ss[ index ] / depth

            # Convert
            if d_cm == "A":
                conv = self.convert.color_convert( d_cm, self.color_space, [num[0] / depth] )
                alpha = num[1] / depth
            if ( d_cm == "RGB" or d_cm == None ):
                conv = self.convert.color_convert( d_cm, self.color_space, [num[0] / depth, num[1] / depth, num[2] / depth] )
                alpha = num[3] / depth
            if d_cm == "CMYK":
                conv = self.convert.color_convert( d_cm, self.color_space, [num[0] / depth, num[1] / depth, num[2] / depth, num[3] / depth] )
                alpha = num[4] / depth

            # Variables
            occlusion = alpha * ssi
            if length == 1:
                # Parse
                n0 = conv[0]
                # Selection 0
                sel_0 = self.analyse.Selector_Linear( n0, r0pa, r0pb, r0pc, r0pd )
                # Factor
                sel_factor = sel_0 * occlusion
            elif length == 3:
                # Parse
                n0 = conv[0]
                n1 = conv[1]
                n2 = conv[2]
                # Selection 0
                if self.color_space in hue_rgb:
                    sel_0 = self.analyse.Selector_Circular( n0, r0pa, r0pb, r0pc, r0pd )
                else:
                    sel_0 = self.analyse.Selector_Linear( n0, r0pa, r0pb, r0pc, r0pd )
                # Selection 1
                sel_1 = self.analyse.Selector_Linear( n1, r1pa, r1pb, r1pc, r1pd )
                # Selection 2
                if self.color_space in hue_xyz:
                    sel_2 = self.analyse.Selector_Circular( n2, r2pa, r2pb, r2pc, r2pd )
                else:
                    sel_2 = self.analyse.Selector_Linear( n2, r2pa, r2pb, r2pc, r2pd )
                # Factor
                sel_factor = sel_0 * sel_1 * sel_2 * occlusion
            elif length == 4:
                # Parse
                n0 = conv[0]
                n1 = conv[1]
                n2 = conv[2]
                n3 = conv[3]
                # Selection
                sel_0 = self.analyse.Selector_Linear( n0, r0pa, r0pb, r0pc, r0pd )
                sel_1 = self.analyse.Selector_Linear( n1, r1pa, r1pb, r1pc, r1pd )
                sel_2 = self.analyse.Selector_Linear( n2, r2pa, r2pb, r2pc, r2pd )
                sel_3 = self.analyse.Selector_Linear( n3, r3pa, r3pb, r3pc, r3pd )
                # Factor
                sel_factor = sel_0 * sel_1 * sel_2 * sel_3 * occlusion

            # Lists
            s = int( sel_factor * k )
            sel_pixels.append( s )
            v = int( sel_factor * 255 )
            o = int( occlusion * 255 )
            draw_pixels.extend( [ v, v, v, o ] )

            # Cycle
            index += 1

    # Progress bar
    self.ProgressBar_Value( 100 )

    # Selection Mask
    if len( sel_pixels ) > 0:
        # Preview
        qimage_format = QImage.Format_RGBA8888
        qpixmap = QPixmap().fromImage( QImage( bytes( draw_pixels ), dw, dh, qimage_format ) )
        self.display_map.Set_Display( qpixmap )
        # Data
        self.range_data = []
        self.range_data.append( { "render":qpixmap, "map":sel_pixels, "dx":dx, "dy":dy, "dw":dw, "dh":dh, "text":"Color Range", "cor":False } )
        # List
        self.Map_Display( qpixmap, False )
        self.Mode_Insert( True )
    else:
        self.Message_Warnning( "ERROR", f"Model { d_cm } and/or Depth { d_cd } not supported" )

    # Stop Worker
    self.Thread_Samples_Quit()


"""
To Do:
- Color Collection mode: White Colors and Black Colors
"""
