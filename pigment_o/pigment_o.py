# Import Krita
from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic
import os.path
import math
from random import randint
# Pigment.O Modules
from .pigment_o_modulo import (
    Channel_Linear,
    Clicks,
    Mixer_Gradient,
    Panel_UVD,
    Panel_ARD,
    Panel_HSV,
    Panel_HSL
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
bg_eraser_on = str("background-color: rgba(212, 212, 212, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_eraser_off = str("background-color: rgba(56, 56, 56, 255);")


# Create Docker
class PigmentODocker(DockWidget):
    """
    Compact Color Picker and Mixer.
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

    # Construct Plugin}
    def User_Interface(self):
        # Widget
        self.window = QWidget()
        self.layout = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/pigment_o.ui', self.window)
        self.setWidget(self.window)
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
    def Setup(self):
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
            self.Krita_Timer()
        else:
            self.layout.check.setCheckState(0)
    def Connect(self):
        # UI Display Options
        self.layout.check.stateChanged.connect(self.Krita_Timer)
        self.layout.sof.toggled.connect(self.Menu_SOF)
        self.layout.gray_sliders.toggled.connect(self.Menu_Gray)
        self.layout.gray_panels.toggled.connect(self.Menu_Gray)
        self.layout.aaa.toggled.connect(self.Menu_AAA)
        self.layout.rgb.toggled.connect(self.Menu_RGB)
        self.layout.ard.toggled.connect(self.Menu_ARD)
        self.layout.hsv.toggled.connect(self.Menu_HSV)
        self.layout.hsl.toggled.connect(self.Menu_HSL)
        self.layout.cmyk.toggled.connect(self.Menu_CMYK)
        self.layout.tip.toggled.connect(self.Menu_TIP)
        self.layout.tts.toggled.connect(self.Menu_TTS)
        self.layout.mixer_selector.currentTextChanged.connect(self.Menu_Mixer)
        self.layout.panel_selector.currentTextChanged.connect(self.Menu_Panel)

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
        # Channel LIGHT
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
        self.panel_hsv = Panel_HSV(self.layout.panel_hsv_fg)
        self.panel_hsv.SIGNAL_HSV_VALUE.connect(self.Signal_HSV)
        self.panel_hsv.SIGNAL_HSV_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsv.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HSV
        self.panel_hsl = Panel_HSL(self.layout.panel_hsl_fg)
        self.panel_hsl.SIGNAL_HSL_VALUE.connect(self.Signal_HSL)
        self.panel_hsl.SIGNAL_HSL_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsl.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel ARD
        self.panel_ard = Panel_ARD(self.layout.panel_ard_fg)
        self.panel_ard.SIGNAL_ARD_VALUE.connect(self.Signal_ARD)
        self.panel_ard.SIGNAL_ARD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_ard.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel UVD
        self.panel_rgb = Panel_UVD(self.layout.panel_uvd_input)
        self.panel_rgb.SIGNAL_UVD_VALUE.connect(self.Signal_UVD)
        self.panel_rgb.SIGNAL_UVD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_rgb.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
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
        self.layout.tip_00.setStyleSheet(bg_alpha)

    # Menu Displays ############################################################
    def Menu_SOF(self):
        font = self.layout.sof.font()
        if self.layout.sof.isChecked():
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
        self.layout.sof.setFont(font)
        self.Pigment_Display()
        self.Settings_Save()
    def Menu_Gray(self):
        self.Pigment_Display()
        self.Settings_Save()
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
        self.Pigment_Display()
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
        self.Pigment_Display()
        self.Settings_Save()
    def Menu_ARD(self):
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
        self.Pigment_Display()
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
        self.Pigment_Display()
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
        self.Pigment_Display()
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
            self.layout.percentage_bot.setMinimumHeight(ui_min_1)
            self.layout.percentage_bot.setMaximumHeight(ui_max_1)
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
            self.layout.hex_string.setMinimumHeight(zero)
            self.layout.hex_string.setMaximumHeight(zero)
    def Menu_TIP(self):
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
            self.layout.cores.setContentsMargins(0, ui_vspacer, 0, ui_vspacer)
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
        self.Mixer_Display()
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
            self.layout.percentage_ard_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_ard_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_ard_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_ard_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_ard.setContentsMargins(0, 0, 0, ui_margin)
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
        self.Mixer_Display()
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
        self.layout.mixer_ard.setContentsMargins(0, 0, 0, zero)
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
        self.Panel_Shrink()
        panel = self.layout.panel_selector.currentText()
        if panel == "PANEL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if panel == "HSV":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSV()
        if panel == "HSL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSL()
        if panel == "ARD":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_RGB()
        if panel == "UVD":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert_RGB()
        self.Settings_Save()
    def Panel_Shrink(self):
        self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    def Menu_Load(self):
        # SOF
        font = self.layout.sof.font()
        if self.layout.sof.isChecked():
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
        self.layout.sof.setFont(font)
        # GRAY
        self.Pigment_Display()
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
        # ARD
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
        # TIP
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
            self.layout.cores.setContentsMargins(0, ui_vspacer, 0, ui_margin)
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
            self.layout.percentage_ard_1.setMinimumHeight(ui_vspacer)
            self.layout.percentage_ard_1.setMaximumHeight(ui_vspacer)
            self.layout.percentage_ard_2.setMinimumHeight(ui_vspacer)
            self.layout.percentage_ard_2.setMaximumHeight(ui_vspacer)
            self.layout.mixer_ard.setContentsMargins(0, 0, 0, ui_margin)
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
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if panel == "HSV":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSV()
        if panel == "HSL":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_HSL()
        if panel == "ARD":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.Pigment_Convert_RGB()
        if panel == "UVD":
            self.layout.panel_neutral.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsv_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_hsl_bg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert_RGB()

    # Krita to Pigment #########################################################
    def Krita_Timer(self):
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
            self.layout.check.setText("C=0")
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

    # Apply Color ##############################################################
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

    # Convert ##################################################################
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

    # Sync Channels ############################################################
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
        self.UVD_Update()
        self.ARD_Update()
        self.panel_hsv.Update_Panel(self.hsv_2, self.hsv_3, self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        self.panel_hsl.Update_Panel(self.hsl_2, self.hsl_3, self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        # Material Live Panel
        # self.object_slider.Update(self.sha_1, self.layout.object_slider.width())
        # self.light_slider.Update(self.sha_2, self.layout.light_slider.width())
        # self.ambient_slider.Update(self.sha_3, self.layout.ambient_slider.width())
        # self.background_slider.Update(self.sha_4, self.layout.background_slider.width())
        panel = self.layout.panel_selector.currentText()
        if panel == "SPHERE":
            self.Shader_Object_Live()
            self.Shader_Light_Live()
            self.Shader_Ambient_Live()
            self.Shader_Background_Live()

    # Send to Krita ############################################################
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
        # SOF
        if self.layout.sof.isChecked() == True:
            sss_sof1 = str(self.NEU_Gradient(self.sof_1 / kritaS))
            sss_sof2 = str(self.NEU_Gradient(self.sof_2))
            sss_sof3 = str(self.NEU_Gradient(self.sof_3))
        else:
            sss_sof1 = str(self.NEU_Gradient(self.lock_size / kritaS))
            sss_sof2 = str(self.NEU_Gradient(self.lock_opacity))
            sss_sof3 = str(self.NEU_Gradient(self.lock_flow))
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
        panel = self.layout.panel_selector.currentText()
        # Colors for Panels
        if panel == "PANEL":
            self.layout.panel_neutral.setStyleSheet(bg_unseen)
        # Foreground Color
        if panel == "FGC":
            if self.layout.gray_panels.isChecked() == False:
                foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.rgb_1*hexRGB, self.rgb_2*hexRGB, self.rgb_3*hexRGB))
                self.layout.panel_neutral.setStyleSheet(foreground_color)
            if self.layout.gray_panels.isChecked() == True:
                foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*kritaRGB, self.aaa_1*kritaRGB, self.aaa_1*kritaRGB))
                self.layout.panel_neutral.setStyleSheet(foreground_color)
        else:
            self.layout.panel_neutral.setStyleSheet(bg_unseen)
        # HSV Color
        if panel == "HSV":
            if self.layout.gray_panels.isChecked() == False:
                hue_left = [self.hsv_1, 0, 1]
                hue_right = [self.hsv_1, 1, 1]
                base_color = self.HSV_Gradient(self.layout.hsv_1_slider.width(), hue_left, hue_right)
                self.layout.panel_hsv_bg.setStyleSheet(base_color)
                base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
                self.layout.panel_hsv_fg.setStyleSheet(base_value)
            if self.layout.gray_panels.isChecked() == True:
                self.layout.panel_hsv_bg.setStyleSheet(bg_unseen)
                base_value = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*hexRGB, self.aaa_1*hexRGB, self.aaa_1*hexRGB))
                self.layout.panel_hsv_fg.setStyleSheet(base_value)
        else:
            self.layout.panel_hsv_bg.setStyleSheet(bg_unseen)
            self.layout.panel_hsv_fg.setStyleSheet(bg_unseen)
        # HSL Color
        if panel == "HSL":
            if self.layout.gray_panels.isChecked() == False:
                hue_left = [self.hsl_1, 0, 0.5]
                hue_right = [self.hsl_1, 1, 0.5]
                base_color = self.HSL_Gradient(self.layout.hsl_1_slider.width(), hue_left, hue_right)
                self.layout.panel_hsl_bg.setStyleSheet(base_color)
                base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.5 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
                self.layout.panel_hsl_fg.setStyleSheet(base_value)
            if self.layout.gray_panels.isChecked() == True:
                self.layout.panel_hsl_bg.setStyleSheet(bg_unseen)
                base_value = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*hexRGB, self.aaa_1*hexRGB, self.aaa_1*hexRGB))
                self.layout.panel_hsl_fg.setStyleSheet(base_value)
        else:
            self.layout.panel_hsl_bg.setStyleSheet(bg_unseen)
            self.layout.panel_hsl_fg.setStyleSheet(bg_unseen)
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
        # Apply ALL Channel Style Sheets
        self.layout.sof_1_slider.setStyleSheet(sss_sof1)
        self.layout.sof_2_slider.setStyleSheet(sss_sof2)
        self.layout.sof_3_slider.setStyleSheet(sss_sof3)
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
        self.mixer_ard_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())
        self.mixer_ard_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())
        self.mixer_ard_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())
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
        width = self.layout.panel_uvd.width()
        height = self.layout.panel_uvd.height()
        # For when UVD Pnale is Minimized
        if width <= 0:
            width = 1
        if height <= 0:
            height = 1
        # Shape Mask like a Perfect Square
        if width >= height:
            self.layout.panel_uvd_mask.setMaximumWidth(height)
            self.layout.panel_uvd_mask.setMaximumHeight(height)
        elif width < height:
            self.layout.panel_uvd_mask.setMaximumWidth(width)
            self.layout.panel_uvd_mask.setMaximumHeight(width)
        # Relocate Panel Cursor due to Size Variation
        self.UVD_Update()
        self.ARD_Update()
        self.panel_hsv.Update_Panel(self.hsv_2, self.hsv_3, self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        self.panel_hsl.Update_Panel(self.hsl_2, self.hsl_3, self.layout.panel_hsl_fg.width(), self.layout.panel_hsl_fg.height(), self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3), self.zoom)
        # Update Display
        self.Pigment_Display()
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
        self.panel_rgb.Update_Panel(
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
        panel = self.layout.panel_selector.currentText()
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

    # Pigment SOF ##############################################################
    def SOF_1_APPLY(self, value):
        self.sof_1 = value
        self.sof_1_slider.Update(value / kritaS, self.layout.sof_1_slider.width())
        self.layout.sof_1_value.setValue(value)
        self.Pigment_Display()
    def SOF_2_APPLY(self, value):
        self.sof_2 = value
        self.sof_2_slider.Update(value, self.layout.sof_2_slider.width())
        self.layout.sof_2_value.setValue(value * kritaO)
        self.Pigment_Display()
    def SOF_3_APPLY(self, value):
        self.sof_3 = value
        self.sof_3_slider.Update(value, self.layout.sof_3_slider.width())
        self.layout.sof_3_value.setValue(value * kritaF)
        self.Pigment_Display()

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
        self.Pigment_Display()
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
        self.Pigment_Display()
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
        self.Pigment_Display()

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
        self.Pigment_Display()
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
        self.Pigment_Display()
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
        self.Pigment_Display()

    # Pigment Channels #########################################################
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

    # Brush Settings ###########################################################
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

    # Palette ##################################################################
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

    # Mixer COLOR ##############################################################
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
            self.Color_RGB(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3, self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l1[1]*hexRGB, self.color_ard_l1[2]*hexRGB, self.color_ard_l1[3]*hexRGB))
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
            self.Color_RGB(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3, self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r1[1]*hexRGB, self.color_ard_r1[2]*hexRGB, self.color_ard_r1[3]*hexRGB))
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
            self.Color_RGB(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3, self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l2[1]*hexRGB, self.color_ard_l2[2]*hexRGB, self.color_ard_l2[3]*hexRGB))
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
            self.Color_RGB(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3, self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r2[1]*hexRGB, self.color_ard_r2[2]*hexRGB, self.color_ard_r2[3]*hexRGB))
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
            self.Color_RGB(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3, self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l3[1]*hexRGB, self.color_ard_l3[2]*hexRGB, self.color_ard_l3[3]*hexRGB))
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
            self.Color_RGB(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
            self.Pigment_Display_Release(0)
            self.UVD_Release()
    def Mixer_ARD_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3, self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Save()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r3[1]*hexRGB, self.color_ard_r3[2]*hexRGB, self.color_ard_r3[3]*hexRGB))
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

    def Mixer_ARD_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_ard_g1 = SIGNAL_MIXER_VALUE / (self.layout.ard_g1.width())
        if self.color_ard_l1[4] <= self.color_ard_r1[4]:
            # Conditions
            cond1 = self.color_ard_r1[4] - self.color_ard_l1[4]
            cond2 = (self.color_ard_l1[4] + 1) - self.color_ard_r1[4]
            if cond1 <= cond2:
                a = self.color_ard_l1[4] + (self.percentage_ard_g1 * cond1)
            else:
                a = self.color_ard_l1[4] - (self.percentage_ard_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l1[4] - self.color_ard_r1[4]
            cond2 = (self.color_ard_r1[4] + 1) - self.color_ard_l1[4]
            if cond1 <= cond2:
                a = self.color_ard_l1[4] - (self.percentage_ard_g1 * cond1)
            else:
                a = self.color_ard_l1[4] + (self.percentage_ard_g1 * cond2)
        # Correct Excess
        if a < 0:
            a = a + 1
        if a > 1:
            a = a - 1
        ard1 = a
        ard2 = (self.color_ard_l1[5] + (self.percentage_ard_g1 * (self.color_ard_r1[5] - self.color_ard_l1[5])))
        ard3 = (self.color_ard_l1[6] + (self.percentage_ard_g1 * (self.color_ard_r1[6] - self.color_ard_l1[6])))
        # Send Values
        self.Color_ARD(ard1, ard2, ard3)
    def Mixer_ARD_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_ard_g2 = SIGNAL_MIXER_VALUE / (self.layout.ard_g2.width())
        if self.color_ard_l2[4] <= self.color_ard_r2[4]:
            # Conditions
            cond1 = self.color_ard_r2[4] - self.color_ard_l2[4]
            cond2 = (self.color_ard_l2[4] + 1) - self.color_ard_r2[4]
            if cond1 <= cond2:
                a = self.color_ard_l2[4] + (self.percentage_ard_g2 * cond1)
            else:
                a = self.color_ard_l2[4] - (self.percentage_ard_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l2[4] - self.color_ard_r2[4]
            cond2 = (self.color_ard_r2[4] + 1) - self.color_ard_l2[4]
            if cond1 <= cond2:
                a = self.color_ard_l2[4] - (self.percentage_ard_g2 * cond1)
            else:
                a = self.color_ard_l2[4] + (self.percentage_ard_g2 * cond2)
        # Correct Excess
        if a < 0:
            a = a + 1
        if a > 1:
            a = a - 1
        ard1 = a
        ard2 = (self.color_ard_l2[5] + (self.percentage_ard_g2 * (self.color_ard_r2[5] - self.color_ard_l2[5])))
        ard3 = (self.color_ard_l2[6] + (self.percentage_ard_g2 * (self.color_ard_r2[6] - self.color_ard_l2[6])))
        # Send Values
        self.Color_ARD(ard1, ard2, ard3)
    def Mixer_ARD_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.percentage_ard_g3 = SIGNAL_MIXER_VALUE / (self.layout.ard_g3.width())
        if self.color_ard_l3[4] <= self.color_ard_r3[4]:
            # Conditions
            cond1 = self.color_ard_r3[4] - self.color_ard_l3[4]
            cond2 = (self.color_ard_l3[4] + 1) - self.color_ard_r3[4]
            if cond1 <= cond2:
                a = self.color_ard_l3[4] + (self.percentage_ard_g3 * cond1)
            else:
                a = self.color_ard_l3[4] - (self.percentage_ard_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l3[4] - self.color_ard_r3[4]
            cond2 = (self.color_ard_r3[4] + 1) - self.color_ard_l3[4]
            if cond1 <= cond2:
                a = self.color_ard_l3[4] - (self.percentage_ard_g3 * cond1)
            else:
                a = self.color_ard_l3[4] + (self.percentage_ard_g3 * cond2)
        # Correct Excess
        if a < 0:
            a = a + 1
        if a > 1:
            a = a - 1
        ard1 = a
        ard2 = (self.color_ard_l3[5] + (self.percentage_ard_g3 * (self.color_ard_r3[5] - self.color_ard_l3[5])))
        ard3 = (self.color_ard_l3[6] + (self.percentage_ard_g3 * (self.color_ard_r3[6] - self.color_ard_l3[6])))
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
        if self.layout.mixer_selector.currentText() == "RGB":
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
        if self.layout.mixer_selector.currentText() == "ARD":
            if (self.color_ard_l1[0] == "True" and self.color_ard_r1[0] == "True"):
                input_ard_l1 = [self.color_ard_l1[4], self.color_ard_l1[5], self.color_ard_l1[6]]
                input_ard_r1 = [self.color_ard_r1[4], self.color_ard_r1[5], self.color_ard_r1[6]]
                mix_ard_g1 = self.ARD_Gradient_Circular(self.layout.ard_g1.width(), input_ard_l1, input_ard_r1)
                self.layout.ard_g1.setStyleSheet(mix_ard_g1)
            if (self.color_ard_l2[0] == "True" and self.color_ard_r2[0] == "True"):
                input_ard_l2 = [self.color_ard_l2[4], self.color_ard_l2[5], self.color_ard_l2[6]]
                input_ard_r2 = [self.color_ard_r2[4], self.color_ard_r2[5], self.color_ard_r2[6]]
                mix_ard_g2 = self.ARD_Gradient_Circular(self.layout.ard_g2.width(), input_ard_l2, input_ard_r2)
                self.layout.ard_g2.setStyleSheet(mix_ard_g2)
            if (self.color_ard_l3[0] == "True" and self.color_ard_r3[0] == "True"):
                input_ard_l3 = [self.color_ard_l3[4], self.color_ard_l3[5], self.color_ard_l3[6]]
                input_ard_r3 = [self.color_ard_r3[4], self.color_ard_r3[5], self.color_ard_r3[6]]
                mix_ard_g3 = self.ARD_Gradient_Circular(self.layout.ard_g3.width(), input_ard_l3, input_ard_r3)
                self.layout.ard_g3.setStyleSheet(mix_ard_g3)
        else:
            self.layout.ard_g1.setStyleSheet(bg_alpha)
            self.layout.ard_g2.setStyleSheet(bg_alpha)
            self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Mixer HSV
        if self.layout.mixer_selector.currentText() == "HSV":
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
        if self.layout.mixer_selector.currentText() == "HSL":
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
        if self.layout.mixer_selector.currentText() == "CMYK":
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

    # Panel Signals#############################################################
    def Signal_UVD(self, SIGNAL_UVD_VALUE):
        self.uvd_1 = round(SIGNAL_UVD_VALUE[0]*kritaUVD, 2) / kritaUVD
        self.uvd_2 = round(SIGNAL_UVD_VALUE[1]*kritaUVD, 2) / kritaUVD
        self.Color_UVD(self.uvd_1, self.uvd_2, self.uvd_3)
    def Signal_ARD(self, SIGNAL_ARD_VALUE):
        self.ard_2 = round(SIGNAL_ARD_VALUE[0]*kritaANG, 2) / kritaANG
        self.ard_3 = round(SIGNAL_ARD_VALUE[1]*kritaRDL, 2) / kritaRDL
        self.Color_ARD(self.ard_1, self.ard_2, self.ard_3)
    def Signal_HSV(self, SIGNAL_HSV_VALUE):
        self.hsv_2 = round(SIGNAL_HSV_VALUE[0]*kritaSVL, 2) / kritaSVL
        self.hsv_3 = round(SIGNAL_HSV_VALUE[1]*kritaSVL, 2) / kritaSVL
        self.Color_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
    def Signal_HSL(self, SIGNAL_HSL_VALUE):
        self.hsl_2 = round(SIGNAL_HSL_VALUE[0]*kritaSVL, 2) / kritaSVL
        self.hsl_3 = round(SIGNAL_HSL_VALUE[1]*kritaSVL, 2) / kritaSVL
        self.Color_HSL(self.hsl_1, self.hsl_2, self.hsl_3)

    # Shader ###################################################################

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
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(212, 212, 212, 255), "
        slider_gradient += "stop:%s rgba(212, 212, 212, 255), \n " % (percentage-0.005)
        slider_gradient += "stop:%s rgba(0, 0, 0, 50), \n " % (percentage+0.001)
        slider_gradient += "stop:1 rgba(0, 0, 0, 50) ) ; \n "
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
    # Colors
    def SVG_Sphere_Diffuse(self, color1, color2, color3, color4, color5, colorB, opacity):
        "RGB Gradient"
        # Set Up Input Colors
        d = 5
        e = 19
        color21 = [(color2[0]-color1[0])/d, (color2[1]-color1[1])/d, (color2[2]-color1[2])/d]
        color32 = [(color3[0]-color2[0])/d, (color3[1]-color2[1])/d, (color3[2]-color2[2])/d]
        color43 = [(color4[0]-color3[0])/d, (color4[1]-color3[1])/d, (color4[2]-color3[2])/d]
        color54 = [(color5[0]-color4[0])/d, (color5[1]-color4[1])/d, (color5[2]-color4[2])/d]
        colorB5 = [(colorB[0]-color5[0])/e, (colorB[1]-color5[1])/e, (colorB[2]-color5[2])/e]
        # Parse Colors
        string_diffuse = str("""\
        <svg
           id="svg8"
           version="1.1"
           viewBox="0 0 70 70"
           height="70mm"
           width="70mm">
          <defs
             id="defs2" />
          <rect
             inkscape:label="45"
             y="-0.55599892"
             x="-8.8817842e-15"
             height="70.670586"
             width="70.114586"
             id="rect1608"
             style="opacity:0;fill:%s;fill-opacity:0;stroke-width:1.06252;stroke-linejoin:bevel;paint-order:markers stroke fill" />
          <path
             inkscape:label="44"
             id="path1589"
             d="M 28.7,60.888121 C 27.25625,60.517786 24.57875,59.464594 22.75,58.547692 17.291198,55.810744 12.652986,50.698683 10.265411,44.787641 5.7697094,33.657405 9.6339614,20.448702 19.431126,13.45759 28.056344,7.3027626 38.92582,6.7371055 48.294855,11.955497 c 3.100471,1.726909 7.645466,6.138599 9.404258,9.128432 8.178086,13.902213 3.123645,30.745212 -11.412579,38.030329 C 41.418853,61.553793 34.152437,62.286721 28.7,60.888121 Z"
             style="opacity:0.05;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="43"
             id="path1587"
             d="M 28.7,60.888121 C 19.227148,58.458253 11.858853,51.168757 9.2334459,41.629752 8.266448,38.116319 8.3462939,31.389327 9.3948631,28.030411 12.71169,17.405514 20.678482,10.36 31.242809,8.7089579 42.99386,6.8724488 55.044486,13.84224 59.543186,25.077211 65.589034,40.176003 56.908883,57.139772 41.211534,60.903073 37.421303,61.81175 32.276796,61.8056 28.7,60.888121 Z"
             style="opacity:0.1;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="42"
             id="path1585"
             d="M 28.7,60.888121 C 15.577038,57.521968 6.9565979,44.95302 8.7555251,31.808282 9.6204651,25.488177 11.949364,20.872126 16.618369,16.223546 19.33647,13.517335 20.343688,12.774708 23.129444,11.422896 27.426458,9.337733 30.390576,8.6437778 35,8.6437778 c 4.416436,0 7.428323,0.6652632 11.337347,2.5041862 10.114881,4.758345 16.403436,16.113982 14.920703,26.94325 C 59.947279,47.66454 54.849606,54.822705 46.286534,59.114258 41.418853,61.553793 34.152437,62.286721 28.7,60.888121 Z"
             style="opacity:0.15;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="41"
             id="path1583"
             d="M 29.75,61.078958 C 20.383973,58.974517 13.203036,52.69727 10.024643,43.835957 7.4893483,36.767587 8.2503676,28.743608 12.119767,21.74554 c 0.816318,-1.476366 2.452834,-3.485176 4.498602,-5.521994 2.718101,-2.706211 3.725319,-3.448838 6.511075,-4.80065 C 27.426458,9.337733 30.390576,8.6437778 35,8.6437778 c 4.416436,0 7.428323,0.6652632 11.337347,2.5041862 5.381526,2.531631 9.815516,6.954889 12.447358,12.417233 1.834381,3.807225 2.606509,7.263777 2.593402,11.609803 -0.03586,11.891834 -8.058232,22.363243 -19.567324,25.540756 -2.947305,0.813715 -9.215614,1.002481 -12.060783,0.363202 z"
             style="opacity:0.2;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="40"
             id="path1581"
             d="M 29.75,61.078958 C 22.045554,59.347855 15.654032,54.664659 11.831882,47.95 9.7819386,44.34871 9.006501,41.427529 8.8307394,36.644283 8.6428625,31.531314 9.0113727,29.074562 10.543486,25.225887 13.386299,18.084731 19.266362,12.536866 26.775,9.911384 29.376172,9.0018537 29.960229,8.9323315 35,8.9323315 c 5.039772,0 5.623828,0.069522 8.225,0.9790525 4.034762,1.410801 7.321625,3.477281 10.35398,6.509635 3.053449,3.053449 5.123219,6.358291 6.48453,10.353981 1.380376,4.051652 1.590411,10.293528 0.493679,14.67131 -2.350985,9.384316 -9.478501,16.710698 -18.746406,19.269446 -2.947305,0.813715 -9.215614,1.002481 -12.060783,0.363202 z"
             style="opacity:0.25;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="39"
             id="path1579"
             d="M 31.316794,61.276981 C 21.272811,59.670551 13.344956,53.028535 9.925055,43.354818 8.8170432,40.220638 8.3979528,33.54391 9.0866772,29.99822 10.875032,20.791407 17.64455,13.103952 26.775,9.911384 29.376172,9.0018537 29.960229,8.9323315 35,8.9323315 c 5.039772,0 5.623828,0.069522 8.225,0.9790525 4.034762,1.410801 7.321625,3.477281 10.35398,6.509635 3.032354,3.032354 5.098835,6.319219 6.509636,10.353981 0.908607,2.598529 0.979317,3.190351 0.982719,8.225 0.0035,5.198742 -0.04209,5.55289 -1.093494,8.491423 -1.573905,4.398884 -3.031126,6.656878 -6.602841,10.231243 -3.559514,3.562152 -6.918254,5.572903 -11.361158,6.801497 -2.944655,0.814285 -8.061306,1.174376 -10.697048,0.752818 z"
             style="opacity:0.3;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="38"
             id="path1577"
             d="M 31.316794,61.276981 C 21.27328,59.670628 13.350875,53.033638 9.9235601,43.354818 8.5966094,39.607477 8.3652534,33.188915 9.4068825,29.020498 11.905407,19.021841 19.636023,11.434293 29.536466,9.2634454 33.251893,8.4487725 39.441622,8.7015243 42.688464,9.8004945 51.451274,12.766473 57.539667,18.952819 60.255349,27.65 c 0.704658,2.256723 0.817964,3.337003 0.807632,7.7 -0.01127,4.758211 -0.07934,5.265725 -1.090502,8.130444 -1.542349,4.369621 -3.01728,6.659366 -6.597479,10.242221 -3.559514,3.562153 -6.918254,5.572903 -11.361158,6.801498 -2.944655,0.814285 -8.061306,1.174376 -10.697048,0.752818 z"
             style="opacity:0.35;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="37"
             id="path1575"
             d="M 28.981464,60.708263 C 21.047663,58.784365 14.689633,53.556058 11.182395,46.071809 9.3832949,42.232627 8.7614569,39.432865 8.7551734,35.143486 8.7368897,22.662486 17.350566,11.93542 29.536466,9.2634454 33.251893,8.4487725 39.441622,8.7015243 42.688464,9.8004946 51.37979,12.742278 57.510548,18.929119 60.202758,27.475 c 1.199968,3.809059 1.364737,9.980628 0.369022,13.821937 -2.461144,9.494709 -9.821591,16.880868 -19.216568,19.283698 -3.13628,0.802127 -9.328837,0.865998 -12.373748,0.127628 z"
             style="opacity:0.4;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="36"
             id="path1573"
             d="M 28.981464,60.708263 C 17.490067,57.921671 9.4290385,48.183821 8.8589942,36.4 8.4778288,28.520638 11.267005,21.5779 17.022415,16.079849 28.803813,4.825269 47.472929,6.813052 56.694088,20.303867 c 3.04841,4.459909 4.380401,8.998306 4.364584,14.871133 -0.01316,4.884768 -0.567245,7.333385 -2.613618,11.55 -3.348572,6.899844 -9.549281,11.927086 -17.089842,13.855635 -3.13628,0.802127 -9.328837,0.865998 -12.373748,0.127628 z"
             style="opacity:0.45;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="35"
             id="path1571"
             d="M 28.981464,60.708263 C 15.840347,57.521625 7.1643936,44.943286 9.0784463,31.853004 9.5912957,28.345605 11.005664,24.218748 12.62685,21.499436 14.339448,18.626792 18.634659,14.364509 21.536612,12.657976 32.112149,6.4388894 45.005044,8.0973249 53.55,16.775914 c 3.082653,3.130862 4.928087,6.127546 6.153997,9.993092 4.738188,14.940483 -3.432457,29.996675 -18.348785,33.811629 -3.13628,0.802127 -9.328837,0.865998 -12.373748,0.127628 z"
             style="opacity:0.5;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="34"
             id="path1569"
             d="M 28.7,60.526042 C 17.693382,57.652108 9.9393392,48.528375 8.8877939,37.214159 8.4461744,32.46251 10.010451,25.888077 12.62685,21.499436 14.339448,18.626792 18.634659,14.364509 21.536612,12.657976 32.112149,6.4388894 45.005044,8.0973249 53.55,16.775914 c 3.082653,3.130862 4.928087,6.127546 6.153997,9.993092 3.133145,9.879455 0.823151,19.788628 -6.265556,26.877335 -3.487635,3.487634 -7.559542,5.787772 -12.226907,6.906732 C 37.394368,61.468207 32.265871,61.457126 28.7,60.526053 Z"
             style="opacity:0.55;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="33"
             id="path1567"
             d="M 29.474502,60.697756 C 16.279814,57.807823 7.1683048,44.916539 9.0799373,31.842805 9.5914154,28.344786 11.007167,24.216226 12.62685,21.499436 14.339448,18.626792 18.634659,14.364509 21.536612,12.657976 32.112149,6.4388894 45.005044,8.0973249 53.55,16.775914 c 3.082653,3.130862 4.928087,6.127546 6.153997,9.993092 3.126316,9.857923 0.836962,19.748293 -6.188689,26.736124 -6.323877,6.289829 -15.554171,9.051388 -24.040806,7.192626 z"
             style="opacity:0.6;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="32"
             id="path1565"
             d="M 29.474502,60.697756 C 24.566826,59.622864 20.135932,57.149914 16.396218,53.398565 13.711371,50.705368 12.165643,48.216437 10.616428,44.091964 7.9052627,36.874029 8.6850249,28.111293 12.62685,21.499436 14.339448,18.626792 18.634659,14.364509 21.536612,12.657976 32.112149,6.4388894 45.005044,8.0973249 53.55,16.775914 c 4.274998,4.341854 6.594556,9.233965 7.391412,15.589011 1.142656,9.112861 -3.489759,19.036488 -11.409772,24.442185 -5.606815,3.826859 -13.424558,5.343328 -20.057138,3.890646 z"
             style="opacity:0.65;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="31"
             id="path1563"
             d="M 29.474502,60.697756 C 20.992177,58.839939 13.971783,52.840375 10.870772,44.799184 9.3666318,40.898819 9.0453321,39.152991 9.0673471,35 c 0.023355,-4.405832 0.7994756,-7.564769 2.9237149,-11.9 1.185049,-2.418494 2.049426,-3.564258 4.620836,-6.125088 1.739706,-1.732549 4.066961,-3.680078 5.171677,-4.327843 C 27.365156,9.3742352 34.90384,8.2366151 40.958834,9.7534388 53.060122,12.784906 60.9,22.936347 60.9,35.574196 c 0,12.165258 -8.881737,22.876654 -20.871102,25.170596 -3.227952,0.61761 -7.608931,0.598084 -10.554396,-0.04704 z"
             style="opacity:0.7;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="30"
             id="path1561"
             d="M 30.275,60.757816 C 21.498758,59.049105 13.981462,52.865473 10.869055,44.794736 9.3667087,40.899019 9.0453377,39.151931 9.0673471,35 c 0.023355,-4.405832 0.7994756,-7.564769 2.9237149,-11.9 1.185049,-2.418494 2.049426,-3.564258 4.620836,-6.125088 1.739706,-1.732549 4.066961,-3.680078 5.171677,-4.327843 C 27.365156,9.3742352 34.90384,8.2366151 40.958834,9.7534388 53.060122,12.784906 60.9,22.936347 60.9,35.574196 c 0,9.70054 -5.559446,18.469374 -14.581476,22.999158 -4.388615,2.203435 -11.18978,3.129472 -16.043524,2.184462 z"
             style="opacity:0.75;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="29"
             id="path1559"
             d="M 30.275,60.757816 C 21.160421,58.983232 13.679026,52.600895 10.538022,43.920307 7.8838697,36.585199 9.0437676,27.158455 13.407993,20.59543 c 1.653965,-2.487271 5.79247,-6.404683 8.396864,-7.948273 6.609009,-3.9170731 15.313214,-4.6084554 22.590305,-1.794366 10.543578,4.077257 17.161704,14.49808 16.402039,25.82646 -0.645487,9.625714 -5.915378,17.59464 -14.478677,21.894103 -4.388615,2.203435 -11.18978,3.129472 -16.043524,2.184462 z"
             style="opacity:0.8;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="28"
             id="path1557"
             d="M 30.275,60.757816 C 21.148146,58.980841 13.679423,52.60199 10.527887,43.892296 9.5955104,41.315547 9.3759095,40.12029 9.2176529,36.760857 8.9269268,30.589416 10.097861,26.114267 13.277998,21.242787 21.67902,8.3737115 38.561435,5.3210496 50.703306,14.475578 c 3.999188,3.015241 7.642132,8.584566 9.202803,14.069227 1.184893,4.164061 1.106608,10.038261 -0.190978,14.330195 -2.068441,6.841632 -6.800269,12.386462 -13.396607,15.698354 -4.388615,2.203435 -11.18978,3.129472 -16.043524,2.184462 z"
             style="opacity:0.85;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="27"
             id="path1555"
             d="M 30.275,60.757816 C 19.745484,58.707747 11.841567,50.819163 9.654441,40.177256 8.2834059,33.506206 9.5322017,26.980771 13.277998,21.242787 21.67902,8.3737115 38.561435,5.3210496 50.703306,14.475578 c 4.002082,3.017423 7.64826,8.593867 9.199215,14.069227 1.028611,3.631329 1.105202,9.719211 0.164871,13.105195 -2.499774,9.001279 -9.432609,16.112208 -18.073108,18.537386 -3.363472,0.944044 -8.512959,1.194693 -11.719284,0.57043 z"
             style="opacity:0.9;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="26"
             id="path1553"
             d="M 31.43311,60.875864 C 24.648705,59.954118 17.883349,55.86182 13.998305,50.329717 7.7782789,41.472718 7.4966199,30.098969 13.277998,21.242787 21.67902,8.3737115 38.561435,5.3210496 50.703306,14.475578 c 4.002082,3.017423 7.64826,8.593867 9.199215,14.069227 1.028611,3.631329 1.105202,9.719211 0.164871,13.105195 -1.412275,5.085363 -4.926012,10.580573 -8.737285,13.66442 -5.329618,4.312392 -13.101427,6.484705 -19.896997,5.561444 z"
             style="opacity:0.95;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="25"
             id="path1551"
             d="M 31.43311,60.875864 C 26.689712,60.231412 21.35721,57.739342 17.561714,54.393262 12.189083,49.656789 8.7071264,41.193761 9.2084265,34.09028 9.8281708,25.30843 13.932773,18.135559 21.005263,13.475082 25.486105,10.522393 29.532889,9.3529096 35.175,9.3801571 46.965229,9.4370962 56.713975,17.012806 59.888804,28.58515 c 0.933478,3.40256 1.01465,9.291269 0.176768,12.823812 -1.172668,4.944002 -4.803823,10.724217 -8.735464,13.905458 -5.329618,4.312392 -13.101428,6.484705 -19.896998,5.561444 z"
             style="opacity:1;display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="24"
             id="path1549"
             d="M 31.43311,60.875864 C 26.689712,60.231412 21.35721,57.739342 17.561714,54.393262 12.140248,49.613736 8.6996948,41.184895 9.2218353,33.961805 9.5709383,29.132451 11.809619,22.490522 13.649471,20.825478 14.034762,20.476795 14.35,20.073203 14.35,19.928608 c 0,-0.477199 4.918022,-5.030387 6.76391,-6.262142 0.9961,-0.664694 1.863917,-1.33505 1.928483,-1.489681 0.06457,-0.15463 0.261442,-0.19212 0.4375,-0.08331 0.176059,0.108811 0.320107,0.03104 0.320107,-0.172819 0,-0.203861 0.118125,-0.344883 0.2625,-0.313384 0.144375,0.0315 0.985431,-0.267103 1.869012,-0.663562 5.621938,-2.5225396 14.406317,-2.0338874 20.773583,1.15558 2.438069,1.221268 7.778351,5.28393 7.418558,5.643724 -0.09968,0.09968 0.441476,0.96903 1.202569,1.931887 1.643992,2.079805 3.611517,6.060246 4.201582,8.500099 0.232774,0.9625 0.573702,1.942565 0.757617,2.177922 0.561344,0.718354 0.409262,8.416371 -0.218421,11.05604 -1.17656,4.947911 -4.806473,10.725207 -8.736892,13.905458 -5.329618,4.312392 -13.101428,6.484705 -19.896998,5.561444 z"
             style="display:inline;fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="23"
             id="path1547"
             d="M 31.43311,60.875864 C 24.648705,59.954118 17.883349,55.86182 13.998305,50.329717 9.3258518,43.676384 7.9605158,35.364249 10.3555,28.152398 c 1.663672,-5.009704 3.11356,-7.367204 6.772236,-11.011572 5.056084,-5.036309 9.596668,-7.12206 16.47943,-7.5699448 11.867756,-0.7722756 22.84657,7.2110648 26.065989,18.9541188 0.872834,3.183715 1.076824,9.95716 0.388017,12.883962 C 58.900446,46.34099 55.265515,52.130134 51.330108,55.31442 46.00049,59.626812 38.22868,61.799125 31.43311,60.875864 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="22"
             id="path1545"
             d="M 28.739188,60.206566 C 22.147151,58.423358 16.907213,54.679786 13.37661,49.231063 8.0821622,41.060229 7.7964516,32.191371 12.529159,22.925 14.409713,19.242982 19.503524,14.293916 23.45,12.314483 27.181967,10.442642 29.394449,9.8450173 33.607166,9.5708812 45.474705,8.7986196 56.474981,16.798683 59.669522,28.525 c 0.794206,2.915315 1.084979,9.396999 0.54501,12.148874 -1.683993,8.582238 -8.689446,16.243504 -17.456204,19.090369 -3.808904,1.236879 -10.322186,1.442381 -14.01914,0.442323 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="21"
             id="path1541"
             d="M 28.739188,60.206566 C 23.956913,58.912917 20.213548,56.800474 16.826404,53.48399 13.91582,50.634125 10.699961,45.304773 10.319084,42.7 10.248714,42.21875 10.006597,40.88 9.7810461,39.725 9.1677306,36.584334 9.5370807,30.449585 10.508036,27.65 c 1.727162,-4.979974 3.270053,-7.308525 6.442255,-9.722731 1.16859,-0.889357 3.124868,-2.52416 4.347284,-3.632898 3.531987,-3.203528 6.509454,-4.3460547 12.309591,-4.7234898 4.475935,-0.2912644 8.243541,0.4679308 12.417834,2.5022648 4.261421,2.076799 8.284822,5.483698 7.455455,6.313065 -0.09873,0.09873 -2.131595,-0.139 -4.517482,-0.528284 -2.385883,-0.389284 -5.016354,-0.707821 -5.845486,-0.707858 -1.644262,-7.5e-5 -4.625401,0.649965 -4.604345,1.003981 0.02828,0.475386 2.350166,2.856836 4.011858,4.114764 C 45.876995,24.806331 55.275076,28.7 58.047839,28.7 c 1.831631,0 2.327161,1.41601 2.327161,6.65 0,4.018763 -0.09673,4.674239 -1.18789,8.05 -1.439441,4.453246 -3.324009,7.453838 -6.655127,10.596243 -2.827591,2.667406 -6.011061,4.546157 -9.773655,5.768 -3.808904,1.236879 -10.322186,1.442381 -14.01914,0.442323 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="20"
             id="path1539"
             d="M 28.739188,60.206566 C 23.956913,58.912917 20.213548,56.800474 16.826404,53.48399 13.91582,50.634125 10.699961,45.304773 10.319084,42.7 10.248714,42.21875 10.006597,40.88 9.7810461,39.725 9.1679179,36.585297 9.5371,30.449808 10.507618,27.65 c 1.066391,-3.076387 1.883465,-4.637699 3.229029,-6.170212 1.831737,-2.086233 3.31145,-2.563222 7.979164,-2.572101 5.117539,-0.0097 9.229257,0.990817 15.384189,3.743614 9.128052,4.082525 10.598549,4.670902 14.779177,5.91346 2.362703,0.702238 5.000852,1.4156 5.862552,1.585248 2.491612,0.490539 2.633964,0.787136 2.628451,5.476452 -0.0043,3.690806 -0.12251,4.464138 -1.187886,7.773539 -1.433502,4.452917 -3.313593,7.448556 -6.650311,10.596243 -2.827591,2.667406 -6.011061,4.546157 -9.773655,5.768 -3.808904,1.236879 -10.322186,1.442381 -14.01914,0.442323 z M 42.875,15.351938 C 30.937971,13.472381 27.770237,12.87996 27.01657,12.386139 26.244258,11.8801 26.228181,11.804229 26.767086,11.208745 28.151614,9.6788583 35.212051,9.0051927 39.912299,9.9545051 44.145363,10.809461 51.45,14.480037 51.45,15.752195 c 0,0.52442 -3.841065,0.34513 -8.575,-0.400257 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="19"
             id="path1537"
             d="M 28.739188,60.206566 C 23.956913,58.912917 20.213548,56.800474 16.826404,53.48399 13.91582,50.634125 10.699961,45.304773 10.319084,42.7 10.248714,42.21875 10.006597,40.88 9.7810461,39.725 8.799749,34.699976 9.9224671,27.447484 12.217825,23.983993 13.818218,21.569141 15.033539,21 18.589725,21 c 7.040278,0 12.07801,1.14324 22.710275,5.153764 2.79125,1.052869 8.066446,2.733081 11.722655,3.733804 7.932379,2.171132 7.650597,1.909805 7.399588,6.862432 -0.544471,10.742917 -7.406382,19.683272 -17.663916,23.014243 -3.808903,1.236879 -10.322185,1.442382 -14.019139,0.442323 z M 46.870834,14.557957 C 46.790625,14.479834 43.33875,13.850384 39.2,13.159179 30.607904,11.724229 28.951051,11.325735 29.141827,10.74006 29.537339,9.5258513 35.785421,9.1057876 40.177256,9.9981392 43.103903,10.592787 48.089583,12.800629 49.148823,13.971077 49.806739,14.698064 49.804783,14.7 48.412577,14.7 c -0.767749,0 -1.461536,-0.06392 -1.541743,-0.142043 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="18"
             id="path1535"
             d="M 28.739188,60.206566 C 23.956913,58.912917 20.213548,56.800474 16.826404,53.48399 13.914073,50.632414 10.695726,45.297612 10.320703,42.7 10.251224,42.21875 10.026892,40.976628 9.8221886,39.939728 8.9506105,35.524867 9.5527715,29.332456 11.134122,26.448268 c 1.697666,-3.096333 1.942573,-3.177742 9.45651,-3.143423 7.443906,0.034 5.397385,-0.393272 24.909368,5.200562 2.21375,0.634654 6.058458,1.686193 8.543798,2.336754 3.458742,0.905359 4.763864,1.411687 5.563463,2.158369 1.042486,0.973495 1.044239,0.981891 0.840602,4.025001 -0.270221,4.038198 -1.959468,9.298009 -3.971558,12.36627 -3.116603,4.752545 -8.163747,8.568794 -13.717977,10.372442 -3.808903,1.236879 -10.322186,1.442382 -14.01914,0.442323 z M 40.075,12.595632 c -7.316401,-1.37025 -8.925,-1.749516 -8.925,-2.104281 0,-0.450273 2.379141,-1.0375553 4.2,-1.0367552 3.904397,0.00172 9.669289,1.6324372 11.733284,3.3190062 l 1.041716,0.851224 -1.4,-0.02297 c -0.77,-0.01263 -3.7625,-0.465435 -6.65,-1.00622 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="17"
             id="path1531"
             d="M 28.875,60.234919 C 19.751996,57.735839 13.523641,51.751476 10.443027,42.525 9.7359118,40.407181 9.625,39.386907 9.625,35 c 0,-4.942364 0.027444,-5.129475 1.05,-7.159362 1.615645,-3.207229 2.256153,-3.52656 6.941319,-3.46066 7.073047,0.09949 11.463983,0.865678 22.5386,3.932848 3.421044,0.947476 8.031331,2.119137 10.245081,2.603691 6.29664,1.378233 9.189264,2.388488 9.72803,3.397535 C 61.075287,36.088164 59.879547,42.704235 57.916593,46.55 54.558875,53.128348 48.957611,57.869938 42,60.023743 38.962844,60.963927 31.948288,61.076788 28.875,60.234919 Z M 39.725,11.139868 C 37.844898,10.783355 36.781342,10.15 38.062773,10.15 c 1.228384,0 4.265051,0.730963 4.479734,1.078327 0.235966,0.381801 -0.451353,0.360221 -2.817507,-0.08846 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="16"
             id="path1529"
             d="M 28.875,60.234919 C 19.751652,57.735744 13.518851,51.74673 10.444187,42.525 c -0.6879248,-2.063268 -0.8170502,-3.168217 -0.8180271,-7 -0.00105,-4.051804 0.085191,-4.71159 0.7874831,-6.025797 1.117734,-2.09163 1.776171,-2.342075 6.036357,-2.296011 6.626088,0.07165 13.821328,1.022068 25.55,3.374911 3.36875,0.675792 7.814845,1.554412 9.880213,1.952491 5.402736,1.041321 7.430006,1.868022 8.013582,3.267865 0.635173,1.523598 0.513489,3.504308 -0.405037,6.593089 C 56.957677,50.902943 50.530217,57.383119 42,60.023743 38.962843,60.963927 31.948288,61.076788 28.875,60.234919 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="15"
             id="path1527"
             d="M 28.875,60.234919 C 19.818009,57.753923 13.516698,51.737991 10.508269,42.7 9.5522424,39.827882 9.1713755,34.296055 9.7956138,32.349171 10.385467,30.509526 11.407023,29.458542 12.872537,29.18361 15.170178,28.75257 26.962552,29.785866 35.35,31.153178 c 4.52375,0.737457 9.24875,1.443262 10.5,1.568457 9.372247,0.937747 13.688269,2.535766 14.1988,5.257145 0.287682,1.533473 -0.637329,5.401403 -1.940659,8.11488 C 54.843344,52.890814 49.157122,57.808177 42,60.023744 38.962843,60.963928 31.948288,61.076789 28.875,60.234919 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="14"
             id="path1525"
             d="M 28.875,60.234919 C 23.702216,58.81793 19.519739,56.322584 16.145625,52.640336 11.251766,47.299549 8.2357492,37.930452 9.9583498,33.419888 c 1.0134592,-2.653704 1.3855272,-2.76355 8.4294232,-2.488618 6.281172,0.245161 13.55137,0.882098 20.287227,1.777349 2.1175,0.281433 6.13375,0.765182 8.925,1.074997 5.958498,0.661364 7.635498,1.026572 9.901006,2.156186 2.007821,1.001126 2.482557,1.987892 2.242027,4.660198 -0.251514,2.79433 -1.447845,5.641661 -3.878718,9.231565 C 52.501204,54.798198 47.860956,58.20942 42,60.023743 38.962843,60.963927 31.948288,61.076788 28.875,60.234919 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="13"
             id="path1521"
             d="M 30.275,60.399874 C 20.879916,58.540226 13.473992,51.856861 10.472587,42.529483 9.4732333,39.423821 9.3698318,35.533652 10.250895,34.188978 c 1.380882,-2.107492 1.66536,-2.156971 9.644028,-1.677385 3.976542,0.239025 10.773827,0.806909 15.105077,1.261965 4.33125,0.455056 9.135,0.928529 10.675,1.052163 8.33728,0.669329 11.775337,1.512955 13.117034,3.218645 0.506089,0.643391 0.704707,1.410539 0.696538,2.690335 -0.02495,3.911446 -2.28221,8.103406 -6.813485,12.653399 -2.566322,2.576928 -3.701407,3.432412 -6.125087,4.616339 -1.63625,0.799278 -3.92,1.701378 -5.075,2.004667 -3.013189,0.791228 -8.253216,0.97405 -11.2,0.390768 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="12"
             id="path1519"
             d="M 30.275,60.399874 C 22.08157,58.778079 15.688071,53.774875 11.90562,46.025 9.5285998,41.154715 9.3032744,36.850261 11.354978,35.505935 12.389984,34.827772 14.11532,34.76748 22.75,35.107734 37.771867,35.699682 51.002798,36.68307 54.504954,37.46792 57.661065,38.175218 59.15,39.604807 59.15,41.927826 c 0,3.19788 -2.938642,8.26286 -7.023559,12.105657 -2.976907,2.800462 -6.863696,4.981011 -10.651441,5.975623 -3.013189,0.791228 -8.253216,0.97405 -11.2,0.390768 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="11"
             id="path1515"
             d="M 31.85,60.573324 C 26.687133,59.856027 21.590085,57.465527 17.860027,54.012063 11.995278,48.582205 8.8691778,40.676622 11.532789,38.011137 c 0.670951,-0.671422 1.127116,-0.735882 5.188916,-0.733243 2.449312,0.0017 10.517045,0.199115 17.928295,0.438942 17.026765,0.550984 20.908051,1.009397 22.563614,2.66496 C 60.765078,43.93326 55.243895,53.26216 46.987836,57.659843 42.427504,60.088955 36.531428,61.223732 31.85,60.573324 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="10"
             id="path1513"
             d="M 31.85,60.573324 C 22.694088,59.301259 13.833721,52.397723 11.501277,44.71866 c -1.304245,-4.293947 -0.255037,-5.914846 3.875222,-5.986747 4.999603,-0.08704 35.076169,0.846472 36.854816,1.143888 2.415669,0.403938 4.310222,1.254631 5.005798,2.247703 2.401263,3.428282 -3.070385,11.76462 -10.18438,15.516428 C 42.399189,60.094139 36.539258,61.224821 31.85,60.573324 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="9"
             id="path1511"
             d="m 31.85,60.573324 c -5.763839,-0.80079 -10.531779,-3.184149 -14.724747,-7.360479 -3.359956,-3.346623 -5.093108,-6.318617 -5.45202,-9.349074 -0.194153,-1.639316 -0.126735,-1.892086 0.734296,-2.753118 l 0.948078,-0.94808 12.309696,0.239778 c 15.467033,0.30128 25.060432,0.745819 27.518391,1.275148 1.275064,0.27459 2.247899,0.75025 2.930486,1.432834 0.909066,0.909065 1.004119,1.20575 0.861574,2.689225 C 56.730537,48.351569 55.391581,50.66034 52.480939,53.55 47.179188,58.813531 39.065176,61.575755 31.85,60.573324 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="8"
             id="path1507"
             d="M 29.05,59.833658 C 21.418024,57.863011 14.15122,51.915412 12.598173,46.368476 c -0.598182,-2.136498 -0.193078,-3.314192 1.403638,-4.080573 1.120922,-0.538013 2.65793,-0.561691 18.383747,-0.283213 22.723027,0.402388 23.841375,0.62448 23.744485,4.71542 -0.09938,4.195993 -4.016002,8.413566 -10.738162,11.563279 C 40.570575,60.542443 34.152844,61.151258 29.05,59.833658 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="7"
             id="path1505"
             d="m 29.05,59.833658 c -8.747246,-2.25862 -16.79883,-9.757139 -15.601063,-14.52942 0.479168,-1.909163 1.02394,-1.953616 19.194605,-1.566341 20.287822,0.432397 21.92997,0.667156 22.438079,3.207701 0.687918,3.4396 -3.101186,8.095654 -8.881621,10.913731 -5.512196,2.687307 -11.651558,3.394076 -17.15,1.974329 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="6"
             id="path1503"
             d="m 29.05,59.833658 c -1.44375,-0.372792 -3.929463,-1.319269 -5.523808,-2.103286 -6.815033,-3.351285 -10.950977,-9.882635 -7.415777,-11.710759 0.867742,-0.448728 3.222248,-0.478576 17.558354,-0.22261 17.653065,0.315192 18.602383,0.417427 19.503059,2.100357 1.626233,3.038647 -1.585475,7.445368 -7.449553,10.221379 C 40.60539,60.541033 34.30098,61.189509 29.05,59.833658 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="5"
             id="path1501"
             d="m 29.05,59.826042 c -6.999369,-1.827602 -12.6,-6.28908 -12.6,-10.037191 0,-0.60514 0.305268,-1.305521 0.7397,-1.697105 0.699132,-0.630178 1.337401,-0.66143 11.6375,-0.5698 12.550755,0.111647 20.469306,0.547379 21.841082,1.201841 0.793992,0.378805 0.975425,0.717206 1.066698,1.989564 0.148169,2.065448 -0.42617,3.293353 -2.320255,4.960596 C 44.668106,59.852089 35.954072,61.628763 29.05,59.826042 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="4"
             id="path1499"
             d="m 29.205305,59.863755 c -3.369715,-0.88374 -4.732883,-1.49288 -7.176088,-3.20669 -3.404455,-2.388091 -4.389967,-4.789861 -2.557016,-6.231662 0.874487,-0.687872 1.340777,-0.724322 9.0125,-0.704504 10.827369,0.02796 17.893708,0.440205 19.555025,1.140807 2.560848,1.079943 2.398742,3.057271 -0.462564,5.642291 -3.928823,3.549455 -12.012052,5.02768 -18.371857,3.359758 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="3"
             id="path1497"
             d="m 30.613408,60.039577 c -3.164759,-0.575007 -6.142229,-1.99361 -8.078666,-3.849044 -1.775431,-1.701161 -1.888236,-2.31167 -0.612541,-3.31513 0.857381,-0.674415 1.367847,-0.724535 7.2625,-0.713052 8.291892,0.01617 15.199474,0.504511 16.841727,1.19069 1.169924,0.488824 1.276534,0.640062 1.062761,1.507642 -0.571938,2.321151 -4.285515,4.61951 -8.589189,5.315902 -2.859661,0.462731 -4.768186,0.429576 -7.886592,-0.137008 z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="2"
             id="path1495"
             d="m 30.1,59.64175 c -2.314586,-0.615839 -4.738975,-2.054332 -5.741308,-3.406561 -0.732387,-0.98805 -0.732447,-0.990752 -0.03369,-1.518583 0.595831,-0.450086 1.950026,-0.501357 9.1,-0.344544 8.82343,0.193519 10.260618,0.352912 10.575257,1.172847 0.293251,0.764193 -0.595724,2.145199 -1.899649,2.951067 C 39.4072,60.160593 33.992908,60.677529 30.1,59.64175 Z"
             style="fill:%s;stroke-width:0.35" />
          <path
             inkscape:label="1"
             id="path1493"
             d="m 30.684495,58.998373 c -0.929777,-0.249911 -1.947902,-0.711781 -2.2625,-1.026379 -0.529327,-0.529326 -0.52627,-0.617683 0.04098,-1.184494 0.51598,-0.515578 1.261687,-0.610078 4.7125,-0.597202 4.639853,0.01732 7.181875,0.558394 7.007648,1.491595 -0.275047,1.473262 -5.975787,2.263366 -9.49863,1.31648 z"
             style="fill:%s;stroke-width:0.35" />
        </svg>
        """ % (
        # Background Color
        self.HEX_6(colorB[0], colorB[1], colorB[2]),
        # 31-54
        self.HEX_6(color5[0]+(colorB5[0]*19), color5[1]+(colorB5[1]*19), color5[2]+(colorB5[2]*19)),
        self.HEX_6(color5[0]+(colorB5[0]*18), color5[1]+(colorB5[1]*18), color5[2]+(colorB5[2]*18)),
        self.HEX_6(color5[0]+(colorB5[0]*17), color5[1]+(colorB5[1]*17), color5[2]+(colorB5[2]*17)),
        self.HEX_6(color5[0]+(colorB5[0]*16), color5[1]+(colorB5[1]*16), color5[2]+(colorB5[2]*16)),
        self.HEX_6(color5[0]+(colorB5[0]*15), color5[1]+(colorB5[1]*15), color5[2]+(colorB5[2]*15)),
        self.HEX_6(color5[0]+(colorB5[0]*14), color5[1]+(colorB5[1]*14), color5[2]+(colorB5[2]*14)),
        self.HEX_6(color5[0]+(colorB5[0]*13), color5[1]+(colorB5[1]*13), color5[2]+(colorB5[2]*13)),
        self.HEX_6(color5[0]+(colorB5[0]*12), color5[1]+(colorB5[1]*12), color5[2]+(colorB5[2]*12)),
        self.HEX_6(color5[0]+(colorB5[0]*11), color5[1]+(colorB5[1]*11), color5[2]+(colorB5[2]*11)),
        self.HEX_6(color5[0]+(colorB5[0]*10), color5[1]+(colorB5[1]*10), color5[2]+(colorB5[2]*10)),
        self.HEX_6(color5[0]+(colorB5[0]*9), color5[1]+(colorB5[1]*9), color5[2]+(colorB5[2]*9)),
        self.HEX_6(color5[0]+(colorB5[0]*8), color5[1]+(colorB5[1]*8), color5[2]+(colorB5[2]*8)),
        self.HEX_6(color5[0]+(colorB5[0]*7), color5[1]+(colorB5[1]*7), color5[2]+(colorB5[2]*7)),
        self.HEX_6(color5[0]+(colorB5[0]*6), color5[1]+(colorB5[1]*6), color5[2]+(colorB5[2]*6)),
        self.HEX_6(color5[0]+(colorB5[0]*5), color5[1]+(colorB5[1]*5), color5[2]+(colorB5[2]*5)),
        self.HEX_6(color5[0]+(colorB5[0]*4), color5[1]+(colorB5[1]*4), color5[2]+(colorB5[2]*4)),
        self.HEX_6(color5[0]+(colorB5[0]*3), color5[1]+(colorB5[1]*3), color5[2]+(colorB5[2]*3)),
        self.HEX_6(color5[0]+(colorB5[0]*2), color5[1]+(colorB5[1]*2), color5[2]+(colorB5[2]*2)),
        self.HEX_6(color5[0]+(colorB5[0]*1), color5[1]+(colorB5[1]*1), color5[2]+(colorB5[2]*1)),
        # Color 5
        self.HEX_6(color5[0], color5[1], color5[2]),
        # 23-29
        self.HEX_6(color4[0]+(color54[0]*5), color4[1]+(color54[1]*5), color4[2]+(color54[2]*5)),
        self.HEX_6(color4[0]+(color54[0]*4), color4[1]+(color54[1]*4), color4[2]+(color54[2]*4)),
        self.HEX_6(color4[0]+(color54[0]*3), color4[1]+(color54[1]*3), color4[2]+(color54[2]*3)),
        self.HEX_6(color4[0]+(color54[0]*2), color4[1]+(color54[1]*2), color4[2]+(color54[2]*2)),
        self.HEX_6(color4[0]+(color54[0]*1), color4[1]+(color54[1]*1), color4[2]+(color54[2]*1)),
        # Color 4
        self.HEX_6(color4[0], color4[1], color4[2]),
        # 16-21
        self.HEX_6(color3[0]+(color43[0]*5), color3[1]+(color43[1]*5), color3[2]+(color43[2]*5)),
        self.HEX_6(color3[0]+(color43[0]*4), color3[1]+(color43[1]*4), color3[2]+(color43[2]*4)),
        self.HEX_6(color3[0]+(color43[0]*3), color3[1]+(color43[1]*3), color3[2]+(color43[2]*3)),
        self.HEX_6(color3[0]+(color43[0]*2), color3[1]+(color43[1]*2), color3[2]+(color43[2]*2)),
        self.HEX_6(color3[0]+(color43[0]*1), color3[1]+(color43[1]*1), color3[2]+(color43[2]*1)),
        # Color 3
        self.HEX_6(color3[0], color3[1], color3[2]),
        # 9-14
        self.HEX_6(color2[0]+(color32[0]*5), color2[1]+(color32[1]*5), color2[2]+(color32[2]*5)),
        self.HEX_6(color2[0]+(color32[0]*4), color2[1]+(color32[1]*4), color2[2]+(color32[2]*4)),
        self.HEX_6(color2[0]+(color32[0]*3), color2[1]+(color32[1]*3), color2[2]+(color32[2]*3)),
        self.HEX_6(color2[0]+(color32[0]*2), color2[1]+(color32[1]*2), color2[2]+(color32[2]*2)),
        self.HEX_6(color2[0]+(color32[0]*1), color2[1]+(color32[1]*1), color2[2]+(color32[2]*1)),
        # Color 2
        self.HEX_6(color2[0], color2[1], color2[2]),
        # 1-7
        self.HEX_6(color1[0]+(color21[0]*5), color1[1]+(color21[1]*5), color1[2]+(color21[2]*5)),
        self.HEX_6(color1[0]+(color21[0]*4), color1[1]+(color21[1]*4), color1[2]+(color21[2]*4)),
        self.HEX_6(color1[0]+(color21[0]*3), color1[1]+(color21[1]*3), color1[2]+(color21[2]*3)),
        self.HEX_6(color1[0]+(color21[0]*2), color1[1]+(color21[1]*2), color1[2]+(color21[2]*2)),
        self.HEX_6(color1[0]+(color21[0]*1), color1[1]+(color21[1]*1), color1[2]+(color21[2]*1)),
        # Color 1
        self.HEX_6(color1[0], color1[1], color1[2])
        ))
        array_diffuse = bytearray(string_diffuse, encoding='utf-8')
        return array_diffuse
        pass

    # Widget Events ############################################################
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
    def resizeEvent(self, event):
        # Maintian Ratio
        self.Ratio()
    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:
            self.timer.stop()
        # Save Settings
        self.Settings_Save()

    # Settings #################################################################
    def Settings_Load(self):
        # Variables
        self.zoom = 0

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
        if (mixer_ard_1_split[0] == "True" and mixer_ard_1_split[7] == "True"):
            # Gradient
            self.color_ard_l1 = ["True", float(mixer_ard_1_split[1]), float(mixer_ard_1_split[2]), float(mixer_ard_1_split[3]), float(mixer_ard_1_split[4]), float(mixer_ard_1_split[5]), float(mixer_ard_1_split[6])]
            self.color_ard_r1 = ["True", float(mixer_ard_1_split[8]), float(mixer_ard_1_split[9]), float(mixer_ard_1_split[10]), float(mixer_ard_1_split[11]), float(mixer_ard_1_split[12]), float(mixer_ard_1_split[13])]
            color_ard_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l1[1]*hexRGB, self.color_ard_l1[2]*hexRGB, self.color_ard_l1[3]*hexRGB))
            color_ard_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r1[1]*hexRGB, self.color_ard_r1[2]*hexRGB, self.color_ard_r1[3]*hexRGB))
            self.layout.ard_l1.setStyleSheet(color_ard_left_1)
            self.layout.ard_r1.setStyleSheet(color_ard_right_1)
        elif (mixer_ard_1_split[0] == "True" and mixer_ard_1_split[7] != "True"):
            # Color Left
            self.color_ard_l1 = ["True", float(mixer_ard_1_split[1]), float(mixer_ard_1_split[2]), float(mixer_ard_1_split[3]), float(mixer_ard_1_split[4]), float(mixer_ard_1_split[5]), float(mixer_ard_1_split[6])]
            self.color_ard_r1 = ["False", 0, 0, 0, 0, 0, 0]
            color_ard_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l1[1]*hexRGB, self.color_ard_l1[2]*hexRGB, self.color_ard_l1[3]*hexRGB))
            self.layout.ard_l1.setStyleSheet(color_ard_left_1)
            self.layout.ard_r1.setStyleSheet(bg_alpha)
        elif (mixer_ard_1_split[0] != "True" and mixer_ard_1_split[7] == "True"):
            # Color Right
            self.color_ard_l1 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_ard_r1 = ["True", float(mixer_ard_1_split[8]), float(mixer_ard_1_split[9]), float(mixer_ard_1_split[10]), float(mixer_ard_1_split[11]), float(mixer_ard_1_split[12]), float(mixer_ard_1_split[13])]
            color_ard_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r1[1]*hexRGB, self.color_ard_r1[2]*hexRGB, self.color_ard_r1[3]*hexRGB))
            self.layout.ard_l1.setStyleSheet(bg_alpha)
            self.layout.ard_r1.setStyleSheet(color_ard_right_1)
        else:
            self.color_ard_l1 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_ard_r1 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.ard_l1.setStyleSheet(bg_alpha)
            self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.percentage_ard_g1 = 0
        self.mixer_ard_g1.Update(self.percentage_ard_g1, self.layout.ard_g1.width())
        # Mixer ARD 2
        mixer_ard_2_string = Krita.instance().readSetting("Pigment.O", "Mixer_ARD_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_ard_2_split = mixer_ard_2_string.split(",")
        if (mixer_ard_2_split[0] == "True" and mixer_ard_2_split[7] == "True"):
            # Gradient
            self.color_ard_l2 = ["True", float(mixer_ard_2_split[1]), float(mixer_ard_2_split[2]), float(mixer_ard_2_split[3]), float(mixer_ard_2_split[4]), float(mixer_ard_2_split[5]), float(mixer_ard_2_split[6])]
            self.color_ard_r2 = ["True", float(mixer_ard_2_split[8]), float(mixer_ard_2_split[9]), float(mixer_ard_2_split[10]), float(mixer_ard_2_split[11]), float(mixer_ard_2_split[12]), float(mixer_ard_2_split[13])]
            color_ard_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l2[1]*hexRGB, self.color_ard_l2[2]*hexRGB, self.color_ard_l2[3]*hexRGB))
            color_ard_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r2[1]*hexRGB, self.color_ard_r2[2]*hexRGB, self.color_ard_r2[3]*hexRGB))
            self.layout.ard_l2.setStyleSheet(color_ard_left_2)
            self.layout.ard_r2.setStyleSheet(color_ard_right_2)
        elif (mixer_ard_2_split[0] == "True" and mixer_ard_2_split[7] != "True"):
            # Color Left
            self.color_ard_l2 = ["True", float(mixer_ard_2_split[1]), float(mixer_ard_2_split[2]), float(mixer_ard_2_split[3]), float(mixer_ard_2_split[4]), float(mixer_ard_2_split[5]), float(mixer_ard_2_split[6])]
            self.color_ard_r2 = ["False", 0, 0, 0, 0, 0, 0]
            color_ard_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l2[1]*hexRGB, self.color_ard_l2[2]*hexRGB, self.color_ard_l2[3]*hexRGB))
            self.layout.ard_l2.setStyleSheet(color_ard_left_2)
            self.layout.ard_r2.setStyleSheet(bg_alpha)
        elif (mixer_ard_2_split[0] != "True" and mixer_ard_2_split[7] == "True"):
            # Color Right
            self.color_ard_l2 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_ard_r2 = ["True", float(mixer_ard_2_split[8]), float(mixer_ard_2_split[9]), float(mixer_ard_2_split[10]), float(mixer_ard_2_split[11]), float(mixer_ard_2_split[12]), float(mixer_ard_2_split[13])]
            color_ard_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r2[1]*hexRGB, self.color_ard_r2[2]*hexRGB, self.color_ard_r2[3]*hexRGB))
            self.layout.ard_l2.setStyleSheet(bg_alpha)
            self.layout.ard_r2.setStyleSheet(color_ard_right_2)
        else:
            self.color_ard_l2 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_ard_r2 = ["False", 0, 0, 0, 0, 0, 0]
            self.layout.ard_l2.setStyleSheet(bg_alpha)
            self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.percentage_ard_g2 = 0
        self.mixer_ard_g2.Update(self.percentage_ard_g2, self.layout.ard_g2.width())
        # Mixer ARD 3
        mixer_ard_3_string = Krita.instance().readSetting("Pigment.O", "Mixer_ARD_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_ard_3_split = mixer_ard_3_string.split(",")
        if (mixer_ard_3_split[0] == "True" and mixer_ard_3_split[7] == "True"):
            # Gradient
            self.color_ard_l3 = ["True", float(mixer_ard_3_split[1]), float(mixer_ard_3_split[2]), float(mixer_ard_3_split[3]), float(mixer_ard_3_split[4]), float(mixer_ard_3_split[5]), float(mixer_ard_3_split[6])]
            self.color_ard_r3 = ["True", float(mixer_ard_3_split[8]), float(mixer_ard_3_split[9]), float(mixer_ard_3_split[10]), float(mixer_ard_3_split[11]), float(mixer_ard_3_split[12]), float(mixer_ard_3_split[13])]
            color_ard_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l3[1]*hexRGB, self.color_ard_l3[2]*hexRGB, self.color_ard_l3[3]*hexRGB))
            color_ard_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r3[1]*hexRGB, self.color_ard_r3[2]*hexRGB, self.color_ard_r3[3]*hexRGB))
            self.layout.ard_l3.setStyleSheet(color_ard_left_3)
            self.layout.ard_r3.setStyleSheet(color_ard_right_3)
        elif (mixer_ard_3_split[0] == "True" and mixer_ard_3_split[7] != "True"):
            # Color Left
            self.color_ard_l3 = ["True", float(mixer_ard_3_split[1]), float(mixer_ard_3_split[2]), float(mixer_ard_3_split[3]), float(mixer_ard_3_split[4]), float(mixer_ard_3_split[5]), float(mixer_ard_3_split[6])]
            self.color_ard_r3 = ["False", 0, 0, 0, 0, 0, 0]
            color_ard_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_l3[1]*hexRGB, self.color_ard_l3[2]*hexRGB, self.color_ard_l3[3]*hexRGB))
            self.layout.ard_l3.setStyleSheet(color_ard_left_3)
            self.layout.ard_r3.setStyleSheet(bg_alpha)
        elif (mixer_ard_3_split[0] != "True" and mixer_ard_3_split[4] == "True"):
            # Color Right
            self.color_ard_l3 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_ard_r3 = ["True", float(mixer_ard_3_split[8]), float(mixer_ard_3_split[9]), float(mixer_ard_3_split[10]), float(mixer_ard_3_split[11]), float(mixer_ard_3_split[12]), float(mixer_ard_3_split[13])]
            color_ard_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_ard_r3[1]*hexRGB, self.color_ard_r3[2]*hexRGB, self.color_ard_r3[3]*hexRGB))
            self.layout.ard_l3.setStyleSheet(bg_alpha)
            self.layout.ard_r3.setStyleSheet(color_ard_right_3)
        else:
            self.color_ard_l3 = ["False", 0, 0, 0, 0, 0, 0]
            self.color_ard_r3 = ["False", 0, 0, 0, 0, 0, 0]
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

        # SOF apply (requires active color first)
        self.SOF_1_APPLY(self.sof_1)
        self.SOF_2_APPLY(self.sof_2)
        self.SOF_3_APPLY(self.sof_3)

        # UI
        ui_string = Krita.instance().readSetting("Pigment.O", "UI", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        ui_split = ui_string.split(",")
        try:
            self.layout.aaa.setChecked(eval(ui_split[0]))
            self.layout.rgb.setChecked(eval(ui_split[1]))
            self.layout.ard.setChecked(eval(ui_split[2]))
            self.layout.hsv.setChecked(eval(ui_split[3]))
            self.layout.hsl.setChecked(eval(ui_split[4]))
            self.layout.cmyk.setChecked(eval(ui_split[5]))
            self.layout.tip.setChecked(eval(ui_split[6]))
            self.layout.tts.setChecked(eval(ui_split[7]))
            self.layout.mixer_selector.setCurrentIndex(int(ui_split[8]))
            self.layout.panel_selector.setCurrentIndex(int(ui_split[9]))
            self.layout.sof.setChecked(eval(ui_split[10]))
            self.layout.gray_sliders.setChecked(eval(ui_split[11]))
            self.layout.gray_panels.setChecked(eval(ui_split[12]))
        except:
            self.layout.aaa.setChecked(False)
            self.layout.rgb.setChecked(True)
            self.layout.ard.setChecked(False)
            self.layout.hsv.setChecked(False)
            self.layout.hsl.setChecked(False)
            self.layout.cmyk.setChecked(False)
            self.layout.tip.setChecked(False)
            self.layout.tts.setChecked(False)
            self.layout.mixer_selector.setCurrentIndex(0)
            self.layout.panel_selector.setCurrentIndex(0)
            self.layout.sof.setChecked(False)
            self.layout.gray_sliders.setChecked(False)
            self.layout.gray_panels.setChecked(False)
        self.Menu_Load()
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
            mixer_list_ard_1 = (str(self.color_ard_l1[0]), str(self.color_ard_l1[1]), str(self.color_ard_l1[2]), str(self.color_ard_l1[3]), str(self.color_ard_l1[4]), str(self.color_ard_l1[5]), str(self.color_ard_l1[6]), str(self.color_ard_r1[0]), str(self.color_ard_r1[1]), str(self.color_ard_r1[2]), str(self.color_ard_r1[3]), str(self.color_ard_r1[4]), str(self.color_ard_r1[5]), str(self.color_ard_r1[6]) )
            mixer_list_ard_2 = (str(self.color_ard_l2[0]), str(self.color_ard_l2[1]), str(self.color_ard_l2[2]), str(self.color_ard_l2[3]), str(self.color_ard_l2[4]), str(self.color_ard_l2[5]), str(self.color_ard_l2[6]), str(self.color_ard_r2[0]), str(self.color_ard_r2[1]), str(self.color_ard_r2[2]), str(self.color_ard_r2[3]), str(self.color_ard_r2[4]), str(self.color_ard_r2[5]), str(self.color_ard_r2[6]) )
            mixer_list_ard_3 = (str(self.color_ard_l3[0]), str(self.color_ard_l3[1]), str(self.color_ard_l3[2]), str(self.color_ard_l3[3]), str(self.color_ard_l3[4]), str(self.color_ard_l3[5]), str(self.color_ard_l3[6]), str(self.color_ard_r3[0]), str(self.color_ard_r3[1]), str(self.color_ard_r3[2]), str(self.color_ard_r3[3]), str(self.color_ard_r3[4]), str(self.color_ard_r3[5]), str(self.color_ard_r3[6]) )
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

            # UI
            ui_list = (
                str(self.layout.aaa.isChecked()),
                str(self.layout.rgb.isChecked()),
                str(self.layout.ard.isChecked()),
                str(self.layout.hsv.isChecked()),
                str(self.layout.hsl.isChecked()),
                str(self.layout.cmyk.isChecked()),
                str(self.layout.tip.isChecked()),
                str(self.layout.tts.isChecked()),
                str(self.layout.mixer_selector.currentIndex()),
                str(self.layout.panel_selector.currentIndex()),
                str(self.layout.sof.isChecked()),
                str(self.layout.gray_sliders.isChecked()),
                str(self.layout.gray_panels.isChecked()),
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

    # Change the Canvas ########################################################
    def canvasChanged(self, canvas):
        pass
