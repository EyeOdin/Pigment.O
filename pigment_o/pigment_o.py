#\\ Import Modules #############################################################
# Krita Modules
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt
import math
import random
import os
import time
# Pigment.O Modules
from .pigment_o_names import *
from .pigment_o_modulo import (
    Luma_Lock,
    Harmony,
    Apply_RGB,
    Panel_UVD,
    Panel_ARD,
    Panel_HSV_4,
    Panel_HSL_3,
    Panel_HSL_4,
    Panel_HSL_4D,
    Panel_YUV,
    Panel_HUE_Circle,
    Panel_GAM_Circle,
    Panel_GAM_Polygon,
    Panel_DOT,
    Panel_OBJ,
    Channel_Linear,
    Clicks,
    Mixer_Gradient,
    )

#//
#\\ Global Variables ###########################################################
# Set Window Title Name
DOCKER_NAME = "Pigment.O"
# Timer
check_timer = 1000  # 1000 = 1 SECOND (Zero will Disable checks)
# Pigment.O Version Date
pigment_o_version = "2021_02_12"
# SOF Constants
k_S = 1000
k_O = 100
k_F = 100
# Color Space Constants
k_AAA = 255
k_RGB = 255
k_UVD = 255  # U(horizontal) V(Vertical) Diagonal
k_ANG = 360  # Angle
k_RDL = 255  # Ratio + Diagonal
k_HUE = 360
k_SVL = 255  # Saturation + Value + Lightness + Chroma + Luma
k_Y = 256
k_U = 256
k_V = 256
k_RYB = 255
k_CMY = 255
k_CMYK = 255
hex_AAA = 100  # DO NOT TOUCH !
hex_RGB = 255  # DO NOT TOUCH !
hex_CMYK = 100  # DO NOT TOUCH !
u_AAA = 1 / k_AAA
u_RGB = 1 / k_RGB
u_ANG = 1 / k_ANG
u_RDL = 1 / k_RDL
u_HUE = 1 / k_HUE
u_SVCLY = 1 / k_SVL
u_Y = 1 / k_Y
u_U = 1 / k_Y
u_V = 1 / k_V
u_RYB = 1 / k_RYB
u_CMY = 1 / k_CMY
u_CMYK = 1 / k_CMYK
h_U = k_U * 0.5
h_V = k_V * 0.5
# Numbers
zero = 0
half = 0.5
unit = 1
two = 2
max_val = 16777215
# UI variables
ui_menu = 20
ui_5 = 5
ui_10 = 10
ui_15 = 15
ui_17 = 17
ui_20 = 20
ui_25 = 25
ui_30 = 30
ui_35 = 35
ui_40 = 40
ui_45 = 45
ui_47 = 47
ui_50 = 50
ui_55 = 55
ui_60 = 60
ui_65 = 65
ui_70 = 70
limit = 400
ui_total = 30
ui_color = 10
ui_harmony = 20
# Brush Tip Default
size = 40
opacity = 1
flow = 1
# Color Reference
color_white = [1, 1, 1]
color_grey = [0.5, 0.5, 0.5]
color_black = [0, 0, 0]
accent_color = [61, 174, 233]
accent_color = [34, 78, 101]
bg_unseen = str("background-color: rgba(0,0,0,0);")
bg_alpha = str("background-color: rgba(0, 0, 0, 50); ")
bg_border = str("background-color: rgba(56, 56, 56, 255); ")
bg_white = str("background-color: rgba(255, 255, 255, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_grey = str("background-color: rgba(127, 127, 127, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_black = str("background-color: rgba(0, 0, 0, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_white_border = str("background-color: rgb(255, 255, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_grey_border = str("background-color: rgb(127, 127, 127); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_black_border = str("background-color: rgb(0, 0, 0); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_gradient = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.000 rgba(0, 0, 0, 0), stop:1.000 rgba(0, 0, 0, 50));")
bg_bw = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.000 rgb(0, 0, 0), stop:1.000 rgb(255, 255, 255));")
bg_eraser_on = str("background-color: rgba(212, 212, 212, 255); border: 1px solid rgba(56, 56, 56, 255) ;")
bg_temp = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.000 rgba(200, 0, 0, 50), stop:0.500 rgba(200, 200, 200, 0), stop:1.000 rgba(0, 100, 200, 50));")
bg_rainbow = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.000 rgb(255, 0, 0), stop:0.167 rgb(255, 255, 0), stop:0.333 rgb(0, 255, 0), stop:0.500 rgb(0, 255, 255), stop:0.666 rgb(0, 0, 255), stop:0.833 rgb(255, 0, 255), stop:1.000 rgb(255, 0, 0)); border: 1px solid rgb(56, 56, 56) ;")
# RYB angle conversion stops
cmy_step = [0, 35/360, 60/360, 120/360, 180/360, 240/360, 300/360, 1]
ryb_step = [0, 60/360, 122/360, 165/360, 218/360, 275/360, 330/360, 1]
# Kalvin Table
k_KKKmin = 1000
k_KKKmax = 12000
k_KKKdelta = k_KKKmax - k_KKKmin
k_KKKhalf = 6500
k_KKKunit = 100
kelvin_table = [
    [1000, 255, 56, 0],
    [1100, 255, 71, 0],
    [1200, 255, 83, 0],
    [1300, 255, 93, 0],
    [1400, 255, 101, 0],
    [1500, 255, 109, 0],
    [1600, 255, 115, 0],
    [1700, 255, 121, 0],
    [1800, 255, 126, 0],
    [1900, 255, 131, 0],
    [2000, 255, 138, 18],
    [2100, 255, 142, 33],
    [2200, 255, 147, 44],
    [2300, 255, 152, 54],
    [2400, 255, 157, 63],
    [2500, 255, 161, 72],
    [2600, 255, 165, 79],
    [2700, 255, 169, 87],
    [2800, 255, 173, 94],
    [2900, 255, 177, 101],
    [3000, 255, 180, 107],
    [3100, 255, 184, 114],
    [3200, 255, 187, 120],
    [3300, 255, 190, 126],
    [3400, 255, 193, 132],
    [3500, 255, 196, 137],
    [3600, 255, 199, 143],
    [3700, 255, 201, 148],
    [3800, 255, 204, 153],
    [3900, 255, 206, 159],
    [4000, 255, 209, 163],
    [4100, 255, 211, 168],
    [4200, 255, 213, 173],
    [4300, 255, 215, 177],
    [4400, 255, 217, 182],
    [4500, 255, 219, 186],
    [4600, 255, 221, 190],
    [4700, 255, 223, 194],
    [4800, 255, 225, 198],
    [4900, 255, 227, 202],
    [5000, 255, 228, 206],
    [5100, 255, 230, 210],
    [5200, 255, 232, 213],
    [5300, 255, 233, 217],
    [5400, 255, 235, 220],
    [5500, 255, 236, 224],
    [5600, 255, 238, 227],
    [5700, 255, 239, 230],
    [5800, 255, 240, 233],
    [5900, 255, 242, 236],
    [6000, 255, 243, 239],
    [6100, 255, 244, 242],
    [6200, 255, 245, 245],
    [6300, 255, 246, 247],
    [6400, 255, 248, 251],
    [6500, 255, 249, 253],
    [6600, 254, 249, 255],
    [6700, 252, 247, 255],
    [6800, 249, 246, 255],
    [6900, 247, 245, 255],
    [7000, 245, 243, 255],
    [7100, 243, 242, 255],
    [7200, 240, 241, 255],
    [7300, 239, 240, 255],
    [7400, 237, 239, 255],
    [7500, 235, 238, 255],
    [7600, 233, 237, 255],
    [7700, 231, 236, 255],
    [7800, 230, 235, 255],
    [7900, 228, 234, 255],
    [8000, 227, 233, 255],
    [8100, 225, 232, 255],
    [8200, 224, 231, 255],
    [8300, 222, 230, 255],
    [8400, 221, 230, 255],
    [8500, 220, 229, 255],
    [8600, 218, 229, 255],
    [8700, 217, 227, 255],
    [8800, 216, 227, 255],
    [8900, 215, 226, 255],
    [9000, 214, 225, 255],
    [9100, 212, 225, 255],
    [9200, 211, 224, 255],
    [9300, 210, 223, 255],
    [9400, 209, 223, 255],
    [9500, 208, 222, 255],
    [9600, 207, 221, 255],
    [9700, 207, 221, 255],
    [9800, 207, 220, 255],
    [9900, 206, 220, 255],
    [10000, 206, 218, 255],
    [10100, 206, 218, 255],
    [10200, 205, 217, 255],
    [10300, 205, 217, 255],
    [10400, 204, 216, 255],
    [10500, 204, 216, 255],
    [10600, 203, 215, 255],
    [10700, 202, 215, 255],
    [10800, 202, 214, 255],
    [10900, 201, 214, 255],
    [11000, 200, 213, 255],
    [11100, 200, 213, 255],
    [11200, 199, 212, 255],
    [11300, 198, 212, 255],
    [11400, 198, 212, 255],
    [11500, 197, 211, 255],
    [11600, 197, 211, 255],
    [11700, 197, 210, 255],
    [11800, 196, 210, 255],
    [11900, 195, 210, 255],
    [12000, 195, 209, 255]]
standard_illuminants = [
    [1000, ""],
    [2724, "LED-V1 - Phosphor-converted violet"],
    [2733, "LED-B1 - Phosphor-converted blue"],
    [2840, "LED-RGB1 - Mixing of red, green, and blue LEDs"],
    [2851, "LED-BH1 - Mixing of phosphor-converted blue LED and red LED (blue-hybrid)"],
    [2856, "A - Incandescent / tungsten"],
    [2940, "F4 - Warm white fluorescent"],
    [2998, "LED-B2 - Phosphor-converted blue"],
    [3000, "F12 - Philips TL83, Ultralume 30"],
    [3450, "F3 - White fluorescent"],
    [4000, "F11 - Philips TL84, Ultralume 40"],
    [4070, "LED-V2 - Phosphor-converted violet"],
    [4103, "LED-B3 - Phosphor-converted blue"],
    [4150, "F6/F9 - Light white fluorescent / cool white deluxe fluorescent"],
    [4230, "F2 - Cool white fluorescent"],
    [4874, "B - Obsolete, direct sunlight at noon"],
    [5000, "F8/F10 - D50 simulator, Sylvania F40 Design 50 / Philips TL85, Ultralume 50"],
    [5003, "D50 - Horizon light, ICC profile PCS"],
    [5109, "LED-B4 - Phosphor-converted blue"],
    [5454, "E - Equal Energy"],
    [5503, "D55 - Mid-morning / mid-afternoon daylight"],
    [6350, "F5 - Daylight fluorescent"],
    [6430, "F1 - Daylight fluorescent"],
    [6500, "F7 - D65 simulator, daylight simulator"],
    [6504, "D65 - Noon daylight: television, sRGB color space"],
    [6598, "LED-B5 - Phosphor-converted blue"],
    [6774, "C - Obsolete, average / North sky daylight"],
    [7504, "D75 - North sky daylight"],
    [9305, "D95 - High-efficiency blue phosphor monitors, BT.2035"],
    [12000, ""],
    ]
#//


# Create Docker
class PigmentODocker(DockWidget):
    """
    Color Picker and Mixer.
    """

    #\\ Initialize the Docker Window ###########################################
    def __init__(self):
        super(PigmentODocker, self).__init__()

        # Construct
        self.Variables()
        self.User_Interface()
        self.Menu_Shrink()

        # Modules and Connections
        self.Harmonys()
        self.Color_ofthe_Day()
        self.Panels()
        self.Gamut()
        self.Dots()
        self.Object()
        self.Channels()
        self.Palette()
        self.Mixers()
        self.Style_Widget()

        # Settings
        self.Version_Settings()
        self.Actions()

    def Variables(self):
        # Luma Coefficients - ITU-R BT.601
        self.luma_r = 0.299
        self.luma_b = 0.114
        self.luma_g = 1 - self.luma_r - self.luma_b # 0.587
        self.luma_pr = 1.402
        self.luma_pb = 1.772
        # Harmony
        self.harmony_active = 0
    def User_Interface(self):
        # Operating System
        self.OS = str(QSysInfo.kernelType()) # WINDOWS=winnt & LINUX=linux
        # Path Name
        self.dir_name = str(os.path.dirname(os.path.realpath(__file__)))
        # Window Title
        self.setWindowTitle(DOCKER_NAME)
        # Pigmento Widget
        self.window = QWidget()
        self.layout = uic.loadUi(self.dir_name + '/pigment_o.ui', self.window)
        self.setWidget(self.window)
        # Theme Variables
        self.theme_krita = 59
        self.theme_pigment = 196
        self.gray_natural = self.HEX_6string(self.theme_krita/255,self.theme_krita/255,self.theme_krita/255)
        self.gray_contrast = self.HEX_6string(self.theme_pigment/255,self.theme_pigment/255,self.theme_pigment/255)
        self.color_accent = "#3daee9"
        # Start Timer and Connect Switch
        if check_timer >= 1000:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Krita_2_Pigment)
            self.timer.start(check_timer)
            # Method ON/OFF switch boot
            self.layout.check.setCheckState(1)
            self.Krita_TIMER()
            # Stop Timer so it does work without the Docker Present
            self.timer.stop()
        else:
            self.layout.check.setCheckState(0)
        # UI 1
        self.layout.sof.toggled.connect(self.Menu_SOF)
        self.layout.aaa.toggled.connect(self.Menu_AAA)
        self.layout.rgb.toggled.connect(self.Menu_RGB)
        self.layout.ard.toggled.connect(self.Menu_ARD)
        self.layout.hsv.toggled.connect(self.Menu_HSV)
        self.layout.hsl.toggled.connect(self.Menu_HSL)
        self.layout.hcy.toggled.connect(self.Menu_HCY)
        self.layout.yuv.toggled.connect(self.Menu_YUV)
        self.layout.ryb.toggled.connect(self.Menu_RYB)
        self.layout.cmy.toggled.connect(self.Menu_CMY)
        self.layout.cmyk.toggled.connect(self.Menu_CMYK)
        self.layout.kkk.toggled.connect(self.Menu_KKK)
        # UI 2
        self.layout.har.toggled.connect(self.Menu_HARMONY)
        self.layout.cotd.toggled.connect(self.Menu_COTD)
        self.layout.pan.toggled.connect(self.Menu_PANEL)
        self.layout.tip.toggled.connect(self.Menu_TIP)
        self.layout.tts.toggled.connect(self.Menu_TTS)
        self.layout.mix.toggled.connect(self.Menu_MIX)
        # UI 3
        self.layout.har_index.currentTextChanged.connect(self.HARMONY_Index)
        self.layout.har_edit.toggled.connect(self.HARMONY_Edit)
        self.layout.pan_index.currentTextChanged.connect(self.Menu_PANEL)
        self.layout.pan_secondary.currentTextChanged.connect(self.Menu_Hue_Secondary)
        self.layout.gam_space.currentTextChanged.connect(self.GAM_Space)
        self.layout.gam_shape.currentTextChanged.connect(self.GAM_Shape)
        self.layout.dot_set.toggled.connect(self.DOT_SET)
        self.layout.obj_index.currentTextChanged.connect(self.OBJ_Index)
        self.layout.obj_set.toggled.connect(self.OBJ_SET)
        self.layout.values.toggled.connect(self.Menu_Value)
        self.layout.hue_shine.toggled.connect(self.Menu_Hue_Shine)
        self.layout.mix_index.currentTextChanged.connect(self.Menu_MIX)
        self.layout.names_display.toggled.connect(self.Menu_Names)
        self.layout.names_closest.clicked.connect(self.HEX_Closest)
        self.layout.wheel_index.currentTextChanged.connect(self.Menu_Wheel)
        self.layout.luminosity.currentTextChanged.connect(self.Menu_Luminosity)
        # UI 4
        self.layout.check.stateChanged.connect(self.Krita_TIMER)
        self.layout.ui_2.toggled.connect(self.Menu_UI_2)
        self.layout.ui_1.toggled.connect(self.Menu_UI_1)
        # Luminosity Lock
        self.luma_lock_1 = Luma_Lock(self.layout.color_1)
        self.luma_lock_1.SIGNAL_LUMA_LOCK.connect(self.Pigment_AAA_1_Lock)
        self.luma_lock_1.Setup(1)
        self.luma_lock_2 = Luma_Lock(self.layout.color_2)
        self.luma_lock_2.SIGNAL_LUMA_LOCK.connect(self.Pigment_AAA_1_Lock)
        self.luma_lock_2.Setup(2)
    def Harmonys(self):
        self.harmony_1 = Harmony(self.layout.harmony_1)
        self.harmony_2 = Harmony(self.layout.harmony_2)
        self.harmony_3 = Harmony(self.layout.harmony_3)
        self.harmony_4 = Harmony(self.layout.harmony_4)
        self.harmony_5 = Harmony(self.layout.harmony_5)
        self.harmony_1.SIGNAL_ACTIVE.connect(self.Harmony_1_Active)
        self.harmony_2.SIGNAL_ACTIVE.connect(self.Harmony_2_Active)
        self.harmony_3.SIGNAL_ACTIVE.connect(self.Harmony_3_Active)
        self.harmony_4.SIGNAL_ACTIVE.connect(self.Harmony_4_Active)
        self.harmony_5.SIGNAL_ACTIVE.connect(self.Harmony_5_Active)
    def Color_ofthe_Day(self):
        # What day is for the User
        self.year = QDate.currentDate().year()
        self.month = QDate.currentDate().month()
        self.day = QDate.currentDate().day()
        self.layout.cotd_date.setText(str(self.year)+"-"+str(self.month)+"-"+str(self.day))
        self.layout.cotd_date.setStyleSheet(bg_alpha)
        # Random Seed
        random.seed(self.year + self.month + self.day)
        # 1
        self.cotd1_1 = round(random.random()*255)/255
        self.cotd1_2 = round(random.random()*255)/255
        self.cotd1_3 = round(random.random()*255)/255
        self.layout.cotd1.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.cotd1_1*255, self.cotd1_2*255, self.cotd1_3*255)))
        self.cotd1 = Apply_RGB(self.layout.cotd1)
        self.cotd1.Setup(self.cotd1_1, self.cotd1_2, self.cotd1_3)
        self.cotd1.SIGNAL_APPLY.connect(self.Apply_RGB)
        # 2
        self.cotd2_1 = round(random.random()*255)/255
        self.cotd2_2 = round(random.random()*255)/255
        self.cotd2_3 = round(random.random()*255)/255
        self.layout.cotd2.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.cotd2_1*255, self.cotd2_2*255, self.cotd2_3*255)))
        self.cotd2 = Apply_RGB(self.layout.cotd2)
        self.cotd2.Setup(self.cotd2_1, self.cotd2_2, self.cotd2_3)
        self.cotd2.SIGNAL_APPLY.connect(self.Apply_RGB)
        # 3
        self.cotd3_1 = round(random.random()*255)/255
        self.cotd3_2 = round(random.random()*255)/255
        self.cotd3_3 = round(random.random()*255)/255
        self.layout.cotd3.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.cotd3_1*255, self.cotd3_2*255, self.cotd3_3*255)))
        self.cotd3 = Apply_RGB(self.layout.cotd3)
        self.cotd3.Setup(self.cotd3_1, self.cotd3_2, self.cotd3_3)
        self.cotd3.SIGNAL_APPLY.connect(self.Apply_RGB)
        # 4
        self.cotd4_1 = round(random.random()*255)/255
        self.cotd4_2 = round(random.random()*255)/255
        self.cotd4_3 = round(random.random()*255)/255
        self.layout.cotd4.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.cotd4_1*255, self.cotd4_2*255, self.cotd4_3*255)))
        self.cotd4 = Apply_RGB(self.layout.cotd4)
        self.cotd4.Setup(self.cotd4_1, self.cotd4_2, self.cotd4_3)
        self.cotd4.SIGNAL_APPLY.connect(self.Apply_RGB)
        # 5
        self.cotd5_1 = round(random.random()*255)/255
        self.cotd5_2 = round(random.random()*255)/255
        self.cotd5_3 = round(random.random()*255)/255
        self.layout.cotd5.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.cotd5_1*255, self.cotd5_2*255, self.cotd5_3*255)))
        self.cotd5 = Apply_RGB(self.layout.cotd5)
        self.cotd5.Setup(self.cotd5_1, self.cotd5_2, self.cotd5_3)
        self.cotd5.SIGNAL_APPLY.connect(self.Apply_RGB)
    def Panels(self):
        # Panel UVD
        self.panel_uvd = Panel_UVD(self.layout.panel_uvd)
        self.panel_uvd.SIGNAL_UVD_VALUE.connect(self.Signal_UVD)
        self.panel_uvd.SIGNAL_UVD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_uvd.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel ARD
        self.panel_ard = Panel_ARD(self.layout.panel_ard)
        self.panel_ard.SIGNAL_ARD_VALUE.connect(self.Signal_ARD)
        self.panel_ard.SIGNAL_ARD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_ard.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HSV
        self.panel_hsv = Panel_HSV_4(self.layout.panel_hsv)
        self.panel_hsv.SIGNAL_HSV_4_VALUE.connect(self.Signal_HSV_4)
        self.panel_hsv.SIGNAL_HSV_4_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsv.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HSL
        self.panel_hsl = Panel_HSL_4(self.layout.panel_hsl)
        self.panel_hsl.SIGNAL_HSL_4_VALUE.connect(self.Signal_HSL_4)
        self.panel_hsl.SIGNAL_HSL_4_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsl.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel YUV
        self.panel_yuv = Panel_YUV(self.layout.panel_yuv)
        self.panel_yuv.SIGNAL_YUV_VALUE.connect(self.Signal_YUV)
        self.panel_yuv.SIGNAL_YUV_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_yuv.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HUE Circle
        self.panel_hue_circle = Panel_HUE_Circle(self.layout.panel_hue_circle)
        self.panel_hue_circle.SIGNAL_HUE_C_VALUE.connect(self.Signal_HUE_Circle)
        self.panel_hue_circle.SIGNAL_HUE_C_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hue_circle.SIGNAL_HUE_C_HARMONY_ACTIVE.connect(self.Pigment_HUE_Harmony_Active)
        self.panel_hue_circle.Active(self.harmony_active)

        # Panel HUE Regular
        self.panel_triangle = Panel_HSL_3(self.layout.panel_triangle)
        self.panel_triangle.SIGNAL_HSL_3_VALUE.connect(self.Signal_HSL_3)
        self.panel_triangle.SIGNAL_HSL_3_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_triangle.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        self.panel_square = Panel_HSV_4(self.layout.panel_square)
        self.panel_square.SIGNAL_HSV_4_VALUE.connect(self.Signal_HSV_4)
        self.panel_square.SIGNAL_HSV_4_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_square.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        self.panel_diamond = Panel_HSL_4D(self.layout.panel_diamond)
        self.panel_diamond.SIGNAL_HSL_4D_VALUE.connect(self.Signal_HSL_4D)
        self.panel_diamond.SIGNAL_HSL_4D_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_diamond.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
    def Gamut(self):
        # Panel GAMut Circle
        self.panel_gam_circle = Panel_GAM_Circle(self.layout.panel_gam_circle)
        self.panel_gam_circle.SIGNAL_GAM_C_VALUE.connect(self.Signal_GAM_Circle)
        self.panel_gam_circle.SIGNAL_GAM_C_RELEASE.connect(self.Pigment_Display_Release)
        # Panel GAMut Poly
        self.panel_gam_polygon = Panel_GAM_Polygon(self.layout.panel_gam_polygon)
        self.panel_gam_polygon.SIGNAL_GAM_P_POINTS.connect(self.Signal_GAM_Points)
        self.panel_gam_polygon.SIGNAL_GAM_P_VALUE.connect(self.Signal_GAM_Polygon)
        self.panel_gam_polygon.SIGNAL_GAM_P_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_gam_polygon.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
    def Dots(self):
        self.panel_dots = Panel_DOT(self.layout.panel_dot_mix)
        self.panel_dots.SIGNAL_DOT_VALUE.connect(self.Signal_DOT)
        self.panel_dots.SIGNAL_DOT_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_dots.SIGNAL_DOT_LOCATION.connect(self.Signal_DOT_Location)

        self.color_dot_1 = Clicks(self.layout.dot_1)
        self.color_dot_1.SIGNAL_APPLY.connect(self.DOT_1_APPLY)
        self.color_dot_1.SIGNAL_SAVE.connect(self.DOT_1_SAVE)
        self.color_dot_1.SIGNAL_CLEAN.connect(self.DOT_1_CLEAN)

        self.color_dot_2 = Clicks(self.layout.dot_2)
        self.color_dot_2.SIGNAL_APPLY.connect(self.DOT_2_APPLY)
        self.color_dot_2.SIGNAL_SAVE.connect(self.DOT_2_SAVE)
        self.color_dot_2.SIGNAL_CLEAN.connect(self.DOT_2_CLEAN)

        self.color_dot_3 = Clicks(self.layout.dot_3)
        self.color_dot_3.SIGNAL_APPLY.connect(self.DOT_3_APPLY)
        self.color_dot_3.SIGNAL_SAVE.connect(self.DOT_3_SAVE)
        self.color_dot_3.SIGNAL_CLEAN.connect(self.DOT_3_CLEAN)

        self.color_dot_4 = Clicks(self.layout.dot_4)
        self.color_dot_4.SIGNAL_APPLY.connect(self.DOT_4_APPLY)
        self.color_dot_4.SIGNAL_SAVE.connect(self.DOT_4_SAVE)
        self.color_dot_4.SIGNAL_CLEAN.connect(self.DOT_4_CLEAN)

        self.layout.dot_swap.clicked.connect(self.DOT_SWAP)
    def Object(self):
        # Panel OBJ (Only updates the Cursor location)
        self.panel_obj = Panel_OBJ(self.layout.layer_cursor)
        self.panel_obj.SIGNAL_OBJ_PRESS.connect(self.Signal_OBJ)
        self.panel_obj.SIGNAL_OBJ_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_obj.SIGNAL_OBJ_LOCATION.connect(self.Signal_OBJ_Location)

        # Background 1
        self.layout.b1_live.clicked.connect(self.BG_1_Exclusion)
        self.b1_color = Clicks(self.layout.b1_color)
        self.b1_color.SIGNAL_APPLY.connect(self.BG_1_APPLY)
        self.b1_color.SIGNAL_SAVE.connect(lambda: self.BG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.bg_1[self.obj_index][4]))
        self.b1_color.SIGNAL_CLEAN.connect(self.BG_1_CLEAN)
        self.b1_alpha = Channel_Linear(self.layout.b1_alpha)
        self.b1_alpha.Setup("NEU")
        self.b1_alpha.SIGNAL_VALUE.connect(self.BG_1_ALPHA)
        # Background 2
        self.layout.b2_live.clicked.connect(self.BG_2_Exclusion)
        self.b2_color = Clicks(self.layout.b2_color)
        self.b2_color.SIGNAL_APPLY.connect(self.BG_2_APPLY)
        self.b2_color.SIGNAL_SAVE.connect(lambda: self.BG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.bg_2[self.obj_index][4]))
        self.b2_color.SIGNAL_CLEAN.connect(self.BG_2_CLEAN)
        self.b2_alpha = Channel_Linear(self.layout.b2_alpha)
        self.b2_alpha.Setup("NEU")
        self.b2_alpha.SIGNAL_VALUE.connect(self.BG_2_ALPHA)
        # Background 3
        self.layout.b3_live.clicked.connect(self.BG_3_Exclusion)
        self.b3_color = Clicks(self.layout.b3_color)
        self.b3_color.SIGNAL_APPLY.connect(self.BG_3_APPLY)
        self.b3_color.SIGNAL_SAVE.connect(lambda: self.BG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.bg_3[self.obj_index][4]))
        self.b3_color.SIGNAL_CLEAN.connect(self.BG_3_CLEAN)
        self.b3_alpha = Channel_Linear(self.layout.b3_alpha)
        self.b3_alpha.Setup("NEU")
        self.b3_alpha.SIGNAL_VALUE.connect(self.BG_3_ALPHA)

        # Diffuse 1
        self.layout.d1_live.clicked.connect(self.DIF_1_Exclusion)
        self.d1_color = Clicks(self.layout.d1_color)
        self.d1_color.SIGNAL_APPLY.connect(self.DIF_1_APPLY)
        self.d1_color.SIGNAL_SAVE.connect(lambda: self.DIF_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_1[self.obj_index][4]))
        self.d1_color.SIGNAL_CLEAN.connect(self.DIF_1_CLEAN)
        self.d1_alpha = Channel_Linear(self.layout.d1_alpha)
        self.d1_alpha.Setup("NEU")
        self.d1_alpha.SIGNAL_VALUE.connect(self.DIF_1_ALPHA)
        # Diffuse 2
        self.layout.d2_live.clicked.connect(self.DIF_2_Exclusion)
        self.d2_color = Clicks(self.layout.d2_color)
        self.d2_color.SIGNAL_APPLY.connect(self.DIF_2_APPLY)
        self.d2_color.SIGNAL_SAVE.connect(lambda: self.DIF_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_2[self.obj_index][4]))
        self.d2_color.SIGNAL_CLEAN.connect(self.DIF_2_CLEAN)
        self.d2_alpha = Channel_Linear(self.layout.d2_alpha)
        self.d2_alpha.Setup("NEU")
        self.d2_alpha.SIGNAL_VALUE.connect(self.DIF_2_ALPHA)
        # Diffuse 3
        self.layout.d3_live.clicked.connect(self.DIF_3_Exclusion)
        self.d3_color = Clicks(self.layout.d3_color)
        self.d3_color.SIGNAL_APPLY.connect(self.DIF_3_APPLY)
        self.d3_color.SIGNAL_SAVE.connect(lambda: self.DIF_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_3[self.obj_index][4]))
        self.d3_color.SIGNAL_CLEAN.connect(self.DIF_3_CLEAN)
        self.d3_alpha = Channel_Linear(self.layout.d3_alpha)
        self.d3_alpha.Setup("NEU")
        self.d3_alpha.SIGNAL_VALUE.connect(self.DIF_3_ALPHA)
        # Diffuse 4
        self.layout.d4_live.clicked.connect(self.DIF_4_Exclusion)
        self.d4_color = Clicks(self.layout.d4_color)
        self.d4_color.SIGNAL_APPLY.connect(self.DIF_4_APPLY)
        self.d4_color.SIGNAL_SAVE.connect(lambda: self.DIF_4_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_4[self.obj_index][4]))
        self.d4_color.SIGNAL_CLEAN.connect(self.DIF_4_CLEAN)
        self.d4_alpha = Channel_Linear(self.layout.d4_alpha)
        self.d4_alpha.Setup("NEU")
        self.d4_alpha.SIGNAL_VALUE.connect(self.DIF_4_ALPHA)
        # Diffuse 5
        self.layout.d5_live.clicked.connect(self.DIF_5_Exclusion)
        self.d5_color = Clicks(self.layout.d5_color)
        self.d5_color.SIGNAL_APPLY.connect(self.DIF_5_APPLY)
        self.d5_color.SIGNAL_SAVE.connect(lambda: self.DIF_5_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_5[self.obj_index][4]))
        self.d5_color.SIGNAL_CLEAN.connect(self.DIF_5_CLEAN)
        self.d5_alpha = Channel_Linear(self.layout.d5_alpha)
        self.d5_alpha.Setup("NEU")
        self.d5_alpha.SIGNAL_VALUE.connect(self.DIF_5_ALPHA)
        # Diffuse 6
        self.layout.d6_live.clicked.connect(self.DIF_6_Exclusion)
        self.d6_color = Clicks(self.layout.d6_color)
        self.d6_color.SIGNAL_APPLY.connect(self.DIF_6_APPLY)
        self.d6_color.SIGNAL_SAVE.connect(lambda: self.DIF_6_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_6[self.obj_index][4]))
        self.d6_color.SIGNAL_CLEAN.connect(self.DIF_6_CLEAN)
        self.d6_alpha = Channel_Linear(self.layout.d6_alpha)
        self.d6_alpha.Setup("NEU")
        self.d6_alpha.SIGNAL_VALUE.connect(self.DIF_6_ALPHA)

        # Foreground 1
        self.layout.f1_live.clicked.connect(self.FG_1_Exclusion)
        self.f1_color = Clicks(self.layout.f1_color)
        self.f1_color.SIGNAL_APPLY.connect(self.FG_1_APPLY)
        self.f1_color.SIGNAL_SAVE.connect(lambda: self.FG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.fg_1[self.obj_index][4]))
        self.f1_color.SIGNAL_CLEAN.connect(self.FG_1_CLEAN)
        self.f1_alpha = Channel_Linear(self.layout.f1_alpha)
        self.f1_alpha.Setup("NEU")
        self.f1_alpha.SIGNAL_VALUE.connect(self.FG_1_ALPHA)
        # Foreground 2
        self.layout.f2_live.clicked.connect(self.FG_2_Exclusion)
        self.f2_color = Clicks(self.layout.f2_color)
        self.f2_color.SIGNAL_APPLY.connect(self.FG_2_APPLY)
        self.f2_color.SIGNAL_SAVE.connect(lambda: self.FG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.fg_2[self.obj_index][4]))
        self.f2_color.SIGNAL_CLEAN.connect(self.FG_2_CLEAN)
        self.f2_alpha = Channel_Linear(self.layout.f2_alpha)
        self.f2_alpha.Setup("NEU")
        self.f2_alpha.SIGNAL_VALUE.connect(self.FG_2_ALPHA)
        # Foreground 3
        self.layout.f3_live.clicked.connect(self.FG_3_Exclusion)
        self.f3_color = Clicks(self.layout.f3_color)
        self.f3_color.SIGNAL_APPLY.connect(self.FG_3_APPLY)
        self.f3_color.SIGNAL_SAVE.connect(lambda: self.FG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.fg_3[self.obj_index][4]))
        self.f3_color.SIGNAL_CLEAN.connect(self.FG_3_CLEAN)
        self.f3_alpha = Channel_Linear(self.layout.f3_alpha)
        self.f3_alpha.Setup("NEU")
        self.f3_alpha.SIGNAL_VALUE.connect(self.FG_3_ALPHA)

        # Style Sheets
        self.layout.panel_obj_mix.setStyleSheet(bg_gradient)
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
        self.layout.layer_11.setStyleSheet(bg_unseen)
        self.layout.layer_12.setStyleSheet(bg_unseen)
        self.layout.layer_cursor.setStyleSheet(bg_unseen)
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
    def Channels(self):
        # SOF Range
        self.layout.sof_1_value.setMinimum(0)
        self.layout.sof_2_value.setMinimum(0)
        self.layout.sof_3_value.setMinimum(0)
        self.layout.sof_1_value.setMaximum(k_S)
        self.layout.sof_2_value.setMaximum(k_O)
        self.layout.sof_3_value.setMaximum(k_F)
        # Channels Range Minimum
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
        self.layout.hcy_1_value.setMinimum(0)
        self.layout.hcy_2_value.setMinimum(0)
        self.layout.hcy_3_value.setMinimum(0)
        self.layout.yuv_1_value.setMinimum(0)
        self.layout.yuv_2_value.setMinimum(0)
        self.layout.yuv_3_value.setMinimum(0)
        self.layout.ryb_1_value.setMinimum(0)
        self.layout.ryb_2_value.setMinimum(0)
        self.layout.ryb_3_value.setMinimum(0)
        self.layout.cmy_1_value.setMinimum(0)
        self.layout.cmy_2_value.setMinimum(0)
        self.layout.cmy_3_value.setMinimum(0)
        self.layout.cmyk_1_value.setMinimum(0)
        self.layout.cmyk_2_value.setMinimum(0)
        self.layout.cmyk_3_value.setMinimum(0)
        self.layout.cmyk_4_value.setMinimum(0)
        self.layout.kkk_1_value.setMinimum(k_KKKmin)
        # Channels Range Maximum
        self.layout.aaa_1_value.setMaximum(k_AAA)
        self.layout.rgb_1_value.setMaximum(k_RGB)
        self.layout.rgb_2_value.setMaximum(k_RGB)
        self.layout.rgb_3_value.setMaximum(k_RGB)
        self.layout.ard_1_value.setMaximum(k_ANG)
        self.layout.ard_2_value.setMaximum(k_RDL)
        self.layout.ard_3_value.setMaximum(k_RDL)
        self.layout.hsv_1_value.setMaximum(k_HUE)
        self.layout.hsv_2_value.setMaximum(k_SVL)
        self.layout.hsv_3_value.setMaximum(k_SVL)
        self.layout.hsl_1_value.setMaximum(k_HUE)
        self.layout.hsl_2_value.setMaximum(k_SVL)
        self.layout.hsl_3_value.setMaximum(k_SVL)
        self.layout.hcy_1_value.setMaximum(k_HUE)
        self.layout.hcy_2_value.setMaximum(k_SVL)
        self.layout.hcy_3_value.setMaximum(k_SVL)
        self.layout.yuv_1_value.setMaximum(k_Y)
        self.layout.yuv_2_value.setMaximum(k_U)
        self.layout.yuv_3_value.setMaximum(k_V)
        self.layout.ryb_1_value.setMaximum(k_RYB)
        self.layout.ryb_2_value.setMaximum(k_RYB)
        self.layout.ryb_3_value.setMaximum(k_RYB)
        self.layout.cmy_1_value.setMaximum(k_CMY)
        self.layout.cmy_2_value.setMaximum(k_CMY)
        self.layout.cmy_3_value.setMaximum(k_CMY)
        self.layout.cmyk_1_value.setMaximum(k_CMYK)
        self.layout.cmyk_2_value.setMaximum(k_CMYK)
        self.layout.cmyk_3_value.setMaximum(k_CMYK)
        self.layout.cmyk_4_value.setMaximum(k_CMYK)
        self.layout.kkk_1_value.setMaximum(k_KKKmax)
        # Module SOF
        self.sof_1_slider = Channel_Linear(self.layout.sof_1_slider)
        self.sof_2_slider = Channel_Linear(self.layout.sof_2_slider)
        self.sof_3_slider = Channel_Linear(self.layout.sof_3_slider)
        self.sof_1_slider.Setup("NEU")
        self.sof_2_slider.Setup("NEU")
        self.sof_3_slider.Setup("NEU")
        # Module Channel
        self.aaa_1_slider = Channel_Linear(self.layout.aaa_1_slider)
        self.aaa_1_slider.Setup("AAA1")
        self.rgb_1_slider = Channel_Linear(self.layout.rgb_1_slider)
        self.rgb_2_slider = Channel_Linear(self.layout.rgb_2_slider)
        self.rgb_3_slider = Channel_Linear(self.layout.rgb_3_slider)
        self.rgb_1_slider.Setup("RGB1")
        self.rgb_2_slider.Setup("RGB2")
        self.rgb_3_slider.Setup("RGB3")
        self.ard_1_slider = Channel_Linear(self.layout.ard_1_slider)
        self.ard_2_slider = Channel_Linear(self.layout.ard_2_slider)
        self.ard_3_slider = Channel_Linear(self.layout.ard_3_slider)
        self.ard_1_slider.Setup("HUE")
        self.ard_2_slider.Setup("ARD2")
        self.ard_3_slider.Setup("ARD3")
        self.hsv_1_slider = Channel_Linear(self.layout.hsv_1_slider)
        self.hsv_2_slider = Channel_Linear(self.layout.hsv_2_slider)
        self.hsv_3_slider = Channel_Linear(self.layout.hsv_3_slider)
        self.hsv_1_slider.Setup("HUE")
        self.hsv_2_slider.Setup("HSV2")
        self.hsv_3_slider.Setup("HSV3")
        self.hsl_1_slider = Channel_Linear(self.layout.hsl_1_slider)
        self.hsl_2_slider = Channel_Linear(self.layout.hsl_2_slider)
        self.hsl_3_slider = Channel_Linear(self.layout.hsl_3_slider)
        self.hsl_1_slider.Setup("HUE")
        self.hsl_2_slider.Setup("HSL2")
        self.hsl_3_slider.Setup("HSL3")
        self.hcy_1_slider = Channel_Linear(self.layout.hcy_1_slider)
        self.hcy_2_slider = Channel_Linear(self.layout.hcy_2_slider)
        self.hcy_3_slider = Channel_Linear(self.layout.hcy_3_slider)
        self.hcy_1_slider.Setup("HUE")
        self.hcy_2_slider.Setup("HCY2")
        self.hcy_3_slider.Setup("HCY3")
        self.yuv_1_slider = Channel_Linear(self.layout.yuv_1_slider)
        self.yuv_2_slider = Channel_Linear(self.layout.yuv_2_slider)
        self.yuv_3_slider = Channel_Linear(self.layout.yuv_3_slider)
        self.yuv_1_slider.Setup("YUV1")
        self.yuv_2_slider.Setup("YUV2")
        self.yuv_3_slider.Setup("YUV3")
        self.ryb_1_slider = Channel_Linear(self.layout.ryb_1_slider)
        self.ryb_2_slider = Channel_Linear(self.layout.ryb_2_slider)
        self.ryb_3_slider = Channel_Linear(self.layout.ryb_3_slider)
        self.ryb_1_slider.Setup("RYB1")
        self.ryb_2_slider.Setup("RYB2")
        self.ryb_3_slider.Setup("RYB3")
        self.cmy_1_slider = Channel_Linear(self.layout.cmy_1_slider)
        self.cmy_2_slider = Channel_Linear(self.layout.cmy_2_slider)
        self.cmy_3_slider = Channel_Linear(self.layout.cmy_3_slider)
        self.cmy_1_slider.Setup("CMY1")
        self.cmy_2_slider.Setup("CMY2")
        self.cmy_3_slider.Setup("CMY3")
        self.cmyk_1_slider = Channel_Linear(self.layout.cmyk_1_slider)
        self.cmyk_2_slider = Channel_Linear(self.layout.cmyk_2_slider)
        self.cmyk_3_slider = Channel_Linear(self.layout.cmyk_3_slider)
        self.cmyk_4_slider = Channel_Linear(self.layout.cmyk_4_slider)
        self.cmyk_1_slider.Setup("CMYK1")
        self.cmyk_2_slider.Setup("CMYK2")
        self.cmyk_3_slider.Setup("CMYK3")
        self.cmyk_4_slider.Setup("CMYK4")
        self.kkk_1_slider = Channel_Linear(self.layout.kkk_1_slider)
        self.kkk_1_slider.Setup("KKK1")

        # SIZE
        self.sof_1_slider.SIGNAL_HALF.connect(lambda: self.SOF_1_APPLY(self.lock_size))
        self.sof_1_slider.SIGNAL_MINUS.connect(self.Pigment_SOF_1_Minus)
        self.sof_1_slider.SIGNAL_PLUS.connect(self.Pigment_SOF_1_Plus)
        self.sof_1_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_1_Slider_Modify)
        self.layout.sof_1_value.valueChanged.connect(self.Pigment_SOF_1_Value_Modify)
        # OPACITY
        self.sof_2_slider.SIGNAL_HALF.connect(lambda: self.SOF_2_APPLY(self.lock_opacity))
        self.sof_2_slider.SIGNAL_MINUS.connect(self.Pigment_SOF_2_Minus)
        self.sof_2_slider.SIGNAL_PLUS.connect(self.Pigment_SOF_2_Plus)
        self.sof_2_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_2_Slider_Modify)
        self.layout.sof_2_value.valueChanged.connect(self.Pigment_SOF_2_Value_Modify)
        # FLOW
        self.sof_3_slider.SIGNAL_HALF.connect(lambda: self.SOF_3_APPLY(self.lock_flow))
        self.sof_3_slider.SIGNAL_MINUS.connect(self.Pigment_SOF_3_Minus)
        self.sof_3_slider.SIGNAL_PLUS.connect(self.Pigment_SOF_3_Plus)
        self.sof_3_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_3_Slider_Modify)
        self.layout.sof_3_value.valueChanged.connect(self.Pigment_SOF_3_Value_Modify)

        # Channel ALPHA
        self.aaa_1_slider.SIGNAL_HALF.connect(self.Pigment_AAA_1_Half)
        self.aaa_1_slider.SIGNAL_MINUS.connect(self.Pigment_AAA_1_Minus)
        self.aaa_1_slider.SIGNAL_PLUS.connect(self.Pigment_AAA_1_Plus)
        self.aaa_1_slider.SIGNAL_VALUE.connect(self.Pigment_AAA_1_Slider_Modify)
        self.aaa_1_slider.SIGNAL_RELEASE.connect(self.Pigment_AAA_1_Slider_Release)
        self.aaa_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.aaa_1_value.valueChanged.connect(self.Pigment_AAA_1_Value_Modify)
        self.layout.aaa_1_value.editingFinished.connect(self.Pigment_AAA_1_Value_Release)

        # Channel RED
        self.rgb_1_slider.SIGNAL_HALF.connect(self.Pigment_RGB_1_Half)
        self.rgb_1_slider.SIGNAL_MINUS.connect(self.Pigment_RGB_1_Minus)
        self.rgb_1_slider.SIGNAL_PLUS.connect(self.Pigment_RGB_1_Plus)
        self.rgb_1_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_1_Slider_Modify)
        self.rgb_1_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_1_Slider_Release)
        self.rgb_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.rgb_1_value.valueChanged.connect(self.Pigment_RGB_1_Value_Modify)
        self.layout.rgb_1_value.editingFinished.connect(self.Pigment_RGB_1_Value_Release)
        # Channel GREEN
        self.rgb_2_slider.SIGNAL_HALF.connect(self.Pigment_RGB_2_Half)
        self.rgb_2_slider.SIGNAL_MINUS.connect(self.Pigment_RGB_2_Minus)
        self.rgb_2_slider.SIGNAL_PLUS.connect(self.Pigment_RGB_2_Plus)
        self.rgb_2_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_2_Slider_Modify)
        self.rgb_2_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_2_Slider_Release)
        self.rgb_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.rgb_2_value.valueChanged.connect(self.Pigment_RGB_2_Value_Modify)
        self.layout.rgb_2_value.editingFinished.connect(self.Pigment_RGB_2_Value_Release)
        # Channel BLUE
        self.rgb_3_slider.SIGNAL_HALF.connect(self.Pigment_RGB_3_Half)
        self.rgb_3_slider.SIGNAL_MINUS.connect(self.Pigment_RGB_3_Minus)
        self.rgb_3_slider.SIGNAL_PLUS.connect(self.Pigment_RGB_3_Plus)
        self.rgb_3_slider.SIGNAL_VALUE.connect(self.Pigment_RGB_3_Slider_Modify)
        self.rgb_3_slider.SIGNAL_RELEASE.connect(self.Pigment_RGB_3_Slider_Release)
        self.rgb_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.rgb_3_value.valueChanged.connect(self.Pigment_RGB_3_Value_Modify)
        self.layout.rgb_3_value.editingFinished.connect(self.Pigment_RGB_3_Value_Release)

        # Channel ANGLE
        self.ard_1_slider.SIGNAL_HALF.connect(self.Pigment_ARD_1_Half)
        self.ard_1_slider.SIGNAL_MINUS.connect(self.Pigment_ARD_1_Minus)
        self.ard_1_slider.SIGNAL_PLUS.connect(self.Pigment_ARD_1_Plus)
        self.ard_1_slider.SIGNAL_VALUE.connect(self.Pigment_ARD_1_Slider_Modify)
        self.ard_1_slider.SIGNAL_RELEASE.connect(self.Pigment_ARD_1_Slider_Release)
        self.ard_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ard_1_value.valueChanged.connect(self.Pigment_ARD_1_Value_Modify)
        self.layout.ard_1_value.editingFinished.connect(self.Pigment_ARD_1_Value_Release)
        # Channel RATIO
        self.ard_2_slider.SIGNAL_HALF.connect(self.Pigment_ARD_2_Half)
        self.ard_2_slider.SIGNAL_MINUS.connect(self.Pigment_ARD_2_Minus)
        self.ard_2_slider.SIGNAL_PLUS.connect(self.Pigment_ARD_2_Plus)
        self.ard_2_slider.SIGNAL_VALUE.connect(self.Pigment_ARD_2_Slider_Modify)
        self.ard_2_slider.SIGNAL_RELEASE.connect(self.Pigment_ARD_2_Slider_Release)
        self.ard_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ard_2_value.valueChanged.connect(self.Pigment_ARD_2_Value_Modify)
        self.layout.ard_2_value.editingFinished.connect(self.Pigment_ARD_2_Value_Release)
        # Channel DIAGONAL
        self.ard_3_slider.SIGNAL_HALF.connect(self.Pigment_ARD_3_Half)
        self.ard_3_slider.SIGNAL_MINUS.connect(self.Pigment_ARD_3_Minus)
        self.ard_3_slider.SIGNAL_PLUS.connect(self.Pigment_ARD_3_Plus)
        self.ard_3_slider.SIGNAL_VALUE.connect(self.Pigment_ARD_3_Slider_Modify)
        self.ard_3_slider.SIGNAL_RELEASE.connect(self.Pigment_ARD_3_Slider_Release)
        self.ard_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ard_3_value.valueChanged.connect(self.Pigment_ARD_3_Value_Modify)
        self.layout.ard_3_value.editingFinished.connect(self.Pigment_ARD_3_Value_Release)

        # Channel HUE
        self.hsv_1_slider.SIGNAL_HALF.connect(self.Pigment_HSV_1_Half)
        self.hsv_1_slider.SIGNAL_MINUS.connect(self.Pigment_HSV_1_Minus)
        self.hsv_1_slider.SIGNAL_PLUS.connect(self.Pigment_HSV_1_Plus)
        self.hsv_1_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_1_Slider_Modify)
        self.hsv_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_1_Slider_Release)
        self.hsv_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsv_1_value.valueChanged.connect(self.Pigment_HSV_1_Value_Modify)
        self.layout.hsv_1_value.editingFinished.connect(self.Pigment_HSV_1_Value_Release)
        # Channel SATURATION
        self.hsv_2_slider.SIGNAL_HALF.connect(self.Pigment_HSV_2_Half)
        self.hsv_2_slider.SIGNAL_MINUS.connect(self.Pigment_HSV_2_Minus)
        self.hsv_2_slider.SIGNAL_PLUS.connect(self.Pigment_HSV_2_Plus)
        self.hsv_2_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_2_Slider_Modify)
        self.hsv_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_2_Slider_Release)
        self.hsv_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsv_2_value.valueChanged.connect(self.Pigment_HSV_2_Value_Modify)
        self.layout.hsv_2_value.editingFinished.connect(self.Pigment_HSV_2_Value_Release)
        # Channel VALUE
        self.hsv_3_slider.SIGNAL_HALF.connect(self.Pigment_HSV_3_Half)
        self.hsv_3_slider.SIGNAL_MINUS.connect(self.Pigment_HSV_3_Minus)
        self.hsv_3_slider.SIGNAL_PLUS.connect(self.Pigment_HSV_3_Plus)
        self.hsv_3_slider.SIGNAL_VALUE.connect(self.Pigment_HSV_3_Slider_Modify)
        self.hsv_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HSV_3_Slider_Release)
        self.hsv_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsv_3_value.valueChanged.connect(self.Pigment_HSV_3_Value_Modify)
        self.layout.hsv_3_value.editingFinished.connect(self.Pigment_HSV_3_Value_Release)

        # Channel HUE
        self.hsl_1_slider.SIGNAL_HALF.connect(self.Pigment_HSL_1_Half)
        self.hsl_1_slider.SIGNAL_MINUS.connect(self.Pigment_HSL_1_Minus)
        self.hsl_1_slider.SIGNAL_PLUS.connect(self.Pigment_HSL_1_Plus)
        self.hsl_1_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_1_Slider_Modify)
        self.hsl_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_1_Slider_Release)
        self.hsl_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsl_1_value.valueChanged.connect(self.Pigment_HSL_1_Value_Modify)
        self.layout.hsl_1_value.editingFinished.connect(self.Pigment_HSL_1_Value_Release)
        # Channel SATURATION
        self.hsl_2_slider.SIGNAL_HALF.connect(self.Pigment_HSL_2_Half)
        self.hsl_2_slider.SIGNAL_MINUS.connect(self.Pigment_HSL_2_Minus)
        self.hsl_2_slider.SIGNAL_PLUS.connect(self.Pigment_HSL_2_Plus)
        self.hsl_2_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_2_Slider_Modify)
        self.hsl_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_2_Slider_Release)
        self.hsl_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsl_2_value.valueChanged.connect(self.Pigment_HSL_2_Value_Modify)
        self.layout.hsl_2_value.editingFinished.connect(self.Pigment_HSL_2_Value_Release)
        # Channel LIGHTNESS
        self.hsl_3_slider.SIGNAL_HALF.connect(self.Pigment_HSL_3_Half)
        self.hsl_3_slider.SIGNAL_MINUS.connect(self.Pigment_HSL_3_Minus)
        self.hsl_3_slider.SIGNAL_PLUS.connect(self.Pigment_HSL_3_Plus)
        self.hsl_3_slider.SIGNAL_VALUE.connect(self.Pigment_HSL_3_Slider_Modify)
        self.hsl_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HSL_3_Slider_Release)
        self.hsl_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hsl_3_value.valueChanged.connect(self.Pigment_HSL_3_Value_Modify)
        self.layout.hsl_3_value.editingFinished.connect(self.Pigment_HSL_3_Value_Release)

        # Channel HUE
        self.hcy_1_slider.SIGNAL_HALF.connect(self.Pigment_HCY_1_Half)
        self.hcy_1_slider.SIGNAL_MINUS.connect(self.Pigment_HCY_1_Minus)
        self.hcy_1_slider.SIGNAL_PLUS.connect(self.Pigment_HCY_1_Plus)
        self.hcy_1_slider.SIGNAL_VALUE.connect(self.Pigment_HCY_1_Slider_Modify)
        self.hcy_1_slider.SIGNAL_RELEASE.connect(self.Pigment_HCY_1_Slider_Release)
        self.hcy_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hcy_1_value.valueChanged.connect(self.Pigment_HCY_1_Value_Modify)
        self.layout.hcy_1_value.editingFinished.connect(self.Pigment_HCY_1_Value_Release)
        # Channel CHROMA
        self.hcy_2_slider.SIGNAL_HALF.connect(self.Pigment_HCY_2_Half)
        self.hcy_2_slider.SIGNAL_MINUS.connect(self.Pigment_HCY_2_Minus)
        self.hcy_2_slider.SIGNAL_PLUS.connect(self.Pigment_HCY_2_Plus)
        self.hcy_2_slider.SIGNAL_VALUE.connect(self.Pigment_HCY_2_Slider_Modify)
        self.hcy_2_slider.SIGNAL_RELEASE.connect(self.Pigment_HCY_2_Slider_Release)
        self.hcy_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hcy_2_value.valueChanged.connect(self.Pigment_HCY_2_Value_Modify)
        self.layout.hcy_2_value.editingFinished.connect(self.Pigment_HCY_2_Value_Release)
        # Channel Y (LUMA)
        self.hcy_3_slider.SIGNAL_HALF.connect(self.Pigment_HCY_3_Half)
        self.hcy_3_slider.SIGNAL_MINUS.connect(self.Pigment_HCY_3_Minus)
        self.hcy_3_slider.SIGNAL_PLUS.connect(self.Pigment_HCY_3_Plus)
        self.hcy_3_slider.SIGNAL_VALUE.connect(self.Pigment_HCY_3_Slider_Modify)
        self.hcy_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HCY_3_Slider_Release)
        self.hcy_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hcy_3_value.valueChanged.connect(self.Pigment_HCY_3_Value_Modify)
        self.layout.hcy_3_value.editingFinished.connect(self.Pigment_HCY_3_Value_Release)

        # Channel Y (LUMA)
        self.yuv_1_slider.SIGNAL_HALF.connect(self.Pigment_YUV_1_Half)
        self.yuv_1_slider.SIGNAL_MINUS.connect(self.Pigment_YUV_1_Minus)
        self.yuv_1_slider.SIGNAL_PLUS.connect(self.Pigment_YUV_1_Plus)
        self.yuv_1_slider.SIGNAL_VALUE.connect(self.Pigment_YUV_1_Slider_Modify)
        self.yuv_1_slider.SIGNAL_RELEASE.connect(self.Pigment_YUV_1_Slider_Release)
        self.yuv_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.yuv_1_value.valueChanged.connect(self.Pigment_YUV_1_Value_Modify)
        self.layout.yuv_1_value.editingFinished.connect(self.Pigment_YUV_1_Value_Release)
        # Channel U (BLUE Projection)
        self.yuv_2_slider.SIGNAL_HALF.connect(self.Pigment_YUV_2_Half)
        self.yuv_2_slider.SIGNAL_MINUS.connect(self.Pigment_YUV_2_Minus)
        self.yuv_2_slider.SIGNAL_PLUS.connect(self.Pigment_YUV_2_Plus)
        self.yuv_2_slider.SIGNAL_VALUE.connect(self.Pigment_YUV_2_Slider_Modify)
        self.yuv_2_slider.SIGNAL_RELEASE.connect(self.Pigment_YUV_2_Slider_Release)
        self.yuv_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.yuv_2_value.valueChanged.connect(self.Pigment_YUV_2_Value_Modify)
        self.layout.yuv_2_value.editingFinished.connect(self.Pigment_YUV_2_Value_Release)
        # Channel V (RED Projection)
        self.yuv_3_slider.SIGNAL_HALF.connect(self.Pigment_YUV_3_Half)
        self.yuv_3_slider.SIGNAL_MINUS.connect(self.Pigment_YUV_3_Minus)
        self.yuv_3_slider.SIGNAL_PLUS.connect(self.Pigment_YUV_3_Plus)
        self.yuv_3_slider.SIGNAL_VALUE.connect(self.Pigment_YUV_3_Slider_Modify)
        self.yuv_3_slider.SIGNAL_RELEASE.connect(self.Pigment_YUV_3_Slider_Release)
        self.yuv_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.yuv_3_value.valueChanged.connect(self.Pigment_YUV_3_Value_Modify)
        self.layout.yuv_3_value.editingFinished.connect(self.Pigment_YUV_3_Value_Release)

        # Channel RED
        self.ryb_1_slider.SIGNAL_HALF.connect(self.Pigment_RYB_1_Half)
        self.ryb_1_slider.SIGNAL_MINUS.connect(self.Pigment_RYB_1_Minus)
        self.ryb_1_slider.SIGNAL_PLUS.connect(self.Pigment_RYB_1_Plus)
        self.ryb_1_slider.SIGNAL_VALUE.connect(self.Pigment_RYB_1_Slider_Modify)
        self.ryb_1_slider.SIGNAL_RELEASE.connect(self.Pigment_RYB_1_Slider_Release)
        self.ryb_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ryb_1_value.valueChanged.connect(self.Pigment_RYB_1_Value_Modify)
        self.layout.ryb_1_value.editingFinished.connect(self.Pigment_RYB_1_Value_Release)
        # Channel YELLOW
        self.ryb_2_slider.SIGNAL_HALF.connect(self.Pigment_RYB_2_Half)
        self.ryb_2_slider.SIGNAL_MINUS.connect(self.Pigment_RYB_2_Minus)
        self.ryb_2_slider.SIGNAL_PLUS.connect(self.Pigment_RYB_2_Plus)
        self.ryb_2_slider.SIGNAL_VALUE.connect(self.Pigment_RYB_2_Slider_Modify)
        self.ryb_2_slider.SIGNAL_RELEASE.connect(self.Pigment_RYB_2_Slider_Release)
        self.ryb_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ryb_2_value.valueChanged.connect(self.Pigment_RYB_2_Value_Modify)
        self.layout.ryb_2_value.editingFinished.connect(self.Pigment_RYB_2_Value_Release)
        # Channel BLUE
        self.ryb_3_slider.SIGNAL_HALF.connect(self.Pigment_RYB_3_Half)
        self.ryb_3_slider.SIGNAL_MINUS.connect(self.Pigment_RYB_3_Minus)
        self.ryb_3_slider.SIGNAL_PLUS.connect(self.Pigment_RYB_3_Plus)
        self.ryb_3_slider.SIGNAL_VALUE.connect(self.Pigment_RYB_3_Slider_Modify)
        self.ryb_3_slider.SIGNAL_RELEASE.connect(self.Pigment_RYB_3_Slider_Release)
        self.ryb_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.ryb_3_value.valueChanged.connect(self.Pigment_RYB_3_Value_Modify)
        self.layout.ryb_3_value.editingFinished.connect(self.Pigment_RYB_3_Value_Release)

        # Channel CYAN
        self.cmy_1_slider.SIGNAL_HALF.connect(self.Pigment_CMY_1_Half)
        self.cmy_1_slider.SIGNAL_MINUS.connect(self.Pigment_CMY_1_Minus)
        self.cmy_1_slider.SIGNAL_PLUS.connect(self.Pigment_CMY_1_Plus)
        self.cmy_1_slider.SIGNAL_VALUE.connect(self.Pigment_CMY_1_Slider_Modify)
        self.cmy_1_slider.SIGNAL_RELEASE.connect(self.Pigment_CMY_1_Slider_Release)
        self.cmy_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmy_1_value.valueChanged.connect(self.Pigment_CMY_1_Value_Modify)
        self.layout.cmy_1_value.editingFinished.connect(self.Pigment_CMY_1_Value_Release)
        # Channel MAGENTA
        self.cmy_2_slider.SIGNAL_HALF.connect(self.Pigment_CMY_2_Half)
        self.cmy_2_slider.SIGNAL_MINUS.connect(self.Pigment_CMY_2_Minus)
        self.cmy_2_slider.SIGNAL_PLUS.connect(self.Pigment_CMY_2_Plus)
        self.cmy_2_slider.SIGNAL_VALUE.connect(self.Pigment_CMY_2_Slider_Modify)
        self.cmy_2_slider.SIGNAL_RELEASE.connect(self.Pigment_CMY_2_Slider_Release)
        self.cmy_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmy_2_value.valueChanged.connect(self.Pigment_CMY_2_Value_Modify)
        self.layout.cmy_2_value.editingFinished.connect(self.Pigment_CMY_2_Value_Release)
        # Channel YELLOW
        self.cmy_3_slider.SIGNAL_HALF.connect(self.Pigment_CMY_3_Half)
        self.cmy_3_slider.SIGNAL_MINUS.connect(self.Pigment_CMY_3_Minus)
        self.cmy_3_slider.SIGNAL_PLUS.connect(self.Pigment_CMY_3_Plus)
        self.cmy_3_slider.SIGNAL_VALUE.connect(self.Pigment_CMY_3_Slider_Modify)
        self.cmy_3_slider.SIGNAL_RELEASE.connect(self.Pigment_CMY_3_Slider_Release)
        self.cmy_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmy_3_value.valueChanged.connect(self.Pigment_CMY_3_Value_Modify)
        self.layout.cmy_3_value.editingFinished.connect(self.Pigment_CMY_3_Value_Release)

        # Channel CYAN
        self.cmyk_1_slider.SIGNAL_HALF.connect(self.Pigment_CMYK_1_Half)
        self.cmyk_1_slider.SIGNAL_MINUS.connect(self.Pigment_CMYK_1_Minus)
        self.cmyk_1_slider.SIGNAL_PLUS.connect(self.Pigment_CMYK_1_Plus)
        self.cmyk_1_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_1_Slider_Modify)
        self.cmyk_1_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_1_Slider_Release)
        self.cmyk_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_1_value.valueChanged.connect(self.Pigment_CMYK_1_Value_Modify)
        self.layout.cmyk_1_value.editingFinished.connect(self.Pigment_CMYK_1_Value_Release)
        # Channel MAGENTA
        self.cmyk_2_slider.SIGNAL_HALF.connect(self.Pigment_CMYK_2_Half)
        self.cmyk_2_slider.SIGNAL_MINUS.connect(self.Pigment_CMYK_2_Minus)
        self.cmyk_2_slider.SIGNAL_PLUS.connect(self.Pigment_CMYK_2_Plus)
        self.cmyk_2_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_2_Slider_Modify)
        self.cmyk_2_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_2_Slider_Release)
        self.cmyk_2_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_2_value.valueChanged.connect(self.Pigment_CMYK_2_Value_Modify)
        self.layout.cmyk_2_value.editingFinished.connect(self.Pigment_CMYK_2_Value_Release)
        # Channel YELLOW
        self.cmyk_3_slider.SIGNAL_HALF.connect(self.Pigment_CMYK_3_Half)
        self.cmyk_3_slider.SIGNAL_MINUS.connect(self.Pigment_CMYK_3_Minus)
        self.cmyk_3_slider.SIGNAL_PLUS.connect(self.Pigment_CMYK_3_Plus)
        self.cmyk_3_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_3_Slider_Modify)
        self.cmyk_3_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_3_Slider_Release)
        self.cmyk_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_3_value.valueChanged.connect(self.Pigment_CMYK_3_Value_Modify)
        self.layout.cmyk_3_value.editingFinished.connect(self.Pigment_CMYK_3_Value_Release)
        # Channel KEY
        self.cmyk_4_slider.SIGNAL_HALF.connect(self.Pigment_CMYK_4_Half)
        self.cmyk_4_slider.SIGNAL_MINUS.connect(self.Pigment_CMYK_4_Minus)
        self.cmyk_4_slider.SIGNAL_PLUS.connect(self.Pigment_CMYK_4_Plus)
        self.cmyk_4_slider.SIGNAL_VALUE.connect(self.Pigment_CMYK_4_Slider_Modify)
        self.cmyk_4_slider.SIGNAL_RELEASE.connect(self.Pigment_CMYK_4_Slider_Release)
        self.cmyk_4_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.cmyk_4_value.valueChanged.connect(self.Pigment_CMYK_4_Value_Modify)
        self.layout.cmyk_4_value.editingFinished.connect(self.Pigment_CMYK_4_Value_Release)
        self.layout.cmyk_4_lock.clicked.connect(self.Pigment_CMYK_4_Lock)

        # Channel KELVIN
        self.kkk_1_slider.SIGNAL_HALF.connect(self.Pigment_KKK_1_Half)
        self.kkk_1_slider.SIGNAL_MINUS.connect(self.Pigment_KKK_1_Minus)
        self.kkk_1_slider.SIGNAL_PLUS.connect(self.Pigment_KKK_1_Plus)
        self.kkk_1_slider.SIGNAL_VALUE.connect(self.Pigment_KKK_1_Slider_Modify)
        self.kkk_1_slider.SIGNAL_RELEASE.connect(self.Pigment_KKK_1_Slider_Release)
        self.kkk_1_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.kkk_1_value.valueChanged.connect(self.Pigment_KKK_1_Value_Modify)
        self.layout.kkk_1_value.editingFinished.connect(self.Pigment_KKK_1_Value_Release)
        self.layout.kkk_1_lock.clicked.connect(self.Pigment_KKK_1_Lock)

        # Hex Input
        self.layout.hex_string.returnPressed.connect(self.HEX_Code)
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
        self.palette_cor_00.SIGNAL_APPLY.connect(self.Cor_00_APPLY)
        self.palette_cor_01.SIGNAL_APPLY.connect(self.Cor_01_APPLY)
        self.palette_cor_02.SIGNAL_APPLY.connect(self.Cor_02_APPLY)
        self.palette_cor_03.SIGNAL_APPLY.connect(self.Cor_03_APPLY)
        self.palette_cor_04.SIGNAL_APPLY.connect(self.Cor_04_APPLY)
        self.palette_cor_05.SIGNAL_APPLY.connect(self.Cor_05_APPLY)
        self.palette_cor_06.SIGNAL_APPLY.connect(self.Cor_06_APPLY)
        self.palette_cor_07.SIGNAL_APPLY.connect(self.Cor_07_APPLY)
        self.palette_cor_08.SIGNAL_APPLY.connect(self.Cor_08_APPLY)
        self.palette_cor_09.SIGNAL_APPLY.connect(self.Cor_09_APPLY)
        self.palette_cor_10.SIGNAL_APPLY.connect(self.Cor_10_APPLY)
        self.palette_cor_00.SIGNAL_SAVE.connect(self.Cor_00_SAVE)
        self.palette_cor_01.SIGNAL_SAVE.connect(self.Cor_01_SAVE)
        self.palette_cor_02.SIGNAL_SAVE.connect(self.Cor_02_SAVE)
        self.palette_cor_03.SIGNAL_SAVE.connect(self.Cor_03_SAVE)
        self.palette_cor_04.SIGNAL_SAVE.connect(self.Cor_04_SAVE)
        self.palette_cor_05.SIGNAL_SAVE.connect(self.Cor_05_SAVE)
        self.palette_cor_06.SIGNAL_SAVE.connect(self.Cor_06_SAVE)
        self.palette_cor_07.SIGNAL_SAVE.connect(self.Cor_07_SAVE)
        self.palette_cor_08.SIGNAL_SAVE.connect(self.Cor_08_SAVE)
        self.palette_cor_09.SIGNAL_SAVE.connect(self.Cor_09_SAVE)
        self.palette_cor_10.SIGNAL_SAVE.connect(self.Cor_10_SAVE)
        self.palette_cor_00.SIGNAL_CLEAN.connect(self.Cor_00_CLEAN)
        self.palette_cor_01.SIGNAL_CLEAN.connect(self.Cor_01_CLEAN)
        self.palette_cor_02.SIGNAL_CLEAN.connect(self.Cor_02_CLEAN)
        self.palette_cor_03.SIGNAL_CLEAN.connect(self.Cor_03_CLEAN)
        self.palette_cor_04.SIGNAL_CLEAN.connect(self.Cor_04_CLEAN)
        self.palette_cor_05.SIGNAL_CLEAN.connect(self.Cor_05_CLEAN)
        self.palette_cor_06.SIGNAL_CLEAN.connect(self.Cor_06_CLEAN)
        self.palette_cor_07.SIGNAL_CLEAN.connect(self.Cor_07_CLEAN)
        self.palette_cor_08.SIGNAL_CLEAN.connect(self.Cor_08_CLEAN)
        self.palette_cor_09.SIGNAL_CLEAN.connect(self.Cor_09_CLEAN)
        self.palette_cor_10.SIGNAL_CLEAN.connect(self.Cor_10_CLEAN)
    def Mixers(self):
        #\\ Module Mixer Colors ################################################
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
        self.mixer_hcy_l1 = Clicks(self.layout.hcy_l1)
        self.mixer_hcy_l2 = Clicks(self.layout.hcy_l2)
        self.mixer_hcy_l3 = Clicks(self.layout.hcy_l3)
        self.mixer_hcy_r1 = Clicks(self.layout.hcy_r1)
        self.mixer_hcy_r2 = Clicks(self.layout.hcy_r2)
        self.mixer_hcy_r3 = Clicks(self.layout.hcy_r3)
        self.mixer_yuv_l1 = Clicks(self.layout.yuv_l1)
        self.mixer_yuv_l2 = Clicks(self.layout.yuv_l2)
        self.mixer_yuv_l3 = Clicks(self.layout.yuv_l3)
        self.mixer_yuv_r1 = Clicks(self.layout.yuv_r1)
        self.mixer_yuv_r2 = Clicks(self.layout.yuv_r2)
        self.mixer_yuv_r3 = Clicks(self.layout.yuv_r3)
        self.mixer_ryb_l1 = Clicks(self.layout.ryb_l1)
        self.mixer_ryb_l2 = Clicks(self.layout.ryb_l2)
        self.mixer_ryb_l3 = Clicks(self.layout.ryb_l3)
        self.mixer_ryb_r1 = Clicks(self.layout.ryb_r1)
        self.mixer_ryb_r2 = Clicks(self.layout.ryb_r2)
        self.mixer_ryb_r3 = Clicks(self.layout.ryb_r3)
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
        self.mixer_rgb_r1.SIGNAL_APPLY.connect(self.Mixer_RGB_R1_APPLY)
        self.mixer_rgb_l2.SIGNAL_APPLY.connect(self.Mixer_RGB_L2_APPLY)
        self.mixer_rgb_r2.SIGNAL_APPLY.connect(self.Mixer_RGB_R2_APPLY)
        self.mixer_rgb_l3.SIGNAL_APPLY.connect(self.Mixer_RGB_L3_APPLY)
        self.mixer_rgb_r3.SIGNAL_APPLY.connect(self.Mixer_RGB_R3_APPLY)
        self.mixer_rgb_l1.SIGNAL_SAVE.connect(self.Mixer_RGB_L1_SAVE)
        self.mixer_rgb_r1.SIGNAL_SAVE.connect(self.Mixer_RGB_R1_SAVE)
        self.mixer_rgb_l2.SIGNAL_SAVE.connect(self.Mixer_RGB_L2_SAVE)
        self.mixer_rgb_r2.SIGNAL_SAVE.connect(self.Mixer_RGB_R2_SAVE)
        self.mixer_rgb_l3.SIGNAL_SAVE.connect(self.Mixer_RGB_L3_SAVE)
        self.mixer_rgb_r3.SIGNAL_SAVE.connect(self.Mixer_RGB_R3_SAVE)
        self.mixer_rgb_l1.SIGNAL_CLEAN.connect(self.Mixer_RGB_L1_CLEAN)
        self.mixer_rgb_r1.SIGNAL_CLEAN.connect(self.Mixer_RGB_R1_CLEAN)
        self.mixer_rgb_l2.SIGNAL_CLEAN.connect(self.Mixer_RGB_L2_CLEAN)
        self.mixer_rgb_r2.SIGNAL_CLEAN.connect(self.Mixer_RGB_R2_CLEAN)
        self.mixer_rgb_l3.SIGNAL_CLEAN.connect(self.Mixer_RGB_L3_CLEAN)
        self.mixer_rgb_r3.SIGNAL_CLEAN.connect(self.Mixer_RGB_R3_CLEAN)
        # ARD connection
        self.mixer_ard_l1.SIGNAL_APPLY.connect(self.Mixer_ARD_L1_APPLY)
        self.mixer_ard_r1.SIGNAL_APPLY.connect(self.Mixer_ARD_R1_APPLY)
        self.mixer_ard_l2.SIGNAL_APPLY.connect(self.Mixer_ARD_L2_APPLY)
        self.mixer_ard_r2.SIGNAL_APPLY.connect(self.Mixer_ARD_R2_APPLY)
        self.mixer_ard_l3.SIGNAL_APPLY.connect(self.Mixer_ARD_L3_APPLY)
        self.mixer_ard_r3.SIGNAL_APPLY.connect(self.Mixer_ARD_R3_APPLY)
        self.mixer_ard_l1.SIGNAL_SAVE.connect(self.Mixer_ARD_L1_SAVE)
        self.mixer_ard_r1.SIGNAL_SAVE.connect(self.Mixer_ARD_R1_SAVE)
        self.mixer_ard_l2.SIGNAL_SAVE.connect(self.Mixer_ARD_L2_SAVE)
        self.mixer_ard_r2.SIGNAL_SAVE.connect(self.Mixer_ARD_R2_SAVE)
        self.mixer_ard_l3.SIGNAL_SAVE.connect(self.Mixer_ARD_L3_SAVE)
        self.mixer_ard_r3.SIGNAL_SAVE.connect(self.Mixer_ARD_R3_SAVE)
        self.mixer_ard_l1.SIGNAL_CLEAN.connect(self.Mixer_ARD_L1_CLEAN)
        self.mixer_ard_r1.SIGNAL_CLEAN.connect(self.Mixer_ARD_R1_CLEAN)
        self.mixer_ard_l2.SIGNAL_CLEAN.connect(self.Mixer_ARD_L2_CLEAN)
        self.mixer_ard_r2.SIGNAL_CLEAN.connect(self.Mixer_ARD_R2_CLEAN)
        self.mixer_ard_l3.SIGNAL_CLEAN.connect(self.Mixer_ARD_L3_CLEAN)
        self.mixer_ard_r3.SIGNAL_CLEAN.connect(self.Mixer_ARD_R3_CLEAN)
        # HSV connection
        self.mixer_hsv_l1.SIGNAL_APPLY.connect(self.Mixer_HSV_L1_APPLY)
        self.mixer_hsv_r1.SIGNAL_APPLY.connect(self.Mixer_HSV_R1_APPLY)
        self.mixer_hsv_l2.SIGNAL_APPLY.connect(self.Mixer_HSV_L2_APPLY)
        self.mixer_hsv_r2.SIGNAL_APPLY.connect(self.Mixer_HSV_R2_APPLY)
        self.mixer_hsv_l3.SIGNAL_APPLY.connect(self.Mixer_HSV_L3_APPLY)
        self.mixer_hsv_r3.SIGNAL_APPLY.connect(self.Mixer_HSV_R3_APPLY)
        self.mixer_hsv_l1.SIGNAL_SAVE.connect(self.Mixer_HSV_L1_SAVE)
        self.mixer_hsv_r1.SIGNAL_SAVE.connect(self.Mixer_HSV_R1_SAVE)
        self.mixer_hsv_l2.SIGNAL_SAVE.connect(self.Mixer_HSV_L2_SAVE)
        self.mixer_hsv_r2.SIGNAL_SAVE.connect(self.Mixer_HSV_R2_SAVE)
        self.mixer_hsv_l3.SIGNAL_SAVE.connect(self.Mixer_HSV_L3_SAVE)
        self.mixer_hsv_r3.SIGNAL_SAVE.connect(self.Mixer_HSV_R3_SAVE)
        self.mixer_hsv_l1.SIGNAL_CLEAN.connect(self.Mixer_HSV_L1_CLEAN)
        self.mixer_hsv_r1.SIGNAL_CLEAN.connect(self.Mixer_HSV_R1_CLEAN)
        self.mixer_hsv_l2.SIGNAL_CLEAN.connect(self.Mixer_HSV_L2_CLEAN)
        self.mixer_hsv_r2.SIGNAL_CLEAN.connect(self.Mixer_HSV_R2_CLEAN)
        self.mixer_hsv_l3.SIGNAL_CLEAN.connect(self.Mixer_HSV_L3_CLEAN)
        self.mixer_hsv_r3.SIGNAL_CLEAN.connect(self.Mixer_HSV_R3_CLEAN)
        # HSL connection
        self.mixer_hsl_l1.SIGNAL_APPLY.connect(self.Mixer_HSL_L1_APPLY)
        self.mixer_hsl_r1.SIGNAL_APPLY.connect(self.Mixer_HSL_R1_APPLY)
        self.mixer_hsl_l2.SIGNAL_APPLY.connect(self.Mixer_HSL_L2_APPLY)
        self.mixer_hsl_r2.SIGNAL_APPLY.connect(self.Mixer_HSL_R2_APPLY)
        self.mixer_hsl_l3.SIGNAL_APPLY.connect(self.Mixer_HSL_L3_APPLY)
        self.mixer_hsl_r3.SIGNAL_APPLY.connect(self.Mixer_HSL_R3_APPLY)
        self.mixer_hsl_l1.SIGNAL_SAVE.connect(self.Mixer_HSL_L1_SAVE)
        self.mixer_hsl_r1.SIGNAL_SAVE.connect(self.Mixer_HSL_R1_SAVE)
        self.mixer_hsl_l2.SIGNAL_SAVE.connect(self.Mixer_HSL_L2_SAVE)
        self.mixer_hsl_r2.SIGNAL_SAVE.connect(self.Mixer_HSL_R2_SAVE)
        self.mixer_hsl_l3.SIGNAL_SAVE.connect(self.Mixer_HSL_L3_SAVE)
        self.mixer_hsl_r3.SIGNAL_SAVE.connect(self.Mixer_HSL_R3_SAVE)
        self.mixer_hsl_l1.SIGNAL_CLEAN.connect(self.Mixer_HSL_L1_CLEAN)
        self.mixer_hsl_r1.SIGNAL_CLEAN.connect(self.Mixer_HSL_R1_CLEAN)
        self.mixer_hsl_l2.SIGNAL_CLEAN.connect(self.Mixer_HSL_L2_CLEAN)
        self.mixer_hsl_r2.SIGNAL_CLEAN.connect(self.Mixer_HSL_R2_CLEAN)
        self.mixer_hsl_l3.SIGNAL_CLEAN.connect(self.Mixer_HSL_L3_CLEAN)
        self.mixer_hsl_r3.SIGNAL_CLEAN.connect(self.Mixer_HSL_R3_CLEAN)
        # HCY connection
        self.mixer_hcy_l1.SIGNAL_APPLY.connect(self.Mixer_HCY_L1_APPLY)
        self.mixer_hcy_r1.SIGNAL_APPLY.connect(self.Mixer_HCY_R1_APPLY)
        self.mixer_hcy_l2.SIGNAL_APPLY.connect(self.Mixer_HCY_L2_APPLY)
        self.mixer_hcy_r2.SIGNAL_APPLY.connect(self.Mixer_HCY_R2_APPLY)
        self.mixer_hcy_l3.SIGNAL_APPLY.connect(self.Mixer_HCY_L3_APPLY)
        self.mixer_hcy_r3.SIGNAL_APPLY.connect(self.Mixer_HCY_R3_APPLY)
        self.mixer_hcy_l1.SIGNAL_SAVE.connect(self.Mixer_HCY_L1_SAVE)
        self.mixer_hcy_r1.SIGNAL_SAVE.connect(self.Mixer_HCY_R1_SAVE)
        self.mixer_hcy_l2.SIGNAL_SAVE.connect(self.Mixer_HCY_L2_SAVE)
        self.mixer_hcy_r2.SIGNAL_SAVE.connect(self.Mixer_HCY_R2_SAVE)
        self.mixer_hcy_l3.SIGNAL_SAVE.connect(self.Mixer_HCY_L3_SAVE)
        self.mixer_hcy_r3.SIGNAL_SAVE.connect(self.Mixer_HCY_R3_SAVE)
        self.mixer_hcy_l1.SIGNAL_CLEAN.connect(self.Mixer_HCY_L1_CLEAN)
        self.mixer_hcy_r1.SIGNAL_CLEAN.connect(self.Mixer_HCY_R1_CLEAN)
        self.mixer_hcy_l2.SIGNAL_CLEAN.connect(self.Mixer_HCY_L2_CLEAN)
        self.mixer_hcy_r2.SIGNAL_CLEAN.connect(self.Mixer_HCY_R2_CLEAN)
        self.mixer_hcy_l3.SIGNAL_CLEAN.connect(self.Mixer_HCY_L3_CLEAN)
        self.mixer_hcy_r3.SIGNAL_CLEAN.connect(self.Mixer_HCY_R3_CLEAN)
        # YUV connection
        self.mixer_yuv_l1.SIGNAL_APPLY.connect(self.Mixer_YUV_L1_APPLY)
        self.mixer_yuv_r1.SIGNAL_APPLY.connect(self.Mixer_YUV_R1_APPLY)
        self.mixer_yuv_l2.SIGNAL_APPLY.connect(self.Mixer_YUV_L2_APPLY)
        self.mixer_yuv_r2.SIGNAL_APPLY.connect(self.Mixer_YUV_R2_APPLY)
        self.mixer_yuv_l3.SIGNAL_APPLY.connect(self.Mixer_YUV_L3_APPLY)
        self.mixer_yuv_r3.SIGNAL_APPLY.connect(self.Mixer_YUV_R3_APPLY)
        self.mixer_yuv_l1.SIGNAL_SAVE.connect(self.Mixer_YUV_L1_SAVE)
        self.mixer_yuv_r1.SIGNAL_SAVE.connect(self.Mixer_YUV_R1_SAVE)
        self.mixer_yuv_l2.SIGNAL_SAVE.connect(self.Mixer_YUV_L2_SAVE)
        self.mixer_yuv_r2.SIGNAL_SAVE.connect(self.Mixer_YUV_R2_SAVE)
        self.mixer_yuv_l3.SIGNAL_SAVE.connect(self.Mixer_YUV_L3_SAVE)
        self.mixer_yuv_r3.SIGNAL_SAVE.connect(self.Mixer_YUV_R3_SAVE)
        self.mixer_yuv_l1.SIGNAL_CLEAN.connect(self.Mixer_YUV_L1_CLEAN)
        self.mixer_yuv_r1.SIGNAL_CLEAN.connect(self.Mixer_YUV_R1_CLEAN)
        self.mixer_yuv_l2.SIGNAL_CLEAN.connect(self.Mixer_YUV_L2_CLEAN)
        self.mixer_yuv_r2.SIGNAL_CLEAN.connect(self.Mixer_YUV_R2_CLEAN)
        self.mixer_yuv_l3.SIGNAL_CLEAN.connect(self.Mixer_YUV_L3_CLEAN)
        self.mixer_yuv_r3.SIGNAL_CLEAN.connect(self.Mixer_YUV_R3_CLEAN)
        # RYB connection
        self.mixer_ryb_l1.SIGNAL_APPLY.connect(self.Mixer_RYB_L1_APPLY)
        self.mixer_ryb_r1.SIGNAL_APPLY.connect(self.Mixer_RYB_R1_APPLY)
        self.mixer_ryb_l2.SIGNAL_APPLY.connect(self.Mixer_RYB_L2_APPLY)
        self.mixer_ryb_r2.SIGNAL_APPLY.connect(self.Mixer_RYB_R2_APPLY)
        self.mixer_ryb_l3.SIGNAL_APPLY.connect(self.Mixer_RYB_L3_APPLY)
        self.mixer_ryb_r3.SIGNAL_APPLY.connect(self.Mixer_RYB_R3_APPLY)
        self.mixer_ryb_l1.SIGNAL_SAVE.connect(self.Mixer_RYB_L1_SAVE)
        self.mixer_ryb_r1.SIGNAL_SAVE.connect(self.Mixer_RYB_R1_SAVE)
        self.mixer_ryb_l2.SIGNAL_SAVE.connect(self.Mixer_RYB_L2_SAVE)
        self.mixer_ryb_r2.SIGNAL_SAVE.connect(self.Mixer_RYB_R2_SAVE)
        self.mixer_ryb_l3.SIGNAL_SAVE.connect(self.Mixer_RYB_L3_SAVE)
        self.mixer_ryb_r3.SIGNAL_SAVE.connect(self.Mixer_RYB_R3_SAVE)
        self.mixer_ryb_l1.SIGNAL_CLEAN.connect(self.Mixer_RYB_L1_CLEAN)
        self.mixer_ryb_r1.SIGNAL_CLEAN.connect(self.Mixer_RYB_R1_CLEAN)
        self.mixer_ryb_l2.SIGNAL_CLEAN.connect(self.Mixer_RYB_L2_CLEAN)
        self.mixer_ryb_r2.SIGNAL_CLEAN.connect(self.Mixer_RYB_R2_CLEAN)
        self.mixer_ryb_l3.SIGNAL_CLEAN.connect(self.Mixer_RYB_L3_CLEAN)
        self.mixer_ryb_r3.SIGNAL_CLEAN.connect(self.Mixer_RYB_R3_CLEAN)
        # CMYK connection
        self.mixer_cmyk_l1.SIGNAL_APPLY.connect(self.Mixer_CMYK_L1_APPLY)
        self.mixer_cmyk_r1.SIGNAL_APPLY.connect(self.Mixer_CMYK_R1_APPLY)
        self.mixer_cmyk_l2.SIGNAL_APPLY.connect(self.Mixer_CMYK_L2_APPLY)
        self.mixer_cmyk_r2.SIGNAL_APPLY.connect(self.Mixer_CMYK_R2_APPLY)
        self.mixer_cmyk_l3.SIGNAL_APPLY.connect(self.Mixer_CMYK_L3_APPLY)
        self.mixer_cmyk_r3.SIGNAL_APPLY.connect(self.Mixer_CMYK_R3_APPLY)
        self.mixer_cmyk_l1.SIGNAL_SAVE.connect(self.Mixer_CMYK_L1_SAVE)
        self.mixer_cmyk_r1.SIGNAL_SAVE.connect(self.Mixer_CMYK_R1_SAVE)
        self.mixer_cmyk_l2.SIGNAL_SAVE.connect(self.Mixer_CMYK_L2_SAVE)
        self.mixer_cmyk_r2.SIGNAL_SAVE.connect(self.Mixer_CMYK_R2_SAVE)
        self.mixer_cmyk_l3.SIGNAL_SAVE.connect(self.Mixer_CMYK_L3_SAVE)
        self.mixer_cmyk_r3.SIGNAL_SAVE.connect(self.Mixer_CMYK_R3_SAVE)
        self.mixer_cmyk_l1.SIGNAL_CLEAN.connect(self.Mixer_CMYK_L1_CLEAN)
        self.mixer_cmyk_r1.SIGNAL_CLEAN.connect(self.Mixer_CMYK_R1_CLEAN)
        self.mixer_cmyk_l2.SIGNAL_CLEAN.connect(self.Mixer_CMYK_L2_CLEAN)
        self.mixer_cmyk_r2.SIGNAL_CLEAN.connect(self.Mixer_CMYK_R2_CLEAN)
        self.mixer_cmyk_l3.SIGNAL_CLEAN.connect(self.Mixer_CMYK_L3_CLEAN)
        self.mixer_cmyk_r3.SIGNAL_CLEAN.connect(self.Mixer_CMYK_R3_CLEAN)

        #//
        #\\ Module Mixer Gradients #############################################
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
        self.mixer_hcy_g1 = Mixer_Gradient(self.layout.hcy_g1)
        self.mixer_hcy_g2 = Mixer_Gradient(self.layout.hcy_g2)
        self.mixer_hcy_g3 = Mixer_Gradient(self.layout.hcy_g3)
        self.mixer_yuv_g1 = Mixer_Gradient(self.layout.yuv_g1)
        self.mixer_yuv_g2 = Mixer_Gradient(self.layout.yuv_g2)
        self.mixer_yuv_g3 = Mixer_Gradient(self.layout.yuv_g3)
        self.mixer_ryb_g1 = Mixer_Gradient(self.layout.ryb_g1)
        self.mixer_ryb_g2 = Mixer_Gradient(self.layout.ryb_g2)
        self.mixer_ryb_g3 = Mixer_Gradient(self.layout.ryb_g3)
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
        self.mixer_hcy_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_HCY_G1)
        self.mixer_hcy_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_HCY_G2)
        self.mixer_hcy_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_HCY_G3)
        self.mixer_yuv_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_YUV_G1)
        self.mixer_yuv_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_YUV_G2)
        self.mixer_yuv_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_YUV_G3)
        self.mixer_ryb_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_RYB_G1)
        self.mixer_ryb_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_RYB_G2)
        self.mixer_ryb_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_RYB_G3)
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
        self.mixer_hcy_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hcy_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_hcy_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_yuv_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_yuv_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_yuv_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_ryb_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_ryb_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_ryb_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)

        #//
    def Style_Widget(self):
        # UI Percentage Gradients Display
        p4 = self.Percentage("4")
        p6 = self.Percentage("6")
        ten = self.Percentage("TEN")
        thirds = self.Percentage("3S")
        # Channels
        self.layout.percentage_top.setStyleSheet(ten)
        self.layout.percentage_bot.setStyleSheet(ten)
        self.layout.label_percent.setStyleSheet(bg_unseen)
        self.layout.eraser.setStyleSheet(bg_alpha)
        self.layout.sof_1_tick.setStyleSheet(bg_unseen)
        self.layout.sof_2_tick.setStyleSheet(bg_unseen)
        self.layout.sof_3_tick.setStyleSheet(bg_unseen)
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
        self.layout.hcy_1_tick.setStyleSheet(p6)
        self.layout.hcy_2_tick.setStyleSheet(p4)
        self.layout.hcy_3_tick.setStyleSheet(p4)
        self.layout.yuv_1_tick.setStyleSheet(p4)
        self.layout.yuv_2_tick.setStyleSheet(p4)
        self.layout.yuv_3_tick.setStyleSheet(p4)
        self.layout.ryb_1_tick.setStyleSheet(p4)
        self.layout.ryb_2_tick.setStyleSheet(p4)
        self.layout.ryb_3_tick.setStyleSheet(p4)
        self.layout.cmy_1_tick.setStyleSheet(p4)
        self.layout.cmy_2_tick.setStyleSheet(p4)
        self.layout.cmy_3_tick.setStyleSheet(p4)
        self.layout.cmyk_1_tick.setStyleSheet(p4)
        self.layout.cmyk_2_tick.setStyleSheet(p4)
        self.layout.cmyk_3_tick.setStyleSheet(p4)
        self.layout.cmyk_4_tick.setStyleSheet(p4)
        self.layout.kkk_1_tick.setStyleSheet(p4)
        # Panels
        self.layout.panel_uvd.setStyleSheet(bg_alpha)
        self.layout.panel_ard.setStyleSheet(thirds)
        self.layout.panel_hue.setStyleSheet(bg_alpha)
        self.layout.panel_hue_box.setStyleSheet(bg_unseen)
        self.layout.panel_gam.setStyleSheet(bg_alpha)
        self.layout.panel_gam_box.setStyleSheet(bg_unseen)
        self.layout.panel_dot_mix.setStyleSheet(bg_alpha)
        self.layout.dot_1.setStyleSheet(bg_alpha)
        self.layout.dot_2.setStyleSheet(bg_alpha)
        self.layout.dot_3.setStyleSheet(bg_alpha)
        self.layout.dot_4.setStyleSheet(bg_alpha)
        # Extras
        self.layout.tip_00.setStyleSheet(bg_alpha)

        # Icons Module
        self.icon_left = self.Icon_Left(self.gray_contrast)
        self.icon_right = self.Icon_Right(self.gray_contrast)
        self.icon_panel = self.Icon_Panel(self.gray_contrast)
        self.icon_corner = self.Icon_Corner(self.gray_contrast)
        self.icon_lock = self.Icon_Lock(self.gray_contrast)
        self.icon_menu = self.Icon_Menu(self.gray_contrast)
        self.icon_slider = self.Icon_Slider(self.gray_contrast)
        self.icon_tip = self.Icon_Tip(self.gray_contrast)
        self.icon_key = self.Icon_Key(self.gray_contrast)

        # Icon SVG Operation
        self.svg_lock_cmyk_4 = QtSvg.QSvgWidget(self.layout.cmyk_4_lock)
        self.svg_lock_cmyk_4.load(self.icon_lock)
        self.svg_lock_kkk_1 = QtSvg.QSvgWidget(self.layout.kkk_1_lock)
        self.svg_lock_kkk_1.load(self.icon_lock)
    def Actions(self):
        # Actions to Build
        sof = True
        rgb = True
        # Build Actions
        if sof == True:
            pass
        if rgb == True:
            pass

    #//
    #\\ Menu Displays ##########################################################
    # Channels
    def Menu_SOF(self):
        font = self.layout.sof.font()
        if self.layout.sof.isChecked():
            font.setBold(True)
            self.layout.sof_1_slider.setMinimumHeight(ui_10)
            self.layout.sof_1_slider.setMaximumHeight(ui_20)
            self.layout.sof_1_value.setMinimumHeight(ui_10)
            self.layout.sof_1_value.setMaximumHeight(ui_20)
            self.layout.sof_1_tick.setMinimumHeight(unit)
            self.layout.sof_1_tick.setMaximumHeight(unit)

            self.layout.sof_2_slider.setMinimumHeight(ui_10)
            self.layout.sof_2_slider.setMaximumHeight(ui_20)
            self.layout.sof_2_value.setMinimumHeight(ui_10)
            self.layout.sof_2_value.setMaximumHeight(ui_20)
            self.layout.sof_2_tick.setMinimumHeight(unit)
            self.layout.sof_2_tick.setMaximumHeight(unit)

            self.layout.sof_3_slider.setMinimumHeight(ui_10)
            self.layout.sof_3_slider.setMaximumHeight(ui_20)
            self.layout.sof_3_value.setMinimumHeight(ui_10)
            self.layout.sof_3_value.setMaximumHeight(ui_20)
            self.layout.sof_3_tick.setMinimumHeight(unit)
            self.layout.sof_3_tick.setMaximumHeight(unit)
        else:
            font.setBold(False)
            self.layout.sof_1_slider.setMinimumHeight(zero)
            self.layout.sof_1_slider.setMaximumHeight(zero)
            self.layout.sof_1_value.setMinimumHeight(zero)
            self.layout.sof_1_value.setMaximumHeight(zero)
            self.layout.sof_1_tick.setMinimumHeight(zero)

            self.layout.sof_2_slider.setMinimumHeight(zero)
            self.layout.sof_2_slider.setMaximumHeight(zero)
            self.layout.sof_2_value.setMinimumHeight(zero)
            self.layout.sof_2_value.setMaximumHeight(zero)
            self.layout.sof_2_tick.setMinimumHeight(zero)

            self.layout.sof_3_slider.setMinimumHeight(zero)
            self.layout.sof_3_slider.setMaximumHeight(zero)
            self.layout.sof_3_value.setMinimumHeight(zero)
            self.layout.sof_3_value.setMaximumHeight(zero)
            self.layout.sof_3_tick.setMinimumHeight(zero)
        self.layout.sof.setFont(font)
        self.Adjust_Spacing()
    def Menu_AAA(self):
        font = self.layout.aaa.font()
        if self.layout.aaa.isChecked():
            font.setBold(True)
            self.chan_aaa = True
            self.layout.aaa_1_label.setMinimumHeight(ui_10)
            self.layout.aaa_1_label.setMaximumHeight(ui_20)
            self.layout.aaa_1_slider.setMinimumHeight(ui_10)
            self.layout.aaa_1_slider.setMaximumHeight(ui_20)
            self.layout.aaa_1_value.setMinimumHeight(ui_10)
            self.layout.aaa_1_value.setMaximumHeight(ui_20)
            self.layout.aaa_1_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_aaa = False
            self.layout.aaa_1_label.setMinimumHeight(zero)
            self.layout.aaa_1_label.setMaximumHeight(zero)
            self.layout.aaa_1_slider.setMinimumHeight(zero)
            self.layout.aaa_1_slider.setMaximumHeight(zero)
            self.layout.aaa_1_value.setMinimumHeight(zero)
            self.layout.aaa_1_value.setMaximumHeight(zero)
            self.layout.aaa_1_tick.setMinimumHeight(zero)
        self.layout.aaa.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_RGB(self):
        font = self.layout.rgb.font()
        if self.layout.rgb.isChecked():
            font.setBold(True)
            self.chan_rgb = True
            self.layout.rgb_1_label.setMinimumHeight(ui_10)
            self.layout.rgb_1_label.setMaximumHeight(ui_20)
            self.layout.rgb_1_slider.setMinimumHeight(ui_10)
            self.layout.rgb_1_slider.setMaximumHeight(ui_20)
            self.layout.rgb_1_value.setMinimumHeight(ui_10)
            self.layout.rgb_1_value.setMaximumHeight(ui_20)
            self.layout.rgb_1_tick.setMinimumHeight(unit)

            self.layout.rgb_2_label.setMinimumHeight(ui_10)
            self.layout.rgb_2_label.setMaximumHeight(ui_20)
            self.layout.rgb_2_slider.setMinimumHeight(ui_10)
            self.layout.rgb_2_slider.setMaximumHeight(ui_20)
            self.layout.rgb_2_value.setMinimumHeight(ui_10)
            self.layout.rgb_2_value.setMaximumHeight(ui_20)
            self.layout.rgb_2_tick.setMinimumHeight(unit)

            self.layout.rgb_3_label.setMinimumHeight(ui_10)
            self.layout.rgb_3_label.setMaximumHeight(ui_20)
            self.layout.rgb_3_slider.setMinimumHeight(ui_10)
            self.layout.rgb_3_slider.setMaximumHeight(ui_20)
            self.layout.rgb_3_value.setMinimumHeight(ui_10)
            self.layout.rgb_3_value.setMaximumHeight(ui_20)
            self.layout.rgb_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_rgb = False
            self.layout.rgb_1_label.setMinimumHeight(zero)
            self.layout.rgb_1_label.setMaximumHeight(zero)
            self.layout.rgb_1_slider.setMinimumHeight(zero)
            self.layout.rgb_1_slider.setMaximumHeight(zero)
            self.layout.rgb_1_value.setMinimumHeight(zero)
            self.layout.rgb_1_value.setMaximumHeight(zero)
            self.layout.rgb_1_tick.setMinimumHeight(zero)

            self.layout.rgb_2_label.setMinimumHeight(zero)
            self.layout.rgb_2_label.setMaximumHeight(zero)
            self.layout.rgb_2_slider.setMinimumHeight(zero)
            self.layout.rgb_2_slider.setMaximumHeight(zero)
            self.layout.rgb_2_value.setMinimumHeight(zero)
            self.layout.rgb_2_value.setMaximumHeight(zero)
            self.layout.rgb_2_tick.setMinimumHeight(zero)

            self.layout.rgb_3_label.setMinimumHeight(zero)
            self.layout.rgb_3_label.setMaximumHeight(zero)
            self.layout.rgb_3_slider.setMinimumHeight(zero)
            self.layout.rgb_3_slider.setMaximumHeight(zero)
            self.layout.rgb_3_value.setMinimumHeight(zero)
            self.layout.rgb_3_value.setMaximumHeight(zero)
            self.layout.rgb_3_tick.setMinimumHeight(zero)
        self.layout.rgb.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_ARD(self):
        font = self.layout.ard.font()
        if self.layout.ard.isChecked():
            font.setBold(True)
            self.chan_ard = True
            self.layout.ard_1_label.setMinimumHeight(ui_10)
            self.layout.ard_1_label.setMaximumHeight(ui_20)
            self.layout.ard_1_slider.setMinimumHeight(ui_10)
            self.layout.ard_1_slider.setMaximumHeight(ui_20)
            self.layout.ard_1_value.setMinimumHeight(ui_10)
            self.layout.ard_1_value.setMaximumHeight(ui_20)
            self.layout.ard_1_tick.setMinimumHeight(unit)

            self.layout.ard_2_label.setMinimumHeight(ui_10)
            self.layout.ard_2_label.setMaximumHeight(ui_20)
            self.layout.ard_2_slider.setMinimumHeight(ui_10)
            self.layout.ard_2_slider.setMaximumHeight(ui_20)
            self.layout.ard_2_value.setMinimumHeight(ui_10)
            self.layout.ard_2_value.setMaximumHeight(ui_20)
            self.layout.ard_2_tick.setMinimumHeight(unit)

            self.layout.ard_3_label.setMinimumHeight(ui_10)
            self.layout.ard_3_label.setMaximumHeight(ui_20)
            self.layout.ard_3_slider.setMinimumHeight(ui_10)
            self.layout.ard_3_slider.setMaximumHeight(ui_20)
            self.layout.ard_3_value.setMinimumHeight(ui_10)
            self.layout.ard_3_value.setMaximumHeight(ui_20)
            self.layout.ard_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_ard = False
            self.layout.ard_1_label.setMinimumHeight(zero)
            self.layout.ard_1_label.setMaximumHeight(zero)
            self.layout.ard_1_slider.setMinimumHeight(zero)
            self.layout.ard_1_slider.setMaximumHeight(zero)
            self.layout.ard_1_value.setMinimumHeight(zero)
            self.layout.ard_1_value.setMaximumHeight(zero)
            self.layout.ard_1_tick.setMinimumHeight(zero)

            self.layout.ard_2_label.setMinimumHeight(zero)
            self.layout.ard_2_label.setMaximumHeight(zero)
            self.layout.ard_2_slider.setMinimumHeight(zero)
            self.layout.ard_2_slider.setMaximumHeight(zero)
            self.layout.ard_2_value.setMinimumHeight(zero)
            self.layout.ard_2_value.setMaximumHeight(zero)
            self.layout.ard_2_tick.setMinimumHeight(zero)

            self.layout.ard_3_label.setMinimumHeight(zero)
            self.layout.ard_3_label.setMaximumHeight(zero)
            self.layout.ard_3_slider.setMinimumHeight(zero)
            self.layout.ard_3_slider.setMaximumHeight(zero)
            self.layout.ard_3_value.setMinimumHeight(zero)
            self.layout.ard_3_value.setMaximumHeight(zero)
            self.layout.ard_3_tick.setMinimumHeight(zero)
        self.layout.ard.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_HSV(self):
        font = self.layout.hsv.font()
        if self.layout.hsv.isChecked():
            font.setBold(True)
            self.chan_hsv = True
            self.layout.hsv_1_label.setMinimumHeight(ui_10)
            self.layout.hsv_1_label.setMaximumHeight(ui_20)
            self.layout.hsv_1_slider.setMinimumHeight(ui_10)
            self.layout.hsv_1_slider.setMaximumHeight(ui_20)
            self.layout.hsv_1_value.setMinimumHeight(ui_10)
            self.layout.hsv_1_value.setMaximumHeight(ui_20)
            self.layout.hsv_1_tick.setMinimumHeight(unit)

            self.layout.hsv_2_label.setMinimumHeight(ui_10)
            self.layout.hsv_2_label.setMaximumHeight(ui_20)
            self.layout.hsv_2_slider.setMinimumHeight(ui_10)
            self.layout.hsv_2_slider.setMaximumHeight(ui_20)
            self.layout.hsv_2_value.setMinimumHeight(ui_10)
            self.layout.hsv_2_value.setMaximumHeight(ui_20)
            self.layout.hsv_2_tick.setMinimumHeight(unit)

            self.layout.hsv_3_label.setMinimumHeight(ui_10)
            self.layout.hsv_3_label.setMaximumHeight(ui_20)
            self.layout.hsv_3_slider.setMinimumHeight(ui_10)
            self.layout.hsv_3_slider.setMaximumHeight(ui_20)
            self.layout.hsv_3_value.setMinimumHeight(ui_10)
            self.layout.hsv_3_value.setMaximumHeight(ui_20)
            self.layout.hsv_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_hsv = False
            self.layout.hsv_1_label.setMinimumHeight(zero)
            self.layout.hsv_1_label.setMaximumHeight(zero)
            self.layout.hsv_1_slider.setMinimumHeight(zero)
            self.layout.hsv_1_slider.setMaximumHeight(zero)
            self.layout.hsv_1_value.setMinimumHeight(zero)
            self.layout.hsv_1_value.setMaximumHeight(zero)
            self.layout.hsv_1_tick.setMinimumHeight(zero)

            self.layout.hsv_2_label.setMinimumHeight(zero)
            self.layout.hsv_2_label.setMaximumHeight(zero)
            self.layout.hsv_2_slider.setMinimumHeight(zero)
            self.layout.hsv_2_slider.setMaximumHeight(zero)
            self.layout.hsv_2_value.setMinimumHeight(zero)
            self.layout.hsv_2_value.setMaximumHeight(zero)
            self.layout.hsv_2_tick.setMinimumHeight(zero)

            self.layout.hsv_3_label.setMinimumHeight(zero)
            self.layout.hsv_3_label.setMaximumHeight(zero)
            self.layout.hsv_3_slider.setMinimumHeight(zero)
            self.layout.hsv_3_slider.setMaximumHeight(zero)
            self.layout.hsv_3_value.setMinimumHeight(zero)
            self.layout.hsv_3_value.setMaximumHeight(zero)
            self.layout.hsv_3_tick.setMinimumHeight(zero)
        self.layout.hsv.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
            self.panel_hsv.update()
        except:
            pass
    def Menu_HSL(self):
        font = self.layout.hsl.font()
        if self.layout.hsl.isChecked():
            font.setBold(True)
            self.chan_hsl = True
            self.layout.hsl_1_label.setMinimumHeight(ui_10)
            self.layout.hsl_1_label.setMaximumHeight(ui_20)
            self.layout.hsl_1_slider.setMinimumHeight(ui_10)
            self.layout.hsl_1_slider.setMaximumHeight(ui_20)
            self.layout.hsl_1_value.setMinimumHeight(ui_10)
            self.layout.hsl_1_value.setMaximumHeight(ui_20)
            self.layout.hsl_1_tick.setMinimumHeight(unit)

            self.layout.hsl_2_label.setMinimumHeight(ui_10)
            self.layout.hsl_2_label.setMaximumHeight(ui_20)
            self.layout.hsl_2_slider.setMinimumHeight(ui_10)
            self.layout.hsl_2_slider.setMaximumHeight(ui_20)
            self.layout.hsl_2_value.setMinimumHeight(ui_10)
            self.layout.hsl_2_value.setMaximumHeight(ui_20)
            self.layout.hsl_2_tick.setMinimumHeight(unit)

            self.layout.hsl_3_label.setMinimumHeight(ui_10)
            self.layout.hsl_3_label.setMaximumHeight(ui_20)
            self.layout.hsl_3_slider.setMinimumHeight(ui_10)
            self.layout.hsl_3_slider.setMaximumHeight(ui_20)
            self.layout.hsl_3_value.setMinimumHeight(ui_10)
            self.layout.hsl_3_value.setMaximumHeight(ui_20)
            self.layout.hsl_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_hsl = False
            self.layout.hsl_1_label.setMinimumHeight(zero)
            self.layout.hsl_1_label.setMaximumHeight(zero)
            self.layout.hsl_1_slider.setMinimumHeight(zero)
            self.layout.hsl_1_slider.setMaximumHeight(zero)
            self.layout.hsl_1_value.setMinimumHeight(zero)
            self.layout.hsl_1_value.setMaximumHeight(zero)
            self.layout.hsl_1_tick.setMinimumHeight(zero)

            self.layout.hsl_2_label.setMinimumHeight(zero)
            self.layout.hsl_2_label.setMaximumHeight(zero)
            self.layout.hsl_2_slider.setMinimumHeight(zero)
            self.layout.hsl_2_slider.setMaximumHeight(zero)
            self.layout.hsl_2_value.setMinimumHeight(zero)
            self.layout.hsl_2_value.setMaximumHeight(zero)
            self.layout.hsl_2_tick.setMinimumHeight(zero)

            self.layout.hsl_3_label.setMinimumHeight(zero)
            self.layout.hsl_3_label.setMaximumHeight(zero)
            self.layout.hsl_3_slider.setMinimumHeight(zero)
            self.layout.hsl_3_slider.setMaximumHeight(zero)
            self.layout.hsl_3_value.setMinimumHeight(zero)
            self.layout.hsl_3_value.setMaximumHeight(zero)
            self.layout.hsl_3_tick.setMinimumHeight(zero)
        self.layout.hsl.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_HCY(self):
        font = self.layout.hcy.font()
        if self.layout.hcy.isChecked():
            font.setBold(True)
            self.chan_hcy = True
            self.layout.hcy_1_label.setMinimumHeight(ui_10)
            self.layout.hcy_1_label.setMaximumHeight(ui_20)
            self.layout.hcy_1_slider.setMinimumHeight(ui_10)
            self.layout.hcy_1_slider.setMaximumHeight(ui_20)
            self.layout.hcy_1_value.setMinimumHeight(ui_10)
            self.layout.hcy_1_value.setMaximumHeight(ui_20)
            self.layout.hcy_1_tick.setMinimumHeight(unit)

            self.layout.hcy_2_label.setMinimumHeight(ui_10)
            self.layout.hcy_2_label.setMaximumHeight(ui_20)
            self.layout.hcy_2_slider.setMinimumHeight(ui_10)
            self.layout.hcy_2_slider.setMaximumHeight(ui_20)
            self.layout.hcy_2_value.setMinimumHeight(ui_10)
            self.layout.hcy_2_value.setMaximumHeight(ui_20)
            self.layout.hcy_2_tick.setMinimumHeight(unit)

            self.layout.hcy_3_label.setMinimumHeight(ui_10)
            self.layout.hcy_3_label.setMaximumHeight(ui_20)
            self.layout.hcy_3_slider.setMinimumHeight(ui_10)
            self.layout.hcy_3_slider.setMaximumHeight(ui_20)
            self.layout.hcy_3_value.setMinimumHeight(ui_10)
            self.layout.hcy_3_value.setMaximumHeight(ui_20)
            self.layout.hcy_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_hcy = False
            self.layout.hcy_1_label.setMinimumHeight(zero)
            self.layout.hcy_1_label.setMaximumHeight(zero)
            self.layout.hcy_1_slider.setMinimumHeight(zero)
            self.layout.hcy_1_slider.setMaximumHeight(zero)
            self.layout.hcy_1_value.setMinimumHeight(zero)
            self.layout.hcy_1_value.setMaximumHeight(zero)
            self.layout.hcy_1_tick.setMinimumHeight(zero)

            self.layout.hcy_2_label.setMinimumHeight(zero)
            self.layout.hcy_2_label.setMaximumHeight(zero)
            self.layout.hcy_2_slider.setMinimumHeight(zero)
            self.layout.hcy_2_slider.setMaximumHeight(zero)
            self.layout.hcy_2_value.setMinimumHeight(zero)
            self.layout.hcy_2_value.setMaximumHeight(zero)
            self.layout.hcy_2_tick.setMinimumHeight(zero)

            self.layout.hcy_3_label.setMinimumHeight(zero)
            self.layout.hcy_3_label.setMaximumHeight(zero)
            self.layout.hcy_3_slider.setMinimumHeight(zero)
            self.layout.hcy_3_slider.setMaximumHeight(zero)
            self.layout.hcy_3_value.setMinimumHeight(zero)
            self.layout.hcy_3_value.setMaximumHeight(zero)
            self.layout.hcy_3_tick.setMinimumHeight(zero)
        self.layout.hcy.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_YUV(self):
        font = self.layout.yuv.font()
        if self.layout.yuv.isChecked():
            font.setBold(True)
            self.chan_yuv = True
            self.layout.yuv_1_label.setMinimumHeight(ui_10)
            self.layout.yuv_1_label.setMaximumHeight(ui_20)
            self.layout.yuv_1_slider.setMinimumHeight(ui_10)
            self.layout.yuv_1_slider.setMaximumHeight(ui_20)
            self.layout.yuv_1_value.setMinimumHeight(ui_10)
            self.layout.yuv_1_value.setMaximumHeight(ui_20)
            self.layout.yuv_1_tick.setMinimumHeight(unit)

            self.layout.yuv_2_label.setMinimumHeight(ui_10)
            self.layout.yuv_2_label.setMaximumHeight(ui_20)
            self.layout.yuv_2_slider.setMinimumHeight(ui_10)
            self.layout.yuv_2_slider.setMaximumHeight(ui_20)
            self.layout.yuv_2_value.setMinimumHeight(ui_10)
            self.layout.yuv_2_value.setMaximumHeight(ui_20)
            self.layout.yuv_2_tick.setMinimumHeight(unit)

            self.layout.yuv_3_label.setMinimumHeight(ui_10)
            self.layout.yuv_3_label.setMaximumHeight(ui_20)
            self.layout.yuv_3_slider.setMinimumHeight(ui_10)
            self.layout.yuv_3_slider.setMaximumHeight(ui_20)
            self.layout.yuv_3_value.setMinimumHeight(ui_10)
            self.layout.yuv_3_value.setMaximumHeight(ui_20)
            self.layout.yuv_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_yuv = False
            self.layout.yuv_1_label.setMinimumHeight(zero)
            self.layout.yuv_1_label.setMaximumHeight(zero)
            self.layout.yuv_1_slider.setMinimumHeight(zero)
            self.layout.yuv_1_slider.setMaximumHeight(zero)
            self.layout.yuv_1_value.setMinimumHeight(zero)
            self.layout.yuv_1_value.setMaximumHeight(zero)
            self.layout.yuv_1_tick.setMinimumHeight(zero)

            self.layout.yuv_2_label.setMinimumHeight(zero)
            self.layout.yuv_2_label.setMaximumHeight(zero)
            self.layout.yuv_2_slider.setMinimumHeight(zero)
            self.layout.yuv_2_slider.setMaximumHeight(zero)
            self.layout.yuv_2_value.setMinimumHeight(zero)
            self.layout.yuv_2_value.setMaximumHeight(zero)
            self.layout.yuv_2_tick.setMinimumHeight(zero)

            self.layout.yuv_3_label.setMinimumHeight(zero)
            self.layout.yuv_3_label.setMaximumHeight(zero)
            self.layout.yuv_3_slider.setMinimumHeight(zero)
            self.layout.yuv_3_slider.setMaximumHeight(zero)
            self.layout.yuv_3_value.setMinimumHeight(zero)
            self.layout.yuv_3_value.setMaximumHeight(zero)
            self.layout.yuv_3_tick.setMinimumHeight(zero)
        self.layout.yuv.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_RYB(self):
        font = self.layout.ryb.font()
        if self.layout.ryb.isChecked():
            font.setBold(True)
            self.chan_ryb = True
            self.layout.ryb_1_label.setMinimumHeight(ui_10)
            self.layout.ryb_1_label.setMaximumHeight(ui_20)
            self.layout.ryb_1_slider.setMinimumHeight(ui_10)
            self.layout.ryb_1_slider.setMaximumHeight(ui_20)
            self.layout.ryb_1_value.setMinimumHeight(ui_10)
            self.layout.ryb_1_value.setMaximumHeight(ui_20)
            self.layout.ryb_1_tick.setMinimumHeight(unit)

            self.layout.ryb_2_label.setMinimumHeight(ui_10)
            self.layout.ryb_2_label.setMaximumHeight(ui_20)
            self.layout.ryb_2_slider.setMinimumHeight(ui_10)
            self.layout.ryb_2_slider.setMaximumHeight(ui_20)
            self.layout.ryb_2_value.setMinimumHeight(ui_10)
            self.layout.ryb_2_value.setMaximumHeight(ui_20)
            self.layout.ryb_2_tick.setMinimumHeight(unit)

            self.layout.ryb_3_label.setMinimumHeight(ui_10)
            self.layout.ryb_3_label.setMaximumHeight(ui_20)
            self.layout.ryb_3_slider.setMinimumHeight(ui_10)
            self.layout.ryb_3_slider.setMaximumHeight(ui_20)
            self.layout.ryb_3_value.setMinimumHeight(ui_10)
            self.layout.ryb_3_value.setMaximumHeight(ui_20)
            self.layout.ryb_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_ryb = False
            self.layout.ryb_1_label.setMinimumHeight(zero)
            self.layout.ryb_1_label.setMaximumHeight(zero)
            self.layout.ryb_1_slider.setMinimumHeight(zero)
            self.layout.ryb_1_slider.setMaximumHeight(zero)
            self.layout.ryb_1_value.setMinimumHeight(zero)
            self.layout.ryb_1_value.setMaximumHeight(zero)
            self.layout.ryb_1_tick.setMinimumHeight(zero)

            self.layout.ryb_2_label.setMinimumHeight(zero)
            self.layout.ryb_2_label.setMaximumHeight(zero)
            self.layout.ryb_2_slider.setMinimumHeight(zero)
            self.layout.ryb_2_slider.setMaximumHeight(zero)
            self.layout.ryb_2_value.setMinimumHeight(zero)
            self.layout.ryb_2_value.setMaximumHeight(zero)
            self.layout.ryb_2_tick.setMinimumHeight(zero)

            self.layout.ryb_3_label.setMinimumHeight(zero)
            self.layout.ryb_3_label.setMaximumHeight(zero)
            self.layout.ryb_3_slider.setMinimumHeight(zero)
            self.layout.ryb_3_slider.setMaximumHeight(zero)
            self.layout.ryb_3_value.setMinimumHeight(zero)
            self.layout.ryb_3_value.setMaximumHeight(zero)
            self.layout.ryb_3_tick.setMinimumHeight(zero)
        self.layout.ryb.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_CMY(self):
        font = self.layout.cmy.font()
        if self.layout.cmy.isChecked():
            font.setBold(True)
            self.chan_cmy = True
            self.layout.cmy_1_label.setMinimumHeight(ui_10)
            self.layout.cmy_1_label.setMaximumHeight(ui_20)
            self.layout.cmy_1_slider.setMinimumHeight(ui_10)
            self.layout.cmy_1_slider.setMaximumHeight(ui_20)
            self.layout.cmy_1_value.setMinimumHeight(ui_10)
            self.layout.cmy_1_value.setMaximumHeight(ui_20)
            self.layout.cmy_1_tick.setMinimumHeight(unit)

            self.layout.cmy_2_label.setMinimumHeight(ui_10)
            self.layout.cmy_2_label.setMaximumHeight(ui_20)
            self.layout.cmy_2_slider.setMinimumHeight(ui_10)
            self.layout.cmy_2_slider.setMaximumHeight(ui_20)
            self.layout.cmy_2_value.setMinimumHeight(ui_10)
            self.layout.cmy_2_value.setMaximumHeight(ui_20)
            self.layout.cmy_2_tick.setMinimumHeight(unit)

            self.layout.cmy_3_label.setMinimumHeight(ui_10)
            self.layout.cmy_3_label.setMaximumHeight(ui_20)
            self.layout.cmy_3_slider.setMinimumHeight(ui_10)
            self.layout.cmy_3_slider.setMaximumHeight(ui_20)
            self.layout.cmy_3_value.setMinimumHeight(ui_10)
            self.layout.cmy_3_value.setMaximumHeight(ui_20)
            self.layout.cmy_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_cmy = False
            self.layout.cmy_1_label.setMinimumHeight(zero)
            self.layout.cmy_1_label.setMaximumHeight(zero)
            self.layout.cmy_1_slider.setMinimumHeight(zero)
            self.layout.cmy_1_slider.setMaximumHeight(zero)
            self.layout.cmy_1_value.setMinimumHeight(zero)
            self.layout.cmy_1_value.setMaximumHeight(zero)
            self.layout.cmy_1_tick.setMinimumHeight(zero)

            self.layout.cmy_2_label.setMinimumHeight(zero)
            self.layout.cmy_2_label.setMaximumHeight(zero)
            self.layout.cmy_2_slider.setMinimumHeight(zero)
            self.layout.cmy_2_slider.setMaximumHeight(zero)
            self.layout.cmy_2_value.setMinimumHeight(zero)
            self.layout.cmy_2_value.setMaximumHeight(zero)
            self.layout.cmy_2_tick.setMinimumHeight(zero)

            self.layout.cmy_3_label.setMinimumHeight(zero)
            self.layout.cmy_3_label.setMaximumHeight(zero)
            self.layout.cmy_3_slider.setMinimumHeight(zero)
            self.layout.cmy_3_slider.setMaximumHeight(zero)
            self.layout.cmy_3_value.setMinimumHeight(zero)
            self.layout.cmy_3_value.setMaximumHeight(zero)
            self.layout.cmy_3_tick.setMinimumHeight(zero)
        self.layout.cmy.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_CMYK(self):
        font = self.layout.cmyk.font()
        if self.layout.cmyk.isChecked():
            font.setBold(True)
            self.chan_cmyk = True
            self.layout.cmyk_1_label.setMinimumHeight(ui_10)
            self.layout.cmyk_1_label.setMaximumHeight(ui_20)
            self.layout.cmyk_1_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_1_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_1_value.setMinimumHeight(ui_10)
            self.layout.cmyk_1_value.setMaximumHeight(ui_20)
            self.layout.cmyk_1_tick.setMinimumHeight(unit)

            self.layout.cmyk_2_label.setMinimumHeight(ui_10)
            self.layout.cmyk_2_label.setMaximumHeight(ui_20)
            self.layout.cmyk_2_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_2_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_2_value.setMinimumHeight(ui_10)
            self.layout.cmyk_2_value.setMaximumHeight(ui_20)
            self.layout.cmyk_2_tick.setMinimumHeight(unit)

            self.layout.cmyk_3_label.setMinimumHeight(ui_10)
            self.layout.cmyk_3_label.setMaximumHeight(ui_20)
            self.layout.cmyk_3_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_3_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_3_value.setMinimumHeight(ui_10)
            self.layout.cmyk_3_value.setMaximumHeight(ui_20)
            self.layout.cmyk_3_tick.setMinimumHeight(unit)

            self.layout.cmyk_4_label.setMinimumHeight(ui_10)
            self.layout.cmyk_4_label.setMaximumHeight(ui_20)
            self.layout.cmyk_4_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_4_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_4_value.setMinimumHeight(ui_10)
            self.layout.cmyk_4_value.setMaximumHeight(ui_20)
            self.layout.cmyk_4_lock.setMinimumHeight(ui_10)
            self.layout.cmyk_4_lock.setMaximumHeight(ui_15)
            self.layout.cmyk_4_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_cmyk = False
            self.layout.cmyk_1_label.setMinimumHeight(zero)
            self.layout.cmyk_1_label.setMaximumHeight(zero)
            self.layout.cmyk_1_slider.setMinimumHeight(zero)
            self.layout.cmyk_1_slider.setMaximumHeight(zero)
            self.layout.cmyk_1_value.setMinimumHeight(zero)
            self.layout.cmyk_1_value.setMaximumHeight(zero)
            self.layout.cmyk_1_tick.setMinimumHeight(zero)

            self.layout.cmyk_2_label.setMinimumHeight(zero)
            self.layout.cmyk_2_label.setMaximumHeight(zero)
            self.layout.cmyk_2_slider.setMinimumHeight(zero)
            self.layout.cmyk_2_slider.setMaximumHeight(zero)
            self.layout.cmyk_2_value.setMinimumHeight(zero)
            self.layout.cmyk_2_value.setMaximumHeight(zero)
            self.layout.cmyk_2_tick.setMinimumHeight(zero)

            self.layout.cmyk_3_label.setMinimumHeight(zero)
            self.layout.cmyk_3_label.setMaximumHeight(zero)
            self.layout.cmyk_3_slider.setMinimumHeight(zero)
            self.layout.cmyk_3_slider.setMaximumHeight(zero)
            self.layout.cmyk_3_value.setMinimumHeight(zero)
            self.layout.cmyk_3_value.setMaximumHeight(zero)
            self.layout.cmyk_3_tick.setMinimumHeight(zero)

            self.layout.cmyk_4_label.setMinimumHeight(zero)
            self.layout.cmyk_4_label.setMaximumHeight(zero)
            self.layout.cmyk_4_slider.setMinimumHeight(zero)
            self.layout.cmyk_4_slider.setMaximumHeight(zero)
            self.layout.cmyk_4_value.setMinimumHeight(zero)
            self.layout.cmyk_4_value.setMaximumHeight(zero)
            self.layout.cmyk_4_lock.setMinimumHeight(zero)
            self.layout.cmyk_4_lock.setMaximumHeight(zero)
            self.layout.cmyk_4_tick.setMinimumHeight(zero)
        self.layout.cmyk.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    def Menu_KKK(self):
        font = self.layout.kkk.font()
        if self.layout.kkk.isChecked():
            font.setBold(True)
            self.chan_kkk = True
            self.layout.kkk_1_label.setMinimumHeight(ui_10)
            self.layout.kkk_1_label.setMaximumHeight(ui_20)
            self.layout.kkk_1_slider.setMinimumHeight(ui_10)
            self.layout.kkk_1_slider.setMaximumHeight(ui_20)
            self.layout.kkk_1_value.setMinimumHeight(ui_10)
            self.layout.kkk_1_value.setMaximumHeight(ui_20)
            self.layout.kkk_1_tick.setMinimumHeight(unit)
            self.layout.kkk_1_tick.setMaximumHeight(unit)
            self.layout.kkk_1_lock.setMinimumHeight(ui_10)
            self.layout.kkk_1_lock.setMaximumHeight(ui_15)
        else:
            font.setBold(False)
            self.chan_kkk = False
            self.layout.kkk_1_label.setMinimumHeight(zero)
            self.layout.kkk_1_label.setMaximumHeight(zero)
            self.layout.kkk_1_slider.setMinimumHeight(zero)
            self.layout.kkk_1_slider.setMaximumHeight(zero)
            self.layout.kkk_1_value.setMinimumHeight(zero)
            self.layout.kkk_1_value.setMaximumHeight(zero)
            self.layout.kkk_1_tick.setMinimumHeight(zero)
            self.layout.kkk_1_tick.setMaximumHeight(zero)
            self.layout.kkk_1_lock.setMinimumHeight(zero)
            self.layout.kkk_1_lock.setMaximumHeight(zero)
        self.layout.kkk.setFont(font)
        self.Adjust_Spacing()
        try:
            self.Pigment_Display()
        except:
            pass
    # Harmony
    def Menu_HARMONY(self):
        font = self.layout.har.font()
        self.harmony_menu = self.layout.har.isChecked() # Boolean
        if self.harmony_menu == False:
            font.setBold(False)
            self.harmony_active = 0
            self.harmony_rule = 0
            self.layout.color_1.setMinimumHeight(ui_total)
            self.layout.color_1.setMaximumHeight(ui_total)
            self.layout.color_2.setMinimumHeight(ui_total)
            self.layout.color_2.setMaximumHeight(ui_total)
            self.layout.harmony_1.setMinimumHeight(zero)
            self.layout.harmony_1.setMaximumHeight(zero)
            self.layout.harmony_2.setMinimumHeight(zero)
            self.layout.harmony_2.setMaximumHeight(zero)
            self.layout.harmony_3.setMinimumHeight(zero)
            self.layout.harmony_3.setMaximumHeight(zero)
            self.layout.harmony_4.setMinimumHeight(zero)
            self.layout.harmony_4.setMaximumHeight(zero)
            self.layout.harmony_5.setMinimumHeight(zero)
            self.layout.harmony_5.setMaximumHeight(zero)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (self.harmony_menu == True and self.harmony_index == "Monochromatic"):
            font.setBold(True)
            self.harmony_rule = 1
            self.layout.color_1.setMinimumHeight(ui_color)
            self.layout.color_1.setMaximumHeight(ui_color)
            self.layout.color_2.setMinimumHeight(ui_color)
            self.layout.color_2.setMaximumHeight(ui_color)
            self.layout.harmony_1.setMinimumHeight(ui_harmony)
            self.layout.harmony_1.setMaximumHeight(ui_harmony)
            self.layout.harmony_2.setMinimumHeight(ui_harmony)
            self.layout.harmony_2.setMaximumHeight(ui_harmony)
            self.layout.harmony_3.setMinimumHeight(ui_harmony)
            self.layout.harmony_3.setMaximumHeight(ui_harmony)
            self.layout.harmony_4.setMinimumHeight(ui_harmony)
            self.layout.harmony_4.setMaximumHeight(ui_harmony)
            self.layout.harmony_5.setMinimumHeight(ui_harmony)
            self.layout.harmony_5.setMaximumHeight(ui_harmony)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (self.harmony_menu == True and self.harmony_index == "Complemantary"):
            font.setBold(True)
            self.harmony_rule = 2
            self.layout.color_1.setMinimumHeight(ui_color)
            self.layout.color_1.setMaximumHeight(ui_color)
            self.layout.color_2.setMinimumHeight(ui_color)
            self.layout.color_2.setMaximumHeight(ui_color)
            self.layout.harmony_1.setMinimumHeight(ui_harmony)
            self.layout.harmony_1.setMaximumHeight(ui_harmony)
            self.layout.harmony_2.setMinimumHeight(ui_harmony)
            self.layout.harmony_2.setMaximumHeight(ui_harmony)
            self.layout.harmony_3.setMinimumHeight(ui_harmony)
            self.layout.harmony_3.setMaximumHeight(ui_harmony)
            self.layout.harmony_4.setMinimumHeight(ui_harmony)
            self.layout.harmony_4.setMaximumHeight(ui_harmony)
            self.layout.harmony_5.setMinimumHeight(ui_harmony)
            self.layout.harmony_5.setMaximumHeight(ui_harmony)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (self.harmony_menu == True and self.harmony_index == "Analogous"):
            font.setBold(True)
            self.harmony_rule = 3
            self.layout.color_1.setMinimumHeight(ui_color)
            self.layout.color_1.setMaximumHeight(ui_color)
            self.layout.color_2.setMinimumHeight(ui_color)
            self.layout.color_2.setMaximumHeight(ui_color)
            self.layout.harmony_1.setMinimumHeight(ui_harmony)
            self.layout.harmony_1.setMaximumHeight(ui_harmony)
            self.layout.harmony_2.setMinimumHeight(ui_harmony)
            self.layout.harmony_2.setMaximumHeight(ui_harmony)
            self.layout.harmony_3.setMinimumHeight(ui_harmony)
            self.layout.harmony_3.setMaximumHeight(ui_harmony)
            self.layout.harmony_4.setMinimumHeight(ui_harmony)
            self.layout.harmony_4.setMaximumHeight(ui_harmony)
            self.layout.harmony_5.setMinimumHeight(ui_harmony)
            self.layout.harmony_5.setMaximumHeight(ui_harmony)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (self.harmony_menu == True and self.harmony_index == "Split Complemantary"):
            font.setBold(True)
            self.harmony_rule = 4
            self.layout.color_1.setMinimumHeight(ui_color)
            self.layout.color_1.setMaximumHeight(ui_color)
            self.layout.color_2.setMinimumHeight(ui_color)
            self.layout.color_2.setMaximumHeight(ui_color)
            self.layout.harmony_1.setMinimumHeight(ui_harmony)
            self.layout.harmony_1.setMaximumHeight(ui_harmony)
            self.layout.harmony_2.setMinimumHeight(ui_harmony)
            self.layout.harmony_2.setMaximumHeight(ui_harmony)
            self.layout.harmony_3.setMinimumHeight(ui_harmony)
            self.layout.harmony_3.setMaximumHeight(ui_harmony)
            self.layout.harmony_4.setMinimumHeight(ui_harmony)
            self.layout.harmony_4.setMaximumHeight(ui_harmony)
            self.layout.harmony_5.setMinimumHeight(ui_harmony)
            self.layout.harmony_5.setMaximumHeight(ui_harmony)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (self.harmony_menu == True and self.harmony_index == "Double Split Complemantary"):
            font.setBold(True)
            self.harmony_rule = 5
            self.layout.color_1.setMinimumHeight(ui_color)
            self.layout.color_1.setMaximumHeight(ui_color)
            self.layout.color_2.setMinimumHeight(ui_color)
            self.layout.color_2.setMaximumHeight(ui_color)
            self.layout.harmony_1.setMinimumHeight(ui_harmony)
            self.layout.harmony_1.setMaximumHeight(ui_harmony)
            self.layout.harmony_2.setMinimumHeight(ui_harmony)
            self.layout.harmony_2.setMaximumHeight(ui_harmony)
            self.layout.harmony_3.setMinimumHeight(ui_harmony)
            self.layout.harmony_3.setMaximumHeight(ui_harmony)
            self.layout.harmony_4.setMinimumHeight(ui_harmony)
            self.layout.harmony_4.setMaximumHeight(ui_harmony)
            self.layout.harmony_5.setMinimumHeight(ui_harmony)
            self.layout.harmony_5.setMaximumHeight(ui_harmony)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        # Active Harmony Color
        if self.harmony_active == 1:
            self.Harmony_1_Active(0)
        if self.harmony_active == 2:
            self.Harmony_2_Active(0)
        if self.harmony_active == 3:
            self.Harmony_3_Active(0)
        if self.harmony_active == 4:
            self.Harmony_4_Active(0)
        if self.harmony_active == 5:
            self.Harmony_5_Active(0)
        # Render State
        if self.harmony_rule == 0:
            self.harmony_render = "COLOR"
        else:
            self.harmony_render = "HARMONY"
        self.layout.har.setFont(font)
        self.Adjust_Spacing()
        self.Ratio()
    def HARMONY_Index(self):
        self.harmony_index = self.layout.har_index.currentText() # Text
    def HARMONY_Edit(self):
        self.harmony_edit = self.layout.har_edit.isChecked() # Boolean
    # Color of the Day
    def Menu_COTD(self):
        font = self.layout.cotd.font()
        if self.layout.cotd.isChecked():
            font.setBold(True)
            self.layout.cotd_date.setMinimumHeight(ui_15)
            self.layout.cotd_date.setMaximumHeight(ui_15)
            self.layout.cotd1.setMinimumHeight(ui_15)
            self.layout.cotd1.setMaximumHeight(ui_15)
            self.layout.cotd2.setMinimumHeight(ui_15)
            self.layout.cotd2.setMaximumHeight(ui_15)
            self.layout.cotd3.setMinimumHeight(ui_15)
            self.layout.cotd3.setMaximumHeight(ui_15)
            self.layout.cotd4.setMinimumHeight(ui_15)
            self.layout.cotd4.setMaximumHeight(ui_15)
            self.layout.cotd5.setMinimumHeight(ui_15)
            self.layout.cotd5.setMaximumHeight(ui_15)
            self.layout.color_of_the_day.setContentsMargins(zero, unit, zero, unit)
        else:
            font.setBold(False)
            self.layout.cotd_date.setMinimumHeight(zero)
            self.layout.cotd_date.setMaximumHeight(zero)
            self.layout.cotd1.setMinimumHeight(zero)
            self.layout.cotd1.setMaximumHeight(zero)
            self.layout.cotd2.setMinimumHeight(zero)
            self.layout.cotd2.setMaximumHeight(zero)
            self.layout.cotd3.setMinimumHeight(zero)
            self.layout.cotd3.setMaximumHeight(zero)
            self.layout.cotd4.setMinimumHeight(zero)
            self.layout.cotd4.setMaximumHeight(zero)
            self.layout.cotd5.setMinimumHeight(zero)
            self.layout.cotd5.setMaximumHeight(zero)
            self.layout.color_of_the_day.setContentsMargins(zero, zero, zero, zero)
        self.layout.cotd.setFont(font)
        self.Adjust_Spacing()
    # Panels
    def Menu_PANEL(self):
        font = self.layout.pan.font()
        self.PANEL_Shrink()
        # Panel States
        panel = self.layout.pan.isChecked()
        self.panel_active = self.layout.pan_index.currentText()
        self.panel_secondary = self.layout.pan_secondary.currentText()
        if panel == False:
            font.setBold(False)
            self.panel_active = "None"
        if (panel == True and self.panel_active == "FGC"):
            font.setBold(True)
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Display()
        if (panel == True and self.panel_active == "RGB"):
            font.setBold(True)
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("RGB", 0)
        if (panel == True and self.panel_active == "ARD"):
            font.setBold(True)
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("RGB", 0)
        if (panel == True and self.panel_active == "HSV"):
            font.setBold(True)
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("HSV", 0)
        if (panel == True and self.panel_active == "HSL"):
            font.setBold(True)
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("HSL", 0)
        if (panel == True and self.panel_active == "YUV"):
            font.setBold(True)
            self.layout.panel_yuv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("YUV", 0)
        if (panel == True and self.panel_active == "HUE"):
            font.setBold(True)
            self.layout.panel_hue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("HSL", 0)
        if (panel == True and self.panel_active == "GAM"):
            font.setBold(True)
            self.layout.panel_gam.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if (panel == True and self.panel_active == "DOT"):
            font.setBold(True)
            self.layout.panel_dot_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.DOT_SET()
        if (panel == True and self.panel_active == "OBJ"):
            font.setBold(True)
            self.OBJ_SET()
            self.OBJ_Index()
            # Object Display
            self.OBJ_Geometry()
            self.OBJ_Save()
            self.OBJ_Alpha()
            # Layers Render Variables
            self.layer_01 = True
            self.layer_02 = True
            self.layer_03 = True
            self.layer_04 = True
            self.layer_05 = True
            self.layer_06 = True
            self.layer_07 = True
            self.layer_08 = True
            self.layer_09 = True
            self.layer_10 = True
            self.layer_11 = True
            self.layer_12 = True
        # Secondary Menu Options
        if self.panel_active == "HUE":
            self.layout.pan_secondary.setEnabled(True)
            self.layout.pan_secondary.setMaximumWidth(max_val)
        if self.panel_active == "GAM":
            self.layout.gam_space.setEnabled(True)
            self.layout.gam_space.setMaximumWidth(max_val)
            self.layout.gam_shape.setEnabled(True)
            self.layout.gam_shape.setMaximumWidth(max_val)
        if self.panel_active == "DOT":
            self.layout.dot_set.setEnabled(True)
            self.layout.dot_set.setMaximumWidth(max_val)
        if self.panel_active == "OBJ":
            self.layout.obj_index.setEnabled(True)
            self.layout.obj_index.setMaximumWidth(max_val)
            self.layout.obj_set.setEnabled(True)
            self.layout.obj_set.setMaximumWidth(max_val)
        self.layout.pan.setFont(font)
        self.Adjust_Spacing()
        self.Pigment_HUE_Harmony_Active(self.harmony_active)
        self.update()
    def PANEL_Shrink(self):
        # SINGLE
        self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_yuv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # HUE
        self.layout.panel_hue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.pan_secondary.setEnabled(False)
        self.layout.pan_secondary.setMaximumWidth(zero)
        # GAM
        self.layout.panel_gam.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.gam_space.setEnabled(False)
        self.layout.gam_space.setMaximumWidth(zero)
        self.layout.gam_shape.setEnabled(False)
        self.layout.gam_shape.setMaximumWidth(zero)
        # DOT
        self.layout.panel_dot_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.dot_set.setEnabled(False)
        self.layout.dot_set.setMaximumWidth(zero)
        self.DOT_Shrink()
        # OBJ
        self.layout.panel_obj_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.obj_index.setEnabled(False)
        self.layout.obj_index.setMaximumWidth(zero)
        self.layout.obj_set.setEnabled(False)
        self.layout.obj_set.setMaximumWidth(zero)
        self.OBJ_Shrink_Top()
        self.OBJ_Shrink_Bot()
    # Panel HUE
    def Menu_Wheel(self):
        wheel = self.layout.wheel_index.currentText()
        if wheel == "CMY":
            self.wheel = "CMY"
        if wheel == "RYB":
            self.wheel = "RYB"
        self.Signal_Send_Panels()
        self.Pigment_Harmony(0)
    def Menu_Hue_Secondary(self):
        self.panel_secondary = self.layout.pan_secondary.currentText()
        if self.panel_secondary == "DOT":
            self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if self.panel_secondary == "TRIANGLE":
            self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if self.panel_secondary == "SQUARE":
            self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if self.panel_secondary == "DIAMOND":
            self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Pigment_Convert("RGB", 0)
    # Panel Gamut
    def GAM_Space(self):
        # self.gamut_space = self.layout.gam_space.currentText()
        space = self.layout.gam_space.currentText()
        if space == "ARD":
            self.gamut_space = "ARD"
        if space == "HSV":
            self.gamut_space = "HSV"
        if space == "HSL":
            self.gamut_space = "HSL"
        if space == "HCY":
            self.gamut_space = "HCY"
        self.panel_gam_circle.update()
        self.panel_gam_polygon.update()
    def GAM_Shape(self):
        gamut = self.layout.gam_shape.currentText()
        if gamut == "None":
            self.gamut_shape = "None"
        if gamut == "Circle":
            self.gamut_shape = "P1_S1" # 1Polygon 1Side
        if gamut == "Triangle":
            self.gamut_shape = "P1_S3" # 1Polygon 3Sides
        if gamut == "Square":
            self.gamut_shape = "P1_S4" # 1Polygon 4Sides
        if gamut == "2 Circles":
            self.gamut_shape = "P2_S1" # 1Polygon 1Sides
        if gamut == "3 Pies":
            self.gamut_shape = "P3_S3" # 3Polygon 3Sides
        if gamut == "Reset":
            # Variables Reset
            self.P1_S1 = [
                0.5,0.1,
                0.9,0.5,
                0.5,0.9,
                0.1,0.5]
            self.P1_S3 = [
                0.5,0.1,
                0.84641,0.7,
                0.15359,0.7]
            self.P1_S4 = [
                0.5,0.1,
                0.9,0.5,
                0.5,0.9,
                0.1,0.5]
            self.P2_S1 = [
                # Circle 1
                0.5,0.1,
                0.675,0.275,
                0.5,0.45,
                0.325,0.275,
                # Circle 2
                0.5,0.55,
                0.675,0.725,
                0.5,0.9,
                0.325,0.725]
            self.P3_S3 = [
                # Center
                0.5,0.5,
                # Hexagon
                0.5,0.15359,
                0.8,0.32679,
                0.8,0.67321,
                0.5,0.84641,
                0.2,0.67321,
                0.2,0.32679]
            # Rotation
            self.P1_S1_r = [
                0.5,0.1,
                0.9,0.5,
                0.5,0.9,
                0.1,0.5]
            self.P1_S3_r = [
                0.5,0.1,
                0.84641,0.7,
                0.15359,0.7]
            self.P1_S4_r = [
                0.5,0.1,
                0.9,0.5,
                0.5,0.9,
                0.1,0.5]
            self.P2_S1_r = [
                # Circle 1
                0.5,0.1,
                0.675,0.275,
                0.5,0.45,
                0.325,0.275,
                # Circle 2
                0.5,0.55,
                0.675,0.725,
                0.5,0.9,
                0.325,0.725]
            self.P3_S3_r = [
                # Center
                0.5,0.5,
                # Hexagon
                0.5,0.15359,
                0.8,0.32679,
                0.8,0.67321,
                0.5,0.84641,
                0.2,0.67321,
                0.2,0.32679]
            # Reset Dropdown Index to previous
            if self.gamut_shape == "None":
                index = 0
            if self.gamut_shape == "P1_S1":
                index = 1
            if self.gamut_shape == "P1_S3":
                index = 2
            if self.gamut_shape == "P1_S4":
                index = 3
            if self.gamut_shape == "P2_S1":
                index = 4
            if self.gamut_shape == "P3_S3":
                index = 5
            self.layout.gam_shape.setCurrentIndex(index)
        self.panel_gam_circle.update()
        self.panel_gam_polygon.update()
    # Panel DOT
    def DOT_SET(self):
        if (self.layout.dot_set.isChecked() == True and self.panel_active == "DOT"):
            self.DOT_Scale()
        if (self.layout.dot_set.isChecked() == False and self.panel_active == "DOT"):
            self.DOT_Shrink()
    def DOT_Shrink(self):
        self.layout.dot_1.setMinimumHeight(zero)
        self.layout.dot_1.setMaximumHeight(zero)
        self.layout.dot_2.setMinimumHeight(zero)
        self.layout.dot_2.setMaximumHeight(zero)
        self.layout.dot_3.setMinimumHeight(zero)
        self.layout.dot_3.setMaximumHeight(zero)
        self.layout.dot_4.setMinimumHeight(zero)
        self.layout.dot_4.setMaximumHeight(zero)
        self.layout.dot_swap.setMinimumHeight(zero)
        self.layout.dot_swap.setMaximumHeight(zero)
        self.layout.panel_dot_colors.setContentsMargins(zero, zero, zero, zero)
        self.layout.panel_dot_colors.setSpacing(zero)
    def DOT_Scale(self):
        self.layout.dot_1.setMinimumHeight(ui_25)
        self.layout.dot_1.setMaximumHeight(ui_25)
        self.layout.dot_2.setMinimumHeight(ui_25)
        self.layout.dot_2.setMaximumHeight(ui_25)
        self.layout.dot_3.setMinimumHeight(ui_25)
        self.layout.dot_3.setMaximumHeight(ui_25)
        self.layout.dot_4.setMinimumHeight(ui_25)
        self.layout.dot_4.setMaximumHeight(ui_25)
        self.layout.dot_swap.setMinimumHeight(ui_25)
        self.layout.dot_swap.setMaximumHeight(ui_25)
        self.layout.panel_dot_colors.setContentsMargins(zero, unit, zero, unit)
        self.layout.panel_dot_colors.setSpacing(2)
    # Panel Object
    def OBJ_Index(self):
        self.obj_index = self.layout.obj_index.currentIndex()
        self.obj_text = self.layout.obj_index.currentText()
        # Paths
        if self.obj_text == "SPHERE":
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
        if self.obj_text == "USER":
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
        # Display
        if self.panel_active == "OBJ":
            # Adjust UI
            self.OBJ_Scale_Top()
            if self.layout.obj_set.isChecked() == True:
                self.OBJ_Scale_Bot()
            # Change Display
            self.OBJ_Geometry()
            self.OBJ_Save()
            self.OBJ_Alpha()
            # Layers Render Variables
            self.layer_01 = True
            self.layer_02 = True
            self.layer_03 = True
            self.layer_04 = True
            self.layer_05 = True
            self.layer_06 = True
            self.layer_07 = True
            self.layer_08 = True
            self.layer_09 = True
            self.layer_10 = True
            self.layer_11 = True
            self.layer_12 = True
    def OBJ_Save(self):
        if self.panel_active == "OBJ":
            self.BG_1_SAVE(self.bg_1[1], self.bg_1[2], self.bg_1[3], self.bg_1[4])
            self.BG_2_SAVE(self.bg_2[1], self.bg_2[2], self.bg_2[3], self.bg_2[4])
            self.BG_3_SAVE(self.bg_3[1], self.bg_3[2], self.bg_3[3], self.bg_3[4])
            self.DIF_1_SAVE(self.dif_1[1], self.dif_1[2], self.dif_1[3], self.dif_1[4])
            self.DIF_2_SAVE(self.dif_2[1], self.dif_2[2], self.dif_2[3], self.dif_2[4])
            self.DIF_3_SAVE(self.dif_3[1], self.dif_3[2], self.dif_3[3], self.dif_3[4])
            self.DIF_4_SAVE(self.dif_4[1], self.dif_4[2], self.dif_4[3], self.dif_4[4])
            self.DIF_5_SAVE(self.dif_5[1], self.dif_5[2], self.dif_5[3], self.dif_5[4])
            self.DIF_6_SAVE(self.dif_6[1], self.dif_6[2], self.dif_6[3], self.dif_6[4])
            self.FG_1_SAVE(self.fg_1[1], self.fg_1[2], self.fg_1[3], self.fg_1[4])
            self.FG_2_SAVE(self.fg_2[1], self.fg_2[2], self.fg_2[3], self.fg_2[4])
            self.FG_3_SAVE(self.fg_3[1], self.fg_3[2], self.fg_3[3], self.fg_3[4])
    def OBJ_SET(self):
        if (self.layout.obj_set.isChecked() == True and self.panel_active == "OBJ"):
            self.OBJ_Scale_Bot()
        if (self.layout.obj_set.isChecked() == False and self.panel_active == "OBJ"):
            self.OBJ_Shrink_Bot()
    def OBJ_Shrink_Top(self):
        # Object View Shrink
        self.layout.panel_obj_mix.setContentsMargins(zero, zero, zero, zero)
        self.layout.panel_obj_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    def OBJ_Shrink_Bot(self):
        # Margins
        self.layout.panel_obj_colors.setContentsMargins(zero, zero, zero, zero)
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
    def OBJ_Scale_Top(self):
        # Object View Scales
        self.layout.panel_obj_mix.setContentsMargins(zero, zero, zero, zero)
        self.layout.panel_obj_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    def OBJ_Scale_Bot(self):
        # Margins
        self.layout.panel_obj_colors.setContentsMargins(zero, unit, zero, unit)
        # BackGround 1
        self.layout.b1_live.setMinimumHeight(ui_20)
        self.layout.b1_live.setMaximumHeight(ui_20)
        self.layout.b1_color.setMinimumHeight(ui_25)
        self.layout.b1_color.setMaximumHeight(ui_25)
        self.layout.b1_alpha.setMinimumHeight(ui_10)
        self.layout.b1_alpha.setMaximumHeight(ui_10)
        # BackGround 2
        self.layout.b2_live.setMinimumHeight(ui_20)
        self.layout.b2_live.setMaximumHeight(ui_20)
        self.layout.b2_color.setMinimumHeight(ui_25)
        self.layout.b2_color.setMaximumHeight(ui_25)
        self.layout.b2_alpha.setMinimumHeight(ui_10)
        self.layout.b2_alpha.setMaximumHeight(ui_10)
        # BackGround 3
        self.layout.b3_live.setMinimumHeight(ui_20)
        self.layout.b3_live.setMaximumHeight(ui_20)
        self.layout.b3_color.setMinimumHeight(ui_25)
        self.layout.b3_color.setMaximumHeight(ui_25)
        self.layout.b3_alpha.setMinimumHeight(ui_10)
        self.layout.b3_alpha.setMaximumHeight(ui_10)
        # Diffuse 1
        self.layout.d1_live.setMinimumHeight(ui_20)
        self.layout.d1_live.setMaximumHeight(ui_20)
        self.layout.d1_color.setMinimumHeight(ui_25)
        self.layout.d1_color.setMaximumHeight(ui_25)
        self.layout.d1_alpha.setMinimumHeight(ui_10)
        self.layout.d1_alpha.setMaximumHeight(ui_10)
        # Diffuse 2
        self.layout.d2_live.setMinimumHeight(ui_20)
        self.layout.d2_live.setMaximumHeight(ui_20)
        self.layout.d2_color.setMinimumHeight(ui_25)
        self.layout.d2_color.setMaximumHeight(ui_25)
        self.layout.d2_alpha.setMinimumHeight(ui_10)
        self.layout.d2_alpha.setMaximumHeight(ui_10)
        # Diffuse 3
        self.layout.d3_live.setMinimumHeight(ui_20)
        self.layout.d3_live.setMaximumHeight(ui_20)
        self.layout.d3_color.setMinimumHeight(ui_25)
        self.layout.d3_color.setMaximumHeight(ui_25)
        self.layout.d3_alpha.setMinimumHeight(ui_10)
        self.layout.d3_alpha.setMaximumHeight(ui_10)
        # Diffuse 4
        self.layout.d4_live.setMinimumHeight(ui_20)
        self.layout.d4_live.setMaximumHeight(ui_20)
        self.layout.d4_color.setMinimumHeight(ui_25)
        self.layout.d4_color.setMaximumHeight(ui_25)
        self.layout.d4_alpha.setMinimumHeight(ui_10)
        self.layout.d4_alpha.setMaximumHeight(ui_10)
        # Diffuse 5
        self.layout.d5_live.setMinimumHeight(ui_20)
        self.layout.d5_live.setMaximumHeight(ui_20)
        self.layout.d5_color.setMinimumHeight(ui_25)
        self.layout.d5_color.setMaximumHeight(ui_25)
        self.layout.d5_alpha.setMinimumHeight(ui_10)
        self.layout.d5_alpha.setMaximumHeight(ui_10)
        # Diffuse 6
        self.layout.d6_live.setMinimumHeight(ui_20)
        self.layout.d6_live.setMaximumHeight(ui_20)
        self.layout.d6_color.setMinimumHeight(ui_25)
        self.layout.d6_color.setMaximumHeight(ui_25)
        self.layout.d6_alpha.setMinimumHeight(ui_10)
        self.layout.d6_alpha.setMaximumHeight(ui_10)
        # ForeGround 1
        self.layout.f1_live.setMinimumHeight(ui_20)
        self.layout.f1_live.setMaximumHeight(ui_20)
        self.layout.f1_color.setMinimumHeight(ui_25)
        self.layout.f1_color.setMaximumHeight(ui_25)
        self.layout.f1_alpha.setMinimumHeight(ui_10)
        self.layout.f1_alpha.setMaximumHeight(ui_10)
        # ForeGround 2
        self.layout.f2_live.setMinimumHeight(ui_20)
        self.layout.f2_live.setMaximumHeight(ui_20)
        self.layout.f2_color.setMinimumHeight(ui_25)
        self.layout.f2_color.setMaximumHeight(ui_25)
        self.layout.f2_alpha.setMinimumHeight(ui_10)
        self.layout.f2_alpha.setMaximumHeight(ui_10)
        # ForeGround 3
        self.layout.f3_live.setMinimumHeight(ui_20)
        self.layout.f3_live.setMaximumHeight(ui_20)
        self.layout.f3_color.setMinimumHeight(ui_25)
        self.layout.f3_color.setMaximumHeight(ui_25)
        self.layout.f3_alpha.setMinimumHeight(ui_10)
        self.layout.f3_alpha.setMaximumHeight(ui_10)
    # Channels
    def Menu_Value(self):
        val = self.layout.values.isChecked()
        if val == True:
            # HEX
            self.layout.hex_string.setMinimumWidth(ui_50)
            self.layout.hex_string.setMaximumWidth(ui_70)
            # SOF
            self.layout.eraser.setMinimumWidth(ui_15)
            self.layout.eraser.setMaximumWidth(ui_15)
            self.layout.sof_1_value.setMinimumWidth(ui_50)
            self.layout.sof_1_value.setMaximumWidth(ui_70)
            self.layout.sof_2_value.setMinimumWidth(ui_50)
            self.layout.sof_2_value.setMaximumWidth(ui_70)
            self.layout.sof_3_value.setMinimumWidth(ui_50)
            self.layout.sof_3_value.setMaximumWidth(ui_70)
            # AAA
            self.layout.aaa_1_label.setMinimumWidth(ui_15)
            self.layout.aaa_1_label.setMaximumWidth(ui_15)
            self.layout.aaa_1_value.setMinimumWidth(ui_50)
            self.layout.aaa_1_value.setMaximumWidth(ui_70)
            # RGB
            self.layout.rgb_1_label.setMinimumWidth(ui_15)
            self.layout.rgb_1_label.setMaximumWidth(ui_15)
            self.layout.rgb_2_label.setMinimumWidth(ui_15)
            self.layout.rgb_2_label.setMaximumWidth(ui_15)
            self.layout.rgb_3_label.setMinimumWidth(ui_15)
            self.layout.rgb_3_label.setMaximumWidth(ui_15)
            self.layout.rgb_1_value.setMinimumWidth(ui_50)
            self.layout.rgb_1_value.setMaximumWidth(ui_70)
            self.layout.rgb_2_value.setMinimumWidth(ui_50)
            self.layout.rgb_2_value.setMaximumWidth(ui_70)
            self.layout.rgb_3_value.setMinimumWidth(ui_50)
            self.layout.rgb_3_value.setMaximumWidth(ui_70)
            # ARD
            self.layout.ard_1_label.setMinimumWidth(ui_15)
            self.layout.ard_1_label.setMaximumWidth(ui_15)
            self.layout.ard_2_label.setMinimumWidth(ui_15)
            self.layout.ard_2_label.setMaximumWidth(ui_15)
            self.layout.ard_3_label.setMinimumWidth(ui_15)
            self.layout.ard_3_label.setMaximumWidth(ui_15)
            self.layout.ard_1_value.setMinimumWidth(ui_50)
            self.layout.ard_1_value.setMaximumWidth(ui_70)
            self.layout.ard_2_value.setMinimumWidth(ui_50)
            self.layout.ard_2_value.setMaximumWidth(ui_70)
            self.layout.ard_3_value.setMinimumWidth(ui_50)
            self.layout.ard_3_value.setMaximumWidth(ui_70)
            # HSV
            self.layout.hsv_1_label.setMinimumWidth(ui_15)
            self.layout.hsv_1_label.setMaximumWidth(ui_15)
            self.layout.hsv_2_label.setMinimumWidth(ui_15)
            self.layout.hsv_2_label.setMaximumWidth(ui_15)
            self.layout.hsv_3_label.setMinimumWidth(ui_15)
            self.layout.hsv_3_label.setMaximumWidth(ui_15)
            self.layout.hsv_1_value.setMinimumWidth(ui_50)
            self.layout.hsv_1_value.setMaximumWidth(ui_70)
            self.layout.hsv_2_value.setMinimumWidth(ui_50)
            self.layout.hsv_2_value.setMaximumWidth(ui_70)
            self.layout.hsv_3_value.setMinimumWidth(ui_50)
            self.layout.hsv_3_value.setMaximumWidth(ui_70)
            # HSL
            self.layout.hsl_1_label.setMinimumWidth(ui_15)
            self.layout.hsl_1_label.setMaximumWidth(ui_15)
            self.layout.hsl_2_label.setMinimumWidth(ui_15)
            self.layout.hsl_2_label.setMaximumWidth(ui_15)
            self.layout.hsl_3_label.setMinimumWidth(ui_15)
            self.layout.hsl_3_label.setMaximumWidth(ui_15)
            self.layout.hsl_1_value.setMinimumWidth(ui_50)
            self.layout.hsl_1_value.setMaximumWidth(ui_70)
            self.layout.hsl_2_value.setMinimumWidth(ui_50)
            self.layout.hsl_2_value.setMaximumWidth(ui_70)
            self.layout.hsl_3_value.setMinimumWidth(ui_50)
            self.layout.hsl_3_value.setMaximumWidth(ui_70)
            # HCY
            self.layout.hcy_1_label.setMinimumWidth(ui_15)
            self.layout.hcy_1_label.setMaximumWidth(ui_15)
            self.layout.hcy_2_label.setMinimumWidth(ui_15)
            self.layout.hcy_2_label.setMaximumWidth(ui_15)
            self.layout.hcy_3_label.setMinimumWidth(ui_15)
            self.layout.hcy_3_label.setMaximumWidth(ui_15)
            self.layout.hcy_1_value.setMinimumWidth(ui_50)
            self.layout.hcy_1_value.setMaximumWidth(ui_70)
            self.layout.hcy_2_value.setMinimumWidth(ui_50)
            self.layout.hcy_2_value.setMaximumWidth(ui_70)
            self.layout.hcy_3_value.setMinimumWidth(ui_50)
            self.layout.hcy_3_value.setMaximumWidth(ui_70)
            # YUV
            self.layout.yuv_1_label.setMinimumWidth(ui_15)
            self.layout.yuv_1_label.setMaximumWidth(ui_15)
            self.layout.yuv_2_label.setMinimumWidth(ui_15)
            self.layout.yuv_2_label.setMaximumWidth(ui_15)
            self.layout.yuv_3_label.setMinimumWidth(ui_15)
            self.layout.yuv_3_label.setMaximumWidth(ui_15)
            self.layout.yuv_1_value.setMinimumWidth(ui_50)
            self.layout.yuv_1_value.setMaximumWidth(ui_70)
            self.layout.yuv_2_value.setMinimumWidth(ui_50)
            self.layout.yuv_2_value.setMaximumWidth(ui_70)
            self.layout.yuv_3_value.setMinimumWidth(ui_50)
            self.layout.yuv_3_value.setMaximumWidth(ui_70)
            # RYB
            self.layout.ryb_1_label.setMinimumWidth(ui_15)
            self.layout.ryb_1_label.setMaximumWidth(ui_15)
            self.layout.ryb_2_label.setMinimumWidth(ui_15)
            self.layout.ryb_2_label.setMaximumWidth(ui_15)
            self.layout.ryb_3_label.setMinimumWidth(ui_15)
            self.layout.ryb_3_label.setMaximumWidth(ui_15)
            self.layout.ryb_1_value.setMinimumWidth(ui_50)
            self.layout.ryb_1_value.setMaximumWidth(ui_70)
            self.layout.ryb_2_value.setMinimumWidth(ui_50)
            self.layout.ryb_2_value.setMaximumWidth(ui_70)
            self.layout.ryb_3_value.setMinimumWidth(ui_50)
            self.layout.ryb_3_value.setMaximumWidth(ui_70)
            # CMY
            self.layout.cmy_1_label.setMinimumWidth(ui_15)
            self.layout.cmy_1_label.setMaximumWidth(ui_15)
            self.layout.cmy_2_label.setMinimumWidth(ui_15)
            self.layout.cmy_2_label.setMaximumWidth(ui_15)
            self.layout.cmy_3_label.setMinimumWidth(ui_15)
            self.layout.cmy_3_label.setMaximumWidth(ui_15)
            self.layout.cmy_1_value.setMinimumWidth(ui_50)
            self.layout.cmy_1_value.setMaximumWidth(ui_70)
            self.layout.cmy_2_value.setMinimumWidth(ui_50)
            self.layout.cmy_2_value.setMaximumWidth(ui_70)
            self.layout.cmy_3_value.setMinimumWidth(ui_50)
            self.layout.cmy_3_value.setMaximumWidth(ui_70)
            # CMYK
            self.layout.cmyk_1_label.setMinimumWidth(ui_15)
            self.layout.cmyk_1_label.setMaximumWidth(ui_15)
            self.layout.cmyk_2_label.setMinimumWidth(ui_15)
            self.layout.cmyk_2_label.setMaximumWidth(ui_15)
            self.layout.cmyk_3_label.setMinimumWidth(ui_15)
            self.layout.cmyk_3_label.setMaximumWidth(ui_15)
            self.layout.cmyk_4_label.setMinimumWidth(ui_15)
            self.layout.cmyk_4_label.setMaximumWidth(ui_15)
            self.layout.cmyk_1_value.setMinimumWidth(ui_50)
            self.layout.cmyk_1_value.setMaximumWidth(ui_70)
            self.layout.cmyk_2_value.setMinimumWidth(ui_50)
            self.layout.cmyk_2_value.setMaximumWidth(ui_70)
            self.layout.cmyk_3_value.setMinimumWidth(ui_50)
            self.layout.cmyk_3_value.setMaximumWidth(ui_70)
            self.layout.cmyk_4_value.setMinimumWidth(ui_35)
            self.layout.cmyk_4_value.setMaximumWidth(ui_55)
            self.layout.cmyk_4_lock.setMinimumWidth(ui_15)
            self.layout.cmyk_4_lock.setMaximumWidth(ui_15)
            # KKK
            self.layout.kkk_1_label.setMinimumWidth(ui_15)
            self.layout.kkk_1_label.setMaximumWidth(ui_15)
            self.layout.kkk_1_value.setMinimumWidth(ui_35)
            self.layout.kkk_1_value.setMaximumWidth(ui_55)
            self.layout.kkk_1_lock.setMinimumWidth(ui_15)
            self.layout.kkk_1_lock.setMaximumWidth(ui_15)
            # Percentage
            self.layout.percentage_bot_value.setMinimumWidth(ui_50)
            self.layout.percentage_bot_value.setMaximumWidth(ui_70)
        else:
            # HEX
            self.layout.hex_string.setMinimumWidth(zero)
            self.layout.hex_string.setMaximumWidth(zero)
            # SOF
            self.layout.eraser.setMinimumWidth(zero)
            self.layout.eraser.setMaximumWidth(zero)
            self.layout.sof_1_value.setMinimumWidth(zero)
            self.layout.sof_1_value.setMaximumWidth(zero)
            self.layout.sof_2_value.setMinimumWidth(zero)
            self.layout.sof_2_value.setMaximumWidth(zero)
            self.layout.sof_3_value.setMinimumWidth(zero)
            self.layout.sof_3_value.setMaximumWidth(zero)
            # AAA
            self.layout.aaa_1_label.setMinimumWidth(zero)
            self.layout.aaa_1_label.setMaximumWidth(zero)
            self.layout.aaa_1_value.setMinimumWidth(zero)
            self.layout.aaa_1_value.setMaximumWidth(zero)
            # RGB
            self.layout.rgb_1_label.setMinimumWidth(zero)
            self.layout.rgb_1_label.setMaximumWidth(zero)
            self.layout.rgb_2_label.setMinimumWidth(zero)
            self.layout.rgb_2_label.setMaximumWidth(zero)
            self.layout.rgb_3_label.setMinimumWidth(zero)
            self.layout.rgb_3_label.setMaximumWidth(zero)
            self.layout.rgb_1_value.setMinimumWidth(zero)
            self.layout.rgb_1_value.setMaximumWidth(zero)
            self.layout.rgb_2_value.setMinimumWidth(zero)
            self.layout.rgb_2_value.setMaximumWidth(zero)
            self.layout.rgb_3_value.setMinimumWidth(zero)
            self.layout.rgb_3_value.setMaximumWidth(zero)
            # ARD
            self.layout.ard_1_label.setMinimumWidth(zero)
            self.layout.ard_1_label.setMaximumWidth(zero)
            self.layout.ard_2_label.setMinimumWidth(zero)
            self.layout.ard_2_label.setMaximumWidth(zero)
            self.layout.ard_3_label.setMinimumWidth(zero)
            self.layout.ard_3_label.setMaximumWidth(zero)
            self.layout.ard_1_value.setMinimumWidth(zero)
            self.layout.ard_1_value.setMaximumWidth(zero)
            self.layout.ard_2_value.setMinimumWidth(zero)
            self.layout.ard_2_value.setMaximumWidth(zero)
            self.layout.ard_3_value.setMinimumWidth(zero)
            self.layout.ard_3_value.setMaximumWidth(zero)
            # HSV
            self.layout.hsv_1_label.setMinimumWidth(zero)
            self.layout.hsv_1_label.setMaximumWidth(zero)
            self.layout.hsv_2_label.setMinimumWidth(zero)
            self.layout.hsv_2_label.setMaximumWidth(zero)
            self.layout.hsv_3_label.setMinimumWidth(zero)
            self.layout.hsv_3_label.setMaximumWidth(zero)
            self.layout.hsv_1_value.setMinimumWidth(zero)
            self.layout.hsv_1_value.setMaximumWidth(zero)
            self.layout.hsv_2_value.setMinimumWidth(zero)
            self.layout.hsv_2_value.setMaximumWidth(zero)
            self.layout.hsv_3_value.setMinimumWidth(zero)
            self.layout.hsv_3_value.setMaximumWidth(zero)
            # HSL
            self.layout.hsl_1_label.setMinimumWidth(zero)
            self.layout.hsl_1_label.setMaximumWidth(zero)
            self.layout.hsl_2_label.setMinimumWidth(zero)
            self.layout.hsl_2_label.setMaximumWidth(zero)
            self.layout.hsl_3_label.setMinimumWidth(zero)
            self.layout.hsl_3_label.setMaximumWidth(zero)
            self.layout.hsl_1_value.setMinimumWidth(zero)
            self.layout.hsl_1_value.setMaximumWidth(zero)
            self.layout.hsl_2_value.setMinimumWidth(zero)
            self.layout.hsl_2_value.setMaximumWidth(zero)
            self.layout.hsl_3_value.setMinimumWidth(zero)
            self.layout.hsl_3_value.setMaximumWidth(zero)
            # HCY
            self.layout.hcy_1_label.setMinimumWidth(zero)
            self.layout.hcy_1_label.setMaximumWidth(zero)
            self.layout.hcy_2_label.setMinimumWidth(zero)
            self.layout.hcy_2_label.setMaximumWidth(zero)
            self.layout.hcy_3_label.setMinimumWidth(zero)
            self.layout.hcy_3_label.setMaximumWidth(zero)
            self.layout.hcy_1_value.setMinimumWidth(zero)
            self.layout.hcy_1_value.setMaximumWidth(zero)
            self.layout.hcy_2_value.setMinimumWidth(zero)
            self.layout.hcy_2_value.setMaximumWidth(zero)
            self.layout.hcy_3_value.setMinimumWidth(zero)
            self.layout.hcy_3_value.setMaximumWidth(zero)
            # YUV
            self.layout.yuv_1_label.setMinimumWidth(zero)
            self.layout.yuv_1_label.setMaximumWidth(zero)
            self.layout.yuv_2_label.setMinimumWidth(zero)
            self.layout.yuv_2_label.setMaximumWidth(zero)
            self.layout.yuv_3_label.setMinimumWidth(zero)
            self.layout.yuv_3_label.setMaximumWidth(zero)
            self.layout.yuv_1_value.setMinimumWidth(zero)
            self.layout.yuv_1_value.setMaximumWidth(zero)
            self.layout.yuv_2_value.setMinimumWidth(zero)
            self.layout.yuv_2_value.setMaximumWidth(zero)
            self.layout.yuv_3_value.setMinimumWidth(zero)
            self.layout.yuv_3_value.setMaximumWidth(zero)
            # RYB
            self.layout.ryb_1_label.setMinimumWidth(zero)
            self.layout.ryb_1_label.setMaximumWidth(zero)
            self.layout.ryb_2_label.setMinimumWidth(zero)
            self.layout.ryb_2_label.setMaximumWidth(zero)
            self.layout.ryb_3_label.setMinimumWidth(zero)
            self.layout.ryb_3_label.setMaximumWidth(zero)
            self.layout.ryb_1_value.setMinimumWidth(zero)
            self.layout.ryb_1_value.setMaximumWidth(zero)
            self.layout.ryb_2_value.setMinimumWidth(zero)
            self.layout.ryb_2_value.setMaximumWidth(zero)
            self.layout.ryb_3_value.setMinimumWidth(zero)
            self.layout.ryb_3_value.setMaximumWidth(zero)
            # CMY
            self.layout.cmy_1_label.setMinimumWidth(zero)
            self.layout.cmy_1_label.setMaximumWidth(zero)
            self.layout.cmy_2_label.setMinimumWidth(zero)
            self.layout.cmy_2_label.setMaximumWidth(zero)
            self.layout.cmy_3_label.setMinimumWidth(zero)
            self.layout.cmy_3_label.setMaximumWidth(zero)
            self.layout.cmy_1_value.setMinimumWidth(zero)
            self.layout.cmy_1_value.setMaximumWidth(zero)
            self.layout.cmy_2_value.setMinimumWidth(zero)
            self.layout.cmy_2_value.setMaximumWidth(zero)
            self.layout.cmy_3_value.setMinimumWidth(zero)
            self.layout.cmy_3_value.setMaximumWidth(zero)
            # CMYK
            self.layout.cmyk_1_label.setMinimumWidth(zero)
            self.layout.cmyk_1_label.setMaximumWidth(zero)
            self.layout.cmyk_2_label.setMinimumWidth(zero)
            self.layout.cmyk_2_label.setMaximumWidth(zero)
            self.layout.cmyk_3_label.setMinimumWidth(zero)
            self.layout.cmyk_3_label.setMaximumWidth(zero)
            self.layout.cmyk_4_label.setMinimumWidth(zero)
            self.layout.cmyk_4_label.setMaximumWidth(zero)
            self.layout.cmyk_1_value.setMinimumWidth(zero)
            self.layout.cmyk_1_value.setMaximumWidth(zero)
            self.layout.cmyk_2_value.setMinimumWidth(zero)
            self.layout.cmyk_2_value.setMaximumWidth(zero)
            self.layout.cmyk_3_value.setMinimumWidth(zero)
            self.layout.cmyk_3_value.setMaximumWidth(zero)
            self.layout.cmyk_4_value.setMinimumWidth(zero)
            self.layout.cmyk_4_value.setMaximumWidth(zero)
            self.layout.cmyk_4_lock.setMinimumWidth(zero)
            self.layout.cmyk_4_lock.setMaximumWidth(zero)
            # KKK
            self.layout.kkk_1_label.setMinimumWidth(zero)
            self.layout.kkk_1_label.setMaximumWidth(zero)
            self.layout.kkk_1_value.setMinimumWidth(zero)
            self.layout.kkk_1_value.setMaximumWidth(zero)
            self.layout.kkk_1_lock.setMinimumWidth(zero)
            self.layout.kkk_1_lock.setMaximumWidth(zero)
            # Percentage
            self.layout.percentage_bot_value.setMinimumWidth(zero)
            self.layout.percentage_bot_value.setMaximumWidth(zero)
        self.Ratio_Channels()
    def Menu_Hue_Shine(self):
        self.hue_shine = self.layout.hue_shine.isChecked()
        self.Pigment_Display()
    # Mixers
    def Menu_TIP(self):
        font = self.layout.tip.font()
        if self.layout.tip.isChecked():
            font.setBold(True)
            self.layout.tip_00.setMinimumHeight(ui_50)
            self.layout.tip_00.setMaximumHeight(ui_50)
            self.layout.cor_00.setMinimumHeight(ui_50)
            self.layout.cor_00.setMaximumHeight(ui_50)
            self.layout.cor_01.setMinimumHeight(ui_50)
            self.layout.cor_01.setMaximumHeight(ui_50)
            self.layout.cor_02.setMinimumHeight(ui_50)
            self.layout.cor_02.setMaximumHeight(ui_50)
            self.layout.cor_03.setMinimumHeight(ui_50)
            self.layout.cor_03.setMaximumHeight(ui_50)
            self.layout.cor_04.setMinimumHeight(ui_50)
            self.layout.cor_04.setMaximumHeight(ui_50)
            self.layout.cor_05.setMinimumHeight(ui_50)
            self.layout.cor_05.setMaximumHeight(ui_50)
            self.layout.cor_06.setMinimumHeight(ui_50)
            self.layout.cor_06.setMaximumHeight(ui_50)
            self.layout.cor_07.setMinimumHeight(ui_50)
            self.layout.cor_07.setMaximumHeight(ui_50)
            self.layout.cor_08.setMinimumHeight(ui_50)
            self.layout.cor_08.setMaximumHeight(ui_50)
            self.layout.cor_09.setMinimumHeight(ui_50)
            self.layout.cor_09.setMaximumHeight(ui_50)
            self.layout.cor_10.setMinimumHeight(ui_50)
            self.layout.cor_10.setMaximumHeight(ui_50)
            self.layout.cores.setContentsMargins(zero, unit, zero, unit)
        else:
            font.setBold(False)
            self.layout.tip_00.setMinimumHeight(zero)
            self.layout.tip_00.setMaximumHeight(zero)
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
    def Menu_TTS(self):
        font = self.layout.tts.font()
        self.menu_tts = self.layout.tts.isChecked()
        if self.menu_tts == True:
            font.setBold(True)
            self.layout.tts_l1.setMinimumHeight(ui_17)
            self.layout.tts_l1.setMaximumHeight(ui_47)
            self.layout.tint.setMinimumHeight(ui_15)
            self.layout.tint.setMaximumHeight(ui_15)
            self.layout.tone.setMinimumHeight(ui_15)
            self.layout.tone.setMaximumHeight(ui_15)
            self.layout.shade.setMinimumHeight(ui_15)
            self.layout.shade.setMaximumHeight(ui_15)
            self.layout.white.setMinimumHeight(ui_15)
            self.layout.white.setMaximumHeight(ui_15)
            self.layout.grey.setMinimumHeight(ui_15)
            self.layout.grey.setMaximumHeight(ui_15)
            self.layout.black.setMinimumHeight(ui_15)
            self.layout.black.setMaximumHeight(ui_15)
            self.layout.tint_tone_shade.setContentsMargins(zero, unit, zero, unit)
            self.layout.tint_tone_shade.setSpacing(unit)
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
            self.layout.tint_tone_shade.setContentsMargins(zero, zero, zero, zero)
            self.layout.tint_tone_shade.setSpacing(zero)
        self.layout.tts.setFont(font)
    def Menu_MIX(self):
        font = self.layout.mix.font()
        self.MIX_Shrink()
        self.menu_mix = self.layout.mix.isChecked()
        self.menu_mix_index = self.layout.mix_index.currentText()
        if self.menu_mix == False:
            font.setBold(False)
        if (self.menu_mix == True and self.menu_mix_index == "RGB"):
            font.setBold(True)
            self.layout.rgb_l1.setMinimumHeight(ui_15)
            self.layout.rgb_l1.setMaximumHeight(ui_15)
            self.layout.rgb_l2.setMinimumHeight(ui_15)
            self.layout.rgb_l2.setMaximumHeight(ui_15)
            self.layout.rgb_l3.setMinimumHeight(ui_15)
            self.layout.rgb_l3.setMaximumHeight(ui_15)
            self.layout.rgb_r1.setMinimumHeight(ui_15)
            self.layout.rgb_r1.setMaximumHeight(ui_15)
            self.layout.rgb_r2.setMinimumHeight(ui_15)
            self.layout.rgb_r2.setMaximumHeight(ui_15)
            self.layout.rgb_r3.setMinimumHeight(ui_15)
            self.layout.rgb_r3.setMaximumHeight(ui_15)
            self.layout.rgb_g1.setMinimumHeight(ui_15)
            self.layout.rgb_g1.setMaximumHeight(ui_15)
            self.layout.rgb_g2.setMinimumHeight(ui_15)
            self.layout.rgb_g2.setMaximumHeight(ui_15)
            self.layout.rgb_g3.setMinimumHeight(ui_15)
            self.layout.rgb_g3.setMaximumHeight(ui_15)
            self.layout.mixer_rgb.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_rgb.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "ARD"):
            font.setBold(True)
            self.layout.ard_l1.setMinimumHeight(ui_15)
            self.layout.ard_l1.setMaximumHeight(ui_15)
            self.layout.ard_l2.setMinimumHeight(ui_15)
            self.layout.ard_l2.setMaximumHeight(ui_15)
            self.layout.ard_l3.setMinimumHeight(ui_15)
            self.layout.ard_l3.setMaximumHeight(ui_15)
            self.layout.ard_r1.setMinimumHeight(ui_15)
            self.layout.ard_r1.setMaximumHeight(ui_15)
            self.layout.ard_r2.setMinimumHeight(ui_15)
            self.layout.ard_r2.setMaximumHeight(ui_15)
            self.layout.ard_r3.setMinimumHeight(ui_15)
            self.layout.ard_r3.setMaximumHeight(ui_15)
            self.layout.ard_g1.setMinimumHeight(ui_15)
            self.layout.ard_g1.setMaximumHeight(ui_15)
            self.layout.ard_g2.setMinimumHeight(ui_15)
            self.layout.ard_g2.setMaximumHeight(ui_15)
            self.layout.ard_g3.setMinimumHeight(ui_15)
            self.layout.ard_g3.setMaximumHeight(ui_15)
            self.layout.mixer_ard.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_ard.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "HSV"):
            font.setBold(True)
            self.layout.hsv_l1.setMinimumHeight(ui_15)
            self.layout.hsv_l1.setMaximumHeight(ui_15)
            self.layout.hsv_l2.setMinimumHeight(ui_15)
            self.layout.hsv_l2.setMaximumHeight(ui_15)
            self.layout.hsv_l3.setMinimumHeight(ui_15)
            self.layout.hsv_l3.setMaximumHeight(ui_15)
            self.layout.hsv_r1.setMinimumHeight(ui_15)
            self.layout.hsv_r1.setMaximumHeight(ui_15)
            self.layout.hsv_r2.setMinimumHeight(ui_15)
            self.layout.hsv_r2.setMaximumHeight(ui_15)
            self.layout.hsv_r3.setMinimumHeight(ui_15)
            self.layout.hsv_r3.setMaximumHeight(ui_15)
            self.layout.hsv_g1.setMinimumHeight(ui_15)
            self.layout.hsv_g1.setMaximumHeight(ui_15)
            self.layout.hsv_g2.setMinimumHeight(ui_15)
            self.layout.hsv_g2.setMaximumHeight(ui_15)
            self.layout.hsv_g3.setMinimumHeight(ui_15)
            self.layout.hsv_g3.setMaximumHeight(ui_15)
            self.layout.mixer_hsv.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_hsv.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "HSL"):
            font.setBold(True)
            self.layout.hsl_l1.setMinimumHeight(ui_15)
            self.layout.hsl_l1.setMaximumHeight(ui_15)
            self.layout.hsl_l2.setMinimumHeight(ui_15)
            self.layout.hsl_l2.setMaximumHeight(ui_15)
            self.layout.hsl_l3.setMinimumHeight(ui_15)
            self.layout.hsl_l3.setMaximumHeight(ui_15)
            self.layout.hsl_r1.setMinimumHeight(ui_15)
            self.layout.hsl_r1.setMaximumHeight(ui_15)
            self.layout.hsl_r2.setMinimumHeight(ui_15)
            self.layout.hsl_r2.setMaximumHeight(ui_15)
            self.layout.hsl_r3.setMinimumHeight(ui_15)
            self.layout.hsl_r3.setMaximumHeight(ui_15)
            self.layout.hsl_g1.setMinimumHeight(ui_15)
            self.layout.hsl_g1.setMaximumHeight(ui_15)
            self.layout.hsl_g2.setMinimumHeight(ui_15)
            self.layout.hsl_g2.setMaximumHeight(ui_15)
            self.layout.hsl_g3.setMinimumHeight(ui_15)
            self.layout.hsl_g3.setMaximumHeight(ui_15)
            self.layout.mixer_hsl.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_hsl.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "HCY"):
            font.setBold(True)
            self.layout.hcy_l1.setMinimumHeight(ui_15)
            self.layout.hcy_l1.setMaximumHeight(ui_15)
            self.layout.hcy_l2.setMinimumHeight(ui_15)
            self.layout.hcy_l2.setMaximumHeight(ui_15)
            self.layout.hcy_l3.setMinimumHeight(ui_15)
            self.layout.hcy_l3.setMaximumHeight(ui_15)
            self.layout.hcy_r1.setMinimumHeight(ui_15)
            self.layout.hcy_r1.setMaximumHeight(ui_15)
            self.layout.hcy_r2.setMinimumHeight(ui_15)
            self.layout.hcy_r2.setMaximumHeight(ui_15)
            self.layout.hcy_r3.setMinimumHeight(ui_15)
            self.layout.hcy_r3.setMaximumHeight(ui_15)
            self.layout.hcy_g1.setMinimumHeight(ui_15)
            self.layout.hcy_g1.setMaximumHeight(ui_15)
            self.layout.hcy_g2.setMinimumHeight(ui_15)
            self.layout.hcy_g2.setMaximumHeight(ui_15)
            self.layout.hcy_g3.setMinimumHeight(ui_15)
            self.layout.hcy_g3.setMaximumHeight(ui_15)
            self.layout.mixer_hcy.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_hcy.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "YUV"):
            font.setBold(True)
            self.layout.yuv_l1.setMinimumHeight(ui_15)
            self.layout.yuv_l1.setMaximumHeight(ui_15)
            self.layout.yuv_l2.setMinimumHeight(ui_15)
            self.layout.yuv_l2.setMaximumHeight(ui_15)
            self.layout.yuv_l3.setMinimumHeight(ui_15)
            self.layout.yuv_l3.setMaximumHeight(ui_15)
            self.layout.yuv_r1.setMinimumHeight(ui_15)
            self.layout.yuv_r1.setMaximumHeight(ui_15)
            self.layout.yuv_r2.setMinimumHeight(ui_15)
            self.layout.yuv_r2.setMaximumHeight(ui_15)
            self.layout.yuv_r3.setMinimumHeight(ui_15)
            self.layout.yuv_r3.setMaximumHeight(ui_15)
            self.layout.yuv_g1.setMinimumHeight(ui_15)
            self.layout.yuv_g1.setMaximumHeight(ui_15)
            self.layout.yuv_g2.setMinimumHeight(ui_15)
            self.layout.yuv_g2.setMaximumHeight(ui_15)
            self.layout.yuv_g3.setMinimumHeight(ui_15)
            self.layout.yuv_g3.setMaximumHeight(ui_15)
            self.layout.mixer_yuv.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_yuv.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "RYB"):
            font.setBold(True)
            self.layout.ryb_l1.setMinimumHeight(ui_15)
            self.layout.ryb_l1.setMaximumHeight(ui_15)
            self.layout.ryb_l2.setMinimumHeight(ui_15)
            self.layout.ryb_l2.setMaximumHeight(ui_15)
            self.layout.ryb_l3.setMinimumHeight(ui_15)
            self.layout.ryb_l3.setMaximumHeight(ui_15)
            self.layout.ryb_r1.setMinimumHeight(ui_15)
            self.layout.ryb_r1.setMaximumHeight(ui_15)
            self.layout.ryb_r2.setMinimumHeight(ui_15)
            self.layout.ryb_r2.setMaximumHeight(ui_15)
            self.layout.ryb_r3.setMinimumHeight(ui_15)
            self.layout.ryb_r3.setMaximumHeight(ui_15)
            self.layout.ryb_g1.setMinimumHeight(ui_15)
            self.layout.ryb_g1.setMaximumHeight(ui_15)
            self.layout.ryb_g2.setMinimumHeight(ui_15)
            self.layout.ryb_g2.setMaximumHeight(ui_15)
            self.layout.ryb_g3.setMinimumHeight(ui_15)
            self.layout.ryb_g3.setMaximumHeight(ui_15)
            self.layout.mixer_ryb.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_ryb.setSpacing(unit)
        if (self.menu_mix == True and self.menu_mix_index == "CMYK"):
            font.setBold(True)
            self.layout.cmyk_l1.setMinimumHeight(ui_15)
            self.layout.cmyk_l1.setMaximumHeight(ui_15)
            self.layout.cmyk_l2.setMinimumHeight(ui_15)
            self.layout.cmyk_l2.setMaximumHeight(ui_15)
            self.layout.cmyk_l3.setMinimumHeight(ui_15)
            self.layout.cmyk_l3.setMaximumHeight(ui_15)
            self.layout.cmyk_r1.setMinimumHeight(ui_15)
            self.layout.cmyk_r1.setMaximumHeight(ui_15)
            self.layout.cmyk_r2.setMinimumHeight(ui_15)
            self.layout.cmyk_r2.setMaximumHeight(ui_15)
            self.layout.cmyk_r3.setMinimumHeight(ui_15)
            self.layout.cmyk_r3.setMaximumHeight(ui_15)
            self.layout.cmyk_g1.setMinimumHeight(ui_15)
            self.layout.cmyk_g1.setMaximumHeight(ui_15)
            self.layout.cmyk_g2.setMinimumHeight(ui_15)
            self.layout.cmyk_g2.setMaximumHeight(ui_15)
            self.layout.cmyk_g3.setMinimumHeight(ui_15)
            self.layout.cmyk_g3.setMaximumHeight(ui_15)
            self.layout.mixer_cmyk.setContentsMargins(zero, unit, zero, unit)
            self.layout.mixer_cmyk.setSpacing(unit)
        self.layout.mix.setFont(font)
        self.Mixer_Display()
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
        self.layout.mixer_rgb.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_rgb.setSpacing(zero)
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
        self.layout.mixer_ard.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_ard.setSpacing(zero)
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
        self.layout.mixer_hsv.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_hsv.setSpacing(zero)
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
        self.layout.mixer_hsl.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_hsl.setSpacing(zero)
        # Mix HCY
        self.layout.hcy_l1.setMinimumHeight(zero)
        self.layout.hcy_l1.setMaximumHeight(zero)
        self.layout.hcy_l2.setMinimumHeight(zero)
        self.layout.hcy_l2.setMaximumHeight(zero)
        self.layout.hcy_l3.setMinimumHeight(zero)
        self.layout.hcy_l3.setMaximumHeight(zero)
        self.layout.hcy_r1.setMinimumHeight(zero)
        self.layout.hcy_r1.setMaximumHeight(zero)
        self.layout.hcy_r2.setMinimumHeight(zero)
        self.layout.hcy_r2.setMaximumHeight(zero)
        self.layout.hcy_r3.setMinimumHeight(zero)
        self.layout.hcy_r3.setMaximumHeight(zero)
        self.layout.hcy_g1.setMinimumHeight(zero)
        self.layout.hcy_g1.setMaximumHeight(zero)
        self.layout.hcy_g2.setMinimumHeight(zero)
        self.layout.hcy_g2.setMaximumHeight(zero)
        self.layout.hcy_g3.setMinimumHeight(zero)
        self.layout.hcy_g3.setMaximumHeight(zero)
        self.layout.mixer_hcy.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_hcy.setSpacing(zero)
        # Mix YUV
        self.layout.yuv_l1.setMinimumHeight(zero)
        self.layout.yuv_l1.setMaximumHeight(zero)
        self.layout.yuv_l2.setMinimumHeight(zero)
        self.layout.yuv_l2.setMaximumHeight(zero)
        self.layout.yuv_l3.setMinimumHeight(zero)
        self.layout.yuv_l3.setMaximumHeight(zero)
        self.layout.yuv_r1.setMinimumHeight(zero)
        self.layout.yuv_r1.setMaximumHeight(zero)
        self.layout.yuv_r2.setMinimumHeight(zero)
        self.layout.yuv_r2.setMaximumHeight(zero)
        self.layout.yuv_r3.setMinimumHeight(zero)
        self.layout.yuv_r3.setMaximumHeight(zero)
        self.layout.yuv_g1.setMinimumHeight(zero)
        self.layout.yuv_g1.setMaximumHeight(zero)
        self.layout.yuv_g2.setMinimumHeight(zero)
        self.layout.yuv_g2.setMaximumHeight(zero)
        self.layout.yuv_g3.setMinimumHeight(zero)
        self.layout.yuv_g3.setMaximumHeight(zero)
        self.layout.mixer_yuv.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_yuv.setSpacing(zero)
        # Mix RYB
        self.layout.ryb_l1.setMinimumHeight(zero)
        self.layout.ryb_l1.setMaximumHeight(zero)
        self.layout.ryb_l2.setMinimumHeight(zero)
        self.layout.ryb_l2.setMaximumHeight(zero)
        self.layout.ryb_l3.setMinimumHeight(zero)
        self.layout.ryb_l3.setMaximumHeight(zero)
        self.layout.ryb_r1.setMinimumHeight(zero)
        self.layout.ryb_r1.setMaximumHeight(zero)
        self.layout.ryb_r2.setMinimumHeight(zero)
        self.layout.ryb_r2.setMaximumHeight(zero)
        self.layout.ryb_r3.setMinimumHeight(zero)
        self.layout.ryb_r3.setMaximumHeight(zero)
        self.layout.ryb_g1.setMinimumHeight(zero)
        self.layout.ryb_g1.setMaximumHeight(zero)
        self.layout.ryb_g2.setMinimumHeight(zero)
        self.layout.ryb_g2.setMaximumHeight(zero)
        self.layout.ryb_g3.setMinimumHeight(zero)
        self.layout.ryb_g3.setMaximumHeight(zero)
        self.layout.mixer_ryb.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_ryb.setSpacing(zero)
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
        self.layout.mixer_cmyk.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_cmyk.setSpacing(zero)
    # Options
    def Menu_Luminosity(self):
        luminosity = self.layout.luminosity.currentText()
        if luminosity == "ITU-R BT.601":
            # Reference
            self.luminosity = "601"
            # Luma Coefficients
            self.luma_r = 0.299
            self.luma_b = 0.114
            self.luma_g = 1 - self.luma_r - self.luma_b # 0.587
            self.luma_pr = 1.402
            self.luma_pb = 1.772
            # Update
            self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
            self.aaa_1_slider.update()
        if luminosity == "ITU-R BT.709":
            # Reference
            self.luminosity = "709"
            # Luma Coefficients
            self.luma_r = 0.2126
            self.luma_b = 0.0722
            self.luma_g = 1 - self.luma_r - self.luma_b # 0.7152
            self.luma_pr = 1.5748
            self.luma_pb = 1.8556
            # Update
            self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
            self.aaa_1_slider.update()
    def Menu_Names(self):
        names = self.layout.names_display.isChecked()
        if names == True:
            self.names_display = True
            self.HEX_Display(str(self.layout.hex_string.text()))
        else:
            self.names_display = False
            self.layout.label.setText("")
    # UI
    def Menu_UI_1(self): # Channels
        if self.layout.ui_1.isChecked() == True:
            # Options 1
            self.layout.sof.setMinimumHeight(ui_menu)
            self.layout.sof.setMaximumHeight(ui_menu)
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
            self.layout.hcy.setMinimumHeight(ui_menu)
            self.layout.hcy.setMaximumHeight(ui_menu)
            self.layout.yuv.setMinimumHeight(ui_menu)
            self.layout.yuv.setMaximumHeight(ui_menu)
            self.layout.ryb.setMinimumHeight(ui_menu)
            self.layout.ryb.setMaximumHeight(ui_menu)
            self.layout.cmy.setMinimumHeight(ui_menu)
            self.layout.cmy.setMaximumHeight(ui_menu)
            self.layout.cmyk.setMinimumHeight(ui_menu)
            self.layout.cmyk.setMaximumHeight(ui_menu)
            self.layout.kkk.setMinimumHeight(ui_menu)
            self.layout.kkk.setMaximumHeight(ui_menu)
            # Options 2
            self.layout.har.setMinimumHeight(ui_menu)
            self.layout.har.setMaximumHeight(ui_menu)
            self.layout.cotd.setMinimumHeight(ui_menu)
            self.layout.cotd.setMaximumHeight(ui_menu)
            self.layout.pan.setMinimumHeight(ui_menu)
            self.layout.pan.setMaximumHeight(ui_menu)
            self.layout.tip.setMinimumHeight(ui_menu)
            self.layout.tip.setMaximumHeight(ui_menu)
            self.layout.tts.setMinimumHeight(ui_menu)
            self.layout.tts.setMaximumHeight(ui_menu)
            self.layout.mix.setMinimumHeight(ui_menu)
            self.layout.mix.setMaximumHeight(ui_menu)
            # Spacing
            self.layout.options_1.setContentsMargins(unit, zero, unit, zero)
            self.layout.options_2.setContentsMargins(unit, zero, unit, zero)
        else:
            # Options 1
            self.layout.sof.setMinimumHeight(zero)
            self.layout.sof.setMaximumHeight(zero)
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
            self.layout.hcy.setMinimumHeight(zero)
            self.layout.hcy.setMaximumHeight(zero)
            self.layout.yuv.setMinimumHeight(zero)
            self.layout.yuv.setMaximumHeight(zero)
            self.layout.ryb.setMinimumHeight(zero)
            self.layout.ryb.setMaximumHeight(zero)
            self.layout.cmy.setMinimumHeight(zero)
            self.layout.cmy.setMaximumHeight(zero)
            self.layout.cmyk.setMinimumHeight(zero)
            self.layout.cmyk.setMaximumHeight(zero)
            self.layout.kkk.setMinimumHeight(zero)
            self.layout.kkk.setMaximumHeight(zero)
            # Options 2
            self.layout.har.setMinimumHeight(zero)
            self.layout.har.setMaximumHeight(zero)
            self.layout.cotd.setMinimumHeight(zero)
            self.layout.cotd.setMaximumHeight(zero)
            self.layout.pan.setMinimumHeight(zero)
            self.layout.pan.setMaximumHeight(zero)
            self.layout.tip.setMinimumHeight(zero)
            self.layout.tip.setMaximumHeight(zero)
            self.layout.tts.setMinimumHeight(zero)
            self.layout.tts.setMaximumHeight(zero)
            self.layout.mix.setMinimumHeight(zero)
            self.layout.mix.setMaximumHeight(zero)
            # Spacing
            self.layout.options_1.setContentsMargins(zero, zero, zero, zero)
            self.layout.options_2.setContentsMargins(zero, zero, zero, zero)
        self.Adjust_Spacing()
        self.Ratio()
    def Menu_UI_2(self): # Option Menus
        if self.layout.ui_2.isChecked() == True:
            # Harmony
            self.layout.menu_harmony.setMinimumHeight(ui_20)
            self.layout.menu_harmony.setMaximumHeight(ui_20)
            self.layout.har_index.setMinimumHeight(ui_20)
            self.layout.har_index.setMaximumHeight(ui_20)
            self.layout.har_edit.setMinimumHeight(ui_20)
            self.layout.har_edit.setMaximumHeight(ui_20)
            # Panel
            self.layout.menu_panel.setMinimumHeight(ui_20)
            self.layout.menu_panel.setMaximumHeight(ui_20)
            self.layout.pan_index.setMinimumHeight(ui_20)
            self.layout.pan_index.setMaximumHeight(ui_20)
            self.layout.pan_secondary.setMinimumHeight(ui_20)
            self.layout.pan_secondary.setMaximumHeight(ui_20)
            self.layout.gam_space.setMinimumHeight(ui_20)
            self.layout.gam_space.setMaximumHeight(ui_20)
            self.layout.gam_shape.setMinimumHeight(ui_20)
            self.layout.gam_shape.setMaximumHeight(ui_20)
            self.layout.dot_set.setMinimumHeight(ui_20)
            self.layout.dot_set.setMaximumHeight(ui_20)
            self.layout.obj_index.setMinimumHeight(ui_20)
            self.layout.obj_index.setMaximumHeight(ui_20)
            self.layout.obj_set.setMinimumHeight(ui_20)
            self.layout.obj_set.setMaximumHeight(ui_20)
            # Channels
            self.layout.menu_values.setMinimumHeight(ui_20)
            self.layout.menu_values.setMaximumHeight(ui_20)
            self.layout.values.setMinimumHeight(ui_20)
            self.layout.values.setMaximumHeight(ui_20)
            self.layout.hue_shine.setMinimumHeight(ui_20)
            self.layout.hue_shine.setMaximumHeight(ui_20)
            # Mixer
            self.layout.menu_mixer.setMinimumHeight(ui_20)
            self.layout.menu_mixer.setMaximumHeight(ui_20)
            self.layout.mix_index.setMinimumHeight(ui_20)
            self.layout.mix_index.setMaximumHeight(ui_20)
            # Names
            self.layout.menu_names.setMinimumHeight(ui_20)
            self.layout.menu_names.setMaximumHeight(ui_20)
            self.layout.names_display.setMinimumHeight(ui_20)
            self.layout.names_display.setMaximumHeight(ui_20)
            self.layout.names_closest.setMinimumHeight(ui_20)
            self.layout.names_closest.setMaximumHeight(ui_20)
            # Mode
            self.layout.menu_mode.setMinimumHeight(ui_20)
            self.layout.menu_mode.setMaximumHeight(ui_20)
            self.layout.wheel_index.setMinimumHeight(ui_20)
            self.layout.wheel_index.setMaximumHeight(ui_20)
            self.layout.luminosity.setMinimumHeight(ui_20)
            self.layout.luminosity.setMaximumHeight(ui_20)
            # Spacing
            self.layout.options_3.setContentsMargins(10, 10, 10, 10)
            self.layout.options_3.setSpacing(6)
        else:
            # Harmony
            self.layout.menu_harmony.setMinimumHeight(zero)
            self.layout.menu_harmony.setMaximumHeight(zero)
            self.layout.har_index.setMinimumHeight(zero)
            self.layout.har_index.setMaximumHeight(zero)
            self.layout.har_edit.setMinimumHeight(zero)
            self.layout.har_edit.setMaximumHeight(zero)
            # Panel
            self.layout.menu_panel.setMinimumHeight(zero)
            self.layout.menu_panel.setMaximumHeight(zero)
            self.layout.pan_index.setMinimumHeight(zero)
            self.layout.pan_index.setMaximumHeight(zero)
            self.layout.pan_secondary.setMinimumHeight(zero)
            self.layout.pan_secondary.setMaximumHeight(zero)
            self.layout.gam_space.setMinimumHeight(zero)
            self.layout.gam_space.setMaximumHeight(zero)
            self.layout.gam_shape.setMinimumHeight(zero)
            self.layout.gam_shape.setMaximumHeight(zero)
            self.layout.dot_set.setMinimumHeight(zero)
            self.layout.dot_set.setMaximumHeight(zero)
            self.layout.obj_index.setMinimumHeight(zero)
            self.layout.obj_index.setMaximumHeight(zero)
            self.layout.obj_set.setMinimumHeight(zero)
            self.layout.obj_set.setMaximumHeight(zero)
            # Channels
            self.layout.menu_values.setMinimumHeight(zero)
            self.layout.menu_values.setMaximumHeight(zero)
            self.layout.values.setMinimumHeight(zero)
            self.layout.values.setMaximumHeight(zero)
            self.layout.hue_shine.setMinimumHeight(zero)
            self.layout.hue_shine.setMaximumHeight(zero)
            # Mixer
            self.layout.menu_mixer.setMinimumHeight(zero)
            self.layout.menu_mixer.setMaximumHeight(zero)
            self.layout.mix_index.setMinimumHeight(zero)
            self.layout.mix_index.setMaximumHeight(zero)
            # Names
            self.layout.menu_names.setMinimumHeight(zero)
            self.layout.menu_names.setMaximumHeight(zero)
            self.layout.names_display.setMinimumHeight(zero)
            self.layout.names_display.setMaximumHeight(zero)
            self.layout.names_closest.setMinimumHeight(zero)
            self.layout.names_closest.setMaximumHeight(zero)
            # Mode
            self.layout.menu_mode.setMinimumHeight(zero)
            self.layout.menu_mode.setMaximumHeight(zero)
            self.layout.wheel_index.setMinimumHeight(zero)
            self.layout.wheel_index.setMaximumHeight(zero)
            self.layout.luminosity.setMinimumHeight(zero)
            self.layout.luminosity.setMaximumHeight(zero)
            # Spacing
            self.layout.options_3.setContentsMargins(zero, zero, zero, zero)
            self.layout.options_3.setSpacing(zero)
        self.Adjust_Spacing()
        self.Ratio()
    # Support
    def Adjust_Spacing(self):
        # Read UI settings for Load
        self.chan_aaa = self.layout.aaa.isChecked()
        self.chan_rgb = self.layout.rgb.isChecked()
        self.chan_ard = self.layout.ard.isChecked()
        self.chan_hsv = self.layout.hsv.isChecked()
        self.chan_hsl = self.layout.hsl.isChecked()
        self.chan_hcy = self.layout.hcy.isChecked()
        self.chan_yuv = self.layout.yuv.isChecked()
        self.chan_ryb = self.layout.ryb.isChecked()
        self.chan_cmy = self.layout.cmy.isChecked()
        self.chan_cmyk = self.layout.cmyk.isChecked()
        self.chan_kkk = self.layout.kkk.isChecked()
        # Adjust Spacing for the Channels
        if (self.chan_aaa == True or self.chan_rgb == True or self.chan_ard == True or self.chan_hsv == True or self.chan_hsl == True or self.chan_hcy == True or self.chan_yuv == True or self.chan_ryb == True or self.chan_cmy == True or self.chan_cmyk == True or self.chan_kkk == True):
            ten = self.Percentage("TEN")
            # Style Sheet
            self.layout.percentage_top.setStyleSheet(ten)
            self.layout.percentage_bot.setStyleSheet(ten)
            # Dimensions
            self.layout.hex_string.setMinimumHeight(ui_menu)
            self.layout.hex_string.setMaximumHeight(ui_menu)
            self.layout.percentage_top.setMinimumHeight(ui_20)
            self.layout.percentage_top.setMaximumHeight(ui_20)
            self.layout.percentage_bot.setMinimumHeight(ui_5)
            self.layout.percentage_bot.setMaximumHeight(ui_5)
            self.layout.percentage_bot_value.setMinimumHeight(ui_5)
            self.layout.percentage_bot_value.setMaximumHeight(ui_5)
        if (self.chan_aaa == False and self.chan_rgb == False and self.chan_ard == False and self.chan_hsv == False and self.chan_hsl == False and self.chan_hcy == False and self.chan_yuv == False and self.chan_ryb == False and self.chan_cmy == False and self.chan_cmyk == False and self.chan_kkk == False):
            self.layout.percentage_top.setStyleSheet(bg_unseen)
            self.layout.percentage_bot.setStyleSheet(bg_unseen)
            self.layout.percentage_top.setMinimumHeight(zero)
            self.layout.percentage_top.setMaximumHeight(zero)
            self.layout.percentage_bot.setMinimumHeight(zero)
            self.layout.percentage_bot.setMaximumHeight(zero)
            self.layout.percentage_bot_value.setMinimumHeight(zero)
            self.layout.percentage_bot_value.setMaximumHeight(zero)
            self.layout.hex_string.setMinimumHeight(zero)
            self.layout.hex_string.setMaximumHeight(zero)
        # Options
        if (self.layout.ui_2.isChecked() == False and self.layout.ui_1.isChecked() == False):
            self.layout.pigmento_options_layout.setContentsMargins(zero, zero, zero, zero)
        else:
            self.layout.pigmento_options_layout.setContentsMargins(6, unit, 6, unit)
        # Compensate Absence of Panel with vertical_spacer
        if self.layout.pan.isChecked() == False:
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Update Everything
        self.update()
    # Start UP UI Shrink
    def Menu_Shrink(self):
        # Options
        self.Options_Height_Zero()
        self.Menu_Value()
        # Interior
        self.Channel_Height_Zero()
        self.Switches_Height_Zero()
        # Adjust
        self.Adjust_Spacing()
    def Options_Height_Zero(self):
        # Options 1
        self.layout.sof.setMinimumHeight(zero)
        self.layout.sof.setMaximumHeight(zero)
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
        self.layout.hcy.setMinimumHeight(zero)
        self.layout.hcy.setMaximumHeight(zero)
        self.layout.yuv.setMinimumHeight(zero)
        self.layout.yuv.setMaximumHeight(zero)
        self.layout.ryb.setMinimumHeight(zero)
        self.layout.ryb.setMaximumHeight(zero)
        self.layout.cmy.setMinimumHeight(zero)
        self.layout.cmy.setMaximumHeight(zero)
        self.layout.cmyk.setMinimumHeight(zero)
        self.layout.cmyk.setMaximumHeight(zero)
        self.layout.kkk.setMinimumHeight(zero)
        self.layout.kkk.setMaximumHeight(zero)
        # Options 2
        self.layout.har.setMinimumHeight(zero)
        self.layout.har.setMaximumHeight(zero)
        self.layout.cotd.setMinimumHeight(zero)
        self.layout.cotd.setMaximumHeight(zero)
        self.layout.pan.setMinimumHeight(zero)
        self.layout.pan.setMaximumHeight(zero)
        self.layout.tip.setMinimumHeight(zero)
        self.layout.tip.setMaximumHeight(zero)
        self.layout.tts.setMinimumHeight(zero)
        self.layout.tts.setMaximumHeight(zero)
        self.layout.mix.setMinimumHeight(zero)
        self.layout.mix.setMaximumHeight(zero)
        # Spacing
        self.layout.options_1.setContentsMargins(zero, zero, zero, zero)
        self.layout.options_2.setContentsMargins(zero, zero, zero, zero)
        # Harmony
        self.layout.menu_harmony.setMinimumHeight(zero)
        self.layout.menu_harmony.setMaximumHeight(zero)
        self.layout.har_index.setMinimumHeight(zero)
        self.layout.har_index.setMaximumHeight(zero)
        self.layout.har_edit.setMinimumHeight(zero)
        self.layout.har_edit.setMaximumHeight(zero)
        # Panel
        self.layout.menu_panel.setMinimumHeight(zero)
        self.layout.menu_panel.setMaximumHeight(zero)
        self.layout.pan_index.setMinimumHeight(zero)
        self.layout.pan_index.setMaximumHeight(zero)
        self.layout.pan_secondary.setMinimumHeight(zero)
        self.layout.pan_secondary.setMaximumHeight(zero)
        self.layout.gam_space.setMinimumHeight(zero)
        self.layout.gam_space.setMaximumHeight(zero)
        self.layout.gam_shape.setMinimumHeight(zero)
        self.layout.gam_shape.setMaximumHeight(zero)
        self.layout.dot_set.setMinimumHeight(zero)
        self.layout.dot_set.setMaximumHeight(zero)
        self.layout.obj_index.setMinimumHeight(zero)
        self.layout.obj_index.setMaximumHeight(zero)
        self.layout.obj_set.setMinimumHeight(zero)
        self.layout.obj_set.setMaximumHeight(zero)
        # Channels
        self.layout.menu_values.setMinimumHeight(zero)
        self.layout.menu_values.setMaximumHeight(zero)
        self.layout.values.setMinimumHeight(zero)
        self.layout.values.setMaximumHeight(zero)
        self.layout.hue_shine.setMinimumHeight(zero)
        self.layout.hue_shine.setMaximumHeight(zero)
        # Mixer
        self.layout.menu_mixer.setMinimumHeight(zero)
        self.layout.menu_mixer.setMaximumHeight(zero)
        self.layout.mix_index.setMinimumHeight(zero)
        self.layout.mix_index.setMaximumHeight(zero)
        # Names
        self.layout.menu_names.setMinimumHeight(zero)
        self.layout.menu_names.setMaximumHeight(zero)
        self.layout.names_display.setMinimumHeight(zero)
        self.layout.names_display.setMaximumHeight(zero)
        self.layout.names_closest.setMinimumHeight(zero)
        self.layout.names_closest.setMaximumHeight(zero)
        # Mode
        self.layout.menu_mode.setMinimumHeight(zero)
        self.layout.menu_mode.setMaximumHeight(zero)
        self.layout.wheel_index.setMinimumHeight(zero)
        self.layout.wheel_index.setMaximumHeight(zero)
        self.layout.luminosity.setMinimumHeight(zero)
        self.layout.luminosity.setMaximumHeight(zero)
        # Spacing
        self.layout.options_3.setContentsMargins(zero, zero, zero, zero)
        self.layout.options_3.setSpacing(zero)
    def Channel_Height_Zero(self):
        self.Menu_SOF()
        self.Menu_AAA()
        self.Menu_RGB()
        self.Menu_ARD()
        self.Menu_HSV()
        self.Menu_HSL()
        self.Menu_HCY()
        self.Menu_YUV()
        self.Menu_RYB()
        self.Menu_CMY()
        self.Menu_CMYK()
        self.Menu_KKK()
    def Switches_Height_Zero(self):
        # HAR
        self.harmony_rule = 0
        self.layout.color_1.setMinimumHeight(ui_30)
        self.layout.color_1.setMaximumHeight(ui_30)
        self.layout.color_2.setMinimumHeight(ui_30)
        self.layout.color_2.setMaximumHeight(ui_30)
        self.layout.harmony_1.setMinimumHeight(zero)
        self.layout.harmony_1.setMaximumHeight(zero)
        self.layout.harmony_2.setMinimumHeight(zero)
        self.layout.harmony_2.setMaximumHeight(zero)
        self.layout.harmony_3.setMinimumHeight(zero)
        self.layout.harmony_3.setMaximumHeight(zero)
        self.layout.harmony_4.setMinimumHeight(zero)
        self.layout.harmony_4.setMaximumHeight(zero)
        self.layout.harmony_5.setMinimumHeight(zero)
        self.layout.harmony_5.setMaximumHeight(zero)
        self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        # COTD
        self.layout.cotd_date.setMinimumHeight(zero)
        self.layout.cotd_date.setMaximumHeight(zero)
        self.layout.cotd1.setMinimumHeight(zero)
        self.layout.cotd1.setMaximumHeight(zero)
        self.layout.cotd2.setMinimumHeight(zero)
        self.layout.cotd2.setMaximumHeight(zero)
        self.layout.cotd3.setMinimumHeight(zero)
        self.layout.cotd3.setMaximumHeight(zero)
        self.layout.cotd4.setMinimumHeight(zero)
        self.layout.cotd4.setMaximumHeight(zero)
        self.layout.cotd5.setMinimumHeight(zero)
        self.layout.cotd5.setMaximumHeight(zero)
        self.layout.color_of_the_day.setContentsMargins(zero, zero, zero, zero)
        # PANEL
        self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.pan_secondary.setEnabled(False)
        # DOT
        self.layout.panel_dot_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.dot_1.setMinimumHeight(zero)
        self.layout.dot_1.setMaximumHeight(zero)
        self.layout.dot_2.setMinimumHeight(zero)
        self.layout.dot_2.setMaximumHeight(zero)
        self.layout.dot_3.setMinimumHeight(zero)
        self.layout.dot_3.setMaximumHeight(zero)
        self.layout.dot_4.setMinimumHeight(zero)
        self.layout.dot_4.setMaximumHeight(zero)
        self.layout.dot_swap.setMinimumHeight(zero)
        self.layout.dot_swap.setMaximumHeight(zero)
        self.layout.panel_dot_colors.setContentsMargins(zero, zero, zero, zero)
        self.layout.panel_dot_colors.setSpacing(0)
        # OBJECT
        self.layout.panel_obj_mix.setContentsMargins(zero, zero, zero, zero)
        self.layout.panel_obj_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_obj_colors.setContentsMargins(zero, zero, zero, zero)
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
        # TIP
        self.layout.tip_00.setMinimumHeight(zero)
        self.layout.tip_00.setMaximumHeight(zero)
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
        self.layout.tint_tone_shade.setContentsMargins(zero, zero, zero, zero)
        self.layout.tint_tone_shade.setSpacing(zero)
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
        self.layout.mixer_rgb.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_rgb.setSpacing(zero)
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
        self.layout.mixer_ard.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_ard.setSpacing(zero)
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
        self.layout.mixer_hsv.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_hsv.setSpacing(zero)
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
        self.layout.mixer_hsl.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_hsl.setSpacing(zero)
        # Mix HCY
        self.layout.hcy_l1.setMinimumHeight(zero)
        self.layout.hcy_l1.setMaximumHeight(zero)
        self.layout.hcy_l2.setMinimumHeight(zero)
        self.layout.hcy_l2.setMaximumHeight(zero)
        self.layout.hcy_l3.setMinimumHeight(zero)
        self.layout.hcy_l3.setMaximumHeight(zero)
        self.layout.hcy_r1.setMinimumHeight(zero)
        self.layout.hcy_r1.setMaximumHeight(zero)
        self.layout.hcy_r2.setMinimumHeight(zero)
        self.layout.hcy_r2.setMaximumHeight(zero)
        self.layout.hcy_r3.setMinimumHeight(zero)
        self.layout.hcy_r3.setMaximumHeight(zero)
        self.layout.hcy_g1.setMinimumHeight(zero)
        self.layout.hcy_g1.setMaximumHeight(zero)
        self.layout.hcy_g2.setMinimumHeight(zero)
        self.layout.hcy_g2.setMaximumHeight(zero)
        self.layout.hcy_g3.setMinimumHeight(zero)
        self.layout.hcy_g3.setMaximumHeight(zero)
        self.layout.mixer_hcy.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_hcy.setSpacing(zero)
        # Mix YUV
        self.layout.yuv_l1.setMinimumHeight(zero)
        self.layout.yuv_l1.setMaximumHeight(zero)
        self.layout.yuv_l2.setMinimumHeight(zero)
        self.layout.yuv_l2.setMaximumHeight(zero)
        self.layout.yuv_l3.setMinimumHeight(zero)
        self.layout.yuv_l3.setMaximumHeight(zero)
        self.layout.yuv_r1.setMinimumHeight(zero)
        self.layout.yuv_r1.setMaximumHeight(zero)
        self.layout.yuv_r2.setMinimumHeight(zero)
        self.layout.yuv_r2.setMaximumHeight(zero)
        self.layout.yuv_r3.setMinimumHeight(zero)
        self.layout.yuv_r3.setMaximumHeight(zero)
        self.layout.yuv_g1.setMinimumHeight(zero)
        self.layout.yuv_g1.setMaximumHeight(zero)
        self.layout.yuv_g2.setMinimumHeight(zero)
        self.layout.yuv_g2.setMaximumHeight(zero)
        self.layout.yuv_g3.setMinimumHeight(zero)
        self.layout.yuv_g3.setMaximumHeight(zero)
        self.layout.mixer_yuv.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_yuv.setSpacing(zero)
        # Mix RYB
        self.layout.ryb_l1.setMinimumHeight(zero)
        self.layout.ryb_l1.setMaximumHeight(zero)
        self.layout.ryb_l2.setMinimumHeight(zero)
        self.layout.ryb_l2.setMaximumHeight(zero)
        self.layout.ryb_l3.setMinimumHeight(zero)
        self.layout.ryb_l3.setMaximumHeight(zero)
        self.layout.ryb_r1.setMinimumHeight(zero)
        self.layout.ryb_r1.setMaximumHeight(zero)
        self.layout.ryb_r2.setMinimumHeight(zero)
        self.layout.ryb_r2.setMaximumHeight(zero)
        self.layout.ryb_r3.setMinimumHeight(zero)
        self.layout.ryb_r3.setMaximumHeight(zero)
        self.layout.ryb_g1.setMinimumHeight(zero)
        self.layout.ryb_g1.setMaximumHeight(zero)
        self.layout.ryb_g2.setMinimumHeight(zero)
        self.layout.ryb_g2.setMaximumHeight(zero)
        self.layout.ryb_g3.setMinimumHeight(zero)
        self.layout.ryb_g3.setMaximumHeight(zero)
        self.layout.mixer_ryb.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_ryb.setSpacing(zero)
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
        self.layout.mixer_cmyk.setContentsMargins(zero, zero, zero, zero)
        self.layout.mixer_cmyk.setSpacing(zero)

    #//
    #\\ Conversions / Trignometry (range 0-1) ##################################
    # Gray Contrast
    def gc(self, r, g, b):
        value = self.rgb_to_aaa(r, g, b)[0]
        if value <= 0.3:
            gc = ( 1 - value )
        elif value >= 0.7:
            gc = ( 1 - value )
        else:
            gc = ( value - 0.3 )
        return gc
    # AAA
    def rgb_to_aaa(self, r, g, b):
        aaa = (self.luma_r*r) + (self.luma_g*g) + (self.luma_b*b)
        return [aaa]
    # UVD
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
    def uvd_hexagon_origins(self, d):
        # Values
        w1 = 0.8660253882408142
        h1 = 0.5000000596046448
        h2 = 1
        diagonal = d * 3
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
            self.O6 = [0 + 0,           0 - (h2*delta1)]  # -1 exception to not be zero area
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
        self.REDAXIS = self.Math_2D_Points_Lines_Angle(10, 0, 0, 0, self.O45[0], self.O45[1])
    # ARD
    def uvd_to_ard(self, u, v, d):
        # Update Origin Points
        self.uvd_hexagon_origins(d)
        # Correct UV values
        u = round(u,15)
        v = round(v,15)
        # Angle
        if (u == 0 and v == 0):
            arc=0
            a=0
        else:
            arc = self.Math_2D_Points_Lines_Angle(u,v, 0,0, self.O45[0],self.O45[1]) # range 0 to 360
            a = arc / 360 # range 0 to 1
        # User Value
        user = self.Math_2D_Points_Distance(0, 0, u, v)
        # Total Value
        diagonal = d * 3
        if diagonal <= 0:
            a = self.angle_live
            total = 1
        elif (diagonal > 0 and diagonal <= 1):
            # Angles according to O45(RED) as Origin
            AR = 0 # RED
            AG = self.Math_2D_Points_Lines_Angle(self.O23[0], self.O23[1], 0, 0, self.O45[0], self.O45[1]) # GREEN
            AB = self.Math_2D_Points_Lines_Angle(self.O61[0], self.O61[1], 0, 0, self.O45[0], self.O45[1]) # BLUE
            # Certain
            if arc == AR:
                total = self.Math_2D_Points_Distance(0, 0, self.O45[0], self.O45[1])
            elif arc == AG:
                total = self.Math_2D_Points_Distance(0, 0, self.O23[0], self.O23[1])
            elif arc == AB:
                total = self.Math_2D_Points_Distance(0, 0, self.O61[0], self.O61[1])
            # Intervals
            elif (arc > AR and arc < AG):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O3[0], self.O3[1], self.O4[0], self.O4[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AG and arc < AB):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O1[0], self.O1[1], self.O2[0], self.O2[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AB or arc < AR):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O5[0], self.O5[1], self.O6[0], self.O6[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal > 1 and diagonal < 2):
            # Angles according to O45(RED) as Origin
            A1 = self.Math_2D_Points_Lines_Angle(self.O1[0], self.O1[1], 0, 0, self.O45[0], self.O45[1]) # O1
            A2 = self.Math_2D_Points_Lines_Angle(self.O2[0], self.O2[1], 0, 0, self.O45[0], self.O45[1]) # O2
            A3 = self.Math_2D_Points_Lines_Angle(self.O3[0], self.O3[1], 0, 0, self.O45[0], self.O45[1]) # O3
            A4 = self.Math_2D_Points_Lines_Angle(self.O4[0], self.O4[1], 0, 0, self.O45[0], self.O45[1]) # O4
            A5 = self.Math_2D_Points_Lines_Angle(self.O5[0], self.O5[1], 0, 0, self.O45[0], self.O45[1]) # O5
            A6 = self.Math_2D_Points_Lines_Angle(self.O6[0], self.O6[1], 0, 0, self.O45[0], self.O45[1]) # O6
            # Certain
            if arc == A1:
                total = self.Math_2D_Points_Distance(0, 0, self.O1[0], self.O1[1])
            elif arc == A2:
                total = self.Math_2D_Points_Distance(0, 0, self.O2[0], self.O2[1])
            elif arc == A3:
                total = self.Math_2D_Points_Distance(0, 0, self.O3[0], self.O3[1])
            elif arc == A4:
                total = self.Math_2D_Points_Distance(0, 0, self.O4[0], self.O4[1])
            elif arc == A5:
                total = self.Math_2D_Points_Distance(0, 0, self.O5[0], self.O5[1])
            elif arc == A6:
                total = self.Math_2D_Points_Distance(0, 0, self.O6[0], self.O6[1])
            # Intervals
            elif (arc > A4 and arc < A3): # 0
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O4[0], self.O4[1], self.O3[0], self.O3[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A3 and arc < A2): # 60
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O3[0], self.O3[1], self.O2[0], self.O2[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A2 and arc < A1): # 120
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O2[0], self.O2[1], self.O1[0], self.O1[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A1 and arc < A6): # 180
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A6 and arc < A5): # 240
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O6[0], self.O6[1], self.O5[0], self.O5[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A5 or arc < A4): # 300
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O5[0], self.O5[1], self.O4[0], self.O4[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal >= 2 and diagonal < 3):
            # Angles according to O45(RED) as Origin
            AY = self.Math_2D_Points_Lines_Angle(self.O34[0], self.O34[1], 0, 0, self.O45[0], self.O45[1]) # YELLOW
            AC = self.Math_2D_Points_Lines_Angle(self.O12[0], self.O12[1], 0, 0, self.O45[0], self.O45[1]) # CYAN
            AM = self.Math_2D_Points_Lines_Angle(self.O56[0], self.O56[1], 0, 0, self.O45[0], self.O45[1]) # MAGENTA
            # Certain
            if arc == AY:
                total = self.Math_2D_Points_Distance(0, 0, self.O34[0], self.O34[1])
            elif arc == AC:
                total = self.Math_2D_Points_Distance(0, 0, self.O12[0], self.O12[1])
            elif arc == AM:
                total = self.Math_2D_Points_Distance(0, 0, self.O56[0], self.O56[1])
            # Intervals
            elif (arc > AY and arc < AC):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O2[0], self.O2[1], self.O3[0], self.O3[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AC and arc < AM):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AM or arc < AY):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O4[0], self.O4[1], self.O5[0], self.O5[1], 0, 0, u, v))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif diagonal >= 3:
            a = self.angle_live
            total = 1
        # Percentual Value of the distance from the center to the outside
        try:
            ratio = user / total
        except:
            ratio = user
        r = ratio
        # Correct out of Bound values
        if a <= 0:
            a = 0
        if a >= 1:
            a = 1
        if r <= 0:
            r = 0
        if r >= 1:
            r = 1
        if d <= 0:
            d = 0
        if d >= 1:
            d = 1
        return [a, r, d]
    def ard_to_uvd(self, a, r, d):
        # Update Origin Points
        self.uvd_hexagon_origins(d)
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
            AR = self.Math_2D_Points_Lines_Angle(self.O45[0], self.O45[1], 0, 0, 1, 0) # RED
            AG = self.Math_2D_Points_Lines_Angle(self.O23[0], self.O23[1], 0, 0, 1, 0) # GREEN
            AB = self.Math_2D_Points_Lines_Angle(self.O61[0], self.O61[1], 0, 0, 1, 0) # BLUE
            # Certain
            if arc == AR: # RED
                total = self.Math_2D_Points_Distance(0, 0, self.O45[0], self.O45[1])
            elif arc == AG: # GREEN
                total = self.Math_2D_Points_Distance(0, 0, self.O23[0], self.O23[1])
            elif arc == AB: # BLUE
                total = self.Math_2D_Points_Distance(0, 0, self.O61[0], self.O61[1])
            # Intervals
            elif (arc > AR and arc < AG):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O3[0], self.O3[1], self.O4[0], self.O4[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AG or arc < AB):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O1[0], self.O1[1], self.O2[0], self.O2[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AB and arc < AR):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O5[0], self.O5[1], self.O6[0], self.O6[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal > 1 and diagonal < 2):
            # Angles according to +U(UVD) as Origin
            A1 = self.Math_2D_Points_Lines_Angle(self.O1[0], self.O1[1], 0, 0, 1, 0) # P1
            A2 = self.Math_2D_Points_Lines_Angle(self.O2[0], self.O2[1], 0, 0, 1, 0) # P2
            A3 = self.Math_2D_Points_Lines_Angle(self.O3[0], self.O3[1], 0, 0, 1, 0) # P3
            A4 = self.Math_2D_Points_Lines_Angle(self.O4[0], self.O4[1], 0, 0, 1, 0) # P4
            A5 = self.Math_2D_Points_Lines_Angle(self.O5[0], self.O5[1], 0, 0, 1, 0) # P5
            A6 = self.Math_2D_Points_Lines_Angle(self.O6[0], self.O6[1], 0, 0, 1, 0) # P6
            # Certain
            if arc == A1:
                total = self.Math_2D_Points_Distance(0, 0, self.O1[0], self.O1[1])
            elif arc == A2:
                total = self.Math_2D_Points_Distance(0, 0, self.O2[0], self.O2[1])
            elif arc == A3:
                total = self.Math_2D_Points_Distance(0, 0, self.O3[0], self.O3[1])
            elif arc == A4:
                total = self.Math_2D_Points_Distance(0, 0, self.O4[0], self.O4[1])
            elif arc == A5:
                total = self.Math_2D_Points_Distance(0, 0, self.O5[0], self.O5[1])
            elif arc == A6:
                total = self.Math_2D_Points_Distance(0, 0, self.O6[0], self.O6[1])
            # Intervals
            elif (arc > A1 and arc < A6): # 180
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A6 and arc < A5): # 240
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O6[0], self.O6[1], self.O5[0], self.O5[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A5 and arc < A4): # 300
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O5[0], self.O5[1], self.O4[0], self.O4[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A4 and arc < A3): # 0
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O4[0], self.O4[1], self.O3[0], self.O3[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            # Desambiguiation due to A2 crossing the Origin Axis
            elif A2 < 180:
                if (arc > A3 or arc < A2): # 60 OR
                    inter = list(self.Math_2D_Points_Lines_Intersection(self.O3[0], self.O3[1], self.O2[0], self.O2[1], 0, 0, ucos, vsin))
                    total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
                if (arc > A2 and arc < A1): # 120 AND
                    inter = list(self.Math_2D_Points_Lines_Intersection(self.O2[0], self.O2[1], self.O1[0], self.O1[1], 0, 0, ucos, vsin))
                    total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif A2 > 180:
                if (arc > A3 and arc < A2): # 60 AND
                    inter = list(self.Math_2D_Points_Lines_Intersection(self.O3[0], self.O3[1], self.O2[0], self.O2[1], 0, 0, ucos, vsin))
                    total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
                if (arc > A2 or arc < A1): # 120 OR
                    inter = list(self.Math_2D_Points_Lines_Intersection(self.O2[0], self.O2[1], self.O1[0], self.O1[1], 0, 0, ucos, vsin))
                    total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal >= 2 and diagonal < 3):
            # Angles according to +U(UVD) as Origin
            AY = self.Math_2D_Points_Lines_Angle(self.O34[0], self.O34[1], 0, 0, 1, 0) # YELLOW
            AC = self.Math_2D_Points_Lines_Angle(self.O12[0], self.O12[1], 0, 0, 1, 0) # CYAN
            AM = self.Math_2D_Points_Lines_Angle(self.O56[0], self.O56[1], 0, 0, 1, 0) # MAGENTA
            # Certain
            if arc == AY:
                total = self.Math_2D_Points_Distance(0, 0, self.O34[0], self.O34[1])
            elif arc == AC:
                total = self.Math_2D_Points_Distance(0, 0, self.O12[0], self.O12[1])
            elif arc == AM:
                total = self.Math_2D_Points_Distance(0, 0, self.O56[0], self.O56[1])
            # Intervals
            elif (arc > AY or arc < AC):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O2[0], self.O2[1], self.O3[0], self.O3[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AC and arc < AM):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O1[0], self.O1[1], self.O6[0], self.O6[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AM and arc < AY):
                inter = list(self.Math_2D_Points_Lines_Intersection(self.O4[0], self.O4[1], self.O5[0], self.O5[1], 0, 0, ucos, vsin))
                total = self.Math_2D_Points_Distance(0, 0, inter[0], inter[1])
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
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return [r, g, b]
    # Angle
    def rgb_to_angle(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        if minc == maxc:
            # return [0.0]
            return [self.angle_live]
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
        return [h]
    # HSV
    def rgb_to_hsv(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        v = maxc
        if minc == maxc:
            # return [0.0, 0.0, v]
            return [self.angle_live, 0.0, v]
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
    # HSL
    def rgb_to_hsl(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        l = ( minc + maxc ) / 2.0
        if minc == maxc:
            # return [0.0, 0.0, l]
            return [self.angle_live, 0.0, l]
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
        r = self.hue_to_rgb( m1, m2, h + ( 1 / 3 ) )
        g = self.hue_to_rgb( m1, m2, h )
        b = self.hue_to_rgb( m1, m2, h - ( 1 / 3 ) )
        return [r, g, b]
    def hue_to_rgb(self, m1, m2, h):
        if h < 0:
            h += 1
        if h > 1:
            h -= 1
        if ( 6 * h ) < 1:
            return ( m1 + ( m2 - m1 ) * 6 * h )
        if ( 2 * h ) < 1:
            return m2
        if ( 3 * h ) < 2:
            return ( m1 + ( m2 - m1 ) * ( ( 2 / 3 ) - h ) * 6 )
        return m1
    # HCY
    def rgb_to_hcy(self, r, g, b):
        y = self.luma_r*r + self.luma_g*g + self.luma_b*b
        p = max(r, g, b)
        n = min(r, g, b)
        d = p - n
        if n == p:
            h = self.angle_live
        elif p == r:
            h = (g - b)/d
            if h < 0:
                h += 6.0
        elif p == g:
            h = ((b - r)/d) + 2.0
        else:  # p==b
            h = ((r - g)/d) + 4.0
        h /= 6.0
        if (r == g == b or y == 0 or y == 1):
            c = 0.0
        else:
            c = max((y-n)/y, (p-y)/(1-y))
        return [h, c, y]
    def hcy_to_rgb(self, h, c, y):
        if c == 0:
            return [y, y, y]
        h %= 1.0
        h *= 6.0
        if h < 1:
            th = h
            tm = self.luma_r + self.luma_g * th
        elif h < 2:
            th = 2.0 - h
            tm = self.luma_g + self.luma_r * th
        elif h < 3:
            th = h - 2.0
            tm = self.luma_g + self.luma_b * th
        elif h < 4:
            th = 4.0 - h
            tm = self.luma_b + self.luma_g * th
        elif h < 5:
            th = h - 4.0
            tm = self.luma_b + self.luma_r * th
        else:
            th = 6.0 - h
            tm = self.luma_r + self.luma_b * th
        # Calculate the RGB components in sorted order
        if tm >= y:
            p = y + y*c*(1-tm)/tm
            o = y + y*c*(th-tm)/tm
            n = y - (y*c)
        else:
            p = y + (1-y)*c
            o = y + (1-y)*c*(th-tm)/(1-tm)
            n = y - (1-y)*c*tm/(1-tm)
        # Back to RGB order
        if h < 1:
            return [p, o, n]
        elif h < 2:
            return [o, p, n]
        elif h < 3:
            return [n, p, o]
        elif h < 4:
            return [n, o, p]
        elif h < 5:
            return [o, n, p]
        else:
            return [p, n, o]
    # YUV
    def rgb_to_yuv(self, r, g, b):
        y = self.luma_r*r + self.luma_g*g + self.luma_b*b
        pb = 0.5 + (0.5 * ((b - y) / (1 - self.luma_b))) # Chroma Blue - " 0.5 + " is the slider adjustment offset
        pr = 0.5 + (0.5 * ((r - y) / (1 - self.luma_r))) # Chroma Red - " 0.5 + " is the slider adjustment offset
        return [y, pb, pr]
    def yuv_to_rgb(self, y, pb, pr):
        pb = pb - 0.5 # slider adjustment offset
        pr = pr - 0.5 # slider adjustment offset
        r = self.luma_pr * pr + y
        g = (-0.344136286201022) * pb + (-0.714136286201022) * pr + y
        b = self.luma_pb * pb + y
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
    # RYB
    def rgb_to_ryb(self, r, g, b):
        red = r
        green = g
        blue = b
        white  = min(red, green, blue)
        red -= white
        green -= white
        blue -= white
        maxgreen = max(red, green, blue)
        yellow = min(red, green)
        red -= yellow
        green -= yellow
        if (blue > 0 and green > 0):
            blue /= 2
            green /= 2
        yellow += green
        blue += green
        maxyellow = max(red, yellow, blue)
        if maxyellow > 0:
            N = maxgreen / maxyellow
            red *= N
            yellow *= N
            blue *= N
        red += white
        yellow += white
        blue += white
        return [red, yellow, blue]
    def ryb_to_rgb(self, r, y, b):
        red = r
        yellow = y
        blue = b
        white = min(red, yellow, blue)
        red -= white
        yellow -= white
        blue -= white
        maxyellow = max(red, yellow, blue)
        green = min(yellow, blue)
        yellow -= green
        blue -= green
        if (blue > 0 and green > 0):
            blue *= 2
            green *= 2
        red += yellow
        green += yellow
        maxgreen = max(red, green, blue)
        if maxgreen > 0:
            N = maxyellow / maxgreen
            red *= N
            green *= N
            blue *= N
        red += white
        green += white
        blue += white
        return [red, green, blue]
    # RYB HUE Conversion
    def hcmy_to_hryb(self, hcmy):
        hcmy = self.Math_1D_Loop(hcmy)
        for i in range(len(cmy_step)):
            if hcmy == cmy_step[i]:
                hryb = ryb_step[i]
        for i in range(len(cmy_step)-1):
            if (hcmy > cmy_step[i] and hcmy < cmy_step[i+1]):
                var = (hcmy - cmy_step[i]) / (cmy_step[i+1] - cmy_step[i])
                hryb = ( ryb_step[i] + (ryb_step[i+1] - ryb_step[i]) * var )
        return hryb
    def hryb_to_hcmy(self, hryb):
        hcmy = self.Math_1D_Loop(hryb)
        for i in range(len(ryb_step)):
            if hryb == ryb_step[i]:
                hcmy = cmy_step[i]
        for i in range(len(ryb_step)-1):
            if (hryb > ryb_step[i] and hryb < ryb_step[i+1]):
                var = (hryb - ryb_step[i]) / (ryb_step[i+1] - ryb_step[i])
                hcmy = ( cmy_step[i] + (cmy_step[i+1] - cmy_step[i]) * var )
        return hcmy
    # CMY
    def rgb_to_cmy(self, r, g, b):
        c = 1 - r
        m = 1 - g
        y = 1 - b
        return [c, m, y]
    def cmy_to_rgb(self, c, m, y):
        r = 1 - c
        g = 1 - m
        b = 1 - y
        return [r, g, b]
    # CMYK
    def rgb_to_cmyk(self, r, g, b):
        q = max(r, g, b)
        if q == 0:
            c = 0
            m = 0
            y = 0
            k = 1
        else:
            if self.cmyk_lock == False:
                k = 1 - max(r, g, b) # Standard Transform
            else:
                k = self.cmyk_4 # Key is Locked
            c = ( 1 - r - k ) / ( 1 - k )
            m = ( 1 - g - k ) / ( 1 - k )
            y = ( 1 - b - k ) / ( 1 - k )
        return [c, m, y, k]
    def cmyk_to_rgb(self, c, m, y, k):
        r = ( 1 - c ) * ( 1 - k )
        g = ( 1 - m ) * ( 1 - k )
        b = ( 1 - y ) * ( 1 - k )
        return [r, g, b]
    # KELVIN
    def kkk_to_rgb(self, k):
        for i in range(len(kelvin_table)):
            # detect list entry
            if (k == kelvin_table[i][0] or (k > kelvin_table[i][0] and k < kelvin_table[i+1][0])):
                # 1 value for that step
                r = kelvin_table[i][1] / 255
                g = kelvin_table[i][2] / 255
                b = kelvin_table[i][3] / 255
        return [r, g, b]
    def kkk_to_lights(self, kkk):
        for i in range(len(standard_illuminants)):
            if (kkk == standard_illuminants[i][0] or (kkk > standard_illuminants[i][0] and kkk < standard_illuminants[i+1][0])):
                self.layout.label.setText(standard_illuminants[i][1])

    # Luminosity Locks
    def luma_lock_ard(self, hi, si, xi):
        # Lock Values
        hl = self.hsx_lock[0]
        sl = self.hsx_lock[1]
        xl = self.hsx_lock[2]
        rl, gl, bl = self.ard_to_rgb(hl, sl, xl)
        aaa_l = self.rgb_to_aaa(rl, gl, bl)[0]
        # Input Values
        ri, gi, bi = self.ard_to_rgb(hi, sl, xl)
        aaa_i = self.rgb_to_aaa(ri, gi, bi)[0]
        # Create the Perceptual Grey of the Input Color
        dri = ri - aaa_i
        dgi = gi - aaa_i
        dbi = bi - aaa_i
        # Shift the Color to the correct level of Perceptual Gray (First Solve)
        r = aaa_l + dri
        g = aaa_l + dgi
        b = aaa_l + dbi
        # Full Saturation State Descrimination
        sat = self.rgb_to_ard(r, g, b)[1]
        if sat >= 1:
            # HSV variation with maximum saturation
            rs, gs, bs = self.ard_to_rgb(hi, 1, xi)
            aaa_s = self.rgb_to_aaa(rs, gs, bs)[0]
            # Create the Perceptual Grey of the Saturated Color
            drs = rs - aaa_s
            dgs = gs - aaa_s
            dbs = bs - aaa_s
            # Shift the Color to the correct level of Perceptual Gray (Second Solve)
            r = aaa_l + drs
            g = aaa_l + dgs
            b = aaa_l + dbs
        # Correct Excess Values
        if r<=0:
            r=0
        if r>=1:
            r=1
        if g<=0:
            g=0
        if g>=1:
            g=1
        if b<=0:
            b=0
        if b>=1:
            b=1
        # Return Color Vector
        return [r, g, b]
    def luma_lock_hsv(self, hi, si, xi):
        # Lock Values
        hl = self.hsx_lock[0]
        sl = self.hsx_lock[1]
        xl = self.hsx_lock[2]
        rl, gl, bl = self.hsv_to_rgb(hl, sl, xl)
        aaa_l = self.rgb_to_aaa(rl, gl, bl)[0]
        # Input Values
        ri, gi, bi = self.hsv_to_rgb(hi, sl, xl)
        aaa_i = self.rgb_to_aaa(ri, gi, bi)[0]
        # Create the Perceptual Grey of the Input Color
        dri = ri - aaa_i
        dgi = gi - aaa_i
        dbi = bi - aaa_i
        # Shift the Color to the correct level of Perceptual Gray (First Solve)
        r = aaa_l + dri
        g = aaa_l + dgi
        b = aaa_l + dbi
        # Full Saturation State Descrimination
        sat = self.rgb_to_hsv(r, g, b)[1]
        if sat >= 1:
            # HSV variation with maximum saturation
            rs, gs, bs = self.hsv_to_rgb(hi, 1, xi)
            aaa_s = self.rgb_to_aaa(rs, gs, bs)[0]
            # Create the Perceptual Grey of the Saturated Color
            drs = rs - aaa_s
            dgs = gs - aaa_s
            dbs = bs - aaa_s
            # Shift the Color to the correct level of Perceptual Gray (Second Solve)
            r = aaa_l + drs
            g = aaa_l + dgs
            b = aaa_l + dbs
        # Correct Excess Values
        if r<=0:
            r=0
        if r>=1:
            r=1
        if g<=0:
            g=0
        if g>=1:
            g=1
        if b<=0:
            b=0
        if b>=1:
            b=1
        # Return Color Vector
        return [r, g, b]
    def luma_lock_hsl(self, hi, si, xi):
        # Lock Values
        hl = self.hsx_lock[0]
        sl = self.hsx_lock[1]
        xl = self.hsx_lock[2]
        rl, gl, bl = self.hsl_to_rgb(hl, sl, xl)
        aaa_l = self.rgb_to_aaa(rl, gl, bl)[0]
        # Input Values
        ri, gi, bi = self.hsl_to_rgb(hi, sl, xl)
        aaa_i = self.rgb_to_aaa(ri, gi, bi)[0]
        # Create the Perceptual Grey of the Input Color
        dri = ri - aaa_i
        dgi = gi - aaa_i
        dbi = bi - aaa_i
        # Shift the Color to the correct level of Perceptual Gray (First Solve)
        r = aaa_l + dri
        g = aaa_l + dgi
        b = aaa_l + dbi
        # Full Saturation State Descrimination
        sat = self.rgb_to_hsl(r, g, b)[1]
        if sat >= 1:
            # HSL variation with maximum saturation
            rs, gs, bs = self.hsl_to_rgb(hi, 1, xi)
            aaa_s = self.rgb_to_aaa(rs, gs, bs)[0]
            # Create the Perceptual Grey of the Saturated Color
            drs = rs - aaa_s
            dgs = gs - aaa_s
            dbs = bs - aaa_s
            # Shift the Color to the correct level of Perceptual Gray (Second Solve)
            r = aaa_l + drs
            g = aaa_l + dgs
            b = aaa_l + dbs
        # Correct Excess Values
        if r<=0:
            r=0
        if r>=1:
            r=1
        if g<=0:
            g=0
        if g>=1:
            g=1
        if b<=0:
            b=0
        if b>=1:
            b=1
        # Return Color Vector
        return [r, g, b]

    # Trignometry
    def Math_1D_Limit(self, var):
        if var <= 0:
            var = 0
        if var >= 1:
            var = 1
        return var
    def Math_1D_Loop(self, var):
        if var <= 0:
            var += 1
        if var >= 1:
            var -= 1
        return var
    def Math_1D_Lerp(self, v0, v1, t):
        return (v0+t*(v1-v0))
    def Math_2D_Points_Distance(self, x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def Math_2D_Points_Lines_Intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Math_2D_Points_Lines_Angle(self, x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle
    def Math_2D_Centroid_Triangle(self, a1, a2, b1, b2, c1, c2):
        cx = (a1+b1+c1)/3
        cy = (a2+b2+c2)/3
        return [cx, cy]
    def Math_2D_Centroid_Square(self, a1, a2, b1, b2, c1, c2, d1, d2):
        cx = (a1+b1+c1+d1)/4
        cy = (a2+b2+c2+d2)/4
        return [cx, cy]
    def Math_3D_Points_Distance(self, x1, y1, z1, x2, y2, z2):
        d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        return d

    #//
    #\\ Krita & Pigment ########################################################
    def Krita_TIMER(self):
        font = self.layout.check.font()
        self.timer_state = self.layout.check.checkState()
        if check_timer >= 1000:
            if self.timer_state == 0:
                font.setBold(False)
                self.layout.check.setText("OFF")
                self.timer.stop()
            elif self.timer_state == 1:
                font.setBold(True)
                self.layout.check.setText("ON")
                self.Krita_2_Pigment()
                self.timer.start()
            elif self.timer_state == 2:
                font.setBold(True)
                self.layout.check.setText("P>K")
                self.timer.stop()
        else:
            font.setBold(False)
            self.layout.check.setText("C<1")
            self.layout.check.setEnabled(False)
        self.layout.check.setFont(font)
    def Krita_2_Pigment(self):
        # Check current Theme color Value (0-255)
        krita_value = QApplication.palette().color(QPalette.Window).value()
        if self.theme_krita != krita_value:
            # Update System Variable
            self.theme_krita = krita_value
            # Contrast Gray Calculation
            # self.theme_pigment = self.gc(krita_value / 255) * 255
            self.theme_pigment = self.gc(krita_value/255, krita_value/255, krita_value/255) * 255
            # RGB Code of contrast Gray
            self.gray_natural = self.HEX_6string(self.theme_krita,self.theme_krita,self.theme_krita)
            self.gray_contrast = self.HEX_6string(self.theme_pigment,self.theme_pigment,self.theme_pigment)

        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            influence = self.aaa_lock == True or self.kkk_lock or self.harmony_rule != 0
            if (self.timer_state == 1 and influence == False):
                try:
                    # Check Eraser Mode ON or OFF
                    kritaEraserAction = Application.action("erase_action")
                    if kritaEraserAction.isChecked() == True:
                        self.layout.eraser.setStyleSheet(bg_eraser_on)
                    else:
                        self.layout.eraser.setStyleSheet(bg_alpha)

                    # Current Krita SOF
                    view = Krita.instance().activeWindow().activeView()
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

                    # Current Krita Color Foreground
                    color_foreground = Application.activeWindow().activeView().foregroundColor()
                    cfg_components = color_foreground.componentsOrdered()
                    cfg_color_model = color_foreground.colorModel()
                    cfg_color_depth = color_foreground.colorDepth()
                    cfg_color_profile = color_foreground.colorProfile()
                    # Current Krita Color Background
                    color_background = Application.activeWindow().activeView().backgroundColor()
                    cbg_components = color_background.componentsOrdered()
                    # Hold UVD D depth for autocorrect error
                    self.d_previous = self.uvd_3
                    # Update Pigmento if Colors Differ
                    if (cfg_color_model == "A" or cfg_color_model == "GRAYA"):
                        # Foreground and Background Colors
                        kac1 = cfg_components[0]
                        # Verify conditions to change Pigment
                        if self.aaa_1 != kac1:
                            if not kritaEraserAction.isChecked():
                                self.angle_live = 0
                                self.Color_APPLY("AAA", kac1, 0, 0, 0)
                                self.Pigment_Display_Release(0)
                    if cfg_color_model == "RGBA":
                        length = len(cfg_components)
                        if length == 2:
                            kac1 = cfg_components[0]
                            if self.aaa_1 != kac1:
                                if not kritaEraserAction.isChecked():
                                    # Check if NOT a GreyScale to memorize HUE
                                    self.angle_live = 0
                                    # Change Pigment
                                    self.Color_APPLY("AAA", kac1, 0, 0, 0)
                                    # Clean Percentage Label Display
                                    self.Pigment_Display_Release(0)
                        else:
                            # Foreground and Background Colors (Krita is in RGB)
                            kac1 = cfg_components[0] # Red
                            kac2 = cfg_components[1] # Green
                            kac3 = cfg_components[2] # Blue
                            # Verify conditions to change Pigment
                            if (self.rgb_1 != kac1 or self.rgb_2 != kac2 or self.rgb_3 != kac3):
                                if not kritaEraserAction.isChecked():
                                    # Check if NOT a GreyScale to memorize HUE
                                    if (kac1 != kac2 or kac2 != kac3 or kac3 != kac1):
                                        self.Color_ANGLE(kac1, kac2, kac3)
                                    # Change Pigment
                                    self.Color_APPLY("RGB", kac1, kac2, kac3, 0)
                                    # Clean Percentage Label Display
                                    self.Pigment_Display_Release(0)
                    if cfg_color_model == "CMYKA":
                        length = len(cfg_components)
                        if length == 2:
                            kac1 = cfg_components[0]
                            if self.aaa_1 != kac1:
                                if not kritaEraserAction.isChecked():
                                    self.angle_live = 0
                                    self.Color_APPLY("AAA", kac1, 0, 0, 0)
                                    self.Pigment_Display_Release(0)
                        else:
                            # Foreground and Background Colors
                            kac1 = cfg_components[0]
                            kac2 = cfg_components[1]
                            kac3 = cfg_components[2]
                            kac4 = cfg_components[3]
                            # Verify conditions to change Pigment
                            if self.cmyk_1 != kac1 or self.cmyk_2 != kac2 or self.cmyk_3 != kac3 or self.cmyk_4 != kac4:
                                if not kritaEraserAction.isChecked():
                                    if (kac1 != kac2 or kac2 != kac3 or kac3 != kac1):
                                        rgb = self.cmyk_to_rgb(kac1, kac2, kac3, kac4)
                                        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
                                    self.Color_APPLY("CMYK", kac1, kac2, kac3, kac4)
                                    self.Pigment_Display_Release(0)
                    if cfg_color_model == "XYZA":
                        pass
                    if cfg_color_model == "LABA":
                        pass
                    if cfg_color_model == "YCbCrA":
                        pass
                except:
                    pass
    def Pigment_2_Krita(self, release):
        # Operating System case sensitive Hold Color until the controler is Released for Linux Users
        if (self.OS == "winnt" or release == "RELEASE"):
            # Check if there is a valid Document Active
            if ((self.canvas() is not None) and (self.canvas().view() is not None)):
                if (self.timer_state == 1 or self.timer_state == 2):
                    # Check Eraser Mode ON or OFF
                    kritaEraserAction = Application.action("erase_action")
                    # Check Document Profile
                    doc = self.Document_Profile()
                    # Alpha mask
                    if (doc[0] == "A" or doc[0] == "GRAYA"):  # Gray with bg_alpha channel
                        # Kelvin AAA Calculations
                        k = self.rgb_to_aaa(self.kkk_1, self.kkk_2, self.kkk_3)
                        # Harmony Consideration for Active Color in AAA
                        if self.harmony_active == 0:
                            if self.kkk_lock == False:
                                kac1 = self.aaa_1
                            if self.kkk_lock == True:
                                kac1 = self.aaa_k1
                        else:
                            # Harmony CMYK Calculations
                            if self.harmony_active == 1:
                                if self.kkk_lock == False:
                                    har_1 = self.rgb_to_aaa(self.har_1[1], self.har_1[2], self.har_1[3])
                                    kac1 = har_1[0]
                                if self.kkk_lock == True:
                                    har_1 = self.rgb_to_aaa(self.har_k1[0], self.har_k1[1], self.har_k1[2])
                                    kac1 = har_1[0]
                            if self.harmony_active == 2:
                                if self.kkk_lock == False:
                                    har_2 = self.rgb_to_aaa(self.har_2[1], self.har_2[2], self.har_2[3])
                                    kac1 = har_2[0]
                                if self.kkk_lock == True:
                                    har_2 = self.rgb_to_aaa(self.har_k2[0], self.har_k2[1], self.har_k2[2])
                                    kac1 = har_2[0]
                            if self.harmony_active == 3:
                                if self.kkk_lock == False:
                                    har_3 = self.rgb_to_aaa(self.har_3[1], self.har_3[2], self.har_3[3])
                                    kac1 = har_3[0]
                                if self.kkk_lock == True:
                                    har_3 = self.rgb_to_aaa(self.har_k3[0], self.har_k3[1], self.har_k3[2])
                                    kac1 = har_3[0]
                            if self.harmony_active == 4:
                                if self.kkk_lock == False:
                                    har_4 = self.rgb_to_aaa(self.har_4[1], self.har_4[2], self.har_4[3])
                                    kac1 = har_4[0]
                                if self.kkk_lock == True:
                                    har_4 = self.rgb_to_aaa(self.har_k4[0], self.har_k4[1], self.har_k4[2])
                                    kac1 = har_4[0]
                            if self.harmony_active == 5:
                                if self.kkk_lock == False:
                                    har_5 = self.rgb_to_aaa(self.har_5[1], self.har_5[2], self.har_5[3])
                                    kac1 = har_5[0]
                                if self.kkk_lock == True:
                                    har_5 = self.rgb_to_aaa(self.har_k5[0], self.har_k5[1], self.har_k5[2])
                                    kac1 = har_5[0]
                        # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                        pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                        pigment_color.setComponents([kac1, 1.0])
                        Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                        # If Eraser, set it ON again
                        if kritaEraserAction.isChecked():
                            kritaEraserAction.trigger()
                    if doc[0] == "RGBA":  # RGB with bg_alpha channel (The actual order of channels is most often BGR!)
                        # Harmony Consideration for Active Color
                        if self.harmony_active == 0:
                            if self.kkk_lock == False:
                                kac1 = self.rgb_1
                                kac2 = self.rgb_2
                                kac3 = self.rgb_3
                            if self.kkk_lock == True:
                                kac1 = self.rgb_k1
                                kac2 = self.rgb_k2
                                kac3 = self.rgb_k3
                        if self.harmony_active == 1:
                            if self.kkk_lock == False:
                                kac1 = self.har_1[1]
                                kac2 = self.har_1[2]
                                kac3 = self.har_1[3]
                            if self.kkk_lock == True:
                                kac1 = self.har_1[1] * self.kkk_1
                                kac2 = self.har_1[2] * self.kkk_2
                                kac3 = self.har_1[3] * self.kkk_3
                        if self.harmony_active == 2:
                            if self.kkk_lock == False:
                                kac1 = self.har_2[1]
                                kac2 = self.har_2[2]
                                kac3 = self.har_2[3]
                            if self.kkk_lock == True:
                                kac1 = self.har_2[1] * self.kkk_1
                                kac2 = self.har_2[2] * self.kkk_2
                                kac3 = self.har_2[3] * self.kkk_3
                        if self.harmony_active == 3:
                            if self.kkk_lock == False:
                                kac1 = self.har_3[1]
                                kac2 = self.har_3[2]
                                kac3 = self.har_3[3]
                            if self.kkk_lock == True:
                                kac1 = self.har_3[1] * self.kkk_1
                                kac2 = self.har_3[2] * self.kkk_2
                                kac3 = self.har_3[3] * self.kkk_3
                        if self.harmony_active == 4:
                            if self.kkk_lock == False:
                                kac1 = self.har_4[1]
                                kac2 = self.har_4[2]
                                kac3 = self.har_4[3]
                            if self.kkk_lock == True:
                                kac1 = self.har_4[1] * self.kkk_1
                                kac2 = self.har_4[2] * self.kkk_2
                                kac3 = self.har_4[3] * self.kkk_3
                        if self.harmony_active == 5:
                            if self.kkk_lock == False:
                                kac1 = self.har_5[1]
                                kac2 = self.har_5[2]
                                kac3 = self.har_5[3]
                            if self.kkk_lock == True:
                                kac1 = self.har_5[1] * self.kkk_1
                                kac2 = self.har_5[2] * self.kkk_2
                                kac3 = self.har_5[3] * self.kkk_3
                        # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                        pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                        if (doc[1] == "U8" or doc[1] == "U16"):
                            pigment_color.setComponents([kac3, kac2, kac1, 1.0])
                        if (doc[1] == "F16" or doc[1] == "F32"):
                            pigment_color.setComponents([kac1, kac2, kac3, 1.0])
                        Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                        # If Eraser, set it ON again
                        if kritaEraserAction.isChecked():
                            kritaEraserAction.trigger()
                    if doc[0] == "CMYKA":  # CMYK with bg_alpha channel
                        # Kelvin CMYK Calculations
                        kkkk = self.rgb_to_cmyk(self.kkk_1, self.kkk_2, self.kkk_3)
                        # Harmony Consideration for Active Color in CMYK
                        if self.harmony_active == 0:
                            if self.kkk_lock == False:
                                kac1 = self.cmyk_1
                                kac2 = self.cmyk_2
                                kac3 = self.cmyk_3
                                kac4 = self.cmyk_4
                            if self.kkk_lock == True:
                                kac1 = self.cmyk_k1
                                kac2 = self.cmyk_k2
                                kac3 = self.cmyk_k3
                                kac4 = self.cmyk_k4
                        else:
                            # Harmony CMYK Calculations
                            if self.harmony_active == 1:
                                if self.kkk_lock == False:
                                    har_1 = self.rgb_to_cmyk(self.har_1[1], self.har_1[2], self.har_1[3])
                                    kac1 = har_1[0]
                                    kac2 = har_1[1]
                                    kac3 = har_1[2]
                                    kac4 = har_1[3]
                                if self.kkk_lock == True:
                                    har_1 = self.rgb_to_cmyk(self.har_k1[0], self.har_k1[1], self.har_k1[2])
                                    kac1 = har_1[0]
                                    kac2 = har_1[1]
                                    kac3 = har_1[2]
                                    kac4 = har_1[3]
                            if self.harmony_active == 2:
                                if self.kkk_lock == False:
                                    har_2 = self.rgb_to_cmyk(self.har_2[1], self.har_2[2], self.har_2[3])
                                    kac1 = har_2[0]
                                    kac2 = har_2[1]
                                    kac3 = har_2[2]
                                    kac4 = har_2[3]
                                if self.kkk_lock == True:
                                    har_2 = self.rgb_to_cmyk(self.har_k2[0], self.har_k2[1], self.har_k2[2])
                                    kac1 = har_2[0]
                                    kac2 = har_2[1]
                                    kac3 = har_2[2]
                                    kac4 = har_2[3]
                            if self.harmony_active == 3:
                                if self.kkk_lock == False:
                                    har_3 = self.rgb_to_cmyk(self.har_3[1], self.har_3[2], self.har_3[3])
                                    kac1 = har_3[0]
                                    kac2 = har_3[1]
                                    kac3 = har_3[2]
                                    kac4 = har_3[3]
                                if self.kkk_lock == True:
                                    har_3 = self.rgb_to_cmyk(self.har_k3[0], self.har_k3[1], self.har_k3[2])
                                    kac1 = har_3[0]
                                    kac2 = har_3[1]
                                    kac3 = har_3[2]
                                    kac4 = har_3[3]
                            if self.harmony_active == 4:
                                if self.kkk_lock == False:
                                    har_4 = self.rgb_to_cmyk(self.har_4[1], self.har_4[2], self.har_4[3])
                                    kac1 = har_4[0]
                                    kac2 = har_4[1]
                                    kac3 = har_4[2]
                                    kac4 = har_4[3]
                                if self.kkk_lock == True:
                                    har_4 = self.rgb_to_cmyk(self.har_k4[0], self.har_k4[1], self.har_k4[2])
                                    kac1 = har_4[0]
                                    kac2 = har_4[1]
                                    kac3 = har_4[2]
                                    kac4 = har_4[3]
                            if self.harmony_active == 5:
                                if self.kkk_lock == False:
                                    har_5 = self.rgb_to_cmyk(self.har_5[1], self.har_5[2], self.har_5[3])
                                    kac1 = har_5[0]
                                    kac2 = har_5[1]
                                    kac3 = har_5[2]
                                    kac4 = har_5[3]
                                if self.kkk_lock == True:
                                    har_5 = self.rgb_to_cmyk(self.har_k5[0], self.har_k5[1], self.har_k5[2])
                                    kac1 = har_5[0]
                                    kac2 = har_5[1]
                                    kac3 = har_5[2]
                                    kac4 = har_5[3]
                        # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                        pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                        pigment_color.setComponents([kac1, kac2, kac3, kac4, 1.0])
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
    #\\ Color Paths ############################################################
    # Convert with Input
    def Color_ANGLE(self, r, g, b):
        # CMY
        hue = self.rgb_to_angle(r,g,b)
        self.angle_live = hue[0]
    def Color_APPLY(self, mode, val1, val2, val3, val4):
        #\\ Convert Something to RGB
        if mode == "AAA":
            aaa = [val1]
            rgb = [aaa[0], aaa[1], aaa[2]]
        if (mode == "RGB" or mode == "LOAD"):
            rgb = [val1, val2, val3]
        if mode == "UVD":
            uvd = [val1, val2, val3]
            rgb = self.uvd_to_rgb(uvd[0], uvd[1], uvd[2])
        if mode == "ARD":
            ard = [val1, val2, val3]
            rgb = self.ard_to_rgb(ard[0], ard[1], ard[2])
            self.angle_live = val1
        if mode == "HSV":
            hsv = [val1, val2, val3]
            rgb = self.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
            self.angle_live = val1
        if mode == "HSL":
            hsl = [val1, val2, val3]
            rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
            self.angle_live = val1
        if mode == "HCY":
            hcy = [val1, val2, val3]
            rgb = self.hcy_to_rgb(hcy[0], hcy[1], hcy[2])
            self.angle_live = val1
        if mode == "YUV":
            yuv = [val1, val2, val3]
            rgb = self.yuv_to_rgb(yuv[0], yuv[1], yuv[2])
        if mode == "RYB":
            ryb = [val1, val2, val3]
            rgb = self.ryb_to_rgb(ryb[0], ryb[1], ryb[2])
        if mode == "CMY":
            cmy = [val1, val2, val3]
            rgb = self.cmy_to_rgb(cmy[0], cmy[1], cmy[2])
        if mode == "CMYK":
            cmyk = [val1, val2, val3, val4]
            rgb = self.cmyk_to_rgb(cmyk[0], cmyk[1], cmyk[2], cmyk[3])
        #//
        #\\ Convert RGB to Other
        if mode != "AAA":
            aaa = self.rgb_to_aaa(rgb[0], rgb[1], rgb[2])
        if (mode != "RGB" or mode != "LOAD"):
            pass
        if mode != "UVD":
            uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
        if mode != "ARD":
            conv = self.rgb_to_ard(rgb[0], rgb[1], rgb[2])
            if (mode == "HSV" or mode == "HSL" or mode == "HCY"):
                ard = [conv[0], conv[1], conv[2]]
            else:
                ard = [self.angle_live, conv[1], conv[2]]
        if mode != "HSV":
            conv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            if (mode == "ARD" or mode == "HSL" or mode == "HCY"):
                hsv = [conv[0], conv[1], conv[2]]
            else:
                hsv = [self.angle_live, conv[1], conv[2]]
        if mode != "HSL":
            conv = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
            if (mode == "ARD" or mode == "HSV" or mode == "HCY"):
                hsl = [conv[0], conv[1], conv[2]]
            else:
                hsl = [self.angle_live, conv[1], conv[2]]
        if mode != "HCY":
            conv = self.rgb_to_hcy(rgb[0], rgb[1], rgb[2])
            if (mode == "ARD" or mode == "HSV" or mode == "HSL"):
                hcy = [conv[0], conv[1], conv[2]]
            else:
                hcy = [self.angle_live, conv[1], conv[2]]
        if mode != "YUV":
            yuv = self.rgb_to_yuv(rgb[0], rgb[1], rgb[2])
        if mode != "RYB":
            ryb = self.rgb_to_ryb(rgb[0], rgb[1], rgb[2])
        if mode != "CMY":
            cmy = self.rgb_to_cmy(rgb[0], rgb[1], rgb[2])
        if mode != "CMYK":
            cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        if mode != "KKK":
            kkk = self.kkk_to_rgb(self.kkk_0)
            self.kkk_1 = kkk[0]
            self.kkk_2 = kkk[1]
            self.kkk_3 = kkk[2]
        #//
        #\\ Variables
        # Alpha
        self.aaa_1 = aaa[0]
        # RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # ARD
        self.ard_1 = ard[0]
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        condition = self.uvd_3 - self.d_previous
        if (condition > -u_RDL and condition < u_RDL):
            self.uvd_3 = self.d_previous
            self.ard_3 = self.d_previous
        # HSV
        self.hsv_1 = hsv[0]
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # HSL
        self.hsl_1 = hsl[0]
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # HCY
        self.hcy_1 = hcy[0]
        self.hcy_2 = hcy[1]
        self.hcy_3 = hcy[2]
        # YUV
        self.yuv_1 = yuv[0]
        self.yuv_2 = yuv[1]
        self.yuv_3 = yuv[2]
        # RYB
        self.ryb_1 = ryb[0]
        self.ryb_2 = ryb[1]
        self.ryb_3 = ryb[2]
        # CMY
        self.cmy_1 = cmy[0]
        self.cmy_2 = cmy[1]
        self.cmy_3 = cmy[2]
        # CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Kelvin
        if self.kkk_lock == True:
            # RGB Kelvin
            self.rgb_k1 = self.rgb_1 * kkk[0]
            self.rgb_k2 = self.rgb_2 * kkk[1]
            self.rgb_k3 = self.rgb_3 * kkk[2]
            # AAA Kelvin
            aaa = self.rgb_to_aaa(self.rgb_k1, self.rgb_k2, self.rgb_k3)
            self.aaa_k1 = aaa[0]
            # CMYK Kelvin
            cmyk = self.rgb_to_cmyk(self.rgb_k1, self.rgb_k2, self.rgb_k3)
            self.cmyk_k1 = cmyk[0]
            self.cmyk_k2 = cmyk[1]
            self.cmyk_k3 = cmyk[2]
            self.cmyk_k4 = cmyk[3]
        #//
        #\\ Pigment Update Values
        self.Pigment_Harmony(mode)
        self.Pigment_Sync(0)
        self.Pigment_2_Krita("HOLD")
        self.Pigment_Display()
        self.Mixer_Display()
        #//
    # Convert with Reference
    def Pigment_Convert(self, mode, ignore):
        #\\ Convert Something to RGB
        if mode == "AAA":
            self.aaa_1 = self.layout.aaa_1_value.value() / k_AAA
            aaa = [self.aaa_1]
            rgb = [self.aaa_1, self.aaa_1, self.aaa_1]
        if mode == "RGB":
            self.rgb_1 = self.layout.rgb_1_value.value() / k_RGB
            self.rgb_2 = self.layout.rgb_2_value.value() / k_RGB
            self.rgb_3 = self.layout.rgb_3_value.value() / k_RGB
            rgb = [self.rgb_1, self.rgb_2, self.rgb_3]
        if mode == "ARD":
            self.ard_1 = self.layout.ard_1_value.value() / k_ANG
            self.ard_2 = self.layout.ard_2_value.value() / k_RDL
            self.ard_3 = self.layout.ard_3_value.value() / k_RDL
            rgb = self.ard_to_rgb(self.ard_1, self.ard_2, self.ard_3)
            ard = [self.ard_1, self.ard_2, self.ard_3]
            self.angle_live = self.ard_1
        if mode == "HSV":
            self.hsv_1 = self.layout.hsv_1_value.value() / k_HUE
            self.hsv_2 = self.layout.hsv_2_value.value() / k_SVL
            self.hsv_3 = self.layout.hsv_3_value.value() / k_SVL
            rgb = self.hsv_to_rgb(self.hsv_1, self.hsv_2, self.hsv_3)
            hsv = [self.hsv_1, self.hsv_2, self.hsv_3]
            self.angle_live = self.hsv_1
        if mode == "HSL":
            self.hsl_1 = self.layout.hsl_1_value.value() / k_HUE
            self.hsl_2 = self.layout.hsl_2_value.value() / k_SVL
            self.hsl_3 = self.layout.hsl_3_value.value() / k_SVL
            rgb = self.hsl_to_rgb(self.hsl_1, self.hsl_2, self.hsl_3)
            hsl = [self.hsl_1, self.hsl_2, self.hsl_3]
            self.angle_live = self.hsl_1
        if mode == "HCY":
            self.hcy_1 = self.layout.hcy_1_value.value() / k_HUE
            self.hcy_2 = self.layout.hcy_2_value.value() / k_SVL
            self.hcy_3 = self.layout.hcy_3_value.value() / k_SVL
            rgb = self.hcy_to_rgb(self.hcy_1, self.hcy_2, self.hcy_3)
            hcy = [self.hcy_1, self.hcy_2, self.hcy_3]
            self.angle_live = self.hcy_1
        if mode == "YUV":
            self.yuv_1 = self.layout.yuv_1_value.value() / k_Y
            self.yuv_2 = self.layout.yuv_2_value.value() / k_U
            self.yuv_3 = self.layout.yuv_3_value.value() / k_V
            yuv = [self.yuv_1, self.yuv_2, self.yuv_3]
            rgb = self.yuv_to_rgb(self.yuv_1, self.yuv_2, self.yuv_3)
        if mode == "RYB":
            self.ryb_1 = self.layout.ryb_1_value.value() / k_RYB
            self.ryb_2 = self.layout.ryb_2_value.value() / k_RYB
            self.ryb_3 = self.layout.ryb_3_value.value() / k_RYB
            ryb = [self.ryb_1, self.ryb_2, self.ryb_3]
            rgb = self.ryb_to_rgb(self.ryb_1, self.ryb_2, self.ryb_3)
        if mode == "CMY":
            self.cmy_1 = self.layout.cmy_1_value.value() / k_CMY
            self.cmy_2 = self.layout.cmy_2_value.value() / k_CMY
            self.cmy_3 = self.layout.cmy_3_value.value() / k_CMY
            rgb = self.cmy_to_rgb(self.cmy_1, self.cmy_2, self.cmy_3)
            cmy = [self.cmy_1, self.cmy_2, self.cmy_3]
        if mode == "CMYK":
            self.cmyk_1 = self.layout.cmyk_1_value.value() / k_CMYK
            self.cmyk_2 = self.layout.cmyk_2_value.value() / k_CMYK
            self.cmyk_3 = self.layout.cmyk_3_value.value() / k_CMYK
            self.cmyk_4 = self.layout.cmyk_4_value.value() / k_CMYK
            rgb = self.cmyk_to_rgb(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
            cmyk = [self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        if mode == "KKK":
            if self.kkk_lock == True:
                self.rgb_1 = self.layout.rgb_1_value.value() / k_RGB
                self.rgb_2 = self.layout.rgb_2_value.value() / k_RGB
                self.rgb_3 = self.layout.rgb_3_value.value() / k_RGB
                self.kkk_0 = self.layout.kkk_1_value.value()
                rgb = [self.rgb_1, self.rgb_2, self.rgb_3]
                kkk = self.kkk_to_rgb(self.kkk_0)
                self.kkk_1 = kkk[0]
                self.kkk_2 = kkk[1]
                self.kkk_3 = kkk[2]
            if self.kkk_lock == False:
                self.kkk_0 = self.layout.kkk_1_value.value()
                rgb = self.kkk_to_rgb(self.kkk_0)
                self.kkk_1 = rgb[0]
                self.kkk_2 = rgb[1]
                self.kkk_3 = rgb[2]
        #//
        #\\ Convert RGB to Other
        if mode != "AAA":
            aaa = self.rgb_to_aaa(rgb[0], rgb[1], rgb[2])
        if mode != "RGB":
            pass
        if mode != "UVD":
            try:
                uvd = self.rgb_to_uvd(rgb[0], rgb[1], rgb[2])
            except:
                uvd = self.ard_to_uvd(ard[0], ard[1], ard[2])
        if mode != "ARD":
            ard = self.rgb_to_ard(rgb[0], rgb[1], rgb[2])
        if mode != "HSV":
            hsv = self.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        if mode != "HSL":
            hsl = self.rgb_to_hsl(rgb[0], rgb[1], rgb[2])
        if mode != "HCY":
            hcy = self.rgb_to_hcy(rgb[0], rgb[1], rgb[2])
        if mode != "YUV":
            yuv = self.rgb_to_yuv(rgb[0], rgb[1], rgb[2])
        if mode != "RYB":
            ryb = self.rgb_to_ryb(rgb[0], rgb[1], rgb[2])
        if mode != "CMY":
            cmy = self.rgb_to_cmy(rgb[0], rgb[1], rgb[2])
        if mode != "CMYK":
            cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        if mode != "KKK":
            self.kkk_0 = self.layout.kkk_1_value.value()
            kkk = self.kkk_to_rgb(self.kkk_0)
            self.kkk_1 = kkk[0]
            self.kkk_2 = kkk[1]
            self.kkk_3 = kkk[2]
        #//
        #\\ Variables
        # HUE
        if (mode != "ARD" and mode != "HSV" and mode != "HSL" and mode != "HCY"):
            self.angle_live = hsv[0]
        # Alpha
        self.aaa_1 = aaa[0]
        # RGB
        self.rgb_1 = rgb[0]
        self.rgb_2 = rgb[1]
        self.rgb_3 = rgb[2]
        # UVD
        self.uvd_1 = uvd[0]
        self.uvd_2 = uvd[1]
        self.uvd_3 = uvd[2]
        # ARD
        self.ard_1 = self.angle_live
        self.ard_2 = ard[1]
        self.ard_3 = ard[2]
        # Correct random D depth
        if (mode != "ARD" or ignore == "IGNORE"):
            condition = self.uvd_3 - self.d_previous
            if (condition > -u_RDL and condition < u_RDL):
                self.uvd_3 = self.d_previous
                self.ard_3 = self.d_previous
        # HSV
        self.hsv_1 = self.angle_live
        self.hsv_2 = hsv[1]
        self.hsv_3 = hsv[2]
        # HSL
        self.hsl_1 = self.angle_live
        self.hsl_2 = hsl[1]
        self.hsl_3 = hsl[2]
        # HCY
        self.hcy_1 = self.angle_live
        self.hcy_2 = hcy[1]
        self.hcy_3 = hcy[2]
        # YUV
        self.yuv_1 = yuv[0]
        self.yuv_2 = yuv[1]
        self.yuv_3 = yuv[2]
        # RYB
        self.ryb_1 = ryb[0]
        self.ryb_2 = ryb[1]
        self.ryb_3 = ryb[2]
        # CMY
        self.cmy_1 = cmy[0]
        self.cmy_2 = cmy[1]
        self.cmy_3 = cmy[2]
        # CMYK
        self.cmyk_1 = cmyk[0]
        self.cmyk_2 = cmyk[1]
        self.cmyk_3 = cmyk[2]
        self.cmyk_4 = cmyk[3]
        # Kelvin
        if self.kkk_lock == True:
            # RGB Kelvin
            self.rgb_k1 = self.rgb_1 * kkk[0]
            self.rgb_k2 = self.rgb_2 * kkk[1]
            self.rgb_k3 = self.rgb_3 * kkk[2]
            # AAA Kelvin
            aaa = self.rgb_to_aaa(self.rgb_k1, self.rgb_k2, self.rgb_k3)
            self.aaa_k1 = aaa[0]
            # CMYK Kelvin
            cmyk = self.rgb_to_cmyk(self.rgb_k1, self.rgb_k2, self.rgb_k3)
            self.cmyk_k1 = cmyk[0]
            self.cmyk_k2 = cmyk[1]
            self.cmyk_k3 = cmyk[2]
            self.cmyk_k4 = cmyk[3]
        #//
        #\\ Pigment Update Values
        self.Pigment_Harmony(mode)
        if mode == "AAA":
            self.Pigment_Sync("AAA")
        if mode == "RGB":
            self.Pigment_Sync("RGB")
        if mode == "ARD":
            self.Pigment_Sync("ARD")
        if mode == "HSV":
            self.Pigment_Sync("HSV")
        if mode == "HSL":
            self.Pigment_Sync("HSL")
        if mode == "HCY":
            self.Pigment_Sync("HCY")
        if mode == "YUV":
            self.Pigment_Sync("YUV")
        if mode == "RYB":
            self.Pigment_Sync("RYB")
        if mode == "CMY":
            self.Pigment_Sync("CMY")
        if mode == "CMYK":
            self.Pigment_Sync("CMYK")
        if mode == "KKK":
            self.Pigment_Sync("KKK")
        self.Pigment_2_Krita("HOLD")
        self.Pigment_Display()
        self.Mixer_Display()
        #//
    def Pigment_Harmony(self, mode):
        # Do Calculations in the active color wheel
        if self.wheel == "CMY":
            angulus = self.angle_live
        if self.wheel == "RYB":
            angulus = self.hcmy_to_hryb(self.angle_live)

        if mode != "LOAD":
            # Harmony ["HSL", rgb_1, rgb_2, rgb_3, hsl_1, hsl_2, hsl_3]
            self.harmony_index = self.layout.har_index.currentText()
            if self.wheel == "CMY":
                if self.harmony_index == "Monochromatic":
                    if self.harmony_active == 1: # Rotating Node
                        # 1
                        self.har_1 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        self.har_2 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        self.har_4 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        self.har_5 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                if self.harmony_index == "Complemantary":
                    if self.harmony_active == 1: # Rotating Node
                        # 1
                        self.har_1 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        self.har_2 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 4
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4: # Rotating Node
                        # 1
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        self.har_4 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5: # Rotating Node Major
                        # 1
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [angulus, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angulus, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        self.har_5 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                if self.harmony_index == "Analogous":
                    if self.harmony_active == 1:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1 / 2
                        if delta1 > delta2:
                            self.harmony_delta = delta2 / 2
                        # 1
                        angle = self.har_3[4] - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        angle = angulus - (2*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 4
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + (2*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1 / 2
                        if delta1 > delta2:
                            self.harmony_delta = delta2 / 2
                        # 1
                        angle = self.har_3[4] - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                if self.harmony_index == "Split Complemantary":
                    if self.harmony_active == 1:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 4
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                if self.harmony_index == "Double Split Complemantary":
                    if self.harmony_active == 1:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] + 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus + 0.5 + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, angulus, self.hsl_2, self.hsl_3]
                        # 4
                        angle = angulus - 0.5 - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] - 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] - 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5:
                        # Delta
                        value1 = angulus # A
                        value2 = self.har_3[4] # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.har_3[4] - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.har_3[4] - 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.har_3[4] + 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.har_3[4] + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [angle, self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [angle, self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.wheel == "RYB":
                if self.harmony_index == "Monochromatic":
                    if self.harmony_active == 1: # Rotating Node
                        # 1
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                if self.harmony_index == "Complemantary":
                    if self.harmony_active == 1: # Rotating Node
                        # 1
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2: # Rotating Node
                        # 1
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4: # Rotating Node
                        # 1
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5: # Rotating Node Major
                        # 1
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        angle = angulus + 0.5
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angulus), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                if self.harmony_index == "Analogous":
                    if self.harmony_active == 1:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1 / 2
                        if delta1 > delta2:
                            self.harmony_delta = delta2 / 2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        angle = angulus - (2*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + (2*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1 / 2
                        if delta1 > delta2:
                            self.harmony_delta = delta2 / 2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (2 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                if self.harmony_index == "Split Complemantary":
                    if self.harmony_active == 1:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4] + 1) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                if self.harmony_index == "Double Split Complemantary":
                    if self.harmony_active == 1:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 2:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) + 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 3: # Rotating Node Major
                        # 1
                        angle = angulus - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_1[5], self.har_1[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = angulus + 0.5 + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        hsl = [self.hryb_to_hcmy(angulus), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = angulus - 0.5 - (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = angulus + (1*self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 4:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) - 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                    if self.harmony_active == 5:
                        # Delta
                        value1 = angulus # A
                        value2 = self.hcmy_to_hryb(self.har_3[4]) # O
                        value3 = value1 + 1
                        value4 = value2 + 1
                        if value1 <= value2:
                            delta1 = value2 - value1
                            delta2 = value3 - value2
                        if value1 > value2:
                            delta1 = value1 - value2
                            delta2 = value4 - value1
                        if delta1 <= delta2:
                            self.harmony_delta = delta1
                        if delta1 > delta2:
                            self.harmony_delta = delta2
                        # 1
                        angle = self.hcmy_to_hryb(self.har_3[4]) - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 2
                        angle = self.hcmy_to_hryb(self.har_3[4]) - 0.5 + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_2[5], self.har_2[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 3
                        if self.harmony_edit == True:
                            hsl = [self.har_3[4], self.har_3[5], self.har_3[6]]
                        else:
                            hsl = [self.har_3[4], self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 4
                        angle = self.hcmy_to_hryb(self.har_3[4]) + 0.5 - (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_4[5], self.har_4[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                        # 5
                        angle = self.hcmy_to_hryb(self.har_3[4]) + (1 * self.harmony_delta)
                        angle = self.Math_1D_Loop(angle)
                        if self.harmony_edit == True:
                            hsl = [self.hryb_to_hcmy(angle), self.har_5[5], self.har_5[6]]
                        else:
                            hsl = [self.hryb_to_hcmy(angle), self.hsl_2, self.hsl_3]
                        rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                        self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]

        # Harmony Influenced by Kalvin
        self.har_k1 = [self.har_1[1] * self.kkk_1, self.har_1[2] * self.kkk_2, self.har_1[3] * self.kkk_3]
        self.har_k2 = [self.har_2[1] * self.kkk_1, self.har_2[2] * self.kkk_2, self.har_2[3] * self.kkk_3]
        self.har_k3 = [self.har_3[1] * self.kkk_1, self.har_3[2] * self.kkk_2, self.har_3[3] * self.kkk_3]
        self.har_k4 = [self.har_4[1] * self.kkk_1, self.har_4[2] * self.kkk_2, self.har_4[3] * self.kkk_3]
        self.har_k5 = [self.har_5[1] * self.kkk_1, self.har_5[2] * self.kkk_2, self.har_5[3] * self.kkk_3]

    #//
    #\\ Sync Channels ##########################################################
    def Pigment_Sync(self, index):
        # Block Signals
        if index != "AAA":
            self.Signal_Block_AAA(True)
        if index != "RGB":
            self.Signal_Block_RGB(True)
        if index != "ARD":
            self.Signal_Block_ARD(True)
        if index != "HSV":
            self.Signal_Block_HSV(True)
        if index != "HSL":
            self.Signal_Block_HSL(True)
        if index != "HCY":
            self.Signal_Block_HCY(True)
        if index != "YUV":
            self.Signal_Block_YUV(True)
        if index != "RYB":
            self.Signal_Block_RYB(True)
        if index != "CMY":
            self.Signal_Block_CMY(True)
        if index != "CMYK":
            self.Signal_Block_CMYK(True)
        if index != "KKK":
            self.Signal_Block_KKK(True)
        # Adjust Channels
        self.Ratio_Channels()
        # Set Values
        if index != "AAA":
            self.Signal_Send_AAA(self.aaa_1)
        if index != "RGB":
            self.Signal_Send_RGB(self.rgb_1, self.rgb_2, self.rgb_3)
        if index != "ARD":
            self.Signal_Send_ARD(self.ard_1, self.ard_2, self.ard_3)
        if index != "HSV":
            self.Signal_Send_HSV(self.hsv_1, self.hsv_2, self.hsv_3)
        if index != "HSL":
            self.Signal_Send_HSL(self.hsl_1, self.hsl_2, self.hsl_3)
        if index != "HCY":
            self.Signal_Send_HCY(self.hcy_1, self.hcy_2, self.hcy_3)
        if index != "YUV":
            self.Signal_Send_YUV(self.yuv_1, self.yuv_2, self.yuv_3)
        if index != "RYB":
            self.Signal_Send_RYB(self.ryb_1, self.ryb_2, self.ryb_3)
        if index != "CMY":
            self.Signal_Send_CMY(self.cmy_1, self.cmy_2, self.cmy_3)
        if index != "CMYK":
            self.Signal_Send_CMYK(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
        if index != "KKK":
            self.Signal_Send_KKK(self.kkk_0)
        # Signal Panels
        self.Signal_Send_Panels()
        # UnBlock Signals
        if index != "AAA":
            self.Signal_Block_AAA(False)
        if index != "RGB":
            self.Signal_Block_RGB(False)
        if index != "ARD":
            self.Signal_Block_ARD(False)
        if index != "HSV":
            self.Signal_Block_HSV(False)
        if index != "HSL":
            self.Signal_Block_HSL(False)
        if index != "HCY":
            self.Signal_Block_HCY(False)
        if index != "YUV":
            self.Signal_Block_YUV(False)
        if index != "RYB":
            self.Signal_Block_RYB(False)
        if index != "CMY":
            self.Signal_Block_CMY(False)
        if index != "CMYK":
            self.Signal_Block_CMYK(False)
        if index != "KKK":
            self.Signal_Block_KKK(False)

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
    def Signal_Block_HCY(self, boolean):
        self.layout.hcy_1_slider.blockSignals(boolean)
        self.layout.hcy_2_slider.blockSignals(boolean)
        self.layout.hcy_3_slider.blockSignals(boolean)
        self.layout.hcy_1_value.blockSignals(boolean)
        self.layout.hcy_2_value.blockSignals(boolean)
        self.layout.hcy_3_value.blockSignals(boolean)
    def Signal_Block_YUV(self, boolean):
        self.layout.yuv_1_slider.blockSignals(boolean)
        self.layout.yuv_2_slider.blockSignals(boolean)
        self.layout.yuv_3_slider.blockSignals(boolean)
        self.layout.yuv_1_value.blockSignals(boolean)
        self.layout.yuv_2_value.blockSignals(boolean)
        self.layout.yuv_3_value.blockSignals(boolean)
    def Signal_Block_RYB(self, boolean):
        self.layout.ryb_1_slider.blockSignals(boolean)
        self.layout.ryb_2_slider.blockSignals(boolean)
        self.layout.ryb_3_slider.blockSignals(boolean)
        self.layout.ryb_1_value.blockSignals(boolean)
        self.layout.ryb_2_value.blockSignals(boolean)
        self.layout.ryb_3_value.blockSignals(boolean)
    def Signal_Block_CMY(self, boolean):
        self.layout.cmy_1_slider.blockSignals(boolean)
        self.layout.cmy_2_slider.blockSignals(boolean)
        self.layout.cmy_3_slider.blockSignals(boolean)
        self.layout.cmy_1_value.blockSignals(boolean)
        self.layout.cmy_2_value.blockSignals(boolean)
        self.layout.cmy_3_value.blockSignals(boolean)
    def Signal_Block_CMYK(self, boolean):
        self.layout.cmyk_1_slider.blockSignals(boolean)
        self.layout.cmyk_2_slider.blockSignals(boolean)
        self.layout.cmyk_3_slider.blockSignals(boolean)
        self.layout.cmyk_4_slider.blockSignals(boolean)
        self.layout.cmyk_1_value.blockSignals(boolean)
        self.layout.cmyk_2_value.blockSignals(boolean)
        self.layout.cmyk_3_value.blockSignals(boolean)
        self.layout.cmyk_4_value.blockSignals(boolean)
    def Signal_Block_KKK(self, boolean):
        self.layout.kkk_1_slider.blockSignals(boolean)
        self.layout.kkk_1_value.blockSignals(boolean)
    # Signal Send
    def Signal_Send_AAA(self, value1):
        self.aaa_1_slider.Update(value1, self.channel_width)
        self.layout.aaa_1_value.setValue(value1 * k_AAA)
    def Signal_Send_RGB(self, value1, value2, value3):
        self.rgb_1_slider.Update(value1, self.channel_width)
        self.rgb_2_slider.Update(value2, self.channel_width)
        self.rgb_3_slider.Update(value3, self.channel_width)
        self.layout.rgb_1_value.setValue(value1 * k_RGB)
        self.layout.rgb_2_value.setValue(value2 * k_RGB)
        self.layout.rgb_3_value.setValue(value3 * k_RGB)
    def Signal_Send_ARD(self, value1, value2, value3):
        self.ard_1_slider.Update(value1, self.channel_width)
        self.ard_2_slider.Update(value2, self.channel_width)
        self.ard_3_slider.Update(value3, self.channel_width)
        self.layout.ard_1_value.setValue(value1 * k_ANG)
        self.layout.ard_2_value.setValue(value2 * k_RDL)
        self.layout.ard_3_value.setValue(value3 * k_RDL)
    def Signal_Send_HSV(self, value1, value2, value3):
        self.hsv_1_slider.Update(value1, self.channel_width)
        self.hsv_2_slider.Update(value2, self.channel_width)
        self.hsv_3_slider.Update(value3, self.channel_width)
        self.layout.hsv_1_value.setValue(value1 * k_HUE)
        self.layout.hsv_2_value.setValue(value2 * k_SVL)
        self.layout.hsv_3_value.setValue(value3 * k_SVL)
    def Signal_Send_HSL(self, value1, value2, value3):
        self.hsl_1_slider.Update(value1, self.channel_width)
        self.hsl_2_slider.Update(value2, self.channel_width)
        self.hsl_3_slider.Update(value3, self.channel_width)
        self.layout.hsl_1_value.setValue(value1 * k_HUE)
        self.layout.hsl_2_value.setValue(value2 * k_SVL)
        self.layout.hsl_3_value.setValue(value3 * k_SVL)
    def Signal_Send_HCY(self, value1, value2, value3):
        self.hcy_1_slider.Update(value1, self.channel_width)
        self.hcy_2_slider.Update(value2, self.channel_width)
        self.hcy_3_slider.Update(value3, self.channel_width)
        self.layout.hcy_1_value.setValue(value1 * k_HUE)
        self.layout.hcy_2_value.setValue(value2 * k_SVL)
        self.layout.hcy_3_value.setValue(value3 * k_SVL)
    def Signal_Send_YUV(self, value1, value2, value3):
        self.yuv_1_slider.Update(value1, self.channel_width)
        self.yuv_2_slider.Update(value2, self.channel_width)
        self.yuv_3_slider.Update(value3, self.channel_width)
        self.layout.yuv_1_value.setValue(value1 * k_Y)
        self.layout.yuv_2_value.setValue(value2 * k_U)
        self.layout.yuv_3_value.setValue(value3 * k_V)
    def Signal_Send_RYB(self, value1, value2, value3):
        self.ryb_1_slider.Update(value1, self.channel_width)
        self.ryb_2_slider.Update(value2, self.channel_width)
        self.ryb_3_slider.Update(value3, self.channel_width)
        self.layout.ryb_1_value.setValue(value1 * k_RYB)
        self.layout.ryb_2_value.setValue(value2 * k_RYB)
        self.layout.ryb_3_value.setValue(value3 * k_RYB)
    def Signal_Send_CMY(self, value1, value2, value3):
        self.cmy_1_slider.Update(value1, self.channel_width)
        self.cmy_2_slider.Update(value2, self.channel_width)
        self.cmy_3_slider.Update(value3, self.channel_width)
        self.layout.cmy_1_value.setValue(value1 * k_CMY)
        self.layout.cmy_2_value.setValue(value2 * k_CMY)
        self.layout.cmy_3_value.setValue(value3 * k_CMY)
    def Signal_Send_CMYK(self, value1, value2, value3, value4):
        self.cmyk_1_slider.Update(value1, self.channel_width)
        self.cmyk_2_slider.Update(value2, self.channel_width)
        self.cmyk_3_slider.Update(value3, self.channel_width)
        self.cmyk_4_slider.Update(value4, self.channel_width)
        self.layout.cmyk_1_value.setValue(value1 * k_CMYK)
        self.layout.cmyk_2_value.setValue(value2 * k_CMYK)
        self.layout.cmyk_3_value.setValue(value3 * k_CMYK)
        self.layout.cmyk_4_value.setValue(value4 * k_CMYK)
    def Signal_Send_KKK(self, value1):
        self.kkk_1_slider.Update((value1-k_KKKmin)/k_KKKdelta, self.channel_width)
        self.layout.kkk_1_value.setValue(value1)
    # Signal Panels
    def Signal_Send_Panels(self):
        if self.panel_active == "RGB":
            self.Update_Panel_UVD()
            self.panel_uvd.update()
        if self.panel_active == "ARD":
            self.Update_Panel_ARD()
            self.panel_ard.update()
        if self.panel_active == "HSV":
            self.Update_Panel_HSV()
            self.panel_hsv.update()
        if self.panel_active == "HSL":
            self.Update_Panel_HSL()
            self.panel_hsl.update()
        if self.panel_active == "YUV":
            self.Update_Panel_YUV()
            self.panel_yuv.update()
        if self.panel_active == "HUE":
            self.Update_Panel_HUE()
            # Update Main
            self.panel_hue_circle.update()
            # Update Secondary
            if self.panel_secondary == "DOT":
                pass
            if self.panel_secondary == "TRIANGLE":
                self.panel_triangle.update()
            if self.panel_secondary == "SQUARE":
                self.panel_square.update()
            if self.panel_secondary == "DIAMOND":
                self.panel_diamond.update()
        if self.panel_active == "GAM":
            self.Update_Panel_GAM_Circle()
            self.Update_Panel_GAM_Polygon(self.P1_S1, self.P1_S3, self.P1_S4, self.P2_S1, self.P3_S3)
            self.panel_gam_polygon.update()
        if self.panel_active == "DOT":
            self.Update_Panel_DOT()
            self.panel_dots.update()
        if self.panel_active == "OBJ":
            self.Object_Live()

    #//
    #\\ Updates ################################################################
    def Update_Luma_Lock(self):
        natural = self.rgb_to_aaa(self.rgb_1, self.rgb_2, self.rgb_3)[0]
        contrast = self.gc(self.rgb_1, self.rgb_2, self.rgb_3)
        self.luma_lock_2.Update(
            self.aaa_lock,
            self.HEX_6string(natural, natural, natural),
            self.HEX_6string(contrast, contrast, contrast),
            self.layout.color_2.width(),
            self.layout.color_2.height())
    # UVD Update
    def Update_Panel_UVD(self):
        # UVD points of interest
        self.Hexagon_Points_UVD()
        # Update Panel
        self.panel_uvd.Update_Panel(
            self.uvd_1, self.uvd_2, self.uvd_3,
            self.PCC,
            self.P1, self.P2, self.P3, self.P4, self.P5, self.P6,
            self.P12, self.P23, self.P34, self.P45, self.P56, self.P61,
            self.uvd_width, self.uvd_height,
            self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom
            )
    def Hexagon_Points_UVD(self):
        # Calculate Original Points
        self.uvd_hexagon_origins(self.uvd_3)
        # Panel Dimensions
        self.uvd_width = self.layout.panel_uvd.width()
        self.uvd_height = self.layout.panel_uvd.height()
        w2 = self.uvd_width * 0.5
        h2 = self.uvd_height * 0.5
        if w2 >= h2:
            side = h2
        if h2 > w2:
            side = w2
        # Single Points
        self.P1 = [w2 + (self.O1[0] * side), h2 + (self.O1[1] * side)]
        self.P2 = [w2 + (self.O2[0] * side), h2 + (self.O2[1] * side)]
        self.P3 = [w2 + (self.O3[0] * side), h2 + (self.O3[1] * side)]
        self.P4 = [w2 + (self.O4[0] * side), h2 + (self.O4[1] * side)]
        self.P5 = [w2 + (self.O5[0] * side), h2 + (self.O5[1] * side)]
        self.P6 = [w2 + (self.O6[0] * side), h2 + (self.O6[1] * side)]
        # Composed Points
        self.PCC = [w2 + (self.OCC[0] * side), h2 + (self.OCC[1] * side)]
        self.P12 = [w2 + (self.O12[0] * side), h2 + (self.O12[1] * side)]
        self.P23 = [w2 + (self.O23[0] * side), h2 + (self.O23[1] * side)]
        self.P34 = [w2 + (self.O34[0] * side), h2 + (self.O34[1] * side)]
        self.P45 = [w2 + (self.O45[0] * side), h2 + (self.O45[1] * side)]
        self.P56 = [w2 + (self.O56[0] * side), h2 + (self.O56[1] * side)]
        self.P61 = [w2 + (self.O61[0] * side), h2 + (self.O61[1] * side)]
    # ARD Update
    def Update_Panel_ARD(self):
        if self.panel_active == "ARD":
            # ARD points of intrest
            self.Hexagon_Points_ARD()
            # Update Panel
            self.panel_ard.Update_Panel(
                self.hsv_to_rgb(self.ard_1, 1, 1),
                self.ard_2, self.ard_3,
                self.T1, self.T2, self.T3, self.cross,
                self.ard_w, self.ard_h,
                self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom
                )
    def Hexagon_Points_ARD(self):
        # Mask
        self.ard_w = self.layout.panel_ard.width()
        self.ard_h = self.layout.panel_ard.height()
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
            self.cross = self.Math_2D_Points_Lines_Intersection(0,0,1,vertex, 0,ddd,1,ddd)
        elif ddd > vertex:
            self.cross = self.Math_2D_Points_Lines_Intersection(0,1,1,vertex, 0,ddd,1,ddd)
        else:
            self.cross = [1, ddd]
    # Updates
    def Update_Panel_HSV(self):
        self.panel_hsv.Update_Panel(
            [self.hsv_1, self.hsv_2, self.hsv_3],
            self.hsv_to_rgb(self.hsv_1, 1, 1),

            self.harmony_render,
            self.harmony_edit,
            self.rgb_to_hsv(self.har_1[1], self.har_1[2], self.har_1[3]),
            self.rgb_to_hsv(self.har_2[1], self.har_2[2], self.har_2[3]),
            self.rgb_to_hsv(self.har_3[1], self.har_3[2], self.har_3[3]),
            self.rgb_to_hsv(self.har_4[1], self.har_4[2], self.har_4[3]),
            self.rgb_to_hsv(self.har_5[1], self.har_5[2], self.har_5[3]),

            self.layout.panel_hsv.width(),
            self.layout.panel_hsv.height(),
            self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom)
    def Update_Panel_HSL(self):
        self.panel_hsl.Update_Panel(
            [self.hsl_1, self.hsl_2, self.hsl_3],
            self.hsl_to_rgb(self.hsl_1, 1, 0.5),

            self.harmony_render,
            self.harmony_edit,
            self.rgb_to_hsl(self.har_1[1], self.har_1[2], self.har_1[3]),
            self.rgb_to_hsl(self.har_2[1], self.har_2[2], self.har_2[3]),
            self.rgb_to_hsl(self.har_3[1], self.har_3[2], self.har_3[3]),
            self.rgb_to_hsl(self.har_4[1], self.har_4[2], self.har_4[3]),
            self.rgb_to_hsl(self.har_5[1], self.har_5[2], self.har_5[3]),

            self.layout.panel_hsl.width(),
            self.layout.panel_hsl.height(),
            self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom)
    def Update_Panel_YUV(self):
        self.panel_yuv.Update_Panel(
            [self.yuv_1, self.yuv_2, self.yuv_3],

            self.yuv_to_rgb(self.yuv_1, 0, 1),
            self.yuv_to_rgb(self.yuv_1, 0, 0.5),
            self.yuv_to_rgb(self.yuv_1, 0, 0),

            self.yuv_to_rgb(self.yuv_1, 1, 1),
            self.yuv_to_rgb(self.yuv_1, 1, 0.5),
            self.yuv_to_rgb(self.yuv_1, 1, 0),

            self.layout.panel_yuv.width(),
            self.layout.panel_yuv.height(),
            self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom)
    def Update_Panel_HUE(self):
        # Hue of Color
        hsv = self.hsv_to_rgb(self.angle_live, 1, 1)
        hsl = self.hsl_to_rgb(self.angle_live, 1, 0.5)
        # Angles
        if self.wheel == "CMY":
            angle_h0 = self.angle_live
            angle_h1 = self.har_1[4] # hsl_1
            angle_h2 = self.har_2[4] # hsl_1
            angle_h3 = self.har_3[4] # hsl_1
            angle_h4 = self.har_4[4] # hsl_1
            angle_h5 = self.har_5[4] # hsl_1
        if self.wheel == "RYB":
            angle_h0 = self.hcmy_to_hryb(self.angle_live)
            angle_h1 = self.hcmy_to_hryb(self.har_1[4])
            angle_h2 = self.hcmy_to_hryb(self.har_2[4])
            angle_h3 = self.hcmy_to_hryb(self.har_3[4])
            angle_h4 = self.hcmy_to_hryb(self.har_4[4])
            angle_h5 = self.hcmy_to_hryb(self.har_5[4])
        # Update Regular
        if self.panel_secondary == "DOT":
            pass
        if self.panel_secondary == "TRIANGLE":
            self.panel_triangle.Update_Panel(
                [self.hsl_1, self.hsl_2, self.hsl_3],
                [hsl[0], hsl[1], hsl[2]],

                self.harmony_render,
                self.harmony_edit,
                self.rgb_to_hsl(self.har_1[1], self.har_1[2], self.har_1[3]),
                self.rgb_to_hsl(self.har_2[1], self.har_2[2], self.har_2[3]),
                self.rgb_to_hsl(self.har_3[1], self.har_3[2], self.har_3[3]),
                self.rgb_to_hsl(self.har_4[1], self.har_4[2], self.har_4[3]),
                self.rgb_to_hsl(self.har_5[1], self.har_5[2], self.har_5[3]),

                self.layout.panel_triangle.width(),
                self.layout.panel_triangle.height(),
                self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom)
        if self.panel_secondary == "SQUARE":
            self.panel_square.Update_Panel(
                [self.hsv_1, self.hsv_2, self.hsv_3],
                [hsv[0], hsv[1], hsv[2]],

                self.harmony_render,
                self.harmony_edit,
                self.rgb_to_hsv(self.har_1[1], self.har_1[2], self.har_1[3]),
                self.rgb_to_hsv(self.har_2[1], self.har_2[2], self.har_2[3]),
                self.rgb_to_hsv(self.har_3[1], self.har_3[2], self.har_3[3]),
                self.rgb_to_hsv(self.har_4[1], self.har_4[2], self.har_4[3]),
                self.rgb_to_hsv(self.har_5[1], self.har_5[2], self.har_5[3]),

                self.layout.panel_square.width(),
                self.layout.panel_square.height(),
                self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom)
        if self.panel_secondary == "DIAMOND":
            self.panel_diamond.Update_Panel(
                [self.hsl_1, self.hsl_2, self.hsl_3],
                [hsl[0], hsl[1], hsl[2]],

                self.harmony_render,
                self.harmony_edit,
                self.rgb_to_hsl(self.har_1[1], self.har_1[2], self.har_1[3]),
                self.rgb_to_hsl(self.har_2[1], self.har_2[2], self.har_2[3]),
                self.rgb_to_hsl(self.har_3[1], self.har_3[2], self.har_3[3]),
                self.rgb_to_hsl(self.har_4[1], self.har_4[2], self.har_4[3]),
                self.rgb_to_hsl(self.har_5[1], self.har_5[2], self.har_5[3]),

                self.layout.panel_diamond.width(),
                self.layout.panel_diamond.height(),
                self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom)
        # Update Circle
        if self.harmony_rule == 0:
            self.panel_hue_circle.Update_Panel(
                self.wheel,
                self.harmony_render,
                self.harmony_index,
                angle_h0,
                [hsl[0], hsl[1], hsl[2]],
                self.layout.panel_hue_circle.width(),
                self.layout.panel_hue_circle.height(),
                self.gray_natural,
                self.gray_contrast)
        if self.harmony_rule != 0:
            self.panel_hue_circle.Update_Harmony_1(
                self.wheel,
                self.harmony_render,
                self.harmony_index,
                angle_h1,
                [self.har_1[1], self.har_1[2], self.har_1[3]], # rgb_1, rgb_2, rgb_3
                self.layout.panel_hue_circle.width(),
                self.layout.panel_hue_circle.height(),
                self.gray_natural,
                self.gray_contrast)
            self.panel_hue_circle.Update_Harmony_2(
                self.wheel,
                self.harmony_render,
                self.harmony_index,
                angle_h2,
                [self.har_2[1], self.har_2[2], self.har_2[3]],
                self.layout.panel_hue_circle.width(),
                self.layout.panel_hue_circle.height(),
                self.gray_natural,
                self.gray_contrast)
            self.panel_hue_circle.Update_Harmony_3(
                self.wheel,
                self.harmony_render,
                self.harmony_index,
                angle_h3,
                [self.har_3[1], self.har_3[2], self.har_3[3]],
                self.layout.panel_hue_circle.width(),
                self.layout.panel_hue_circle.height(),
                self.gray_natural,
                self.gray_contrast)
            self.panel_hue_circle.Update_Harmony_4(
                self.wheel,
                self.harmony_render,
                self.harmony_index,
                angle_h4,
                [self.har_4[1], self.har_4[2], self.har_4[3]],
                self.layout.panel_hue_circle.width(),
                self.layout.panel_hue_circle.height(),
                self.gray_natural,
                self.gray_contrast)
            self.panel_hue_circle.Update_Harmony_5(
                self.wheel,
                self.harmony_render,
                self.harmony_index,
                angle_h5,
                [self.har_5[1], self.har_5[2], self.har_5[3]],
                self.layout.panel_hue_circle.width(),
                self.layout.panel_hue_circle.height(),
                self.gray_natural,
                self.gray_contrast)
    # Gamut Update
    def Update_Panel_GAM_Circle(self):
        # Update Circle for Angle
        self.panel_gam_circle.Update_Panel(
            self.gamut_angle,
            self.P1_S1,
            self.P1_S3,
            self.P1_S4,
            self.P2_S1,
            self.P3_S3,
            self.layout.panel_gam_circle.width(),
            self.layout.panel_gam_circle.height(),
            self.gray_natural,
            self.gray_contrast
            )
    def Update_Panel_GAM_Polygon(self, P1_S1, P1_S3, P1_S4, P2_S1, P3_S3):
        # Polygon List Build
        panel_gam_polygon_width = self.layout.panel_gam_polygon.width()
        panel_gam_polygon_height = self.layout.panel_gam_polygon.height()
        # Update Circle of Colors and Polygon
        if self.wheel == "CMY":
            if self.gamut_space == "ARD":
                self.panel_gam_polygon.Update_Panel(
                    self.angle_live,
                    self.ard_2,
                    self.wheel,
                    self.ard_to_rgb(0/360, 0, self.ard_3), # Gray
                    self.ard_to_rgb(0/360, 1, self.ard_3), # Red
                    self.ard_to_rgb(10/360, 1, self.ard_3),
                    self.ard_to_rgb(20/360, 1, self.ard_3),
                    self.ard_to_rgb(30/360, 1, self.ard_3),
                    self.ard_to_rgb(40/360, 1, self.ard_3),
                    self.ard_to_rgb(50/360, 1, self.ard_3),
                    self.ard_to_rgb(60/360, 1, self.ard_3), # Yellow
                    self.ard_to_rgb(70/360, 1, self.ard_3),
                    self.ard_to_rgb(80/360, 1, self.ard_3),
                    self.ard_to_rgb(90/360, 1, self.ard_3),
                    self.ard_to_rgb(100/360, 1, self.ard_3),
                    self.ard_to_rgb(110/360, 1, self.ard_3),
                    self.ard_to_rgb(120/360, 1, self.ard_3), # Green
                    self.ard_to_rgb(130/360, 1, self.ard_3),
                    self.ard_to_rgb(140/360, 1, self.ard_3),
                    self.ard_to_rgb(150/360, 1, self.ard_3),
                    self.ard_to_rgb(160/360, 1, self.ard_3),
                    self.ard_to_rgb(170/360, 1, self.ard_3),
                    self.ard_to_rgb(180/360, 1, self.ard_3), # Cyan
                    self.ard_to_rgb(190/360, 1, self.ard_3),
                    self.ard_to_rgb(200/360, 1, self.ard_3),
                    self.ard_to_rgb(210/360, 1, self.ard_3),
                    self.ard_to_rgb(220/360, 1, self.ard_3),
                    self.ard_to_rgb(230/360, 1, self.ard_3),
                    self.ard_to_rgb(240/360, 1, self.ard_3), # Blue
                    self.ard_to_rgb(250/360, 1, self.ard_3),
                    self.ard_to_rgb(260/360, 1, self.ard_3),
                    self.ard_to_rgb(270/360, 1, self.ard_3),
                    self.ard_to_rgb(280/360, 1, self.ard_3),
                    self.ard_to_rgb(290/360, 1, self.ard_3),
                    self.ard_to_rgb(300/360, 1, self.ard_3), # Magenta
                    self.ard_to_rgb(310/360, 1, self.ard_3),
                    self.ard_to_rgb(320/360, 1, self.ard_3),
                    self.ard_to_rgb(330/360, 1, self.ard_3),
                    self.ard_to_rgb(340/360, 1, self.ard_3),
                    self.ard_to_rgb(350/360, 1, self.ard_3),
                    self.ard_to_rgb(360/360, 1, self.ard_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
            if self.gamut_space == "HSV":
                self.panel_gam_polygon.Update_Panel(
                    self.angle_live,
                    self.hsv_2,
                    self.wheel,
                    self.hsv_to_rgb(0/360, 0, self.hsv_3), # Gray
                    self.hsv_to_rgb(0/360, 1, self.hsv_3), # Red
                    self.hsv_to_rgb(10/360, 1, self.hsv_3),
                    self.hsv_to_rgb(20/360, 1, self.hsv_3),
                    self.hsv_to_rgb(30/360, 1, self.hsv_3),
                    self.hsv_to_rgb(40/360, 1, self.hsv_3),
                    self.hsv_to_rgb(50/360, 1, self.hsv_3),
                    self.hsv_to_rgb(60/360, 1, self.hsv_3), # Yellow
                    self.hsv_to_rgb(70/360, 1, self.hsv_3),
                    self.hsv_to_rgb(80/360, 1, self.hsv_3),
                    self.hsv_to_rgb(90/360, 1, self.hsv_3),
                    self.hsv_to_rgb(100/360, 1, self.hsv_3),
                    self.hsv_to_rgb(110/360, 1, self.hsv_3),
                    self.hsv_to_rgb(120/360, 1, self.hsv_3), # Green
                    self.hsv_to_rgb(130/360, 1, self.hsv_3),
                    self.hsv_to_rgb(140/360, 1, self.hsv_3),
                    self.hsv_to_rgb(150/360, 1, self.hsv_3),
                    self.hsv_to_rgb(160/360, 1, self.hsv_3),
                    self.hsv_to_rgb(170/360, 1, self.hsv_3),
                    self.hsv_to_rgb(180/360, 1, self.hsv_3), # Cyan
                    self.hsv_to_rgb(190/360, 1, self.hsv_3),
                    self.hsv_to_rgb(200/360, 1, self.hsv_3),
                    self.hsv_to_rgb(210/360, 1, self.hsv_3),
                    self.hsv_to_rgb(220/360, 1, self.hsv_3),
                    self.hsv_to_rgb(230/360, 1, self.hsv_3),
                    self.hsv_to_rgb(240/360, 1, self.hsv_3), # Blue
                    self.hsv_to_rgb(250/360, 1, self.hsv_3),
                    self.hsv_to_rgb(260/360, 1, self.hsv_3),
                    self.hsv_to_rgb(270/360, 1, self.hsv_3),
                    self.hsv_to_rgb(280/360, 1, self.hsv_3),
                    self.hsv_to_rgb(290/360, 1, self.hsv_3),
                    self.hsv_to_rgb(300/360, 1, self.hsv_3), # Magenta
                    self.hsv_to_rgb(310/360, 1, self.hsv_3),
                    self.hsv_to_rgb(320/360, 1, self.hsv_3),
                    self.hsv_to_rgb(330/360, 1, self.hsv_3),
                    self.hsv_to_rgb(340/360, 1, self.hsv_3),
                    self.hsv_to_rgb(350/360, 1, self.hsv_3),
                    self.hsv_to_rgb(360/360, 1, self.hsv_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
            if self.gamut_space == "HSL":
                self.panel_gam_polygon.Update_Panel(
                    self.angle_live,
                    self.hsl_2,
                    self.wheel,
                    self.hsl_to_rgb(0/360, 0, self.hsl_3), # Gray
                    self.hsl_to_rgb(0/360, 1, self.hsl_3), # Red
                    self.hsl_to_rgb(10/360, 1, self.hsl_3),
                    self.hsl_to_rgb(20/360, 1, self.hsl_3),
                    self.hsl_to_rgb(30/360, 1, self.hsl_3),
                    self.hsl_to_rgb(40/360, 1, self.hsl_3),
                    self.hsl_to_rgb(50/360, 1, self.hsl_3),
                    self.hsl_to_rgb(60/360, 1, self.hsl_3), # Yellow
                    self.hsl_to_rgb(70/360, 1, self.hsl_3),
                    self.hsl_to_rgb(80/360, 1, self.hsl_3),
                    self.hsl_to_rgb(90/360, 1, self.hsl_3),
                    self.hsl_to_rgb(100/360, 1, self.hsl_3),
                    self.hsl_to_rgb(110/360, 1, self.hsl_3),
                    self.hsl_to_rgb(120/360, 1, self.hsl_3), # Green
                    self.hsl_to_rgb(130/360, 1, self.hsl_3),
                    self.hsl_to_rgb(140/360, 1, self.hsl_3),
                    self.hsl_to_rgb(150/360, 1, self.hsl_3),
                    self.hsl_to_rgb(160/360, 1, self.hsl_3),
                    self.hsl_to_rgb(170/360, 1, self.hsl_3),
                    self.hsl_to_rgb(180/360, 1, self.hsl_3), # Cyan
                    self.hsl_to_rgb(190/360, 1, self.hsl_3),
                    self.hsl_to_rgb(200/360, 1, self.hsl_3),
                    self.hsl_to_rgb(210/360, 1, self.hsl_3),
                    self.hsl_to_rgb(220/360, 1, self.hsl_3),
                    self.hsl_to_rgb(230/360, 1, self.hsl_3),
                    self.hsl_to_rgb(240/360, 1, self.hsl_3), # Blue
                    self.hsl_to_rgb(250/360, 1, self.hsl_3),
                    self.hsl_to_rgb(260/360, 1, self.hsl_3),
                    self.hsl_to_rgb(270/360, 1, self.hsl_3),
                    self.hsl_to_rgb(280/360, 1, self.hsl_3),
                    self.hsl_to_rgb(290/360, 1, self.hsl_3),
                    self.hsl_to_rgb(300/360, 1, self.hsl_3), # Magenta
                    self.hsl_to_rgb(310/360, 1, self.hsl_3),
                    self.hsl_to_rgb(320/360, 1, self.hsl_3),
                    self.hsl_to_rgb(330/360, 1, self.hsl_3),
                    self.hsl_to_rgb(340/360, 1, self.hsl_3),
                    self.hsl_to_rgb(350/360, 1, self.hsl_3),
                    self.hsl_to_rgb(360/360, 1, self.hsl_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
            if self.gamut_space == "HCY":
                self.panel_gam_polygon.Update_Panel(
                    self.angle_live,
                    self.hcy_2,
                    self.wheel,
                    self.hcy_to_rgb(0/360, 0, self.hcy_3), # Gray
                    self.hcy_to_rgb(0/360, 1, self.hcy_3), # Red
                    self.hcy_to_rgb(10/360, 1, self.hcy_3),
                    self.hcy_to_rgb(20/360, 1, self.hcy_3),
                    self.hcy_to_rgb(30/360, 1, self.hcy_3),
                    self.hcy_to_rgb(40/360, 1, self.hcy_3),
                    self.hcy_to_rgb(50/360, 1, self.hcy_3),
                    self.hcy_to_rgb(60/360, 1, self.hcy_3), # Yellow
                    self.hcy_to_rgb(70/360, 1, self.hcy_3),
                    self.hcy_to_rgb(80/360, 1, self.hcy_3),
                    self.hcy_to_rgb(90/360, 1, self.hcy_3),
                    self.hcy_to_rgb(100/360, 1, self.hcy_3),
                    self.hcy_to_rgb(110/360, 1, self.hcy_3),
                    self.hcy_to_rgb(120/360, 1, self.hcy_3), # Green
                    self.hcy_to_rgb(130/360, 1, self.hcy_3),
                    self.hcy_to_rgb(140/360, 1, self.hcy_3),
                    self.hcy_to_rgb(150/360, 1, self.hcy_3),
                    self.hcy_to_rgb(160/360, 1, self.hcy_3),
                    self.hcy_to_rgb(170/360, 1, self.hcy_3),
                    self.hcy_to_rgb(180/360, 1, self.hcy_3), # Cyan
                    self.hcy_to_rgb(190/360, 1, self.hcy_3),
                    self.hcy_to_rgb(200/360, 1, self.hcy_3),
                    self.hcy_to_rgb(210/360, 1, self.hcy_3),
                    self.hcy_to_rgb(220/360, 1, self.hcy_3),
                    self.hcy_to_rgb(230/360, 1, self.hcy_3),
                    self.hcy_to_rgb(240/360, 1, self.hcy_3), # Blue
                    self.hcy_to_rgb(250/360, 1, self.hcy_3),
                    self.hcy_to_rgb(260/360, 1, self.hcy_3),
                    self.hcy_to_rgb(270/360, 1, self.hcy_3),
                    self.hcy_to_rgb(280/360, 1, self.hcy_3),
                    self.hcy_to_rgb(290/360, 1, self.hcy_3),
                    self.hcy_to_rgb(300/360, 1, self.hcy_3), # Magenta
                    self.hcy_to_rgb(310/360, 1, self.hcy_3),
                    self.hcy_to_rgb(320/360, 1, self.hcy_3),
                    self.hcy_to_rgb(330/360, 1, self.hcy_3),
                    self.hcy_to_rgb(340/360, 1, self.hcy_3),
                    self.hcy_to_rgb(350/360, 1, self.hcy_3),
                    self.hcy_to_rgb(360/360, 1, self.hcy_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
        if self.wheel == "RYB":
            if self.gamut_space == "ARD":
                self.panel_gam_polygon.Update_Panel(
                    self.hcmy_to_hryb(self.angle_live),
                    self.ard_2,
                    self.wheel,
                    self.ard_to_rgb(self.hryb_to_hcmy(0/360), 0, self.ard_3), # Gray
                    self.ard_to_rgb(self.hryb_to_hcmy(0/360), 1, self.ard_3), # Red
                    self.ard_to_rgb(self.hryb_to_hcmy(10/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(20/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(30/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(40/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(50/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(60/360), 1, self.ard_3), # Yellow
                    self.ard_to_rgb(self.hryb_to_hcmy(70/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(80/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(90/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(100/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(110/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(120/360), 1, self.ard_3), # Green
                    self.ard_to_rgb(self.hryb_to_hcmy(130/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(140/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(150/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(160/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(170/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(180/360), 1, self.ard_3), # Cyan
                    self.ard_to_rgb(self.hryb_to_hcmy(190/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(200/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(210/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(220/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(230/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(240/360), 1, self.ard_3), # Blue
                    self.ard_to_rgb(self.hryb_to_hcmy(250/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(260/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(270/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(280/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(290/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(300/360), 1, self.ard_3), # Magenta
                    self.ard_to_rgb(self.hryb_to_hcmy(310/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(320/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(330/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(340/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(350/360), 1, self.ard_3),
                    self.ard_to_rgb(self.hryb_to_hcmy(360/360), 1, self.ard_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
            if self.gamut_space == "HSV":
                self.panel_gam_polygon.Update_Panel(
                    self.hcmy_to_hryb(self.angle_live),
                    self.hsv_2,
                    self.wheel,
                    self.hsv_to_rgb(self.hryb_to_hcmy(0/360), 0, self.hsv_3), # Gray
                    self.hsv_to_rgb(self.hryb_to_hcmy(0/360), 1, self.hsv_3), # Red
                    self.hsv_to_rgb(self.hryb_to_hcmy(10/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(20/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(30/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(40/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(50/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(60/360), 1, self.hsv_3), # Yellow
                    self.hsv_to_rgb(self.hryb_to_hcmy(70/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(80/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(90/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(100/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(110/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(120/360), 1, self.hsv_3), # Green
                    self.hsv_to_rgb(self.hryb_to_hcmy(130/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(140/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(150/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(160/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(170/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(180/360), 1, self.hsv_3), # Cyan
                    self.hsv_to_rgb(self.hryb_to_hcmy(190/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(200/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(210/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(220/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(230/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(240/360), 1, self.hsv_3), # Blue
                    self.hsv_to_rgb(self.hryb_to_hcmy(250/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(260/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(270/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(280/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(290/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(300/360), 1, self.hsv_3), # Magenta
                    self.hsv_to_rgb(self.hryb_to_hcmy(310/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(320/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(330/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(340/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(350/360), 1, self.hsv_3),
                    self.hsv_to_rgb(self.hryb_to_hcmy(360/360), 1, self.hsv_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
            if self.gamut_space == "HSL":
                self.panel_gam_polygon.Update_Panel(
                    self.hcmy_to_hryb(self.angle_live),
                    self.hsl_2,
                    self.wheel,
                    self.hsl_to_rgb(self.hryb_to_hcmy(0/360), 0, self.hsl_3), # Gray
                    self.hsl_to_rgb(self.hryb_to_hcmy(0/360), 1, self.hsl_3), # Red
                    self.hsl_to_rgb(self.hryb_to_hcmy(10/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(20/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(30/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(40/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(50/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(60/360), 1, self.hsl_3), # Yellow
                    self.hsl_to_rgb(self.hryb_to_hcmy(70/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(80/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(90/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(100/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(110/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(120/360), 1, self.hsl_3), # Green
                    self.hsl_to_rgb(self.hryb_to_hcmy(130/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(140/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(150/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(160/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(170/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(180/360), 1, self.hsl_3), # Cyan
                    self.hsl_to_rgb(self.hryb_to_hcmy(190/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(200/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(210/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(220/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(230/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(240/360), 1, self.hsl_3), # Blue
                    self.hsl_to_rgb(self.hryb_to_hcmy(250/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(260/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(270/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(280/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(290/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(300/360), 1, self.hsl_3), # Magenta
                    self.hsl_to_rgb(self.hryb_to_hcmy(310/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(320/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(330/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(340/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(350/360), 1, self.hsl_3),
                    self.hsl_to_rgb(self.hryb_to_hcmy(360/360), 1, self.hsl_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
            if self.gamut_space == "HCY":
                self.panel_gam_polygon.Update_Panel(
                    self.hcmy_to_hryb(self.angle_live),
                    self.hcy_2,
                    self.wheel,
                    self.hcy_to_rgb(self.hryb_to_hcmy(0/360), 0, self.hcy_3), # Gray
                    self.hcy_to_rgb(self.hryb_to_hcmy(0/360), 1, self.hcy_3), # Red
                    self.hcy_to_rgb(self.hryb_to_hcmy(10/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(20/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(30/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(40/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(50/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(60/360), 1, self.hcy_3), # Yellow
                    self.hcy_to_rgb(self.hryb_to_hcmy(70/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(80/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(90/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(100/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(110/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(120/360), 1, self.hcy_3), # Green
                    self.hcy_to_rgb(self.hryb_to_hcmy(130/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(140/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(150/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(160/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(170/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(180/360), 1, self.hcy_3), # Cyan
                    self.hcy_to_rgb(self.hryb_to_hcmy(190/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(200/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(210/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(220/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(230/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(240/360), 1, self.hcy_3), # Blue
                    self.hcy_to_rgb(self.hryb_to_hcmy(250/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(260/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(270/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(280/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(290/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(300/360), 1, self.hcy_3), # Magenta
                    self.hcy_to_rgb(self.hryb_to_hcmy(310/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(320/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(330/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(340/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(350/360), 1, self.hcy_3),
                    self.hcy_to_rgb(self.hryb_to_hcmy(360/360), 1, self.hcy_3), # Red
                    self.gamut_shape,
                    P1_S1,
                    P1_S3,
                    P1_S4,
                    P2_S1,
                    P3_S3,
                    panel_gam_polygon_width,
                    panel_gam_polygon_height,
                    self.gray_natural,
                    self.gray_contrast,
                    self.HEX_6string(self.rgb_1, self.rgb_2, self.rgb_3),
                    self.zoom)
    # DOT Update
    def Update_Panel_DOT(self):
        self.panel_dots.Update_Panel(
            self.dot_1,
            self.dot_2,
            self.dot_3,
            self.dot_4,
            self.layout.panel_dot_mix.width(),
            self.layout.panel_dot_mix.height())

    #//
    #\\ Display ################################################################
    def Pigment_Display(self):
        # Foreground Color Display
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_1*255, self.rgb_2*255, self.rgb_3*255))
        self.layout.color_1.setStyleSheet(active_color_1)
        # SOF
        self.layout.sof_1_slider.setStyleSheet(bg_alpha)
        self.layout.sof_2_slider.setStyleSheet(bg_alpha)
        self.layout.sof_3_slider.setStyleSheet(bg_alpha)
        # AAA
        if self.chan_aaa == True:
            sss_aaa1 = str(self.RGB_Gradient([0, 0, 0], [1, 1, 1]))
            self.layout.aaa_1_slider.setStyleSheet(sss_aaa1)
        # RGB
        if self.chan_rgb == True:
            sss_rgb1 = str(self.RGB_Gradient([0, self.rgb_2, self.rgb_3], [1, self.rgb_2, self.rgb_3]))
            sss_rgb2 = str(self.RGB_Gradient([self.rgb_1, 0, self.rgb_3], [self.rgb_1, 1, self.rgb_3]))
            sss_rgb3 = str(self.RGB_Gradient([self.rgb_1, self.rgb_2, 0], [self.rgb_1, self.rgb_2, 1]))
            self.layout.rgb_1_slider.setStyleSheet(sss_rgb1)
            self.layout.rgb_2_slider.setStyleSheet(sss_rgb2)
            self.layout.rgb_3_slider.setStyleSheet(sss_rgb3)
        # ARD
        if self.chan_ard == True:
            if (self.ard_3 != 0 and self.ard_3 != 1):
                if self.hue_shine == True:
                    sss_ard1 = str(bg_rainbow)
                else:
                    sss_ard1 = str(self.ARD_Gradient_Linear(self.channel_width, [0, self.ard_2, self.ard_3], [1, self.ard_2, self.ard_3]))
            if self.ard_3 == 0:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.channel_width, [0, 0, self.ard_3], [1, 0, self.ard_3]))
            if self.ard_3 == 1:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.channel_width, [0, 0, self.ard_3], [1, 0, self.ard_3]))
            sss_ard2 = str(self.ARD_Gradient_Linear(self.channel_width, [self.ard_1, 0, self.ard_3], [self.ard_1, 1, self.ard_3]))
            sss_ard3 = str(self.ARD_Gradient_Linear(self.channel_width, [self.ard_1, self.ard_2, 0], [self.ard_1, self.ard_2, 1]))
            self.layout.ard_1_slider.setStyleSheet(sss_ard1)
            self.layout.ard_2_slider.setStyleSheet(sss_ard2)
            self.layout.ard_3_slider.setStyleSheet(sss_ard3)
        # HSV
        if self.chan_hsv == True:
            if self.hue_shine == True:
                sss_hsv1 = str(bg_rainbow)
            else:
                sss_hsv1 = str(self.HUE_Gradient("HSV", self.channel_width, [0, self.hsv_2, self.hsv_3], [1, self.hsv_2, self.hsv_3]))
            sss_hsv2 = str(self.HSV_Gradient(self.channel_width, [self.hsv_1, 0, self.hsv_3], [self.hsv_1, 1, self.hsv_3]))
            sss_hsv3 = str(self.HSV_Gradient(self.channel_width, [self.hsv_1, self.hsv_2, 0], [self.hsv_1, self.hsv_2, 1]))
            self.layout.hsv_1_slider.setStyleSheet(sss_hsv1)
            self.layout.hsv_2_slider.setStyleSheet(sss_hsv2)
            self.layout.hsv_3_slider.setStyleSheet(sss_hsv3)
        # HSL
        if self.chan_hsl == True:
            if self.hue_shine == True:
                sss_hsl1 = str(bg_rainbow)
            else:
                sss_hsl1 = str(self.HUE_Gradient("HSL", self.channel_width, [0, self.hsl_2, self.hsl_3], [1, self.hsl_2, self.hsl_3]))
            sss_hsl2 = str(self.HSL_Gradient(self.channel_width, [self.hsl_1, 0, self.hsl_3], [self.hsl_1, 1, self.hsl_3]))
            sss_hsl3 = str(self.HSL_Gradient(self.channel_width, [self.hsl_1, self.hsl_2, 0], [self.hsl_1, self.hsl_2, 1]))
            self.layout.hsl_1_slider.setStyleSheet(sss_hsl1)
            self.layout.hsl_2_slider.setStyleSheet(sss_hsl2)
            self.layout.hsl_3_slider.setStyleSheet(sss_hsl3)
        # HCY
        if self.chan_hcy == True:
            if self.hue_shine == True:
                sss_hcy1 = str(bg_rainbow)
            else:
                sss_hcy1 = str(self.HUE_Gradient("HCY", self.channel_width, [0, self.hcy_2, self.hcy_3], [1, self.hcy_2, self.hcy_3]))
            sss_hcy2 = str(self.HCY_Gradient(self.channel_width, [self.hcy_1, 0, self.hcy_3], [self.hcy_1, 1, self.hcy_3]))
            sss_hcy3 = str(self.HCY_Gradient(self.channel_width, [self.hcy_1, self.hcy_2, 0], [self.hcy_1, self.hcy_2, 1]))
            self.layout.hcy_1_slider.setStyleSheet(sss_hcy1)
            self.layout.hcy_2_slider.setStyleSheet(sss_hcy2)
            self.layout.hcy_3_slider.setStyleSheet(sss_hcy3)
        # YUV
        if self.chan_yuv == True:
            sss_yuv1 = str(self.YUV_Gradient([0, self.yuv_2, self.yuv_3], [1, self.yuv_2, self.yuv_3]))
            sss_yuv2 = str(self.YUV_Gradient([self.yuv_1, 0, self.yuv_3], [self.yuv_1, 1, self.yuv_3]))
            sss_yuv3 = str(self.YUV_Gradient([self.yuv_1, self.yuv_2, 0], [self.yuv_1, self.yuv_2, 1]))
            self.layout.yuv_1_slider.setStyleSheet(sss_yuv1)
            self.layout.yuv_2_slider.setStyleSheet(sss_yuv2)
            self.layout.yuv_3_slider.setStyleSheet(sss_yuv3)
        # RYB
        if self.chan_ryb == True:
            sss_ryb1 = str(self.RYB_Gradient([0, self.ryb_2, self.ryb_3], [1, self.ryb_2, self.ryb_3]))
            sss_ryb2 = str(self.RYB_Gradient([self.ryb_1, 0, self.ryb_3], [self.ryb_1, 1, self.ryb_3]))
            sss_ryb3 = str(self.RYB_Gradient([self.ryb_1, self.ryb_2, 0], [self.ryb_1, self.ryb_2, 1]))
            self.layout.ryb_1_slider.setStyleSheet(sss_ryb1)
            self.layout.ryb_2_slider.setStyleSheet(sss_ryb2)
            self.layout.ryb_3_slider.setStyleSheet(sss_ryb3)
        # CMY
        if self.chan_cmy == True:
            sss_cmy1 = str(self.CMY_Gradient([0, self.cmy_2, self.cmy_3], [1, self.cmy_2, self.cmy_3]))
            sss_cmy2 = str(self.CMY_Gradient([self.cmy_1, 0, self.cmy_3], [self.cmy_1, 1, self.cmy_3]))
            sss_cmy3 = str(self.CMY_Gradient([self.cmy_1, self.cmy_2, 0], [self.cmy_1, self.cmy_2, 1]))
            self.layout.cmy_1_slider.setStyleSheet(sss_cmy1)
            self.layout.cmy_2_slider.setStyleSheet(sss_cmy2)
            self.layout.cmy_3_slider.setStyleSheet(sss_cmy3)
        # CMYK
        if self.chan_cmyk == True:
            sss_cmyk1 = str(self.CMYK_Gradient(self.channel_width, [0, self.cmyk_2, self.cmyk_3, self.cmyk_4], [1, self.cmyk_2, self.cmyk_3, self.cmyk_4]))
            sss_cmyk2 = str(self.CMYK_Gradient(self.channel_width, [self.cmyk_1, 0, self.cmyk_3, self.cmyk_4], [self.cmyk_1, 1, self.cmyk_3, self.cmyk_4]))
            sss_cmyk3 = str(self.CMYK_Gradient(self.channel_width, [self.cmyk_1, self.cmyk_2, 0, self.cmyk_4], [self.cmyk_1, self.cmyk_2, 1, self.cmyk_4]))
            sss_cmyk4 = str(self.CMYK_Gradient(self.channel_width, [self.cmyk_1, self.cmyk_2, self.cmyk_3, 0], [self.cmyk_1, self.cmyk_2, self.cmyk_3, 1]))
            self.layout.cmyk_1_slider.setStyleSheet(sss_cmyk1)
            self.layout.cmyk_2_slider.setStyleSheet(sss_cmyk2)
            self.layout.cmyk_3_slider.setStyleSheet(sss_cmyk3)
            self.layout.cmyk_4_slider.setStyleSheet(sss_cmyk4)
        # KKK
        if self.chan_kkk == True:
            if self.kkk_lock == False:
                sss_kkk1 = str(self.KKK_Gradient(1, 1, 1))
            if self.kkk_lock == True:
                sss_kkk1 = str(self.KKK_Gradient(self.rgb_1, self.rgb_2, self.rgb_3))
            self.layout.kkk_1_slider.setStyleSheet(sss_kkk1)
        # Hex Color
        hex = self.Pigment_2_HEX()
        self.layout.hex_string.setText(str(hex))
        self.HEX_Display(str(hex))
        # Harmony
        if self.harmony_rule != 0:
            self.layout.harmony_1.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_1[1]*255, self.har_1[2]*255, self.har_1[3]*255)))
            self.layout.harmony_2.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_2[1]*255, self.har_2[2]*255, self.har_2[3]*255)))
            self.layout.harmony_3.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_3[1]*255, self.har_3[2]*255, self.har_3[3]*255)))
            self.layout.harmony_4.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_4[1]*255, self.har_4[2]*255, self.har_4[3]*255)))
            self.layout.harmony_5.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_5[1]*255, self.har_5[2]*255, self.har_5[3]*255)))
            self.layout.color_harmonys.setStyleSheet(str("QWidget { background-color: %s; }" % (self.gray_natural)))
        # ForeGround Color
        if self.panel_active == "FGC":
            if self.harmony_rule == 0:
                if self.kkk_lock == False:
                    foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.rgb_1*255, self.rgb_2*255, self.rgb_3*255))
                    self.layout.fgc_1.setStyleSheet(foreground_color)
                    self.layout.fgc_2.setStyleSheet(foreground_color)
                    self.layout.fgc_3.setStyleSheet(foreground_color)
                    self.layout.fgc_4.setStyleSheet(foreground_color)
                    self.layout.fgc_5.setStyleSheet(foreground_color)
                if self.kkk_lock == True:
                    foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.rgb_k1*255, self.rgb_k2*255, self.rgb_k3*255))
                    self.layout.fgc_1.setStyleSheet(foreground_color)
                    self.layout.fgc_2.setStyleSheet(foreground_color)
                    self.layout.fgc_3.setStyleSheet(foreground_color)
                    self.layout.fgc_4.setStyleSheet(foreground_color)
                    self.layout.fgc_5.setStyleSheet(foreground_color)
            if self.harmony_rule != 0:
                har_1 = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_1[1]*255, self.har_1[2]*255, self.har_1[3]*255))
                har_2 = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_2[1]*255, self.har_2[2]*255, self.har_2[3]*255))
                har_3 = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_3[1]*255, self.har_3[2]*255, self.har_3[3]*255))
                har_4 = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_4[1]*255, self.har_4[2]*255, self.har_4[3]*255))
                har_5 = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.har_5[1]*255, self.har_5[2]*255, self.har_5[3]*255))
                self.layout.fgc_1.setStyleSheet(har_1)
                self.layout.fgc_2.setStyleSheet(har_2)
                self.layout.fgc_3.setStyleSheet(har_3)
                self.layout.fgc_4.setStyleSheet(har_4)
                self.layout.fgc_5.setStyleSheet(har_5)
        else:
            self.layout.fgc_1.setStyleSheet(bg_unseen)
            self.layout.fgc_2.setStyleSheet(bg_unseen)
            self.layout.fgc_3.setStyleSheet(bg_unseen)
            self.layout.fgc_4.setStyleSheet(bg_unseen)
            self.layout.fgc_5.setStyleSheet(bg_unseen)
    def Pigment_Display_Release(self, SIGNAL_RELEASE):
        # Apply color for Linux Users
        self.Pigment_2_Krita("RELEASE")
        # Dusplay Release Color
        if self.kkk_lock == False:
            active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_1*255, self.rgb_2*255, self.rgb_3*255))
        if self.kkk_lock == True:
            active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_k1*255, self.rgb_k2*255, self.rgb_k3*255))
        self.layout.color_2.setStyleSheet(active_color_2)
        # Zoom Reset
        self.zoom = 0
        # Color Name
        hex = str(self.layout.hex_string.text())
        self.HEX_Display(hex)
        # Save the new HSX LOCK values
        if self.hsl_2 < 1:
            if self.aaa_lock == True:
                self.AAA_1_Value_Lock()
        # Update the Luma Lock Display button
        self.Update_Luma_Lock()
        # Gamut Verticies
        self.P1_S1 = self.P1_S1_r
        self.P1_S3 = self.P1_S3_r
        self.P1_S4 = self.P1_S4_r
        self.P2_S1 = self.P2_S1_r
        self.P3_S3 = self.P3_S3_r
        # Update the Widget
        self.Ratio()
        # Label Clean
        self.layout.label_percent.setText("")
    def Mixer_Display(self):
        # Update Variables
        self.menu_tts = self.layout.tts.isChecked()
        self.menu_mix = self.layout.mix.isChecked()
        self.menu_mix_index = self.layout.mix_index.currentText()
        # Mixer Tint, Tone, Shade
        if self.menu_tts == True:
            if self.color_tts[0] == "True":
                input_tint = [self.color_tts[1], self.color_tts[2], self.color_tts[3]]
                mix_tint = self.RGB_Gradient(input_tint, color_white)
                mix_tone = self.RGB_Gradient(input_tint, self.gray_tts)
                mix_shade = self.RGB_Gradient(input_tint, color_black)
                self.layout.tint.setStyleSheet(mix_tint)
                self.layout.tone.setStyleSheet(mix_tone)
                self.layout.shade.setStyleSheet(mix_shade)
            else:
                self.spacer_tint = 0
                self.spacer_tone = 0
                self.spacer_shade = 0
        else:
            self.layout.tint.setStyleSheet(bg_alpha)
            self.layout.tone.setStyleSheet(bg_alpha)
            self.layout.shade.setStyleSheet(bg_alpha)
        # Mixer RGB
        if (self.menu_mix == True and self.menu_mix_index == "RGB"):
            if (self.color_rgb_l1[0] == "True" and self.color_rgb_r1[0] == "True"):
                input_rgb_l1 = [self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3]]
                input_rgb_r1 = [self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3]]
                mix_rgb_g1 = self.RGB_Gradient(input_rgb_l1, input_rgb_r1)
                self.layout.rgb_g1.setStyleSheet(mix_rgb_g1)
            else:
                self.spacer_rgb_g1 = 0
            if (self.color_rgb_l2[0] == "True" and self.color_rgb_r2[0] == "True"):
                input_rgb_l2 = [self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3]]
                input_rgb_r2 = [self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3]]
                mix_rgb_g2 = self.RGB_Gradient(input_rgb_l2, input_rgb_r2)
                self.layout.rgb_g2.setStyleSheet(mix_rgb_g2)
            else:
                self.spacer_rgb_g2 = 0
            if (self.color_rgb_l3[0] == "True" and self.color_rgb_r3[0] == "True"):
                input_rgb_l3 = [self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3]]
                input_rgb_r3 = [self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3]]
                mix_rgb_g3 = self.RGB_Gradient(input_rgb_l3, input_rgb_r3)
                self.layout.rgb_g3.setStyleSheet(mix_rgb_g3)
            else:
                self.spacer_rgb_g3 = 0
        else:
            self.layout.rgb_g1.setStyleSheet(bg_alpha)
            self.layout.rgb_g2.setStyleSheet(bg_alpha)
            self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Mixer ARD
        if (self.menu_mix == True and self.menu_mix_index == "ARD"):
            if (self.color_ard_l1[0] == "True" and self.color_ard_r1[0] == "True"):
                input_ard_l1 = [self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3]]
                input_ard_r1 = [self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3]]
                mix_ard_g1 = self.ARD_Gradient_Circular(self.mixer_width, input_ard_l1, input_ard_r1)
                self.layout.ard_g1.setStyleSheet(mix_ard_g1)
            else:
                self.spacer_ard_g1 = 0
            if (self.color_ard_l2[0] == "True" and self.color_ard_r2[0] == "True"):
                input_ard_l2 = [self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3]]
                input_ard_r2 = [self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3]]
                mix_ard_g2 = self.ARD_Gradient_Circular(self.mixer_width, input_ard_l2, input_ard_r2)
                self.layout.ard_g2.setStyleSheet(mix_ard_g2)
            else:
                self.spacer_ard_g2 = 0
            if (self.color_ard_l3[0] == "True" and self.color_ard_r3[0] == "True"):
                input_ard_l3 = [self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3]]
                input_ard_r3 = [self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3]]
                mix_ard_g3 = self.ARD_Gradient_Circular(self.mixer_width, input_ard_l3, input_ard_r3)
                self.layout.ard_g3.setStyleSheet(mix_ard_g3)
            else:
                self.spacer_ard_g3 = 0
        else:
            self.layout.ard_g1.setStyleSheet(bg_alpha)
            self.layout.ard_g2.setStyleSheet(bg_alpha)
            self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Mixer HSV
        if (self.menu_mix == True and self.menu_mix_index == "HSV"):
            if (self.color_hsv_l1[0] == "True" and self.color_hsv_r1[0] == "True"):
                input_hsv_l1 = [self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3]]
                input_hsv_r1 = [self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3]]
                mix_hsv_g1 = self.HSV_Gradient(self.mixer_width, input_hsv_l1, input_hsv_r1)
                self.layout.hsv_g1.setStyleSheet(mix_hsv_g1)
            else:
                self.spacer_hsv_g1 = 0
            if (self.color_hsv_l2[0] == "True" and self.color_hsv_r2[0] == "True"):
                input_hsv_l2 = [self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3]]
                input_hsv_r2 = [self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3]]
                mix_hsv_g2 = self.HSV_Gradient(self.mixer_width, input_hsv_l2, input_hsv_r2)
                self.layout.hsv_g2.setStyleSheet(mix_hsv_g2)
            else:
                self.spacer_hsv_g2 = 0
            if (self.color_hsv_l3[0] == "True" and self.color_hsv_r3[0] == "True"):
                input_hsv_l3 = [self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3]]
                input_hsv_r3 = [self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3]]
                mix_hsv_g3 = self.HSV_Gradient(self.mixer_width, input_hsv_l3, input_hsv_r3)
                self.layout.hsv_g3.setStyleSheet(mix_hsv_g3)
            else:
                self.spacer_hsv_g3 = 0
        else:
            self.layout.hsv_g1.setStyleSheet(bg_alpha)
            self.layout.hsv_g2.setStyleSheet(bg_alpha)
            self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Mixer HSL
        if (self.menu_mix == True and self.menu_mix_index == "HSL"):
            if (self.color_hsl_l1[0] == "True" and self.color_hsl_r1[0] == "True"):
                input_hsl_l1 = [self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3]]
                input_hsl_r1 = [self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3]]
                mix_hsl_g1 = self.HSL_Gradient(self.mixer_width, input_hsl_l1, input_hsl_r1)
                self.layout.hsl_g1.setStyleSheet(mix_hsl_g1)
            else:
                self.spacer_hsl_g1 = 0
            if (self.color_hsl_l2[0] == "True" and self.color_hsl_r2[0] == "True"):
                input_hsl_l2 = [self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3]]
                input_hsl_r2 = [self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3]]
                mix_hsl_g2 = self.HSL_Gradient(self.mixer_width, input_hsl_l2, input_hsl_r2)
                self.layout.hsl_g2.setStyleSheet(mix_hsl_g2)
            else:
                self.spacer_hsl_g2 = 0
            if (self.color_hsl_l3[0] == "True" and self.color_hsl_r3[0] == "True"):
                input_hsl_l3 = [self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3]]
                input_hsl_r3 = [self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3]]
                mix_hsl_g3 = self.HSL_Gradient(self.mixer_width, input_hsl_l3, input_hsl_r3)
                self.layout.hsl_g3.setStyleSheet(mix_hsl_g3)
            else:
                self.spacer_hsl_g3 = 0
        else:
            self.layout.hsl_g1.setStyleSheet(bg_alpha)
            self.layout.hsl_g2.setStyleSheet(bg_alpha)
            self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Mixer HCY
        if (self.menu_mix == True and self.menu_mix_index == "HCY"):
            if (self.color_hcy_l1[0] == "True" and self.color_hcy_r1[0] == "True"):
                input_hcy_l1 = [self.color_hcy_l1[1], self.color_hcy_l1[2], self.color_hcy_l1[3]]
                input_hcy_r1 = [self.color_hcy_r1[1], self.color_hcy_r1[2], self.color_hcy_r1[3]]
                mix_hcy_g1 = self.HCY_Gradient(self.mixer_width, input_hcy_l1, input_hcy_r1)
                self.layout.hcy_g1.setStyleSheet(mix_hcy_g1)
            else:
                self.spacer_hcy_g1 = 0
            if (self.color_hcy_l2[0] == "True" and self.color_hcy_r2[0] == "True"):
                input_hcy_l2 = [self.color_hcy_l2[1], self.color_hcy_l2[2], self.color_hcy_l2[3]]
                input_hcy_r2 = [self.color_hcy_r2[1], self.color_hcy_r2[2], self.color_hcy_r2[3]]
                mix_hcy_g2 = self.HCY_Gradient(self.mixer_width, input_hcy_l2, input_hcy_r2)
                self.layout.hcy_g2.setStyleSheet(mix_hcy_g2)
            else:
                self.spacer_hcy_g2 = 0
            if (self.color_hcy_l3[0] == "True" and self.color_hcy_r3[0] == "True"):
                input_hcy_l3 = [self.color_hcy_l3[1], self.color_hcy_l3[2], self.color_hcy_l3[3]]
                input_hcy_r3 = [self.color_hcy_r3[1], self.color_hcy_r3[2], self.color_hcy_r3[3]]
                mix_hcy_g3 = self.HCY_Gradient(self.mixer_width, input_hcy_l3, input_hcy_r3)
                self.layout.hcy_g3.setStyleSheet(mix_hcy_g3)
            else:
                self.spacer_hcy_g3 = 0
        else:
            self.layout.hcy_g1.setStyleSheet(bg_alpha)
            self.layout.hcy_g2.setStyleSheet(bg_alpha)
            self.layout.hcy_g3.setStyleSheet(bg_alpha)
        # Mixer YUV
        if (self.menu_mix == True and self.menu_mix_index == "YUV"):
            if (self.color_yuv_l1[0] == "True" and self.color_yuv_r1[0] == "True"):
                input_yuv_l1 = [self.color_yuv_l1[1], self.color_yuv_l1[2], self.color_yuv_l1[3]]
                input_yuv_r1 = [self.color_yuv_r1[1], self.color_yuv_r1[2], self.color_yuv_r1[3]]
                mix_yuv_g1 = self.YUV_Gradient(input_yuv_l1, input_yuv_r1)
                self.layout.yuv_g1.setStyleSheet(mix_yuv_g1)
            else:
                self.spacer_yuv_g1 = 0
            if (self.color_yuv_l2[0] == "True" and self.color_yuv_r2[0] == "True"):
                input_yuv_l2 = [self.color_yuv_l2[1], self.color_yuv_l2[2], self.color_yuv_l2[3]]
                input_yuv_r2 = [self.color_yuv_r2[1], self.color_yuv_r2[2], self.color_yuv_r2[3]]
                mix_yuv_g2 = self.YUV_Gradient(input_yuv_l2, input_yuv_r2)
                self.layout.yuv_g2.setStyleSheet(mix_yuv_g2)
            else:
                self.spacer_yuv_g2 = 0
            if (self.color_yuv_l3[0] == "True" and self.color_yuv_r3[0] == "True"):
                input_yuv_l3 = [self.color_yuv_l3[1], self.color_yuv_l3[2], self.color_yuv_l3[3]]
                input_yuv_r3 = [self.color_yuv_r3[1], self.color_yuv_r3[2], self.color_yuv_r3[3]]
                mix_yuv_g3 = self.YUV_Gradient(input_yuv_l3, input_yuv_r3)
                self.layout.yuv_g3.setStyleSheet(mix_yuv_g3)
            else:
                self.spacer_yuv_g3 = 0
        else:
            self.layout.yuv_g1.setStyleSheet(bg_alpha)
            self.layout.yuv_g2.setStyleSheet(bg_alpha)
            self.layout.yuv_g3.setStyleSheet(bg_alpha)
        # Mixer RYB
        if (self.menu_mix == True and self.menu_mix_index == "RYB"):
            if (self.color_ryb_l1[0] == "True" and self.color_ryb_r1[0] == "True"):
                input_ryb_l1 = [self.color_ryb_l1[1], self.color_ryb_l1[2], self.color_ryb_l1[3]]
                input_ryb_r1 = [self.color_ryb_r1[1], self.color_ryb_r1[2], self.color_ryb_r1[3]]
                mix_ryb_g1 = self.RYB_Gradient(input_ryb_l1, input_ryb_r1)
                self.layout.ryb_g1.setStyleSheet(mix_ryb_g1)
            else:
                self.spacer_ryb_g1 = 0
            if (self.color_ryb_l2[0] == "True" and self.color_ryb_r2[0] == "True"):
                input_ryb_l2 = [self.color_ryb_l2[1], self.color_ryb_l2[2], self.color_ryb_l2[3]]
                input_ryb_r2 = [self.color_ryb_r2[1], self.color_ryb_r2[2], self.color_ryb_r2[3]]
                mix_ryb_g2 = self.RYB_Gradient(input_ryb_l2, input_ryb_r2)
                self.layout.ryb_g2.setStyleSheet(mix_ryb_g2)
            else:
                self.spacer_ryb_g2 = 0
            if (self.color_ryb_l3[0] == "True" and self.color_ryb_r3[0] == "True"):
                input_ryb_l3 = [self.color_ryb_l3[1], self.color_ryb_l3[2], self.color_ryb_l3[3]]
                input_ryb_r3 = [self.color_ryb_r3[1], self.color_ryb_r3[2], self.color_ryb_r3[3]]
                mix_ryb_g3 = self.RYB_Gradient(input_ryb_l3, input_ryb_r3)
                self.layout.ryb_g3.setStyleSheet(mix_ryb_g3)
            else:
                self.spacer_ryb_g3 = 0
        else:
            self.layout.ryb_g1.setStyleSheet(bg_alpha)
            self.layout.ryb_g2.setStyleSheet(bg_alpha)
            self.layout.ryb_g3.setStyleSheet(bg_alpha)
        # Mixer CMYK
        if (self.menu_mix == True and self.menu_mix_index == "CMYK"):
            if (self.color_cmyk_l1[0] == "True" and self.color_cmyk_r1[0] == "True"):
                input_cmyk_l1 = [self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4]]
                input_cmyk_r1 = [self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4]]
                mix_cmyk_g1 = self.CMYK_Gradient(self.mixer_width, input_cmyk_l1, input_cmyk_r1)
                self.layout.cmyk_g1.setStyleSheet(mix_cmyk_g1)
            else:
                self.spacer_cmyk_g1 = 0
            if (self.color_cmyk_l2[0] == "True" and self.color_cmyk_r2[0] == "True"):
                input_cmyk_l2 = [self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4]]
                input_cmyk_r2 = [self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4]]
                mix_cmyk_g2 = self.CMYK_Gradient(self.mixer_width, input_cmyk_l2, input_cmyk_r2)
                self.layout.cmyk_g2.setStyleSheet(mix_cmyk_g2)
            else:
                self.spacer_cmyk_g2 = 0
            if (self.color_cmyk_l3[0] == "True" and self.color_cmyk_r3[0] == "True"):
                input_cmyk_l3 = [self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4]]
                input_cmyk_r3 = [self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4]]
                mix_cmyk_g3 = self.CMYK_Gradient(self.mixer_width, input_cmyk_l3, input_cmyk_r3)
                self.layout.cmyk_g3.setStyleSheet(mix_cmyk_g3)
            else:
                self.spacer_cmyk_g3 = 0
        else:
            self.layout.cmyk_g1.setStyleSheet(bg_alpha)
            self.layout.cmyk_g2.setStyleSheet(bg_alpha)
            self.layout.cmyk_g3.setStyleSheet(bg_alpha)
    # Aspect Ratio
    def Ratio(self):
        # Redimension Channels Sliders
        self.Ratio_Channels()

        # Redimension Frames to be Centered
        self.Ratio_Box()

        # Relocate Panel Cursor due to Size Variation
        self.panel_active = self.layout.pan_index.currentText()
        try:
            if self.panel_active == "RGB":
                self.Update_Panel_UVD()
            if self.panel_active == "ARD":
                self.Update_Panel_ARD()
            if self.panel_active == "HSV":
                self.Update_Panel_HSV()
            if self.panel_active == "HSL":
                self.Update_Panel_HSL()
            if self.panel_active == "YUV":
                self.Update_Panel_YUV()
            if self.panel_active == "HUE":
                self.Update_Panel_HUE()
            if self.panel_active == "GAM":
                self.Update_Panel_GAM_Circle()
                self.Update_Panel_GAM_Polygon(self.P1_S1, self.P1_S3, self.P1_S4, self.P2_S1, self.P3_S3)
            if self.panel_active == "DOT":
                self.Update_Panel_DOT()
                self.panel_dots.Location(self.dot_location_x, self.dot_location_y, self.layout.panel_dot_mix.width(), self.layout.panel_dot_mix.height())
            if self.panel_active == "OBJ":
                self.panel_obj.Location(self.obj_location_x, self.obj_location_y, self.layout.panel_obj_mix.width(), self.layout.panel_obj_mix.height())
                self.OBJ_Alpha()
        except:
            pass
    def Ratio_Channels(self):
        # Channels
        self.channel_width = self.layout.rgb_1_slider.width()
        self.mixer_width = self.layout.rgb_g1.width()
        # Harmony
        try:
            self.harmony_1.Update(self.layout.harmony_1.width(), self.layout.harmony_1.height())
            self.harmony_2.Update(self.layout.harmony_2.width(), self.layout.harmony_2.height())
            self.harmony_3.Update(self.layout.harmony_3.width(), self.layout.harmony_3.height())
            self.harmony_4.Update(self.layout.harmony_4.width(), self.layout.harmony_4.height())
            self.harmony_5.Update(self.layout.harmony_5.width(), self.layout.harmony_5.height())
        except:
            pass
        # Relocate SOF Handle due to Size Variation
        try:
            self.sof_1_slider.Update(self.sof_1 / k_S, self.channel_width)
            self.sof_2_slider.Update(self.sof_2, self.channel_width)
            self.sof_3_slider.Update(self.sof_3, self.channel_width)
        except:
            pass
        # Relocate Channel Handle due to Size Variation
        try:
            if self.chan_aaa == True:
                self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
            if self.chan_rgb == True:
                self.rgb_1_slider.Update(self.rgb_1, self.channel_width)
                self.rgb_2_slider.Update(self.rgb_2, self.channel_width)
                self.rgb_3_slider.Update(self.rgb_3, self.channel_width)
            if self.chan_ard == True:
                self.ard_1_slider.Update(self.ard_1, self.channel_width)
                self.ard_2_slider.Update(self.ard_2, self.channel_width)
                self.ard_3_slider.Update(self.ard_3, self.channel_width)
            if self.chan_hsv == True:
                self.hsv_1_slider.Update(self.hsv_1, self.channel_width)
                self.hsv_2_slider.Update(self.hsv_2, self.channel_width)
                self.hsv_3_slider.Update(self.hsv_3, self.channel_width)
            if self.chan_hsl == True:
                self.hsl_1_slider.Update(self.hsl_1, self.channel_width)
                self.hsl_2_slider.Update(self.hsl_2, self.channel_width)
                self.hsl_3_slider.Update(self.hsl_3, self.channel_width)
            if self.chan_hcy == True:
                self.hcy_1_slider.Update(self.hcy_1, self.channel_width)
                self.hcy_2_slider.Update(self.hcy_2, self.channel_width)
                self.hcy_3_slider.Update(self.hcy_3, self.channel_width)
            if self.chan_yuv == True:
                self.yuv_1_slider.Update(self.yuv_1, self.channel_width)
                self.yuv_2_slider.Update(self.yuv_2, self.channel_width)
                self.yuv_3_slider.Update(self.yuv_3, self.channel_width)
            if self.chan_ryb == True:
                self.ryb_1_slider.Update(self.ryb_1, self.channel_width)
                self.ryb_2_slider.Update(self.ryb_2, self.channel_width)
                self.ryb_3_slider.Update(self.ryb_3, self.channel_width)
            if self.chan_cmy == True:
                self.cmy_1_slider.Update(self.cmy_1, self.channel_width)
                self.cmy_2_slider.Update(self.cmy_2, self.channel_width)
                self.cmy_3_slider.Update(self.cmy_3, self.channel_width)
            if self.chan_cmyk == True:
                self.cmyk_1_slider.Update(self.cmyk_1, self.channel_width)
                self.cmyk_2_slider.Update(self.cmyk_2, self.channel_width)
                self.cmyk_3_slider.Update(self.cmyk_3, self.channel_width)
                self.cmyk_4_slider.Update(self.cmyk_4, self.channel_width)
            if self.chan_kkk == True:
                self.kkk_1_slider.Update((self.kkk_0-k_KKKmin)/k_KKKdelta, self.channel_width)
        except:
            pass
        # Mixers
        try:
            # Relocate TTS Handles due to Size Variation
            if self.menu_tts == True:
                self.mixer_tint.Update(self.spacer_tint, self.layout.tint.width())
                self.mixer_tone.Update(self.spacer_tone, self.layout.tone.width())
                self.mixer_shade.Update(self.spacer_shade, self.layout.shade.width())
            # Relocate MIX Handles due to Size Variation
            if self.menu_mix == True:
                if self.menu_mix_index == "RGB":
                    self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.mixer_width)
                    self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.mixer_width)
                    self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.mixer_width)
                if self.menu_mix_index == "ARD":
                    self.mixer_ard_g1.Update(self.spacer_ard_g1, self.mixer_width)
                    self.mixer_ard_g2.Update(self.spacer_ard_g2, self.mixer_width)
                    self.mixer_ard_g3.Update(self.spacer_ard_g3, self.mixer_width)
                if self.menu_mix_index == "HSV":
                    self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.mixer_width)
                    self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.mixer_width)
                    self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.mixer_width)
                if self.menu_mix_index == "HSL":
                    self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.mixer_width)
                    self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.mixer_width)
                    self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.mixer_width)
                if self.menu_mix_index == "HCY":
                    self.mixer_hcy_g1.Update(self.spacer_hcy_g1, self.mixer_width)
                    self.mixer_hcy_g2.Update(self.spacer_hcy_g2, self.mixer_width)
                    self.mixer_hcy_g3.Update(self.spacer_hcy_g3, self.mixer_width)
                if self.menu_mix_index == "YUV":
                    self.mixer_yuv_g1.Update(self.spacer_yuv_g1, self.mixer_width)
                    self.mixer_yuv_g2.Update(self.spacer_yuv_g2, self.mixer_width)
                    self.mixer_yuv_g3.Update(self.spacer_yuv_g3, self.mixer_width)
                if self.menu_mix_index == "RYB":
                    self.mixer_ryb_g1.Update(self.spacer_ryb_g1, self.mixer_width)
                    self.mixer_ryb_g2.Update(self.spacer_ryb_g2, self.mixer_width)
                    self.mixer_ryb_g3.Update(self.spacer_ryb_g3, self.mixer_width)
                if self.menu_mix_index == "CMYK":
                    self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.mixer_width)
                    self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.mixer_width)
                    self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.mixer_width)
        except:
            pass
    def Ratio_Box(self):
        # Luma Lock Button Update
        self.Update_Luma_Lock()
        # Panel Widget Alignment
        if self.panel_active == "HUE":
            # HUE Panel Ratio Adjust to maintain Square
            hue_width = self.layout.panel_hue.width()
            hue_height = self.layout.panel_hue.height()
            if hue_width <= 0:
                hue_width = 1
            if hue_height <= 0:
                hue_height = 1
            if hue_width >= hue_height:
                self.layout.panel_hue_box.setMaximumWidth(hue_height)
                self.layout.panel_hue_box.setMaximumHeight(hue_height)
            if hue_width < hue_height:
                self.layout.panel_hue_box.setMaximumWidth(hue_width)
                self.layout.panel_hue_box.setMaximumHeight(hue_width)
            # Adjust Circle Geometry
            self.layout.panel_hue_circle.setGeometry(0,0,self.layout.panel_hue_box.width(),self.layout.panel_hue_box.height())
            # Adjust Regular
            self.panel_secondary = self.layout.pan_secondary.currentText()
            if self.panel_secondary == "DOT":
                self.layout.panel_hue_regular_mask.setGeometry(0,0, 0,0)
            if self.panel_secondary == "TRIANGLE":
                # Adjust Regular Geometry
                d1 = 0.28754
                d2 = 0.132
                d3 = 0.637388
                d4 = 0.735992
                panel_hue_box_width = self.layout.panel_hue_box.width()
                panel_hue_box_height = self.layout.panel_hue_box.height()
                self.layout.panel_hue_regular_mask.setGeometry(
                    panel_hue_box_width*d1, panel_hue_box_height*d2,
                    panel_hue_box_width*d3, panel_hue_box_height*d4)
                # Adjust Regular Mask
                panel_hue_regular_mask_width = self.layout.panel_hue_regular_mask.width()
                panel_hue_regular_mask_height = self.layout.panel_hue_regular_mask.height()
                region_polygon = QPolygon([
                    QPoint(0, 0),
                    QPoint(0, panel_hue_regular_mask_height),
                    QPoint(panel_hue_regular_mask_width, panel_hue_regular_mask_height*0.5)
                    ])
                self.layout.panel_hue_regular_mask.setMask(QRegion(region_polygon))
            if self.panel_secondary == "SQUARE":
                # Adjust Regular Geometry
                d1 = 0.2
                d2 = 1 - (2*d1)
                panel_hue_box_width = self.layout.panel_hue_box.width()
                panel_hue_box_height = self.layout.panel_hue_box.height()
                self.layout.panel_hue_regular_mask.setGeometry(
                    panel_hue_box_width*d1, panel_hue_box_height*d1,
                    panel_hue_box_width*d2, panel_hue_box_height*d2)
                # Adjust Regular Mask
                panel_hue_regular_mask_width = self.layout.panel_hue_regular_mask.width()
                panel_hue_regular_mask_height = self.layout.panel_hue_regular_mask.height()
                region_polygon = QPolygon([
                    QPoint(0, 0),
                    QPoint(panel_hue_regular_mask_width, 0),
                    QPoint(panel_hue_regular_mask_width, panel_hue_regular_mask_height),
                    QPoint(0, panel_hue_regular_mask_height)
                    ])
                self.layout.panel_hue_regular_mask.setMask(QRegion(region_polygon))
            if self.panel_secondary == "DIAMOND":
                # Adjust Regular Geometry
                d1 = 0.075
                d2 = 1 - (2*d1)
                panel_hue_box_width = self.layout.panel_hue_box.width()
                panel_hue_box_height = self.layout.panel_hue_box.height()
                self.layout.panel_hue_regular_mask.setGeometry(
                    panel_hue_box_width*d1, panel_hue_box_height*d1,
                    panel_hue_box_width*d2, panel_hue_box_height*d2)
                # Adjust Regular Mask
                panel_hue_regular_mask_width = self.layout.panel_hue_regular_mask.width()
                panel_hue_regular_mask_height = self.layout.panel_hue_regular_mask.height()
                region_polygon = QPolygon([
                    QPoint(panel_hue_regular_mask_width*0.5, 0),
                    QPoint(panel_hue_regular_mask_width, panel_hue_regular_mask_height*0.5),
                    QPoint(panel_hue_regular_mask_width*0.5, panel_hue_regular_mask_height),
                    QPoint(0, panel_hue_regular_mask_height*0.5)
                    ])
                self.layout.panel_hue_regular_mask.setMask(QRegion(region_polygon))
        if self.panel_active == "GAM":
            # GAM Panel Ratio Adjust to maintain Square
            gam_width = self.layout.panel_gam.width()
            gam_height = self.layout.panel_gam.height()
            if gam_width <= 0:
                gam_width = 1
            if gam_height <= 0:
                gam_height = 1
            if gam_width >= gam_height:
                circle = gam_height
            if gam_width < gam_height:
                circle = gam_width
            self.layout.panel_gam_box.setMaximumWidth(circle)
            self.layout.panel_gam_box.setMaximumHeight(circle)
            # Adjust Circle Geometry
            self.layout.panel_gam_circle.setGeometry(0,0,circle,circle)
            g1 = 0.05
            g2 = 1 - (2*g1)
            self.layout.panel_gam_polygon.setGeometry(circle*g1,circle*g1, circle*g2,circle*g2)
            gp_w = self.layout.panel_gam_polygon.width()
            gp_h = self.layout.panel_gam_polygon.height()
            gamut_polygon = QRegion(0,0, gp_w,gp_h, QRegion.Ellipse)
            self.layout.panel_gam_polygon.setMask(gamut_polygon)
        if self.panel_active == "OBJ":
            self.OBJ_Geometry()

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
        aaa1 = self.aaa_1 * hex_AAA
        rgb1 = self.rgb_1 * hex_RGB
        rgb2 = self.rgb_2 * hex_RGB
        rgb3 = self.rgb_3 * hex_RGB
        cmyk1 = self.cmyk_1 * hex_CMYK
        cmyk2 = self.cmyk_2 * hex_CMYK
        cmyk3 = self.cmyk_3 * hex_CMYK
        cmyk4 = self.cmyk_4 * hex_CMYK
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
        hex = self.layout.hex_string.text().lower()
        try:
            length = len(hex)
            if (hex[0] == "#" and length == 3):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                # Apply to Pigment
                aaa1 = hex1 / hex_AAA
                self.angle_live = 0
                self.Color_APPLY("AAA", aaa1, 0, 0, 0)
            elif (hex[0] == "#" and length == 7):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                # Apply to Pigment
                rgb1 = hex1 / hex_RGB
                rgb2 = hex2 / hex_RGB
                rgb3 = hex3 / hex_RGB
                self.Color_ANGLE(rgb1, rgb2, rgb3)
                self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
            elif (hex[0] == "#" and length == 9):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                hex4 = int(format(int(hex[7:9],16),'02d'))
                # Apply to Pigment
                cmyk1 = hex1 / hex_CMYK
                cmyk2 = hex2 / hex_CMYK
                cmyk3 = hex3 / hex_CMYK
                cmyk4 = hex4 / hex_CMYK
                rgb = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
                self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
                self.Color_APPLY("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
            else:
                self.layout.hex_string.setText("Error")
        except:
            self.layout.hex_string.setText("Error")
        self.Pigment_Display_Release(0)
    def HEX_6string(self, red, green, blue):
        # Transform into HEX
        hex1 = str(hex(int(red * hex_RGB)))[2:4].zfill(2)
        hex2 = str(hex(int(green * hex_RGB)))[2:4].zfill(2)
        hex3 = str(hex(int(blue * hex_RGB)))[2:4].zfill(2)
        pigment_hex = str("#"+hex1+hex2+hex3)
        return pigment_hex
    def HEX_Display(self, hex):
        if self.names_display == True:
            self.layout.label.setText("")
            for i in range(len(color_names)):
                if hex == color_names[i][0]:
                    self.layout.label.setText(str(color_names[i][1]))
    def HEX_Closest(self):
        # Original HEX Point
        hex_start = self.layout.hex_string.text().lower()
        ps = self.HEX_Point(hex_start)
        # Calculate Distances
        index = [0,1]
        for i in range(len(color_names)):
            pe = self.HEX_Point(color_names[i][0])
            d = self.Math_3D_Points_Distance(ps[0], ps[1], ps[2], pe[0], pe[1], pe[2])
            if d < index[1]:
                index = [i , d]
        # Final Color
        rgb = self.HEX_Point(color_names[index[0]][0])
        # Move Location to Closest Point
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("RGB", rgb[0], rgb[1], rgb[2], 0)
        self.Pigment_Display_Release(0)
    def HEX_Point(self, hex):
        length = len(hex)
        if (hex[0] == "#" and length == 3):
            # Parse Hex Code
            hex1 = int(format(int(hex[1:3],16),'02d'))
            # Apply to Pigment
            val1 = hex1 / hex_AAA
            val2 = val1
            val3 = val1
        elif (hex[0] == "#" and length == 7):
            # Parse Hex Code
            hex1 = int(format(int(hex[1:3],16),'02d'))
            hex2 = int(format(int(hex[3:5],16),'02d'))
            hex3 = int(format(int(hex[5:7],16),'02d'))
            # Apply to Pigment
            val1 = hex1 / hex_RGB
            val2 = hex2 / hex_RGB
            val3 = hex3 / hex_RGB
        elif (hex[0] == "#" and length == 9):
            # Parse Hex Code
            hex1 = int(format(int(hex[1:3],16),'02d'))
            hex2 = int(format(int(hex[3:5],16),'02d'))
            hex3 = int(format(int(hex[5:7],16),'02d'))
            hex4 = int(format(int(hex[7:9],16),'02d'))
            # Apply to Pigment
            cmyk1 = hex1 / hex_CMYK
            cmyk2 = hex2 / hex_CMYK
            cmyk3 = hex3 / hex_CMYK
            cmyk4 = hex4 / hex_CMYK
            val1, val2, val3 = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        return [val1, val2, val3]

    #//
    #\\ SOF ####################################################################
    def SOF_1_APPLY(self, value):
        self.sof_1 = value
        self.sof_1_slider.Update(value / k_S, self.channel_width)
        self.layout.sof_1_value.setValue(value)
    def SOF_2_APPLY(self, value):
        self.sof_2 = value
        self.sof_2_slider.Update(value, self.channel_width)
        self.layout.sof_2_value.setValue(value * k_O)
    def SOF_3_APPLY(self, value):
        self.sof_3 = value
        self.sof_3_slider.Update(value, self.channel_width)
        self.layout.sof_3_value.setValue(value * k_F)

    def Pigment_SOF_1_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.sof_1 - 1
            if self.sof_1 <= zero:
                self.sof_1 = zero
            self.sof_1_slider.Update(self.sof_1 / k_S, self.channel_width)
            self.layout.sof_1_value.setValue(self.sof_1)
            self.sof_1_slider.update()
    def Pigment_SOF_2_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.sof_2 - (unit/k_O)
            if self.sof_2 <= zero:
                self.sof_2 = zero
            self.sof_2_slider.Update(self.sof_2, self.channel_width)
            self.layout.sof_2_value.setValue(self.sof_2 * k_O)
            self.sof_2_slider.update()
    def Pigment_SOF_3_Minus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.sof_3 - (unit/k_F)
            if self.sof_3 <= zero:
                self.sof_3 = zero
            self.sof_3_slider.Update(self.sof_3, self.channel_width)
            self.layout.sof_3_value.setValue(self.sof_3 * k_F)
            self.sof_3_slider.update()

    def Pigment_SOF_1_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.sof_1 + 1
            if self.sof_1 >= k_S:
                self.sof_1 = k_S
            self.sof_1_slider.Update(self.sof_1 / k_S, self.channel_width)
            self.layout.sof_1_value.setValue(self.sof_1)
            self.sof_1_slider.update()
    def Pigment_SOF_2_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.sof_2 + (unit/k_O)
            if self.sof_2 >= unit:
                self.sof_2 = unit
            self.sof_2_slider.Update(self.sof_2, self.channel_width)
            self.layout.sof_2_value.setValue(self.sof_2 * k_O)
            self.sof_2_slider.update()
    def Pigment_SOF_3_Plus(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.sof_3 + (unit/k_F)
            if self.sof_3 >= unit:
                self.sof_3 = unit
            self.sof_3_slider.Update(self.sof_3, self.channel_width)
            self.layout.sof_3_value.setValue(self.sof_3 * k_F)
            self.sof_3_slider.update()

    def Pigment_SOF_1_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = SIGNAL_VALUE * k_S
            self.layout.sof_1_value.setValue(self.sof_1)
            if (self.timer_state == 1 or self.timer_state == 2):
                Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
        else:
            self.sof_1 = self.lock_size
            self.sof_1_slider.Update(self.sof_1 / k_S, self.channel_width)
            self.layout.sof_1_value.setValue(self.sof_1)
        self.sof_1_slider.update()
    def Pigment_SOF_2_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = SIGNAL_VALUE
            self.layout.sof_2_value.setValue(self.sof_2 * k_O)
            if (self.timer_state == 1 or self.timer_state == 2):
                Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
        else:
            self.sof_2 = self.lock_opacity
            self.sof_2_slider.Update(self.sof_2, self.channel_width)
            self.layout.sof_2_value.setValue(self.sof_2 * k_O)
        self.sof_2_slider.update()
    def Pigment_SOF_3_Slider_Modify(self, SIGNAL_VALUE):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = SIGNAL_VALUE
            self.layout.sof_3_value.setValue(self.sof_3 * k_F)
            if (self.timer_state == 1 or self.timer_state == 2):
                Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
        else:
            self.sof_3 = self.lock_flow
            self.sof_3_slider.Update(self.sof_3, self.channel_width)
            self.layout.sof_3_value.setValue(self.sof_3 * k_F)
        self.sof_3_slider.update()

    def Pigment_SOF_1_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_1 = self.layout.sof_1_value.value()
            self.sof_1_slider.Update(self.sof_1 / k_S, self.channel_width)
            if (self.timer_state == 1 or self.timer_state == 2):
                Krita.instance().activeWindow().activeView().setBrushSize(self.sof_1)
        else:
            self.sof_1 = self.lock_size
            self.sof_1_slider.Update(self.sof_1 / k_S, self.channel_width)
            self.layout.sof_1_value.setValue(self.sof_1)
        self.update()
    def Pigment_SOF_2_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_2 = self.layout.sof_2_value.value() / k_O
            self.sof_2_slider.Update(self.sof_2, self.channel_width)
            if (self.timer_state == 1 or self.timer_state == 2):
                Krita.instance().activeWindow().activeView().setPaintingOpacity(self.sof_2)
        else:
            self.sof_2 = self.lock_opacity
            self.sof_2_slider.Update(self.sof_2, self.channel_width)
            self.layout.sof_2_value.setValue(self.sof_2 * k_O)
        self.update()
    def Pigment_SOF_3_Value_Modify(self):
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            self.sof_3 = self.layout.sof_3_value.value() / k_F
            self.sof_3_slider.Update(self.sof_3, self.channel_width)
            if (self.timer_state == 1 or self.timer_state == 2):
                Krita.instance().activeWindow().activeView().setPaintingFlow(self.sof_3)
        else:
            self.sof_3 = self.lock_flow
            self.sof_3_slider.Update(self.sof_3, self.channel_width)
            self.layout.sof_3_value.setValue(self.sof_3 * k_F)
        self.update()

    #//
    #\\ Channels ###############################################################
    def Pigment_AAA_1_Lock(self, SIGNAL_LUMA_LOCK):
        if self.aaa_lock != True:
            # Status
            self.aaa_lock = True
            # Value Lock
            self.AAA_1_Value_Lock()
        else:
            # Key Status
            self.aaa_lock = False
            # Value Lock
            self.hsx_lock = [0, 0, 0]
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def AAA_1_Value_Lock(self):
        if self.panel_active == "ARD":
            self.hsx_lock = [self.ard_1, self.ard_2, self.ard_3]
        elif self.panel_active == "HSV":
            self.hsx_lock = [self.hsv_1, self.hsv_2, self.hsv_3]
        elif self.panel_active == "HSL":
            self.hsx_lock = [self.hsl_1, self.hsl_2, self.hsl_3]
        elif self.panel_active == "HUE":
            self.hsx_lock = [self.hsl_1, self.hsl_2, self.hsl_3]
    def Pigment_CMYK_4_Lock(self):
        if self.layout.cmyk_4_lock.isChecked():
            self.icon_lock = self.Icon_Lock(self.color_accent)
            self.svg_lock_cmyk_4.load(self.icon_lock)
            self.cmyk_lock = True
        else:
            self.icon_lock = self.Icon_Lock(self.gray_contrast)
            self.svg_lock_cmyk_4.load(self.icon_lock)
            self.cmyk_lock = False
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Lock(self):
        if self.layout.kkk_1_lock.isChecked():
            self.icon_lock = self.Icon_Lock(self.color_accent)
            self.svg_lock_kkk_1.load(self.icon_lock)
            self.kkk_lock = True
        else:
            self.icon_lock = self.Icon_Lock(self.gray_contrast)
            self.svg_lock_kkk_1.load(self.icon_lock)
            self.kkk_lock = False
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Half(self):
        self.aaa_1 = half
        self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
        self.layout.aaa_1_value.setValue(self.aaa_1 * k_AAA)
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Half(self):
        self.rgb_1 = half
        self.rgb_1_slider.Update(self.rgb_1, self.channel_width)
        self.layout.rgb_1_value.setValue(self.rgb_1 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Half(self):
        self.rgb_2 = half
        self.rgb_2_slider.Update(self.rgb_2, self.channel_width)
        self.layout.rgb_2_value.setValue(self.rgb_2 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Half(self):
        self.rgb_3 = half
        self.rgb_3_slider.Update(self.rgb_3, self.channel_width)
        self.layout.rgb_3_value.setValue(self.rgb_3 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
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
        self.ard_1_slider.Update(ang/360, self.channel_width)
        self.layout.ard_1_value.setValue((ang/360) * k_ANG)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Half(self):
        self.ard_2 = half
        self.ard_2_slider.Update(self.ard_2, self.channel_width)
        self.layout.ard_2_value.setValue(self.ard_2 * k_RDL)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
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
        self.ard_3_slider.Update(diagonal/360, self.channel_width)
        self.layout.ard_3_value.setValue((diagonal/360) * k_RDL)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
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
        self.hsv_1_slider.Update(hue/360, self.channel_width)
        self.layout.hsv_1_value.setValue((hue/360) * k_HUE)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Half(self):
        self.hsv_2 = half
        self.hsv_2_slider.Update(self.hsv_2, self.channel_width)
        self.layout.hsv_2_value.setValue(self.hsv_2 * k_SVL)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Half(self):
        self.hsv_3 = half
        self.hsv_3_slider.Update(self.hsv_3, self.channel_width)
        self.layout.hsv_3_value.setValue(self.hsv_3 * k_SVL)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
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
        self.hsl_1_slider.Update(hue/360, self.channel_width)
        self.layout.hsl_1_value.setValue((hue/360) * k_HUE)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Half(self):
        self.hsl_2 = half
        self.hsl_2_slider.Update(self.hsl_2, self.channel_width)
        self.layout.hsl_2_value.setValue(self.hsl_2 * k_SVL)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Half(self):
        self.hsl_3 = half
        self.hsl_3_slider.Update(self.hsl_3, self.channel_width)
        self.layout.hsl_3_value.setValue(self.hsl_3 * k_SVL)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Half(self):
        # Nearest Pure Color Pick
        hue = self.hcy_1 * 360
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
        self.hcy_1_slider.Update(hue/360, self.channel_width)
        self.layout.hcy_1_value.setValue((hue/360) * k_HUE)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Half(self):
        self.hcy_2 = half
        self.hcy_2_slider.Update(self.hcy_2, self.channel_width)
        self.layout.hcy_2_value.setValue(self.hcy_2 * k_SVL)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Half(self):
        self.hcy_3 = half
        self.hcy_3_slider.Update(self.hcy_3, self.channel_width)
        self.layout.hcy_3_value.setValue(self.hcy_3 * k_SVL)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_1_Half(self):
        self.yuv_1 = half
        self.yuv_1_slider.Update(self.yuv_1, self.channel_width)
        self.layout.yuv_1_value.setValue(self.yuv_1 * k_Y)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_2_Half(self):
        self.yuv_2 = half
        self.yuv_2_slider.Update(self.yuv_2, self.channel_width)
        self.layout.yuv_2_value.setValue(self.yuv_2 * k_U)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_3_Half(self):
        self.yuv_3 = half
        self.yuv_3_slider.Update(self.yuv_3, self.channel_width)
        self.layout.yuv_3_value.setValue(self.yuv_3 * k_V)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_1_Half(self):
        self.ryb_1 = half
        self.ryb_1_slider.Update(self.ryb_1, self.channel_width)
        self.layout.ryb_1_value.setValue(self.ryb_1 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_2_Half(self):
        self.ryb_2 = half
        self.ryb_2_slider.Update(self.ryb_2, self.channel_width)
        self.layout.ryb_2_value.setValue(self.ryb_2 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_3_Half(self):
        self.ryb_3 = half
        self.ryb_3_slider.Update(self.ryb_3, self.channel_width)
        self.layout.ryb_3_value.setValue(self.ryb_3 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Half(self):
        self.cmy_1 = half
        self.cmy_1_slider.Update(self.cmy_1, self.channel_width)
        self.layout.cmy_1_value.setValue(self.cmy_1 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Half(self):
        self.cmy_2 = half
        self.cmy_2_slider.Update(self.cmy_2, self.channel_width)
        self.layout.cmy_2_value.setValue(self.cmy_2 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Half(self):
        self.cmy_3 = half
        self.cmy_3_slider.Update(self.cmy_3, self.channel_width)
        self.layout.cmy_3_value.setValue(self.cmy_3 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Half(self):
        self.cmyk_1 = half
        self.cmyk_1_slider.Update(self.cmyk_1, self.channel_width)
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Half(self):
        self.cmyk_2 = half
        self.cmyk_2_slider.Update(self.cmyk_2, self.channel_width)
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Half(self):
        self.cmyk_3 = half
        self.cmyk_3_slider.Update(self.cmyk_3, self.channel_width)
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Half(self):
        self.cmyk_4 = half
        self.cmyk_4_slider.Update(self.cmyk_4, self.channel_width)
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Half(self):
        self.kkk_0 = k_KKKhalf
        self.kkk_1_slider.Update(0.5, self.channel_width)
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Minus(self):
        self.aaa_1 = self.aaa_1 - u_RGB
        if self.aaa_1 <= zero:
            self.aaa_1 = zero
        self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
        self.layout.aaa_1_value.setValue(self.aaa_1 * k_RGB)
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Minus(self):
        self.rgb_1 = self.rgb_1 - u_RGB
        if self.rgb_1 <= zero:
            self.rgb_1 = zero
        self.rgb_1_slider.Update(self.rgb_1, self.channel_width)
        self.layout.rgb_1_value.setValue(self.rgb_1 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Minus(self):
        self.rgb_2 = self.rgb_2 - u_RGB
        if self.rgb_2 <= zero:
            self.rgb_2 = zero
        self.rgb_2_slider.Update(self.rgb_2, self.channel_width)
        self.layout.rgb_2_value.setValue(self.rgb_2 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Minus(self):
        self.rgb_3 = self.rgb_3 - u_RGB
        if self.rgb_3 <= zero:
            self.rgb_3 = zero
        self.rgb_3_slider.Update(self.rgb_3, self.channel_width)
        self.layout.rgb_3_value.setValue(self.rgb_3 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Minus(self):
        self.ard_1 = self.ard_1 - u_ANG
        if self.ard_1 <= zero:
            self.ard_1 = zero
        self.ard_1_slider.Update(self.ard_1, self.channel_width)
        self.layout.ard_1_value.setValue(self.ard_1 * k_ANG)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Minus(self):
        self.ard_2 = self.ard_2 - u_RDL
        if self.ard_2 <= zero:
            self.ard_2 = zero
        self.ard_2_slider.Update(self.ard_2, self.channel_width)
        self.layout.ard_2_value.setValue(self.ard_2 * k_RDL)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Minus(self):
        self.ard_3 = self.ard_3 - u_RDL
        if self.ard_3 <= zero:
            self.ard_3 = zero
        self.ard_3_slider.Update(self.ard_3, self.channel_width)
        self.layout.ard_3_value.setValue(self.ard_3 * k_RDL)
        self.Pigment_Convert("ARD", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Minus(self):
        self.hsv_1 = self.hsv_1 - u_HUE
        if self.hsv_1 <= zero:
            self.hsv_1 = zero
        self.hsv_1_slider.Update(self.hsv_1, self.channel_width)
        self.layout.hsv_1_value.setValue(self.hsv_1 * k_HUE)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Minus(self):
        self.hsv_2 = self.hsv_2 - u_SVCLY
        if self.hsv_2 <= zero:
            self.hsv_2 = zero
        self.hsv_2_slider.Update(self.hsv_2, self.channel_width)
        self.layout.hsv_2_value.setValue(self.hsv_2 * k_SVL)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Minus(self):
        self.hsv_3 = self.hsv_3 - u_SVCLY
        if self.hsv_3 <= zero:
            self.hsv_3 = zero
        self.hsv_3_slider.Update(self.hsv_3, self.channel_width)
        self.layout.hsv_3_value.setValue(self.hsv_3 * k_SVL)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Minus(self):
        self.hsl_1 = self.hsl_1 - u_HUE
        if self.hsl_1 <= zero:
            self.hsl_1 = zero
        self.hsl_1_slider.Update(self.hsl_1, self.channel_width)
        self.layout.hsl_1_value.setValue(self.hsl_1 * k_HUE)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Minus(self):
        self.hsl_2 = self.hsl_2 - u_SVCLY
        if self.hsl_2 <= zero:
            self.hsl_2 = zero
        self.hsl_2_slider.Update(self.hsl_2, self.channel_width)
        self.layout.hsl_2_value.setValue(self.hsl_2 * k_SVL)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Minus(self):
        self.hsl_3 = self.hsl_3 - u_SVCLY
        if self.hsl_3 <= zero:
            self.hsl_3 = zero
        self.hsl_3_slider.Update(self.hsl_3, self.channel_width)
        self.layout.hsl_3_value.setValue(self.hsl_3 * k_SVL)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Minus(self):
        self.hcy_1 = self.hcy_1 - u_HUE
        if self.hcy_1 <= zero:
            self.hcy_1 = zero
        self.hcy_1_slider.Update(self.hcy_1, self.channel_width)
        self.layout.hcy_1_value.setValue(self.hcy_1 * k_HUE)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Minus(self):
        self.hcy_2 = self.hcy_2 - u_SVCLY
        if self.hcy_2 <= zero:
            self.hcy_2 = zero
        self.hcy_2_slider.Update(self.hcy_2, self.channel_width)
        self.layout.hcy_2_value.setValue(self.hcy_2 * k_SVL)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Minus(self):
        self.hcy_3 = self.hcy_3 - u_SVCLY
        if self.hcy_3 <= zero:
            self.hcy_3 = zero
        self.hcy_3_slider.Update(self.hcy_3, self.channel_width)
        self.layout.hcy_3_value.setValue(self.hcy_3 * k_SVL)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_1_Minus(self):
        self.yuv_1 = self.yuv_1 - u_Y
        if self.yuv_1 <= zero:
            self.yuv_1 = zero
        self.yuv_1_slider.Update(self.yuv_1, self.channel_width)
        self.layout.yuv_1_value.setValue(self.yuv_1 * k_Y)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_2_Minus(self):
        self.yuv_2 = self.yuv_2 - u_U
        if self.yuv_2 <= zero:
            self.yuv_2 = zero
        self.yuv_2_slider.Update(self.yuv_2, self.channel_width)
        self.layout.yuv_2_value.setValue(self.yuv_2 * k_U)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_3_Minus(self):
        self.yuv_3 = self.yuv_3 - u_V
        if self.yuv_3 <= zero:
            self.yuv_3 = zero
        self.yuv_3_slider.Update(self.yuv_3, self.channel_width)
        self.layout.yuv_3_value.setValue(self.yuv_3 * k_V)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_1_Minus(self):
        self.ryb_1 = self.ryb_1 - u_RYB
        if self.ryb_1 <= zero:
            self.ryb_1 = zero
        self.ryb_1_slider.Update(self.ryb_1, self.channel_width)
        self.layout.ryb_1_value.setValue(self.ryb_1 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_2_Minus(self):
        self.ryb_2 = self.ryb_2 - u_RYB
        if self.ryb_2 <= zero:
            self.ryb_2 = zero
        self.ryb_2_slider.Update(self.ryb_2, self.channel_width)
        self.layout.ryb_2_value.setValue(self.ryb_2 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_3_Minus(self):
        self.ryb_3 = self.ryb_3 - u_RYB
        if self.ryb_3 <= zero:
            self.ryb_3 = zero
        self.ryb_3_slider.Update(self.ryb_3, self.channel_width)
        self.layout.ryb_3_value.setValue(self.ryb_3 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Minus(self):
        self.cmy_1 = self.cmy_1 - u_CMY
        if self.cmy_1 <= zero:
            self.cmy_1 = zero
        self.cmy_1_slider.Update(self.cmy_1, self.channel_width)
        self.layout.cmy_1_value.setValue(self.cmy_1 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Minus(self):
        self.cmy_2 = self.cmy_2 - u_CMY
        if self.cmy_2 <= zero:
            self.cmy_2 = zero
        self.cmy_2_slider.Update(self.cmy_2, self.channel_width)
        self.layout.cmy_2_value.setValue(self.cmy_2 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Minus(self):
        self.cmy_3 = self.cmy_3 - u_CMY
        if self.cmy_3 <= zero:
            self.cmy_3 = zero
        self.cmy_3_slider.Update(self.cmy_3, self.channel_width)
        self.layout.cmy_3_value.setValue(self.cmy_3 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Minus(self):
        self.cmyk_1 = self.cmyk_1 - u_CMYK
        if self.cmyk_1 <= zero:
            self.cmyk_1 = zero
        self.cmyk_1_slider.Update(self.cmyk_1, self.channel_width)
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Minus(self):
        self.cmyk_2 = self.cmyk_2 - u_CMYK
        if self.cmyk_2 <= zero:
            self.cmyk_2 = zero
        self.cmyk_2_slider.Update(self.cmyk_2, self.channel_width)
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Minus(self):
        self.cmyk_3 = self.cmyk_3 - u_CMYK
        if self.cmyk_3 <= zero:
            self.cmyk_3 = zero
        self.cmyk_3_slider.Update(self.cmyk_3, self.channel_width)
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Minus(self):
        self.cmyk_4 = self.cmyk_4 - u_CMYK
        if self.cmyk_4 <= zero:
            self.cmyk_4 = zero
        self.cmyk_4_slider.Update(self.cmyk_4, self.channel_width)
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Minus(self):
        self.kkk_0 = self.kkk_0 - k_KKKunit
        if self.kkk_0 <= zero:
            self.kkk_0 = zero
        self.kkk_1_slider.Update((self.kkk_0 - k_KKKmin) / k_KKKdelta, self.channel_width)
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Plus(self):
        self.aaa_1 = self.aaa_1 + u_AAA
        if self.aaa_1 >= unit:
            self.aaa_1 = unit
        self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
        self.layout.aaa_1_value.setValue(self.aaa_1 * k_AAA)
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Plus(self):
        self.rgb_1 = self.rgb_1 + u_RGB
        if self.rgb_1 >= unit:
            self.rgb_1 = unit
        self.rgb_1_slider.Update(self.rgb_1, self.channel_width)
        self.layout.rgb_1_value.setValue(self.rgb_1 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Plus(self):
        self.rgb_2 = self.rgb_2 + u_RGB
        if self.rgb_2 >= unit:
            self.rgb_2 = unit
        self.rgb_2_slider.Update(self.rgb_2, self.channel_width)
        self.layout.rgb_2_value.setValue(self.rgb_2 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Plus(self):
        self.rgb_3 = self.rgb_3 + u_RGB
        if self.rgb_3 >= unit:
            self.rgb_3 = unit
        self.rgb_3_slider.Update(self.rgb_3, self.channel_width)
        self.layout.rgb_3_value.setValue(self.rgb_3 * k_RGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Plus(self):
        self.ard_1 = self.ard_1 + u_ANG
        if self.ard_1 >= unit:
            self.ard_1 = unit
        self.ard_1_slider.Update(self.ard_1, self.channel_width)
        self.layout.ard_1_value.setValue(self.ard_1 * k_ANG)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Plus(self):
        self.ard_2 = self.ard_2 + u_RDL
        if self.ard_2 >= unit:
            self.ard_2 = unit
        self.ard_2_slider.Update(self.ard_2, self.channel_width)
        self.layout.ard_2_value.setValue(self.ard_2 * k_RDL)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Plus(self):
        self.ard_3 = self.ard_3 + u_RDL
        if self.ard_3 >= unit:
            self.ard_3 = unit
        self.ard_3_slider.Update(self.ard_3, self.channel_width)
        self.layout.ard_3_value.setValue(self.ard_3 * k_RDL)
        self.Pigment_Convert("ARD", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Plus(self):
        self.hsv_1 = self.hsv_1 + u_HUE
        if self.hsv_1 >= unit:
            self.hsv_1 = unit
        self.hsv_1_slider.Update(self.hsv_1, self.channel_width)
        self.layout.hsv_1_value.setValue(self.hsv_1 * k_HUE)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Plus(self):
        self.hsv_2 = self.hsv_2 + u_SVCLY
        if self.hsv_2 >= unit:
            self.hsv_2 = unit
        self.hsv_2_slider.Update(self.hsv_2, self.channel_width)
        self.layout.hsv_2_value.setValue(self.hsv_2 * k_SVL)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Plus(self):
        self.hsv_3 = self.hsv_3 + u_SVCLY
        if self.hsv_3 >= unit:
            self.hsv_3 = unit
        self.hsv_3_slider.Update(self.hsv_3, self.channel_width)
        self.layout.hsv_3_value.setValue(self.hsv_3 * k_SVL)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Plus(self):
        self.hsl_1 = self.hsl_1 + u_HUE
        if self.hsl_1 >= unit:
            self.hsl_1 = unit
        self.hsl_1_slider.Update(self.hsl_1, self.channel_width)
        self.layout.hsl_1_value.setValue(self.hsl_1 * k_HUE)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Plus(self):
        self.hsl_2 = self.hsl_2 + u_SVCLY
        if self.hsl_2 >= unit:
            self.hsl_2 = unit
        self.hsl_2_slider.Update(self.hsl_2, self.channel_width)
        self.layout.hsl_2_value.setValue(self.hsl_2 * k_SVL)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Plus(self):
        self.hsl_3 = self.hsl_3 + u_SVCLY
        if self.hsl_3 >= unit:
            self.hsl_3 = unit
        self.hsl_3_slider.Update(self.hsl_3, self.channel_width)
        self.layout.hsl_3_value.setValue(self.hsl_3 * k_SVL)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Plus(self):
        self.hcy_1 = self.hcy_1 + u_HUE
        if self.hcy_1 >= unit:
            self.hcy_1 = unit
        self.hcy_1_slider.Update(self.hcy_1, self.channel_width)
        self.layout.hcy_1_value.setValue(self.hcy_1 * k_HUE)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Plus(self):
        self.hcy_2 = self.hcy_2 + u_SVCLY
        if self.hcy_2 >= unit:
            self.hcy_2 = unit
        self.hcy_2_slider.Update(self.hcy_2, self.channel_width)
        self.layout.hcy_2_value.setValue(self.hcy_2 * k_SVL)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Plus(self):
        self.hcy_3 = self.hcy_3 + u_SVCLY
        if self.hcy_3 >= unit:
            self.hcy_3 = unit
        self.hcy_3_slider.Update(self.hcy_3, self.channel_width)
        self.layout.hcy_3_value.setValue(self.hcy_3 * k_SVL)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_1_Plus(self):
        self.yuv_1 = self.yuv_1 + u_Y
        if self.yuv_1 >= unit:
            self.yuv_1 = unit
        self.yuv_1_slider.Update(self.yuv_1, self.channel_width)
        self.layout.yuv_1_value.setValue(self.yuv_1 * k_Y)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_2_Plus(self):
        self.yuv_2 = self.yuv_2 + u_U
        if self.yuv_2 >= unit:
            self.yuv_2 = unit
        self.yuv_2_slider.Update(self.yuv_2, self.channel_width)
        self.layout.yuv_2_value.setValue(self.yuv_2 * k_U)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_3_Plus(self):
        self.yuv_3 = self.yuv_3 + u_V
        if self.yuv_3 >= unit:
            self.yuv_3 = unit
        self.yuv_3_slider.Update(self.yuv_3, self.channel_width)
        self.layout.yuv_3_value.setValue(self.yuv_3 * k_V)
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_1_Plus(self):
        self.ryb_1 = self.ryb_1 + u_RYB
        if self.ryb_1 >= unit:
            self.ryb_1 = unit
        self.ryb_1_slider.Update(self.ryb_1, self.channel_width)
        self.layout.ryb_1_value.setValue(self.ryb_1 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_2_Plus(self):
        self.ryb_2 = self.ryb_2 + u_RYB
        if self.ryb_2 >= unit:
            self.ryb_2 = unit
        self.ryb_2_slider.Update(self.ryb_2, self.channel_width)
        self.layout.ryb_2_value.setValue(self.ryb_2 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_3_Plus(self):
        self.ryb_3 = self.ryb_3 + u_RYB
        if self.ryb_3 >= unit:
            self.ryb_3 = unit
        self.ryb_3_slider.Update(self.ryb_3, self.channel_width)
        self.layout.ryb_3_value.setValue(self.ryb_3 * k_RYB)
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Plus(self):
        self.cmy_1 = self.cmy_1 + u_CMY
        if self.cmy_1 >= unit:
            self.cmy_1 = unit
        self.cmy_1_slider.Update(self.cmy_1, self.channel_width)
        self.layout.cmy_1_value.setValue(self.cmy_1 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Plus(self):
        self.cmy_2 = self.cmy_2 + u_CMY
        if self.cmy_2 >= unit:
            self.cmy_2 = unit
        self.cmy_2_slider.Update(self.cmy_2, self.channel_width)
        self.layout.cmy_2_value.setValue(self.cmy_2 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Plus(self):
        self.cmy_3 = self.cmy_3 + u_CMY
        if self.cmy_3 >= unit:
            self.cmy_3 = unit
        self.cmy_3_slider.Update(self.cmy_3, self.channel_width)
        self.layout.cmy_3_value.setValue(self.cmy_3 * k_CMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Plus(self):
        self.cmyk_1 = self.cmyk_1 + u_CMYK
        if self.cmyk_1 >= unit:
            self.cmyk_1 = unit
        self.cmyk_1_slider.Update(self.cmyk_1, self.channel_width)
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Plus(self):
        self.cmyk_2 = self.cmyk_2 + u_CMYK
        if self.cmyk_2 >= unit:
            self.cmyk_2 = unit
        self.cmyk_2_slider.Update(self.cmyk_2, self.channel_width)
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Plus(self):
        self.cmyk_3 = self.cmyk_3 + u_CMYK
        if self.cmyk_3 >= unit:
            self.cmyk_3 = unit
        self.cmyk_3_slider.Update(self.cmyk_3, self.channel_width)
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Plus(self):
        self.cmyk_4 = self.cmyk_4 + u_CMYK
        if self.cmyk_4 >= unit:
            self.cmyk_4 = unit
        self.cmyk_4_slider.Update(self.cmyk_4, self.channel_width)
        self.layout.cmyk_3_value.setValue(self.cmyk_4 * k_CMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Plus(self):
        self.kkk_0 = self.kkk_0 + k_KKKunit
        if self.kkk_0 >= k_KKKmax:
            self.kkk_0 = k_KKKmax
        self.kkk_1_slider.Update((self.kkk_0 - k_KKKmin) / k_KKKdelta, self.channel_width)
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Slider_Modify(self, SIGNAL_VALUE):
        self.aaa_1 = SIGNAL_VALUE
        send = int(self.aaa_1 * k_AAA)
        self.layout.aaa_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("AAA", 0)
    def Pigment_RGB_1_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_1 = SIGNAL_VALUE
        send = int(self.rgb_1 * k_RGB)
        self.layout.rgb_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_2_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_2 = SIGNAL_VALUE
        send = int(self.rgb_2 * k_RGB)
        self.layout.rgb_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_3_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_3 = SIGNAL_VALUE
        send = int(self.rgb_3 * k_RGB)
        self.layout.rgb_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_ARD_1_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_1 = SIGNAL_VALUE
        send = int(self.ard_1 * k_ANG)
        self.layout.ard_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_2_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_2 = SIGNAL_VALUE
        send = int(self.ard_2 * k_RDL)
        self.layout.ard_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_3_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_3 = SIGNAL_VALUE
        send = int(self.ard_3 * k_RDL)
        self.layout.ard_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_HSV_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_1 = SIGNAL_VALUE
        send = int(self.hsv_1 * k_HUE)
        self.layout.hsv_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_2 = SIGNAL_VALUE
        send = int(self.hsv_2 * k_SVL)
        self.layout.hsv_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_3 = SIGNAL_VALUE
        send = int(self.hsv_3 * k_SVL)
        self.layout.hsv_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSL_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_1 = SIGNAL_VALUE
        send = int(self.hsl_1 * k_HUE)
        self.layout.hsl_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_2 = SIGNAL_VALUE
        send = int(self.hsl_2 * k_SVL)
        self.layout.hsl_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_3 = SIGNAL_VALUE
        send = int(self.hsl_3 * k_SVL)
        self.layout.hsl_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HCY_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hcy_1 = SIGNAL_VALUE
        send = int(self.hcy_1 * k_HUE)
        self.layout.hcy_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hcy_2 = SIGNAL_VALUE
        send = int(self.hcy_2 * k_SVL)
        self.layout.hcy_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hcy_3 = SIGNAL_VALUE
        send = int(self.hcy_3 * k_SVL)
        self.layout.hcy_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_YUV_1_Slider_Modify(self, SIGNAL_VALUE):
        self.yuv_1 = SIGNAL_VALUE
        send = int(self.yuv_1 * k_Y)
        self.layout.yuv_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("YUV", 0)
    def Pigment_YUV_2_Slider_Modify(self, SIGNAL_VALUE):
        self.yuv_2 = SIGNAL_VALUE
        send = int(self.yuv_2 * k_U)
        self.layout.yuv_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(-50+SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("YUV", 0)
    def Pigment_YUV_3_Slider_Modify(self, SIGNAL_VALUE):
        self.yuv_3 = SIGNAL_VALUE
        send = int(self.yuv_3 * k_V)
        self.layout.yuv_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(-50+SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("YUV", 0)
    def Pigment_RYB_1_Slider_Modify(self, SIGNAL_VALUE):
        self.ryb_1 = SIGNAL_VALUE
        send = int(self.ryb_1 * k_RYB)
        self.layout.ryb_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RYB", 0)
    def Pigment_RYB_2_Slider_Modify(self, SIGNAL_VALUE):
        self.ryb_2 = SIGNAL_VALUE
        send = int(self.ryb_2 * k_RYB)
        self.layout.ryb_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RYB", 0)
    def Pigment_RYB_3_Slider_Modify(self, SIGNAL_VALUE):
        self.ryb_3 = SIGNAL_VALUE
        send = int(self.ryb_3 * k_RYB)
        self.layout.ryb_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RYB", 0)
    def Pigment_CMY_1_Slider_Modify(self, SIGNAL_VALUE):
        self.cmy_1 = SIGNAL_VALUE
        send = int(self.cmy_1 * k_CMY)
        self.layout.cmy_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_2_Slider_Modify(self, SIGNAL_VALUE):
        self.cmy_2 = SIGNAL_VALUE
        send = int(self.cmy_2 * k_CMY)
        self.layout.cmy_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_3_Slider_Modify(self, SIGNAL_VALUE):
        self.cmy_3 = SIGNAL_VALUE
        send = int(self.cmy_3 * k_CMY)
        self.layout.cmy_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMYK_1_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_1 = SIGNAL_VALUE
        send = int(self.cmyk_1 * k_CMYK)
        self.layout.cmyk_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_2_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_2 = SIGNAL_VALUE
        send = int(self.cmyk_2 * k_CMYK)
        self.layout.cmyk_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_3_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_3 = SIGNAL_VALUE
        send = int(self.cmyk_3 * k_CMYK)
        self.layout.cmyk_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_4_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_4 = SIGNAL_VALUE
        send = int(self.cmyk_4 * k_CMYK)
        self.layout.cmyk_4_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_KKK_1_Slider_Modify(self, SIGNAL_VALUE):
        self.kkk_0 = int((SIGNAL_VALUE * k_KKKdelta) + k_KKKmin)
        self.layout.kkk_1_value.setValue(self.kkk_0)
        # self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.kkk_to_lights(self.layout.kkk_1_value.value())
        self.Pigment_Convert("KKK", 0)

    def Pigment_AAA_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Slider_Release(self, SIGNAL_RELEASE):
        self.sync = ["HSV", 0]
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Slider_Release(self, SIGNAL_RELEASE):
        self.sync = ["HSV", 0]
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Slider_Release(self, SIGNAL_RELEASE):
        self.sync = ["HSV", 0]
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.layout.label.setText("")
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Value_Modify(self):
        self.aaa_1 = self.layout.aaa_1_value.value() / k_AAA
        self.aaa_1_slider.Update(self.aaa_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.aaa_1*100,2))+" %")
        self.Pigment_Convert("AAA", 0)
    def Pigment_RGB_1_Value_Modify(self):
        self.rgb_1 = self.layout.rgb_1_value.value() / k_RGB
        self.rgb_1_slider.Update(self.rgb_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.rgb_1*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_2_Value_Modify(self):
        self.rgb_2 = self.layout.rgb_2_value.value() / k_RGB
        self.rgb_2_slider.Update(self.rgb_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.rgb_2*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_3_Value_Modify(self):
        self.rgb_3 = self.layout.rgb_3_value.value() / k_RGB
        self.rgb_3_slider.Update(self.rgb_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.rgb_3*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_ARD_1_Value_Modify(self):
        self.ard_1 = self.layout.ard_1_value.value() / k_ANG
        self.ard_1_slider.Update(self.ard_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.ard_1*100,2))+" º")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_2_Value_Modify(self):
        self.ard_2 = self.layout.ard_2_value.value() / k_RDL
        self.ard_2_slider.Update(self.ard_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.ard_2*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_3_Value_Modify(self):
        self.ard_3 = self.layout.ard_3_value.value() / k_RDL
        self.ard_3_slider.Update(self.ard_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.ard_3*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_HSV_1_Value_Modify(self):
        self.hsv_1 = self.layout.hsv_1_value.value() / k_HUE
        self.hsv_1_slider.Update(self.hsv_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hsv_1*100,2))+" º")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_2_Value_Modify(self):
        self.hsv_2 = self.layout.hsv_2_value.value() / k_SVL
        self.hsv_2_slider.Update(self.hsv_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hsv_2*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_3_Value_Modify(self):
        self.hsv_3 = self.layout.hsv_3_value.value() / k_SVL
        self.hsv_3_slider.Update(self.hsv_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hsv_3*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSL_1_Value_Modify(self):
        self.hsl_1 = self.layout.hsl_1_value.value() / k_HUE
        self.hsl_1_slider.Update(self.hsl_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hsl_1*100,2))+" º")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_2_Value_Modify(self):
        self.hsl_2 = self.layout.hsl_2_value.value() / k_SVL
        self.hsl_2_slider.Update(self.hsl_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hsl_2*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_3_Value_Modify(self):
        self.hsl_3 = self.layout.hsl_3_value.value() / k_SVL
        self.hsl_3_slider.Update(self.hsl_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hsl_3*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HCY_1_Value_Modify(self):
        self.hcy_1 = self.layout.hcy_1_value.value() / k_HUE
        self.hcy_1_slider.Update(self.hcy_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hcy_1*100,2))+" º")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_2_Value_Modify(self):
        self.hcy_2 = self.layout.hcy_2_value.value() / k_SVL
        self.hcy_2_slider.Update(self.hcy_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hcy_2*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_3_Value_Modify(self):
        self.hcy_3 = self.layout.hcy_3_value.value() / k_SVL
        self.hcy_3_slider.Update(self.hcy_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.hcy_3*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_YUV_1_Value_Modify(self):
        self.yuv_1 = self.layout.yuv_1_value.value() / k_Y
        self.yuv_1_slider.Update(self.yuv_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.yuv_1*100,2))+" %")
        self.Pigment_Convert("YUV", 0)
    def Pigment_YUV_2_Value_Modify(self):
        self.yuv_2 = self.layout.yuv_2_value.value() / k_U
        self.yuv_2_slider.Update(self.yuv_2, self.channel_width)
        self.layout.label_percent.setText(str(round(-50+self.yuv_2*100,2))+" %")
        self.Pigment_Convert("YUV", 0)
    def Pigment_YUV_3_Value_Modify(self):
        self.yuv_3 = self.layout.yuv_3_value.value() / k_V
        self.yuv_3_slider.Update(self.yuv_3, self.channel_width)
        self.layout.label_percent.setText(str(round(-50+self.yuv_3*100,2))+" %")
        self.Pigment_Convert("YUV", 0)
    def Pigment_RYB_1_Value_Modify(self):
        self.rgb_1 = self.layout.rgb_1_value.value() / k_RYB
        self.rgb_1_slider.Update(self.rgb_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.rgb_1*100,2))+" %")
        self.Pigment_Convert("RYB", 0)
    def Pigment_RYB_2_Value_Modify(self):
        self.rgb_2 = self.layout.rgb_2_value.value() / k_RYB
        self.rgb_2_slider.Update(self.rgb_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.rgb_2*100,2))+" %")
        self.Pigment_Convert("RYB", 0)
    def Pigment_RYB_3_Value_Modify(self):
        self.rgb_3 = self.layout.rgb_3_value.value() / k_RYB
        self.rgb_3_slider.Update(self.rgb_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.rgb_3*100,2))+" %")
        self.Pigment_Convert("RYB", 0)
    def Pigment_CMY_1_Value_Modify(self):
        self.cmy_1 = self.layout.cmy_1_value.value() / k_CMY
        self.cmy_1_slider.Update(self.cmy_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmy_1*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_2_Value_Modify(self):
        self.cmy_2 = self.layout.cmy_2_value.value() / k_CMY
        self.cmy_2_slider.Update(self.cmy_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmy_2*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_3_Value_Modify(self):
        self.cmy_3 = self.layout.cmy_3_value.value() / k_CMY
        self.cmy_3_slider.Update(self.cmy_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmy_3*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMYK_1_Value_Modify(self):
        self.cmyk_1 = self.layout.cmyk_1_value.value() / k_CMYK
        self.cmyk_1_slider.Update(self.cmyk_1, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmyk_1*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_2_Value_Modify(self):
        self.cmyk_2 = self.layout.cmyk_2_value.value() / k_CMYK
        self.cmyk_2_slider.Update(self.cmyk_2, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmyk_2*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_3_Value_Modify(self):
        self.cmyk_3 = self.layout.cmyk_3_value.value() / k_CMYK
        self.cmyk_3_slider.Update(self.cmyk_3, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmyk_3*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_4_Value_Modify(self):
        self.cmyk_4 = self.layout.cmyk_4_value.value() / k_CMYK
        self.cmyk_4_slider.Update(self.cmyk_4, self.channel_width)
        self.layout.label_percent.setText(str(round(self.cmyk_4*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_KKK_1_Value_Modify(self):
        self.kkk_0 = self.layout.kkk_1_value.value()
        self.kkk_1_slider.Update((self.kkk_0 - k_KKKmin) / k_KKKdelta, self.channel_width)
        # self.layout.label_percent.setText(str(round(((self.kkk_0 - k_KKKmin) / k_KKKdelta)*100,2))+" %")
        self.kkk_to_lights(self.layout.kkk_1_value.value())
        self.Pigment_Convert("KKK", 0)

    def Pigment_AAA_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
        self.layout.label_percent.setText("")
    def Pigment_RGB_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_YUV_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("YUV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
        self.layout.label_percent.setText("")
    def Pigment_RYB_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RYB_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("RYB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
        self.layout.label_percent.setText("")
    def Pigment_CMY_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Value_Release(self):
        self.layout.label_percent.setText("")
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Value_Release(self):
        self.layout.label_percent.setText("")
        self.layout.label.setText("")
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

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
            self.layout.tip_00.update()
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

    #//
    #\\ Palette ################################################################
    def Cor_00_APPLY(self, SIGNAL_CLICKS):
        if self.cor_00[0] == "True":
            self.Color_ANGLE(self.cor_00[1], self.cor_00[2], self.cor_00[3])
            self.Color_APPLY("RGB", self.cor_00[1], self.cor_00[2], self.cor_00[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_00_SAVE(self, SIGNAL_CLICKS):
        self.cor_00 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_00[1]*255, self.cor_00[2]*255, self.cor_00[3]*255))
        self.layout.cor_00.setStyleSheet(color)
    def Cor_00_CLEAN(self, SIGNAL_CLICKS):
        self.cor_00 = ["False", 0, 0, 0]
        self.layout.cor_00.setStyleSheet(bg_alpha)

    def Cor_01_APPLY(self, SIGNAL_CLICKS):
        if self.cor_01[0] == "True":
            self.Color_ANGLE(self.cor_01[1], self.cor_01[2], self.cor_01[3])
            self.Color_APPLY("RGB", self.cor_01[1], self.cor_01[2], self.cor_01[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_01_SAVE(self, SIGNAL_CLICKS):
        self.cor_01 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_01[1]*255, self.cor_01[2]*255, self.cor_01[3]*255))
        self.layout.cor_01.setStyleSheet(color)
    def Cor_01_CLEAN(self, SIGNAL_CLICKS):
        self.cor_01 = ["False", 0, 0, 0]
        self.layout.cor_01.setStyleSheet(bg_alpha)

    def Cor_02_APPLY(self, SIGNAL_CLICKS):
        if self.cor_02[0] == "True":
            self.Color_ANGLE(self.cor_02[1], self.cor_02[2], self.cor_02[3])
            self.Color_APPLY("RGB", self.cor_02[1], self.cor_02[2], self.cor_02[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_02_SAVE(self, SIGNAL_CLICKS):
        self.cor_02 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]

        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_02[1]*255, self.cor_02[2]*255, self.cor_02[3]*255))
        self.layout.cor_02.setStyleSheet(color)
    def Cor_02_CLEAN(self, SIGNAL_CLICKS):
        self.cor_02 = ["False", 0, 0, 0]
        self.layout.cor_02.setStyleSheet(bg_alpha)

    def Cor_03_APPLY(self, SIGNAL_CLICKS):
        if self.cor_03[0] == "True":
            self.Color_ANGLE(self.cor_03[1], self.cor_03[2], self.cor_03[3])
            self.Color_APPLY("RGB", self.cor_03[1], self.cor_03[2], self.cor_03[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_03_SAVE(self, SIGNAL_CLICKS):
        self.cor_03 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_03[1]*255, self.cor_03[2]*255, self.cor_03[3]*255))
        self.layout.cor_03.setStyleSheet(color)
    def Cor_03_CLEAN(self, SIGNAL_CLICKS):
        self.cor_03 = ["False", 0, 0, 0]
        self.layout.cor_03.setStyleSheet(bg_alpha)

    def Cor_04_APPLY(self, SIGNAL_CLICKS):
        if self.cor_04[0] == "True":
            self.Color_ANGLE(self.cor_04[1], self.cor_04[2], self.cor_04[3])
            self.Color_APPLY("RGB", self.cor_04[1], self.cor_04[2], self.cor_04[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_04_SAVE(self, SIGNAL_CLICKS):
        self.cor_04 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_04[1]*255, self.cor_04[2]*255, self.cor_04[3]*255))
        self.layout.cor_04.setStyleSheet(color)
    def Cor_04_CLEAN(self, SIGNAL_CLICKS):
        self.cor_04 = ["False", 0, 0, 0]
        self.layout.cor_04.setStyleSheet(bg_alpha)

    def Cor_05_APPLY(self, SIGNAL_CLICKS):
        if self.cor_05[0] == "True":
            self.Color_ANGLE(self.cor_05[1], self.cor_05[2], self.cor_05[3])
            self.Color_APPLY("RGB", self.cor_05[1], self.cor_05[2], self.cor_05[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_05_SAVE(self, SIGNAL_CLICKS):
        self.cor_05 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_05[1]*255, self.cor_05[2]*255, self.cor_05[3]*255))
        self.layout.cor_05.setStyleSheet(color)
    def Cor_05_CLEAN(self, SIGNAL_CLICKS):
        self.cor_05 = ["False", 0, 0, 0]
        self.layout.cor_05.setStyleSheet(bg_alpha)

    def Cor_06_APPLY(self, SIGNAL_CLICKS):
        if self.cor_06[0] == "True":
            self.Color_ANGLE(self.cor_06[1], self.cor_06[2], self.cor_06[3])
            self.Color_APPLY("RGB", self.cor_06[1], self.cor_06[2], self.cor_06[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_06_SAVE(self, SIGNAL_CLICKS):
        self.cor_06 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_06[1]*255, self.cor_06[2]*255, self.cor_06[3]*255))
        self.layout.cor_06.setStyleSheet(color)
    def Cor_06_CLEAN(self, SIGNAL_CLICKS):
        self.cor_06 = ["False", 0, 0, 0]
        self.layout.cor_06.setStyleSheet(bg_alpha)

    def Cor_07_APPLY(self, SIGNAL_CLICKS):
        if self.cor_07[0] == "True":
            self.Color_ANGLE(self.cor_07[1], self.cor_07[2], self.cor_07[3])
            self.Color_APPLY("RGB", self.cor_07[1], self.cor_07[2], self.cor_07[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_07_SAVE(self, SIGNAL_CLICKS):
        self.cor_07 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_07[1]*255, self.cor_07[2]*255, self.cor_07[3]*255))
        self.layout.cor_07.setStyleSheet(color)
    def Cor_07_CLEAN(self, SIGNAL_CLICKS):
        self.cor_07 = ["False", 0, 0, 0]
        self.layout.cor_07.setStyleSheet(bg_alpha)

    def Cor_08_APPLY(self, SIGNAL_CLICKS):
        if self.cor_08[0] == "True":
            self.Color_ANGLE(self.cor_08[1], self.cor_08[2], self.cor_08[3])
            self.Color_APPLY("RGB", self.cor_08[1], self.cor_08[2], self.cor_08[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_08_SAVE(self, SIGNAL_CLICKS):
        self.cor_08 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_08[1]*255, self.cor_08[2]*255, self.cor_08[3]*255))
        self.layout.cor_08.setStyleSheet(color)
    def Cor_08_CLEAN(self, SIGNAL_CLICKS):
        self.cor_08 = ["False", 0, 0, 0]
        self.layout.cor_08.setStyleSheet(bg_alpha)

    def Cor_09_APPLY(self, SIGNAL_CLICKS):
        if self.cor_09[0] == "True":
            self.Color_ANGLE(self.cor_09[1], self.cor_09[2], self.cor_09[3])
            self.Color_APPLY("RGB", self.cor_09[1], self.cor_09[2], self.cor_09[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_09_SAVE(self, SIGNAL_CLICKS):
        self.cor_09 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_09[1]*255, self.cor_09[2]*255, self.cor_09[3]*255))
        self.layout.cor_09.setStyleSheet(color)
    def Cor_09_CLEAN(self, SIGNAL_CLICKS):
        self.cor_09 = ["False", 0, 0, 0]
        self.layout.cor_09.setStyleSheet(bg_alpha)

    def Cor_10_APPLY(self, SIGNAL_CLICKS):
        if self.cor_10[0] == "True":
            self.Color_ANGLE(self.cor_10[1], self.cor_10[2], self.cor_10[3])
            self.Color_APPLY("RGB", self.cor_10[1], self.cor_10[2], self.cor_10[3], 0)
            self.Pigment_Display_Release(0)
    def Cor_10_SAVE(self, SIGNAL_CLICKS):
        self.cor_10 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_10[1]*255, self.cor_10[2]*255, self.cor_10[3]*255))
        self.layout.cor_10.setStyleSheet(color)
    def Cor_10_CLEAN(self, SIGNAL_CLICKS):
        self.cor_10 = ["False", 0, 0, 0]
        self.layout.cor_10.setStyleSheet(bg_alpha)

    #//
    #\\ Mixer COLOR ############################################################
    # TTS
    def Mixer_TTS_APPLY(self, SIGNAL_APPLY):
        if self.color_tts[0] == "True":
            self.Color_APPLY("RGB", self.color_tts[1], self.color_tts[2], self.color_tts[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_TTS_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_tts = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        gray = self.rgb_to_aaa(self.rgb_1, self.rgb_2, self.rgb_3)
        self.gray_tts = [gray[0], gray[0], gray[0]]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ; " % (self.color_tts[1]*255, self.color_tts[2]*255, self.color_tts[3]*255))
        bg_gray_tts = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ; " % (self.gray_tts[0]*255, self.gray_tts[1]*255, self.gray_tts[2]*255))
        self.layout.tts_l1.setStyleSheet(color)
        self.layout.white.setStyleSheet(bg_white)
        self.layout.grey.setStyleSheet(bg_gray_tts)
        self.layout.black.setStyleSheet(bg_black)
        self.Mixer_Display()
    def Mixer_TTS_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_tts = ["False", 0, 0, 0]
        self.gray_tts = color_grey
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
        self.spacer_tint = 0
        self.spacer_tone = 0
        self.spacer_shade = 0
        self.mixer_tint.Update(self.spacer_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.spacer_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.spacer_shade, self.layout.shade.width())

    # RGB
    def Mixer_RGB_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l1[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_L1_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*255, self.color_rgb_l1[2]*255, self.color_rgb_l1[3]*255))
        self.layout.rgb_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l1 = ["False", 0, 0, 0]
        # Display
        self.layout.rgb_l1.setStyleSheet(bg_alpha)
        self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.mixer_width)

    def Mixer_RGB_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r1[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_R1_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*255, self.color_rgb_r1[2]*255, self.color_rgb_r1[3]*255))
        self.layout.rgb_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r1 = ["False", 0, 0, 0]
        # Display
        self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.mixer_width)

    def Mixer_RGB_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l2[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_L2_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*255, self.color_rgb_l2[2]*255, self.color_rgb_l2[3]*255))
        self.layout.rgb_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l2 = ["False", 0, 0, 0]
        # Display
        self.layout.rgb_l2.setStyleSheet(bg_alpha)
        self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.mixer_width)

    def Mixer_RGB_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r2[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_R2_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*255, self.color_rgb_r2[2]*255, self.color_rgb_r2[3]*255))
        self.layout.rgb_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r2 = ["False", 0, 0, 0]
        # Display
        self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.mixer_width)

    def Mixer_RGB_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l3[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_L3_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*255, self.color_rgb_l3[2]*255, self.color_rgb_l3[3]*255))
        self.layout.rgb_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l3 = ["False", 0, 0, 0]
        # Display
        self.layout.rgb_l3.setStyleSheet(bg_alpha)
        self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.mixer_width)

    def Mixer_RGB_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r3[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_R3_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*255, self.color_rgb_r3[2]*255, self.color_rgb_r3[3]*255))
        self.layout.rgb_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r3 = ["False", 0, 0, 0]
        # Display
        self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.mixer_width)

    # ARD
    def Mixer_ARD_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l1[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l1 = ["True", self.ard_1, self.ard_2, self.ard_3]
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l1 = ["False", 0, 0, 0, 0, 0, 0]
        # Display
        self.layout.ard_l1.setStyleSheet(bg_alpha)
        self.layout.ard_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g1 = 0
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.mixer_width)

    def Mixer_ARD_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r1[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r1 = ["True", self.ard_1, self.ard_2, self.ard_3]
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r1 = ["False", 0, 0, 0, 0, 0, 0]
        # Display
        self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.layout.ard_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g1 = 0
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.mixer_width)

    def Mixer_ARD_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l2[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l2 = ["True", self.ard_1, self.ard_2, self.ard_3]
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l2 = ["False", 0, 0, 0, 0, 0, 0]
        # Display
        self.layout.ard_l2.setStyleSheet(bg_alpha)
        self.layout.ard_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g2 = 0
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.mixer_width)

    def Mixer_ARD_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r2[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r2 = ["True", self.ard_1, self.ard_2, self.ard_3]
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r2 = ["False", 0, 0, 0, 0, 0, 0]
        # Display
        self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.layout.ard_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g2 = 0
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.mixer_width)

    def Mixer_ARD_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l3[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l3 = ["True", self.ard_1, self.ard_2, self.ard_3]
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l3 = ["False", 0, 0, 0, 0, 0, 0]
        # Display
        self.layout.ard_l3.setStyleSheet(bg_alpha)
        self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g3 = 0
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.mixer_width)

    def Mixer_ARD_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r3[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r3 = ["True", self.ard_1, self.ard_2, self.ard_3]
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r3 = ["False", 0, 0, 0, 0, 0, 0]
        # Display
        self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g3 = 0
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.mixer_width)

    # HSV
    def Mixer_HSV_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l1[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_L1_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_l1 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l1 = ["False", 0, 0, 0]
        # Display
        self.layout.hsv_l1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.mixer_width)

    def Mixer_HSV_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r1[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_R1_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_r1 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r1 = ["False", 0, 0, 0]
        # Display
        self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.mixer_width)

    def Mixer_HSV_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l2[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_l2 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l2 = ["False", 0, 0, 0]
        # Display
        self.layout.hsv_l2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.mixer_width)

    def Mixer_HSV_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r2[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_r2 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r2 = ["False", 0, 0, 0]
        # Display
        self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.mixer_width)

    def Mixer_HSV_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l3[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_l3 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l3 = ["False", 0, 0, 0]
        # Display
        self.layout.hsv_l3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.mixer_width)

    def Mixer_HSV_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r3[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_r3 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r3 = ["False", 0, 0, 0]
        # Display
        self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.mixer_width)

    # HSL
    def Mixer_HSL_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l1[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l1 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l1 = ["False", 0, 0, 0]
        # Display
        self.layout.hsl_l1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.mixer_width)

    def Mixer_HSL_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r1[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r1 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r1 = ["False", 0, 0, 0]
        # Display
        self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.mixer_width)

    def Mixer_HSL_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l2[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l2 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l2 = ["False", 0, 0, 0]
        # Display
        self.layout.hsl_l2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.mixer_width)

    def Mixer_HSL_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r2[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r2 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r2 = ["False", 0, 0, 0]
        # Display
        self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.mixer_width)

    def Mixer_HSL_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l3[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l3 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l3 = ["False", 0, 0, 0]
        # Display
        self.layout.hsl_l3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.mixer_width)

    def Mixer_HSL_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r3[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r3 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r3 = ["False", 0, 0, 0]
        # Display
        self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.mixer_width)

    # HCY
    def Mixer_HCY_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hcy_l1[0] == "True":
            self.Color_APPLY("HCY", self.color_hcy_l1[1], self.color_hcy_l1[2], self.color_hcy_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HCY_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hcy_l1 = ["True", self.hcy_1, self.hcy_2, self.hcy_3]
        # Display
        rgb = self.hcy_to_rgb(self.color_hcy_l1[1], self.color_hcy_l1[2], self.color_hcy_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hcy_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HCY_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hcy_l1 = ["False", 0, 0, 0]
        # Display
        self.layout.hcy_l1.setStyleSheet(bg_alpha)
        self.layout.hcy_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hcy_g1 = 0
        self.mixer_hcy_g1.Update(self.spacer_hcy_g1, self.mixer_width)

    def Mixer_HCY_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hcy_r1[0] == "True":
            self.Color_APPLY("HCY", self.color_hcy_r1[1], self.color_hcy_r1[2], self.color_hcy_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HCY_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hcy_r1 = ["True", self.hcy_1, self.hcy_2, self.hcy_3]
        # Display
        rgb = self.hcy_to_rgb(self.color_hcy_r1[1], self.color_hcy_r1[2], self.color_hcy_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hcy_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HCY_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hcy_r1 = ["False", 0, 0, 0]
        # Display
        self.layout.hcy_r1.setStyleSheet(bg_alpha)
        self.layout.hcy_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hcy_g1 = 0
        self.mixer_hcy_g1.Update(self.spacer_hcy_g1, self.mixer_width)

    def Mixer_HCY_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hcy_l2[0] == "True":
            self.Color_APPLY("HCY", self.color_hcy_l2[1], self.color_hcy_l2[2], self.color_hcy_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HCY_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hcy_l2 = ["True", self.hcy_1, self.hcy_2, self.hcy_3]
        # Display
        rgb = self.hcy_to_rgb(self.color_hcy_l2[1], self.color_hcy_l2[2], self.color_hcy_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hcy_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HCY_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hcy_l2 = ["False", 0, 0, 0]
        # Display
        self.layout.hcy_l2.setStyleSheet(bg_alpha)
        self.layout.hcy_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hcy_g2 = 0
        self.mixer_hcy_g2.Update(self.spacer_hcy_g2, self.mixer_width)

    def Mixer_HCY_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hcy_r2[0] == "True":
            self.Color_APPLY("HCY", self.color_hcy_r2[1], self.color_hcy_r2[2], self.color_hcy_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HCY_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hcy_r2 = ["True", self.hcy_1, self.hcy_2, self.hcy_3]
        # Display
        rgb = self.hcy_to_rgb(self.color_hcy_r2[1], self.color_hcy_r2[2], self.color_hcy_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hcy_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HCY_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hcy_r2 = ["False", 0, 0, 0]
        # Display
        self.layout.hcy_r2.setStyleSheet(bg_alpha)
        self.layout.hcy_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hcy_g2 = 0
        self.mixer_hcy_g2.Update(self.spacer_hcy_g2, self.mixer_width)

    def Mixer_HCY_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hcy_l3[0] == "True":
            self.Color_APPLY("HCY", self.color_hcy_l3[1], self.color_hcy_l3[2], self.color_hcy_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HCY_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hcy_l3 = ["True", self.hcy_1, self.hcy_2, self.hcy_3]
        # Display
        rgb = self.hcy_to_rgb(self.color_hcy_l3[1], self.color_hcy_l3[2], self.color_hcy_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hcy_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HCY_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hcy_l3 = ["False", 0, 0, 0]
        # Display
        self.layout.hcy_l3.setStyleSheet(bg_alpha)
        self.layout.hcy_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hcy_g3 = 0
        self.mixer_hcy_g3.Update(self.spacer_hcy_g3, self.mixer_width)

    def Mixer_HCY_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hcy_r3[0] == "True":
            self.Color_APPLY("HCY", self.color_hcy_r3[1], self.color_hcy_r3[2], self.color_hcy_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HCY_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hcy_r3 = ["True", self.hcy_1, self.hcy_2, self.hcy_3]
        # Display
        rgb = self.hcy_to_rgb(self.color_hcy_r3[1], self.color_hcy_r3[2], self.color_hcy_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hcy_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HCY_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hcy_r3 = ["False", 0, 0, 0]
        # Display
        self.layout.hcy_r3.setStyleSheet(bg_alpha)
        self.layout.hcy_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hcy_g3 = 0
        self.mixer_hcy_g3.Update(self.spacer_hcy_g3, self.mixer_width)

    # YUV
    def Mixer_YUV_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_yuv_l1[0] == "True":
            self.Color_APPLY("YUV", self.color_yuv_l1[1], self.color_yuv_l1[2], self.color_yuv_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_YUV_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_yuv_l1 = ["True", self.yuv_1, self.yuv_2, self.yuv_3]
        # Display
        rgb = self.yuv_to_rgb(self.color_yuv_l1[1], self.color_yuv_l1[2], self.color_yuv_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.yuv_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_YUV_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_yuv_l1 = ["False", 0, 0, 0]
        # Display
        self.layout.yuv_l1.setStyleSheet(bg_alpha)
        self.layout.yuv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_yuv_g1 = 0
        self.mixer_yuv_g1.Update(self.spacer_yuv_g1, self.mixer_width)

    def Mixer_YUV_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_yuv_r1[0] == "True":
            self.Color_APPLY("YUV", self.color_yuv_r1[1], self.color_yuv_r1[2], self.color_yuv_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_YUV_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_yuv_r1 = ["True", self.yuv_1, self.yuv_2, self.yuv_3]
        # Display
        rgb = self.yuv_to_rgb(self.color_yuv_r1[1], self.color_yuv_r1[2], self.color_yuv_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.yuv_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_YUV_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_yuv_r1 = ["False", 0, 0, 0]
        # Display
        self.layout.yuv_r1.setStyleSheet(bg_alpha)
        self.layout.yuv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_yuv_g1 = 0
        self.mixer_yuv_g1.Update(self.spacer_yuv_g1, self.mixer_width)

    def Mixer_YUV_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_yuv_l2[0] == "True":
            self.Color_APPLY("YUV", self.color_yuv_l2[1], self.color_yuv_l2[2], self.color_yuv_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_YUV_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_yuv_l2 = ["True", self.yuv_1, self.yuv_2, self.yuv_3]
        # Display
        rgb = self.yuv_to_rgb(self.color_yuv_l2[1], self.color_yuv_l2[2], self.color_yuv_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.yuv_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_YUV_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_yuv_l2 = ["False", 0, 0, 0]
        # Display
        self.layout.yuv_l2.setStyleSheet(bg_alpha)
        self.layout.yuv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_yuv_g2 = 0
        self.mixer_yuv_g2.Update(self.spacer_yuv_g2, self.mixer_width)

    def Mixer_YUV_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_yuv_r2[0] == "True":
            self.Color_APPLY("YUV", self.color_yuv_r2[1], self.color_yuv_r2[2], self.color_yuv_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_YUV_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_yuv_r2 = ["True", self.yuv_1, self.yuv_2, self.yuv_3]
        # Display
        rgb = self.yuv_to_rgb(self.color_yuv_r2[1], self.color_yuv_r2[2], self.color_yuv_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.yuv_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_YUV_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_yuv_r2 = ["False", 0, 0, 0]
        # Display
        self.layout.yuv_r2.setStyleSheet(bg_alpha)
        self.layout.yuv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_yuv_g2 = 0
        self.mixer_yuv_g2.Update(self.spacer_yuv_g2, self.mixer_width)

    def Mixer_YUV_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_yuv_l3[0] == "True":
            self.Color_APPLY("YUV", self.color_yuv_l3[1], self.color_yuv_l3[2], self.color_yuv_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_YUV_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_yuv_l3 = ["True", self.yuv_1, self.yuv_2, self.yuv_3]
        # Display
        rgb = self.yuv_to_rgb(self.color_yuv_l3[1], self.color_yuv_l3[2], self.color_yuv_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.yuv_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_YUV_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_yuv_l3 = ["False", 0, 0, 0]
        # Display
        self.layout.yuv_l3.setStyleSheet(bg_alpha)
        self.layout.yuv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_yuv_g3 = 0
        self.mixer_yuv_g3.Update(self.spacer_yuv_g3, self.mixer_width)

    def Mixer_YUV_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_yuv_r3[0] == "True":
            self.Color_APPLY("YUV", self.color_yuv_r3[1], self.color_yuv_r3[2], self.color_yuv_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_YUV_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_yuv_r3 = ["True", self.yuv_1, self.yuv_2, self.yuv_3]
        # Display
        rgb = self.yuv_to_rgb(self.color_yuv_r3[1], self.color_yuv_r3[2], self.color_yuv_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.yuv_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_YUV_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_yuv_r3 = ["False", 0, 0, 0]
        # Display
        self.layout.yuv_r3.setStyleSheet(bg_alpha)
        self.layout.yuv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_yuv_g3 = 0
        self.mixer_yuv_g3.Update(self.spacer_yuv_g3, self.mixer_width)

    # RYB
    def Mixer_RYB_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_ryb_l1[0] == "True":
            self.Color_APPLY("RYB", self.color_ryb_l1[1], self.color_ryb_l1[2], self.color_ryb_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RYB_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ryb_l1 = ["True", self.ryb_1, self.ryb_2, self.ryb_3]
        # Display
        rgb = self.ryb_to_rgb(self.color_ryb_l1[1], self.color_ryb_l1[2], self.color_ryb_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ryb_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RYB_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ryb_l1 = ["False", 0, 0, 0]
        # Display
        self.layout.ryb_l1.setStyleSheet(bg_alpha)
        self.layout.ryb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ryb_g1 = 0
        self.mixer_ryb_g1.Update(self.spacer_ryb_g1, self.mixer_width)

    def Mixer_RYB_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_ryb_r1[0] == "True":
            self.Color_APPLY("RYB", self.color_ryb_r1[1], self.color_ryb_r1[2], self.color_ryb_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RYB_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ryb_r1 = ["True", self.ryb_1, self.ryb_2, self.ryb_3]
        # Display
        rgb = self.ryb_to_rgb(self.color_ryb_r1[1], self.color_ryb_r1[2], self.color_ryb_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ryb_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RYB_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ryb_r1 = ["False", 0, 0, 0]
        # Display
        self.layout.ryb_r1.setStyleSheet(bg_alpha)
        self.layout.ryb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ryb_g1 = 0
        self.mixer_ryb_g1.Update(self.spacer_ryb_g1, self.mixer_width)

    def Mixer_RYB_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_ryb_l2[0] == "True":
            self.Color_APPLY("RYB", self.color_ryb_l2[1], self.color_ryb_l2[2], self.color_ryb_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RYB_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ryb_l2 = ["True", self.ryb_1, self.ryb_2, self.ryb_3]
        # Display
        rgb = self.ryb_to_rgb(self.color_ryb_l2[1], self.color_ryb_l2[2], self.color_ryb_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ryb_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RYB_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ryb_l2 = ["False", 0, 0, 0]
        # Display
        self.layout.ryb_l2.setStyleSheet(bg_alpha)
        self.layout.ryb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ryb_g2 = 0
        self.mixer_ryb_g2.Update(self.spacer_ryb_g2, self.mixer_width)

    def Mixer_RYB_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_ryb_r2[0] == "True":
            self.Color_APPLY("RYB", self.color_ryb_r2[1], self.color_ryb_r2[2], self.color_ryb_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RYB_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ryb_r2 = ["True", self.ryb_1, self.ryb_2, self.ryb_3]
        # Display
        rgb = self.ryb_to_rgb(self.color_ryb_r2[1], self.color_ryb_r2[2], self.color_ryb_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ryb_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RYB_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ryb_r2 = ["False", 0, 0, 0]
        # Display
        self.layout.ryb_r2.setStyleSheet(bg_alpha)
        self.layout.ryb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ryb_g2 = 0
        self.mixer_ryb_g2.Update(self.spacer_ryb_g2, self.mixer_width)

    def Mixer_RYB_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_ryb_l3[0] == "True":
            self.Color_APPLY("RYB", self.color_ryb_l3[1], self.color_ryb_l3[2], self.color_ryb_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RYB_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ryb_l3 = ["True", self.ryb_1, self.ryb_2, self.ryb_3]
        # Display
        rgb = self.ryb_to_rgb(self.color_ryb_l3[1], self.color_ryb_l3[2], self.color_ryb_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ryb_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RYB_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ryb_l3 = ["False", 0, 0, 0]
        # Display
        self.layout.ryb_l3.setStyleSheet(bg_alpha)
        self.layout.ryb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ryb_g3 = 0
        self.mixer_ryb_g3.Update(self.spacer_ryb_g3, self.mixer_width)

    def Mixer_RYB_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_ryb_r3[0] == "True":
            self.Color_APPLY("RYB", self.color_ryb_r3[1], self.color_ryb_r3[2], self.color_ryb_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RYB_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ryb_r3 = ["True", self.ryb_1, self.ryb_2, self.ryb_3]
        # Display
        rgb = self.ryb_to_rgb(self.color_ryb_r3[1], self.color_ryb_r3[2], self.color_ryb_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ryb_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RYB_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ryb_r3 = ["False", 0, 0, 0]
        # Display
        self.layout.ryb_r3.setStyleSheet(bg_alpha)
        self.layout.ryb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ryb_g3 = 0
        self.mixer_ryb_g3.Update(self.spacer_ryb_g3, self.mixer_width)

    # CMYK
    def Mixer_CMYK_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l1[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l1 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
        # Display
        self.layout.cmyk_l1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.mixer_width)

    def Mixer_CMYK_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r1[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r1 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
        # Display
        self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.mixer_width)

    def Mixer_CMYK_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l2[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l2 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
        # Display
        self.layout.cmyk_l2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.mixer_width)

    def Mixer_CMYK_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r2[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r2 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
        # Display
        self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.mixer_width)

    def Mixer_CMYK_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l3[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l3 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
        # Display
        self.layout.cmyk_l3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.mixer_width)

    def Mixer_CMYK_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r3[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r3 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
        # Display
        self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.mixer_width)

    #//
    #\\ Mixer Gradient #########################################################
    def Mixer_Tint(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_tint = SIGNAL_MIXER_VALUE / (self.layout.tint.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_tts[1]) + (self.spacer_tint * (color_white[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.spacer_tint * (color_white[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.spacer_tint * (color_white[2] - self.color_tts[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
    def Mixer_Tone(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_tone = SIGNAL_MIXER_VALUE / (self.layout.tone.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_tts[1]) + (self.spacer_tone * (self.gray_tts[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.spacer_tone * (self.gray_tts[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.spacer_tone * (self.gray_tts[2] - self.color_tts[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
    def Mixer_Shade(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_shade = SIGNAL_MIXER_VALUE / (self.layout.shade.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_tts[1]) + (self.spacer_shade * (color_black[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.spacer_shade * (color_black[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.spacer_shade * (color_black[2] - self.color_tts[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)

    def Mixer_RGB_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_rgb_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l1[1] + (self.spacer_rgb_g1 * (self.color_rgb_r1[1] - self.color_rgb_l1[1])))
        rgb2 = (self.color_rgb_l1[2] + (self.spacer_rgb_g1 * (self.color_rgb_r1[2] - self.color_rgb_l1[2])))
        rgb3 = (self.color_rgb_l1[3] + (self.spacer_rgb_g1 * (self.color_rgb_r1[3] - self.color_rgb_l1[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
    def Mixer_RGB_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_rgb_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l2[1] + (self.spacer_rgb_g2 * (self.color_rgb_r2[1] - self.color_rgb_l2[1])))
        rgb2 = (self.color_rgb_l2[2] + (self.spacer_rgb_g2 * (self.color_rgb_r2[2] - self.color_rgb_l2[2])))
        rgb3 = (self.color_rgb_l2[3] + (self.spacer_rgb_g2 * (self.color_rgb_r2[3] - self.color_rgb_l2[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
    def Mixer_RGB_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_rgb_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l3[1] + (self.spacer_rgb_g3 * (self.color_rgb_r3[1] - self.color_rgb_l3[1])))
        rgb2 = (self.color_rgb_l3[2] + (self.spacer_rgb_g3 * (self.color_rgb_r3[2] - self.color_rgb_l3[2])))
        rgb3 = (self.color_rgb_l3[3] + (self.spacer_rgb_g3 * (self.color_rgb_r3[3] - self.color_rgb_l3[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)

    def Mixer_ARD_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ard_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_ard_l1[1] <= self.color_ard_r1[1]:
            # Conditions
            cond1 = self.color_ard_r1[1] - self.color_ard_l1[1]
            cond2 = (self.color_ard_l1[1] + 1) - self.color_ard_r1[1]
            if cond1 <= cond2:
                ang = self.color_ard_l1[1] + (self.spacer_ard_g1 * cond1)
            else:
                ang = self.color_ard_l1[1] - (self.spacer_ard_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l1[1] - self.color_ard_r1[1]
            cond2 = (self.color_ard_r1[1] + 1) - self.color_ard_l1[1]
            if cond1 <= cond2:
                ang = self.color_ard_l1[1] - (self.spacer_ard_g1 * cond1)
            else:
                ang = self.color_ard_l1[1] + (self.spacer_ard_g1 * cond2)
        # Correct Excess
        if ang < 0:
            ang = ang + 1
        if ang > 1:
            ang = ang - 1
        ard1 = ang
        ard2 = (self.color_ard_l1[2] + (self.spacer_ard_g1 * (self.color_ard_r1[2] - self.color_ard_l1[2])))
        ard3 = (self.color_ard_l1[3] + (self.spacer_ard_g1 * (self.color_ard_r1[3] - self.color_ard_l1[3])))
        # Send Values
        self.Color_APPLY("ARD", ard1, ard2, ard3, 0)
    def Mixer_ARD_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ard_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_ard_l2[1] <= self.color_ard_r2[1]:
            # Conditions
            cond1 = self.color_ard_r2[1] - self.color_ard_l2[1]
            cond2 = (self.color_ard_l2[1] + 1) - self.color_ard_r2[1]
            if cond1 <= cond2:
                ang = self.color_ard_l2[1] + (self.spacer_ard_g2 * cond1)
            else:
                ang = self.color_ard_l2[1] - (self.spacer_ard_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l2[1] - self.color_ard_r2[1]
            cond2 = (self.color_ard_r2[1] + 1) - self.color_ard_l2[1]
            if cond1 <= cond2:
                ang = self.color_ard_l2[1] - (self.spacer_ard_g2 * cond1)
            else:
                ang = self.color_ard_l2[1] + (self.spacer_ard_g2 * cond2)
        # Correct Excess
        if ang < 0:
            ang = ang + 1
        if ang > 1:
            ang = ang - 1
        ard1 = ang
        ard2 = (self.color_ard_l2[2] + (self.spacer_ard_g2 * (self.color_ard_r2[2] - self.color_ard_l2[2])))
        ard3 = (self.color_ard_l2[3] + (self.spacer_ard_g2 * (self.color_ard_r2[3] - self.color_ard_l2[3])))
        # Send Values
        self.Color_APPLY("ARD", ard1, ard2, ard3, 0)
    def Mixer_ARD_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ard_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_ard_l3[1] <= self.color_ard_r3[1]:
            # Conditions
            cond1 = self.color_ard_r3[1] - self.color_ard_l3[1]
            cond2 = (self.color_ard_l3[1] + 1) - self.color_ard_r3[1]
            if cond1 <= cond2:
                ang = self.color_ard_l3[1] + (self.spacer_ard_g3 * cond1)
            else:
                ang = self.color_ard_l3[1] - (self.spacer_ard_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_ard_l3[1] - self.color_ard_r3[1]
            cond2 = (self.color_ard_r3[1] + 1) - self.color_ard_l3[1]
            if cond1 <= cond2:
                ang = self.color_ard_l3[1] - (self.spacer_ard_g3 * cond1)
            else:
                ang = self.color_ard_l3[1] + (self.spacer_ard_g3 * cond2)
        # Correct Excess
        if ang < 0:
            ang = ang + 1
        if ang > 1:
            ang = ang - 1
        ard1 = ang
        ard2 = (self.color_ard_l3[2] + (self.spacer_ard_g3 * (self.color_ard_r3[2] - self.color_ard_l3[2])))
        ard3 = (self.color_ard_l3[3] + (self.spacer_ard_g3 * (self.color_ard_r3[3] - self.color_ard_l3[3])))
        # Send Values
        self.Color_APPLY("ARD", ard1, ard2, ard3, 0)

    def Mixer_HSV_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hsv_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hsv_l1[1] <= self.color_hsv_r1[1]:
            # Conditions
            cond1 = self.color_hsv_r1[1] - self.color_hsv_l1[1]
            cond2 = (self.color_hsv_l1[1] + 1) - self.color_hsv_r1[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l1[1] + (self.spacer_hsv_g1 * cond1)
            else:
                hue = self.color_hsv_l1[1] - (self.spacer_hsv_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsv_l1[1] - self.color_hsv_r1[1]
            cond2 = (self.color_hsv_r1[1] + 1) - self.color_hsv_l1[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l1[1] - (self.spacer_hsv_g1 * cond1)
            else:
                hue = self.color_hsv_l1[1] + (self.spacer_hsv_g1 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l1[2] + (self.spacer_hsv_g1 * (self.color_hsv_r1[2] - self.color_hsv_l1[2])))
        hsv3 = (self.color_hsv_l1[3] + (self.spacer_hsv_g1 * (self.color_hsv_r1[3] - self.color_hsv_l1[3])))
        # Send Values
        self.Color_APPLY("HSV", hsv1, hsv2, hsv3, 0)
    def Mixer_HSV_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hsv_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hsv_l2[1] <= self.color_hsv_r2[1]:
            # Conditions
            cond1 = self.color_hsv_r2[1] - self.color_hsv_l2[1]
            cond2 = (self.color_hsv_l2[1] + 1) - self.color_hsv_r2[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l2[1] + (self.spacer_hsv_g2 * cond1)
            else:
                hue = self.color_hsv_l2[1] - (self.spacer_hsv_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsv_l2[1] - self.color_hsv_r2[1]
            cond2 = (self.color_hsv_r2[1] + 1) - self.color_hsv_l2[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l2[1] - (self.spacer_hsv_g2 * cond1)
            else:
                hue = self.color_hsv_l2[1] + (self.spacer_hsv_g2 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l2[2] + (self.spacer_hsv_g2 * (self.color_hsv_r2[2] - self.color_hsv_l2[2])))
        hsv3 = (self.color_hsv_l2[3] + (self.spacer_hsv_g2 * (self.color_hsv_r2[3] - self.color_hsv_l2[3])))
        # Send Values
        self.Color_APPLY("HSV", hsv1, hsv2, hsv3, 0)
    def Mixer_HSV_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hsv_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hsv_l3[1] <= self.color_hsv_r3[1]:
            # Conditions
            cond1 = self.color_hsv_r3[1] - self.color_hsv_l3[1]
            cond2 = (self.color_hsv_l3[1] + 1) - self.color_hsv_r3[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l3[1] + (self.spacer_hsv_g3 * cond1)
            else:
                hue = self.color_hsv_l3[1] - (self.spacer_hsv_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsv_l3[1] - self.color_hsv_r3[1]
            cond2 = (self.color_hsv_r3[1] + 1) - self.color_hsv_l3[1]
            if cond1 <= cond2:
                hue = self.color_hsv_l3[1] - (self.spacer_hsv_g3 * cond1)
            else:
                hue = self.color_hsv_l3[1] + (self.spacer_hsv_g3 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsv1 = hue
        hsv2 = (self.color_hsv_l3[2] + (self.spacer_hsv_g3 * (self.color_hsv_r3[2] - self.color_hsv_l3[2])))
        hsv3 = (self.color_hsv_l3[3] + (self.spacer_hsv_g3 * (self.color_hsv_r3[3] - self.color_hsv_l3[3])))
        # Send Values
        self.Color_APPLY("HSV", hsv1, hsv2, hsv3, 0)

    def Mixer_HSL_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hsl_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hsl_l1[1] <= self.color_hsl_r1[1]:
            # Conditions
            cond1 = self.color_hsl_r1[1] - self.color_hsl_l1[1]
            cond2 = (self.color_hsl_l1[1] + 1) - self.color_hsl_r1[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l1[1] + (self.spacer_hsl_g1 * cond1)
            else:
                hue = self.color_hsl_l1[1] - (self.spacer_hsl_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsl_l1[1] - self.color_hsl_r1[1]
            cond2 = (self.color_hsl_r1[1] + 1) - self.color_hsl_l1[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l1[1] - (self.spacer_hsl_g1 * cond1)
            else:
                hue = self.color_hsl_l1[1] + (self.spacer_hsl_g1 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l1[2] + (self.spacer_hsl_g1 * (self.color_hsl_r1[2] - self.color_hsl_l1[2])))
        hsl3 = (self.color_hsl_l1[3] + (self.spacer_hsl_g1 * (self.color_hsl_r1[3] - self.color_hsl_l1[3])))
        # Send Values
        self.Color_APPLY("HSL", hsl1, hsl2, hsl3, 0)
    def Mixer_HSL_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hsl_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hsl_l2[1] <= self.color_hsl_r2[1]:
            # Conditions
            cond1 = self.color_hsl_r2[1] - self.color_hsl_l2[1]
            cond2 = (self.color_hsl_l2[1] + 1) - self.color_hsl_r2[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l2[1] + (self.spacer_hsl_g2 * cond1)
            else:
                hue = self.color_hsl_l2[1] - (self.spacer_hsl_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsl_l2[1] - self.color_hsl_r2[1]
            cond2 = (self.color_hsl_r2[1] + 1) - self.color_hsl_l2[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l2[1] - (self.spacer_hsl_g2 * cond1)
            else:
                hue = self.color_hsl_l2[1] + (self.spacer_hsl_g2 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l2[2] + (self.spacer_hsl_g2 * (self.color_hsl_r2[2] - self.color_hsl_l2[2])))
        hsl3 = (self.color_hsl_l2[3] + (self.spacer_hsl_g2 * (self.color_hsl_r2[3] - self.color_hsl_l2[3])))
        # Send Values
        self.Color_APPLY("HSL", hsl1, hsl2, hsl3, 0)
    def Mixer_HSL_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hsl_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hsl_l3[1] <= self.color_hsl_r3[1]:
            # Conditions
            cond1 = self.color_hsl_r3[1] - self.color_hsl_l3[1]
            cond2 = (self.color_hsl_l3[1] + 1) - self.color_hsl_r3[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l3[1] + (self.spacer_hsl_g3 * cond1)
            else:
                hue = self.color_hsl_l3[1] - (self.spacer_hsl_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_hsl_l3[1] - self.color_hsl_r3[1]
            cond2 = (self.color_hsl_r3[1] + 1) - self.color_hsl_l3[1]
            if cond1 <= cond2:
                hue = self.color_hsl_l3[1] - (self.spacer_hsl_g3 * cond1)
            else:
                hue = self.color_hsl_l3[1] + (self.spacer_hsl_g3 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hsl1 = hue
        hsl2 = (self.color_hsl_l3[2] + (self.spacer_hsl_g3 * (self.color_hsl_r3[2] - self.color_hsl_l3[2])))
        hsl3 = (self.color_hsl_l3[3] + (self.spacer_hsl_g3 * (self.color_hsl_r3[3] - self.color_hsl_l3[3])))
        # Send Values
        self.Color_APPLY("HSL", hsl1, hsl2, hsl3, 0)

    def Mixer_HCY_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hcy_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hcy_l1[1] <= self.color_hcy_r1[1]:
            # Conditions
            cond1 = self.color_hcy_r1[1] - self.color_hcy_l1[1]
            cond2 = (self.color_hcy_l1[1] + 1) - self.color_hcy_r1[1]
            if cond1 <= cond2:
                hue = self.color_hcy_l1[1] + (self.spacer_hcy_g1 * cond1)
            else:
                hue = self.color_hcy_l1[1] - (self.spacer_hcy_g1 * cond2)
        else:
            # Conditions
            cond1 = self.color_hcy_l1[1] - self.color_hcy_r1[1]
            cond2 = (self.color_hcy_r1[1] + 1) - self.color_hcy_l1[1]
            if cond1 <= cond2:
                hue = self.color_hcy_l1[1] - (self.spacer_hcy_g1 * cond1)
            else:
                hue = self.color_hcy_l1[1] + (self.spacer_hcy_g1 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hcy1 = hue
        hcy2 = (self.color_hcy_l1[2] + (self.spacer_hcy_g1 * (self.color_hcy_r1[2] - self.color_hcy_l1[2])))
        hcy3 = (self.color_hcy_l1[3] + (self.spacer_hcy_g1 * (self.color_hcy_r1[3] - self.color_hcy_l1[3])))
        # Send Values
        self.Color_APPLY("HCY", hcy1, hcy2, hcy3, 0)
    def Mixer_HCY_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hcy_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hcy_l2[1] <= self.color_hcy_r2[1]:
            # Conditions
            cond1 = self.color_hcy_r2[1] - self.color_hcy_l2[1]
            cond2 = (self.color_hcy_l2[1] + 1) - self.color_hcy_r2[1]
            if cond1 <= cond2:
                hue = self.color_hcy_l2[1] + (self.spacer_hcy_g2 * cond1)
            else:
                hue = self.color_hcy_l2[1] - (self.spacer_hcy_g2 * cond2)
        else:
            # Conditions
            cond1 = self.color_hcy_l2[1] - self.color_hcy_r2[1]
            cond2 = (self.color_hcy_r2[1] + 1) - self.color_hcy_l2[1]
            if cond1 <= cond2:
                hue = self.color_hcy_l2[1] - (self.spacer_hcy_g2 * cond1)
            else:
                hue = self.color_hcy_l2[1] + (self.spacer_hcy_g2 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hcy1 = hue
        hcy2 = (self.color_hcy_l2[2] + (self.spacer_hcy_g2 * (self.color_hcy_r2[2] - self.color_hcy_l2[2])))
        hcy3 = (self.color_hcy_l2[3] + (self.spacer_hcy_g2 * (self.color_hcy_r2[3] - self.color_hcy_l2[3])))
        # Send Values
        self.Color_APPLY("HCY", hcy1, hcy2, hcy3, 0)
    def Mixer_HCY_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_hcy_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        if self.color_hcy_l3[1] <= self.color_hcy_r3[1]:
            # Conditions
            cond1 = self.color_hcy_r3[1] - self.color_hcy_l3[1]
            cond2 = (self.color_hcy_l3[1] + 1) - self.color_hcy_r3[1]
            if cond1 <= cond2:
                hue = self.color_hcy_l3[1] + (self.spacer_hcy_g3 * cond1)
            else:
                hue = self.color_hcy_l3[1] - (self.spacer_hcy_g3 * cond2)
        else:
            # Conditions
            cond1 = self.color_hcy_l3[1] - self.color_hcy_r3[1]
            cond2 = (self.color_hcy_r3[1] + 1) - self.color_hcy_l3[1]
            if cond1 <= cond2:
                hue = self.color_hcy_l3[1] - (self.spacer_hcy_g3 * cond1)
            else:
                hue = self.color_hcy_l3[1] + (self.spacer_hcy_g3 * cond2)
        # Correct Excess
        if hue < 0:
            hue = hue + 1
        if hue > 1:
            hue = hue - 1
        hcy1 = hue
        hcy2 = (self.color_hcy_l3[2] + (self.spacer_hcy_g3 * (self.color_hcy_r3[2] - self.color_hcy_l3[2])))
        hcy3 = (self.color_hcy_l3[3] + (self.spacer_hcy_g3 * (self.color_hcy_r3[3] - self.color_hcy_l3[3])))
        # Send Values
        self.Color_APPLY("HCY", hcy1, hcy2, hcy3, 0)

    def Mixer_YUV_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_yuv_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        yuv1 = (self.color_yuv_l1[1] + (self.spacer_yuv_g1 * (self.color_yuv_r1[1] - self.color_yuv_l1[1])))
        yuv2 = (self.color_yuv_l1[2] + (self.spacer_yuv_g1 * (self.color_yuv_r1[2] - self.color_yuv_l1[2])))
        yuv3 = (self.color_yuv_l1[3] + (self.spacer_yuv_g1 * (self.color_yuv_r1[3] - self.color_yuv_l1[3])))
        # Send Values
        rgb = self.yuv_to_rgb(yuv1, yuv2, yuv3)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("YUV", yuv1, yuv2, yuv3, 0)
    def Mixer_YUV_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_yuv_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        yuv1 = (self.color_yuv_l2[1] + (self.spacer_yuv_g2 * (self.color_yuv_r2[1] - self.color_yuv_l2[1])))
        yuv2 = (self.color_yuv_l2[2] + (self.spacer_yuv_g2 * (self.color_yuv_r2[2] - self.color_yuv_l2[2])))
        yuv3 = (self.color_yuv_l2[3] + (self.spacer_yuv_g2 * (self.color_yuv_r2[3] - self.color_yuv_l2[3])))
        # Send Values
        rgb = self.yuv_to_rgb(yuv1, yuv2, yuv3)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("YUV", yuv1, yuv2, yuv3, 0)
    def Mixer_YUV_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_yuv_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        yuv1 = (self.color_yuv_l3[1] + (self.spacer_yuv_g3 * (self.color_yuv_r3[1] - self.color_yuv_l3[1])))
        yuv2 = (self.color_yuv_l3[2] + (self.spacer_yuv_g3 * (self.color_yuv_r3[2] - self.color_yuv_l3[2])))
        yuv3 = (self.color_yuv_l3[3] + (self.spacer_yuv_g3 * (self.color_yuv_r3[3] - self.color_yuv_l3[3])))
        # Send Values
        rgb = self.yuv_to_rgb(yuv1, yuv2, yuv3)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("YUV", yuv1, yuv2, yuv3, 0)

    def Mixer_RYB_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ryb_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        ryb1 = (self.color_ryb_l1[1] + (self.spacer_ryb_g1 * (self.color_ryb_r1[1] - self.color_ryb_l1[1])))
        ryb2 = (self.color_ryb_l1[2] + (self.spacer_ryb_g1 * (self.color_ryb_r1[2] - self.color_ryb_l1[2])))
        ryb3 = (self.color_ryb_l1[3] + (self.spacer_ryb_g1 * (self.color_ryb_r1[3] - self.color_ryb_l1[3])))
        # Send Values
        rgb = self.ryb_to_rgb(ryb1, ryb2, ryb3)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("RYB", ryb1, ryb2, ryb3, 0)
    def Mixer_RYB_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ryb_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        ryb1 = (self.color_ryb_l2[1] + (self.spacer_ryb_g2 * (self.color_ryb_r2[1] - self.color_ryb_l2[1])))
        ryb2 = (self.color_ryb_l2[2] + (self.spacer_ryb_g2 * (self.color_ryb_r2[2] - self.color_ryb_l2[2])))
        ryb3 = (self.color_ryb_l2[3] + (self.spacer_ryb_g2 * (self.color_ryb_r2[3] - self.color_ryb_l2[3])))
        # Send Values
        rgb = self.ryb_to_rgb(ryb1, ryb2, ryb3)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("RYB", ryb1, ryb2, ryb3, 0)
    def Mixer_RYB_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ryb_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        ryb1 = (self.color_ryb_l3[1] + (self.spacer_ryb_g3 * (self.color_ryb_r3[1] - self.color_ryb_l3[1])))
        ryb2 = (self.color_ryb_l3[2] + (self.spacer_ryb_g3 * (self.color_ryb_r3[2] - self.color_ryb_l3[2])))
        ryb3 = (self.color_ryb_l3[3] + (self.spacer_ryb_g3 * (self.color_ryb_r3[3] - self.color_ryb_l3[3])))
        # Send Values
        rgb = self.ryb_to_rgb(ryb1, ryb2, ryb3)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("RYB", ryb1, ryb2, ryb3, 0)

    def Mixer_CMYK_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_cmyk_g1 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l1[1] + (self.spacer_cmyk_g1 * (self.color_cmyk_r1[1] - self.color_cmyk_l1[1])))
        cmyk2 = (self.color_cmyk_l1[2] + (self.spacer_cmyk_g1 * (self.color_cmyk_r1[2] - self.color_cmyk_l1[2])))
        cmyk3 = (self.color_cmyk_l1[3] + (self.spacer_cmyk_g1 * (self.color_cmyk_r1[3] - self.color_cmyk_l1[3])))
        cmyk4 = (self.color_cmyk_l1[4] + (self.spacer_cmyk_g1 * (self.color_cmyk_r1[4] - self.color_cmyk_l1[4])))
        # Send Values
        rgb = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_CMYK_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_cmyk_g2 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l2[1] + (self.spacer_cmyk_g2 * (self.color_cmyk_r2[1] - self.color_cmyk_l2[1])))
        cmyk2 = (self.color_cmyk_l2[2] + (self.spacer_cmyk_g2 * (self.color_cmyk_r2[2] - self.color_cmyk_l2[2])))
        cmyk3 = (self.color_cmyk_l2[3] + (self.spacer_cmyk_g2 * (self.color_cmyk_r2[3] - self.color_cmyk_l2[3])))
        cmyk4 = (self.color_cmyk_l2[4] + (self.spacer_cmyk_g2 * (self.color_cmyk_r2[4] - self.color_cmyk_l2[4])))
        # Send Values
        rgb = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
    def Mixer_CMYK_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_cmyk_g3 = SIGNAL_MIXER_VALUE / (self.mixer_width)
        # Percentual Value added to Left Color Percentil
        cmyk1 = (self.color_cmyk_l3[1] + (self.spacer_cmyk_g3 * (self.color_cmyk_r3[1] - self.color_cmyk_l3[1])))
        cmyk2 = (self.color_cmyk_l3[2] + (self.spacer_cmyk_g3 * (self.color_cmyk_r3[2] - self.color_cmyk_l3[2])))
        cmyk3 = (self.color_cmyk_l3[3] + (self.spacer_cmyk_g3 * (self.color_cmyk_r3[3] - self.color_cmyk_l3[3])))
        cmyk4 = (self.color_cmyk_l3[4] + (self.spacer_cmyk_g3 * (self.color_cmyk_r3[4] - self.color_cmyk_l3[4])))
        # Send Values
        rgb = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
        self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
        self.Color_APPLY("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)

    #//
    #\\ Harmony ################################################################
    def Harmony_1_Active(self, SIGNAL_ACTIVE):
        self.harmony_menu = self.layout.har.isChecked()
        if self.harmony_menu == True:
            self.harmony_active = 1
            self.harmony_1.Active(True)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_1[1], self.har_1[2], self.har_1[3])
            self.Color_APPLY("RGB", self.har_1[1], self.har_1[2], self.har_1[3], 0)
            self.Pigment_Display_Release(0)
        else:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
        # Update Display
        self.Ratio_Channels()
    def Harmony_2_Active(self, SIGNAL_ACTIVE):
        self.harmony_menu = self.layout.har.isChecked()
        if self.harmony_menu == True:
            self.harmony_active = 2
            self.harmony_1.Active(False)
            self.harmony_2.Active(True)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_2[1], self.har_2[2], self.har_2[3])
            self.Color_APPLY("RGB", self.har_2[1], self.har_2[2], self.har_2[3], 0)
            self.Pigment_Display_Release(0)
        else:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
        # Update Display
        self.Ratio_Channels()
    def Harmony_3_Active(self, SIGNAL_ACTIVE):
        self.harmony_menu = self.layout.har.isChecked()
        if self.harmony_menu == True:
            self.harmony_active = 3
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(True)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_3[1], self.har_3[2], self.har_3[3])
            self.Color_APPLY("RGB", self.har_3[1], self.har_3[2], self.har_3[3], 0)
            self.Pigment_Display_Release(0)
        else:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
        # Update Display
        self.Ratio_Channels()
    def Harmony_4_Active(self, SIGNAL_ACTIVE):
        self.harmony_menu = self.layout.har.isChecked()
        if self.harmony_menu == True:
            self.harmony_active = 4
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(True)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_4[1], self.har_4[2], self.har_4[3])
            self.Color_APPLY("RGB", self.har_4[1], self.har_4[2], self.har_4[3], 0)
            self.Pigment_Display_Release(0)
        else:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
        # Update Display
        self.Ratio_Channels()
    def Harmony_5_Active(self, SIGNAL_ACTIVE):
        self.harmony_menu = self.layout.har.isChecked()
        if self.harmony_menu == True:
            self.harmony_active = 5
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(True)
            self.Color_ANGLE(self.har_5[1], self.har_5[2], self.har_5[3])
            self.Color_APPLY("RGB", self.har_5[1], self.har_5[2], self.har_5[3], 0)
            self.Pigment_Display_Release(0)
        else:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
        # Update Display
        self.Ratio_Channels()

    def Pigment_HUE_Harmony_Active(self, SIGNAL_HUE_C_HARMONY_ACTIVE):
        self.harmony_active = int(SIGNAL_HUE_C_HARMONY_ACTIVE)
        if self.harmony_active == 1:
            self.harmony_1.Active(True)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_1[1], self.har_1[2], self.har_1[3])
            self.Color_APPLY("RGB", self.har_1[1], self.har_1[2], self.har_1[3], 0)
            self.Pigment_Display_Release(0)
        if self.harmony_active == 2:
            self.harmony_1.Active(False)
            self.harmony_2.Active(True)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_2[1], self.har_2[2], self.har_2[3])
            self.Color_APPLY("RGB", self.har_2[1], self.har_2[2], self.har_2[3], 0)
            self.Pigment_Display_Release(0)
        if self.harmony_active == 3:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(True)
            self.harmony_4.Active(False)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_3[1], self.har_3[2], self.har_3[3])
            self.Color_APPLY("RGB", self.har_3[1], self.har_3[2], self.har_3[3], 0)
            self.Pigment_Display_Release(0)
        if self.harmony_active == 4:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(True)
            self.harmony_5.Active(False)
            self.Color_ANGLE(self.har_4[1], self.har_4[2], self.har_4[3])
            self.Color_APPLY("RGB", self.har_4[1], self.har_4[2], self.har_4[3], 0)
            self.Pigment_Display_Release(0)
        if self.harmony_active == 5:
            self.harmony_1.Active(False)
            self.harmony_2.Active(False)
            self.harmony_3.Active(False)
            self.harmony_4.Active(False)
            self.harmony_5.Active(True)
            self.Color_ANGLE(self.har_5[1], self.har_5[2], self.har_5[3])
            self.Color_APPLY("RGB", self.har_5[1], self.har_5[2], self.har_5[3], 0)
            self.Pigment_Display_Release(0)
        # Update Display
        self.Ratio_Channels()

    #//
    #\\ DOT ####################################################################
    def DOT_1_APPLY(self, SIGNAL_CLICKS):
        if self.dot_1[0] == "True":
            self.Color_ANGLE(self.dot_1[1], self.dot_1[2], self.dot_1[3])
            self.Color_APPLY("RGB", self.dot_1[1], self.dot_1[2], self.dot_1[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_1_SAVE(self, SIGNAL_CLICKS):
        self.dot_1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
        self.layout.dot_1.setStyleSheet(color)
        self.layout.panel_dot_mix.update()
    def DOT_1_CLEAN(self, SIGNAL_CLICKS):
        self.dot_1 = ["False", 0, 0, 0]
        self.layout.dot_1.setStyleSheet(bg_alpha)
        self.layout.panel_dot_mix.update()

    def DOT_2_APPLY(self, SIGNAL_CLICKS):
        if self.dot_2[0] == "True":
            self.Color_ANGLE(self.dot_2[1], self.dot_2[2], self.dot_2[3])
            self.Color_APPLY("RGB", self.dot_2[1], self.dot_2[2], self.dot_2[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_2_SAVE(self, SIGNAL_CLICKS):
        self.dot_2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
        self.layout.dot_2.setStyleSheet(color)
        self.layout.panel_dot_mix.update()
    def DOT_2_CLEAN(self, SIGNAL_CLICKS):
        self.dot_2 = ["False", 0, 0, 0]
        self.layout.dot_2.setStyleSheet(bg_alpha)
        self.layout.panel_dot_mix.update()

    def DOT_3_APPLY(self, SIGNAL_CLICKS):
        if self.dot_3[0] == "True":
            self.Color_ANGLE(self.dot_3[1], self.dot_3[2], self.dot_3[3])
            self.Color_APPLY("RGB", self.dot_3[1], self.dot_3[2], self.dot_3[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_3_SAVE(self, SIGNAL_CLICKS):
        self.dot_3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
        self.layout.dot_3.setStyleSheet(color)
        self.layout.panel_dot_mix.update()
    def DOT_3_CLEAN(self, SIGNAL_CLICKS):
        self.dot_3 = ["False", 0, 0, 0]
        self.layout.dot_3.setStyleSheet(bg_alpha)
        self.layout.panel_dot_mix.update()

    def DOT_4_APPLY(self, SIGNAL_CLICKS):
        if self.dot_4[0] == "True":
            self.Color_ANGLE(self.dot_4[1], self.dot_4[2], self.dot_4[3])
            self.Color_APPLY("RGB", self.dot_4[1], self.dot_4[2], self.dot_4[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_4_SAVE(self, SIGNAL_CLICKS):
        self.dot_4 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
        self.layout.dot_4.setStyleSheet(color)
        self.layout.panel_dot_mix.update()
    def DOT_4_CLEAN(self, SIGNAL_CLICKS):
        self.dot_4 = ["False", 0, 0, 0]
        self.layout.dot_4.setStyleSheet(bg_alpha)
        self.layout.panel_dot_mix.update()

    def DOT_SWAP(self):
        # transition variables to do the swap
        a1 = [self.dot_1[0], self.dot_1[1], self.dot_1[2], self.dot_1[3]]
        a2 = [self.dot_2[0], self.dot_2[1], self.dot_2[2], self.dot_2[3]]
        b1 = [self.dot_3[0], self.dot_3[1], self.dot_3[2], self.dot_3[3]]
        b2 = [self.dot_4[0], self.dot_4[1], self.dot_4[2], self.dot_4[3]]
        # swap the variables
        self.dot_1 = [b1[0], b1[1], b1[2], b1[3]]
        self.dot_2 = [b2[0], b2[1], b2[2], b2[3]]
        self.dot_3 = [a1[0], a1[1], a1[2], a1[3]]
        self.dot_4 = [a2[0], a2[1], a2[2], a2[3]]
        # Apply Colors
        if self.dot_1[0] == "True":
            color_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
            self.layout.dot_1.setStyleSheet(color_1)
        else:
            self.layout.dot_1.setStyleSheet(bg_alpha)
        if self.dot_2[0] == "True":
            color_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
            self.layout.dot_2.setStyleSheet(color_2)
        else:
            self.layout.dot_2.setStyleSheet(bg_alpha)
        if self.dot_3[0] == "True":
            color_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
            self.layout.dot_3.setStyleSheet(color_3)
        else:
            self.layout.dot_3.setStyleSheet(bg_alpha)
        if self.dot_4[0] == "True":
            color_4 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
            self.layout.dot_4.setStyleSheet(color_4)
        else:
            self.layout.dot_4.setStyleSheet(bg_alpha)
        # Update Display
        self.layout.panel_dot_mix.update()

    #//
    #\\ OBJ ####################################################################
    def BG_1_LIVE(self):
        if self.layout.b1_live.isChecked() == True:
            self.BG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.bg_1[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def BG_1_APPLY(self):
        if self.bg_1[self.obj_index][0] == "True":
            self.Color_ANGLE(self.bg_1[self.obj_index][1], self.bg_1[self.obj_index][2], self.bg_1[self.obj_index][3])
            self.Color_APPLY("RGB", self.bg_1[self.obj_index][1], self.bg_1[self.obj_index][2], self.bg_1[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def BG_1_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.bg_1[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_1[self.obj_index][1]*255, self.bg_1[self.obj_index][2]*255, self.bg_1[self.obj_index][3]*255, self.bg_1[self.obj_index][4]*255))
        self.layout.b1_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_01 = True
        self.Pigment_Display_Release(0)
    def BG_1_CLEAN(self):
        self.bg_1[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.b1_color.setStyleSheet(bg_alpha)
        self.layer_01 = True
    def BG_1_ALPHA(self, SIGNAL_VALUE):
        self.bg_1[self.obj_index][4] = SIGNAL_VALUE
        self.BG_1_Exclusion()
        self.BG_1_SAVE(self.bg_1[self.obj_index][1], self.bg_1[self.obj_index][2], self.bg_1[self.obj_index][3], self.bg_1[self.obj_index][4])
        self.layout.b1_alpha.update()
        self.layer_01 = True
        self.Pigment_Display_Release(0)
    def BG_1_Exclusion(self):
        # Auto Exclusive
        # self.layout.b1_live.setChecked(0)
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
        self.Color_ANGLE(self.bg_1[self.obj_index][1], self.bg_1[self.obj_index][2], self.bg_1[self.obj_index][3])
        self.Color_APPLY("RGB", self.bg_1[self.obj_index][1], self.bg_1[self.obj_index][2], self.bg_1[self.obj_index][3], 0)

    def BG_2_LIVE(self):
        if self.layout.b2_live.isChecked() == True:
            self.BG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.bg_2[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def BG_2_APPLY(self):
        if self.bg_2[self.obj_index][0] == "True":
            self.Color_ANGLE(self.bg_2[self.obj_index][1], self.bg_2[self.obj_index][2], self.bg_2[self.obj_index][3])
            self.Color_APPLY("RGB", self.bg_2[self.obj_index][1], self.bg_2[self.obj_index][2], self.bg_2[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def BG_2_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.bg_2[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_2[self.obj_index][1]*255, self.bg_2[self.obj_index][2]*255, self.bg_2[self.obj_index][3]*255, self.bg_2[self.obj_index][4]*255))
        self.layout.b2_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_02 = True
        self.Pigment_Display_Release(0)
    def BG_2_CLEAN(self):
        self.bg_2[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.b2_color.setStyleSheet(bg_alpha)
        self.layer_02 = True
    def BG_2_ALPHA(self, SIGNAL_VALUE):
        self.bg_2[self.obj_index][4] = SIGNAL_VALUE
        self.BG_2_Exclusion()
        self.BG_2_SAVE(self.bg_2[self.obj_index][1], self.bg_2[self.obj_index][2], self.bg_2[self.obj_index][3], self.bg_2[self.obj_index][4])
        self.layout.b2_alpha.update()
        self.layer_02 = True
        self.Pigment_Display_Release(0)
    def BG_2_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        # self.layout.b2_live.setChecked(0)
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
        self.Color_ANGLE(self.bg_2[self.obj_index][1], self.bg_2[self.obj_index][2], self.bg_2[self.obj_index][3])
        self.Color_APPLY("RGB", self.bg_2[self.obj_index][1], self.bg_2[self.obj_index][2], self.bg_2[self.obj_index][3], 0)

    def BG_3_LIVE(self):
        if self.layout.b3_live.isChecked() == True:
            self.BG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.bg_3[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def BG_3_APPLY(self):
        if self.bg_3[self.obj_index][0] == "True":
            self.Color_ANGLE(self.bg_3[self.obj_index][1], self.bg_3[self.obj_index][2], self.bg_3[self.obj_index][3])
            self.Color_APPLY("RGB", self.bg_3[self.obj_index][1], self.bg_3[self.obj_index][2], self.bg_3[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def BG_3_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.bg_3[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_3[self.obj_index][1]*255, self.bg_3[self.obj_index][2]*255, self.bg_3[self.obj_index][3]*255, self.bg_3[self.obj_index][4]*255))
        self.layout.b3_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_03 = True
        self.Pigment_Display_Release(0)
    def BG_3_CLEAN(self):
        self.bg_3[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.b3_color.setStyleSheet(bg_alpha)
        self.layer_03 = True
    def BG_3_ALPHA(self, SIGNAL_VALUE):
        self.bg_3[self.obj_index][4] = SIGNAL_VALUE
        self.BG_3_Exclusion()
        self.BG_3_SAVE(self.bg_3[self.obj_index][1], self.bg_3[self.obj_index][2], self.bg_3[self.obj_index][3], self.bg_3[self.obj_index][4])
        self.layout.b3_alpha.update()
        self.layer_03 = True
        self.Pigment_Display_Release(0)
    def BG_3_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        # self.layout.b3_live.setChecked(0)
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
        self.Color_ANGLE(self.bg_3[self.obj_index][1], self.bg_3[self.obj_index][2], self.bg_3[self.obj_index][3])
        self.Color_APPLY("RGB", self.bg_3[self.obj_index][1], self.bg_3[self.obj_index][2], self.bg_3[self.obj_index][3], 0)

    def DIF_1_LIVE(self):
        if self.layout.d1_live.isChecked() == True:
            self.DIF_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_1[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def DIF_1_APPLY(self):
        if self.dif_1[self.obj_index][0] == "True":
            self.Color_ANGLE(self.dif_1[self.obj_index][1], self.dif_1[self.obj_index][2], self.dif_1[self.obj_index][3])
            self.Color_APPLY("RGB", self.dif_1[self.obj_index][1], self.dif_1[self.obj_index][2], self.dif_1[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def DIF_1_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.dif_1[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_1[self.obj_index][1]*255, self.dif_1[self.obj_index][2]*255, self.dif_1[self.obj_index][3]*255, self.dif_1[self.obj_index][4]*255))
        self.layout.d1_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_04 = True
        self.Pigment_Display_Release(0)
    def DIF_1_CLEAN(self):
        self.dif_1[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.d1_color.setStyleSheet(bg_alpha)
        self.layer_04 = True
    def DIF_1_ALPHA(self, SIGNAL_VALUE):
        self.dif_1[self.obj_index][4] = SIGNAL_VALUE
        self.DIF_1_Exclusion()
        self.DIF_1_SAVE(self.dif_1[self.obj_index][1], self.dif_1[self.obj_index][2], self.dif_1[self.obj_index][3], self.dif_1[self.obj_index][4])
        self.layout.d1_alpha.update()
        self.layer_04 = True
        self.Pigment_Display_Release(0)
    def DIF_1_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        # self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.dif_1[self.obj_index][1], self.dif_1[self.obj_index][2], self.dif_1[self.obj_index][3])
        self.Color_APPLY("RGB", self.dif_1[self.obj_index][1], self.dif_1[self.obj_index][2], self.dif_1[self.obj_index][3], 0)

    def DIF_2_LIVE(self):
        if self.layout.d2_live.isChecked() == True:
            self.DIF_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_1[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def DIF_2_APPLY(self):
        if self.dif_2[self.obj_index][0] == "True":
            self.Color_ANGLE(self.dif_2[self.obj_index][1], self.dif_2[self.obj_index][2], self.dif_2[self.obj_index][3])
            self.Color_APPLY("RGB", self.dif_2[self.obj_index][1], self.dif_2[self.obj_index][2], self.dif_2[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def DIF_2_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.dif_2[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_2[self.obj_index][1]*255, self.dif_2[self.obj_index][2]*255, self.dif_2[self.obj_index][3]*255, self.dif_2[self.obj_index][4]*255))
        self.layout.d2_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_05 = True
        self.Pigment_Display_Release(0)
    def DIF_2_CLEAN(self):
        self.dif_2[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.d2_color.setStyleSheet(bg_alpha)
        self.layer_05 = True
    def DIF_2_ALPHA(self, SIGNAL_VALUE):
        self.dif_2[self.obj_index][4] = SIGNAL_VALUE
        self.DIF_2_Exclusion()
        self.DIF_2_SAVE(self.dif_2[self.obj_index][1], self.dif_2[self.obj_index][2], self.dif_2[self.obj_index][3], self.dif_2[self.obj_index][4])
        self.layout.d2_alpha.update()
        self.layer_05 = True
        self.Pigment_Display_Release(0)
    def DIF_2_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        # self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.dif_2[self.obj_index][1], self.dif_2[self.obj_index][2], self.dif_2[self.obj_index][3])
        self.Color_APPLY("RGB", self.dif_2[self.obj_index][1], self.dif_2[self.obj_index][2], self.dif_2[self.obj_index][3], 0)

    def DIF_3_LIVE(self):
        if self.layout.d3_live.isChecked() == True:
            self.DIF_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_3[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def DIF_3_APPLY(self):
        if self.dif_3[self.obj_index][0] == "True":
            self.Color_ANGLE(self.dif_3[self.obj_index][1], self.dif_3[self.obj_index][2], self.dif_3[self.obj_index][3])
            self.Color_APPLY("RGB", self.dif_3[self.obj_index][1], self.dif_3[self.obj_index][2], self.dif_3[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def DIF_3_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.dif_3[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_3[self.obj_index][1]*255, self.dif_3[self.obj_index][2]*255, self.dif_3[self.obj_index][3]*255, self.dif_3[self.obj_index][4]*255))
        self.layout.d3_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_06 = True
        self.Pigment_Display_Release(0)
    def DIF_3_CLEAN(self):
        self.dif_3[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.d3_color.setStyleSheet(bg_alpha)
        self.layer_06 = True
    def DIF_3_ALPHA(self, SIGNAL_VALUE):
        self.dif_3[self.obj_index][4] = SIGNAL_VALUE
        self.DIF_3_Exclusion()
        self.DIF_3_SAVE(self.dif_3[self.obj_index][1], self.dif_3[self.obj_index][2], self.dif_3[self.obj_index][3], self.dif_3[self.obj_index][4])
        self.layout.d3_alpha.update()
        self.layer_06 = True
        self.Pigment_Display_Release(0)
    def DIF_3_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        # self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.dif_3[self.obj_index][1], self.dif_3[self.obj_index][2], self.dif_3[self.obj_index][3])
        self.Color_APPLY("RGB", self.dif_3[self.obj_index][1], self.dif_3[self.obj_index][2], self.dif_3[self.obj_index][3], 0)

    def DIF_4_LIVE(self):
        if self.layout.d4_live.isChecked() == True:
            self.DIF_4_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_4[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def DIF_4_APPLY(self):
        if self.dif_4[self.obj_index][0] == "True":
            self.Color_ANGLE(self.dif_4[self.obj_index][1], self.dif_4[self.obj_index][2], self.dif_4[self.obj_index][3])
            self.Color_APPLY("RGB", self.dif_4[self.obj_index][1], self.dif_4[self.obj_index][2], self.dif_4[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def DIF_4_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.dif_4[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_4[self.obj_index][1]*255, self.dif_4[self.obj_index][2]*255, self.dif_4[self.obj_index][3]*255, self.dif_4[self.obj_index][4]*255))
        self.layout.d4_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_07 = True
        self.Pigment_Display_Release(0)
    def DIF_4_CLEAN(self):
        self.dif_4[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.d4_color.setStyleSheet(bg_alpha)
        self.layer_07 = True
    def DIF_4_ALPHA(self, SIGNAL_VALUE):
        self.dif_4[self.obj_index][4] = SIGNAL_VALUE
        self.DIF_4_Exclusion()
        self.DIF_4_SAVE(self.dif_4[self.obj_index][1], self.dif_4[self.obj_index][2], self.dif_4[self.obj_index][3], self.dif_4[self.obj_index][4])
        self.layout.d4_alpha.update()
        self.layer_07 = True
        self.Pigment_Display_Release(0)
    def DIF_4_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        # self.layout.d4_live.setChecked(0)
        self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.dif_4[self.obj_index][1], self.dif_4[self.obj_index][2], self.dif_4[self.obj_index][3])
        self.Color_APPLY("RGB", self.dif_4[self.obj_index][1], self.dif_4[self.obj_index][2], self.dif_4[self.obj_index][3], 0)

    def DIF_5_LIVE(self):
        if self.layout.d5_live.isChecked() == True:
            self.DIF_5_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_5[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def DIF_5_APPLY(self):
        if self.dif_5[self.obj_index][0] == "True":
            self.Color_ANGLE(self.dif_5[self.obj_index][1], self.dif_5[self.obj_index][2], self.dif_5[self.obj_index][3])
            self.Color_APPLY("RGB", self.dif_5[self.obj_index][1], self.dif_5[self.obj_index][2], self.dif_5[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def DIF_5_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.dif_5[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_5[self.obj_index][1]*255, self.dif_5[self.obj_index][2]*255, self.dif_5[self.obj_index][3]*255, self.dif_5[self.obj_index][4]*255))
        self.layout.d5_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_08 = True
        self.Pigment_Display_Release(0)
    def DIF_5_CLEAN(self):
        self.dif_5[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.d5_color.setStyleSheet(bg_alpha)
        self.layer_08 = True
    def DIF_5_ALPHA(self, SIGNAL_VALUE):
        self.dif_5[self.obj_index][4] = SIGNAL_VALUE
        self.DIF_5_Exclusion()
        self.DIF_5_SAVE(self.dif_5[self.obj_index][1], self.dif_5[self.obj_index][2], self.dif_5[self.obj_index][3], self.dif_5[self.obj_index][4])
        self.layout.d5_alpha.update()
        self.layer_08 = True
        self.Pigment_Display_Release(0)
    def DIF_5_Exclusion(self):
        # Auto Exclusive
        self.layout.b1_live.setChecked(0)
        self.layout.b2_live.setChecked(0)
        self.layout.b3_live.setChecked(0)
        self.layout.d1_live.setChecked(0)
        self.layout.d2_live.setChecked(0)
        self.layout.d3_live.setChecked(0)
        self.layout.d4_live.setChecked(0)
        # self.layout.d5_live.setChecked(0)
        self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.dif_5[self.obj_index][1], self.dif_5[self.obj_index][2], self.dif_5[self.obj_index][3])
        self.Color_APPLY("RGB", self.dif_5[self.obj_index][1], self.dif_5[self.obj_index][2], self.dif_5[self.obj_index][3], 0)

    def DIF_6_LIVE(self):
        if self.layout.d6_live.isChecked() == True:
            self.DIF_6_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.dif_6[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def DIF_6_APPLY(self):
        if self.dif_6[self.obj_index][0] == "True":
            self.Color_ANGLE(self.dif_6[self.obj_index][1], self.dif_6[self.obj_index][2], self.dif_6[self.obj_index][3])
            self.Color_APPLY("RGB", self.dif_6[self.obj_index][1], self.dif_6[self.obj_index][2], self.dif_6[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def DIF_6_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.dif_6[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_6[self.obj_index][1]*255, self.dif_6[self.obj_index][2]*255, self.dif_6[self.obj_index][3]*255, self.dif_6[self.obj_index][4]*255))
        self.layout.d6_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_09 = True
        self.Pigment_Display_Release(0)
    def DIF_6_CLEAN(self):
        self.dif_6[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.d6_color.setStyleSheet(bg_alpha)
        self.layer_09 = True
    def DIF_6_ALPHA(self, SIGNAL_VALUE):
        self.dif_6[self.obj_index][4] = SIGNAL_VALUE
        self.DIF_6_Exclusion()
        self.DIF_6_SAVE(self.dif_6[self.obj_index][1], self.dif_6[self.obj_index][2], self.dif_6[self.obj_index][3], self.dif_6[self.obj_index][4])
        self.layout.d6_alpha.update()
        self.layer_09 = True
        self.Pigment_Display_Release(0)
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
        # self.layout.d6_live.setChecked(0)
        self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.dif_6[self.obj_index][1], self.dif_6[self.obj_index][2], self.dif_6[self.obj_index][3])
        self.Color_APPLY("RGB", self.dif_6[self.obj_index][1], self.dif_6[self.obj_index][2], self.dif_6[self.obj_index][3], 0)

    def FG_1_LIVE(self):
        if self.layout.f1_live.isChecked() == True:
            self.FG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.fg_1[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def FG_1_APPLY(self):
        if self.fg_1[self.obj_index][0] == "True":
            self.Color_ANGLE(self.fg_1[self.obj_index][1], self.fg_1[self.obj_index][2], self.fg_1[self.obj_index][3])
            self.Color_APPLY("RGB", self.fg_1[self.obj_index][1], self.fg_1[self.obj_index][2], self.fg_1[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def FG_1_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.fg_1[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_1[self.obj_index][1]*255, self.fg_1[self.obj_index][2]*255, self.fg_1[self.obj_index][3]*255, self.fg_1[self.obj_index][4]*255))
        self.layout.f1_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_10 = True
        self.Pigment_Display_Release(0)
    def FG_1_CLEAN(self):
        self.fg_1[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.f1_color.setStyleSheet(bg_alpha)
        self.layer_10 = True
    def FG_1_ALPHA(self, SIGNAL_VALUE):
        self.fg_1[self.obj_index][4] = SIGNAL_VALUE
        self.FG_1_Exclusion()
        self.FG_1_SAVE(self.fg_1[self.obj_index][1], self.fg_1[self.obj_index][2], self.fg_1[self.obj_index][3], self.fg_1[self.obj_index][4])
        self.layout.f1_alpha.update()
        self.layer_10 = True
        self.Pigment_Display_Release(0)
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
        # self.layout.f1_live.setChecked(0)
        self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.fg_1[self.obj_index][1], self.fg_1[self.obj_index][2], self.fg_1[self.obj_index][3])
        self.Color_APPLY("RGB", self.fg_1[self.obj_index][1], self.fg_1[self.obj_index][2], self.fg_1[self.obj_index][3], 0)

    def FG_2_LIVE(self):
        if self.layout.f2_live.isChecked() == True:
            self.FG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.fg_2[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def FG_2_APPLY(self):
        if self.fg_2[self.obj_index][0] == "True":
            self.Color_ANGLE(self.fg_2[self.obj_index][1], self.fg_2[self.obj_index][2], self.fg_2[self.obj_index][3])
            self.Color_APPLY("RGB", self.fg_2[self.obj_index][1], self.fg_2[self.obj_index][2], self.fg_2[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def FG_2_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.fg_2[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_2[self.obj_index][1]*255, self.fg_2[self.obj_index][2]*255, self.fg_2[self.obj_index][3]*255, self.fg_2[self.obj_index][4]*255))
        self.layout.f2_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_11 = True
        self.Pigment_Display_Release(0)
    def FG_2_CLEAN(self):
        self.fg_2[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.f2_color.setStyleSheet(bg_alpha)
        self.layer_11 = True
    def FG_2_ALPHA(self, SIGNAL_VALUE):
        self.fg_2[self.obj_index][4] = SIGNAL_VALUE
        self.FG_2_Exclusion()
        self.FG_2_SAVE(self.fg_2[self.obj_index][1], self.fg_2[self.obj_index][2], self.fg_2[self.obj_index][3], self.fg_2[self.obj_index][4])
        self.layout.f2_alpha.update()
        self.layer_11 = True
        self.Pigment_Display_Release(0)
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
        # self.layout.f2_live.setChecked(0)
        self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.fg_2[self.obj_index][1], self.fg_2[self.obj_index][2], self.fg_2[self.obj_index][3])
        self.Color_APPLY("RGB", self.fg_2[self.obj_index][1], self.fg_2[self.obj_index][2], self.fg_2[self.obj_index][3], 0)

    def FG_3_LIVE(self):
        if self.layout.f3_live.isChecked() == True:
            self.FG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.fg_3[self.obj_index][4])
            self.Pigment_Display_Release(0)
    def FG_3_APPLY(self):
        if self.fg_3[self.obj_index][0] == "True":
            self.Color_ANGLE(self.fg_3[self.obj_index][1], self.fg_3[self.obj_index][2], self.fg_3[self.obj_index][3])
            self.Color_APPLY("RGB", self.fg_3[self.obj_index][1], self.fg_3[self.obj_index][2], self.fg_3[self.obj_index][3], 0)
            self.Pigment_Display_Release(0)
    def FG_3_SAVE(self, val_1, val_2, val_3, val_4):
        # Variable
        self.fg_3[self.obj_index] = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_3[self.obj_index][1]*255, self.fg_3[self.obj_index][2]*255, self.fg_3[self.obj_index][3]*255, self.fg_3[self.obj_index][4]*255))
        self.layout.f3_color.setStyleSheet(color)
        # Update Object Representation
        self.layer_12 = True
        self.Pigment_Display_Release(0)
    def FG_3_CLEAN(self):
        self.fg_3[self.obj_index] = ["False", 0, 0, 0, 0]
        self.layout.f3_color.setStyleSheet(bg_alpha)
        self.layer_12 = True
    def FG_3_ALPHA(self, SIGNAL_VALUE):
        self.fg_3[self.obj_index][4] = SIGNAL_VALUE
        self.FG_3_Exclusion()
        self.FG_3_SAVE(self.fg_3[self.obj_index][1], self.fg_3[self.obj_index][2], self.fg_3[self.obj_index][3], self.fg_3[self.obj_index][4])
        self.layout.f3_alpha.update()
        self.layer_12 = True
        self.Pigment_Display_Release(0)
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
        # self.layout.f3_live.setChecked(0)
        # Apply Color before Live
        self.Color_ANGLE(self.fg_3[self.obj_index][1], self.fg_3[self.obj_index][2], self.fg_3[self.obj_index][3])
        self.Color_APPLY("RGB", self.fg_3[self.obj_index][1], self.fg_3[self.obj_index][2], self.fg_3[self.obj_index][3], 0)

    def Layer_01_Paint(self, event, width, height):
        self.pixmap_bg_1 = QPixmap.fromImage(QImage(self.path_bg_1))
        image1 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image1.fill(QColor(self.bg_1[self.obj_index][1]*255, self.bg_1[self.obj_index][2]*255, self.bg_1[self.obj_index][3]*255, self.bg_1[self.obj_index][4]*255))
        pixmap_color1 = QPixmap.fromImage(image1)
        painter1 = QPainter()
        painter1.begin(self.pixmap_bg_1)
        painter1.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter1.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter1.drawImage(0,0,pixmap_color1.toImage())
        painter1.end()
        self.layout.layer_01.setPixmap(self.pixmap_bg_1)
    def Layer_02_Paint(self, event, width, height):
        self.pixmap_bg_2 = QPixmap.fromImage(QImage(self.path_bg_2))
        image2 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image2.fill(QColor(self.bg_2[self.obj_index][1]*255, self.bg_2[self.obj_index][2]*255, self.bg_2[self.obj_index][3]*255, self.bg_2[self.obj_index][4]*255))
        pixmap_color2 = QPixmap.fromImage(image2)
        painter2 = QPainter()
        painter2.begin(self.pixmap_bg_2)
        painter2.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter2.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter2.drawImage(0,0,pixmap_color2.toImage())
        painter2.end()
        self.layout.layer_02.setPixmap(self.pixmap_bg_2)
    def Layer_03_Paint(self, event, width, height):
        self.pixmap_bg_3 = QPixmap.fromImage(QImage(self.path_bg_3))
        image3 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image3.fill(QColor(self.bg_3[self.obj_index][1]*255, self.bg_3[self.obj_index][2]*255, self.bg_3[self.obj_index][3]*255, self.bg_3[self.obj_index][4]*255))
        pixmap_color3 = QPixmap.fromImage(image3)
        painter3 = QPainter()
        painter3.begin(self.pixmap_bg_3)
        painter3.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter3.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter3.drawImage(0,0,pixmap_color3.toImage())
        painter3.end()
        self.layout.layer_03.setPixmap(self.pixmap_bg_3)
    def Layer_04_Paint(self, event, width, height):
        self.pixmap_dif_1 = QPixmap.fromImage(QImage(self.path_dif_1))
        image4 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image4.fill(QColor(self.dif_1[self.obj_index][1]*255, self.dif_1[self.obj_index][2]*255, self.dif_1[self.obj_index][3]*255, self.dif_1[self.obj_index][4]*255))
        pixmap_color4 = QPixmap.fromImage(image4)
        painter4 = QPainter()
        painter4.begin(self.pixmap_dif_1)
        painter4.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter4.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter4.drawImage(0,0,pixmap_color4.toImage())
        painter4.end()
        self.layout.layer_04.setPixmap(self.pixmap_dif_1)
    def Layer_05_Paint(self, event, width, height):
        self.pixmap_dif_2 = QPixmap.fromImage(QImage(self.path_dif_2))
        image5 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image5.fill(QColor(self.dif_2[self.obj_index][1]*255, self.dif_2[self.obj_index][2]*255, self.dif_2[self.obj_index][3]*255, self.dif_2[self.obj_index][4]*255))
        pixmap_color5 = QPixmap.fromImage(image5)
        painter5 = QPainter()
        painter5.begin(self.pixmap_dif_2)
        painter5.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter5.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter5.drawImage(0,0,pixmap_color5.toImage())
        painter5.end()
        self.layout.layer_05.setPixmap(self.pixmap_dif_2)
    def Layer_06_Paint(self, event, width, height):
        self.pixmap_dif_3 = QPixmap.fromImage(QImage(self.path_dif_3))
        image6 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image6.fill(QColor(self.dif_3[self.obj_index][1]*255, self.dif_3[self.obj_index][2]*255, self.dif_3[self.obj_index][3]*255, self.dif_3[self.obj_index][4]*255))
        pixmap_color6 = QPixmap.fromImage(image6)
        painter6 = QPainter()
        painter6.begin(self.pixmap_dif_3)
        painter6.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter6.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter6.drawImage(0,0,pixmap_color6.toImage())
        painter6.end()
        self.layout.layer_06.setPixmap(self.pixmap_dif_3)
    def Layer_07_Paint(self, event, width, height):
        self.pixmap_dif_4 = QPixmap.fromImage(QImage(self.path_dif_4))
        image7 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image7.fill(QColor(self.dif_4[self.obj_index][1]*255, self.dif_4[self.obj_index][2]*255, self.dif_4[self.obj_index][3]*255, self.dif_4[self.obj_index][4]*255))
        pixmap_color7 = QPixmap.fromImage(image7)
        painter7 = QPainter()
        painter7.begin(self.pixmap_dif_4)
        painter7.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter7.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter7.drawImage(0,0,pixmap_color7.toImage())
        painter7.end()
        self.layout.layer_07.setPixmap(self.pixmap_dif_4)
    def Layer_08_Paint(self, event, width, height):
        self.pixmap_dif_5 = QPixmap.fromImage(QImage(self.path_dif_5))
        image8 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image8.fill(QColor(self.dif_5[self.obj_index][1]*255, self.dif_5[self.obj_index][2]*255, self.dif_5[self.obj_index][3]*255, self.dif_5[self.obj_index][4]*255))
        pixmap_color8 = QPixmap.fromImage(image8)
        painter8 = QPainter()
        painter8.begin(self.pixmap_dif_5)
        painter8.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter8.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter8.drawImage(0,0,pixmap_color8.toImage())
        painter8.end()
        self.layout.layer_08.setPixmap(self.pixmap_dif_5)
    def Layer_09_Paint(self, event, width, height):
        self.pixmap_dif_6 = QPixmap.fromImage(QImage(self.path_dif_6))
        image9 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image9.fill(QColor(self.dif_6[self.obj_index][1]*255, self.dif_6[self.obj_index][2]*255, self.dif_6[self.obj_index][3]*255, self.dif_6[self.obj_index][4]*255))
        pixmap_color9 = QPixmap.fromImage(image9)
        painter9 = QPainter()
        painter9.begin(self.pixmap_dif_6)
        painter9.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter9.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter9.drawImage(0,0,pixmap_color9.toImage())
        painter9.end()
        self.layout.layer_09.setPixmap(self.pixmap_dif_6)
    def Layer_10_Paint(self, event, width, height):
        self.pixmap_fg_1 = QPixmap.fromImage(QImage(self.path_fg_1))
        image10 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image10.fill(QColor(self.fg_1[self.obj_index][1]*255, self.fg_1[self.obj_index][2]*255, self.fg_1[self.obj_index][3]*255, self.fg_1[self.obj_index][4]*255))
        pixmap_color10 = QPixmap.fromImage(image10)
        painter10 = QPainter()
        painter10.begin(self.pixmap_fg_1)
        painter10.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter10.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter10.drawImage(0,0,pixmap_color10.toImage())
        painter10.end()
        self.layout.layer_10.setPixmap(self.pixmap_fg_1)
    def Layer_11_Paint(self, event, width, height):
        self.pixmap_fg_2 = QPixmap.fromImage(QImage(self.path_fg_2))
        image11 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image11.fill(QColor(self.fg_2[self.obj_index][1]*255, self.fg_2[self.obj_index][2]*255, self.fg_2[self.obj_index][3]*255, self.fg_2[self.obj_index][4]*255))
        pixmap_color11 = QPixmap.fromImage(image11)
        painter11 = QPainter()
        painter11.begin(self.pixmap_fg_2)
        painter11.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter11.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter11.drawImage(0,0,pixmap_color11.toImage())
        painter11.end()
        self.layout.layer_11.setPixmap(self.pixmap_fg_2)
    def Layer_12_Paint(self, event, width, height):
        self.pixmap_fg_3 = QPixmap.fromImage(QImage(self.path_fg_3))
        image12 = QImage(width+limit, height+limit, QImage.Format_ARGB32_Premultiplied)
        image12.fill(QColor(self.fg_3[self.obj_index][1]*255, self.fg_3[self.obj_index][2]*255, self.fg_3[self.obj_index][3]*255, self.fg_3[self.obj_index][4]*255))
        pixmap_color12 = QPixmap.fromImage(image12)
        painter12 = QPainter()
        painter12.begin(self.pixmap_fg_3)
        painter12.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter12.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter12.drawImage(0,0,pixmap_color12.toImage())
        painter12.end()
        self.layout.layer_12.setPixmap(self.pixmap_fg_3)

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

    def OBJ_Geometry(self):
        if self.panel_active == "OBJ":
            self.obj_w = self.layout.panel_obj_mix.width()
            self.obj_h = self.layout.panel_obj_mix.height()
            self.layout.layer_01.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_02.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_03.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_04.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_05.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_06.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_07.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_08.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_09.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_10.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_11.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_12.setGeometry(0,0,self.obj_w,self.obj_h)
            self.layout.layer_cursor.setGeometry(0,0,self.obj_w,self.obj_h)
    def OBJ_Save(self):
        color01 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_1[self.obj_index][1]*255, self.bg_1[self.obj_index][2]*255, self.bg_1[self.obj_index][3]*255, self.bg_1[self.obj_index][4]*255))
        color02 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_2[self.obj_index][1]*255, self.bg_2[self.obj_index][2]*255, self.bg_2[self.obj_index][3]*255, self.bg_2[self.obj_index][4]*255))
        color03 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_3[self.obj_index][1]*255, self.bg_3[self.obj_index][2]*255, self.bg_3[self.obj_index][3]*255, self.bg_3[self.obj_index][4]*255))
        color04 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_1[self.obj_index][1]*255, self.dif_1[self.obj_index][2]*255, self.dif_1[self.obj_index][3]*255, self.dif_1[self.obj_index][4]*255))
        color05 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_2[self.obj_index][1]*255, self.dif_2[self.obj_index][2]*255, self.dif_2[self.obj_index][3]*255, self.dif_2[self.obj_index][4]*255))
        color06 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_3[self.obj_index][1]*255, self.dif_3[self.obj_index][2]*255, self.dif_3[self.obj_index][3]*255, self.dif_3[self.obj_index][4]*255))
        color07 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_4[self.obj_index][1]*255, self.dif_4[self.obj_index][2]*255, self.dif_4[self.obj_index][3]*255, self.dif_4[self.obj_index][4]*255))
        color08 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_5[self.obj_index][1]*255, self.dif_5[self.obj_index][2]*255, self.dif_5[self.obj_index][3]*255, self.dif_5[self.obj_index][4]*255))
        color09 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dif_6[self.obj_index][1]*255, self.dif_6[self.obj_index][2]*255, self.dif_6[self.obj_index][3]*255, self.dif_6[self.obj_index][4]*255))
        color10 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_1[self.obj_index][1]*255, self.fg_1[self.obj_index][2]*255, self.fg_1[self.obj_index][3]*255, self.fg_1[self.obj_index][4]*255))
        color11 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_2[self.obj_index][1]*255, self.fg_2[self.obj_index][2]*255, self.fg_2[self.obj_index][3]*255, self.fg_2[self.obj_index][4]*255))
        color12 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.fg_3[self.obj_index][1]*255, self.fg_3[self.obj_index][2]*255, self.fg_3[self.obj_index][3]*255, self.fg_3[self.obj_index][4]*255))
        self.layout.b1_color.setStyleSheet(color01)
        self.layout.b2_color.setStyleSheet(color02)
        self.layout.b3_color.setStyleSheet(color03)
        self.layout.d1_color.setStyleSheet(color04)
        self.layout.d2_color.setStyleSheet(color05)
        self.layout.d3_color.setStyleSheet(color06)
        self.layout.d4_color.setStyleSheet(color07)
        self.layout.d5_color.setStyleSheet(color08)
        self.layout.d6_color.setStyleSheet(color09)
        self.layout.f1_color.setStyleSheet(color10)
        self.layout.f2_color.setStyleSheet(color11)
        self.layout.f3_color.setStyleSheet(color12)
    def OBJ_Alpha(self):
        self.b1_alpha.Update(self.bg_1[self.obj_index][4], self.layout.b1_alpha.width())
        self.b2_alpha.Update(self.bg_2[self.obj_index][4], self.layout.b2_alpha.width())
        self.b3_alpha.Update(self.bg_3[self.obj_index][4], self.layout.b3_alpha.width())
        self.d1_alpha.Update(self.dif_1[self.obj_index][4], self.layout.d1_alpha.width())
        self.d2_alpha.Update(self.dif_2[self.obj_index][4], self.layout.d2_alpha.width())
        self.d3_alpha.Update(self.dif_3[self.obj_index][4], self.layout.d3_alpha.width())
        self.d4_alpha.Update(self.dif_4[self.obj_index][4], self.layout.d4_alpha.width())
        self.d5_alpha.Update(self.dif_5[self.obj_index][4], self.layout.d5_alpha.width())
        self.d6_alpha.Update(self.dif_6[self.obj_index][4], self.layout.d6_alpha.width())
        self.f1_alpha.Update(self.fg_1[self.obj_index][4], self.layout.f1_alpha.width())
        self.f2_alpha.Update(self.fg_2[self.obj_index][4], self.layout.f2_alpha.width())
        self.f3_alpha.Update(self.fg_3[self.obj_index][4], self.layout.f3_alpha.width())
        self.layout.b1_alpha.update()
        self.layout.b2_alpha.update()
        self.layout.b3_alpha.update()
        self.layout.d1_alpha.update()
        self.layout.d2_alpha.update()
        self.layout.d3_alpha.update()
        self.layout.d4_alpha.update()
        self.layout.d5_alpha.update()
        self.layout.d6_alpha.update()
        self.layout.f1_alpha.update()
        self.layout.f2_alpha.update()
        self.layout.f3_alpha.update()
    def OBJ_Render(self, event):
        if self.layer_01 == True:
            self.Layer_01_Paint(event, self.obj_w, self.obj_h)
            self.layer_01 = False
        if self.layer_02 == True:
            self.Layer_02_Paint(event, self.obj_w, self.obj_h)
            self.layer_02 = False
        if self.layer_03 == True:
            self.Layer_03_Paint(event, self.obj_w, self.obj_h)
            self.layer_03 = False
        if self.layer_04 == True:
            self.Layer_04_Paint(event, self.obj_w, self.obj_h)
            self.layer_04 = False
        if self.layer_05 == True:
            self.Layer_05_Paint(event, self.obj_w, self.obj_h)
            self.layer_05 = False
        if self.layer_06 == True:
            self.Layer_06_Paint(event, self.obj_w, self.obj_h)
            self.layer_06 = False
        if self.layer_07 == True:
            self.Layer_07_Paint(event, self.obj_w, self.obj_h)
            self.layer_07 = False
        if self.layer_08 == True:
            self.Layer_08_Paint(event, self.obj_w, self.obj_h)
            self.layer_08 = False
        if self.layer_09 == True:
            self.Layer_09_Paint(event, self.obj_w, self.obj_h)
            self.layer_09 = False
        if self.layer_10 == True:
            self.Layer_10_Paint(event, self.obj_w, self.obj_h)
            self.layer_10 = False
        if self.layer_11 == True:
            self.Layer_11_Paint(event, self.obj_w, self.obj_h)
            self.layer_11 = False
        if self.layer_12 == True:
            self.Layer_12_Paint(event, self.obj_w, self.obj_h)
            self.layer_12 = False

    #//
    #\\ Signals ################################################################
    def Apply_RGB(self, SIGNAL_APPLY):
        self.rgb_1 = SIGNAL_APPLY[0]
        self.rgb_2 = SIGNAL_APPLY[1]
        self.rgb_3 = SIGNAL_APPLY[2]
        self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
        self.Pigment_Display_Release(0)

    def Signal_UVD(self, SIGNAL_UVD_VALUE):
        if SIGNAL_UVD_VALUE[0] == "UV":
            self.uvd_1 = round(SIGNAL_UVD_VALUE[1]*k_UVD, 2) / k_UVD
            self.uvd_2 = round(SIGNAL_UVD_VALUE[2]*k_UVD, 2) / k_UVD
        if SIGNAL_UVD_VALUE[0] == "D":
            factor = 100
            self.uvd_3 = self.uvd_3 + (SIGNAL_UVD_VALUE[3]/factor)
            self.uvd_3 = self.Math_1D_Limit(self.uvd_3)
        hue = self.uvd_to_ard(self.uvd_1, self.uvd_2, self.uvd_3)
        self.angle_live = hue[0]
        self.Color_APPLY("UVD", self.uvd_1, self.uvd_2, self.uvd_3, 0)
        self.layout.label_percent.setText("")

    def Signal_ARD(self, SIGNAL_ARD_VALUE):
        if SIGNAL_ARD_VALUE[0] == "A":
            factor = 100
            if self.wheel == "CMY":
                hue = self.ard_1 + (SIGNAL_ARD_VALUE[1]/factor)
            if self.wheel == "RYB":
                hue = self.hcmy_to_hryb(self.ard_1) + (SIGNAL_ARD_VALUE[1]/factor)
            if hue <= 0:
                hue += 1
            if hue >= 1:
                hue -= 1
            if self.wheel == "CMY":
                self.angle_live = self.ard_1 = hue
            if self.wheel == "RYB":
                self.angle_live = self.ard_1 = self.hryb_to_hcmy(hue)
            if self.aaa_lock == True:
                ll = self.luma_lock_ard(self.ard_1, self.ard_2, self.ard_3)
                self.Color_APPLY("RGB", ll[0], ll[1], ll[2], 0)
            else:
                self.Color_APPLY("ARD", self.ard_1, self.ard_2, self.ard_3, 0)
        if SIGNAL_ARD_VALUE[0] == "RD":
            self.ard_2 = round(SIGNAL_ARD_VALUE[2]*k_RDL, 2) / k_RDL
            self.ard_3 = round(SIGNAL_ARD_VALUE[3]*k_RDL, 2) / k_RDL
            self.Color_APPLY("ARD", self.ard_1, self.ard_2, self.ard_3, 0)
        self.layout.label_percent.setText("")

    def Signal_HSV_4(self, SIGNAL_HSV_4_VALUE): # Solo e Hue
        if SIGNAL_HSV_4_VALUE[0] == "H":
            factor = 100
            if self.wheel == "CMY":
                hue = self.hsv_1 + (SIGNAL_HSV_4_VALUE[1]/factor)
            if self.wheel == "RYB":
                hue = self.hcmy_to_hryb(self.hsv_1) + (SIGNAL_HSV_4_VALUE[1]/factor)
            if hue <= 0:
                hue += 1
            if hue >= 1:
                hue -= 1
            if self.wheel == "CMY":
                self.angle_live = self.hsv_1 = hue
            if self.wheel == "RYB":
                self.angle_live = self.hsv_1 = self.hryb_to_hcmy(hue)
            if self.aaa_lock == True:
                ll = self.luma_lock_hsv(self.hsv_1, self.hsv_2, self.hsv_3)
                self.Color_APPLY("RGB", ll[0], ll[1], ll[2], 0)
            else:
                self.Color_APPLY("HSV", self.angle_live, self.hsv_2, self.hsv_3, 0)
        if SIGNAL_HSV_4_VALUE[0] == "SV":
            self.hsv_2 = round(SIGNAL_HSV_4_VALUE[2]*k_SVL, 2) / k_SVL
            self.hsv_3 = round(SIGNAL_HSV_4_VALUE[3]*k_SVL, 2) / k_SVL
            self.Color_APPLY("HSV", self.angle_live, self.hsv_2, self.hsv_3, 0)
        self.layout.label_percent.setText("")

    def Signal_HSL_3(self, SIGNAL_HSL_3_VALUE): # Hue Triangle
        if SIGNAL_HSL_3_VALUE[0] == "H":
            factor = 100
            if self.wheel == "CMY":
                hue = self.hsl_1 + (SIGNAL_HSL_3_VALUE[1]/factor)
            if self.wheel == "RYB":
                hue = self.hcmy_to_hryb(self.hsl_1) + (SIGNAL_HSL_3_VALUE[1]/factor)
            if hue <= 0:
                hue += 1
            if hue >= 1:
                hue -= 1
            if self.wheel == "CMY":
                self.angle_live = self.hsl_1 = hue
            if self.wheel == "RYB":
                self.angle_live = self.hsl_1 = self.hryb_to_hcmy(hue)
            if self.aaa_lock == True:
                ll = self.luma_lock_hsl(self.hsl_1, self.hsl_2, self.hsl_3)
                self.Color_APPLY("RGB", ll[0], ll[1], ll[2], 0)
            else:
                self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        if SIGNAL_HSL_3_VALUE[0] == "SL":
            self.hsl_2 = round(SIGNAL_HSL_3_VALUE[2]*k_SVL, 2) / k_SVL
            self.hsl_3 = round(SIGNAL_HSL_3_VALUE[3]*k_SVL, 2) / k_SVL
            self.Color_APPLY("HSL", self.angle_live, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HSL_4(self, SIGNAL_HSL_4_VALUE): # Solo
        if SIGNAL_HSL_4_VALUE[0] == "H":
            factor = 100
            if self.wheel == "CMY":
                hue = self.hsl_1 + (SIGNAL_HSL_4_VALUE[1]/factor)
            if self.wheel == "RYB":
                hue = self.hcmy_to_hryb(self.hsl_1) + (SIGNAL_HSL_4_VALUE[1]/factor)
            if hue <= 0:
                hue += 1
            if hue >= 1:
                hue -= 1
            if self.wheel == "CMY":
                self.angle_live = self.hsl_1 = hue
            if self.wheel == "RYB":
                self.angle_live = self.hsl_1 = self.hryb_to_hcmy(hue)
            if self.aaa_lock == True:
                ll = self.luma_lock_hsl(self.hsl_1, self.hsl_2, self.hsl_3)
                self.Color_APPLY("RGB", ll[0], ll[1], ll[2], 0)
            else:
                self.Color_APPLY("HSL", self.angle_live, self.hsl_2, self.hsl_3, 0)
        if SIGNAL_HSL_4_VALUE[0] == "SL":
            self.hsl_2 = round(SIGNAL_HSL_4_VALUE[2]*k_SVL, 2) / k_SVL
            self.hsl_3 = round(SIGNAL_HSL_4_VALUE[3]*k_SVL, 2) / k_SVL
            self.Color_APPLY("HSL", self.angle_live, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HSL_4D(self, SIGNAL_HSL_4D_VALUE): # Hue Diamond
        if SIGNAL_HSL_4D_VALUE[0] == "H":
            factor = 100
            if self.wheel == "CMY":
                hue = self.hsl_1 + (SIGNAL_HSL_4D_VALUE[1]/factor)
            if self.wheel == "RYB":
                hue = self.hcmy_to_hryb(self.hsl_1) + (SIGNAL_HSL_4D_VALUE[1]/factor)
            if hue <= 0:
                hue += 1
            if hue >= 1:
                hue -= 1
            if self.wheel == "CMY":
                self.angle_live = self.hsl_1 = hue
            if self.wheel == "RYB":
                self.angle_live = self.hsl_1 = self.hryb_to_hcmy(hue)
            if self.aaa_lock == True:
                ll = self.luma_lock_hsl(self.hsl_1, self.hsl_2, self.hsl_3)
                self.Color_APPLY("RGB", ll[0], ll[1], ll[2], 0)
            else:
                self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        if SIGNAL_HSL_4D_VALUE[0] == "SL":
            self.hsl_2 = round(SIGNAL_HSL_4D_VALUE[2]*k_SVL, 2) / k_SVL
            self.hsl_3 = round(SIGNAL_HSL_4D_VALUE[3]*k_SVL, 2) / k_SVL
            self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")

    def Signal_YUV(self, SIGNAL_YUV_VALUE):
        if SIGNAL_YUV_VALUE[0] == "Y":
            factor = 100
            self.yuv_1 = round(self.yuv_1 + (SIGNAL_YUV_VALUE[1]/factor), 2)
            self.Color_APPLY("YUV", self.yuv_1, self.yuv_2, self.yuv_3, 0)
        if SIGNAL_YUV_VALUE[0] == "UV":
            self.yuv_2 = round(SIGNAL_YUV_VALUE[2]*k_U, 2) / k_U
            self.yuv_3 = round(SIGNAL_YUV_VALUE[3]*k_V, 2) / k_V
            rgb = self.yuv_to_rgb(self.yuv_1, self.yuv_2, self.yuv_3)
            self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
            self.Color_APPLY("YUV", self.yuv_1, self.yuv_2, self.yuv_3, 0)
        self.layout.label_percent.setText("")

    def Signal_HUE_Circle(self, SIGNAL_HUE_C_VALUE):
        # Adjust Angle for CMY or RYB
        if self.wheel == "CMY":
            self.angle_live = self.hsl_1 = SIGNAL_HUE_C_VALUE[0]
        if self.wheel == "RYB":
            self.angle_live = self.hsl_1 = self.hryb_to_hcmy(SIGNAL_HUE_C_VALUE[0])
        # Consider if Luminosity Lock is ON of OFF and APPLY the color
        if self.aaa_lock == True:
            ll = self.luma_lock_hsl(self.hsl_1, self.hsl_2, self.hsl_3)
            self.Color_APPLY("RGB", ll[0], ll[1], ll[2], 0)
        else:
            self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")

    def Signal_GAM_Circle(self, SIGNAL_GAM_C_VALUE):
        self.gamut_angle = SIGNAL_GAM_C_VALUE[0]
        self.P1_S1_r = SIGNAL_GAM_C_VALUE[1]
        self.P1_S3_r = SIGNAL_GAM_C_VALUE[2]
        self.P1_S4_r = SIGNAL_GAM_C_VALUE[3]
        self.P2_S1_r = SIGNAL_GAM_C_VALUE[4]
        self.P3_S3_r = SIGNAL_GAM_C_VALUE[5]
        # Update Rotation
        self.Update_Panel_GAM_Circle()
        self.Update_Panel_GAM_Polygon(self.P1_S1_r, self.P1_S3_r, self.P1_S4_r, self.P2_S1_r, self.P3_S3_r)
        self.layout.panel_gam.update()
        self.layout.label_percent.setText("")
    def Signal_GAM_Points(self, SIGNAL_GAM_P_POINTS):
        if SIGNAL_GAM_P_POINTS[0] == "None":
            pass
        if SIGNAL_GAM_P_POINTS[0] == "P1_S1":
            if SIGNAL_GAM_P_POINTS[1] == 1:
                self.P1_S1[0] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S1[1] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 2:
                self.P1_S1[2] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S1[3] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 3:
                self.P1_S1[4] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S1[5] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 4:
                self.P1_S1[6] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S1[7] = SIGNAL_GAM_P_POINTS[3]
            self.panel_gam_circle.update()
            self.panel_gam_polygon.update()
        if SIGNAL_GAM_P_POINTS[0] == "P1_S3":
            if SIGNAL_GAM_P_POINTS[1] == 1:
                self.P1_S3[0] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S3[1] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 2:
                self.P1_S3[2] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S3[3] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 3:
                self.P1_S3[4] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S3[5] = SIGNAL_GAM_P_POINTS[3]
            self.panel_gam_circle.update()
            self.panel_gam_polygon.update()
        if SIGNAL_GAM_P_POINTS[0] == "P1_S4":
            if SIGNAL_GAM_P_POINTS[1] == 1:
                self.P1_S4[0] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S4[1] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 2:
                self.P1_S4[2] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S4[3] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 3:
                self.P1_S4[4] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S4[5] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 4:
                self.P1_S4[6] = SIGNAL_GAM_P_POINTS[2]
                self.P1_S4[7] = SIGNAL_GAM_P_POINTS[3]
            self.panel_gam_circle.update()
            self.panel_gam_polygon.update()
        if SIGNAL_GAM_P_POINTS[0] == "P2_S1":
            if SIGNAL_GAM_P_POINTS[1] == 1:
                self.P2_S1[0] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[1] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 2:
                self.P2_S1[2] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[3] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 3:
                self.P2_S1[4] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[5] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 4:
                self.P2_S1[6] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[7] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 5:
                self.P2_S1[8] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[9] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 6:
                self.P2_S1[10] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[11] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 7:
                self.P2_S1[12] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[13] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 8:
                self.P2_S1[14] = SIGNAL_GAM_P_POINTS[2]
                self.P2_S1[15] = SIGNAL_GAM_P_POINTS[3]
            self.panel_gam_circle.update()
            self.panel_gam_polygon.update()
        if SIGNAL_GAM_P_POINTS[0] == "P3_S3":
            if SIGNAL_GAM_P_POINTS[1] == 1:
                self.P3_S3[0] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[1] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 2:
                self.P3_S3[2] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[3] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 3:
                self.P3_S3[4] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[5] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 4:
                self.P3_S3[6] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[7] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 5:
                self.P3_S3[8] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[9] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 6:
                self.P3_S3[10] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[11] = SIGNAL_GAM_P_POINTS[3]
            if SIGNAL_GAM_P_POINTS[1] == 7:
                self.P3_S3[12] = SIGNAL_GAM_P_POINTS[2]
                self.P3_S3[13] = SIGNAL_GAM_P_POINTS[3]
            self.panel_gam_circle.update()
            self.panel_gam_polygon.update()
        self.layout.label_percent.setText("")
    def Signal_GAM_Polygon(self, SIGNAL_GAM_P_VALUE):
        if SIGNAL_GAM_P_VALUE[0] == "12":
            if self.gamut_space == "ARD":
                if self.wheel == "CMY":
                    hue = self.Math_1D_Loop(SIGNAL_GAM_P_VALUE[1])
                    self.angle_live = self.ard_1 = hue
                    self.ard_2 = SIGNAL_GAM_P_VALUE[2]
                if self.wheel == "RYB":
                    hue = self.Math_1D_Loop(self.hryb_to_hcmy(SIGNAL_GAM_P_VALUE[1]))
                    self.angle_live = self.ard_1 = hue
                    self.ard_2 = SIGNAL_GAM_P_VALUE[2]
                self.Color_APPLY("ARD", self.angle_live, self.ard_2, self.ard_3, 0)
            if self.gamut_space == "HSV":
                if self.wheel == "CMY":
                    hue = self.Math_1D_Loop(SIGNAL_GAM_P_VALUE[1])
                    self.angle_live = self.hsv_1 = hue
                    self.hsv_2 = SIGNAL_GAM_P_VALUE[2]
                if self.wheel == "RYB":
                    hue = self.Math_1D_Loop(self.hryb_to_hcmy(SIGNAL_GAM_P_VALUE[1]))
                    self.angle_live = self.hsv_1 = hue
                    self.hsv_2 = SIGNAL_GAM_P_VALUE[2]
                self.Color_APPLY("HSV", self.angle_live, self.hsv_2, self.hsv_3, 0)
            if self.gamut_space == "HSL":
                if self.wheel == "CMY":
                    hue = self.Math_1D_Loop(SIGNAL_GAM_P_VALUE[1])
                    self.angle_live = self.hsl_1 = hue
                    self.hsl_2 = SIGNAL_GAM_P_VALUE[2]
                if self.wheel == "RYB":
                    hue = self.Math_1D_Loop(self.hryb_to_hcmy(SIGNAL_GAM_P_VALUE[1]))
                    self.angle_live = self.hsl_1 = hue
                    self.hsl_2 = SIGNAL_GAM_P_VALUE[2]
                self.Color_APPLY("HSL", self.angle_live, self.hsl_2, self.hsl_3, 0)
            if self.gamut_space == "HCY":
                if self.wheel == "CMY":
                    hue = self.Math_1D_Loop(SIGNAL_GAM_P_VALUE[1])
                    self.angle_live = self.hcy_1 = hue
                    self.hcy_2 = SIGNAL_GAM_P_VALUE[2]
                if self.wheel == "RYB":
                    hue = self.Math_1D_Loop(self.hryb_to_hcmy(SIGNAL_GAM_P_VALUE[1]))
                    self.angle_live = self.hcy_1 = hue
                    self.hcy_2 = SIGNAL_GAM_P_VALUE[2]
                self.Color_APPLY("HCY", self.angle_live, self.hcy_2, self.hcy_3, 0)
        if SIGNAL_GAM_P_VALUE[0] == "3":
            factor = 100
            if self.gamut_space == "ARD":
                self.ard_3 = self.ard_3 + (SIGNAL_GAM_P_VALUE[3]/factor)
                self.ard_3 = self.Math_1D_Limit(self.ard_3)
                self.Color_APPLY("ARD", self.ard_1, self.ard_2, self.ard_3, 0)
            if self.gamut_space == "HSV":
                self.hsv_3 = self.hsv_3 + (SIGNAL_GAM_P_VALUE[3]/factor)
                self.hsv_3 = self.Math_1D_Limit(self.hsv_3)
                self.Color_APPLY("HSV", self.hsv_1, self.hsv_2, self.hsv_3, 0)
            if self.gamut_space == "HSL":
                self.hsl_3 = self.hsl_3 + (SIGNAL_GAM_P_VALUE[3]/factor)
                self.hsl_3 = self.Math_1D_Limit(self.hsl_3)
                self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
            if self.gamut_space == "HCY":
                self.hcy_3 = self.hcy_3 + (SIGNAL_GAM_P_VALUE[3]/factor)
                self.hcy_3 = self.Math_1D_Limit(self.hcy_3)
                self.Color_APPLY("HCY", self.hcy_1, self.hcy_2, self.hcy_3, 0)
        self.layout.label_percent.setText("")

    def Signal_DOT(self, SIGNAL_DOT_VALUE):
        # Geometry
        width = self.layout.panel_dot_mix.width()
        height = self.layout.panel_dot_mix.height()
        pixmap = self.layout.panel_dot_mix.grab(QRect(QPoint(0, 0), QPoint(width, height)))
        image = pixmap.toImage()
        scaled = image.scaled(QSize(width, height))
        color = scaled.pixelColor(SIGNAL_DOT_VALUE[0], SIGNAL_DOT_VALUE[1])
        # Apply Color Values
        if (color.red() != 0 and color.green() != 0 and color.blue() != 0):
            self.rgb_1 = color.red()/255
            self.rgb_2 = color.green()/255
            self.rgb_3 = color.blue()/255
            # Apply Colors
            self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
            self.layout.label_percent.setText("")
    def Signal_DOT_Location(self, SIGNAL_DOT_LOCATION):
        self.dot_location_x = SIGNAL_DOT_LOCATION[0]
        self.dot_location_y = SIGNAL_DOT_LOCATION[1]

    def Signal_OBJ(self, SIGNAL_OBJ_PRESS):
        # Geometry
        width = self.obj_w
        height = self.obj_h
        pixmap = self.layout.panel_obj_mix.grab(QRect(QPoint(0, 0), QPoint(self.obj_w, self.obj_h)))
        image = pixmap.toImage()
        color = image.pixelColor(SIGNAL_OBJ_PRESS[0], SIGNAL_OBJ_PRESS[1])
        # Apply Color Values
        self.rgb_1 = color.red()/255
        self.rgb_2 = color.green()/255
        self.rgb_3 = color.blue()/255
        # Apply Colors
        self.angle_live = self.rgb_to_angle(self.rgb_1, self.rgb_2, self.rgb_3)[0]
        self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
        self.layout.label_percent.setText("")
    def Signal_OBJ_Location(self, SIGNAL_OBJ_LOCATION):
        self.obj_location_x = SIGNAL_OBJ_LOCATION[0]
        self.obj_location_y = SIGNAL_OBJ_LOCATION[1]

    def Pigment_Panel_Zoom(self, SIGNAL_ZOOM):
        self.zoom = SIGNAL_ZOOM

    #//
    #\\ Style ##################################################################
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
            "stop:0.996 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(255, 255, 255, 255), \n"+
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
            "stop:0.996 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(255, 255, 255, 255), \n"+
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
            "stop:0.996 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(255, 255, 255, 255), \n"+
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
            width = int(width / 50) + 1
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
            # ARD to RGB Conversion
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
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # HUE entry type
        if hue == "HSV":
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
        if hue == "HCY":
            # Convert Left
            left_rgb = self.hcy_to_rgb(left[0], left[1], left[2])
            left_r = round(left_rgb[0],3)
            left_g = round(left_rgb[1],3)
            left_b = round(left_rgb[2],3)
            # Convert Right
            right_rgb = self.hcy_to_rgb(right[0], right[1], right[2])
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
            ssc = (left[1] + (stop * cond1))
            vly = (left[2] + (stop * cond2))
            # H** to RGB Conversion
            if hue == "HSV":
                rgb = self.hsv_to_rgb(h, ssc, vly)
            if hue == "HSL":
                rgb = self.hsl_to_rgb(h, ssc, vly)
            if hue == "HCY":
                rgb = self.hcy_to_rgb(h, ssc, vly)
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
            width = int(width / 50) + 1
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
            width = int(width / 50) + 1
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
    def HCY_Gradient(self, width, color_left, color_right):
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
        left_rgb = self.hcy_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.hcy_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, left_r*255, left_g*255, left_b*255)
        try:
            width = int(width / 50) + 1
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
            c = (left[1] + (stop * cond3))
            y = (left[2] + (stop * cond4))

            # HSL to RGB Conversion
            rgb = self.hcy_to_rgb(h, c, y)
            r = round(rgb[0],3)
            g = round(rgb[1],3)
            b = round(rgb[2],3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, r*255, g*255, b*255)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) ; \n " % (1.000, right_r*255, right_g*255, right_b*255)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    def YUV_Gradient(self, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Convert Left
        left_rgb = self.yuv_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.yuv_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Middle Points
        mid25_rgb = self.yuv_to_rgb(left[0]+((right[0]-left[0])*0.25), left[1]+((right[1]-left[1])*0.25), left[2]+((right[2]-left[2])*0.25))
        mid25_r = round(mid25_rgb[0],3)
        mid25_g = round(mid25_rgb[1],3)
        mid25_b = round(mid25_rgb[2],3)
        mid50_rgb = self.yuv_to_rgb(left[0]+((right[0]-left[0])*0.5), left[1]+((right[1]-left[1])*0.5), left[2]+((right[2]-left[2])*0.5))
        mid50_r = round(mid50_rgb[0],3)
        mid50_g = round(mid50_rgb[1],3)
        mid50_b = round(mid50_rgb[2],3)
        mid75_rgb = self.yuv_to_rgb(left[0]+((right[0]-left[0])*0.75), left[1]+((right[1]-left[1])*0.75), left[2]+((right[2]-left[2])*0.75))
        mid75_r = round(mid75_rgb[0],3)
        mid75_g = round(mid75_rgb[1],3)
        mid75_b = round(mid75_rgb[2],3)
        # Style String
        slider_gradient = (
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%s, %s, %s), stop:0.25 rgb(%s, %s, %s), stop:0.5 rgb(%s, %s, %s), stop:0.75 rgb(%s, %s, %s), stop:1 rgb(%s, %s, %s) ) ; border: 1px solid rgba(56, 56, 56, 255) ;"
         % (left_r*255, left_g*255, left_b*255, mid25_r*255, mid25_g*255, mid25_b*255, mid50_r*255, mid50_g*255, mid50_b*255, mid75_r*255, mid75_g*255, mid75_b*255, right_r*255, right_g*255, right_b*255)
         )
        # Return StyleSheet String
        return slider_gradient
    def RYB_Gradient(self, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Convert Left
        left_rgb = self.ryb_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.ryb_to_rgb(right[0], right[1], right[2])
        right_r = round(right_rgb[0],3)
        right_g = round(right_rgb[1],3)
        right_b = round(right_rgb[2],3)
        # Middle Points
        mid25_rgb = self.ryb_to_rgb(left[0]+((right[0]-left[0])*0.25), left[1]+((right[1]-left[1])*0.25), left[2]+((right[2]-left[2])*0.25))
        mid25_r = round(mid25_rgb[0],3)
        mid25_g = round(mid25_rgb[1],3)
        mid25_b = round(mid25_rgb[2],3)
        mid50_rgb = self.ryb_to_rgb(left[0]+((right[0]-left[0])*0.5), left[1]+((right[1]-left[1])*0.5), left[2]+((right[2]-left[2])*0.5))
        mid50_r = round(mid50_rgb[0],3)
        mid50_g = round(mid50_rgb[1],3)
        mid50_b = round(mid50_rgb[2],3)
        mid75_rgb = self.ryb_to_rgb(left[0]+((right[0]-left[0])*0.75), left[1]+((right[1]-left[1])*0.75), left[2]+((right[2]-left[2])*0.75))
        mid75_r = round(mid75_rgb[0],3)
        mid75_g = round(mid75_rgb[1],3)
        mid75_b = round(mid75_rgb[2],3)
        # Style String
        slider_gradient = (
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%s, %s, %s), stop:0.25 rgb(%s, %s, %s), stop:0.5 rgb(%s, %s, %s), stop:0.75 rgb(%s, %s, %s), stop:1 rgb(%s, %s, %s) ) ; border: 1px solid rgba(56, 56, 56, 255) ;"
         % (left_r*255, left_g*255, left_b*255, mid25_r*255, mid25_g*255, mid25_b*255, mid50_r*255, mid50_g*255, mid50_b*255, mid75_r*255, mid75_g*255, mid75_b*255, right_r*255, right_g*255, right_b*255)
         )
        # Return StyleSheet String
        return slider_gradient
    def CMY_Gradient(self, color_left, color_right):
        """ Input: 0-1 """
        # Colors
        left = [color_left[0], color_left[1], color_left[2]]
        right = [color_right[0], color_right[1], color_right[2]]
        # Convert Left
        left_rgb = self.cmy_to_rgb(left[0], left[1], left[2])
        left_r = round(left_rgb[0],3)
        left_g = round(left_rgb[1],3)
        left_b = round(left_rgb[2],3)
        # Convert Right
        right_rgb = self.cmy_to_rgb(right[0], right[1], right[2])
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
    def KKK_Gradient(self, r, g, b):
        """ Input: 0-1 """
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n"
        length = len(kelvin_table) - 1
        for i in range(length):
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (round(i/length,3), kelvin_table[i][1]*r, kelvin_table[i][2]*g, kelvin_table[i][3]*b)
        slider_gradient += "stop:%s rgb(%s, %s, %s)); \n " % (1.000, kelvin_table[length][1]*r, kelvin_table[length][2]*g, kelvin_table[length][3]*b)
        slider_gradient += "border: 1px solid rgba(56, 56, 56, 255) ; "
        # Return StyleSheet String
        return slider_gradient
    # Icons
    def Icon_Corner(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <path \n" +
        "       style=\"fill:"+hex+";stroke:none;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;fill-opacity:1\" \n" +
        "       d=\"M 1.0583333,2.9104166 2.9104166,1.0583333 V 2.9104166 H 1.0583333\" \n" +
        "       id=\"path876\" /> \n" +
        "  </g> \n" +
        "</svg>"
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Menu(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke-width:2.06501;stroke-dasharray:2.06501, 2.06501\" \n" +
        "       id=\"rect874\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"0.52916646\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"2.3812499\" /> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke-width:2.065;stroke-dasharray:2.065, 2.065\" \n" +
        "       id=\"rect876\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"1.0583335\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"1.0583333\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Left(self, hex):
        string = str(
        "<svg width=\"20\" height=\"20\" viewBox=\"0 0 5.2916665 5.2916668\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g inkscape:label=\"Layer 1\" inkscape:groupmode=\"layer\" id=\"layer1\"> \n" +
        "    <path \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "       d=\"M 1.8520833,2.6458333 3.4395833,1.5875 v 2.1166667 l -1.5875,-1.0583334\" \n" +
        "       id=\"path832\" \n" +
        "       sodipodi:nodetypes=\"cccc\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Right(self, hex):
        string = str(
        "<svg width=\"20\" height=\"20\" viewBox=\"0 0 5.2916665 5.2916668\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <path \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "       d=\"M 3.4395833,2.6458333 1.8520833,1.5875 v 2.1166667 l 1.5875,-1.0583334\" \n" +
        "       id=\"path832\" \n" +
        "       sodipodi:nodetypes=\"cccc\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Panel(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583\" \n" +
        "       id=\"rect888\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"1.8520833\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"1.0583333\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Lock(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <rect \n" +
        "       style=\"display:inline;opacity:1;fill:"+hex+";fill-opacity:1;stroke-width:1.84699;stroke-dasharray:1.84699, 1.84699\" \n" +
        "       id=\"rect833\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"1.0583333\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"1.8520834\" \n" +
        "       inkscape:label=\"bot\" /> \n" +
        "    <path \n" +
        "       style=\"display:inline;fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\" \n" +
        "       d=\"M 1.3229165,1.8520834 V 1.3229167 L 1.5874998,1.0583334 h 0.79375 L 2.6458331,1.3229167 V 1.8520834 H 2.3812498 l 10e-8,-0.419573 L 2.2716562,1.3229167 H 1.6970938 l -0.1095939,0.1095939 -1e-7,0.4195728 H 1.3229165\" \n" +
        "       id=\"path846\" \n" +
        "       sodipodi:nodetypes=\"ccccccccccccc\" \n" +
        "       inkscape:label=\"top\" /> \n" +
        "  </g> \n" +
        "</svg>"
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Tip(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <circle \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583\" \n" +
        "       id=\"path890\" \n" +
        "       cx=\"1.984375\" \n" +
        "       cy=\"1.984375\" \n" +
        "       r=\"0.92604166\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Tip_Empty(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <path \n" +
        "        id=\"path890\" \n" +
        "        style=\"fill:#d4d4d4;fill-opacity:1;stroke:none;stroke-width:0.999999\" \n" +
        "        d=\"M 7.5,4 A 3.5,3.5 0 0 0 4,7.5 3.5,3.5 0 0 0 7.5,11 3.5,3.5 0 0 0 11,7.5 3.5,3.5 0 0 0 7.5,4 Z M 7.4511719,5.5 A 1.9999999,1.9999999 0 0 1 7.5,5.5 a 1.9999999,1.9999999 0 0 1 2,2 1.9999999,1.9999999 0 0 1 -2,2 1.9999999,1.9999999 0 0 1 -2,-2 1.9999999,1.9999999 0 0 1 1.9511719,-2 z\" \n" +
        "        transform=\"scale(0.26458333)\" /> \n" +
        "  </g> \n" +
        "</svg>"
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Slider(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\"> \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\"> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.187088\" \n" +
        "       id=\"rect880\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"0.26458341\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"1.0583333\" /> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.187088\" \n" +
        "       id=\"rect882\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"0.26458329\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"2.1166666\" /> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0.264583\" \n" +
        "       id=\"rect884\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"0.26458332\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"2.6458333\" /> \n" +
        "    <rect \n" +
        "       style=\"fill:"+hex+";stroke-width:0.264583\" \n" +
        "       id=\"rect835\" \n" +
        "       width=\"1.8520833\" \n" +
        "       height=\"0.26458332\" \n" +
        "       x=\"1.0583333\" \n" +
        "       y=\"1.5875\" /> \n" +
        "  </g> \n" +
        "</svg> "
        )
        array = bytearray(string, encoding='utf-8')
        return array
    def Icon_Key(self, hex):
        string = str(
        "<svg width=\"15\" height=\"15\" viewBox=\"0 0 3.9687499 3.9687501\" version=\"1.1\" id=\"svg8\" > \n" +
        "  <defs id=\"defs2\" /> \n" +
        "  <g \n" +
        "     inkscape:label=\"Layer 1\" \n" +
        "     inkscape:groupmode=\"layer\" \n" +
        "     id=\"layer1\" \n" +
        "     style=\"display:inline\"> \n" +
        "    <path \n" +
        "       id=\"key\" \n" +
        "       style=\"fill:"+hex+";fill-opacity:1;stroke:none;stroke-width:0;stroke-dasharray:0, 0\" \n" +
        "       d=\"M 7.5,4 A 3.5000002,3.4999997 0 0 0 4,7.5 3.5000002,3.4999997 0 0 0 7.5,11 3.5000002,3.4999997 0 0 0 11,7.5 3.5000002,3.4999997 0 0 0 7.5,4 Z m -1,1.5 h 2 v 4 h -2 z\" \n" +
        "       transform=\"scale(0.26458333)\" /> \n" +
        "  </g> \n" +
        "</svg>"
        )
        array = bytearray(string, encoding='utf-8')
        return array
    # Cursor
    def SVG_Cursor_LMB(self):
        string_cursor_lmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#ffffff;fill-opacity:1;stroke:none;stroke-width:1.29929912\" \n" +
        "     d=\"M 50,6 A 43.999998,43.999998 0 0 0 6,50 43.999998,43.999998 0 0 0 50,94 43.999998,43.999998 0 0 0 94,50 43.999998,43.999998 0 0 0 50,6 Z m 0,6.5 A 37.500001,37.500001 0 0 1 87.5,50 37.500001,37.500001 0 0 1 50,87.5 37.500001,37.500001 0 0 1 12.5,50 37.500001,37.500001 0 0 1 50,12.5 Z\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     id=\"circle821\" \n" +
        "     inkscape:label=\"White\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "</svg> "
        )
        array_cursor_lmb = bytearray(string_cursor_lmb, encoding='utf-8')
        return array_cursor_lmb

    #//
    #\\ Widget Events ##########################################################
    # Docker Events
    def showEvent(self, event):
        # Layout loads as vertical Size Policy Ignore for correct loading purposes and after the loadding is done I can set it up to the correct Size policy so it works well after, This happens after the init function has ended
        self.window.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # Colors
        self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
        self.Pigment_Display()
        self.Mixer_Display()
        self.Ratio()
        # Start Timer when the Docker is Present
        if check_timer >= 1000:
            self.timer.start()
    def enterEvent(self, event):
        # Check Krita Once before editing Pigmento
        self.Krita_2_Pigment()
        # Confirm Panel
        self.Ratio()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.stop()
    def leaveEvent(self, event):
        # Save Settings
        self.Default_Save()

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
        self.Default_Save()
    # Keyboard Events
    def keyPressEvent(self, event):
        """keyPressEvent to work requires the mouse to be over Pigmento docker and for that given key be free from any Shortcuts"""
        # Select Operation
        set_1 = "RGB"
        set_2 = "RGB"
        set_3 = "RGB"
        # Set 1
        if event.key() == Qt.Key_U:
            if set_1 == "SOF":self.Pigment_SOF_1_Plus()
            if set_1 == "AAA":self.Pigment_AAA_1_Plus()
            if set_1 == "RGB":self.Pigment_RGB_1_Plus()
            if set_1 == "ARD":self.Pigment_ARD_1_Plus()
            if set_1 == "HSV":self.Pigment_HSV_1_Plus()
            if set_1 == "HSL":self.Pigment_HSL_1_Plus()
            if set_1 == "HCY":self.Pigment_HCY_1_Plus()
            if set_1 == "RYB":self.Pigment_RYB_1_Plus()
            if set_1 == "CMY":self.Pigment_CMY_1_Plus()
            if set_1 == "CMYK":self.Pigment_CMYK_1_Plus()
            if set_1 == "KKK":self.Pigment_KKK_1_Plus()
        if event.key() == Qt.Key_J:
            if set_1 == "SOF":self.Pigment_SOF_1_Minus()
            if set_1 == "AAA":self.Pigment_AAA_1_Minus()
            if set_1 == "RGB":self.Pigment_RGB_1_Minus()
            if set_1 == "ARD":self.Pigment_ARD_1_Minus()
            if set_1 == "HSV":self.Pigment_HSV_1_Minus()
            if set_1 == "HSL":self.Pigment_HSL_1_Minus()
            if set_1 == "HCY":self.Pigment_HCY_1_Minus()
            if set_1 == "RYB":self.Pigment_RYB_1_Minus()
            if set_1 == "CMY":self.Pigment_CMY_1_Minus()
            if set_1 == "CMYK":self.Pigment_CMYK_1_Minus()
            if set_1 == "KKK":self.Pigment_KKK_1_Minus()
        # Set 2
        if event.key() == Qt.Key_I:
            if set_2 == "SOF":self.Pigment_SOF_2_Plus()
            if set_2 == "RGB":self.Pigment_RGB_2_Plus()
            if set_2 == "ARD":self.Pigment_ARD_2_Plus()
            if set_2 == "HSV":self.Pigment_HSV_2_Plus()
            if set_2 == "HSL":self.Pigment_HSL_2_Plus()
            if set_2 == "HCY":self.Pigment_HCY_2_Plus()
            if set_2 == "RYB":self.Pigment_RYB_2_Plus()
            if set_2 == "CMY":self.Pigment_CMY_2_Plus()
            if set_2 == "CMYK":self.Pigment_CMYK_2_Plus()
        if event.key() == Qt.Key_K:
            if set_2 == "SOF":self.Pigment_SOF_2_Minus()
            if set_2 == "RGB":self.Pigment_RGB_2_Minus()
            if set_2 == "ARD":self.Pigment_ARD_2_Minus()
            if set_2 == "HSV":self.Pigment_HSV_2_Minus()
            if set_2 == "HSL":self.Pigment_HSL_2_Minus()
            if set_2 == "HCY":self.Pigment_HCY_2_Minus()
            if set_2 == "RYB":self.Pigment_RYB_2_Minus()
            if set_2 == "CMY":self.Pigment_CMY_2_Minus()
            if set_2 == "CMYK":self.Pigment_CMYK_2_Minus()
        # Set 3
        if event.key() == Qt.Key_O:
            if set_3 == "SOF":self.Pigment_SOF_3_Plus()
            if set_3 == "RGB":self.Pigment_RGB_3_Plus()
            if set_3 == "ARD":self.Pigment_ARD_3_Plus()
            if set_3 == "HSV":self.Pigment_HSV_3_Plus()
            if set_3 == "HSL":self.Pigment_HSL_3_Plus()
            if set_3 == "HCY":self.Pigment_HCY_3_Plus()
            if set_3 == "RYB":self.Pigment_RYB_3_Plus()
            if set_3 == "CMY":self.Pigment_CMY_3_Plus()
            if set_3 == "CMYK":self.Pigment_CMYK_3_Plus()
        if event.key() == Qt.Key_L:
            if set_3 == "SOF":self.Pigment_SOF_3_Minus()
            if set_3 == "RGB":self.Pigment_RGB_3_Minus()
            if set_3 == "ARD":self.Pigment_ARD_3_Minus()
            if set_3 == "HSV":self.Pigment_HSV_3_Minus()
            if set_3 == "HSL":self.Pigment_HSL_3_Minus()
            if set_3 == "HCY":self.Pigment_HCY_3_Minus()
            if set_3 == "RYB":self.Pigment_RYB_3_Minus()
            if set_3 == "CMY":self.Pigment_CMY_3_Minus()
            if set_3 == "CMYK":self.Pigment_CMYK_3_Minus()
    def keyReleaseEvent(self, event):
        pass
    # Paint Events
    def paintEvent(self, event):
        # Update Frames on Widget Recalling
        self.Ratio_Box()
        # Updates Painter on PANEL Widget Recalling
        try:
            if self.panel_active == "RGB":
                self.Update_Panel_UVD()
            if self.panel_active == "ARD":
                self.Update_Panel_ARD()
            if self.panel_active == "HSV":
                self.Update_Panel_HSV()
            if self.panel_active == "HSL":
                self.Update_Panel_HSL()
            if self.panel_active == "YUV":
                self.Update_Panel_YUV()
            if self.panel_active == "HUE":
                self.Update_Panel_HUE()
            if self.panel_active == "GAM":
                self.Update_Panel_GAM_Circle()
                self.Update_Panel_GAM_Polygon(self.P1_S1_r, self.P1_S3_r, self.P1_S4_r, self.P2_S1_r, self.P3_S3_r)
            if self.panel_active == "DOT":
                self.Update_Panel_DOT()
            if self.panel_active == "OBJ":
                if self.layer_01 == True:
                    self.Layer_01_Paint(event, self.obj_w, self.obj_h)
                    self.layer_01 = False
                if self.layer_02 == True:
                    self.Layer_02_Paint(event, self.obj_w, self.obj_h)
                    self.layer_02 = False
                if self.layer_03 == True:
                    self.Layer_03_Paint(event, self.obj_w, self.obj_h)
                    self.layer_03 = False
                if self.layer_04 == True:
                    self.Layer_04_Paint(event, self.obj_w, self.obj_h)
                    self.layer_04 = False
                if self.layer_05 == True:
                    self.Layer_05_Paint(event, self.obj_w, self.obj_h)
                    self.layer_05 = False
                if self.layer_06 == True:
                    self.Layer_06_Paint(event, self.obj_w, self.obj_h)
                    self.layer_06 = False
                if self.layer_07 == True:
                    self.Layer_07_Paint(event, self.obj_w, self.obj_h)
                    self.layer_07 = False
                if self.layer_08 == True:
                    self.Layer_08_Paint(event, self.obj_w, self.obj_h)
                    self.layer_08 = False
                if self.layer_09 == True:
                    self.Layer_09_Paint(event, self.obj_w, self.obj_h)
                    self.layer_09 = False
                if self.layer_10 == True:
                    self.Layer_10_Paint(event, self.obj_w, self.obj_h)
                    self.layer_10 = False
                if self.layer_11 == True:
                    self.Layer_11_Paint(event, self.obj_w, self.obj_h)
                    self.layer_11 = False
                if self.layer_12 == True:
                    self.Layer_12_Paint(event, self.obj_w, self.obj_h)
                    self.layer_12 = False
        except:
            pass
        # Return Paint event to Regain Docker Title
        return super().paintEvent(event)

    #//
    #\\ Settings ###############################################################
    def Version_Settings(self):
        self.Default_Boot()
        try:
            version = self.Settings_Load_Version()
            if pigment_o_version == version:
                self.Settings_Load_Misc()
                self.Settings_Load_ActiveColor()
                self.Settings_Load_UI()
        except:
            QtCore.qDebug("Load Error - Wrong Version")

    def Default_Boot(self):
        # First To Load
        #\\ Locks ##############################################################
        self.aaa_lock = False # AAA / BW channel
        self.hsx_lock = [0, 0, 0] # AAA / BW hsx value to bind too while doing variation
        self.cmyk_lock = False # CMYK channel
        self.kkk_lock = False  # KELVIN channel

        #//
        #\\ Harmony ############################################################
        self.harmony_menu = False
        self.harmony_rule = 0
        self.harmony_active = 0
        self.harmony_render = "COLOR"
        self.harmony_index = "Analogous"
        self.harmony_edit = False
        self.harmony_delta = 30
        self.har_1 = ["HSL", 0,0,0, 0,0,0]
        self.har_2 = ["HSL", 0,0,0, 0,0,0]
        self.har_3 = ["HSL", 0,0,0, 0,0,0]
        self.har_4 = ["HSL", 0,0,0, 0,0,0]
        self.har_5 = ["HSL", 0,0,0, 0,0,0]
        self.layout.harmony_1.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_1[1]*255, self.har_1[2]*255, self.har_1[3]*255)))
        self.layout.harmony_2.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_2[1]*255, self.har_2[2]*255, self.har_2[3]*255)))
        self.layout.harmony_3.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_3[1]*255, self.har_3[2]*255, self.har_3[3]*255)))
        self.layout.harmony_4.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_4[1]*255, self.har_4[2]*255, self.har_4[3]*255)))
        self.layout.harmony_5.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_5[1]*255, self.har_5[2]*255, self.har_5[3]*255)))

        #//
        #\\ Panel ##############################################################
        self.panel_active = "HSV"
        self.zoom = 0

        #//
        #\\ Panel HUE ##########################################################
        self.panel_secondary = "DOT"

        #//
        #\\ Panel GAM ##########################################################
        self.gamut_space = "ARD"
        self.gamut_shape = "None"
        self.gamut_initial = 0
        self.gamut_angle = 0

        # Memory
        self.P1_S1 = [
            0.5,0.1,
            0.9,0.5,
            0.5,0.9,
            0.1,0.5]
        self.P1_S3 = [
            0.5,0.1,
            0.84641,0.7,
            0.15359,0.7]
        self.P1_S4 = [
            0.5,0.1,
            0.9,0.5,
            0.5,0.9,
            0.1,0.5]
        self.P2_S1 = [
            # Circle 1
            0.5,0.1,
            0.675,0.275,
            0.5,0.45,
            0.325,0.275,
            # Circle 2
            0.5,0.55,
            0.675,0.725,
            0.5,0.9,
            0.325,0.725]
        self.P3_S3 = [
            # Center
            0.5,0.5,
            # Hexagon
            0.5,0.15359,
            0.8,0.32679,
            0.8,0.67321,
            0.5,0.84641,
            0.2,0.67321,
            0.2,0.32679]
        # Rotation
        self.P1_S1_r = [
            0.5,0.1,
            0.9,0.5,
            0.5,0.9,
            0.1,0.5]
        self.P1_S3_r = [
            0.5,0.1,
            0.84641,0.7,
            0.15359,0.7]
        self.P1_S4_r = [
            0.5,0.1,
            0.9,0.5,
            0.5,0.9,
            0.1,0.5]
        self.P2_S1_r = [
            # Circle 1
            0.5,0.1,
            0.675,0.275,
            0.5,0.45,
            0.325,0.275,
            # Circle 2
            0.5,0.55,
            0.675,0.725,
            0.5,0.9,
            0.325,0.725]
        self.P3_S3_r = [
            # Center
            0.5,0.5,
            # Hexagon
            0.5,0.15359,
            0.8,0.32679,
            0.8,0.67321,
            0.5,0.84641,
            0.2,0.67321,
            0.2,0.32679]
        #//
        #\\ Panel DOT ##########################################################
        self.dot_location_x = 0
        self.dot_location_y = 0
        self.dot_1 = ["True", 183/255, 46/255, 53/255, 1] # Cadmium Red
        self.dot_2 = ["True", 237/255, 181/255, 37/255, 1] # Yellow Ochre
        self.dot_3 = ["True", 41/255, 36/255, 33/255, 1] # IvoryBlack
        self.dot_4 = ["True", 237/255, 240/255, 236/255, 1] # Titanium White
        color1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
        color2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
        color3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
        color4 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
        self.layout.dot_1.setStyleSheet(color1)
        self.layout.dot_2.setStyleSheet(color2)
        self.layout.dot_3.setStyleSheet(color3)
        self.layout.dot_4.setStyleSheet(color4)

        #//
        #\\ Panel OBJ ##########################################################
        # Index Display
        self.obj_index = 0
        self.obj_text = "SPHERE"
        # Cursor Variables
        self.obj_location_x = 0
        self.obj_location_y = 0
        # Panel Variables
        self.obj_w = 0
        self.obj_h = 0
        # Object Color Sets
        self.bg_1 = [
            ["False", 0.5, 0.5, 0.5, 0],
            ["True", 0, 0, 0, 1]]
        self.bg_2 = [
            ["True", 0, 0, 0, 1],
            ["True", 0, 0, 0, 1]]
        self.bg_3 = [
            ["True", 0, 0, 0, 1],
            ["True", 0, 0, 0, 1]]
        self.dif_1 = [
            ["True", 35/255, 20/255, 2/255, 1],
            ["True", 0, 0, 0, 1]]
        self.dif_2 = [
            ["True", 84/255, 55/255, 19/255, 1],
            ["True", 0, 0, 0, 1]]
        self.dif_3 = [
            ["True", 254/255, 159/255, 14/255, 1],
            ["True", 0, 0, 0, 1]]
        self.dif_4 = [
            ["True", 255/255, 202/255, 50/255, 1],
            ["True", 0, 0, 0, 1]]
        self.dif_5 = [
            ["False", 0, 0, 0, 0],
            ["True", 0, 0, 0, 1]]
        self.dif_6 = [
            ["False", 0, 0, 0, 0],
            ["True", 0, 0, 0, 1]]
        self.fg_1 = [
            ["True", 0, 0, 0, 1],
            ["True", 0, 0, 0, 1]]
        self.fg_2 = [
            ["True", 255/255, 255/255, 150/255, 1],
            ["True", 0, 0, 0, 1]]
        self.fg_3 = [
            ["True", 1, 1, 1, 1],
            ["True", 0, 0, 0, 1]]
        # First Object to Load
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
        # Save First Object
        self.OBJ_Geometry()
        self.OBJ_Save()
        self.OBJ_Alpha()
        # Layers Render Variables
        self.layer_01 = True
        self.layer_02 = True
        self.layer_03 = True
        self.layer_04 = True
        self.layer_05 = True
        self.layer_06 = True
        self.layer_07 = True
        self.layer_08 = True
        self.layer_09 = True
        self.layer_10 = True
        self.layer_11 = True
        self.layer_12 = True

        #//
        #\\ SOF ################################################################
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

        #//
        #\\ Channels ###########################################################
        self.hue_shine = False

        #//
        #\\ TIP ################################################################
        self.lock_size = size
        self.lock_opacity = opacity
        self.lock_flow = flow
        self.cor_00 = ["False", 0, 0, 0]
        self.cor_01 = ["False", 0, 0, 0]
        self.cor_02 = ["False", 0, 0, 0]
        self.cor_03 = ["False", 0, 0, 0]
        self.cor_04 = ["False", 0, 0, 0]
        self.cor_05 = ["False", 0, 0, 0]
        self.cor_06 = ["False", 0, 0, 0]
        self.cor_07 = ["False", 0, 0, 0]
        self.cor_08 = ["False", 0, 0, 0]
        self.cor_09 = ["False", 0, 0, 0]
        self.cor_10 = ["False", 0, 0, 0]
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

        #//
        #\\ TTS ################################################################
        self.color_tts = ["False", 0, 0, 0]
        self.gray_tts = color_grey
        self.spacer_tint = 0
        self.spacer_tone = 0
        self.spacer_shade = 0

        #//
        #\\ Mixer TTS ##########################################################
        # Default Load
        self.color_tts = ["False", 0, 0, 0]
        self.gray_tts = color_grey
        self.layout.tts_l1.setStyleSheet(bg_alpha)
        self.layout.white.setStyleSheet(bg_alpha)
        self.layout.grey.setStyleSheet(bg_alpha)
        self.layout.black.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_tint = 0
        self.spacer_tone = 0
        self.spacer_shade = 0
        self.mixer_tint.Update(self.spacer_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.spacer_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.spacer_shade, self.layout.shade.width())

        #//
        #\\ Mixer RGB ##########################################################
        # Mixer RGB 1
        self.color_rgb_l1 = ["False", 0, 0, 0]
        self.color_rgb_r1 = ["False", 0, 0, 0]
        self.layout.rgb_l1.setStyleSheet(bg_alpha)
        self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.spacer_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.mixer_width)
        # Mixer RGB 2
        self.color_rgb_l2 = ["False", 0, 0, 0]
        self.color_rgb_r2 = ["False", 0, 0, 0]
        self.layout.rgb_l2.setStyleSheet(bg_alpha)
        self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.spacer_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.mixer_width)
        # Mixer RGB 3
        self.color_rgb_l3 = ["False", 0, 0, 0]
        self.color_rgb_r3 = ["False", 0, 0, 0]
        self.layout.rgb_l3.setStyleSheet(bg_alpha)
        self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.spacer_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.mixer_width)

        #//
        #\\ Mixer ARD ##########################################################
        # Mixer ARD 1
        self.color_ard_l1 = ["False", 0, 0, 0]
        self.color_ard_r1 = ["False", 0, 0, 0]
        self.layout.ard_l1.setStyleSheet(bg_alpha)
        self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.spacer_ard_g1 = 0
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.mixer_width)
        # Mixer ARD 2
        self.color_ard_l2 = ["False", 0, 0, 0]
        self.color_ard_r2 = ["False", 0, 0, 0]
        self.layout.ard_l2.setStyleSheet(bg_alpha)
        self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.spacer_ard_g2 = 0
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.mixer_width)
        # Mixer ARD 3
        self.color_ard_l3 = ["False", 0, 0, 0]
        self.color_ard_r3 = ["False", 0, 0, 0]
        self.layout.ard_l3.setStyleSheet(bg_alpha)
        self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.spacer_ard_g3 = 0
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.mixer_width)

        #//
        #\\ Mixer HSV ##########################################################
        # Mixer HSV 1
        self.color_hsv_l1 = ["False", 0, 0, 0]
        self.color_hsv_r1 = ["False", 0, 0, 0]
        self.layout.hsv_l1.setStyleSheet(bg_alpha)
        self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.spacer_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.mixer_width)
        # Mixer HSV 2
        self.color_hsv_l2 = ["False", 0, 0, 0]
        self.color_hsv_r2 = ["False", 0, 0, 0]
        self.layout.hsv_l2.setStyleSheet(bg_alpha)
        self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.spacer_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.mixer_width)
        # Mixer HSV 3
        self.color_hsv_l3 = ["False", 0, 0, 0]
        self.color_hsv_r3 = ["False", 0, 0, 0]
        self.layout.hsv_l3.setStyleSheet(bg_alpha)
        self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.spacer_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.mixer_width)

        #//
        #\\ Mixer HSL ##########################################################
        # Mixer HSL 1
        self.color_hsl_l1 = ["False", 0, 0, 0]
        self.color_hsl_r1 = ["False", 0, 0, 0]
        self.layout.hsl_l1.setStyleSheet(bg_alpha)
        self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.spacer_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.mixer_width)
        # Mixer HSL 2
        self.color_hsl_l2 = ["False", 0, 0, 0]
        self.color_hsl_r2 = ["False", 0, 0, 0]
        self.layout.hsl_l2.setStyleSheet(bg_alpha)
        self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.spacer_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.mixer_width)
        # Mixer HSL 3
        self.color_hsl_l3 = ["False", 0, 0, 0]
        self.color_hsl_r3 = ["False", 0, 0, 0]
        self.layout.hsl_l3.setStyleSheet(bg_alpha)
        self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.spacer_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.mixer_width)

        #//
        #\\ Mixer HCY ##########################################################
        # Mixer HCY 1
        self.color_hcy_l1 = ["False", 0, 0, 0]
        self.color_hcy_r1 = ["False", 0, 0, 0]
        self.layout.hcy_l1.setStyleSheet(bg_alpha)
        self.layout.hcy_r1.setStyleSheet(bg_alpha)
        self.spacer_hcy_g1 = 0
        self.mixer_hcy_g1.Update(self.spacer_hcy_g1, self.mixer_width)
        # Mixer HCY 2
        self.color_hcy_l2 = ["False", 0, 0, 0]
        self.color_hcy_r2 = ["False", 0, 0, 0]
        self.layout.hcy_l2.setStyleSheet(bg_alpha)
        self.layout.hcy_r2.setStyleSheet(bg_alpha)
        self.spacer_hcy_g2 = 0
        self.mixer_hcy_g2.Update(self.spacer_hcy_g2, self.mixer_width)
        # Mixer HCY 3
        self.color_hcy_l3 = ["False", 0, 0, 0]
        self.color_hcy_r3 = ["False", 0, 0, 0]
        self.layout.hcy_l3.setStyleSheet(bg_alpha)
        self.layout.hcy_r3.setStyleSheet(bg_alpha)
        self.spacer_hcy_g3 = 0
        self.mixer_hcy_g3.Update(self.spacer_hcy_g3, self.mixer_width)

        #//
        #\\ Mixer YUV ##########################################################
        # Mixer YUV 1
        self.color_yuv_l1 = ["False", 0, 0, 0]
        self.color_yuv_r1 = ["False", 0, 0, 0]
        self.layout.yuv_l1.setStyleSheet(bg_alpha)
        self.layout.yuv_r1.setStyleSheet(bg_alpha)
        self.spacer_yuv_g1 = 0
        self.mixer_yuv_g1.Update(self.spacer_yuv_g1, self.mixer_width)
        # Mixer YUV 2
        self.color_yuv_l2 = ["False", 0, 0, 0]
        self.color_yuv_r2 = ["False", 0, 0, 0]
        self.layout.yuv_l2.setStyleSheet(bg_alpha)
        self.layout.yuv_r2.setStyleSheet(bg_alpha)
        self.spacer_yuv_g2 = 0
        self.mixer_yuv_g2.Update(self.spacer_yuv_g2, self.mixer_width)
        # Mixer YUV 3
        self.color_yuv_l3 = ["False", 0, 0, 0]
        self.color_yuv_r3 = ["False", 0, 0, 0]
        self.layout.yuv_l3.setStyleSheet(bg_alpha)
        self.layout.yuv_r3.setStyleSheet(bg_alpha)
        self.spacer_yuv_g3 = 0
        self.mixer_yuv_g3.Update(self.spacer_yuv_g3, self.mixer_width)

        #//
        #\\ Mixer RYB ##########################################################
        # Mixer RYB 1
        self.color_ryb_l1 = ["False", 0, 0, 0]
        self.color_ryb_r1 = ["False", 0, 0, 0]
        self.layout.ryb_l1.setStyleSheet(bg_alpha)
        self.layout.ryb_r1.setStyleSheet(bg_alpha)
        self.spacer_ryb_g1 = 0
        self.mixer_ryb_g1.Update(self.spacer_ryb_g1, self.mixer_width)
        # Mixer RYB 2
        self.color_ryb_l2 = ["False", 0, 0, 0]
        self.color_ryb_r2 = ["False", 0, 0, 0]
        self.layout.ryb_l2.setStyleSheet(bg_alpha)
        self.layout.ryb_r2.setStyleSheet(bg_alpha)
        self.spacer_ryb_g2 = 0
        self.mixer_ryb_g2.Update(self.spacer_ryb_g2, self.mixer_width)
        # Mixer RYB 3
        self.color_ryb_l3 = ["False", 0, 0, 0]
        self.color_ryb_r3 = ["False", 0, 0, 0]
        self.layout.ryb_l3.setStyleSheet(bg_alpha)
        self.layout.ryb_r3.setStyleSheet(bg_alpha)
        self.spacer_ryb_g3 = 0
        self.mixer_ryb_g3.Update(self.spacer_ryb_g3, self.mixer_width)

        #//
        #\\ Mixer CMYK #########################################################
        # Mixer CMYK 1
        self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
        self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
        self.layout.cmyk_l1.setStyleSheet(bg_alpha)
        self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.spacer_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.mixer_width)
        # Mixer CMYK 2
        self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
        self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
        self.layout.cmyk_l2.setStyleSheet(bg_alpha)
        self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.spacer_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.mixer_width)
        # Mixer CMYK 3
        self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
        self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
        self.layout.cmyk_l3.setStyleSheet(bg_alpha)
        self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.spacer_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.mixer_width)

        #//
        #\\ Mixer Gradient Display #############################################
        self.Mixer_Display()

        #//
        #\\ Color Names ########################################################
        self.names_display = False

        #//
        #\\ Mode ###############################################################
        self.wheel = "CMY"
        self.luminosity = "601"

        #//
        # Last To Load
        #\\ Active Color #######################################################
        # Active Color
        self.rgb_1 = 0
        self.rgb_2 = 0
        self.rgb_3 = 0
        self.angle_live = 0
        self.angle_ryb = 0
        self.uvd_1 = 0
        self.uvd_2 = 0
        self.uvd_3 = 0
        self.d_previous = 0
        self.kkk_0 = 6500
        self.kkk_1 = 255/255
        self.kkk_2 = 249/255
        self.kkk_3 = 253/255
        # Apply Active Color
        self.Hexagon_Points_UVD()
        self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
        self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
        self.Pigment_Display_Release(0)

        #//
        #\\ User Interface #####################################################
        # UI 1
        self.layout.sof.setChecked(False)
        self.layout.aaa.setChecked(False)
        self.layout.rgb.setChecked(False)
        self.layout.ard.setChecked(False)
        self.layout.hsv.setChecked(True)
        self.layout.hsl.setChecked(False)
        self.layout.hcy.setChecked(False)
        self.layout.yuv.setChecked(False)
        self.layout.ryb.setChecked(False)
        self.layout.cmy.setChecked(False)
        self.layout.cmyk.setChecked(False)
        self.layout.kkk.setChecked(False)
        # UI 2
        self.layout.har.setChecked(False)
        self.layout.cotd.setChecked(False)
        self.layout.pan.setChecked(True)
        self.layout.tip.setChecked(False)
        self.layout.tts.setChecked(False)
        self.layout.mix.setChecked(False)
        # UI 3
        self.layout.har_index.setCurrentIndex(2)
        self.layout.har_edit.setChecked(False)
        self.layout.pan_index.setCurrentIndex(3)
        self.layout.pan_secondary.setCurrentIndex(0)
        self.layout.gam_space.setCurrentIndex(0)
        self.layout.gam_shape.setCurrentIndex(0)
        self.layout.dot_set.setChecked(False)
        self.layout.obj_index.setCurrentIndex(0)
        self.layout.obj_set.setChecked(False)
        self.layout.values.setChecked(True)
        self.layout.hue_shine.setChecked(False)
        self.layout.mix_index.setCurrentIndex(2)
        self.layout.names_display.setChecked(False)
        self.layout.wheel_index.setCurrentIndex(0)
        self.layout.luminosity.setCurrentIndex(0)
        # UI4
        self.timer_state = 1 # Timer = ON

        #//
    def Default_Save(self):
        self.Settings_Save_Misc()
        self.Settings_Save_ActiveColor()
        self.Settings_Save_UI()
        self.Settings_Save_Version()

    def Settings_Load_Version(self):
        try:
            version = Krita.instance().readSetting("Pigment.O", "version", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        except:
            version = "False"
        return version
    def Settings_Save_Version(self):
        Krita.instance().writeSetting("Pigment.O", "version", str(pigment_o_version))

    def Settings_Load_UI(self):
        try:
            ui_string = Krita.instance().readSetting("Pigment.O", "ui", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            ui_split = ui_string.split(",")
            self.layout.sof.setChecked(eval(ui_split[0]))
            self.layout.aaa.setChecked(eval(ui_split[1]))
            self.layout.rgb.setChecked(eval(ui_split[2]))
            self.layout.ard.setChecked(eval(ui_split[3]))
            self.layout.hsv.setChecked(eval(ui_split[4]))
            self.layout.hsl.setChecked(eval(ui_split[5]))
            self.layout.hcy.setChecked(eval(ui_split[6]))
            self.layout.yuv.setChecked(eval(ui_split[7]))
            self.layout.ryb.setChecked(eval(ui_split[8]))
            self.layout.cmy.setChecked(eval(ui_split[9]))
            self.layout.cmyk.setChecked(eval(ui_split[10]))
            self.layout.kkk.setChecked(eval(ui_split[11]))

            self.layout.har.setChecked(eval(ui_split[12]))
            self.layout.cotd.setChecked(eval(ui_split[13]))
            self.layout.pan.setChecked(eval(ui_split[14]))
            self.layout.tip.setChecked(eval(ui_split[15]))
            self.layout.tts.setChecked(eval(ui_split[16]))
            self.layout.mix.setChecked(eval(ui_split[17]))

            self.layout.har_index.setCurrentIndex(eval(ui_split[18]))
            self.layout.har_edit.setChecked(eval(ui_split[19]))
            self.layout.pan_index.setCurrentIndex(eval(ui_split[20]))
            self.layout.pan_secondary.setCurrentIndex(eval(ui_split[21]))
            self.layout.gam_space.setCurrentIndex(eval(ui_split[22]))
            self.layout.gam_shape.setCurrentIndex(eval(ui_split[23]))
            self.layout.dot_set.setChecked(eval(ui_split[24]))
            self.layout.obj_index.setCurrentIndex(eval(ui_split[25]))
            self.layout.obj_set.setChecked(eval(ui_split[26]))
            self.layout.values.setChecked(eval(ui_split[27]))
            self.layout.hue_shine.setChecked(eval(ui_split[28]))
            self.layout.mix_index.setCurrentIndex(eval(ui_split[29]))
            self.layout.names_display.setChecked(eval(ui_split[30]))
            self.layout.names_closest.setChecked(eval(ui_split[31]))
            self.layout.luminosity.setCurrentIndex(eval(ui_split[32]))
            self.layout.wheel_index.setCurrentIndex(eval(ui_split[33]))
        except:
            QtCore.qDebug("Load Error - UI")
    def Settings_Save_UI(self):
        ui_list = (
            str(self.layout.sof.isChecked()),
            str(self.layout.aaa.isChecked()),
            str(self.layout.rgb.isChecked()),
            str(self.layout.ard.isChecked()),
            str(self.layout.hsv.isChecked()),
            str(self.layout.hsl.isChecked()),
            str(self.layout.hcy.isChecked()),
            str(self.layout.yuv.isChecked()),
            str(self.layout.ryb.isChecked()),
            str(self.layout.cmy.isChecked()),
            str(self.layout.cmyk.isChecked()),
            str(self.layout.kkk.isChecked()),

            str(self.layout.har.isChecked()),
            str(self.layout.cotd.isChecked()),
            str(self.layout.pan.isChecked()),
            str(self.layout.tip.isChecked()),
            str(self.layout.tts.isChecked()),
            str(self.layout.mix.isChecked()),

            str(self.layout.har_index.currentIndex()),
            str(self.layout.har_edit.isChecked()),
            str(self.layout.pan_index.currentIndex()),
            str(self.layout.pan_secondary.currentIndex()),
            str(self.layout.gam_space.currentIndex()),
            str(self.layout.gam_shape.currentIndex()),
            str(self.layout.dot_set.isChecked()),
            str(self.layout.obj_index.currentIndex()),
            str(self.layout.obj_set.isChecked()),
            str(self.layout.values.isChecked()),
            str(self.layout.hue_shine.isChecked()),
            str(self.layout.mix_index.currentIndex()),
            str(self.layout.names_display.isChecked()),
            str(self.layout.names_closest.isChecked()),
            str(self.layout.luminosity.currentIndex()),
            str(self.layout.wheel_index.currentIndex()),
            )
        ui_string = ','.join(ui_list)
        Krita.instance().writeSetting("Pigment.O", "ui", ui_string)

    def Settings_Load_ActiveColor(self):
        try:
            # Active Color
            active_color_string = Krita.instance().readSetting("Pigment.O", "active_color", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            active_color_split = active_color_string.split(",")
            self.rgb_1 = float(active_color_split[0])
            self.rgb_2 = float(active_color_split[1])
            self.rgb_3 = float(active_color_split[2])
            self.angle_live = float(active_color_split[3])
            self.angle_ryb = float(active_color_split[4])
            self.uvd_1 = float(active_color_split[5])
            self.uvd_2 = float(active_color_split[6])
            self.uvd_3 = float(active_color_split[7])
            self.d_previous = float(active_color_split[8])
            self.kkk_0 = float(active_color_split[9])
            self.kkk_1 = float(active_color_split[10])
            self.kkk_2 = float(active_color_split[11])
            self.kkk_3 = float(active_color_split[12])

            # Active Harmony Read
            har_00_string = Krita.instance().readSetting("Pigment.O", "har_00", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            har_01_string = Krita.instance().readSetting("Pigment.O", "har_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            har_02_string = Krita.instance().readSetting("Pigment.O", "har_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            har_03_string = Krita.instance().readSetting("Pigment.O", "har_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            har_04_string = Krita.instance().readSetting("Pigment.O", "har_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            har_05_string = Krita.instance().readSetting("Pigment.O", "har_05", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            # Active Harmony Split
            har_00_split = har_00_string.split(",")
            har_01_split = har_01_string.split(",")
            har_02_split = har_02_string.split(",")
            har_03_split = har_03_string.split(",")
            har_04_split = har_04_string.split(",")
            har_05_split = har_05_string.split(",")
            # Active Harmony Variables
            self.wheel = str(har_00_split[0])
            self.harmony_index = str(har_00_split[1])
            self.harmony_rule = int(har_00_split[2])
            self.harmony_active = int(har_00_split[3])
            self.harmony_delta = float(har_00_split[4])
            self.harmony_edit = eval(har_00_split[5])
            self.har_1 = ["HSL", eval(har_01_split[1]),eval(har_01_split[2]),eval(har_01_split[3]), eval(har_01_split[4]),eval(har_01_split[5]),eval(har_01_split[6])]
            self.har_2 = ["HSL", eval(har_02_split[1]),eval(har_02_split[2]),eval(har_02_split[3]), eval(har_02_split[4]),eval(har_02_split[5]),eval(har_02_split[6])]
            self.har_3 = ["HSL", eval(har_03_split[1]),eval(har_03_split[2]),eval(har_03_split[3]), eval(har_03_split[4]),eval(har_03_split[5]),eval(har_03_split[6])]
            self.har_4 = ["HSL", eval(har_04_split[1]),eval(har_04_split[2]),eval(har_04_split[3]), eval(har_04_split[4]),eval(har_04_split[5]),eval(har_04_split[6])]
            self.har_5 = ["HSL", eval(har_05_split[1]),eval(har_05_split[2]),eval(har_05_split[3]), eval(har_05_split[4]),eval(har_05_split[5]),eval(har_05_split[6])]

            # Apply Colors
            if self.harmony_active == 1:
                self.Harmony_1_Active(0)
            elif self.harmony_active == 2:
                self.Harmony_2_Active(0)
            elif self.harmony_active == 3:
                self.Harmony_3_Active(0)
            elif self.harmony_active == 4:
                self.Harmony_4_Active(0)
            elif self.harmony_active == 5:
                self.Harmony_5_Active(0)
            else:
                self.Hexagon_Points_UVD()
                self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
                self.Color_APPLY("LOAD", self.rgb_1, self.rgb_2, self.rgb_3, 0)
                self.Pigment_Display_Release(0)
                self.layout.label.setText("COLOR")
            # Harmony Display GUI if active
            if self.panel_active == "HUE":
                self.Update_Panel_HUE()
        except:
            QtCore.qDebug("Load Error - Active Color")
    def Settings_Save_ActiveColor(self):
        # Active Color
        try:
            active_color_list = (
                str(self.rgb_1),
                str(self.rgb_2),
                str(self.rgb_3),
                str(self.angle_live),
                str(self.angle_ryb),
                str(self.uvd_1),
                str(self.uvd_2),
                str(self.uvd_3),
                str(self.d_previous),
                str(self.kkk_0),
                str(self.kkk_1),
                str(self.kkk_2),
                str(self.kkk_3),
                )
            active_color_string = ','.join(active_color_list)
            Krita.instance().writeSetting("Pigment.O", "active_color", active_color_string)
        except:
            QtCore.qDebug("Save Error - Active Color")
        # Harmony
        try:
            har_list_00 = (
                str(self.wheel),
                str(self.harmony_index),
                str(self.harmony_rule),
                str(self.harmony_active),
                str(self.harmony_delta),
                str(self.harmony_edit),
                )
            har_list_01 = (str(self.har_1[0]), str(self.har_1[1]), str(self.har_1[2]), str(self.har_1[3]), str(self.har_1[4]), str(self.har_1[5]), str(self.har_1[6]))
            har_list_02 = (str(self.har_2[0]), str(self.har_2[1]), str(self.har_2[2]), str(self.har_2[3]), str(self.har_2[4]), str(self.har_2[5]), str(self.har_2[6]))
            har_list_03 = (str(self.har_3[0]), str(self.har_3[1]), str(self.har_3[2]), str(self.har_3[3]), str(self.har_3[4]), str(self.har_3[5]), str(self.har_3[6]))
            har_list_04 = (str(self.har_4[0]), str(self.har_4[1]), str(self.har_4[2]), str(self.har_4[3]), str(self.har_4[4]), str(self.har_4[5]), str(self.har_4[6]))
            har_list_05 = (str(self.har_5[0]), str(self.har_5[1]), str(self.har_5[2]), str(self.har_5[3]), str(self.har_5[4]), str(self.har_5[5]), str(self.har_5[6]))
            har_string_00 = ','.join(har_list_00)
            har_string_01 = ','.join(har_list_01)
            har_string_02 = ','.join(har_list_02)
            har_string_03 = ','.join(har_list_03)
            har_string_04 = ','.join(har_list_04)
            har_string_05 = ','.join(har_list_05)
            Krita.instance().writeSetting("Pigment.O", "har_00", har_string_00)
            Krita.instance().writeSetting("Pigment.O", "har_01", har_string_01)
            Krita.instance().writeSetting("Pigment.O", "har_02", har_string_02)
            Krita.instance().writeSetting("Pigment.O", "har_03", har_string_03)
            Krita.instance().writeSetting("Pigment.O", "har_04", har_string_04)
            Krita.instance().writeSetting("Pigment.O", "har_05", har_string_05)
        except:
            QtCore.qDebug("Save Error - Active Harmony")


    def Settings_Load_Misc(self):
        #\\ Panel GAM ##########################################################
        try:
            gam_p1s1_string = Krita.instance().readSetting("Pigment.O", "gam_p1s1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            gam_p1s3_string = Krita.instance().readSetting("Pigment.O", "gam_p1s3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            gam_p1s4_string = Krita.instance().readSetting("Pigment.O", "gam_p1s4", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            gam_p2s1_string = Krita.instance().readSetting("Pigment.O", "gam_p2s1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            gam_p3s3_string = Krita.instance().readSetting("Pigment.O", "gam_p3s3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            p1s1s = gam_p1s1_string.split(",")
            p1s3s = gam_p1s3_string.split(",")
            p1s4s = gam_p1s4_string.split(",")
            p2s1s = gam_p2s1_string.split(",")
            p3s3s = gam_p3s3_string.split(",")
            # Update Variables
            self.P1_S1 = self.P1_S1_r = [
                eval(p1s1s[0]), eval(p1s1s[1]),
                eval(p1s1s[2]), eval(p1s1s[3]),
                eval(p1s1s[4]), eval(p1s1s[5]),
                eval(p1s1s[6]), eval(p1s1s[7]),
                ]
            self.P1_S3 = self.P1_S3_r = [
                eval(p1s3s[0]), eval(p1s3s[1]),
                eval(p1s3s[2]), eval(p1s3s[3]),
                eval(p1s3s[4]), eval(p1s3s[5]),
                ]
            self.P1_S4 = self.P1_S4_r = [
                eval(p1s4s[0]), eval(p1s4s[1]),
                eval(p1s4s[2]), eval(p1s4s[3]),
                eval(p1s4s[4]), eval(p1s4s[5]),
                eval(p1s4s[6]), eval(p1s4s[7]),
                ]
            self.P2_S1 = self.P2_S1_r = [
                eval(p2s1s[0]), eval(p2s1s[1]),
                eval(p2s1s[2]), eval(p2s1s[3]),
                eval(p2s1s[4]), eval(p2s1s[5]),
                eval(p2s1s[6]), eval(p2s1s[7]),
                eval(p2s1s[8]), eval(p2s1s[9]),
                eval(p2s1s[10]), eval(p2s1s[11]),
                eval(p2s1s[12]), eval(p2s1s[13]),
                eval(p2s1s[14]), eval(p2s1s[15]),
                ]
            self.P3_S3 = self.P3_S3_r = [
                eval(p3s3s[0]), eval(p3s3s[1]),
                eval(p3s3s[2]), eval(p3s3s[3]),
                eval(p3s3s[4]), eval(p3s3s[5]),
                eval(p3s3s[6]), eval(p3s3s[7]),
                eval(p3s3s[8]), eval(p3s3s[9]),
                eval(p3s3s[10]), eval(p3s3s[11]),
                eval(p3s3s[12]), eval(p3s3s[13]),
                ]
            # Update widget with Variables
            self.Update_Panel_GAM_Polygon(self.P1_S1, self.P1_S3, self.P1_S4, self.P2_S1, self.P3_S3)
        except:
            QtCore.qDebug("Load Error - Panel GAM")
        #//
        #\\ Panel DOT ##########################################################
        try:
            dot_01_string = Krita.instance().readSetting("Pigment.O", "dot_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            dot_02_string = Krita.instance().readSetting("Pigment.O", "dot_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            dot_03_string = Krita.instance().readSetting("Pigment.O", "dot_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            dot_04_string = Krita.instance().readSetting("Pigment.O", "dot_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            dot_01_split = dot_01_string.split(",")
            dot_02_split = dot_02_string.split(",")
            dot_03_split = dot_03_string.split(",")
            dot_04_split = dot_04_string.split(",")
            if (dot_01_split[0] == "True" or dot_02_split[0] == "True" or dot_03_split[0] == "True" or dot_04_split[0] == "True"):
                if dot_01_split[0] == "True":
                    self.dot_1 = ["True", float(dot_01_split[1]), float(dot_01_split[2]), float(dot_01_split[3])]
                    color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
                    self.layout.dot_1.setStyleSheet(color)
                else:
                    self.dot_1 = ["False", 0, 0, 0]
                    self.layout.dot_1.setStyleSheet(bg_alpha)
                if dot_02_split[0] == "True":
                    self.dot_2 = ["True", float(dot_02_split[1]), float(dot_02_split[2]), float(dot_02_split[3])]
                    color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
                    self.layout.dot_2.setStyleSheet(color)
                else:
                    self.dot_2 = ["False", 0, 0, 0]
                    self.layout.dot_2.setStyleSheet(bg_alpha)
                if dot_03_split[0] == "True":
                    self.dot_3 = ["True", float(dot_03_split[1]), float(dot_03_split[2]), float(dot_03_split[3])]
                    color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
                    self.layout.dot_3.setStyleSheet(color)
                else:
                    self.dot_3 = ["False", 0, 0, 0]
                    self.layout.dot_3.setStyleSheet(bg_alpha)
                if dot_04_split[0] == "True":
                    self.dot_4 = ["True", float(dot_04_split[1]), float(dot_04_split[2]), float(dot_04_split[3])]
                    color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
                    self.layout.dot_4.setStyleSheet(color)
                else:
                    self.dot_4 = ["False", 0, 0, 0]
                    self.layout.dot_4.setStyleSheet(bg_alpha)
        except:
            QtCore.qDebug("Load Error - Panel DOT")
        #//
        #\\ Panel OBJ ##########################################################
        try:
            # Load from File
            object_00_string = Krita.instance().readSetting("Pigment.O", "obj_00", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            object_01_string = Krita.instance().readSetting("Pigment.O", "obj_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            obj00s = object_00_string.split(",")
            obj01s = object_01_string.split(",")
            # Assign Variables
            self.bg_1 = [
                [eval(obj00s[0]), eval(obj00s[1]), eval(obj00s[2]), eval(obj00s[3]), eval(obj00s[4])],
                [eval(obj01s[0]), eval(obj01s[1]), eval(obj01s[2]), eval(obj01s[3]), eval(obj01s[4])]]
            self.bg_2 = [
                [eval(obj00s[5]), eval(obj00s[6]), eval(obj00s[7]), eval(obj00s[8]), eval(obj00s[9])],
                [eval(obj01s[5]), eval(obj01s[6]), eval(obj01s[7]), eval(obj01s[8]), eval(obj01s[9])]]
            self.bg_3 = [
                [eval(obj00s[10]), eval(obj00s[11]), eval(obj00s[12]), eval(obj00s[13]), eval(obj00s[14])],
                [eval(obj01s[10]), eval(obj01s[11]), eval(obj01s[12]), eval(obj01s[13]), eval(obj01s[14])]]
            self.dif_1 = [
                [eval(obj00s[15]), eval(obj00s[16]), eval(obj00s[17]), eval(obj00s[18]), eval(obj00s[19])],
                [eval(obj01s[15]), eval(obj01s[16]), eval(obj01s[17]), eval(obj01s[18]), eval(obj01s[19])]]
            self.dif_2 = [
                [eval(obj00s[20]), eval(obj00s[21]), eval(obj00s[22]), eval(obj00s[23]), eval(obj00s[24])],
                [eval(obj01s[20]), eval(obj01s[21]), eval(obj01s[22]), eval(obj01s[23]), eval(obj01s[24])]]
            self.dif_3 = [
                [eval(obj00s[25]), eval(obj00s[26]), eval(obj00s[27]), eval(obj00s[28]), eval(obj00s[29])],
                [eval(obj01s[25]), eval(obj01s[26]), eval(obj01s[27]), eval(obj01s[28]), eval(obj01s[29])]]
            self.dif_4 = [
                [eval(obj00s[30]), eval(obj00s[31]), eval(obj00s[32]), eval(obj00s[33]), eval(obj00s[34])],
                [eval(obj01s[30]), eval(obj01s[31]), eval(obj01s[32]), eval(obj01s[33]), eval(obj01s[34])]]
            self.dif_5 = [
                [eval(obj00s[35]), eval(obj00s[36]), eval(obj00s[37]), eval(obj00s[38]), eval(obj00s[39])],
                [eval(obj01s[35]), eval(obj01s[36]), eval(obj01s[37]), eval(obj01s[38]), eval(obj01s[39])]]
            self.dif_6 = [
                [eval(obj00s[40]), eval(obj00s[41]), eval(obj00s[42]), eval(obj00s[43]), eval(obj00s[44])],
                [eval(obj01s[40]), eval(obj01s[41]), eval(obj01s[42]), eval(obj01s[43]), eval(obj01s[44])]]
            self.fg_1 = [
                [eval(obj00s[45]), eval(obj00s[46]), eval(obj00s[47]), eval(obj00s[48]), eval(obj00s[49])],
                [eval(obj01s[45]), eval(obj01s[46]), eval(obj01s[47]), eval(obj01s[48]), eval(obj01s[49])]]
            self.fg_2 = [
                [eval(obj00s[50]), eval(obj00s[51]), eval(obj00s[52]), eval(obj00s[53]), eval(obj00s[54])],
                [eval(obj01s[50]), eval(obj01s[51]), eval(obj01s[52]), eval(obj01s[53]), eval(obj01s[54])]]
            self.fg_3 = [
                [eval(obj00s[55]), eval(obj00s[56]), eval(obj00s[57]), eval(obj00s[58]), eval(obj00s[59])],
                [eval(obj01s[55]), eval(obj01s[56]), eval(obj01s[57]), eval(obj01s[58]), eval(obj01s[59])]]
            # Verify Need to Render
            if (self.bg_1[0][0] == False and self.bg_2[0][0] == False and self.bg_3[0][0] == False and
            self.dif_1[0][0] == False and self.dif_2[0][0] == False and self.dif_3[0][0] == False and self.dif_4[0][0] == False and self.dif_5[0][0] == False and self.dif_6[0][0] == False and
            self.fg_1[0][0] == False and self.fg_2[0][0] == False and self.fg_3[0][0] == False):
                self.bg_1[0] = ["False", 0.5, 0.5, 0.5, 0]
                self.bg_2[0] = ["True", 0, 0, 0, 1]
                self.bg_3[0] = ["True", 0, 0, 0, 1]
                self.dif_1[0] = ["True", 35/255, 20/255, 2/255, 1]
                self.dif_2[0] = ["True", 84/255, 55/255, 19/255, 1]
                self.dif_3[0] = ["True", 254/255, 159/255, 14/255, 1]
                self.dif_4[0] = ["True", 255/255, 202/255, 50/255, 1]
                self.dif_5[0] = ["False", 0, 0, 0, 0]
                self.dif_6[0] = ["False", 0, 0, 0, 0]
                self.fg_1[0] = ["True", 0, 0, 0, 1]
                self.fg_2[0] = ["True", 255/255, 255/255, 150/255, 1]
                self.fg_3[0] = ["True", 1, 1, 1, 1]
            if (self.bg_1[1][0] == False and self.bg_2[1][0] == False and self.bg_3[1][0] == False and
            self.dif_1[1][0] == False and self.dif_2[1][0] == False and self.dif_3[1][0] == False and self.dif_4[1][0] == False and self.dif_5[1][0] == False and self.dif_6[1][0] == False and
            self.fg_1[1][0] == False and self.fg_2[1][0] == False and self.fg_3[1][0] == False):
                self.bg_1[1] = ["True", 0, 0, 0, 1]
                self.bg_2[1] = ["True", 0, 0, 0, 1]
                self.bg_3[1] = ["True", 0, 0, 0, 1]
                self.dif_1[1] = ["True", 0, 0, 0, 1]
                self.dif_2[1] = ["True", 0, 0, 0, 1]
                self.dif_3[1] = ["True", 0, 0, 0, 1]
                self.dif_4[1] = ["True", 0, 0, 0, 1]
                self.dif_5[1] = ["True", 0, 0, 0, 1]
                self.dif_6[1] = ["True", 0, 0, 0, 1]
                self.fg_1[1] = ["True", 0, 0, 0, 1]
                self.fg_2[1] = ["True", 0, 0, 0, 1]
                self.fg_3[1] = ["True", 0, 0, 0, 1]
            # Save First Object
            self.OBJ_Geometry()
            self.OBJ_Save()
            self.OBJ_Alpha()
            # Layers Render Variables
            self.layer_01 = True
            self.layer_02 = True
            self.layer_03 = True
            self.layer_04 = True
            self.layer_05 = True
            self.layer_06 = True
            self.layer_07 = True
            self.layer_08 = True
            self.layer_09 = True
            self.layer_10 = True
            self.layer_11 = True
            self.layer_12 = True
        except:
            QtCore.qDebug("Load Error - Panel OBJ")
        #//
        #\\ SOF ################################################################
        try:
            tip_sof_string = Krita.instance().readSetting("Pigment.O", "tip_SOF", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            tip_sof_split = tip_sof_string.split(",")
            self.lock_size = float(tip_sof_split[0])
            self.lock_opacity = float(tip_sof_split[1])
            self.lock_flow = float(tip_sof_split[2])
            self.sof_1 = float(tip_sof_split[0])
            self.sof_2 = float(tip_sof_split[1])
            self.sof_3 = float(tip_sof_split[2])
            self.tip_00.Setup_SOF(self.lock_size, self.lock_opacity, self.lock_flow)
            self.SOF_1_APPLY(self.sof_1)
            self.SOF_2_APPLY(self.sof_2)
            self.SOF_3_APPLY(self.sof_3)
        except:
            QtCore.qDebug("Load Error - TIP SOF")
        #//
        #\\ TIP ################################################################
        try:
            cor_00_string = Krita.instance().readSetting("Pigment.O", "tip_cor_00", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_01_string = Krita.instance().readSetting("Pigment.O", "tip_cor_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_02_string = Krita.instance().readSetting("Pigment.O", "tip_cor_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_03_string = Krita.instance().readSetting("Pigment.O", "tip_cor_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_04_string = Krita.instance().readSetting("Pigment.O", "tip_cor_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_05_string = Krita.instance().readSetting("Pigment.O", "tip_cor_05", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_06_string = Krita.instance().readSetting("Pigment.O", "tip_cor_06", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_07_string = Krita.instance().readSetting("Pigment.O", "tip_cor_07", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_08_string = Krita.instance().readSetting("Pigment.O", "tip_cor_08", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_09_string = Krita.instance().readSetting("Pigment.O", "tip_cor_09", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_10_string = Krita.instance().readSetting("Pigment.O", "tip_cor_10", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            cor_00_split = cor_00_string.split(",")
            cor_01_split = cor_01_string.split(",")
            cor_02_split = cor_02_string.split(",")
            cor_03_split = cor_03_string.split(",")
            cor_04_split = cor_04_string.split(",")
            cor_05_split = cor_05_string.split(",")
            cor_06_split = cor_06_string.split(",")
            cor_07_split = cor_07_string.split(",")
            cor_08_split = cor_08_string.split(",")
            cor_09_split = cor_09_string.split(",")
            cor_10_split = cor_10_string.split(",")
            if cor_00_split[0] == "True":
                self.cor_00 = ["True", float(cor_00_split[1]), float(cor_00_split[2]), float(cor_00_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_00[1]*255, self.cor_00[2]*255, self.cor_00[3]*255))
                self.layout.cor_00.setStyleSheet(color)
            if cor_01_split[0] == "True":
                self.cor_01 = ["True", float(cor_01_split[1]), float(cor_01_split[2]), float(cor_01_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_01[1]*255, self.cor_01[2]*255, self.cor_01[3]*255))
                self.layout.cor_01.setStyleSheet(color)
            if cor_02_split[0] == "True":
                self.cor_02 = ["True", float(cor_02_split[1]), float(cor_02_split[2]), float(cor_02_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_02[1]*255, self.cor_02[2]*255, self.cor_02[3]*255))
                self.layout.cor_02.setStyleSheet(color)
            if cor_03_split[0] == "True":
                self.cor_03 = ["True", float(cor_03_split[1]), float(cor_03_split[2]), float(cor_03_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_03[1]*255, self.cor_03[2]*255, self.cor_03[3]*255))
                self.layout.cor_03.setStyleSheet(color)
            if cor_04_split[0] == "True":
                self.cor_04 = ["True", float(cor_04_split[1]), float(cor_04_split[2]), float(cor_04_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_04[1]*255, self.cor_04[2]*255, self.cor_04[3]*255))
                self.layout.cor_04.setStyleSheet(color)
            if cor_05_split[0] == "True":
                self.cor_05 = ["True", float(cor_05_split[1]), float(cor_05_split[2]), float(cor_05_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_05[1]*255, self.cor_05[2]*255, self.cor_05[3]*255))
                self.layout.cor_05.setStyleSheet(color)
            if cor_06_split[0] == "True":
                self.cor_06 = ["True", float(cor_06_split[1]), float(cor_06_split[2]), float(cor_06_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_06[1]*255, self.cor_06[2]*255, self.cor_06[3]*255))
                self.layout.cor_06.setStyleSheet(color)
            if cor_07_split[0] == "True":
                self.cor_07 = ["True", float(cor_07_split[1]), float(cor_07_split[2]), float(cor_07_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_07[1]*255, self.cor_07[2]*255, self.cor_07[3]*255))
                self.layout.cor_07.setStyleSheet(color)
            if cor_08_split[0] == "True":
                self.cor_08 = ["True", float(cor_08_split[1]), float(cor_08_split[2]), float(cor_08_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_08[1]*255, self.cor_08[2]*255, self.cor_08[3]*255))
                self.layout.cor_08.setStyleSheet(color)
            if cor_09_split[0] == "True":
                self.cor_09 = ["True", float(cor_09_split[1]), float(cor_09_split[2]), float(cor_09_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_09[1]*255, self.cor_09[2]*255, self.cor_09[3]*255))
                self.layout.cor_09.setStyleSheet(color)
            if cor_10_split[0] == "True":
                self.cor_10 = ["True", float(cor_10_split[1]), float(cor_10_split[2]), float(cor_10_split[3])]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.cor_10[1]*255, self.cor_10[2]*255, self.cor_10[3]*255))
                self.layout.cor_10.setStyleSheet(color)
        except:
            QtCore.qDebug("Load Error - TIP Palette")

        #//
        #\\ Mixer TTS ##########################################################
        try:
            mixer_tts_string = Krita.instance().readSetting("Pigment.O", "mix_TTS", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_tts_split = mixer_tts_string.split(",")
            if mixer_tts_split[0] == "True":
                self.color_tts = ["True", float(mixer_tts_split[1]), float(mixer_tts_split[2]), float(mixer_tts_split[3])]
                gray = self.rgb_to_aaa(self.color_tts[1], self.color_tts[2], self.color_tts[3])
                self.gray_tts = [gray[0], gray[0], gray[0]]
                color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_tts[1]*255, self.color_tts[2]*255, self.color_tts[3]*255))
                bg_gray_tts = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ; " % (self.gray_tts[0]*255, self.gray_tts[1]*255, self.gray_tts[2]*255))
                self.layout.tts_l1.setStyleSheet(color)
                self.layout.white.setStyleSheet(bg_white)
                self.layout.grey.setStyleSheet(bg_gray_tts)
                self.layout.black.setStyleSheet(bg_black)
        except:
            QtCore.qDebug("Load Error - Mixer TTS")
        #//
        #\\ Mixer RGB ##########################################################
        try:
            # Mixer RGB 1
            mixer_rgb_1_string = Krita.instance().readSetting("Pigment.O", "mix_RGB_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_rgb_1_split = mixer_rgb_1_string.split(",")
            if (mixer_rgb_1_split[0] == "True" and mixer_rgb_1_split[4] == "True"):
                # Gradient
                self.color_rgb_l1 = ["True", float(mixer_rgb_1_split[1]), float(mixer_rgb_1_split[2]), float(mixer_rgb_1_split[3])]
                self.color_rgb_r1 = ["True", float(mixer_rgb_1_split[5]), float(mixer_rgb_1_split[6]), float(mixer_rgb_1_split[7])]
                color_rgb_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*255, self.color_rgb_l1[2]*255, self.color_rgb_l1[3]*255))
                color_rgb_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*255, self.color_rgb_r1[2]*255, self.color_rgb_r1[3]*255))
                self.layout.rgb_l1.setStyleSheet(color_rgb_left_1)
                self.layout.rgb_r1.setStyleSheet(color_rgb_right_1)
            elif (mixer_rgb_1_split[0] == "True" and mixer_rgb_1_split[4] != "True"):
                # Color Left
                self.color_rgb_l1 = ["True", float(mixer_rgb_1_split[1]), float(mixer_rgb_1_split[2]), float(mixer_rgb_1_split[3])]
                self.color_rgb_r1 = ["False", 0, 0, 0]
                color_rgb_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*255, self.color_rgb_l1[2]*255, self.color_rgb_l1[3]*255))
                self.layout.rgb_l1.setStyleSheet(color_rgb_left_1)
                self.layout.rgb_r1.setStyleSheet(bg_alpha)
            elif (mixer_rgb_1_split[0] != "True" and mixer_rgb_1_split[4] == "True"):
                # Color Right
                self.color_rgb_l1 = ["False", 0, 0, 0]
                self.color_rgb_r1 = ["True", float(mixer_rgb_1_split[5]), float(mixer_rgb_1_split[6]), float(mixer_rgb_1_split[7])]
                color_rgb_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*255, self.color_rgb_r1[2]*255, self.color_rgb_r1[3]*255))
                self.layout.rgb_l1.setStyleSheet(bg_alpha)
                self.layout.rgb_r1.setStyleSheet(color_rgb_right_1)
            # Mixer RGB 2
            mixer_rgb_2_string = Krita.instance().readSetting("Pigment.O", "mix_RGB_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_rgb_2_split = mixer_rgb_2_string.split(",")
            if (mixer_rgb_2_split[0] == "True" and mixer_rgb_2_split[4] == "True"):
                # Gradient
                self.color_rgb_l2 = ["True", float(mixer_rgb_2_split[1]), float(mixer_rgb_2_split[2]), float(mixer_rgb_2_split[3])]
                self.color_rgb_r2 = ["True", float(mixer_rgb_2_split[5]), float(mixer_rgb_2_split[6]), float(mixer_rgb_2_split[7])]
                color_rgb_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*255, self.color_rgb_l2[2]*255, self.color_rgb_l2[3]*255))
                color_rgb_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*255, self.color_rgb_r2[2]*255, self.color_rgb_r2[3]*255))
                self.layout.rgb_l2.setStyleSheet(color_rgb_left_2)
                self.layout.rgb_r2.setStyleSheet(color_rgb_right_2)
            elif (mixer_rgb_2_split[0] == "True" and mixer_rgb_2_split[4] != "True"):
                # Color Left
                self.color_rgb_l2 = ["True", float(mixer_rgb_2_split[1]), float(mixer_rgb_2_split[2]), float(mixer_rgb_2_split[3])]
                self.color_rgb_r2 = ["False", 0, 0, 0]
                color_rgb_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*255, self.color_rgb_l2[2]*255, self.color_rgb_l2[3]*255))
                self.layout.rgb_l2.setStyleSheet(color_rgb_left_2)
                self.layout.rgb_r2.setStyleSheet(bg_alpha)
            elif (mixer_rgb_2_split[0] != "True" and mixer_rgb_2_split[4] == "True"):
                # Color Right
                self.color_rgb_l2 = ["False", 0, 0, 0]
                self.color_rgb_r2 = ["True", float(mixer_rgb_2_split[5]), float(mixer_rgb_2_split[6]), float(mixer_rgb_2_split[7])]
                color_rgb_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*255, self.color_rgb_r2[2]*255, self.color_rgb_r2[3]*255))
                self.layout.rgb_l2.setStyleSheet(bg_alpha)
                self.layout.rgb_r2.setStyleSheet(color_rgb_right_2)
            # Mixer RGB 3
            mixer_rgb_3_string = Krita.instance().readSetting("Pigment.O", "mix_RGB_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_rgb_3_split = mixer_rgb_3_string.split(",")
            if (mixer_rgb_3_split[0] == "True" and mixer_rgb_3_split[4] == "True"):
                # Gradient
                self.color_rgb_l3 = ["True", float(mixer_rgb_3_split[1]), float(mixer_rgb_3_split[2]), float(mixer_rgb_3_split[3])]
                self.color_rgb_r3 = ["True", float(mixer_rgb_3_split[5]), float(mixer_rgb_3_split[6]), float(mixer_rgb_3_split[7])]
                color_rgb_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*255, self.color_rgb_l3[2]*255, self.color_rgb_l3[3]*255))
                color_rgb_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*255, self.color_rgb_r3[2]*255, self.color_rgb_r3[3]*255))
                self.layout.rgb_l3.setStyleSheet(color_rgb_left_3)
                self.layout.rgb_r3.setStyleSheet(color_rgb_right_3)
            elif (mixer_rgb_3_split[0] == "True" and mixer_rgb_3_split[4] != "True"):
                # Color Left
                self.color_rgb_l3 = ["True", float(mixer_rgb_3_split[1]), float(mixer_rgb_3_split[2]), float(mixer_rgb_3_split[3])]
                self.color_rgb_r3 = ["False", 0, 0, 0]
                color_rgb_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*255, self.color_rgb_l3[2]*255, self.color_rgb_l3[3]*255))
                self.layout.rgb_l3.setStyleSheet(color_rgb_left_3)
                self.layout.rgb_r3.setStyleSheet(bg_alpha)
            elif (mixer_rgb_3_split[0] != "True" and mixer_rgb_3_split[4] == "True"):
                # Color Right
                self.color_rgb_l3 = ["False", 0, 0, 0]
                self.color_rgb_r3 = ["True", float(mixer_rgb_3_split[5]), float(mixer_rgb_3_split[6]), float(mixer_rgb_3_split[7])]
                color_rgb_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*255, self.color_rgb_r3[2]*255, self.color_rgb_r3[3]*255))
                self.layout.rgb_l3.setStyleSheet(bg_alpha)
                self.layout.rgb_r3.setStyleSheet(color_rgb_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer RGB")
        #//
        #\\ Mixer ARD ##########################################################
        try:
            # Mixer ARD 1
            mixer_ard_1_string = Krita.instance().readSetting("Pigment.O", "mix_ARD_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_ard_1_split = mixer_ard_1_string.split(",")
            if (mixer_ard_1_split[0] == "True" and mixer_ard_1_split[4] == "True"):
                # Gradient
                self.color_ard_l1 = ["True", float(mixer_ard_1_split[1]), float(mixer_ard_1_split[2]), float(mixer_ard_1_split[3])]
                self.color_ard_r1 = ["True", float(mixer_ard_1_split[5]), float(mixer_ard_1_split[6]), float(mixer_ard_1_split[7])]
                rgb_ard_l1 = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
                rgb_ard_r1 = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
                color_ard_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l1[0]*255, rgb_ard_l1[1]*255, rgb_ard_l1[2]*255))
                color_ard_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r1[0]*255, rgb_ard_r1[1]*255, rgb_ard_r1[2]*255))
                self.layout.ard_l1.setStyleSheet(color_ard_left_1)
                self.layout.ard_r1.setStyleSheet(color_ard_right_1)
            elif (mixer_ard_1_split[0] == "True" and mixer_ard_1_split[4] != "True"):
                # Color Left
                self.color_ard_l1 = ["True", float(mixer_ard_1_split[1]), float(mixer_ard_1_split[2]), float(mixer_ard_1_split[3])]
                self.color_ard_r1 = ["False", 0, 0, 0]
                rgb_ard_l1 = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
                color_ard_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l1[0]*255, rgb_ard_l1[1]*255, rgb_ard_l1[2]*255))
                self.layout.ard_l1.setStyleSheet(color_ard_left_1)
                self.layout.ard_r1.setStyleSheet(bg_alpha)
            elif (mixer_ard_1_split[0] != "True" and mixer_ard_1_split[4] == "True"):
                # Color Right
                self.color_ard_l1 = ["False", 0, 0, 0]
                self.color_ard_r1 = ["True", float(mixer_ard_1_split[5]), float(mixer_ard_1_split[6]), float(mixer_ard_1_split[7])]
                rgb_ard_r1 = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])
                color_ard_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r1[0]*255, rgb_ard_r1[1]*255, rgb_ard_r1[2]*255))
                self.layout.ard_l1.setStyleSheet(bg_alpha)
                self.layout.ard_r1.setStyleSheet(color_ard_right_1)
            # Mixer ARD 2
            mixer_ard_2_string = Krita.instance().readSetting("Pigment.O", "mix_ARD_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_ard_2_split = mixer_ard_2_string.split(",")
            if (mixer_ard_2_split[0] == "True" and mixer_ard_2_split[4] == "True"):
                # Gradient
                self.color_ard_l2 = ["True", float(mixer_ard_2_split[1]), float(mixer_ard_2_split[2]), float(mixer_ard_2_split[3])]
                self.color_ard_r2 = ["True", float(mixer_ard_2_split[5]), float(mixer_ard_2_split[6]), float(mixer_ard_2_split[7])]
                rgb_ard_l2 = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
                rgb_ard_r2 = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
                color_ard_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l2[0]*255, rgb_ard_l2[1]*255, rgb_ard_l2[2]*255))
                color_ard_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r2[0]*255, rgb_ard_r2[1]*255, rgb_ard_r2[2]*255))
                self.layout.ard_l2.setStyleSheet(color_ard_left_2)
                self.layout.ard_r2.setStyleSheet(color_ard_right_2)
            elif (mixer_ard_2_split[0] == "True" and mixer_ard_2_split[4] != "True"):
                # Color Left
                self.color_ard_l2 = ["True", float(mixer_ard_2_split[1]), float(mixer_ard_2_split[2]), float(mixer_ard_2_split[3])]
                self.color_ard_r2 = ["False", 0, 0, 0]
                rgb_ard_l2 = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
                color_ard_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l2[0]*255, rgb_ard_l2[1]*255, rgb_ard_l2[2]*255))
                self.layout.ard_l2.setStyleSheet(color_ard_left_2)
                self.layout.ard_r2.setStyleSheet(bg_alpha)
            elif (mixer_ard_2_split[0] != "True" and mixer_ard_2_split[4] == "True"):
                # Color Right
                self.color_ard_l2 = ["False", 0, 0, 0]
                self.color_ard_r2 = ["True", float(mixer_ard_2_split[5]), float(mixer_ard_2_split[6]), float(mixer_ard_2_split[7])]
                rgb_ard_r2 = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
                color_ard_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r2[0]*255, rgb_ard_r2[1]*255, rgb_ard_r2[2]*255))
                self.layout.ard_l2.setStyleSheet(bg_alpha)
                self.layout.ard_r2.setStyleSheet(color_ard_right_2)
            # Mixer ARD 3
            mixer_ard_3_string = Krita.instance().readSetting("Pigment.O", "mix_ARD_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_ard_3_split = mixer_ard_3_string.split(",")
            if (mixer_ard_3_split[0] == "True" and mixer_ard_3_split[4] == "True"):
                # Gradient
                self.color_ard_l3 = ["True", float(mixer_ard_3_split[1]), float(mixer_ard_3_split[2]), float(mixer_ard_3_split[3])]
                self.color_ard_r3 = ["True", float(mixer_ard_3_split[5]), float(mixer_ard_3_split[6]), float(mixer_ard_3_split[7])]
                rgb_ard_l3 = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
                rgb_ard_r3 = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
                color_ard_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l3[0]*255, rgb_ard_l3[1]*255, rgb_ard_l3[2]*255))
                color_ard_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r3[0]*255, rgb_ard_r3[1]*255, rgb_ard_r3[2]*255))
                self.layout.ard_l3.setStyleSheet(color_ard_left_3)
                self.layout.ard_r3.setStyleSheet(color_ard_right_3)
            elif (mixer_ard_3_split[0] == "True" and mixer_ard_3_split[4] != "True"):
                # Color Left
                self.color_ard_l3 = ["True", float(mixer_ard_3_split[1]), float(mixer_ard_3_split[2]), float(mixer_ard_3_split[3])]
                self.color_ard_r3 = ["False", 0, 0, 0]
                rgb_ard_l3 = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
                color_ard_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_l3[0]*255, rgb_ard_l3[1]*255, rgb_ard_l3[2]*255))
                self.layout.ard_l3.setStyleSheet(color_ard_left_3)
                self.layout.ard_r3.setStyleSheet(bg_alpha)
            elif (mixer_ard_3_split[0] != "True" and mixer_ard_3_split[4] == "True"):
                # Color Right
                self.color_ard_l3 = ["False", 0, 0, 0]
                self.color_ard_r3 = ["True", float(mixer_ard_3_split[5]), float(mixer_ard_3_split[6]), float(mixer_ard_3_split[7])]
                rgb_ard_r3 = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
                color_ard_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ard_r3[0]*255, rgb_ard_r3[1]*255, rgb_ard_r3[2]*255))
                self.layout.ard_l3.setStyleSheet(bg_alpha)
                self.layout.ard_r3.setStyleSheet(color_ard_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer ARD")
        #//
        #\\ Mixer HSV ##########################################################
        try:
            # Mixer HSV 1
            mixer_hsv_1_string = Krita.instance().readSetting("Pigment.O", "mix_HSV_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hsv_1_split = mixer_hsv_1_string.split(",")
            if (mixer_hsv_1_split[0] == "True" and mixer_hsv_1_split[4] == "True"):
                # Gradient
                self.color_hsv_l1 = ["True", float(mixer_hsv_1_split[1]), float(mixer_hsv_1_split[2]), float(mixer_hsv_1_split[3])]
                self.color_hsv_r1 = ["True", float(mixer_hsv_1_split[5]), float(mixer_hsv_1_split[6]), float(mixer_hsv_1_split[7])]
                rgb_hsv_l1 = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
                rgb_hsv_r1 = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
                color_hsv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l1[0]*255, rgb_hsv_l1[1]*255, rgb_hsv_l1[2]*255))
                color_hsv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r1[0]*255, rgb_hsv_r1[1]*255, rgb_hsv_r1[2]*255))
                self.layout.hsv_l1.setStyleSheet(color_hsv_left_1)
                self.layout.hsv_r1.setStyleSheet(color_hsv_right_1)
            elif (mixer_hsv_1_split[0] == "True" and mixer_hsv_1_split[4] != "True"):
                # Color Left
                self.color_hsv_l1 = ["True", float(mixer_hsv_1_split[1]), float(mixer_hsv_1_split[2]), float(mixer_hsv_1_split[3])]
                self.color_hsv_r1 = ["False", 0, 0, 0]
                rgb_hsv_l1 = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
                color_hsv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l1[0]*255, rgb_hsv_l1[1]*255, rgb_hsv_l1[2]*255))
                self.layout.hsv_l1.setStyleSheet(color_hsv_left_1)
                self.layout.hsv_r1.setStyleSheet(bg_alpha)
            elif (mixer_hsv_1_split[0] != "True" and mixer_hsv_1_split[4] == "True"):
                # Color Right
                self.color_hsv_l1 = ["False", 0, 0, 0]
                self.color_hsv_r1 = ["True", float(mixer_hsv_1_split[5]), float(mixer_hsv_1_split[6]), float(mixer_hsv_1_split[7])]
                rgb_hsv_r1 = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
                color_hsv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r1[0]*255, rgb_hsv_r1[1]*255, rgb_hsv_r1[2]*255))
                self.layout.hsv_l1.setStyleSheet(bg_alpha)
                self.layout.hsv_r1.setStyleSheet(color_hsv_right_1)
            # Mixer HSV 2
            mixer_hsv_2_string = Krita.instance().readSetting("Pigment.O", "mix_HSV_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hsv_2_split = mixer_hsv_2_string.split(",")
            if (mixer_hsv_2_split[0] == "True" and mixer_hsv_2_split[4] == "True"):
                # Gradient
                self.color_hsv_l2 = ["True", float(mixer_hsv_2_split[1]), float(mixer_hsv_2_split[2]), float(mixer_hsv_2_split[3])]
                self.color_hsv_r2 = ["True", float(mixer_hsv_2_split[5]), float(mixer_hsv_2_split[6]), float(mixer_hsv_2_split[7])]
                rgb_hsv_l2 = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
                rgb_hsv_r2 = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
                color_hsv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l2[0]*255, rgb_hsv_l2[1]*255, rgb_hsv_l2[2]*255))
                color_hsv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r2[0]*255, rgb_hsv_r2[1]*255, rgb_hsv_r2[2]*255))
                self.layout.hsv_l2.setStyleSheet(color_hsv_left_2)
                self.layout.hsv_r2.setStyleSheet(color_hsv_right_2)
            elif (mixer_hsv_2_split[0] == "True" and mixer_hsv_2_split[4] != "True"):
                # Color Left
                self.color_hsv_l2 = ["True", float(mixer_hsv_2_split[1]), float(mixer_hsv_2_split[2]), float(mixer_hsv_2_split[3])]
                self.color_hsv_r2 = ["False", 0, 0, 0]
                rgb_hsv_l2 = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
                color_hsv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l2[0]*255, rgb_hsv_l2[1]*255, rgb_hsv_l2[2]*255))
                self.layout.hsv_l2.setStyleSheet(color_hsv_left_2)
                self.layout.hsv_r2.setStyleSheet(bg_alpha)
            elif (mixer_hsv_2_split[0] != "True" and mixer_hsv_2_split[4] == "True"):
                # Color Right
                self.color_hsv_l2 = ["False", 0, 0, 0]
                self.color_hsv_r2 = ["True", float(mixer_hsv_2_split[5]), float(mixer_hsv_2_split[6]), float(mixer_hsv_2_split[7])]
                rgb_hsv_r2 = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
                color_hsv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r2[0]*255, rgb_hsv_r2[1]*255, rgb_hsv_r2[2]*255))
                self.layout.hsv_l2.setStyleSheet(bg_alpha)
                self.layout.hsv_r2.setStyleSheet(color_hsv_right_2)
            # Mixer HSV 3
            mixer_hsv_3_string = Krita.instance().readSetting("Pigment.O", "mix_HSV_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hsv_3_split = mixer_hsv_3_string.split(",")
            if (mixer_hsv_3_split[0] == "True" and mixer_hsv_3_split[4] == "True"):
                # Gradient
                self.color_hsv_l3 = ["True", float(mixer_hsv_3_split[1]), float(mixer_hsv_3_split[2]), float(mixer_hsv_3_split[3])]
                self.color_hsv_r3 = ["True", float(mixer_hsv_3_split[5]), float(mixer_hsv_3_split[6]), float(mixer_hsv_3_split[7])]
                rgb_hsv_l3 = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
                rgb_hsv_r3 = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
                color_hsv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l3[0]*255, rgb_hsv_l3[1]*255, rgb_hsv_l3[2]*255))
                color_hsv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r3[0]*255, rgb_hsv_r3[1]*255, rgb_hsv_r3[2]*255))
                self.layout.hsv_l3.setStyleSheet(color_hsv_left_3)
                self.layout.hsv_r3.setStyleSheet(color_hsv_right_3)
            elif (mixer_hsv_3_split[0] == "True" and mixer_hsv_3_split[4] != "True"):
                # Color Left
                self.color_hsv_l3 = ["True", float(mixer_hsv_3_split[1]), float(mixer_hsv_3_split[2]), float(mixer_hsv_3_split[3])]
                self.color_hsv_r3 = ["False", 0, 0, 0]
                rgb_hsv_l3 = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
                color_hsv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_l3[0]*255, rgb_hsv_l3[1]*255, rgb_hsv_l3[2]*255))
                self.layout.hsv_l3.setStyleSheet(color_hsv_left_3)
                self.layout.hsv_r3.setStyleSheet(bg_alpha)
            elif (mixer_hsv_3_split[0] != "True" and mixer_hsv_3_split[4] == "True"):
                # Color Right
                self.color_hsv_l3 = ["False", 0, 0, 0]
                self.color_hsv_r3 = ["True", float(mixer_hsv_3_split[5]), float(mixer_hsv_3_split[6]), float(mixer_hsv_3_split[7])]
                rgb_hsv_r3 = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
                color_hsv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsv_r3[0]*255, rgb_hsv_r3[1]*255, rgb_hsv_r3[2]*255))
                self.layout.hsv_l3.setStyleSheet(bg_alpha)
                self.layout.hsv_r3.setStyleSheet(color_hsv_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer HSV")
        #//
        #\\ Mixer HSL ##########################################################
        try:
            # Mixer HSL 1
            mixer_hsl_1_string = Krita.instance().readSetting("Pigment.O", "mix_HSL_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hsl_1_split = mixer_hsl_1_string.split(",")
            if (mixer_hsl_1_split[0] == "True" and mixer_hsl_1_split[4] == "True"):
                # Gradient
                self.color_hsl_l1 = ["True", float(mixer_hsl_1_split[1]), float(mixer_hsl_1_split[2]), float(mixer_hsl_1_split[3])]
                self.color_hsl_r1 = ["True", float(mixer_hsl_1_split[5]), float(mixer_hsl_1_split[6]), float(mixer_hsl_1_split[7])]
                rgb_hsl_l1 = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
                rgb_hsl_r1 = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
                color_hsl_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l1[0]*255, rgb_hsl_l1[1]*255, rgb_hsl_l1[2]*255))
                color_hsl_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r1[0]*255, rgb_hsl_r1[1]*255, rgb_hsl_r1[2]*255))
                self.layout.hsl_l1.setStyleSheet(color_hsl_left_1)
                self.layout.hsl_r1.setStyleSheet(color_hsl_right_1)
            elif (mixer_hsl_1_split[0] == "True" and mixer_hsl_1_split[4] != "True"):
                # Color Left
                self.color_hsl_l1 = ["True", float(mixer_hsl_1_split[1]), float(mixer_hsl_1_split[2]), float(mixer_hsl_1_split[3])]
                self.color_hsl_r1 = ["False", 0, 0, 0]
                rgb_hsl_l1 = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
                color_hsl_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l1[0]*255, rgb_hsl_l1[1]*255, rgb_hsl_l1[2]*255))
                self.layout.hsl_l1.setStyleSheet(color_hsl_left_1)
                self.layout.hsl_r1.setStyleSheet(bg_alpha)
            elif (mixer_hsl_1_split[0] != "True" and mixer_hsl_1_split[4] == "True"):
                # Color Right
                self.color_hsl_l1 = ["False", 0, 0, 0]
                self.color_hsl_r1 = ["True", float(mixer_hsl_1_split[5]), float(mixer_hsl_1_split[6]), float(mixer_hsl_1_split[7])]
                rgb_hsl_r1 = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
                color_hsl_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r1[0]*255, rgb_hsl_r1[1]*255, rgb_hsl_r1[2]*255))
                self.layout.hsl_l1.setStyleSheet(bg_alpha)
                self.layout.hsl_r1.setStyleSheet(color_hsl_right_1)
            # Mixer HSL 2
            mixer_hsl_2_string = Krita.instance().readSetting("Pigment.O", "mix_HSL_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hsl_2_split = mixer_hsl_2_string.split(",")
            if (mixer_hsl_2_split[0] == "True" and mixer_hsl_2_split[4] == "True"):
                # Gradient
                self.color_hsl_l2 = ["True", float(mixer_hsl_2_split[1]), float(mixer_hsl_2_split[2]), float(mixer_hsl_2_split[3])]
                self.color_hsl_r2 = ["True", float(mixer_hsl_2_split[5]), float(mixer_hsl_2_split[6]), float(mixer_hsl_2_split[7])]
                rgb_hsl_l2 = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
                rgb_hsl_r2 = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
                color_hsl_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l2[0]*255, rgb_hsl_l2[1]*255, rgb_hsl_l2[2]*255))
                color_hsl_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r2[0]*255, rgb_hsl_r2[1]*255, rgb_hsl_r2[2]*255))
                self.layout.hsl_l2.setStyleSheet(color_hsl_left_2)
                self.layout.hsl_r2.setStyleSheet(color_hsl_right_2)
            elif (mixer_hsl_2_split[0] == "True" and mixer_hsl_2_split[4] != "True"):
                # Color Left
                self.color_hsl_l2 = ["True", float(mixer_hsl_2_split[1]), float(mixer_hsl_2_split[2]), float(mixer_hsl_2_split[3])]
                self.color_hsl_r2 = ["False", 0, 0, 0]
                rgb_hsl_l2 = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
                color_hsl_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l2[0]*255, rgb_hsl_l2[1]*255, rgb_hsl_l2[2]*255))
                self.layout.hsl_l2.setStyleSheet(color_hsl_left_2)
                self.layout.hsl_r2.setStyleSheet(bg_alpha)
            elif (mixer_hsl_2_split[0] != "True" and mixer_hsl_2_split[4] == "True"):
                # Color Right
                self.color_hsl_l2 = ["False", 0, 0, 0]
                self.color_hsl_r2 = ["True", float(mixer_hsl_2_split[5]), float(mixer_hsl_2_split[6]), float(mixer_hsl_2_split[7])]
                rgb_hsl_r2 = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
                color_hsl_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r2[0]*255, rgb_hsl_r2[1]*255, rgb_hsl_r2[2]*255))
                self.layout.hsl_l2.setStyleSheet(bg_alpha)
                self.layout.hsl_r2.setStyleSheet(color_hsl_right_2)
            # Mixer HSL 3
            mixer_hsl_3_string = Krita.instance().readSetting("Pigment.O", "mix_HSL_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hsl_3_split = mixer_hsl_3_string.split(",")
            if (mixer_hsl_3_split[0] == "True" and mixer_hsl_3_split[4] == "True"):
                # Gradient
                self.color_hsl_l3 = ["True", float(mixer_hsl_3_split[1]), float(mixer_hsl_3_split[2]), float(mixer_hsl_3_split[3])]
                self.color_hsl_r3 = ["True", float(mixer_hsl_3_split[5]), float(mixer_hsl_3_split[6]), float(mixer_hsl_3_split[7])]
                rgb_hsl_l3 = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
                rgb_hsl_r3 = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
                color_hsl_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l3[0]*255, rgb_hsl_l3[1]*255, rgb_hsl_l3[2]*255))
                color_hsl_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r3[0]*255, rgb_hsl_r3[1]*255, rgb_hsl_r3[2]*255))
                self.layout.hsl_l3.setStyleSheet(color_hsl_left_3)
                self.layout.hsl_r3.setStyleSheet(color_hsl_right_3)
            elif (mixer_hsl_3_split[0] == "True" and mixer_hsl_3_split[4] != "True"):
                # Color Left
                self.color_hsl_l3 = ["True", float(mixer_hsl_3_split[1]), float(mixer_hsl_3_split[2]), float(mixer_hsl_3_split[3])]
                self.color_hsl_r3 = ["False", 0, 0, 0]
                rgb_hsl_l3 = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
                color_hsl_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_l3[0]*255, rgb_hsl_l3[1]*255, rgb_hsl_l3[2]*255))
                self.layout.hsl_l3.setStyleSheet(color_hsl_left_3)
                self.layout.hsl_r3.setStyleSheet(bg_alpha)
            elif (mixer_hsl_3_split[0] != "True" and mixer_hsl_3_split[4] == "True"):
                # Color Right
                self.color_hsl_l3 = ["False", 0, 0, 0]
                self.color_hsl_r3 = ["True", float(mixer_hsl_3_split[5]), float(mixer_hsl_3_split[6]), float(mixer_hsl_3_split[7])]
                rgb_hsl_r3 = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
                color_hsl_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hsl_r3[0]*255, rgb_hsl_r3[1]*255, rgb_hsl_r3[2]*255))
                self.layout.hsl_l3.setStyleSheet(bg_alpha)
                self.layout.hsl_r3.setStyleSheet(color_hsl_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer HSL")
        #//
        #\\ Mixer HCY ##########################################################
        try:
            # Mixer HCY 1
            mixer_hcy_1_string = Krita.instance().readSetting("Pigment.O", "mix_HCY_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hcy_1_split = mixer_hcy_1_string.split(",")
            if (mixer_hcy_1_split[0] == "True" and mixer_hcy_1_split[4] == "True"):
                # Gradient
                self.color_hcy_l1 = ["True", float(mixer_hcy_1_split[1]), float(mixer_hcy_1_split[2]), float(mixer_hcy_1_split[3])]
                self.color_hcy_r1 = ["True", float(mixer_hcy_1_split[5]), float(mixer_hcy_1_split[6]), float(mixer_hcy_1_split[7])]
                rgb_hcy_l1 = self.hcy_to_rgb(self.color_hcy_l1[1], self.color_hcy_l1[2], self.color_hcy_l1[3])
                rgb_hcy_r1 = self.hcy_to_rgb(self.color_hcy_r1[1], self.color_hcy_r1[2], self.color_hcy_r1[3])
                color_hcy_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_l1[0]*255, rgb_hcy_l1[1]*255, rgb_hcy_l1[2]*255))
                color_hcy_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_r1[0]*255, rgb_hcy_r1[1]*255, rgb_hcy_r1[2]*255))
                self.layout.hcy_l1.setStyleSheet(color_hcy_left_1)
                self.layout.hcy_r1.setStyleSheet(color_hcy_right_1)
            elif (mixer_hcy_1_split[0] == "True" and mixer_hcy_1_split[4] != "True"):
                # Color Left
                self.color_hcy_l1 = ["True", float(mixer_hcy_1_split[1]), float(mixer_hcy_1_split[2]), float(mixer_hcy_1_split[3])]
                self.color_hcy_r1 = ["False", 0, 0, 0]
                rgb_hcy_l1 = self.hcy_to_rgb(self.color_hcy_l1[1], self.color_hcy_l1[2], self.color_hcy_l1[3])
                color_hcy_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_l1[0]*255, rgb_hcy_l1[1]*255, rgb_hcy_l1[2]*255))
                self.layout.hcy_l1.setStyleSheet(color_hcy_left_1)
                self.layout.hcy_r1.setStyleSheet(bg_alpha)
            elif (mixer_hcy_1_split[0] != "True" and mixer_hcy_1_split[4] == "True"):
                # Color Right
                self.color_hcy_l1 = ["False", 0, 0, 0]
                self.color_hcy_r1 = ["True", float(mixer_hcy_1_split[5]), float(mixer_hcy_1_split[6]), float(mixer_hcy_1_split[7])]
                rgb_hcy_r1 = self.hcy_to_rgb(self.color_hcy_r1[1], self.color_hcy_r1[2], self.color_hcy_r1[3])
                color_hcy_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_r1[0]*255, rgb_hcy_r1[1]*255, rgb_hcy_r1[2]*255))
                self.layout.hcy_l1.setStyleSheet(bg_alpha)
                self.layout.hcy_r1.setStyleSheet(color_hcy_right_1)
            # Mixer HCY 2
            mixer_hcy_2_string = Krita.instance().readSetting("Pigment.O", "mix_HCY_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hcy_2_split = mixer_hcy_2_string.split(",")
            if (mixer_hcy_2_split[0] == "True" and mixer_hcy_2_split[4] == "True"):
                # Gradient
                self.color_hcy_l2 = ["True", float(mixer_hcy_2_split[1]), float(mixer_hcy_2_split[2]), float(mixer_hcy_2_split[3])]
                self.color_hcy_r2 = ["True", float(mixer_hcy_2_split[5]), float(mixer_hcy_2_split[6]), float(mixer_hcy_2_split[7])]
                rgb_hcy_l2 = self.hcy_to_rgb(self.color_hcy_l2[1], self.color_hcy_l2[2], self.color_hcy_l2[3])
                rgb_hcy_r2 = self.hcy_to_rgb(self.color_hcy_r2[1], self.color_hcy_r2[2], self.color_hcy_r2[3])
                color_hcy_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_l2[0]*255, rgb_hcy_l2[1]*255, rgb_hcy_l2[2]*255))
                color_hcy_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_r2[0]*255, rgb_hcy_r2[1]*255, rgb_hcy_r2[2]*255))
                self.layout.hcy_l2.setStyleSheet(color_hcy_left_2)
                self.layout.hcy_r2.setStyleSheet(color_hcy_right_2)
            elif (mixer_hcy_2_split[0] == "True" and mixer_hcy_2_split[4] != "True"):
                # Color Left
                self.color_hcy_l2 = ["True", float(mixer_hcy_2_split[1]), float(mixer_hcy_2_split[2]), float(mixer_hcy_2_split[3])]
                self.color_hcy_r2 = ["False", 0, 0, 0]
                rgb_hcy_l2 = self.hcy_to_rgb(self.color_hcy_l2[1], self.color_hcy_l2[2], self.color_hcy_l2[3])
                color_hcy_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_l2[0]*255, rgb_hcy_l2[1]*255, rgb_hcy_l2[2]*255))
                self.layout.hcy_l2.setStyleSheet(color_hcy_left_2)
                self.layout.hcy_r2.setStyleSheet(bg_alpha)
            elif (mixer_hcy_2_split[0] != "True" and mixer_hcy_2_split[4] == "True"):
                # Color Right
                self.color_hcy_l2 = ["False", 0, 0, 0]
                self.color_hcy_r2 = ["True", float(mixer_hcy_2_split[5]), float(mixer_hcy_2_split[6]), float(mixer_hcy_2_split[7])]
                rgb_hcy_r2 = self.hcy_to_rgb(self.color_hcy_r2[1], self.color_hcy_r2[2], self.color_hcy_r2[3])
                color_hcy_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_r2[0]*255, rgb_hcy_r2[1]*255, rgb_hcy_r2[2]*255))
                self.layout.hcy_l2.setStyleSheet(bg_alpha)
                self.layout.hcy_r2.setStyleSheet(color_hcy_right_2)
            # Mixer HCY 3
            mixer_hcy_3_string = Krita.instance().readSetting("Pigment.O", "mix_HCY_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_hcy_3_split = mixer_hcy_3_string.split(",")
            if (mixer_hcy_3_split[0] == "True" and mixer_hcy_3_split[4] == "True"):
                # Gradient
                self.color_hcy_l3 = ["True", float(mixer_hcy_3_split[1]), float(mixer_hcy_3_split[2]), float(mixer_hcy_3_split[3])]
                self.color_hcy_r3 = ["True", float(mixer_hcy_3_split[5]), float(mixer_hcy_3_split[6]), float(mixer_hcy_3_split[7])]
                rgb_hcy_l3 = self.hcy_to_rgb(self.color_hcy_l3[1], self.color_hcy_l3[2], self.color_hcy_l3[3])
                rgb_hcy_r3 = self.hcy_to_rgb(self.color_hcy_r3[1], self.color_hcy_r3[2], self.color_hcy_r3[3])
                color_hcy_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_l3[0]*255, rgb_hcy_l3[1]*255, rgb_hcy_l3[2]*255))
                color_hcy_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_r3[0]*255, rgb_hcy_r3[1]*255, rgb_hcy_r3[2]*255))
                self.layout.hcy_l3.setStyleSheet(color_hcy_left_3)
                self.layout.hcy_r3.setStyleSheet(color_hcy_right_3)
            elif (mixer_hcy_3_split[0] == "True" and mixer_hcy_3_split[4] != "True"):
                # Color Left
                self.color_hcy_l3 = ["True", float(mixer_hcy_3_split[1]), float(mixer_hcy_3_split[2]), float(mixer_hcy_3_split[3])]
                self.color_hcy_r3 = ["False", 0, 0, 0]
                rgb_hcy_l3 = self.hcy_to_rgb(self.color_hcy_l3[1], self.color_hcy_l3[2], self.color_hcy_l3[3])
                color_hcy_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_l3[0]*255, rgb_hcy_l3[1]*255, rgb_hcy_l3[2]*255))
                self.layout.hcy_l3.setStyleSheet(color_hcy_left_3)
                self.layout.hcy_r3.setStyleSheet(bg_alpha)
            elif (mixer_hcy_3_split[0] != "True" and mixer_hcy_3_split[4] == "True"):
                # Color Right
                self.color_hcy_l3 = ["False", 0, 0, 0]
                self.color_hcy_r3 = ["True", float(mixer_hcy_3_split[5]), float(mixer_hcy_3_split[6]), float(mixer_hcy_3_split[7])]
                rgb_hcy_r3 = self.hcy_to_rgb(self.color_hcy_r3[1], self.color_hcy_r3[2], self.color_hcy_r3[3])
                color_hcy_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_hcy_r3[0]*255, rgb_hcy_r3[1]*255, rgb_hcy_r3[2]*255))
                self.layout.hcy_l3.setStyleSheet(bg_alpha)
                self.layout.hcy_r3.setStyleSheet(color_hcy_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer HCY")
        #//
        #\\ Mixer YUV ##########################################################
        try:
            # Mixer YUV 1
            mixer_yuv_1_string = Krita.instance().readSetting("Pigment.O", "mix_YUV_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_yuv_1_split = mixer_yuv_1_string.split(",")
            if (mixer_yuv_1_split[0] == "True" and mixer_yuv_1_split[4] == "True"):
                # Gradient
                self.color_yuv_l1 = ["True", float(mixer_yuv_1_split[1]), float(mixer_yuv_1_split[2]), float(mixer_yuv_1_split[3])]
                self.color_yuv_r1 = ["True", float(mixer_yuv_1_split[5]), float(mixer_yuv_1_split[6]), float(mixer_yuv_1_split[7])]
                rgb_yuv_l1 = self.yuv_to_rgb(self.color_yuv_l1[1], self.color_yuv_l1[2], self.color_yuv_l1[3])
                rgb_yuv_r1 = self.yuv_to_rgb(self.color_yuv_r1[1], self.color_yuv_r1[2], self.color_yuv_r1[3])
                color_yuv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_l1[0]*255, rgb_yuv_l1[1]*255, rgb_yuv_l1[2]*255))
                color_yuv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_r1[0]*255, rgb_yuv_r1[1]*255, rgb_yuv_r1[2]*255))
                self.layout.yuv_l1.setStyleSheet(color_yuv_left_1)
                self.layout.yuv_r1.setStyleSheet(color_yuv_right_1)
            elif (mixer_yuv_1_split[0] == "True" and mixer_yuv_1_split[4] != "True"):
                # Color Left
                self.color_yuv_l1 = ["True", float(mixer_yuv_1_split[1]), float(mixer_yuv_1_split[2]), float(mixer_yuv_1_split[3])]
                self.color_yuv_r1 = ["False", 0, 0, 0]
                rgb_yuv_l1 = self.yuv_to_rgb(self.color_yuv_l1[1], self.color_yuv_l1[2], self.color_yuv_l1[3])
                color_yuv_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_l1[0]*255, rgb_yuv_l1[1]*255, rgb_yuv_l1[2]*255))
                self.layout.yuv_l1.setStyleSheet(color_yuv_left_1)
                self.layout.yuv_r1.setStyleSheet(bg_alpha)
            elif (mixer_yuv_1_split[0] != "True" and mixer_yuv_1_split[4] == "True"):
                # Color Right
                self.color_yuv_l1 = ["False", 0, 0, 0]
                self.color_yuv_r1 = ["True", float(mixer_yuv_1_split[5]), float(mixer_yuv_1_split[6]), float(mixer_yuv_1_split[7])]
                rgb_yuv_r1 = self.yuv_to_rgb(self.color_yuv_r1[1], self.color_yuv_r1[2], self.color_yuv_r1[3])
                color_yuv_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_r1[0]*255, rgb_yuv_r1[1]*255, rgb_yuv_r1[2]*255))
                self.layout.yuv_l1.setStyleSheet(bg_alpha)
                self.layout.yuv_r1.setStyleSheet(color_yuv_right_1)
            # Mixer YUV 2
            mixer_yuv_2_string = Krita.instance().readSetting("Pigment.O", "mix_YUV_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_yuv_2_split = mixer_yuv_2_string.split(",")
            if (mixer_yuv_2_split[0] == "True" and mixer_yuv_2_split[4] == "True"):
                # Gradient
                self.color_yuv_l2 = ["True", float(mixer_yuv_2_split[1]), float(mixer_yuv_2_split[2]), float(mixer_yuv_2_split[3])]
                self.color_yuv_r2 = ["True", float(mixer_yuv_2_split[5]), float(mixer_yuv_2_split[6]), float(mixer_yuv_2_split[7])]
                rgb_yuv_l2 = self.yuv_to_rgb(self.color_yuv_l2[1], self.color_yuv_l2[2], self.color_yuv_l2[3])
                rgb_yuv_r2 = self.yuv_to_rgb(self.color_yuv_r2[1], self.color_yuv_r2[2], self.color_yuv_r2[3])
                color_yuv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_l2[0]*255, rgb_yuv_l2[1]*255, rgb_yuv_l2[2]*255))
                color_yuv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_r2[0]*255, rgb_yuv_r2[1]*255, rgb_yuv_r2[2]*255))
                self.layout.yuv_l2.setStyleSheet(color_yuv_left_2)
                self.layout.yuv_r2.setStyleSheet(color_yuv_right_2)
            elif (mixer_yuv_2_split[0] == "True" and mixer_yuv_2_split[4] != "True"):
                # Color Left
                self.color_yuv_l2 = ["True", float(mixer_yuv_2_split[1]), float(mixer_yuv_2_split[2]), float(mixer_yuv_2_split[3])]
                self.color_yuv_r2 = ["False", 0, 0, 0]
                rgb_yuv_l2 = self.yuv_to_rgb(self.color_yuv_l2[1], self.color_yuv_l2[2], self.color_yuv_l2[3])
                color_yuv_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_l2[0]*255, rgb_yuv_l2[1]*255, rgb_yuv_l2[2]*255))
                self.layout.yuv_l2.setStyleSheet(color_yuv_left_2)
                self.layout.yuv_r2.setStyleSheet(bg_alpha)
            elif (mixer_yuv_2_split[0] != "True" and mixer_yuv_2_split[4] == "True"):
                # Color Right
                self.color_yuv_l2 = ["False", 0, 0, 0]
                self.color_yuv_r2 = ["True", float(mixer_yuv_2_split[5]), float(mixer_yuv_2_split[6]), float(mixer_yuv_2_split[7])]
                rgb_yuv_r2 = self.yuv_to_rgb(self.color_yuv_r2[1], self.color_yuv_r2[2], self.color_yuv_r2[3])
                color_yuv_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_r2[0]*255, rgb_yuv_r2[1]*255, rgb_yuv_r2[2]*255))
                self.layout.yuv_l2.setStyleSheet(bg_alpha)
                self.layout.yuv_r2.setStyleSheet(color_yuv_right_2)
            # Mixer YUV 3
            mixer_yuv_3_string = Krita.instance().readSetting("Pigment.O", "mix_YUV_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_yuv_3_split = mixer_yuv_3_string.split(",")
            if (mixer_yuv_3_split[0] == "True" and mixer_yuv_3_split[4] == "True"):
                # Gradient
                self.color_yuv_l3 = ["True", float(mixer_yuv_3_split[1]), float(mixer_yuv_3_split[2]), float(mixer_yuv_3_split[3])]
                self.color_yuv_r3 = ["True", float(mixer_yuv_3_split[5]), float(mixer_yuv_3_split[6]), float(mixer_yuv_3_split[7])]
                rgb_yuv_l3 = self.yuv_to_rgb(self.color_yuv_l3[1], self.color_yuv_l3[2], self.color_yuv_l3[3])
                rgb_yuv_r3 = self.yuv_to_rgb(self.color_yuv_r3[1], self.color_yuv_r3[2], self.color_yuv_r3[3])
                color_yuv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_l3[0]*255, rgb_yuv_l3[1]*255, rgb_yuv_l3[2]*255))
                color_yuv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_r3[0]*255, rgb_yuv_r3[1]*255, rgb_yuv_r3[2]*255))
                self.layout.yuv_l3.setStyleSheet(color_yuv_left_3)
                self.layout.yuv_r3.setStyleSheet(color_yuv_right_3)
            elif (mixer_yuv_3_split[0] == "True" and mixer_yuv_3_split[4] != "True"):
                # Color Left
                self.color_yuv_l3 = ["True", float(mixer_yuv_3_split[1]), float(mixer_yuv_3_split[2]), float(mixer_yuv_3_split[3])]
                self.color_yuv_r3 = ["False", 0, 0, 0]
                rgb_yuv_l3 = self.yuv_to_rgb(self.color_yuv_l3[1], self.color_yuv_l3[2], self.color_yuv_l3[3])
                color_yuv_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_l3[0]*255, rgb_yuv_l3[1]*255, rgb_yuv_l3[2]*255))
                self.layout.yuv_l3.setStyleSheet(color_yuv_left_3)
                self.layout.yuv_r3.setStyleSheet(bg_alpha)
            elif (mixer_yuv_3_split[0] != "True" and mixer_yuv_3_split[4] == "True"):
                # Color Right
                self.color_yuv_l3 = ["False", 0, 0, 0]
                self.color_yuv_r3 = ["True", float(mixer_yuv_3_split[5]), float(mixer_yuv_3_split[6]), float(mixer_yuv_3_split[7])]
                rgb_yuv_r3 = self.yuv_to_rgb(self.color_yuv_r3[1], self.color_yuv_r3[2], self.color_yuv_r3[3])
                color_yuv_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_yuv_r3[0]*255, rgb_yuv_r3[1]*255, rgb_yuv_r3[2]*255))
                self.layout.yuv_l3.setStyleSheet(bg_alpha)
                self.layout.yuv_r3.setStyleSheet(color_yuv_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer YUV")
        #//
        #\\ Mixer RYB ##########################################################
        try:
            # Mixer RYB 1
            mixer_ryb_1_string = Krita.instance().readSetting("Pigment.O", "mix_RYB_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_ryb_1_split = mixer_ryb_1_string.split(",")
            if (mixer_ryb_1_split[0] == "True" and mixer_ryb_1_split[4] == "True"):
                # Gradient
                self.color_ryb_l1 = ["True", float(mixer_ryb_1_split[1]), float(mixer_ryb_1_split[2]), float(mixer_ryb_1_split[3])]
                self.color_ryb_r1 = ["True", float(mixer_ryb_1_split[5]), float(mixer_ryb_1_split[6]), float(mixer_ryb_1_split[7])]
                rgb_ryb_l1 = self.ryb_to_rgb(self.color_ryb_l1[1], self.color_ryb_l1[2], self.color_ryb_l1[3])
                rgb_ryb_r1 = self.ryb_to_rgb(self.color_ryb_r1[1], self.color_ryb_r1[2], self.color_ryb_r1[3])
                color_ryb_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_l1[0]*255, rgb_ryb_l1[1]*255, rgb_ryb_l1[2]*255))
                color_ryb_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_r1[0]*255, rgb_ryb_r1[1]*255, rgb_ryb_r1[2]*255))
                self.layout.ryb_l1.setStyleSheet(color_ryb_left_1)
                self.layout.ryb_r1.setStyleSheet(color_ryb_right_1)
            elif (mixer_ryb_1_split[0] == "True" and mixer_ryb_1_split[4] != "True"):
                # Color Left
                self.color_ryb_l1 = ["True", float(mixer_ryb_1_split[1]), float(mixer_ryb_1_split[2]), float(mixer_ryb_1_split[3])]
                self.color_ryb_r1 = ["False", 0, 0, 0]
                rgb_ryb_l1 = self.ryb_to_rgb(self.color_ryb_l1[1], self.color_ryb_l1[2], self.color_ryb_l1[3])
                color_ryb_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_l1[0]*255, rgb_ryb_l1[1]*255, rgb_ryb_l1[2]*255))
                self.layout.ryb_l1.setStyleSheet(color_ryb_left_1)
                self.layout.ryb_r1.setStyleSheet(bg_alpha)
            elif (mixer_ryb_1_split[0] != "True" and mixer_ryb_1_split[4] == "True"):
                # Color Right
                self.color_ryb_l1 = ["False", 0, 0, 0]
                self.color_ryb_r1 = ["True", float(mixer_ryb_1_split[5]), float(mixer_ryb_1_split[6]), float(mixer_ryb_1_split[7])]
                rgb_ryb_r1 = self.ryb_to_rgb(self.color_ryb_r1[1], self.color_ryb_r1[2], self.color_ryb_r1[3])
                color_ryb_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_r1[0]*255, rgb_ryb_r1[1]*255, rgb_ryb_r1[2]*255))
                self.layout.ryb_l1.setStyleSheet(bg_alpha)
                self.layout.ryb_r1.setStyleSheet(color_ryb_right_1)
            # Mixer RYB 2
            mixer_ryb_2_string = Krita.instance().readSetting("Pigment.O", "mix_RYB_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_ryb_2_split = mixer_ryb_2_string.split(",")
            if (mixer_ryb_2_split[0] == "True" and mixer_ryb_2_split[4] == "True"):
                # Gradient
                self.color_ryb_l2 = ["True", float(mixer_ryb_2_split[1]), float(mixer_ryb_2_split[2]), float(mixer_ryb_2_split[3])]
                self.color_ryb_r2 = ["True", float(mixer_ryb_2_split[5]), float(mixer_ryb_2_split[6]), float(mixer_ryb_2_split[7])]
                rgb_ryb_l2 = self.ryb_to_rgb(self.color_ryb_l2[1], self.color_ryb_l2[2], self.color_ryb_l2[3])
                rgb_ryb_r2 = self.ryb_to_rgb(self.color_ryb_r2[1], self.color_ryb_r2[2], self.color_ryb_r2[3])
                color_ryb_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_l2[0]*255, rgb_ryb_l2[1]*255, rgb_ryb_l2[2]*255))
                color_ryb_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_r2[0]*255, rgb_ryb_r2[1]*255, rgb_ryb_r2[2]*255))
                self.layout.ryb_l2.setStyleSheet(color_ryb_left_2)
                self.layout.ryb_r2.setStyleSheet(color_ryb_right_2)
            elif (mixer_ryb_2_split[0] == "True" and mixer_ryb_2_split[4] != "True"):
                # Color Left
                self.color_ryb_l2 = ["True", float(mixer_ryb_2_split[1]), float(mixer_ryb_2_split[2]), float(mixer_ryb_2_split[3])]
                self.color_ryb_r2 = ["False", 0, 0, 0]
                rgb_ryb_l2 = self.ryb_to_rgb(self.color_ryb_l2[1], self.color_ryb_l2[2], self.color_ryb_l2[3])
                color_ryb_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_l2[0]*255, rgb_ryb_l2[1]*255, rgb_ryb_l2[2]*255))
                self.layout.ryb_l2.setStyleSheet(color_ryb_left_2)
                self.layout.ryb_r2.setStyleSheet(bg_alpha)
            elif (mixer_ryb_2_split[0] != "True" and mixer_ryb_2_split[4] == "True"):
                # Color Right
                self.color_ryb_l2 = ["False", 0, 0, 0]
                self.color_ryb_r2 = ["True", float(mixer_ryb_2_split[5]), float(mixer_ryb_2_split[6]), float(mixer_ryb_2_split[7])]
                rgb_ryb_r2 = self.ryb_to_rgb(self.color_ryb_r2[1], self.color_ryb_r2[2], self.color_ryb_r2[3])
                color_ryb_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_r2[0]*255, rgb_ryb_r2[1]*255, rgb_ryb_r2[2]*255))
                self.layout.ryb_l2.setStyleSheet(bg_alpha)
                self.layout.ryb_r2.setStyleSheet(color_ryb_right_2)
            # Mixer RYB 3
            mixer_ryb_3_string = Krita.instance().readSetting("Pigment.O", "mix_RYB_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_ryb_3_split = mixer_ryb_3_string.split(",")
            if (mixer_ryb_3_split[0] == "True" and mixer_ryb_3_split[4] == "True"):
                # Gradient
                self.color_ryb_l3 = ["True", float(mixer_ryb_3_split[1]), float(mixer_ryb_3_split[2]), float(mixer_ryb_3_split[3])]
                self.color_ryb_r3 = ["True", float(mixer_ryb_3_split[5]), float(mixer_ryb_3_split[6]), float(mixer_ryb_3_split[7])]
                rgb_ryb_l3 = self.ryb_to_rgb(self.color_ryb_l3[1], self.color_ryb_l3[2], self.color_ryb_l3[3])
                rgb_ryb_r3 = self.ryb_to_rgb(self.color_ryb_r3[1], self.color_ryb_r3[2], self.color_ryb_r3[3])
                color_ryb_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_l3[0]*255, rgb_ryb_l3[1]*255, rgb_ryb_l3[2]*255))
                color_ryb_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_r3[0]*255, rgb_ryb_r3[1]*255, rgb_ryb_r3[2]*255))
                self.layout.ryb_l3.setStyleSheet(color_ryb_left_3)
                self.layout.ryb_r3.setStyleSheet(color_ryb_right_3)
            elif (mixer_ryb_3_split[0] == "True" and mixer_ryb_3_split[4] != "True"):
                # Color Left
                self.color_ryb_l3 = ["True", float(mixer_ryb_3_split[1]), float(mixer_ryb_3_split[2]), float(mixer_ryb_3_split[3])]
                self.color_ryb_r3 = ["False", 0, 0, 0]
                rgb_ryb_l3 = self.ryb_to_rgb(self.color_ryb_l3[1], self.color_ryb_l3[2], self.color_ryb_l3[3])
                color_ryb_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_l3[0]*255, rgb_ryb_l3[1]*255, rgb_ryb_l3[2]*255))
                self.layout.ryb_l3.setStyleSheet(color_ryb_left_3)
                self.layout.ryb_r3.setStyleSheet(bg_alpha)
            elif (mixer_ryb_3_split[0] != "True" and mixer_ryb_3_split[4] == "True"):
                # Color Right
                self.color_ryb_l3 = ["False", 0, 0, 0]
                self.color_ryb_r3 = ["True", float(mixer_ryb_3_split[5]), float(mixer_ryb_3_split[6]), float(mixer_ryb_3_split[7])]
                rgb_ryb_r3 = self.ryb_to_rgb(self.color_ryb_r3[1], self.color_ryb_r3[2], self.color_ryb_r3[3])
                color_ryb_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_ryb_r3[0]*255, rgb_ryb_r3[1]*255, rgb_ryb_r3[2]*255))
                self.layout.ryb_l3.setStyleSheet(bg_alpha)
                self.layout.ryb_r3.setStyleSheet(color_ryb_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer RYB")
        #//
        #\\ Mixer CMYK #########################################################
        try:
            # Mixer CMYK 1
            mixer_cmyk_1_string = Krita.instance().readSetting("Pigment.O", "mix_CMYK_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_cmyk_1_split = mixer_cmyk_1_string.split(",")
            if (mixer_cmyk_1_split[0] == "True" and mixer_cmyk_1_split[5] == "True"):
                # Gradient
                self.color_cmyk_l1 = ["True", float(mixer_cmyk_1_split[1]), float(mixer_cmyk_1_split[2]), float(mixer_cmyk_1_split[3]), float(mixer_cmyk_1_split[4])]
                self.color_cmyk_r1 = ["True", float(mixer_cmyk_1_split[6]), float(mixer_cmyk_1_split[7]), float(mixer_cmyk_1_split[8]), float(mixer_cmyk_1_split[9])]
                rgb_cmyk_l1 = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
                rgb_cmyk_r1 = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
                color_cmyk_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l1[0]*255, rgb_cmyk_l1[1]*255, rgb_cmyk_l1[2]*255))
                color_cmyk_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r1[0]*255, rgb_cmyk_r1[1]*255, rgb_cmyk_r1[2]*255))
                self.layout.cmyk_l1.setStyleSheet(color_cmyk_left_1)
                self.layout.cmyk_r1.setStyleSheet(color_cmyk_right_1)
            elif (mixer_cmyk_1_split[0] == "True" and mixer_cmyk_1_split[5] != "True"):
                # Color Left
                self.color_cmyk_l1 = ["True", float(mixer_cmyk_1_split[1]), float(mixer_cmyk_1_split[2]), float(mixer_cmyk_1_split[3]), float(mixer_cmyk_1_split[4])]
                self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
                rgb_cmyk_l1 = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
                color_cmyk_left_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l1[0]*255, rgb_cmyk_l1[1]*255, rgb_cmyk_l1[2]*255))
                self.layout.cmyk_l1.setStyleSheet(color_cmyk_left_1)
                self.layout.cmyk_r1.setStyleSheet(bg_alpha)
            elif (mixer_cmyk_1_split[0] != "True" and mixer_cmyk_1_split[5] == "True"):
                # Color Right
                self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
                self.color_cmyk_r1 = ["True", float(mixer_cmyk_1_split[6]), float(mixer_cmyk_1_split[7]), float(mixer_cmyk_1_split[8]), float(mixer_cmyk_1_split[9])]
                rgb_cmyk_r1 = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
                color_cmyk_right_1 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r1[0]*255, rgb_cmyk_r1[1]*255, rgb_cmyk_r1[2]*255))
                self.layout.cmyk_l1.setStyleSheet(bg_alpha)
                self.layout.cmyk_r1.setStyleSheet(color_cmyk_right_1)
            # Mixer CMYK 2
            mixer_cmyk_2_string = Krita.instance().readSetting("Pigment.O", "mix_CMYK_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_cmyk_2_split = mixer_cmyk_2_string.split(",")
            if (mixer_cmyk_2_split[0] == "True" and mixer_cmyk_2_split[5] == "True"):
                # Gradient
                self.color_cmyk_l2 = ["True", float(mixer_cmyk_2_split[1]), float(mixer_cmyk_2_split[2]), float(mixer_cmyk_2_split[3]), float(mixer_cmyk_2_split[4])]
                self.color_cmyk_r2 = ["True", float(mixer_cmyk_2_split[6]), float(mixer_cmyk_2_split[7]), float(mixer_cmyk_2_split[8]), float(mixer_cmyk_2_split[9])]
                rgb_cmyk_l2 = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
                rgb_cmyk_r2 = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
                color_cmyk_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l2[0]*255, rgb_cmyk_l2[1]*255, rgb_cmyk_l2[2]*255))
                color_cmyk_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r2[0]*255, rgb_cmyk_r2[1]*255, rgb_cmyk_r2[2]*255))
                self.layout.cmyk_l2.setStyleSheet(color_cmyk_left_2)
                self.layout.cmyk_r2.setStyleSheet(color_cmyk_right_2)
            elif (mixer_cmyk_2_split[0] == "True" and mixer_cmyk_2_split[5] != "True"):
                # Color Left
                self.color_cmyk_l2 =  ["True", float(mixer_cmyk_2_split[1]), float(mixer_cmyk_2_split[2]), float(mixer_cmyk_2_split[3]), float(mixer_cmyk_2_split[4])]
                self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
                rgb_cmyk_l2 = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
                color_cmyk_left_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l2[0]*255, rgb_cmyk_l2[1]*255, rgb_cmyk_l2[2]*255))
                self.layout.cmyk_l2.setStyleSheet(color_cmyk_left_2)
                self.layout.cmyk_r2.setStyleSheet(bg_alpha)
            elif (mixer_cmyk_2_split[0] != "True" and mixer_cmyk_2_split[5] == "True"):
                # Color Right
                self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
                self.color_cmyk_r2 = ["True", float(mixer_cmyk_2_split[6]), float(mixer_cmyk_2_split[7]), float(mixer_cmyk_2_split[8]), float(mixer_cmyk_2_split[9])]
                rgb_cmyk_r2 = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
                color_cmyk_right_2 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r2[0]*255, rgb_cmyk_r2[1]*255, rgb_cmyk_r2[2]*255))
                self.layout.cmyk_l2.setStyleSheet(bg_alpha)
                self.layout.cmyk_r2.setStyleSheet(color_cmyk_right_2)
            # Mixer CMYK 3
            mixer_cmyk_3_string = Krita.instance().readSetting("Pigment.O", "mix_CMYK_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            mixer_cmyk_3_split = mixer_cmyk_3_string.split(",")
            if (mixer_cmyk_3_split[0] == "True" and mixer_cmyk_3_split[5] == "True"):
                # Gradient
                self.color_cmyk_l3 = ["True", float(mixer_cmyk_3_split[1]), float(mixer_cmyk_3_split[2]), float(mixer_cmyk_3_split[3]), float(mixer_cmyk_3_split[4])]
                self.color_cmyk_r3 = ["True", float(mixer_cmyk_3_split[6]), float(mixer_cmyk_3_split[7]), float(mixer_cmyk_3_split[8]), float(mixer_cmyk_3_split[9])]
                rgb_cmyk_l3 = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
                rgb_cmyk_r3 = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
                color_cmyk_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l3[0]*255, rgb_cmyk_l3[1]*255, rgb_cmyk_l3[2]*255))
                color_cmyk_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r3[0]*255, rgb_cmyk_r3[1]*255, rgb_cmyk_r3[2]*255))
                self.layout.cmyk_l3.setStyleSheet(color_cmyk_left_3)
                self.layout.cmyk_r3.setStyleSheet(color_cmyk_right_3)
            elif (mixer_cmyk_3_split[0] == "True" and mixer_cmyk_3_split[5] != "True"):
                # Color Left
                self.color_cmyk_l3 =  ["True", float(mixer_cmyk_3_split[1]), float(mixer_cmyk_3_split[2]), float(mixer_cmyk_3_split[3]), float(mixer_cmyk_3_split[4])]
                self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
                rgb_cmyk_l3 = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
                color_cmyk_left_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_l3[0]*255, rgb_cmyk_l3[1]*255, rgb_cmyk_l3[2]*255))
                self.layout.cmyk_l3.setStyleSheet(color_cmyk_left_3)
                self.layout.cmyk_r3.setStyleSheet(bg_alpha)
            elif (mixer_cmyk_3_split[0] != "True" and mixer_cmyk_3_split[5] == "True"):
                # Color Right
                self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
                self.color_cmyk_r3 = ["True", float(mixer_cmyk_3_split[6]), float(mixer_cmyk_3_split[7]), float(mixer_cmyk_3_split[8]), float(mixer_cmyk_3_split[9])]
                rgb_cmyk_r3 = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
                color_cmyk_right_3 = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb_cmyk_r3[0]*255, rgb_cmyk_r3[1]*255, rgb_cmyk_r3[2]*255))
                self.layout.cmyk_l3.setStyleSheet(bg_alpha)
                self.layout.cmyk_r3.setStyleSheet(color_cmyk_right_3)
        except:
            QtCore.qDebug("Load Error - Mixer CMYK")
        #//
        #\\ Mixer Gradient Display #############################################
        self.Mixer_Display()

        #//
    def Settings_Save_Misc(self):
        #\\ Panel GAM ##########################################################
        if self.panel_active == "GAM":
            gam_list_p1s1 = (
                str(self.P1_S1[0]), str(self.P1_S1[1]),
                str(self.P1_S1[2]), str(self.P1_S1[3]),
                str(self.P1_S1[4]), str(self.P1_S1[5]),
                str(self.P1_S1[6]), str(self.P1_S1[7]),
                )
            gam_list_p1s3 = (
                str(self.P1_S3[0]), str(self.P1_S3[1]),
                str(self.P1_S3[2]), str(self.P1_S3[3]),
                str(self.P1_S3[4]), str(self.P1_S3[5]),
                )
            gam_list_p1s4 = (
                str(self.P1_S4[0]), str(self.P1_S4[1]),
                str(self.P1_S4[2]), str(self.P1_S4[3]),
                str(self.P1_S4[4]), str(self.P1_S4[5]),
                str(self.P1_S4[6]), str(self.P1_S4[7]),
                )
            gam_list_p2s1 = (
                str(self.P2_S1[0]), str(self.P2_S1[1]),
                str(self.P2_S1[2]), str(self.P2_S1[3]),
                str(self.P2_S1[4]), str(self.P2_S1[5]),
                str(self.P2_S1[6]), str(self.P2_S1[7]),
                str(self.P2_S1[8]), str(self.P2_S1[9]),
                str(self.P2_S1[10]), str(self.P2_S1[11]),
                str(self.P2_S1[12]), str(self.P2_S1[13]),
                str(self.P2_S1[14]), str(self.P2_S1[15]),
                )
            gam_list_p3s3 = (
                str(self.P3_S3[0]), str(self.P3_S3[1]),
                str(self.P3_S3[2]), str(self.P3_S3[3]),
                str(self.P3_S3[4]), str(self.P3_S3[5]),
                str(self.P3_S3[6]), str(self.P3_S3[7]),
                str(self.P3_S3[8]), str(self.P3_S3[9]),
                str(self.P3_S3[10]), str(self.P3_S3[11]),
                str(self.P3_S3[12]), str(self.P3_S3[13]),
                )
            gam_string_p1s1 = ','.join(gam_list_p1s1)
            gam_string_p1s3 = ','.join(gam_list_p1s3)
            gam_string_p1s4 = ','.join(gam_list_p1s4)
            gam_string_p2s1 = ','.join(gam_list_p2s1)
            gam_string_p3s3 = ','.join(gam_list_p3s3)
            Krita.instance().writeSetting("Pigment.O", "gam_p1s1", gam_string_p1s1)
            Krita.instance().writeSetting("Pigment.O", "gam_p1s3", gam_string_p1s3)
            Krita.instance().writeSetting("Pigment.O", "gam_p1s4", gam_string_p1s4)
            Krita.instance().writeSetting("Pigment.O", "gam_p2s1", gam_string_p2s1)
            Krita.instance().writeSetting("Pigment.O", "gam_p3s3", gam_string_p3s3)
        #//
        #\\ Panel DOT ##########################################################
        if self.panel_active == "DOT":
            dot_list_01 = (str(self.dot_1[0]), str(self.dot_1[1]), str(self.dot_1[2]), str(self.dot_1[3]))
            dot_list_02 = (str(self.dot_2[0]), str(self.dot_2[1]), str(self.dot_2[2]), str(self.dot_2[3]))
            dot_list_03 = (str(self.dot_3[0]), str(self.dot_3[1]), str(self.dot_3[2]), str(self.dot_3[3]))
            dot_list_04 = (str(self.dot_4[0]), str(self.dot_4[1]), str(self.dot_4[2]), str(self.dot_4[3]))
            dot_string_01 = ','.join(dot_list_01)
            dot_string_02 = ','.join(dot_list_02)
            dot_string_03 = ','.join(dot_list_03)
            dot_string_04 = ','.join(dot_list_04)
            Krita.instance().writeSetting("Pigment.O", "dot_01", dot_string_01)
            Krita.instance().writeSetting("Pigment.O", "dot_02", dot_string_02)
            Krita.instance().writeSetting("Pigment.O", "dot_03", dot_string_03)
            Krita.instance().writeSetting("Pigment.O", "dot_04", dot_string_04)
        #//
        #\\ Panel OBJ ##########################################################
        if self.panel_active == "OBJ":
            object_00_list = (
            str(self.bg_1[0][0]), str(self.bg_1[0][1]), str(self.bg_1[0][2]), str(self.bg_1[0][3]), str(self.bg_1[0][4]),
            str(self.bg_2[0][0]), str(self.bg_2[0][1]), str(self.bg_2[0][2]), str(self.bg_2[0][3]), str(self.bg_2[0][4]),
            str(self.bg_3[0][0]), str(self.bg_3[0][1]), str(self.bg_3[0][2]), str(self.bg_3[0][3]), str(self.bg_3[0][4]),
            str(self.dif_1[0][0]), str(self.dif_1[0][1]), str(self.dif_1[0][2]), str(self.dif_1[0][3]), str(self.dif_1[0][4]),
            str(self.dif_2[0][0]), str(self.dif_2[0][1]), str(self.dif_2[0][2]), str(self.dif_2[0][3]), str(self.dif_2[0][4]),
            str(self.dif_3[0][0]), str(self.dif_3[0][1]), str(self.dif_3[0][2]), str(self.dif_3[0][3]), str(self.dif_3[0][4]),
            str(self.dif_4[0][0]), str(self.dif_4[0][1]), str(self.dif_4[0][2]), str(self.dif_4[0][3]), str(self.dif_4[0][4]),
            str(self.dif_5[0][0]), str(self.dif_5[0][1]), str(self.dif_5[0][2]), str(self.dif_5[0][3]), str(self.dif_5[0][4]),
            str(self.dif_6[0][0]), str(self.dif_6[0][1]), str(self.dif_6[0][2]), str(self.dif_6[0][3]), str(self.dif_6[0][4]),
            str(self.fg_1[0][0]), str(self.fg_1[0][1]), str(self.fg_1[0][2]), str(self.fg_1[0][3]), str(self.fg_1[0][4]),
            str(self.fg_2[0][0]), str(self.fg_2[0][1]), str(self.fg_2[0][2]), str(self.fg_2[0][3]), str(self.fg_2[0][4]),
            str(self.fg_3[0][0]), str(self.fg_3[0][1]), str(self.fg_3[0][2]), str(self.fg_3[0][3]), str(self.fg_3[0][4]),
            )
            object_00_string = ','.join(object_00_list)
            Krita.instance().writeSetting("Pigment.O", "obj_00", object_00_string)

            object_01_list = (
            str(self.bg_1[1][0]), str(self.bg_1[1][1]), str(self.bg_1[1][2]), str(self.bg_1[1][3]), str(self.bg_1[1][4]),
            str(self.bg_2[1][0]), str(self.bg_2[1][1]), str(self.bg_2[1][2]), str(self.bg_2[1][3]), str(self.bg_2[1][4]),
            str(self.bg_3[1][0]), str(self.bg_3[1][1]), str(self.bg_3[1][2]), str(self.bg_3[1][3]), str(self.bg_3[1][4]),
            str(self.dif_1[1][0]), str(self.dif_1[1][1]), str(self.dif_1[1][2]), str(self.dif_1[1][3]), str(self.dif_1[1][4]),
            str(self.dif_2[1][0]), str(self.dif_2[1][1]), str(self.dif_2[1][2]), str(self.dif_2[1][3]), str(self.dif_2[1][4]),
            str(self.dif_3[1][0]), str(self.dif_3[1][1]), str(self.dif_3[1][2]), str(self.dif_3[1][3]), str(self.dif_3[1][4]),
            str(self.dif_4[1][0]), str(self.dif_4[1][1]), str(self.dif_4[1][2]), str(self.dif_4[1][3]), str(self.dif_4[1][4]),
            str(self.dif_5[1][0]), str(self.dif_5[1][1]), str(self.dif_5[1][2]), str(self.dif_5[1][3]), str(self.dif_5[1][4]),
            str(self.dif_6[1][0]), str(self.dif_6[1][1]), str(self.dif_6[1][2]), str(self.dif_6[1][3]), str(self.dif_6[1][4]),
            str(self.fg_1[1][0]), str(self.fg_1[1][1]), str(self.fg_1[1][2]), str(self.fg_1[1][3]), str(self.fg_1[1][4]),
            str(self.fg_2[1][0]), str(self.fg_2[1][1]), str(self.fg_2[1][2]), str(self.fg_2[1][3]), str(self.fg_2[1][4]),
            str(self.fg_3[1][0]), str(self.fg_3[1][1]), str(self.fg_3[1][2]), str(self.fg_3[1][3]), str(self.fg_3[1][4]),
            )
            object_01_string = ','.join(object_01_list)
            Krita.instance().writeSetting("Pigment.O", "obj_01", object_01_string)
        #//
        #\\ SOF ################################################################
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Save Settings
            tip_sof_list = (str(self.lock_size), str(self.lock_opacity), str(self.lock_flow))
            tip_sof_string = ','.join(tip_sof_list)
            Krita.instance().writeSetting("Pigment.O", "tip_SOF", tip_sof_string)
        #//
        #\\ TIP ################################################################
        cor_00_list = (str(self.cor_00[0]), str(self.cor_00[1]), str(self.cor_00[2]), str(self.cor_00[3]))
        cor_01_list = (str(self.cor_01[0]), str(self.cor_01[1]), str(self.cor_01[2]), str(self.cor_01[3]))
        cor_02_list = (str(self.cor_02[0]), str(self.cor_02[1]), str(self.cor_02[2]), str(self.cor_02[3]))
        cor_03_list = (str(self.cor_03[0]), str(self.cor_03[1]), str(self.cor_03[2]), str(self.cor_03[3]))
        cor_04_list = (str(self.cor_04[0]), str(self.cor_04[1]), str(self.cor_04[2]), str(self.cor_04[3]))
        cor_05_list = (str(self.cor_05[0]), str(self.cor_05[1]), str(self.cor_05[2]), str(self.cor_05[3]))
        cor_06_list = (str(self.cor_06[0]), str(self.cor_06[1]), str(self.cor_06[2]), str(self.cor_06[3]))
        cor_07_list = (str(self.cor_07[0]), str(self.cor_07[1]), str(self.cor_07[2]), str(self.cor_07[3]))
        cor_08_list = (str(self.cor_08[0]), str(self.cor_08[1]), str(self.cor_08[2]), str(self.cor_08[3]))
        cor_09_list = (str(self.cor_09[0]), str(self.cor_09[1]), str(self.cor_09[2]), str(self.cor_09[3]))
        cor_10_list = (str(self.cor_10[0]), str(self.cor_10[1]), str(self.cor_10[2]), str(self.cor_10[3]))
        cor_00_string = ','.join(cor_00_list)
        cor_01_string = ','.join(cor_01_list)
        cor_02_string = ','.join(cor_02_list)
        cor_03_string = ','.join(cor_03_list)
        cor_04_string = ','.join(cor_04_list)
        cor_05_string = ','.join(cor_05_list)
        cor_06_string = ','.join(cor_06_list)
        cor_07_string = ','.join(cor_07_list)
        cor_08_string = ','.join(cor_08_list)
        cor_09_string = ','.join(cor_09_list)
        cor_10_string = ','.join(cor_10_list)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_00", cor_00_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_01", cor_01_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_02", cor_02_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_03", cor_03_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_04", cor_04_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_05", cor_05_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_06", cor_06_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_07", cor_07_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_08", cor_08_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_09", cor_09_string)
        Krita.instance().writeSetting("Pigment.O", "tip_cor_10", cor_10_string)
        #//
        #\\ Mixer TTS ##########################################################
        color_tts_list = (str(self.color_tts[0]), str(self.color_tts[1]), str(self.color_tts[2]), str(self.color_tts[3]))
        color_tts_string = ','.join(color_tts_list)
        Krita.instance().writeSetting("Pigment.O", "mix_TTS", color_tts_string)
        #//
        #\\ Mixer ##############################################################
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
        mixer_list_hcy_1 = (str(self.color_hcy_l1[0]), str(self.color_hcy_l1[1]), str(self.color_hcy_l1[2]), str(self.color_hcy_l1[3]), str(self.color_hcy_r1[0]),  str(self.color_hcy_r1[1]), str(self.color_hcy_r1[2]), str(self.color_hcy_r1[3]))
        mixer_list_hcy_2 = (str(self.color_hcy_l2[0]), str(self.color_hcy_l2[1]), str(self.color_hcy_l2[2]), str(self.color_hcy_l2[3]), str(self.color_hcy_r2[0]),  str(self.color_hcy_r2[1]), str(self.color_hcy_r2[2]), str(self.color_hcy_r2[3]))
        mixer_list_hcy_3 = (str(self.color_hcy_l3[0]), str(self.color_hcy_l3[1]), str(self.color_hcy_l3[2]), str(self.color_hcy_l3[3]), str(self.color_hcy_r3[0]),  str(self.color_hcy_r3[1]), str(self.color_hcy_r3[2]), str(self.color_hcy_r3[3]))
        mixer_list_yuv_1 = (str(self.color_yuv_l1[0]), str(self.color_yuv_l1[1]), str(self.color_yuv_l1[2]), str(self.color_yuv_l1[3]), str(self.color_yuv_r1[0]),  str(self.color_yuv_r1[1]), str(self.color_yuv_r1[2]), str(self.color_yuv_r1[3]))
        mixer_list_yuv_2 = (str(self.color_yuv_l2[0]), str(self.color_yuv_l2[1]), str(self.color_yuv_l2[2]), str(self.color_yuv_l2[3]), str(self.color_yuv_r2[0]),  str(self.color_yuv_r2[1]), str(self.color_yuv_r2[2]), str(self.color_yuv_r2[3]))
        mixer_list_yuv_3 = (str(self.color_yuv_l3[0]), str(self.color_yuv_l3[1]), str(self.color_yuv_l3[2]), str(self.color_yuv_l3[3]), str(self.color_yuv_r3[0]),  str(self.color_yuv_r3[1]), str(self.color_yuv_r3[2]), str(self.color_yuv_r3[3]))
        mixer_list_ryb_1 = (str(self.color_ryb_l1[0]), str(self.color_ryb_l1[1]), str(self.color_ryb_l1[2]), str(self.color_ryb_l1[3]), str(self.color_ryb_r1[0]),  str(self.color_ryb_r1[1]), str(self.color_ryb_r1[2]), str(self.color_ryb_r1[3]))
        mixer_list_ryb_2 = (str(self.color_ryb_l2[0]), str(self.color_ryb_l2[1]), str(self.color_ryb_l2[2]), str(self.color_ryb_l2[3]), str(self.color_ryb_r2[0]),  str(self.color_ryb_r2[1]), str(self.color_ryb_r2[2]), str(self.color_ryb_r2[3]))
        mixer_list_ryb_3 = (str(self.color_ryb_l3[0]), str(self.color_ryb_l3[1]), str(self.color_ryb_l3[2]), str(self.color_ryb_l3[3]), str(self.color_ryb_r3[0]),  str(self.color_ryb_r3[1]), str(self.color_ryb_r3[2]), str(self.color_ryb_r3[3]))
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
        mixer_string_hcy_1 = ','.join(mixer_list_hcy_1)
        mixer_string_hcy_2 = ','.join(mixer_list_hcy_2)
        mixer_string_hcy_3 = ','.join(mixer_list_hcy_3)
        mixer_string_yuv_1 = ','.join(mixer_list_yuv_1)
        mixer_string_yuv_2 = ','.join(mixer_list_yuv_2)
        mixer_string_yuv_3 = ','.join(mixer_list_yuv_3)
        mixer_string_ryb_1 = ','.join(mixer_list_ryb_1)
        mixer_string_ryb_2 = ','.join(mixer_list_ryb_2)
        mixer_string_ryb_3 = ','.join(mixer_list_ryb_3)
        mixer_string_cmyk_1 = ','.join(mixer_list_cmyk_1)
        mixer_string_cmyk_2 = ','.join(mixer_list_cmyk_2)
        mixer_string_cmyk_3 = ','.join(mixer_list_cmyk_3)
        Krita.instance().writeSetting("Pigment.O", "mix_RGB_1", mixer_string_rgb_1)
        Krita.instance().writeSetting("Pigment.O", "mix_RGB_2", mixer_string_rgb_2)
        Krita.instance().writeSetting("Pigment.O", "mix_RGB_3", mixer_string_rgb_3)
        Krita.instance().writeSetting("Pigment.O", "mix_ARD_1", mixer_string_ard_1)
        Krita.instance().writeSetting("Pigment.O", "mix_ARD_2", mixer_string_ard_2)
        Krita.instance().writeSetting("Pigment.O", "mix_ARD_3", mixer_string_ard_3)
        Krita.instance().writeSetting("Pigment.O", "mix_HSV_1", mixer_string_hsv_1)
        Krita.instance().writeSetting("Pigment.O", "mix_HSV_2", mixer_string_hsv_2)
        Krita.instance().writeSetting("Pigment.O", "mix_HSV_3", mixer_string_hsv_3)
        Krita.instance().writeSetting("Pigment.O", "mix_HSL_1", mixer_string_hsl_1)
        Krita.instance().writeSetting("Pigment.O", "mix_HSL_2", mixer_string_hsl_2)
        Krita.instance().writeSetting("Pigment.O", "mix_HSL_3", mixer_string_hsl_3)
        Krita.instance().writeSetting("Pigment.O", "mix_HCY_1", mixer_string_hcy_1)
        Krita.instance().writeSetting("Pigment.O", "mix_HCY_2", mixer_string_hcy_2)
        Krita.instance().writeSetting("Pigment.O", "mix_HCY_3", mixer_string_hcy_3)
        Krita.instance().writeSetting("Pigment.O", "mix_YUV_1", mixer_string_yuv_1)
        Krita.instance().writeSetting("Pigment.O", "mix_YUV_2", mixer_string_yuv_2)
        Krita.instance().writeSetting("Pigment.O", "mix_YUV_3", mixer_string_yuv_3)
        Krita.instance().writeSetting("Pigment.O", "mix_RYB_1", mixer_string_ryb_1)
        Krita.instance().writeSetting("Pigment.O", "mix_RYB_2", mixer_string_ryb_2)
        Krita.instance().writeSetting("Pigment.O", "mix_RYB_3", mixer_string_ryb_3)
        Krita.instance().writeSetting("Pigment.O", "mix_CMYK_1", mixer_string_cmyk_1)
        Krita.instance().writeSetting("Pigment.O", "mix_CMYK_2", mixer_string_cmyk_2)
        Krita.instance().writeSetting("Pigment.O", "mix_CMYK_3", mixer_string_cmyk_3)
        #//

    #//
    #\\ Change the Canvas ######################################################
    def canvasChanged(self, canvas):
        # Pop Up Message
        # QMessageBox.information(QWidget(), i18n("Warnning"), i18n("message"))

        # Log Viewer Message
        # QtCore.qDebug("message")
        # QtCore.qWarning("message")
        # QtCore.qCritical("message")
        # self.update()
        pass

    #//
