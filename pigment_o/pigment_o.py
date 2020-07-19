# Import Krita
from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic
import os.path
import math
# Pigment.O Modules
from .pigment_o_modulo import (
    Channel_Linear_Diamond,
    Clicks,
    Mixer_Gradient,
    Panel_RGB,
    Panel_HSV,
    Panel_HSL
    )

# Set Window Title Name
DOCKER_NAME = "Pigment.O"
# Timer
check_timer = 1000  # 1000 = 1 SECOND (Zero will Disable checks)
# Color Space Constants
kritaAAA = 255
kritaRGB = 255
kritaHUE = 360
kritaSVL = 255
kritaCMYK = 255
hexAAA = 100  # DO NOT TOUCH !
hexRGB = 255  # DO NOT TOUCH !
hexHUE = 360  # DO NOT TOUCH !
hexSVL = 100  # DO NOT TOUCH !
hexCMYK = 100  # DO NOT TOUCH !
# Numbers
zero = 0
half = 0.5
unit = 1
unitAAA = 1 / kritaAAA
unitRGB = 1 / kritaRGB
unitHUE = 1 / kritaHUE
unitSVL = 1 / kritaSVL
unitCMYK = 1 / kritaCMYK
# UI variables
ui_min_1 = 8
ui_max_1 = 15
ui_min_2 = 5
ui_max_2 = 10
ui_min_3 = 19
ui_max_3 = 34
ui_tip = 30
ui_margin = 5
ui_vspacer = 2
# Brush Tip Default
size = 40
opacity = 1
flow = 1
# Color Reference
color_white = [1, 1, 1]
color_grey = [0.5, 0.5, 0.5]
color_black = [0, 0, 0]
bg_unseen = str("background-color: rgba(0,0,0,0);")
bg_alpha = str("background-color: rgba(0, 0, 0, 50); ")
bg_white = str("background-color: rgba(255, 255, 255, 255); ")
bg_grey = str("background-color: rgba(127, 127, 127, 255); ")
bg_black = str("background-color: rgba(0, 0, 0, 255); ")
bg_white_border = str("background-color: rgb(255, 255, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_grey_border = str("background-color: rgb(127, 127, 127); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_black_border = str("background-color: rgb(0, 0, 0); border: 1px solid rgba(56, 56, 56, 255) ;")


# Create Docker
class PigmentODocker(DockWidget):
    """
    Compact Color Selector with various Color Spaces to choose from
    """

    # Initialize the Docker Window #############################################
    def __init__(self):
        super(PigmentODocker, self).__init__()

        # Window Title
        self.setWindowTitle(DOCKER_NAME)

        # Construct
        self.User_Interface()
        self.Setup()
        self.Connect()
        self.Palette()
        self.Mixers()
        self.Style_Sheet()
        self.Settings_Load()

    # Construct Plugin
    def User_Interface(self):
        # Widget
        self.window = QWidget()
        self.layout = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/pigment_o.ui', self.window)
        self.setWidget(self.window)
        # Values Range
        self.layout.aaa_1_value.setMinimum(0)
        self.layout.rgb_1_value.setMinimum(0)
        self.layout.rgb_2_value.setMinimum(0)
        self.layout.rgb_3_value.setMinimum(0)
        self.layout.hsv_1_value.setMinimum(0)
        self.layout.hsv_2_value.setMinimum(0)
        self.layout.hsv_3_value.setMinimum(0)
        self.layout.hsl_1_value.setMinimum(0)
        self.layout.hsl_2_value.setMinimum(0)
        self.layout.hsl_3_value.setMinimum(0)
        self.layout.cmyk_1_value.setMinimum(0)
        self.layout.cmyk_2_value.setMinimum(0)
        self.layout.cmyk_3_value.setMinimum(0)
        self.layout.cmyk_4_value.setMinimum(0)
        self.layout.aaa_1_value.setMaximum(kritaAAA)
        self.layout.rgb_1_value.setMaximum(kritaRGB)
        self.layout.rgb_2_value.setMaximum(kritaRGB)
        self.layout.rgb_3_value.setMaximum(kritaRGB)
        self.layout.hsv_1_value.setMaximum(kritaHUE)
        self.layout.hsv_2_value.setMaximum(kritaSVL)
        self.layout.hsv_3_value.setMaximum(kritaSVL)
        self.layout.hsl_1_value.setMaximum(kritaHUE)
        self.layout.hsl_2_value.setMaximum(kritaSVL)
        self.layout.hsl_3_value.setMaximum(kritaSVL)
        self.layout.cmyk_1_value.setMaximum(kritaCMYK)
        self.layout.cmyk_2_value.setMaximum(kritaCMYK)
        self.layout.cmyk_3_value.setMaximum(kritaCMYK)
        self.layout.cmyk_4_value.setMaximum(kritaCMYK)
    def Setup(self):
        # Module Channel
        self.aaa_1_slider = Channel_Linear_Diamond(self.layout.aaa_1_slider)
        self.aaa_1_slider.Setup("AAA")
        self.rgb_1_slider = Channel_Linear_Diamond(self.layout.rgb_1_slider)
        self.rgb_2_slider = Channel_Linear_Diamond(self.layout.rgb_2_slider)
        self.rgb_3_slider = Channel_Linear_Diamond(self.layout.rgb_3_slider)
        self.rgb_1_slider.Setup("RGB")
        self.rgb_2_slider.Setup("RGB")
        self.rgb_3_slider.Setup("RGB")
        self.hsv_1_slider = Channel_Linear_Diamond(self.layout.hsv_1_slider)
        self.hsv_2_slider = Channel_Linear_Diamond(self.layout.hsv_2_slider)
        self.hsv_3_slider = Channel_Linear_Diamond(self.layout.hsv_3_slider)
        self.hsv_1_slider.Setup("HUE")
        self.hsv_2_slider.Setup("SVL")
        self.hsv_3_slider.Setup("SVL")
        self.hsl_1_slider = Channel_Linear_Diamond(self.layout.hsl_1_slider)
        self.hsl_2_slider = Channel_Linear_Diamond(self.layout.hsl_2_slider)
        self.hsl_3_slider = Channel_Linear_Diamond(self.layout.hsl_3_slider)
        self.hsl_1_slider.Setup("HUE")
        self.hsl_2_slider.Setup("SVL")
        self.hsl_3_slider.Setup("SVL")
        self.cmyk_1_slider = Channel_Linear_Diamond(self.layout.cmyk_1_slider)
        self.cmyk_2_slider = Channel_Linear_Diamond(self.layout.cmyk_2_slider)
        self.cmyk_3_slider = Channel_Linear_Diamond(self.layout.cmyk_3_slider)
        self.cmyk_4_slider = Channel_Linear_Diamond(self.layout.cmyk_4_slider)
        self.cmyk_1_slider.Setup("CMYK")
        self.cmyk_2_slider.Setup("CMYK")
        self.cmyk_3_slider.Setup("CMYK")
        self.cmyk_4_slider.Setup("CMYK")

        # Start Timer and Connect Switch
        if check_timer >= 1000:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Krita_Update)
            self.timer.start(check_timer)
            # Method ON/OFF switch boot
            self.layout.check.setChecked(True)
            self.Krita_Timer()
    def Connect(self):
        # UI Display Options
        self.layout.check.toggled.connect(self.Krita_Timer)
        self.layout.aaa.toggled.connect(self.Menu_AAA)
        self.layout.rgb.toggled.connect(self.Menu_RGB)
        self.layout.hsv.toggled.connect(self.Menu_HSV)
        self.layout.hsl.toggled.connect(self.Menu_HSL)
        self.layout.cmyk.toggled.connect(self.Menu_CMYK)
        self.layout.tip.toggled.connect(self.Menu_TIP)
        self.layout.tts.toggled.connect(self.Menu_TTS)
        self.layout.mixer_selector.currentTextChanged.connect(self.Menu_Mixer)
        self.layout.panel_selector.currentTextChanged.connect(self.Menu_Panel)

        # Channel ALPHA
        self.layout.aaa_1_label.clicked.connect(self.Pigment_AAA_1_Half)
        self.layout.aaa_1_minus.clicked.connect(self.Pigment_AAA_1_Minus)
        self.layout.aaa_1_plus.clicked.connect(self.Pigment_AAA_1_Plus)
        self.aaa_1_slider.SIGNAL_VALUE.connect(self.Pigment_AAA_1_Slider_Modify)
        self.aaa_1_slider.SIGNAL_RELEASE.connect(self.Pigment_AAA_1_Slider_Release)
        self.layout.aaa_1_value.valueChanged.connect(self.Pigment_AAA_1_Value_Modify)
        self.layout.aaa_1_value.editingFinished.connect(self.Pigment_AAA_1_Value_Release)

        # Channel RED
        self.layout.rgb_1_label.clicked.connect(self.Pigment_RGB_1_Half)
        self.layout.rgb_1_minus.clicked.connect(self.Pigment_RGB_1_Minus)
        self.layout.rgb_1_plus.clicked.connect(self.Pigment_RGB_1_Plus)
        self.rgb_1_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_1_Slider_Modify)
        self.rgb_1_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_1_Slider_Release)
        self.layout.rgb_1_value.valueChanged.connect(self.Pigment_RGB_1_Value_Modify)
        self.layout.rgb_1_value.editingFinished.connect(self.Pigment_RGB_1_Value_Release)
        # Channel GREEN
        self.layout.rgb_2_label.clicked.connect(self.Pigment_RGB_2_Half)
        self.layout.rgb_2_minus.clicked.connect(self.Pigment_RGB_2_Minus)
        self.layout.rgb_2_plus.clicked.connect(self.Pigment_RGB_2_Plus)
        self.rgb_2_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_2_Slider_Modify)
        self.rgb_2_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_2_Slider_Release)
        self.layout.rgb_2_value.valueChanged.connect(self.Pigment_RGB_2_Value_Modify)
        self.layout.rgb_2_value.editingFinished.connect(self.Pigment_RGB_2_Value_Release)
        # Channel BLUE
        self.layout.rgb_3_label.clicked.connect(self.Pigment_RGB_3_Half)
        self.layout.rgb_3_minus.clicked.connect(self.Pigment_RGB_3_Minus)
        self.layout.rgb_3_plus.clicked.connect(self.Pigment_RGB_3_Plus)
        self.rgb_3_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_3_Slider_Modify)
        self.rgb_3_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_3_Slider_Release)
        self.layout.rgb_3_value.valueChanged.connect(self.Pigment_RGB_3_Value_Modify)
        self.layout.rgb_3_value.editingFinished.connect(self.Pigment_RGB_3_Value_Release)

        # Channel HUE
        self.layout.hsv_1_label.clicked.connect(self.Pigment_HSV_1_Half)
        self.layout.hsv_1_minus.clicked.connect(self.Pigment_HSV_1_Minus)
        self.layout.hsv_1_plus.clicked.connect(self.Pigment_HSV_1_Plus)
        self.hsv_1_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_1_Slider_Modify)
        self.hsv_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_1_Slider_Release)
        self.layout.hsv_1_value.valueChanged.connect(self.Pigment_HSV_1_Value_Modify)
        self.layout.hsv_1_value.editingFinished.connect(self.Pigment_HSV_1_Value_Release)
        # Channel SATURATION
        self.layout.hsv_2_label.clicked.connect(self.Pigment_HSV_2_Half)
        self.layout.hsv_2_minus.clicked.connect(self.Pigment_HSV_2_Minus)
        self.layout.hsv_2_plus.clicked.connect(self.Pigment_HSV_2_Plus)
        self.hsv_2_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_2_Slider_Modify)
        self.hsv_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_2_Slider_Release)
        self.layout.hsv_2_value.valueChanged.connect(self.Pigment_HSV_2_Value_Modify)
        self.layout.hsv_2_value.editingFinished.connect(self.Pigment_HSV_2_Value_Release)
        # Channel VALUE
        self.layout.hsv_3_label.clicked.connect(self.Pigment_HSV_3_Half)
        self.layout.hsv_3_minus.clicked.connect(self.Pigment_HSV_3_Minus)
        self.layout.hsv_3_plus.clicked.connect(self.Pigment_HSV_3_Plus)
        self.hsv_3_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_3_Slider_Modify)
        self.hsv_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_3_Slider_Release)
        self.layout.hsv_3_value.valueChanged.connect(self.Pigment_HSV_3_Value_Modify)
        self.layout.hsv_3_value.editingFinished.connect(self.Pigment_HSV_3_Value_Release)

        # Channel HUE
        self.layout.hsl_1_label.clicked.connect(self.Pigment_HSL_1_Half)
        self.layout.hsl_1_minus.clicked.connect(self.Pigment_HSL_1_Minus)
        self.layout.hsl_1_plus.clicked.connect(self.Pigment_HSL_1_Plus)
        self.hsl_1_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_1_Slider_Modify)
        self.hsl_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_1_Slider_Release)
        self.layout.hsl_1_value.valueChanged.connect(self.Pigment_HSL_1_Value_Modify)
        self.layout.hsl_1_value.editingFinished.connect(self.Pigment_HSL_1_Value_Release)
        # Channel SATURATION
        self.layout.hsl_2_label.clicked.connect(self.Pigment_HSL_2_Half)
        self.layout.hsl_2_minus.clicked.connect(self.Pigment_HSL_2_Minus)
        self.layout.hsl_2_plus.clicked.connect(self.Pigment_HSL_2_Plus)
        self.hsl_2_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_2_Slider_Modify)
        self.hsl_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_2_Slider_Release)
        self.layout.hsl_2_value.valueChanged.connect(self.Pigment_HSL_2_Value_Modify)
        self.layout.hsl_2_value.editingFinished.connect(self.Pigment_HSL_2_Value_Release)
        # Channel LIGHT
        self.layout.hsl_3_label.clicked.connect(self.Pigment_HSL_3_Half)
        self.layout.hsl_3_minus.clicked.connect(self.Pigment_HSL_3_Minus)
        self.layout.hsl_3_plus.clicked.connect(self.Pigment_HSL_3_Plus)
        self.hsl_3_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_3_Slider_Modify)
        self.hsl_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_3_Slider_Release)
        self.layout.hsl_3_value.valueChanged.connect(self.Pigment_HSL_3_Value_Modify)
        self.layout.hsl_3_value.editingFinished.connect(self.Pigment_HSL_3_Value_Release)

        # Channel CYAN
        self.layout.cmyk_1_label.clicked.connect(self.Pigment_CMYK_1_Half)
        self.layout.cmyk_1_minus.clicked.connect(self.Pigment_CMYK_1_Minus)
        self.layout.cmyk_1_plus.clicked.connect(self.Pigment_CMYK_1_Plus)
        self.cmyk_1_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_1_Slider_Modify)
        self.cmyk_1_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_1_Slider_Release)
        self.layout.cmyk_1_value.valueChanged.connect(self.Pigment_CMYK_1_Value_Modify)
        self.layout.cmyk_1_value.editingFinished.connect(self.Pigment_CMYK_1_Value_Release)
        # Channel MAGENTA
        self.layout.cmyk_2_label.clicked.connect(self.Pigment_CMYK_2_Half)
        self.layout.cmyk_2_minus.clicked.connect(self.Pigment_CMYK_2_Minus)
        self.layout.cmyk_2_plus.clicked.connect(self.Pigment_CMYK_2_Plus)
        self.cmyk_2_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_2_Slider_Modify)
        self.cmyk_2_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_2_Slider_Release)
        self.layout.cmyk_2_value.valueChanged.connect(self.Pigment_CMYK_2_Value_Modify)
        self.layout.cmyk_2_value.editingFinished.connect(self.Pigment_CMYK_2_Value_Release)
        # Channel YELLOW
        self.layout.cmyk_3_label.clicked.connect(self.Pigment_CMYK_3_Half)
        self.layout.cmyk_3_minus.clicked.connect(self.Pigment_CMYK_3_Minus)
        self.layout.cmyk_3_plus.clicked.connect(self.Pigment_CMYK_3_Plus)
        self.cmyk_3_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_3_Slider_Modify)
        self.cmyk_3_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_3_Slider_Release)
        self.layout.cmyk_3_value.valueChanged.connect(self.Pigment_CMYK_3_Value_Modify)
        self.layout.cmyk_3_value.editingFinished.connect(self.Pigment_CMYK_3_Value_Release)
        # Channel KEY
        self.layout.cmyk_4_label.clicked.connect(self.Pigment_CMYK_4_Half)
        self.layout.cmyk_4_minus.clicked.connect(self.Pigment_CMYK_4_Minus)
        self.layout.cmyk_4_plus.clicked.connect(self.Pigment_CMYK_4_Plus)
        self.cmyk_4_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_4_Slider_Modify)
        self.cmyk_4_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_4_Slider_Release)
        self.layout.cmyk_4_value.valueChanged.connect(self.Pigment_CMYK_4_Value_Modify)
        self.layout.cmyk_4_value.editingFinished.connect(self.Pigment_CMYK_4_Value_Release)

        # Hex Input
        self.layout.hex_string.returnPressed.connect(self.HEX_Code)

        # RGB UVD plane Color
        self.panel_rgb = Panel_RGB(self.layout.panel_rgb_uvd_input)
        self.panel_rgb.SIGNAL_RGB_VALUE.connect(self.Signal_RGB)
        self.panel_rgb.SIGNAL_RGB_RELEASE.connect(self.Pigment_Display_Release)

        # Module Panel HSV
        self.panel_hsv = Panel_HSV(self.layout.panel_hsv_fg)
        self.panel_hsv.SIGNAL_HSV_VALUE.connect(self.Signal_HSV)
        self.panel_hsv.SIGNAL_HSV_RELEASE.connect(self.Pigment_Display_Release)

        # Module Panel HSV
        self.panel_hsl = Panel_HSL(self.layout.panel_hsl_fg)
        self.panel_hsl.SIGNAL_HSL_VALUE.connect(self.Signal_HSL)
        self.panel_hsl.SIGNAL_HSL_RELEASE.connect(self.Pigment_Display_Release)
    def Palette(self):
        # Tip
        self.tip_00 = Clicks(self.layout.tip_00)
        self.tip_00.SIGNAL_APPLY.connect(self.Brush_Lock_APPLY)
        self.tip_00.SIGNAL_SAVE.connect(self.Brush_Lock_SAVE)
        self.tip_00.SIGNAL_CLEAN.connect(self.Brush_Lock_CLEAN)
        # Palette Colors
        self.palette_cor_00 = Clicks(self.layout.cor_00)
        self.palette_cor_01 = Clicks(self.layout.cor_01)
        self.palette_cor_02 = Clicks(self.layout.cor_02)
        self.palette_cor_03 = Clicks(self.layout.cor_03)
        self.palette_cor_04 = Clicks(self.layout.cor_04)
        self.palette_cor_05 = Clicks(self.layout.cor_05)
        self.palette_cor_06 = Clicks(self.layout.cor_06)
        self.palette_cor_07 = Clicks(self.layout.cor_07)
        self.palette_cor_08 = Clicks(self.layout.cor_08)
        self.palette_cor_09 = Clicks(self.layout.cor_09)
        self.palette_cor_10 = Clicks(self.layout.cor_10)
        # Palette Signal
        self.palette_cor_00.SIGNAL_APPLY.connect(self.Color_00_APPLY)
        self.palette_cor_00.SIGNAL_SAVE.connect(self.Color_00_SAVE)
        self.palette_cor_00.SIGNAL_CLEAN.connect(self.Color_00_CLEAN)
        self.palette_cor_01.SIGNAL_APPLY.connect(self.Color_01_APPLY)
        self.palette_cor_01.SIGNAL_SAVE.connect(self.Color_01_SAVE)
        self.palette_cor_01.SIGNAL_CLEAN.connect(self.Color_01_CLEAN)
        self.palette_cor_02.SIGNAL_APPLY.connect(self.Color_02_APPLY)
        self.palette_cor_02.SIGNAL_SAVE.connect(self.Color_02_SAVE)
        self.palette_cor_02.SIGNAL_CLEAN.connect(self.Color_02_CLEAN)
        self.palette_cor_03.SIGNAL_APPLY.connect(self.Color_03_APPLY)
        self.palette_cor_03.SIGNAL_SAVE.connect(self.Color_03_SAVE)
        self.palette_cor_03.SIGNAL_CLEAN.connect(self.Color_03_CLEAN)
        self.palette_cor_04.SIGNAL_APPLY.connect(self.Color_04_APPLY)
        self.palette_cor_04.SIGNAL_SAVE.connect(self.Color_04_SAVE)
        self.palette_cor_04.SIGNAL_CLEAN.connect(self.Color_04_CLEAN)
        self.palette_cor_05.SIGNAL_APPLY.connect(self.Color_05_APPLY)
        self.palette_cor_05.SIGNAL_SAVE.connect(self.Color_05_SAVE)
        self.palette_cor_05.SIGNAL_CLEAN.connect(self.Color_05_CLEAN)
        self.palette_cor_06.SIGNAL_APPLY.connect(self.Color_06_APPLY)
        self.palette_cor_06.SIGNAL_SAVE.connect(self.Color_06_SAVE)
        self.palette_cor_06.SIGNAL_CLEAN.connect(self.Color_06_CLEAN)
        self.palette_cor_07.SIGNAL_APPLY.connect(self.Color_07_APPLY)
        self.palette_cor_07.SIGNAL_SAVE.connect(self.Color_07_SAVE)
        self.palette_cor_07.SIGNAL_CLEAN.connect(self.Color_07_CLEAN)
        self.palette_cor_08.SIGNAL_APPLY.connect(self.Color_08_APPLY)
        self.palette_cor_08.SIGNAL_SAVE.connect(self.Color_08_SAVE)
        self.palette_cor_08.SIGNAL_CLEAN.connect(self.Color_08_CLEAN)
        self.palette_cor_09.SIGNAL_APPLY.connect(self.Color_09_APPLY)
        self.palette_cor_09.SIGNAL_SAVE.connect(self.Color_09_SAVE)
        self.palette_cor_09.SIGNAL_CLEAN.connect(self.Color_09_CLEAN)
        self.palette_cor_10.SIGNAL_APPLY.connect(self.Color_10_APPLY)
        self.palette_cor_10.SIGNAL_SAVE.connect(self.Color_10_SAVE)
        self.palette_cor_10.SIGNAL_CLEAN.connect(self.Color_10_CLEAN)
    def Mixers(self):
        # Module Mixer Colors
        self.mixer_tts = Clicks(self.layout.tts_l1)
        self.mixer_rgb_l1 = Clicks(self.layout.rgb_l1)
        self.mixer_rgb_l2 = Clicks(self.layout.rgb_l2)
        self.mixer_rgb_l3 = Clicks(self.layout.rgb_l3)
        self.mixer_rgb_r1 = Clicks(self.layout.rgb_r1)
        self.mixer_rgb_r2 = Clicks(self.layout.rgb_r2)
        self.mixer_rgb_r3 = Clicks(self.layout.rgb_r3)
        self.mixer_hsv_l1 = Clicks(self.layout.hsv_l1)
        self.mixer_hsv_l2 = Clicks(self.layout.hsv_l2)
        self.mixer_hsv_l3 = Clicks(self.layout.hsv_l3)
        self.mixer_hsv_r1 = Clicks(self.layout.hsv_r1)
        self.mixer_hsv_r2 = Clicks(self.layout.hsv_r2)
        self.mixer_hsv_r3 = Clicks(self.layout.hsv_r3)
        self.mixer_hsl_l1 = Clicks(self.layout.hsl_l1)
        self.mixer_hsl_l2 = Clicks(self.layout.hsl_l2)
        self.mixer_hsl_l3 = Clicks(self.layout.hsl_l3)
        self.mixer_hsl_r1 = Clicks(self.layout.hsl_r1)
        self.mixer_hsl_r2 = Clicks(self.layout.hsl_r2)
        self.mixer_hsl_r3 = Clicks(self.layout.hsl_r3)
        self.mixer_cmyk_l1 = Clicks(self.layout.cmyk_l1)
        self.mixer_cmyk_l2 = Clicks(self.layout.cmyk_l2)
        self.mixer_cmyk_l3 = Clicks(self.layout.cmyk_l3)
        self.mixer_cmyk_r1 = Clicks(self.layout.cmyk_r1)
        self.mixer_cmyk_r2 = Clicks(self.layout.cmyk_r2)
        self.mixer_cmyk_r3 = Clicks(self.layout.cmyk_r3)
        # TTS connection
        self.mixer_tts.SIGNAL_APPLY.connect(self.Mixer_TTS_APPLY)
        self.mixer_tts.SIGNAL_SAVE.connect(self.Mixer_TTS_SAVE)
        self.mixer_tts.SIGNAL_CLEAN.connect(self.Mixer_TTS_CLEAN)
        # RGB connection
        self.mixer_rgb_l1.SIGNAL_APPLY.connect(self.Mixer_RGB_L1_APPLY)
        self.mixer_rgb_l1.SIGNAL_SAVE.connect(self.Mixer_RGB_L1_SAVE)
        self.mixer_rgb_l1.SIGNAL_CLEAN.connect(self.Mixer_RGB_L1_CLEAN)
        self.mixer_rgb_r1.SIGNAL_APPLY.connect(self.Mixer_RGB_R1_APPLY)
        self.mixer_rgb_r1.SIGNAL_SAVE.connect(self.Mixer_RGB_R1_SAVE)
        self.mixer_rgb_r1.SIGNAL_CLEAN.connect(self.Mixer_RGB_R1_CLEAN)
        self.mixer_rgb_l2.SIGNAL_APPLY.connect(self.Mixer_RGB_L2_APPLY)
        self.mixer_rgb_l2.SIGNAL_SAVE.connect(self.Mixer_RGB_L2_SAVE)
        self.mixer_rgb_l2.SIGNAL_CLEAN.connect(self.Mixer_RGB_L2_CLEAN)
        self.mixer_rgb_r2.SIGNAL_APPLY.connect(self.Mixer_RGB_R2_APPLY)
        self.mixer_rgb_r2.SIGNAL_SAVE.connect(self.Mixer_RGB_R2_SAVE)
        self.mixer_rgb_r2.SIGNAL_CLEAN.connect(self.Mixer_RGB_R2_CLEAN)
        self.mixer_rgb_l3.SIGNAL_APPLY.connect(self.Mixer_RGB_L3_APPLY)
        self.mixer_rgb_l3.SIGNAL_SAVE.connect(self.Mixer_RGB_L3_SAVE)
        self.mixer_rgb_l3.SIGNAL_CLEAN.connect(self.Mixer_RGB_L3_CLEAN)
        self.mixer_rgb_r3.SIGNAL_APPLY.connect(self.Mixer_RGB_R3_APPLY)
        self.mixer_rgb_r3.SIGNAL_SAVE.connect(self.Mixer_RGB_R3_SAVE)
        self.mixer_rgb_r3.SIGNAL_CLEAN.connect(self.Mixer_RGB_R3_CLEAN)
        # HSV connection
        self.mixer_hsv_l1.SIGNAL_APPLY.connect(self.Mixer_HSV_L1_APPLY)
        self.mixer_hsv_l1.SIGNAL_SAVE.connect(self.Mixer_HSV_L1_SAVE)
        self.mixer_hsv_l1.SIGNAL_CLEAN.connect(self.Mixer_HSV_L1_CLEAN)
        self.mixer_hsv_r1.SIGNAL_APPLY.connect(self.Mixer_HSV_R1_APPLY)
        self.mixer_hsv_r1.SIGNAL_SAVE.connect(self.Mixer_HSV_R1_SAVE)
        self.mixer_hsv_r1.SIGNAL_CLEAN.connect(self.Mixer_HSV_R1_CLEAN)
        self.mixer_hsv_l2.SIGNAL_APPLY.connect(self.Mixer_HSV_L2_APPLY)
        self.mixer_hsv_l2.SIGNAL_SAVE.connect(self.Mixer_HSV_L2_SAVE)
        self.mixer_hsv_l2.SIGNAL_CLEAN.connect(self.Mixer_HSV_L2_CLEAN)
        self.mixer_hsv_r2.SIGNAL_APPLY.connect(self.Mixer_HSV_R2_APPLY)
        self.mixer_hsv_r2.SIGNAL_SAVE.connect(self.Mixer_HSV_R2_SAVE)
        self.mixer_hsv_r2.SIGNAL_CLEAN.connect(self.Mixer_HSV_R2_CLEAN)
        self.mixer_hsv_l3.SIGNAL_APPLY.connect(self.Mixer_HSV_L3_APPLY)
        self.mixer_hsv_l3.SIGNAL_SAVE.connect(self.Mixer_HSV_L3_SAVE)
        self.mixer_hsv_l3.SIGNAL_CLEAN.connect(self.Mixer_HSV_L3_CLEAN)
        self.mixer_hsv_r3.SIGNAL_APPLY.connect(self.Mixer_HSV_R3_APPLY)
        self.mixer_hsv_r3.SIGNAL_SAVE.connect(self.Mixer_HSV_R3_SAVE)
        self.mixer_hsv_r3.SIGNAL_CLEAN.connect(self.Mixer_HSV_R3_CLEAN)
        # HSL connection
        self.mixer_hsl_l1.SIGNAL_APPLY.connect(self.Mixer_HSL_L1_APPLY)
        self.mixer_hsl_l1.SIGNAL_SAVE.connect(self.Mixer_HSL_L1_SAVE)
        self.mixer_hsl_l1.SIGNAL_CLEAN.connect(self.Mixer_HSL_L1_CLEAN)
        self.mixer_hsl_r1.SIGNAL_APPLY.connect(self.Mixer_HSL_R1_APPLY)
        self.mixer_hsl_r1.SIGNAL_SAVE.connect(self.Mixer_HSL_R1_SAVE)
        self.mixer_hsl_r1.SIGNAL_CLEAN.connect(self.Mixer_HSL_R1_CLEAN)
        self.mixer_hsl_l2.SIGNAL_APPLY.connect(self.Mixer_HSL_L2_APPLY)
        self.mixer_hsl_l2.SIGNAL_SAVE.connect(self.Mixer_HSL_L2_SAVE)
        self.mixer_hsl_l2.SIGNAL_CLEAN.connect(self.Mixer_HSL_L2_CLEAN)
        self.mixer_hsl_r2.SIGNAL_APPLY.connect(self.Mixer_HSL_R2_APPLY)
        self.mixer_hsl_r2.SIGNAL_SAVE.connect(self.Mixer_HSL_R2_SAVE)
        self.mixer_hsl_r2.SIGNAL_CLEAN.connect(self.Mixer_HSL_R2_CLEAN)
        self.mixer_hsl_l3.SIGNAL_APPLY.connect(self.Mixer_HSL_L3_APPLY)
        self.mixer_hsl_l3.SIGNAL_SAVE.connect(self.Mixer_HSL_L3_SAVE)
        self.mixer_hsl_l3.SIGNAL_CLEAN.connect(self.Mixer_HSL_L3_CLEAN)
        self.mixer_hsl_r3.SIGNAL_APPLY.connect(self.Mixer_HSL_R3_APPLY)
        self.mixer_hsl_r3.SIGNAL_SAVE.connect(self.Mixer_HSL_R3_SAVE)
        self.mixer_hsl_r3.SIGNAL_CLEAN.connect(self.Mixer_HSL_R3_CLEAN)
        # CMYK connection
        self.mixer_cmyk_l1.SIGNAL_APPLY.connect(self.Mixer_CMYK_L1_APPLY)
        self.mixer_cmyk_l1.SIGNAL_SAVE.connect(self.Mixer_CMYK_L1_SAVE)
        self.mixer_cmyk_l1.SIGNAL_CLEAN.connect(self.Mixer_CMYK_L1_CLEAN)
        self.mixer_cmyk_r1.SIGNAL_APPLY.connect(self.Mixer_CMYK_R1_APPLY)
        self.mixer_cmyk_r1.SIGNAL_SAVE.connect(self.Mixer_CMYK_R1_SAVE)
        self.mixer_cmyk_r1.SIGNAL_CLEAN.connect(self.Mixer_CMYK_R1_CLEAN)
        self.mixer_cmyk_l2.SIGNAL_APPLY.connect(self.Mixer_CMYK_L2_APPLY)
        self.mixer_cmyk_l2.SIGNAL_SAVE.connect(self.Mixer_CMYK_L2_SAVE)
        self.mixer_cmyk_l2.SIGNAL_CLEAN.connect(self.Mixer_CMYK_L2_CLEAN)
        self.mixer_cmyk_r2.SIGNAL_APPLY.connect(self.Mixer_CMYK_R2_APPLY)
        self.mixer_cmyk_r2.SIGNAL_SAVE.connect(self.Mixer_CMYK_R2_SAVE)
        self.mixer_cmyk_r2.SIGNAL_CLEAN.connect(self.Mixer_CMYK_R2_CLEAN)
        self.mixer_cmyk_l3.SIGNAL_APPLY.connect(self.Mixer_CMYK_L3_APPLY)
        self.mixer_cmyk_l3.SIGNAL_SAVE.connect(self.Mixer_CMYK_L3_SAVE)
        self.mixer_cmyk_l3.SIGNAL_CLEAN.connect(self.Mixer_CMYK_L3_CLEAN)
        self.mixer_cmyk_r3.SIGNAL_APPLY.connect(self.Mixer_CMYK_R3_APPLY)
        self.mixer_cmyk_r3.SIGNAL_SAVE.connect(self.Mixer_CMYK_R3_SAVE)
        self.mixer_cmyk_r3.SIGNAL_CLEAN.connect(self.Mixer_CMYK_R3_CLEAN)

        # Module Mixer Gradients
        self.mixer_tint = Mixer_Gradient(self.layout.tint)
        self.mixer_tone = Mixer_Gradient(self.layout.tone)
        self.mixer_shade = Mixer_Gradient(self.layout.shade)
        self.mixer_rgb_g1 = Mixer_Gradient(self.layout.rgb_g1)
        self.mixer_rgb_g2 = Mixer_Gradient(self.layout.rgb_g2)
        self.mixer_rgb_g3 = Mixer_Gradient(self.layout.rgb_g3)
        self.mixer_hsv_g1 = Mixer_Gradient(self.layout.hsv_g1)
        self.mixer_hsv_g2 = Mixer_Gradient(self.layout.hsv_g2)
        self.mixer_hsv_g3 = Mixer_Gradient(self.layout.hsv_g3)
        self.mixer_hsl_g1 = Mixer_Gradient(self.layout.hsl_g1)
        self.mixer_hsl_g2 = Mixer_Gradient(self.layout.hsl_g2)
        self.mixer_hsl_g3 = Mixer_Gradient(self.layout.hsl_g3)
        self.mixer_cmyk_g1 = Mixer_Gradient(self.layout.cmyk_g1)
        self.mixer_cmyk_g2 = Mixer_Gradient(self.layout.cmyk_g2)
        self.mixer_cmyk_g3 = Mixer_Gradient(self.layout.cmyk_g3)
        # Mixer Gradient Connect
        self.mixer_tint.SIGNAL_MIXER_VALUE.connect(self.Mixer_Tint)
        self.mixer_tone.SIGNAL_MIXER_VALUE.connect(self.Mixer_Tone)
        self.mixer_shade.SIGNAL_MIXER_VALUE.connect(self.Mixer_Shade)
        self.mixer_rgb_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_RGB_G1)
        self.mixer_rgb_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_RGB_G2)
        self.mixer_rgb_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_RGB_G3)
        self.mixer_hsv_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_HSV_G1)
        self.mixer_hsv_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_HSV_G2)
        self.mixer_hsv_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_HSV_G3)
        self.mixer_hsl_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_HSL_G1)
        self.mixer_hsl_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_HSL_G2)
        self.mixer_hsl_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_HSL_G3)
        self.mixer_cmyk_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_CMYK_G1)
        self.mixer_cmyk_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_CMYK_G2)
        self.mixer_cmyk_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_CMYK_G3)
        # Previous Selected Mixer Sliders
        self.mixer_tint.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_tone.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_shade.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_rgb_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_rgb_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_rgb_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsv_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsv_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsv_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsl_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsl_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hsl_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
    def Style_Sheet(self):
        # UI Percentage Gradients Display
        p4 = self.Percentage("4")
        p6 = self.Percentage("6")
        ten = self.Percentage("TEN")
        self.layout.percentage_top.setStyleSheet(ten)
        self.layout.percentage_bot.setStyleSheet(ten)
        self.layout.aaa_1_tick.setStyleSheet(p4)
        self.layout.rgb_1_tick.setStyleSheet(p4)
        self.layout.rgb_2_tick.setStyleSheet(p4)
        self.layout.rgb_3_tick.setStyleSheet(p4)
        self.layout.hsv_1_tick.setStyleSheet(p6)
        self.layout.hsv_2_tick.setStyleSheet(p4)
        self.layout.hsv_3_tick.setStyleSheet(p4)
        self.layout.hsl_1_tick.setStyleSheet(p6)
        self.layout.hsl_2_tick.setStyleSheet(p4)
        self.layout.hsl_3_tick.setStyleSheet(p4)
        self.layout.cmyk_1_tick.setStyleSheet(p4)
        self.layout.cmyk_2_tick.setStyleSheet(p4)
        self.layout.cmyk_3_tick.setStyleSheet(p4)
        self.layout.cmyk_4_tick.setStyleSheet(p4)
        self.layout.percentage_tts_1.setStyleSheet(bg_unseen)
        self.layout.percentage_tts_2.setStyleSheet(bg_unseen)
        self.layout.percentage_rgb_1.setStyleSheet(bg_unseen)
        self.layout.percentage_rgb_2.setStyleSheet(bg_unseen)
        self.layout.percentage_hsv_1.setStyleSheet(bg_unseen)
        self.layout.percentage_hsv_2.setStyleSheet(bg_unseen)
        self.layout.percentage_hsl_1.setStyleSheet(bg_unseen)
        self.layout.percentage_hsl_2.setStyleSheet(bg_unseen)
        self.layout.percentage_cmyk_1.setStyleSheet(bg_unseen)
        self.layout.percentage_cmyk_2.setStyleSheet(bg_unseen)

    # Menu Displays ############################################################
    def Menu_AAA(self):
        font = self.layout.aaa.font()
        if self.layout.aaa.isChecked():
            font.setBold(True)
            self.layout.aaa_1_label.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_label.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_minus.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_minus.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_slider.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_slider.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_plus.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_plus.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_value.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_value.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.aaa_1_label.setMinimumHeight(zero)
            self.layout.aaa_1_label.setMaximumHeight(zero)
            self.layout.aaa_1_minus.setMinimumHeight(zero)
            self.layout.aaa_1_minus.setMaximumHeight(zero)
            self.layout.aaa_1_slider.setMinimumHeight(zero)
            self.layout.aaa_1_slider.setMaximumHeight(zero)
            self.layout.aaa_1_plus.setMinimumHeight(zero)
            self.layout.aaa_1_plus.setMaximumHeight(zero)
            self.layout.aaa_1_value.setMinimumHeight(zero)
            self.layout.aaa_1_value.setMaximumHeight(zero)
            self.layout.aaa_1_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.aaa.setFont(font)
        self.Settings_Save()
    def Menu_RGB(self):
        font = self.layout.rgb.font()
        if self.layout.rgb.isChecked():
            font.setBold(True)
            self.layout.rgb_1_label.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_label.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_minus.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_minus.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_slider.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_slider.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_plus.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_plus.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_value.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_value.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_tick.setMinimumHeight(unit)
            self.layout.rgb_2_label.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_label.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_minus.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_minus.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_slider.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_slider.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_plus.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_plus.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_value.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_value.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_tick.setMinimumHeight(unit)
            self.layout.rgb_3_label.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_label.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_minus.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_minus.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_slider.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_slider.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_plus.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_plus.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_value.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_value.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.rgb_1_label.setMinimumHeight(zero)
            self.layout.rgb_1_label.setMaximumHeight(zero)
            self.layout.rgb_1_minus.setMinimumHeight(zero)
            self.layout.rgb_1_minus.setMaximumHeight(zero)
            self.layout.rgb_1_slider.setMinimumHeight(zero)
            self.layout.rgb_1_slider.setMaximumHeight(zero)
            self.layout.rgb_1_plus.setMinimumHeight(zero)
            self.layout.rgb_1_plus.setMaximumHeight(zero)
            self.layout.rgb_1_value.setMinimumHeight(zero)
            self.layout.rgb_1_value.setMaximumHeight(zero)
            self.layout.rgb_1_tick.setMinimumHeight(zero)
            self.layout.rgb_2_label.setMinimumHeight(zero)
            self.layout.rgb_2_label.setMaximumHeight(zero)
            self.layout.rgb_2_minus.setMinimumHeight(zero)
            self.layout.rgb_2_minus.setMaximumHeight(zero)
            self.layout.rgb_2_slider.setMinimumHeight(zero)
            self.layout.rgb_2_slider.setMaximumHeight(zero)
            self.layout.rgb_2_plus.setMinimumHeight(zero)
            self.layout.rgb_2_plus.setMaximumHeight(zero)
            self.layout.rgb_2_value.setMinimumHeight(zero)
            self.layout.rgb_2_value.setMaximumHeight(zero)
            self.layout.rgb_2_tick.setMinimumHeight(zero)
            self.layout.rgb_3_label.setMinimumHeight(zero)
            self.layout.rgb_3_label.setMaximumHeight(zero)
            self.layout.rgb_3_minus.setMinimumHeight(zero)
            self.layout.rgb_3_minus.setMaximumHeight(zero)
            self.layout.rgb_3_slider.setMinimumHeight(zero)
            self.layout.rgb_3_slider.setMaximumHeight(zero)
            self.layout.rgb_3_plus.setMinimumHeight(zero)
            self.layout.rgb_3_plus.setMaximumHeight(zero)
            self.layout.rgb_3_value.setMinimumHeight(zero)
            self.layout.rgb_3_value.setMaximumHeight(zero)
            self.layout.rgb_3_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.rgb.setFont(font)
        self.Settings_Save()
    def Menu_HSV(self):
        font = self.layout.hsv.font()
        if self.layout.hsv.isChecked():
            font.setBold(True)
            self.layout.hsv_1_label.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_label.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_minus.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_minus.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_slider.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_slider.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_plus.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_plus.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_value.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_value.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_tick.setMinimumHeight(unit)
            self.layout.hsv_2_label.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_label.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_minus.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_minus.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_slider.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_slider.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_plus.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_plus.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_value.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_value.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_tick.setMinimumHeight(unit)
            self.layout.hsv_3_label.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_label.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_minus.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_minus.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_slider.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_slider.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_plus.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_plus.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_value.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_value.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.hsv_1_label.setMinimumHeight(zero)
            self.layout.hsv_1_label.setMaximumHeight(zero)
            self.layout.hsv_1_minus.setMinimumHeight(zero)
            self.layout.hsv_1_minus.setMaximumHeight(zero)
            self.layout.hsv_1_slider.setMinimumHeight(zero)
            self.layout.hsv_1_slider.setMaximumHeight(zero)
            self.layout.hsv_1_plus.setMinimumHeight(zero)
            self.layout.hsv_1_plus.setMaximumHeight(zero)
            self.layout.hsv_1_value.setMinimumHeight(zero)
            self.layout.hsv_1_value.setMaximumHeight(zero)
            self.layout.hsv_1_tick.setMinimumHeight(zero)
            self.layout.hsv_2_label.setMinimumHeight(zero)
            self.layout.hsv_2_label.setMaximumHeight(zero)
            self.layout.hsv_2_minus.setMinimumHeight(zero)
            self.layout.hsv_2_minus.setMaximumHeight(zero)
            self.layout.hsv_2_slider.setMinimumHeight(zero)
            self.layout.hsv_2_slider.setMaximumHeight(zero)
            self.layout.hsv_2_plus.setMinimumHeight(zero)
            self.layout.hsv_2_plus.setMaximumHeight(zero)
            self.layout.hsv_2_value.setMinimumHeight(zero)
            self.layout.hsv_2_value.setMaximumHeight(zero)
            self.layout.hsv_2_tick.setMinimumHeight(zero)
            self.layout.hsv_3_label.setMinimumHeight(zero)
            self.layout.hsv_3_label.setMaximumHeight(zero)
            self.layout.hsv_3_minus.setMinimumHeight(zero)
            self.layout.hsv_3_minus.setMaximumHeight(zero)
            self.layout.hsv_3_slider.setMinimumHeight(zero)
            self.layout.hsv_3_slider.setMaximumHeight(zero)
            self.layout.hsv_3_plus.setMinimumHeight(zero)
            self.layout.hsv_3_plus.setMaximumHeight(zero)
            self.layout.hsv_3_value.setMinimumHeight(zero)
            self.layout.hsv_3_value.setMaximumHeight(zero)
            self.layout.hsv_3_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.hsv.setFont(font)
        self.Settings_Save()
    def Menu_HSL(self):
        font = self.layout.hsl.font()
        if self.layout.hsl.isChecked():
            font.setBold(True)
            self.layout.hsl_1_label.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_label.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_minus.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_minus.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_slider.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_slider.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_plus.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_plus.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_value.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_value.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_tick.setMinimumHeight(unit)
            self.layout.hsl_2_label.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_label.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_minus.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_minus.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_slider.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_slider.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_plus.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_plus.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_value.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_value.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_tick.setMinimumHeight(unit)
            self.layout.hsl_3_label.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_label.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_minus.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_minus.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_slider.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_slider.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_plus.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_plus.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_value.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_value.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.hsl_1_label.setMinimumHeight(zero)
            self.layout.hsl_1_label.setMaximumHeight(zero)
            self.layout.hsl_1_minus.setMinimumHeight(zero)
            self.layout.hsl_1_minus.setMaximumHeight(zero)
            self.layout.hsl_1_slider.setMinimumHeight(zero)
            self.layout.hsl_1_slider.setMaximumHeight(zero)
            self.layout.hsl_1_plus.setMinimumHeight(zero)
            self.layout.hsl_1_plus.setMaximumHeight(zero)
            self.layout.hsl_1_value.setMinimumHeight(zero)
            self.layout.hsl_1_value.setMaximumHeight(zero)
            self.layout.hsl_1_tick.setMinimumHeight(zero)
            self.layout.hsl_2_label.setMinimumHeight(zero)
            self.layout.hsl_2_label.setMaximumHeight(zero)
            self.layout.hsl_2_minus.setMinimumHeight(zero)
            self.layout.hsl_2_minus.setMaximumHeight(zero)
            self.layout.hsl_2_slider.setMinimumHeight(zero)
            self.layout.hsl_2_slider.setMaximumHeight(zero)
            self.layout.hsl_2_plus.setMinimumHeight(zero)
            self.layout.hsl_2_plus.setMaximumHeight(zero)
            self.layout.hsl_2_value.setMinimumHeight(zero)
            self.layout.hsl_2_value.setMaximumHeight(zero)
            self.layout.hsl_2_tick.setMinimumHeight(zero)
            self.layout.hsl_3_label.setMinimumHeight(zero)
            self.layout.hsl_3_label.setMaximumHeight(zero)
            self.layout.hsl_3_minus.setMinimumHeight(zero)
            self.layout.hsl_3_minus.setMaximumHeight(zero)
            self.layout.hsl_3_slider.setMinimumHeight(zero)
            self.layout.hsl_3_slider.setMaximumHeight(zero)
            self.layout.hsl_3_plus.setMinimumHeight(zero)
            self.layout.hsl_3_plus.setMaximumHeight(zero)
            self.layout.hsl_3_value.setMinimumHeight(zero)
            self.layout.hsl_3_value.setMaximumHeight(zero)
            self.layout.hsl_3_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.hsl.setFont(font)
        self.Settings_Save()
    def Menu_CMYK(self):
        font = self.layout.cmyk.font()
        if self.layout.cmyk.isChecked():
            font.setBold(True)
            self.layout.cmyk_1_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_tick.setMinimumHeight(unit)
            self.layout.cmyk_2_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_tick.setMinimumHeight(unit)
            self.layout.cmyk_3_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_tick.setMinimumHeight(unit)
            self.layout.cmyk_4_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.cmyk_1_label.setMinimumHeight(zero)
            self.layout.cmyk_1_label.setMaximumHeight(zero)
            self.layout.cmyk_1_minus.setMinimumHeight(zero)
            self.layout.cmyk_1_minus.setMaximumHeight(zero)
            self.layout.cmyk_1_slider.setMinimumHeight(zero)
            self.layout.cmyk_1_slider.setMaximumHeight(zero)
            self.layout.cmyk_1_plus.setMinimumHeight(zero)
            self.layout.cmyk_1_plus.setMaximumHeight(zero)
            self.layout.cmyk_1_value.setMinimumHeight(zero)
            self.layout.cmyk_1_value.setMaximumHeight(zero)
            self.layout.cmyk_1_tick.setMinimumHeight(zero)
            self.layout.cmyk_2_label.setMinimumHeight(zero)
            self.layout.cmyk_2_label.setMaximumHeight(zero)
            self.layout.cmyk_2_minus.setMinimumHeight(zero)
            self.layout.cmyk_2_minus.setMaximumHeight(zero)
            self.layout.cmyk_2_slider.setMinimumHeight(zero)
            self.layout.cmyk_2_slider.setMaximumHeight(zero)
            self.layout.cmyk_2_plus.setMinimumHeight(zero)
            self.layout.cmyk_2_plus.setMaximumHeight(zero)
            self.layout.cmyk_2_value.setMinimumHeight(zero)
            self.layout.cmyk_2_value.setMaximumHeight(zero)
            self.layout.cmyk_2_tick.setMinimumHeight(zero)
            self.layout.cmyk_3_label.setMinimumHeight(zero)
            self.layout.cmyk_3_label.setMaximumHeight(zero)
            self.layout.cmyk_3_minus.setMinimumHeight(zero)
            self.layout.cmyk_3_minus.setMaximumHeight(zero)
            self.layout.cmyk_3_slider.setMinimumHeight(zero)
            self.layout.cmyk_3_slider.setMaximumHeight(zero)
            self.layout.cmyk_3_plus.setMinimumHeight(zero)
            self.layout.cmyk_3_plus.setMaximumHeight(zero)
            self.layout.cmyk_3_value.setMinimumHeight(zero)
            self.layout.cmyk_3_value.setMaximumHeight(zero)
            self.layout.cmyk_3_tick.setMinimumHeight(zero)
            self.layout.cmyk_4_label.setMinimumHeight(zero)
            self.layout.cmyk_4_label.setMaximumHeight(zero)
            self.layout.cmyk_4_minus.setMinimumHeight(zero)
            self.layout.cmyk_4_minus.setMaximumHeight(zero)
            self.layout.cmyk_4_slider.setMinimumHeight(zero)
            self.layout.cmyk_4_slider.setMaximumHeight(zero)
            self.layout.cmyk_4_plus.setMinimumHeight(zero)
            self.layout.cmyk_4_plus.setMaximumHeight(zero)
            self.layout.cmyk_4_value.setMinimumHeight(zero)
            self.layout.cmyk_4_value.setMaximumHeight(zero)
            self.layout.cmyk_4_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.cmyk.setFont(font)
        self.Settings_Save()

    def Menu_TIP(self):
        font = self.layout.tip.font()
        if self.layout.tip.isChecked():
            font.setBold(True)
            self.layout.tip_00.setMinimumHeight(ui_tip)
            self.layout.tip_00.setMaximumHeight(ui_tip)
            self.layout.line.setMinimumHeight(ui_tip)
            self.layout.line.setMaximumHeight(ui_tip)
            self.layout.cor_00.setMinimumHeight(ui_tip)
            self.layout.cor_00.setMaximumHeight(ui_tip)
            self.layout.cor_01.setMinimumHeight(ui_tip)
            self.layout.cor_01.setMaximumHeight(ui_tip)
            self.layout.cor_02.setMinimumHeight(ui_tip)
            self.layout.cor_02.setMaximumHeight(ui_tip)
            self.layout.cor_03.setMinimumHeight(ui_tip)
            self.layout.cor_03.setMaximumHeight(ui_tip)
            self.layout.cor_04.setMinimumHeight(ui_tip)
            self.layout.cor_04.setMaximumHeight(ui_tip)
            self.layout.cor_05.setMinimumHeight(ui_tip)
            self.layout.cor_05.setMaximumHeight(ui_tip)
            self.layout.cor_06.setMinimumHeight(ui_tip)
            self.layout.cor_06.setMaximumHeight(ui_tip)
            self.layout.cor_07.setMinimumHeight(ui_tip)
            self.layout.cor_07.setMaximumHeight(ui_tip)
            self.layout.cor_08.setMinimumHeight(ui_tip)
            self.layout.cor_08.setMaximumHeight(ui_tip)
            self.layout.cor_09.setMinimumHeight(ui_tip)
            self.layout.cor_09.setMaximumHeight(ui_tip)
            self.layout.cor_10.setMinimumHeight(ui_tip)
            self.layout.cor_10.setMaximumHeight(ui_tip)
            self.layout.cores.setContentsMargins(0, ui_vspacer, 0, ui_margin)
        else:
            font.setBold(False)
            self.layout.tip_00.setMinimumHeight(zero)
            self.layout.tip_00.setMaximumHeight(zero)
            self.layout.line.setMinimumHeight(zero)
            self.layout.line.setMaximumHeight(zero)
            self.layout.cor_00.setMinimumHeight(zero)
            self.layout.cor_00.setMaximumHeight(zero)
            self.layout.cor_01.setMinimumHeight(zero)
            self.layout.cor_01.setMaximumHeight(zero)
            self.layout.cor_02.setMinimumHeight(zero)
            self.layout.cor_02.setMaximumHeight(zero)
            self.layout.cor_03.setMinimumHeight(zero)
            self.layout.cor_03.setMaximumHeight(zero)
            self.layout.cor_04.setMinimumHeight(zero)
            self.layout.cor_04.setMaximumHeight(zero)
            self.layout.cor_05.setMinimumHeight(zero)
            self.layout.cor_05.setMaximumHeight(zero)
            self.layout.cor_06.setMinimumHeight(zero)
            self.layout.cor_06.setMaximumHeight(zero)
            self.layout.cor_07.setMinimumHeight(zero)
            self.layout.cor_07.setMaximumHeight(zero)
            self.layout.cor_08.setMinimumHeight(zero)
            self.layout.cor_08.setMaximumHeight(zero)
            self.layout.cor_09.setMinimumHeight(zero)
            self.layout.cor_09.setMaximumHeight(zero)
            self.layout.cor_10.setMinimumHeight(zero)
            self.layout.cor_10.setMaximumHeight(zero)
            self.layout.cores.setContentsMargins(0, zero, 0, zero)
        self.layout.tip.setFont(font)
        self.Settings_Save()
    def Menu_TTS(self):
        font = self.layout.tts.font()
        if self.layout.tts.isChecked():
            font.setBold(True)
            self.layout.tts_l1.setMinimumHeight(ui_min_3)
            self.layout.tts_l1.setMaximumHeight(ui_max_3)
            self.layout.tint.setMinimumHeight(ui_min_2)
            self.layout.tint.setMaximumHeight(ui_max_2)
            self.layout.tone.setMinimumHeight(ui_min_2)
            self.layout.tone.setMaximumHeight(ui_max_2)
            self.layout.shade.setMinimumHeight(ui_min_2)
            self.layout.shade.setMaximumHeight(ui_max_2)
            self.layout.white.setMinimumHeight(ui_min_2)
            self.layout.white.setMaximumHeight(ui_max_2)
            self.layout.grey.setMinimumHeight(ui_min_2)
            self.layout.grey.setMaximumHeight(ui_max_2)
            self.layout.black.setMinimumHeight(ui_min_2)
            self.layout.black.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_tts_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_tts_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_tts_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_tts_2.setMaximumHeight(ui_vspacer)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, ui_margin)
        else:
            font.setBold(False)
            self.layout.tts_l1.setMinimumHeight(zero)
            self.layout.tts_l1.setMaximumHeight(zero)
            self.layout.tint.setMinimumHeight(zero)
            self.layout.tint.setMaximumHeight(zero)
            self.layout.tone.setMinimumHeight(zero)
            self.layout.tone.setMaximumHeight(zero)
            self.layout.shade.setMinimumHeight(zero)
            self.layout.shade.setMaximumHeight(zero)
            self.layout.white.setMinimumHeight(zero)
            self.layout.white.setMaximumHeight(zero)
            self.layout.grey.setMinimumHeight(zero)
            self.layout.grey.setMaximumHeight(zero)
            self.layout.black.setMinimumHeight(zero)
            self.layout.black.setMaximumHeight(zero)
            self.layout.spacer_tts_1.setMinimumHeight(zero)
            self.layout.spacer_tts_1.setMaximumHeight(zero)
            self.layout.spacer_tts_2.setMinimumHeight(zero)
            self.layout.spacer_tts_2.setMaximumHeight(zero)
            self.layout.spacer_tts_3.setMinimumHeight(zero)
            self.layout.spacer_tts_3.setMaximumHeight(zero)
            self.layout.spacer_tts_4.setMinimumHeight(zero)
            self.layout.spacer_tts_4.setMaximumHeight(zero)
            self.layout.percentage_tts_1.setMinimumHeight(zero)
            self.layout.percentage_tts_1.setMaximumHeight(zero)
            self.layout.percentage_tts_2.setMinimumHeight(zero)
            self.layout.percentage_tts_2.setMaximumHeight(zero)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, zero)
        self.layout.tts.setFont(font)
        self.Settings_Save()
    def Menu_Mixer(self):
        mixer = self.layout.mixer_selector.currentText()
        self.Mixer_Shrink()
        if mixer == "RGB":
            self.layout.rgb_l1.setMinimumHeight(ui_min_2)
            self.layout.rgb_l1.setMaximumHeight(ui_max_2)
            self.layout.rgb_l2.setMinimumHeight(ui_min_2)
            self.layout.rgb_l2.setMaximumHeight(ui_max_2)
            self.layout.rgb_l3.setMinimumHeight(ui_min_2)
            self.layout.rgb_l3.setMaximumHeight(ui_max_2)
            self.layout.rgb_r1.setMinimumHeight(ui_min_2)
            self.layout.rgb_r1.setMaximumHeight(ui_max_2)
            self.layout.rgb_r2.setMinimumHeight(ui_min_2)
            self.layout.rgb_r2.setMaximumHeight(ui_max_2)
            self.layout.rgb_r3.setMinimumHeight(ui_min_2)
            self.layout.rgb_r3.setMaximumHeight(ui_max_2)
            self.layout.rgb_g1.setMinimumHeight(ui_min_2)
            self.layout.rgb_g1.setMaximumHeight(ui_max_2)
            self.layout.rgb_g2.setMinimumHeight(ui_min_2)
            self.layout.rgb_g2.setMaximumHeight(ui_max_2)
            self.layout.rgb_g3.setMinimumHeight(ui_min_2)
            self.layout.rgb_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_rgb_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_rgb_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_rgb_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_rgb_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_rgb.setContentsMargins(0, 0, 0, ui_margin)
        elif mixer == "HSV":
            self.layout.hsv_l1.setMinimumHeight(ui_min_2)
            self.layout.hsv_l1.setMaximumHeight(ui_max_2)
            self.layout.hsv_l2.setMinimumHeight(ui_min_2)
            self.layout.hsv_l2.setMaximumHeight(ui_max_2)
            self.layout.hsv_l3.setMinimumHeight(ui_min_2)
            self.layout.hsv_l3.setMaximumHeight(ui_max_2)
            self.layout.hsv_r1.setMinimumHeight(ui_min_2)
            self.layout.hsv_r1.setMaximumHeight(ui_max_2)
            self.layout.hsv_r2.setMinimumHeight(ui_min_2)
            self.layout.hsv_r2.setMaximumHeight(ui_max_2)
            self.layout.hsv_r3.setMinimumHeight(ui_min_2)
            self.layout.hsv_r3.setMaximumHeight(ui_max_2)
            self.layout.hsv_g1.setMinimumHeight(ui_min_2)
            self.layout.hsv_g1.setMaximumHeight(ui_max_2)
            self.layout.hsv_g2.setMinimumHeight(ui_min_2)
            self.layout.hsv_g2.setMaximumHeight(ui_max_2)
            self.layout.hsv_g3.setMinimumHeight(ui_min_2)
            self.layout.hsv_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_hsv_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsv_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_hsv_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsv_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_hsv.setContentsMargins(0, 0, 0, ui_margin)
        elif mixer == "HSL":
            self.layout.hsl_l1.setMinimumHeight(ui_min_2)
            self.layout.hsl_l1.setMaximumHeight(ui_max_2)
            self.layout.hsl_l2.setMinimumHeight(ui_min_2)
            self.layout.hsl_l2.setMaximumHeight(ui_max_2)
            self.layout.hsl_l3.setMinimumHeight(ui_min_2)
            self.layout.hsl_l3.setMaximumHeight(ui_max_2)
            self.layout.hsl_r1.setMinimumHeight(ui_min_2)
            self.layout.hsl_r1.setMaximumHeight(ui_max_2)
            self.layout.hsl_r2.setMinimumHeight(ui_min_2)
            self.layout.hsl_r2.setMaximumHeight(ui_max_2)
            self.layout.hsl_r3.setMinimumHeight(ui_min_2)
            self.layout.hsl_r3.setMaximumHeight(ui_max_2)
            self.layout.hsl_g1.setMinimumHeight(ui_min_2)
            self.layout.hsl_g1.setMaximumHeight(ui_max_2)
            self.layout.hsl_g2.setMinimumHeight(ui_min_2)
            self.layout.hsl_g2.setMaximumHeight(ui_max_2)
            self.layout.hsl_g3.setMinimumHeight(ui_min_2)
            self.layout.hsl_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_hsl_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsl_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_hsl_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsl_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_hsl.setContentsMargins(0, 0, 0, ui_margin)
        elif mixer == "CMYK":
            self.layout.cmyk_l1.setMinimumHeight(ui_min_2)
            self.layout.cmyk_l1.setMaximumHeight(ui_max_2)
            self.layout.cmyk_l2.setMinimumHeight(ui_min_2)
            self.layout.cmyk_l2.setMaximumHeight(ui_max_2)
            self.layout.cmyk_l3.setMinimumHeight(ui_min_2)
            self.layout.cmyk_l3.setMaximumHeight(ui_max_2)
            self.layout.cmyk_r1.setMinimumHeight(ui_min_2)
            self.layout.cmyk_r1.setMaximumHeight(ui_max_2)
            self.layout.cmyk_r2.setMinimumHeight(ui_min_2)
            self.layout.cmyk_r2.setMaximumHeight(ui_max_2)
            self.layout.cmyk_r3.setMinimumHeight(ui_min_2)
            self.layout.cmyk_r3.setMaximumHeight(ui_max_2)
            self.layout.cmyk_g1.setMinimumHeight(ui_min_2)
            self.layout.cmyk_g1.setMaximumHeight(ui_max_2)
            self.layout.cmyk_g2.setMinimumHeight(ui_min_2)
            self.layout.cmyk_g2.setMaximumHeight(ui_max_2)
            self.layout.cmyk_g3.setMinimumHeight(ui_min_2)
            self.layout.cmyk_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_cmyk_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_cmyk_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_cmyk_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_cmyk_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_cmyk.setContentsMargins(0, 0, 0, ui_margin)
        self.Settings_Save()
    def Mixer_Shrink(self):
        # Mix RGB
        self.layout.rgb_l1.setMinimumHeight(zero)
        self.layout.rgb_l1.setMaximumHeight(zero)
        self.layout.rgb_l2.setMinimumHeight(zero)
        self.layout.rgb_l2.setMaximumHeight(zero)
        self.layout.rgb_l3.setMinimumHeight(zero)
        self.layout.rgb_l3.setMaximumHeight(zero)
        self.layout.rgb_r1.setMinimumHeight(zero)
        self.layout.rgb_r1.setMaximumHeight(zero)
        self.layout.rgb_r2.setMinimumHeight(zero)
        self.layout.rgb_r2.setMaximumHeight(zero)
        self.layout.rgb_r3.setMinimumHeight(zero)
        self.layout.rgb_r3.setMaximumHeight(zero)
        self.layout.rgb_g1.setMinimumHeight(zero)
        self.layout.rgb_g1.setMaximumHeight(zero)
        self.layout.rgb_g2.setMinimumHeight(zero)
        self.layout.rgb_g2.setMaximumHeight(zero)
        self.layout.rgb_g3.setMinimumHeight(zero)
        self.layout.rgb_g3.setMaximumHeight(zero)
        self.layout.spacer_rgb_1.setMinimumHeight(zero)
        self.layout.spacer_rgb_1.setMaximumHeight(zero)
        self.layout.spacer_rgb_2.setMinimumHeight(zero)
        self.layout.spacer_rgb_2.setMaximumHeight(zero)
        self.layout.spacer_rgb_3.setMinimumHeight(zero)
        self.layout.spacer_rgb_3.setMaximumHeight(zero)
        self.layout.spacer_rgb_4.setMinimumHeight(zero)
        self.layout.spacer_rgb_4.setMaximumHeight(zero)
        self.layout.percentage_rgb_1.setMinimumHeight(zero)
        self.layout.percentage_rgb_1.setMaximumHeight(zero)
        self.layout.percentage_rgb_2.setMinimumHeight(zero)
        self.layout.percentage_rgb_2.setMaximumHeight(zero)
        self.layout.mixer_rgb.setContentsMargins(0, 0, 0, zero)
        # Mix HSV
        self.layout.hsv_l1.setMinimumHeight(zero)
        self.layout.hsv_l1.setMaximumHeight(zero)
        self.layout.hsv_l2.setMinimumHeight(zero)
        self.layout.hsv_l2.setMaximumHeight(zero)
        self.layout.hsv_l3.setMinimumHeight(zero)
        self.layout.hsv_l3.setMaximumHeight(zero)
        self.layout.hsv_r1.setMinimumHeight(zero)
        self.layout.hsv_r1.setMaximumHeight(zero)
        self.layout.hsv_r2.setMinimumHeight(zero)
        self.layout.hsv_r2.setMaximumHeight(zero)
        self.layout.hsv_r3.setMinimumHeight(zero)
        self.layout.hsv_r3.setMaximumHeight(zero)
        self.layout.hsv_g1.setMinimumHeight(zero)
        self.layout.hsv_g1.setMaximumHeight(zero)
        self.layout.hsv_g2.setMinimumHeight(zero)
        self.layout.hsv_g2.setMaximumHeight(zero)
        self.layout.hsv_g3.setMinimumHeight(zero)
        self.layout.hsv_g3.setMaximumHeight(zero)
        self.layout.spacer_hsv_1.setMinimumHeight(zero)
        self.layout.spacer_hsv_1.setMaximumHeight(zero)
        self.layout.spacer_hsv_2.setMinimumHeight(zero)
        self.layout.spacer_hsv_2.setMaximumHeight(zero)
        self.layout.spacer_hsv_3.setMinimumHeight(zero)
        self.layout.spacer_hsv_3.setMaximumHeight(zero)
        self.layout.spacer_hsv_4.setMinimumHeight(zero)
        self.layout.spacer_hsv_4.setMaximumHeight(zero)
        self.layout.percentage_hsv_1.setMinimumHeight(zero)
        self.layout.percentage_hsv_1.setMaximumHeight(zero)
        self.layout.percentage_hsv_2.setMinimumHeight(zero)
        self.layout.percentage_hsv_2.setMaximumHeight(zero)
        self.layout.mixer_hsv.setContentsMargins(0, 0, 0, zero)
        # Mix HSL
        self.layout.hsl_l1.setMinimumHeight(zero)
        self.layout.hsl_l1.setMaximumHeight(zero)
        self.layout.hsl_l2.setMinimumHeight(zero)
        self.layout.hsl_l2.setMaximumHeight(zero)
        self.layout.hsl_l3.setMinimumHeight(zero)
        self.layout.hsl_l3.setMaximumHeight(zero)
        self.layout.hsl_r1.setMinimumHeight(zero)
        self.layout.hsl_r1.setMaximumHeight(zero)
        self.layout.hsl_r2.setMinimumHeight(zero)
        self.layout.hsl_r2.setMaximumHeight(zero)
        self.layout.hsl_r3.setMinimumHeight(zero)
        self.layout.hsl_r3.setMaximumHeight(zero)
        self.layout.hsl_g1.setMinimumHeight(zero)
        self.layout.hsl_g1.setMaximumHeight(zero)
        self.layout.hsl_g2.setMinimumHeight(zero)
        self.layout.hsl_g2.setMaximumHeight(zero)
        self.layout.hsl_g3.setMinimumHeight(zero)
        self.layout.hsl_g3.setMaximumHeight(zero)
        self.layout.spacer_hsl_1.setMinimumHeight(zero)
        self.layout.spacer_hsl_1.setMaximumHeight(zero)
        self.layout.spacer_hsl_2.setMinimumHeight(zero)
        self.layout.spacer_hsl_2.setMaximumHeight(zero)
        self.layout.spacer_hsl_3.setMinimumHeight(zero)
        self.layout.spacer_hsl_3.setMaximumHeight(zero)
        self.layout.spacer_hsl_4.setMinimumHeight(zero)
        self.layout.spacer_hsl_4.setMaximumHeight(zero)
        self.layout.percentage_hsl_1.setMinimumHeight(zero)
        self.layout.percentage_hsl_1.setMaximumHeight(zero)
        self.layout.percentage_hsl_2.setMinimumHeight(zero)
        self.layout.percentage_hsl_2.setMaximumHeight(zero)
        self.layout.mixer_hsl.setContentsMargins(0, 0, 0, zero)
        # Mix CMYK
        self.layout.cmyk_l1.setMinimumHeight(zero)
        self.layout.cmyk_l1.setMaximumHeight(zero)
        self.layout.cmyk_l2.setMinimumHeight(zero)
        self.layout.cmyk_l2.setMaximumHeight(zero)
        self.layout.cmyk_l3.setMinimumHeight(zero)
        self.layout.cmyk_l3.setMaximumHeight(zero)
        self.layout.cmyk_r1.setMinimumHeight(zero)
        self.layout.cmyk_r1.setMaximumHeight(zero)
        self.layout.cmyk_r2.setMinimumHeight(zero)
        self.layout.cmyk_r2.setMaximumHeight(zero)
        self.layout.cmyk_r3.setMinimumHeight(zero)
        self.layout.cmyk_r3.setMaximumHeight(zero)
        self.layout.cmyk_g1.setMinimumHeight(zero)
        self.layout.cmyk_g1.setMaximumHeight(zero)
        self.layout.cmyk_g2.setMinimumHeight(zero)
        self.layout.cmyk_g2.setMaximumHeight(zero)
        self.layout.cmyk_g3.setMinimumHeight(zero)
        self.layout.cmyk_g3.setMaximumHeight(zero)
        self.layout.spacer_cmyk_1.setMinimumHeight(zero)
        self.layout.spacer_cmyk_1.setMaximumHeight(zero)
        self.layout.spacer_cmyk_2.setMinimumHeight(zero)
        self.layout.spacer_cmyk_2.setMaximumHeight(zero)
        self.layout.spacer_cmyk_3.setMinimumHeight(zero)
        self.layout.spacer_cmyk_3.setMaximumHeight(zero)
        self.layout.spacer_cmyk_4.setMinimumHeight(zero)
        self.layout.spacer_cmyk_4.setMaximumHeight(zero)
        self.layout.percentage_cmyk_1.setMinimumHeight(zero)
        self.layout.percentage_cmyk_1.setMaximumHeight(zero)
        self.layout.percentage_cmyk_2.setMinimumHeight(zero)
        self.layout.percentage_cmyk_2.setMaximumHeight(zero)
        self.layout.mixer_cmyk.setContentsMargins(0, 0, 0, zero)
    def Menu_Panel(self):
        panel = self.layout.panel_selector.currentText()
        self.Panel_Shrink()
        if panel == "PANEL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if (panel == "RGB" or panel == "RGB0"):
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_RGB()
        if (panel == "HSV" or panel == "HSV0"):
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSV()
        if (panel == "HSL" or panel == "HSL0"):
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert_HSL()
        self.Settings_Save()
    def Panel_Shrink(self):
        self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def Menu_Load(self):
        # AAA
        font = self.layout.aaa.font()
        if self.layout.aaa.isChecked():
            font.setBold(True)
            self.layout.aaa_1_label.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_label.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_minus.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_minus.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_slider.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_slider.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_plus.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_plus.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_value.setMinimumHeight(ui_min_1)
            self.layout.aaa_1_value.setMaximumHeight(ui_max_1)
            self.layout.aaa_1_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.aaa_1_label.setMinimumHeight(zero)
            self.layout.aaa_1_label.setMaximumHeight(zero)
            self.layout.aaa_1_minus.setMinimumHeight(zero)
            self.layout.aaa_1_minus.setMaximumHeight(zero)
            self.layout.aaa_1_slider.setMinimumHeight(zero)
            self.layout.aaa_1_slider.setMaximumHeight(zero)
            self.layout.aaa_1_plus.setMinimumHeight(zero)
            self.layout.aaa_1_plus.setMaximumHeight(zero)
            self.layout.aaa_1_value.setMinimumHeight(zero)
            self.layout.aaa_1_value.setMaximumHeight(zero)
            self.layout.aaa_1_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.aaa.setFont(font)
        # RGB
        font = self.layout.rgb.font()
        if self.layout.rgb.isChecked():
            font.setBold(True)
            self.layout.rgb_1_label.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_label.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_minus.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_minus.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_slider.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_slider.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_plus.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_plus.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_value.setMinimumHeight(ui_min_1)
            self.layout.rgb_1_value.setMaximumHeight(ui_max_1)
            self.layout.rgb_1_tick.setMinimumHeight(unit)
            self.layout.rgb_2_label.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_label.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_minus.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_minus.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_slider.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_slider.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_plus.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_plus.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_value.setMinimumHeight(ui_min_1)
            self.layout.rgb_2_value.setMaximumHeight(ui_max_1)
            self.layout.rgb_2_tick.setMinimumHeight(unit)
            self.layout.rgb_3_label.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_label.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_minus.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_minus.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_slider.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_slider.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_plus.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_plus.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_value.setMinimumHeight(ui_min_1)
            self.layout.rgb_3_value.setMaximumHeight(ui_max_1)
            self.layout.rgb_3_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.rgb_1_label.setMinimumHeight(zero)
            self.layout.rgb_1_label.setMaximumHeight(zero)
            self.layout.rgb_1_minus.setMinimumHeight(zero)
            self.layout.rgb_1_minus.setMaximumHeight(zero)
            self.layout.rgb_1_slider.setMinimumHeight(zero)
            self.layout.rgb_1_slider.setMaximumHeight(zero)
            self.layout.rgb_1_plus.setMinimumHeight(zero)
            self.layout.rgb_1_plus.setMaximumHeight(zero)
            self.layout.rgb_1_value.setMinimumHeight(zero)
            self.layout.rgb_1_value.setMaximumHeight(zero)
            self.layout.rgb_1_tick.setMinimumHeight(zero)
            self.layout.rgb_2_label.setMinimumHeight(zero)
            self.layout.rgb_2_label.setMaximumHeight(zero)
            self.layout.rgb_2_minus.setMinimumHeight(zero)
            self.layout.rgb_2_minus.setMaximumHeight(zero)
            self.layout.rgb_2_slider.setMinimumHeight(zero)
            self.layout.rgb_2_slider.setMaximumHeight(zero)
            self.layout.rgb_2_plus.setMinimumHeight(zero)
            self.layout.rgb_2_plus.setMaximumHeight(zero)
            self.layout.rgb_2_value.setMinimumHeight(zero)
            self.layout.rgb_2_value.setMaximumHeight(zero)
            self.layout.rgb_2_tick.setMinimumHeight(zero)
            self.layout.rgb_3_label.setMinimumHeight(zero)
            self.layout.rgb_3_label.setMaximumHeight(zero)
            self.layout.rgb_3_minus.setMinimumHeight(zero)
            self.layout.rgb_3_minus.setMaximumHeight(zero)
            self.layout.rgb_3_slider.setMinimumHeight(zero)
            self.layout.rgb_3_slider.setMaximumHeight(zero)
            self.layout.rgb_3_plus.setMinimumHeight(zero)
            self.layout.rgb_3_plus.setMaximumHeight(zero)
            self.layout.rgb_3_value.setMinimumHeight(zero)
            self.layout.rgb_3_value.setMaximumHeight(zero)
            self.layout.rgb_3_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.rgb.setFont(font)
        # HSV
        font = self.layout.hsv.font()
        if self.layout.hsv.isChecked():
            font.setBold(True)
            self.layout.hsv_1_label.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_label.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_minus.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_minus.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_slider.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_slider.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_plus.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_plus.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_value.setMinimumHeight(ui_min_1)
            self.layout.hsv_1_value.setMaximumHeight(ui_max_1)
            self.layout.hsv_1_tick.setMinimumHeight(unit)
            self.layout.hsv_2_label.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_label.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_minus.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_minus.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_slider.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_slider.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_plus.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_plus.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_value.setMinimumHeight(ui_min_1)
            self.layout.hsv_2_value.setMaximumHeight(ui_max_1)
            self.layout.hsv_2_tick.setMinimumHeight(unit)
            self.layout.hsv_3_label.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_label.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_minus.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_minus.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_slider.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_slider.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_plus.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_plus.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_value.setMinimumHeight(ui_min_1)
            self.layout.hsv_3_value.setMaximumHeight(ui_max_1)
            self.layout.hsv_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.hsv_1_label.setMinimumHeight(zero)
            self.layout.hsv_1_label.setMaximumHeight(zero)
            self.layout.hsv_1_minus.setMinimumHeight(zero)
            self.layout.hsv_1_minus.setMaximumHeight(zero)
            self.layout.hsv_1_slider.setMinimumHeight(zero)
            self.layout.hsv_1_slider.setMaximumHeight(zero)
            self.layout.hsv_1_plus.setMinimumHeight(zero)
            self.layout.hsv_1_plus.setMaximumHeight(zero)
            self.layout.hsv_1_value.setMinimumHeight(zero)
            self.layout.hsv_1_value.setMaximumHeight(zero)
            self.layout.hsv_1_tick.setMinimumHeight(zero)
            self.layout.hsv_2_label.setMinimumHeight(zero)
            self.layout.hsv_2_label.setMaximumHeight(zero)
            self.layout.hsv_2_minus.setMinimumHeight(zero)
            self.layout.hsv_2_minus.setMaximumHeight(zero)
            self.layout.hsv_2_slider.setMinimumHeight(zero)
            self.layout.hsv_2_slider.setMaximumHeight(zero)
            self.layout.hsv_2_plus.setMinimumHeight(zero)
            self.layout.hsv_2_plus.setMaximumHeight(zero)
            self.layout.hsv_2_value.setMinimumHeight(zero)
            self.layout.hsv_2_value.setMaximumHeight(zero)
            self.layout.hsv_2_tick.setMinimumHeight(zero)
            self.layout.hsv_3_label.setMinimumHeight(zero)
            self.layout.hsv_3_label.setMaximumHeight(zero)
            self.layout.hsv_3_minus.setMinimumHeight(zero)
            self.layout.hsv_3_minus.setMaximumHeight(zero)
            self.layout.hsv_3_slider.setMinimumHeight(zero)
            self.layout.hsv_3_slider.setMaximumHeight(zero)
            self.layout.hsv_3_plus.setMinimumHeight(zero)
            self.layout.hsv_3_plus.setMaximumHeight(zero)
            self.layout.hsv_3_value.setMinimumHeight(zero)
            self.layout.hsv_3_value.setMaximumHeight(zero)
            self.layout.hsv_3_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.hsv.setFont(font)
        # HSL
        font = self.layout.hsl.font()
        if self.layout.hsl.isChecked():
            font.setBold(True)
            self.layout.hsl_1_label.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_label.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_minus.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_minus.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_slider.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_slider.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_plus.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_plus.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_value.setMinimumHeight(ui_min_1)
            self.layout.hsl_1_value.setMaximumHeight(ui_max_1)
            self.layout.hsl_1_tick.setMinimumHeight(unit)
            self.layout.hsl_2_label.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_label.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_minus.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_minus.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_slider.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_slider.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_plus.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_plus.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_value.setMinimumHeight(ui_min_1)
            self.layout.hsl_2_value.setMaximumHeight(ui_max_1)
            self.layout.hsl_2_tick.setMinimumHeight(unit)
            self.layout.hsl_3_label.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_label.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_minus.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_minus.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_slider.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_slider.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_plus.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_plus.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_value.setMinimumHeight(ui_min_1)
            self.layout.hsl_3_value.setMaximumHeight(ui_max_1)
            self.layout.hsl_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.hsl_1_label.setMinimumHeight(zero)
            self.layout.hsl_1_label.setMaximumHeight(zero)
            self.layout.hsl_1_minus.setMinimumHeight(zero)
            self.layout.hsl_1_minus.setMaximumHeight(zero)
            self.layout.hsl_1_slider.setMinimumHeight(zero)
            self.layout.hsl_1_slider.setMaximumHeight(zero)
            self.layout.hsl_1_plus.setMinimumHeight(zero)
            self.layout.hsl_1_plus.setMaximumHeight(zero)
            self.layout.hsl_1_value.setMinimumHeight(zero)
            self.layout.hsl_1_value.setMaximumHeight(zero)
            self.layout.hsl_1_tick.setMinimumHeight(zero)
            self.layout.hsl_2_label.setMinimumHeight(zero)
            self.layout.hsl_2_label.setMaximumHeight(zero)
            self.layout.hsl_2_minus.setMinimumHeight(zero)
            self.layout.hsl_2_minus.setMaximumHeight(zero)
            self.layout.hsl_2_slider.setMinimumHeight(zero)
            self.layout.hsl_2_slider.setMaximumHeight(zero)
            self.layout.hsl_2_plus.setMinimumHeight(zero)
            self.layout.hsl_2_plus.setMaximumHeight(zero)
            self.layout.hsl_2_value.setMinimumHeight(zero)
            self.layout.hsl_2_value.setMaximumHeight(zero)
            self.layout.hsl_2_tick.setMinimumHeight(zero)
            self.layout.hsl_3_label.setMinimumHeight(zero)
            self.layout.hsl_3_label.setMaximumHeight(zero)
            self.layout.hsl_3_minus.setMinimumHeight(zero)
            self.layout.hsl_3_minus.setMaximumHeight(zero)
            self.layout.hsl_3_slider.setMinimumHeight(zero)
            self.layout.hsl_3_slider.setMaximumHeight(zero)
            self.layout.hsl_3_plus.setMinimumHeight(zero)
            self.layout.hsl_3_plus.setMaximumHeight(zero)
            self.layout.hsl_3_value.setMinimumHeight(zero)
            self.layout.hsl_3_value.setMaximumHeight(zero)
            self.layout.hsl_3_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.hsl.setFont(font)
        # CMYK
        font = self.layout.cmyk.font()
        if self.layout.cmyk.isChecked():
            font.setBold(True)
            self.layout.cmyk_1_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_1_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_1_tick.setMinimumHeight(unit)
            self.layout.cmyk_2_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_2_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_2_tick.setMinimumHeight(unit)
            self.layout.cmyk_3_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_3_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_3_tick.setMinimumHeight(unit)
            self.layout.cmyk_4_label.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_label.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_minus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_minus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_slider.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_slider.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_plus.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_plus.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_value.setMinimumHeight(ui_min_1)
            self.layout.cmyk_4_value.setMaximumHeight(ui_max_1)
            self.layout.cmyk_4_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.aaa.isChecked() == True or
            self.layout.rgb.isChecked() == True or
            self.layout.hsv.isChecked() == True or
            self.layout.hsl.isChecked() == True or
            self.layout.cmyk.isChecked() == True):
                ten = self.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            font.setBold(False)
            self.layout.cmyk_1_label.setMinimumHeight(zero)
            self.layout.cmyk_1_label.setMaximumHeight(zero)
            self.layout.cmyk_1_minus.setMinimumHeight(zero)
            self.layout.cmyk_1_minus.setMaximumHeight(zero)
            self.layout.cmyk_1_slider.setMinimumHeight(zero)
            self.layout.cmyk_1_slider.setMaximumHeight(zero)
            self.layout.cmyk_1_plus.setMinimumHeight(zero)
            self.layout.cmyk_1_plus.setMaximumHeight(zero)
            self.layout.cmyk_1_value.setMinimumHeight(zero)
            self.layout.cmyk_1_value.setMaximumHeight(zero)
            self.layout.cmyk_1_tick.setMinimumHeight(zero)
            self.layout.cmyk_2_label.setMinimumHeight(zero)
            self.layout.cmyk_2_label.setMaximumHeight(zero)
            self.layout.cmyk_2_minus.setMinimumHeight(zero)
            self.layout.cmyk_2_minus.setMaximumHeight(zero)
            self.layout.cmyk_2_slider.setMinimumHeight(zero)
            self.layout.cmyk_2_slider.setMaximumHeight(zero)
            self.layout.cmyk_2_plus.setMinimumHeight(zero)
            self.layout.cmyk_2_plus.setMaximumHeight(zero)
            self.layout.cmyk_2_value.setMinimumHeight(zero)
            self.layout.cmyk_2_value.setMaximumHeight(zero)
            self.layout.cmyk_2_tick.setMinimumHeight(zero)
            self.layout.cmyk_3_label.setMinimumHeight(zero)
            self.layout.cmyk_3_label.setMaximumHeight(zero)
            self.layout.cmyk_3_minus.setMinimumHeight(zero)
            self.layout.cmyk_3_minus.setMaximumHeight(zero)
            self.layout.cmyk_3_slider.setMinimumHeight(zero)
            self.layout.cmyk_3_slider.setMaximumHeight(zero)
            self.layout.cmyk_3_plus.setMinimumHeight(zero)
            self.layout.cmyk_3_plus.setMaximumHeight(zero)
            self.layout.cmyk_3_value.setMinimumHeight(zero)
            self.layout.cmyk_3_value.setMaximumHeight(zero)
            self.layout.cmyk_3_tick.setMinimumHeight(zero)
            self.layout.cmyk_4_label.setMinimumHeight(zero)
            self.layout.cmyk_4_label.setMaximumHeight(zero)
            self.layout.cmyk_4_minus.setMinimumHeight(zero)
            self.layout.cmyk_4_minus.setMaximumHeight(zero)
            self.layout.cmyk_4_slider.setMinimumHeight(zero)
            self.layout.cmyk_4_slider.setMaximumHeight(zero)
            self.layout.cmyk_4_plus.setMinimumHeight(zero)
            self.layout.cmyk_4_plus.setMaximumHeight(zero)
            self.layout.cmyk_4_value.setMinimumHeight(zero)
            self.layout.cmyk_4_value.setMaximumHeight(zero)
            self.layout.cmyk_4_tick.setMinimumHeight(zero)
            # Remove Percentage Style
            if (self.layout.aaa.isChecked() == False and
            self.layout.rgb.isChecked() == False and
            self.layout.hsv.isChecked() == False and
            self.layout.hsl.isChecked() == False and
            self.layout.cmyk.isChecked() == False):
                self.layout.percentage_top.setStyleSheet(bg_unseen)
                self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.cmyk.setFont(font)
        # TIP
        font = self.layout.tip.font()
        if self.layout.tip.isChecked():
            font.setBold(True)
            self.layout.tip_00.setMinimumHeight(ui_tip)
            self.layout.tip_00.setMaximumHeight(ui_tip)
            self.layout.line.setMinimumHeight(ui_tip)
            self.layout.line.setMaximumHeight(ui_tip)
            self.layout.cor_00.setMinimumHeight(ui_tip)
            self.layout.cor_00.setMaximumHeight(ui_tip)
            self.layout.cor_01.setMinimumHeight(ui_tip)
            self.layout.cor_01.setMaximumHeight(ui_tip)
            self.layout.cor_02.setMinimumHeight(ui_tip)
            self.layout.cor_02.setMaximumHeight(ui_tip)
            self.layout.cor_03.setMinimumHeight(ui_tip)
            self.layout.cor_03.setMaximumHeight(ui_tip)
            self.layout.cor_04.setMinimumHeight(ui_tip)
            self.layout.cor_04.setMaximumHeight(ui_tip)
            self.layout.cor_05.setMinimumHeight(ui_tip)
            self.layout.cor_05.setMaximumHeight(ui_tip)
            self.layout.cor_06.setMinimumHeight(ui_tip)
            self.layout.cor_06.setMaximumHeight(ui_tip)
            self.layout.cor_07.setMinimumHeight(ui_tip)
            self.layout.cor_07.setMaximumHeight(ui_tip)
            self.layout.cor_08.setMinimumHeight(ui_tip)
            self.layout.cor_08.setMaximumHeight(ui_tip)
            self.layout.cor_09.setMinimumHeight(ui_tip)
            self.layout.cor_09.setMaximumHeight(ui_tip)
            self.layout.cor_10.setMinimumHeight(ui_tip)
            self.layout.cor_10.setMaximumHeight(ui_tip)
            self.layout.cores.setContentsMargins(0, ui_vspacer, 0, ui_margin)
        else:
            font.setBold(False)
            self.layout.tip_00.setMinimumHeight(zero)
            self.layout.tip_00.setMaximumHeight(zero)
            self.layout.line.setMinimumHeight(zero)
            self.layout.line.setMaximumHeight(zero)
            self.layout.cor_00.setMinimumHeight(zero)
            self.layout.cor_00.setMaximumHeight(zero)
            self.layout.cor_01.setMinimumHeight(zero)
            self.layout.cor_01.setMaximumHeight(zero)
            self.layout.cor_02.setMinimumHeight(zero)
            self.layout.cor_02.setMaximumHeight(zero)
            self.layout.cor_03.setMinimumHeight(zero)
            self.layout.cor_03.setMaximumHeight(zero)
            self.layout.cor_04.setMinimumHeight(zero)
            self.layout.cor_04.setMaximumHeight(zero)
            self.layout.cor_05.setMinimumHeight(zero)
            self.layout.cor_05.setMaximumHeight(zero)
            self.layout.cor_06.setMinimumHeight(zero)
            self.layout.cor_06.setMaximumHeight(zero)
            self.layout.cor_07.setMinimumHeight(zero)
            self.layout.cor_07.setMaximumHeight(zero)
            self.layout.cor_08.setMinimumHeight(zero)
            self.layout.cor_08.setMaximumHeight(zero)
            self.layout.cor_09.setMinimumHeight(zero)
            self.layout.cor_09.setMaximumHeight(zero)
            self.layout.cor_10.setMinimumHeight(zero)
            self.layout.cor_10.setMaximumHeight(zero)
            self.layout.cores.setContentsMargins(0, zero, 0, zero)
        self.layout.tip.setFont(font)
        # TTS
        font = self.layout.tts.font()
        if self.layout.tts.isChecked():
            font.setBold(True)
            self.layout.tts_l1.setMinimumHeight(ui_min_3)
            self.layout.tts_l1.setMaximumHeight(ui_max_3)
            self.layout.tint.setMinimumHeight(ui_min_2)
            self.layout.tint.setMaximumHeight(ui_max_2)
            self.layout.tone.setMinimumHeight(ui_min_2)
            self.layout.tone.setMaximumHeight(ui_max_2)
            self.layout.shade.setMinimumHeight(ui_min_2)
            self.layout.shade.setMaximumHeight(ui_max_2)
            self.layout.white.setMinimumHeight(ui_min_2)
            self.layout.white.setMaximumHeight(ui_max_2)
            self.layout.grey.setMinimumHeight(ui_min_2)
            self.layout.grey.setMaximumHeight(ui_max_2)
            self.layout.black.setMinimumHeight(ui_min_2)
            self.layout.black.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_tts_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_tts_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_tts_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_tts_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_tts_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_tts_2.setMaximumHeight(ui_vspacer)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, ui_margin)
        else:
            font.setBold(False)
            self.layout.tts_l1.setMinimumHeight(zero)
            self.layout.tts_l1.setMaximumHeight(zero)
            self.layout.tint.setMinimumHeight(zero)
            self.layout.tint.setMaximumHeight(zero)
            self.layout.tone.setMinimumHeight(zero)
            self.layout.tone.setMaximumHeight(zero)
            self.layout.shade.setMinimumHeight(zero)
            self.layout.shade.setMaximumHeight(zero)
            self.layout.white.setMinimumHeight(zero)
            self.layout.white.setMaximumHeight(zero)
            self.layout.grey.setMinimumHeight(zero)
            self.layout.grey.setMaximumHeight(zero)
            self.layout.black.setMinimumHeight(zero)
            self.layout.black.setMaximumHeight(zero)
            self.layout.spacer_tts_1.setMinimumHeight(zero)
            self.layout.spacer_tts_1.setMaximumHeight(zero)
            self.layout.spacer_tts_2.setMinimumHeight(zero)
            self.layout.spacer_tts_2.setMaximumHeight(zero)
            self.layout.spacer_tts_3.setMinimumHeight(zero)
            self.layout.spacer_tts_3.setMaximumHeight(zero)
            self.layout.spacer_tts_4.setMinimumHeight(zero)
            self.layout.spacer_tts_4.setMaximumHeight(zero)
            self.layout.percentage_tts_1.setMinimumHeight(zero)
            self.layout.percentage_tts_1.setMaximumHeight(zero)
            self.layout.percentage_tts_2.setMinimumHeight(zero)
            self.layout.percentage_tts_2.setMaximumHeight(zero)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, zero)
        self.layout.tts.setFont(font)
        # MIXER
        mixer = self.layout.mixer_selector.currentText()
        self.Mixer_Shrink()
        if mixer == "RGB":
            self.layout.rgb_l1.setMinimumHeight(ui_min_2)
            self.layout.rgb_l1.setMaximumHeight(ui_max_2)
            self.layout.rgb_l2.setMinimumHeight(ui_min_2)
            self.layout.rgb_l2.setMaximumHeight(ui_max_2)
            self.layout.rgb_l3.setMinimumHeight(ui_min_2)
            self.layout.rgb_l3.setMaximumHeight(ui_max_2)
            self.layout.rgb_r1.setMinimumHeight(ui_min_2)
            self.layout.rgb_r1.setMaximumHeight(ui_max_2)
            self.layout.rgb_r2.setMinimumHeight(ui_min_2)
            self.layout.rgb_r2.setMaximumHeight(ui_max_2)
            self.layout.rgb_r3.setMinimumHeight(ui_min_2)
            self.layout.rgb_r3.setMaximumHeight(ui_max_2)
            self.layout.rgb_g1.setMinimumHeight(ui_min_2)
            self.layout.rgb_g1.setMaximumHeight(ui_max_2)
            self.layout.rgb_g2.setMinimumHeight(ui_min_2)
            self.layout.rgb_g2.setMaximumHeight(ui_max_2)
            self.layout.rgb_g3.setMinimumHeight(ui_min_2)
            self.layout.rgb_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_rgb_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_rgb_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_rgb_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_rgb_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_rgb_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_rgb_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_rgb.setContentsMargins(0, 0, 0, ui_margin)
        elif mixer == "HSV":
            self.layout.hsv_l1.setMinimumHeight(ui_min_2)
            self.layout.hsv_l1.setMaximumHeight(ui_max_2)
            self.layout.hsv_l2.setMinimumHeight(ui_min_2)
            self.layout.hsv_l2.setMaximumHeight(ui_max_2)
            self.layout.hsv_l3.setMinimumHeight(ui_min_2)
            self.layout.hsv_l3.setMaximumHeight(ui_max_2)
            self.layout.hsv_r1.setMinimumHeight(ui_min_2)
            self.layout.hsv_r1.setMaximumHeight(ui_max_2)
            self.layout.hsv_r2.setMinimumHeight(ui_min_2)
            self.layout.hsv_r2.setMaximumHeight(ui_max_2)
            self.layout.hsv_r3.setMinimumHeight(ui_min_2)
            self.layout.hsv_r3.setMaximumHeight(ui_max_2)
            self.layout.hsv_g1.setMinimumHeight(ui_min_2)
            self.layout.hsv_g1.setMaximumHeight(ui_max_2)
            self.layout.hsv_g2.setMinimumHeight(ui_min_2)
            self.layout.hsv_g2.setMaximumHeight(ui_max_2)
            self.layout.hsv_g3.setMinimumHeight(ui_min_2)
            self.layout.hsv_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsv_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsv_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_hsv_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsv_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_hsv_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsv_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_hsv.setContentsMargins(0, 0, 0, ui_margin)
        elif mixer == "HSL":
            self.layout.hsl_l1.setMinimumHeight(ui_min_2)
            self.layout.hsl_l1.setMaximumHeight(ui_max_2)
            self.layout.hsl_l2.setMinimumHeight(ui_min_2)
            self.layout.hsl_l2.setMaximumHeight(ui_max_2)
            self.layout.hsl_l3.setMinimumHeight(ui_min_2)
            self.layout.hsl_l3.setMaximumHeight(ui_max_2)
            self.layout.hsl_r1.setMinimumHeight(ui_min_2)
            self.layout.hsl_r1.setMaximumHeight(ui_max_2)
            self.layout.hsl_r2.setMinimumHeight(ui_min_2)
            self.layout.hsl_r2.setMaximumHeight(ui_max_2)
            self.layout.hsl_r3.setMinimumHeight(ui_min_2)
            self.layout.hsl_r3.setMaximumHeight(ui_max_2)
            self.layout.hsl_g1.setMinimumHeight(ui_min_2)
            self.layout.hsl_g1.setMaximumHeight(ui_max_2)
            self.layout.hsl_g2.setMinimumHeight(ui_min_2)
            self.layout.hsl_g2.setMaximumHeight(ui_max_2)
            self.layout.hsl_g3.setMinimumHeight(ui_min_2)
            self.layout.hsl_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_hsl_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_hsl_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_hsl_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsl_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_hsl_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_hsl_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_hsl.setContentsMargins(0, 0, 0, ui_margin)
        elif mixer == "CMYK":
            self.layout.cmyk_l1.setMinimumHeight(ui_min_2)
            self.layout.cmyk_l1.setMaximumHeight(ui_max_2)
            self.layout.cmyk_l2.setMinimumHeight(ui_min_2)
            self.layout.cmyk_l2.setMaximumHeight(ui_max_2)
            self.layout.cmyk_l3.setMinimumHeight(ui_min_2)
            self.layout.cmyk_l3.setMaximumHeight(ui_max_2)
            self.layout.cmyk_r1.setMinimumHeight(ui_min_2)
            self.layout.cmyk_r1.setMaximumHeight(ui_max_2)
            self.layout.cmyk_r2.setMinimumHeight(ui_min_2)
            self.layout.cmyk_r2.setMaximumHeight(ui_max_2)
            self.layout.cmyk_r3.setMinimumHeight(ui_min_2)
            self.layout.cmyk_r3.setMaximumHeight(ui_max_2)
            self.layout.cmyk_g1.setMinimumHeight(ui_min_2)
            self.layout.cmyk_g1.setMaximumHeight(ui_max_2)
            self.layout.cmyk_g2.setMinimumHeight(ui_min_2)
            self.layout.cmyk_g2.setMaximumHeight(ui_max_2)
            self.layout.cmyk_g3.setMinimumHeight(ui_min_2)
            self.layout.cmyk_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_cmyk_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_cmyk_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_cmyk_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_cmyk_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_cmyk_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_cmyk_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_cmyk.setContentsMargins(0, 0, 0, ui_margin)
        # PANEL
        panel = self.layout.panel_selector.currentText()
        self.Panel_Shrink()
        if panel == "PANEL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if (panel == "RGB" or panel == "RGB0"):
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_RGB()
        if (panel == "HSV" or panel == "HSV0"):
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSV()
        if (panel == "HSL" or panel == "HSL0"):
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_rgb_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert_HSL()

    # Krita to Pigment #########################################################
    def Krita_Timer(self):
        font = self.layout.check.font()
        if self.layout.check.isChecked():
            font.setBold(True)
            self.layout.check.setText("ON")
            self.Krita_Update()
        else:
            font.setBold(False)
            self.layout.check.setText("OFF")
        self.layout.check.setFont(font)
    def Krita_Update(self):
        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            pigment = self.layout.check.text()
            if (pigment == "ON" or pigment == "&ON"):
                # Check Eraser Mode ON or OFF
                kritaEraserAction = Application.action("erase_action")
                # Document Profile
                doc = self.Document_Profile()
                try:
                    # Current Krita Color
                    color_foreground = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    color_foreground = Application.activeWindow().activeView().foregroundColor()
                    color_background = Application.activeWindow().activeView().backgroundColor()
                    components_fg = color_foreground.components()
                    components_bg = color_background.components()
                    # Hold UVD D depth for autocorrect error
                    self.d_previous = self.rgb_d
                    # Update Pigmento if Values Differ
                    if (doc[0] == "A" or doc[0] == "GRAYA"):
                        # Foreground and Background Colors
                        kac1 = components_fg[0]
                        kbc1 = components_fg[0]
                        # Verify conditions to change Pigment
                        if self.aaa_1 != kac1:
                            if not kritaEraserAction.isChecked():
                                self.Color_AAA(kac1)
                                self.Pigment_Display_Release(0)
                    elif doc[0] == "RGBA":
                        length = len(components_fg)
                        if length == 2:
                            kac1 = components_fg[0]
                            if self.aaa_1 != kac1:
                                if not kritaEraserAction.isChecked():
                                    # Change Pigment
                                    self.Color_AAA(kac1)
                                    # Clean Percentage Label Display
                                    self.Pigment_Display_Release(0)
                        else:
                            if (doc[1] == "U8" or doc[1] == "U16"):
                                # Foreground and Background Colors (Krita is in BGR)
                                kac1 = components_fg[2] # Blue
                                kac2 = components_fg[1] # Green
                                kac3 = components_fg[0] # Red
                                kbc1 = components_bg[2]
                                kbc2 = components_bg[1]
                                kbc3 = components_bg[0]
                            if (doc[1] == "F16" or doc[1] == "F32"):
                                kac1 = components_fg[0] # Red
                                kac2 = components_fg[1] # Green
                                kac3 = components_fg[2] # Blue
                                kbc1 = components_bg[0]
                                kbc2 = components_bg[1]
                                kbc3 = components_bg[2]
                            # Verify conditions to change Pigment
                            if (self.rgb_1 != kac1 or self.rgb_2 != kac2 or self.rgb_3 != kac3):
                                if not kritaEraserAction.isChecked():
                                    # Change Pigment
                                    self.Color_RGB(kac1, kac2, kac3)
                                    # Clean Percentage Label Display
                                    self.Pigment_Display_Release(0)
                    elif doc[0] == "CMYKA":
                        length = len(components_fg)
                        if length == 2:
                            kac1 = components_fg[0]
                            if self.aaa_1 != kac1:
                                if not kritaEraserAction.isChecked():
                                    self.Color_AAA(kac1)
                                    self.Pigment_Display_Release(0)
                        else:
                            # Foreground and Background Colors
                            kac1 = components_fg[0]
                            kac2 = components_fg[1]
                            kac3 = components_fg[2]
                            kac4 = components_fg[3]
                            kbc1 = components_fg[0]
                            kbc2 = components_fg[1]
                            kbc3 = components_fg[2]
                            kbc4 = components_fg[3]
                            # Verify conditions to change Pigment
                            if self.cmyk_1 != kac1 or self.cmyk_2 != kac2 or self.cmyk_3 != kac3 or self.cmyk_4 != kac4:
                                if not kritaEraserAction.isChecked():
                                    self.Color_CMYK(kac1, kac2, kac3, kac4)
                                    self.Pigment_Display_Release(0)
                    elif doc[0] == "XYZA":
                        pass
                    elif doc[0] == "LABA":
                        pass
                    elif doc[0] == "YCbCrA":
                        pass
                except:
                    pass
    def Color_AAA(self, a):
        rgb = [a, a, a]
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = a
        # to RGB
        self.rgb_1 = a
        self.rgb_2 = a
        self.rgb_3 = a
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        condition = self.rgb_d - self.d_previous
        if (condition > -0.004 and condition < 0.004):
            self.rgb_d = self.d_previous
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_UPDATE()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Color_RGB(self, r, g, b):
        # Convertions
        uvd = self.rgb_to_uvd(r, g, b)
        hsv = self.rgb_to_hsv(r, g, b)
        hsl = self.rgb_to_hsl(r, g, b)
        cmyk = self.rgb_to_cmyk(r, g, b)
        # to AAA
        self.aaa_1 = max(r, g, b)
        # to RGB
        self.rgb_1 = r
        self.rgb_2 = g
        self.rgb_3 = b
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        condition = self.rgb_d - self.d_previous
        if (condition > -0.004 and condition < 0.004):
            self.rgb_d = self.d_previous
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_UPDATE()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Color_HSV(self, h, s, v):
        rgb = self.hsv_to_rgb(h, s, v)
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        condition = self.rgb_d - self.d_previous
        if (condition > -0.004 and condition < 0.004):
            self.rgb_d = self.d_previous
        # to HSV
        self.hsv_1 = h
        self.hsv_2 = s
        self.hsv_3 = v
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_UPDATE()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Color_HSL(self, h, s, l):
        rgb = self.hsl_to_rgb(h, s, l)
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        condition = self.rgb_d - self.d_previous
        if (condition > -0.004 and condition < 0.004):
            self.rgb_d = self.d_previous
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = h
        self.hsl_2 = s
        self.hsl_3 = l
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_UPDATE()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Color_CMYK(self, c, m, y, k):
        rgb = self.cmyk_to_rgb(c, m, y, k)
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        condition = self.rgb_d - self.d_previous
        if (condition > -0.004 and condition < 0.004):
            self.rgb_d = self.d_previous
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = c
        self.cmyk_2 = m
        self.cmyk_3 = y
        self.cmyk_4 = k
        # Pigment Update Values
        self.Pigment_Sync_UPDATE()
        self.Pigment_2_Krita()
        self.Pigment_Display()

    # Convert ##################################################################
    def Pigment_Convert_AAA(self):
        # Original
        self.aaa_1 = self.layout.aaa_1_value.value() / kritaAAA
        # Converts
        uvd = self.rgb_to_uvd(self.aaa_1, self.aaa_1, self.aaa_1)
        hsv = self.rgb_to_hsv(self.aaa_1, self.aaa_1, self.aaa_1)
        hsl = self.rgb_to_hsl(self.aaa_1, self.aaa_1, self.aaa_1)
        cmyk = self.rgb_to_cmyk(self.aaa_1, self.aaa_1, self.aaa_1)
        # to RGB
        self.rgb_1 = self.aaa_1
        self.rgb_2 = self.aaa_1
        self.rgb_3 = self.aaa_1
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_AAA()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Pigment_Convert_RGB(self):
        # Original
        self.rgb_1 = self.layout.rgb_1_value.value() / kritaRGB
        self.rgb_2 = self.layout.rgb_2_value.value() / kritaRGB
        self.rgb_3 = self.layout.rgb_3_value.value() / kritaRGB
        # Conversions
        uvd = self.rgb_to_uvd(self.rgb_1, self.rgb_2, self.rgb_3)
        hsv = self.rgb_to_hsv(self.rgb_1, self.rgb_2, self.rgb_3)
        hsl = self.rgb_to_hsl(self.rgb_1, self.rgb_2, self.rgb_3)
        cmyk = self.rgb_to_cmyk(self.rgb_1, self.rgb_2, self.rgb_3)
        # to Alpha
        self.aaa_1 = max(self.rgb_1, self.rgb_2, self.rgb_3)
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_RGB()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Pigment_Convert_HSV(self):
        # Original
        self.hsv_1 = self.layout.hsv_1_value.value() / kritaHUE
        self.hsv_2 = self.layout.hsv_2_value.value() / kritaSVL
        self.hsv_3 = self.layout.hsv_3_value.value() / kritaSVL
        # Conversions
        rgb = self.hsv_to_rgb(self.hsv_1, self.hsv_2, self.hsv_3)
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_HSV()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Pigment_Convert_HSL(self):
        # Original
        self.hsl_1 = self.layout.hsl_1_value.value() / kritaHUE
        self.hsl_2 = self.layout.hsl_2_value.value() / kritaSVL
        self.hsl_3 = self.layout.hsl_3_value.value() / kritaSVL
        # Conversions
        rgb = self.hsl_to_rgb(self.hsl_1, self.hsl_2, self.hsl_3)
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Pigment Update Values
        self.Pigment_Sync_HSL()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    def Pigment_Convert_CMYK(self):
        # Original
        self.cmyk_1 = self.layout.cmyk_1_value.value() / kritaCMYK
        self.cmyk_2 = self.layout.cmyk_2_value.value() / kritaCMYK
        self.cmyk_3 = self.layout.cmyk_3_value.value() / kritaCMYK
        self.cmyk_4 = self.layout.cmyk_4_value.value() / kritaCMYK
        # Conversions
        rgb = self.cmyk_to_rgb(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.rgb_u = uvd[0]
        self.rgb_v = uvd[1]
        self.rgb_d = uvd[2]
        # to HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # to HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # Pigment Update Values
        self.Pigment_Sync_CMYK()
        self.Pigment_2_Krita()
        self.Pigment_Display()
    # RGB HSV HSL CMYK UVD
    def rgb_to_hsv(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        v = maxc
        if minc == maxc:
            return [0.0, 0.0, v]
        s = (maxc-minc) / maxc
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        if r == maxc:
            h = bc-gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = ( h / 6.0 ) % 1.0
        return [h, s, v]
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return [v, v, v]
        i = int(h*6.0) # XXX assume int() truncates!
        f = (h * 6.0) - i
        p = v * ( 1.0 - s )
        q = v * ( 1.0 - s * f )
        t = v * ( 1.0 - s * ( 1.0 - f ))
        i = i%6
        if i == 0:
            return [v, t, p]
        if i == 1:
            return [q, v, p]
        if i == 2:
            return [p, v, t]
        if i == 3:
            return [p, q, v]
        if i == 4:
            return [t, p, v]
        if i == 5:
            return [v, p, q]
    def rgb_to_hsl(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        # XXX Can optimize (maxc+minc) and (maxc-minc)
        l = ( minc + maxc ) / 2.0
        if minc == maxc:
            return [0.0, 0.0, l]
        if l <= 0.5:
            s = ( maxc - minc ) / ( maxc + minc )
        else:
            s = ( maxc - minc ) / ( 2.0 - maxc - minc )
        rc = ( maxc - r ) / ( maxc - minc )
        gc = ( maxc - g ) / ( maxc - minc )
        bc = ( maxc - b ) / ( maxc - minc )
        if r == maxc:
            h = bc-gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = ( h / 6.0) % 1.0
        return [h, s, l]
    def hsl_to_rgb(self, h, s, l):
        if s == 0.0:
            return [l, l, l]
        if l <= 0.5:
            m2 = l * ( 1.0 + s )
        else:
            m2 = l + s - ( l * s )
        m1 = 2.0 * l - m2
        return [self._v(m1, m2, h + ( 1.0 / 3.0 )), self._v(m1, m2, h), self._v(m1, m2, h - ( 1.0 / 3.0 ))]
    def _v(self, m1, m2, hue):
        hue = hue % 1.0
        if hue <  ( 1.0 / 6.0 ) :
            return m1 + ( m2 - m1 ) * hue * 6.0
        if hue < 0.5:
            return m2
        if hue <  ( 2.0 / 3.0 ) :
            return m1 + ( m2 - m1 ) * (( 2.0 / 3.0 ) - hue ) * 6.0
        return m1
    def rgb_to_cmyk(self, r, g, b):
        q = max(r, g, b)
        if q == 0:
            c = 0
            m = 0
            y = 0
            k = 1
        else:
            k = 1 - max(r, g, b)
            c = ( 1 - r - k ) / ( 1 - k )
            m = ( 1 - g - k ) / ( 1 - k )
            y = ( 1 - b - k ) / ( 1 - k )
        return [c, m, y, k]
    def cmyk_to_rgb(self, c, m, y, k):
        r = ( 1 - c ) * ( 1 - k )
        g = ( 1 - m ) * ( 1 - k )
        b = ( 1 - y ) * ( 1 - k )
        return [r, g, b]
    def rgb_to_uvd(self, r, g, b):
        # MatrixInverse * RGB
        MatrixInv = [[-0.866025808, 0.866025808, -0.0000000000000000961481791],
                     [ 0.500000010, 0.499999990, -1.00000000],
                     [ 0.333333497, 0.333333503,  0.333333000]]
        u = MatrixInv[0][0]*r + MatrixInv[0][1]*g + MatrixInv[0][2]*b
        v = MatrixInv[1][0]*r + MatrixInv[1][1]*g + MatrixInv[1][2]*b
        d = MatrixInv[2][0]*r + MatrixInv[2][1]*g + MatrixInv[2][2]*b
        return [u, v, d]
    def uvd_to_rgb(self, u, v, d):
        # Matrix * UVD
        Matrix = [[-0.57735,          0.333333, 1],
                  [ 0.57735,          0.333333, 1],
                  [-0.0000000113021, -0.666667, 1]]
        r = Matrix[0][0]*u + Matrix[0][1]*v + Matrix[0][2]*d
        g = Matrix[1][0]*u + Matrix[1][1]*v + Matrix[1][2]*d
        b = Matrix[2][0]*u + Matrix[2][1]*v + Matrix[2][2]*d
        return [r, g, b]

    # Sync Channels ############################################################
    def Pigment_Sync_AAA(self):
        # Block Signals
        self.Signal_Block_RGB(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_RGB(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_RGB(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_HSV(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_HSL(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_CMYK(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_UPDATE(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    # Signal Block
    def Signal_Block_AAA(self, boolean):
        self.layout.aaa_1_slider.blockSignals(boolean)
        self.layout.aaa_1_value.blockSignals(boolean)
    def Signal_Block_RGB(self, boolean):
        self.layout.rgb_1_slider.blockSignals(boolean)
        self.layout.rgb_2_slider.blockSignals(boolean)
        self.layout.rgb_3_slider.blockSignals(boolean)
        self.layout.rgb_1_value.blockSignals(boolean)
        self.layout.rgb_2_value.blockSignals(boolean)
        self.layout.rgb_3_value.blockSignals(boolean)
    def Signal_Block_HSV(self, boolean):
        self.layout.hsv_1_slider.blockSignals(boolean)
        self.layout.hsv_2_slider.blockSignals(boolean)
        self.layout.hsv_3_slider.blockSignals(boolean)
        self.layout.hsv_1_value.blockSignals(boolean)
        self.layout.hsv_2_value.blockSignals(boolean)
        self.layout.hsv_3_value.blockSignals(boolean)
    def Signal_Block_HSL(self, boolean):
        self.layout.hsl_1_slider.blockSignals(boolean)
        self.layout.hsl_2_slider.blockSignals(boolean)
        self.layout.hsl_3_slider.blockSignals(boolean)
        self.layout.hsl_1_value.blockSignals(boolean)
        self.layout.hsl_2_value.blockSignals(boolean)
        self.layout.hsl_3_value.blockSignals(boolean)
    def Signal_Block_CMYK(self, boolean):
        self.layout.cmyk_1_slider.blockSignals(boolean)
        self.layout.cmyk_2_slider.blockSignals(boolean)
        self.layout.cmyk_3_slider.blockSignals(boolean)
        self.layout.cmyk_4_slider.blockSignals(boolean)
        self.layout.cmyk_1_value.blockSignals(boolean)
        self.layout.cmyk_2_value.blockSignals(boolean)
        self.layout.cmyk_3_value.blockSignals(boolean)
        self.layout.cmyk_4_value.blockSignals(boolean)
    # Signal Send
    def Signal_Send_AAA(self, value1):
        self.aaa_1_slider.Update(value1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(value1 * kritaAAA)
    def Signal_Send_RGB(self, value1, value2, value3):
        self.rgb_1_slider.Update(value1, self.layout.rgb_1_slider.width())
        self.rgb_2_slider.Update(value2, self.layout.rgb_2_slider.width())
        self.rgb_3_slider.Update(value3, self.layout.rgb_3_slider.width())
        self.layout.rgb_1_value.setValue(value1 * kritaRGB)
        self.layout.rgb_2_value.setValue(value2 * kritaRGB)
        self.layout.rgb_3_value.setValue(value3 * kritaRGB)
    def Signal_Send_HSV(self, value1, value2, value3):
        self.hsv_1_slider.Update(value1, self.layout.hsv_1_slider.width())
        self.hsv_2_slider.Update(value2, self.layout.hsv_2_slider.width())
        self.hsv_3_slider.Update(value3, self.layout.hsv_3_slider.width())
        self.layout.hsv_1_value.setValue(value1 * kritaHUE)
        self.layout.hsv_2_value.setValue(value2 * kritaSVL)
        self.layout.hsv_3_value.setValue(value3 * kritaSVL)
    def Signal_Send_HSL(self, value1, value2, value3):
        self.hsl_1_slider.Update(value1, self.layout.hsl_1_slider.width())
        self.hsl_2_slider.Update(value2, self.layout.hsl_2_slider.width())
        self.hsl_3_slider.Update(value3, self.layout.hsl_3_slider.width())
        self.layout.hsl_1_value.setValue(value1 * kritaHUE)
        self.layout.hsl_2_value.setValue(value2 * kritaSVL)
        self.layout.hsl_3_value.setValue(value3 * kritaSVL)
    def Signal_Send_CMYK(self, value1, value2, value3, value4):
        self.cmyk_1_slider.Update(value1, self.layout.cmyk_1_slider.width())
        self.cmyk_2_slider.Update(value2, self.layout.cmyk_2_slider.width())
        self.cmyk_3_slider.Update(value3, self.layout.cmyk_3_slider.width())
        self.cmyk_4_slider.Update(value4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_1_value.setValue(value1 * kritaCMYK)
        self.layout.cmyk_2_value.setValue(value2 * kritaCMYK)
        self.layout.cmyk_3_value.setValue(value3 * kritaCMYK)
        self.layout.cmyk_4_value.setValue(value4 * kritaCMYK)
    def Signal_Send_Panels(self):
        self.Update_UVD()
        self.panel_hsv.Update_Panel(self.hsv_2, self.hsv_3, self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6_SVG())
        self.panel_hsl.Update_Panel(self.hsl_2, self.hsl_3, self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6_SVG())

    # Send to Krita ############################################################
    def Pigment_2_Krita(self):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            pigment = self.layout.check.text()
            if (pigment == "ON" or pigment == "&ON"):
                # Check Eraser Mode ON or OFF
                kritaEraserAction = Application.action("erase_action")
                # Check Document Profile
                doc = self.Document_Profile()
                # Alpha mask
                if doc[0] == "A":
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([self.aaa_1])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                if doc[0] == "GRAYA":  # Gray with bg_alpha channel
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([self.aaa_1, 1.0])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                if doc[0] == "RGBA":  # RGB with bg_alpha channel (The actual order of channels is most often BGR!)
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    if (doc[1] == "U8" or doc[1] == "U16"):
                        pigment_color.setComponents([self.rgb_3, self.rgb_2, self.rgb_1, 1.0])
                    if (doc[1] == "F16" or doc[1] == "F32"):
                        pigment_color.setComponents([self.rgb_1, self.rgb_2, self.rgb_3, 1.0])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                if doc[0] == "CMYKA":  # CMYK with bg_alpha channel
                    # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                    pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    pigment_color.setComponents([self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4, 1.0])
                    Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                    # If Eraser, set it ON again
                    if kritaEraserAction.isChecked():
                        kritaEraserAction.trigger()
                if doc[0] == "XYZA":  # XYZ with bg_alpha channel
                    pass
                if doc[0] == "LABA":  # LAB with bg_alpha channel
                    pass
                if doc[0] == "YCbCrA":  # YCbCr with bg_alpha channel
                    pass
    def Document_Profile(self):
        try:
            ki = Krita.instance()
            ad = ki.activeDocument()
            color_model = ad.colorModel()
            color_depth = ad.colorDepth()
            color_profile = ad.colorProfile()
            doc = []
            doc.append(color_model)
            doc.append(color_depth)
            doc.append(color_profile)
        except:
            doc = ["NONE", "NONE", "NONE"]
        return doc

    # Display ##################################################################
    def Pigment_Display(self):
        # Display Colors
        self.Pigment_Display_Colors()
        # Foreground Color Display (Top Left)
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.Drgb_1*kritaRGB, self.Drgb_2*kritaRGB, self.Drgb_3*kritaRGB))
        self.layout.color_1.setStyleSheet(active_color_1)
        # Alpha
        sss_aaa = str(self.RGB_Gradient(self.layout.aaa_1_slider.width(), [0, 0, 0], [1, 1, 1]))
        # RGB
        sss_rgb1 = str(self.RGB_Gradient(self.layout.rgb_1_slider.width(), [0, self.Drgb_2, self.Drgb_3], [1, self.Drgb_2, self.Drgb_3]))
        sss_rgb2 = str(self.RGB_Gradient(self.layout.rgb_2_slider.width(), [self.Drgb_1, 0, self.Drgb_3], [self.Drgb_1, 1, self.Drgb_3]))
        sss_rgb3 = str(self.RGB_Gradient(self.layout.rgb_3_slider.width(), [self.Drgb_1, self.Drgb_2, 0], [self.Drgb_1, self.Drgb_2, 1]))
        # HSV
        # sss_hsv1 = str(self.Slider("HSV", 0))
        sss_hsv1 = str(self.HUE_HSV_Gradient(0/hexHUE, 60/hexHUE, 120/hexHUE, 180/hexHUE, 240/hexHUE, 300/hexHUE, 360/hexHUE, self.Dhsv_2, self.Dhsv_3))
        sss_hsv2 = str(self.HSV_Gradient(self.layout.hsv_2_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, 0, self.Dhsv_3], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, 1, self.Dhsv_3]))
        sss_hsv3 = str(self.HSV_Gradient(self.layout.hsv_3_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, 0], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, 1]))
        # HSL
        # sss_hsl1 = str(self.Slider("HSL", 0))
        sss_hsl1 = str(self.HUE_HSL_Gradient(0/hexHUE, 60/hexHUE, 120/hexHUE, 180/hexHUE, 240/hexHUE, 300/hexHUE, 360/hexHUE, self.Dhsl_2, self.Dhsl_3))
        sss_hsl2 = str(self.HSL_Gradient(self.layout.hsl_2_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, 0, self.Dhsl_3], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, 1, self.Dhsl_3]))
        sss_hsl3 = str(self.HSL_Gradient(self.layout.hsl_3_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, 0], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, 1]))
        # CMYK
        sss_cmyk1 = str(self.CMYK_Gradient(self.layout.cmyk_1_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, 0, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4], [self.Drgb_1, self.Drgb_2, self.Drgb_3, 1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]))
        sss_cmyk2 = str(self.CMYK_Gradient(self.layout.cmyk_2_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, 0, self.Dcmyk_3, self.Dcmyk_4], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, 1, self.Dcmyk_3, self.Dcmyk_4]))
        sss_cmyk3 = str(self.CMYK_Gradient(self.layout.cmyk_3_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, 0, self.Dcmyk_4], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, 1, self.Dcmyk_4]))
        sss_cmyk4 = str(self.CMYK_Gradient(self.layout.cmyk_4_slider.width(), [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, 0], [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, 1]))
        # Apply Style Sheets
        self.layout.aaa_1_slider.setStyleSheet(sss_aaa)
        self.layout.rgb_1_slider.setStyleSheet(sss_rgb1)
        self.layout.rgb_2_slider.setStyleSheet(sss_rgb2)
        self.layout.rgb_3_slider.setStyleSheet(sss_rgb3)
        self.layout.hsv_1_slider.setStyleSheet(sss_hsv1)
        self.layout.hsv_2_slider.setStyleSheet(sss_hsv2)
        self.layout.hsv_3_slider.setStyleSheet(sss_hsv3)
        self.layout.hsl_1_slider.setStyleSheet(sss_hsl1)
        self.layout.hsl_2_slider.setStyleSheet(sss_hsl2)
        self.layout.hsl_3_slider.setStyleSheet(sss_hsl3)
        self.layout.cmyk_1_slider.setStyleSheet(sss_cmyk1)
        self.layout.cmyk_2_slider.setStyleSheet(sss_cmyk2)
        self.layout.cmyk_3_slider.setStyleSheet(sss_cmyk3)
        self.layout.cmyk_4_slider.setStyleSheet(sss_cmyk4)
        # Hex Color
        hex = self.Pigment_2_HEX()
        self.layout.hex_string.setText(str(hex))
        # Panel Display
        panel = self.layout.panel_selector.currentText()
        # Colors for Panels
        if panel == "RGB":
            self.Update_UVD()
        elif panel == "RGB0":
            self.Update_UVD()
        elif panel == "HSV":
            hue_left = [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, 0, 1]
            hue_right = [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, 1, 1]
            base_color = self.HSV_Gradient(self.layout.hsv_1_slider.width(), hue_left, hue_right)
            self.layout.panel_hsv_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
            self.layout.panel_hsv_fg.setStyleSheet(base_value)
        elif panel == "HSV0":
            base_color = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsv_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsv_fg.setStyleSheet(base_value)
        elif panel == "HSL":
            hue_left = [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, 0, 0.5]
            hue_right = [self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, 1, 0.5]
            base_color = self.HSL_Gradient(self.layout.hsl_1_slider.width(), hue_left, hue_right)
            self.layout.panel_hsl_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.5 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
            self.layout.panel_hsl_fg.setStyleSheet(base_value)
        elif panel == "HSL0":
            base_color = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsl_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsl_fg.setStyleSheet(base_value)
    def Pigment_Display_Release(self, SIGNAL_RELEASE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Dusplay Release Color
        active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.Drgb_1*kritaRGB, self.Drgb_2*kritaRGB, self.Drgb_3*kritaRGB))
        self.layout.color_2.setStyleSheet(active_color_2)
        # RGB Panel Update
        panel = self.layout.panel_selector.currentText()
        if panel == "RGB":
            self.UVD_Color(self.rgb_d)
        if panel == "RGB0":
            self.UVD_Gray(self.rgb_d)
        # Label Percent Clean
        self.layout.label_percent.setText("")
    def Pigment_Display_Colors(self):
        # Localized color values
        self.Drgb_1 = self.rgb_1
        self.Drgb_2 = self.rgb_2
        self.Drgb_3 = self.rgb_3
        # Correct out of Bound values
        if self.Drgb_1 <= 0:
            self.Drgb_1 = 0
        if self.Drgb_1 >= 1:
            self.Drgb_1 = 1
        if self.Drgb_2 <= 0:
            self.Drgb_2 = 0
        if self.Drgb_2 >= 1:
            self.Drgb_2 = 1
        if self.Drgb_3 <= 0:
            self.Drgb_3 = 0
        if self.Drgb_3 >= 1:
            self.Drgb_3 = 1
        # Convert Corrected RGB
        hsv = self.rgb_to_hsv(self.Drgb_1, self.Drgb_2, self.Drgb_3)
        hsl = self.rgb_to_hsl(self.Drgb_1, self.Drgb_2, self.Drgb_3)
        cmyk = self.rgb_to_cmyk(self.Drgb_1, self.Drgb_2, self.Drgb_3)
        # to AAA
        self.Daaa_1 = max(self.Drgb_1, self.Drgb_2, self.Drgb_3)
        # to HSV
        self.Dhsv_1 = hsv[0]
        self.Dhsv_2 = hsv[1]
        self.Dhsv_3 = hsv[2]
        # to HSL
        self.Dhsl_1 = hsl[0]
        self.Dhsl_2 = hsl[1]
        self.Dhsl_3 = hsl[2]
        # to CMYK
        self.Dcmyk_1 = cmyk[0]
        self.Dcmyk_2 = cmyk[1]
        self.Dcmyk_3 = cmyk[2]
        self.Dcmyk_4 = cmyk[3]
    def Ratio(self):
        # Relocate Channel Handle due to Size Variation
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        # Relocate Mixer Handle due to Size Variation
        self.mixer_tint.Update(self.percentage_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.percentage_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.percentage_shade, self.layout.shade.width())
        self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
        self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
        self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())
        # UVD Panel Ratio Adjust to maintain Square
        width = self.layout.panel_rgb_uvd.width()
        height = self.layout.panel_rgb_uvd.height()
        if width >= height:
            self.distance = height
            self.layout.panel_rgb_uvd_mask.setMaximumWidth(height)
            self.layout.panel_rgb_uvd_mask.setMaximumHeight(height)
        elif width < height:
            self.distance = width
            self.layout.panel_rgb_uvd_mask.setMaximumWidth(width)
            self.layout.panel_rgb_uvd_mask.setMaximumHeight(width)
        # Relocate Panel Cursor due to Size Variation
        self.Update_UVD()
        self.panel_hsv.Update_Panel(self.hsv_2, self.hsv_3, self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6_SVG())
        self.panel_hsl.Update_Panel(self.hsl_2, self.hsl_3, self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6_SVG())
        # Update Display
        self.Pigment_Display()
    # UVD Display
    def Update_UVD(self):
        # UVD points of interest
        self.Hexagon_Points()
        # Masking
        hexagon = QPolygon([
            QPoint(self.P1[0], self.P1[1]),
            QPoint(self.P2[0], self.P2[1]),
            QPoint(self.P3[0], self.P3[1]),
            QPoint(self.P4[0], self.P4[1]),
            QPoint(self.P5[0], self.P5[1]),
            QPoint(self.P6[0], self.P6[1]),
            ])
        self.layout.panel_rgb_uvd_mask.setMask(QRegion(hexagon))
        # Update Panel
        self.panel_rgb.Update_Panel(
            self.rgb_u, self.rgb_v, self.rgb_d,
            self.PCC,
            self.P1, self.P2, self.P3, self.P4, self.P5, self.P6,
            self.P12, self.P23, self.P34, self.P45, self.P56, self.P61,
            self.distance, self.distance,
            self.HEX_6_SVG()
            )
    def Hexagon_Points(self):
        # QPolygon
        width = self.layout.panel_rgb_uvd.width()
        height = self.layout.panel_rgb_uvd.height()
        if width >= height:
            self.distance = height
        elif width < height:
            self.distance = width
        one_third = 1/3
        two_third = 2/3
        unit_25 = (0.25 * self.distance) / one_third
        unit_50 = (0.5 * self.distance) / one_third
        unit_43 = (0.433 * self.distance) / one_third
        half_h = 0.5 * self.layout.panel_rgb_uvd_mask.width()
        half_d = 0.5 * self.distance
        side_l = half_h - (0.433 * self.distance)
        side_r = half_h + (0.433 * self.distance)
        side_u = half_d - (0.25 * self.distance)
        side_d = half_d + (0.25 * self.distance)
        diagonal = self.rgb_d
        delta1 = diagonal
        delta2 = diagonal - (1/3)
        delta3 = diagonal - (2/3)
        # Diagonal Progression
        if diagonal <= 0.0:
            self.P1 = [0,0]
            self.P2 = [0,0]
            self.P3 = [0,0]
            self.P4 = [0,0]
            self.P5 = [0,0]
            self.P6 = [0,0]
        elif (diagonal > 0.0 and diagonal <= one_third):
            self.P1 = [half_h,                  half_d-(unit_50*delta1)]  # -1 exception to not be zero area
            self.P2 = [half_h+(unit_43*delta1), half_d+(unit_25*delta1)]
            self.P3 = [half_h+(unit_43*delta1), half_d+(unit_25*delta1)]
            self.P4 = [half_h-(unit_43*delta1), half_d+(unit_25*delta1)]
            self.P5 = [half_h-(unit_43*delta1), half_d+(unit_25*delta1)]
            self.P6 = [half_h,                  half_d-(unit_50*delta1)]  # -1 exception to not be zero area
        elif (diagonal > one_third and diagonal < two_third):
            self.P1 = [half_h+(unit_43*delta2), 0+(unit_25*delta2)]
            self.P2 = [side_r,                  side_d-(unit_50*delta2)]
            self.P3 = [side_r-(unit_43*delta2), side_d+(unit_25*delta2)]
            self.P4 = [side_l+(unit_43*delta2), side_d+(unit_25*delta2)]
            self.P5 = [side_l,                  side_d-(unit_50*delta2)]
            self.P6 = [half_h-(unit_43*delta2), 0+(unit_25*delta2)]
        elif (diagonal >= two_third and diagonal < 1):
            self.P1 = [side_r-(unit_43*delta3), side_u+(unit_25*delta3)]
            self.P2 = [side_r-(unit_43*delta3), side_u+(unit_25*delta3)]
            self.P3 = [half_h,                  self.distance-(unit_50*delta3)]
            self.P4 = [half_h,                  self.distance-(unit_50*delta3)]
            self.P5 = [side_l+(unit_43*delta3), side_u+(unit_25*delta3)]
            self.P6 = [side_l+(unit_43*delta3), side_u+(unit_25*delta3)]
        elif diagonal >= 1:
            self.P1 = [0,0]
            self.P2 = [0,0]
            self.P3 = [0,0]
            self.P4 = [0,0]
            self.P5 = [0,0]
            self.P6 = [0,0]
        # Points
        self.PCC = [half_h, half_d]
        self.P12 = [self.P1[0] + ((self.P2[0] - self.P1[0]) / 2), self.P1[1] + ((self.P2[1] - self.P1[1]) / 2)]
        self.P23 = [self.P2[0] + ((self.P3[0] - self.P2[0]) / 2), self.P2[1] + ((self.P3[1] - self.P2[1]) / 2)]
        self.P34 = [self.P3[0] + ((self.P4[0] - self.P3[0]) / 2), self.P3[1] + ((self.P4[1] - self.P3[1]) / 2)]
        self.P45 = [self.P4[0] + ((self.P5[0] - self.P4[0]) / 2), self.P4[1] + ((self.P5[1] - self.P4[1]) / 2)]
        self.P56 = [self.P5[0] + ((self.P6[0] - self.P5[0]) / 2), self.P5[1] + ((self.P6[1] - self.P5[1]) / 2)]
        self.P61 = [self.P6[0] + ((self.P1[0] - self.P6[0]) / 2), self.P6[1] + ((self.P1[1] - self.P6[1]) / 2)]
    def UVD_Color(self, rgb_d):
        half = 0.5 * self.distance
        # Verify UVD D change with previous selected color to see if it is worth changing
        self.image = QImage(self.distance, self.distance, QImage.Format_RGB32)
        # Cycle through Pixels
        for w in range(self.distance):
            for h in range(self.distance):
                # Consider pixel location and its location color
                u = (w-half)/half
                v = (h-half)/half
                d = self.rgb_d
                # Convert UVD to RGB
                r = -0.57735*u + 0.333333*v + 1*d
                g = 0.57735*u + 0.333333*v + 1*d
                b = -0.0000000113021*u -0.666667*v + 1*d
                # Correct out of Bound values
                if (r<0 or r>1):
                    r=round(r)
                if (g<0 or g>1):
                    g=round(g)
                if (b<0 or b>1):
                    b=round(b)
                # Set Pixel on index
                color = qRgb(r*kritaRGB, g*kritaRGB, b*kritaRGB)
                self.image.setPixel(w, h, color)
        self.layout.panel_rgb_uvd_input.setPixmap(QPixmap(self.image))
    def UVD_Gray(self, rgb_d):
        half = 0.5 * self.distance
        # Verify UVD D change with previous selected color to see if it is worth changing
        self.image = QImage(self.distance, self.distance, QImage.Format_RGB32)
        # Cycle through Pixels
        for w in range(self.distance):
            for h in range(self.distance):
                color = qRgb(rgb_d*kritaRGB, rgb_d*kritaRGB, rgb_d*kritaRGB)
                self.image.setPixel(w, h, color)
        self.layout.panel_rgb_uvd_input.setPixmap(QPixmap(self.image))

    # Hex Codes ################################################################
    def Pigment_2_HEX(self):
        # Check Amount of Channels
        doc = self.Document_Profile()
        if (doc[0] == "A" or doc[0] == "GRAYA"):
            channels = "ONE"
        elif doc[0] == "CMYKA":
            channels = "FOUR"
        else:
            channels = "THREE"
        # Convert Fraction Values to Real HEX Values
        aaa1 = self.Daaa_1 * hexAAA
        rgb1 = self.Drgb_1 * hexRGB
        rgb2 = self.Drgb_2 * hexRGB
        rgb3 = self.Drgb_3 * hexRGB
        cmyk1 = self.Dcmyk_1 * hexCMYK
        cmyk2 = self.Dcmyk_2 * hexCMYK
        cmyk3 = self.Dcmyk_3 * hexCMYK
        cmyk4 = self.Dcmyk_4 * hexCMYK
        # Considering how many channels for HEX code
        if channels == "ONE":
            hex1 = str(hex(int(aaa1)))[2:4].zfill(2)
            pigment_hex = str("#"+hex1)
        elif channels == "THREE":
            hex1 = str(hex(int(rgb1)))[2:4].zfill(2)
            hex2 = str(hex(int(rgb2)))[2:4].zfill(2)
            hex3 = str(hex(int(rgb3)))[2:4].zfill(2)
            pigment_hex = str("#"+hex1+hex2+hex3)
        elif channels == "FOUR":
            hex1 = str(hex(int(cmyk1)))[2:4].zfill(2)
            hex2 = str(hex(int(cmyk2)))[2:4].zfill(2)
            hex3 = str(hex(int(cmyk3)))[2:4].zfill(2)
            hex4 = str(hex(int(cmyk4)))[2:4].zfill(2)
            pigment_hex = str("#"+hex1+hex2+hex3+hex4)
        return pigment_hex
    def HEX_Code(self):
        hex = self.layout.hex_string.text()
        try:
            length = len(hex)
            if (hex[0] == "#" and length == 3):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                # Apply to Pigment
                aaa1 = hex1 / hexAAA
                self.Color_AAA(aaa1)
            elif (hex[0] == "#" and length == 7):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                # Apply to Pigment
                rgb1 = hex1 / hexRGB
                rgb2 = hex2 / hexRGB
                rgb3 = hex3 / hexRGB
                self.Color_RGB(rgb1, rgb2, rgb3)
            elif (hex[0] == "#" and length == 9):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                hex4 = int(format(int(hex[7:9],16),'02d'))
                # Apply to Pigment
                cmyk1 = hex1 / hexCMYK
                cmyk2 = hex2 / hexCMYK
                cmyk3 = hex3 / hexCMYK
                cmyk4 = hex4 / hexCMYK
                self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)
            else:
                self.layout.hex_string.setText("Error")
        except:
            self.layout.hex_string.setText("Error")
        self.Pigment_Display_Release(0)
    def HEX_6_SVG(self):
        # Display Values
        self.Pigment_Display_Colors()
        # Transform into HEX
        hex1 = str(hex(int(self.Drgb_1*hexRGB)))[2:4].zfill(2)
        hex2 = str(hex(int(self.Drgb_2*hexRGB)))[2:4].zfill(2)
        hex3 = str(hex(int(self.Drgb_3*hexRGB)))[2:4].zfill(2)
        pigment_hex = str("#"+hex1+hex2+hex3)
        return pigment_hex

    # Pigment Channels #########################################################
    def Pigment_AAA_1_Half(self):
        self.aaa_1 = half
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaAAA)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Half(self):
        self.rgb_1 = half
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Half(self):
        self.rgb_2 = half
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Half(self):
        self.rgb_3 = half
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Half(self):
        self.hsv_1 = half
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_2_Half(self):
        self.hsv_2 = half
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_3_Half(self):
        self.hsv_3 = half
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSL_1_Half(self):
        self.hsl_1 = half
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_2_Half(self):
        self.hsl_2 = half
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_3_Half(self):
        self.hsl_3 = half
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_CMYK_1_Half(self):
        self.cmyk_1 = half
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_2_Half(self):
        self.cmyk_2 = half
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_3_Half(self):
        self.cmyk_3 = half
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_4_Half(self):
        self.cmyk_4 = half
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()

    def Pigment_AAA_1_Minus(self):
        self.aaa_1 = self.aaa_1 - unitRGB
        if self.aaa_1 <= zero:
            self.aaa_1 = zero
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Minus(self):
        self.rgb_1 = self.rgb_1 - unitRGB
        if self.rgb_1 <= zero:
            self.rgb_1 = zero
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Minus(self):
        self.rgb_2 = self.rgb_2 - unitRGB
        if self.rgb_2 <= zero:
            self.rgb_2 = zero
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Minus(self):
        self.rgb_3 = self.rgb_3 - unitRGB
        if self.rgb_3 <= zero:
            self.rgb_3 = zero
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Minus(self):
        self.hsv_1 = self.hsv_1 - unitHUE
        if self.hsv_1 <= zero:
            self.hsv_1 = zero
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_2_Minus(self):
        self.hsv_2 = self.hsv_2 - unitSVL
        if self.hsv_2 <= zero:
            self.hsv_2 = zero
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_3_Minus(self):
        self.hsv_3 = self.hsv_3 - unitSVL
        if self.hsv_3 <= zero:
            self.hsv_3 = zero
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSL_1_Minus(self):
        self.hsl_1 = self.hsl_1 - unitHUE
        if self.hsl_1 <= zero:
            self.hsl_1 = zero
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSL_2_Minus(self):
        self.hsl_2 = self.hsl_2 - unitSVL
        if self.hsl_2 <= zero:
            self.hsl_2 = zero
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSL_3_Minus(self):
        self.hsl_3 = self.hsl_3 - unitSVL
        if self.hsl_3 <= zero:
            self.hsl_3 = zero
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_CMYK_1_Minus(self):
        self.cmyk_1 = self.cmyk_1 - unitCMYK
        if self.cmyk_1 <= zero:
            self.cmyk_1 = zero
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_CMYK_2_Minus(self):
        self.cmyk_2 = self.cmyk_2 - unitCMYK
        if self.cmyk_2 <= zero:
            self.cmyk_2 = zero
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_CMYK_3_Minus(self):
        self.cmyk_3 = self.cmyk_3 - unitCMYK
        if self.cmyk_3 <= zero:
            self.cmyk_3 = zero
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_CMYK_4_Minus(self):
        self.cmyk_4 = self.cmyk_4 - unitCMYK
        if self.cmyk_4 <= zero:
            self.cmyk_4 = zero
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()

    def Pigment_AAA_1_Plus(self):
        self.aaa_1 = self.aaa_1 + unitAAA
        if self.aaa_1 >= unit:
            self.aaa_1 = unit
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaAAA)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Plus(self):
        self.rgb_1 = self.rgb_1 + unitRGB
        if self.rgb_1 >= unit:
            self.rgb_1 = unit
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Plus(self):
        self.rgb_2 = self.rgb_2 + unitRGB
        if self.rgb_2 >= unit:
            self.rgb_2 = unit
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Plus(self):
        self.rgb_3 = self.rgb_3 + unitRGB
        if self.rgb_3 >= unit:
            self.rgb_3 = unit
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Plus(self):
        self.hsv_1 = self.hsv_1 + unitHUE
        if self.hsv_1 >= unit:
            self.hsv_1 = unit
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_2_Plus(self):
        self.hsv_2 = self.hsv_2 + unitSVL
        if self.hsv_2 >= unit:
            self.hsv_2 = unit
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_3_Plus(self):
        self.hsv_3 = self.hsv_3 + unitSVL
        if self.hsv_3 >= unit:
            self.hsv_3 = unit
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSL_1_Plus(self):
        self.hsl_1 = self.hsl_1 + unitHUE
        if self.hsl_1 >= unit:
            self.hsl_1 = unit
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_2_Plus(self):
        self.hsl_2 = self.hsl_2 + unitSVL
        if self.hsl_2 >= unit:
            self.hsl_2 = unit
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_3_Plus(self):
        self.hsl_3 = self.hsl_3 + unitSVL
        if self.hsl_3 >= unit:
            self.hsl_3 = unit
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVL)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_CMYK_1_Plus(self):
        self.cmyk_1 = self.cmyk_1 + unitCMYK
        if self.cmyk_1 >= unit:
            self.cmyk_1 = unit
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_2_Plus(self):
        self.cmyk_2 = self.cmyk_2 + unitCMYK
        if self.cmyk_2 >= unit:
            self.cmyk_2 = unit
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_3_Plus(self):
        self.cmyk_3 = self.cmyk_3 + unitCMYK
        if self.cmyk_3 >= unit:
            self.cmyk_3 = unit
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_4_Plus(self):
        self.cmyk_4 = self.cmyk_4 + unitCMYK
        if self.cmyk_4 >= unit:
            self.cmyk_4 = unit
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()

    def Pigment_AAA_1_Slider_Modify(self, SIGNAL_VALUE):
        self.aaa_1 = SIGNAL_VALUE
        send = int(self.aaa_1 * kritaAAA)
        self.layout.aaa_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_1 = SIGNAL_VALUE
        send = int(self.rgb_1 * kritaRGB)
        self.layout.rgb_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_2 = SIGNAL_VALUE
        send = int(self.rgb_2 * kritaRGB)
        self.layout.rgb_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_3 = SIGNAL_VALUE
        send = int(self.rgb_3 * kritaRGB)
        self.layout.rgb_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_1 = SIGNAL_VALUE
        send = int(self.hsv_1 * kritaHUE)
        self.layout.hsv_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" º")
        self.Pigment_Convert_HSV()
    def Pigment_HSV_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_2 = SIGNAL_VALUE
        send = int(self.hsv_2 * kritaSVL)
        self.layout.hsv_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_HSV()
    def Pigment_HSV_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_3 = SIGNAL_VALUE
        send = int(self.hsv_3 * kritaSVL)
        self.layout.hsv_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_HSV()
    def Pigment_HSL_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_1 = SIGNAL_VALUE
        send = int(self.hsl_1 * kritaHUE)
        self.layout.hsl_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" º")
        self.Pigment_Convert_HSL()
    def Pigment_HSL_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_2 = SIGNAL_VALUE
        send = int(self.hsl_2 * kritaSVL)
        self.layout.hsl_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_HSL()
    def Pigment_HSL_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_3 = SIGNAL_VALUE
        send = int(self.hsl_3 * kritaSVL)
        self.layout.hsl_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_HSL()
    def Pigment_CMYK_1_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_1 = SIGNAL_VALUE
        send = int(self.cmyk_1 * kritaCMYK)
        self.layout.cmyk_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_2_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_2 = SIGNAL_VALUE
        send = int(self.cmyk_2 * kritaCMYK)
        self.layout.cmyk_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_3_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_3 = SIGNAL_VALUE
        send = int(self.cmyk_3 * kritaCMYK)
        self.layout.cmyk_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_4_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_4 = SIGNAL_VALUE
        send = int(self.cmyk_4 * kritaCMYK)
        self.layout.cmyk_4_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_CMYK()

    def Pigment_AAA_1_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_2_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_3_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSL_1_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_2_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_3_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_CMYK_1_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_2_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_3_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_4_Slider_Release(self, SIGNAL_RELEASE):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()

    def Pigment_AAA_1_Value_Modify(self):
        self.aaa_1 = self.layout.aaa_1_value.value() / kritaAAA
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.label_percent.setText(str(round(self.aaa_1*100,2))+" %")
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Value_Modify(self):
        self.rgb_1 = self.layout.rgb_1_value.value() / kritaRGB
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.label_percent.setText(str(round(self.rgb_1*100,2))+" %")
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Value_Modify(self):
        self.rgb_2 = self.layout.rgb_2_value.value() / kritaRGB
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.label_percent.setText(str(round(self.rgb_2*100,2))+" %")
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Value_Modify(self):
        self.rgb_3 = self.layout.rgb_3_value.value() / kritaRGB
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.label_percent.setText(str(round(self.rgb_3*100,2))+" %")
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Value_Modify(self):
        self.hsv_1 = self.layout.hsv_1_value.value() / kritaHUE
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.label_percent.setText(str(round(self.hsv_1*100,2))+" º")
        self.Pigment_Convert_HSV()
    def Pigment_HSV_2_Value_Modify(self):
        self.hsv_2 = self.layout.hsv_2_value.value() / kritaSVL
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.label_percent.setText(str(round(self.hsv_2*100,2))+" %")
        self.Pigment_Convert_HSV()
    def Pigment_HSV_3_Value_Modify(self):
        self.hsv_3 = self.layout.hsv_3_value.value() / kritaSVL
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.label_percent.setText(str(round(self.hsv_3*100,2))+" %")
        self.Pigment_Convert_HSV()
    def Pigment_HSL_1_Value_Modify(self):
        self.hsl_1 = self.layout.hsl_1_value.value() / kritaHUE
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.label_percent.setText(str(round(self.hsl_1*100,2))+" º")
        self.Pigment_Convert_HSL()
    def Pigment_HSL_2_Value_Modify(self):
        self.hsl_2 = self.layout.hsl_2_value.value() / kritaSVL
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.label_percent.setText(str(round(self.hsl_2*100,2))+" %")
        self.Pigment_Convert_HSL()
    def Pigment_HSL_3_Value_Modify(self):
        self.hsl_3 = self.layout.hsl_3_value.value() / kritaSVL
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.label_percent.setText(str(round(self.hsl_3*100,2))+" %")
        self.Pigment_Convert_HSL()
    def Pigment_CMYK_1_Value_Modify(self):
        self.cmyk_1 = self.layout.cmyk_1_value.value() / kritaCMYK
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_1*100,2))+" %")
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_2_Value_Modify(self):
        self.cmyk_2 = self.layout.cmyk_2_value.value() / kritaCMYK
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_2*100,2))+" %")
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_3_Value_Modify(self):
        self.cmyk_3 = self.layout.cmyk_3_value.value() / kritaCMYK
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_3*100,2))+" %")
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_4_Value_Modify(self):
        self.cmyk_4 = self.layout.cmyk_4_value.value() / kritaCMYK
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_4*100,2))+" %")
        self.Pigment_Convert_CMYK()

    def Pigment_AAA_1_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_AAA()
    def Pigment_RGB_1_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_2_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_RGB_3_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_RGB()
    def Pigment_HSV_1_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_2_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSV_3_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSV()
    def Pigment_HSL_1_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_2_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_HSL_3_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_HSL()
    def Pigment_CMYK_1_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_2_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_3_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()
    def Pigment_CMYK_4_Value_Release(self):
        self.Pigment_Display_Release(0)
        self.Pigment_Convert_CMYK()

    # Brush Settings ###########################################################
    def Brush_Lock_APPLY(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.view = Krita.instance().activeWindow().activeView()
            self.view.setBrushSize(self.size)
            self.view.setPaintingOpacity(self.opacity)
            self.view.setPaintingFlow(self.flow)
            self.tip_00.Setup(self.size, self.opacity, self.flow)
    def Brush_Lock_SAVE(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.view = Krita.instance().activeWindow().activeView()
            self.size = self.view.brushSize()
            self.opacity = self.view.paintingOpacity()
            self.flow = self.view.paintingFlow()
            self.tip_00.Setup(self.size, self.opacity, self.flow)
            self.Settings_Save()
    def Brush_Lock_CLEAN(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.view = Krita.instance().activeWindow().activeView()
            self.size = size
            self.opacity = opacity
            self.flow = flow
            self.view.setBrushSize(self.size)
            self.view.setPaintingOpacity(self.opacity)
            self.view.setPaintingFlow(self.flow)
            self.tip_00.Setup(size, opacity, flow)
            self.Settings_Save()

    # Palette ##################################################################
    def Color_00_APPLY(self, SIGNAL_CLICKS):
        if self.color_00[0] == "True":
            self.Color_RGB(self.color_00[1], self.color_00[2], self.color_00[3])
            self.Pigment_Display_Release(0)
    def Color_00_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_00 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_00[1]*hexRGB, self.color_00[2]*hexRGB, self.color_00[3]*hexRGB))
        self.layout.cor_00.setStyleSheet(color)
    def Color_00_CLEAN(self, SIGNAL_CLICKS):
        self.color_00 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_00.setStyleSheet(bg_alpha)

    def Color_01_APPLY(self, SIGNAL_CLICKS):
        if self.color_01[0] == "True":
            self.Color_RGB(self.color_01[1], self.color_01[2], self.color_01[3])
            self.Pigment_Display_Release(0)
    def Color_01_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_01 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_01[1]*hexRGB, self.color_01[2]*hexRGB, self.color_01[3]*hexRGB))
        self.layout.cor_01.setStyleSheet(color)
    def Color_01_CLEAN(self, SIGNAL_CLICKS):
        self.color_01 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_01.setStyleSheet(bg_alpha)

    def Color_02_APPLY(self, SIGNAL_CLICKS):
        if self.color_02[0] == "True":
            self.Color_RGB(self.color_02[1], self.color_02[2], self.color_02[3])
            self.Pigment_Display_Release(0)
    def Color_02_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_02 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_02[1]*hexRGB, self.color_02[2]*hexRGB, self.color_02[3]*hexRGB))
        self.layout.cor_02.setStyleSheet(color)
    def Color_02_CLEAN(self, SIGNAL_CLICKS):
        self.color_02 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_02.setStyleSheet(bg_alpha)

    def Color_03_APPLY(self, SIGNAL_CLICKS):
        if self.color_03[0] == "True":
            self.Color_RGB(self.color_03[1], self.color_03[2], self.color_03[3])
            self.Pigment_Display_Release(0)
    def Color_03_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_03 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_03[1]*hexRGB, self.color_03[2]*hexRGB, self.color_03[3]*hexRGB))
        self.layout.cor_03.setStyleSheet(color)
    def Color_03_CLEAN(self, SIGNAL_CLICKS):
        self.color_03 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_03.setStyleSheet(bg_alpha)

    def Color_04_APPLY(self, SIGNAL_CLICKS):
        if self.color_04[0] == "True":
            self.Color_RGB(self.color_04[1], self.color_04[2], self.color_04[3])
            self.Pigment_Display_Release(0)
    def Color_04_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_04 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_04[1]*hexRGB, self.color_04[2]*hexRGB, self.color_04[3]*hexRGB))
        self.layout.cor_04.setStyleSheet(color)
    def Color_04_CLEAN(self, SIGNAL_CLICKS):
        self.color_04 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_04.setStyleSheet(bg_alpha)

    def Color_05_APPLY(self, SIGNAL_CLICKS):
        if self.color_05[0] == "True":
            self.Color_RGB(self.color_05[1], self.color_05[2], self.color_05[3])
            self.Pigment_Display_Release(0)
    def Color_05_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_05 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_05[1]*hexRGB, self.color_05[2]*hexRGB, self.color_05[3]*hexRGB))
        self.layout.cor_05.setStyleSheet(color)
    def Color_05_CLEAN(self, SIGNAL_CLICKS):
        self.color_05 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_05.setStyleSheet(bg_alpha)

    def Color_06_APPLY(self, SIGNAL_CLICKS):
        if self.color_06[0] == "True":
            self.Color_RGB(self.color_06[1], self.color_06[2], self.color_06[3])
            self.Pigment_Display_Release(0)
    def Color_06_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_06 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_06[1]*hexRGB, self.color_06[2]*hexRGB, self.color_06[3]*hexRGB))
        self.layout.cor_06.setStyleSheet(color)
    def Color_06_CLEAN(self, SIGNAL_CLICKS):
        self.color_06 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_06.setStyleSheet(bg_alpha)

    def Color_07_APPLY(self, SIGNAL_CLICKS):
        if self.color_07[0] == "True":
            self.Color_RGB(self.color_07[1], self.color_07[2], self.color_07[3])
            self.Pigment_Display_Release(0)
    def Color_07_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_07 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_07[1]*hexRGB, self.color_07[2]*hexRGB, self.color_07[3]*hexRGB))
        self.layout.cor_07.setStyleSheet(color)
    def Color_07_CLEAN(self, SIGNAL_CLICKS):
        self.color_07 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_07.setStyleSheet(bg_alpha)

    def Color_08_APPLY(self, SIGNAL_CLICKS):
        if self.color_08[0] == "True":
            self.Color_RGB(self.color_08[1], self.color_08[2], self.color_08[3])
            self.Pigment_Display_Release(0)
    def Color_08_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_08 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_08[1]*hexRGB, self.color_08[2]*hexRGB, self.color_08[3]*hexRGB))
        self.layout.cor_08.setStyleSheet(color)
    def Color_08_CLEAN(self, SIGNAL_CLICKS):
        self.color_08 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_08.setStyleSheet(bg_alpha)

    def Color_09_APPLY(self, SIGNAL_CLICKS):
        if self.color_09[0] == "True":
            self.Color_RGB(self.color_09[1], self.color_09[2], self.color_09[3])
            self.Pigment_Display_Release(0)
    def Color_09_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_09 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_09[1]*hexRGB, self.color_09[2]*hexRGB, self.color_09[3]*hexRGB))
        self.layout.cor_09.setStyleSheet(color)
    def Color_09_CLEAN(self, SIGNAL_CLICKS):
        self.color_09 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_09.setStyleSheet(bg_alpha)

    def Color_10_APPLY(self, SIGNAL_CLICKS):
        if self.color_10[0] == "True":
            self.Color_RGB(self.color_10[1], self.color_10[2], self.color_10[3])
            self.Pigment_Display_Release(0)
    def Color_10_SAVE(self, SIGNAL_CLICKS):
        self.Pigment_Display_Colors()
        self.color_10 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_10[1]*hexRGB, self.color_10[2]*hexRGB, self.color_10[3]*hexRGB))
        self.layout.cor_10.setStyleSheet(color)
    def Color_10_CLEAN(self, SIGNAL_CLICKS):
        self.color_10 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_10.setStyleSheet(bg_alpha)

    # Mixer COLOR ##############################################################
    def Mixer_TTS_APPLY(self, SIGNAL_APPLY):
        if self.color_tts[0] == "True":
            self.Color_RGB(self.color_tts[1], self.color_tts[2], self.color_tts[3])
    def Mixer_TTS_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_tts = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ; " % (self.color_tts[1]*hexRGB, self.color_tts[2]*hexRGB, self.color_tts[3]*hexRGB))
        self.layout.tts_l1.setStyleSheet(color)
        self.layout.white.setStyleSheet(bg_white)
        self.layout.grey.setStyleSheet(bg_grey)
        self.layout.black.setStyleSheet(bg_black)
        self.Mixer_Display()
    def Mixer_TTS_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_tts = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.tts_l1.setStyleSheet(bg_alpha)
        self.layout.white.setStyleSheet(bg_alpha)
        self.layout.grey.setStyleSheet(bg_alpha)
        self.layout.black.setStyleSheet(bg_alpha)
        self.layout.tint.setStyleSheet(bg_alpha)
        self.layout.tone.setStyleSheet(bg_alpha)
        self.layout.shade.setStyleSheet(bg_alpha)
        self.Mixer_Display()
        # Correct Values
        self.percentage_tint = 0
        self.percentage_tone = 0
        self.percentage_shade = 0
        self.mixer_tint.Update(self.percentage_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.percentage_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.percentage_shade, self.layout.shade.width())

    def Mixer_RGB_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l1[0] == "True":
            self.Color_RGB(self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3])
    def Mixer_RGB_L1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_rgb_l1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*hexRGB, self.color_rgb_l1[2]*hexRGB, self.color_rgb_l1[3]*hexRGB))
        self.layout.rgb_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l1 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.rgb_l1.setStyleSheet(bg_alpha)
        self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())

    def Mixer_RGB_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r1[0] == "True":
            self.Color_RGB(self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3])
    def Mixer_RGB_R1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_rgb_r1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*hexRGB, self.color_rgb_r1[2]*hexRGB, self.color_rgb_r1[3]*hexRGB))
        self.layout.rgb_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r1 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())

    def Mixer_RGB_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l2[0] == "True":
            self.Color_RGB(self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3])
    def Mixer_RGB_L2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_rgb_l2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*hexRGB, self.color_rgb_l2[2]*hexRGB, self.color_rgb_l2[3]*hexRGB))
        self.layout.rgb_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l2 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.rgb_l2.setStyleSheet(bg_alpha)
        self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())

    def Mixer_RGB_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r2[0] == "True":
            self.Color_RGB(self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3])
    def Mixer_RGB_R2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_rgb_r2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*hexRGB, self.color_rgb_r2[2]*hexRGB, self.color_rgb_r2[3]*hexRGB))
        self.layout.rgb_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r2 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())

    def Mixer_RGB_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l3[0] == "True":
            self.Color_RGB(self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3])
    def Mixer_RGB_L3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_rgb_l3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*hexRGB, self.color_rgb_l3[2]*hexRGB, self.color_rgb_l3[3]*hexRGB))
        self.layout.rgb_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l3 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.rgb_l3.setStyleSheet(bg_alpha)
        self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_RGB_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r3[0] == "True":
            self.Color_RGB(self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3])
    def Mixer_RGB_R3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # Color Math
        self.color_rgb_r3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*hexRGB, self.color_rgb_r3[2]*hexRGB, self.color_rgb_r3[3]*hexRGB))
        self.layout.rgb_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r3 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_HSV_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l1[0] == "True":
            self.Color_RGB(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
    def Mixer_HSV_L1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_l1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, self.Dhsv_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l1[1]*hexRGB, self.color_hsv_l1[2]*hexRGB, self.color_hsv_l1[3]*hexRGB))
        self.layout.hsv_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_l1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r1[0] == "True":
            self.Color_RGB(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
    def Mixer_HSV_R1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_r1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, self.Dhsv_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r1[1]*hexRGB, self.color_hsv_r1[2]*hexRGB, self.color_hsv_r1[3]*hexRGB))
        self.layout.hsv_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l2[0] == "True":
            self.Color_RGB(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
    def Mixer_HSV_L2_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_l2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, self.Dhsv_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l2[1]*hexRGB, self.color_hsv_l2[2]*hexRGB, self.color_hsv_l2[3]*hexRGB))
        self.layout.hsv_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_l2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r2[0] == "True":
            self.Color_RGB(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
    def Mixer_HSV_R2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_r2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, self.Dhsv_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r2[1]*hexRGB, self.color_hsv_r2[2]*hexRGB, self.color_hsv_r2[3]*hexRGB))
        self.layout.hsv_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l3[0] == "True":
            self.Color_RGB(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
    def Mixer_HSV_L3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_l3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, self.Dhsv_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l3[1]*hexRGB, self.color_hsv_l3[2]*hexRGB, self.color_hsv_l3[3]*hexRGB))
        self.layout.hsv_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_l3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSV_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r3[0] == "True":
            self.Color_RGB(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
    def Mixer_HSV_R3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_r3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsv_1, self.Dhsv_2, self.Dhsv_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r3[1]*hexRGB, self.color_hsv_r3[2]*hexRGB, self.color_hsv_r3[3]*hexRGB))
        self.layout.hsv_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSL_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l1[0] == "True":
            self.Color_RGB(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
    def Mixer_HSL_L1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, L]
        self.color_hsl_l1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, self.Dhsl_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l1[1]*hexRGB, self.color_hsl_l1[2]*hexRGB, self.color_hsl_l1[3]*hexRGB))
        self.layout.hsl_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_l1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())

    def Mixer_HSL_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r1[0] == "True":
            self.Color_RGB(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
    def Mixer_HSL_R1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, L]
        self.color_hsl_r1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, self.Dhsl_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r1[1]*hexRGB, self.color_hsl_r1[2]*hexRGB, self.color_hsl_r1[3]*hexRGB))
        self.layout.hsl_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())

    def Mixer_HSL_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l2[0] == "True":
            self.Color_RGB(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
    def Mixer_HSL_L2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, L]
        self.color_hsl_l2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, self.Dhsl_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l2[1]*hexRGB, self.color_hsl_l2[2]*hexRGB, self.color_hsl_l2[3]*hexRGB))
        self.layout.hsl_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_l2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())

    def Mixer_HSL_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r2[0] == "True":
            self.Color_RGB(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
    def Mixer_HSL_R2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, L]
        self.color_hsl_r2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, self.Dhsl_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r2[1]*hexRGB, self.color_hsl_r2[2]*hexRGB, self.color_hsl_r2[3]*hexRGB))
        self.layout.hsl_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())

    def Mixer_HSL_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l3[0] == "True":
            self.Color_RGB(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
    def Mixer_HSL_L3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, L]
        self.color_hsl_l3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, self.Dhsl_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l3[1]*hexRGB, self.color_hsl_l3[2]*hexRGB, self.color_hsl_l3[3]*hexRGB))
        self.layout.hsl_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_l3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_HSL_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r3[0] == "True":
            self.Color_RGB(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
    def Mixer_HSL_R3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, H, S, L]
        self.color_hsl_r3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dhsl_1, self.Dhsl_2, self.Dhsl_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r3[1]*hexRGB, self.color_hsl_r3[2]*hexRGB, self.color_hsl_r3[3]*hexRGB))
        self.layout.hsl_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_CMYK_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l1[0] == "True":
            self.Color_RGB(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3])
    def Mixer_CMYK_L1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, C, M, Y, K]
        self.color_cmyk_l1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l1[1]*hexRGB, self.color_cmyk_l1[2]*hexRGB, self.color_cmyk_l1[3]*hexRGB))
        self.layout.cmyk_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l1 = ["False", 0, 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_l1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())

    def Mixer_CMYK_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r1[0] == "True":
            self.Color_RGB(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3])
    def Mixer_CMYK_R1_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, C, M, Y, K]
        self.color_cmyk_r1 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r1[1]*hexRGB, self.color_cmyk_r1[2]*hexRGB, self.color_cmyk_r1[3]*hexRGB))
        self.layout.cmyk_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r1 = ["False", 0, 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())

    def Mixer_CMYK_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l2[0] == "True":
            self.Color_RGB(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3])
    def Mixer_CMYK_L2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, C, M, Y, K]
        self.color_cmyk_l2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l2[1]*hexRGB, self.color_cmyk_l2[2]*hexRGB, self.color_cmyk_l2[3]*hexRGB))
        self.layout.cmyk_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l2 = ["False", 0, 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_l2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())

    def Mixer_CMYK_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r2[0] == "True":
            self.Color_RGB(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3])
    def Mixer_CMYK_R2_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, C, M, Y, K]
        self.color_cmyk_r2 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r2[1]*hexRGB, self.color_cmyk_r2[2]*hexRGB, self.color_cmyk_r2[3]*hexRGB))
        self.layout.cmyk_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r2 = ["False", 0, 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())

    def Mixer_CMYK_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l3[0] == "True":
            self.Color_RGB(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3])
    def Mixer_CMYK_L3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, C, M, Y, K]
        self.color_cmyk_l3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l3[1]*hexRGB, self.color_cmyk_l3[2]*hexRGB, self.color_cmyk_l3[3]*hexRGB))
        self.layout.cmyk_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l3 = ["False", 0, 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_l3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

    def Mixer_CMYK_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r3[0] == "True":
            self.Color_RGB(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3])
    def Mixer_CMYK_R3_SAVE(self, SIGNAL_SAVE):
        # Display Colors
        self.Pigment_Display_Colors()
        # color = [Bool, R, G, B, C, M, Y, K]
        self.color_cmyk_r3 = ["True", self.Drgb_1, self.Drgb_2, self.Drgb_3, self.Dcmyk_1, self.Dcmyk_2, self.Dcmyk_3, self.Dcmyk_4]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r3[1]*hexRGB, self.color_cmyk_r3[2]*hexRGB, self.color_cmyk_r3[3]*hexRGB))
        self.layout.cmyk_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r3 = ["False", 0, 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

    # Mixer Gradient ###########################################################
    def Mixer_Tint(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_tint = SIGNAL_MIXER_VALUE / (self.layout.tint.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_tts[1]) + (self.percentage_tint * (color_white[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.percentage_tint * (color_white[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.percentage_tint * (color_white[2] - self.color_tts[3])))
        # Send Values
        self.Color_RGB(rgb1, rgb2, rgb3)
    def Mixer_Tone(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_tone = SIGNAL_MIXER_VALUE / (self.layout.tone.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_tts[1]) + (self.percentage_tone * (color_grey[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.percentage_tone * (color_grey[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.percentage_tone * (color_grey[2] - self.color_tts[3])))
        # Send Values
        self.Color_RGB(rgb1, rgb2, rgb3)
    def Mixer_Shade(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_shade = SIGNAL_MIXER_VALUE / (self.layout.shade.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_tts[1]) + (self.percentage_shade * (color_black[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.percentage_shade * (color_black[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.percentage_shade * (color_black[2] - self.color_tts[3])))
        # Send Values
        self.Color_RGB(rgb1, rgb2, rgb3)

    def Mixer_RGB_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_rgb_g1 = SIGNAL_MIXER_VALUE / (self.layout.rgb_g1.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l1[1] + (self.percentage_rgb_g1 * (self.color_rgb_r1[1] - self.color_rgb_l1[1])))
        rgb2 = (self.color_rgb_l1[2] + (self.percentage_rgb_g1 * (self.color_rgb_r1[2] - self.color_rgb_l1[2])))
        rgb3 = (self.color_rgb_l1[3] + (self.percentage_rgb_g1 * (self.color_rgb_r1[3] - self.color_rgb_l1[3])))
        # Send Values
        self.Color_RGB(rgb1, rgb2, rgb3)
    def Mixer_RGB_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_rgb_g2 = SIGNAL_MIXER_VALUE / (self.layout.rgb_g2.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l2[1] + (self.percentage_rgb_g2 * (self.color_rgb_r2[1] - self.color_rgb_l2[1])))
        rgb2 = (self.color_rgb_l2[2] + (self.percentage_rgb_g2 * (self.color_rgb_r2[2] - self.color_rgb_l2[2])))
        rgb3 = (self.color_rgb_l2[3] + (self.percentage_rgb_g2 * (self.color_rgb_r2[3] - self.color_rgb_l2[3])))
        # Send Values
        self.Color_RGB(rgb1, rgb2, rgb3)
    def Mixer_RGB_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_rgb_g3 = SIGNAL_MIXER_VALUE / (self.layout.rgb_g3.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l3[1] + (self.percentage_rgb_g3 * (self.color_rgb_r3[1] - self.color_rgb_l3[1])))
        rgb2 = (self.color_rgb_l3[2] + (self.percentage_rgb_g3 * (self.color_rgb_r3[2] - self.color_rgb_l3[2])))
        rgb3 = (self.color_rgb_l3[3] + (self.percentage_rgb_g3 * (self.color_rgb_r3[3] - self.color_rgb_l3[3])))
        # Send Values
        self.Color_RGB(rgb1, rgb2, rgb3)

    def Mixer_HSV_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsv_g1 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g1.width())
        # Conditions
        cond1 = self.color_hsv_r1[4] - self.color_hsv_l1[4]
        cond2 = (self.color_hsv_l1[4] + 1) - self.color_hsv_r1[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l1[4] + (self.percentage_hsv_g1 * cond1))
        else:
            hue = (self.color_hsv_l1[4] - (self.percentage_hsv_g1 * cond2))
            if hue <= 0:
                hue = hue + 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l1[5] + (self.percentage_hsv_g1 * (self.color_hsv_r1[5] - self.color_hsv_l1[5])))
        hsv3 = (self.color_hsv_l1[6] + (self.percentage_hsv_g1 * (self.color_hsv_r1[6] - self.color_hsv_l1[6])))
        # Send Values
        self.Color_HSV(hsv1, hsv2, hsv3)
    def Mixer_HSV_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsv_g2 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g2.width())
        # Conditions
        cond1 = self.color_hsv_r2[4] - self.color_hsv_l2[4]
        cond2 = (self.color_hsv_l2[4] + 1) - self.color_hsv_r2[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l2[4] + (self.percentage_hsv_g2 * cond1))
        else:
            hue = (self.color_hsv_l2[4] - (self.percentage_hsv_g2 * cond2))
            if hue <= 0:
                hue = hue + 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l2[5] + (self.percentage_hsv_g2 * (self.color_hsv_r2[5] - self.color_hsv_l2[5])))
        hsv3 = (self.color_hsv_l2[6] + (self.percentage_hsv_g2 * (self.color_hsv_r2[6] - self.color_hsv_l2[6])))
        # Send Values
        self.Color_HSV(hsv1, hsv2, hsv3)
    def Mixer_HSV_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsv_g3 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g3.width())
        # Conditions
        cond1 = self.color_hsv_r3[4] - self.color_hsv_l3[4]
        cond2 = (self.color_hsv_l3[4] + 1) - self.color_hsv_r3[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l3[4] + (self.percentage_hsv_g3 * cond1))
        else:
            hue = (self.color_hsv_l3[4] - (self.percentage_hsv_g3 * cond2))
            if hue <= 0:
                hue = hue + 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l3[5] + (self.percentage_hsv_g3 * (self.color_hsv_r3[5] - self.color_hsv_l3[5])))
        hsv3 = (self.color_hsv_l3[6] + (self.percentage_hsv_g3 * (self.color_hsv_r3[6] - self.color_hsv_l3[6])))
        # Send Values
        self.Color_HSV(hsv1, hsv2, hsv3)

    def Mixer_HSL_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsl_g1 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g1.width())
        # Conditions
        cond1 = self.color_hsl_r1[4] - self.color_hsl_l1[4]
        cond2 = (self.color_hsl_l1[4] + 1) - self.color_hsl_r1[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsl_l1[4] + (self.percentage_hsl_g1 * cond1))
        else:
            hue = (self.color_hsl_l1[4] - (self.percentage_hsl_g1 * cond2))
            if hue <= 0:
                hue = hue + 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l1[5] + (self.percentage_hsl_g1 * (self.color_hsl_r1[5] - self.color_hsl_l1[5])))
        hsl3 = (self.color_hsl_l1[6] + (self.percentage_hsl_g1 * (self.color_hsl_r1[6] - self.color_hsl_l1[6])))
        # Send Values
        self.Color_HSL(hsl1, hsl2, hsl3)
    def Mixer_HSL_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsl_g2 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g2.width())
        # Conditions
        cond1 = self.color_hsl_r2[4] - self.color_hsl_l2[4]
        cond2 = (self.color_hsl_l2[4] + 1) - self.color_hsl_r2[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsl_l2[4] + (self.percentage_hsl_g2 * cond1))
        else:
            hue = (self.color_hsl_l2[4] - (self.percentage_hsl_g2 * cond2))
            if hue <= 0:
                hue = hue + 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l2[5] + (self.percentage_hsl_g2 * (self.color_hsl_r2[5] - self.color_hsl_l2[5])))
        hsl3 = (self.color_hsl_l2[6] + (self.percentage_hsl_g2 * (self.color_hsl_r2[6] - self.color_hsl_l2[6])))
        # Send Values
        self.Color_HSL(hsl1, hsl2, hsl3)
    def Mixer_HSL_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsl_g3 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g3.width())
        # Conditions
        cond1 = self.color_hsl_r3[4] - self.color_hsl_l3[4]
        cond2 = (self.color_hsl_l3[4] + 1) - self.color_hsl_r3[4]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsl_l3[4] + (self.percentage_hsl_g3 * cond1))
        else:
            hue = (self.color_hsl_l3[4] - (self.percentage_hsl_g3 * cond2))
            if hue <= 0:
                hue = hue + 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l3[5] + (self.percentage_hsl_g3 * (self.color_hsl_r3[5] - self.color_hsl_l3[5])))
        hsl3 = (self.color_hsl_l3[6] + (self.percentage_hsl_g3 * (self.color_hsl_r3[6] - self.color_hsl_l3[6])))
        # Send Values
        self.Color_HSL(hsl1, hsl2, hsl3)

    def Mixer_CMYK_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_cmyk_g1 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g1.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l1[4] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[4] - self.color_cmyk_l1[4])))
        cmyk2 = (self.color_cmyk_l1[5] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[5] - self.color_cmyk_l1[5])))
        cmyk3 = (self.color_cmyk_l1[6] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[6] - self.color_cmyk_l1[6])))
        cmyk4 = (self.color_cmyk_l1[7] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[7] - self.color_cmyk_l1[7])))
        # Send Values
        self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_CMYK_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_cmyk_g2 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g2.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l2[4] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[4] - self.color_cmyk_l2[4])))
        cmyk2 = (self.color_cmyk_l2[5] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[5] - self.color_cmyk_l2[5])))
        cmyk3 = (self.color_cmyk_l2[6] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[6] - self.color_cmyk_l2[6])))
        cmyk4 = (self.color_cmyk_l2[7] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[7] - self.color_cmyk_l2[7])))
        # Send Values
        self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_CMYK_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_cmyk_g3 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g3.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l3[4] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[4] - self.color_cmyk_l3[4])))
        cmyk2 = (self.color_cmyk_l3[5] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[5] - self.color_cmyk_l3[5])))
        cmyk3 = (self.color_cmyk_l3[6] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[6] - self.color_cmyk_l3[6])))
        cmyk4 = (self.color_cmyk_l3[7] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[7] - self.color_cmyk_l3[7])))
        # Send Values
        self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)

    # Mixer Options
    def Mixer_Display(self):
        # Mixer Tint, Tone, Shade
        if self.color_tts[0] == "True":
            input_tint = [self.color_tts[1], self.color_tts[2], self.color_tts[3]]
            mix_tint = self.RGB_Gradient(self.layout.tint.width(), input_tint, color_white)
            mix_tone = self.RGB_Gradient(self.layout.tone.width(), input_tint, color_grey)
            mix_shade = self.RGB_Gradient(self.layout.shade.width(), input_tint, color_black)
            self.layout.tint.setStyleSheet(mix_tint)
            self.layout.tone.setStyleSheet(mix_tone)
            self.layout.shade.setStyleSheet(mix_shade)
        else:
            self.layout.tint.setStyleSheet(bg_alpha)
            self.layout.tone.setStyleSheet(bg_alpha)
            self.layout.shade.setStyleSheet(bg_alpha)

        # Mixer RGB 1
        if (self.color_rgb_l1[0] == "True" and self.color_rgb_r1[0] == "True"):
            input_rgb_l1 = [self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3]]
            input_rgb_r1 = [self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3]]
            mix_rgb_g1 = self.RGB_Gradient(self.layout.rgb_g1.width(), input_rgb_l1, input_rgb_r1)
            self.layout.rgb_g1.setStyleSheet(mix_rgb_g1)
        else:
            self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Mixer RGB 2
        if (self.color_rgb_l2[0] == "True" and self.color_rgb_r2[0] == "True"):
            input_rgb_l2 = [self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3]]
            input_rgb_r2 = [self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3]]
            mix_rgb_g2 = self.RGB_Gradient(self.layout.rgb_g2.width(), input_rgb_l2, input_rgb_r2)
            self.layout.rgb_g2.setStyleSheet(mix_rgb_g2)
        else:
            self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Mixer RGB 3
        if (self.color_rgb_l3[0] == "True" and self.color_rgb_r3[0] == "True"):
            input_rgb_l3 = [self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3]]
            input_rgb_r3 = [self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3]]
            mix_rgb_g3 = self.RGB_Gradient(self.layout.rgb_g3.width(), input_rgb_l3, input_rgb_r3)
            self.layout.rgb_g3.setStyleSheet(mix_rgb_g3)
        else:
            self.layout.rgb_g3.setStyleSheet(bg_alpha)

        # Mixer HSV 1
        if (self.color_hsv_l1[0] == "True" and self.color_hsv_r1[0] == "True"):
            input_hsv_l1 = [self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3], self.color_hsv_l1[4], self.color_hsv_l1[5], self.color_hsv_l1[6]]
            input_hsv_r1 = [self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3], self.color_hsv_r1[4], self.color_hsv_r1[5], self.color_hsv_r1[6]]
            mix_hsv_g1 = self.HSV_Gradient(self.layout.hsv_g1.width(), input_hsv_l1, input_hsv_r1)
            self.layout.hsv_g1.setStyleSheet(mix_hsv_g1)
        else:
            self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Mixer HSV 2
        if (self.color_hsv_l2[0] == "True" and self.color_hsv_r2[0] == "True"):
            input_hsv_l2 = [self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3], self.color_hsv_l2[4], self.color_hsv_l2[5], self.color_hsv_l2[6]]
            input_hsv_r2 = [self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3], self.color_hsv_r2[4], self.color_hsv_r2[5], self.color_hsv_r2[6]]
            mix_hsv_g2 = self.HSV_Gradient(self.layout.hsv_g2.width(), input_hsv_l2, input_hsv_r2)
            self.layout.hsv_g2.setStyleSheet(mix_hsv_g2)
        else:
            self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Mixer HSV 3
        if (self.color_hsv_l3[0] == "True" and self.color_hsv_r3[0] == "True"):
            input_hsv_l3 = [self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3], self.color_hsv_l3[4], self.color_hsv_l3[5], self.color_hsv_l3[6]]
            input_hsv_r3 = [self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3], self.color_hsv_r3[4], self.color_hsv_r3[5], self.color_hsv_r3[6]]
            mix_hsv_g3 = self.HSV_Gradient(self.layout.hsv_g3.width(), input_hsv_l3, input_hsv_r3)
            self.layout.hsv_g3.setStyleSheet(mix_hsv_g3)
        else:
            self.layout.hsv_g3.setStyleSheet(bg_alpha)

        # Mixer HSL 1
        if (self.color_hsl_l1[0] == "True" and self.color_hsl_r1[0] == "True"):
            input_hsl_l1 = [self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3], self.color_hsl_l1[4], self.color_hsl_l1[5], self.color_hsl_l1[6]]
            input_hsl_r1 = [self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3], self.color_hsl_r1[4], self.color_hsl_r1[5], self.color_hsl_r1[6]]
            mix_hsl_g1 = self.HSL_Gradient(self.layout.hsl_g1.width(), input_hsl_l1, input_hsl_r1)
            self.layout.hsl_g1.setStyleSheet(mix_hsl_g1)
        else:
            self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Mixer HSL 2
        if (self.color_hsl_l2[0] == "True" and self.color_hsl_r2[0] == "True"):
            input_hsl_l2 = [self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3], self.color_hsl_l2[4], self.color_hsl_l2[5], self.color_hsl_l2[6]]
            input_hsl_r2 = [self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3], self.color_hsl_r2[4], self.color_hsl_r2[5], self.color_hsl_r2[6]]
            mix_hsl_g2 = self.HSL_Gradient(self.layout.hsl_g2.width(), input_hsl_l2, input_hsl_r2)
            self.layout.hsl_g2.setStyleSheet(mix_hsl_g2)
        else:
            self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Mixer HSL 3
        if (self.color_hsl_l3[0] == "True" and self.color_hsl_r3[0] == "True"):
            input_hsl_l3 = [self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3], self.color_hsl_l3[4], self.color_hsl_l3[5], self.color_hsl_l3[6]]
            input_hsl_r3 = [self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3], self.color_hsl_r3[4], self.color_hsl_r3[5], self.color_hsl_r3[6]]
            mix_hsl_g3 = self.HSL_Gradient(self.layout.hsl_g3.width(), input_hsl_l3, input_hsl_r3)
            self.layout.hsl_g3.setStyleSheet(mix_hsl_g3)
        else:
            self.layout.hsl_g3.setStyleSheet(bg_alpha)

        # Mixer CMYK 1
        if (self.color_cmyk_l1[0] == "True" and self.color_cmyk_r1[0] == "True"):
            input_cmyk_l1 = [self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4], self.color_cmyk_l1[5], self.color_cmyk_l1[6], self.color_cmyk_l1[7]]
            input_cmyk_r1 = [self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4], self.color_cmyk_r1[5], self.color_cmyk_r1[6], self.color_cmyk_r1[7]]
            mix_cmyk_g1 = self.CMYK_Gradient(self.layout.cmyk_g1.width(), input_cmyk_l1, input_cmyk_r1)
            self.layout.cmyk_g1.setStyleSheet(mix_cmyk_g1)
        else:
            self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Mixer CMYK 2
        if (self.color_cmyk_l2[0] == "True" and self.color_cmyk_r2[0] == "True"):
            input_cmyk_l2 = [self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4], self.color_cmyk_l2[5], self.color_cmyk_l2[6], self.color_cmyk_l2[7]]
            input_cmyk_r2 = [self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4], self.color_cmyk_r2[5], self.color_cmyk_r2[6], self.color_cmyk_r2[7]]
            mix_cmyk_g2 = self.CMYK_Gradient(self.layout.cmyk_g2.width(), input_cmyk_l2, input_cmyk_r2)
            self.layout.cmyk_g2.setStyleSheet(mix_cmyk_g2)
        else:
            self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Mixer CMYK 3
        if (self.color_cmyk_l3[0] == "True" and self.color_cmyk_r3[0] == "True"):
            input_cmyk_l3 = [self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4], self.color_cmyk_l3[5], self.color_cmyk_l3[6], self.color_cmyk_l3[7]]
            input_cmyk_r3 = [self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4], self.color_cmyk_r3[5], self.color_cmyk_r3[6], self.color_cmyk_r3[7]]
            mix_cmyk_g3 = self.CMYK_Gradient(self.layout.cmyk_g3.width(), input_cmyk_l3, input_cmyk_r3)
            self.layout.cmyk_g3.setStyleSheet(mix_cmyk_g3)
        else:
            self.layout.cmyk_g3.setStyleSheet(bg_alpha)

    # Panel ####################################################################
    def Signal_RGB(self, SIGNAL_RGB_VALUE):
        # Correct Out of bound values of UV
        u = SIGNAL_RGB_VALUE[0]
        v = SIGNAL_RGB_VALUE[1]
        if u<-0.8660258:
            u=-0.8660258
        if u>0.8660258:
            u=-0.8660258
        if v<-0.9999999:
            v=-0.9999999
        if v>0.9999999:
            v=0.9999999
        # Apply UV values
        self.rgb_u = round(u, 2)
        self.rgb_v = round(v, 2)
        rgb = self.uvd_to_rgb(self.rgb_u, self.rgb_v, self.rgb_d)
        self.Color_RGB(rgb[0], rgb[1], rgb[2])
    def Signal_HSV(self, SIGNAL_HSV_VALUE):
        self.hsv_2 = round(SIGNAL_HSV_VALUE[0]*kritaSVL, 2)
        self.hsv_3 = round(SIGNAL_HSV_VALUE[1]*kritaSVL, 2)
        self.Color_HSV(self.hsv_1, self.hsv_2/kritaSVL, self.hsv_3/kritaSVL)
    def Signal_HSL(self, SIGNAL_HSL_VALUE):
        self.hsl_2 = round(SIGNAL_HSL_VALUE[0]*kritaSVL, 2)
        self.hsl_3 = round(SIGNAL_HSL_VALUE[1]*kritaSVL, 2)
        self.Color_HSL(self.hsl_1, self.hsl_2/kritaSVL, self.hsl_3/kritaSVL)

    # Style ####################################################################
    def Slider(self, mode, ch):
        # Correct out of Bound values
        rgb_1 = self.rgb_1
        rgb_2 = self.rgb_2
        rgb_3 = self.rgb_3
        if (rgb_1<0 or rgb_1>1):
            rgb_1=round(rgb_1,0)
        if (rgb_2<0 or rgb_2>1):
            rgb_2=round(rgb_2,0)
        if (rgb_3<0 or rgb_3>1):
            rgb_3=round(rgb_3,0)
        # Style Sheets
        if mode == "AAA":
            slider_gradient = str(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255)); \n"
            "border: 1px solid rgba(56, 56, 56, 255);")
        elif mode == "RGB":
            # Gradient on each end
            gradients = [
            [    0*hexRGB, rgb_2*hexRGB, rgb_3*hexRGB,     1*hexRGB, rgb_2*hexRGB, rgb_3*hexRGB],
            [rgb_1*hexRGB,     0*hexRGB, rgb_3*hexRGB, rgb_1*hexRGB,     1*hexRGB, rgb_3*hexRGB],
            [rgb_1*hexRGB, rgb_2*hexRGB,     0*hexRGB, rgb_1*hexRGB, rgb_2*hexRGB,     1*hexRGB]]
            slider_gradient = str(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(%s, %s, %s, 255), stop:1 rgba(%s, %s, %s, 255)); \n" % (gradients[ch][0], gradients[ch][1], gradients[ch][2], gradients[ch][3], gradients[ch][4], gradients[ch][5]) +
            "border: 1px solid rgba(56, 56, 56, 255);")
        elif mode == "HSV":
            # RGB points of representation for the Slider
            rgb_000 = self.hsv_to_rgb(  0/hexHUE, self.hsv_2, self.hsv_3)
            rgb_060 = self.hsv_to_rgb( 60/hexHUE, self.hsv_2, self.hsv_3)
            rgb_120 = self.hsv_to_rgb(120/hexHUE, self.hsv_2, self.hsv_3)
            rgb_180 = self.hsv_to_rgb(180/hexHUE, self.hsv_2, self.hsv_3)
            rgb_240 = self.hsv_to_rgb(240/hexHUE, self.hsv_2, self.hsv_3)
            rgb_300 = self.hsv_to_rgb(300/hexHUE, self.hsv_2, self.hsv_3)
            rgb_360 = self.hsv_to_rgb(360/hexHUE, self.hsv_2, self.hsv_3)
            rgb_h0v = self.hsv_to_rgb(self.hsv_1, 0, self.hsv_3)
            rgb_h1v = self.hsv_to_rgb(self.hsv_1, 1, self.hsv_3)
            rgb_hs0 = self.hsv_to_rgb(self.hsv_1, self.hsv_2, 0)
            rgb_hs1 = self.hsv_to_rgb(self.hsv_1, self.hsv_2, 1)
            # Style Sheet for the Sliders in HSV
            slider_gradient = str(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n " +
            "stop:0.000 rgba(%s, %s, %s, 255), \n " % (rgb_000[0]*hexRGB, rgb_000[1]*hexRGB, rgb_000[2]*hexRGB) +
            "stop:0.166 rgba(%s, %s, %s, 255), \n " % (rgb_060[0]*hexRGB, rgb_060[1]*hexRGB, rgb_060[2]*hexRGB) +
            "stop:0.333 rgba(%s, %s, %s, 255), \n " % (rgb_120[0]*hexRGB, rgb_120[1]*hexRGB, rgb_120[2]*hexRGB) +
            "stop:0.500 rgba(%s, %s, %s, 255), \n " % (rgb_180[0]*hexRGB, rgb_180[1]*hexRGB, rgb_180[2]*hexRGB) +
            "stop:0.666 rgba(%s, %s, %s, 255), \n " % (rgb_240[0]*hexRGB, rgb_240[1]*hexRGB, rgb_240[2]*hexRGB) +
            "stop:0.833 rgba(%s, %s, %s, 255), \n " % (rgb_300[0]*hexRGB, rgb_300[1]*hexRGB, rgb_300[2]*hexRGB) +
            "stop:1.000 rgba(%s, %s, %s, 255));\n " % (rgb_360[0]*hexRGB, rgb_360[1]*hexRGB, rgb_360[2]*hexRGB) +
            "border: 1px solid rgba(56, 56, 56, 255);")
        elif mode == "HSL":
            # RGB points of representation for the Slider
            rgb_000 = self.hsl_to_rgb(  0/hexHUE, self.hsl_2, self.hsl_3)
            rgb_060 = self.hsl_to_rgb( 60/hexHUE, self.hsl_2, self.hsl_3)
            rgb_120 = self.hsl_to_rgb(120/hexHUE, self.hsl_2, self.hsl_3)
            rgb_180 = self.hsl_to_rgb(180/hexHUE, self.hsl_2, self.hsl_3)
            rgb_240 = self.hsl_to_rgb(240/hexHUE, self.hsl_2, self.hsl_3)
            rgb_300 = self.hsl_to_rgb(300/hexHUE, self.hsl_2, self.hsl_3)
            rgb_360 = self.hsl_to_rgb(360/hexHUE, self.hsl_2, self.hsl_3)
            rgb_h0v = self.hsl_to_rgb(self.hsl_1, 0, self.hsl_3)
            rgb_h1v = self.hsl_to_rgb(self.hsl_1, 1, self.hsl_3)
            rgb_hs0 = self.hsl_to_rgb(self.hsl_1, self.hsl_2 , 0)
            rgb_hs5 = self.hsl_to_rgb(self.hsl_1, self.hsl_2, 0.5)
            rgb_hs1 = self.hsl_to_rgb(self.hsl_1, self.hsl_2, 1)
            # Style Sheet for the Sliders in HSL
            slider_gradient = str(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n " +
            "stop:0.000 rgba(%s, %s, %s, 255), \n " % (rgb_000[0]*hexRGB, rgb_000[1]*hexRGB, rgb_000[2]*hexRGB) +
            "stop:0.166 rgba(%s, %s, %s, 255), \n " % (rgb_060[0]*hexRGB, rgb_060[1]*hexRGB, rgb_060[2]*hexRGB) +
            "stop:0.333 rgba(%s, %s, %s, 255), \n " % (rgb_120[0]*hexRGB, rgb_120[1]*hexRGB, rgb_120[2]*hexRGB) +
            "stop:0.500 rgba(%s, %s, %s, 255), \n " % (rgb_180[0]*hexRGB, rgb_180[1]*hexRGB, rgb_180[2]*hexRGB) +
            "stop:0.666 rgba(%s, %s, %s, 255), \n " % (rgb_240[0]*hexRGB, rgb_240[1]*hexRGB, rgb_240[2]*hexRGB) +
            "stop:0.833 rgba(%s, %s, %s, 255), \n " % (rgb_300[0]*hexRGB, rgb_300[1]*hexRGB, rgb_300[2]*hexRGB) +
            "stop:1.000 rgba(%s, %s, %s, 255));\n " % (rgb_360[0]*hexRGB, rgb_360[1]*hexRGB, rgb_360[2]*hexRGB) +
            "border: 1px solid rgba(56, 56, 56, 255);")
        return slider_gradient
    def Percentage(self, count):
        self.count = count
        if self.count == "3":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(255, 255, 255, 255), \n"+
            "stop:0.003 rgba(255, 255, 255, 255), \n"+
            "stop:0.004 rgba(0, 0, 0, 0), \n"+
            "stop:0.331 rgba(0, 0, 0, 0), \n"+
            "stop:0.332 rgba(255, 255, 255, 255), \n"+
            "stop:0.334 rgba(255, 255, 255, 255), \n"+
            "stop:0.335 rgba(0, 0, 0, 0), \n"+
            "stop:0.664 rgba(0, 0, 0, 0), \n"+
            "stop:0.665 rgba(255, 255, 255, 255), \n"+
            "stop:0.667 rgba(255, 255, 255, 255), \n"+
            "stop:0.668 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(0, 0, 0, 0), \n"+
            "stop:0.998 rgba(255, 255, 255, 255), \n"+
            "stop:1.000 rgba(255, 255, 255, 255));"
            )
        elif self.count == "4":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(255, 255, 255, 255), \n"+
            "stop:0.003 rgba(255, 255, 255, 255), \n"+
            "stop:0.004 rgba(0, 0, 0, 0), \n"+
            "stop:0.248 rgba(0, 0, 0, 0), \n"+
            "stop:0.249 rgba(255, 255, 255, 255), \n"+
            "stop:0.251 rgba(255, 255, 255, 255), \n"+
            "stop:0.252 rgba(0, 0, 0, 0), \n"+
            "stop:0.498 rgba(0, 0, 0, 0), \n"+
            "stop:0.499 rgba(255, 255, 255, 255), \n"+
            "stop:0.501 rgba(255, 255, 255, 255), \n"+
            "stop:0.502 rgba(0, 0, 0, 0), \n"+
            "stop:0.748 rgba(0, 0, 0, 0), \n"+
            "stop:0.749 rgba(255, 255, 255, 255), \n"+
            "stop:0.751 rgba(255, 255, 255, 255), \n"+
            "stop:0.752 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(0, 0, 0, 0), \n"+
            "stop:0.998 rgba(255, 255, 255, 255), \n"+
            "stop:1.000 rgba(255, 255, 255, 255));"
            )
        elif self.count == "6":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(255, 255, 255, 255), \n"+
            "stop:0.003 rgba(255, 255, 255, 255), \n"+
            "stop:0.004 rgba(0, 0, 0, 0), \n"+
            "stop:0.164 rgba(0, 0, 0, 0), \n"+
            "stop:0.165 rgba(255, 255, 255, 255), \n"+
            "stop:0.167 rgba(255, 255, 255, 255), \n"+
            "stop:0.168 rgba(0, 0, 0, 0), \n"+
            "stop:0.331 rgba(0, 0, 0, 0), \n"+
            "stop:0.332 rgba(255, 255, 255, 255), \n"+
            "stop:0.334 rgba(255, 255, 255, 255), \n"+
            "stop:0.335 rgba(0, 0, 0, 0), \n"+
            "stop:0.498 rgba(0, 0, 0, 0), \n"+
            "stop:0.499 rgba(255, 255, 255, 255), \n"+
            "stop:0.501 rgba(255, 255, 255, 255), \n"+
            "stop:0.502 rgba(0, 0, 0, 0), \n"+
            "stop:0.664 rgba(0, 0, 0, 0), \n"+
            "stop:0.665 rgba(255, 255, 255, 255), \n"+
            "stop:0.667 rgba(255, 255, 255, 255), \n"+
            "stop:0.668 rgba(0, 0, 0, 0), \n"+
            "stop:0.831 rgba(0, 0, 0, 0), \n"+
            "stop:0.832 rgba(255, 255, 255, 255), \n"+
            "stop:0.834 rgba(255, 255, 255, 255), \n"+
            "stop:0.835 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(0, 0, 0, 0), \n"+
            "stop:0.998 rgba(255, 255, 255, 255), \n"+
            "stop:1.000 rgba(255, 255, 255, 255));"
            )
        elif self.count == "TEN":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(0, 0, 0, 50), \n"+
            "stop:0.099 rgba(0, 0, 0, 50), \n"+
            "stop:0.100 rgba(0, 0, 0, 0), \n"+
            "stop:0.199 rgba(0, 0, 0, 0), \n"+
            "stop:0.200 rgba(0, 0, 0, 50), \n"+
            "stop:0.299 rgba(0, 0, 0, 50), \n"+
            "stop:0.300 rgba(0, 0, 0, 0), \n"+
            "stop:0.399 rgba(0, 0, 0, 0), \n"+
            "stop:0.400 rgba(0, 0, 0, 50), \n"+
            "stop:0.499 rgba(0, 0, 0, 50), \n"+
            "stop:0.500 rgba(0, 0, 0, 0), \n"+
            "stop:0.599 rgba(0, 0, 0, 0), \n"+
            "stop:0.600 rgba(0, 0, 0, 50), \n"+
            "stop:0.699 rgba(0, 0, 0, 50), \n"+
            "stop:0.700 rgba(0, 0, 0, 0), \n"+
            "stop:0.799 rgba(0, 0, 0, 0), \n"+
            "stop:0.800 rgba(0, 0, 0, 50), \n"+
            "stop:0.899 rgba(0, 0, 0, 50), \n"+
            "stop:0.900 rgba(0, 0, 0, 0), \n"+
            "stop:0.999 rgba(0, 0, 0, 0), \n"+
            "stop:1.000 rgba(0, 0, 0, 50));"
            )
        return percentage_style_sheet
    # Gradients
    def RGB_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors ( R G B )
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Conditions
        cond1 = right[0] - left[0]
        cond2 = right[1] - left[1]
        cond3 = right[2] - left[2]
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, color_left[0]*255, color_left[1]*255, color_left[2]*255)
        try:
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # RGB Calculation
            r = round((left[0] + (stop * cond1)),3)
            g = round((left[1] + (stop * cond2)),3)
            b = round((left[2] + (stop * cond3)),3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, color_right[0]*255, color_right[1]*255, color_right[2]*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def HUE_HSV_Gradient(self, r, y, g, c, b, m, rr, hsv_2, hsv_3):
        """ Input: 0-1 """
        # RGB points of representation for the Slider
        rgb_000 = self.hsv_to_rgb(r, hsv_2, hsv_3)
        rgb_060 = self.hsv_to_rgb(y, hsv_2, hsv_3)
        rgb_120 = self.hsv_to_rgb(g, hsv_2, hsv_3)
        rgb_180 = self.hsv_to_rgb(c, hsv_2, hsv_3)
        rgb_240 = self.hsv_to_rgb(b, hsv_2, hsv_3)
        rgb_300 = self.hsv_to_rgb(m, hsv_2, hsv_3)
        rgb_360 = self.hsv_to_rgb(rr, hsv_2, hsv_3)
        # Style Sheet for the Sliders in HSV
        slider_gradient = str(
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n " +
        "stop:0.000 rgba(%s, %s, %s, 255), \n " % (round(rgb_000[0]*hexRGB,3), round(rgb_000[1]*hexRGB,3), round(rgb_000[2]*hexRGB,3)) +
        "stop:0.166 rgba(%s, %s, %s, 255), \n " % (round(rgb_060[0]*hexRGB,3), round(rgb_060[1]*hexRGB,3), round(rgb_060[2]*hexRGB,3)) +
        "stop:0.333 rgba(%s, %s, %s, 255), \n " % (round(rgb_120[0]*hexRGB,3), round(rgb_120[1]*hexRGB,3), round(rgb_120[2]*hexRGB,3)) +
        "stop:0.500 rgba(%s, %s, %s, 255), \n " % (round(rgb_180[0]*hexRGB,3), round(rgb_180[1]*hexRGB,3), round(rgb_180[2]*hexRGB,3)) +
        "stop:0.666 rgba(%s, %s, %s, 255), \n " % (round(rgb_240[0]*hexRGB,3), round(rgb_240[1]*hexRGB,3), round(rgb_240[2]*hexRGB,3)) +
        "stop:0.833 rgba(%s, %s, %s, 255), \n " % (round(rgb_300[0]*hexRGB,3), round(rgb_300[1]*hexRGB,3), round(rgb_300[2]*hexRGB,3)) +
        "stop:1.000 rgba(%s, %s, %s, 255));\n " % (round(rgb_360[0]*hexRGB,3), round(rgb_360[1]*hexRGB,3), round(rgb_360[2]*hexRGB,3)) +
        "border: 1px solid rgba(56, 56, 56, 255);")
        # Return
        return slider_gradient
    def HUE_HSL_Gradient(self, r, y, g, c, b, m, rr, hsl_2, hsl_3):
        """ Input: 0-1 """
        # RGB points of representation for the Slider
        rgb_000 = self.hsl_to_rgb(r, hsl_2, hsl_3)
        rgb_060 = self.hsl_to_rgb(y, hsl_2, hsl_3)
        rgb_120 = self.hsl_to_rgb(g, hsl_2, hsl_3)
        rgb_180 = self.hsl_to_rgb(c, hsl_2, hsl_3)
        rgb_240 = self.hsl_to_rgb(b, hsl_2, hsl_3)
        rgb_300 = self.hsl_to_rgb(m, hsl_2, hsl_3)
        rgb_360 = self.hsl_to_rgb(rr, hsl_2, hsl_3)
        # Style Sheet for the Sliders in HSV
        slider_gradient = str(
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n " +
        "stop:0.000 rgba(%s, %s, %s, 255), \n " % (round(rgb_000[0]*hexRGB,3), round(rgb_000[1]*hexRGB,3), round(rgb_000[2]*hexRGB,3)) +
        "stop:0.166 rgba(%s, %s, %s, 255), \n " % (round(rgb_060[0]*hexRGB,3), round(rgb_060[1]*hexRGB,3), round(rgb_060[2]*hexRGB,3)) +
        "stop:0.333 rgba(%s, %s, %s, 255), \n " % (round(rgb_120[0]*hexRGB,3), round(rgb_120[1]*hexRGB,3), round(rgb_120[2]*hexRGB,3)) +
        "stop:0.500 rgba(%s, %s, %s, 255), \n " % (round(rgb_180[0]*hexRGB,3), round(rgb_180[1]*hexRGB,3), round(rgb_180[2]*hexRGB,3)) +
        "stop:0.666 rgba(%s, %s, %s, 255), \n " % (round(rgb_240[0]*hexRGB,3), round(rgb_240[1]*hexRGB,3), round(rgb_240[2]*hexRGB,3)) +
        "stop:0.833 rgba(%s, %s, %s, 255), \n " % (round(rgb_300[0]*hexRGB,3), round(rgb_300[1]*hexRGB,3), round(rgb_300[2]*hexRGB,3)) +
        "stop:1.000 rgba(%s, %s, %s, 255));\n " % (round(rgb_360[0]*hexRGB,3), round(rgb_360[1]*hexRGB,3), round(rgb_360[2]*hexRGB,3)) +
        "border: 1px solid rgba(56, 56, 56, 255);")
        # Return
        return slider_gradient
    def HSV_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors ( R G B H S V )
        left = [color_left[0], color_left[1], color_left[2], color_left[3], color_left[4], color_left[5]]
        right = [color_right[0], color_right[1], color_right[2], color_right[3], color_right[4], color_right[5]]
        # Conditions
        cond1 = right[3] - left[3]
        cond2 = (left[3] + 1) - right[3]
        cond3 = right[4] - left[4]
        cond4 = right[5] - left[5]
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, color_left[0]*255, color_left[1]*255, color_left[2]*255)
        try:
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # HSV Calculation
            if cond1 <= cond2:
                h = left[3] + (stop * cond1)
            else:
                h = left[3] - (stop * cond2)
                if h <= 0:
                    h = h + 1
            h = h
            s = (left[4] + (stop * cond3))
            v = (left[5] + (stop * cond4))

            # HSV to RGB Conversion
            rgb = self.hsv_to_rgb(h, s, v)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, color_right[0]*255, color_right[1]*255, color_right[2]*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def HSL_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors ( R G B H S L )
        left = [color_left[0], color_left[1], color_left[2], color_left[3], color_left[4], color_left[5]]
        right = [color_right[0], color_right[1], color_right[2], color_right[3], color_right[4], color_right[5]]
        # Conditions
        cond1 = right[3] - left[3]
        cond2 = (left[3] + 1) - right[3]
        cond3 = right[4] - left[4]
        cond4 = right[5] - left[5]
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, color_left[0]*255, color_left[1]*255, color_left[2]*255)
        try:
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # HSV Calculation
            if cond1 <= cond2:
                h = left[3] + (stop * cond1)
            else:
                h = left[3] - (stop * cond2)
                if h <= 0:
                    h = h + 1
            h = h
            s = (left[4] + (stop * cond3))
            l = (left[5] + (stop * cond4))

            # HSL to RGB Conversion
            rgb = self.hsl_to_rgb(h, s, l)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, color_right[0]*255, color_right[1]*255, color_right[2]*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def CMYK_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors ( R G B C Y M K )
        left = [color_left[0], color_left[1], color_left[2], color_left[3], color_left[4], color_left[5], color_left[6]]
        right = [color_right[0], color_right[1], color_right[2], color_right[3], color_right[4], color_right[5], color_right[6]]
        # Conditions
        cond1 = right[3] - left[3]
        cond2 = right[4] - left[4]
        cond3 = right[5] - left[5]
        cond4 = right[6] - left[6]
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, color_left[0]*255, color_left[1]*255, color_left[2]*255)
        try:
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # CMYK Calculation
            cmyk1 = (left[3] + (stop * cond1))
            cmyk2 = (left[4] + (stop * cond2))
            cmyk3 = (left[5] + (stop * cond3))
            cmyk4 = (left[6] + (stop * cond4))
            # CMYK to RGB Conversion
            rgb = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, color_right[0]*255, color_right[1]*255, color_right[2]*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient

    # Widget Events ############################################################
    def enterEvent(self, event):
        # Check Krita Once before edit
        self.Krita_Update()
        # Confirm Panel
        self.Ratio()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.stop()
    def leaveEvent(self, event):
        # Start Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.start()
    def showEvent(self, event):
        self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Pigment_Display_Release(0)
        self.Ratio()
        self.Mixer_Display()
    def resizeEvent(self, event):
        self.Ratio()
    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:
            self.timer.stop()
        # Save Settings
        self.Settings_Save()

    # Settings #################################################################
    def Settings_Load(self):
        # Brush Size Opacity Flow
        tip_sof_string = Krita.instance().readSetting("Pigment.O", "Tip SOF", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        tip_sof_split = tip_sof_string.split(",")
        try:
            self.size = float(tip_sof_split[0])
            self.opacity = float(tip_sof_split[1])
            self.flow = float(tip_sof_split[2])
            self.tip_00.Setup(self.size, self.opacity, self.flow)
        except:
            self.size = size
            self.opacity = opacity
            self.flow = flow
            self.tip_00.Setup(size, opacity, flow)

        # Palette
        color_00_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_00", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_01_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_02_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_03_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_04_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_05_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_05", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_06_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_06", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_07_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_07", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_08_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_08", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_09_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_09", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_10_string = Krita.instance().readSetting("Pigment.O", "Tip_Color_10", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_00_split = color_00_string.split(",")
        color_01_split = color_01_string.split(",")
        color_02_split = color_02_string.split(",")
        color_03_split = color_03_string.split(",")
        color_04_split = color_04_string.split(",")
        color_05_split = color_05_string.split(",")
        color_06_split = color_06_string.split(",")
        color_07_split = color_07_string.split(",")
        color_08_split = color_08_string.split(",")
        color_09_split = color_09_string.split(",")
        color_10_split = color_10_string.split(",")
        if color_00_split[0] == "True":
            self.color_00 = ["True", float(color_00_split[1]), float(color_00_split[2]), float(color_00_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_00[1]*hexRGB, self.color_00[2]*hexRGB, self.color_00[3]*hexRGB))
            self.layout.cor_00.setStyleSheet(color)
        else:
            self.color_00 = ["False", 0, 0, 0]
            self.layout.cor_00.setStyleSheet(bg_alpha)
        if color_01_split[0] == "True":
            self.color_01 = ["True", float(color_01_split[1]), float(color_01_split[2]), float(color_01_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_01[1]*hexRGB, self.color_01[2]*hexRGB, self.color_01[3]*hexRGB))
            self.layout.cor_01.setStyleSheet(color)
        else:
            self.color_01 = ["False", 0, 0, 0]
            self.layout.cor_01.setStyleSheet(bg_alpha)
        if color_02_split[0] == "True":
            self.color_02 = ["True", float(color_02_split[1]), float(color_02_split[2]), float(color_02_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_02[1]*hexRGB, self.color_02[2]*hexRGB, self.color_02[3]*hexRGB))
            self.layout.cor_02.setStyleSheet(color)
        else:
            self.color_02 = ["False", 0, 0, 0]
            self.layout.cor_02.setStyleSheet(bg_alpha)
        if color_03_split[0] == "True":
            self.color_03 = ["True", float(color_03_split[1]), float(color_03_split[2]), float(color_03_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_03[1]*hexRGB, self.color_03[2]*hexRGB, self.color_03[3]*hexRGB))
            self.layout.cor_03.setStyleSheet(color)
        else:
            self.color_03 = ["False", 0, 0, 0]
            self.layout.cor_03.setStyleSheet(bg_alpha)
        if color_04_split[0] == "True":
            self.color_04 = ["True", float(color_04_split[1]), float(color_04_split[2]), float(color_04_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_04[1]*hexRGB, self.color_04[2]*hexRGB, self.color_04[3]*hexRGB))
            self.layout.cor_04.setStyleSheet(color)
        else:
            self.color_04 = ["False", 0, 0, 0]
            self.layout.cor_04.setStyleSheet(bg_alpha)
        if color_05_split[0] == "True":
            self.color_05 = ["True", float(color_05_split[1]), float(color_05_split[2]), float(color_05_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_05[1]*hexRGB, self.color_05[2]*hexRGB, self.color_05[3]*hexRGB))
            self.layout.cor_05.setStyleSheet(color)
        else:
            self.color_05 = ["False", 0, 0, 0]
            self.layout.cor_05.setStyleSheet(bg_alpha)
        if color_06_split[0] == "True":
            self.color_06 = ["True", float(color_06_split[1]), float(color_06_split[2]), float(color_06_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_06[1]*hexRGB, self.color_06[2]*hexRGB, self.color_06[3]*hexRGB))
            self.layout.cor_06.setStyleSheet(color)
        else:
            self.color_06 = ["False", 0, 0, 0]
            self.layout.cor_06.setStyleSheet(bg_alpha)
        if color_07_split[0] == "True":
            self.color_07 = ["True", float(color_07_split[1]), float(color_07_split[2]), float(color_07_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_07[1]*hexRGB, self.color_07[2]*hexRGB, self.color_07[3]*hexRGB))
            self.layout.cor_07.setStyleSheet(color)
        else:
            self.color_07 = ["False", 0, 0, 0]
            self.layout.cor_07.setStyleSheet(bg_alpha)
        if color_08_split[0] == "True":
            self.color_08 = ["True", float(color_08_split[1]), float(color_08_split[2]), float(color_08_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_08[1]*hexRGB, self.color_08[2]*hexRGB, self.color_08[3]*hexRGB))
            self.layout.cor_08.setStyleSheet(color)
        else:
            self.color_08 = ["False", 0, 0, 0]
            self.layout.cor_08.setStyleSheet(bg_alpha)
        if color_09_split[0] == "True":
            self.color_09 = ["True", float(color_09_split[1]), float(color_09_split[2]), float(color_09_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_09[1]*hexRGB, self.color_09[2]*hexRGB, self.color_09[3]*hexRGB))
            self.layout.cor_09.setStyleSheet(color)
        else:
            self.color_09 = ["False", 0, 0, 0]
            self.layout.cor_09.setStyleSheet(bg_alpha)
        if color_10_split[0] == "True":
            self.color_10 = ["True", float(color_10_split[1]), float(color_10_split[2]), float(color_10_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_10[1]*hexRGB, self.color_10[2]*hexRGB, self.color_10[3]*hexRGB))
            self.layout.cor_10.setStyleSheet(color)
        else:
            self.color_10 = ["False", 0, 0, 0]
            self.layout.cor_10.setStyleSheet(bg_alpha)

        # Mixer TTS
        mixer_tts_string = Krita.instance().readSetting("Pigment.O", "Mixer_TTS", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_tts_split = mixer_tts_string.split(",")
        if mixer_tts_split[0] == "True":
            self.color_tts = ["True", float(mixer_tts_split[1]), float(mixer_tts_split[2]), float(mixer_tts_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_tts[1]*hexRGB, self.color_tts[2]*hexRGB, self.color_tts[3]*hexRGB))
            self.layout.tts_l1.setStyleSheet(color)
            self.layout.white.setStyleSheet(bg_white)
            self.layout.grey.setStyleSheet(bg_grey)
            self.layout.black.setStyleSheet(bg_black)
        else:
            self.color_tts = ["False", 0, 0, 0]
            self.layout.tts_l1.setStyleSheet(bg_alpha)
            self.layout.white.setStyleSheet(bg_alpha)
            self.layout.grey.setStyleSheet(bg_alpha)
            self.layout.black.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_tint = 0
        self.percentage_tone = 0
        self.percentage_shade = 0
        self.mixer_tint.Update(self.percentage_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.percentage_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.percentage_shade, self.layout.shade.width())

        # Mixer RGB 1
        mixer_rgb_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_RGB_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_rgb_1_split = mixer_rgb_1_string.split(",")
        if (mixer_rgb_1_split[0] == "True" and mixer_rgb_1_split[4] == "True"):
            # Gradient
            self.color_rgb_l1 = ["True", float(mixer_rgb_1_split[1]), float(mixer_rgb_1_split[2]), float(mixer_rgb_1_split[3])]
            self.color_rgb_r1 = ["True", float(mixer_rgb_1_split[5]), float(mixer_rgb_1_split[6]), float(mixer_rgb_1_split[7])]
            color_rgb_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*hexRGB, self.color_rgb_l1[2]*hexRGB, self.color_rgb_l1[3]*hexRGB))
            color_rgb_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*hexRGB, self.color_rgb_r1[2]*hexRGB, self.color_rgb_r1[3]*hexRGB))
            self.layout.rgb_l1.setStyleSheet(color_rgb_left_1)
            self.layout.rgb_r1.setStyleSheet(color_rgb_right_1)
        elif (mixer_rgb_1_split[0] == "True" and mixer_rgb_1_split[4] != "True"):
            # Color Left
            self.color_rgb_l1 = ["True", float(mixer_rgb_1_split[1]), float(mixer_rgb_1_split[2]), float(mixer_rgb_1_split[3])]
            self.color_rgb_r1 = ["False", 0, 0, 0]
            color_rgb_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*hexRGB, self.color_rgb_l1[2]*hexRGB, self.color_rgb_l1[3]*hexRGB))
            self.layout.rgb_l1.setStyleSheet(color_rgb_left_1)
            self.layout.rgb_r1.setStyleSheet(bg_alpha)
        elif (mixer_rgb_1_split[0] != "True" and mixer_rgb_1_split[4] == "True"):
            # Color Right
            self.color_rgb_l1 = ["False", 0, 0, 0]
            self.color_rgb_r1 = ["True", float(mixer_rgb_1_split[5]), float(mixer_rgb_1_split[6]), float(mixer_rgb_1_split[7])]
            color_rgb_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*hexRGB, self.color_rgb_r1[2]*hexRGB, self.color_rgb_r1[3]*hexRGB))
            self.layout.rgb_l1.setStyleSheet(bg_alpha)
            self.layout.rgb_r1.setStyleSheet(color_rgb_right_1)
        else:
            self.color_rgb_l1 = ["False", 0, 0, 0]
            self.color_rgb_r1 = ["False", 0, 0, 0]
            self.layout.rgb_l1.setStyleSheet(bg_alpha)
            self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.percentage_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
        # Mixer RGB 2
        mixer_rgb_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_RGB_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_rgb_2_split = mixer_rgb_2_string.split(",")
        if (mixer_rgb_2_split[0] == "True" and mixer_rgb_2_split[4] == "True"):
            # Gradient
            self.color_rgb_l2 = ["True", float(mixer_rgb_2_split[1]), float(mixer_rgb_2_split[2]), float(mixer_rgb_2_split[3])]
            self.color_rgb_r2 = ["True", float(mixer_rgb_2_split[5]), float(mixer_rgb_2_split[6]), float(mixer_rgb_2_split[7])]
            color_rgb_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*hexRGB, self.color_rgb_l2[2]*hexRGB, self.color_rgb_l2[3]*hexRGB))
            color_rgb_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*hexRGB, self.color_rgb_r2[2]*hexRGB, self.color_rgb_r2[3]*hexRGB))
            self.layout.rgb_l2.setStyleSheet(color_rgb_left_2)
            self.layout.rgb_r2.setStyleSheet(color_rgb_right_2)
        elif (mixer_rgb_2_split[0] == "True" and mixer_rgb_2_split[4] != "True"):
            # Color Left
            self.color_rgb_l2 = ["True", float(mixer_rgb_2_split[1]), float(mixer_rgb_2_split[2]), float(mixer_rgb_2_split[3])]
            self.color_rgb_r2 = ["False", 0, 0, 0]
            color_rgb_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*hexRGB, self.color_rgb_l2[2]*hexRGB, self.color_rgb_l2[3]*hexRGB))
            self.layout.rgb_l2.setStyleSheet(color_rgb_left_2)
            self.layout.rgb_r2.setStyleSheet(bg_alpha)
        elif (mixer_rgb_2_split[0] != "True" and mixer_rgb_2_split[4] == "True"):
            # Color Right
            self.color_rgb_l2 = ["False", 0, 0, 0]
            self.color_rgb_r2 = ["True", float(mixer_rgb_2_split[5]), float(mixer_rgb_2_split[6]), float(mixer_rgb_2_split[7])]
            color_rgb_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*hexRGB, self.color_rgb_r2[2]*hexRGB, self.color_rgb_r2[3]*hexRGB))
            self.layout.rgb_l2.setStyleSheet(bg_alpha)
            self.layout.rgb_r2.setStyleSheet(color_rgb_right_2)
        else:
            self.color_rgb_l2 = ["False", 0, 0, 0]
            self.color_rgb_r2 = ["False", 0, 0, 0]
            self.layout.rgb_l2.setStyleSheet(bg_alpha)
            self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.percentage_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
        # Mixer RGB 3
        mixer_rgb_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_RGB_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_rgb_3_split = mixer_rgb_3_string.split(",")
        if (mixer_rgb_3_split[0] == "True" and mixer_rgb_3_split[4] == "True"):
            # Gradient
            self.color_rgb_l3 = ["True", float(mixer_rgb_3_split[1]), float(mixer_rgb_3_split[2]), float(mixer_rgb_3_split[3])]
            self.color_rgb_r3 = ["True", float(mixer_rgb_3_split[5]), float(mixer_rgb_3_split[6]), float(mixer_rgb_3_split[7])]
            color_rgb_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*hexRGB, self.color_rgb_l3[2]*hexRGB, self.color_rgb_l3[3]*hexRGB))
            color_rgb_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*hexRGB, self.color_rgb_r3[2]*hexRGB, self.color_rgb_r3[3]*hexRGB))
            self.layout.rgb_l3.setStyleSheet(color_rgb_left_3)
            self.layout.rgb_r3.setStyleSheet(color_rgb_right_3)
        elif (mixer_rgb_3_split[0] == "True" and mixer_rgb_3_split[4] != "True"):
            # Color Left
            self.color_rgb_l3 = ["True", float(mixer_rgb_3_split[1]), float(mixer_rgb_3_split[2]), float(mixer_rgb_3_split[3])]
            self.color_rgb_r3 = ["False", 0, 0, 0]
            color_rgb_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*hexRGB, self.color_rgb_l3[2]*hexRGB, self.color_rgb_l3[3]*hexRGB))
            self.layout.rgb_l3.setStyleSheet(color_rgb_left_3)
            self.layout.rgb_r3.setStyleSheet(bg_alpha)
        elif (mixer_rgb_3_split[0] != "True" and mixer_rgb_3_split[4] == "True"):
            # Color Right
            self.color_rgb_l3 = ["False", 0, 0, 0]
            self.color_rgb_r3 = ["True", float(mixer_rgb_3_split[5]), float(mixer_rgb_3_split[6]), float(mixer_rgb_3_split[7])]
            color_rgb_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*hexRGB, self.color_rgb_r3[2]*hexRGB, self.color_rgb_r3[3]*hexRGB))
            self.layout.rgb_l3.setStyleSheet(bg_alpha)
            self.layout.rgb_r3.setStyleSheet(color_rgb_right_3)
        else:
            self.color_rgb_l3 = ["False", 0, 0, 0]
            self.color_rgb_r3 = ["False", 0, 0, 0]
            self.layout.rgb_l3.setStyleSheet(bg_alpha)
            self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.percentage_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

        # Mixer HSV 1
        mixer_hsv_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSV_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsv_1_split = mixer_hsv_1_string.split(",")
        if (mixer_hsv_1_split[0] == "True" and mixer_hsv_1_split[7] == "True"):
            # Gradient
            self.color_hsv_l1 = ["True", float(mixer_hsv_1_split[1]), float(mixer_hsv_1_split[2]), float(mixer_hsv_1_split[3]), float(mixer_hsv_1_split[4]), float(mixer_hsv_1_split[5]), float(mixer_hsv_1_split[6])]
            self.color_hsv_r1 = ["True", float(mixer_hsv_1_split[8]), float(mixer_hsv_1_split[9]), float(mixer_hsv_1_split[10]), float(mixer_hsv_1_split[11]), float(mixer_hsv_1_split[12]), float(mixer_hsv_1_split[13])]
            color_hsv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l1[1]*hexRGB, self.color_hsv_l1[2]*hexRGB, self.color_hsv_l1[3]*hexRGB))
            color_hsv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r1[1]*hexRGB, self.color_hsv_r1[2]*hexRGB, self.color_hsv_r1[3]*hexRGB))
            self.layout.hsv_l1.setStyleSheet(color_hsv_left_1)
            self.layout.hsv_r1.setStyleSheet(color_hsv_right_1)
        elif (mixer_hsv_1_split[0] == "True" and mixer_hsv_1_split[7] != "True"):
            # Color Left
            self.color_hsv_l1 = ["True", float(mixer_hsv_1_split[1]), float(mixer_hsv_1_split[2]), float(mixer_hsv_1_split[3]), float(mixer_hsv_1_split[4]), float(mixer_hsv_1_split[5]), float(mixer_hsv_1_split[6])]
            self.color_hsv_r1 = ["False", 0, 0, 0, 0, 0, 0]
            color_hsv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l1[1]*hexRGB, self.color_hsv_l1[2]*hexRGB, self.color_hsv_l1[3]*hexRGB))
            self.layout.hsv_l1.setStyleSheet(color_hsv_left_1)
            self.layout.hsv_r1.setStyleSheet(bg_alpha)
        elif (mixer_hsv_1_split[0] != "True" and mixer_hsv_1_split[7] == "True"):
            # Color Right
            self.color_hsv_l1 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsv_r1 = ["True", float(mixer_hsv_1_split[8]), float(mixer_hsv_1_split[9]), float(mixer_hsv_1_split[10]), float(mixer_hsv_1_split[11]), float(mixer_hsv_1_split[12]), float(mixer_hsv_1_split[13])]
            color_hsv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r1[1]*hexRGB, self.color_hsv_r1[2]*hexRGB, self.color_hsv_r1[3]*hexRGB))
            self.layout.hsv_l1.setStyleSheet(bg_alpha)
            self.layout.hsv_r1.setStyleSheet(color_hsv_right_1)
        else:
            self.color_hsv_l1 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsv_r1 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.hsv_l1.setStyleSheet(bg_alpha)
            self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
        # Mixer HSV 2
        mixer_hsv_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSV_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsv_2_split = mixer_hsv_2_string.split(",")
        if (mixer_hsv_2_split[0] == "True" and mixer_hsv_2_split[7] == "True"):
            # Gradient
            self.color_hsv_l2 = ["True", float(mixer_hsv_2_split[1]), float(mixer_hsv_2_split[2]), float(mixer_hsv_2_split[3]), float(mixer_hsv_2_split[4]), float(mixer_hsv_2_split[5]), float(mixer_hsv_2_split[6])]
            self.color_hsv_r2 = ["True", float(mixer_hsv_2_split[8]), float(mixer_hsv_2_split[9]), float(mixer_hsv_2_split[10]), float(mixer_hsv_2_split[11]), float(mixer_hsv_2_split[12]), float(mixer_hsv_2_split[13])]
            color_hsv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l2[1]*hexRGB, self.color_hsv_l2[2]*hexRGB, self.color_hsv_l2[3]*hexRGB))
            color_hsv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r2[1]*hexRGB, self.color_hsv_r2[2]*hexRGB, self.color_hsv_r2[3]*hexRGB))
            self.layout.hsv_l2.setStyleSheet(color_hsv_left_2)
            self.layout.hsv_r2.setStyleSheet(color_hsv_right_2)
        elif (mixer_hsv_2_split[0] == "True" and mixer_hsv_2_split[7] != "True"):
            # Color Left
            self.color_hsv_l2 = ["True", float(mixer_hsv_2_split[1]), float(mixer_hsv_2_split[2]), float(mixer_hsv_2_split[3]), float(mixer_hsv_2_split[4]), float(mixer_hsv_2_split[5]), float(mixer_hsv_2_split[6])]
            self.color_hsv_r2 = ["False", 0, 0, 0, 0, 0, 0]
            color_hsv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l2[1]*hexRGB, self.color_hsv_l2[2]*hexRGB, self.color_hsv_l2[3]*hexRGB))
            self.layout.hsv_l2.setStyleSheet(color_hsv_left_2)
            self.layout.hsv_r2.setStyleSheet(bg_alpha)
        elif (mixer_hsv_2_split[0] != "True" and mixer_hsv_2_split[7] == "True"):
            # Color Right
            self.color_hsv_l2 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsv_r2 = ["True", float(mixer_hsv_2_split[8]), float(mixer_hsv_2_split[9]), float(mixer_hsv_2_split[10]), float(mixer_hsv_2_split[11]), float(mixer_hsv_2_split[12]), float(mixer_hsv_2_split[13])]
            color_hsv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r2[1]*hexRGB, self.color_hsv_r2[2]*hexRGB, self.color_hsv_r2[3]*hexRGB))
            self.layout.hsv_l2.setStyleSheet(bg_alpha)
            self.layout.hsv_r2.setStyleSheet(color_hsv_right_2)
        else:
            self.color_hsv_l2 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsv_r2 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.hsv_l2.setStyleSheet(bg_alpha)
            self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
        # Mixer HSV 3
        mixer_hsv_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSV_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsv_3_split = mixer_hsv_3_string.split(",")
        if (mixer_hsv_3_split[0] == "True" and mixer_hsv_3_split[7] == "True"):
            # Gradient
            self.color_hsv_l3 = ["True", float(mixer_hsv_3_split[1]), float(mixer_hsv_3_split[2]), float(mixer_hsv_3_split[3]), float(mixer_hsv_3_split[4]), float(mixer_hsv_3_split[5]), float(mixer_hsv_3_split[6])]
            self.color_hsv_r3 = ["True", float(mixer_hsv_3_split[8]), float(mixer_hsv_3_split[9]), float(mixer_hsv_3_split[10]), float(mixer_hsv_3_split[11]), float(mixer_hsv_3_split[12]), float(mixer_hsv_3_split[13])]
            color_hsv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l3[1]*hexRGB, self.color_hsv_l3[2]*hexRGB, self.color_hsv_l3[3]*hexRGB))
            color_hsv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r3[1]*hexRGB, self.color_hsv_r3[2]*hexRGB, self.color_hsv_r3[3]*hexRGB))
            self.layout.hsv_l3.setStyleSheet(color_hsv_left_3)
            self.layout.hsv_r3.setStyleSheet(color_hsv_right_3)
        elif (mixer_hsv_3_split[0] == "True" and mixer_hsv_3_split[7] != "True"):
            # Color Left
            self.color_hsv_l3 = ["True", float(mixer_hsv_3_split[1]), float(mixer_hsv_3_split[2]), float(mixer_hsv_3_split[3]), float(mixer_hsv_3_split[4]), float(mixer_hsv_3_split[5]), float(mixer_hsv_3_split[6])]
            self.color_hsv_r3 = ["False", 0, 0, 0, 0, 0, 0]
            color_hsv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_l3[1]*hexRGB, self.color_hsv_l3[2]*hexRGB, self.color_hsv_l3[3]*hexRGB))
            self.layout.hsv_l3.setStyleSheet(color_hsv_left_3)
            self.layout.hsv_r3.setStyleSheet(bg_alpha)
        elif (mixer_hsv_3_split[0] != "True" and mixer_hsv_3_split[7] == "True"):
            # Color Right
            self.color_hsv_l3 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsv_r3 = ["True", float(mixer_hsv_3_split[8]), float(mixer_hsv_3_split[9]), float(mixer_hsv_3_split[10]), float(mixer_hsv_3_split[11]), float(mixer_hsv_3_split[12]), float(mixer_hsv_3_split[13])]
            color_hsv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsv_r3[1]*hexRGB, self.color_hsv_r3[2]*hexRGB, self.color_hsv_r3[3]*hexRGB))
            self.layout.hsv_l3.setStyleSheet(bg_alpha)
            self.layout.hsv_r3.setStyleSheet(color_hsv_right_3)
        else:
            self.color_hsv_l3 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsv_r3 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.hsv_l3.setStyleSheet(bg_alpha)
            self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

        # Mixer HSL 1
        mixer_hsl_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSL_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsl_1_split = mixer_hsl_1_string.split(",")
        if (mixer_hsl_1_split[0] == "True" and mixer_hsl_1_split[7] == "True"):
            # Gradient
            self.color_hsl_l1 = ["True", float(mixer_hsl_1_split[1]), float(mixer_hsl_1_split[2]), float(mixer_hsl_1_split[3]), float(mixer_hsl_1_split[4]), float(mixer_hsl_1_split[5]), float(mixer_hsl_1_split[6])]
            self.color_hsl_r1 = ["True", float(mixer_hsl_1_split[8]), float(mixer_hsl_1_split[9]), float(mixer_hsl_1_split[10]), float(mixer_hsl_1_split[11]), float(mixer_hsl_1_split[12]), float(mixer_hsl_1_split[13])]
            color_hsl_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l1[1]*hexRGB, self.color_hsl_l1[2]*hexRGB, self.color_hsl_l1[3]*hexRGB))
            color_hsl_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r1[1]*hexRGB, self.color_hsl_r1[2]*hexRGB, self.color_hsl_r1[3]*hexRGB))
            self.layout.hsl_l1.setStyleSheet(color_hsl_left_1)
            self.layout.hsl_r1.setStyleSheet(color_hsl_right_1)
        elif (mixer_hsl_1_split[0] == "True" and mixer_hsl_1_split[7] != "True"):
            # Color Left
            self.color_hsl_l1 = ["True", float(mixer_hsl_1_split[1]), float(mixer_hsl_1_split[2]), float(mixer_hsl_1_split[3]), float(mixer_hsl_1_split[4]), float(mixer_hsl_1_split[5]), float(mixer_hsl_1_split[6])]
            self.color_hsl_r1 = ["False", 0, 0, 0, 0, 0, 0]
            color_hsl_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l1[1]*hexRGB, self.color_hsl_l1[2]*hexRGB, self.color_hsl_l1[3]*hexRGB))
            self.layout.hsl_l1.setStyleSheet(color_hsl_left_1)
            self.layout.hsl_r1.setStyleSheet(bg_alpha)
        elif (mixer_hsl_1_split[0] != "True" and mixer_hsl_1_split[7] == "True"):
            # Color Right
            self.color_hsl_l1 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsl_r1 = ["True", float(mixer_hsl_1_split[8]), float(mixer_hsl_1_split[9]), float(mixer_hsl_1_split[10]), float(mixer_hsl_1_split[11]), float(mixer_hsl_1_split[12]), float(mixer_hsl_1_split[13])]
            color_hsl_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r1[1]*hexRGB, self.color_hsl_r1[2]*hexRGB, self.color_hsl_r1[3]*hexRGB))
            self.layout.hsl_l1.setStyleSheet(bg_alpha)
            self.layout.hsl_r1.setStyleSheet(color_hsl_right_1)
        else:
            self.color_hsl_l1 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsl_r1 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.hsl_l1.setStyleSheet(bg_alpha)
            self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
        # Mixer HSL 2
        mixer_hsl_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSL_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsl_2_split = mixer_hsl_2_string.split(",")
        if (mixer_hsl_2_split[0] == "True" and mixer_hsl_2_split[7] == "True"):
            # Gradient
            self.color_hsl_l2 = ["True", float(mixer_hsl_2_split[1]), float(mixer_hsl_2_split[2]), float(mixer_hsl_2_split[3]), float(mixer_hsl_2_split[4]), float(mixer_hsl_2_split[5]), float(mixer_hsl_2_split[6])]
            self.color_hsl_r2 = ["True", float(mixer_hsl_2_split[8]), float(mixer_hsl_2_split[9]), float(mixer_hsl_2_split[10]), float(mixer_hsl_2_split[11]), float(mixer_hsl_2_split[12]), float(mixer_hsl_2_split[13])]
            color_hsl_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l2[1]*hexRGB, self.color_hsl_l2[2]*hexRGB, self.color_hsl_l2[3]*hexRGB))
            color_hsl_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r2[1]*hexRGB, self.color_hsl_r2[2]*hexRGB, self.color_hsl_r2[3]*hexRGB))
            self.layout.hsl_l2.setStyleSheet(color_hsl_left_2)
            self.layout.hsl_r2.setStyleSheet(color_hsl_right_2)
        elif (mixer_hsl_2_split[0] == "True" and mixer_hsl_2_split[7] != "True"):
            # Color Left
            self.color_hsl_l2 = ["True", float(mixer_hsl_2_split[1]), float(mixer_hsl_2_split[2]), float(mixer_hsl_2_split[3]), float(mixer_hsl_2_split[4]), float(mixer_hsl_2_split[5]), float(mixer_hsl_2_split[6])]
            self.color_hsl_r2 = ["False", 0, 0, 0, 0, 0, 0]
            color_hsl_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l2[1]*hexRGB, self.color_hsl_l2[2]*hexRGB, self.color_hsl_l2[3]*hexRGB))
            self.layout.hsl_l2.setStyleSheet(color_hsl_left_2)
            self.layout.hsl_r2.setStyleSheet(bg_alpha)
        elif (mixer_hsl_2_split[0] != "True" and mixer_hsl_2_split[7] == "True"):
            # Color Right
            self.color_hsl_l2 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsl_r2 = ["True", float(mixer_hsl_2_split[8]), float(mixer_hsl_2_split[9]), float(mixer_hsl_2_split[10]), float(mixer_hsl_2_split[11]), float(mixer_hsl_2_split[12]), float(mixer_hsl_2_split[13])]
            color_hsl_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r2[1]*hexRGB, self.color_hsl_r2[2]*hexRGB, self.color_hsl_r2[3]*hexRGB))
            self.layout.hsl_l2.setStyleSheet(bg_alpha)
            self.layout.hsl_r2.setStyleSheet(color_hsl_right_2)
        else:
            self.color_hsl_l2 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsl_r2 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.hsl_l2.setStyleSheet(bg_alpha)
            self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
        # Mixer HSL 3
        mixer_hsl_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSL_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsl_3_split = mixer_hsl_3_string.split(",")
        if (mixer_hsl_3_split[0] == "True" and mixer_hsl_3_split[7] == "True"):
            # Gradient
            self.color_hsl_l3 = ["True", float(mixer_hsl_3_split[1]), float(mixer_hsl_3_split[2]), float(mixer_hsl_3_split[3]), float(mixer_hsl_3_split[4]), float(mixer_hsl_3_split[5]), float(mixer_hsl_3_split[6])]
            self.color_hsl_r3 = ["True", float(mixer_hsl_3_split[8]), float(mixer_hsl_3_split[9]), float(mixer_hsl_3_split[10]), float(mixer_hsl_3_split[11]), float(mixer_hsl_3_split[12]), float(mixer_hsl_3_split[13])]
            color_hsl_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l3[1]*hexRGB, self.color_hsl_l3[2]*hexRGB, self.color_hsl_l3[3]*hexRGB))
            color_hsl_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r3[1]*hexRGB, self.color_hsl_r3[2]*hexRGB, self.color_hsl_r3[3]*hexRGB))
            self.layout.hsl_l3.setStyleSheet(color_hsl_left_3)
            self.layout.hsl_r3.setStyleSheet(color_hsl_right_3)
        elif (mixer_hsl_3_split[0] == "True" and mixer_hsl_3_split[7] != "True"):
            # Color Left
            self.color_hsl_l3 = ["True", float(mixer_hsl_3_split[1]), float(mixer_hsl_3_split[2]), float(mixer_hsl_3_split[3]), float(mixer_hsl_3_split[4]), float(mixer_hsl_3_split[5]), float(mixer_hsl_3_split[6])]
            self.color_hsl_r3 = ["False", 0, 0, 0, 0, 0, 0]
            color_hsl_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_l3[1]*hexRGB, self.color_hsl_l3[2]*hexRGB, self.color_hsl_l3[3]*hexRGB))
            self.layout.hsl_l3.setStyleSheet(color_hsl_left_3)
            self.layout.hsl_r3.setStyleSheet(bg_alpha)
        elif (mixer_hsl_3_split[0] != "True" and mixer_hsl_3_split[7] == "True"):
            # Color Right
            self.color_hsl_l3 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsl_r3 = ["True", float(mixer_hsl_3_split[8]), float(mixer_hsl_3_split[9]), float(mixer_hsl_3_split[10]), float(mixer_hsl_3_split[11]), float(mixer_hsl_3_split[12]), float(mixer_hsl_3_split[13])]
            color_hsl_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_hsl_r3[1]*hexRGB, self.color_hsl_r3[2]*hexRGB, self.color_hsl_r3[3]*hexRGB))
            self.layout.hsl_l3.setStyleSheet(bg_alpha)
            self.layout.hsl_r3.setStyleSheet(color_hsl_right_3)
        else:
            self.color_hsl_l3 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_hsl_r3 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.hsl_l3.setStyleSheet(bg_alpha)
            self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

        # Mixer CMYK 1
        mixer_cmyk_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_CMYK_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_cmyk_1_split = mixer_cmyk_1_string.split(",")
        if (mixer_cmyk_1_split[0] == "True" and mixer_cmyk_1_split[8] == "True"):
            # Gradient
            self.color_cmyk_l1 = ["True", float(mixer_cmyk_1_split[1]), float(mixer_cmyk_1_split[2]), float(mixer_cmyk_1_split[3]), float(mixer_cmyk_1_split[4]), float(mixer_cmyk_1_split[5]), float(mixer_cmyk_1_split[6]), float(mixer_cmyk_1_split[7])]
            self.color_cmyk_r1 = ["True", float(mixer_cmyk_1_split[9]), float(mixer_cmyk_1_split[10]), float(mixer_cmyk_1_split[11]), float(mixer_cmyk_1_split[12]), float(mixer_cmyk_1_split[13]), float(mixer_cmyk_1_split[14]), float(mixer_cmyk_1_split[15])]
            color_cmyk_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l1[1]*hexRGB, self.color_cmyk_l1[2]*hexRGB, self.color_cmyk_l1[3]*hexRGB))
            color_cmyk_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r1[1]*hexRGB, self.color_cmyk_r1[2]*hexRGB, self.color_cmyk_r1[3]*hexRGB))
            self.layout.cmyk_l1.setStyleSheet(color_cmyk_left_1)
            self.layout.cmyk_r1.setStyleSheet(color_cmyk_right_1)
        elif (mixer_cmyk_1_split[0] == "True" and mixer_cmyk_1_split[8] != "True"):
            # Color Left
            self.color_cmyk_l1 = ["True", float(mixer_cmyk_1_split[1]), float(mixer_cmyk_1_split[2]), float(mixer_cmyk_1_split[3]), float(mixer_cmyk_1_split[4]), float(mixer_cmyk_1_split[5]), float(mixer_cmyk_1_split[6]), float(mixer_cmyk_1_split[7])]
            self.color_cmyk_r1 = ["False", 0, 0, 0, 0, 0, 0, 0]
            color_cmyk_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l1[1]*hexRGB, self.color_cmyk_l1[2]*hexRGB, self.color_cmyk_l1[3]*hexRGB))
            self.layout.cmyk_l1.setStyleSheet(color_cmyk_left_1)
            self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        elif (mixer_cmyk_1_split[0] != "True" and mixer_cmyk_1_split[8] == "True"):
            # Color Right
            self.color_cmyk_l1 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.color_cmyk_r1 = ["True", float(mixer_cmyk_1_split[9]), float(mixer_cmyk_1_split[10]), float(mixer_cmyk_1_split[11]), float(mixer_cmyk_1_split[12]), float(mixer_cmyk_1_split[13]), float(mixer_cmyk_1_split[14]), float(mixer_cmyk_1_split[15])]
            color_cmyk_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r1[1]*hexRGB, self.color_cmyk_r1[2]*hexRGB, self.color_cmyk_r1[3]*hexRGB))
            self.layout.cmyk_l1.setStyleSheet(bg_alpha)
            self.layout.cmyk_r1.setStyleSheet(color_cmyk_right_1)
        else:
            self.color_cmyk_l1 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.color_cmyk_r1 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.layout.cmyk_l1.setStyleSheet(bg_alpha)
            self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
        # Mixer CMYK 2
        mixer_cmyk_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_CMYK_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_cmyk_2_split = mixer_cmyk_2_string.split(",")
        if (mixer_cmyk_2_split[0] == "True" and mixer_cmyk_2_split[8] == "True"):
            # Gradient
            self.color_cmyk_l2 = ["True", float(mixer_cmyk_2_split[1]), float(mixer_cmyk_2_split[2]), float(mixer_cmyk_2_split[3]), float(mixer_cmyk_2_split[4]), float(mixer_cmyk_2_split[5]), float(mixer_cmyk_2_split[6]), float(mixer_cmyk_2_split[7])]
            self.color_cmyk_r2 = ["True", float(mixer_cmyk_2_split[9]), float(mixer_cmyk_2_split[10]), float(mixer_cmyk_2_split[11]), float(mixer_cmyk_2_split[12]), float(mixer_cmyk_2_split[13]), float(mixer_cmyk_2_split[14]), float(mixer_cmyk_2_split[15])]
            color_cmyk_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l2[1]*hexRGB, self.color_cmyk_l2[2]*hexRGB, self.color_cmyk_l2[3]*hexRGB))
            color_cmyk_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r2[1]*hexRGB, self.color_cmyk_r2[2]*hexRGB, self.color_cmyk_r2[3]*hexRGB))
            self.layout.cmyk_l2.setStyleSheet(color_cmyk_left_2)
            self.layout.cmyk_r2.setStyleSheet(color_cmyk_right_2)
        elif (mixer_cmyk_2_split[0] == "True" and mixer_cmyk_2_split[8] != "True"):
            # Color Left
            self.color_cmyk_l2 =  ["True", float(mixer_cmyk_2_split[1]), float(mixer_cmyk_2_split[2]), float(mixer_cmyk_2_split[3]), float(mixer_cmyk_2_split[4]), float(mixer_cmyk_2_split[5]), float(mixer_cmyk_2_split[6]), float(mixer_cmyk_2_split[7])]
            self.color_cmyk_r2 = ["False", 0, 0, 0, 0, 0, 0, 0]
            color_cmyk_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l2[1]*hexRGB, self.color_cmyk_l2[2]*hexRGB, self.color_cmyk_l2[3]*hexRGB))
            self.layout.cmyk_l2.setStyleSheet(color_cmyk_left_2)
            self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        elif (mixer_cmyk_2_split[0] != "True" and mixer_cmyk_2_split[8] == "True"):
            # Color Right
            self.color_cmyk_l2 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.color_cmyk_r2 = ["True", float(mixer_cmyk_2_split[9]), float(mixer_cmyk_2_split[10]), float(mixer_cmyk_2_split[11]), float(mixer_cmyk_2_split[12]), float(mixer_cmyk_2_split[13]), float(mixer_cmyk_2_split[14]), float(mixer_cmyk_2_split[15])]
            color_cmyk_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r2[1]*hexRGB, self.color_cmyk_r2[2]*hexRGB, self.color_cmyk_r2[3]*hexRGB))
            self.layout.cmyk_l2.setStyleSheet(bg_alpha)
            self.layout.cmyk_r2.setStyleSheet(color_cmyk_right_2)
        else:
            self.color_cmyk_l2 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.color_cmyk_r2 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.layout.cmyk_l2.setStyleSheet(bg_alpha)
            self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
        # Mixer CMYK 3
        mixer_cmyk_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_CMYK_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_cmyk_3_split = mixer_cmyk_3_string.split(",")
        if (mixer_cmyk_3_split[0] == "True" and mixer_cmyk_3_split[8] == "True"):
            # Gradient
            self.color_cmyk_l3 = ["True", float(mixer_cmyk_3_split[1]), float(mixer_cmyk_3_split[2]), float(mixer_cmyk_3_split[3]), float(mixer_cmyk_3_split[4]), float(mixer_cmyk_3_split[5]), float(mixer_cmyk_3_split[6]), float(mixer_cmyk_3_split[7])]
            self.color_cmyk_r3 = ["True", float(mixer_cmyk_3_split[9]), float(mixer_cmyk_3_split[10]), float(mixer_cmyk_3_split[11]), float(mixer_cmyk_3_split[12]), float(mixer_cmyk_3_split[13]), float(mixer_cmyk_3_split[14]), float(mixer_cmyk_3_split[15])]
            color_cmyk_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l3[1]*hexRGB, self.color_cmyk_l3[2]*hexRGB, self.color_cmyk_l3[3]*hexRGB))
            color_cmyk_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r3[1]*hexRGB, self.color_cmyk_r3[2]*hexRGB, self.color_cmyk_r3[3]*hexRGB))
            self.layout.cmyk_l3.setStyleSheet(color_cmyk_left_3)
            self.layout.cmyk_r3.setStyleSheet(color_cmyk_right_3)
        elif (mixer_cmyk_3_split[0] == "True" and mixer_cmyk_3_split[8] != "True"):
            # Color Left
            self.color_cmyk_l3 =  ["True", float(mixer_cmyk_3_split[1]), float(mixer_cmyk_3_split[2]), float(mixer_cmyk_3_split[3]), float(mixer_cmyk_3_split[4]), float(mixer_cmyk_3_split[5]), float(mixer_cmyk_3_split[6]), float(mixer_cmyk_3_split[7])]
            self.color_cmyk_r3 = ["False", 0, 0, 0, 0, 0, 0, 0]
            color_cmyk_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_l3[1]*hexRGB, self.color_cmyk_l3[2]*hexRGB, self.color_cmyk_l3[3]*hexRGB))
            self.layout.cmyk_l3.setStyleSheet(color_cmyk_left_3)
            self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        elif (mixer_cmyk_3_split[0] != "True" and mixer_cmyk_3_split[8] == "True"):
            # Color Right
            self.color_cmyk_l3 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.color_cmyk_r3 = ["True", float(mixer_cmyk_3_split[9]), float(mixer_cmyk_3_split[10]), float(mixer_cmyk_3_split[11]), float(mixer_cmyk_3_split[12]), float(mixer_cmyk_3_split[13]), float(mixer_cmyk_3_split[14]), float(mixer_cmyk_3_split[15])]
            color_cmyk_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_cmyk_r3[1]*hexRGB, self.color_cmyk_r3[2]*hexRGB, self.color_cmyk_r3[3]*hexRGB))
            self.layout.cmyk_l3.setStyleSheet(bg_alpha)
            self.layout.cmyk_r3.setStyleSheet(color_cmyk_right_3)
        else:
            self.color_cmyk_l3 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.color_cmyk_r3 = ["False", 0, 0, 0, 0, 0, 0, 0]
            self.layout.cmyk_l3.setStyleSheet(bg_alpha)
            self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

        # Active Color
        active_color_string = Krita.instance().readSetting("Pigment.O", "Active_Color", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        active_color_split = active_color_string.split(",")
        try:
            self.rgb_1 = float(active_color_split[0])
            self.rgb_2 = float(active_color_split[1])
            self.rgb_3 = float(active_color_split[2])
            self.rgb_u = float(active_color_split[3])
            self.rgb_v = float(active_color_split[4])
            self.rgb_d = float(active_color_split[5])
            self.d_previous = float(active_color_split[6])
            self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Pigment_Display_Release(0)
        except:
            self.rgb_1 = 0
            self.rgb_2 = 0
            self.rgb_3 = 0
            self.rgb_u = 0
            self.rgb_v = 0
            self.rgb_d = 0
            self.d_previous = 0
            self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Pigment_Display_Release(0)

        # UI
        ui_string = Krita.instance().readSetting("Pigment.O", "UI", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        ui_split = ui_string.split(",")
        if (ui_split[0] == "True" or ui_split[0] == "False"):
            self.layout.aaa.setChecked(eval(ui_split[0]))
            self.layout.rgb.setChecked(eval(ui_split[1]))
            self.layout.hsv.setChecked(eval(ui_split[2]))
            self.layout.hsl.setChecked(eval(ui_split[3]))
            self.layout.cmyk.setChecked(eval(ui_split[4]))
            self.layout.tip.setChecked(eval(ui_split[5]))
            self.layout.tts.setChecked(eval(ui_split[6]))
            self.layout.mixer_selector.setCurrentIndex(int(ui_split[7]))
            self.layout.panel_selector.setCurrentIndex(int(ui_split[8]))
        else:
            self.layout.aaa.setChecked(False)
            self.layout.rgb.setChecked(True)
            self.layout.hsv.setChecked(False)
            self.layout.hsl.setChecked(False)
            self.layout.cmyk.setChecked(False)
            self.layout.tip.setChecked(False)
            self.layout.tts.setChecked(False)
            self.layout.mixer_selector.setCurrentIndex(0)
            self.layout.panel_selector.setCurrentIndex(0)
        self.Menu_Load()
    def Settings_Save(self):
        # Brush Size Opacity Flow
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Current View
            self.view = Krita.instance().activeWindow().activeView()
            self.size = self.view.brushSize()
            self.opacity = self.view.paintingOpacity()
            self.flow = self.view.paintingFlow()
            self.tip_00.Setup(self.size, self.opacity, self.flow)
            # Save Settings
            tip_sof_list = (str(self.view.brushSize()), str(self.view.paintingOpacity()), str(self.view.paintingFlow()))
            tip_sof_string = ','.join(tip_sof_list)
            Krita.instance().writeSetting("Pigment.O", "Tip SOF", tip_sof_string)

        # Palette
        color_00_list = (str(self.color_00[0]), str(self.color_00[1]), str(self.color_00[2]), str(self.color_00[3]))
        color_01_list = (str(self.color_01[0]), str(self.color_01[1]), str(self.color_01[2]), str(self.color_01[3]))
        color_02_list = (str(self.color_02[0]), str(self.color_02[1]), str(self.color_02[2]), str(self.color_02[3]))
        color_03_list = (str(self.color_03[0]), str(self.color_03[1]), str(self.color_03[2]), str(self.color_03[3]))
        color_04_list = (str(self.color_04[0]), str(self.color_04[1]), str(self.color_04[2]), str(self.color_04[3]))
        color_05_list = (str(self.color_05[0]), str(self.color_05[1]), str(self.color_05[2]), str(self.color_05[3]))
        color_06_list = (str(self.color_06[0]), str(self.color_06[1]), str(self.color_06[2]), str(self.color_06[3]))
        color_07_list = (str(self.color_07[0]), str(self.color_07[1]), str(self.color_07[2]), str(self.color_07[3]))
        color_08_list = (str(self.color_08[0]), str(self.color_08[1]), str(self.color_08[2]), str(self.color_08[3]))
        color_09_list = (str(self.color_09[0]), str(self.color_09[1]), str(self.color_09[2]), str(self.color_09[3]))
        color_10_list = (str(self.color_10[0]), str(self.color_10[1]), str(self.color_10[2]), str(self.color_10[3]))
        color_00_string = ','.join(color_00_list)
        color_01_string = ','.join(color_01_list)
        color_02_string = ','.join(color_02_list)
        color_03_string = ','.join(color_03_list)
        color_04_string = ','.join(color_04_list)
        color_05_string = ','.join(color_05_list)
        color_06_string = ','.join(color_06_list)
        color_07_string = ','.join(color_07_list)
        color_08_string = ','.join(color_08_list)
        color_09_string = ','.join(color_09_list)
        color_10_string = ','.join(color_10_list)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_00", color_00_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_01", color_01_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_02", color_02_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_03", color_03_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_04", color_04_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_05", color_05_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_06", color_06_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_07", color_07_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_08", color_08_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_09", color_09_string)
        Krita.instance().writeSetting("Pigment.O", "Tip_Color_10", color_10_string)

        # TTS
        color_tts_list = (str(self.color_tts[0]), str(self.color_tts[1]), str(self.color_tts[2]), str(self.color_tts[3]))
        color_tts_string = ','.join(color_tts_list)
        Krita.instance().writeSetting("Pigment.O", "Mixer_TTS", color_tts_string)

        # Mixer
        mixer_list_rgb_1 = (str(self.color_rgb_l1[0]), str(self.color_rgb_l1[1]), str(self.color_rgb_l1[2]), str(self.color_rgb_l1[3]), str(self.color_rgb_r1[0]),  str(self.color_rgb_r1[1]), str(self.color_rgb_r1[2]), str(self.color_rgb_r1[3]))
        mixer_list_rgb_2 = (str(self.color_rgb_l2[0]), str(self.color_rgb_l2[1]), str(self.color_rgb_l2[2]), str(self.color_rgb_l2[3]), str(self.color_rgb_r2[0]),  str(self.color_rgb_r2[1]), str(self.color_rgb_r2[2]), str(self.color_rgb_r2[3]))
        mixer_list_rgb_3 = (str(self.color_rgb_l3[0]), str(self.color_rgb_l3[1]), str(self.color_rgb_l3[2]), str(self.color_rgb_l3[3]), str(self.color_rgb_r3[0]),  str(self.color_rgb_r3[1]), str(self.color_rgb_r3[2]), str(self.color_rgb_r3[3]))
        mixer_list_hsv_1 = (str(self.color_hsv_l1[0]), str(self.color_hsv_l1[1]), str(self.color_hsv_l1[2]), str(self.color_hsv_l1[3]), str(self.color_hsv_l1[4]), str(self.color_hsv_l1[5]), str(self.color_hsv_l1[6]), str(self.color_hsv_r1[0]), str(self.color_hsv_r1[1]), str(self.color_hsv_r1[2]), str(self.color_hsv_r1[3]), str(self.color_hsv_r1[4]), str(self.color_hsv_r1[5]), str(self.color_hsv_r1[6]))
        mixer_list_hsv_2 = (str(self.color_hsv_l2[0]), str(self.color_hsv_l2[1]), str(self.color_hsv_l2[2]), str(self.color_hsv_l2[3]), str(self.color_hsv_l2[4]), str(self.color_hsv_l2[5]), str(self.color_hsv_l2[6]), str(self.color_hsv_r2[0]), str(self.color_hsv_r2[1]), str(self.color_hsv_r2[2]), str(self.color_hsv_r2[3]), str(self.color_hsv_r2[4]), str(self.color_hsv_r2[5]), str(self.color_hsv_r2[6]))
        mixer_list_hsv_3 = (str(self.color_hsv_l3[0]), str(self.color_hsv_l3[1]), str(self.color_hsv_l3[2]), str(self.color_hsv_l3[3]), str(self.color_hsv_l3[4]), str(self.color_hsv_l3[5]), str(self.color_hsv_l3[6]), str(self.color_hsv_r3[0]), str(self.color_hsv_r3[1]), str(self.color_hsv_r3[2]), str(self.color_hsv_r3[3]), str(self.color_hsv_r3[4]), str(self.color_hsv_r3[5]), str(self.color_hsv_r3[6]))
        mixer_list_hsl_1 = (str(self.color_hsl_l1[0]), str(self.color_hsl_l1[1]), str(self.color_hsl_l1[2]), str(self.color_hsl_l1[3]), str(self.color_hsl_l1[4]), str(self.color_hsl_l1[5]), str(self.color_hsl_l1[6]), str(self.color_hsl_r1[0]), str(self.color_hsl_r1[1]), str(self.color_hsl_r1[2]), str(self.color_hsl_r1[3]), str(self.color_hsl_r1[4]), str(self.color_hsl_r1[5]), str(self.color_hsl_r1[6]))
        mixer_list_hsl_2 = (str(self.color_hsl_l2[0]), str(self.color_hsl_l2[1]), str(self.color_hsl_l2[2]), str(self.color_hsl_l2[3]), str(self.color_hsl_l2[4]), str(self.color_hsl_l2[5]), str(self.color_hsl_l2[6]), str(self.color_hsl_r2[0]), str(self.color_hsl_r2[1]), str(self.color_hsl_r2[2]), str(self.color_hsl_r2[3]), str(self.color_hsl_r2[4]), str(self.color_hsl_r2[5]), str(self.color_hsl_r2[6]))
        mixer_list_hsl_3 = (str(self.color_hsl_l3[0]), str(self.color_hsl_l3[1]), str(self.color_hsl_l3[2]), str(self.color_hsl_l3[3]), str(self.color_hsl_l3[4]), str(self.color_hsl_l3[5]), str(self.color_hsl_l3[6]), str(self.color_hsl_r3[0]), str(self.color_hsl_r3[1]), str(self.color_hsl_r3[2]), str(self.color_hsl_r3[3]), str(self.color_hsl_r3[4]), str(self.color_hsl_r3[5]), str(self.color_hsl_r3[6]))
        mixer_list_cmyk_1 = (str(self.color_cmyk_l1[0]), str(self.color_cmyk_l1[1]), str(self.color_cmyk_l1[2]), str(self.color_cmyk_l1[3]), str(self.color_cmyk_l1[4]), str(self.color_cmyk_l1[5]), str(self.color_cmyk_l1[6]), str(self.color_cmyk_l1[7]), str(self.color_cmyk_r1[0]), str(self.color_cmyk_r1[1]), str(self.color_cmyk_r1[2]), str(self.color_cmyk_r1[3]), str(self.color_cmyk_r1[4]), str(self.color_cmyk_r1[5]), str(self.color_cmyk_r1[6]), str(self.color_cmyk_r1[7]))
        mixer_list_cmyk_2 = (str(self.color_cmyk_l2[0]), str(self.color_cmyk_l2[1]), str(self.color_cmyk_l2[2]), str(self.color_cmyk_l2[3]), str(self.color_cmyk_l2[4]), str(self.color_cmyk_l2[5]), str(self.color_cmyk_l2[6]), str(self.color_cmyk_l2[7]), str(self.color_cmyk_r2[0]), str(self.color_cmyk_r2[1]), str(self.color_cmyk_r2[2]), str(self.color_cmyk_r2[3]), str(self.color_cmyk_r2[4]), str(self.color_cmyk_r2[5]), str(self.color_cmyk_r2[6]), str(self.color_cmyk_r2[7]))
        mixer_list_cmyk_3 = (str(self.color_cmyk_l3[0]), str(self.color_cmyk_l3[1]), str(self.color_cmyk_l3[2]), str(self.color_cmyk_l3[3]), str(self.color_cmyk_l3[4]), str(self.color_cmyk_l3[5]), str(self.color_cmyk_l3[6]), str(self.color_cmyk_l3[7]), str(self.color_cmyk_r3[0]), str(self.color_cmyk_r3[1]), str(self.color_cmyk_r3[2]), str(self.color_cmyk_r3[3]), str(self.color_cmyk_r3[4]), str(self.color_cmyk_r3[5]), str(self.color_cmyk_r3[6]), str(self.color_cmyk_r3[7]))
        mixer_string_rgb_1 = ','.join(mixer_list_rgb_1)
        mixer_string_rgb_2 = ','.join(mixer_list_rgb_2)
        mixer_string_rgb_3 = ','.join(mixer_list_rgb_3)
        mixer_string_hsv_1 = ','.join(mixer_list_hsv_1)
        mixer_string_hsv_2 = ','.join(mixer_list_hsv_2)
        mixer_string_hsv_3 = ','.join(mixer_list_hsv_3)
        mixer_string_hsl_1 = ','.join(mixer_list_hsl_1)
        mixer_string_hsl_2 = ','.join(mixer_list_hsl_2)
        mixer_string_hsl_3 = ','.join(mixer_list_hsl_3)
        mixer_string_cmyk_1 = ','.join(mixer_list_cmyk_1)
        mixer_string_cmyk_2 = ','.join(mixer_list_cmyk_2)
        mixer_string_cmyk_3 = ','.join(mixer_list_cmyk_3)
        Krita.instance().writeSetting("Pigment.O", "Mixer_RGB_1", mixer_string_rgb_1)
        Krita.instance().writeSetting("Pigment.O", "Mixer_RGB_2", mixer_string_rgb_2)
        Krita.instance().writeSetting("Pigment.O", "Mixer_RGB_3", mixer_string_rgb_3)
        Krita.instance().writeSetting("Pigment.O", "Mixer_HSV_1", mixer_string_hsv_1)
        Krita.instance().writeSetting("Pigment.O", "Mixer_HSV_2", mixer_string_hsv_2)
        Krita.instance().writeSetting("Pigment.O", "Mixer_HSV_3", mixer_string_hsv_3)
        Krita.instance().writeSetting("Pigment.O", "Mixer_HSL_1", mixer_string_hsl_1)
        Krita.instance().writeSetting("Pigment.O", "Mixer_HSL_2", mixer_string_hsl_2)
        Krita.instance().writeSetting("Pigment.O", "Mixer_HSL_3", mixer_string_hsl_3)
        Krita.instance().writeSetting("Pigment.O", "Mixer_CMYK_1", mixer_string_cmyk_1)
        Krita.instance().writeSetting("Pigment.O", "Mixer_CMYK_2", mixer_string_cmyk_2)
        Krita.instance().writeSetting("Pigment.O", "Mixer_CMYK_3", mixer_string_cmyk_3)

        # UI
        ui_list = (
            str(self.layout.aaa.isChecked()),
            str(self.layout.rgb.isChecked()),
            str(self.layout.hsv.isChecked()),
            str(self.layout.hsl.isChecked()),
            str(self.layout.cmyk.isChecked()),
            str(self.layout.tip.isChecked()),
            str(self.layout.tts.isChecked()),
            str(self.layout.mixer_selector.currentIndex()),
            str(self.layout.panel_selector.currentIndex())
            )
        ui_string = ','.join(ui_list)
        Krita.instance().writeSetting("Pigment.O", "UI", ui_string)
    def Settings_Save_Color(self):
        # Active Color
        active_color_list = (
            str(self.rgb_1),
            str(self.rgb_2),
            str(self.rgb_3),
            str(self.rgb_u),
            str(self.rgb_v),
            str(self.rgb_d),
            str(self.d_previous),
            )
        active_color_string = ','.join(active_color_list)
        Krita.instance().writeSetting("Pigment.O", "Active_Color", active_color_string)

    # Change the Canvas ########################################################
    def canvasChanged(self, canvas):
        pass
