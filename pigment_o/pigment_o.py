# Import Krita
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
import os.path
import math
from random import randint
# Pigment.O Modules
from .pigment_o_modulo import (
    Channel_Linear,
    Clicks,
    Menu_Event,
    Mixer_Gradient,
    Panel_HSV,
    Panel_HSL,
    Panel_ARD,
    Panel_UVD
    )

# Set Window Title Name
DOCKER_NAME = "Pigment.O"
# Timer
check_timer = 1000  # 1000 = 1 SECOND (Zero will Disable checks)
# SOF Constants
kritaS = 1000
kritaO = 100
kritaF = 100
# Color Space Constants
kritaAAA = 255
kritaRGB = 255
kritaUVD = 255  # U(horizontal) V(Vertical) Diagonal
kritaANG = 360  # Angle
kritaRDL = 255  # Ratio + Diagonal
kritaHUE = 360
kritaSVL = 255  # Saturation + Value + Lightness
kritaCMYK = 255
hexAAA = 100  # DO NOT TOUCH !
hexRGB = 255  # DO NOT TOUCH !
hexHUE = 360  # DO NOT TOUCH !
hexSVL = 100  # DO NOT TOUCH !
hexCMYK = 100  # DO NOT TOUCH !
unitAAA = 1 / kritaAAA
unitRGB = 1 / kritaRGB
unitANG = 1 / kritaANG
unitRDL = 1 / kritaRDL
unitHUE = 1 / kritaHUE
unitSVL = 1 / kritaSVL
unitCMYK = 1 / kritaCMYK
# Numbers
zero = 0
half = 0.5
unit = 1
two = 2
max_val = 16777215
# UI variables
ui_menu = 13
ui_min_1 = 8
ui_max_1 = 15
ui_min_2 = 5
ui_max_2 = 10
ui_min_3 = 19
ui_max_3 = 34
ui_tip = 30
ui_margin = 5
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
bg_white = str("background-color: rgba(255, 255, 255, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_grey = str("background-color: rgba(127, 127, 127, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_black = str("background-color: rgba(0, 0, 0, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_white_border = str("background-color: rgb(255, 255, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_grey_border = str("background-color: rgb(127, 127, 127); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_black_border = str("background-color: rgb(0, 0, 0); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_gradient = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.000 rgba(0, 0, 0, 0), stop:1.000 rgba(0, 0, 0, 50));")
bg_eraser_on = str("background-color: rgba(212, 212, 212, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_eraser_off = str("background-color: rgba(56, 56, 56, 255);")
# D65 - Daylight, sRGB, Adobe-RGB, 2ºC
factorX = 95.047
factorY = 100.000
factorZ = 108.883


# Create Docker
class PigmentODocker(DockWidget):
    """
    Compact Color Picker and Mixer.
    """

    #\\ Initialize the Docker Window ###########################################
    def __init__(self):
        super(PigmentODocker, self).__init__()

        # Construct
        self.User_Interface()
        self.Setup()
        self.Connect()
        self.Palette()
        self.Mixers()
        self.Object()
        self.Style_Sheet()

        # self.Default_Boot()
        self.Settings_Colors()
        self.Settings_UI()

    def User_Interface(self):
        # Widget
        self.window = QWidget()
        self.dir_name = str(os.path.dirname(os.path.realpath(__file__)))
        self.layout = uic.loadUi(self.dir_name + '/pigment_o.ui', self.window)
        self.setWindowTitle(DOCKER_NAME)
        self.setWidget(self.window)
    def Setup(self):
        # SOF Range
        self.layout.sof_1_value.setMinimum(0)
        self.layout.sof_2_value.setMinimum(0)
        self.layout.sof_3_value.setMinimum(0)
        self.layout.sof_1_value.setMaximum(kritaS)
        self.layout.sof_2_value.setMaximum(kritaO)
        self.layout.sof_3_value.setMaximum(kritaF)
        # Channels Range
        self.layout.aaa_1_value.setMinimum(0)
        self.layout.rgb_1_value.setMinimum(0)
        self.layout.rgb_2_value.setMinimum(0)
        self.layout.rgb_3_value.setMinimum(0)
        self.layout.ard_1_value.setMinimum(0)
        self.layout.ard_2_value.setMinimum(0)
        self.layout.ard_3_value.setMinimum(0)
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
        self.layout.ard_1_value.setMaximum(kritaANG)
        self.layout.ard_2_value.setMaximum(kritaRDL)
        self.layout.ard_3_value.setMaximum(kritaRDL)
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
        # Module SOF
        self.sof_1_slider = Channel_Linear(self.layout.sof_1_slider)
        self.sof_2_slider = Channel_Linear(self.layout.sof_2_slider)
        self.sof_3_slider = Channel_Linear(self.layout.sof_3_slider)
        self.sof_1_slider.Setup("NEU")
        self.sof_2_slider.Setup("NEU")
        self.sof_3_slider.Setup("NEU")
        # Module Channel
        self.aaa_1_slider = Channel_Linear(self.layout.aaa_1_slider)
        self.aaa_1_slider.Setup("AAA")
        self.rgb_1_slider = Channel_Linear(self.layout.rgb_1_slider)
        self.rgb_2_slider = Channel_Linear(self.layout.rgb_2_slider)
        self.rgb_3_slider = Channel_Linear(self.layout.rgb_3_slider)
        self.rgb_1_slider.Setup("RGB")
        self.rgb_2_slider.Setup("RGB")
        self.rgb_3_slider.Setup("RGB")
        self.ard_1_slider = Channel_Linear(self.layout.ard_1_slider)
        self.ard_2_slider = Channel_Linear(self.layout.ard_2_slider)
        self.ard_3_slider = Channel_Linear(self.layout.ard_3_slider)
        self.ard_1_slider.Setup("ANG")
        self.ard_2_slider.Setup("RDL")
        self.ard_3_slider.Setup("DEP")
        self.hsv_1_slider = Channel_Linear(self.layout.hsv_1_slider)
        self.hsv_2_slider = Channel_Linear(self.layout.hsv_2_slider)
        self.hsv_3_slider = Channel_Linear(self.layout.hsv_3_slider)
        self.hsv_1_slider.Setup("HUE")
        self.hsv_2_slider.Setup("SVL")
        self.hsv_3_slider.Setup("SVL")
        self.hsl_1_slider = Channel_Linear(self.layout.hsl_1_slider)
        self.hsl_2_slider = Channel_Linear(self.layout.hsl_2_slider)
        self.hsl_3_slider = Channel_Linear(self.layout.hsl_3_slider)
        self.hsl_1_slider.Setup("HUE")
        self.hsl_2_slider.Setup("SVL")
        self.hsl_3_slider.Setup("SVL")
        self.cmyk_1_slider = Channel_Linear(self.layout.cmyk_1_slider)
        self.cmyk_2_slider = Channel_Linear(self.layout.cmyk_2_slider)
        self.cmyk_3_slider = Channel_Linear(self.layout.cmyk_3_slider)
        self.cmyk_4_slider = Channel_Linear(self.layout.cmyk_4_slider)
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
            self.layout.check.setCheckState(1)
            self.Krita_TIMER()
        else:
            self.layout.check.setCheckState(0)
    def Connect(self):
        # UI Display Options
        self.layout.check.stateChanged.connect(self.Krita_TIMER)
        self.layout.option.toggled.connect(lambda: self.Menu_Options("SAVE"))
        self.layout.aaa.toggled.connect(lambda: self.Menu_AAA("SAVE"))
        self.layout.rgb.toggled.connect(lambda: self.Menu_RGB("SAVE"))
        self.layout.ard.toggled.connect(lambda: self.Menu_ARD("SAVE"))
        self.layout.hsv.toggled.connect(lambda: self.Menu_HSV("SAVE"))
        self.layout.hsl.toggled.connect(lambda: self.Menu_HSL("SAVE"))
        self.layout.cmyk.toggled.connect(lambda: self.Menu_CMYK("SAVE"))
        self.layout.tip.toggled.connect(lambda: self.Menu_TIP("SAVE"))
        self.layout.tts.toggled.connect(lambda: self.Menu_TTS("SAVE"))
        self.layout.mix.currentTextChanged.connect(lambda: self.Menu_MIX("SAVE"))
        self.layout.panel.currentTextChanged.connect(lambda: self.Menu_PANEL("SAVE"))
        self.layout.obj.currentTextChanged.connect(lambda: self.Menu_OBJ("SAVE"))
        self.layout.sof_sliders.toggled.connect(self.Menu_SOF) # No SAVE
        self.layout.gray_sliders.toggled.connect(self.Menu_GRAY) # No SAVE
        self.layout.gray_panels.toggled.connect(self.Menu_GRAY) # No SAVE

        # SIZE
        self.layout.sof_1_label.clicked.connect(lambda: self.SOF_1_APPLY(self.lock_size))
        self.sof_1_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_1_Slider_Modify)
        self.layout.sof_1_value.valueChanged.connect(self.Pigment_SOF_1_Value_Modify)
        # OPACITY
        self.layout.sof_2_label.clicked.connect(lambda: self.SOF_2_APPLY(self.lock_opacity))
        self.sof_2_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_2_Slider_Modify)
        self.layout.sof_2_value.valueChanged.connect(self.Pigment_SOF_2_Value_Modify)
        # FLOW
        self.layout.sof_3_label.clicked.connect(lambda: self.SOF_3_APPLY(self.lock_flow))
        self.sof_3_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_3_Slider_Modify)
        self.layout.sof_3_value.valueChanged.connect(self.Pigment_SOF_3_Value_Modify)

        # Channel ALPHA
        self.layout.aaa_1_label.clicked.connect(self.Pigment_AAA_1_Half)
        self.layout.aaa_1_minus.clicked.connect(self.Pigment_AAA_1_Minus)
        self.layout.aaa_1_plus.clicked.connect(self.Pigment_AAA_1_Plus)
        self.aaa_1_slider.SIGNAL_VALUE.connect(self.Pigment_AAA_1_Slider_Modify)
        self.aaa_1_slider.SIGNAL_RELEASE.connect(self.Pigment_AAA_1_Slider_Release)
        self.aaa_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.aaa_1_value.valueChanged.connect(self.Pigment_AAA_1_Value_Modify)
        self.layout.aaa_1_value.editingFinished.connect(self.Pigment_AAA_1_Value_Release)

        # Channel RED
        self.layout.rgb_1_label.clicked.connect(self.Pigment_RGB_1_Half)
        self.layout.rgb_1_minus.clicked.connect(self.Pigment_RGB_1_Minus)
        self.layout.rgb_1_plus.clicked.connect(self.Pigment_RGB_1_Plus)
        self.rgb_1_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_1_Slider_Modify)
        self.rgb_1_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_1_Slider_Release)
        self.rgb_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.rgb_1_value.valueChanged.connect(self.Pigment_RGB_1_Value_Modify)
        self.layout.rgb_1_value.editingFinished.connect(self.Pigment_RGB_1_Value_Release)
        # Channel GREEN
        self.layout.rgb_2_label.clicked.connect(self.Pigment_RGB_2_Half)
        self.layout.rgb_2_minus.clicked.connect(self.Pigment_RGB_2_Minus)
        self.layout.rgb_2_plus.clicked.connect(self.Pigment_RGB_2_Plus)
        self.rgb_2_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_2_Slider_Modify)
        self.rgb_2_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_2_Slider_Release)
        self.rgb_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.rgb_2_value.valueChanged.connect(self.Pigment_RGB_2_Value_Modify)
        self.layout.rgb_2_value.editingFinished.connect(self.Pigment_RGB_2_Value_Release)
        # Channel BLUE
        self.layout.rgb_3_label.clicked.connect(self.Pigment_RGB_3_Half)
        self.layout.rgb_3_minus.clicked.connect(self.Pigment_RGB_3_Minus)
        self.layout.rgb_3_plus.clicked.connect(self.Pigment_RGB_3_Plus)
        self.rgb_3_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_3_Slider_Modify)
        self.rgb_3_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_3_Slider_Release)
        self.rgb_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.rgb_3_value.valueChanged.connect(self.Pigment_RGB_3_Value_Modify)
        self.layout.rgb_3_value.editingFinished.connect(self.Pigment_RGB_3_Value_Release)

        # Channel ANGLE
        self.layout.ard_1_label.clicked.connect(self.Pigment_ARD_1_Half)
        self.layout.ard_1_minus.clicked.connect(self.Pigment_ARD_1_Minus)
        self.layout.ard_1_plus.clicked.connect(self.Pigment_ARD_1_Plus)
        self.ard_1_slider.SIGNAL_VALUE.connect(self.Pigment_ARD_1_Slider_Modify)
        self.ard_1_slider.SIGNAL_RELEASE.connect(self.Pigment_ARD_1_Slider_Release)
        self.ard_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ard_1_value.valueChanged.connect(self.Pigment_ARD_1_Value_Modify)
        self.layout.ard_1_value.editingFinished.connect(self.Pigment_ARD_1_Value_Release)
        # Channel RATIO
        self.layout.ard_2_label.clicked.connect(self.Pigment_ARD_2_Half)
        self.layout.ard_2_minus.clicked.connect(self.Pigment_ARD_2_Minus)
        self.layout.ard_2_plus.clicked.connect(self.Pigment_ARD_2_Plus)
        self.ard_2_slider.SIGNAL_VALUE.connect(self.Pigment_ARD_2_Slider_Modify)
        self.ard_2_slider.SIGNAL_RELEASE.connect(self.Pigment_ARD_2_Slider_Release)
        self.ard_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ard_2_value.valueChanged.connect(self.Pigment_ARD_2_Value_Modify)
        self.layout.ard_2_value.editingFinished.connect(self.Pigment_ARD_2_Value_Release)
        # Channel DIAGONAL
        self.layout.ard_3_label.clicked.connect(self.Pigment_ARD_3_Half)
        self.layout.ard_3_minus.clicked.connect(self.Pigment_ARD_3_Minus)
        self.layout.ard_3_plus.clicked.connect(self.Pigment_ARD_3_Plus)
        self.ard_3_slider.SIGNAL_VALUE.connect(self.Pigment_ARD_3_Slider_Modify)
        self.ard_3_slider.SIGNAL_RELEASE.connect(self.Pigment_ARD_3_Slider_Release)
        self.ard_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ard_3_value.valueChanged.connect(self.Pigment_ARD_3_Value_Modify)
        self.layout.ard_3_value.editingFinished.connect(self.Pigment_ARD_3_Value_Release)

        # Channel HUE
        self.layout.hsv_1_label.clicked.connect(self.Pigment_HSV_1_Half)
        self.layout.hsv_1_minus.clicked.connect(self.Pigment_HSV_1_Minus)
        self.layout.hsv_1_plus.clicked.connect(self.Pigment_HSV_1_Plus)
        self.hsv_1_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_1_Slider_Modify)
        self.hsv_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_1_Slider_Release)
        self.hsv_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsv_1_value.valueChanged.connect(self.Pigment_HSV_1_Value_Modify)
        self.layout.hsv_1_value.editingFinished.connect(self.Pigment_HSV_1_Value_Release)
        # Channel SATURATION
        self.layout.hsv_2_label.clicked.connect(self.Pigment_HSV_2_Half)
        self.layout.hsv_2_minus.clicked.connect(self.Pigment_HSV_2_Minus)
        self.layout.hsv_2_plus.clicked.connect(self.Pigment_HSV_2_Plus)
        self.hsv_2_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_2_Slider_Modify)
        self.hsv_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_2_Slider_Release)
        self.hsv_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsv_2_value.valueChanged.connect(self.Pigment_HSV_2_Value_Modify)
        self.layout.hsv_2_value.editingFinished.connect(self.Pigment_HSV_2_Value_Release)
        # Channel VALUE
        self.layout.hsv_3_label.clicked.connect(self.Pigment_HSV_3_Half)
        self.layout.hsv_3_minus.clicked.connect(self.Pigment_HSV_3_Minus)
        self.layout.hsv_3_plus.clicked.connect(self.Pigment_HSV_3_Plus)
        self.hsv_3_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_3_Slider_Modify)
        self.hsv_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_3_Slider_Release)
        self.hsv_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsv_3_value.valueChanged.connect(self.Pigment_HSV_3_Value_Modify)
        self.layout.hsv_3_value.editingFinished.connect(self.Pigment_HSV_3_Value_Release)

        # Channel HUE
        self.layout.hsl_1_label.clicked.connect(self.Pigment_HSL_1_Half)
        self.layout.hsl_1_minus.clicked.connect(self.Pigment_HSL_1_Minus)
        self.layout.hsl_1_plus.clicked.connect(self.Pigment_HSL_1_Plus)
        self.hsl_1_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_1_Slider_Modify)
        self.hsl_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_1_Slider_Release)
        self.hsl_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsl_1_value.valueChanged.connect(self.Pigment_HSL_1_Value_Modify)
        self.layout.hsl_1_value.editingFinished.connect(self.Pigment_HSL_1_Value_Release)
        # Channel SATURATION
        self.layout.hsl_2_label.clicked.connect(self.Pigment_HSL_2_Half)
        self.layout.hsl_2_minus.clicked.connect(self.Pigment_HSL_2_Minus)
        self.layout.hsl_2_plus.clicked.connect(self.Pigment_HSL_2_Plus)
        self.hsl_2_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_2_Slider_Modify)
        self.hsl_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_2_Slider_Release)
        self.hsl_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsl_2_value.valueChanged.connect(self.Pigment_HSL_2_Value_Modify)
        self.layout.hsl_2_value.editingFinished.connect(self.Pigment_HSL_2_Value_Release)
        # Channel LIGHTNESS
        self.layout.hsl_3_label.clicked.connect(self.Pigment_HSL_3_Half)
        self.layout.hsl_3_minus.clicked.connect(self.Pigment_HSL_3_Minus)
        self.layout.hsl_3_plus.clicked.connect(self.Pigment_HSL_3_Plus)
        self.hsl_3_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_3_Slider_Modify)
        self.hsl_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_3_Slider_Release)
        self.hsl_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsl_3_value.valueChanged.connect(self.Pigment_HSL_3_Value_Modify)
        self.layout.hsl_3_value.editingFinished.connect(self.Pigment_HSL_3_Value_Release)

        # Channel CYAN
        self.layout.cmyk_1_label.clicked.connect(self.Pigment_CMYK_1_Half)
        self.layout.cmyk_1_minus.clicked.connect(self.Pigment_CMYK_1_Minus)
        self.layout.cmyk_1_plus.clicked.connect(self.Pigment_CMYK_1_Plus)
        self.cmyk_1_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_1_Slider_Modify)
        self.cmyk_1_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_1_Slider_Release)
        self.cmyk_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_1_value.valueChanged.connect(self.Pigment_CMYK_1_Value_Modify)
        self.layout.cmyk_1_value.editingFinished.connect(self.Pigment_CMYK_1_Value_Release)
        # Channel MAGENTA
        self.layout.cmyk_2_label.clicked.connect(self.Pigment_CMYK_2_Half)
        self.layout.cmyk_2_minus.clicked.connect(self.Pigment_CMYK_2_Minus)
        self.layout.cmyk_2_plus.clicked.connect(self.Pigment_CMYK_2_Plus)
        self.cmyk_2_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_2_Slider_Modify)
        self.cmyk_2_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_2_Slider_Release)
        self.cmyk_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_2_value.valueChanged.connect(self.Pigment_CMYK_2_Value_Modify)
        self.layout.cmyk_2_value.editingFinished.connect(self.Pigment_CMYK_2_Value_Release)
        # Channel YELLOW
        self.layout.cmyk_3_label.clicked.connect(self.Pigment_CMYK_3_Half)
        self.layout.cmyk_3_minus.clicked.connect(self.Pigment_CMYK_3_Minus)
        self.layout.cmyk_3_plus.clicked.connect(self.Pigment_CMYK_3_Plus)
        self.cmyk_3_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_3_Slider_Modify)
        self.cmyk_3_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_3_Slider_Release)
        self.cmyk_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_3_value.valueChanged.connect(self.Pigment_CMYK_3_Value_Modify)
        self.layout.cmyk_3_value.editingFinished.connect(self.Pigment_CMYK_3_Value_Release)
        # Channel KEY
        self.layout.cmyk_4_label.clicked.connect(self.Pigment_CMYK_4_Half)
        self.layout.cmyk_4_minus.clicked.connect(self.Pigment_CMYK_4_Minus)
        self.layout.cmyk_4_plus.clicked.connect(self.Pigment_CMYK_4_Plus)
        self.cmyk_4_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_4_Slider_Modify)
        self.cmyk_4_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_4_Slider_Release)
        self.cmyk_4_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_4_value.valueChanged.connect(self.Pigment_CMYK_4_Value_Modify)
        self.layout.cmyk_4_value.editingFinished.connect(self.Pigment_CMYK_4_Value_Release)

        # Hex Input
        self.layout.hex_string.returnPressed.connect(self.HEX_Code)

        # Panel HSV
        self.panel_hsv = Panel_HSV(self.layout.panel_hsv_1)
        self.panel_hsv.SIGNAL_HSV_VALUE.connect(self.Signal_HSV)
        self.panel_hsv.SIGNAL_HSV_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsv.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HSV
        self.panel_hsl = Panel_HSL(self.layout.panel_hsl_1)
        self.panel_hsl.SIGNAL_HSL_VALUE.connect(self.Signal_HSL)
        self.panel_hsl.SIGNAL_HSL_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsl.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel ARD
        self.panel_ard = Panel_ARD(self.layout.panel_ard_fg)
        self.panel_ard.SIGNAL_ARD_VALUE.connect(self.Signal_ARD)
        self.panel_ard.SIGNAL_ARD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_ard.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel UVD
        self.panel_uvd = Panel_UVD(self.layout.panel_uvd_input)
        self.panel_uvd.SIGNAL_UVD_VALUE.connect(self.Signal_UVD)
        self.panel_uvd.SIGNAL_UVD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_uvd.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
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
        self.mixer_ard_l1 = Clicks(self.layout.ard_l1)
        self.mixer_ard_l2 = Clicks(self.layout.ard_l2)
        self.mixer_ard_l3 = Clicks(self.layout.ard_l3)
        self.mixer_ard_r1 = Clicks(self.layout.ard_r1)
        self.mixer_ard_r2 = Clicks(self.layout.ard_r2)
        self.mixer_ard_r3 = Clicks(self.layout.ard_r3)
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
        # ARD connection
        self.mixer_ard_l1.SIGNAL_APPLY.connect(self.Mixer_ARD_L1_APPLY)
        self.mixer_ard_l1.SIGNAL_SAVE.connect(self.Mixer_ARD_L1_SAVE)
        self.mixer_ard_l1.SIGNAL_CLEAN.connect(self.Mixer_ARD_L1_CLEAN)
        self.mixer_ard_r1.SIGNAL_APPLY.connect(self.Mixer_ARD_R1_APPLY)
        self.mixer_ard_r1.SIGNAL_SAVE.connect(self.Mixer_ARD_R1_SAVE)
        self.mixer_ard_r1.SIGNAL_CLEAN.connect(self.Mixer_ARD_R1_CLEAN)
        self.mixer_ard_l2.SIGNAL_APPLY.connect(self.Mixer_ARD_L2_APPLY)
        self.mixer_ard_l2.SIGNAL_SAVE.connect(self.Mixer_ARD_L2_SAVE)
        self.mixer_ard_l2.SIGNAL_CLEAN.connect(self.Mixer_ARD_L2_CLEAN)
        self.mixer_ard_r2.SIGNAL_APPLY.connect(self.Mixer_ARD_R2_APPLY)
        self.mixer_ard_r2.SIGNAL_SAVE.connect(self.Mixer_ARD_R2_SAVE)
        self.mixer_ard_r2.SIGNAL_CLEAN.connect(self.Mixer_ARD_R2_CLEAN)
        self.mixer_ard_l3.SIGNAL_APPLY.connect(self.Mixer_ARD_L3_APPLY)
        self.mixer_ard_l3.SIGNAL_SAVE.connect(self.Mixer_ARD_L3_SAVE)
        self.mixer_ard_l3.SIGNAL_CLEAN.connect(self.Mixer_ARD_L3_CLEAN)
        self.mixer_ard_r3.SIGNAL_APPLY.connect(self.Mixer_ARD_R3_APPLY)
        self.mixer_ard_r3.SIGNAL_SAVE.connect(self.Mixer_ARD_R3_SAVE)
        self.mixer_ard_r3.SIGNAL_CLEAN.connect(self.Mixer_ARD_R3_CLEAN)
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
        self.mixer_ard_g1 = Mixer_Gradient(self.layout.ard_g1)
        self.mixer_ard_g2 = Mixer_Gradient(self.layout.ard_g2)
        self.mixer_ard_g3 = Mixer_Gradient(self.layout.ard_g3)

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
        self.mixer_ard_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_ARD_G1)
        self.mixer_ard_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_ARD_G2)
        self.mixer_ard_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_ARD_G3)
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
        self.mixer_ard_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_ard_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_ard_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
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
        # UVD Release Panel Update
        self.mixer_tint.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_tone.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_shade.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_rgb_g1.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_rgb_g2.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_rgb_g3.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_ard_g1.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_ard_g2.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_ard_g3.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_hsv_g1.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_hsv_g2.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_hsv_g3.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_hsl_g1.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_hsl_g2.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_hsl_g3.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_cmyk_g1.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_cmyk_g2.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.UVD_Release)
    def Object(self):
        # BackGround 1
        self.layout.b1_live.clicked.connect(self.BG_1_Exclusion)
        self.b1_color = Clicks(self.layout.b1_color)
        self.b1_color.SIGNAL_APPLY.connect(self.BG_1_APPLY)
        self.b1_color.SIGNAL_SAVE.connect(lambda: self.BG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b1a, "SAVE"))
        self.b1_color.SIGNAL_CLEAN.connect(self.BG_1_CLEAN)
        self.b1_alpha = Channel_Linear(self.layout.b1_alpha)
        self.b1_alpha.Setup("NEU")
        self.b1_alpha.SIGNAL_VALUE.connect(self.BG_1_ALPHA)
        # BackGround 2
        self.layout.b2_live.clicked.connect(self.BG_2_Exclusion)
        self.b2_color = Clicks(self.layout.b2_color)
        self.b2_color.SIGNAL_APPLY.connect(self.BG_2_APPLY)
        self.b2_color.SIGNAL_SAVE.connect(lambda: self.BG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b2a, "SAVE"))
        self.b2_color.SIGNAL_CLEAN.connect(self.BG_2_CLEAN)
        self.b2_alpha = Channel_Linear(self.layout.b2_alpha)
        self.b2_alpha.Setup("NEU")
        self.b2_alpha.SIGNAL_VALUE.connect(self.BG_2_ALPHA)
        # BackGround 3
        self.layout.b3_live.clicked.connect(self.BG_3_Exclusion)
        self.b3_color = Clicks(self.layout.b3_color)
        self.b3_color.SIGNAL_APPLY.connect(self.BG_3_APPLY)
        self.b3_color.SIGNAL_SAVE.connect(lambda: self.BG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b3a, "SAVE"))
        self.b3_color.SIGNAL_CLEAN.connect(self.BG_3_CLEAN)
        self.b3_alpha = Channel_Linear(self.layout.b3_alpha)
        self.b3_alpha.Setup("NEU")
        self.b3_alpha.SIGNAL_VALUE.connect(self.BG_3_ALPHA)

        # Diffuse 1
        self.layout.d1_live.clicked.connect(self.DIF_1_Exclusion)
        self.d1_color = Clicks(self.layout.d1_color)
        self.d1_color.SIGNAL_APPLY.connect(self.DIF_1_APPLY)
        self.d1_color.SIGNAL_SAVE.connect(lambda: self.DIF_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d1a, "SAVE"))
        self.d1_color.SIGNAL_CLEAN.connect(self.DIF_1_CLEAN)
        self.d1_alpha = Channel_Linear(self.layout.d1_alpha)
        self.d1_alpha.Setup("NEU")
        self.d1_alpha.SIGNAL_VALUE.connect(self.DIF_1_ALPHA)
        # Diffuse 2
        self.layout.d2_live.clicked.connect(self.DIF_2_Exclusion)
        self.d2_color = Clicks(self.layout.d2_color)
        self.d2_color.SIGNAL_APPLY.connect(self.DIF_2_APPLY)
        self.d2_color.SIGNAL_SAVE.connect(lambda: self.DIF_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d2a, "SAVE"))
        self.d2_color.SIGNAL_CLEAN.connect(self.DIF_2_CLEAN)
        self.d2_alpha = Channel_Linear(self.layout.d2_alpha)
        self.d2_alpha.Setup("NEU")
        self.d2_alpha.SIGNAL_VALUE.connect(self.DIF_2_ALPHA)
        # Diffuse 3
        self.layout.d3_live.clicked.connect(self.DIF_3_Exclusion)
        self.d3_color = Clicks(self.layout.d3_color)
        self.d3_color.SIGNAL_APPLY.connect(self.DIF_3_APPLY)
        self.d3_color.SIGNAL_SAVE.connect(lambda: self.DIF_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d3a, "SAVE"))
        self.d3_color.SIGNAL_CLEAN.connect(self.DIF_3_CLEAN)
        self.d3_alpha = Channel_Linear(self.layout.d3_alpha)
        self.d3_alpha.Setup("NEU")
        self.d3_alpha.SIGNAL_VALUE.connect(self.DIF_3_ALPHA)
        # Diffuse 4
        self.layout.d4_live.clicked.connect(self.DIF_4_Exclusion)
        self.d4_color = Clicks(self.layout.d4_color)
        self.d4_color.SIGNAL_APPLY.connect(self.DIF_4_APPLY)
        self.d4_color.SIGNAL_SAVE.connect(lambda: self.DIF_4_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d4a, "SAVE"))
        self.d4_color.SIGNAL_CLEAN.connect(self.DIF_4_CLEAN)
        self.d4_alpha = Channel_Linear(self.layout.d4_alpha)
        self.d4_alpha.Setup("NEU")
        self.d4_alpha.SIGNAL_VALUE.connect(self.DIF_4_ALPHA)
        # Diffuse 5
        self.layout.d5_live.clicked.connect(self.DIF_5_Exclusion)
        self.d5_color = Clicks(self.layout.d5_color)
        self.d5_color.SIGNAL_APPLY.connect(self.DIF_5_APPLY)
        self.d5_color.SIGNAL_SAVE.connect(lambda: self.DIF_5_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d5a, "SAVE"))
        self.d5_color.SIGNAL_CLEAN.connect(self.DIF_5_CLEAN)
        self.d5_alpha = Channel_Linear(self.layout.d5_alpha)
        self.d5_alpha.Setup("NEU")
        self.d5_alpha.SIGNAL_VALUE.connect(self.DIF_5_ALPHA)
        # Diffuse 6
        self.layout.d6_live.clicked.connect(self.DIF_6_Exclusion)
        self.d6_color = Clicks(self.layout.d6_color)
        self.d6_color.SIGNAL_APPLY.connect(self.DIF_6_APPLY)
        self.d6_color.SIGNAL_SAVE.connect(lambda: self.DIF_6_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d6a, "SAVE"))
        self.d6_color.SIGNAL_CLEAN.connect(self.DIF_6_CLEAN)
        self.d6_alpha = Channel_Linear(self.layout.d6_alpha)
        self.d6_alpha.Setup("NEU")
        self.d6_alpha.SIGNAL_VALUE.connect(self.DIF_6_ALPHA)

        # ForeGround 1
        self.layout.f1_live.clicked.connect(self.FG_1_Exclusion)
        self.f1_color = Clicks(self.layout.f1_color)
        self.f1_color.SIGNAL_APPLY.connect(self.FG_1_APPLY)
        self.f1_color.SIGNAL_SAVE.connect(lambda: self.FG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f1a, "SAVE"))
        self.f1_color.SIGNAL_CLEAN.connect(self.FG_1_CLEAN)
        self.f1_alpha = Channel_Linear(self.layout.f1_alpha)
        self.f1_alpha.Setup("NEU")
        self.f1_alpha.SIGNAL_VALUE.connect(self.FG_1_ALPHA)
        # ForeGround 2
        self.layout.f2_live.clicked.connect(self.FG_2_Exclusion)
        self.f2_color = Clicks(self.layout.f2_color)
        self.f2_color.SIGNAL_APPLY.connect(self.FG_2_APPLY)
        self.f2_color.SIGNAL_SAVE.connect(lambda: self.FG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f2a, "SAVE"))
        self.f2_color.SIGNAL_CLEAN.connect(self.FG_2_CLEAN)
        self.f2_alpha = Channel_Linear(self.layout.f2_alpha)
        self.f2_alpha.Setup("NEU")
        self.f2_alpha.SIGNAL_VALUE.connect(self.FG_2_ALPHA)
        # ForeGround 3
        self.layout.f3_live.clicked.connect(self.FG_3_Exclusion)
        self.f3_color = Clicks(self.layout.f3_color)
        self.f3_color.SIGNAL_APPLY.connect(self.FG_3_APPLY)
        self.f3_color.SIGNAL_SAVE.connect(lambda: self.FG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f3a, "SAVE"))
        self.f3_color.SIGNAL_CLEAN.connect(self.FG_3_CLEAN)
        self.f3_alpha = Channel_Linear(self.layout.f3_alpha)
        self.f3_alpha.Setup("NEU")
        self.f3_alpha.SIGNAL_VALUE.connect(self.FG_3_ALPHA)

        # Tracking (Mouse + Tablet) Events For Object Panel
        self.layout.layers_widget.setMouseTracking(True)
        self.layout.layers_widget.setTabletTracking(True)
        self.layout.layers_widget.installEventFilter(self)

        # Style Sheets
        self.layout.layers_widget.setStyleSheet(bg_gradient)
        self.layout.layer_01.setStyleSheet(bg_unseen)
        self.layout.layer_02.setStyleSheet(bg_unseen)
        self.layout.layer_03.setStyleSheet(bg_unseen)
        self.layout.layer_04.setStyleSheet(bg_unseen)
        self.layout.layer_05.setStyleSheet(bg_unseen)
        self.layout.layer_06.setStyleSheet(bg_unseen)
        self.layout.layer_07.setStyleSheet(bg_unseen)
        self.layout.layer_08.setStyleSheet(bg_unseen)
        self.layout.layer_09.setStyleSheet(bg_unseen)
        self.layout.layer_10.setStyleSheet(bg_unseen)
        self.layout.b1_color.setStyleSheet(bg_alpha)
        self.layout.b2_color.setStyleSheet(bg_alpha)
        self.layout.b3_color.setStyleSheet(bg_alpha)
        self.layout.d1_color.setStyleSheet(bg_alpha)
        self.layout.d2_color.setStyleSheet(bg_alpha)
        self.layout.d3_color.setStyleSheet(bg_alpha)
        self.layout.d4_color.setStyleSheet(bg_alpha)
        self.layout.d5_color.setStyleSheet(bg_alpha)
        self.layout.d6_color.setStyleSheet(bg_alpha)
        self.layout.f1_color.setStyleSheet(bg_alpha)
        self.layout.f2_color.setStyleSheet(bg_alpha)
        self.layout.f3_color.setStyleSheet(bg_alpha)
        self.layout.b1_alpha.setStyleSheet(bg_alpha)
        self.layout.b2_alpha.setStyleSheet(bg_alpha)
        self.layout.b3_alpha.setStyleSheet(bg_alpha)
        self.layout.d1_alpha.setStyleSheet(bg_alpha)
        self.layout.d2_alpha.setStyleSheet(bg_alpha)
        self.layout.d3_alpha.setStyleSheet(bg_alpha)
        self.layout.d4_alpha.setStyleSheet(bg_alpha)
        self.layout.d5_alpha.setStyleSheet(bg_alpha)
        self.layout.d6_alpha.setStyleSheet(bg_alpha)
        self.layout.f1_alpha.setStyleSheet(bg_alpha)
        self.layout.f2_alpha.setStyleSheet(bg_alpha)
        self.layout.f3_alpha.setStyleSheet(bg_alpha)
    def Style_Sheet(self):
        # UI Percentage Gradients Display
        p4 = self.Percentage("4")
        p6 = self.Percentage("6")
        ten = self.Percentage("TEN")
        thirds = self.Percentage("3S")
        self.layout.eraser.setStyleSheet(bg_alpha)
        self.layout.percentage_top.setStyleSheet(ten)
        self.layout.percentage_bot.setStyleSheet(ten)
        self.layout.label_percent.setStyleSheet(bg_unseen)
        self.layout.aaa_1_tick.setStyleSheet(p4)
        self.layout.rgb_1_tick.setStyleSheet(p4)
        self.layout.rgb_2_tick.setStyleSheet(p4)
        self.layout.rgb_3_tick.setStyleSheet(p4)
        self.layout.ard_1_tick.setStyleSheet(p6)
        self.layout.ard_2_tick.setStyleSheet(p4)
        self.layout.ard_3_tick.setStyleSheet(p6)
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
        self.layout.panel_ard.setStyleSheet(thirds)
        self.layout.panel_uvd.setStyleSheet(bg_alpha)
        self.layout.tip_00.setStyleSheet(bg_alpha)

    #//
    #\\ Menu Displays ##########################################################
    def Menu_Options(self, save):
        if self.layout.option.isChecked() == True:
            # Options 1
            self.layout.aaa.setMinimumHeight(ui_menu)
            self.layout.aaa.setMaximumHeight(ui_menu)
            self.layout.rgb.setMinimumHeight(ui_menu)
            self.layout.rgb.setMaximumHeight(ui_menu)
            self.layout.ard.setMinimumHeight(ui_menu)
            self.layout.ard.setMaximumHeight(ui_menu)
            self.layout.hsv.setMinimumHeight(ui_menu)
            self.layout.hsv.setMaximumHeight(ui_menu)
            self.layout.hsl.setMinimumHeight(ui_menu)
            self.layout.hsl.setMaximumHeight(ui_menu)
            self.layout.cmyk.setMinimumHeight(ui_menu)
            self.layout.cmyk.setMaximumHeight(ui_menu)
            # Options 2
            self.layout.tip.setMinimumHeight(ui_menu)
            self.layout.tip.setMaximumHeight(ui_menu)
            self.layout.tts.setMinimumHeight(ui_menu)
            self.layout.tts.setMaximumHeight(ui_menu)
            self.layout.mix.setMinimumHeight(ui_menu)
            self.layout.mix.setMaximumHeight(ui_menu)
            # self.layout.dym.setMinimumHeight(ui_menu)
            # self.layout.dym.setMaximumHeight(ui_menu)
            # Options 3
            self.layout.panel.setMinimumHeight(ui_menu)
            self.layout.panel.setMaximumHeight(ui_menu)
            self.layout.obj.setMinimumHeight(ui_menu)
            self.layout.obj.setMaximumHeight(ui_menu)
        else:
            # Options 1
            self.layout.aaa.setMinimumHeight(zero)
            self.layout.aaa.setMaximumHeight(zero)
            self.layout.rgb.setMinimumHeight(zero)
            self.layout.rgb.setMaximumHeight(zero)
            self.layout.ard.setMinimumHeight(zero)
            self.layout.ard.setMaximumHeight(zero)
            self.layout.hsv.setMinimumHeight(zero)
            self.layout.hsv.setMaximumHeight(zero)
            self.layout.hsl.setMinimumHeight(zero)
            self.layout.hsl.setMaximumHeight(zero)
            self.layout.cmyk.setMinimumHeight(zero)
            self.layout.cmyk.setMaximumHeight(zero)
            # Options 2
            self.layout.tip.setMinimumHeight(zero)
            self.layout.tip.setMaximumHeight(zero)
            self.layout.tts.setMinimumHeight(zero)
            self.layout.tts.setMaximumHeight(zero)
            self.layout.mix.setMinimumHeight(zero)
            self.layout.mix.setMaximumHeight(zero)
            # self.layout.dym.setMinimumHeight(zero)
            # self.layout.dym.setMaximumHeight(zero)
            # Options 3
            self.layout.panel.setMinimumHeight(zero)
            self.layout.panel.setMaximumHeight(zero)
            self.layout.obj.setMinimumHeight(zero)
            self.layout.obj.setMaximumHeight(zero)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
        self.update()

    def Menu_SOF(self):
        font = self.layout.sof_sliders.font()
        if self.layout.sof_sliders.isChecked():
            font.setBold(True)
            self.layout.sof_1_label.setMinimumHeight(ui_min_1)
            self.layout.sof_1_label.setMaximumHeight(ui_max_1)
            self.layout.sof_1_slider.setMinimumHeight(ui_min_1)
            self.layout.sof_1_slider.setMaximumHeight(ui_max_1)
            self.layout.sof_1_value.setMinimumHeight(ui_min_1)
            self.layout.sof_1_value.setMaximumHeight(ui_max_1)
            self.layout.sof_1_tick.setMinimumHeight(unit)
            self.layout.sof_2_label.setMinimumHeight(ui_min_1)
            self.layout.sof_2_label.setMaximumHeight(ui_max_1)
            self.layout.sof_2_slider.setMinimumHeight(ui_min_1)
            self.layout.sof_2_slider.setMaximumHeight(ui_max_1)
            self.layout.sof_2_value.setMinimumHeight(ui_min_1)
            self.layout.sof_2_value.setMaximumHeight(ui_max_1)
            self.layout.sof_2_tick.setMinimumHeight(unit)
            self.layout.sof_3_label.setMinimumHeight(ui_min_1)
            self.layout.sof_3_label.setMaximumHeight(ui_max_1)
            self.layout.sof_3_slider.setMinimumHeight(ui_min_1)
            self.layout.sof_3_slider.setMaximumHeight(ui_max_1)
            self.layout.sof_3_value.setMinimumHeight(ui_min_1)
            self.layout.sof_3_value.setMaximumHeight(ui_max_1)
            self.layout.sof_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.layout.sof_1_label.setMinimumHeight(zero)
            self.layout.sof_1_label.setMaximumHeight(zero)
            self.layout.sof_1_slider.setMinimumHeight(zero)
            self.layout.sof_1_slider.setMaximumHeight(zero)
            self.layout.sof_1_value.setMinimumHeight(zero)
            self.layout.sof_1_value.setMaximumHeight(zero)
            self.layout.sof_1_tick.setMinimumHeight(zero)
            self.layout.sof_2_label.setMinimumHeight(zero)
            self.layout.sof_2_label.setMaximumHeight(zero)
            self.layout.sof_2_slider.setMinimumHeight(zero)
            self.layout.sof_2_slider.setMaximumHeight(zero)
            self.layout.sof_2_value.setMinimumHeight(zero)
            self.layout.sof_2_value.setMaximumHeight(zero)
            self.layout.sof_2_tick.setMinimumHeight(zero)
            self.layout.sof_3_label.setMinimumHeight(zero)
            self.layout.sof_3_label.setMaximumHeight(zero)
            self.layout.sof_3_slider.setMinimumHeight(zero)
            self.layout.sof_3_slider.setMaximumHeight(zero)
            self.layout.sof_3_value.setMinimumHeight(zero)
            self.layout.sof_3_value.setMaximumHeight(zero)
            self.layout.sof_3_tick.setMinimumHeight(zero)
        self.layout.sof_sliders.setFont(font)
        self.Pigment_Display()
    def Menu_GRAY(self):
        self.Pigment_Display()

    def Menu_AAA(self, save):
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
            self.Menu_Percentage()
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
            self.Menu_Percentage()
        self.layout.aaa.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_RGB(self, save):
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
            self.Menu_Percentage()
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
            self.Menu_Percentage()
        self.layout.rgb.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_ARD(self, save):
        font = self.layout.ard.font()
        if self.layout.ard.isChecked():
            font.setBold(True)
            self.layout.ard_1_label.setMinimumHeight(ui_min_1)
            self.layout.ard_1_label.setMaximumHeight(ui_max_1)
            self.layout.ard_1_minus.setMinimumHeight(ui_min_1)
            self.layout.ard_1_minus.setMaximumHeight(ui_max_1)
            self.layout.ard_1_slider.setMinimumHeight(ui_min_1)
            self.layout.ard_1_slider.setMaximumHeight(ui_max_1)
            self.layout.ard_1_plus.setMinimumHeight(ui_min_1)
            self.layout.ard_1_plus.setMaximumHeight(ui_max_1)
            self.layout.ard_1_value.setMinimumHeight(ui_min_1)
            self.layout.ard_1_value.setMaximumHeight(ui_max_1)
            self.layout.ard_1_tick.setMinimumHeight(unit)
            self.layout.ard_2_label.setMinimumHeight(ui_min_1)
            self.layout.ard_2_label.setMaximumHeight(ui_max_1)
            self.layout.ard_2_minus.setMinimumHeight(ui_min_1)
            self.layout.ard_2_minus.setMaximumHeight(ui_max_1)
            self.layout.ard_2_slider.setMinimumHeight(ui_min_1)
            self.layout.ard_2_slider.setMaximumHeight(ui_max_1)
            self.layout.ard_2_plus.setMinimumHeight(ui_min_1)
            self.layout.ard_2_plus.setMaximumHeight(ui_max_1)
            self.layout.ard_2_value.setMinimumHeight(ui_min_1)
            self.layout.ard_2_value.setMaximumHeight(ui_max_1)
            self.layout.ard_2_tick.setMinimumHeight(unit)
            self.layout.ard_3_label.setMinimumHeight(ui_min_1)
            self.layout.ard_3_label.setMaximumHeight(ui_max_1)
            self.layout.ard_3_minus.setMinimumHeight(ui_min_1)
            self.layout.ard_3_minus.setMaximumHeight(ui_max_1)
            self.layout.ard_3_slider.setMinimumHeight(ui_min_1)
            self.layout.ard_3_slider.setMaximumHeight(ui_max_1)
            self.layout.ard_3_plus.setMinimumHeight(ui_min_1)
            self.layout.ard_3_plus.setMaximumHeight(ui_max_1)
            self.layout.ard_3_value.setMinimumHeight(ui_min_1)
            self.layout.ard_3_value.setMaximumHeight(ui_max_1)
            self.layout.ard_3_tick.setMinimumHeight(unit)
            self.Menu_Percentage()
        else:
            font.setBold(False)
            self.layout.ard_1_label.setMinimumHeight(zero)
            self.layout.ard_1_label.setMaximumHeight(zero)
            self.layout.ard_1_minus.setMinimumHeight(zero)
            self.layout.ard_1_minus.setMaximumHeight(zero)
            self.layout.ard_1_slider.setMinimumHeight(zero)
            self.layout.ard_1_slider.setMaximumHeight(zero)
            self.layout.ard_1_plus.setMinimumHeight(zero)
            self.layout.ard_1_plus.setMaximumHeight(zero)
            self.layout.ard_1_value.setMinimumHeight(zero)
            self.layout.ard_1_value.setMaximumHeight(zero)
            self.layout.ard_1_tick.setMinimumHeight(zero)
            self.layout.ard_2_label.setMinimumHeight(zero)
            self.layout.ard_2_label.setMaximumHeight(zero)
            self.layout.ard_2_minus.setMinimumHeight(zero)
            self.layout.ard_2_minus.setMaximumHeight(zero)
            self.layout.ard_2_slider.setMinimumHeight(zero)
            self.layout.ard_2_slider.setMaximumHeight(zero)
            self.layout.ard_2_plus.setMinimumHeight(zero)
            self.layout.ard_2_plus.setMaximumHeight(zero)
            self.layout.ard_2_value.setMinimumHeight(zero)
            self.layout.ard_2_value.setMaximumHeight(zero)
            self.layout.ard_2_tick.setMinimumHeight(zero)
            self.layout.ard_3_label.setMinimumHeight(zero)
            self.layout.ard_3_label.setMaximumHeight(zero)
            self.layout.ard_3_minus.setMinimumHeight(zero)
            self.layout.ard_3_minus.setMaximumHeight(zero)
            self.layout.ard_3_slider.setMinimumHeight(zero)
            self.layout.ard_3_slider.setMaximumHeight(zero)
            self.layout.ard_3_plus.setMinimumHeight(zero)
            self.layout.ard_3_plus.setMaximumHeight(zero)
            self.layout.ard_3_value.setMinimumHeight(zero)
            self.layout.ard_3_value.setMaximumHeight(zero)
            self.layout.ard_3_tick.setMinimumHeight(zero)
            self.Menu_Percentage()
        self.layout.ard.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_HSV(self, save):
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
            self.Menu_Percentage()
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
            self.Menu_Percentage()
        self.layout.hsv.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_HSL(self, save):
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
            self.Menu_Percentage()
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
            self.Menu_Percentage()
        self.layout.hsl.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_CMYK(self, save):
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
            self.Menu_Percentage()
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
            self.Menu_Percentage()
        self.layout.cmyk.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_Percentage(self):
        # Place Percentage Style
        if (self.layout.aaa.isChecked() == True or
        self.layout.rgb.isChecked() == True or
        self.layout.ard.isChecked() == True or
        self.layout.hsv.isChecked() == True or
        self.layout.hsl.isChecked() == True or
        self.layout.cmyk.isChecked() == True):
            ten = self.Percentage("TEN")
            self.layout.percentage_top.setStyleSheet(ten)
            self.layout.percentage_bot.setStyleSheet(ten)
            self.layout.percentage_top.setMinimumHeight(ui_min_1)
            self.layout.percentage_top.setMaximumHeight(ui_max_1)
            self.layout.percentage_bot.setMinimumHeight(ui_margin)
            self.layout.percentage_bot.setMaximumHeight(ui_margin)
            self.layout.percentage_spacer.setMinimumHeight(ui_margin)
            self.layout.percentage_spacer.setMaximumHeight(ui_margin)
            self.layout.hex_string.setMinimumHeight(ui_min_1)
            self.layout.hex_string.setMaximumHeight(ui_max_1)
        if (self.layout.aaa.isChecked() == False and
        self.layout.rgb.isChecked() == False and
        self.layout.ard.isChecked() == False and
        self.layout.hsv.isChecked() == False and
        self.layout.hsl.isChecked() == False and
        self.layout.cmyk.isChecked() == False):
            self.layout.percentage_top.setStyleSheet(bg_unseen)
            self.layout.percentage_bot.setStyleSheet(bg_unseen)
            self.layout.percentage_top.setMinimumHeight(zero)
            self.layout.percentage_top.setMaximumHeight(zero)
            self.layout.percentage_bot.setMinimumHeight(zero)
            self.layout.percentage_bot.setMaximumHeight(zero)
            self.layout.percentage_spacer.setMinimumHeight(zero)
            self.layout.percentage_spacer.setMaximumHeight(zero)
            self.layout.hex_string.setMinimumHeight(zero)
            self.layout.hex_string.setMaximumHeight(zero)

    def Menu_TIP(self, save):
        font = self.layout.tip.font()
        if self.layout.tip.isChecked():
            font.setBold(True)
            self.layout.tip_00.setMinimumHeight(ui_tip)
            self.layout.tip_00.setMaximumHeight(ui_tip)
            self.layout.line_1.setMinimumHeight(ui_tip)
            self.layout.line_1.setMaximumHeight(ui_tip)
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
            self.layout.cores.setContentsMargins(two, unit, two, unit)
        else:
            font.setBold(False)
            self.layout.tip_00.setMinimumHeight(zero)
            self.layout.tip_00.setMaximumHeight(zero)
            self.layout.line_1.setMinimumHeight(zero)
            self.layout.line_1.setMaximumHeight(zero)
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
            self.layout.cores.setContentsMargins(zero, zero, zero, zero)
        self.layout.tip.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save()
    def Menu_TTS(self, save):
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
            self.layout.percentage_tts_1.setMinimumHeight(unit)
            self.layout.percentage_tts_1.setMaximumHeight(unit)
            self.layout.percentage_tts_2.setMinimumHeight(unit)
            self.layout.percentage_tts_2.setMaximumHeight(unit)
            self.layout.tint_tone_shade.setContentsMargins(two, unit, two, unit)
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
            self.layout.tint_tone_shade.setContentsMargins(zero, zero, zero, zero)
        self.layout.tts.setFont(font)
        if save == "SAVE":
            self.Mixer_Display()
            self.Settings_Save()
    def Menu_MIX(self, save):
        mixer = self.layout.mix.currentText()
        self.MIX_Shrink()
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
            self.layout.percentage_rgb_1.setMinimumHeight(unit)
            self.layout.percentage_rgb_1.setMaximumHeight(unit)
            self.layout.percentage_rgb_2.setMinimumHeight(unit)
            self.layout.percentage_rgb_2.setMaximumHeight(unit)
            self.layout.mixer_rgb.setContentsMargins(two, unit, two, unit)
        elif mixer == "ARD":
            self.layout.ard_l1.setMinimumHeight(ui_min_2)
            self.layout.ard_l1.setMaximumHeight(ui_max_2)
            self.layout.ard_l2.setMinimumHeight(ui_min_2)
            self.layout.ard_l2.setMaximumHeight(ui_max_2)
            self.layout.ard_l3.setMinimumHeight(ui_min_2)
            self.layout.ard_l3.setMaximumHeight(ui_max_2)
            self.layout.ard_r1.setMinimumHeight(ui_min_2)
            self.layout.ard_r1.setMaximumHeight(ui_max_2)
            self.layout.ard_r2.setMinimumHeight(ui_min_2)
            self.layout.ard_r2.setMaximumHeight(ui_max_2)
            self.layout.ard_r3.setMinimumHeight(ui_min_2)
            self.layout.ard_r3.setMaximumHeight(ui_max_2)
            self.layout.ard_g1.setMinimumHeight(ui_min_2)
            self.layout.ard_g1.setMaximumHeight(ui_max_2)
            self.layout.ard_g2.setMinimumHeight(ui_min_2)
            self.layout.ard_g2.setMaximumHeight(ui_max_2)
            self.layout.ard_g3.setMinimumHeight(ui_min_2)
            self.layout.ard_g3.setMaximumHeight(ui_max_2)
            self.layout.spacer_ard_1.setMinimumHeight(ui_min_2)
            self.layout.spacer_ard_1.setMaximumHeight(ui_max_2)
            self.layout.spacer_ard_2.setMinimumHeight(ui_min_2)
            self.layout.spacer_ard_2.setMaximumHeight(ui_max_2)
            self.layout.spacer_ard_3.setMinimumHeight(ui_min_2)
            self.layout.spacer_ard_3.setMaximumHeight(ui_max_2)
            self.layout.spacer_ard_4.setMinimumHeight(ui_min_2)
            self.layout.spacer_ard_4.setMaximumHeight(ui_max_2)
            self.layout.percentage_ard_1.setMinimumHeight(unit)
            self.layout.percentage_ard_1.setMaximumHeight(unit)
            self.layout.percentage_ard_2.setMinimumHeight(unit)
            self.layout.percentage_ard_2.setMaximumHeight(unit)
            self.layout.mixer_ard.setContentsMargins(two, unit, two, unit)
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
            self.layout.percentage_hsv_1.setMinimumHeight(unit)
            self.layout.percentage_hsv_1.setMaximumHeight(unit)
            self.layout.percentage_hsv_2.setMinimumHeight(unit)
            self.layout.percentage_hsv_2.setMaximumHeight(unit)
            self.layout.mixer_hsv.setContentsMargins(two, unit, two, unit)
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
            self.layout.percentage_hsl_1.setMinimumHeight(unit)
            self.layout.percentage_hsl_1.setMaximumHeight(unit)
            self.layout.percentage_hsl_2.setMinimumHeight(unit)
            self.layout.percentage_hsl_2.setMaximumHeight(unit)
            self.layout.mixer_hsl.setContentsMargins(two, unit, two, unit)
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
            self.layout.percentage_cmyk_1.setMinimumHeight(unit)
            self.layout.percentage_cmyk_1.setMaximumHeight(unit)
            self.layout.percentage_cmyk_2.setMinimumHeight(unit)
            self.layout.percentage_cmyk_2.setMaximumHeight(unit)
            self.layout.mixer_cmyk.setContentsMargins(two, unit, two, unit)
        if save == "SAVE":
            self.Mixer_Display()
            self.Ratio()
            self.Settings_Save()
    def MIX_Shrink(self):
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
        self.layout.mixer_rgb.setContentsMargins(zero, zero, zero, zero)
        # Mix ARD
        self.layout.ard_l1.setMinimumHeight(zero)
        self.layout.ard_l1.setMaximumHeight(zero)
        self.layout.ard_l2.setMinimumHeight(zero)
        self.layout.ard_l2.setMaximumHeight(zero)
        self.layout.ard_l3.setMinimumHeight(zero)
        self.layout.ard_l3.setMaximumHeight(zero)
        self.layout.ard_r1.setMinimumHeight(zero)
        self.layout.ard_r1.setMaximumHeight(zero)
        self.layout.ard_r2.setMinimumHeight(zero)
        self.layout.ard_r2.setMaximumHeight(zero)
        self.layout.ard_r3.setMinimumHeight(zero)
        self.layout.ard_r3.setMaximumHeight(zero)
        self.layout.ard_g1.setMinimumHeight(zero)
        self.layout.ard_g1.setMaximumHeight(zero)
        self.layout.ard_g2.setMinimumHeight(zero)
        self.layout.ard_g2.setMaximumHeight(zero)
        self.layout.ard_g3.setMinimumHeight(zero)
        self.layout.ard_g3.setMaximumHeight(zero)
        self.layout.spacer_ard_1.setMinimumHeight(zero)
        self.layout.spacer_ard_1.setMaximumHeight(zero)
        self.layout.spacer_ard_2.setMinimumHeight(zero)
        self.layout.spacer_ard_2.setMaximumHeight(zero)
        self.layout.spacer_ard_3.setMinimumHeight(zero)
        self.layout.spacer_ard_3.setMaximumHeight(zero)
        self.layout.spacer_ard_4.setMinimumHeight(zero)
        self.layout.spacer_ard_4.setMaximumHeight(zero)
        self.layout.percentage_ard_1.setMinimumHeight(zero)
        self.layout.percentage_ard_1.setMaximumHeight(zero)
        self.layout.percentage_ard_2.setMinimumHeight(zero)
        self.layout.percentage_ard_2.setMaximumHeight(zero)
        self.layout.mixer_ard.setContentsMargins(zero, zero, zero, zero)
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
        self.layout.mixer_hsv.setContentsMargins(zero, zero, zero, zero)
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
        self.layout.mixer_hsl.setContentsMargins(zero, zero, zero, zero)
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
        self.layout.mixer_cmyk.setContentsMargins(zero, zero, zero, zero)
    def Menu_PANEL(self, save):
        panel = self.layout.panel.currentText()
        if panel == "PANEL":
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if panel == "FGC":
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if panel == "HSV":
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSV()
        if panel == "HSL":
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSL()
        if panel == "ARD":
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_RGB()
        if panel == "UVD":
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert_RGB()
        self.Vertical_Spacer()
        if save == "SAVE":
            self.Pigment_Display()
            self.Ratio()
            self.Settings_Save()
    def Menu_OBJ(self, save):
        object = self.layout.obj.currentText()
        self.OBJ_Shrink()
        if object == "OBJECT":
            # Colors
            self.bg_1 = ["False", 0, 0, 0, 0]
            self.bg_2 = ["False", 0, 0, 0, 1]
            self.bg_3 = ["False", 0, 0, 0, 1]
            self.dif_1 = ["False", 0, 0, 0, 1]
            self.dif_2 = ["False", 0, 0, 0, 1]
            self.dif_3 = ["False", 0, 0, 0, 1]
            self.dif_4 = ["False", 0, 0, 0, 1]
            self.dif_5 = ["False", 0, 0, 0, 1]
            self.dif_6 = ["False", 0, 0, 0, 1]
            self.fg_1 = ["False", 0, 0, 0, 1]
            self.fg_2 = ["False", 0, 0, 0, 1]
            self.fg_3 = ["False", 0, 0, 0, 1]
            # Alphas
            self.b1a = 0
            self.b2a = 1
            self.b3a = 1
            self.d1a = 1
            self.d2a = 1
            self.d3a = 1
            self.d4a = 1
            self.d5a = 1
            self.d6a = 1
            self.f1a = 1
            self.f2a = 1
            self.f3a = 1
        if object == "SPHERE":
            # Paths
            self.path_bg_1 = str(self.dir_name + "/OBJECT/SPHERE/bg_1.png")
            self.path_bg_2 = str(self.dir_name + "/OBJECT/SPHERE/bg_2.png")
            self.path_bg_3 = str(self.dir_name + "/OBJECT/SPHERE/bg_3.png")
            self.path_dif_1 = str(self.dir_name + "/OBJECT/SPHERE/dif_1.png")
            self.path_dif_2 = str(self.dir_name + "/OBJECT/SPHERE/dif_2.png")
            self.path_dif_3 = str(self.dir_name + "/OBJECT/SPHERE/dif_3.png")
            self.path_dif_4 = str(self.dir_name + "/OBJECT/SPHERE/dif_4.png")
            self.path_dif_5 = str(self.dir_name + "/OBJECT/SPHERE/dif_5.png")
            self.path_dif_6 = str(self.dir_name + "/OBJECT/SPHERE/dif_6.png")
            self.path_fg_1 = str(self.dir_name + "/OBJECT/SPHERE/fg_1.png")
            self.path_fg_2 = str(self.dir_name + "/OBJECT/SPHERE/fg_2.png")
            self.path_fg_3 = str(self.dir_name + "/OBJECT/SPHERE/fg_3.png")
            # Colors
            self.bg_1 = ["True", 0.5, 0.5, 0.5, 0]
            self.bg_2 = ["True", 0, 0, 0, 1]
            self.bg_3 = ["True", 0, 0, 0, 1]
            self.dif_1 = ["True", 35/255, 20/255, 2/255, 1]
            self.dif_2 = ["True", 84/255, 55/255, 19/255, 1]
            self.dif_3 = ["True", 254/255, 159/255, 14/255, 1]
            self.dif_4 = ["True", 255/255, 202/255, 50/255, 1]
            self.dif_5 = ["False", 0, 0, 0, 0]
            self.dif_6 = ["False", 0, 0, 0, 0]
            self.fg_1 = ["True", 0, 0, 0, 1]
            self.fg_2 = ["True", 255/255, 255/255, 150/255, 1]
            self.fg_3 = ["True", 1, 1, 1, 1]
            # Alphas
            self.b1a = 0
            self.b2a = 1
            self.b3a = 1
            self.d1a = 1
            self.d2a = 1
            self.d3a = 1
            self.d4a = 1
            self.d5a = 0
            self.d6a = 0
            self.f1a = 1
            self.f2a = 1
            self.f3a = 1
            # Reset
            self.OBJ_Scale()
            self.OBJ_Save()
        if object == "BLOB":
            self.path_bg_1 = str(self.dir_name + "/OBJECT/BLOB/bg_1.png")
            self.path_bg_2 = str(self.dir_name + "/OBJECT/BLOB/bg_2.png")
            self.path_bg_3 = str(self.dir_name + "/OBJECT/BLOB/bg_3.png")
            self.path_dif_1 = str(self.dir_name + "/OBJECT/BLOB/dif_1.png")
            self.path_dif_2 = str(self.dir_name + "/OBJECT/BLOB/dif_2.png")
            self.path_dif_3 = str(self.dir_name + "/OBJECT/BLOB/dif_3.png")
            self.path_dif_4 = str(self.dir_name + "/OBJECT/BLOB/dif_4.png")
            self.path_dif_5 = str(self.dir_name + "/OBJECT/BLOB/dif_5.png")
            self.path_dif_6 = str(self.dir_name + "/OBJECT/BLOB/dif_6.png")
            self.path_fg_1 = str(self.dir_name + "/OBJECT/BLOB/fg_1.png")
            self.path_fg_2 = str(self.dir_name + "/OBJECT/BLOB/fg_2.png")
            self.path_fg_3 = str(self.dir_name + "/OBJECT/BLOB/fg_3.png")
            # Colors
            self.bg_1 = ["True", 0.5, 0.5, 0.5, 0]
            self.bg_2 = ["False", 0, 0, 0, 0]
            self.bg_3 = ["False", 0, 0, 0, 0]
            self.dif_1 = ["True", 192/255, 224/255, 235/255, 1]
            self.dif_2 = ["True", 77/255, 9/255, 86/255, 1]
            self.dif_3 = ["False", 0, 0, 0, 0]
            self.dif_4 = ["False", 0, 0, 0, 0]
            self.dif_5 = ["False", 0, 0, 0, 0]
            self.dif_6 = ["False", 0, 0, 0, 0]
            self.fg_1 = ["False", 0, 0, 0, 0]
            self.fg_2 = ["False", 0, 0, 0, 0]
            self.fg_3 = ["False", 0, 0, 0, 0]
            # Alphas
            self.b1a = 0
            self.b2a = 0
            self.b3a = 0
            self.d1a = 1
            self.d2a = 1
            self.d3a = 0
            self.d4a = 0
            self.d5a = 0
            self.d6a = 0
            self.f1a = 0
            self.f2a = 0
            self.f3a = 0
            # Reset
            self.OBJ_Scale()
            self.OBJ_Save()
        if object == "USER":
            self.path_bg_1 = str(self.dir_name + "/OBJECT/USER/bg_1.png")
            self.path_bg_2 = str(self.dir_name + "/OBJECT/USER/bg_2.png")
            self.path_bg_3 = str(self.dir_name + "/OBJECT/USER/bg_3.png")
            self.path_dif_1 = str(self.dir_name + "/OBJECT/USER/dif_1.png")
            self.path_dif_2 = str(self.dir_name + "/OBJECT/USER/dif_2.png")
            self.path_dif_3 = str(self.dir_name + "/OBJECT/USER/dif_3.png")
            self.path_dif_4 = str(self.dir_name + "/OBJECT/USER/dif_4.png")
            self.path_dif_5 = str(self.dir_name + "/OBJECT/USER/dif_5.png")
            self.path_dif_6 = str(self.dir_name + "/OBJECT/USER/dif_6.png")
            self.path_fg_1 = str(self.dir_name + "/OBJECT/USER/fg_1.png")
            self.path_fg_2 = str(self.dir_name + "/OBJECT/USER/fg_2.png")
            self.path_fg_3 = str(self.dir_name + "/OBJECT/USER/fg_3.png")
            # Colors
            self.bg_1 = ["True", 0.5, 0.5, 0.5, 0]
            self.bg_2 = ["True", 0, 0, 0, 1]
            self.bg_3 = ["True", 0, 0, 0, 1]
            self.dif_1 = ["True", 0, 0, 0, 1]
            self.dif_2 = ["True", 0, 0, 0, 1]
            self.dif_3 = ["True", 0, 0, 0, 1]
            self.dif_4 = ["True", 0, 0, 0, 1]
            self.dif_5 = ["True", 0, 0, 0, 1]
            self.dif_6 = ["True", 0, 0, 0, 1]
            self.fg_1 = ["True", 0, 0, 0, 1]
            self.fg_2 = ["True", 0, 0, 0, 1]
            self.fg_3 = ["True", 0, 0, 0, 1]
            # Alphas
            self.b1a = 0
            self.b2a = 1
            self.b3a = 1
            self.d1a = 1
            self.d2a = 1
            self.d3a = 1
            self.d4a = 1
            self.d5a = 1
            self.d6a = 1
            self.f1a = 1
            self.f2a = 1
            self.f3a = 1
            # Reset
            self.OBJ_Scale()
            self.OBJ_Save()
        self.Vertical_Spacer()
        if save == "SAVE":
            self.Pigment_Display()
            self.Ratio()
            self.Settings_Save()
    def OBJ_Shrink(self):
        # Close Live
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # BackGround 1
        self.layout.b1_live.setMinimumHeight(zero)
        self.layout.b1_live.setMaximumHeight(zero)
        self.layout.b1_color.setMinimumHeight(zero)
        self.layout.b1_color.setMaximumHeight(zero)
        self.layout.b1_alpha.setMinimumHeight(zero)
        self.layout.b1_alpha.setMaximumHeight(zero)
        # BackGround 2
        self.layout.b2_live.setMinimumHeight(zero)
        self.layout.b2_live.setMaximumHeight(zero)
        self.layout.b2_color.setMinimumHeight(zero)
        self.layout.b2_color.setMaximumHeight(zero)
        self.layout.b2_alpha.setMinimumHeight(zero)
        self.layout.b2_alpha.setMaximumHeight(zero)
        # BackGround 3
        self.layout.b3_live.setMinimumHeight(zero)
        self.layout.b3_live.setMaximumHeight(zero)
        self.layout.b3_color.setMinimumHeight(zero)
        self.layout.b3_color.setMaximumHeight(zero)
        self.layout.b3_alpha.setMinimumHeight(zero)
        self.layout.b3_alpha.setMaximumHeight(zero)
        # Diffuse 1
        self.layout.d1_live.setMinimumHeight(zero)
        self.layout.d1_live.setMaximumHeight(zero)
        self.layout.d1_color.setMinimumHeight(zero)
        self.layout.d1_color.setMaximumHeight(zero)
        self.layout.d1_alpha.setMinimumHeight(zero)
        self.layout.d1_alpha.setMaximumHeight(zero)
        # Diffuse 2
        self.layout.d2_live.setMinimumHeight(zero)
        self.layout.d2_live.setMaximumHeight(zero)
        self.layout.d2_color.setMinimumHeight(zero)
        self.layout.d2_color.setMaximumHeight(zero)
        self.layout.d2_alpha.setMinimumHeight(zero)
        self.layout.d2_alpha.setMaximumHeight(zero)
        # Diffuse 3
        self.layout.d3_live.setMinimumHeight(zero)
        self.layout.d3_live.setMaximumHeight(zero)
        self.layout.d3_color.setMinimumHeight(zero)
        self.layout.d3_color.setMaximumHeight(zero)
        self.layout.d3_alpha.setMinimumHeight(zero)
        self.layout.d3_alpha.setMaximumHeight(zero)
        # Diffuse 4
        self.layout.d4_live.setMinimumHeight(zero)
        self.layout.d4_live.setMaximumHeight(zero)
        self.layout.d4_color.setMinimumHeight(zero)
        self.layout.d4_color.setMaximumHeight(zero)
        self.layout.d4_alpha.setMinimumHeight(zero)
        self.layout.d4_alpha.setMaximumHeight(zero)
        # Diffuse 5
        self.layout.d5_live.setMinimumHeight(zero)
        self.layout.d5_live.setMaximumHeight(zero)
        self.layout.d5_color.setMinimumHeight(zero)
        self.layout.d5_color.setMaximumHeight(zero)
        self.layout.d5_alpha.setMinimumHeight(zero)
        self.layout.d5_alpha.setMaximumHeight(zero)
        # Diffuse 6
        self.layout.d6_live.setMinimumHeight(zero)
        self.layout.d6_live.setMaximumHeight(zero)
        self.layout.d6_color.setMinimumHeight(zero)
        self.layout.d6_color.setMaximumHeight(zero)
        self.layout.d6_alpha.setMinimumHeight(zero)
        self.layout.d6_alpha.setMaximumHeight(zero)
        # ForeGround 1
        self.layout.f1_live.setMinimumHeight(zero)
        self.layout.f1_live.setMaximumHeight(zero)
        self.layout.f1_color.setMinimumHeight(zero)
        self.layout.f1_color.setMaximumHeight(zero)
        self.layout.f1_alpha.setMinimumHeight(zero)
        self.layout.f1_alpha.setMaximumHeight(zero)
        # ForeGround 2
        self.layout.f2_live.setMinimumHeight(zero)
        self.layout.f2_live.setMaximumHeight(zero)
        self.layout.f2_color.setMinimumHeight(zero)
        self.layout.f2_color.setMaximumHeight(zero)
        self.layout.f2_alpha.setMinimumHeight(zero)
        self.layout.f2_alpha.setMaximumHeight(zero)
        # ForeGround 3
        self.layout.f3_live.setMinimumHeight(zero)
        self.layout.f3_live.setMaximumHeight(zero)
        self.layout.f3_color.setMinimumHeight(zero)
        self.layout.f3_color.setMaximumHeight(zero)
        self.layout.f3_alpha.setMinimumHeight(zero)
        self.layout.f3_alpha.setMaximumHeight(zero)
        # Spacer
        self.layout.spacer_object.setMinimumHeight(zero)
        self.layout.spacer_object.setMaximumHeight(zero)
        self.layout.objects.setContentsMargins(zero, zero, zero, zero)
        self.layout.layers_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    def OBJ_Scale(self):
        # BackGround 1
        self.layout.b1_live.setMinimumHeight(ui_max_2)
        self.layout.b1_live.setMaximumHeight(ui_max_2)
        self.layout.b1_color.setMinimumHeight(ui_max_1)
        self.layout.b1_color.setMaximumHeight(ui_tip)
        self.layout.b1_alpha.setMinimumHeight(ui_min_2)
        self.layout.b1_alpha.setMaximumHeight(ui_min_2)
        # BackGround 2
        self.layout.b2_live.setMinimumHeight(ui_max_2)
        self.layout.b2_live.setMaximumHeight(ui_max_2)
        self.layout.b2_color.setMinimumHeight(ui_max_1)
        self.layout.b2_color.setMaximumHeight(ui_tip)
        self.layout.b2_alpha.setMinimumHeight(ui_min_2)
        self.layout.b2_alpha.setMaximumHeight(ui_min_2)
        # BackGround 3
        self.layout.b3_live.setMinimumHeight(ui_max_2)
        self.layout.b3_live.setMaximumHeight(ui_max_2)
        self.layout.b3_color.setMinimumHeight(ui_max_1)
        self.layout.b3_color.setMaximumHeight(ui_tip)
        self.layout.b3_alpha.setMinimumHeight(ui_min_2)
        self.layout.b3_alpha.setMaximumHeight(ui_min_2)
        # Diffuse 1
        self.layout.d1_live.setMinimumHeight(ui_max_2)
        self.layout.d1_live.setMaximumHeight(ui_max_2)
        self.layout.d1_color.setMinimumHeight(ui_max_1)
        self.layout.d1_color.setMaximumHeight(ui_tip)
        self.layout.d1_alpha.setMinimumHeight(ui_min_2)
        self.layout.d1_alpha.setMaximumHeight(ui_min_2)
        # Diffuse 2
        self.layout.d2_live.setMinimumHeight(ui_max_2)
        self.layout.d2_live.setMaximumHeight(ui_max_2)
        self.layout.d2_color.setMinimumHeight(ui_max_1)
        self.layout.d2_color.setMaximumHeight(ui_tip)
        self.layout.d2_alpha.setMinimumHeight(ui_min_2)
        self.layout.d2_alpha.setMaximumHeight(ui_min_2)
        # Diffuse 3
        self.layout.d3_live.setMinimumHeight(ui_max_2)
        self.layout.d3_live.setMaximumHeight(ui_max_2)
        self.layout.d3_color.setMinimumHeight(ui_max_1)
        self.layout.d3_color.setMaximumHeight(ui_tip)
        self.layout.d3_alpha.setMinimumHeight(ui_min_2)
        self.layout.d3_alpha.setMaximumHeight(ui_min_2)
        # Diffuse 4
        self.layout.d4_live.setMinimumHeight(ui_max_2)
        self.layout.d4_live.setMaximumHeight(ui_max_2)
        self.layout.d4_color.setMinimumHeight(ui_max_1)
        self.layout.d4_color.setMaximumHeight(ui_tip)
        self.layout.d4_alpha.setMinimumHeight(ui_min_2)
        self.layout.d4_alpha.setMaximumHeight(ui_min_2)
        # Diffuse 5
        self.layout.d5_live.setMinimumHeight(ui_max_2)
        self.layout.d5_live.setMaximumHeight(ui_max_2)
        self.layout.d5_color.setMinimumHeight(ui_max_1)
        self.layout.d5_color.setMaximumHeight(ui_tip)
        self.layout.d5_alpha.setMinimumHeight(ui_min_2)
        self.layout.d5_alpha.setMaximumHeight(ui_min_2)
        # Diffuse 6
        self.layout.d6_live.setMinimumHeight(ui_max_2)
        self.layout.d6_live.setMaximumHeight(ui_max_2)
        self.layout.d6_color.setMinimumHeight(ui_max_1)
        self.layout.d6_color.setMaximumHeight(ui_tip)
        self.layout.d6_alpha.setMinimumHeight(ui_min_2)
        self.layout.d6_alpha.setMaximumHeight(ui_min_2)
        # ForeGround 1
        self.layout.f1_live.setMinimumHeight(ui_max_2)
        self.layout.f1_live.setMaximumHeight(ui_max_2)
        self.layout.f1_color.setMinimumHeight(ui_max_1)
        self.layout.f1_color.setMaximumHeight(ui_tip)
        self.layout.f1_alpha.setMinimumHeight(ui_min_2)
        self.layout.f1_alpha.setMaximumHeight(ui_min_2)
        # ForeGround 2
        self.layout.f2_live.setMinimumHeight(ui_max_2)
        self.layout.f2_live.setMaximumHeight(ui_max_2)
        self.layout.f2_color.setMinimumHeight(ui_max_1)
        self.layout.f2_color.setMaximumHeight(ui_tip)
        self.layout.f2_alpha.setMinimumHeight(ui_min_2)
        self.layout.f2_alpha.setMaximumHeight(ui_min_2)
        # ForeGround 3
        self.layout.f3_live.setMinimumHeight(ui_max_2)
        self.layout.f3_live.setMaximumHeight(ui_max_2)
        self.layout.f3_color.setMinimumHeight(ui_max_1)
        self.layout.f3_color.setMaximumHeight(ui_tip)
        self.layout.f3_alpha.setMinimumHeight(ui_min_2)
        self.layout.f3_alpha.setMaximumHeight(ui_min_2)
        # Spacer
        self.layout.spacer_object.setMinimumHeight(two)
        self.layout.spacer_object.setMaximumHeight(two)
        self.layout.objects.setContentsMargins(two, unit, two, unit)
        self.layout.layers_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    def OBJ_Save(self):
        self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, self.bg_2[1]*255, self.bg_2[2]*255, self.bg_2[3]*255, self.bg_2[4]*255))
        self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, self.bg_3[1]*255, self.bg_3[2]*255, self.bg_3[3]*255, self.bg_3[4]*255))
        self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, self.dif_1[1]*255, self.dif_1[2]*255, self.dif_1[3]*255, self.dif_1[4]*255))
        self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, self.dif_2[1]*255, self.dif_2[2]*255, self.dif_2[3]*255, self.dif_2[4]*255))
        self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, self.dif_3[1]*255, self.dif_3[2]*255, self.dif_3[3]*255, self.dif_3[4]*255))
        self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, self.dif_4[1]*255, self.dif_4[2]*255, self.dif_4[3]*255, self.dif_4[4]*255))
        self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, self.dif_5[1]*255, self.dif_5[2]*255, self.dif_5[3]*255, self.dif_5[4]*255))
        self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, self.dif_6[1]*255, self.dif_6[2]*255, self.dif_6[3]*255, self.dif_6[4]*255))
        self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, self.fg_1[1]*255, self.fg_1[2]*255, self.fg_1[3]*255, self.fg_1[4]*255))
        self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, self.fg_2[1]*255, self.fg_2[2]*255, self.fg_2[3]*255, self.fg_2[4]*255))
        self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, self.fg_3[1]*255, self.fg_3[2]*255, self.fg_3[3]*255, self.fg_3[4]*255))
        self.BG_1_SAVE(self.bg_1[1], self.bg_1[2], self.bg_1[3], self.bg_1[4], "SAVE")
        self.BG_2_SAVE(self.bg_2[1], self.bg_2[2], self.bg_2[3], self.bg_2[4], "SAVE")
        self.BG_3_SAVE(self.bg_3[1], self.bg_3[2], self.bg_3[3], self.bg_3[4], "SAVE")
        self.DIF_1_SAVE(self.dif_1[1], self.dif_1[2], self.dif_1[3], self.dif_1[4], "SAVE")
        self.DIF_2_SAVE(self.dif_2[1], self.dif_2[2], self.dif_2[3], self.dif_2[4], "SAVE")
        self.DIF_3_SAVE(self.dif_3[1], self.dif_3[2], self.dif_3[3], self.dif_3[4], "SAVE")
        self.DIF_4_SAVE(self.dif_4[1], self.dif_4[2], self.dif_4[3], self.dif_4[4], "SAVE")
        self.DIF_5_SAVE(self.dif_5[1], self.dif_5[2], self.dif_5[3], self.dif_5[4], "SAVE")
        self.DIF_6_SAVE(self.dif_6[1], self.dif_6[2], self.dif_6[3], self.dif_6[4], "SAVE")
        self.FG_1_SAVE(self.fg_1[1], self.fg_1[2], self.fg_1[3], self.fg_1[4], "SAVE")
        self.FG_2_SAVE(self.fg_2[1], self.fg_2[2], self.fg_2[3], self.fg_2[4], "SAVE")
        self.FG_3_SAVE(self.fg_3[1], self.fg_3[2], self.fg_3[3], self.fg_3[4], "SAVE")
    def Vertical_Spacer(self):
        if (self.layout.panel.currentText() == "PANEL" and self.layout.obj.font() == False):
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        else:
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

    def Menu_Shrink(self):
        # Options
        self.layout.aaa.setMinimumHeight(zero)
        self.layout.aaa.setMaximumHeight(zero)
        self.layout.rgb.setMinimumHeight(zero)
        self.layout.rgb.setMaximumHeight(zero)
        self.layout.ard.setMinimumHeight(zero)
        self.layout.ard.setMaximumHeight(zero)
        self.layout.hsv.setMinimumHeight(zero)
        self.layout.hsv.setMaximumHeight(zero)
        self.layout.hsl.setMinimumHeight(zero)
        self.layout.hsl.setMaximumHeight(zero)
        self.layout.cmyk.setMinimumHeight(zero)
        self.layout.cmyk.setMaximumHeight(zero)
        self.layout.tip.setMinimumHeight(zero)
        self.layout.tip.setMaximumHeight(zero)
        self.layout.tts.setMinimumHeight(zero)
        self.layout.tts.setMaximumHeight(zero)
        self.layout.mix.setMinimumHeight(zero)
        self.layout.mix.setMaximumHeight(zero)
        # self.layout.dym.setMinimumHeight(zero)
        # self.layout.dym.setMaximumHeight(zero)
        self.layout.panel.setMinimumHeight(zero)
        self.layout.panel.setMaximumHeight(zero)
        self.layout.obj.setMinimumHeight(zero)
        self.layout.obj.setMaximumHeight(zero)
        # AAA
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
        # RGB
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
        # ARD
        self.layout.ard_1_label.setMinimumHeight(zero)
        self.layout.ard_1_label.setMaximumHeight(zero)
        self.layout.ard_1_minus.setMinimumHeight(zero)
        self.layout.ard_1_minus.setMaximumHeight(zero)
        self.layout.ard_1_slider.setMinimumHeight(zero)
        self.layout.ard_1_slider.setMaximumHeight(zero)
        self.layout.ard_1_plus.setMinimumHeight(zero)
        self.layout.ard_1_plus.setMaximumHeight(zero)
        self.layout.ard_1_value.setMinimumHeight(zero)
        self.layout.ard_1_value.setMaximumHeight(zero)
        self.layout.ard_1_tick.setMinimumHeight(zero)
        self.layout.ard_2_label.setMinimumHeight(zero)
        self.layout.ard_2_label.setMaximumHeight(zero)
        self.layout.ard_2_minus.setMinimumHeight(zero)
        self.layout.ard_2_minus.setMaximumHeight(zero)
        self.layout.ard_2_slider.setMinimumHeight(zero)
        self.layout.ard_2_slider.setMaximumHeight(zero)
        self.layout.ard_2_plus.setMinimumHeight(zero)
        self.layout.ard_2_plus.setMaximumHeight(zero)
        self.layout.ard_2_value.setMinimumHeight(zero)
        self.layout.ard_2_value.setMaximumHeight(zero)
        self.layout.ard_2_tick.setMinimumHeight(zero)
        self.layout.ard_3_label.setMinimumHeight(zero)
        self.layout.ard_3_label.setMaximumHeight(zero)
        self.layout.ard_3_minus.setMinimumHeight(zero)
        self.layout.ard_3_minus.setMaximumHeight(zero)
        self.layout.ard_3_slider.setMinimumHeight(zero)
        self.layout.ard_3_slider.setMaximumHeight(zero)
        self.layout.ard_3_plus.setMinimumHeight(zero)
        self.layout.ard_3_plus.setMaximumHeight(zero)
        self.layout.ard_3_value.setMinimumHeight(zero)
        self.layout.ard_3_value.setMaximumHeight(zero)
        self.layout.ard_3_tick.setMinimumHeight(zero)
        # HSV
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
        # HSL
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
        # CMYK
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
        # Percentage
        self.layout.percentage_top.setStyleSheet(bg_unseen)
        self.layout.percentage_bot.setStyleSheet(bg_unseen)
        self.layout.percentage_top.setMinimumHeight(zero)
        self.layout.percentage_top.setMaximumHeight(zero)
        self.layout.percentage_bot.setMinimumHeight(zero)
        self.layout.percentage_bot.setMaximumHeight(zero)
        self.layout.percentage_spacer.setMinimumHeight(zero)
        self.layout.percentage_spacer.setMaximumHeight(zero)
        self.layout.hex_string.setMinimumHeight(zero)
        self.layout.hex_string.setMaximumHeight(zero)
        # TIP
        self.layout.tip_00.setMinimumHeight(zero)
        self.layout.tip_00.setMaximumHeight(zero)
        self.layout.line_1.setMinimumHeight(zero)
        self.layout.line_1.setMaximumHeight(zero)
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
        self.layout.cores.setContentsMargins(zero, zero, zero, zero)
        # TTS
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
        self.layout.tint_tone_shade.setContentsMargins(zero, zero, zero, zero)
        # Mixer
        self.MIX_Shrink()
        # Panel
        self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Object
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        self.layout.b1_live.setMinimumHeight(zero)
        self.layout.b1_live.setMaximumHeight(zero)
        self.layout.b1_color.setMinimumHeight(zero)
        self.layout.b1_color.setMaximumHeight(zero)
        self.layout.b1_alpha.setMinimumHeight(zero)
        self.layout.b1_alpha.setMaximumHeight(zero)
        self.layout.b2_live.setMinimumHeight(zero)
        self.layout.b2_live.setMaximumHeight(zero)
        self.layout.b2_color.setMinimumHeight(zero)
        self.layout.b2_color.setMaximumHeight(zero)
        self.layout.b2_alpha.setMinimumHeight(zero)
        self.layout.b2_alpha.setMaximumHeight(zero)
        self.layout.b3_live.setMinimumHeight(zero)
        self.layout.b3_live.setMaximumHeight(zero)
        self.layout.b3_color.setMinimumHeight(zero)
        self.layout.b3_color.setMaximumHeight(zero)
        self.layout.b3_alpha.setMinimumHeight(zero)
        self.layout.b3_alpha.setMaximumHeight(zero)
        self.layout.d1_live.setMinimumHeight(zero)
        self.layout.d1_live.setMaximumHeight(zero)
        self.layout.d1_color.setMinimumHeight(zero)
        self.layout.d1_color.setMaximumHeight(zero)
        self.layout.d1_alpha.setMinimumHeight(zero)
        self.layout.d1_alpha.setMaximumHeight(zero)
        self.layout.d2_live.setMinimumHeight(zero)
        self.layout.d2_live.setMaximumHeight(zero)
        self.layout.d2_color.setMinimumHeight(zero)
        self.layout.d2_color.setMaximumHeight(zero)
        self.layout.d2_alpha.setMinimumHeight(zero)
        self.layout.d2_alpha.setMaximumHeight(zero)
        self.layout.d3_live.setMinimumHeight(zero)
        self.layout.d3_live.setMaximumHeight(zero)
        self.layout.d3_color.setMinimumHeight(zero)
        self.layout.d3_color.setMaximumHeight(zero)
        self.layout.d3_alpha.setMinimumHeight(zero)
        self.layout.d3_alpha.setMaximumHeight(zero)
        self.layout.d4_live.setMinimumHeight(zero)
        self.layout.d4_live.setMaximumHeight(zero)
        self.layout.d4_color.setMinimumHeight(zero)
        self.layout.d4_color.setMaximumHeight(zero)
        self.layout.d4_alpha.setMinimumHeight(zero)
        self.layout.d4_alpha.setMaximumHeight(zero)
        self.layout.d5_live.setMinimumHeight(zero)
        self.layout.d5_live.setMaximumHeight(zero)
        self.layout.d5_color.setMinimumHeight(zero)
        self.layout.d5_color.setMaximumHeight(zero)
        self.layout.d5_alpha.setMinimumHeight(zero)
        self.layout.d5_alpha.setMaximumHeight(zero)
        self.layout.d6_live.setMinimumHeight(zero)
        self.layout.d6_live.setMaximumHeight(zero)
        self.layout.d6_color.setMinimumHeight(zero)
        self.layout.d6_color.setMaximumHeight(zero)
        self.layout.d6_alpha.setMinimumHeight(zero)
        self.layout.d6_alpha.setMaximumHeight(zero)
        self.layout.f1_live.setMinimumHeight(zero)
        self.layout.f1_live.setMaximumHeight(zero)
        self.layout.f1_color.setMinimumHeight(zero)
        self.layout.f1_color.setMaximumHeight(zero)
        self.layout.f1_alpha.setMinimumHeight(zero)
        self.layout.f1_alpha.setMaximumHeight(zero)
        self.layout.f2_live.setMinimumHeight(zero)
        self.layout.f2_live.setMaximumHeight(zero)
        self.layout.f2_color.setMinimumHeight(zero)
        self.layout.f2_color.setMaximumHeight(zero)
        self.layout.f2_alpha.setMinimumHeight(zero)
        self.layout.f2_alpha.setMaximumHeight(zero)
        self.layout.f3_live.setMinimumHeight(zero)
        self.layout.f3_live.setMaximumHeight(zero)
        self.layout.f3_color.setMinimumHeight(zero)
        self.layout.f3_color.setMaximumHeight(zero)
        self.layout.f3_alpha.setMinimumHeight(zero)
        self.layout.f3_alpha.setMaximumHeight(zero)
        self.layout.spacer_object.setMinimumHeight(zero)
        self.layout.spacer_object.setMaximumHeight(zero)
        self.layout.objects.setContentsMargins(zero, zero, zero, zero)
        self.layout.layers_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Vertical Spacer
        self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # SOF
        self.layout.sof_1_label.setMinimumHeight(zero)
        self.layout.sof_1_label.setMaximumHeight(zero)
        self.layout.sof_1_slider.setMinimumHeight(zero)
        self.layout.sof_1_slider.setMaximumHeight(zero)
        self.layout.sof_1_value.setMinimumHeight(zero)
        self.layout.sof_1_value.setMaximumHeight(zero)
        self.layout.sof_1_tick.setMinimumHeight(zero)
        self.layout.sof_2_label.setMinimumHeight(zero)
        self.layout.sof_2_label.setMaximumHeight(zero)
        self.layout.sof_2_slider.setMinimumHeight(zero)
        self.layout.sof_2_slider.setMaximumHeight(zero)
        self.layout.sof_2_value.setMinimumHeight(zero)
        self.layout.sof_2_value.setMaximumHeight(zero)
        self.layout.sof_2_tick.setMinimumHeight(zero)
        self.layout.sof_3_label.setMinimumHeight(zero)
        self.layout.sof_3_label.setMaximumHeight(zero)
        self.layout.sof_3_slider.setMinimumHeight(zero)
        self.layout.sof_3_slider.setMaximumHeight(zero)
        self.layout.sof_3_value.setMinimumHeight(zero)
        self.layout.sof_3_value.setMaximumHeight(zero)
        self.layout.sof_3_tick.setMinimumHeight(zero)

    #//
    #\\ Krita to Pigment #######################################################
    def Krita_TIMER(self):
        font = self.layout.check.font()
        state = self.layout.check.checkState()
        if check_timer >= 1000:
            if state == 0:
                font.setBold(False)
                self.layout.check.setText("OFF")
                self.timer.stop()
            elif state == 1:
                font.setBold(True)
                self.layout.check.setText("ON")
                self.Krita_Update()
                self.timer.start()
            elif state == 2:
                font.setBold(True)
                self.layout.check.setText("P>K")
                self.timer.stop()
        else:
            font.setBold(False)
            self.layout.check.setText("C<1")
            self.layout.check.setEnabled(False)
        self.layout.check.setFont(font)
    def Krita_Update(self):
        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            state = self.layout.check.checkState()
            if state == 1:
                try:
                    # Document Profile
                    doc = self.Document_Profile()
                    view = Krita.instance().activeWindow().activeView()
                    # Check Eraser Mode ON or OFF
                    kritaEraserAction = Application.action("erase_action")
                    if kritaEraserAction.isChecked() == True:
                        self.layout.eraser.setStyleSheet(bg_eraser_on)
                    else:
                        self.layout.eraser.setStyleSheet(bg_eraser_off)
                    # Current Krita SOF
                    ks = view.brushSize()
                    ko = view.paintingOpacity()
                    kf = view.paintingFlow()
                    # Update Pigmento if SOF Differ
                    if self.sof_1 != ks:
                        self.sof_1 = ks
                        self.SOF_1_APPLY(self.sof_1)
                    if self.sof_2 != ko:
                        self.sof_2 = ko
                        self.SOF_2_APPLY(self.sof_2)
                    if self.sof_3 != kf:
                        self.sof_3 = kf
                        self.SOF_3_APPLY(self.sof_3)
                    # Current Krita Color
                    color_foreground = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                    color_foreground = Application.activeWindow().activeView().foregroundColor()
                    color_background = Application.activeWindow().activeView().backgroundColor()
                    components_fg = color_foreground.components()
                    components_bg = color_background.components()
                    # Hold UVD D depth for autocorrect error
                    self.d_previous = self.uvd_3
                    # Update Pigmento if Colors Differ
                    if (doc[0] == "A" or doc[0] == "GRAYA"):
                        # Change Display to Black and White Automatic
                        self.layout.gray_panels.setChecked(True)
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
                            self.layout.gray_panels.setChecked(True)
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

    #//
    #\\ Apply Color ############################################################
    def Color_AAA(self, a):
        rgb = [a, a, a]
        uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
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
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
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
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
    def Color_ARD(self, a, r, d):
        # Convertions
        uvd = self.ard_to_uvd(a, r, d)
        rgb = self.uvd_to_rgb(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = a
        self.ard_2 = r
        self.ard_3 = d
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
    def Color_UVD(self, u, v, d):
        # Convertions
        rgb = self.uvd_to_rgb(u, v, d)
        ard = self.uvd_to_ard(u, v, d)
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = u
        self.uvd_2 = v
        self.uvd_3 = d
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        # to AAA
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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

    #//
    #\\ Convert ################################################################
    def Pigment_Convert_AAA(self):
        # Original
        self.aaa_1 = self.layout.aaa_1_value.value() / kritaAAA
        # Converts
        uvd = self.rgb_to_uvd(self.aaa_1, self.aaa_1, self.aaa_1)
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(self.aaa_1, self.aaa_1, self.aaa_1)
        hsl = self.rgb_to_hsl(self.aaa_1, self.aaa_1, self.aaa_1)
        cmyk = self.rgb_to_cmyk(self.aaa_1, self.aaa_1, self.aaa_1)
        # to RGB
        self.rgb_1 = self.aaa_1
        self.rgb_2 = self.aaa_1
        self.rgb_3 = self.aaa_1
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(self.rgb_1, self.rgb_2, self.rgb_3)
        hsl = self.rgb_to_hsl(self.rgb_1, self.rgb_2, self.rgb_3)
        cmyk = self.rgb_to_cmyk(self.rgb_1, self.rgb_2, self.rgb_3)
        # to Alpha
        self.aaa_1 = max(self.rgb_1, self.rgb_2, self.rgb_3)
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
    def Pigment_Convert_ARD(self, ignore):
        # Original
        self.ard_1 = self.layout.ard_1_value.value() / kritaANG
        self.ard_2 = self.layout.ard_2_value.value() / kritaRDL
        self.ard_3 = self.layout.ard_3_value.value() / kritaRDL
        # Conversions
        uvd = self.ard_to_uvd(self.ard_1, self.ard_2, self.ard_3)
        rgb = self.uvd_to_rgb(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # Correct random D depth
        if ignore == 0:
            condition = self.uvd_3 - self.d_previous
            if (condition > -unitRDL and condition < unitRDL):
                self.uvd_3 = self.d_previous
                self.ard_3 = self.d_previous
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
        self.Pigment_Sync_ARD()
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        # to Alpha
        self.aaa_1 = max(rgb[0], rgb[1], rgb[2])
        # to RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # to UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # to ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -unitRDL and condition < unitRDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
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
    # AAA RGB HSV HSL CMYK  Input range 0.0 to 1.0
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
    # XYZ LAB YIQ
    def rgb_to_xyz(self, r, g, b):
        if r > 0.04045:
            r = ( ( r + 0.055 ) / 1.055 ) ** 2.4
        else:
            r = r / 12.92
        if g > 0.04045:
            g = ( ( g + 0.055 ) / 1.055 ) ** 2.4
        else:
            g = g / 12.92
        if b > 0.04045:
            b = ( ( b + 0.055 ) / 1.055 ) ** 2.4
        else:
            b = b / 12.92
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        return x, y, z
    def xyz_to_rgb(self, x, y, z):
        r = x *  3.2406 + y * -1.5372 + z * -0.4986
        g = x * -0.9689 + y *  1.8758 + z *  0.0415
        b = x *  0.0557 + y * -0.2040 + z *  1.0570
        if r > 0.0031308:
            r = 1.055 * ( r ** ( 1 / 2.4 ) ) - 0.055
        else:
            r = 12.92 * r
        if g > 0.0031308:
            g = 1.055 * ( g ** ( 1 / 2.4 ) ) - 0.055
        else:
            g = 12.92 * g
        if b > 0.0031308:
            b = 1.055 * ( b ** ( 1 / 2.4 ) ) - 0.055
        else:
            b = 12.92 * b
        return r, g, b
    def xyz_to_lab(self, x, y, z):
        if x > 0.008856:
            x = x ** ( 1/3 )
        else:
            x = ( 7.787 * x ) + ( 16 / 116 )
        if y > 0.008856:
            y = y ** ( 1/3 )
        else:
            y = ( 7.787 * y ) + ( 16 / 116 )
        if z > 0.008856:
            z = z ** ( 1/3 )
        else:
            z = ( 7.787 * z ) + ( 16 / 116 )
        l = ( 116 * y ) - 16
        a = 500 * ( x - y )
        b = 200 * ( y - z )
        l = l / factorX
        a = a / factorY
        b = b / factorZ
        return l, a, b
    def lab_to_xyz(self, l, a, b):
        y = ( l + 16 ) / 116
        x = a / 500 + y
        z = y - b / 200
        if (y**3)  > 0.008856:
            y = y**3
        else:
            y = ( y - 16 / 116 ) / 7.787
        if (x**3)  > 0.008856:
            x = x**3
        else:
            x = ( x - 16 / 116 ) / 7.787
        if (z**3)  > 0.008856:
            z = z**3
        else:
            z = ( z - 16 / 116 ) / 7.787
        return x, y, z
    def rgb_to_yiq(self, r, g, b):
        y = 0.30*r + 0.59*g + 0.11*b
        i = 0.74*(r-y) - 0.27*(b-y)
        q = 0.48*(r-y) + 0.41*(b-y)
        return y, i, q
    def yiq_to_rgb(self, y, i, q):
        # r = y + (0.27*q + 0.41*i) / (0.74*0.41 + 0.27*0.48)
        # b = y + (0.74*q - 0.48*i) / (0.74*0.41 + 0.27*0.48)
        # g = y - (0.30*(r-y) + 0.11*(b-y)) / 0.59

        r = y + 0.9468822170900693*i + 0.6235565819861433*q
        g = y - 0.27478764629897834*i - 0.6356910791873801*q
        b = y - 1.1085450346420322*i + 1.7090069284064666*q

        if r < 0.0:
            r = 0.0
        if g < 0.0:
            g = 0.0
        if b < 0.0:
            b = 0.0
        if r > 1.0:
            r = 1.0
        if g > 1.0:
            g = 1.0
        if b > 1.0:
            b = 1.0
        return r, g, b
    # UVD ARD Input Range 0.0 to 1.0
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
        # Correct out of Bound values
        if r <= 0:
            r = 0
        if r >= 1:
            r = 1
        if g <= 0:
            g = 0
        if g >= 1:
            g = 1
        if b <= 0:
            b = 0
        if b >= 1:
            b = 1
        return [r, g, b]
    def uvd_hexagon_origins(self):
        # Values
        w1 = 0.8660253882408142
        h1 = 0.5000000596046448
        h2 = 1
        diagonal = self.uvd_3 * 3
        delta1 = diagonal
        delta2 = diagonal - 1
        delta3 = diagonal - 2
        # Single Points
        if diagonal <= 0.0:
            self.O1 = [0, 0]
            self.O2 = [0, 0]
            self.O3 = [0, 0]
            self.O4 = [0, 0]
            self.O5 = [0, 0]
            self.O6 = [0, 0]
        elif (diagonal > 0.0 and diagonal <= 1.0):
            self.O1 = [0 + 0,           0 - (h2*delta1)]  # -1 exception to not be zero area
            self.O2 = [0 + (w1*delta1), 0 + (h1*delta1)]
            self.O3 = [0 + (w1*delta1), 0 + (h1*delta1)]
            self.O4 = [0 - (w1*delta1), 0 + (h1*delta1)]
            self.O5 = [0 - (w1*delta1), 0 + (h1*delta1)]
            self.O6 = [0 + 0,                0 - (h2*delta1)]  # -1 exception to not be zero area
        elif (diagonal > 1.0 and diagonal < 2.0):
            self.O1 = [ 0  + (w1*delta2), -h2 + (h1*delta2)]
            self.O2 = [ w1 + 0,            h1 - (h2*delta2)]
            self.O3 = [ w1 - (w1*delta2),  h1 + (h1*delta2)]
            self.O4 = [-w1 + (w1*delta2),  h1 + (h1*delta2)]
            self.O5 = [-w1 + 0,            h1 - (h2*delta2)]
            self.O6 = [  0 - (w1*delta2), -h2 + (h1*delta2)]
        elif (diagonal >= 2.0 and diagonal < 3.0):
            self.O1 = [ w1 - (w1*delta3), -h1 + (h1*delta3)]
            self.O2 = [ w1 - (w1*delta3), -h1 + (h1*delta3)]
            self.O3 = [ 0  + 0,            h2 - (h2*delta3)]
            self.O4 = [ 0  + 0,            h2 - (h2*delta3)]
            self.O5 = [-w1 + (w1*delta3), -h1 + (h1*delta3)]
            self.O6 = [-w1 + (w1*delta3), -h1 + (h1*delta3)]
        elif diagonal >= 3.0:
            self.O1 = [0, 0]
            self.O2 = [0, 0]
            self.O3 = [0, 0]
            self.O4 = [0, 0]
            self.O5 = [0, 0]
            self.O6 = [0, 0]
        # Composed Points
        self.OCC = [0, 0]
        self.O12 = [self.O1[0] + ((self.O2[0] - self.O1[0]) / 2), self.O1[1] + ((self.O2[1] - self.O1[1]) / 2)]
        self.O23 = [self.O2[0] + ((self.O3[0] - self.O2[0]) / 2), self.O2[1] + ((self.O3[1] - self.O2[1]) / 2)]
        self.O34 = [self.O3[0] + ((self.O4[0] - self.O3[0]) / 2), self.O3[1] + ((self.O4[1] - self.O3[1]) / 2)]
        self.O45 = [self.O4[0] + ((self.O5[0] - self.O4[0]) / 2), self.O4[1] + ((self.O5[1] - self.O4[1]) / 2)]
        self.O56 = [self.O5[0] + ((self.O6[0] - self.O5[0]) / 2), self.O5[1] + ((self.O6[1] - self.O5[1]) / 2)]
        self.O61 = [self.O6[0] + ((self.O1[0] - self.O6[0]) / 2), self.O6[1] + ((self.O1[1] - self.O6[1]) / 2)]
        # Angle to Red Axis as Origin
        self.REDAXIS = self.angle(10, 0, 0, 0, self.O45[0], self.O45[1])
    def uvd_to_ard(self, u, v, d):
        # Correct UV values
        u = round(u,15)
        v = round(v,15)
        # Angle
        if (u == 0 and v == 0):
            arc=0
            a=0
        else:
            arc = self.angle(u,v, 0,0, self.O45[0],self.O45[1]) # range 0 to 360
            a = arc / 360 # range 0 to 1
        # User Value
        user = self.distance(0, 0, u, v)
        # Total Value
        diagonal = d * 3
        if diagonal <= 0:
            a = 0
            total = 1
        elif (diagonal > 0 and diagonal <= 1):
            # Angles according to O45(RED) as Origin
            AR = 0 # RED
            AG = self.angle(self.O23[0], self.O23[1], 0, 0, self.O45[0], self.O45[1]) # GREEN
            AB = self.angle(self.O61[0], self.O61[1], 0, 0, self.O45[0], self.O45[1]) # BLUE
            # Certain
            if arc == AR:
                total = self.distance(0, 0, self.O45[0], self.O45[1])
            elif arc == AG:
                total = self.distance(0, 0, self.O23[0], self.O23[1])
            elif arc == AB:
                total = self.distance(0, 0, self.O61[0], self.O61[1])
            # Intervals
            elif (arc > AR and arc < AG):
                inter = list(self.intersection(self.O3[0], self.O3[1], self.O4[0], self.O4[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AG and arc < AB):
                inter = list(self.intersection(self.O1[0], self.O1[1], self.O2[0], self.O2[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AB or arc < AR):
                inter = list(self.intersection(self.O5[0], self.O5[1], self.O6[0], self.O6[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
        elif (diagonal > 1 and diagonal < 2):
            # Angles according to O45(RED) as Origin
            A1 = self.angle(self.O1[0], self.O1[1], 0, 0, self.O45[0], self.O45[1]) # O1
            A2 = self.angle(self.O2[0], self.O2[1], 0, 0, self.O45[0], self.O45[1]) # O2
            A3 = self.angle(self.O3[0], self.O3[1], 0, 0, self.O45[0], self.O45[1]) # O3
            A4 = self.angle(self.O4[0], self.O4[1], 0, 0, self.O45[0], self.O45[1]) # O4
            A5 = self.angle(self.O5[0], self.O5[1], 0, 0, self.O45[0], self.O45[1]) # O5
            A6 = self.angle(self.O6[0], self.O6[1], 0, 0, self.O45[0], self.O45[1]) # O6
            # Certain
            if arc == A1:
                total = self.distance(0, 0, self.O1[0], self.O1[1])
            elif arc == A2:
                total = self.distance(0, 0, self.O2[0], self.O2[1])
            elif arc == A3:
                total = self.distance(0, 0, self.O3[0], self.O3[1])
            elif arc == A4:
                total = self.distance(0, 0, self.O4[0], self.O4[1])
            elif arc == A5:
                total = self.distance(0, 0, self.O5[0], self.O5[1])
            elif arc == A6:
                total = self.distance(0, 0, self.O6[0], self.O6[1])
            # Intervals
            elif (arc > A4 and arc < A3): # 0
                inter = list(self.intersection(self.O4[0], self.O4[1], self.O3[0], self.O3[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A3 and arc < A2): # 60
                inter = list(self.intersection(self.O3[0], self.O3[1], self.O2[0], self.O2[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A2 and arc < A1): # 120
                inter = list(self.intersection(self.O2[0], self.O2[1], self.O1[0], self.O1[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A1 and arc < A6): # 180
                inter = list(self.intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A6 and arc < A5): # 240
                inter = list(self.intersection(self.O6[0], self.O6[1], self.O5[0], self.O5[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A5 or arc < A4): # 300
                inter = list(self.intersection(self.O5[0], self.O5[1], self.O4[0], self.O4[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
        elif (diagonal >= 2 and diagonal < 3):
            # Angles according to O45(RED) as Origin
            AY = self.angle(self.O34[0], self.O34[1], 0, 0, self.O45[0], self.O45[1]) # YELLOW
            AC = self.angle(self.O12[0], self.O12[1], 0, 0, self.O45[0], self.O45[1]) # CYAN
            AM = self.angle(self.O56[0], self.O56[1], 0, 0, self.O45[0], self.O45[1]) # MAGENTA
            # Certain
            if arc == AY:
                total = self.distance(0, 0, self.O34[0], self.O34[1])
            elif arc == AC:
                total = self.distance(0, 0, self.O12[0], self.O12[1])
            elif arc == AM:
                total = self.distance(0, 0, self.O56[0], self.O56[1])
            # Intervals
            elif (arc > AY and arc < AC):
                inter = list(self.intersection(self.O2[0], self.O2[1], self.O3[0], self.O3[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AC and arc < AM):
                inter = list(self.intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AM or arc < AY):
                inter = list(self.intersection(self.O4[0], self.O4[1], self.O5[0], self.O5[1], 0, 0, u, v))
                total = self.distance(0, 0, inter[0], inter[1])
        elif diagonal >= 3:
            a = 0
            total = 1
        # Percentual Value of the distance from the center to the outside
        try:
            ratio = user / total
        except:
            ratio = user
        r = ratio
        return [a, r, d]
    def ard_to_uvd(self, a, r, d):
        # Angle according to normal zero axis +U right and counter clockwise
        a360 = a * 360
        arc = a360 - self.REDAXIS
        if a360 < self.REDAXIS:
            arc = (360 - self.REDAXIS) + a360
        # Intersection Vector line Point
        ucos =  math.cos(math.radians(arc))
        vsin = -math.sin(math.radians(arc))
        # Diagonal Depth
        diagonal = d * 3
        if diagonal <= 0:
            total = 1
        elif (diagonal > 0 and diagonal <= 1):
            # Angles according to +U(UVD) as Origin
            AR = self.angle(self.O45[0], self.O45[1], 0, 0, 1, 0) # RED
            AG = self.angle(self.O23[0], self.O23[1], 0, 0, 1, 0) # GREEN
            AB = self.angle(self.O61[0], self.O61[1], 0, 0, 1, 0) # BLUE
            # Certain
            if arc == AR: # RED
                total = self.distance(0, 0, self.O45[0], self.O45[1])
            elif arc == AG: # GREEN
                total = self.distance(0, 0, self.O23[0], self.O23[1])
            elif arc == AB: # BLUE
                total = self.distance(0, 0, self.O61[0], self.O61[1])
            # Intervals
            elif (arc > AR and arc < AG):
                inter = list(self.intersection(self.O3[0], self.O3[1], self.O4[0], self.O4[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AG or arc < AB):
                inter = list(self.intersection(self.O1[0], self.O1[1], self.O2[0], self.O2[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AB and arc < AR):
                inter = list(self.intersection(self.O5[0], self.O5[1], self.O6[0], self.O6[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
        elif (diagonal > 1 and diagonal < 2):
            # Angles according to +U(UVD) as Origin
            A1 = self.angle(self.O1[0], self.O1[1], 0, 0, 1, 0) # P1
            A2 = self.angle(self.O2[0], self.O2[1], 0, 0, 1, 0) # P2
            A3 = self.angle(self.O3[0], self.O3[1], 0, 0, 1, 0) # P3
            A4 = self.angle(self.O4[0], self.O4[1], 0, 0, 1, 0) # P4
            A5 = self.angle(self.O5[0], self.O5[1], 0, 0, 1, 0) # P5
            A6 = self.angle(self.O6[0], self.O6[1], 0, 0, 1, 0) # P6
            # Certain
            if arc == A1:
                total = self.distance(0, 0, self.O1[0], self.O1[1])
            elif arc == A2:
                total = self.distance(0, 0, self.O2[0], self.O2[1])
            elif arc == A3:
                total = self.distance(0, 0, self.O3[0], self.O3[1])
            elif arc == A4:
                total = self.distance(0, 0, self.O4[0], self.O4[1])
            elif arc == A5:
                total = self.distance(0, 0, self.O5[0], self.O5[1])
            elif arc == A6:
                total = self.distance(0, 0, self.O6[0], self.O6[1])
            # Intervals
            elif (arc > A1 and arc < A6): # 180
                inter = list(self.intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A6 and arc < A5): # 240
                inter = list(self.intersection(self.O6[0], self.O6[1], self.O5[0], self.O5[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A5 and arc < A4): # 300
                inter = list(self.intersection(self.O5[0], self.O5[1], self.O4[0], self.O4[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > A4 and arc < A3): # 0
                inter = list(self.intersection(self.O4[0], self.O4[1], self.O3[0], self.O3[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            # Desambiguiation due to A2 crossing the Origin Axis
            elif A2 < 180:
                if (arc > A3 or arc < A2): # 60 OR
                    inter = list(self.intersection(self.O3[0], self.O3[1], self.O2[0], self.O2[1], 0, 0, ucos, vsin))
                    total = self.distance(0, 0, inter[0], inter[1])
                if (arc > A2 and arc < A1): # 120 AND
                    inter = list(self.intersection(self.O2[0], self.O2[1], self.O1[0], self.O1[1], 0, 0, ucos, vsin))
                    total = self.distance(0, 0, inter[0], inter[1])
            elif A2 > 180:
                if (arc > A3 and arc < A2): # 60 AND
                    inter = list(self.intersection(self.O3[0], self.O3[1], self.O2[0], self.O2[1], 0, 0, ucos, vsin))
                    total = self.distance(0, 0, inter[0], inter[1])
                if (arc > A2 or arc < A1): # 120 OR
                    inter = list(self.intersection(self.O2[0], self.O2[1], self.O1[0], self.O1[1], 0, 0, ucos, vsin))
                    total = self.distance(0, 0, inter[0], inter[1])
        elif (diagonal >= 2 and diagonal < 3):
            # Angles according to +U(UVD) as Origin
            AY = self.angle(self.O34[0], self.O34[1], 0, 0, 1, 0) # YELLOW
            AC = self.angle(self.O12[0], self.O12[1], 0, 0, 1, 0) # CYAN
            AM = self.angle(self.O56[0], self.O56[1], 0, 0, 1, 0) # MAGENTA
            # Certain
            if arc == AY:
                total = self.distance(0, 0, self.O34[0], self.O34[1])
            elif arc == AC:
                total = self.distance(0, 0, self.O12[0], self.O12[1])
            elif arc == AM:
                total = self.distance(0, 0, self.O56[0], self.O56[1])
            # Intervals
            elif (arc > AY or arc < AC):
                inter = list(self.intersection(self.O2[0], self.O2[1], self.O3[0], self.O3[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AC and arc < AM):
                inter = list(self.intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
            elif (arc > AM and arc < AY):
                inter = list(self.intersection(self.O4[0], self.O4[1], self.O5[0], self.O5[1], 0, 0, ucos, vsin))
                total = self.distance(0, 0, inter[0], inter[1])
        elif diagonal >= 3:
            total = 1
        # User Distance to Center
        user = r * total
        u = user * math.cos(math.radians(arc))
        v = user * -math.sin(math.radians(arc))
        # Correct UV for D extreme value
        if (d==0 or d==1):
            u = 0
            v = 0
        return [u, v, d]
    def rgb_to_ard(self, r, g, b):
        uvd = self.rgb_to_uvd(r, g, b)
        ard = self.uvd_to_ard(uvd[0], uvd[1], uvd[2])
        a = ard[0]
        r = ard[1]
        d = ard[2]
        return [a, r, d]
    def ard_to_rgb(self, a, r, d):
        uvd = self.ard_to_uvd(a, r, d)
        rgb = self.uvd_to_rgb(uvd[0], uvd[1], uvd[2])
        # Correct out of Bound values
        if rgb[0] <= 0:
            rgb[0] = 0
        if rgb[0] >= 1:
            rgb[0] = 1
        if rgb[1] <= 0:
            uvd[1] = 0
        if rgb[1] >= 1:
            rgb[1] = 1
        if rgb[2] <= 0:
            rgb[2] = 0
        if rgb[2] >= 1:
            rgb[2] = 1
        # Values
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return [r, g, b]
    # Trignometry
    def angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle
    def distance(self, x1, y1, x2, y2):
        # Point 1 = x1, y1
        # Point 2 = x2, y2
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # Line 1 = x1,y1, x2,y2
        # Line 2 = x3,y3, x4,y4
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return [xx, yy]

    #//
    #\\ Sync Channels ##########################################################
    def Pigment_Sync_AAA(self):
        # Block Signals
        self.Signal_Block_RGB(True)
        self.Signal_Block_ARD(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_RGB(False)
        self.Signal_Block_ARD(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_RGB(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_ARD(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_ARD(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_ARD(self):
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
    def Pigment_Sync_HSV(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_ARD(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_ARD(False)
        self.Signal_Block_HSL(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_HSL(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_ARD(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_ARD(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_CMYK(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_CMYK(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_ARD(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_ARD(False)
        self.Signal_Block_HSV(False)
        self.Signal_Block_HSL(False)
        # Settings
        self.Settings_Save_Color()
    def Pigment_Sync_UPDATE(self):
        # Block Signals
        self.Signal_Block_AAA(True)
        self.Signal_Block_RGB(True)
        self.Signal_Block_ARD(True)
        self.Signal_Block_HSV(True)
        self.Signal_Block_HSL(True)
        self.Signal_Block_CMYK(True)
        # Set Values
        self.Signal_Send_AAA(self.aaa_1)
        self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        self.Signal_Send_Panels()
        # UnBlock Signals
        self.Signal_Block_AAA(False)
        self.Signal_Block_RGB(False)
        self.Signal_Block_ARD(False)
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
    def Signal_Block_ARD(self, boolean):
        self.layout.ard_1_slider.blockSignals(boolean)
        self.layout.ard_2_slider.blockSignals(boolean)
        self.layout.ard_3_slider.blockSignals(boolean)
        self.layout.ard_1_value.blockSignals(boolean)
        self.layout.ard_2_value.blockSignals(boolean)
        self.layout.ard_3_value.blockSignals(boolean)
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
    def Signal_Send_ARD(self, value1, value2, value3):
        self.ard_1_slider.Update(value1, self.layout.ard_1_slider.width())
        self.ard_2_slider.Update(value2, self.layout.ard_2_slider.width())
        self.ard_3_slider.Update(value3, self.layout.ard_3_slider.width())
        self.layout.ard_1_value.setValue(value1 * kritaANG)
        self.layout.ard_2_value.setValue(value2 * kritaRDL)
        self.layout.ard_3_value.setValue(value3 * kritaRDL)
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
        # Graphical Panels
        self.panel_hsv.Update_Panel(self.hsv_2, self.hsv_3, self.layout.panel_hsv_1.width(), self.layout.panel_hsv_1.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        self.panel_hsl.Update_Panel(self.hsl_2, self.hsl_3, self.layout.panel_hsl_1.width(), self.layout.panel_hsl_1.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        self.ARD_Update()
        self.UVD_Update()
        # Objects
        self.Object_Live()

    #//
    #\\ Pigment to Krita #######################################################
    def Pigment_2_Krita(self):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
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
            doc = [
                str(Krita.instance().activeDocument().colorModel()),
                str(Krita.instance().activeDocument().colorDepth()),
                str(Krita.instance().activeDocument().colorProfile()),
                ]
        except:
            doc = ["NONE", "NONE", "NONE"]
        return doc

    #//
    #\\ Pigment Display ########################################################
    def Pigment_Display(self):
        # Foreground Color Display (Top Left)
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_1*hexRGB, self.rgb_2*hexRGB, self.rgb_3*hexRGB))
        self.layout.color_1.setStyleSheet(active_color_1)
        # Color/Gray Sliders Display
        # ARD
        if (self.layout.aaa.isChecked() == True and self.layout.gray_sliders.isChecked() == False):
            sss_aaa = str(self.RGB_Gradient([0, 0, 0], [1, 1, 1]))
        else:
            sss_aaa = bg_alpha
        # RGB
        if (self.layout.rgb.isChecked() == True and self.layout.gray_sliders.isChecked() == False):
            sss_rgb1 = str(self.RGB_Gradient([0, self.rgb_2, self.rgb_3], [1, self.rgb_2, self.rgb_3]))
            sss_rgb2 = str(self.RGB_Gradient([self.rgb_1, 0, self.rgb_3], [self.rgb_1, 1, self.rgb_3]))
            sss_rgb3 = str(self.RGB_Gradient([self.rgb_1, self.rgb_2, 0], [self.rgb_1, self.rgb_2, 1]))
        else:
            sss_rgb1 = bg_alpha
            sss_rgb2 = bg_alpha
            sss_rgb3 = bg_alpha
        # ARD
        if (self.layout.ard.isChecked() == True and self.layout.gray_sliders.isChecked() == False):
            if self.ard_3 == 0:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [0, 0, self.ard_3], [1, 0, self.ard_3]))
            elif self.ard_3 == 1:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [0, 0, self.ard_3], [1, 0, self.ard_3]))
            else:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [0, self.ard_2, self.ard_3], [1, self.ard_2, self.ard_3]))
            sss_ard2 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [self.ard_1, 0, self.ard_3], [self.ard_1, 1, self.ard_3]))
            sss_ard3 = str(self.RGB_Gradient([0, 0, 0], [1, 1, 1]))
        else:
            sss_ard1 = bg_alpha
            sss_ard2 = bg_alpha
            sss_ard3 = bg_alpha
        # HSV
        if (self.layout.hsv.isChecked() == True and self.layout.gray_sliders.isChecked() == False):
            sss_hsv1 = str(self.HUE_Gradient("HSV", self.layout.hsv_1_slider.width(), [0, self.hsv_2, self.hsv_3], [1, self.hsv_2, self.hsv_3]))
            sss_hsv2 = str(self.HSV_Gradient(self.layout.hsv_2_slider.width(), [self.hsv_1, 0, self.hsv_3], [self.hsv_1, 1, self.hsv_3]))
            sss_hsv3 = str(self.HSV_Gradient(self.layout.hsv_3_slider.width(), [self.hsv_1, self.hsv_2, 0], [self.hsv_1, self.hsv_2, 1]))
        else:
            sss_hsv1 = bg_alpha
            sss_hsv2 = bg_alpha
            sss_hsv3 = bg_alpha
        # HSL
        if (self.layout.hsl.isChecked() == True and self.layout.gray_sliders.isChecked() == False):
            sss_hsl1 = str(self.HUE_Gradient("HSL", self.layout.hsl_1_slider.width(), [0, self.hsl_2, self.hsl_3], [1, self.hsl_2, self.hsl_3]))
            sss_hsl2 = str(self.HSL_Gradient(self.layout.hsl_2_slider.width(), [self.hsl_1, 0, self.hsl_3], [self.hsl_1, 1, self.hsl_3]))
            sss_hsl3 = str(self.HSL_Gradient(self.layout.hsl_3_slider.width(), [self.hsl_1, self.hsl_2, 0], [self.hsl_1, self.hsl_2, 1]))
        else:
            sss_hsl1 = bg_alpha
            sss_hsl2 = bg_alpha
            sss_hsl3 = bg_alpha
        # CMYK
        if (self.layout.cmyk.isChecked() == True and self.layout.gray_sliders.isChecked() == False):
            sss_cmyk1 = str(self.CMYK_Gradient(self.layout.cmyk_1_slider.width(), [0, self.cmyk_2, self.cmyk_3, self.cmyk_4], [1, self.cmyk_2, self.cmyk_3, self.cmyk_4]))
            sss_cmyk2 = str(self.CMYK_Gradient(self.layout.cmyk_2_slider.width(), [self.cmyk_1, 0, self.cmyk_3, self.cmyk_4], [self.cmyk_1, 1, self.cmyk_3, self.cmyk_4]))
            sss_cmyk3 = str(self.CMYK_Gradient(self.layout.cmyk_3_slider.width(), [self.cmyk_1, self.cmyk_2, 0, self.cmyk_4], [self.cmyk_1, self.cmyk_2, 1, self.cmyk_4]))
            sss_cmyk4 = str(self.CMYK_Gradient(self.layout.cmyk_4_slider.width(), [self.cmyk_1, self.cmyk_2, self.cmyk_3, 0], [self.cmyk_1, self.cmyk_2, self.cmyk_3, 1]))
        else:
            sss_cmyk1 = bg_alpha
            sss_cmyk2 = bg_alpha
            sss_cmyk3 = bg_alpha
            sss_cmyk4 = bg_alpha
        # Hex Color
        hex = self.Pigment_2_HEX()
        self.layout.hex_string.setText(str(hex))
        # Panel Display
        panel = self.layout.panel.currentText()
        # Colors for Panels
        if panel == "PANEL":
            self.layout.panel_fgc.setStyleSheet(bg_unseen)
        # Foreground Color
        if panel == "FGC":
            if self.layout.gray_panels.isChecked() == False:
                foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.rgb_1*hexRGB, self.rgb_2*hexRGB, self.rgb_3*hexRGB))
                self.layout.panel_fgc.setStyleSheet(foreground_color)
            if self.layout.gray_panels.isChecked() == True:
                foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*kritaRGB, self.aaa_1*kritaRGB, self.aaa_1*kritaRGB))
                self.layout.panel_fgc.setStyleSheet(foreground_color)
        else:
            self.layout.panel_fgc.setStyleSheet(bg_unseen)
        # HSV Color
        if panel == "HSV":
            if self.layout.gray_panels.isChecked() == False:
                hue_left = [self.hsv_1, 0, 1]
                hue_right = [self.hsv_1, 1, 1]
                base_color = self.HSV_Gradient(self.layout.hsv_1_slider.width(), hue_left, hue_right)
                self.layout.panel_hsv.setStyleSheet(base_color)
                base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
                self.layout.panel_hsv_1.setStyleSheet(base_value)
            if self.layout.gray_panels.isChecked() == True:
                self.layout.panel_hsv.setStyleSheet(bg_unseen)
                base_value = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*hexRGB, self.aaa_1*hexRGB, self.aaa_1*hexRGB))
                self.layout.panel_hsv_1.setStyleSheet(base_value)
        else:
            self.layout.panel_hsv.setStyleSheet(bg_unseen)
            self.layout.panel_hsv_1.setStyleSheet(bg_unseen)
        # HSL Color
        if panel == "HSL":
            if self.layout.gray_panels.isChecked() == False:
                hue_left = [self.hsl_1, 0, 0.5]
                hue_right = [self.hsl_1, 1, 0.5]
                base_color = self.HSL_Gradient(self.layout.hsl_1_slider.width(), hue_left, hue_right)
                self.layout.panel_hsl.setStyleSheet(base_color)
                base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.5 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
                self.layout.panel_hsl_1.setStyleSheet(base_value)
            if self.layout.gray_panels.isChecked() == True:
                self.layout.panel_hsl.setStyleSheet(bg_unseen)
                base_value = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*hexRGB, self.aaa_1*hexRGB, self.aaa_1*hexRGB))
                self.layout.panel_hsl_1.setStyleSheet(base_value)
        else:
            self.layout.panel_hsl.setStyleSheet(bg_unseen)
            self.layout.panel_hsl_1.setStyleSheet(bg_unseen)
        # ARD Color
        if panel == "ARD":
            if self.layout.gray_panels.isChecked() == False:
                self.ARD_Triangle_Points()
                # Black and White Gradient
                base_color = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(0, 0, 0, 255)); }")
                self.layout.panel_ard_bg.setStyleSheet(base_color)
                hue = self.hsv_to_rgb(self.ard_1, 1, 1)
                base_value = (
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(%f, %f, %f, 0), stop:1 rgba(%f, %f, %f, 255)); "
                % (hue[0]*255, hue[1]*255, hue[2]*255, hue[0]*255, hue[1]*255, hue[2]*255)
                )
                self.layout.panel_ard_fg.setStyleSheet(base_value)
            if self.layout.gray_panels.isChecked() == True:
                base_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*hexRGB, self.aaa_1*hexRGB, self.aaa_1*hexRGB))
                self.layout.panel_ard_bg.setStyleSheet(base_color)
                self.layout.panel_ard_fg.setStyleSheet(bg_unseen)
        else:
            self.layout.panel_ard_bg.setStyleSheet(bg_unseen)
            self.layout.panel_ard_fg.setStyleSheet(bg_unseen)
        # UVD Color
        if panel == "UVD":
            if self.layout.gray_panels.isChecked() == False:
                self.UVD_Update()
            if self.layout.gray_panels.isChecked() == True:
                self.UVD_Update()
        else:
            self.layout.panel_uvd_mask.setStyleSheet(bg_unseen)
            self.layout.panel_uvd_input.setStyleSheet(bg_unseen)
        # Object
        object = self.layout.obj.currentText()
        if (object != "OBJECT"):
            self.Object_Live()
            self.Object_Render()
            self.Object_Alpha()
        # Apply ALL Channel Style Sheets
        self.layout.sof_1_slider.setStyleSheet(bg_alpha)
        self.layout.sof_2_slider.setStyleSheet(bg_alpha)
        self.layout.sof_3_slider.setStyleSheet(bg_alpha)
        self.layout.aaa_1_slider.setStyleSheet(sss_aaa)
        self.layout.rgb_1_slider.setStyleSheet(sss_rgb1)
        self.layout.rgb_2_slider.setStyleSheet(sss_rgb2)
        self.layout.rgb_3_slider.setStyleSheet(sss_rgb3)
        self.layout.ard_1_slider.setStyleSheet(sss_ard1)
        self.layout.ard_2_slider.setStyleSheet(sss_ard2)
        self.layout.ard_3_slider.setStyleSheet(sss_ard3)
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
    def Pigment_Display_Release(self, SIGNAL_RELEASE):
        # Localized color values
        self.rgb_1 = self.rgb_1
        self.rgb_2 = self.rgb_2
        self.rgb_3 = self.rgb_3
        # Correct out of Bound values
        if self.rgb_1 <= 0:
            self.rgb_1 = 0
        if self.rgb_1 >= 1:
            self.rgb_1 = 1
        if self.rgb_2 <= 0:
            self.rgb_2 = 0
        if self.rgb_2 >= 1:
            self.rgb_2 = 1
        if self.rgb_3 <= 0:
            self.rgb_3 = 0
        if self.rgb_3 >= 1:
            self.rgb_3 = 1
        # Dusplay Release Color
        active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_1*hexRGB, self.rgb_2*hexRGB, self.rgb_3*hexRGB))
        self.layout.color_2.setStyleSheet(active_color_2)
    def Ratio(self):
        # Relocate SOF Handle due to Size Variation
        self.sof_1_slider.Update(self.sof_1 / kritaS, self.layout.sof_1_slider.width())
        self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width())
        self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width())
        # Relocate Channel Handle due to Size Variation
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
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
        self.mixer_ard_g1.Update(self.percentage_ard_g1, self.layout.ard_g1.width())
        self.mixer_ard_g2.Update(self.percentage_ard_g2, self.layout.ard_g2.width())
        self.mixer_ard_g3.Update(self.percentage_ard_g3, self.layout.ard_g3.width())
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())
        # Relocate Object Alpha Handle due to Size Variation
        if self.layout.obj.currentText() != "OBJECT":
            self.Object_Render()
            self.Object_Alpha()
        # UVD Panel Ratio Adjust to maintain Square
        uvd_width = self.layout.panel_uvd.width()
        uvd_height = self.layout.panel_uvd.height()
        # For when UVD Panle is Minimized
        if uvd_width <= 0:
            uvd_width = 1
        if uvd_height <= 0:
            uvd_height = 1
        # Shape Mask like a Perfect Square
        if uvd_width >= uvd_height:
            self.layout.panel_uvd_mask.setMaximumWidth(uvd_height)
            self.layout.panel_uvd_mask.setMaximumHeight(uvd_height)
        elif uvd_width < uvd_height:
            self.layout.panel_uvd_mask.setMaximumWidth(uvd_width)
            self.layout.panel_uvd_mask.setMaximumHeight(uvd_width)

        # Relocate Panel Cursor due to Size Variation
        self.UVD_Update()
        self.ARD_Update()
        self.panel_hsv.Update_Panel(self.hsv_2, self.hsv_3, self.layout.panel_hsv_1.width(), self.layout.panel_hsv_1.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        self.panel_hsl.Update_Panel(self.hsl_2, self.hsl_3, self.layout.panel_hsl_1.width(), self.layout.panel_hsl_1.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        # Update Display
        self.Pigment_Display()
    # RGB Update
    def RGB_R_Color(self, red):
        pass
    def RGB_G_Color(self, green):
        pass
    def RGB_B_Color(self, blue):
        pass
    def RGB_Gray(self, value):
        pass
    # UVD Display
    def UVD_Update(self):
        # UVD points of interest
        self.UVD_Hexagon_Points()
        # Masking
        hexagon = QPolygon([
            QPoint(self.P1[0], self.P1[1]),
            QPoint(self.P2[0], self.P2[1]),
            QPoint(self.P3[0], self.P3[1]),
            QPoint(self.P4[0], self.P4[1]),
            QPoint(self.P5[0], self.P5[1]),
            QPoint(self.P6[0], self.P6[1]),
            ])
        self.layout.panel_uvd_mask.setMask(QRegion(hexagon))
        # Update Panel
        self.panel_uvd.Update_Panel(
            self.uvd_1, self.uvd_2, self.uvd_3,
            self.PCC,
            self.P1, self.P2, self.P3, self.P4, self.P5, self.P6,
            self.P12, self.P23, self.P34, self.P45, self.P56, self.P61,
            self.width, self.height,
            self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom
            )
    def UVD_Hexagon_Points(self):
        # Calculate Original Points
        self.uvd_hexagon_origins()
        # Panel Dimensions
        self.width = self.layout.panel_uvd_mask.width()
        self.height = self.layout.panel_uvd_mask.height()
        w2 = self.width / 2
        h2 = self.height / 2
        # Single Points
        self.P1 = [w2 + (self.O1[0] * w2), h2 + (self.O1[1] * h2)]
        self.P2 = [w2 + (self.O2[0] * w2), h2 + (self.O2[1] * h2)]
        self.P3 = [w2 + (self.O3[0] * w2), h2 + (self.O3[1] * h2)]
        self.P4 = [w2 + (self.O4[0] * w2), h2 + (self.O4[1] * h2)]
        self.P5 = [w2 + (self.O5[0] * w2), h2 + (self.O5[1] * h2)]
        self.P6 = [w2 + (self.O6[0] * w2), h2 + (self.O6[1] * h2)]
        # Composed Points
        self.PCC = [w2 + (self.OCC[0] * w2), h2 + (self.OCC[1] * h2)]
        self.P12 = [w2 + (self.O12[0] * w2), h2 + (self.O12[1] * h2)]
        self.P23 = [w2 + (self.O23[0] * w2), h2 + (self.O23[1] * h2)]
        self.P34 = [w2 + (self.O34[0] * w2), h2 + (self.O34[1] * h2)]
        self.P45 = [w2 + (self.O45[0] * w2), h2 + (self.O45[1] * h2)]
        self.P56 = [w2 + (self.O56[0] * w2), h2 + (self.O56[1] * h2)]
        self.P61 = [w2 + (self.O61[0] * w2), h2 + (self.O61[1] * h2)]
    def UVD_Color(self, rgb_d):
        # Measures
        self.width = self.layout.panel_uvd_mask.width()
        self.height = self.layout.panel_uvd_mask.height()
        w2 = 0.5 * self.width
        h2 = 0.5 * self.height
        # Create and format the Image
        self.image = QImage(self.width, self.height, QImage.Format_RGB32)
        # Cycle through Pixels
        for w in range(self.width):
            for h in range(self.height):
                # Consider pixel location and its location color
                u = (w-w2)/w2
                v = (h-h2)/h2
                d = self.uvd_3
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
                color = qRgb(r*hexRGB, g*hexRGB, b*hexRGB)
                self.image.setPixel(w, h, color)
        self.layout.panel_uvd_input.setPixmap(QPixmap(self.image))
    def UVD_Gray(self, rgb_d):
        # Measures
        self.width = self.layout.panel_uvd_mask.width()
        self.height = self.layout.panel_uvd_mask.height()
        w2 = 0.5 * self.width
        h2 = 0.5 * self.height
        # Verify UVD D change with previous selected color to see if it is worth changing
        self.image = QImage(self.width, self.height, QImage.Format_RGB32)
        # Cycle through Pixels
        for w in range(self.width):
            for h in range(self.height):
                color = qRgb(rgb_d*hexRGB, rgb_d*hexRGB, rgb_d*hexRGB)
                self.image.setPixel(w, h, color)
        self.layout.panel_uvd_input.setPixmap(QPixmap(self.image))
    def UVD_Release(self):
        # UVD Panel Update Color Display
        if self.layout.gray_panels.isChecked() == False:
            self.UVD_Color(self.uvd_3)
        if self.layout.gray_panels.isChecked() == True:
            self.UVD_Gray(self.uvd_3)
        # Label Percent Clean
        self.layout.label_percent.setText("")
    # ARD Display
    def ARD_Update(self):
        panel = self.layout.panel.currentText()
        if panel == "ARD":
            # ARD points of intrest
            self.ARD_Triangle_Points()
            # Masking
            triangle = QPolygon([
                QPoint(self.T1[0], self.T1[1]),
                QPoint(self.T2[0], self.T2[1]*self.ard_mask_h),
                QPoint(self.T3[0]*self.ard_mask_w, self.T3[1]*self.ard_mask_h),
                ])
            self.layout.panel_ard_mask.setMask(QRegion(triangle))
            # Update Panel
            self.panel_ard.Update_Panel(
                self.ard_2, self.ard_3,
                self.T1, self.T2, self.T3, self.cross,
                self.ard_mask_w, self.ard_mask_h,
                self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom
                )
    def ARD_Triangle_Points(self):
        # Mask
        self.ard_mask_w = self.layout.panel_ard_mask.width()
        self.ard_mask_h = self.layout.panel_ard_mask.height()
        hue = self.ard_1*360
        if hue < 0:
            value = 60
        if (hue >= 0 and hue < 60):
            value = 60 + (hue-0)
        if (hue >= 60 and hue < 120):
            value = 120 - (hue-60)
        if (hue >= 120 and hue < 180):
            value = 60 + (hue-120)
        if (hue >= 180 and hue < 240):
            value = 120 - (hue-180)
        if (hue >= 240 and hue < 300):
            value = 60 + (hue-240)
        if (hue >= 300 and hue < 360):
            value = 120 - (hue-300)
        if hue >= 360:
            value = 60
        vertex = 1 - (round(value) / 180)
        # Triangle
        self.T1 = [0, 0]
        self.T2 = [0 , 1]
        self.T3 = [1, vertex]
        # Intersection
        ddd = 1 - self.ard_3
        if ddd < vertex:
            self.cross = self.intersection(0,0,1,vertex, 0,ddd,1,ddd)
        elif ddd > vertex:
            self.cross = self.intersection(0,1,1,vertex, 0,ddd,1,ddd)
        else:
            self.cross = [1, ddd]

    #//
    #\\ Hex Codes ##############################################################
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
        aaa1 = self.aaa_1 * hexAAA
        rgb1 = self.rgb_1 * hexRGB
        rgb2 = self.rgb_2 * hexRGB
        rgb3 = self.rgb_3 * hexRGB
        cmyk1 = self.cmyk_1 * hexCMYK
        cmyk2 = self.cmyk_2 * hexCMYK
        cmyk3 = self.cmyk_3 * hexCMYK
        cmyk4 = self.cmyk_4 * hexCMYK
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
    def HEX_6(self, red, green, blue):
        # Transform into HEX
        hex1 = str(hex(int(red * hexRGB)))[2:4].zfill(2)
        hex2 = str(hex(int(green * hexRGB)))[2:4].zfill(2)
        hex3 = str(hex(int(blue * hexRGB)))[2:4].zfill(2)
        pigment_hex = str("#"+hex1+hex2+hex3)
        return pigment_hex

    #//
    #\\ Pigment SOF ############################################################
    def SOF_1_APPLY(self, value):
        self.sof_1 = value
        self.sof_1_slider.Update(value / kritaS, self.layout.sof_1_slider.width())
        self.layout.sof_1_value.setValue(value)
    def SOF_2_APPLY(self, value):
        self.sof_2 = value
        self.sof_2_slider.Update(value, self.layout.sof_2_slider.width())
        self.layout.sof_2_value.setValue(value * kritaO)
    def SOF_3_APPLY(self, value):
        self.sof_3 = value
        self.sof_3_slider.Update(value, self.layout.sof_3_slider.width())
        self.layout.sof_3_value.setValue(value * kritaF)

    def Pigment_SOF_1_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = SIGNAL_VALUE * kritaS
            self.layout.sof_1_value.setValue(self.sof_1)
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
                Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
        else:
            self.sof_1 = self.lock_size
            self.sof_1_slider.Update(self.sof_1 / kritaS, self.layout.sof_1_slider.width())
            self.layout.sof_1_value.setValue(self.sof_1)
        self.update()
    def Pigment_SOF_2_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = SIGNAL_VALUE
            self.layout.sof_2_value.setValue(self.sof_2 * kritaO)
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
                Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
        else:
            self.sof_2 = self.lock_opacity
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width())
            self.layout.sof_2_value.setValue(self.sof_2 * kritaO)
        self.update()
    def Pigment_SOF_3_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = SIGNAL_VALUE
            self.layout.sof_3_value.setValue(self.sof_3 * kritaF)
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
                Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
        else:
            self.sof_3 = self.lock_flow
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width())
            self.layout.sof_3_value.setValue(self.sof_3 * kritaF)
        self.update()

    def Pigment_SOF_1_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.layout.sof_1_value.value()
            self.sof_1_slider.Update(self.sof_1 / kritaS, self.layout.sof_1_slider.width())
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
                Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
        else:
            self.sof_1 = self.lock_size
            self.sof_1_slider.Update(self.sof_1 / kritaS, self.layout.sof_1_slider.width())
            self.layout.sof_1_value.setValue(self.sof_1)
        self.update()
    def Pigment_SOF_2_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.layout.sof_2_value.value() / kritaO
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width())
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
                Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
        else:
            self.sof_2 = self.lock_opacity
            self.sof_2_slider.Update(self.sof_2, self.layout.sof_2_slider.width())
            self.layout.sof_2_value.setValue(self.sof_2 * kritaO)
        self.update()
    def Pigment_SOF_3_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.layout.sof_3_value.value() / kritaF
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width())
            state = self.layout.check.checkState()
            if (state == 1 or state == 2):
                Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
        else:
            self.sof_3 = self.lock_flow
            self.sof_3_slider.Update(self.sof_3, self.layout.sof_3_slider.width())
            self.layout.sof_3_value.setValue(self.sof_3 * kritaF)
        self.update()

    #//
    #\\ Pigment Channels #######################################################
    def Pigment_AAA_1_Half(self):
        self.aaa_1 = half
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaAAA)
        self.Pigment_Convert_AAA()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_1_Half(self):
        self.rgb_1 = half
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_2_Half(self):
        self.rgb_2 = half
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_3_Half(self):
        self.rgb_3 = half
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_1_Half(self):
        # Nearest Pure Color Pick
        ang = self.ard_1 * 360
        if (ang >= 0 and ang <= 30):
            ang = 0
        elif (ang > 30 and ang <= 90):
            ang = 60
        elif (ang > 90 and ang <= 150):
            ang = 120
        elif (ang > 150 and ang <= 210):
            ang = 180
        elif (ang > 210 and ang <= 270):
            ang = 240
        elif (ang > 270 and ang <= 330):
            ang = 300
        elif (ang > 330 and ang <= 360):
            ang = 360
        # Apply Hue
        self.ard_1_slider.Update(ang/360, self.layout.hsv_1_slider.width())
        self.layout.ard_1_value.setValue((ang/360) * kritaANG)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_2_Half(self):
        self.ard_2 = half
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.ard_2_value.setValue(self.ard_2 * kritaRDL)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_3_Half(self):
        # Nearest Pure Color Pick
        diagonal = self.ard_3 * 360
        if (diagonal >= 0 and diagonal <= 30):
            diagonal = 0
        elif (diagonal > 30 and diagonal <= 90):
            diagonal = 60
        elif (diagonal > 90 and diagonal <= 150):
            diagonal = 120
        elif (diagonal > 150 and diagonal <= 210):
            diagonal = 180
        elif (diagonal > 210 and diagonal <= 270):
            diagonal = 240
        elif (diagonal > 270 and diagonal <= 330):
            diagonal = 300
        elif (diagonal > 330 and diagonal <= 360):
            diagonal = 360
        # Apply Hue
        self.ard_3_slider.Update(diagonal/360, self.layout.hsv_1_slider.width())
        self.layout.ard_3_value.setValue((diagonal/360) * kritaRDL)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_1_Half(self):
        # Nearest Pure Color Pick
        hue = self.hsv_1 * 360
        if (hue >= 0 and hue <= 30):
            hue = 0
        elif (hue > 30 and hue <= 90):
            hue = 60
        elif (hue > 90 and hue <= 150):
            hue = 120
        elif (hue > 150 and hue <= 210):
            hue = 180
        elif (hue > 210 and hue <= 270):
            hue = 240
        elif (hue > 270 and hue <= 330):
            hue = 300
        elif (hue > 330 and hue <= 360):
            hue = 360
        # Apply Hue
        self.hsv_1_slider.Update(hue/360, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue((hue/360) * kritaHUE)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_2_Half(self):
        self.hsv_2 = half
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVL)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_3_Half(self):
        self.hsv_3 = half
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVL)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_1_Half(self):
        # Nearest Pure Color Pick
        hue = self.hsl_1 * 360
        if (hue >= 0 and hue <= 30):
            hue = 0
        elif (hue > 30 and hue <= 90):
            hue = 60
        elif (hue > 90 and hue <= 150):
            hue = 120
        elif (hue > 150 and hue <= 210):
            hue = 180
        elif (hue > 210 and hue <= 270):
            hue = 240
        elif (hue > 270 and hue <= 330):
            hue = 300
        elif (hue > 330 and hue <= 360):
            hue = 360
        # Apply Hue
        self.hsl_1_slider.Update(hue/360, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue((hue/360) * kritaHUE)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_2_Half(self):
        self.hsl_2 = half
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVL)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_3_Half(self):
        self.hsl_3 = half
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVL)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_1_Half(self):
        self.cmyk_1 = half
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_2_Half(self):
        self.cmyk_2 = half
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_3_Half(self):
        self.cmyk_3 = half
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_4_Half(self):
        self.cmyk_4 = half
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()

    def Pigment_AAA_1_Minus(self):
        self.aaa_1 = self.aaa_1 - unitRGB
        if self.aaa_1 <= zero:
            self.aaa_1 = zero
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaRGB)
        self.Pigment_Convert_AAA()
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Minus(self):
        self.rgb_1 = self.rgb_1 - unitRGB
        if self.rgb_1 <= zero:
            self.rgb_1 = zero
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Minus(self):
        self.rgb_2 = self.rgb_2 - unitRGB
        if self.rgb_2 <= zero:
            self.rgb_2 = zero
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Minus(self):
        self.rgb_3 = self.rgb_3 - unitRGB
        if self.rgb_3 <= zero:
            self.rgb_3 = zero
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Minus(self):
        self.ard_1 = self.ard_1 - unitANG
        if self.ard_1 <= zero:
            self.ard_1 = zero
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.layout.ard_1_value.setValue(self.ard_1 * kritaANG)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Minus(self):
        self.ard_2 = self.ard_2 - unitRDL
        if self.ard_2 <= zero:
            self.ard_2 = zero
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.ard_2_value.setValue(self.ard_2 * kritaRDL)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Minus(self):
        self.ard_3 = self.ard_3 - unitRDL
        if self.ard_3 <= zero:
            self.ard_3 = zero
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
        self.layout.ard_3_value.setValue(self.ard_3 * kritaRDL)
        self.Pigment_Convert_ARD(1)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Minus(self):
        self.hsv_1 = self.hsv_1 - unitHUE
        if self.hsv_1 <= zero:
            self.hsv_1 = zero
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Minus(self):
        self.hsv_2 = self.hsv_2 - unitSVL
        if self.hsv_2 <= zero:
            self.hsv_2 = zero
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVL)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Minus(self):
        self.hsv_3 = self.hsv_3 - unitSVL
        if self.hsv_3 <= zero:
            self.hsv_3 = zero
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVL)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Minus(self):
        self.hsl_1 = self.hsl_1 - unitHUE
        if self.hsl_1 <= zero:
            self.hsl_1 = zero
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Minus(self):
        self.hsl_2 = self.hsl_2 - unitSVL
        if self.hsl_2 <= zero:
            self.hsl_2 = zero
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVL)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Minus(self):
        self.hsl_3 = self.hsl_3 - unitSVL
        if self.hsl_3 <= zero:
            self.hsl_3 = zero
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVL)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Minus(self):
        self.cmyk_1 = self.cmyk_1 - unitCMYK
        if self.cmyk_1 <= zero:
            self.cmyk_1 = zero
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Minus(self):
        self.cmyk_2 = self.cmyk_2 - unitCMYK
        if self.cmyk_2 <= zero:
            self.cmyk_2 = zero
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Minus(self):
        self.cmyk_3 = self.cmyk_3 - unitCMYK
        if self.cmyk_3 <= zero:
            self.cmyk_3 = zero
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Minus(self):
        self.cmyk_4 = self.cmyk_4 - unitCMYK
        if self.cmyk_4 <= zero:
            self.cmyk_4 = zero
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Plus(self):
        self.aaa_1 = self.aaa_1 + unitAAA
        if self.aaa_1 >= unit:
            self.aaa_1 = unit
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaAAA)
        self.Pigment_Convert_AAA()
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Plus(self):
        self.rgb_1 = self.rgb_1 + unitRGB
        if self.rgb_1 >= unit:
            self.rgb_1 = unit
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Plus(self):
        self.rgb_2 = self.rgb_2 + unitRGB
        if self.rgb_2 >= unit:
            self.rgb_2 = unit
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Plus(self):
        self.rgb_3 = self.rgb_3 + unitRGB
        if self.rgb_3 >= unit:
            self.rgb_3 = unit
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Plus(self):
        self.ard_1 = self.ard_1 + unitANG
        if self.ard_1 >= unit:
            self.ard_1 = unit
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.layout.ard_1_value.setValue(self.ard_1 * kritaANG)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Plus(self):
        self.ard_2 = self.ard_2 + unitRDL
        if self.ard_2 >= unit:
            self.ard_2 = unit
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.ard_2_value.setValue(self.ard_2 * kritaRDL)
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Plus(self):
        self.ard_3 = self.ard_3 + unitRDL
        if self.ard_3 >= unit:
            self.ard_3 = unit
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
        self.layout.ard_3_value.setValue(self.ard_3 * kritaRDL)
        self.Pigment_Convert_ARD(1)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Plus(self):
        self.hsv_1 = self.hsv_1 + unitHUE
        if self.hsv_1 >= unit:
            self.hsv_1 = unit
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Plus(self):
        self.hsv_2 = self.hsv_2 + unitSVL
        if self.hsv_2 >= unit:
            self.hsv_2 = unit
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVL)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Plus(self):
        self.hsv_3 = self.hsv_3 + unitSVL
        if self.hsv_3 >= unit:
            self.hsv_3 = unit
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVL)
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Plus(self):
        self.hsl_1 = self.hsl_1 + unitHUE
        if self.hsl_1 >= unit:
            self.hsl_1 = unit
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Plus(self):
        self.hsl_2 = self.hsl_2 + unitSVL
        if self.hsl_2 >= unit:
            self.hsl_2 = unit
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVL)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Plus(self):
        self.hsl_3 = self.hsl_3 + unitSVL
        if self.hsl_3 >= unit:
            self.hsl_3 = unit
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVL)
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Plus(self):
        self.cmyk_1 = self.cmyk_1 + unitCMYK
        if self.cmyk_1 >= unit:
            self.cmyk_1 = unit
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Plus(self):
        self.cmyk_2 = self.cmyk_2 + unitCMYK
        if self.cmyk_2 >= unit:
            self.cmyk_2 = unit
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Plus(self):
        self.cmyk_3 = self.cmyk_3 + unitCMYK
        if self.cmyk_3 >= unit:
            self.cmyk_3 = unit
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Plus(self):
        self.cmyk_4 = self.cmyk_4 + unitCMYK
        if self.cmyk_4 >= unit:
            self.cmyk_4 = unit
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)

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
    def Pigment_ARD_1_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_1 = SIGNAL_VALUE
        send = int(self.ard_1 * kritaANG)
        self.layout.ard_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert_ARD(0)
    def Pigment_ARD_2_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_2 = SIGNAL_VALUE
        send = int(self.ard_2 * kritaRDL)
        self.layout.ard_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_ARD(0)
    def Pigment_ARD_3_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_3 = SIGNAL_VALUE
        send = int(self.ard_3 * kritaRDL)
        self.layout.ard_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert_ARD(0)
    def Pigment_HSV_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_1 = SIGNAL_VALUE
        send = int(self.hsv_1 * kritaHUE)
        self.layout.hsv_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
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
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
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
        self.zoom = 0
        self.Pigment_Convert_AAA()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_4_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()

    def Pigment_Panel_Zoom(self, SIGNAL_ZOOM):
        self.zoom = SIGNAL_ZOOM

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
    def Pigment_ARD_1_Value_Modify(self):
        self.ard_1 = self.layout.ard_1_value.value() / kritaANG
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.layout.label_percent.setText(str(round(self.ard_1*100,2))+" º")
        self.Pigment_Convert_ARD(0)
    def Pigment_ARD_2_Value_Modify(self):
        self.ard_2 = self.layout.ard_2_value.value() / kritaRDL
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.label_percent.setText(str(round(self.ard_2*100,2))+" %")
        self.Pigment_Convert_ARD(0)
    def Pigment_ARD_3_Value_Modify(self):
        self.ard_3 = self.layout.ard_3_value.value() / kritaRDL
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
        self.layout.label_percent.setText(str(round(self.ard_3*100,2))+" %")
        self.Pigment_Convert_ARD(0)
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
        self.Pigment_Convert_AAA()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_1_Value_Release(self):
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_2_Value_Release(self):
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_RGB_3_Value_Release(self):
        self.Pigment_Convert_RGB()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_1_Value_Release(self):
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_2_Value_Release(self):
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_ARD_3_Value_Release(self):
        self.Pigment_Convert_ARD(0)
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_1_Value_Release(self):
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_2_Value_Release(self):
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSV_3_Value_Release(self):
        self.Pigment_Convert_HSV()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_1_Value_Release(self):
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_2_Value_Release(self):
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_HSL_3_Value_Release(self):
        self.Pigment_Convert_HSL()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_1_Value_Release(self):
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_2_Value_Release(self):
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_3_Value_Release(self):
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()
    def Pigment_CMYK_4_Value_Release(self):
        self.Pigment_Convert_CMYK()
        self.Pigment_Display_Release(0)
        self.UVD_Release()

    #//
    #\\ Brush Settings #########################################################
    def Brush_Lock_APPLY(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.view = Krita.instance().activeWindow().activeView()
            self.view.setBrushSize(self.lock_size)
            self.view.setPaintingOpacity(self.lock_opacity)
            self.view.setPaintingFlow(self.lock_flow)
            self.tip_00.Setup_SOF(self.lock_size, self.lock_opacity, self.lock_flow)
            self.SOF_1_APPLY(self.lock_size)
            self.SOF_2_APPLY(self.lock_opacity)
            self.SOF_3_APPLY(self.lock_flow)
            self.Pigment_Display()
    def Brush_Lock_SAVE(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.view = Krita.instance().activeWindow().activeView()
            self.lock_size = self.view.brushSize()
            self.lock_opacity = self.view.paintingOpacity()
            self.lock_flow = self.view.paintingFlow()
            self.tip_00.Setup_SOF(self.lock_size, self.lock_opacity, self.lock_flow)
            self.Settings_Save()
    def Brush_Lock_CLEAN(self, SIGNAL_CLICKS):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.view = Krita.instance().activeWindow().activeView()
            self.lock_size = size
            self.lock_opacity = opacity
            self.lock_flow = flow
            self.view.setBrushSize(self.lock_size)
            self.view.setPaintingOpacity(self.lock_opacity)
            self.view.setPaintingFlow(self.lock_flow)
            self.tip_00.Setup_SOF(size, opacity, flow)
            self.SOF_1_APPLY(self.lock_size)
            self.SOF_2_APPLY(self.lock_opacity)
            self.SOF_3_APPLY(self.lock_flow)
            self.Pigment_Display()
            self.Settings_Save()

    #//
    #\\ Palette ################################################################
    def Color_00_APPLY(self, SIGNAL_CLICKS):
        if self.color_00[0] == "True":
            self.Color_RGB(self.color_00[1], self.color_00[2], self.color_00[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Color_00_SAVE(self, SIGNAL_CLICKS):
        self.color_00 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_01_SAVE(self, SIGNAL_CLICKS):
        self.color_01 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_02_SAVE(self, SIGNAL_CLICKS):
        self.color_02 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_03_SAVE(self, SIGNAL_CLICKS):
        self.color_03 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_04_SAVE(self, SIGNAL_CLICKS):
        self.color_04 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_05_SAVE(self, SIGNAL_CLICKS):
        self.color_05 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_06_SAVE(self, SIGNAL_CLICKS):
        self.color_06 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_07_SAVE(self, SIGNAL_CLICKS):
        self.color_07 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_08_SAVE(self, SIGNAL_CLICKS):
        self.color_08 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_09_SAVE(self, SIGNAL_CLICKS):
        self.color_09 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.UVD_Release()
    def Color_10_SAVE(self, SIGNAL_CLICKS):
        self.color_10 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Save()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_10[1]*hexRGB, self.color_10[2]*hexRGB, self.color_10[3]*hexRGB))
        self.layout.cor_10.setStyleSheet(color)
    def Color_10_CLEAN(self, SIGNAL_CLICKS):
        self.color_10 = ["False", 0, 0, 0]
        self.Settings_Save()
        self.layout.cor_10.setStyleSheet(bg_alpha)

    #//
    #\\ Mixer COLOR ############################################################
    def Mixer_TTS_APPLY(self, SIGNAL_APPLY):
        if self.color_tts[0] == "True":
            self.Color_RGB(self.color_tts[1], self.color_tts[2], self.color_tts[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_TTS_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_tts = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_RGB_L1_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_RGB_R1_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_RGB_L2_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_RGB_R2_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_RGB_L3_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_RGB_R3_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
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

    def Mixer_ARD_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l1[0] == "True":
            self.Color_ARD(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l1 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.ard_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.ard_l1.setStyleSheet(bg_alpha)
        self.layout.ard_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_ard_g1 = 0
        self.mixer_ard_g1.Update(self.percentage_ard_g1, self.layout.ard_g1.width())

    def Mixer_ARD_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r1[0] == "True":
            self.Color_ARD(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r1 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.ard_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.layout.ard_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_ard_g1 = 0
        self.mixer_ard_g1.Update(self.percentage_ard_g1, self.layout.ard_g1.width())

    def Mixer_ARD_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l2[0] == "True":
            self.Color_ARD(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l2 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.ard_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.ard_l2.setStyleSheet(bg_alpha)
        self.layout.ard_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_ard_g2 = 0
        self.mixer_ard_g2.Update(self.percentage_ard_g2, self.layout.ard_g2.width())

    def Mixer_ARD_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r2[0] == "True":
            self.Color_ARD(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r2 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.ard_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.layout.ard_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_ard_g2 = 0
        self.mixer_ard_g2.Update(self.percentage_ard_g2, self.layout.ard_g2.width())

    def Mixer_ARD_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l3[0] == "True":
            self.Color_ARD(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l3 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.ard_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.ard_l3.setStyleSheet(bg_alpha)
        self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_ard_g3 = 0
        self.mixer_ard_g3.Update(self.percentage_ard_g3, self.layout.ard_g3.width())

    def Mixer_ARD_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r3[0] == "True":
            self.Color_ARD(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r3 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.ard_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_ard_g3 = 0
        self.mixer_ard_g3.Update(self.percentage_ard_g3, self.layout.ard_g3.width())

    def Mixer_HSV_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l1[0] == "True":
            self.Color_HSV(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSV_L1_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_l1 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Save()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsv_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l1 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_l1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r1[0] == "True":
            self.Color_HSV(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSV_R1_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_r1 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Save()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsv_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r1 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l2[0] == "True":
            self.Color_HSV(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSV_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_l2 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Save()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsv_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l2 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_l2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r2[0] == "True":
            self.Color_HSV(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSV_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_r2 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Save()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsv_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r2 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l3[0] == "True":
            self.Color_HSV(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSV_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_l3 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Save()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsv_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l3 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_l3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSV_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r3[0] == "True":
            self.Color_HSV(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSV_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_r3 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Save()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsv_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r3 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSL_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l1[0] == "True":
            self.Color_HSL(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSL_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l1 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Save()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsl_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l1 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_l1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())

    def Mixer_HSL_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r1[0] == "True":
            self.Color_HSL(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSL_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r1 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Save()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsl_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r1 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())

    def Mixer_HSL_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l2[0] == "True":
            self.Color_HSL(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSL_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l2 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Save()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsl_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l2 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_l2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())

    def Mixer_HSL_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r2[0] == "True":
            self.Color_HSL(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSL_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r2 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Save()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsl_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r2 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())

    def Mixer_HSL_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l3[0] == "True":
            self.Color_HSL(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSL_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l3 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Save()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsl_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l3 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_l3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_HSL_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r3[0] == "True":
            self.Color_HSL(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_HSL_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r3 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Save()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.hsl_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r3 = ["False", 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_CMYK_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l1[0] == "True":
            self.Color_CMYK(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_CMYK_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l1 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Save()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.cmyk_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_l1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())

    def Mixer_CMYK_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r1[0] == "True":
            self.Color_CMYK(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_CMYK_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r1 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Save()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.cmyk_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())

    def Mixer_CMYK_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l2[0] == "True":
            self.Color_CMYK(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_CMYK_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l2 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Save()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.cmyk_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_l2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())

    def Mixer_CMYK_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r2[0] == "True":
            self.Color_CMYK(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_CMYK_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r2 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Save()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.cmyk_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())

    def Mixer_CMYK_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l3[0] == "True":
            self.Color_CMYK(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_CMYK_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l3 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Save()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.cmyk_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_l3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

    def Mixer_CMYK_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r3[0] == "True":
            self.Color_CMYK(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_CMYK_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r3 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Save()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*hexRGB, rgb[1]*hexRGB, rgb[2]*hexRGB))
        self.layout.cmyk_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
        self.Settings_Save()
        # Display
        self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

    #//
    #\\ Mixer Gradient #########################################################
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

    def Mixer_ARD_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_ard_g1 = SIGNAL_MIXER_VALUE / (self.layout.ard_g1.width())
        if self.color_ard_l1[1] <= self.color_ard_r1[1]:
            # Conditions
            cond1 = self.color_ard_r1[1] - self.color_ard_l1[1]
            cond2 = (self.color_ard_l1[1] + 1) - self.color_ard_r1[1]
            if cond1 <= cond2:
                a = self.color_ard_l1[1] + (self.percentage_ard_g1 * cond1)
            else:
                a = self.color_ard_l1[1] - (self.percentage_ard_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l1[1] - self.color_ard_r1[1]
            cond2 = (self.color_ard_r1[1] + 1) - self.color_ard_l1[1]
            if cond1 <= cond2:
                a = self.color_ard_l1[1] - (self.percentage_ard_g1 * cond1)
            else:
                a = self.color_ard_l1[1] + (self.percentage_ard_g1 * cond2)
        # Correct Excess
        if a < 0:
            a = a + 1
        if a > 1:
            a = a - 1
        ard1 = a
        ard2 = (self.color_ard_l1[2] + (self.percentage_ard_g1 * (self.color_ard_r1[2] - self.color_ard_l1[2])))
        ard3 = (self.color_ard_l1[3] + (self.percentage_ard_g1 * (self.color_ard_r1[3] - self.color_ard_l1[3])))
        # Send Values
        self.Color_ARD(ard1, ard2, ard3)
    def Mixer_ARD_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_ard_g2 = SIGNAL_MIXER_VALUE / (self.layout.ard_g2.width())
        if self.color_ard_l2[1] <= self.color_ard_r2[1]:
            # Conditions
            cond1 = self.color_ard_r2[1] - self.color_ard_l2[1]
            cond2 = (self.color_ard_l2[1] + 1) - self.color_ard_r2[1]
            if cond1 <= cond2:
                a = self.color_ard_l2[1] + (self.percentage_ard_g2 * cond1)
            else:
                a = self.color_ard_l2[1] - (self.percentage_ard_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l2[1] - self.color_ard_r2[1]
            cond2 = (self.color_ard_r2[1] + 1) - self.color_ard_l2[1]
            if cond1 <= cond2:
                a = self.color_ard_l2[1] - (self.percentage_ard_g2 * cond1)
            else:
                a = self.color_ard_l2[1] + (self.percentage_ard_g2 * cond2)
        # Correct Excess
        if a < 0:
            a = a + 1
        if a > 1:
            a = a - 1
        ard1 = a
        ard2 = (self.color_ard_l2[2] + (self.percentage_ard_g2 * (self.color_ard_r2[2] - self.color_ard_l2[2])))
        ard3 = (self.color_ard_l2[3] + (self.percentage_ard_g2 * (self.color_ard_r2[3] - self.color_ard_l2[3])))
        # Send Values
        self.Color_ARD(ard1, ard2, ard3)
    def Mixer_ARD_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_ard_g3 = SIGNAL_MIXER_VALUE / (self.layout.ard_g3.width())
        if self.color_ard_l3[1] <= self.color_ard_r3[1]:
            # Conditions
            cond1 = self.color_ard_r3[1] - self.color_ard_l3[1]
            cond2 = (self.color_ard_l3[1] + 1) - self.color_ard_r3[1]
            if cond1 <= cond2:
                a = self.color_ard_l3[1] + (self.percentage_ard_g3 * cond1)
            else:
                a = self.color_ard_l3[1] - (self.percentage_ard_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l3[1] - self.color_ard_r3[1]
            cond2 = (self.color_ard_r3[1] + 1) - self.color_ard_l3[1]
            if cond1 <= cond2:
                a = self.color_ard_l3[1] - (self.percentage_ard_g3 * cond1)
            else:
                a = self.color_ard_l3[1] + (self.percentage_ard_g3 * cond2)
        # Correct Excess
        if a < 0:
            a = a + 1
        if a > 1:
            a = a - 1
        ard1 = a
        ard2 = (self.color_ard_l3[2] + (self.percentage_ard_g3 * (self.color_ard_r3[2] - self.color_ard_l3[2])))
        ard3 = (self.color_ard_l3[3] + (self.percentage_ard_g3 * (self.color_ard_r3[3] - self.color_ard_l3[3])))
        # Send Values
        self.Color_ARD(ard1, ard2, ard3)

    def Mixer_HSV_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsv_g1 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g1.width())
        if self.color_hsv_l1[1] <= self.color_hsv_r1[1]:
            # Conditions
            cond1 = self.color_hsv_r1[1] - self.color_hsv_l1[1]
            cond2 = (self.color_hsv_l1[1] + 1) - self.color_hsv_r1[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l1[1] + (self.percentage_hsv_g1 * cond1)
            else:
                hue = self.color_hsv_l1[1] - (self.percentage_hsv_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsv_l1[1] - self.color_hsv_r1[1]
            cond2 = (self.color_hsv_r1[1] + 1) - self.color_hsv_l1[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l1[1] - (self.percentage_hsv_g1 * cond1)
            else:
                hue = self.color_hsv_l1[1] + (self.percentage_hsv_g1 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l1[2] + (self.percentage_hsv_g1 * (self.color_hsv_r1[2] - self.color_hsv_l1[2])))
        hsv3 = (self.color_hsv_l1[3] + (self.percentage_hsv_g1 * (self.color_hsv_r1[3] - self.color_hsv_l1[3])))
        # Send Values
        self.Color_HSV(hsv1, hsv2, hsv3)
    def Mixer_HSV_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsv_g2 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g2.width())
        if self.color_hsv_l2[1] <= self.color_hsv_r2[1]:
            # Conditions
            cond1 = self.color_hsv_r2[1] - self.color_hsv_l2[1]
            cond2 = (self.color_hsv_l2[1] + 1) - self.color_hsv_r2[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l2[1] + (self.percentage_hsv_g2 * cond1)
            else:
                hue = self.color_hsv_l2[1] - (self.percentage_hsv_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsv_l2[1] - self.color_hsv_r2[1]
            cond2 = (self.color_hsv_r2[1] + 1) - self.color_hsv_l2[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l2[1] - (self.percentage_hsv_g2 * cond1)
            else:
                hue = self.color_hsv_l2[1] + (self.percentage_hsv_g2 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l2[2] + (self.percentage_hsv_g2 * (self.color_hsv_r2[2] - self.color_hsv_l2[2])))
        hsv3 = (self.color_hsv_l2[3] + (self.percentage_hsv_g2 * (self.color_hsv_r2[3] - self.color_hsv_l2[3])))
        # Send Values
        self.Color_HSV(hsv1, hsv2, hsv3)
    def Mixer_HSV_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsv_g3 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g3.width())
        if self.color_hsv_l3[1] <= self.color_hsv_r3[1]:
            # Conditions
            cond1 = self.color_hsv_r3[1] - self.color_hsv_l3[1]
            cond2 = (self.color_hsv_l3[1] + 1) - self.color_hsv_r3[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l3[1] + (self.percentage_hsv_g3 * cond1)
            else:
                hue = self.color_hsv_l3[1] - (self.percentage_hsv_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsv_l3[1] - self.color_hsv_r3[1]
            cond2 = (self.color_hsv_r3[1] + 1) - self.color_hsv_l3[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l3[1] - (self.percentage_hsv_g3 * cond1)
            else:
                hue = self.color_hsv_l3[1] + (self.percentage_hsv_g3 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l3[2] + (self.percentage_hsv_g3 * (self.color_hsv_r3[2] - self.color_hsv_l3[2])))
        hsv3 = (self.color_hsv_l3[3] + (self.percentage_hsv_g3 * (self.color_hsv_r3[3] - self.color_hsv_l3[3])))
        # Send Values
        self.Color_HSV(hsv1, hsv2, hsv3)

    def Mixer_HSL_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsl_g1 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g1.width())
        if self.color_hsl_l1[1] <= self.color_hsl_r1[1]:
            # Conditions
            cond1 = self.color_hsl_r1[1] - self.color_hsl_l1[1]
            cond2 = (self.color_hsl_l1[1] + 1) - self.color_hsl_r1[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l1[1] + (self.percentage_hsl_g1 * cond1)
            else:
                hue = self.color_hsl_l1[1] - (self.percentage_hsl_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsl_l1[1] - self.color_hsl_r1[1]
            cond2 = (self.color_hsl_r1[1] + 1) - self.color_hsl_l1[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l1[1] - (self.percentage_hsl_g1 * cond1)
            else:
                hue = self.color_hsl_l1[1] + (self.percentage_hsl_g1 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l1[2] + (self.percentage_hsl_g1 * (self.color_hsl_r1[2] - self.color_hsl_l1[2])))
        hsl3 = (self.color_hsl_l1[3] + (self.percentage_hsl_g1 * (self.color_hsl_r1[3] - self.color_hsl_l1[3])))
        # Send Values
        self.Color_HSL(hsl1, hsl2, hsl3)
    def Mixer_HSL_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsl_g2 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g2.width())
        if self.color_hsl_l2[1] <= self.color_hsl_r2[1]:
            # Conditions
            cond1 = self.color_hsl_r2[1] - self.color_hsl_l2[1]
            cond2 = (self.color_hsl_l2[1] + 1) - self.color_hsl_r2[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l2[1] + (self.percentage_hsl_g2 * cond1)
            else:
                hue = self.color_hsl_l2[1] - (self.percentage_hsl_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsl_l2[1] - self.color_hsl_r2[1]
            cond2 = (self.color_hsl_r2[1] + 1) - self.color_hsl_l2[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l2[1] - (self.percentage_hsl_g2 * cond1)
            else:
                hue = self.color_hsl_l2[1] + (self.percentage_hsl_g2 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l2[2] + (self.percentage_hsl_g2 * (self.color_hsl_r2[2] - self.color_hsl_l2[2])))
        hsl3 = (self.color_hsl_l2[3] + (self.percentage_hsl_g2 * (self.color_hsl_r2[3] - self.color_hsl_l2[3])))
        # Send Values
        self.Color_HSL(hsl1, hsl2, hsl3)
    def Mixer_HSL_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_hsl_g3 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g3.width())
        if self.color_hsl_l3[1] <= self.color_hsl_r3[1]:
            # Conditions
            cond1 = self.color_hsl_r3[1] - self.color_hsl_l3[1]
            cond2 = (self.color_hsl_l3[1] + 1) - self.color_hsl_r3[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l3[1] + (self.percentage_hsl_g3 * cond1)
            else:
                hue = self.color_hsl_l3[1] - (self.percentage_hsl_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsl_l3[1] - self.color_hsl_r3[1]
            cond2 = (self.color_hsl_r3[1] + 1) - self.color_hsl_l3[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l3[1] - (self.percentage_hsl_g3 * cond1)
            else:
                hue = self.color_hsl_l3[1] + (self.percentage_hsl_g3 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l3[2] + (self.percentage_hsl_g3 * (self.color_hsl_r3[2] - self.color_hsl_l3[2])))
        hsl3 = (self.color_hsl_l3[3] + (self.percentage_hsl_g3 * (self.color_hsl_r3[3] - self.color_hsl_l3[3])))
        # Send Values
        self.Color_HSL(hsl1, hsl2, hsl3)

    def Mixer_CMYK_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_cmyk_g1 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g1.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l1[1] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[1] - self.color_cmyk_l1[1])))
        cmyk2 = (self.color_cmyk_l1[2] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[2] - self.color_cmyk_l1[2])))
        cmyk3 = (self.color_cmyk_l1[3] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[3] - self.color_cmyk_l1[3])))
        cmyk4 = (self.color_cmyk_l1[4] + (self.percentage_cmyk_g1 * (self.color_cmyk_r1[4] - self.color_cmyk_l1[4])))
        # Send Values
        self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_CMYK_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_cmyk_g2 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g2.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l2[1] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[1] - self.color_cmyk_l2[1])))
        cmyk2 = (self.color_cmyk_l2[2] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[2] - self.color_cmyk_l2[2])))
        cmyk3 = (self.color_cmyk_l2[3] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[3] - self.color_cmyk_l2[3])))
        cmyk4 = (self.color_cmyk_l2[4] + (self.percentage_cmyk_g2 * (self.color_cmyk_r2[4] - self.color_cmyk_l2[4])))
        # Send Values
        self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_CMYK_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_cmyk_g3 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g3.width())
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l3[1] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[1] - self.color_cmyk_l3[1])))
        cmyk2 = (self.color_cmyk_l3[2] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[2] - self.color_cmyk_l3[2])))
        cmyk3 = (self.color_cmyk_l3[3] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[3] - self.color_cmyk_l3[3])))
        cmyk4 = (self.color_cmyk_l3[4] + (self.percentage_cmyk_g3 * (self.color_cmyk_r3[4] - self.color_cmyk_l3[4])))
        # Send Values
        self.Color_CMYK(cmyk1, cmyk2, cmyk3, cmyk4)

    # Mixer Options
    def Mixer_Display(self):
        # Mixer Tint, Tone, Shade
        if (self.color_tts[0] == "True" and self.layout.tts.isChecked() == True):
            input_tint = [self.color_tts[1], self.color_tts[2], self.color_tts[3]]
            mix_tint = self.RGB_Gradient(input_tint, color_white)
            mix_tone = self.RGB_Gradient(input_tint, color_grey)
            mix_shade = self.RGB_Gradient(input_tint, color_black)
            self.layout.tint.setStyleSheet(mix_tint)
            self.layout.tone.setStyleSheet(mix_tone)
            self.layout.shade.setStyleSheet(mix_shade)
        else:
            self.layout.tint.setStyleSheet(bg_alpha)
            self.layout.tone.setStyleSheet(bg_alpha)
            self.layout.shade.setStyleSheet(bg_alpha)
        # Mixer RGB
        if self.layout.mix.currentText() == "RGB":
            if (self.color_rgb_l1[0] == "True" and self.color_rgb_r1[0] == "True"):
                input_rgb_l1 = [self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3]]
                input_rgb_r1 = [self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3]]
                mix_rgb_g1 = self.RGB_Gradient(input_rgb_l1, input_rgb_r1)
                self.layout.rgb_g1.setStyleSheet(mix_rgb_g1)
            if (self.color_rgb_l2[0] == "True" and self.color_rgb_r2[0] == "True"):
                input_rgb_l2 = [self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3]]
                input_rgb_r2 = [self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3]]
                mix_rgb_g2 = self.RGB_Gradient(input_rgb_l2, input_rgb_r2)
                self.layout.rgb_g2.setStyleSheet(mix_rgb_g2)
            if (self.color_rgb_l3[0] == "True" and self.color_rgb_r3[0] == "True"):
                input_rgb_l3 = [self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3]]
                input_rgb_r3 = [self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3]]
                mix_rgb_g3 = self.RGB_Gradient(input_rgb_l3, input_rgb_r3)
                self.layout.rgb_g3.setStyleSheet(mix_rgb_g3)
        else:
            self.layout.rgb_g1.setStyleSheet(bg_alpha)
            self.layout.rgb_g2.setStyleSheet(bg_alpha)
            self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Mixer ARD
        if self.layout.mix.currentText() == "ARD":
            if (self.color_ard_l1[0] == "True" and self.color_ard_r1[0] == "True"):
                input_ard_l1 = [self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3]]
                input_ard_r1 = [self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3]]
                mix_ard_g1 = self.ARD_Gradient_Circular(self.layout.ard_g1.width(), input_ard_l1, input_ard_r1)
                self.layout.ard_g1.setStyleSheet(mix_ard_g1)
            if (self.color_ard_l2[0] == "True" and self.color_ard_r2[0] == "True"):
                input_ard_l2 = [self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3]]
                input_ard_r2 = [self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3]]
                mix_ard_g2 = self.ARD_Gradient_Circular(self.layout.ard_g2.width(), input_ard_l2, input_ard_r2)
                self.layout.ard_g2.setStyleSheet(mix_ard_g2)
            if (self.color_ard_l3[0] == "True" and self.color_ard_r3[0] == "True"):
                input_ard_l3 = [self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3]]
                input_ard_r3 = [self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3]]
                mix_ard_g3 = self.ARD_Gradient_Circular(self.layout.ard_g3.width(), input_ard_l3, input_ard_r3)
                self.layout.ard_g3.setStyleSheet(mix_ard_g3)
        else:
            self.layout.ard_g1.setStyleSheet(bg_alpha)
            self.layout.ard_g2.setStyleSheet(bg_alpha)
            self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Mixer HSV
        if self.layout.mix.currentText() == "HSV":
            if (self.color_hsv_l1[0] == "True" and self.color_hsv_r1[0] == "True"):
                input_hsv_l1 = [self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3]]
                input_hsv_r1 = [self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3]]
                mix_hsv_g1 = self.HSV_Gradient(self.layout.hsv_g1.width(), input_hsv_l1, input_hsv_r1)
                self.layout.hsv_g1.setStyleSheet(mix_hsv_g1)
            if (self.color_hsv_l2[0] == "True" and self.color_hsv_r2[0] == "True"):
                input_hsv_l2 = [self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3]]
                input_hsv_r2 = [self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3]]
                mix_hsv_g2 = self.HSV_Gradient(self.layout.hsv_g2.width(), input_hsv_l2, input_hsv_r2)
                self.layout.hsv_g2.setStyleSheet(mix_hsv_g2)
            if (self.color_hsv_l3[0] == "True" and self.color_hsv_r3[0] == "True"):
                input_hsv_l3 = [self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3]]
                input_hsv_r3 = [self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3]]
                mix_hsv_g3 = self.HSV_Gradient(self.layout.hsv_g3.width(), input_hsv_l3, input_hsv_r3)
                self.layout.hsv_g3.setStyleSheet(mix_hsv_g3)
        else:
            self.layout.hsv_g1.setStyleSheet(bg_alpha)
            self.layout.hsv_g2.setStyleSheet(bg_alpha)
            self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Mixer HSL
        if self.layout.mix.currentText() == "HSL":
            if (self.color_hsl_l1[0] == "True" and self.color_hsl_r1[0] == "True"):
                input_hsl_l1 = [self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3]]
                input_hsl_r1 = [self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3]]
                mix_hsl_g1 = self.HSL_Gradient(self.layout.hsl_g1.width(), input_hsl_l1, input_hsl_r1)
                self.layout.hsl_g1.setStyleSheet(mix_hsl_g1)
            if (self.color_hsl_l2[0] == "True" and self.color_hsl_r2[0] == "True"):
                input_hsl_l2 = [self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3]]
                input_hsl_r2 = [self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3]]
                mix_hsl_g2 = self.HSL_Gradient(self.layout.hsl_g2.width(), input_hsl_l2, input_hsl_r2)
                self.layout.hsl_g2.setStyleSheet(mix_hsl_g2)
            if (self.color_hsl_l3[0] == "True" and self.color_hsl_r3[0] == "True"):
                input_hsl_l3 = [self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3]]
                input_hsl_r3 = [self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3]]
                mix_hsl_g3 = self.HSL_Gradient(self.layout.hsl_g3.width(), input_hsl_l3, input_hsl_r3)
                self.layout.hsl_g3.setStyleSheet(mix_hsl_g3)
        else:
            self.layout.hsl_g1.setStyleSheet(bg_alpha)
            self.layout.hsl_g2.setStyleSheet(bg_alpha)
            self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Mixer CMYK
        if self.layout.mix.currentText() == "CMYK":
            if (self.color_cmyk_l1[0] == "True" and self.color_cmyk_r1[0] == "True"):
                input_cmyk_l1 = [self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4]]
                input_cmyk_r1 = [self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4]]
                mix_cmyk_g1 = self.CMYK_Gradient(self.layout.cmyk_g1.width(), input_cmyk_l1, input_cmyk_r1)
                self.layout.cmyk_g1.setStyleSheet(mix_cmyk_g1)
            if (self.color_cmyk_l2[0] == "True" and self.color_cmyk_r2[0] == "True"):
                input_cmyk_l2 = [self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4]]
                input_cmyk_r2 = [self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4]]
                mix_cmyk_g2 = self.CMYK_Gradient(self.layout.cmyk_g2.width(), input_cmyk_l2, input_cmyk_r2)
                self.layout.cmyk_g2.setStyleSheet(mix_cmyk_g2)
            if (self.color_cmyk_l3[0] == "True" and self.color_cmyk_r3[0] == "True"):
                input_cmyk_l3 = [self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4]]
                input_cmyk_r3 = [self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4]]
                mix_cmyk_g3 = self.CMYK_Gradient(self.layout.cmyk_g3.width(), input_cmyk_l3, input_cmyk_r3)
                self.layout.cmyk_g3.setStyleSheet(mix_cmyk_g3)
        else:
            self.layout.cmyk_g1.setStyleSheet(bg_alpha)
            self.layout.cmyk_g2.setStyleSheet(bg_alpha)
            self.layout.cmyk_g3.setStyleSheet(bg_alpha)

    #//
    #\\ Panel Signals###########################################################
    def Signal_HSV(self, SIGNAL_HSV_VALUE):
        self.hsv_2 = round(SIGNAL_HSV_VALUE[0]*kritaSVL, 2) / kritaSVL
        self.hsv_3 = round(SIGNAL_HSV_VALUE[1]*kritaSVL, 2) / kritaSVL
        self.Color_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
    def Signal_HSL(self, SIGNAL_HSL_VALUE):
        self.hsl_2 = round(SIGNAL_HSL_VALUE[0]*kritaSVL, 2) / kritaSVL
        self.hsl_3 = round(SIGNAL_HSL_VALUE[1]*kritaSVL, 2) / kritaSVL
        self.Color_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
    def Signal_ARD(self, SIGNAL_ARD_VALUE):
        self.ard_2 = round(SIGNAL_ARD_VALUE[0]*kritaANG, 2) / kritaANG
        self.ard_3 = round(SIGNAL_ARD_VALUE[1]*kritaRDL, 2) / kritaRDL
        self.Color_ARD(self.ard_1, self.ard_2, self.ard_3)
    def Signal_UVD(self, SIGNAL_UVD_VALUE):
        self.uvd_1 = round(SIGNAL_UVD_VALUE[0]*kritaUVD, 2) / kritaUVD
        self.uvd_2 = round(SIGNAL_UVD_VALUE[1]*kritaUVD, 2) / kritaUVD
        self.Color_UVD(self.uvd_1, self.uvd_2, self.uvd_3)
    def Signal_OBJ(self, SIGNAL_OBJECT):
        # Geometry
        # self.update()
        width = self.layout.layers_widget.width()
        height = self.layout.layers_widget.height()
        pixmap = self.layout.layers_widget.grab(QRect(QPoint(0, 0), QPoint(width, height)))
        image = pixmap.toImage()
        scaled = image.scaled(QSize(width, height))
        color = scaled.pixelColor(SIGNAL_OBJECT[0], SIGNAL_OBJECT[1])
        # Apply Color Values
        self.rgb_1 = color.red()/255
        self.rgb_2 = color.green()/255
        self.rgb_3 = color.blue()/255
        self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Pigment_Display_Release(0)

    #//
    #\\ Object #################################################################
    def BG_1_Exclusion(self):
        # Auto Exclusive
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.bg_1[1], self.bg_1[2], self.bg_1[3])
    def BG_1_LIVE(self):
        if self.layout.b1_live.isChecked() == True:
            self.BG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b1a, "SAVE")
            self.Pigment_Display_Release(0)
    def BG_1_APPLY(self):
        if self.bg_1[0] == "True":
            self.Color_RGB(self.bg_1[1], self.bg_1[2], self.bg_1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def BG_1_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.bg_1 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        self.layout.b1_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def BG_1_CLEAN(self):
        self.bg_1 = ["False", 0, 0, 0, 1]
        self.b1a = 1
        self.layout.b1_color.setStyleSheet(bg_alpha)
        self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, 0, 0, 0, 1))
        self.Settings_Save()
    def BG_1_ALPHA(self, SIGNAL_VALUE):
        self.b1a = SIGNAL_VALUE
        self.BG_1_Exclusion()
        self.BG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b1a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def BG_2_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.bg_2[1], self.bg_2[2], self.bg_2[3])
    def BG_2_LIVE(self):
        if self.layout.b2_live.isChecked() == True:
            self.BG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b2a, "SAVE")
            self.Pigment_Display_Release(0)
    def BG_2_APPLY(self):
        if self.bg_2[0] == "True":
            self.Color_RGB(self.bg_2[1], self.bg_2[2], self.bg_2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def BG_2_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.bg_2 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, self.bg_2[1]*255, self.bg_2[2]*255, self.bg_2[3]*255, self.bg_2[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_2[1]*255, self.bg_2[2]*255, self.bg_2[3]*255, self.bg_2[4]*255))
        self.layout.b2_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, self.bg_2[1]*255, self.bg_2[2]*255, self.bg_2[3]*255, self.bg_2[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def BG_2_CLEAN(self):
        self.bg_2 = ["False", 0, 0, 0, 1]
        self.b2a = 1
        self.layout.b2_color.setStyleSheet(bg_alpha)
        self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, 0, 0, 0, 1))
        self.Settings_Save()
    def BG_2_ALPHA(self, SIGNAL_VALUE):
        self.b2a = SIGNAL_VALUE
        self.BG_2_Exclusion()
        self.BG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b2a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def BG_3_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.bg_3[1], self.bg_3[2], self.bg_3[3])
    def BG_3_LIVE(self):
        if self.layout.b3_live.isChecked() == True:
            self.BG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b3a, "SAVE")
            self.Pigment_Display_Release(0)
    def BG_3_APPLY(self):
        if self.bg_3[0] == "True":
            self.Color_RGB(self.bg_3[1], self.bg_3[2], self.bg_3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def BG_3_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.bg_3 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, self.bg_3[1]*255, self.bg_3[2]*255, self.bg_3[3]*255, self.bg_3[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_3[1]*255, self.bg_3[2]*255, self.bg_3[3]*255, self.bg_3[4]*255))
        self.layout.b3_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, self.bg_3[1]*255, self.bg_3[2]*255, self.bg_3[3]*255, self.bg_3[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def BG_3_CLEAN(self):
        self.bg_3 = ["False", 0, 0, 0, 1]
        self.b3a = 1
        self.layout.b3_color.setStyleSheet(bg_alpha)
        self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, 0, 0, 0, 1))
        self.Settings_Save()
    def BG_3_ALPHA(self, SIGNAL_VALUE):
        self.b3a = SIGNAL_VALUE
        self.BG_3_Exclusion()
        self.BG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b3a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def DIF_1_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.dif_1[1], self.dif_1[2], self.dif_1[3])
    def DIF_1_LIVE(self):
        if self.layout.d1_live.isChecked() == True:
            self.DIF_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d1a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_1_APPLY(self):
        if self.dif_1[0] == "True":
            self.Color_RGB(self.dif_1[1], self.dif_1[2], self.dif_1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def DIF_1_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.dif_1 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, self.dif_1[1]*255, self.dif_1[2]*255, self.dif_1[3]*255, self.dif_1[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_1[1]*255, self.dif_1[2]*255, self.dif_1[3]*255, self.dif_1[4]*255))
        self.layout.d1_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, self.dif_1[1]*255, self.dif_1[2]*255, self.dif_1[3]*255, self.dif_1[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def DIF_1_CLEAN(self):
        self.dif_1 = ["False", 0, 0, 0, 1]
        self.d1a = 1
        self.layout.d1_color.setStyleSheet(bg_alpha)
        self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, 0, 0, 0, 1))
        self.Settings_Save()
    def DIF_1_ALPHA(self, SIGNAL_VALUE):
        self.d1a = SIGNAL_VALUE
        self.DIF_1_Exclusion()
        self.DIF_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d1a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def DIF_2_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.dif_2[1], self.dif_2[2], self.dif_2[3])
    def DIF_2_LIVE(self):
        if self.layout.d2_live.isChecked() == True:
            self.DIF_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d2a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_2_APPLY(self):
        if self.dif_2[0] == "True":
            self.Color_RGB(self.dif_2[1], self.dif_2[2], self.dif_2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def DIF_2_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.dif_2 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, self.dif_2[1]*255, self.dif_2[2]*255, self.dif_2[3]*255, self.dif_2[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_2[1]*255, self.dif_2[2]*255, self.dif_2[3]*255, self.dif_2[4]*255))
        self.layout.d2_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, self.dif_2[1]*255, self.dif_2[2]*255, self.dif_2[3]*255, self.dif_2[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def DIF_2_CLEAN(self):
        self.dif_2 = ["False", 0, 0, 0, 1]
        self.d2a = 1
        self.layout.d2_color.setStyleSheet(bg_alpha)
        self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, 0, 0, 0, 1))
        self.Settings_Save()
    def DIF_2_ALPHA(self, SIGNAL_VALUE):
        self.d2a = SIGNAL_VALUE
        self.DIF_2_Exclusion()
        self.DIF_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d2a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def DIF_3_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.dif_3[1], self.dif_3[2], self.dif_3[3])
    def DIF_3_LIVE(self):
        if self.layout.d3_live.isChecked() == True:
            self.DIF_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d3a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_3_APPLY(self):
        if self.dif_3[0] == "True":
            self.Color_RGB(self.dif_3[1], self.dif_3[2], self.dif_3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def DIF_3_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.dif_3 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, self.dif_3[1]*255, self.dif_3[2]*255, self.dif_3[3]*255, self.dif_3[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_3[1]*255, self.dif_3[2]*255, self.dif_3[3]*255, self.dif_3[4]*255))
        self.layout.d3_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, self.dif_3[1]*255, self.dif_3[2]*255, self.dif_3[3]*255, self.dif_3[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def DIF_3_CLEAN(self):
        self.dif_3 = ["False", 0, 0, 0, 1]
        self.d3a = 1
        self.layout.d3_color.setStyleSheet(bg_alpha)
        self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, 0, 0, 0, 1))
        self.Settings_Save()
    def DIF_3_ALPHA(self, SIGNAL_VALUE):
        self.d3a = SIGNAL_VALUE
        self.DIF_3_Exclusion()
        self.DIF_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d3a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def DIF_4_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.dif_4[1], self.dif_4[2], self.dif_4[3])
    def DIF_4_LIVE(self):
        if self.layout.d4_live.isChecked() == True:
            self.DIF_4_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d4a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_4_APPLY(self):
        if self.dif_4[0] == "True":
            self.Color_RGB(self.dif_4[1], self.dif_4[2], self.dif_4[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def DIF_4_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.dif_4 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, self.dif_4[1]*255, self.dif_4[2]*255, self.dif_4[3]*255, self.dif_4[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_4[1]*255, self.dif_4[2]*255, self.dif_4[3]*255, self.dif_4[4]*255))
        self.layout.d4_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, self.dif_4[1]*255, self.dif_4[2]*255, self.dif_4[3]*255, self.dif_4[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def DIF_4_CLEAN(self):
        self.dif_4 = ["False", 0, 0, 0, 1]
        self.d4a = 1
        self.layout.d4_color.setStyleSheet(bg_alpha)
        self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, 0, 0, 0, 1))
        self.Settings_Save()
    def DIF_4_ALPHA(self, SIGNAL_VALUE):
        self.d4a = SIGNAL_VALUE
        self.DIF_4_Exclusion()
        self.DIF_4_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d4a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def DIF_5_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.dif_5[1], self.dif_5[2], self.dif_5[3])
    def DIF_5_LIVE(self):
        if self.layout.d5_live.isChecked() == True:
            self.DIF_5_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d5a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_5_APPLY(self):
        if self.dif_5[0] == "True":
            self.Color_RGB(self.dif_5[1], self.dif_5[2], self.dif_5[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def DIF_5_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.dif_5 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, self.dif_5[1]*255, self.dif_5[2]*255, self.dif_5[3]*255, self.dif_5[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_5[1]*255, self.dif_5[2]*255, self.dif_5[3]*255, self.dif_5[4]*255))
        self.layout.d5_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, self.dif_5[1]*255, self.dif_5[2]*255, self.dif_5[3]*255, self.dif_5[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def DIF_5_CLEAN(self):
        self.dif_5 = ["False", 0, 0, 0, 1]
        self.d5a = 1
        self.layout.d5_color.setStyleSheet(bg_alpha)
        self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, 0, 0, 0, 1))
        self.Settings_Save()
    def DIF_5_ALPHA(self, SIGNAL_VALUE):
        self.d5a = SIGNAL_VALUE
        self.DIF_5_Exclusion()
        self.DIF_5_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d5a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def DIF_6_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.dif_6[1], self.dif_6[2], self.dif_6[3])
    def DIF_6_LIVE(self):
        if self.layout.d6_live.isChecked() == True:
            self.DIF_6_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d6a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_6_APPLY(self):
        if self.dif_6[0] == "True":
            self.Color_RGB(self.dif_6[1], self.dif_6[2], self.dif_6[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def DIF_6_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.dif_6 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, self.dif_6[1]*255, self.dif_6[2]*255, self.dif_6[3]*255, self.dif_6[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_6[1]*255, self.dif_6[2]*255, self.dif_6[3]*255, self.dif_6[4]*255))
        self.layout.d6_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, self.dif_6[1]*255, self.dif_6[2]*255, self.dif_6[3]*255, self.dif_6[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def DIF_6_CLEAN(self):
        self.dif_6 = ["False", 0, 0, 0, 1]
        self.d6a = 1
        self.layout.d6_color.setStyleSheet(bg_alpha)
        self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, 0, 0, 0, 1))
        self.Settings_Save()
    def DIF_6_ALPHA(self, SIGNAL_VALUE):
        self.d6a = SIGNAL_VALUE
        self.DIF_6_Exclusion()
        self.DIF_6_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d6a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def FG_1_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.fg_1[1], self.fg_1[2], self.fg_1[3])
    def FG_1_LIVE(self):
        if self.layout.f1_live.isChecked() == True:
            self.FG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f1a, "SAVE")
            self.Pigment_Display_Release(0)
    def FG_1_APPLY(self):
        if self.fg_1[0] == "True":
            self.Color_RGB(self.fg_1[1], self.fg_1[2], self.fg_1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def FG_1_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.fg_1 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, self.fg_1[1]*255, self.fg_1[2]*255, self.fg_1[3]*255, self.fg_1[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_1[1]*255, self.fg_1[2]*255, self.fg_1[3]*255, self.fg_1[4]*255))
        self.layout.f1_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, self.fg_1[1]*255, self.fg_1[2]*255, self.fg_1[3]*255, self.fg_1[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def FG_1_CLEAN(self):
        self.fg_1 = ["False", 0, 0, 0, 1]
        self.f1a = 1
        self.layout.f1_color.setStyleSheet(bg_alpha)
        self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, 0, 0, 0, 1))
        self.Settings_Save()
    def FG_1_ALPHA(self, SIGNAL_VALUE):
        self.f1a = SIGNAL_VALUE
        self.FG_1_Exclusion()
        self.FG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f1a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def FG_2_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.fg_2[1], self.fg_2[2], self.fg_2[3])
    def FG_2_LIVE(self):
        if self.layout.f2_live.isChecked() == True:
            self.FG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f2a, "SAVE")
            self.Pigment_Display_Release(0)
    def FG_2_APPLY(self):
        if self.fg_2[0] == "True":
            self.Color_RGB(self.fg_2[1], self.fg_2[2], self.fg_2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def FG_2_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.fg_2 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, self.fg_2[1]*255, self.fg_2[2]*255, self.fg_2[3]*255, self.fg_2[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_2[1]*255, self.fg_2[2]*255, self.fg_2[3]*255, self.fg_2[4]*255))
        self.layout.f2_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, self.fg_2[1]*255, self.fg_2[2]*255, self.fg_2[3]*255, self.fg_2[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def FG_2_CLEAN(self):
        self.fg_2 = ["False", 0, 0, 0, 1]
        self.f2a = 1
        self.layout.f2_color.setStyleSheet(bg_alpha)
        self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, 0, 0, 0, 1))
        self.Settings_Save()
    def FG_2_ALPHA(self, SIGNAL_VALUE):
        self.f2a = SIGNAL_VALUE
        self.FG_2_Exclusion()
        self.FG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f2a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def FG_3_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        # Apply Color before Live
        self.Color_RGB(self.fg_3[1], self.fg_3[2], self.fg_3[3])
    def FG_3_LIVE(self):
        if self.layout.f3_live.isChecked() == True:
            self.FG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f3a, "SAVE")
            self.Pigment_Display_Release(0)
    def FG_3_APPLY(self):
        if self.fg_3[0] == "True":
            self.Color_RGB(self.fg_3[1], self.fg_3[2], self.fg_3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def FG_3_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.fg_3 = ["True", val_1, val_2, val_3, val_4]
        # Update Object Representation
        self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, self.fg_3[1]*255, self.fg_3[2]*255, self.fg_3[3]*255, self.fg_3[4]*255))
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_3[1]*255, self.fg_3[2]*255, self.fg_3[3]*255, self.fg_3[4]*255))
        self.layout.f3_color.setStyleSheet(color)
        # Render Object
        self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, self.fg_3[1]*255, self.fg_3[2]*255, self.fg_3[3]*255, self.fg_3[4]*255))
        # Save
        if save == "SAVE":
            self.Settings_Save()
    def FG_3_CLEAN(self):
        self.fg_3 = ["False", 0, 0, 0, 1]
        self.f3a = 1
        self.layout.f3_color.setStyleSheet(bg_alpha)
        self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, 0, 0, 0, 1))
        self.Settings_Save()
    def FG_3_ALPHA(self, SIGNAL_VALUE):
        self.f3a = SIGNAL_VALUE
        self.FG_3_Exclusion()
        self.FG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f3a, "SAVE")
        self.Pigment_Display_Release(0)
        self.update()

    def Object_Live(self):
        self.BG_1_LIVE()
        self.BG_2_LIVE()
        self.BG_3_LIVE()
        self.DIF_1_LIVE()
        self.DIF_2_LIVE()
        self.DIF_3_LIVE()
        self.DIF_4_LIVE()
        self.DIF_5_LIVE()
        self.DIF_6_LIVE()
        self.FG_1_LIVE()
        self.FG_2_LIVE()
        self.FG_3_LIVE()
    def Object_Render(self):
        if self.layout.obj.currentText() != "OBJECT":
            # Object Label Geometry
            self.layout.layer_01.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_02.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_03.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_04.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_05.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_06.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_07.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_08.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_09.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_10.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_11.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            self.layout.layer_12.setGeometry(0,0,self.layout.layers_widget.width(),self.layout.layers_widget.height())
            # Render Layers
            if self.bg_1[0] == "True":
                self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
                self.BG_1_SAVE(self.bg_1[1], self.bg_1[2], self.bg_1[3], self.bg_1[4], "SAVE")
            if self.bg_2[0] == "True":
                self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, self.bg_2[1]*255, self.bg_2[2]*255, self.bg_2[3]*255, self.bg_2[4]*255))
                self.BG_2_SAVE(self.bg_2[1], self.bg_2[2], self.bg_2[3], self.bg_2[4], "SAVE")
            if self.bg_3[0] == "True":
                self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, self.bg_3[1]*255, self.bg_3[2]*255, self.bg_3[3]*255, self.bg_3[4]*255))
                self.BG_3_SAVE(self.bg_3[1], self.bg_3[2], self.bg_3[3], self.bg_3[4], "SAVE")
            if self.dif_1[0] == "True":
                self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, self.dif_1[1]*255, self.dif_1[2]*255, self.dif_1[3]*255, self.dif_1[4]*255))
                self.DIF_1_SAVE(self.dif_1[1], self.dif_1[2], self.dif_1[3], self.dif_1[4], "SAVE")
            if self.dif_2[0] == "True":
                self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, self.dif_2[1]*255, self.dif_2[2]*255, self.dif_2[3]*255, self.dif_2[4]*255))
                self.DIF_2_SAVE(self.dif_2[1], self.dif_2[2], self.dif_2[3], self.dif_2[4], "SAVE")
            if self.dif_3[0] == "True":
                self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, self.dif_3[1]*255, self.dif_3[2]*255, self.dif_3[3]*255, self.dif_3[4]*255))
                self.DIF_3_SAVE(self.dif_3[1], self.dif_3[2], self.dif_3[3], self.dif_3[4], "SAVE")
            if self.dif_4[0] == "True":
                self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, self.dif_4[1]*255, self.dif_4[2]*255, self.dif_4[3]*255, self.dif_4[4]*255))
                self.DIF_4_SAVE(self.dif_4[1], self.dif_4[2], self.dif_4[3], self.dif_4[4], "SAVE")
            if self.dif_5[0] == "True":
                self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, self.dif_5[1]*255, self.dif_5[2]*255, self.dif_5[3]*255, self.dif_5[4]*255))
                self.DIF_5_SAVE(self.dif_5[1], self.dif_5[2], self.dif_5[3], self.dif_5[4], "SAVE")
            if self.dif_6[0] == "True":
                self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, self.dif_6[1]*255, self.dif_6[2]*255, self.dif_6[3]*255, self.dif_6[4]*255))
                self.DIF_6_SAVE(self.dif_6[1], self.dif_6[2], self.dif_6[3], self.dif_6[4], "SAVE")
            if self.fg_1[0] == "True":
                self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, self.fg_1[1]*255, self.fg_1[2]*255, self.fg_1[3]*255, self.fg_1[4]*255))
                self.FG_1_SAVE(self.fg_1[1], self.fg_1[2], self.fg_1[3], self.fg_1[4], "SAVE")
            if self.fg_2[0] == "True":
                self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, self.fg_2[1]*255, self.fg_2[2]*255, self.fg_2[3]*255, self.fg_2[4]*255))
                self.FG_2_SAVE(self.fg_2[1], self.fg_2[2], self.fg_2[3], self.fg_2[4], "SAVE")
            if self.fg_3[0] == "True":
                self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, self.fg_3[1]*255, self.fg_3[2]*255, self.fg_3[3]*255, self.fg_3[4]*255))
                self.FG_3_SAVE(self.fg_3[1], self.fg_3[2], self.fg_3[3], self.fg_3[4], "SAVE")
    def Object_Alpha(self):
        self.b1_alpha.Update(self.b1a, self.layout.b1_alpha.width())
        self.b2_alpha.Update(self.b2a, self.layout.b2_alpha.width())
        self.b3_alpha.Update(self.b3a, self.layout.b3_alpha.width())
        self.d1_alpha.Update(self.d1a, self.layout.d1_alpha.width())
        self.d2_alpha.Update(self.d2a, self.layout.d2_alpha.width())
        self.d3_alpha.Update(self.d3a, self.layout.d3_alpha.width())
        self.d4_alpha.Update(self.d4a, self.layout.d4_alpha.width())
        self.d5_alpha.Update(self.d5a, self.layout.d5_alpha.width())
        self.d6_alpha.Update(self.d6a, self.layout.d6_alpha.width())
        self.f1_alpha.Update(self.f1a, self.layout.f1_alpha.width())
        self.f2_alpha.Update(self.f2a, self.layout.f2_alpha.width())
        self.f3_alpha.Update(self.f3a, self.layout.f3_alpha.width())
    def Mask_Color(self, file, r, g, b, a):
        pixmap = QPixmap.fromImage(QImage(file))
        image = QImage(pixmap.width(), pixmap.height(), QImage.Format_ARGB32_Premultiplied)
        image.fill(QColor(r, g, b, a))
        pixmap_color = QPixmap.fromImage(image)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.drawImage(0,0,pixmap_color.toImage())
        painter.end()
        return pixmap

    #//
    #\\ Style ##################################################################
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
        elif self.count == "3S":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:0, y2:1, \n"+
            "stop:0.000 rgba(0, 0, 0, 50), \n"+
            "stop:0.332 rgba(0, 0, 0, 50), \n"+
            "stop:0.333 rgba(0, 0, 0, 0), \n"+
            "stop:0.666 rgba(0, 0, 0, 0), \n"+
            "stop:0.667 rgba(0, 0, 0, 50), \n"+
            "stop:1.000 rgba(0, 0, 0, 50));"
            )
        return percentage_style_sheet
    # Gradients
    def NEU_Gradient(self, percentage):
        """ Input: 0-1 """
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 50), "
        slider_gradient += "stop:%s rgba(0, 0, 0, 50), \n " % (percentage-0.005)
        slider_gradient += "stop:%s rgba(0, 0, 0, 0), \n " % (percentage+0.001)
        slider_gradient += "stop:1 rgba(0, 0, 0, 0) ) ; \n "
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def RGB_Gradient(self, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Convert Left
        left_r = round(left[0],3)
        left_g = round(left[1],3)
        left_b = round(left[2],3)
        # Convert Right
        right_r = round(right[0],3)
        right_g = round(right[1],3)
        right_b = round(right[2],3)
        # Style String
        slider_gradient = (
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%s, %s, %s), stop:1 rgb(%s, %s, %s) ) ; border: 1px solid rgba(56, 56, 56, 255) ;"
        % (left_r*255, left_g*255, left_b*255, right_r*255, right_g*255, right_b*255)
        )
        # Return StyleSheet String
        return slider_gradient
    def HUE_Gradient(self, hue, width, color_left, color_right):
        # HUE entry type
        if hue == "HSV":
            # Colors
            left = [color_left[0], color_left[1], color_left[2]]
            right = [color_right[0], color_right[1], color_right[2]]
            # Convert Left
            left_rgb = self.hsv_to_rgb(left[0], left[1], left[2])
            left_r = round(left_rgb[0],3)
            left_g = round(left_rgb[1],3)
            left_b = round(left_rgb[2],3)
            # Convert Right
            right_rgb = self.hsv_to_rgb(right[0], right[1], right[2])
            right_r = round(right_rgb[0],3)
            right_g = round(right_rgb[1],3)
            right_b = round(right_rgb[2],3)
        if hue == "HSL":
            # Colors
            left = [color_left[0], color_left[1], color_left[2]]
            right = [color_right[0], color_right[1], color_right[2]]
            # Convert Left
            left_rgb = self.hsl_to_rgb(left[0], left[1], left[2])
            left_r = round(left_rgb[0],3)
            left_g = round(left_rgb[1],3)
            left_b = round(left_rgb[2],3)
            # Convert Right
            right_rgb = self.hsl_to_rgb(right[0], right[1], right[2])
            right_r = round(right_rgb[0],3)
            right_g = round(right_rgb[1],3)
            right_b = round(right_rgb[2],3)
        # Conditions
        cond0 = right[0] - left[0]
        cond1 = right[1] - left[1]
        cond2 = right[2] - left[2]
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, left_r*255, left_g*255, left_b*255)
        try:
            width = int(width / 10) + 1
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            h = (left[0] + (stop * cond0))
            s = (left[1] + (stop * cond1))
            v = (left[2] + (stop * cond2))
            # HSV to RGB Conversion
            rgb = self.hsv_to_rgb(h, s, v)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, right_r*255, right_g*255, right_b*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def HSV_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Conditions
        cond1 = right[0] - left[0]
        cond2 = (left[0] + 1) - right[0]
        cond3 = right[1] - left[1]
        cond4 = right[2] - left[2]
        # Convert Left
        left_rgb = self.hsv_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.hsv_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, left_r*255, left_g*255, left_b*255)
        try:
            width = int(width / 20) + 1
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # Angle Calculations
            if left[0] <= right[0]:
                # Conditions
                cond1 = right[0] - left[0]
                cond2 = (left[0] + 1) - right[0]
                if cond1 <= cond2:
                    h = left[0] + (stop * cond1)
                else:
                    h = left[0] - (stop * cond2)
            else:
                # Conditions
                cond1 = left[0] - right[0]
                cond2 = (right[0] + 1) - left[0]
                if cond1 <= cond2:
                    h = left[0] - (stop * cond1)
                else:
                    h = left[0] + (stop * cond2)
            # Correct Excess
            if h < 0:
                h = h + 1
            if h > 1:
                h = h - 1
            h = h
            s = (left[1] + (stop * cond3))
            v = (left[2] + (stop * cond4))

            # HSV to RGB Conversion
            rgb = self.hsv_to_rgb(h, s, v)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, right_r*255, right_g*255, right_b*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def HSL_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Conditions
        cond1 = right[0] - left[0]
        cond2 = (left[0] + 1) - right[0]
        cond3 = right[1] - left[1]
        cond4 = right[2] - left[2]
        # Convert Left
        left_rgb = self.hsl_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.hsl_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, left_r*255, left_g*255, left_b*255)
        try:
            width = int(width / 20) + 1
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # Angle Calculations
            if left[0] <= right[0]:
                # Conditions
                cond1 = right[0] - left[0]
                cond2 = (left[0] + 1) - right[0]
                if cond1 <= cond2:
                    h = left[0] + (stop * cond1)
                else:
                    h = left[0] - (stop * cond2)
            else:
                # Conditions
                cond1 = left[0] - right[0]
                cond2 = (right[0] + 1) - left[0]
                if cond1 <= cond2:
                    h = left[0] - (stop * cond1)
                else:
                    h = left[0] + (stop * cond2)
            # Correct Excess
            if h < 0:
                h = h + 1
            if h > 1:
                h = h - 1
            h = h
            s = (left[1] + (stop * cond3))
            l = (left[2] + (stop * cond4))

            # HSL to RGB Conversion
            rgb = self.hsl_to_rgb(h, s, l)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, right_r*255, right_g*255, right_b*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def CMYK_Gradient(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2], color_left[3]]
        right = [color_right[0], color_right[1], color_right[2], color_right[3]]
        # Convert Left
        left_rgb = self.cmyk_to_rgb(left[0], left[1], left[2], left[3])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.cmyk_to_rgb(right[0], right[1], right[2], right[3])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Style String
        slider_gradient = (
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%s, %s, %s), stop:1 rgb(%s, %s, %s) ) ; border: 1px solid rgba(56, 56, 56, 255) ;"
         % (left_r*255, left_g*255, left_b*255, right_r*255, right_g*255, right_b*255)
         )
        # Return StyleSheet String
        return slider_gradient
    def ARD_Gradient_Linear(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Conditions
        cond1 = right[0] - left[0]
        cond2 = right[1] - left[1]
        cond3 = right[2] - left[2]
        # Convert Left
        left_rgb = self.ard_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.ard_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, left_r*255, left_g*255, left_b*255)
        try:
            width = int(width / 10) + 1
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # ARD Calculation
            ard1 = (left[0] + (stop * cond1))
            ard2 = (left[1] + (stop * cond2))
            ard3 = (left[2] + (stop * cond3))
            # ARD to RGB Conversion
            rgb = self.ard_to_rgb(ard1, ard2, ard3)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, right_r*255, right_g*255, right_b*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def ARD_Gradient_Circular(self, width, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Conditions
        cond1 = right[0] - left[0]
        cond2 = (left[0] + 1) - right[0]
        cond3 = right[1] - left[1]
        cond4 = right[2] - left[2]
        # Convert Left
        left_rgb = self.ard_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0]*255,3)
        left_g = round(left_rgb[1]*255,3)
        left_b = round(left_rgb[2]*255,3)
        # Convert Right
        right_rgb = self.ard_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0]*255,3)
        right_g = round(right_rgb[1]*255,3)
        right_b = round(right_rgb[2]*255,3)
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, left_r, left_g, left_b)
        try:
            width = int(width / 10) + 1
            unit = 1 / width
        except:
            unit = 0
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # Angle Calculations
            if left[0] <= right[0]:
                # Conditions
                cond1 = right[0] - left[0]
                cond2 = (left[0] + 1) - right[0]
                if cond1 <= cond2:
                    a = left[0] + (stop * cond1)
                else:
                    a = left[0] - (stop * cond2)
            else:
                # Conditions
                cond1 = left[0] - right[0]
                cond2 = (right[0] + 1) - left[0]
                if cond1 <= cond2:
                    a = left[0] - (stop * cond1)
                else:
                    a = left[0] + (stop * cond2)
            # Correct Excess
            if a < 0:
                a = a + 1
            if a > 1:
                a = a - 1
            a = a
            r = (left[1] + (stop * cond3))
            d = (left[2] + (stop * cond4))
            # HSV to RGB Conversion
            rgb = self.ard_to_rgb(a, r, d)
            r = round(rgb[0]*255,3)
            g = round(rgb[1]*255,3)
            b = round(rgb[2]*255,3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r, g, b)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, right_r, right_g, right_b)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient

    #//
    #\\ Widget Events ##########################################################
    def showEvent(self, event):
        self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Pigment_Display()
        self.Mixer_Display()
        self.Ratio()
    def enterEvent(self, event):
        # Check Krita Once before edit
        self.Krita_Update()
        # Confirm Panel
        self.Ratio()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.stop()
        # UVD Panel Update
        if self.layout.gray_panels.isChecked() == False:
            self.UVD_Color(self.uvd_3)
        if self.layout.gray_panels.isChecked() == True:
            self.UVD_Gray(self.uvd_3)
    def leaveEvent(self, event):
        # Start Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.start()
    def eventFilter(self, source, event):
        # Object Panel Color Picker
        if (event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseMove or event.type() == QtCore.QEvent.MouseButtonRelease):
            self.Signal_OBJ([event.x(),  event.y()])
        return super(PigmentODocker, self).eventFilter(source, event)
    def resizeEvent(self, event):
        # Maintian Ratio
        self.Ratio()
    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:
            self.timer.stop()
        # Save Settings
        self.Settings_Save()

    #//
    #\\ Settings ###############################################################
    def Default_Boot(self):
        # Variables
        self.zoom = 0
        # Brush Size Opacity Flow
        self.lock_size = size
        self.lock_opacity = opacity
        self.lock_flow = flow
        self.sof_1 = size
        self.sof_2 = opacity
        self.sof_3 = flow
        self.tip_00.Setup_SOF(size, opacity, flow)
        # Palette
        self.color_00 = ["False", 0, 0, 0]
        self.color_01 = ["False", 0, 0, 0]
        self.color_02 = ["False", 0, 0, 0]
        self.color_03 = ["False", 0, 0, 0]
        self.color_04 = ["False", 0, 0, 0]
        self.color_05 = ["False", 0, 0, 0]
        self.color_06 = ["False", 0, 0, 0]
        self.color_07 = ["False", 0, 0, 0]
        self.color_08 = ["False", 0, 0, 0]
        self.color_09 = ["False", 0, 0, 0]
        self.color_10 = ["False", 0, 0, 0]
        self.layout.cor_00.setStyleSheet(bg_alpha)
        self.layout.cor_01.setStyleSheet(bg_alpha)
        self.layout.cor_02.setStyleSheet(bg_alpha)
        self.layout.cor_03.setStyleSheet(bg_alpha)
        self.layout.cor_04.setStyleSheet(bg_alpha)
        self.layout.cor_05.setStyleSheet(bg_alpha)
        self.layout.cor_06.setStyleSheet(bg_alpha)
        self.layout.cor_07.setStyleSheet(bg_alpha)
        self.layout.cor_08.setStyleSheet(bg_alpha)
        self.layout.cor_09.setStyleSheet(bg_alpha)
        self.layout.cor_10.setStyleSheet(bg_alpha)
        # Mixer TTS
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
        self.color_rgb_l1 = ["False", 0, 0, 0]
        self.color_rgb_r1 = ["False", 0, 0, 0]
        self.layout.rgb_l1.setStyleSheet(bg_alpha)
        self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.percentage_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
        # Mixer RGB 2
        self.color_rgb_l2 = ["False", 0, 0, 0]
        self.color_rgb_r2 = ["False", 0, 0, 0]
        self.layout.rgb_l2.setStyleSheet(bg_alpha)
        self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.percentage_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
        # Mixer RGB 3
        self.color_rgb_l3 = ["False", 0, 0, 0]
        self.color_rgb_r3 = ["False", 0, 0, 0]
        self.layout.rgb_l3.setStyleSheet(bg_alpha)
        self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.percentage_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

        # Mixer ARD 1
        self.color_ard_l1 = ["False", 0, 0, 0, 0, 0, 0]
        self.color_ard_r1 = ["False", 0, 0, 0, 0, 0, 0]
        self.layout.ard_l1.setStyleSheet(bg_alpha)
        self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.percentage_ard_g1 = 0
        self.mixer_ard_g1.Update(self.percentage_ard_g1, self.layout.ard_g1.width())
        # Mixer ARD 2
        self.color_ard_l2 = ["False", 0, 0, 0, 0, 0, 0]
        self.color_ard_r2 = ["False", 0, 0, 0, 0, 0, 0]
        self.layout.ard_l2.setStyleSheet(bg_alpha)
        self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.percentage_ard_g2 = 0
        self.mixer_ard_g2.Update(self.percentage_ard_g2, self.layout.ard_g2.width())
        # Mixer ARD 3
        self.color_ard_l3 = ["False", 0, 0, 0, 0, 0, 0]
        self.color_ard_r3 = ["False", 0, 0, 0, 0, 0, 0]
        self.layout.ard_l3.setStyleSheet(bg_alpha)
        self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.percentage_ard_g3 = 0
        self.mixer_ard_g3.Update(self.percentage_ard_g3, self.layout.ard_g3.width())

        # Mixer HSV 1
        self.color_hsv_l1 = ["False", 0, 0, 0]
        self.color_hsv_r1 = ["False", 0, 0, 0]
        self.layout.hsv_l1.setStyleSheet(bg_alpha)
        self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
        # Mixer HSV 2
        self.color_hsv_l2 = ["False", 0, 0, 0]
        self.color_hsv_r2 = ["False", 0, 0, 0]
        self.layout.hsv_l2.setStyleSheet(bg_alpha)
        self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
        # Mixer HSV 3
        self.color_hsv_l3 = ["False", 0, 0, 0]
        self.color_hsv_r3 = ["False", 0, 0, 0]
        self.layout.hsv_l3.setStyleSheet(bg_alpha)
        self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

        # Mixer HSL 1
        self.color_hsl_l1 = ["False", 0, 0, 0]
        self.color_hsl_r1 = ["False", 0, 0, 0]
        self.layout.hsl_l1.setStyleSheet(bg_alpha)
        self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
        # Mixer HSL 2
        self.color_hsl_l2 = ["False", 0, 0, 0]
        self.color_hsl_r2 = ["False", 0, 0, 0]
        self.layout.hsl_l2.setStyleSheet(bg_alpha)
        self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
        # Mixer HSL 3
        self.color_hsl_l3 = ["False", 0, 0, 0]
        self.color_hsl_r3 = ["False", 0, 0, 0]
        self.layout.hsl_l3.setStyleSheet(bg_alpha)
        self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

        # Mixer CMYK 1
        self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
        self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
        self.layout.cmyk_l1.setStyleSheet(bg_alpha)
        self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
        # Mixer CMYK 2
        self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
        self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
        self.layout.cmyk_l2.setStyleSheet(bg_alpha)
        self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
        # Mixer CMYK 3
        self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
        self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
        self.layout.cmyk_l3.setStyleSheet(bg_alpha)
        self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

        # Mixer Gradient Display
        self.Mixer_Display()

        # Object
        self.bg_1 = ["True", 0.0, 0.0, 0.0, 1]
        self.bg_2 = ["True", 0.0, 0.0, 0.0, 1]
        self.bg_3 = ["False", 0.0, 0.0, 0.0, 1]
        self.dif_1 = ["True", 35/255, 20/255, 2/255, 1]
        self.dif_2 = ["True", 84/255, 55/255, 19/255, 1]
        self.dif_3 = ["True", 254/255, 159/255, 14/255, 1]
        self.dif_4 = ["True", 255/255, 202/255, 50/255, 1]
        self.dif_5 = ["False", 0, 0, 0, 1]
        self.dif_6 = ["False", 0, 0, 0, 1]
        self.fg_1 = ["True", 0, 0, 0, 1]
        self.fg_2 = ["True", 100/100, 100/100, 59/100, 1]
        self.fg_3 = ["True", 1, 1, 1, 1]
        self.b1a = 1
        self.b2a = 1
        self.b3a = 1
        self.d1a = 1
        self.d2a = 1
        self.d3a = 1
        self.d4a = 1
        self.d5a = 1
        self.d6a = 1
        self.f1a = 1
        self.f2a = 1
        self.f3a = 1
        self.Object_Render()
        self.Object_Alpha()

        # Active Color
        self.rgb_1 = 0
        self.rgb_2 = 0
        self.rgb_3 = 0
        self.uvd_1 = 0
        self.uvd_2 = 0
        self.uvd_3 = 0
        self.d_previous = 0
        self.UVD_Hexagon_Points()
        self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Pigment_Display_Release(0)

        # SOF apply (requires active color first)
        self.SOF_1_APPLY(self.sof_1)
        self.SOF_2_APPLY(self.sof_2)
        self.SOF_3_APPLY(self.sof_3)

        # UI
        self.layout.option.setChecked(False)
        self.layout.aaa.setChecked(False)
        self.layout.rgb.setChecked(True)
        self.layout.ard.setChecked(False)
        self.layout.hsv.setChecked(False)
        self.layout.hsl.setChecked(False)
        self.layout.cmyk.setChecked(False)
        self.layout.tip.setChecked(False)
        self.layout.tts.setChecked(False)
        self.layout.mix.setCurrentIndex(0)
        self.layout.panel.setCurrentIndex(0)
        self.layout.obj.setChecked(True)
        self.layout.sof_sliders.setChecked(False)
        self.layout.gray_sliders.setChecked(False)
        self.layout.gray_panels.setChecked(False)
        self.Menu_Options(0)
        self.Menu_AAA(0)
        self.Menu_RGB(0)
        self.Menu_ARD(0)
        self.Menu_HSV(0)
        self.Menu_HSL(0)
        self.Menu_CMYK(0)
        self.Menu_TIP(0)
        self.Menu_TTS(0)
        self.Menu_MIX(0)
        self.Menu_PANEL(0)
        self.Menu_OBJ(0)
        self.Menu_SOF()

    def Settings_UI(self):
        # Brush Size Opacity Flow
        tip_sof_string = Krita.instance().readSetting("Pigment.O", "Tip SOF", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        tip_sof_split = tip_sof_string.split(",")
        try:
            self.lock_size = float(tip_sof_split[0])
            self.lock_opacity = float(tip_sof_split[1])
            self.lock_flow = float(tip_sof_split[2])
            self.sof_1 = float(tip_sof_split[0])
            self.sof_2 = float(tip_sof_split[1])
            self.sof_3 = float(tip_sof_split[2])
            self.tip_00.Setup_SOF(self.lock_size, self.lock_opacity, self.lock_flow)
        except:
            self.lock_size = size
            self.lock_opacity = opacity
            self.lock_flow = flow
            self.sof_1 = size
            self.sof_2 = opacity
            self.sof_3 = flow
            self.tip_00.Setup_SOF(size, opacity, flow)
        self.SOF_1_APPLY(self.sof_1)
        self.SOF_2_APPLY(self.sof_2)
        self.SOF_3_APPLY(self.sof_3)

        # UI
        self.Menu_Shrink()
        ui_string = Krita.instance().readSetting("Pigment.O", "UI", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        ui_split = ui_string.split(",")
        try:
            self.layout.option.setChecked(eval(ui_split[0]))
            self.layout.aaa.setChecked(eval(ui_split[1]))
            self.layout.rgb.setChecked(eval(ui_split[2]))
            self.layout.ard.setChecked(eval(ui_split[3]))
            self.layout.hsv.setChecked(eval(ui_split[4]))
            self.layout.hsl.setChecked(eval(ui_split[5]))
            self.layout.cmyk.setChecked(eval(ui_split[6]))
            self.layout.tip.setChecked(eval(ui_split[7]))
            self.layout.tts.setChecked(eval(ui_split[8]))
            self.layout.mix.setCurrentIndex(int(ui_split[9]))
            self.layout.panel.setCurrentIndex(int(ui_split[10]))
            self.layout.obj.setCurrentIndex(eval(ui_split[11]))
            self.layout.sof_sliders.setChecked(False)
            self.layout.gray_sliders.setChecked(False)
            self.layout.gray_panels.setChecked(False)
        except:
            self.layout.option.setChecked(False)
            self.layout.aaa.setChecked(False)
            self.layout.rgb.setChecked(True)
            self.layout.ard.setChecked(False)
            self.layout.hsv.setChecked(False)
            self.layout.hsl.setChecked(False)
            self.layout.cmyk.setChecked(False)
            self.layout.tip.setChecked(False)
            self.layout.tts.setChecked(False)
            self.layout.mix.setCurrentIndex(0)
            self.layout.panel.setCurrentIndex(0)
            self.layout.obj.setCurrentIndex(0)
            self.layout.sof_sliders.setChecked(False)
            self.layout.gray_sliders.setChecked(False)
            self.layout.gray_panels.setChecked(False)
    def Settings_Colors(self):
        # Variables
        self.zoom = 0

        # Active Color
        active_color_string = Krita.instance().readSetting("Pigment.O", "Active_Color", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        active_color_split = active_color_string.split(",")
        try:
            self.rgb_1 = float(active_color_split[0])
            self.rgb_2 = float(active_color_split[1])
            self.rgb_3 = float(active_color_split[2])
            self.uvd_1 = float(active_color_split[3])
            self.uvd_2 = float(active_color_split[4])
            self.uvd_3 = float(active_color_split[5])
            self.d_previous = float(active_color_split[6])
            self.UVD_Hexagon_Points()
            self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Pigment_Display_Release(0)
        except:
            self.rgb_1 = 0
            self.rgb_2 = 0
            self.rgb_3 = 0
            self.uvd_1 = 0
            self.uvd_2 = 0
            self.uvd_3 = 0
            self.d_previous = 0
            self.UVD_Hexagon_Points()
            self.Color_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Pigment_Display_Release(0)

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

        # Mixer ARD 1
        mixer_ard_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_ARD_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_ard_1_split = mixer_ard_1_string.split(",")
        if (mixer_ard_1_split[0] == "True" and mixer_ard_1_split[4] == "True"):
            # Gradient
            self.color_ard_l1 = ["True", float(mixer_ard_1_split[1]), float(mixer_ard_1_split[2]), float(mixer_ard_1_split[3])]
            self.color_ard_r1 = ["True", float(mixer_ard_1_split[5]), float(mixer_ard_1_split[6]), float(mixer_ard_1_split[7])]
            rgb_ard_l1 = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
            rgb_ard_r1 = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
            color_ard_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l1[0]*hexRGB, rgb_ard_l1[1]*hexRGB, rgb_ard_l1[2]*hexRGB))
            color_ard_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r1[0]*hexRGB, rgb_ard_r1[1]*hexRGB, rgb_ard_r1[2]*hexRGB))
            self.layout.ard_l1.setStyleSheet(color_ard_left_1)
            self.layout.ard_r1.setStyleSheet(color_ard_right_1)
        elif (mixer_ard_1_split[0] == "True" and mixer_ard_1_split[4] != "True"):
            # Color Left
            self.color_ard_l1 = ["True", float(mixer_ard_1_split[1]), float(mixer_ard_1_split[2]), float(mixer_ard_1_split[3])]
            self.color_ard_r1 = ["False", 0, 0, 0]
            rgb_ard_l1 = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
            color_ard_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l1[0]*hexRGB, rgb_ard_l1[1]*hexRGB, rgb_ard_l1[2]*hexRGB))
            self.layout.ard_l1.setStyleSheet(color_ard_left_1)
            self.layout.ard_r1.setStyleSheet(bg_alpha)
        elif (mixer_ard_1_split[0] != "True" and mixer_ard_1_split[4] == "True"):
            # Color Right
            self.color_ard_l1 = ["False", 0, 0, 0]
            self.color_ard_r1 = ["True", float(mixer_ard_1_split[5]), float(mixer_ard_1_split[6]), float(mixer_ard_1_split[7])]
            rgb_ard_r1 = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
            color_ard_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r1[0]*hexRGB, rgb_ard_r1[1]*hexRGB, rgb_ard_r1[2]*hexRGB))
            self.layout.ard_l1.setStyleSheet(bg_alpha)
            self.layout.ard_r1.setStyleSheet(color_ard_right_1)
        else:
            self.color_ard_l1 = ["False", 0, 0, 0]
            self.color_ard_r1 = ["False", 0, 0, 0]
            self.layout.ard_l1.setStyleSheet(bg_alpha)
            self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.percentage_ard_g1 = 0
        self.mixer_ard_g1.Update(self.percentage_ard_g1, self.layout.ard_g1.width())
        # Mixer ARD 2
        mixer_ard_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_ARD_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_ard_2_split = mixer_ard_2_string.split(",")
        if (mixer_ard_2_split[0] == "True" and mixer_ard_2_split[4] == "True"):
            # Gradient
            self.color_ard_l2 = ["True", float(mixer_ard_2_split[1]), float(mixer_ard_2_split[2]), float(mixer_ard_2_split[3])]
            self.color_ard_r2 = ["True", float(mixer_ard_2_split[5]), float(mixer_ard_2_split[6]), float(mixer_ard_2_split[7])]
            rgb_ard_l2 = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
            rgb_ard_r2 = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
            color_ard_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l2[0]*hexRGB, rgb_ard_l2[1]*hexRGB, rgb_ard_l2[2]*hexRGB))
            color_ard_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r2[0]*hexRGB, rgb_ard_r2[1]*hexRGB, rgb_ard_r2[2]*hexRGB))
            self.layout.ard_l2.setStyleSheet(color_ard_left_2)
            self.layout.ard_r2.setStyleSheet(color_ard_right_2)
        elif (mixer_ard_2_split[0] == "True" and mixer_ard_2_split[4] != "True"):
            # Color Left
            self.color_ard_l2 = ["True", float(mixer_ard_2_split[1]), float(mixer_ard_2_split[2]), float(mixer_ard_2_split[3])]
            self.color_ard_r2 = ["False", 0, 0, 0]
            rgb_ard_l2 = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
            color_ard_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l2[0]*hexRGB, rgb_ard_l2[1]*hexRGB, rgb_ard_l2[2]*hexRGB))
            self.layout.ard_l2.setStyleSheet(color_ard_left_2)
            self.layout.ard_r2.setStyleSheet(bg_alpha)
        elif (mixer_ard_2_split[0] != "True" and mixer_ard_2_split[4] == "True"):
            # Color Right
            self.color_ard_l2 = ["False", 0, 0, 0]
            self.color_ard_r2 = ["True", float(mixer_ard_2_split[5]), float(mixer_ard_2_split[6]), float(mixer_ard_2_split[7])]
            rgb_ard_r2 = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
            color_ard_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r2[0]*hexRGB, rgb_ard_r2[1]*hexRGB, rgb_ard_r2[2]*hexRGB))
            self.layout.ard_l2.setStyleSheet(bg_alpha)
            self.layout.ard_r2.setStyleSheet(color_ard_right_2)
        else:
            self.color_ard_l2 = ["False", 0, 0, 0]
            self.color_ard_r2 = ["False", 0, 0, 0]
            self.layout.ard_l2.setStyleSheet(bg_alpha)
            self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.percentage_ard_g2 = 0
        self.mixer_ard_g2.Update(self.percentage_ard_g2, self.layout.ard_g2.width())
        # Mixer ARD 3
        mixer_ard_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_ARD_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_ard_3_split = mixer_ard_3_string.split(",")
        if (mixer_ard_3_split[0] == "True" and mixer_ard_3_split[4] == "True"):
            # Gradient
            self.color_ard_l3 = ["True", float(mixer_ard_3_split[1]), float(mixer_ard_3_split[2]), float(mixer_ard_3_split[3])]
            self.color_ard_r3 = ["True", float(mixer_ard_3_split[5]), float(mixer_ard_3_split[6]), float(mixer_ard_3_split[7])]
            rgb_ard_l3 = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
            rgb_ard_r3 = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
            color_ard_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l3[0]*hexRGB, rgb_ard_l3[1]*hexRGB, rgb_ard_l3[2]*hexRGB))
            color_ard_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r3[0]*hexRGB, rgb_ard_r3[1]*hexRGB, rgb_ard_r3[2]*hexRGB))
            self.layout.ard_l3.setStyleSheet(color_ard_left_3)
            self.layout.ard_r3.setStyleSheet(color_ard_right_3)
        elif (mixer_ard_3_split[0] == "True" and mixer_ard_3_split[4] != "True"):
            # Color Left
            self.color_ard_l3 = ["True", float(mixer_ard_3_split[1]), float(mixer_ard_3_split[2]), float(mixer_ard_3_split[3])]
            self.color_ard_r3 = ["False", 0, 0, 0]
            rgb_ard_l3 = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
            color_ard_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l3[0]*hexRGB, rgb_ard_l3[1]*hexRGB, rgb_ard_l3[2]*hexRGB))
            self.layout.ard_l3.setStyleSheet(color_ard_left_3)
            self.layout.ard_r3.setStyleSheet(bg_alpha)
        elif (mixer_ard_3_split[0] != "True" and mixer_ard_3_split[4] == "True"):
            # Color Right
            self.color_ard_l3 = ["False", 0, 0, 0]
            self.color_ard_r3 = ["True", float(mixer_ard_3_split[5]), float(mixer_ard_3_split[6]), float(mixer_ard_3_split[7])]
            rgb_ard_r3 = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
            color_ard_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r3[0]*hexRGB, rgb_ard_r3[1]*hexRGB, rgb_ard_r3[2]*hexRGB))
            self.layout.ard_l3.setStyleSheet(bg_alpha)
            self.layout.ard_r3.setStyleSheet(color_ard_right_3)
        else:
            self.color_ard_l3 = ["False", 0, 0, 0]
            self.color_ard_r3 = ["False", 0, 0, 0]
            self.layout.ard_l3.setStyleSheet(bg_alpha)
            self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.percentage_ard_g3 = 0
        self.mixer_ard_g3.Update(self.percentage_ard_g3, self.layout.ard_g3.width())

        # Mixer HSV 1
        mixer_hsv_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSV_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsv_1_split = mixer_hsv_1_string.split(",")
        if (mixer_hsv_1_split[0] == "True" and mixer_hsv_1_split[4] == "True"):
            # Gradient
            self.color_hsv_l1 = ["True", float(mixer_hsv_1_split[1]), float(mixer_hsv_1_split[2]), float(mixer_hsv_1_split[3])]
            self.color_hsv_r1 = ["True", float(mixer_hsv_1_split[5]), float(mixer_hsv_1_split[6]), float(mixer_hsv_1_split[7])]
            rgb_hsv_l1 = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
            rgb_hsv_r1 = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
            color_hsv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l1[0]*hexRGB, rgb_hsv_l1[1]*hexRGB, rgb_hsv_l1[2]*hexRGB))
            color_hsv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r1[0]*hexRGB, rgb_hsv_r1[1]*hexRGB, rgb_hsv_r1[2]*hexRGB))
            self.layout.hsv_l1.setStyleSheet(color_hsv_left_1)
            self.layout.hsv_r1.setStyleSheet(color_hsv_right_1)
        elif (mixer_hsv_1_split[0] == "True" and mixer_hsv_1_split[4] != "True"):
            # Color Left
            self.color_hsv_l1 = ["True", float(mixer_hsv_1_split[1]), float(mixer_hsv_1_split[2]), float(mixer_hsv_1_split[3])]
            self.color_hsv_r1 = ["False", 0, 0, 0]
            rgb_hsv_l1 = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
            color_hsv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l1[0]*hexRGB, rgb_hsv_l1[1]*hexRGB, rgb_hsv_l1[2]*hexRGB))
            self.layout.hsv_l1.setStyleSheet(color_hsv_left_1)
            self.layout.hsv_r1.setStyleSheet(bg_alpha)
        elif (mixer_hsv_1_split[0] != "True" and mixer_hsv_1_split[4] == "True"):
            # Color Right
            self.color_hsv_l1 = ["False", 0, 0, 0]
            self.color_hsv_r1 = ["True", float(mixer_hsv_1_split[5]), float(mixer_hsv_1_split[6]), float(mixer_hsv_1_split[7])]
            rgb_hsv_r1 = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
            color_hsv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r1[0]*hexRGB, rgb_hsv_r1[1]*hexRGB, rgb_hsv_r1[2]*hexRGB))
            self.layout.hsv_l1.setStyleSheet(bg_alpha)
            self.layout.hsv_r1.setStyleSheet(color_hsv_right_1)
        else:
            self.color_hsv_l1 = ["False", 0, 0, 0]
            self.color_hsv_r1 = ["False", 0, 0, 0]
            self.layout.hsv_l1.setStyleSheet(bg_alpha)
            self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.percentage_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())
        # Mixer HSV 2
        mixer_hsv_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSV_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsv_2_split = mixer_hsv_2_string.split(",")
        if (mixer_hsv_2_split[0] == "True" and mixer_hsv_2_split[4] == "True"):
            # Gradient
            self.color_hsv_l2 = ["True", float(mixer_hsv_2_split[1]), float(mixer_hsv_2_split[2]), float(mixer_hsv_2_split[3])]
            self.color_hsv_r2 = ["True", float(mixer_hsv_2_split[5]), float(mixer_hsv_2_split[6]), float(mixer_hsv_2_split[7])]
            rgb_hsv_l2 = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
            rgb_hsv_r2 = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
            color_hsv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l2[0]*hexRGB, rgb_hsv_l2[1]*hexRGB, rgb_hsv_l2[2]*hexRGB))
            color_hsv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r2[0]*hexRGB, rgb_hsv_r2[1]*hexRGB, rgb_hsv_r2[2]*hexRGB))
            self.layout.hsv_l2.setStyleSheet(color_hsv_left_2)
            self.layout.hsv_r2.setStyleSheet(color_hsv_right_2)
        elif (mixer_hsv_2_split[0] == "True" and mixer_hsv_2_split[4] != "True"):
            # Color Left
            self.color_hsv_l2 = ["True", float(mixer_hsv_2_split[1]), float(mixer_hsv_2_split[2]), float(mixer_hsv_2_split[3])]
            self.color_hsv_r2 = ["False", 0, 0, 0]
            rgb_hsv_l2 = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
            color_hsv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l2[0]*hexRGB, rgb_hsv_l2[1]*hexRGB, rgb_hsv_l2[2]*hexRGB))
            self.layout.hsv_l2.setStyleSheet(color_hsv_left_2)
            self.layout.hsv_r2.setStyleSheet(bg_alpha)
        elif (mixer_hsv_2_split[0] != "True" and mixer_hsv_2_split[4] == "True"):
            # Color Right
            self.color_hsv_l2 = ["False", 0, 0, 0]
            self.color_hsv_r2 = ["True", float(mixer_hsv_2_split[5]), float(mixer_hsv_2_split[6]), float(mixer_hsv_2_split[7])]
            rgb_hsv_r2 = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
            color_hsv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r2[0]*hexRGB, rgb_hsv_r2[1]*hexRGB, rgb_hsv_r2[2]*hexRGB))
            self.layout.hsv_l2.setStyleSheet(bg_alpha)
            self.layout.hsv_r2.setStyleSheet(color_hsv_right_2)
        else:
            self.color_hsv_l2 = ["False", 0, 0, 0]
            self.color_hsv_r2 = ["False", 0, 0, 0]
            self.layout.hsv_l2.setStyleSheet(bg_alpha)
            self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.percentage_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())
        # Mixer HSV 3
        mixer_hsv_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSV_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsv_3_split = mixer_hsv_3_string.split(",")
        if (mixer_hsv_3_split[0] == "True" and mixer_hsv_3_split[4] == "True"):
            # Gradient
            self.color_hsv_l3 = ["True", float(mixer_hsv_3_split[1]), float(mixer_hsv_3_split[2]), float(mixer_hsv_3_split[3])]
            self.color_hsv_r3 = ["True", float(mixer_hsv_3_split[5]), float(mixer_hsv_3_split[6]), float(mixer_hsv_3_split[7])]
            rgb_hsv_l3 = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
            rgb_hsv_r3 = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
            color_hsv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l3[0]*hexRGB, rgb_hsv_l3[1]*hexRGB, rgb_hsv_l3[2]*hexRGB))
            color_hsv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r3[0]*hexRGB, rgb_hsv_r3[1]*hexRGB, rgb_hsv_r3[2]*hexRGB))
            self.layout.hsv_l3.setStyleSheet(color_hsv_left_3)
            self.layout.hsv_r3.setStyleSheet(color_hsv_right_3)
        elif (mixer_hsv_3_split[0] == "True" and mixer_hsv_3_split[4] != "True"):
            # Color Left
            self.color_hsv_l3 = ["True", float(mixer_hsv_3_split[1]), float(mixer_hsv_3_split[2]), float(mixer_hsv_3_split[3])]
            self.color_hsv_r3 = ["False", 0, 0, 0]
            rgb_hsv_l3 = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
            color_hsv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l3[0]*hexRGB, rgb_hsv_l3[1]*hexRGB, rgb_hsv_l3[2]*hexRGB))
            self.layout.hsv_l3.setStyleSheet(color_hsv_left_3)
            self.layout.hsv_r3.setStyleSheet(bg_alpha)
        elif (mixer_hsv_3_split[0] != "True" and mixer_hsv_3_split[4] == "True"):
            # Color Right
            self.color_hsv_l3 = ["False", 0, 0, 0]
            self.color_hsv_r3 = ["True", float(mixer_hsv_3_split[5]), float(mixer_hsv_3_split[6]), float(mixer_hsv_3_split[7])]
            rgb_hsv_r3 = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
            color_hsv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r3[0]*hexRGB, rgb_hsv_r3[1]*hexRGB, rgb_hsv_r3[2]*hexRGB))
            self.layout.hsv_l3.setStyleSheet(bg_alpha)
            self.layout.hsv_r3.setStyleSheet(color_hsv_right_3)
        else:
            self.color_hsv_l3 = ["False", 0, 0, 0]
            self.color_hsv_r3 = ["False", 0, 0, 0]
            self.layout.hsv_l3.setStyleSheet(bg_alpha)
            self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.percentage_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

        # Mixer HSL 1
        mixer_hsl_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSL_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsl_1_split = mixer_hsl_1_string.split(",")
        if (mixer_hsl_1_split[0] == "True" and mixer_hsl_1_split[4] == "True"):
            # Gradient
            self.color_hsl_l1 = ["True", float(mixer_hsl_1_split[1]), float(mixer_hsl_1_split[2]), float(mixer_hsl_1_split[3])]
            self.color_hsl_r1 = ["True", float(mixer_hsl_1_split[5]), float(mixer_hsl_1_split[6]), float(mixer_hsl_1_split[7])]
            rgb_hsl_l1 = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
            rgb_hsl_r1 = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
            color_hsl_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l1[0]*hexRGB, rgb_hsl_l1[1]*hexRGB, rgb_hsl_l1[2]*hexRGB))
            color_hsl_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r1[0]*hexRGB, rgb_hsl_r1[1]*hexRGB, rgb_hsl_r1[2]*hexRGB))
            self.layout.hsl_l1.setStyleSheet(color_hsl_left_1)
            self.layout.hsl_r1.setStyleSheet(color_hsl_right_1)
        elif (mixer_hsl_1_split[0] == "True" and mixer_hsl_1_split[4] != "True"):
            # Color Left
            self.color_hsl_l1 = ["True", float(mixer_hsl_1_split[1]), float(mixer_hsl_1_split[2]), float(mixer_hsl_1_split[3])]
            self.color_hsl_r1 = ["False", 0, 0, 0]
            rgb_hsl_l1 = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
            color_hsl_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l1[0]*hexRGB, rgb_hsl_l1[1]*hexRGB, rgb_hsl_l1[2]*hexRGB))
            self.layout.hsl_l1.setStyleSheet(color_hsl_left_1)
            self.layout.hsl_r1.setStyleSheet(bg_alpha)
        elif (mixer_hsl_1_split[0] != "True" and mixer_hsl_1_split[4] == "True"):
            # Color Right
            self.color_hsl_l1 = ["False", 0, 0, 0]
            self.color_hsl_r1 = ["True", float(mixer_hsl_1_split[5]), float(mixer_hsl_1_split[6]), float(mixer_hsl_1_split[7])]
            rgb_hsl_r1 = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
            color_hsl_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r1[0]*hexRGB, rgb_hsl_r1[1]*hexRGB, rgb_hsl_r1[2]*hexRGB))
            self.layout.hsl_l1.setStyleSheet(bg_alpha)
            self.layout.hsl_r1.setStyleSheet(color_hsl_right_1)
        else:
            self.color_hsl_l1 = ["False", 0, 0, 0]
            self.color_hsl_r1 = ["False", 0, 0, 0]
            self.layout.hsl_l1.setStyleSheet(bg_alpha)
            self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.percentage_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.percentage_hsl_g1, self.layout.hsl_g1.width())
        # Mixer HSL 2
        mixer_hsl_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSL_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsl_2_split = mixer_hsl_2_string.split(",")
        if (mixer_hsl_2_split[0] == "True" and mixer_hsl_2_split[4] == "True"):
            # Gradient
            self.color_hsl_l2 = ["True", float(mixer_hsl_2_split[1]), float(mixer_hsl_2_split[2]), float(mixer_hsl_2_split[3])]
            self.color_hsl_r2 = ["True", float(mixer_hsl_2_split[5]), float(mixer_hsl_2_split[6]), float(mixer_hsl_2_split[7])]
            rgb_hsl_l2 = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
            rgb_hsl_r2 = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
            color_hsl_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l2[0]*hexRGB, rgb_hsl_l2[1]*hexRGB, rgb_hsl_l2[2]*hexRGB))
            color_hsl_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r2[0]*hexRGB, rgb_hsl_r2[1]*hexRGB, rgb_hsl_r2[2]*hexRGB))
            self.layout.hsl_l2.setStyleSheet(color_hsl_left_2)
            self.layout.hsl_r2.setStyleSheet(color_hsl_right_2)
        elif (mixer_hsl_2_split[0] == "True" and mixer_hsl_2_split[4] != "True"):
            # Color Left
            self.color_hsl_l2 = ["True", float(mixer_hsl_2_split[1]), float(mixer_hsl_2_split[2]), float(mixer_hsl_2_split[3])]
            self.color_hsl_r2 = ["False", 0, 0, 0]
            rgb_hsl_l2 = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
            color_hsl_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l2[0]*hexRGB, rgb_hsl_l2[1]*hexRGB, rgb_hsl_l2[2]*hexRGB))
            self.layout.hsl_l2.setStyleSheet(color_hsl_left_2)
            self.layout.hsl_r2.setStyleSheet(bg_alpha)
        elif (mixer_hsl_2_split[0] != "True" and mixer_hsl_2_split[4] == "True"):
            # Color Right
            self.color_hsl_l2 = ["False", 0, 0, 0]
            self.color_hsl_r2 = ["True", float(mixer_hsl_2_split[5]), float(mixer_hsl_2_split[6]), float(mixer_hsl_2_split[7])]
            rgb_hsl_r2 = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
            color_hsl_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r2[0]*hexRGB, rgb_hsl_r2[1]*hexRGB, rgb_hsl_r2[2]*hexRGB))
            self.layout.hsl_l2.setStyleSheet(bg_alpha)
            self.layout.hsl_r2.setStyleSheet(color_hsl_right_2)
        else:
            self.color_hsl_l2 = ["False", 0, 0, 0]
            self.color_hsl_r2 = ["False", 0, 0, 0]
            self.layout.hsl_l2.setStyleSheet(bg_alpha)
            self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.percentage_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.percentage_hsl_g2, self.layout.hsl_g2.width())
        # Mixer HSL 3
        mixer_hsl_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_HSL_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_hsl_3_split = mixer_hsl_3_string.split(",")
        if (mixer_hsl_3_split[0] == "True" and mixer_hsl_3_split[4] == "True"):
            # Gradient
            self.color_hsl_l3 = ["True", float(mixer_hsl_3_split[1]), float(mixer_hsl_3_split[2]), float(mixer_hsl_3_split[3])]
            self.color_hsl_r3 = ["True", float(mixer_hsl_3_split[5]), float(mixer_hsl_3_split[6]), float(mixer_hsl_3_split[7])]
            rgb_hsl_l3 = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
            rgb_hsl_r3 = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
            color_hsl_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l3[0]*hexRGB, rgb_hsl_l3[1]*hexRGB, rgb_hsl_l3[2]*hexRGB))
            color_hsl_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r3[0]*hexRGB, rgb_hsl_r3[1]*hexRGB, rgb_hsl_r3[2]*hexRGB))
            self.layout.hsl_l3.setStyleSheet(color_hsl_left_3)
            self.layout.hsl_r3.setStyleSheet(color_hsl_right_3)
        elif (mixer_hsl_3_split[0] == "True" and mixer_hsl_3_split[4] != "True"):
            # Color Left
            self.color_hsl_l3 = ["True", float(mixer_hsl_3_split[1]), float(mixer_hsl_3_split[2]), float(mixer_hsl_3_split[3])]
            self.color_hsl_r3 = ["False", 0, 0, 0]
            rgb_hsl_l3 = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
            color_hsl_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l3[0]*hexRGB, rgb_hsl_l3[1]*hexRGB, rgb_hsl_l3[2]*hexRGB))
            self.layout.hsl_l3.setStyleSheet(color_hsl_left_3)
            self.layout.hsl_r3.setStyleSheet(bg_alpha)
        elif (mixer_hsl_3_split[0] != "True" and mixer_hsl_3_split[4] == "True"):
            # Color Right
            self.color_hsl_l3 = ["False", 0, 0, 0]
            self.color_hsl_r3 = ["True", float(mixer_hsl_3_split[5]), float(mixer_hsl_3_split[6]), float(mixer_hsl_3_split[7])]
            rgb_hsl_r3 = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
            color_hsl_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r3[0]*hexRGB, rgb_hsl_r3[1]*hexRGB, rgb_hsl_r3[2]*hexRGB))
            self.layout.hsl_l3.setStyleSheet(bg_alpha)
            self.layout.hsl_r3.setStyleSheet(color_hsl_right_3)
        else:
            self.color_hsl_l3 = ["False", 0, 0, 0]
            self.color_hsl_r3 = ["False", 0, 0, 0]
            self.layout.hsl_l3.setStyleSheet(bg_alpha)
            self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.percentage_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.percentage_hsl_g3, self.layout.hsl_g3.width())

        # Mixer CMYK 1
        mixer_cmyk_1_string = Krita.instance().readSetting("Pigment.O", "Mixer_CMYK_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_cmyk_1_split = mixer_cmyk_1_string.split(",")
        if (mixer_cmyk_1_split[0] == "True" and mixer_cmyk_1_split[5] == "True"):
            # Gradient
            self.color_cmyk_l1 = ["True", float(mixer_cmyk_1_split[1]), float(mixer_cmyk_1_split[2]), float(mixer_cmyk_1_split[3]), float(mixer_cmyk_1_split[4])]
            self.color_cmyk_r1 = ["True", float(mixer_cmyk_1_split[6]), float(mixer_cmyk_1_split[7]), float(mixer_cmyk_1_split[8]), float(mixer_cmyk_1_split[9])]
            rgb_cmyk_l1 = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
            rgb_cmyk_r1 = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
            color_cmyk_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l1[0]*hexRGB, rgb_cmyk_l1[1]*hexRGB, rgb_cmyk_l1[2]*hexRGB))
            color_cmyk_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r1[0]*hexRGB, rgb_cmyk_r1[1]*hexRGB, rgb_cmyk_r1[2]*hexRGB))
            self.layout.cmyk_l1.setStyleSheet(color_cmyk_left_1)
            self.layout.cmyk_r1.setStyleSheet(color_cmyk_right_1)
        elif (mixer_cmyk_1_split[0] == "True" and mixer_cmyk_1_split[5] != "True"):
            # Color Left
            self.color_cmyk_l1 = ["True", float(mixer_cmyk_1_split[1]), float(mixer_cmyk_1_split[2]), float(mixer_cmyk_1_split[3]), float(mixer_cmyk_1_split[4])]
            self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
            rgb_cmyk_l1 = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
            color_cmyk_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l1[0]*hexRGB, rgb_cmyk_l1[1]*hexRGB, rgb_cmyk_l1[2]*hexRGB))
            self.layout.cmyk_l1.setStyleSheet(color_cmyk_left_1)
            self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        elif (mixer_cmyk_1_split[0] != "True" and mixer_cmyk_1_split[5] == "True"):
            # Color Right
            self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r1 = ["True", float(mixer_cmyk_1_split[6]), float(mixer_cmyk_1_split[7]), float(mixer_cmyk_1_split[8]), float(mixer_cmyk_1_split[9])]
            rgb_cmyk_r1 = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
            color_cmyk_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r1[0]*hexRGB, rgb_cmyk_r1[1]*hexRGB, rgb_cmyk_r1[2]*hexRGB))
            self.layout.cmyk_l1.setStyleSheet(bg_alpha)
            self.layout.cmyk_r1.setStyleSheet(color_cmyk_right_1)
        else:
            self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
            self.layout.cmyk_l1.setStyleSheet(bg_alpha)
            self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.percentage_cmyk_g1, self.layout.cmyk_g1.width())
        # Mixer CMYK 2
        mixer_cmyk_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_CMYK_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_cmyk_2_split = mixer_cmyk_2_string.split(",")
        if (mixer_cmyk_2_split[0] == "True" and mixer_cmyk_2_split[5] == "True"):
            # Gradient
            self.color_cmyk_l2 = ["True", float(mixer_cmyk_2_split[1]), float(mixer_cmyk_2_split[2]), float(mixer_cmyk_2_split[3]), float(mixer_cmyk_2_split[4])]
            self.color_cmyk_r2 = ["True", float(mixer_cmyk_2_split[6]), float(mixer_cmyk_2_split[7]), float(mixer_cmyk_2_split[8]), float(mixer_cmyk_2_split[9])]
            rgb_cmyk_l2 = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
            rgb_cmyk_r2 = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
            color_cmyk_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l2[0]*hexRGB, rgb_cmyk_l2[1]*hexRGB, rgb_cmyk_l2[2]*hexRGB))
            color_cmyk_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r2[0]*hexRGB, rgb_cmyk_r2[1]*hexRGB, rgb_cmyk_r2[2]*hexRGB))
            self.layout.cmyk_l2.setStyleSheet(color_cmyk_left_2)
            self.layout.cmyk_r2.setStyleSheet(color_cmyk_right_2)
        elif (mixer_cmyk_2_split[0] == "True" and mixer_cmyk_2_split[5] != "True"):
            # Color Left
            self.color_cmyk_l2 =  ["True", float(mixer_cmyk_2_split[1]), float(mixer_cmyk_2_split[2]), float(mixer_cmyk_2_split[3]), float(mixer_cmyk_2_split[4])]
            self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
            rgb_cmyk_l2 = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
            color_cmyk_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l2[0]*hexRGB, rgb_cmyk_l2[1]*hexRGB, rgb_cmyk_l2[2]*hexRGB))
            self.layout.cmyk_l2.setStyleSheet(color_cmyk_left_2)
            self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        elif (mixer_cmyk_2_split[0] != "True" and mixer_cmyk_2_split[5] == "True"):
            # Color Right
            self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r2 = ["True", float(mixer_cmyk_2_split[6]), float(mixer_cmyk_2_split[7]), float(mixer_cmyk_2_split[8]), float(mixer_cmyk_2_split[9])]
            rgb_cmyk_r2 = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
            color_cmyk_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r2[0]*hexRGB, rgb_cmyk_r2[1]*hexRGB, rgb_cmyk_r2[2]*hexRGB))
            self.layout.cmyk_l2.setStyleSheet(bg_alpha)
            self.layout.cmyk_r2.setStyleSheet(color_cmyk_right_2)
        else:
            self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
            self.layout.cmyk_l2.setStyleSheet(bg_alpha)
            self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.percentage_cmyk_g2, self.layout.cmyk_g2.width())
        # Mixer CMYK 3
        mixer_cmyk_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_CMYK_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_cmyk_3_split = mixer_cmyk_3_string.split(",")
        if (mixer_cmyk_3_split[0] == "True" and mixer_cmyk_3_split[5] == "True"):
            # Gradient
            self.color_cmyk_l3 = ["True", float(mixer_cmyk_3_split[1]), float(mixer_cmyk_3_split[2]), float(mixer_cmyk_3_split[3]), float(mixer_cmyk_3_split[4])]
            self.color_cmyk_r3 = ["True", float(mixer_cmyk_3_split[6]), float(mixer_cmyk_3_split[7]), float(mixer_cmyk_3_split[8]), float(mixer_cmyk_3_split[9])]
            rgb_cmyk_l3 = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
            rgb_cmyk_r3 = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
            color_cmyk_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l3[0]*hexRGB, rgb_cmyk_l3[1]*hexRGB, rgb_cmyk_l3[2]*hexRGB))
            color_cmyk_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r3[0]*hexRGB, rgb_cmyk_r3[1]*hexRGB, rgb_cmyk_r3[2]*hexRGB))
            self.layout.cmyk_l3.setStyleSheet(color_cmyk_left_3)
            self.layout.cmyk_r3.setStyleSheet(color_cmyk_right_3)
        elif (mixer_cmyk_3_split[0] == "True" and mixer_cmyk_3_split[5] != "True"):
            # Color Left
            self.color_cmyk_l3 =  ["True", float(mixer_cmyk_3_split[1]), float(mixer_cmyk_3_split[2]), float(mixer_cmyk_3_split[3]), float(mixer_cmyk_3_split[4])]
            self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
            rgb_cmyk_l3 = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
            color_cmyk_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l3[0]*hexRGB, rgb_cmyk_l3[1]*hexRGB, rgb_cmyk_l3[2]*hexRGB))
            self.layout.cmyk_l3.setStyleSheet(color_cmyk_left_3)
            self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        elif (mixer_cmyk_3_split[0] != "True" and mixer_cmyk_3_split[5] == "True"):
            # Color Right
            self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r3 = ["True", float(mixer_cmyk_3_split[6]), float(mixer_cmyk_3_split[7]), float(mixer_cmyk_3_split[8]), float(mixer_cmyk_3_split[9])]
            rgb_cmyk_r3 = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
            color_cmyk_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r3[0]*hexRGB, rgb_cmyk_r3[1]*hexRGB, rgb_cmyk_r3[2]*hexRGB))
            self.layout.cmyk_l3.setStyleSheet(bg_alpha)
            self.layout.cmyk_r3.setStyleSheet(color_cmyk_right_3)
        else:
            self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
            self.layout.cmyk_l3.setStyleSheet(bg_alpha)
            self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.percentage_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.percentage_cmyk_g3, self.layout.cmyk_g3.width())

        # Mixer Gradient Display
        self.Mixer_Display()

        # Object
        object_01_string = Krita.instance().readSetting("Pigment.O", "Object_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_02_string = Krita.instance().readSetting("Pigment.O", "Object_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_03_string = Krita.instance().readSetting("Pigment.O", "Object_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_04_string = Krita.instance().readSetting("Pigment.O", "Object_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_05_string = Krita.instance().readSetting("Pigment.O", "Object_05", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_06_string = Krita.instance().readSetting("Pigment.O", "Object_06", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_07_string = Krita.instance().readSetting("Pigment.O", "Object_07", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_08_string = Krita.instance().readSetting("Pigment.O", "Object_08", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_09_string = Krita.instance().readSetting("Pigment.O", "Object_09", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_10_string = Krita.instance().readSetting("Pigment.O", "Object_10", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_11_string = Krita.instance().readSetting("Pigment.O", "Object_11", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_12_string = Krita.instance().readSetting("Pigment.O", "Object_12", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_01_split = object_01_string.split(",")
        object_02_split = object_02_string.split(",")
        object_03_split = object_03_string.split(",")
        object_04_split = object_04_string.split(",")
        object_05_split = object_05_string.split(",")
        object_06_split = object_06_string.split(",")
        object_07_split = object_07_string.split(",")
        object_08_split = object_08_string.split(",")
        object_09_split = object_09_string.split(",")
        object_10_split = object_10_string.split(",")
        object_11_split = object_11_string.split(",")
        object_12_split = object_12_string.split(",")
        try:
            self.bg_1 = [str(object_01_split[0]), float(object_01_split[1]), float(object_01_split[2]), float(object_01_split[3]), float(object_01_split[4])]
            self.bg_2 = [str(object_02_split[0]), float(object_02_split[1]), float(object_02_split[2]), float(object_02_split[3]), float(object_02_split[4])]
            self.bg_3 = [str(object_03_split[0]), float(object_03_split[1]), float(object_03_split[2]), float(object_03_split[3]), float(object_03_split[4])]
            self.dif_1 = [str(object_04_split[0]), float(object_04_split[1]), float(object_04_split[2]), float(object_04_split[3]), float(object_04_split[4])]
            self.dif_2 = [str(object_05_split[0]), float(object_05_split[1]), float(object_05_split[2]), float(object_05_split[3]), float(object_05_split[4])]
            self.dif_3 = [str(object_06_split[0]), float(object_06_split[1]), float(object_06_split[2]), float(object_06_split[3]), float(object_06_split[4])]
            self.dif_4 = [str(object_07_split[0]), float(object_07_split[1]), float(object_07_split[2]), float(object_07_split[3]), float(object_07_split[4])]
            self.dif_5 = [str(object_08_split[0]), float(object_08_split[1]), float(object_08_split[2]), float(object_08_split[3]), float(object_08_split[4])]
            self.dif_6 = [str(object_09_split[0]), float(object_09_split[1]), float(object_09_split[2]), float(object_09_split[3]), float(object_09_split[4])]
            self.fg_1 = [str(object_10_split[0]), float(object_10_split[1]), float(object_10_split[2]), float(object_10_split[3]), float(object_10_split[4])]
            self.fg_2 = [str(object_11_split[0]), float(object_11_split[1]), float(object_11_split[2]), float(object_11_split[3]), float(object_11_split[4])]
            self.fg_3 = [str(object_12_split[0]), float(object_12_split[1]), float(object_12_split[2]), float(object_12_split[3]), float(object_12_split[4])]
            self.b1a = float(object_01_split[4])
            self.b2a = float(object_02_split[4])
            self.b3a = float(object_03_split[4])
            self.d1a = float(object_04_split[4])
            self.d2a = float(object_05_split[4])
            self.d3a = float(object_06_split[4])
            self.d4a = float(object_07_split[4])
            self.d5a = float(object_08_split[4])
            self.d6a = float(object_09_split[4])
            self.f1a = float(object_10_split[4])
            self.f2a = float(object_11_split[4])
            self.f3a = float(object_12_split[4])
        except:
            self.bg_1 = ["False", 0, 0, 0, 0]
            self.bg_2 = ["False", 0, 0, 0, 1]
            self.bg_3 = ["False", 0, 0, 0, 1]
            self.dif_1 = ["False", 0, 0, 0, 1]
            self.dif_2 = ["False", 0, 0, 0, 1]
            self.dif_3 = ["False", 0, 0, 0, 1]
            self.dif_4 = ["False", 0, 0, 0, 1]
            self.dif_5 = ["False", 0, 0, 0, 1]
            self.dif_6 = ["False", 0, 0, 0, 1]
            self.fg_1 = ["False", 0, 0, 0, 1]
            self.fg_2 = ["False", 0, 0, 0, 1]
            self.fg_3 = ["False", 0, 0, 0, 1]
            self.b1a = 0
            self.b2a = 1
            self.b3a = 1
            self.d1a = 1
            self.d2a = 1
            self.d3a = 1
            self.d4a = 1
            self.d5a = 1
            self.d6a = 1
            self.f1a = 1
            self.f2a = 1
            self.f3a = 1
        # File Paths
        self.path_bg_1 = str(self.dir_name + "/OBJECT/SPHERE/bg_1.png")
        self.path_bg_2 = str(self.dir_name + "/OBJECT/SPHERE/bg_2.png")
        self.path_bg_3 = str(self.dir_name + "/OBJECT/SPHERE/bg_3.png")
        self.path_dif_1 = str(self.dir_name + "/OBJECT/SPHERE/dif_1.png")
        self.path_dif_2 = str(self.dir_name + "/OBJECT/SPHERE/dif_2.png")
        self.path_dif_3 = str(self.dir_name + "/OBJECT/SPHERE/dif_3.png")
        self.path_dif_4 = str(self.dir_name + "/OBJECT/SPHERE/dif_4.png")
        self.path_dif_5 = str(self.dir_name + "/OBJECT/SPHERE/dif_5.png")
        self.path_dif_6 = str(self.dir_name + "/OBJECT/SPHERE/dif_6.png")
        self.path_fg_1 = str(self.dir_name + "/OBJECT/SPHERE/fg_1.png")
        self.path_fg_2 = str(self.dir_name + "/OBJECT/SPHERE/fg_2.png")
        self.path_fg_3 = str(self.dir_name + "/OBJECT/SPHERE/fg_3.png")
        # Reload Layers
        self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, self.bg_2[1]*255, self.bg_2[2]*255, self.bg_2[3]*255, self.bg_2[4]*255))
        self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, self.bg_3[1]*255, self.bg_3[2]*255, self.bg_3[3]*255, self.bg_3[4]*255))
        self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, self.dif_1[1]*255, self.dif_1[2]*255, self.dif_1[3]*255, self.dif_1[4]*255))
        self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, self.dif_2[1]*255, self.dif_2[2]*255, self.dif_2[3]*255, self.dif_2[4]*255))
        self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, self.dif_3[1]*255, self.dif_3[2]*255, self.dif_3[3]*255, self.dif_3[4]*255))
        self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, self.dif_4[1]*255, self.dif_4[2]*255, self.dif_4[3]*255, self.dif_4[4]*255))
        self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, self.dif_5[1]*255, self.dif_5[2]*255, self.dif_5[3]*255, self.dif_5[4]*255))
        self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, self.dif_6[1]*255, self.dif_6[2]*255, self.dif_6[3]*255, self.dif_6[4]*255))
        self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, self.fg_1[1]*255, self.fg_1[2]*255, self.fg_1[3]*255, self.fg_1[4]*255))
        self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, self.fg_2[1]*255, self.fg_2[2]*255, self.fg_2[3]*255, self.fg_2[4]*255))
        self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, self.fg_3[1]*255, self.fg_3[2]*255, self.fg_3[3]*255, self.fg_3[4]*255))
        if self.bg_1[0] == "True":
            self.BG_1_SAVE(self.bg_1[1], self.bg_1[2], self.bg_1[3], self.bg_1[4], 0)
        if self.bg_2[0] == "True":
            self.BG_2_SAVE(self.bg_2[1], self.bg_2[2], self.bg_2[3], self.bg_2[4], 0)
        if self.bg_3[0] == "True":
            self.BG_3_SAVE(self.bg_3[1], self.bg_3[2], self.bg_3[3], self.bg_3[4], 0)
        if self.dif_1[0] == "True":
            self.DIF_1_SAVE(self.dif_1[1], self.dif_1[2], self.dif_1[3], self.dif_1[4], 0)
        if self.dif_2[0] == "True":
            self.DIF_2_SAVE(self.dif_2[1], self.dif_2[2], self.dif_2[3], self.dif_2[4], 0)
        if self.dif_3[0] == "True":
            self.DIF_3_SAVE(self.dif_3[1], self.dif_3[2], self.dif_3[3], self.dif_3[4], 0)
        if self.dif_4[0] == "True":
            self.DIF_4_SAVE(self.dif_4[1], self.dif_4[2], self.dif_4[3], self.dif_4[4], 0)
        if self.dif_5[0] == "True":
            self.DIF_5_SAVE(self.dif_5[1], self.dif_5[2], self.dif_5[3], self.dif_5[4], 0)
        if self.dif_6[0] == "True":
            self.DIF_6_SAVE(self.dif_6[1], self.dif_6[2], self.dif_6[3], self.dif_6[4], 0)
        if self.fg_1[0] == "True":
            self.FG_1_SAVE(self.fg_1[1], self.fg_1[2], self.fg_1[3], self.fg_1[4], 0)
        if self.fg_2[0] == "True":
            self.FG_2_SAVE(self.fg_2[1], self.fg_2[2], self.fg_2[3], self.fg_2[4], 0)
        if self.fg_3[0] == "True":
            self.FG_3_SAVE(self.fg_3[1], self.fg_3[2], self.fg_3[3], self.fg_3[4], 0)

    def Settings_Save(self):
        try:
            # Brush Size Opacity Flow
            if ((self.canvas() is not None) and (self.canvas().view() is not None)):
                # Save Settings
                tip_sof_list = (str(self.lock_size), str(self.lock_opacity), str(self.lock_flow))
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
            mixer_list_ard_1 = (str(self.color_ard_l1[0]), str(self.color_ard_l1[1]), str(self.color_ard_l1[2]), str(self.color_ard_l1[3]), str(self.color_ard_r1[0]), str(self.color_ard_r1[1]), str(self.color_ard_r1[2]), str(self.color_ard_r1[3]))
            mixer_list_ard_2 = (str(self.color_ard_l2[0]), str(self.color_ard_l2[1]), str(self.color_ard_l2[2]), str(self.color_ard_l2[3]), str(self.color_ard_r2[0]), str(self.color_ard_r2[1]), str(self.color_ard_r2[2]), str(self.color_ard_r2[3]))
            mixer_list_ard_3 = (str(self.color_ard_l3[0]), str(self.color_ard_l3[1]), str(self.color_ard_l3[2]), str(self.color_ard_l3[3]), str(self.color_ard_r3[0]), str(self.color_ard_r3[1]), str(self.color_ard_r3[2]), str(self.color_ard_r3[3]))
            mixer_list_hsv_1 = (str(self.color_hsv_l1[0]), str(self.color_hsv_l1[1]), str(self.color_hsv_l1[2]), str(self.color_hsv_l1[3]), str(self.color_hsv_r1[0]),  str(self.color_hsv_r1[1]), str(self.color_hsv_r1[2]), str(self.color_hsv_r1[3]))
            mixer_list_hsv_2 = (str(self.color_hsv_l2[0]), str(self.color_hsv_l2[1]), str(self.color_hsv_l2[2]), str(self.color_hsv_l2[3]), str(self.color_hsv_r2[0]),  str(self.color_hsv_r2[1]), str(self.color_hsv_r2[2]), str(self.color_hsv_r2[3]))
            mixer_list_hsv_3 = (str(self.color_hsv_l3[0]), str(self.color_hsv_l3[1]), str(self.color_hsv_l3[2]), str(self.color_hsv_l3[3]), str(self.color_hsv_r3[0]),  str(self.color_hsv_r3[1]), str(self.color_hsv_r3[2]), str(self.color_hsv_r3[3]))
            mixer_list_hsl_1 = (str(self.color_hsl_l1[0]), str(self.color_hsl_l1[1]), str(self.color_hsl_l1[2]), str(self.color_hsl_l1[3]), str(self.color_hsl_r1[0]),  str(self.color_hsl_r1[1]), str(self.color_hsl_r1[2]), str(self.color_hsl_r1[3]))
            mixer_list_hsl_2 = (str(self.color_hsl_l2[0]), str(self.color_hsl_l2[1]), str(self.color_hsl_l2[2]), str(self.color_hsl_l2[3]), str(self.color_hsl_r2[0]),  str(self.color_hsl_r2[1]), str(self.color_hsl_r2[2]), str(self.color_hsl_r2[3]))
            mixer_list_hsl_3 = (str(self.color_hsl_l3[0]), str(self.color_hsl_l3[1]), str(self.color_hsl_l3[2]), str(self.color_hsl_l3[3]), str(self.color_hsl_r3[0]),  str(self.color_hsl_r3[1]), str(self.color_hsl_r3[2]), str(self.color_hsl_r3[3]))
            mixer_list_cmyk_1 = (str(self.color_cmyk_l1[0]), str(self.color_cmyk_l1[1]), str(self.color_cmyk_l1[2]), str(self.color_cmyk_l1[3]), str(self.color_cmyk_l1[4]), str(self.color_cmyk_r1[0]),  str(self.color_cmyk_r1[1]), str(self.color_cmyk_r1[2]), str(self.color_cmyk_r1[3]), str(self.color_cmyk_r1[4]))
            mixer_list_cmyk_2 = (str(self.color_cmyk_l2[0]), str(self.color_cmyk_l2[1]), str(self.color_cmyk_l2[2]), str(self.color_cmyk_l2[3]), str(self.color_cmyk_l2[4]), str(self.color_cmyk_r2[0]),  str(self.color_cmyk_r2[1]), str(self.color_cmyk_r2[2]), str(self.color_cmyk_r2[3]), str(self.color_cmyk_r2[4]))
            mixer_list_cmyk_3 = (str(self.color_cmyk_l3[0]), str(self.color_cmyk_l3[1]), str(self.color_cmyk_l3[2]), str(self.color_cmyk_l3[3]), str(self.color_cmyk_l3[4]), str(self.color_cmyk_r3[0]),  str(self.color_cmyk_r3[1]), str(self.color_cmyk_r3[2]), str(self.color_cmyk_r3[3]), str(self.color_cmyk_r3[4]))
            mixer_string_rgb_1 = ','.join(mixer_list_rgb_1)
            mixer_string_rgb_2 = ','.join(mixer_list_rgb_2)
            mixer_string_rgb_3 = ','.join(mixer_list_rgb_3)
            mixer_string_ard_1 = ','.join(mixer_list_ard_1)
            mixer_string_ard_2 = ','.join(mixer_list_ard_2)
            mixer_string_ard_3 = ','.join(mixer_list_ard_3)
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
            Krita.instance().writeSetting("Pigment.O", "Mixer_ARD_1", mixer_string_ard_1)
            Krita.instance().writeSetting("Pigment.O", "Mixer_ARD_2", mixer_string_ard_2)
            Krita.instance().writeSetting("Pigment.O", "Mixer_ARD_3", mixer_string_ard_3)
            Krita.instance().writeSetting("Pigment.O", "Mixer_HSV_1", mixer_string_hsv_1)
            Krita.instance().writeSetting("Pigment.O", "Mixer_HSV_2", mixer_string_hsv_2)
            Krita.instance().writeSetting("Pigment.O", "Mixer_HSV_3", mixer_string_hsv_3)
            Krita.instance().writeSetting("Pigment.O", "Mixer_HSL_1", mixer_string_hsl_1)
            Krita.instance().writeSetting("Pigment.O", "Mixer_HSL_2", mixer_string_hsl_2)
            Krita.instance().writeSetting("Pigment.O", "Mixer_HSL_3", mixer_string_hsl_3)
            Krita.instance().writeSetting("Pigment.O", "Mixer_CMYK_1", mixer_string_cmyk_1)
            Krita.instance().writeSetting("Pigment.O", "Mixer_CMYK_2", mixer_string_cmyk_2)
            Krita.instance().writeSetting("Pigment.O", "Mixer_CMYK_3", mixer_string_cmyk_3)

            # Object
            object_list_01 = (str(self.bg_1[0]), str(self.bg_1[1]), str(self.bg_1[2]), str(self.bg_1[3]), str(self.bg_1[4]))
            object_list_02 = (str(self.bg_2[0]), str(self.bg_2[1]), str(self.bg_2[2]), str(self.bg_2[3]), str(self.bg_2[4]))
            object_list_03 = (str(self.bg_3[0]), str(self.bg_3[1]), str(self.bg_3[2]), str(self.bg_3[3]), str(self.bg_3[4]))
            object_list_04 = (str(self.dif_1[0]), str(self.dif_1[1]), str(self.dif_1[2]), str(self.dif_1[3]), str(self.dif_1[4]))
            object_list_05 = (str(self.dif_2[0]), str(self.dif_2[1]), str(self.dif_2[2]), str(self.dif_2[3]), str(self.dif_2[4]))
            object_list_06 = (str(self.dif_3[0]), str(self.dif_3[1]), str(self.dif_3[2]), str(self.dif_3[3]), str(self.dif_3[4]))
            object_list_07 = (str(self.dif_4[0]), str(self.dif_4[1]), str(self.dif_4[2]), str(self.dif_4[3]), str(self.dif_4[4]))
            object_list_08 = (str(self.dif_5[0]), str(self.dif_5[1]), str(self.dif_5[2]), str(self.dif_5[3]), str(self.dif_5[4]))
            object_list_09 = (str(self.dif_6[0]), str(self.dif_6[1]), str(self.dif_6[2]), str(self.dif_6[3]), str(self.dif_6[4]))
            object_list_10 = (str(self.fg_1[0]), str(self.fg_1[1]), str(self.fg_1[2]), str(self.fg_1[3]), str(self.fg_1[4]))
            object_list_11 = (str(self.fg_2[0]), str(self.fg_2[1]), str(self.fg_2[2]), str(self.fg_2[3]), str(self.fg_2[4]))
            object_list_12 = (str(self.fg_3[0]), str(self.fg_3[1]), str(self.fg_3[2]), str(self.fg_3[3]), str(self.fg_3[4]))
            object_string_01 = ','.join(object_list_01)
            object_string_02 = ','.join(object_list_02)
            object_string_03 = ','.join(object_list_03)
            object_string_04 = ','.join(object_list_04)
            object_string_05 = ','.join(object_list_05)
            object_string_06 = ','.join(object_list_06)
            object_string_07 = ','.join(object_list_07)
            object_string_08 = ','.join(object_list_08)
            object_string_09 = ','.join(object_list_09)
            object_string_10 = ','.join(object_list_10)
            object_string_11 = ','.join(object_list_11)
            object_string_12 = ','.join(object_list_12)
            Krita.instance().writeSetting("Pigment.O", "Object_01", object_string_01)
            Krita.instance().writeSetting("Pigment.O", "Object_02", object_string_02)
            Krita.instance().writeSetting("Pigment.O", "Object_03", object_string_03)
            Krita.instance().writeSetting("Pigment.O", "Object_04", object_string_04)
            Krita.instance().writeSetting("Pigment.O", "Object_05", object_string_05)
            Krita.instance().writeSetting("Pigment.O", "Object_06", object_string_06)
            Krita.instance().writeSetting("Pigment.O", "Object_07", object_string_07)
            Krita.instance().writeSetting("Pigment.O", "Object_08", object_string_08)
            Krita.instance().writeSetting("Pigment.O", "Object_09", object_string_09)
            Krita.instance().writeSetting("Pigment.O", "Object_10", object_string_10)
            Krita.instance().writeSetting("Pigment.O", "Object_11", object_string_11)
            Krita.instance().writeSetting("Pigment.O", "Object_12", object_string_12)

            # UI
            ui_list = (
                str(self.layout.option.isChecked()),
                str(self.layout.aaa.isChecked()),
                str(self.layout.rgb.isChecked()),
                str(self.layout.ard.isChecked()),
                str(self.layout.hsv.isChecked()),
                str(self.layout.hsl.isChecked()),
                str(self.layout.cmyk.isChecked()),
                str(self.layout.tip.isChecked()),
                str(self.layout.tts.isChecked()),
                str(self.layout.mix.currentIndex()),
                str(self.layout.panel.currentIndex()),
                str(self.layout.obj.currentIndex()),
                )
            ui_string = ','.join(ui_list)
            Krita.instance().writeSetting("Pigment.O", "UI", ui_string)
        except:
            pass
    def Settings_Save_Color(self):
        # Active Color
        active_color_list = (
            str(self.rgb_1),
            str(self.rgb_2),
            str(self.rgb_3),
            str(self.uvd_1),
            str(self.uvd_2),
            str(self.uvd_3),
            str(self.d_previous),
            )
        active_color_string = ','.join(active_color_list)
        Krita.instance().writeSetting("Pigment.O", "Active_Color", active_color_string)

    #//
    #\\ Change the Canvas ######################################################
    def canvasChanged(self, canvas):
        pass
    #//
