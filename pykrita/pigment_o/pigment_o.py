# Import Krita
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt
import math
import random
import os
# Pigment.O Modules
from .pigment_o_modulo import (
    Channel_Linear,
    Clicks,
    Apply_RGB,
    Mixer_Gradient,
    Harmony,
    Panel_UVD,
    Panel_ARD,
    Panel_HSV_4,
    Panel_HSL_3,
    Panel_HSL_4,
    Panel_HSL_4D,
    Panel_HUE_Circle,
    Panel_DOT,
    Panel_OBJ,
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
kritaSVLCY = 255  # Saturation + Value + Lightness + Chroma + Luma
kritaRYB = 255
kritaCMY = 255
kritaCMYK = 255
hexAAA = 100  # DO NOT TOUCH !
hexRGB = 255  # DO NOT TOUCH !
hexCMYK = 100  # DO NOT TOUCH !
unitAAA = 1 / kritaAAA
unitRGB = 1 / kritaRGB
unitANG = 1 / kritaANG
unitRDL = 1 / kritaRDL
unitHUE = 1 / kritaHUE
unitSVLY = 1 / kritaSVLCY
unitRYB = 1 / kritaRYB
unitCMY = 1 / kritaCMY
unitCMYK = 1 / kritaCMYK
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
# Luma Coefficients
gammaR = 0.2126
gammaG = 0.7152
gammaB = 0.0722
gammaG = 2.2
lumaR = 0.3
lumaG = 0.59
lumaB = 0.11
# D65 - Daylight, sRGB, Adobe-RGB, 2ºC
factorX = 95.047
factorY = 100.000
factorZ = 108.883
# Kalvin Table
kritaKKKmin = 1000
kritaKKKmax = 12000
kritaKKKdelta = kritaKKKmax - kritaKKKmin
kritaKKKhalf = 6500
kritaKKKunit = 100
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


# Create Action
class PigmentOExtension(Extension):
    """
    Color Shortcut Set.
    """

    #\\ Initialize #############################################################
    def __init__(self, parent):
        super(PigmentOExtension, self).__init__(parent)
        self.sof_1 = 10
        self.sof_23 = 5
        self.rgb = 1
    def setup(self):
        pass

    #//
    #\\ Actions ################################################################
    def createActions(self, window):
        # Actions to Build
        sof = False
        rgb = True
        # Build Actions
        if sof == True:
            action_sof_1_minus = window.createAction("action_sof_1_minus", "SOF Size Minus")
            action_sof_1_minus.triggered.connect(self.SOF_1_Minus)
            action_sof_1_plus = window.createAction("action_sof_1_plus", "SOF Size Plus")
            action_sof_1_plus.triggered.connect(self.SOF_1_Plus)

            action_sof_2_minus = window.createAction("action_sof_2_minus", "SOF Opacity Minus")
            action_sof_2_minus.triggered.connect(self.SOF_2_Minus)
            action_sof_2_plus = window.createAction("action_sof_2_plus", "SOF Opacity Plus")
            action_sof_2_plus.triggered.connect(self.SOF_2_Plus)

            action_sof_3_minus = window.createAction("action_sof_3_minus", "SOF Flow Minus")
            action_sof_3_minus.triggered.connect(self.SOF_3_Minus)
            action_sof_3_plus = window.createAction("action_sof_3_plus", "SOF Flow Plus")
            action_sof_3_plus.triggered.connect(self.SOF_3_Plus)
        if rgb == True:
            action_rgb_1_minus = window.createAction("action_rgb_1_minus", "RGB Red Minus")
            action_rgb_1_minus.triggered.connect(self.RGB_1_Minus)
            action_rgb_1_plus = window.createAction("action_rgb_1_plus", "RGB Red Plus")
            action_rgb_1_plus.triggered.connect(self.RGB_1_Plus)

            action_rgb_2_minus = window.createAction("action_rgb_2_minus", "RGB Green Minus")
            action_rgb_2_minus.triggered.connect(self.RGB_2_Minus)
            action_rgb_2_plus = window.createAction("action_rgb_2_plus", "RGB Green Plus")
            action_rgb_2_plus.triggered.connect(self.RGB_2_Plus)

            action_rgb_3_minus = window.createAction("action_rgb_3_minus", "RGB Blue Minus")
            action_rgb_3_minus.triggered.connect(self.RGB_3_Minus)
            action_rgb_3_plus = window.createAction("action_rgb_3_plus", "RGB Blue Plus")
            action_rgb_3_plus.triggered.connect(self.RGB_3_Plus)

    #//
    #\\ Krita and Pigment ######################################################
    def Krita_2_Pigment(self):
        # Current Krita Color Foreground
        color_foreground = Application.activeWindow().activeView().foregroundColor()
        cfg_components = color_foreground.componentsOrdered()
        cfg_color_model = color_foreground.colorModel()
        cfg_color_depth = color_foreground.colorDepth()
        cfg_color_profile = color_foreground.colorProfile()
        color_background = Application.activeWindow().activeView().backgroundColor()
        cbg_components = color_background.componentsOrdered()
        if (cfg_color_model == "A" or cfg_color_model == "GRAYA"):
            mode = "AAA"
            kac1 = cfg_components[0]
            kac2 = 0
            kac3 = 0
            kac4 = 0
            return [mode, kac1, kac2, kac3, kac4]
        if cfg_color_model == "RGBA":
            length = len(cfg_components)
            if length == 2:
                mode = "RGB"
                kac1 = cfg_components[0]
                kac2 = 0
                kac3 = 0
                kac4 = 0
                return [mode, kac1, kac2, kac3, kac4]
            else:
                mode = "RGB"
                kac1 = cfg_components[0] # Red
                kac2 = cfg_components[1] # Green
                kac3 = cfg_components[2] # Blue
                kac4 = 0
                return [mode, kac1, kac2, kac3, kac4]
        if cfg_color_model == "CMYKA":
            length = len(cfg_components)
            if length == 2:
                mode = "AAA"
                kac1 = cfg_components[0]
                kac2 = 0
                kac3 = 0
                kac4 = 0
                return [mode, kac1, kac2, kac3, kac4]
            else:
                mode = "CMYK"
                kac1 = cfg_components[0]
                kac2 = cfg_components[1]
                kac3 = cfg_components[2]
                kac4 = cfg_components[3]
                return [mode, kac1, kac2, kac3, kac4]
        if cfg_color_model == "XYZA":
            pass
        if cfg_color_model == "LABA":
            pass
        if cfg_color_model == "YCbCrA":
            pass
    def Pigment_2_Krita(self, kac1, kac2, kac3, kac4):
        # Appoly Color considering current Document
        doc = self.Document_Profile()
        if (doc[0] == "A" or doc[0] == "GRAYA"):
            pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
            pigment_color.setComponents([kac1, 1.0])
            Application.activeWindow().activeView().setForeGroundColor(pigment_color)
        if doc[0] == "RGBA":  # RGB with bg_alpha channel (The actual order of channels is most often BGR!)
            pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
            if (doc[1] == "U8" or doc[1] == "U16"):
                pigment_color.setComponents([kac3, kac2, kac1, 1.0])
            if (doc[1] == "F16" or doc[1] == "F32"):
                pigment_color.setComponents([kac1, kac2, kac3, 1.0])
            Application.activeWindow().activeView().setForeGroundColor(pigment_color)
        if doc[0] == "CMYKA":  # CMYK with bg_alpha channel
            pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
            pigment_color.setComponents([kac1, kac2, kac3, kac4, 1.0])
            Application.activeWindow().activeView().setForeGroundColor(pigment_color)
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
    def Krita_2_SOF(self):
        # Current Krita SOF
        view = Krita.instance().activeWindow().activeView()
        ks = view.brushSize()
        ko = view.paintingOpacity()
        kf = view.paintingFlow()
        return [ks, ko, kf]
    def SOF_2_Krita(self, mode, value):
        if mode == "SIZE":
            Krita.instance().activeWindow().activeView().setBrushSize(value)
        if mode == "OPACITY":
            Krita.instance().activeWindow().activeView().setPaintingOpacity(value)
        if mode == "FLOW":
            Krita.instance().activeWindow().activeView().setPaintingFlow(value)

    #//
    #\\ SOF ####################################################################
    def SOF_1_Minus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            sof = self.Krita_2_SOF()
            # Calculations
            sof[0] = sof[0] - (self.sof)
            if sof[0] <= 0:
                sof[0] = 0
            # Apply variation Color
            self.Pigment_2_Krita(sof[0], sof[1], sof[2], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def SOF_1_Plus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[1] = kac[1] + (self.rgb * unitRGB)
            if kac[1] >= 1:
                kac[1] = 1
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def SOF_2_Minus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[2] = kac[2] - (self.rgb * unitRGB)
            if kac[2] <= 0:
                kac[2] = 0
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def SOF_2_Plus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[2] = kac[2] + (self.rgb * unitRGB)
            if kac[2] >= 1:
                kac[2] = 1
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def SOF_3_Minus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[3] = kac[3] - (self.rgb * unitRGB)
            if kac[3] <= 0:
                kac[3] = 0
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def SOF_3_Plus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[3] = kac[3] + (self.rgb * unitRGB)
            if kac[3] >= 1:
                kac[3] = 1
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass

    #//
    #\\ RGB ####################################################################
    def RGB_1_Minus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[1] = kac[1] - (self.rgb * unitRGB)
            if kac[1] <= 0:
                kac[1] = 0
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def RGB_1_Plus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[1] = kac[1] + (self.rgb * unitRGB)
            if kac[1] >= 1:
                kac[1] = 1
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def RGB_2_Minus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[2] = kac[2] - (self.rgb * unitRGB)
            if kac[2] <= 0:
                kac[2] = 0
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def RGB_2_Plus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[2] = kac[2] + (self.rgb * unitRGB)
            if kac[2] >= 1:
                kac[2] = 1
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def RGB_3_Minus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[3] = kac[3] - (self.rgb * unitRGB)
            if kac[3] <= 0:
                kac[3] = 0
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass
    def RGB_3_Plus(self):
        try:
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            eraser = kritaEraserAction.isChecked()
            # Krita Values
            kac = self.Krita_2_Pigment()
            # Calculations
            kac[3] = kac[3] + (self.rgb * unitRGB)
            if kac[3] >= 1:
                kac[3] = 1
            # Apply variation Color
            self.Pigment_2_Krita(kac[1], kac[2], kac[3], 0)
            # Reactivate Eraser after Application
            if eraser == True:
                kritaEraserAction.trigger()
        except:
            pass

    #//
    #\\ Translate Color Space / Trignometry (range 0-1) ########################
    # AAA
    def rgb_to_aaa(self, r, g, b):
        aaa = math.sqrt( (0.299*r**2) + (0.587*g**2) + (0.114*b**2) )
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
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return [r, g, b]
    # Angle
    def rgb_to_angle(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        if minc == maxc:
            return [0.0]
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
    # HSL
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
    # HCY
    def rgb_to_hcy(self, r, g, b):
        y = lumaR*r + lumaG*g + lumaB*b
        p = max(r, g, b)
        n = min(r, g, b)
        d = p - n
        if n == p:
            h = 0.0
        elif p == r:
            h = (g - b)/d
            if h < 0:
                h += 6.0
        elif p == g:
            h = ((b - r)/d) + 2.0
        else:  # p==b
            h = ((r - g)/d) + 4.0
        h /= 6.0
        if r == g == b:
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
            tm = lumaR + lumaG * th
        elif h < 2:
            th = 2.0 - h
            tm = lumaG + lumaR * th
        elif h < 3:
            th = h - 2.0
            tm = lumaG + lumaB * th
        elif h < 4:
            th = 4.0 - h
            tm = lumaB + lumaG * th
        elif h < 5:
            th = h - 4.0
            tm = lumaB + lumaR * th
        else:
            th = 6.0 - h
            tm = lumaR + lumaB * th
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
        self.User_Interface()
        self.Menu_Shrink()

        # Modules and Connections
        self.Harmonys()
        self.Color_ofthe_Day()
        self.Panels()
        self.Dots()
        self.Object()
        self.Channels()
        self.Palette()
        self.Mixers()
        self.Style_Widget()

        # Settings
        self.Settings_Load_Misc()
        self.Settings_Load_ActiveColor()
        self.Settings_Load_UI()

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
        # Theme
        self.theme_krita = 59
        self.theme_pigment = 196
        self.gray_natural = self.HEX_6(self.theme_krita/255,self.theme_krita/255,self.theme_krita/255)
        self.gray_contrast = self.HEX_6(self.theme_pigment/255,self.theme_pigment/255,self.theme_pigment/255)
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
        self.layout.har_index.currentTextChanged.connect(lambda: self.Menu_HAR("SAVE"))
        self.layout.har_edit.toggled.connect(lambda: self.Menu_HAR("SAVE"))
        self.layout.pan_index.currentTextChanged.connect(lambda: self.Menu_PAN("SAVE"))
        self.layout.pan_secondary.currentTextChanged.connect(lambda: self.Menu_PAN("SAVE"))
        self.layout.obj_index.currentTextChanged.connect(lambda: self.Menu_OBJ("SAVE"))
        self.layout.obj_set.toggled.connect(lambda: self.OBJ_SET("SAVE"))
        self.layout.values.toggled.connect(lambda: self.Menu_Value("SAVE"))
        self.layout.mix_index.currentTextChanged.connect(lambda: self.Menu_MIX("SAVE"))
        self.layout.gray.toggled.connect(lambda: self.Menu_GRAY("SAVE"))
        # UI 2
        self.layout.sof.toggled.connect(lambda: self.Menu_SOF("SAVE"))
        self.layout.aaa.toggled.connect(lambda: self.Menu_AAA("SAVE"))
        self.layout.rgb.toggled.connect(lambda: self.Menu_RGB("SAVE"))
        self.layout.ard.toggled.connect(lambda: self.Menu_ARD("SAVE"))
        self.layout.hsv.toggled.connect(lambda: self.Menu_HSV("SAVE"))
        self.layout.hsl.toggled.connect(lambda: self.Menu_HSL("SAVE"))
        self.layout.hcy.toggled.connect(lambda: self.Menu_HCY("SAVE"))
        self.layout.cmy.toggled.connect(lambda: self.Menu_CMY("SAVE"))
        self.layout.cmyk.toggled.connect(lambda: self.Menu_CMYK("SAVE"))
        self.layout.kkk.toggled.connect(lambda: self.Menu_KKK("SAVE"))
        # UI 2
        self.layout.har.toggled.connect(lambda: self.Menu_HAR("SAVE"))
        self.layout.cotd.toggled.connect(lambda: self.Menu_COTD("SAVE"))
        self.layout.pan.toggled.connect(lambda: self.Menu_PAN("SAVE"))
        self.layout.obj.toggled.connect(lambda: self.Menu_OBJ("SAVE"))
        self.layout.dot.toggled.connect(lambda: self.Menu_DOT("SAVE"))
        self.layout.tip.toggled.connect(lambda: self.Menu_TIP("SAVE"))
        self.layout.tts.toggled.connect(lambda: self.Menu_TTS("SAVE"))
        self.layout.mix.toggled.connect(lambda: self.Menu_MIX("SAVE"))
        # UI 3
        self.layout.check.stateChanged.connect(self.Krita_TIMER)
        self.layout.menu.toggled.connect(lambda: self.Menu_UI2("SAVE"))
        self.layout.option.toggled.connect(lambda: self.Menu_UI1("SAVE"))
    def Harmonys(self):
        self.harmony_1 = Harmony(self.layout.harmony_1)
        self.harmony_1.SIGNAL_ACTIVE.connect(self.Harmony_1_Active)
        self.harmony_1.Update(self.layout.harmony_1.width(), self.layout.harmony_1.height())

        self.harmony_2 = Harmony(self.layout.harmony_2)
        self.harmony_2.SIGNAL_ACTIVE.connect(self.Harmony_2_Active)
        self.harmony_2.Update(self.layout.harmony_2.width(), self.layout.harmony_2.height())

        self.harmony_3 = Harmony(self.layout.harmony_3)
        self.harmony_3.SIGNAL_ACTIVE.connect(self.Harmony_3_Active)
        self.harmony_3.Update(self.layout.harmony_3.width(), self.layout.harmony_3.height())

        self.harmony_4 = Harmony(self.layout.harmony_4)
        self.harmony_4.SIGNAL_ACTIVE.connect(self.Harmony_4_Active)
        self.harmony_4.Update(self.layout.harmony_4.width(), self.layout.harmony_4.height())

        self.harmony_5 = Harmony(self.layout.harmony_5)
        self.harmony_5.SIGNAL_ACTIVE.connect(self.Harmony_5_Active)
        self.harmony_5.Update(self.layout.harmony_5.width(), self.layout.harmony_5.height())
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
        self.panel_uvd = Panel_UVD(self.layout.panel_uvd_input)
        self.panel_uvd.SIGNAL_UVD_VALUE.connect(self.Signal_UVD)
        self.panel_uvd.SIGNAL_UVD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_uvd.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel ARD
        self.panel_ard = Panel_ARD(self.layout.panel_ard_input)
        self.panel_ard.SIGNAL_ARD_VALUE.connect(self.Signal_ARD)
        self.panel_ard.SIGNAL_ARD_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_ard.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HSV
        self.panel_hsv = Panel_HSV_4(self.layout.panel_hsv)
        self.panel_hsv.SIGNAL_HSV_4_VALUE.connect(self.Signal_HSV_4)
        self.panel_hsv.SIGNAL_HSV_4_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsv.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HSL
        self.panel_hsl_4 = Panel_HSL_4(self.layout.panel_hsl)
        self.panel_hsl_4.SIGNAL_HSL_4_VALUE.connect(self.Signal_HSL_4)
        self.panel_hsl_4.SIGNAL_HSL_4_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_hsl_4.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

        # Panel HUE Circle
        self.panel_hue_circle = Panel_HUE_Circle(self.layout.panel_hue_circle_input)
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
    def Dots(self):
        # Display
        self.panel_dots = Panel_DOT(self.layout.panel_dot_mix)
        self.panel_dots.SIGNAL_DOT_VALUE.connect(self.Signal_DOT)
        self.panel_dots.SIGNAL_DOT_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_dots.SIGNAL_DOT_LOCATION.connect(self.Signal_DOT_Location)
        self.panel_dots.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)

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
    def Object(self):
        # Panel OBJ (Only updates the Cursor location)
        self.panel_obj = Panel_OBJ(self.layout.layer_cursor)
        self.panel_obj.SIGNAL_OBJ_PRESS.connect(self.Signal_OBJ)
        self.panel_obj.SIGNAL_OBJ_RELEASE.connect(self.Pigment_Display_Release)
        self.panel_obj.SIGNAL_OBJ_LOCATION.connect(self.Signal_OBJ_Location)

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
        self.layout.hcy_1_value.setMinimum(0)
        self.layout.hcy_2_value.setMinimum(0)
        self.layout.hcy_3_value.setMinimum(0)
        self.layout.cmy_1_value.setMinimum(0)
        self.layout.cmy_2_value.setMinimum(0)
        self.layout.cmy_3_value.setMinimum(0)
        self.layout.cmyk_1_value.setMinimum(0)
        self.layout.cmyk_2_value.setMinimum(0)
        self.layout.cmyk_3_value.setMinimum(0)
        self.layout.cmyk_4_value.setMinimum(0)
        self.layout.kkk_1_value.setMinimum(kritaKKKmin)
        self.layout.aaa_1_value.setMaximum(kritaAAA)
        self.layout.rgb_1_value.setMaximum(kritaRGB)
        self.layout.rgb_2_value.setMaximum(kritaRGB)
        self.layout.rgb_3_value.setMaximum(kritaRGB)
        self.layout.ard_1_value.setMaximum(kritaANG)
        self.layout.ard_2_value.setMaximum(kritaRDL)
        self.layout.ard_3_value.setMaximum(kritaRDL)
        self.layout.hsv_1_value.setMaximum(kritaHUE)
        self.layout.hsv_2_value.setMaximum(kritaSVLCY)
        self.layout.hsv_3_value.setMaximum(kritaSVLCY)
        self.layout.hsl_1_value.setMaximum(kritaHUE)
        self.layout.hsl_2_value.setMaximum(kritaSVLCY)
        self.layout.hsl_3_value.setMaximum(kritaSVLCY)
        self.layout.hcy_1_value.setMaximum(kritaHUE)
        self.layout.hcy_2_value.setMaximum(kritaSVLCY)
        self.layout.hcy_3_value.setMaximum(kritaSVLCY)
        self.layout.cmy_1_value.setMaximum(kritaCMY)
        self.layout.cmy_2_value.setMaximum(kritaCMY)
        self.layout.cmy_3_value.setMaximum(kritaCMY)
        self.layout.cmyk_1_value.setMaximum(kritaCMYK)
        self.layout.cmyk_2_value.setMaximum(kritaCMYK)
        self.layout.cmyk_3_value.setMaximum(kritaCMYK)
        self.layout.cmyk_4_value.setMaximum(kritaCMYK)
        self.layout.kkk_1_value.setMaximum(kritaKKKmax)
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
        self.sof_1_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_1_Slider_Modify)
        self.layout.sof_1_value.valueChanged.connect(self.Pigment_SOF_1_Value_Modify)
        # OPACITY
        self.sof_2_slider.SIGNAL_HALF.connect(lambda: self.SOF_2_APPLY(self.lock_opacity))
        self.sof_2_slider.SIGNAL_VALUE.connect(self.Pigment_SOF_2_Slider_Modify)
        self.layout.sof_2_value.valueChanged.connect(self.Pigment_SOF_2_Value_Modify)
        # FLOW
        self.sof_3_slider.SIGNAL_HALF.connect(lambda: self.SOF_3_APPLY(self.lock_flow))
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
        # Channel LUMA
        self.hcy_3_slider.SIGNAL_HALF.connect(self.Pigment_HCY_3_Half)
        self.hcy_3_slider.SIGNAL_MINUS.connect(self.Pigment_HCY_3_Minus)
        self.hcy_3_slider.SIGNAL_PLUS.connect(self.Pigment_HCY_3_Plus)
        self.hcy_3_slider.SIGNAL_VALUE.connect(self.Pigment_HCY_3_Slider_Modify)
        self.hcy_3_slider.SIGNAL_RELEASE.connect(self.Pigment_HCY_3_Slider_Release)
        self.hcy_3_slider.SIGNAL_ZOOM.connect(self.Pigment_Panel_Zoom)
        self.layout.hcy_3_value.valueChanged.connect(self.Pigment_HCY_3_Value_Modify)
        self.layout.hcy_3_value.editingFinished.connect(self.Pigment_HCY_3_Value_Release)

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
        self.palette_cor_00.SIGNAL_APPLY.connect(self.Color_00_APPLY)
        self.palette_cor_01.SIGNAL_APPLY.connect(self.Color_01_APPLY)
        self.palette_cor_02.SIGNAL_APPLY.connect(self.Color_02_APPLY)
        self.palette_cor_03.SIGNAL_APPLY.connect(self.Color_03_APPLY)
        self.palette_cor_04.SIGNAL_APPLY.connect(self.Color_04_APPLY)
        self.palette_cor_05.SIGNAL_APPLY.connect(self.Color_05_APPLY)
        self.palette_cor_06.SIGNAL_APPLY.connect(self.Color_06_APPLY)
        self.palette_cor_07.SIGNAL_APPLY.connect(self.Color_07_APPLY)
        self.palette_cor_08.SIGNAL_APPLY.connect(self.Color_08_APPLY)
        self.palette_cor_09.SIGNAL_APPLY.connect(self.Color_09_APPLY)
        self.palette_cor_10.SIGNAL_APPLY.connect(self.Color_10_APPLY)
        self.palette_cor_00.SIGNAL_SAVE.connect(self.Color_00_SAVE)
        self.palette_cor_01.SIGNAL_SAVE.connect(self.Color_01_SAVE)
        self.palette_cor_02.SIGNAL_SAVE.connect(self.Color_02_SAVE)
        self.palette_cor_03.SIGNAL_SAVE.connect(self.Color_03_SAVE)
        self.palette_cor_04.SIGNAL_SAVE.connect(self.Color_04_SAVE)
        self.palette_cor_05.SIGNAL_SAVE.connect(self.Color_05_SAVE)
        self.palette_cor_06.SIGNAL_SAVE.connect(self.Color_06_SAVE)
        self.palette_cor_07.SIGNAL_SAVE.connect(self.Color_07_SAVE)
        self.palette_cor_08.SIGNAL_SAVE.connect(self.Color_08_SAVE)
        self.palette_cor_09.SIGNAL_SAVE.connect(self.Color_09_SAVE)
        self.palette_cor_10.SIGNAL_SAVE.connect(self.Color_10_SAVE)
        self.palette_cor_00.SIGNAL_CLEAN.connect(self.Color_00_CLEAN)
        self.palette_cor_01.SIGNAL_CLEAN.connect(self.Color_01_CLEAN)
        self.palette_cor_02.SIGNAL_CLEAN.connect(self.Color_02_CLEAN)
        self.palette_cor_03.SIGNAL_CLEAN.connect(self.Color_03_CLEAN)
        self.palette_cor_04.SIGNAL_CLEAN.connect(self.Color_04_CLEAN)
        self.palette_cor_05.SIGNAL_CLEAN.connect(self.Color_05_CLEAN)
        self.palette_cor_06.SIGNAL_CLEAN.connect(self.Color_06_CLEAN)
        self.palette_cor_07.SIGNAL_CLEAN.connect(self.Color_07_CLEAN)
        self.palette_cor_08.SIGNAL_CLEAN.connect(self.Color_08_CLEAN)
        self.palette_cor_09.SIGNAL_CLEAN.connect(self.Color_09_CLEAN)
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
        # self.mixer_hcy_l1 = Clicks(self.layout.hcy_l1)
        # self.mixer_hcy_l2 = Clicks(self.layout.hcy_l2)
        # self.mixer_hcy_l3 = Clicks(self.layout.hcy_l3)
        # self.mixer_hcy_r1 = Clicks(self.layout.hcy_r1)
        # self.mixer_hcy_r2 = Clicks(self.layout.hcy_r2)
        # self.mixer_hcy_r3 = Clicks(self.layout.hcy_r3)
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
        # # HCY connection
        # self.mixer_hcy_l1.SIGNAL_APPLY.connect(self.Mixer_HCY_L1_APPLY)
        # self.mixer_hcy_r1.SIGNAL_APPLY.connect(self.Mixer_HCY_R1_APPLY)
        # self.mixer_hcy_l2.SIGNAL_APPLY.connect(self.Mixer_HCY_L2_APPLY)
        # self.mixer_hcy_r2.SIGNAL_APPLY.connect(self.Mixer_HCY_R2_APPLY)
        # self.mixer_hcy_l3.SIGNAL_APPLY.connect(self.Mixer_HCY_L3_APPLY)
        # self.mixer_hcy_r3.SIGNAL_APPLY.connect(self.Mixer_HCY_R3_APPLY)
        # self.mixer_hcy_l1.SIGNAL_SAVE.connect(self.Mixer_HCY_L1_SAVE)
        # self.mixer_hcy_r1.SIGNAL_SAVE.connect(self.Mixer_HCY_R1_SAVE)
        # self.mixer_hcy_l2.SIGNAL_SAVE.connect(self.Mixer_HCY_L2_SAVE)
        # self.mixer_hcy_r2.SIGNAL_SAVE.connect(self.Mixer_HCY_R2_SAVE)
        # self.mixer_hcy_l3.SIGNAL_SAVE.connect(self.Mixer_HCY_L3_SAVE)
        # self.mixer_hcy_r3.SIGNAL_SAVE.connect(self.Mixer_HCY_R3_SAVE)
        # self.mixer_hcy_l1.SIGNAL_CLEAN.connect(self.Mixer_HCY_L1_CLEAN)
        # self.mixer_hcy_r1.SIGNAL_CLEAN.connect(self.Mixer_HCY_R1_CLEAN)
        # self.mixer_hcy_l2.SIGNAL_CLEAN.connect(self.Mixer_HCY_L2_CLEAN)
        # self.mixer_hcy_r2.SIGNAL_CLEAN.connect(self.Mixer_HCY_R2_CLEAN)
        # self.mixer_hcy_l3.SIGNAL_CLEAN.connect(self.Mixer_HCY_L3_CLEAN)
        # self.mixer_hcy_r3.SIGNAL_CLEAN.connect(self.Mixer_HCY_R3_CLEAN)
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
        # self.mixer_hcy_g1 = Mixer_Gradient(self.layout.hcy_g1)
        # self.mixer_hcy_g2 = Mixer_Gradient(self.layout.hcy_g2)
        # self.mixer_hcy_g3 = Mixer_Gradient(self.layout.hcy_g3)
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
        # self.mixer_hcy_g1.SIGNAL_MIXER_VALUE.connect(self.Mixer_HCY_G1)
        # self.mixer_hcy_g2.SIGNAL_MIXER_VALUE.connect(self.Mixer_HCY_G2)
        # self.mixer_hcy_g3.SIGNAL_MIXER_VALUE.connect(self.Mixer_HCY_G3)
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
        # self.mixer_hcy_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        # self.mixer_hcy_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        # self.mixer_hcy_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g1.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g2.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
        self.mixer_cmyk_g3.SIGNAL_MIXER_RELEASE.connect(self.Pigment_Display_Release)
    def Style_Widget(self):
        # UI Percentage Gradients Display
        p4 = self.Percentage("4")
        p6 = self.Percentage("6")
        ten = self.Percentage("TEN")
        thirds = self.Percentage("3S")
        # Style Sheets
        self.layout.eraser.setStyleSheet(bg_alpha)
        self.layout.percentage_top.setStyleSheet(ten)
        self.layout.percentage_bot.setStyleSheet(ten)
        self.layout.label_percent.setStyleSheet(bg_unseen)
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
        self.layout.cmy_1_tick.setStyleSheet(p4)
        self.layout.cmy_2_tick.setStyleSheet(p4)
        self.layout.cmy_3_tick.setStyleSheet(p4)
        self.layout.cmyk_1_tick.setStyleSheet(p4)
        self.layout.cmyk_2_tick.setStyleSheet(p4)
        self.layout.cmyk_3_tick.setStyleSheet(p4)
        self.layout.cmyk_4_tick.setStyleSheet(p4)
        self.layout.kkk_1_tick.setStyleSheet(p4)
        self.layout.panel_ard.setStyleSheet(thirds)
        self.layout.panel_uvd.setStyleSheet(bg_alpha)
        self.layout.tip_00.setStyleSheet(bg_alpha)
        self.layout.panel_dot_mix.setStyleSheet(bg_alpha)
        self.layout.dot_1.setStyleSheet(bg_alpha)
        self.layout.dot_2.setStyleSheet(bg_alpha)
        self.layout.dot_3.setStyleSheet(bg_alpha)
        self.layout.dot_4.setStyleSheet(bg_alpha)

        # Icons Module
        self.icon_left = self.Icon_Left(self.gray_contrast)
        self.icon_right = self.Icon_Right(self.gray_contrast)
        self.icon_panel = self.Icon_Panel(self.gray_contrast)
        self.icon_corner = self.Icon_Corner(self.gray_contrast)
        self.icon_lock = self.Icon_Lock(self.gray_contrast)
        self.icon_menu = self.Icon_Menu(self.gray_contrast)
        self.icon_slider = self.Icon_Slider(self.gray_contrast)

        # Icon SVG Operation
        self.svg_option = QtSvg.QSvgWidget(self.layout.option)
        self.svg_option.load(self.icon_corner)
        self.svg_menu = QtSvg.QSvgWidget(self.layout.menu)
        self.svg_menu.load(self.icon_menu)
        self.svg_lock_kkk_1 = QtSvg.QSvgWidget(self.layout.kkk_1_lock)
        self.svg_lock_kkk_1.load(self.icon_lock)

    #//
    #\\ Menu Displays ##########################################################
    def Menu_UI1(self, save):
        if self.layout.option.isChecked() == True:
            # Icon
            self.icon_corner = self.Icon_Corner(self.color_accent)
            self.svg_option.load(self.icon_corner)
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
            self.layout.obj.setMinimumHeight(ui_menu)
            self.layout.obj.setMaximumHeight(ui_menu)
            self.layout.dot.setMinimumHeight(ui_menu)
            self.layout.dot.setMaximumHeight(ui_menu)
            self.layout.tip.setMinimumHeight(ui_menu)
            self.layout.tip.setMaximumHeight(ui_menu)
            self.layout.tts.setMinimumHeight(ui_menu)
            self.layout.tts.setMaximumHeight(ui_menu)
            self.layout.mix.setMinimumHeight(ui_menu)
            self.layout.mix.setMaximumHeight(ui_menu)
            # Spacing
            self.layout.options_1.setContentsMargins(zero, zero, zero, zero)
            self.layout.options_2.setContentsMargins(zero, zero, zero, zero)
        else:
            # Icon
            self.icon_corner = self.Icon_Corner(self.gray_contrast)
            self.svg_option.load(self.icon_corner)
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
            self.layout.obj.setMinimumHeight(zero)
            self.layout.obj.setMaximumHeight(zero)
            self.layout.dot.setMinimumHeight(zero)
            self.layout.dot.setMaximumHeight(zero)
            self.layout.tip.setMinimumHeight(zero)
            self.layout.tip.setMaximumHeight(zero)
            self.layout.tts.setMinimumHeight(zero)
            self.layout.tts.setMaximumHeight(zero)
            self.layout.mix.setMinimumHeight(zero)
            self.layout.mix.setMaximumHeight(zero)
            # Spacing
            self.layout.options_1.setContentsMargins(zero, zero, zero, zero)
            self.layout.options_2.setContentsMargins(zero, zero, zero, zero)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_UI2(self, save):
        if self.layout.menu.isChecked() == True:
            # Icon
            self.icon_menu = self.Icon_Menu(self.color_accent)
            self.svg_menu.load(self.icon_menu)
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
            # Object
            self.layout.menu_object.setMinimumHeight(ui_20)
            self.layout.menu_object.setMaximumHeight(ui_20)
            self.layout.obj_index.setMinimumHeight(ui_20)
            self.layout.obj_index.setMaximumHeight(ui_20)
            self.layout.obj_set.setMinimumHeight(ui_20)
            self.layout.obj_set.setMaximumHeight(ui_20)
            # Channels
            self.layout.menu_values.setMinimumHeight(ui_20)
            self.layout.menu_values.setMaximumHeight(ui_20)
            self.layout.values.setMinimumHeight(ui_20)
            self.layout.values.setMaximumHeight(ui_20)
            # Mixer
            self.layout.menu_mixer.setMinimumHeight(ui_20)
            self.layout.menu_mixer.setMaximumHeight(ui_20)
            self.layout.mix_index.setMinimumHeight(ui_20)
            self.layout.mix_index.setMaximumHeight(ui_20)
            # Gray Mode
            self.layout.menu_gray.setMinimumHeight(ui_20)
            self.layout.menu_gray.setMaximumHeight(ui_20)
            self.layout.gray.setMinimumHeight(ui_20)
            self.layout.gray.setMaximumHeight(ui_20)
            # Spacing
            self.layout.options_3.setContentsMargins(10, 10, 10, 10)
            self.layout.options_3.setSpacing(6)
        else:
            # Icon
            self.icon_menu = self.Icon_Menu(self.gray_contrast)
            self.svg_menu.load(self.icon_menu)
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
            # Object
            self.layout.menu_object.setMinimumHeight(zero)
            self.layout.menu_object.setMaximumHeight(zero)
            self.layout.obj_index.setMinimumHeight(zero)
            self.layout.obj_index.setMaximumHeight(zero)
            self.layout.obj_set.setMinimumHeight(zero)
            self.layout.obj_set.setMaximumHeight(zero)
            # Channels
            self.layout.menu_values.setMinimumHeight(zero)
            self.layout.menu_values.setMaximumHeight(zero)
            self.layout.values.setMinimumHeight(zero)
            self.layout.values.setMaximumHeight(zero)
            # Mixer
            self.layout.menu_mixer.setMinimumHeight(zero)
            self.layout.menu_mixer.setMaximumHeight(zero)
            self.layout.mix_index.setMinimumHeight(zero)
            self.layout.mix_index.setMaximumHeight(zero)
            # Gray Mode
            self.layout.menu_gray.setMinimumHeight(zero)
            self.layout.menu_gray.setMaximumHeight(zero)
            self.layout.gray.setMinimumHeight(zero)
            self.layout.gray.setMaximumHeight(zero)
            # Spacing
            self.layout.options_3.setContentsMargins(zero, zero, zero, zero)
            self.layout.options_3.setSpacing(0)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_Value(self, save):
        val = self.layout.values.isChecked()
        if val == True:
            # HEX
            self.layout.hex_string.setMinimumWidth(ui_50)
            self.layout.hex_string.setMaximumWidth(ui_70)
            # SOF
            self.layout.sof_1_value.setMinimumWidth(ui_50)
            self.layout.sof_1_value.setMaximumWidth(ui_70)
            self.layout.sof_2_value.setMinimumWidth(ui_50)
            self.layout.sof_2_value.setMaximumWidth(ui_70)
            self.layout.sof_3_value.setMinimumWidth(ui_50)
            self.layout.sof_3_value.setMaximumWidth(ui_70)
            # AAA
            self.layout.aaa_1_value.setMinimumWidth(ui_50)
            self.layout.aaa_1_value.setMaximumWidth(ui_70)
            # RGB
            self.layout.rgb_1_value.setMinimumWidth(ui_50)
            self.layout.rgb_1_value.setMaximumWidth(ui_70)
            self.layout.rgb_2_value.setMinimumWidth(ui_50)
            self.layout.rgb_2_value.setMaximumWidth(ui_70)
            self.layout.rgb_3_value.setMinimumWidth(ui_50)
            self.layout.rgb_3_value.setMaximumWidth(ui_70)
            # ARD
            self.layout.ard_1_value.setMinimumWidth(ui_50)
            self.layout.ard_1_value.setMaximumWidth(ui_70)
            self.layout.ard_2_value.setMinimumWidth(ui_50)
            self.layout.ard_2_value.setMaximumWidth(ui_70)
            self.layout.ard_3_value.setMinimumWidth(ui_50)
            self.layout.ard_3_value.setMaximumWidth(ui_70)
            # HSV
            self.layout.hsv_1_value.setMinimumWidth(ui_50)
            self.layout.hsv_1_value.setMaximumWidth(ui_70)
            self.layout.hsv_2_value.setMinimumWidth(ui_50)
            self.layout.hsv_2_value.setMaximumWidth(ui_70)
            self.layout.hsv_3_value.setMinimumWidth(ui_50)
            self.layout.hsv_3_value.setMaximumWidth(ui_70)
            # HSL
            self.layout.hsl_1_value.setMinimumWidth(ui_50)
            self.layout.hsl_1_value.setMaximumWidth(ui_70)
            self.layout.hsl_2_value.setMinimumWidth(ui_50)
            self.layout.hsl_2_value.setMaximumWidth(ui_70)
            self.layout.hsl_3_value.setMinimumWidth(ui_50)
            self.layout.hsl_3_value.setMaximumWidth(ui_70)
            # HCY
            self.layout.hcy_1_value.setMinimumWidth(ui_50)
            self.layout.hcy_1_value.setMaximumWidth(ui_70)
            self.layout.hcy_2_value.setMinimumWidth(ui_50)
            self.layout.hcy_2_value.setMaximumWidth(ui_70)
            self.layout.hcy_3_value.setMinimumWidth(ui_50)
            self.layout.hcy_3_value.setMaximumWidth(ui_70)
            # CMY
            self.layout.cmy_1_value.setMinimumWidth(ui_50)
            self.layout.cmy_1_value.setMaximumWidth(ui_70)
            self.layout.cmy_2_value.setMinimumWidth(ui_50)
            self.layout.cmy_2_value.setMaximumWidth(ui_70)
            self.layout.cmy_3_value.setMinimumWidth(ui_50)
            self.layout.cmy_3_value.setMaximumWidth(ui_70)
            # CMYK
            self.layout.cmyk_1_value.setMinimumWidth(ui_50)
            self.layout.cmyk_1_value.setMaximumWidth(ui_70)
            self.layout.cmyk_2_value.setMinimumWidth(ui_50)
            self.layout.cmyk_2_value.setMaximumWidth(ui_70)
            self.layout.cmyk_3_value.setMinimumWidth(ui_50)
            self.layout.cmyk_3_value.setMaximumWidth(ui_70)
            self.layout.cmyk_4_value.setMinimumWidth(ui_50)
            self.layout.cmyk_4_value.setMaximumWidth(ui_70)
            # KKK
            self.layout.kkk_1_value.setMinimumWidth(ui_50)
            self.layout.kkk_1_value.setMaximumWidth(ui_70)
            # Percentage
            self.layout.percentage_bot_value.setMinimumWidth(ui_50)
            self.layout.percentage_bot_value.setMaximumWidth(ui_70)
        else:
            # Hex
            self.layout.hex_string.setMinimumWidth(zero)
            self.layout.hex_string.setMaximumWidth(zero)
            # SOF
            self.layout.sof_1_value.setMinimumWidth(zero)
            self.layout.sof_1_value.setMaximumWidth(zero)
            self.layout.sof_2_value.setMinimumWidth(zero)
            self.layout.sof_2_value.setMaximumWidth(zero)
            self.layout.sof_3_value.setMinimumWidth(zero)
            self.layout.sof_3_value.setMaximumWidth(zero)
            # AAA
            self.layout.aaa_1_value.setMinimumWidth(zero)
            self.layout.aaa_1_value.setMaximumWidth(zero)
            # RGB
            self.layout.rgb_1_value.setMinimumWidth(zero)
            self.layout.rgb_1_value.setMaximumWidth(zero)
            self.layout.rgb_2_value.setMinimumWidth(zero)
            self.layout.rgb_2_value.setMaximumWidth(zero)
            self.layout.rgb_3_value.setMinimumWidth(zero)
            self.layout.rgb_3_value.setMaximumWidth(zero)
            # ARD
            self.layout.ard_1_value.setMinimumWidth(zero)
            self.layout.ard_1_value.setMaximumWidth(zero)
            self.layout.ard_2_value.setMinimumWidth(zero)
            self.layout.ard_2_value.setMaximumWidth(zero)
            self.layout.ard_3_value.setMinimumWidth(zero)
            self.layout.ard_3_value.setMaximumWidth(zero)
            # HSV
            self.layout.hsv_1_value.setMinimumWidth(zero)
            self.layout.hsv_1_value.setMaximumWidth(zero)
            self.layout.hsv_2_value.setMinimumWidth(zero)
            self.layout.hsv_2_value.setMaximumWidth(zero)
            self.layout.hsv_3_value.setMinimumWidth(zero)
            self.layout.hsv_3_value.setMaximumWidth(zero)
            # HSL
            self.layout.hsl_1_value.setMinimumWidth(zero)
            self.layout.hsl_1_value.setMaximumWidth(zero)
            self.layout.hsl_2_value.setMinimumWidth(zero)
            self.layout.hsl_2_value.setMaximumWidth(zero)
            self.layout.hsl_3_value.setMinimumWidth(zero)
            self.layout.hsl_3_value.setMaximumWidth(zero)
            # HCY
            self.layout.hcy_1_value.setMinimumWidth(zero)
            self.layout.hcy_1_value.setMaximumWidth(zero)
            self.layout.hcy_2_value.setMinimumWidth(zero)
            self.layout.hcy_2_value.setMaximumWidth(zero)
            self.layout.hcy_3_value.setMinimumWidth(zero)
            self.layout.hcy_3_value.setMaximumWidth(zero)
            # CMY
            self.layout.cmy_1_value.setMinimumWidth(zero)
            self.layout.cmy_1_value.setMaximumWidth(zero)
            self.layout.cmy_2_value.setMinimumWidth(zero)
            self.layout.cmy_2_value.setMaximumWidth(zero)
            self.layout.cmy_3_value.setMinimumWidth(zero)
            self.layout.cmy_3_value.setMaximumWidth(zero)
            # CMYK
            self.layout.cmyk_1_value.setMinimumWidth(zero)
            self.layout.cmyk_1_value.setMaximumWidth(zero)
            self.layout.cmyk_2_value.setMinimumWidth(zero)
            self.layout.cmyk_2_value.setMaximumWidth(zero)
            self.layout.cmyk_3_value.setMinimumWidth(zero)
            self.layout.cmyk_3_value.setMaximumWidth(zero)
            self.layout.cmyk_4_value.setMinimumWidth(zero)
            self.layout.cmyk_4_value.setMaximumWidth(zero)
            # KKK
            self.layout.kkk_1_value.setMinimumWidth(zero)
            self.layout.kkk_1_value.setMaximumWidth(zero)
            # Percentage
            self.layout.percentage_bot_value.setMinimumWidth(zero)
            self.layout.percentage_bot_value.setMaximumWidth(zero)
        self.update()
        if save == "SAVE":
            self.Spacer_Gap()
            self.Ratio()
            self.Settings_Save_UI()
    def Menu_GRAY(self, save):
        if self.layout.gray.isChecked() == True:
            self.gray = True
        else:
            self.gray = False
        self.Pigment_Display()
        self.Mixer_Display()
        if save == "SAVE":
            self.Settings_Save_UI()
    # Channels
    def Menu_SOF(self, save):
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
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_AAA(self, save):
        font = self.layout.aaa.font()
        if self.layout.aaa.isChecked():
            font.setBold(True)
            self.chan_aaa = True
            self.layout.aaa_1_slider.setMinimumHeight(ui_10)
            self.layout.aaa_1_slider.setMaximumHeight(ui_20)
            self.layout.aaa_1_value.setMinimumHeight(ui_10)
            self.layout.aaa_1_value.setMaximumHeight(ui_20)
            self.layout.aaa_1_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_aaa = False
            self.layout.aaa_1_slider.setMinimumHeight(zero)
            self.layout.aaa_1_slider.setMaximumHeight(zero)
            self.layout.aaa_1_value.setMinimumHeight(zero)
            self.layout.aaa_1_value.setMaximumHeight(zero)
            self.layout.aaa_1_tick.setMinimumHeight(zero)
        self.layout.aaa.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_RGB(self, save):
        font = self.layout.rgb.font()
        if self.layout.rgb.isChecked():
            font.setBold(True)
            self.chan_rgb = True
            self.layout.rgb_1_slider.setMinimumHeight(ui_10)
            self.layout.rgb_1_slider.setMaximumHeight(ui_20)
            self.layout.rgb_1_value.setMinimumHeight(ui_10)
            self.layout.rgb_1_value.setMaximumHeight(ui_20)
            self.layout.rgb_1_tick.setMinimumHeight(unit)
            self.layout.rgb_2_slider.setMinimumHeight(ui_10)
            self.layout.rgb_2_slider.setMaximumHeight(ui_20)
            self.layout.rgb_2_value.setMinimumHeight(ui_10)
            self.layout.rgb_2_value.setMaximumHeight(ui_20)
            self.layout.rgb_2_tick.setMinimumHeight(unit)
            self.layout.rgb_3_slider.setMinimumHeight(ui_10)
            self.layout.rgb_3_slider.setMaximumHeight(ui_20)
            self.layout.rgb_3_value.setMinimumHeight(ui_10)
            self.layout.rgb_3_value.setMaximumHeight(ui_20)
            self.layout.rgb_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_rgb = False
            self.layout.rgb_1_slider.setMinimumHeight(zero)
            self.layout.rgb_1_slider.setMaximumHeight(zero)
            self.layout.rgb_1_value.setMinimumHeight(zero)
            self.layout.rgb_1_value.setMaximumHeight(zero)
            self.layout.rgb_1_tick.setMinimumHeight(zero)
            self.layout.rgb_2_slider.setMinimumHeight(zero)
            self.layout.rgb_2_slider.setMaximumHeight(zero)
            self.layout.rgb_2_value.setMinimumHeight(zero)
            self.layout.rgb_2_value.setMaximumHeight(zero)
            self.layout.rgb_2_tick.setMinimumHeight(zero)
            self.layout.rgb_3_slider.setMinimumHeight(zero)
            self.layout.rgb_3_slider.setMaximumHeight(zero)
            self.layout.rgb_3_value.setMinimumHeight(zero)
            self.layout.rgb_3_value.setMaximumHeight(zero)
            self.layout.rgb_3_tick.setMinimumHeight(zero)
        self.layout.rgb.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_ARD(self, save):
        font = self.layout.ard.font()
        if self.layout.ard.isChecked():
            font.setBold(True)
            self.chan_ard = True
            self.layout.ard_1_slider.setMinimumHeight(ui_10)
            self.layout.ard_1_slider.setMaximumHeight(ui_20)
            self.layout.ard_1_value.setMinimumHeight(ui_10)
            self.layout.ard_1_value.setMaximumHeight(ui_20)
            self.layout.ard_1_tick.setMinimumHeight(unit)
            self.layout.ard_2_slider.setMinimumHeight(ui_10)
            self.layout.ard_2_slider.setMaximumHeight(ui_20)
            self.layout.ard_2_value.setMinimumHeight(ui_10)
            self.layout.ard_2_value.setMaximumHeight(ui_20)
            self.layout.ard_2_tick.setMinimumHeight(unit)
            self.layout.ard_3_slider.setMinimumHeight(ui_10)
            self.layout.ard_3_slider.setMaximumHeight(ui_20)
            self.layout.ard_3_value.setMinimumHeight(ui_10)
            self.layout.ard_3_value.setMaximumHeight(ui_20)
            self.layout.ard_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_ard = False
            self.layout.ard_1_slider.setMinimumHeight(zero)
            self.layout.ard_1_slider.setMaximumHeight(zero)
            self.layout.ard_1_value.setMinimumHeight(zero)
            self.layout.ard_1_value.setMaximumHeight(zero)
            self.layout.ard_1_tick.setMinimumHeight(zero)
            self.layout.ard_2_slider.setMinimumHeight(zero)
            self.layout.ard_2_slider.setMaximumHeight(zero)
            self.layout.ard_2_value.setMinimumHeight(zero)
            self.layout.ard_2_value.setMaximumHeight(zero)
            self.layout.ard_2_tick.setMinimumHeight(zero)
            self.layout.ard_3_slider.setMinimumHeight(zero)
            self.layout.ard_3_slider.setMaximumHeight(zero)
            self.layout.ard_3_value.setMinimumHeight(zero)
            self.layout.ard_3_value.setMaximumHeight(zero)
            self.layout.ard_3_tick.setMinimumHeight(zero)
        self.layout.ard.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_HSV(self, save):
        font = self.layout.hsv.font()
        if self.layout.hsv.isChecked():
            font.setBold(True)
            self.chan_hsv = True
            self.layout.hsv_1_slider.setMinimumHeight(ui_10)
            self.layout.hsv_1_slider.setMaximumHeight(ui_20)
            self.layout.hsv_1_value.setMinimumHeight(ui_10)
            self.layout.hsv_1_value.setMaximumHeight(ui_20)
            self.layout.hsv_1_tick.setMinimumHeight(unit)
            self.layout.hsv_2_slider.setMinimumHeight(ui_10)
            self.layout.hsv_2_slider.setMaximumHeight(ui_20)
            self.layout.hsv_2_value.setMinimumHeight(ui_10)
            self.layout.hsv_2_value.setMaximumHeight(ui_20)
            self.layout.hsv_2_tick.setMinimumHeight(unit)
            self.layout.hsv_3_slider.setMinimumHeight(ui_10)
            self.layout.hsv_3_slider.setMaximumHeight(ui_20)
            self.layout.hsv_3_value.setMinimumHeight(ui_10)
            self.layout.hsv_3_value.setMaximumHeight(ui_20)
            self.layout.hsv_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_hsv = False
            self.layout.hsv_1_slider.setMinimumHeight(zero)
            self.layout.hsv_1_slider.setMaximumHeight(zero)
            self.layout.hsv_1_value.setMinimumHeight(zero)
            self.layout.hsv_1_value.setMaximumHeight(zero)
            self.layout.hsv_1_tick.setMinimumHeight(zero)
            self.layout.hsv_2_slider.setMinimumHeight(zero)
            self.layout.hsv_2_slider.setMaximumHeight(zero)
            self.layout.hsv_2_value.setMinimumHeight(zero)
            self.layout.hsv_2_value.setMaximumHeight(zero)
            self.layout.hsv_2_tick.setMinimumHeight(zero)
            self.layout.hsv_3_slider.setMinimumHeight(zero)
            self.layout.hsv_3_slider.setMaximumHeight(zero)
            self.layout.hsv_3_value.setMinimumHeight(zero)
            self.layout.hsv_3_value.setMaximumHeight(zero)
            self.layout.hsv_3_tick.setMinimumHeight(zero)
        self.layout.hsv.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_HSL(self, save):
        font = self.layout.hsl.font()
        if self.layout.hsl.isChecked():
            font.setBold(True)
            self.chan_hsl = True
            self.layout.hsl_1_slider.setMinimumHeight(ui_10)
            self.layout.hsl_1_slider.setMaximumHeight(ui_20)
            self.layout.hsl_1_value.setMinimumHeight(ui_10)
            self.layout.hsl_1_value.setMaximumHeight(ui_20)
            self.layout.hsl_1_tick.setMinimumHeight(unit)
            self.layout.hsl_2_slider.setMinimumHeight(ui_10)
            self.layout.hsl_2_slider.setMaximumHeight(ui_20)
            self.layout.hsl_2_value.setMinimumHeight(ui_10)
            self.layout.hsl_2_value.setMaximumHeight(ui_20)
            self.layout.hsl_2_tick.setMinimumHeight(unit)
            self.layout.hsl_3_slider.setMinimumHeight(ui_10)
            self.layout.hsl_3_slider.setMaximumHeight(ui_20)
            self.layout.hsl_3_value.setMinimumHeight(ui_10)
            self.layout.hsl_3_value.setMaximumHeight(ui_20)
            self.layout.hsl_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_hsl = False
            self.layout.hsl_1_slider.setMinimumHeight(zero)
            self.layout.hsl_1_slider.setMaximumHeight(zero)
            self.layout.hsl_1_value.setMinimumHeight(zero)
            self.layout.hsl_1_value.setMaximumHeight(zero)
            self.layout.hsl_1_tick.setMinimumHeight(zero)
            self.layout.hsl_2_slider.setMinimumHeight(zero)
            self.layout.hsl_2_slider.setMaximumHeight(zero)
            self.layout.hsl_2_value.setMinimumHeight(zero)
            self.layout.hsl_2_value.setMaximumHeight(zero)
            self.layout.hsl_2_tick.setMinimumHeight(zero)
            self.layout.hsl_3_slider.setMinimumHeight(zero)
            self.layout.hsl_3_slider.setMaximumHeight(zero)
            self.layout.hsl_3_value.setMinimumHeight(zero)
            self.layout.hsl_3_value.setMaximumHeight(zero)
            self.layout.hsl_3_tick.setMinimumHeight(zero)
        self.layout.hsl.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_HCY(self, save):
        font = self.layout.hcy.font()
        if self.layout.hcy.isChecked():
            font.setBold(True)
            self.chan_hcy = True
            self.layout.hcy_1_slider.setMinimumHeight(ui_10)
            self.layout.hcy_1_slider.setMaximumHeight(ui_20)
            self.layout.hcy_1_value.setMinimumHeight(ui_10)
            self.layout.hcy_1_value.setMaximumHeight(ui_20)
            self.layout.hcy_1_tick.setMinimumHeight(unit)
            self.layout.hcy_2_slider.setMinimumHeight(ui_10)
            self.layout.hcy_2_slider.setMaximumHeight(ui_20)
            self.layout.hcy_2_value.setMinimumHeight(ui_10)
            self.layout.hcy_2_value.setMaximumHeight(ui_20)
            self.layout.hcy_2_tick.setMinimumHeight(unit)
            self.layout.hcy_3_slider.setMinimumHeight(ui_10)
            self.layout.hcy_3_slider.setMaximumHeight(ui_20)
            self.layout.hcy_3_value.setMinimumHeight(ui_10)
            self.layout.hcy_3_value.setMaximumHeight(ui_20)
            self.layout.hcy_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_hcy = False
            self.layout.hcy_1_slider.setMinimumHeight(zero)
            self.layout.hcy_1_slider.setMaximumHeight(zero)
            self.layout.hcy_1_value.setMinimumHeight(zero)
            self.layout.hcy_1_value.setMaximumHeight(zero)
            self.layout.hcy_1_tick.setMinimumHeight(zero)
            self.layout.hcy_2_slider.setMinimumHeight(zero)
            self.layout.hcy_2_slider.setMaximumHeight(zero)
            self.layout.hcy_2_value.setMinimumHeight(zero)
            self.layout.hcy_2_value.setMaximumHeight(zero)
            self.layout.hcy_2_tick.setMinimumHeight(zero)
            self.layout.hcy_3_slider.setMinimumHeight(zero)
            self.layout.hcy_3_slider.setMaximumHeight(zero)
            self.layout.hcy_3_value.setMinimumHeight(zero)
            self.layout.hcy_3_value.setMaximumHeight(zero)
            self.layout.hcy_3_tick.setMinimumHeight(zero)
        self.layout.hcy.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_CMY(self, save):
        font = self.layout.cmy.font()
        if self.layout.cmy.isChecked():
            font.setBold(True)
            self.chan_cmy = True
            self.layout.cmy_1_slider.setMinimumHeight(ui_10)
            self.layout.cmy_1_slider.setMaximumHeight(ui_20)
            self.layout.cmy_1_value.setMinimumHeight(ui_10)
            self.layout.cmy_1_value.setMaximumHeight(ui_20)
            self.layout.cmy_1_tick.setMinimumHeight(unit)
            self.layout.cmy_2_slider.setMinimumHeight(ui_10)
            self.layout.cmy_2_slider.setMaximumHeight(ui_20)
            self.layout.cmy_2_value.setMinimumHeight(ui_10)
            self.layout.cmy_2_value.setMaximumHeight(ui_20)
            self.layout.cmy_2_tick.setMinimumHeight(unit)
            self.layout.cmy_3_slider.setMinimumHeight(ui_10)
            self.layout.cmy_3_slider.setMaximumHeight(ui_20)
            self.layout.cmy_3_value.setMinimumHeight(ui_10)
            self.layout.cmy_3_value.setMaximumHeight(ui_20)
            self.layout.cmy_3_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_cmy = False
            self.layout.cmy_1_slider.setMinimumHeight(zero)
            self.layout.cmy_1_slider.setMaximumHeight(zero)
            self.layout.cmy_1_value.setMinimumHeight(zero)
            self.layout.cmy_1_value.setMaximumHeight(zero)
            self.layout.cmy_1_tick.setMinimumHeight(zero)
            self.layout.cmy_2_slider.setMinimumHeight(zero)
            self.layout.cmy_2_slider.setMaximumHeight(zero)
            self.layout.cmy_2_value.setMinimumHeight(zero)
            self.layout.cmy_2_value.setMaximumHeight(zero)
            self.layout.cmy_2_tick.setMinimumHeight(zero)
            self.layout.cmy_3_slider.setMinimumHeight(zero)
            self.layout.cmy_3_slider.setMaximumHeight(zero)
            self.layout.cmy_3_value.setMinimumHeight(zero)
            self.layout.cmy_3_value.setMaximumHeight(zero)
            self.layout.cmy_3_tick.setMinimumHeight(zero)
        self.layout.cmy.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_CMYK(self, save):
        font = self.layout.cmyk.font()
        if self.layout.cmyk.isChecked():
            font.setBold(True)
            self.chan_cmyk = True
            self.layout.cmyk_1_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_1_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_1_value.setMinimumHeight(ui_10)
            self.layout.cmyk_1_value.setMaximumHeight(ui_20)
            self.layout.cmyk_1_tick.setMinimumHeight(unit)
            self.layout.cmyk_2_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_2_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_2_value.setMinimumHeight(ui_10)
            self.layout.cmyk_2_value.setMaximumHeight(ui_20)
            self.layout.cmyk_2_tick.setMinimumHeight(unit)
            self.layout.cmyk_3_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_3_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_3_value.setMinimumHeight(ui_10)
            self.layout.cmyk_3_value.setMaximumHeight(ui_20)
            self.layout.cmyk_3_tick.setMinimumHeight(unit)
            self.layout.cmyk_4_slider.setMinimumHeight(ui_10)
            self.layout.cmyk_4_slider.setMaximumHeight(ui_20)
            self.layout.cmyk_4_value.setMinimumHeight(ui_10)
            self.layout.cmyk_4_value.setMaximumHeight(ui_20)
            self.layout.cmyk_4_tick.setMinimumHeight(unit)
        else:
            font.setBold(False)
            self.chan_cmyk = False
            self.layout.cmyk_1_slider.setMinimumHeight(zero)
            self.layout.cmyk_1_slider.setMaximumHeight(zero)
            self.layout.cmyk_1_value.setMinimumHeight(zero)
            self.layout.cmyk_1_value.setMaximumHeight(zero)
            self.layout.cmyk_1_tick.setMinimumHeight(zero)
            self.layout.cmyk_2_slider.setMinimumHeight(zero)
            self.layout.cmyk_2_slider.setMaximumHeight(zero)
            self.layout.cmyk_2_value.setMinimumHeight(zero)
            self.layout.cmyk_2_value.setMaximumHeight(zero)
            self.layout.cmyk_2_tick.setMinimumHeight(zero)
            self.layout.cmyk_3_slider.setMinimumHeight(zero)
            self.layout.cmyk_3_slider.setMaximumHeight(zero)
            self.layout.cmyk_3_value.setMinimumHeight(zero)
            self.layout.cmyk_3_value.setMaximumHeight(zero)
            self.layout.cmyk_3_tick.setMinimumHeight(zero)
            self.layout.cmyk_4_slider.setMinimumHeight(zero)
            self.layout.cmyk_4_slider.setMaximumHeight(zero)
            self.layout.cmyk_4_value.setMinimumHeight(zero)
            self.layout.cmyk_4_value.setMaximumHeight(zero)
            self.layout.cmyk_4_tick.setMinimumHeight(zero)
        self.layout.cmyk.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_KKK(self, save):
        font = self.layout.kkk.font()
        if self.layout.kkk.isChecked():
            font.setBold(True)
            self.chan_kkk = True
            self.layout.kkk_1_slider.setMinimumHeight(ui_10)
            self.layout.kkk_1_slider.setMaximumHeight(ui_20)
            self.layout.kkk_1_value.setMinimumHeight(ui_10)
            self.layout.kkk_1_value.setMaximumHeight(ui_20)
            self.layout.kkk_1_tick.setMinimumHeight(unit)
            self.layout.kkk_1_tick.setMaximumHeight(unit)
            self.layout.kkk_1_lock.setMinimumHeight(ui_10)
            self.layout.kkk_1_lock.setMaximumHeight(ui_20)
        else:
            font.setBold(False)
            self.chan_kkk = False
            self.layout.kkk_1_slider.setMinimumHeight(zero)
            self.layout.kkk_1_slider.setMaximumHeight(zero)
            self.layout.kkk_1_value.setMinimumHeight(zero)
            self.layout.kkk_1_value.setMaximumHeight(zero)
            self.layout.kkk_1_tick.setMinimumHeight(zero)
            self.layout.kkk_1_tick.setMaximumHeight(zero)
            self.layout.kkk_1_lock.setMinimumHeight(zero)
            self.layout.kkk_1_lock.setMaximumHeight(zero)
        self.layout.kkk.setFont(font)
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    # Header
    def Menu_HAR(self, save):
        font = self.layout.har.font()
        har_active = self.layout.har.isChecked()
        har_index = self.layout.har_index.currentText()
        if har_active == False:
            font.setBold(False)
            self.harmony_active = 0
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
        if (har_active == True and har_index == "Monochromatic"):
            font.setBold(True)
            self.harmony_index = "Monochromatic"
            self.harmony_active = 3
            self.layout.color_1.setMinimumHeight(ui_10)
            self.layout.color_1.setMaximumHeight(ui_10)
            self.layout.color_2.setMinimumHeight(ui_10)
            self.layout.color_2.setMaximumHeight(ui_10)
            self.layout.harmony_1.setMinimumHeight(ui_20)
            self.layout.harmony_1.setMaximumHeight(ui_20)
            self.layout.harmony_2.setMinimumHeight(ui_20)
            self.layout.harmony_2.setMaximumHeight(ui_20)
            self.layout.harmony_3.setMinimumHeight(ui_20)
            self.layout.harmony_3.setMaximumHeight(ui_20)
            self.layout.harmony_4.setMinimumHeight(ui_20)
            self.layout.harmony_4.setMaximumHeight(ui_20)
            self.layout.harmony_5.setMinimumHeight(ui_20)
            self.layout.harmony_5.setMaximumHeight(ui_20)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (har_active == True and har_index == "Complemantary"):
            font.setBold(True)
            self.harmony_index = "Complemantary"
            self.harmony_active = 3
            self.layout.color_1.setMinimumHeight(ui_10)
            self.layout.color_1.setMaximumHeight(ui_10)
            self.layout.color_2.setMinimumHeight(ui_10)
            self.layout.color_2.setMaximumHeight(ui_10)
            self.layout.harmony_1.setMinimumHeight(ui_20)
            self.layout.harmony_1.setMaximumHeight(ui_20)
            self.layout.harmony_2.setMinimumHeight(ui_20)
            self.layout.harmony_2.setMaximumHeight(ui_20)
            self.layout.harmony_3.setMinimumHeight(ui_20)
            self.layout.harmony_3.setMaximumHeight(ui_20)
            self.layout.harmony_4.setMinimumHeight(ui_20)
            self.layout.harmony_4.setMaximumHeight(ui_20)
            self.layout.harmony_5.setMinimumHeight(ui_20)
            self.layout.harmony_5.setMaximumHeight(ui_20)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (har_active == True and har_index == "Analogous"):
            font.setBold(True)
            self.harmony_index = "Analogous"
            self.harmony_active = 3
            self.layout.color_1.setMinimumHeight(ui_10)
            self.layout.color_1.setMaximumHeight(ui_10)
            self.layout.color_2.setMinimumHeight(ui_10)
            self.layout.color_2.setMaximumHeight(ui_10)
            self.layout.harmony_1.setMinimumHeight(ui_20)
            self.layout.harmony_1.setMaximumHeight(ui_20)
            self.layout.harmony_2.setMinimumHeight(ui_20)
            self.layout.harmony_2.setMaximumHeight(ui_20)
            self.layout.harmony_3.setMinimumHeight(ui_20)
            self.layout.harmony_3.setMaximumHeight(ui_20)
            self.layout.harmony_4.setMinimumHeight(ui_20)
            self.layout.harmony_4.setMaximumHeight(ui_20)
            self.layout.harmony_5.setMinimumHeight(ui_20)
            self.layout.harmony_5.setMaximumHeight(ui_20)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (har_active == True and har_index == "Split Complemantary"):
            font.setBold(True)
            self.harmony_index = "Split Complemantary"
            self.harmony_active = 3
            self.layout.color_1.setMinimumHeight(ui_10)
            self.layout.color_1.setMaximumHeight(ui_10)
            self.layout.color_2.setMinimumHeight(ui_10)
            self.layout.color_2.setMaximumHeight(ui_10)
            self.layout.harmony_1.setMinimumHeight(ui_20)
            self.layout.harmony_1.setMaximumHeight(ui_20)
            self.layout.harmony_2.setMinimumHeight(ui_20)
            self.layout.harmony_2.setMaximumHeight(ui_20)
            self.layout.harmony_3.setMinimumHeight(ui_20)
            self.layout.harmony_3.setMaximumHeight(ui_20)
            self.layout.harmony_4.setMinimumHeight(ui_20)
            self.layout.harmony_4.setMaximumHeight(ui_20)
            self.layout.harmony_5.setMinimumHeight(ui_20)
            self.layout.harmony_5.setMaximumHeight(ui_20)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        if (har_active == True and har_index == "Double Split Complemantary"):
            font.setBold(True)
            self.harmony_index = "Double Split Complemantary"
            self.harmony_active = 3
            self.layout.color_1.setMinimumHeight(ui_10)
            self.layout.color_1.setMaximumHeight(ui_10)
            self.layout.color_2.setMinimumHeight(ui_10)
            self.layout.color_2.setMaximumHeight(ui_10)
            self.layout.harmony_1.setMinimumHeight(ui_20)
            self.layout.harmony_1.setMaximumHeight(ui_20)
            self.layout.harmony_2.setMinimumHeight(ui_20)
            self.layout.harmony_2.setMaximumHeight(ui_20)
            self.layout.harmony_3.setMinimumHeight(ui_20)
            self.layout.harmony_3.setMaximumHeight(ui_20)
            self.layout.harmony_4.setMinimumHeight(ui_20)
            self.layout.harmony_4.setMaximumHeight(ui_20)
            self.layout.harmony_5.setMinimumHeight(ui_20)
            self.layout.harmony_5.setMaximumHeight(ui_20)
            self.layout.color_harmonys.setContentsMargins(zero, zero, zero, zero)
        har_edit = self.layout.har_edit.isChecked()
        if har_edit == True:
            self.harmony_edit = True
        else:
            self.harmony_edit = False
        self.layout.har.setFont(font)
        self.update()
        if save == "SAVE":
            self.Spacer_Gap()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_COTD(self, save):
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
            self.Spacer_Gap()
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
            self.Spacer_Gap()
        self.layout.cotd.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save_UI()
    # Panels
    def Menu_PAN(self, save):
        font = self.layout.pan.font()
        self.PANEL_Shrink()
        pan_active = self.layout.pan.isChecked()
        pan_index = self.layout.pan_index.currentText()
        if pan_active == False:
            font.setBold(False)
            self.panel_active = "None"
        if (pan_active == True and pan_index == "FGC"):
            font.setBold(True)
            self.panel_active = "FGC"
            self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if (pan_active == True and pan_index == "RGB"):
            font.setBold(True)
            self.panel_active = "RGB"
            self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("RGB", 0)
        if (pan_active == True and pan_index == "ARD"):
            font.setBold(True)
            self.panel_active = "ARD"
            self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("RGB", 0)
        if (pan_active == True and pan_index == "HSV"):
            font.setBold(True)
            self.panel_active = "HSV"
            self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("HSV", 0)
        if (pan_active == True and pan_index == "HSL"):
            font.setBold(True)
            self.panel_active = "HSL"
            self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("HSL", 0)
        if (pan_active == True and pan_index == "HUE"):
            font.setBold(True)
            # Adjust Primary GUI
            self.panel_active = "HUE"
            self.layout.panel_hue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if pan_index == "HUE":
            # Adjust Secondary GUI
            self.pan_sec = self.layout.pan_secondary.currentText()
            self.layout.pan_secondary.setEnabled(True)
            if self.pan_sec == "DOT":
                self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if self.pan_sec == "TRIANGLE":
                self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if self.pan_sec == "SQUARE":
                self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if self.pan_sec == "DIAMOND":
                self.layout.panel_triangle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.layout.panel_square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.layout.panel_diamond.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.Pigment_Convert("RGB", 0)
        self.Spacer_Vertical()
        self.layout.pan.setFont(font)
        if save == "SAVE":
            self.Ratio()
            self.Pigment_Display()
            self.Settings_Save_UI()
    def PANEL_Shrink(self):
        # Primary
        self.layout.panel_fgc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_uvd.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_ard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hsl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.panel_hue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Secondary
        self.layout.pan_secondary.setEnabled(False)
    # Dots
    def Menu_DOT(self, save):
        font = self.layout.dot.font()
        if self.layout.dot.isChecked():
            font.setBold(True)
            self.dot_active = True
            self.layout.panel_dot_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.dot_1.setMinimumHeight(ui_25)
            self.layout.dot_1.setMaximumHeight(ui_25)
            self.layout.dot_2.setMinimumHeight(ui_25)
            self.layout.dot_2.setMaximumHeight(ui_25)
            self.layout.dot_3.setMinimumHeight(ui_25)
            self.layout.dot_3.setMaximumHeight(ui_25)
            self.layout.dot_4.setMinimumHeight(ui_25)
            self.layout.dot_4.setMaximumHeight(ui_25)
            self.layout.panel_dot_colors.setContentsMargins(zero, unit, zero, unit)
            self.layout.panel_dot_colors.setSpacing(2)
            self.Spacer_Vertical()
        else:
            font.setBold(False)
            self.dot_active = False
            self.layout.panel_dot_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.dot_1.setMinimumHeight(zero)
            self.layout.dot_1.setMaximumHeight(zero)
            self.layout.dot_2.setMinimumHeight(zero)
            self.layout.dot_2.setMaximumHeight(zero)
            self.layout.dot_3.setMinimumHeight(zero)
            self.layout.dot_3.setMaximumHeight(zero)
            self.layout.dot_4.setMinimumHeight(zero)
            self.layout.dot_4.setMaximumHeight(zero)
            self.layout.panel_dot_colors.setContentsMargins(zero, zero, zero, zero)
            self.layout.panel_dot_colors.setSpacing(0)
            self.Spacer_Vertical()
        self.layout.dot.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save_UI()
    # Object
    def Menu_OBJ(self, save):
        font = self.layout.obj.font()
        # Colors Panel Shrink
        self.OBJ_Shrink_Top()
        self.OBJ_Shrink_Bot()
        # Select Object
        self.obj_active = self.layout.obj.isChecked()
        self.obj_index = self.layout.obj_index.currentText()
        if self.obj_active == False:
            font.setBold(False)
        if (self.obj_active == True and self.obj_index == "SPHERE"):
            font.setBold(True)
            # Paths
            # self.path_bg_1 = str(self.dir_name + "/OBJECT/SPHERE/bg_1.png")
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
            # Reset
            self.OBJ_Scale_Top()
            if self.layout.obj_set.isChecked() == False:
                self.OBJ_Scale_Bot()
            self.OBJ_Save()
        if (self.obj_active == True and self.obj_index == "USER"):
            font.setBold(True)
            # Paths
            # self.path_bg_1 = str(self.dir_name + "/OBJECT/USER/bg_1.png")
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
            # Reset
            self.OBJ_Scale_Top()
            if self.layout.obj_set.isChecked() == False:
                self.OBJ_Scale_Bot()
            self.OBJ_Save()
        self.OBJ_SET(0)
        self.Spacer_Vertical()
        self.layout.obj.setFont(font)
        if save == "SAVE":
            self.Ratio()
            self.Pigment_Display()
            self.Settings_Save_UI()
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
    def OBJ_Save(self):
        # self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
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
    def OBJ_SET(self, save):
        if (self.layout.obj_set.isChecked() == True and self.layout.obj.isChecked() == True):
            self.OBJ_Scale_Bot()
        if (self.layout.obj_set.isChecked() == False and self.layout.obj.isChecked() == True):
            self.OBJ_Shrink_Bot()
        if save == "SAVE":
            self.Settings_Save_UI()
    # Mixers
    def Menu_TIP(self, save):
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
            self.Spacer_Gap()
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
            self.Spacer_Gap()
        self.layout.tip.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Settings_Save_UI()
    def Menu_TTS(self, save):
        font = self.layout.tts.font()
        if self.layout.tts.isChecked():
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
            self.Spacer_Gap()
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
            self.Spacer_Gap()
        self.layout.tts.setFont(font)
        if save == "SAVE":
            self.Pigment_Display()
            self.Mixer_Display()
            self.Settings_Save_UI()
    def Menu_MIX(self, save):
        font = self.layout.mix.font()
        self.MIX_Shrink()
        mix_active = self.layout.mix.isChecked()
        mix_index = self.layout.mix_index.currentText()
        if mix_active == False:
            font.setBold(False)
        if (mix_active == True and mix_index == "RGB"):
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
        if (mix_active == True and mix_index == "ARD"):
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
        if (mix_active == True and mix_index == "HSV"):
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
        if (mix_active == True and mix_index == "HSL"):
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
        if (mix_active == True and mix_index == "HCY"):
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
        if (mix_active == True and mix_index == "CMYK"):
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
        self.Spacer_Gap()
        self.layout.mix.setFont(font)
        if save == "SAVE":
            self.Ratio()
            self.Pigment_Display()
            self.Mixer_Display()
            self.Settings_Save_UI()
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
        # # Mix HCY
        # self.layout.hcy_l1.setMinimumHeight(zero)
        # self.layout.hcy_l1.setMaximumHeight(zero)
        # self.layout.hcy_l2.setMinimumHeight(zero)
        # self.layout.hcy_l2.setMaximumHeight(zero)
        # self.layout.hcy_l3.setMinimumHeight(zero)
        # self.layout.hcy_l3.setMaximumHeight(zero)
        # self.layout.hcy_r1.setMinimumHeight(zero)
        # self.layout.hcy_r1.setMaximumHeight(zero)
        # self.layout.hcy_r2.setMinimumHeight(zero)
        # self.layout.hcy_r2.setMaximumHeight(zero)
        # self.layout.hcy_r3.setMinimumHeight(zero)
        # self.layout.hcy_r3.setMaximumHeight(zero)
        # self.layout.hcy_g1.setMinimumHeight(zero)
        # self.layout.hcy_g1.setMaximumHeight(zero)
        # self.layout.hcy_g2.setMinimumHeight(zero)
        # self.layout.hcy_g2.setMaximumHeight(zero)
        # self.layout.hcy_g3.setMinimumHeight(zero)
        # self.layout.hcy_g3.setMaximumHeight(zero)
        # self.layout.mixer_hcy.setContentsMargins(zero, zero, zero, zero)
        # self.layout.mixer_hcy.setSpacing(zero)
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
    # Support
    def Spacer_Gap(self):
        # Eraser
        if (self.layout.sof.isChecked() == True and
        self.layout.values.isChecked() == True):
            self.layout.eraser.setMinimumWidth(ui_15)
            self.layout.eraser.setMaximumWidth(ui_15)
        else:
            self.layout.eraser.setMinimumWidth(zero)
            self.layout.eraser.setMaximumWidth(zero)
        # Lock
        if (self.layout.kkk.isChecked() == True and
        self.layout.values.isChecked() == True):
            self.layout.kkk_1_lock.setMinimumWidth(ui_15)
            self.layout.kkk_1_lock.setMaximumWidth(ui_15)
        else:
            self.layout.kkk_1_lock.setMinimumWidth(zero)
            self.layout.kkk_1_lock.setMaximumWidth(zero)
        # Channels
        if (self.chan_aaa == True or
        self.chan_rgb == True or
        self.chan_ard == True or
        self.chan_hsv == True or
        self.chan_hsl == True or
        self.chan_hcy == True or
        self.chan_cmy == True or
        self.chan_cmyk == True or
        self.chan_kkk == True):
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
        if (self.chan_aaa == False and
        self.chan_rgb == False and
        self.chan_ard == False and
        self.chan_hsv == False and
        self.chan_hsl == False and
        self.chan_hcy == False and
        self.chan_cmy == False and
        self.chan_cmyk == False and
        self.chan_kkk == False):
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
    def Spacer_Vertical(self):
        if (self.layout.pan.isChecked() == False and
            self.layout.obj.isChecked() == False and
            self.layout.dot.isChecked() == False):
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            self.layout.vertical_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    # Start UP UI Shrink
    def Menu_Shrink(self):
        # Options
        self.Options_Height_Zero()
        self.Menu_Value(0)
        # Interior
        self.Channel_Height_Zero()
        self.Switches_Height_Zero()
        # Adjust
        self.Spacer_Gap()
        self.Spacer_Vertical()
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
        self.layout.obj.setMinimumHeight(zero)
        self.layout.obj.setMaximumHeight(zero)
        self.layout.dot.setMinimumHeight(zero)
        self.layout.dot.setMaximumHeight(zero)
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
        # Object
        self.layout.menu_object.setMinimumHeight(zero)
        self.layout.menu_object.setMaximumHeight(zero)
        self.layout.obj_index.setMinimumHeight(zero)
        self.layout.obj_index.setMaximumHeight(zero)
        self.layout.obj_set.setMinimumHeight(zero)
        self.layout.obj_set.setMaximumHeight(zero)
        # Channels
        self.layout.menu_values.setMinimumHeight(zero)
        self.layout.menu_values.setMaximumHeight(zero)
        self.layout.values.setMinimumHeight(zero)
        self.layout.values.setMaximumHeight(zero)
        # Mixer
        self.layout.menu_mixer.setMinimumHeight(zero)
        self.layout.menu_mixer.setMaximumHeight(zero)
        self.layout.mix_index.setMinimumHeight(zero)
        self.layout.mix_index.setMaximumHeight(zero)
        # Gray Mode
        self.layout.menu_gray.setMinimumHeight(zero)
        self.layout.menu_gray.setMaximumHeight(zero)
        self.layout.gray.setMinimumHeight(zero)
        self.layout.gray.setMaximumHeight(zero)
        # Spacing
        self.layout.options_3.setContentsMargins(zero, zero, zero, zero)
        self.layout.options_3.setSpacing(0)
    def Channel_Height_Zero(self):
        # SOF
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
        # AAA
        self.chan_aaa = False
        self.layout.aaa_1_slider.setMinimumHeight(zero)
        self.layout.aaa_1_slider.setMaximumHeight(zero)
        self.layout.aaa_1_value.setMinimumHeight(zero)
        self.layout.aaa_1_value.setMaximumHeight(zero)
        self.layout.aaa_1_tick.setMinimumHeight(zero)
        # RGB
        self.chan_rgb = False
        self.layout.rgb_1_slider.setMinimumHeight(zero)
        self.layout.rgb_1_slider.setMaximumHeight(zero)
        self.layout.rgb_1_value.setMinimumHeight(zero)
        self.layout.rgb_1_value.setMaximumHeight(zero)
        self.layout.rgb_1_tick.setMinimumHeight(zero)
        self.layout.rgb_2_slider.setMinimumHeight(zero)
        self.layout.rgb_2_slider.setMaximumHeight(zero)
        self.layout.rgb_2_value.setMinimumHeight(zero)
        self.layout.rgb_2_value.setMaximumHeight(zero)
        self.layout.rgb_2_tick.setMinimumHeight(zero)
        self.layout.rgb_3_slider.setMinimumHeight(zero)
        self.layout.rgb_3_slider.setMaximumHeight(zero)
        self.layout.rgb_3_value.setMinimumHeight(zero)
        self.layout.rgb_3_value.setMaximumHeight(zero)
        self.layout.rgb_3_tick.setMinimumHeight(zero)
        # ARD
        self.chan_ard = False
        self.layout.ard_1_slider.setMinimumHeight(zero)
        self.layout.ard_1_slider.setMaximumHeight(zero)
        self.layout.ard_1_value.setMinimumHeight(zero)
        self.layout.ard_1_value.setMaximumHeight(zero)
        self.layout.ard_1_tick.setMinimumHeight(zero)
        self.layout.ard_2_slider.setMinimumHeight(zero)
        self.layout.ard_2_slider.setMaximumHeight(zero)
        self.layout.ard_2_value.setMinimumHeight(zero)
        self.layout.ard_2_value.setMaximumHeight(zero)
        self.layout.ard_2_tick.setMinimumHeight(zero)
        self.layout.ard_3_slider.setMinimumHeight(zero)
        self.layout.ard_3_slider.setMaximumHeight(zero)
        self.layout.ard_3_value.setMinimumHeight(zero)
        self.layout.ard_3_value.setMaximumHeight(zero)
        self.layout.ard_3_tick.setMinimumHeight(zero)
        # HSV
        self.chan_hsv = False
        self.layout.hsv_1_slider.setMinimumHeight(zero)
        self.layout.hsv_1_slider.setMaximumHeight(zero)
        self.layout.hsv_1_value.setMinimumHeight(zero)
        self.layout.hsv_1_value.setMaximumHeight(zero)
        self.layout.hsv_1_tick.setMinimumHeight(zero)
        self.layout.hsv_2_slider.setMinimumHeight(zero)
        self.layout.hsv_2_slider.setMaximumHeight(zero)
        self.layout.hsv_2_value.setMinimumHeight(zero)
        self.layout.hsv_2_value.setMaximumHeight(zero)
        self.layout.hsv_2_tick.setMinimumHeight(zero)
        self.layout.hsv_3_slider.setMinimumHeight(zero)
        self.layout.hsv_3_slider.setMaximumHeight(zero)
        self.layout.hsv_3_value.setMinimumHeight(zero)
        self.layout.hsv_3_value.setMaximumHeight(zero)
        self.layout.hsv_3_tick.setMinimumHeight(zero)
        # HSL
        self.chan_hsl = False
        self.layout.hsl_1_slider.setMinimumHeight(zero)
        self.layout.hsl_1_slider.setMaximumHeight(zero)
        self.layout.hsl_1_value.setMinimumHeight(zero)
        self.layout.hsl_1_value.setMaximumHeight(zero)
        self.layout.hsl_1_tick.setMinimumHeight(zero)
        self.layout.hsl_2_slider.setMinimumHeight(zero)
        self.layout.hsl_2_slider.setMaximumHeight(zero)
        self.layout.hsl_2_value.setMinimumHeight(zero)
        self.layout.hsl_2_value.setMaximumHeight(zero)
        self.layout.hsl_2_tick.setMinimumHeight(zero)
        self.layout.hsl_3_slider.setMinimumHeight(zero)
        self.layout.hsl_3_slider.setMaximumHeight(zero)
        self.layout.hsl_3_value.setMinimumHeight(zero)
        self.layout.hsl_3_value.setMaximumHeight(zero)
        self.layout.hsl_3_tick.setMinimumHeight(zero)
        # HCY
        self.chan_hcy = False
        self.layout.hcy_1_slider.setMinimumHeight(zero)
        self.layout.hcy_1_slider.setMaximumHeight(zero)
        self.layout.hcy_1_value.setMinimumHeight(zero)
        self.layout.hcy_1_value.setMaximumHeight(zero)
        self.layout.hcy_1_tick.setMinimumHeight(zero)
        self.layout.hcy_2_slider.setMinimumHeight(zero)
        self.layout.hcy_2_slider.setMaximumHeight(zero)
        self.layout.hcy_2_value.setMinimumHeight(zero)
        self.layout.hcy_2_value.setMaximumHeight(zero)
        self.layout.hcy_2_tick.setMinimumHeight(zero)
        self.layout.hcy_3_slider.setMinimumHeight(zero)
        self.layout.hcy_3_slider.setMaximumHeight(zero)
        self.layout.hcy_3_value.setMinimumHeight(zero)
        self.layout.hcy_3_value.setMaximumHeight(zero)
        self.layout.hcy_3_tick.setMinimumHeight(zero)
        # CMY
        self.chan_cmy = False
        self.layout.cmy_1_slider.setMinimumHeight(zero)
        self.layout.cmy_1_slider.setMaximumHeight(zero)
        self.layout.cmy_1_value.setMinimumHeight(zero)
        self.layout.cmy_1_value.setMaximumHeight(zero)
        self.layout.cmy_1_tick.setMinimumHeight(zero)
        self.layout.cmy_2_slider.setMinimumHeight(zero)
        self.layout.cmy_2_slider.setMaximumHeight(zero)
        self.layout.cmy_2_value.setMinimumHeight(zero)
        self.layout.cmy_2_value.setMaximumHeight(zero)
        self.layout.cmy_2_tick.setMinimumHeight(zero)
        self.layout.cmy_3_slider.setMinimumHeight(zero)
        self.layout.cmy_3_slider.setMaximumHeight(zero)
        self.layout.cmy_3_value.setMinimumHeight(zero)
        self.layout.cmy_3_value.setMaximumHeight(zero)
        self.layout.cmy_3_tick.setMinimumHeight(zero)
        # CMYK
        self.chan_cmyk = False
        self.layout.cmyk_1_slider.setMinimumHeight(zero)
        self.layout.cmyk_1_slider.setMaximumHeight(zero)
        self.layout.cmyk_1_value.setMinimumHeight(zero)
        self.layout.cmyk_1_value.setMaximumHeight(zero)
        self.layout.cmyk_1_tick.setMinimumHeight(zero)
        self.layout.cmyk_2_slider.setMinimumHeight(zero)
        self.layout.cmyk_2_slider.setMaximumHeight(zero)
        self.layout.cmyk_2_value.setMinimumHeight(zero)
        self.layout.cmyk_2_value.setMaximumHeight(zero)
        self.layout.cmyk_2_tick.setMinimumHeight(zero)
        self.layout.cmyk_3_slider.setMinimumHeight(zero)
        self.layout.cmyk_3_slider.setMaximumHeight(zero)
        self.layout.cmyk_3_value.setMinimumHeight(zero)
        self.layout.cmyk_3_value.setMaximumHeight(zero)
        self.layout.cmyk_3_tick.setMinimumHeight(zero)
        self.layout.cmyk_4_slider.setMinimumHeight(zero)
        self.layout.cmyk_4_slider.setMaximumHeight(zero)
        self.layout.cmyk_4_value.setMinimumHeight(zero)
        self.layout.cmyk_4_value.setMaximumHeight(zero)
        self.layout.cmyk_4_tick.setMinimumHeight(zero)
        # KKK
        self.chan_kkk = False
        self.layout.kkk_1_slider.setMinimumHeight(zero)
        self.layout.kkk_1_slider.setMaximumHeight(zero)
        self.layout.kkk_1_value.setMinimumHeight(zero)
        self.layout.kkk_1_value.setMaximumHeight(zero)
        self.layout.kkk_1_tick.setMinimumHeight(zero)
        self.layout.kkk_1_tick.setMaximumHeight(zero)
        self.layout.kkk_1_lock.setMinimumHeight(zero)
        self.layout.kkk_1_lock.setMaximumHeight(zero)
    def Switches_Height_Zero(self):
        # HAR
        self.harmony_active = 0
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
        self.dot_active = False
        self.layout.panel_dot_mix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.dot_1.setMinimumHeight(zero)
        self.layout.dot_1.setMaximumHeight(zero)
        self.layout.dot_2.setMinimumHeight(zero)
        self.layout.dot_2.setMaximumHeight(zero)
        self.layout.dot_3.setMinimumHeight(zero)
        self.layout.dot_3.setMaximumHeight(zero)
        self.layout.dot_4.setMinimumHeight(zero)
        self.layout.dot_4.setMaximumHeight(zero)
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
        # # Mix HCY
        # self.layout.hcy_l1.setMinimumHeight(zero)
        # self.layout.hcy_l1.setMaximumHeight(zero)
        # self.layout.hcy_l2.setMinimumHeight(zero)
        # self.layout.hcy_l2.setMaximumHeight(zero)
        # self.layout.hcy_l3.setMinimumHeight(zero)
        # self.layout.hcy_l3.setMaximumHeight(zero)
        # self.layout.hcy_r1.setMinimumHeight(zero)
        # self.layout.hcy_r1.setMaximumHeight(zero)
        # self.layout.hcy_r2.setMinimumHeight(zero)
        # self.layout.hcy_r2.setMaximumHeight(zero)
        # self.layout.hcy_r3.setMinimumHeight(zero)
        # self.layout.hcy_r3.setMaximumHeight(zero)
        # self.layout.hcy_g1.setMinimumHeight(zero)
        # self.layout.hcy_g1.setMaximumHeight(zero)
        # self.layout.hcy_g2.setMinimumHeight(zero)
        # self.layout.hcy_g2.setMaximumHeight(zero)
        # self.layout.hcy_g3.setMinimumHeight(zero)
        # self.layout.hcy_g3.setMaximumHeight(zero)
        # self.layout.mixer_hcy.setContentsMargins(zero, zero, zero, zero)
        # self.layout.mixer_hcy.setSpacing(zero)
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
    #\\ Krita & Pigment ########################################################
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
                self.Krita_2_Pigment()
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
    def Krita_2_Pigment(self):
        # Check current Theme color Value (0-255)
        krita = QApplication.palette().color(QPalette.Window).value()
        if self.theme_krita != krita:
            # Update System Variable
            self.theme_krita = krita
            # Contrast Gray Calculation
            if self.theme_krita <= 101:
                self.theme_pigment = ( 255 - self.theme_krita ) / 255
            elif self.theme_krita >= 153:
                self.theme_pigment = ( 255 - self.theme_krita ) / 255
            else:
                self.theme_pigment = ( self.theme_krita - 52 ) / 255
            # RGB Code of contrast Gray
            self.gray_natural = self.HEX_6(self.theme_krita,self.theme_krita,self.theme_krita)
            self.gray_contrast = self.HEX_6(self.theme_pigment,self.theme_pigment,self.theme_pigment)

        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            state = self.layout.check.checkState()
            influence = self.kkk_lock or self.harmony_active != 0
            if (state == 1 and influence == False):
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
                state = self.layout.check.checkState()
                if (state == 1 or state == 2):
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
        hue = self.rgb_to_angle(r,g,b)
        self.angle_live = hue[0]
    def Color_APPLY(self, mode, val1, val2, val3, val4):
        # Convert Something to RGB
        if mode == "AAA":
            aaa = [val1]
            rgb = [aaa[0], aaa[1], aaa[2]]
        if mode == "RGB":
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
        if mode == "CMY":
            cmy = [val1, val2, val3]
            rgb = self.cmy_to_rgb(cmy[0], cmy[1], cmy[2])
        if mode == "CMYK":
            cmyk = [val1, val2, val3, val4]
            rgb = self.cmyk_to_rgb(cmyk[0], cmyk[1], cmyk[2], cmyk[3])
        # Convert RGB to Other
        if mode != "AAA":
            aaa = self.rgb_to_aaa(rgb[0], rgb[1], rgb[2])
        if mode != "RGB":
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
        if mode != "CMY":
            cmy = self.rgb_to_cmy(rgb[0], rgb[1], rgb[2])
        if mode != "CMYK":
            cmyk = self.rgb_to_cmyk(rgb[0], rgb[1], rgb[2])
        if mode != "KKK":
            kkk = self.kkk_to_rgb(self.kkk_0)
            self.kkk_1 = kkk[0]
            self.kkk_2 = kkk[1]
            self.kkk_3 = kkk[2]
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
        if (condition > -unitRDL and condition < unitRDL):
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
        # Pigment Update Values
        self.Pigment_Harmony()
        self.Pigment_Sync(0)
        self.Pigment_2_Krita("HOLD")
        self.Pigment_Display()
    # Convert with Reference
    def Pigment_Convert(self, mode, ignore):
        # Conversion Out of this Mode
        if mode == "AAA":
            self.aaa_1 = self.layout.aaa_1_value.value() / kritaAAA
            aaa = [self.aaa_1]
            rgb = [self.aaa_1, self.aaa_1, self.aaa_1]
        if mode == "RGB":
            self.rgb_1 = self.layout.rgb_1_value.value() / kritaRGB
            self.rgb_2 = self.layout.rgb_2_value.value() / kritaRGB
            self.rgb_3 = self.layout.rgb_3_value.value() / kritaRGB
            rgb = [self.rgb_1, self.rgb_2, self.rgb_3]
        if mode == "ARD":
            self.ard_1 = self.layout.ard_1_value.value() / kritaANG
            self.ard_2 = self.layout.ard_2_value.value() / kritaRDL
            self.ard_3 = self.layout.ard_3_value.value() / kritaRDL
            rgb = self.ard_to_rgb(self.ard_1, self.ard_2, self.ard_3)
            ard = [self.ard_1, self.ard_2, self.ard_3]
            self.angle_live = self.ard_1
        if mode == "HSV":
            self.hsv_1 = self.layout.hsv_1_value.value() / kritaHUE
            self.hsv_2 = self.layout.hsv_2_value.value() / kritaSVLCY
            self.hsv_3 = self.layout.hsv_3_value.value() / kritaSVLCY
            rgb = self.hsv_to_rgb(self.hsv_1, self.hsv_2, self.hsv_3)
            hsv = [self.hsv_1, self.hsv_2, self.hsv_3]
            self.angle_live = self.hsv_1
        if mode == "HSL":
            self.hsl_1 = self.layout.hsl_1_value.value() / kritaHUE
            self.hsl_2 = self.layout.hsl_2_value.value() / kritaSVLCY
            self.hsl_3 = self.layout.hsl_3_value.value() / kritaSVLCY
            rgb = self.hsl_to_rgb(self.hsl_1, self.hsl_2, self.hsl_3)
            hsl = [self.hsl_1, self.hsl_2, self.hsl_3]
            self.angle_live = self.hsl_1
        if mode == "HCY":
            self.hcy_1 = self.layout.hcy_1_value.value() / kritaHUE
            self.hcy_2 = self.layout.hcy_2_value.value() / kritaSVLCY
            self.hcy_3 = self.layout.hcy_3_value.value() / kritaSVLCY
            rgb = self.hcy_to_rgb(self.hcy_1, self.hcy_2, self.hcy_3)
            hcy = [self.hcy_1, self.hcy_2, self.hcy_3]
            self.angle_live = self.hcy_1
        if mode == "CMY":
            self.cmy_1 = self.layout.cmy_1_value.value() / kritaCMY
            self.cmy_2 = self.layout.cmy_2_value.value() / kritaCMY
            self.cmy_3 = self.layout.cmy_3_value.value() / kritaCMY
            rgb = self.cmy_to_rgb(self.cmy_1, self.cmy_2, self.cmy_3)
            cmy = [self.cmy_1, self.cmy_2, self.cmy_3]
        if mode == "CMYK":
            self.cmyk_1 = self.layout.cmyk_1_value.value() / kritaCMYK
            self.cmyk_2 = self.layout.cmyk_2_value.value() / kritaCMYK
            self.cmyk_3 = self.layout.cmyk_3_value.value() / kritaCMYK
            self.cmyk_4 = self.layout.cmyk_4_value.value() / kritaCMYK
            rgb = self.cmyk_to_rgb(self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4)
            cmyk = [self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        if mode == "KKK":
            if self.kkk_lock == True:
                self.rgb_1 = self.layout.rgb_1_value.value() / kritaRGB
                self.rgb_2 = self.layout.rgb_2_value.value() / kritaRGB
                self.rgb_3 = self.layout.rgb_3_value.value() / kritaRGB
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
        # Conversion Into this Mode
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
            if (condition > -unitRDL and condition < unitRDL):
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
        # Pigment Update Values
        self.Pigment_Harmony()
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
        if mode == "CMY":
            self.Pigment_Sync("CMY")
        if mode == "CMYK":
            self.Pigment_Sync("CMYK")
        if mode == "KKK":
            self.Pigment_Sync("KKK")
        self.Pigment_2_Krita("HOLD")
        self.Pigment_Display()
    def Pigment_Harmony(self):
        # Harmony
        har_index = self.layout.har_index.currentText()
        if har_index == "Monochromatic":
            if self.harmony_active == 1: # Rotating Node
                # 1
                self.har_1 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 2
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 2: # Rotating Node
                # 1
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                self.har_2 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 3: # Rotating Node Major
                # 1
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 4
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 4: # Rotating Node
                # 1
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                self.har_4 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 5
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 5: # Rotating Node
                # 1
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                self.har_5 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
        if har_index == "Complemantary":
            if self.harmony_active == 1: # Rotating Node
                # 1
                self.har_1 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 2
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 2: # Rotating Node
                # 1
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                self.har_2 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 3: # Rotating Node Major
                # 1
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 4
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 4: # Rotating Node
                # 1
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                self.har_4 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 5
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 5: # Rotating Node Major
                # 1
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                angle = self.angle_live + 0.5
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_3[5], self.har_3[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                if self.harmony_edit == True:
                    hsl = [self.angle_live, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [self.angle_live, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                self.har_5 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
        if har_index == "Analogous":
            if self.harmony_active == 1:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + (2 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 2:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit:
                    hsl = [angle,  self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + (2 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 3: # Rotating Node Major
                # 1
                angle = self.angle_live - (2*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.angle_live - (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 4
                angle = self.angle_live + (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.angle_live + (2*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 4:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + (2 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 5:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + (2 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
        if har_index == "Split Complemantary":
            if self.harmony_active == 1:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 2:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit:
                    hsl = [angle,  self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 3: # Rotating Node Major
                # 1
                angle = self.angle_live - (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.angle_live - (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 4
                angle = self.angle_live + (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.angle_live + (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 4:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 5:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] + 1 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + 1 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
        if har_index == "Double Split Complemantary":
            if self.harmony_active == 1:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - 0.5 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + 0.5 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 2:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + 0.5 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 3: # Rotating Node Major
                # 1
                angle = self.angle_live - (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_1[5], self.har_1[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.angle_live + 0.5 + (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                self.har_3 = ["HSL", self.rgb_1, self.rgb_2, self.rgb_3, self.angle_live, self.hsl_2, self.hsl_3]
                # 4
                angle = self.angle_live - 0.5 - (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.angle_live + (1*self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 4:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] - 0.5 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
            if self.harmony_active == 5:
                # Delta
                value1 = self.angle_live # A
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
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_1 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 2
                angle = self.har_3[4] - 0.5 + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle, self.har_2[5], self.har_2[6]]
                else:
                    hsl = [angle, self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_2 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 3
                if self.harmony_edit == True:
                    hsl = [self.har_3[4],  self.har_3[5], self.har_3[6]]
                else:
                    hsl = [self.har_3[4],  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_3 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 4
                angle = self.har_3[4] + 0.5 - (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_4[5], self.har_4[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_4 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
                # 5
                angle = self.har_3[4] + (1 * self.harmony_delta)
                if angle >= 1:
                    angle = angle - 1
                if angle <= 0:
                    angle = angle + 1
                if self.harmony_edit == True:
                    hsl = [angle,  self.har_5[5], self.har_5[6]]
                else:
                    hsl = [angle,  self.hsl_2, self.hsl_3]
                rgb = self.hsl_to_rgb(hsl[0], hsl[1], hsl[2])
                self.har_5 = ["HSL", rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]]
        # Harmony Influenced by Kalvin
        self.har_k1 = [self.har_1[1] * self.kkk_1, self.har_1[2] * self.kkk_2, self.har_1[3] * self.kkk_3]
        self.har_k2 = [self.har_2[1] * self.kkk_1, self.har_2[2] * self.kkk_2, self.har_2[3] * self.kkk_3]
        self.har_k3 = [self.har_3[1] * self.kkk_1, self.har_3[2] * self.kkk_2, self.har_3[3] * self.kkk_3]
        self.har_k4 = [self.har_4[1] * self.kkk_1, self.har_4[2] * self.kkk_2, self.har_4[3] * self.kkk_3]
        self.har_k5 = [self.har_5[1] * self.kkk_1, self.har_5[2] * self.kkk_2, self.har_5[3] * self.kkk_3]

    #//
    #\\ Conversions / Trignometry (range 0-1) ##################################
    # AAA
    def rgb_to_aaa(self, r, g, b):
        aaa = math.sqrt( (0.299*r**2) + (0.587*g**2) + (0.114*b**2) )
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
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return [r, g, b]
    # Angle
    def rgb_to_angle(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        if minc == maxc:
            return [0.0]
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
    # HSL
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
    # HCY
    def rgb_to_hcy(self, r, g, b):
        y = lumaR*r + lumaG*g + lumaB*b
        p = max(r, g, b)
        n = min(r, g, b)
        d = p - n
        if n == p:
            h = 0.0
        elif p == r:
            h = (g - b)/d
            if h < 0:
                h += 6.0
        elif p == g:
            h = ((b - r)/d) + 2.0
        else:  # p==b
            h = ((r - g)/d) + 4.0
        h /= 6.0
        if r == g == b:
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
            tm = lumaR + lumaG * th
        elif h < 2:
            th = 2.0 - h
            tm = lumaG + lumaR * th
        elif h < 3:
            th = h - 2.0
            tm = lumaG + lumaB * th
        elif h < 4:
            th = 4.0 - h
            tm = lumaB + lumaG * th
        elif h < 5:
            th = h - 4.0
            tm = lumaB + lumaR * th
        else:
            th = 6.0 - h
            tm = lumaR + lumaB * th
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

    # RYB ###################################################################### NEW
    def rgb_to_ryb(self, rgb_r, rgb_g, rgb_b):
        white = min(rgb_r, rgb_g, rgb_b)
        black = min(1 - rgb_r, 1 - rgb_g, 1 - rgb_b)
        (rgb_r, rgb_g, rgb_b) = (x - white for x in (rgb_r, rgb_g, rgb_b))

        yellow = min(rgb_r, rgb_g)
        ryb_r = rgb_r - yellow
        ryb_y = (yellow + rgb_g) / 2
        ryb_b = (rgb_b + rgb_g - yellow) / 2

        norm = 0
        if max(rgb_r, rgb_g, rgb_b) != 0:
            norm = max(ryb_r, ryb_y, ryb_b) / max(rgb_r, rgb_g, rgb_b)
        ryb_r = ryb_r / norm if norm > 0 else ryb_r
        ryb_y = ryb_y / norm if norm > 0 else ryb_y
        ryb_b = ryb_b / norm if norm > 0 else ryb_b

        (ryb_r, ryb_y, ryb_b) = (x + black for x in (ryb_r, ryb_y, ryb_b))
        return [ryb_r, ryb_y, ryb_b]
    def ryb_to_rgb(self, ryb_r, ryb_y, ryb_b):
        black = min(ryb_r, ryb_y, ryb_b)
        white = min(1 - ryb_r, 1 - ryb_y, 1 - ryb_b)
        (ryb_r, ryb_y, ryb_b) = (x - black for x in (ryb_r, ryb_y, ryb_b))

        green = min(ryb_y, ryb_b)
        rgb_r = ryb_r + ryb_y - green
        rgb_g = ryb_y + green
        rgb_b = 2 * (ryb_b - green)

        norm = 0
        if max(ryb_r, ryb_y, ryb_b) != 0:
            norm = max(rgb_r, rgb_g, rgb_b) / max(ryb_r, ryb_y, ryb_b)
        rgb_r = rgb_r / norm if norm > 0 else rgb_r
        rgb_g = rgb_g / norm if norm > 0 else rgb_g
        rgb_b = rgb_b / norm if norm > 0 else rgb_b

        (rgb_r, rgb_g, rgb_b) = (x + white for x in (rgb_r, rgb_g, rgb_b))
        return [rgb_r, rgb_g, rgb_b]
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
    # YCbCr #################################################################### NEW
    def rgb_to_ycbcr(self, r, g, b):
        y = 0.299 * r + 0.587 * g + 0.114 * b
        cb = -0.169 * r - 0.331 * g + 0.500 * b
        cr = 0.500 * r - 0.419 * g - 0.081 * b
        return [y, cb, cr]
    def ycbcr_to_rgb(self, y, cb, cr):
        r = y + 1.403 * cr
        g = y - 0.344 * cb - 0.714 * cr
        b = y + 1.773 * cb
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

    # XYZ
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
    # LAB
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
    # YIQ
    def rgb_to_yiq(self, r, g, b):
        y = 0.299*r + 0.587*g + 0.114*b
        i = 0.5959**r - 0.2746*g - 0.3213*b
        q = 0.2115*r - 0.5227*g + 0.3112*b
        return [y, i, q]
    def yiq_to_rgb(self, y, i, q):
        r = 1*y + 0.956*i + 0.619*q
        g = 1*y - 0.272*i - 0.647*q
        b = 1*y - 1.106*i + 1.703*q

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
        if index != "CMY":
            self.Signal_Block_CMY(True)
        if index != "CMYK":
            self.Signal_Block_CMYK(True)
        if index != "KKK":
            self.Signal_Block_KKK(True)
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
        if index != "CMY":
            self.Signal_Block_CMY(False)
        if index != "CMYK":
            self.Signal_Block_CMYK(False)
        if index != "KKK":
            self.Signal_Block_KKK(False)
        # Settings
        self.Settings_Save_ActiveColor()
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
        self.layout.hsv_2_value.setValue(value2 * kritaSVLCY)
        self.layout.hsv_3_value.setValue(value3 * kritaSVLCY)
    def Signal_Send_HSL(self, value1, value2, value3):
        self.hsl_1_slider.Update(value1, self.layout.hsl_1_slider.width())
        self.hsl_2_slider.Update(value2, self.layout.hsl_2_slider.width())
        self.hsl_3_slider.Update(value3, self.layout.hsl_3_slider.width())
        self.layout.hsl_1_value.setValue(value1 * kritaHUE)
        self.layout.hsl_2_value.setValue(value2 * kritaSVLCY)
        self.layout.hsl_3_value.setValue(value3 * kritaSVLCY)
    def Signal_Send_HCY(self, value1, value2, value3):
        self.hcy_1_slider.Update(value1, self.layout.hcy_1_slider.width())
        self.hcy_2_slider.Update(value2, self.layout.hcy_2_slider.width())
        self.hcy_3_slider.Update(value3, self.layout.hcy_3_slider.width())
        self.layout.hcy_1_value.setValue(value1 * kritaHUE)
        self.layout.hcy_2_value.setValue(value2 * kritaSVLCY)
        self.layout.hcy_3_value.setValue(value3 * kritaSVLCY)
    def Signal_Send_CMY(self, value1, value2, value3):
        self.cmy_1_slider.Update(value1, self.layout.cmy_1_slider.width())
        self.cmy_2_slider.Update(value2, self.layout.cmy_2_slider.width())
        self.cmy_3_slider.Update(value3, self.layout.cmy_3_slider.width())
        self.layout.cmy_1_value.setValue(value1 * kritaCMY)
        self.layout.cmy_2_value.setValue(value2 * kritaCMY)
        self.layout.cmy_3_value.setValue(value3 * kritaCMY)
    def Signal_Send_CMYK(self, value1, value2, value3, value4):
        self.cmyk_1_slider.Update(value1, self.layout.cmyk_1_slider.width())
        self.cmyk_2_slider.Update(value2, self.layout.cmyk_2_slider.width())
        self.cmyk_3_slider.Update(value3, self.layout.cmyk_3_slider.width())
        self.cmyk_4_slider.Update(value4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_1_value.setValue(value1 * kritaCMYK)
        self.layout.cmyk_2_value.setValue(value2 * kritaCMYK)
        self.layout.cmyk_3_value.setValue(value3 * kritaCMYK)
        self.layout.cmyk_4_value.setValue(value4 * kritaCMYK)
    def Signal_Send_KKK(self, value1):
        self.kkk_1_slider.Update((value1-kritaKKKmin)/kritaKKKdelta, self.layout.kkk_1_slider.width())
        self.layout.kkk_1_value.setValue(value1)
    def Signal_Send_Panels(self):
        self.UVD_Update()
        self.ARD_Update()
        self.Update_Panel_HSV()
        self.Update_Panel_HSL()
        self.Update_Panel_HUE()
        self.Update_DOT()
        self.Object_Live()
    # UVD Update
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
            self.aaa_1,
            self.uvd_1, self.uvd_2, self.uvd_3,
            self.PCC,
            self.P1, self.P2, self.P3, self.P4, self.P5, self.P6,
            self.P12, self.P23, self.P34, self.P45, self.P56, self.P61,
            self.uvd_width, self.uvd_height,
            self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom
            )
    def UVD_Hexagon_Points(self):
        # Calculate Original Points
        self.uvd_hexagon_origins(self.uvd_3)
        # Panel Dimensions
        self.uvd_width = self.layout.panel_uvd_mask.width()
        self.uvd_height = self.layout.panel_uvd_mask.height()
        w2 = self.uvd_width / 2
        h2 = self.uvd_height / 2
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
    # ARD Update
    def ARD_Update(self):
        if self.panel_active == "ARD":
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
                self.aaa_1,
                self.hsv_to_rgb(self.ard_1, 1, 1),
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
    # Updates
    def Update_Panel_HSV(self):
        self.panel_hsv.Update_Panel(
            self.aaa_1,
            [self.hsv_1, self.hsv_2, self.hsv_3],
            self.hsv_to_rgb(self.hsv_1, 1, 1),
            self.layout.panel_hsv.width(),
            self.layout.panel_hsv.height(),
            self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom)
    def Update_Panel_HSL(self):
        self.panel_hsl_4.Update_Panel(
            self.aaa_1,
            [self.hsl_1, self.hsl_2, self.hsl_3],
            self.hsl_to_rgb(self.hsl_1, 1, 0.5),
            self.layout.panel_hsl.width(),
            self.layout.panel_hsl.height(),
            self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
            self.zoom)
    def Update_Panel_HUE(self):
        # Hue of Color
        hsv = self.hsv_to_rgb(self.angle_live, 1, 1)
        hsl = self.hsl_to_rgb(self.angle_live, 1, 0.5)
        # Update Regular
        if self.pan_sec == "DOT":
            pass
        if self.pan_sec == "TRIANGLE":
            self.panel_triangle.Update_Panel(
                self.aaa_1,
                [self.hsl_1, self.hsl_2, self.hsl_3],
                [hsl[0], hsl[1], hsl[2]],
                self.layout.panel_triangle.width(),
                self.layout.panel_triangle.height(),
                self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom
                )
        if self.pan_sec == "SQUARE":
            self.panel_square.Update_Panel(
                self.aaa_1,
                [self.hsv_1, self.hsv_2, self.hsv_3],
                [hsv[0], hsv[1], hsv[2]],
                self.layout.panel_square.width(),
                self.layout.panel_square.height(),
                self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom)
        if self.pan_sec == "DIAMOND":
            self.panel_diamond.Update_Panel(
                self.aaa_1,
                [self.hsl_1, self.hsl_2, self.hsl_3],
                [hsl[0], hsl[1], hsl[2]],
                self.layout.panel_diamond.width(),
                self.layout.panel_diamond.height(),
                self.HEX_6(self.rgb_1, self.rgb_2, self.rgb_3),
                self.zoom
                )
        # Update Circle
        if self.harmony_active == 0:
            self.panel_hue_circle.Update_Panel(
                # self.aaa_1,
                # [self.rgb_1, self.rgb_2, self.rgb_3],
                self.angle_live,
                [hsl[0], hsl[1], hsl[2]],
                self.layout.panel_hue_circle_mask.width(),
                self.layout.panel_hue_circle_mask.height(),
                self.gray_natural,
                self.gray_contrast
                )
        if self.harmony_active != 0:
            self.panel_hue_circle.Update_Harmony_1(
                self.har_1[4], # hsl_1
                [self.har_1[1], self.har_1[2], self.har_1[3]], # rgb_1, rgb_2, rgb_3
                self.layout.panel_hue_circle_mask.width(),
                self.layout.panel_hue_circle_mask.height(),
                self.gray_natural,
                self.gray_contrast
                )
            self.panel_hue_circle.Update_Harmony_2(
                self.har_2[4],
                [self.har_2[1], self.har_2[2], self.har_2[3]],
                self.layout.panel_hue_circle_mask.width(),
                self.layout.panel_hue_circle_mask.height(),
                self.gray_natural,
                self.gray_contrast
                )
            self.panel_hue_circle.Update_Harmony_3(
                self.har_3[4],
                [self.har_3[1], self.har_3[2], self.har_3[3]],
                self.layout.panel_hue_circle_mask.width(),
                self.layout.panel_hue_circle_mask.height(),
                self.gray_natural,
                self.gray_contrast
                )
            self.panel_hue_circle.Update_Harmony_4(
                self.har_4[4],
                [self.har_4[1], self.har_4[2], self.har_4[3]],
                self.layout.panel_hue_circle_mask.width(),
                self.layout.panel_hue_circle_mask.height(),
                self.gray_natural,
                self.gray_contrast
                )
            self.panel_hue_circle.Update_Harmony_5(
                self.har_5[4],
                [self.har_5[1], self.har_5[2], self.har_5[3]],
                self.layout.panel_hue_circle_mask.width(),
                self.layout.panel_hue_circle_mask.height(),
                self.gray_natural,
                self.gray_contrast
                )
    def Update_DOT(self):
        self.panel_dots.Update_Panel(
            self.dot_1,
            self.dot_2,
            self.dot_3,
            self.dot_4,
            self.layout.panel_dot_mix.width(),
            self.layout.panel_dot_mix.height()
            )

    #//
    #\\ Display ################################################################
    def Pigment_Display(self):
        # Foreground Color Display
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_1*255, self.rgb_2*255, self.rgb_3*255))
        self.layout.color_1.setStyleSheet(active_color_1)
        # AAA
        if (self.chan_aaa == True and self.gray == False):
            sss_aaa1 = str(self.RGB_Gradient([0, 0, 0], [1, 1, 1]))
        else:
            sss_aaa1 = bg_bw
        # RGB
        if (self.chan_rgb == True and self.gray == False):
            sss_rgb1 = str(self.RGB_Gradient([0, self.rgb_2, self.rgb_3], [1, self.rgb_2, self.rgb_3]))
            sss_rgb2 = str(self.RGB_Gradient([self.rgb_1, 0, self.rgb_3], [self.rgb_1, 1, self.rgb_3]))
            sss_rgb3 = str(self.RGB_Gradient([self.rgb_1, self.rgb_2, 0], [self.rgb_1, self.rgb_2, 1]))
        else:
            sss_rgb1 = bg_alpha
            sss_rgb2 = bg_alpha
            sss_rgb3 = bg_alpha
        # ARD
        if (self.chan_ard == True and self.gray == False):
            if (self.ard_3 != 0 and self.ard_3 != 1):
                sss_ard1 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [0, self.ard_2, self.ard_3], [1, self.ard_2, self.ard_3]))
            if self.ard_3 == 0:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [0, 0, self.ard_3], [1, 0, self.ard_3]))
            if self.ard_3 == 1:
                sss_ard1 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [0, 0, self.ard_3], [1, 0, self.ard_3]))
            sss_ard2 = str(self.ARD_Gradient_Linear(self.layout.ard_2_slider.width(), [self.ard_1, 0, self.ard_3], [self.ard_1, 1, self.ard_3]))
            sss_ard3 = str(self.RGB_Gradient([0, 0, 0], [1, 1, 1]))
        else:
            sss_ard1 = bg_alpha
            sss_ard2 = bg_alpha
            sss_ard3 = bg_alpha
        # HSV
        if (self.chan_hsv == True and self.gray == False):
            sss_hsv1 = str(self.HUE_Gradient("HSV", self.layout.hsv_1_slider.width(), [0, self.hsv_2, self.hsv_3], [1, self.hsv_2, self.hsv_3]))
            sss_hsv2 = str(self.HSV_Gradient(self.layout.hsv_2_slider.width(), [self.hsv_1, 0, self.hsv_3], [self.hsv_1, 1, self.hsv_3]))
            sss_hsv3 = str(self.HSV_Gradient(self.layout.hsv_3_slider.width(), [self.hsv_1, self.hsv_2, 0], [self.hsv_1, self.hsv_2, 1]))
        else:
            sss_hsv1 = bg_alpha
            sss_hsv2 = bg_alpha
            sss_hsv3 = bg_alpha
        # HSL
        if (self.chan_hsl == True and self.gray == False):
            sss_hsl1 = str(self.HUE_Gradient("HSL", self.layout.hsl_1_slider.width(), [0, self.hsl_2, self.hsl_3], [1, self.hsl_2, self.hsl_3]))
            sss_hsl2 = str(self.HSL_Gradient(self.layout.hsl_2_slider.width(), [self.hsl_1, 0, self.hsl_3], [self.hsl_1, 1, self.hsl_3]))
            sss_hsl3 = str(self.HSL_Gradient(self.layout.hsl_3_slider.width(), [self.hsl_1, self.hsl_2, 0], [self.hsl_1, self.hsl_2, 1]))
        else:
            sss_hsl1 = bg_alpha
            sss_hsl2 = bg_alpha
            sss_hsl3 = bg_alpha
        # HCY
        if (self.chan_hcy == True and self.gray == False):
            sss_hcy1 = str(self.HUE_Gradient("HCY", self.layout.hcy_1_slider.width(), [0, self.hcy_2, self.hcy_3], [1, self.hcy_2, self.hcy_3]))
            sss_hcy2 = str(self.HCY_Gradient(self.layout.hcy_2_slider.width(), [self.hcy_1, 0, self.hcy_3], [self.hcy_1, 1, self.hcy_3]))
            sss_hcy3 = str(self.HCY_Gradient(self.layout.hcy_3_slider.width(), [self.hcy_1, self.hcy_2, 0], [self.hcy_1, self.hcy_2, 1]))
        else:
            sss_hcy1 = bg_alpha
            sss_hcy2 = bg_alpha
            sss_hcy3 = bg_alpha
        # CMY
        if (self.chan_cmy == True and self.gray == False):
            sss_cmy1 = str(self.CMY_Gradient([0, self.cmy_2, self.cmy_3], [1, self.cmy_2, self.cmy_3]))
            sss_cmy2 = str(self.CMY_Gradient([self.cmy_1, 0, self.cmy_3], [self.cmy_1, 1, self.cmy_3]))
            sss_cmy3 = str(self.CMY_Gradient([self.cmy_1, self.cmy_2, 0], [self.cmy_1, self.cmy_2, 1]))
        else:
            sss_cmy1 = bg_alpha
            sss_cmy2 = bg_alpha
            sss_cmy3 = bg_alpha
        # CMYK
        if (self.chan_cmyk == True and self.gray == False):
            sss_cmyk1 = str(self.CMYK_Gradient(self.layout.cmyk_1_slider.width(), [0, self.cmyk_2, self.cmyk_3, self.cmyk_4], [1, self.cmyk_2, self.cmyk_3, self.cmyk_4]))
            sss_cmyk2 = str(self.CMYK_Gradient(self.layout.cmyk_2_slider.width(), [self.cmyk_1, 0, self.cmyk_3, self.cmyk_4], [self.cmyk_1, 1, self.cmyk_3, self.cmyk_4]))
            sss_cmyk3 = str(self.CMYK_Gradient(self.layout.cmyk_3_slider.width(), [self.cmyk_1, self.cmyk_2, 0, self.cmyk_4], [self.cmyk_1, self.cmyk_2, 1, self.cmyk_4]))
            sss_cmyk4 = str(self.CMYK_Gradient(self.layout.cmyk_4_slider.width(), [self.cmyk_1, self.cmyk_2, self.cmyk_3, 0], [self.cmyk_1, self.cmyk_2, self.cmyk_3, 1]))
        else:
            sss_cmyk1 = bg_alpha
            sss_cmyk2 = bg_alpha
            sss_cmyk3 = bg_alpha
            sss_cmyk4 = bg_alpha
        # KKK
        if (self.chan_kkk == True and self.gray == False):
            if self.kkk_lock == False:
                sss_kkk1 = str(self.KKK_Gradient(1, 1, 1))
            if self.kkk_lock == True:
                sss_kkk1 = str(self.KKK_Gradient(self.rgb_1, self.rgb_2, self.rgb_3))
        else:
            sss_kkk1 = bg_alpha
        # Hex Color
        hex = self.Pigment_2_HEX()
        self.layout.hex_string.setText(str(hex))
        # Harmony
        if self.harmony_active != 0:
            self.layout.harmony_1.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_1[1]*255, self.har_1[2]*255, self.har_1[3]*255)))
            self.layout.harmony_2.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_2[1]*255, self.har_2[2]*255, self.har_2[3]*255)))
            self.layout.harmony_3.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_3[1]*255, self.har_3[2]*255, self.har_3[3]*255)))
            self.layout.harmony_4.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_4[1]*255, self.har_4[2]*255, self.har_4[3]*255)))
            self.layout.harmony_5.setStyleSheet(str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.har_5[1]*255, self.har_5[2]*255, self.har_5[3]*255)))
        # ForeGround Color
        if self.panel_active == "FGC":
            if self.gray == False:
                if self.kkk_lock == False:
                    foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.rgb_1*255, self.rgb_2*255, self.rgb_3*255))
                if self.kkk_lock == True:
                    foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.rgb_k1*255, self.rgb_k2*255, self.rgb_k3*255))
                self.layout.panel_fgc.setStyleSheet(foreground_color)
            if self.gray == True:
                foreground_color = str("QWidget { background-color: rgb(%f, %f, %f); }" % (self.aaa_1*kritaRGB, self.aaa_1*kritaRGB, self.aaa_1*kritaRGB))
                self.layout.panel_fgc.setStyleSheet(foreground_color)
        else:
            self.layout.panel_fgc.setStyleSheet(bg_unseen)
        # RGB Color
        if self.panel_active == "RGB":
            if self.gray == False:
                self.panel_uvd.Setup("COLOR")
            if self.gray == True:
                self.panel_uvd.Setup("GRAY")
        else:
            self.panel_uvd.Setup("NONE")
        # ARD Color
        if self.panel_active == "ARD":
            if self.gray == False:
                self.panel_ard.Setup("COLOR")
            if self.gray == True:
                self.panel_ard.Setup("GRAY")
        else:
            self.panel_ard.Setup("NONE")
        # HSV Color
        if self.panel_active == "HSV":
            if self.gray == False:
                self.panel_hsv.Render("COLOR")
            if self.gray == True:
                self.panel_hsv.Render("GRAY")
        else:
            self.panel_hsv.Render("NONE")
        # HSL Color
        if self.panel_active == "HSL":
            if self.gray == False:
                self.panel_hsl_4.Render("COLOR")
            if self.gray == True:
                self.panel_hsl_4.Render("GRAY")
        else:
            self.panel_hsl_4.Render("NONE")
        # HUE Color
        if self.panel_active == "HUE":
            if self.harmony_active == 0:
                if self.gray == False:
                    self.layout.panel_hue.setStyleSheet(bg_alpha)
                    self.layout.panel_hue_box.setStyleSheet(bg_unseen)
                    self.panel_hue_circle.Render("COLOR")
                    if self.pan_sec == "TRIANGLE":
                        self.panel_triangle.Render("COLOR")
                    else:
                        self.panel_triangle.Render("NONE")
                    if self.pan_sec == "SQUARE":
                        self.panel_square.Render("COLOR")
                    else:
                        self.panel_square.Render("NONE")
                    if self.pan_sec == "DIAMOND":
                        self.panel_diamond.Render("COLOR")
                    else:
                        self.panel_diamond.Render("NONE")
                if self.gray == True:
                    self.layout.panel_hue.setStyleSheet(bg_alpha)
                    self.layout.panel_hue_box.setStyleSheet(bg_unseen)
                    self.panel_hue_circle.Render("GRAY")
                    if self.pan_sec == "TRIANGLE":
                        self.panel_triangle.Render("GRAY")
                    else:
                        self.panel_triangle.Render("NONE")
                    if self.pan_sec == "SQUARE":
                        self.panel_square.Render("GRAY")
                    else:
                        self.panel_square.Render("NONE")
                    if self.pan_sec == "DIAMOND":
                        self.panel_diamond.Render("GRAY")
                    else:
                        self.panel_diamond.Render("NONE")
            if self.harmony_active != 0:
                if self.harmony_index == "Monochromatic":
                    self.panel_hue_circle.Render("HARMONY")
                    self.panel_hue_circle.Harmony("Monochromatic")
                if self.harmony_index == "Complemantary":
                    self.panel_hue_circle.Render("HARMONY")
                    self.panel_hue_circle.Harmony("Complemantary")
                if self.harmony_index == "Analogous":
                    self.panel_hue_circle.Render("HARMONY")
                    self.panel_hue_circle.Harmony("Analogous")
                if self.harmony_index == "Split Complemantary":
                    self.panel_hue_circle.Render("HARMONY")
                    self.panel_hue_circle.Harmony("Split Complemantary")
                if self.harmony_index == "Double Split Complemantary":
                    self.panel_hue_circle.Render("HARMONY")
                    self.panel_hue_circle.Harmony("Double Split Complemantary")
                if self.pan_sec == "TRIANGLE":
                    self.panel_triangle.Render("COLOR")
                else:
                    self.panel_triangle.Render("NONE")
                if self.pan_sec == "SQUARE":
                    self.panel_square.Render("COLOR")
                else:
                    self.panel_square.Render("NONE")
                if self.pan_sec == "DIAMOND":
                    self.panel_diamond.Render("COLOR")
                else:
                    self.panel_diamond.Render("NONE")
        else:
            self.panel_hue_circle.Render("NONE")
            self.panel_triangle.Render("NONE")
            self.panel_square.Render("NONE")
            self.panel_diamond.Render("NONE")
        # DOTs
        if self.dot_active == True:
            self.Update_DOT()
        # Object
        if self.obj_active == True:
            self.Object_Live()
            self.Object_Render()
            self.Object_Alpha()
        # Apply ALL Channel Style Sheets
        self.layout.sof_1_slider.setStyleSheet(bg_alpha)
        self.layout.sof_2_slider.setStyleSheet(bg_alpha)
        self.layout.sof_3_slider.setStyleSheet(bg_alpha)
        self.layout.aaa_1_slider.setStyleSheet(sss_aaa1)
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
        self.layout.hcy_1_slider.setStyleSheet(sss_hcy1)
        self.layout.hcy_2_slider.setStyleSheet(sss_hcy2)
        self.layout.hcy_3_slider.setStyleSheet(sss_hcy3)
        self.layout.cmy_1_slider.setStyleSheet(sss_cmy1)
        self.layout.cmy_2_slider.setStyleSheet(sss_cmy2)
        self.layout.cmy_3_slider.setStyleSheet(sss_cmy3)
        self.layout.cmyk_1_slider.setStyleSheet(sss_cmyk1)
        self.layout.cmyk_2_slider.setStyleSheet(sss_cmyk2)
        self.layout.cmyk_3_slider.setStyleSheet(sss_cmyk3)
        self.layout.cmyk_4_slider.setStyleSheet(sss_cmyk4)
        self.layout.kkk_1_slider.setStyleSheet(sss_kkk1)
    def Pigment_Display_Release(self, SIGNAL_RELEASE):
        # Apply color for Linux Users
        self.Pigment_2_Krita("RELEASE")
        # Dusplay Release Color
        if self.kkk_lock == False:
            active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_1*255, self.rgb_2*255, self.rgb_3*255))
        if self.kkk_lock == True:
            active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (self.rgb_k1*255, self.rgb_k2*255, self.rgb_k3*255))
        self.layout.color_2.setStyleSheet(active_color_2)
        # Clean Up
        self.zoom = 0
        self.layout.label_percent.setText("")
    def Mixer_Display(self):
        # Mixer Tint, Tone, Shade
        if (self.color_tts[0] == "True" and self.layout.tts.isChecked() == True and self.gray == False):
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
        if (self.layout.mix.isChecked() == True and self.layout.mix_index.currentText() == "RGB" and self.gray == False):
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
        if (self.layout.mix.isChecked() == True and self.layout.mix_index.currentText() == "ARD" and self.gray == False):
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
        if (self.layout.mix.isChecked() == True and self.layout.mix_index.currentText() == "HSV" and self.gray == False):
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
        if (self.layout.mix.isChecked() == True and self.layout.mix_index.currentText() == "HSL" and self.gray == False):
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
        if (self.layout.mix.isChecked() == True and self.layout.mix_index.currentText() == "CMYK" and self.gray == False):
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
    # Aspect Ratio
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
        self.hcy_1_slider.Update(self.hcy_1, self.layout.hcy_1_slider.width())
        self.hcy_2_slider.Update(self.hcy_2, self.layout.hcy_2_slider.width())
        self.hcy_3_slider.Update(self.hcy_3, self.layout.hcy_3_slider.width())
        self.cmy_1_slider.Update(self.cmy_1, self.layout.cmy_1_slider.width())
        self.cmy_2_slider.Update(self.cmy_2, self.layout.cmy_2_slider.width())
        self.cmy_3_slider.Update(self.cmy_3, self.layout.cmy_3_slider.width())
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.kkk_1_slider.Update((self.kkk_0-kritaKKKmin)/kritaKKKdelta, self.layout.kkk_1_slider.width())
        # Relocate Mixer Handle due to Size Variation
        self.mixer_tint.Update(self.spacer_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.spacer_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.spacer_shade, self.layout.shade.width())
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.layout.rgb_g1.width())
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.layout.rgb_g2.width())
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.layout.rgb_g3.width())
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.layout.ard_g1.width())
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.layout.ard_g2.width())
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.layout.ard_g3.width())
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.layout.hsv_g1.width())
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.layout.hsv_g2.width())
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.layout.hsv_g3.width())
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.layout.hsl_g1.width())
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.layout.hsl_g2.width())
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.layout.hsl_g3.width())
        # self.mixer_hcy_g1.Update(self.spacer_hcy_g1, self.layout.hcy_g1.width())
        # self.mixer_hcy_g2.Update(self.spacer_hcy_g2, self.layout.hcy_g2.width())
        # self.mixer_hcy_g3.Update(self.spacer_hcy_g3, self.layout.hcy_g3.width())
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.layout.cmyk_g1.width())
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.layout.cmyk_g2.width())
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.layout.cmyk_g3.width())

        # Redimension Frames to be Centered
        self.Box_Ratio()

        # Relocate Object Alpha Handle due to Size Variation
        if self.layout.dot.isChecked() == True:
            self.panel_dots.Location(self.dot_location_x, self.dot_location_y, self.layout.panel_dot_mix.width(), self.layout.panel_dot_mix.height())

        # Relocate Object Alpha Handle due to Size Variation
        if self.obj_active == True:
            self.Object_Render()
            self.Object_Alpha()
            self.panel_obj.Location(self.obj_location_x, self.obj_location_y, self.layout.panel_obj_mix.width(), self.layout.panel_obj_mix.height())

        # Relocate Panel Cursor due to Size Variation
        self.UVD_Update()
        self.ARD_Update()
        self.Update_Panel_HSV()
        self.Update_Panel_HSL()
        self.Update_Panel_HUE()
        self.Update_DOT()
        # Update Display
        self.Pigment_Display()
    def Box_Ratio(self):
        # Harmony
        self.harmony_1.Update(self.layout.harmony_1.width(), self.layout.harmony_1.height())
        self.harmony_2.Update(self.layout.harmony_2.width(), self.layout.harmony_2.height())
        self.harmony_3.Update(self.layout.harmony_3.width(), self.layout.harmony_3.height())
        self.harmony_4.Update(self.layout.harmony_4.width(), self.layout.harmony_4.height())
        self.harmony_5.Update(self.layout.harmony_5.width(), self.layout.harmony_5.height())

        # UVD Panel Ratio Adjust to maintain Square
        uvd_width = self.layout.panel_uvd.width()
        uvd_height = self.layout.panel_uvd.height()
        if uvd_width <= 0:
            uvd_width = 1
        if uvd_height <= 0:
            uvd_height = 1
        if uvd_width >= uvd_height:
            self.layout.panel_uvd_mask.setMaximumWidth(uvd_height)
            self.layout.panel_uvd_mask.setMaximumHeight(uvd_height)
        if uvd_width < uvd_height:
            self.layout.panel_uvd_mask.setMaximumWidth(uvd_width)
            self.layout.panel_uvd_mask.setMaximumHeight(uvd_width)

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
        self.layout.panel_hue_circle_mask.setGeometry(0,0,self.layout.panel_hue_box.width(),self.layout.panel_hue_box.height())
        region = QRegion(0,0, self.layout.panel_hue_circle_mask.width(),self.layout.panel_hue_circle_mask.height(), QRegion.Ellipse)
        self.layout.panel_hue_circle_mask.setMask(region)
        if self.pan_sec == "DOT":
            self.layout.panel_hue_regular_mask.setGeometry(0,0, 0,0)
        if self.pan_sec == "TRIANGLE":
            # Adjust Regular Geometry
            d1 = 0.28754
            d2 = 0.132
            d3 = 0.637388
            d4 = 0.735992
            self.layout.panel_hue_regular_mask.setGeometry(self.layout.panel_hue_box.width()*d1,self.layout.panel_hue_box.height()*d2, self.layout.panel_hue_box.width()*d3,self.layout.panel_hue_box.height()*d4)
            # Adjust Mask Regular
            region_polygon = QPolygon([
                QPoint(0, 0),
                QPoint(0, self.layout.panel_hue_regular_mask.height()),
                QPoint(self.layout.panel_hue_regular_mask.width(), self.layout.panel_hue_regular_mask.height()/2)
                ])
            self.layout.panel_hue_regular_mask.setMask(QRegion(region_polygon))
        if self.pan_sec == "SQUARE":
            # Adjust Regular Geometry
            d1 = 0.2
            d2 = 1 - (2*d1)
            self.layout.panel_hue_regular_mask.setGeometry(self.layout.panel_hue_box.width()*d1,self.layout.panel_hue_box.height()*d1, self.layout.panel_hue_box.width()*d2,self.layout.panel_hue_box.height()*d2)
            # Adjust Mask Regular
            region_polygon = QPolygon([
                QPoint(0, 0),
                QPoint(self.layout.panel_hue_regular_mask.width(), 0),
                QPoint(self.layout.panel_hue_regular_mask.width(), self.layout.panel_hue_regular_mask.height()),
                QPoint(0, self.layout.panel_hue_regular_mask.height())
                ])
            self.layout.panel_hue_regular_mask.setMask(QRegion(region_polygon))
        if self.pan_sec == "DIAMOND":
            # Adjust Regular Geometry
            d1 = 0.075
            d2 = 1 - (2*d1)
            self.layout.panel_hue_regular_mask.setGeometry(self.layout.panel_hue_box.width()*d1,self.layout.panel_hue_box.height()*d1, self.layout.panel_hue_box.width()*d2,self.layout.panel_hue_box.height()*d2)
            # Adjust Mask Regular
            region_polygon = QPolygon([
                QPoint(self.layout.panel_hue_regular_mask.width()/2, 0),
                QPoint(self.layout.panel_hue_regular_mask.width(), self.layout.panel_hue_regular_mask.height()/2),
                QPoint(self.layout.panel_hue_regular_mask.width()/2, self.layout.panel_hue_regular_mask.height()),
                QPoint(0, self.layout.panel_hue_regular_mask.height()/2)
                ])
            self.layout.panel_hue_regular_mask.setMask(QRegion(region_polygon))

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
                self.angle_live = 0
                self.Color_APPLY("AAA", aaa1, 0, 0, 0)
            elif (hex[0] == "#" and length == 7):
                # Parse Hex Code
                hex1 = int(format(int(hex[1:3],16),'02d'))
                hex2 = int(format(int(hex[3:5],16),'02d'))
                hex3 = int(format(int(hex[5:7],16),'02d'))
                # Apply to Pigment
                rgb1 = hex1 / hexRGB
                rgb2 = hex2 / hexRGB
                rgb3 = hex3 / hexRGB
                self.Color_ANGLE(rgb1, rgb2, rgb3)
                self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
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
                rgb = self.cmyk_to_rgb(cmyk1, cmyk2, cmyk3, cmyk4)
                self.Color_ANGLE(rgb[0], rgb[1], rgb[2])
                self.Color_APPLY("CMYK", cmyk1, cmyk2, cmyk3, cmyk4)
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
    #\\ SOF ####################################################################
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
    #\\ Channels ###############################################################
    def Pigment_KKK_1_Lock(self):
        if self.layout.kkk_1_lock.isChecked():
            self.kkk_lock = True
            self.icon_lock = self.Icon_Lock(self.color_accent)
            self.svg_lock_kkk_1.load(self.icon_lock)
        else:
            self.kkk_lock = False
            self.icon_lock = self.Icon_Lock(self.gray_contrast)
            self.svg_lock_kkk_1.load(self.icon_lock)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Half(self):
        self.aaa_1 = half
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaAAA)
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Half(self):
        self.rgb_1 = half
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Half(self):
        self.rgb_2 = half
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Half(self):
        self.rgb_3 = half
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
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
        self.ard_1_slider.Update(ang/360, self.layout.hsv_1_slider.width())
        self.layout.ard_1_value.setValue((ang/360) * kritaANG)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Half(self):
        self.ard_2 = half
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.ard_2_value.setValue(self.ard_2 * kritaRDL)
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
        self.ard_3_slider.Update(diagonal/360, self.layout.hsv_1_slider.width())
        self.layout.ard_3_value.setValue((diagonal/360) * kritaRDL)
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
        self.hsv_1_slider.Update(hue/360, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue((hue/360) * kritaHUE)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Half(self):
        self.hsv_2 = half
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVLCY)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Half(self):
        self.hsv_3 = half
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVLCY)
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
        self.hsl_1_slider.Update(hue/360, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue((hue/360) * kritaHUE)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Half(self):
        self.hsl_2 = half
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVLCY)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Half(self):
        self.hsl_3 = half
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVLCY)
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
        self.hcy_1_slider.Update(hue/360, self.layout.hcy_1_slider.width())
        self.layout.hcy_1_value.setValue((hue/360) * kritaHUE)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Half(self):
        self.hcy_2 = half
        self.hcy_2_slider.Update(self.hcy_2, self.layout.hcy_2_slider.width())
        self.layout.hcy_2_value.setValue(self.hcy_2 * kritaSVLCY)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Half(self):
        self.hcy_3 = half
        self.hcy_3_slider.Update(self.hcy_3, self.layout.hcy_3_slider.width())
        self.layout.hcy_3_value.setValue(self.hcy_3 * kritaSVLCY)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Half(self):
        self.cmy_1 = half
        self.cmy_1_slider.Update(self.cmy_1, self.layout.cmy_1_slider.width())
        self.layout.cmy_1_value.setValue(self.cmy_1 * kritaRGB)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Half(self):
        self.cmy_2 = half
        self.cmy_2_slider.Update(self.cmy_2, self.layout.cmy_2_slider.width())
        self.layout.cmy_2_value.setValue(self.cmy_2 * kritaRGB)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Half(self):
        self.cmy_3 = half
        self.cmy_3_slider.Update(self.cmy_3, self.layout.cmy_3_slider.width())
        self.layout.cmy_3_value.setValue(self.cmy_3 * kritaRGB)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Half(self):
        self.cmyk_1 = half
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Half(self):
        self.cmyk_2 = half
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Half(self):
        self.cmyk_3 = half
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Half(self):
        self.cmyk_4 = half
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Half(self):
        self.kkk_0 = 6500
        self.kkk_1_slider.Update(0.5, self.layout.kkk_1_slider.width())
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Minus(self):
        self.aaa_1 = self.aaa_1 - unitRGB
        if self.aaa_1 <= zero:
            self.aaa_1 = zero
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaRGB)
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Minus(self):
        self.rgb_1 = self.rgb_1 - unitRGB
        if self.rgb_1 <= zero:
            self.rgb_1 = zero
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Minus(self):
        self.rgb_2 = self.rgb_2 - unitRGB
        if self.rgb_2 <= zero:
            self.rgb_2 = zero
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Minus(self):
        self.rgb_3 = self.rgb_3 - unitRGB
        if self.rgb_3 <= zero:
            self.rgb_3 = zero
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Minus(self):
        self.ard_1 = self.ard_1 - unitANG
        if self.ard_1 <= zero:
            self.ard_1 = zero
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.layout.ard_1_value.setValue(self.ard_1 * kritaANG)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Minus(self):
        self.ard_2 = self.ard_2 - unitRDL
        if self.ard_2 <= zero:
            self.ard_2 = zero
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.ard_2_value.setValue(self.ard_2 * kritaRDL)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Minus(self):
        self.ard_3 = self.ard_3 - unitRDL
        if self.ard_3 <= zero:
            self.ard_3 = zero
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
        self.layout.ard_3_value.setValue(self.ard_3 * kritaRDL)
        self.Pigment_Convert("ARD", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Minus(self):
        self.hsv_1 = self.hsv_1 - unitHUE
        if self.hsv_1 <= zero:
            self.hsv_1 = zero
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Minus(self):
        self.hsv_2 = self.hsv_2 - unitSVLY
        if self.hsv_2 <= zero:
            self.hsv_2 = zero
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVLCY)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Minus(self):
        self.hsv_3 = self.hsv_3 - unitSVLY
        if self.hsv_3 <= zero:
            self.hsv_3 = zero
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVLCY)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Minus(self):
        self.hsl_1 = self.hsl_1 - unitHUE
        if self.hsl_1 <= zero:
            self.hsl_1 = zero
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Minus(self):
        self.hsl_2 = self.hsl_2 - unitSVLY
        if self.hsl_2 <= zero:
            self.hsl_2 = zero
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVLCY)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Minus(self):
        self.hsl_3 = self.hsl_3 - unitSVLY
        if self.hsl_3 <= zero:
            self.hsl_3 = zero
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVLCY)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Minus(self):
        self.hcy_1 = self.hcy_1 - unitHUE
        if self.hcy_1 <= zero:
            self.hcy_1 = zero
        self.hcy_1_slider.Update(self.hcy_1, self.layout.hcy_1_slider.width())
        self.layout.hcy_1_value.setValue(self.hcy_1 * kritaHUE)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Minus(self):
        self.hcy_2 = self.hcy_2 - unitSVLY
        if self.hcy_2 <= zero:
            self.hcy_2 = zero
        self.hcy_2_slider.Update(self.hcy_2, self.layout.hcy_2_slider.width())
        self.layout.hcy_2_value.setValue(self.hcy_2 * kritaSVLCY)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Minus(self):
        self.hcy_3 = self.hcy_3 - unitSVLY
        if self.hcy_3 <= zero:
            self.hcy_3 = zero
        self.hcy_3_slider.Update(self.hcy_3, self.layout.hcy_3_slider.width())
        self.layout.hcy_3_value.setValue(self.hcy_3 * kritaSVLCY)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Minus(self):
        self.cmy_1 = self.cmy_1 - unitCMY
        if self.cmy_1 <= zero:
            self.cmy_1 = zero
        self.cmy_1_slider.Update(self.cmy_1, self.layout.cmy_1_slider.width())
        self.layout.cmy_1_value.setValue(self.cmy_1 * kritaRGB)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Minus(self):
        self.cmy_2 = self.cmy_2 - unitCMY
        if self.cmy_2 <= zero:
            self.cmy_2 = zero
        self.cmy_2_slider.Update(self.cmy_2, self.layout.cmy_2_slider.width())
        self.layout.cmy_2_value.setValue(self.cmy_2 * kritaRGB)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Minus(self):
        self.cmy_3 = self.cmy_3 - unitCMY
        if self.cmy_3 <= zero:
            self.cmy_3 = zero
        self.cmy_3_slider.Update(self.cmy_3, self.layout.cmy_3_slider.width())
        self.layout.cmy_3_value.setValue(self.cmy_3 * kritaRGB)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Minus(self):
        self.cmyk_1 = self.cmyk_1 - unitCMYK
        if self.cmyk_1 <= zero:
            self.cmyk_1 = zero
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Minus(self):
        self.cmyk_2 = self.cmyk_2 - unitCMYK
        if self.cmyk_2 <= zero:
            self.cmyk_2 = zero
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Minus(self):
        self.cmyk_3 = self.cmyk_3 - unitCMYK
        if self.cmyk_3 <= zero:
            self.cmyk_3 = zero
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Minus(self):
        self.cmyk_4 = self.cmyk_4 - unitCMYK
        if self.cmyk_4 <= zero:
            self.cmyk_4 = zero
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_4_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Minus(self):
        self.kkk_0 = self.kkk_0 - kritaKKKunit
        if self.kkk_0 <= zero:
            self.kkk_0 = zero
        self.kkk_1_slider.Update((self.kkk_0 - kritaKKKmin) / kritaKKKdelta, self.layout.kkk_1_slider.width())
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Plus(self):
        self.aaa_1 = self.aaa_1 + unitAAA
        if self.aaa_1 >= unit:
            self.aaa_1 = unit
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.aaa_1_value.setValue(self.aaa_1 * kritaAAA)
        self.Pigment_Convert("AAA", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_1_Plus(self):
        self.rgb_1 = self.rgb_1 + unitRGB
        if self.rgb_1 >= unit:
            self.rgb_1 = unit
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.rgb_1_value.setValue(self.rgb_1 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_2_Plus(self):
        self.rgb_2 = self.rgb_2 + unitRGB
        if self.rgb_2 >= unit:
            self.rgb_2 = unit
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.rgb_2_value.setValue(self.rgb_2 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_RGB_3_Plus(self):
        self.rgb_3 = self.rgb_3 + unitRGB
        if self.rgb_3 >= unit:
            self.rgb_3 = unit
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.rgb_3_value.setValue(self.rgb_3 * kritaRGB)
        self.Pigment_Convert("RGB", 0)
        self.Pigment_Display_Release(0)
    def Pigment_ARD_1_Plus(self):
        self.ard_1 = self.ard_1 + unitANG
        if self.ard_1 >= unit:
            self.ard_1 = unit
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.layout.ard_1_value.setValue(self.ard_1 * kritaANG)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_2_Plus(self):
        self.ard_2 = self.ard_2 + unitRDL
        if self.ard_2 >= unit:
            self.ard_2 = unit
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.ard_2_value.setValue(self.ard_2 * kritaRDL)
        self.Pigment_Convert("ARD", "IGNORE")
        self.Pigment_Display_Release(0)
    def Pigment_ARD_3_Plus(self):
        self.ard_3 = self.ard_3 + unitRDL
        if self.ard_3 >= unit:
            self.ard_3 = unit
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
        self.layout.ard_3_value.setValue(self.ard_3 * kritaRDL)
        self.Pigment_Convert("ARD", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_1_Plus(self):
        self.hsv_1 = self.hsv_1 + unitHUE
        if self.hsv_1 >= unit:
            self.hsv_1 = unit
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.hsv_1_value.setValue(self.hsv_1 * kritaHUE)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Plus(self):
        self.hsv_2 = self.hsv_2 + unitSVLY
        if self.hsv_2 >= unit:
            self.hsv_2 = unit
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.hsv_2_value.setValue(self.hsv_2 * kritaSVLCY)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Plus(self):
        self.hsv_3 = self.hsv_3 + unitSVLY
        if self.hsv_3 >= unit:
            self.hsv_3 = unit
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.hsv_3_value.setValue(self.hsv_3 * kritaSVLCY)
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_1_Plus(self):
        self.hsl_1 = self.hsl_1 + unitHUE
        if self.hsl_1 >= unit:
            self.hsl_1 = unit
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.hsl_1_value.setValue(self.hsl_1 * kritaHUE)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_2_Plus(self):
        self.hsl_2 = self.hsl_2 + unitSVLY
        if self.hsl_2 >= unit:
            self.hsl_2 = unit
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.hsl_2_value.setValue(self.hsl_2 * kritaSVLCY)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSL_3_Plus(self):
        self.hsl_3 = self.hsl_3 + unitSVLY
        if self.hsl_3 >= unit:
            self.hsl_3 = unit
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.hsl_3_value.setValue(self.hsl_3 * kritaSVLCY)
        self.Pigment_Convert("HSL", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_1_Plus(self):
        self.hcy_1 = self.hcy_1 + unitHUE
        if self.hcy_1 >= unit:
            self.hcy_1 = unit
        self.hcy_1_slider.Update(self.hcy_1, self.layout.hcy_1_slider.width())
        self.layout.hcy_1_value.setValue(self.hcy_1 * kritaHUE)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_2_Plus(self):
        self.hcy_2 = self.hcy_2 + unitSVLY
        if self.hcy_2 >= unit:
            self.hcy_2 = unit
        self.hcy_2_slider.Update(self.hcy_2, self.layout.hcy_2_slider.width())
        self.layout.hcy_2_value.setValue(self.hcy_2 * kritaSVLCY)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HCY_3_Plus(self):
        self.hcy_3 = self.hcy_3 + unitSVLY
        if self.hcy_3 >= unit:
            self.hcy_3 = unit
        self.hcy_3_slider.Update(self.hcy_3, self.layout.hcy_3_slider.width())
        self.layout.hcy_3_value.setValue(self.hcy_3 * kritaSVLCY)
        self.Pigment_Convert("HCY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_1_Plus(self):
        self.cmy_1 = self.cmy_1 + unitCMY
        if self.cmy_1 >= unit:
            self.cmy_1 = unit
        self.cmy_1_slider.Update(self.cmy_1, self.layout.cmy_1_slider.width())
        self.layout.cmy_1_value.setValue(self.cmy_1 * kritaCMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_2_Plus(self):
        self.cmy_2 = self.cmy_2 + unitCMY
        if self.cmy_2 >= unit:
            self.cmy_2 = unit
        self.cmy_2_slider.Update(self.cmy_2, self.layout.cmy_2_slider.width())
        self.layout.cmy_2_value.setValue(self.cmy_2 * kritaCMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMY_3_Plus(self):
        self.cmy_3 = self.cmy_3 + unitCMY
        if self.cmy_3 >= unit:
            self.cmy_3 = unit
        self.cmy_3_slider.Update(self.cmy_3, self.layout.cmy_3_slider.width())
        self.layout.cmy_3_value.setValue(self.cmy_3 * kritaCMY)
        self.Pigment_Convert("CMY", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_1_Plus(self):
        self.cmyk_1 = self.cmyk_1 + unitCMYK
        if self.cmyk_1 >= unit:
            self.cmyk_1 = unit
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.cmyk_1_value.setValue(self.cmyk_1 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_2_Plus(self):
        self.cmyk_2 = self.cmyk_2 + unitCMYK
        if self.cmyk_2 >= unit:
            self.cmyk_2 = unit
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.cmyk_2_value.setValue(self.cmyk_2 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_3_Plus(self):
        self.cmyk_3 = self.cmyk_3 + unitCMYK
        if self.cmyk_3 >= unit:
            self.cmyk_3 = unit
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_3 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_CMYK_4_Plus(self):
        self.cmyk_4 = self.cmyk_4 + unitCMYK
        if self.cmyk_4 >= unit:
            self.cmyk_4 = unit
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.cmyk_3_value.setValue(self.cmyk_4 * kritaCMYK)
        self.Pigment_Convert("CMYK", 0)
        self.Pigment_Display_Release(0)
    def Pigment_KKK_1_Plus(self):
        self.kkk_0 = self.kkk_0 + kritaKKKunit
        if self.kkk_0 >= kritaKKKmax:
            self.kkk_0 = kritaKKKmax
        self.kkk_1_slider.Update((self.kkk_0 - kritaKKKmin) / kritaKKKdelta, self.layout.kkk_1_slider.width())
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Slider_Modify(self, SIGNAL_VALUE):
        self.aaa_1 = SIGNAL_VALUE
        send = int(self.aaa_1 * kritaAAA)
        self.layout.aaa_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("AAA", 0)
    def Pigment_RGB_1_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_1 = SIGNAL_VALUE
        send = int(self.rgb_1 * kritaRGB)
        self.layout.rgb_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_2_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_2 = SIGNAL_VALUE
        send = int(self.rgb_2 * kritaRGB)
        self.layout.rgb_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_3_Slider_Modify(self, SIGNAL_VALUE):
        self.rgb_3 = SIGNAL_VALUE
        send = int(self.rgb_3 * kritaRGB)
        self.layout.rgb_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_ARD_1_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_1 = SIGNAL_VALUE
        send = int(self.ard_1 * kritaANG)
        self.layout.ard_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_2_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_2 = SIGNAL_VALUE
        send = int(self.ard_2 * kritaRDL)
        self.layout.ard_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_3_Slider_Modify(self, SIGNAL_VALUE):
        self.ard_3 = SIGNAL_VALUE
        send = int(self.ard_3 * kritaRDL)
        self.layout.ard_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_HSV_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_1 = SIGNAL_VALUE
        send = int(self.hsv_1 * kritaHUE)
        self.layout.hsv_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_2 = SIGNAL_VALUE
        send = int(self.hsv_2 * kritaSVLCY)
        self.layout.hsv_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hsv_3 = SIGNAL_VALUE
        send = int(self.hsv_3 * kritaSVLCY)
        self.layout.hsv_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSL_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_1 = SIGNAL_VALUE
        send = int(self.hsl_1 * kritaHUE)
        self.layout.hsl_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_2 = SIGNAL_VALUE
        send = int(self.hsl_2 * kritaSVLCY)
        self.layout.hsl_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hsl_3 = SIGNAL_VALUE
        send = int(self.hsl_3 * kritaSVLCY)
        self.layout.hsl_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HCY_1_Slider_Modify(self, SIGNAL_VALUE):
        self.hcy_1 = SIGNAL_VALUE
        send = int(self.hcy_1 * kritaHUE)
        self.layout.hcy_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*360,2))+" º")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_2_Slider_Modify(self, SIGNAL_VALUE):
        self.hcy_2 = SIGNAL_VALUE
        send = int(self.hcy_2 * kritaSVLCY)
        self.layout.hcy_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_3_Slider_Modify(self, SIGNAL_VALUE):
        self.hcy_3 = SIGNAL_VALUE
        send = int(self.hcy_3 * kritaSVLCY)
        self.layout.hcy_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_CMY_1_Slider_Modify(self, SIGNAL_VALUE):
        self.cmy_1 = SIGNAL_VALUE
        send = int(self.cmy_1 * kritaCMY)
        self.layout.cmy_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_2_Slider_Modify(self, SIGNAL_VALUE):
        self.cmy_2 = SIGNAL_VALUE
        send = int(self.cmy_2 * kritaCMY)
        self.layout.cmy_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_3_Slider_Modify(self, SIGNAL_VALUE):
        self.cmy_3 = SIGNAL_VALUE
        send = int(self.cmy_3 * kritaCMY)
        self.layout.cmy_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMYK_1_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_1 = SIGNAL_VALUE
        send = int(self.cmyk_1 * kritaCMYK)
        self.layout.cmyk_1_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_2_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_2 = SIGNAL_VALUE
        send = int(self.cmyk_2 * kritaCMYK)
        self.layout.cmyk_2_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_3_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_3 = SIGNAL_VALUE
        send = int(self.cmyk_3 * kritaCMYK)
        self.layout.cmyk_3_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_4_Slider_Modify(self, SIGNAL_VALUE):
        self.cmyk_4 = SIGNAL_VALUE
        send = int(self.cmyk_4 * kritaCMYK)
        self.layout.cmyk_4_value.setValue(send)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_KKK_1_Slider_Modify(self, SIGNAL_VALUE):
        self.kkk_0 = int((SIGNAL_VALUE * kritaKKKdelta) + kritaKKKmin)
        self.layout.kkk_1_value.setValue(self.kkk_0)
        self.layout.label_percent.setText(str(round(SIGNAL_VALUE*100,2))+" %")
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
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_2_Slider_Release(self, SIGNAL_RELEASE):
        self.zoom = 0
        self.layout.label_percent.setText("")
        self.Pigment_Convert("HSV", 0)
        self.Pigment_Display_Release(0)
    def Pigment_HSV_3_Slider_Release(self, SIGNAL_RELEASE):
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
        self.Pigment_Convert("KKK", 0)
        self.Pigment_Display_Release(0)

    def Pigment_AAA_1_Value_Modify(self):
        self.aaa_1 = self.layout.aaa_1_value.value() / kritaAAA
        self.aaa_1_slider.Update(self.aaa_1, self.layout.aaa_1_slider.width())
        self.layout.label_percent.setText(str(round(self.aaa_1*100,2))+" %")
        self.Pigment_Convert("AAA", 0)
    def Pigment_RGB_1_Value_Modify(self):
        self.rgb_1 = self.layout.rgb_1_value.value() / kritaRGB
        self.rgb_1_slider.Update(self.rgb_1, self.layout.rgb_1_slider.width())
        self.layout.label_percent.setText(str(round(self.rgb_1*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_2_Value_Modify(self):
        self.rgb_2 = self.layout.rgb_2_value.value() / kritaRGB
        self.rgb_2_slider.Update(self.rgb_2, self.layout.rgb_2_slider.width())
        self.layout.label_percent.setText(str(round(self.rgb_2*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_RGB_3_Value_Modify(self):
        self.rgb_3 = self.layout.rgb_3_value.value() / kritaRGB
        self.rgb_3_slider.Update(self.rgb_3, self.layout.rgb_3_slider.width())
        self.layout.label_percent.setText(str(round(self.rgb_3*100,2))+" %")
        self.Pigment_Convert("RGB", 0)
    def Pigment_ARD_1_Value_Modify(self):
        self.ard_1 = self.layout.ard_1_value.value() / kritaANG
        self.ard_1_slider.Update(self.ard_1, self.layout.ard_1_slider.width())
        self.layout.label_percent.setText(str(round(self.ard_1*100,2))+" º")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_2_Value_Modify(self):
        self.ard_2 = self.layout.ard_2_value.value() / kritaRDL
        self.ard_2_slider.Update(self.ard_2, self.layout.ard_2_slider.width())
        self.layout.label_percent.setText(str(round(self.ard_2*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_ARD_3_Value_Modify(self):
        self.ard_3 = self.layout.ard_3_value.value() / kritaRDL
        self.ard_3_slider.Update(self.ard_3, self.layout.ard_3_slider.width())
        self.layout.label_percent.setText(str(round(self.ard_3*100,2))+" %")
        self.Pigment_Convert("ARD", "IGNORE")
    def Pigment_HSV_1_Value_Modify(self):
        self.hsv_1 = self.layout.hsv_1_value.value() / kritaHUE
        self.hsv_1_slider.Update(self.hsv_1, self.layout.hsv_1_slider.width())
        self.layout.label_percent.setText(str(round(self.hsv_1*100,2))+" º")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_2_Value_Modify(self):
        self.hsv_2 = self.layout.hsv_2_value.value() / kritaSVLCY
        self.hsv_2_slider.Update(self.hsv_2, self.layout.hsv_2_slider.width())
        self.layout.label_percent.setText(str(round(self.hsv_2*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSV_3_Value_Modify(self):
        self.hsv_3 = self.layout.hsv_3_value.value() / kritaSVLCY
        self.hsv_3_slider.Update(self.hsv_3, self.layout.hsv_3_slider.width())
        self.layout.label_percent.setText(str(round(self.hsv_3*100,2))+" %")
        self.Pigment_Convert("HSV", 0)
    def Pigment_HSL_1_Value_Modify(self):
        self.hsl_1 = self.layout.hsl_1_value.value() / kritaHUE
        self.hsl_1_slider.Update(self.hsl_1, self.layout.hsl_1_slider.width())
        self.layout.label_percent.setText(str(round(self.hsl_1*100,2))+" º")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_2_Value_Modify(self):
        self.hsl_2 = self.layout.hsl_2_value.value() / kritaSVLCY
        self.hsl_2_slider.Update(self.hsl_2, self.layout.hsl_2_slider.width())
        self.layout.label_percent.setText(str(round(self.hsl_2*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HSL_3_Value_Modify(self):
        self.hsl_3 = self.layout.hsl_3_value.value() / kritaSVLCY
        self.hsl_3_slider.Update(self.hsl_3, self.layout.hsl_3_slider.width())
        self.layout.label_percent.setText(str(round(self.hsl_3*100,2))+" %")
        self.Pigment_Convert("HSL", 0)
    def Pigment_HCY_1_Value_Modify(self):
        self.hcy_1 = self.layout.hcy_1_value.value() / kritaHUE
        self.hcy_1_slider.Update(self.hcy_1, self.layout.hcy_1_slider.width())
        self.layout.label_percent.setText(str(round(self.hcy_1*100,2))+" º")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_2_Value_Modify(self):
        self.hcy_2 = self.layout.hcy_2_value.value() / kritaSVLCY
        self.hcy_2_slider.Update(self.hcy_2, self.layout.hcy_2_slider.width())
        self.layout.label_percent.setText(str(round(self.hcy_2*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_HCY_3_Value_Modify(self):
        self.hcy_3 = self.layout.hcy_3_value.value() / kritaSVLCY
        self.hcy_3_slider.Update(self.hcy_3, self.layout.hcy_3_slider.width())
        self.layout.label_percent.setText(str(round(self.hcy_3*100,2))+" %")
        self.Pigment_Convert("HCY", 0)
    def Pigment_CMY_1_Value_Modify(self):
        self.cmy_1 = self.layout.cmy_1_value.value() / kritaCMY
        self.cmy_1_slider.Update(self.cmy_1, self.layout.cmy_1_slider.width())
        self.layout.label_percent.setText(str(round(self.cmy_1*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_2_Value_Modify(self):
        self.cmy_2 = self.layout.cmy_2_value.value() / kritaCMY
        self.cmy_2_slider.Update(self.cmy_2, self.layout.cmy_2_slider.width())
        self.layout.label_percent.setText(str(round(self.cmy_2*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMY_3_Value_Modify(self):
        self.cmy_3 = self.layout.cmy_3_value.value() / kritaCMY
        self.cmy_3_slider.Update(self.cmy_3, self.layout.cmy_3_slider.width())
        self.layout.label_percent.setText(str(round(self.cmy_3*100,2))+" %")
        self.Pigment_Convert("CMY", 0)
    def Pigment_CMYK_1_Value_Modify(self):
        self.cmyk_1 = self.layout.cmyk_1_value.value() / kritaCMYK
        self.cmyk_1_slider.Update(self.cmyk_1, self.layout.cmyk_1_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_1*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_2_Value_Modify(self):
        self.cmyk_2 = self.layout.cmyk_2_value.value() / kritaCMYK
        self.cmyk_2_slider.Update(self.cmyk_2, self.layout.cmyk_2_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_2*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_3_Value_Modify(self):
        self.cmyk_3 = self.layout.cmyk_3_value.value() / kritaCMYK
        self.cmyk_3_slider.Update(self.cmyk_3, self.layout.cmyk_3_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_3*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_CMYK_4_Value_Modify(self):
        self.cmyk_4 = self.layout.cmyk_4_value.value() / kritaCMYK
        self.cmyk_4_slider.Update(self.cmyk_4, self.layout.cmyk_4_slider.width())
        self.layout.label_percent.setText(str(round(self.cmyk_4*100,2))+" %")
        self.Pigment_Convert("CMYK", 0)
    def Pigment_KKK_1_Value_Modify(self):
        self.kkk_0 = self.layout.kkk_1_value.value()
        self.kkk_1_slider.Update((self.kkk_0 - kritaKKKmin) / kritaKKKdelta, self.layout.kkk_1_slider.width())
        self.layout.label_percent.setText(str(round(((self.kkk_0 - kritaKKKmin) / kritaKKKdelta)*100,2))+" %")
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
            self.Settings_Load_Misc()
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
            self.Settings_Load_Misc()

    #//
    #\\ Palette ################################################################
    def Color_00_APPLY(self, SIGNAL_CLICKS):
        if self.color_00[0] == "True":
            self.Color_ANGLE(self.color_00[1], self.color_00[2], self.color_00[3])
            self.Color_APPLY("RGB", self.color_00[1], self.color_00[2], self.color_00[3], 0)
            self.Pigment_Display_Release(0)
    def Color_00_SAVE(self, SIGNAL_CLICKS):
        self.color_00 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_00[1]*255, self.color_00[2]*255, self.color_00[3]*255))
        self.layout.cor_00.setStyleSheet(color)
    def Color_00_CLEAN(self, SIGNAL_CLICKS):
        self.color_00 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_00.setStyleSheet(bg_alpha)

    def Color_01_APPLY(self, SIGNAL_CLICKS):
        if self.color_01[0] == "True":
            self.Color_ANGLE(self.color_01[1], self.color_01[2], self.color_01[3])
            self.Color_APPLY("RGB", self.color_01[1], self.color_01[2], self.color_01[3], 0)
            self.Pigment_Display_Release(0)
    def Color_01_SAVE(self, SIGNAL_CLICKS):
        self.color_01 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_01[1]*255, self.color_01[2]*255, self.color_01[3]*255))
        self.layout.cor_01.setStyleSheet(color)
    def Color_01_CLEAN(self, SIGNAL_CLICKS):
        self.color_01 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_01.setStyleSheet(bg_alpha)

    def Color_02_APPLY(self, SIGNAL_CLICKS):
        if self.color_02[0] == "True":
            self.Color_ANGLE(self.color_02[1], self.color_02[2], self.color_02[3])
            self.Color_APPLY("RGB", self.color_02[1], self.color_02[2], self.color_02[3], 0)
            self.Pigment_Display_Release(0)
    def Color_02_SAVE(self, SIGNAL_CLICKS):
        self.color_02 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_02[1]*255, self.color_02[2]*255, self.color_02[3]*255))
        self.layout.cor_02.setStyleSheet(color)
    def Color_02_CLEAN(self, SIGNAL_CLICKS):
        self.color_02 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_02.setStyleSheet(bg_alpha)

    def Color_03_APPLY(self, SIGNAL_CLICKS):
        if self.color_03[0] == "True":
            self.Color_ANGLE(self.color_03[1], self.color_03[2], self.color_03[3])
            self.Color_APPLY("RGB", self.color_03[1], self.color_03[2], self.color_03[3], 0)
            self.Pigment_Display_Release(0)
    def Color_03_SAVE(self, SIGNAL_CLICKS):
        self.color_03 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_03[1]*255, self.color_03[2]*255, self.color_03[3]*255))
        self.layout.cor_03.setStyleSheet(color)
    def Color_03_CLEAN(self, SIGNAL_CLICKS):
        self.color_03 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_03.setStyleSheet(bg_alpha)

    def Color_04_APPLY(self, SIGNAL_CLICKS):
        if self.color_04[0] == "True":
            self.Color_ANGLE(self.color_04[1], self.color_04[2], self.color_04[3])
            self.Color_APPLY("RGB", self.color_04[1], self.color_04[2], self.color_04[3], 0)
            self.Pigment_Display_Release(0)
    def Color_04_SAVE(self, SIGNAL_CLICKS):
        self.color_04 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_04[1]*255, self.color_04[2]*255, self.color_04[3]*255))
        self.layout.cor_04.setStyleSheet(color)
    def Color_04_CLEAN(self, SIGNAL_CLICKS):
        self.color_04 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_04.setStyleSheet(bg_alpha)

    def Color_05_APPLY(self, SIGNAL_CLICKS):
        if self.color_05[0] == "True":
            self.Color_ANGLE(self.color_05[1], self.color_05[2], self.color_05[3])
            self.Color_APPLY("RGB", self.color_05[1], self.color_05[2], self.color_05[3], 0)
            self.Pigment_Display_Release(0)
    def Color_05_SAVE(self, SIGNAL_CLICKS):
        self.color_05 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_05[1]*255, self.color_05[2]*255, self.color_05[3]*255))
        self.layout.cor_05.setStyleSheet(color)
    def Color_05_CLEAN(self, SIGNAL_CLICKS):
        self.color_05 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_05.setStyleSheet(bg_alpha)

    def Color_06_APPLY(self, SIGNAL_CLICKS):
        if self.color_06[0] == "True":
            self.Color_ANGLE(self.color_06[1], self.color_06[2], self.color_06[3])
            self.Color_APPLY("RGB", self.color_06[1], self.color_06[2], self.color_06[3], 0)
            self.Pigment_Display_Release(0)
    def Color_06_SAVE(self, SIGNAL_CLICKS):
        self.color_06 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_06[1]*255, self.color_06[2]*255, self.color_06[3]*255))
        self.layout.cor_06.setStyleSheet(color)
    def Color_06_CLEAN(self, SIGNAL_CLICKS):
        self.color_06 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_06.setStyleSheet(bg_alpha)

    def Color_07_APPLY(self, SIGNAL_CLICKS):
        if self.color_07[0] == "True":
            self.Color_ANGLE(self.color_07[1], self.color_07[2], self.color_07[3])
            self.Color_APPLY("RGB", self.color_07[1], self.color_07[2], self.color_07[3], 0)
            self.Pigment_Display_Release(0)
    def Color_07_SAVE(self, SIGNAL_CLICKS):
        self.color_07 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_07[1]*255, self.color_07[2]*255, self.color_07[3]*255))
        self.layout.cor_07.setStyleSheet(color)
    def Color_07_CLEAN(self, SIGNAL_CLICKS):
        self.color_07 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_07.setStyleSheet(bg_alpha)

    def Color_08_APPLY(self, SIGNAL_CLICKS):
        if self.color_08[0] == "True":
            self.Color_ANGLE(self.color_08[1], self.color_08[2], self.color_08[3])
            self.Color_APPLY("RGB", self.color_08[1], self.color_08[2], self.color_08[3], 0)
            self.Pigment_Display_Release(0)
    def Color_08_SAVE(self, SIGNAL_CLICKS):
        self.color_08 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_08[1]*255, self.color_08[2]*255, self.color_08[3]*255))
        self.layout.cor_08.setStyleSheet(color)
    def Color_08_CLEAN(self, SIGNAL_CLICKS):
        self.color_08 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_08.setStyleSheet(bg_alpha)

    def Color_09_APPLY(self, SIGNAL_CLICKS):
        if self.color_09[0] == "True":
            self.Color_ANGLE(self.color_09[1], self.color_09[2], self.color_09[3])
            self.Color_APPLY("RGB", self.color_09[1], self.color_09[2], self.color_09[3], 0)
            self.Pigment_Display_Release(0)
    def Color_09_SAVE(self, SIGNAL_CLICKS):
        self.color_09 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_09[1]*255, self.color_09[2]*255, self.color_09[3]*255))
        self.layout.cor_09.setStyleSheet(color)
    def Color_09_CLEAN(self, SIGNAL_CLICKS):
        self.color_09 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_09.setStyleSheet(bg_alpha)

    def Color_10_APPLY(self, SIGNAL_CLICKS):
        if self.color_10[0] == "True":
            self.Color_ANGLE(self.color_10[1], self.color_10[2], self.color_10[3])
            self.Color_APPLY("RGB", self.color_10[1], self.color_10[2], self.color_10[3], 0)
            self.Pigment_Display_Release(0)
    def Color_10_SAVE(self, SIGNAL_CLICKS):
        self.color_10 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_10[1]*255, self.color_10[2]*255, self.color_10[3]*255))
        self.layout.cor_10.setStyleSheet(color)
    def Color_10_CLEAN(self, SIGNAL_CLICKS):
        self.color_10 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        self.layout.cor_10.setStyleSheet(bg_alpha)

    #//
    #\\ Mixer COLOR ############################################################
    def Mixer_TTS_APPLY(self, SIGNAL_APPLY):
        if self.color_tts[0] == "True":
            self.Color_APPLY("RGB", self.color_tts[1], self.color_tts[2], self.color_tts[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_TTS_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_tts = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ; " % (self.color_tts[1]*255, self.color_tts[2]*255, self.color_tts[3]*255))
        self.layout.tts_l1.setStyleSheet(color)
        self.layout.white.setStyleSheet(bg_white)
        self.layout.grey.setStyleSheet(bg_grey)
        self.layout.black.setStyleSheet(bg_black)
        self.Mixer_Display()
    def Mixer_TTS_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_tts = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
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

    def Mixer_RGB_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l1[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_L1_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l1[1]*255, self.color_rgb_l1[2]*255, self.color_rgb_l1[3]*255))
        self.layout.rgb_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l1 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.rgb_l1.setStyleSheet(bg_alpha)
        self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.layout.rgb_g1.width())

    def Mixer_RGB_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r1[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_r1[1], self.color_rgb_r1[2], self.color_rgb_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_R1_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r1[1]*255, self.color_rgb_r1[2]*255, self.color_rgb_r1[3]*255))
        self.layout.rgb_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r1 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.layout.rgb_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.layout.rgb_g1.width())

    def Mixer_RGB_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l2[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_L2_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l2[1]*255, self.color_rgb_l2[2]*255, self.color_rgb_l2[3]*255))
        self.layout.rgb_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l2 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.rgb_l2.setStyleSheet(bg_alpha)
        self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.layout.rgb_g2.width())

    def Mixer_RGB_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r2[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_r2[1], self.color_rgb_r2[2], self.color_rgb_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_R2_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r2[1]*255, self.color_rgb_r2[2]*255, self.color_rgb_r2[3]*255))
        self.layout.rgb_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r2 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.layout.rgb_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.layout.rgb_g2.width())

    def Mixer_RGB_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_l3[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_L3_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_l3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_l3[1]*255, self.color_rgb_l3[2]*255, self.color_rgb_l3[3]*255))
        self.layout.rgb_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_l3 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.rgb_l3.setStyleSheet(bg_alpha)
        self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_RGB_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_rgb_r3[0] == "True":
            self.Color_APPLY("RGB", self.color_rgb_r3[1], self.color_rgb_r3[2], self.color_rgb_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_RGB_R3_SAVE(self, SIGNAL_SAVE):
        # Color Math
        self.color_rgb_r3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        self.Settings_Load_Misc()
        # Display
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_rgb_r3[1]*255, self.color_rgb_r3[2]*255, self.color_rgb_r3[3]*255))
        self.layout.rgb_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_RGB_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_rgb_r3 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.layout.rgb_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_ARD_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l1[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l1 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l1[1], self.color_ard_l1[2], self.color_ard_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.ard_l1.setStyleSheet(bg_alpha)
        self.layout.ard_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g1 = 0
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.layout.ard_g1.width())

    def Mixer_ARD_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r1[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r1 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r1[1], self.color_ard_r1[2], self.color_ard_r1[3])

        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r1 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.layout.ard_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g1 = 0
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.layout.ard_g1.width())

    def Mixer_ARD_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l2[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l2 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l2[1], self.color_ard_l2[2], self.color_ard_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.ard_l2.setStyleSheet(bg_alpha)
        self.layout.ard_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g2 = 0
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.layout.ard_g2.width())

    def Mixer_ARD_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r2[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r2 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r2[1], self.color_ard_r2[2], self.color_ard_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r2 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.layout.ard_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g2 = 0
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.layout.ard_g2.width())

    def Mixer_ARD_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_l3[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_l3 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_l3[1], self.color_ard_l3[2], self.color_ard_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_l3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.ard_l3.setStyleSheet(bg_alpha)
        self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g3 = 0
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.layout.ard_g3.width())

    def Mixer_ARD_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_ard_r3[0] == "True":
            self.Color_APPLY("ARD", self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_ARD_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_ard_r3 = ["True", self.ard_1, self.ard_2, self.ard_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.ard_to_rgb(self.color_ard_r3[1], self.color_ard_r3[2], self.color_ard_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.ard_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_ARD_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_ard_r3 = ["False", 0, 0, 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.layout.ard_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_ard_g3 = 0
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.layout.ard_g3.width())

    def Mixer_HSV_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l1[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_L1_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_l1 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l1[1], self.color_hsv_l1[2], self.color_hsv_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l1 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsv_l1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r1[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_R1_SAVE(self, SIGNAL_SAVE):
        # color = [Bool, R, G, B, H, S, V]
        self.color_hsv_r1 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r1[1], self.color_hsv_r1[2], self.color_hsv_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r1 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.layout.hsv_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l2[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_l2 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l2[1], self.color_hsv_l2[2], self.color_hsv_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l2 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsv_l2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r2[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_r2 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r2[1], self.color_hsv_r2[2], self.color_hsv_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r2 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.layout.hsv_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_l3[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_l3 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_l3[1], self.color_hsv_l3[2], self.color_hsv_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_l3 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsv_l3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSV_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsv_r3[0] == "True":
            self.Color_APPLY("HSV", self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSV_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsv_r3 = ["True", self.hsv_1, self.hsv_2, self.hsv_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsv_to_rgb(self.color_hsv_r3[1], self.color_hsv_r3[2], self.color_hsv_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsv_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSV_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsv_r3 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.layout.hsv_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSL_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l1[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l1 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l1[1], self.color_hsl_l1[2], self.color_hsl_l1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l1 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsl_l1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.layout.hsl_g1.width())

    def Mixer_HSL_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r1[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r1 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r1[1], self.color_hsl_r1[2], self.color_hsl_r1[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r1 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.layout.hsl_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.layout.hsl_g1.width())

    def Mixer_HSL_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l2[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l2 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l2[1], self.color_hsl_l2[2], self.color_hsl_l2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l2 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsl_l2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.layout.hsl_g2.width())

    def Mixer_HSL_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r2[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r2 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r2[1], self.color_hsl_r2[2], self.color_hsl_r2[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r2 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.layout.hsl_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.layout.hsl_g2.width())

    def Mixer_HSL_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_l3[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_l3 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_l3[1], self.color_hsl_l3[2], self.color_hsl_l3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_l3 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsl_l3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_HSL_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_hsl_r3[0] == "True":
            self.Color_APPLY("HSL", self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3], 0)
            self.Pigment_Display_Release(0)
    def Mixer_HSL_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_hsl_r3 = ["True", self.hsl_1, self.hsl_2, self.hsl_3]
        self.Settings_Load_Misc()
        # Display
        rgb = self.hsl_to_rgb(self.color_hsl_r3[1], self.color_hsl_r3[2], self.color_hsl_r3[3])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.hsl_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_HSL_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_hsl_r3 = ["False", 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.layout.hsl_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.layout.hsl_g3.width())

    def Mixer_CMYK_L1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l1[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4], 0)
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_L1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l1 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Load_Misc()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l1[1], self.color_cmyk_l1[2], self.color_cmyk_l1[3], self.color_cmyk_l1[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_l1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.cmyk_l1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.layout.cmyk_g1.width())

    def Mixer_CMYK_R1_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r1[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4], 0)
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_R1_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r1 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Load_Misc()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r1[1], self.color_cmyk_r1[2], self.color_cmyk_r1[3], self.color_cmyk_r1[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_r1.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R1_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.layout.cmyk_g1.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.layout.cmyk_g1.width())

    def Mixer_CMYK_L2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l2[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4], 0)
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_L2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l2 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Load_Misc()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l2[1], self.color_cmyk_l2[2], self.color_cmyk_l2[3], self.color_cmyk_l2[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_l2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.cmyk_l2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.layout.cmyk_g2.width())

    def Mixer_CMYK_R2_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r2[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4], 0)
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_R2_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r2 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Load_Misc()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r2[1], self.color_cmyk_r2[2], self.color_cmyk_r2[3], self.color_cmyk_r2[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_r2.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R2_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.layout.cmyk_g2.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.layout.cmyk_g2.width())

    def Mixer_CMYK_L3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_l3[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4], 0)
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_L3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_l3 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Load_Misc()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_l3[1], self.color_cmyk_l3[2], self.color_cmyk_l3[3], self.color_cmyk_l3[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_l3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_L3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.cmyk_l3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.layout.cmyk_g3.width())

    def Mixer_CMYK_R3_APPLY(self, SIGNAL_APPLY):
        if self.color_cmyk_r3[0] == "True":
            self.Color_APPLY("CMYK", self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4], 0)
            self.Pigment_Display_Release(0)
    def Mixer_CMYK_R3_SAVE(self, SIGNAL_SAVE):
        # color
        self.color_cmyk_r3 = ["True", self.cmyk_1, self.cmyk_2, self.cmyk_3, self.cmyk_4]
        self.Settings_Load_Misc()
        # Display
        rgb = self.cmyk_to_rgb(self.color_cmyk_r3[1], self.color_cmyk_r3[2], self.color_cmyk_r3[3], self.color_cmyk_r3[4])
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (rgb[0]*255, rgb[1]*255, rgb[2]*255))
        self.layout.cmyk_r3.setStyleSheet(color)
        self.Mixer_Display()
    def Mixer_CMYK_R3_CLEAN(self, SIGNAL_CLEAN):
        # Color Math
        self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
        self.Settings_Load_Misc()
        # Display
        self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.layout.cmyk_g3.setStyleSheet(bg_alpha)
        # Correct Values
        self.spacer_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.layout.cmyk_g3.width())

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
        rgb1 = ((self.color_tts[1]) + (self.spacer_tone * (color_grey[0] - self.color_tts[1])))
        rgb2 = ((self.color_tts[2]) + (self.spacer_tone * (color_grey[1] - self.color_tts[2])))
        rgb3 = ((self.color_tts[3]) + (self.spacer_tone * (color_grey[2] - self.color_tts[3])))
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
        self.spacer_rgb_g1 = SIGNAL_MIXER_VALUE / (self.layout.rgb_g1.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l1[1] + (self.spacer_rgb_g1 * (self.color_rgb_r1[1] - self.color_rgb_l1[1])))
        rgb2 = (self.color_rgb_l1[2] + (self.spacer_rgb_g1 * (self.color_rgb_r1[2] - self.color_rgb_l1[2])))
        rgb3 = (self.color_rgb_l1[3] + (self.spacer_rgb_g1 * (self.color_rgb_r1[3] - self.color_rgb_l1[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
    def Mixer_RGB_G2(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_rgb_g2 = SIGNAL_MIXER_VALUE / (self.layout.rgb_g2.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l2[1] + (self.spacer_rgb_g2 * (self.color_rgb_r2[1] - self.color_rgb_l2[1])))
        rgb2 = (self.color_rgb_l2[2] + (self.spacer_rgb_g2 * (self.color_rgb_r2[2] - self.color_rgb_l2[2])))
        rgb3 = (self.color_rgb_l2[3] + (self.spacer_rgb_g2 * (self.color_rgb_r2[3] - self.color_rgb_l2[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)
    def Mixer_RGB_G3(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_rgb_g3 = SIGNAL_MIXER_VALUE / (self.layout.rgb_g3.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l3[1] + (self.spacer_rgb_g3 * (self.color_rgb_r3[1] - self.color_rgb_l3[1])))
        rgb2 = (self.color_rgb_l3[2] + (self.spacer_rgb_g3 * (self.color_rgb_r3[2] - self.color_rgb_l3[2])))
        rgb3 = (self.color_rgb_l3[3] + (self.spacer_rgb_g3 * (self.color_rgb_r3[3] - self.color_rgb_l3[3])))
        # Send Values
        self.Color_ANGLE(rgb1, rgb2, rgb3)
        self.Color_APPLY("RGB", rgb1, rgb2, rgb3, 0)

    def Mixer_ARD_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_ard_g1 = SIGNAL_MIXER_VALUE / (self.layout.ard_g1.width())
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
        self.spacer_ard_g2 = SIGNAL_MIXER_VALUE / (self.layout.ard_g2.width())
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
        self.spacer_ard_g3 = SIGNAL_MIXER_VALUE / (self.layout.ard_g3.width())
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
        self.spacer_hsv_g1 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g1.width())
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
        self.spacer_hsv_g2 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g2.width())
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
        self.spacer_hsv_g3 = SIGNAL_MIXER_VALUE / (self.layout.hsv_g3.width())
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
        self.spacer_hsl_g1 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g1.width())
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
        self.spacer_hsl_g2 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g2.width())
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
        self.spacer_hsl_g3 = SIGNAL_MIXER_VALUE / (self.layout.hsl_g3.width())
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

    def Mixer_CMYK_G1(self, SIGNAL_MIXER_VALUE):
        # Percentage Value
        self.spacer_cmyk_g1 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g1.width())
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
        self.spacer_cmyk_g2 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g2.width())
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
        self.spacer_cmyk_g3 = SIGNAL_MIXER_VALUE / (self.layout.cmyk_g3.width())
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
        har_active = self.layout.har.isChecked()
        if har_active == True:
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
    def Harmony_2_Active(self, SIGNAL_ACTIVE):
        har_active = self.layout.har.isChecked()
        if har_active == True:
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
    def Harmony_3_Active(self, SIGNAL_ACTIVE):
        har_active = self.layout.har.isChecked()
        if har_active == True:
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
    def Harmony_4_Active(self, SIGNAL_ACTIVE):
        har_active = self.layout.har.isChecked()
        if har_active == True:
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
    def Harmony_5_Active(self, SIGNAL_ACTIVE):
        har_active = self.layout.har.isChecked()
        if har_active == True:
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

    #//
    #\\ Dot ####################################################################
    def DOT_1_APPLY(self, SIGNAL_CLICKS):
        if self.dot_1[0] == "True":
            self.Color_ANGLE(self.dot_1[1], self.dot_1[2], self.dot_1[3])
            self.Color_APPLY("RGB", self.dot_1[1], self.dot_1[2], self.dot_1[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_1_SAVE(self, SIGNAL_CLICKS):
        self.dot_1 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
        self.layout.dot_1.setStyleSheet(color)
    def DOT_1_CLEAN(self, SIGNAL_CLICKS):
        self.dot_1 = ["False", 0, 0, 0]
        self.layout.dot_1.setStyleSheet(bg_alpha)

    def DOT_2_APPLY(self, SIGNAL_CLICKS):
        if self.dot_2[0] == "True":
            self.Color_ANGLE(self.dot_2[1], self.dot_2[2], self.dot_2[3])
            self.Color_APPLY("RGB", self.dot_2[1], self.dot_2[2], self.dot_2[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_2_SAVE(self, SIGNAL_CLICKS):
        self.dot_2 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
        self.layout.dot_2.setStyleSheet(color)
    def DOT_2_CLEAN(self, SIGNAL_CLICKS):
        self.dot_2 = ["False", 0, 0, 0]
        self.layout.dot_2.setStyleSheet(bg_alpha)

    def DOT_3_APPLY(self, SIGNAL_CLICKS):
        if self.dot_3[0] == "True":
            self.Color_ANGLE(self.dot_3[1], self.dot_3[2], self.dot_3[3])
            self.Color_APPLY("RGB", self.dot_3[1], self.dot_3[2], self.dot_3[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_3_SAVE(self, SIGNAL_CLICKS):
        self.dot_3 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
        self.layout.dot_3.setStyleSheet(color)
    def DOT_3_CLEAN(self, SIGNAL_CLICKS):
        self.dot_3 = ["False", 0, 0, 0]
        self.layout.dot_3.setStyleSheet(bg_alpha)

    def DOT_4_APPLY(self, SIGNAL_CLICKS):
        if self.dot_4[0] == "True":
            self.Color_ANGLE(self.dot_4[1], self.dot_4[2], self.dot_4[3])
            self.Color_APPLY("RGB", self.dot_4[1], self.dot_4[2], self.dot_4[3], 0)
            self.Pigment_Display_Release(0)
    def DOT_4_SAVE(self, SIGNAL_CLICKS):
        self.dot_4 = ["True", self.rgb_1, self.rgb_2, self.rgb_3]
        color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
        self.layout.dot_4.setStyleSheet(color)
    def DOT_4_CLEAN(self, SIGNAL_CLICKS):
        self.dot_4 = ["False", 0, 0, 0]
        self.layout.dot_4.setStyleSheet(bg_alpha)

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
            self.uvd_1 = round(SIGNAL_UVD_VALUE[1]*kritaUVD, 2) / kritaUVD
            self.uvd_2 = round(SIGNAL_UVD_VALUE[2]*kritaUVD, 2) / kritaUVD
        if SIGNAL_UVD_VALUE[0] == "D":
            factor = 100
            self.uvd_3 = self.uvd_3 + (SIGNAL_UVD_VALUE[3]/factor)
            # Limit the Add operation
            if self.uvd_3 <= 0:
                self.uvd_3 = 0
            elif self.uvd_3 >= 1:
                self.uvd_3 = 1
        hue = self.uvd_to_ard(self.uvd_1, self.uvd_2, self.uvd_3)
        self.angle_live = hue[0]
        self.Color_APPLY("UVD", self.uvd_1, self.uvd_2, self.uvd_3, 0)
        self.layout.label_percent.setText("")
    def Signal_ARD(self, SIGNAL_ARD_VALUE):
        if SIGNAL_ARD_VALUE[0] == "A":
            factor = 100
            self.ard_1 = self.ard_1 + (SIGNAL_ARD_VALUE[1]/factor)
            # Cycle the Add operation
            if self.ard_1 <= 0:
                self.ard_1 = 1
            elif self.ard_1 >= 1:
                self.ard_1 = 0
            self.angle_live = self.ard_1
        if SIGNAL_ARD_VALUE[0] == "RD":
            self.ard_2 = round(SIGNAL_ARD_VALUE[2]*kritaRDL, 2) / kritaRDL
            self.ard_3 = round(SIGNAL_ARD_VALUE[3]*kritaRDL, 2) / kritaRDL
        self.Color_APPLY("ARD", self.ard_1, self.ard_2, self.ard_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HSV_4(self, SIGNAL_HSV_4_VALUE):
        if SIGNAL_HSV_4_VALUE[0] == "H":
            factor = 100
            self.hsv_1 = self.hsv_1 + (SIGNAL_HSV_4_VALUE[1]/factor)
            if self.hsv_1 <= 0:
                self.hsv_1 = 1
            elif self.hsv_1 >= 1:
                self.hsv_1 = 0
            self.angle_live = self.hsv_1
            self.Color_APPLY("HSV", self.hsv_1, self.hsv_2, self.hsv_3, 0)
        if SIGNAL_HSV_4_VALUE[0] == "SL":
            self.hsv_2 = round(SIGNAL_HSV_4_VALUE[2]*kritaSVLCY, 2) / kritaSVLCY
            self.hsv_3 = round(SIGNAL_HSV_4_VALUE[3]*kritaSVLCY, 2) / kritaSVLCY
            self.angle_live = self.hsv_1
            self.Color_APPLY("HSV", self.angle_live, self.hsv_2, self.hsv_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HSL_3(self, SIGNAL_HSL_3_VALUE):
        if SIGNAL_HSL_3_VALUE[0] == "H":
            factor = 100
            self.hsl_1 = self.hsl_1 + (SIGNAL_HSL_3_VALUE[1]/factor)
            if self.hsl_1 <= 0:
                self.hsl_1 = 1
            elif self.hsl_1 >= 1:
                self.hsl_1 = 0
            self.angle_live = self.hsl_1
            self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        if SIGNAL_HSL_3_VALUE[0] == "SL":
            self.hsl_2 = round(SIGNAL_HSL_3_VALUE[2]*kritaSVLCY, 2) / kritaSVLCY
            self.hsl_3 = round(SIGNAL_HSL_3_VALUE[3]*kritaSVLCY, 2) / kritaSVLCY
            self.Color_APPLY("HSL", self.angle_live, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HSL_4(self, SIGNAL_HSL_4_VALUE):
        if SIGNAL_HSL_4_VALUE[0] == "H":
            factor = 100
            self.hsl_1 = self.hsl_1 + (SIGNAL_HSL_4_VALUE[1]/factor)
            if self.hsl_1 <= 0:
                self.hsl_1 = 1
            elif self.hsl_1 >= 1:
                self.hsl_1 = 0
            self.angle_live = self.hsl_1
            self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        if SIGNAL_HSL_4_VALUE[0] == "SL":
            self.hsl_2 = round(SIGNAL_HSL_4_VALUE[2]*kritaSVLCY, 2) / kritaSVLCY
            self.hsl_3 = round(SIGNAL_HSL_4_VALUE[3]*kritaSVLCY, 2) / kritaSVLCY
            self.Color_APPLY("HSL", self.angle_live, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HSL_4D(self, SIGNAL_HSL_4D_VALUE):
        if SIGNAL_HSL_4D_VALUE[0] == "H":
            factor = 100
            self.hsl_1 = self.hsl_1 + (SIGNAL_HSL_4D_VALUE[1]/factor)
            # Cycle the Add operation
            if self.hsl_1 <= 0:
                self.hsl_1 = 1
            elif self.hsl_1 >= 1:
                self.hsl_1 = 0
            self.angle_live = self.hsl_1
        if SIGNAL_HSL_4D_VALUE[0] == "SL":
            self.hsl_2 = round(SIGNAL_HSL_4D_VALUE[2]*kritaSVLCY, 2) / kritaSVLCY
            self.hsl_3 = round(SIGNAL_HSL_4D_VALUE[3]*kritaSVLCY, 2) / kritaSVLCY
        self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
        self.layout.label_percent.setText("")
    def Signal_HUE_Circle(self, SIGNAL_HUE_C_VALUE):
        self.hsl_1 = SIGNAL_HUE_C_VALUE[0]
        self.angle_live = self.hsl_1
        self.Color_APPLY("HSL", self.hsl_1, self.hsl_2, self.hsl_3, 0)
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
        width = self.layout.panel_obj_mix.width()
        height = self.layout.panel_obj_mix.height()
        pixmap = self.layout.panel_obj_mix.grab(QRect(QPoint(0, 0), QPoint(width, height)))
        image = pixmap.toImage()
        scaled = image.scaled(QSize(width, height))
        color = scaled.pixelColor(SIGNAL_OBJ_PRESS[0], SIGNAL_OBJ_PRESS[1])
        # Apply Color Values
        self.rgb_1 = color.red()/255
        self.rgb_2 = color.green()/255
        self.rgb_3 = color.blue()/255
        # Apply Colors
        hue = self.rgb_to_hsv(self.rgb_1, self.rgb_2, self.rgb_3)
        self.angle_live = hue[0]
        self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
        self.layout.label_percent.setText("")
    def Signal_OBJ_Location(self, SIGNAL_OBJ_LOCATION):
        self.obj_location_x = SIGNAL_OBJ_LOCATION[0]
        self.obj_location_y = SIGNAL_OBJ_LOCATION[1]
    def Pigment_Panel_Zoom(self, SIGNAL_ZOOM):
        self.zoom = SIGNAL_ZOOM

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
        self.Color_ANGLE(self.bg_1[1], self.bg_1[2], self.bg_1[3])
        self.Color_APPLY("RGB", self.bg_1[1], self.bg_1[2], self.bg_1[3], 0)
    def BG_1_LIVE(self):
        if self.layout.b1_live.isChecked() == True:
            self.BG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b1a, "SAVE")
            self.Pigment_Display_Release(0)
    def BG_1_APPLY(self):
        if self.bg_1[0] == "True":
            self.Color_ANGLE(self.bg_1[1], self.bg_1[2], self.bg_1[3])
            self.Color_APPLY("RGB", self.bg_1[1], self.bg_1[2], self.bg_1[3], 0)
            self.Pigment_Display_Release(0)
    def BG_1_SAVE(self, val_1, val_2, val_3, val_4, save):
        # Variable
        self.bg_1 = ["True", val_1, val_2, val_3, val_4]
        # Update Color Isolated Representation
        color1 = str("background-color: rgba(%f, %f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        color2 = str("background-color: rgba(%f, %f, %f, %f);" % (self.bg_1[1]*255, self.bg_1[2]*255, self.bg_1[3]*255, self.bg_1[4]*255))
        self.layout.b1_color.setStyleSheet(color1)
        self.layout.layer_01.setStyleSheet(color2)
        # Save
        if save == "SAVE":
            self.Settings_Save_Misc()
    def BG_1_CLEAN(self):
        self.bg_1 = ["False", 0, 0, 0, 1]
        self.b1a = 1
        self.layout.b1_color.setStyleSheet(bg_alpha)
        self.layout.layer_01.setPixmap(self.Mask_Color(self.path_bg_1, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.bg_2[1], self.bg_2[2], self.bg_2[3])
        self.Color_APPLY("RGB", self.bg_2[1], self.bg_2[2], self.bg_2[3], 0)
    def BG_2_LIVE(self):
        if self.layout.b2_live.isChecked() == True:
            self.BG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b2a, "SAVE")
            self.Pigment_Display_Release(0)
    def BG_2_APPLY(self):
        if self.bg_2[0] == "True":
            self.Color_ANGLE(self.bg_2[1], self.bg_2[2], self.bg_2[3])
            self.Color_APPLY("RGB", self.bg_2[1], self.bg_2[2], self.bg_2[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def BG_2_CLEAN(self):
        self.bg_2 = ["False", 0, 0, 0, 1]
        self.b2a = 1
        self.layout.b2_color.setStyleSheet(bg_alpha)
        self.layout.layer_02.setPixmap(self.Mask_Color(self.path_bg_2, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.bg_3[1], self.bg_3[2], self.bg_3[3])
        self.Color_APPLY("RGB", self.bg_3[1], self.bg_3[2], self.bg_3[3], 0)
    def BG_3_LIVE(self):
        if self.layout.b3_live.isChecked() == True:
            self.BG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.b3a, "SAVE")
            self.Pigment_Display_Release(0)
    def BG_3_APPLY(self):
        if self.bg_3[0] == "True":
            self.Color_ANGLE(self.bg_3[1], self.bg_3[2], self.bg_3[3])
            self.Color_APPLY("RGB", self.bg_3[1], self.bg_3[2], self.bg_3[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def BG_3_CLEAN(self):
        self.bg_3 = ["False", 0, 0, 0, 1]
        self.b3a = 1
        self.layout.b3_color.setStyleSheet(bg_alpha)
        self.layout.layer_03.setPixmap(self.Mask_Color(self.path_bg_3, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.dif_1[1], self.dif_1[2], self.dif_1[3])
        self.Color_APPLY("RGB", self.dif_1[1], self.dif_1[2], self.dif_1[3], 0)
    def DIF_1_LIVE(self):
        if self.layout.d1_live.isChecked() == True:
            self.DIF_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d1a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_1_APPLY(self):
        if self.dif_1[0] == "True":
            self.Color_ANGLE(self.dif_1[1], self.dif_1[2], self.dif_1[3])
            self.Color_APPLY("RGB", self.dif_1[1], self.dif_1[2], self.dif_1[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def DIF_1_CLEAN(self):
        self.dif_1 = ["False", 0, 0, 0, 1]
        self.d1a = 1
        self.layout.d1_color.setStyleSheet(bg_alpha)
        self.layout.layer_04.setPixmap(self.Mask_Color(self.path_dif_1, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.dif_2[1], self.dif_2[2], self.dif_2[3])
        self.Color_APPLY("RGB", self.dif_2[1], self.dif_2[2], self.dif_2[3], 0)
    def DIF_2_LIVE(self):
        if self.layout.d2_live.isChecked() == True:
            self.DIF_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d2a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_2_APPLY(self):
        if self.dif_2[0] == "True":
            self.Color_ANGLE(self.dif_2[1], self.dif_2[2], self.dif_2[3])
            self.Color_APPLY("RGB", self.dif_2[1], self.dif_2[2], self.dif_2[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def DIF_2_CLEAN(self):
        self.dif_2 = ["False", 0, 0, 0, 1]
        self.d2a = 1
        self.layout.d2_color.setStyleSheet(bg_alpha)
        self.layout.layer_05.setPixmap(self.Mask_Color(self.path_dif_2, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.dif_3[1], self.dif_3[2], self.dif_3[3])
        self.Color_APPLY("RGB", self.dif_3[1], self.dif_3[2], self.dif_3[3], 0)
    def DIF_3_LIVE(self):
        if self.layout.d3_live.isChecked() == True:
            self.DIF_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d3a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_3_APPLY(self):
        if self.dif_3[0] == "True":
            self.Color_ANGLE(self.dif_3[1], self.dif_3[2], self.dif_3[3])
            self.Color_APPLY("RGB", self.dif_3[1], self.dif_3[2], self.dif_3[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def DIF_3_CLEAN(self):
        self.dif_3 = ["False", 0, 0, 0, 1]
        self.d3a = 1
        self.layout.d3_color.setStyleSheet(bg_alpha)
        self.layout.layer_06.setPixmap(self.Mask_Color(self.path_dif_3, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.dif_4[1], self.dif_4[2], self.dif_4[3])
        self.Color_APPLY("RGB", self.dif_4[1], self.dif_4[2], self.dif_4[3], 0)
    def DIF_4_LIVE(self):
        if self.layout.d4_live.isChecked() == True:
            self.DIF_4_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d4a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_4_APPLY(self):
        if self.dif_4[0] == "True":
            self.Color_ANGLE(self.dif_4[1], self.dif_4[2], self.dif_4[3])
            self.Color_APPLY("RGB", self.dif_4[1], self.dif_4[2], self.dif_4[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def DIF_4_CLEAN(self):
        self.dif_4 = ["False", 0, 0, 0, 1]
        self.d4a = 1
        self.layout.d4_color.setStyleSheet(bg_alpha)
        self.layout.layer_07.setPixmap(self.Mask_Color(self.path_dif_4, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.dif_5[1], self.dif_5[2], self.dif_5[3])
        self.Color_APPLY("RGB", self.dif_5[1], self.dif_5[2], self.dif_5[3], 0)
    def DIF_5_LIVE(self):
        if self.layout.d5_live.isChecked() == True:
            self.DIF_5_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d5a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_5_APPLY(self):
        if self.dif_5[0] == "True":
            self.Color_ANGLE(self.dif_5[1], self.dif_5[2], self.dif_5[3])
            self.Color_APPLY("RGB", self.dif_5[1], self.dif_5[2], self.dif_5[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def DIF_5_CLEAN(self):
        self.dif_5 = ["False", 0, 0, 0, 1]
        self.d5a = 1
        self.layout.d5_color.setStyleSheet(bg_alpha)
        self.layout.layer_08.setPixmap(self.Mask_Color(self.path_dif_5, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.dif_6[1], self.dif_6[2], self.dif_6[3])
        self.Color_APPLY("RGB", self.dif_6[1], self.dif_6[2], self.dif_6[3], 0)
    def DIF_6_LIVE(self):
        if self.layout.d6_live.isChecked() == True:
            self.DIF_6_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.d6a, "SAVE")
            self.Pigment_Display_Release(0)
    def DIF_6_APPLY(self):
        if self.dif_6[0] == "True":
            self.Color_ANGLE(self.dif_6[1], self.dif_6[2], self.dif_6[3])
            self.Color_APPLY("RGB", self.dif_6[1], self.dif_6[2], self.dif_6[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def DIF_6_CLEAN(self):
        self.dif_6 = ["False", 0, 0, 0, 1]
        self.d6a = 1
        self.layout.d6_color.setStyleSheet(bg_alpha)
        self.layout.layer_09.setPixmap(self.Mask_Color(self.path_dif_6, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.fg_1[1], self.fg_1[2], self.fg_1[3])
        self.Color_APPLY("RGB", self.fg_1[1], self.fg_1[2], self.fg_1[3], 0)
    def FG_1_LIVE(self):
        if self.layout.f1_live.isChecked() == True:
            self.FG_1_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f1a, "SAVE")
            self.Pigment_Display_Release(0)
    def FG_1_APPLY(self):
        if self.fg_1[0] == "True":
            self.Color_ANGLE(self.fg_1[1], self.fg_1[2], self.fg_1[3])
            self.Color_APPLY("RGB", self.fg_1[1], self.fg_1[2], self.fg_1[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def FG_1_CLEAN(self):
        self.fg_1 = ["False", 0, 0, 0, 1]
        self.f1a = 1
        self.layout.f1_color.setStyleSheet(bg_alpha)
        self.layout.layer_10.setPixmap(self.Mask_Color(self.path_fg_1, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.fg_2[1], self.fg_2[2], self.fg_2[3])
        self.Color_APPLY("RGB", self.fg_2[1], self.fg_2[2], self.fg_2[3], 0)
    def FG_2_LIVE(self):
        if self.layout.f2_live.isChecked() == True:
            self.FG_2_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f2a, "SAVE")
            self.Pigment_Display_Release(0)
    def FG_2_APPLY(self):
        if self.fg_2[0] == "True":
            self.Color_ANGLE(self.fg_2[1], self.fg_2[2], self.fg_2[3])
            self.Color_APPLY("RGB", self.fg_2[1], self.fg_2[2], self.fg_2[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def FG_2_CLEAN(self):
        self.fg_2 = ["False", 0, 0, 0, 1]
        self.f2a = 1
        self.layout.f2_color.setStyleSheet(bg_alpha)
        self.layout.layer_11.setPixmap(self.Mask_Color(self.path_fg_2, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        self.Color_ANGLE(self.fg_3[1], self.fg_3[2], self.fg_3[3])
        self.Color_APPLY("RGB", self.fg_3[1], self.fg_3[2], self.fg_3[3], 0)
    def FG_3_LIVE(self):
        if self.layout.f3_live.isChecked() == True:
            self.FG_3_SAVE(self.rgb_1, self.rgb_2, self.rgb_3, self.f3a, "SAVE")
            self.Pigment_Display_Release(0)
    def FG_3_APPLY(self):
        if self.fg_3[0] == "True":
            self.Color_ANGLE(self.fg_3[1], self.fg_3[2], self.fg_3[3])
            self.Color_APPLY("RGB", self.fg_3[1], self.fg_3[2], self.fg_3[3], 0)
            self.Pigment_Display_Release(0)
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
            self.Settings_Save_Misc()
    def FG_3_CLEAN(self):
        self.fg_3 = ["False", 0, 0, 0, 1]
        self.f3a = 1
        self.layout.f3_color.setStyleSheet(bg_alpha)
        self.layout.layer_12.setPixmap(self.Mask_Color(self.path_fg_3, 0, 0, 0, 1))
        self.Settings_Save_Misc()
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
        if self.obj_active == True:
            # Object Label Geometry
            self.Object_Geometry()
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
    def Object_Geometry(self):
        self.layout.layer_01.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_02.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_03.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_04.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_05.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_06.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_07.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_08.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_09.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_10.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_11.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_12.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
        self.layout.layer_cursor.setGeometry(0,0,self.layout.panel_obj_mix.width(),self.layout.panel_obj_mix.height())
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
        painter = QPainter(self)
        painter.begin(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.drawImage(0,0,pixmap_color.toImage())
        painter.end()
        return pixmap

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
        # Check Krita Once before edit
        self.Krita_2_Pigment()
        # Confirm Panel
        self.Ratio()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.stop()
    def leaveEvent(self, event):
        # Start Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.start()
        # Save Settings
        self.Settings_Save_Misc()
        self.Settings_Save_ActiveColor()
        self.Settings_Save_UI()
    def paintEvent(self, event):
        # Update Frames on Widget Recalling
        self.Box_Ratio()
        # Updates Painter on Widget Recalling
        self.UVD_Update()
        self.ARD_Update()
        self.Update_Panel_HSV()
        self.Update_Panel_HSL()
        self.Update_Panel_HUE()
        # Update Object Geometry on Widget Recalling
        self.Object_Geometry()
        # Return Paint event to Regain Docker Title
        return super().paintEvent(event)
    def resizeEvent(self, event):
        # Maintian Ratio
        self.Ratio()
    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:
            self.timer.stop()
        # Save Settings
        self.Settings_Save_Misc()
        self.Settings_Save_ActiveColor()
        self.Settings_Save_UI()

    #//
    #\\ Settings ###############################################################
    def Settings_Load_UI(self):
        try:
            ui_string = Krita.instance().readSetting("Pigment.O", "UI", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            ui_split = ui_string.split(",")
            self.layout.har_index.setCurrentIndex(eval(ui_split[0]))
            self.layout.har_edit.setChecked(eval(ui_split[1]))
            self.layout.pan_index.setCurrentIndex(eval(ui_split[2]))
            self.layout.pan_secondary.setCurrentIndex(eval(ui_split[3]))
            self.layout.obj_index.setCurrentIndex(eval(ui_split[4]))
            self.layout.obj_set.setChecked(eval(ui_split[5]))
            self.layout.values.setChecked(eval(ui_split[6]))
            self.layout.mix_index.setCurrentIndex(eval(ui_split[7]))
            self.layout.gray.setChecked(eval(ui_split[8]))

            self.layout.sof.setChecked(eval(ui_split[9]))
            self.layout.aaa.setChecked(eval(ui_split[10]))
            self.layout.rgb.setChecked(eval(ui_split[11]))
            self.layout.ard.setChecked(eval(ui_split[12]))
            self.layout.hsv.setChecked(eval(ui_split[13]))
            self.layout.hsl.setChecked(eval(ui_split[14]))
            self.layout.hcy.setChecked(eval(ui_split[15]))
            self.layout.cmy.setChecked(eval(ui_split[16]))
            self.layout.cmyk.setChecked(eval(ui_split[17]))
            self.layout.kkk.setChecked(eval(ui_split[18]))

            self.layout.har.setChecked(False)
            self.layout.cotd.setChecked(eval(ui_split[20]))
            self.layout.pan.setChecked(eval(ui_split[21]))
            self.layout.dot.setChecked(eval(ui_split[22]))
            self.layout.obj.setChecked(eval(ui_split[23]))
            self.layout.tip.setChecked(eval(ui_split[24]))
            self.layout.tts.setChecked(eval(ui_split[25]))
            self.layout.mix.setChecked(eval(ui_split[26]))
        except:
            self.layout.har_index.setCurrentIndex(2)
            self.layout.har_edit.setChecked(False)
            self.layout.pan_index.setCurrentIndex(3)
            self.layout.pan_secondary.setCurrentIndex(1)
            self.layout.obj_index.setCurrentIndex(0)
            self.layout.obj_set.setChecked(False)
            self.layout.values.setChecked(False)
            self.layout.mix_index.setCurrentIndex(0)
            self.layout.gray.setChecked(False)

            self.layout.sof.setChecked(False)
            self.layout.aaa.setChecked(False)
            self.layout.rgb.setChecked(False)
            self.layout.ard.setChecked(False)
            self.layout.hsv.setChecked(True)
            self.layout.hsl.setChecked(False)
            self.layout.hcy.setChecked(False)
            self.layout.cmy.setChecked(False)
            self.layout.cmyk.setChecked(False)
            self.layout.kkk.setChecked(False)

            self.layout.har.setChecked(False)
            self.layout.cotd.setChecked(False)
            self.layout.pan.setChecked(True)
            self.layout.dot.setChecked(False)
            self.layout.obj.setChecked(False)
            self.layout.tip.setChecked(False)
            self.layout.tts.setChecked(False)
            self.layout.mix.setChecked(False)
    def Settings_Save_UI(self):
        ui_list = (
            str(self.layout.har_index.currentIndex()),
            str(self.layout.har_edit.isChecked()),
            str(self.layout.pan_index.currentIndex()),
            str(self.layout.pan_secondary.currentIndex()),
            str(self.layout.obj_index.currentIndex()),
            str(self.layout.obj_set.isChecked()),
            str(self.layout.values.isChecked()),
            str(self.layout.mix_index.currentIndex()),
            str(self.layout.gray.isChecked()),

            str(self.layout.sof.isChecked()),
            str(self.layout.aaa.isChecked()),
            str(self.layout.rgb.isChecked()),
            str(self.layout.ard.isChecked()),
            str(self.layout.hsv.isChecked()),
            str(self.layout.hsl.isChecked()),
            str(self.layout.hcy.isChecked()),
            str(self.layout.cmy.isChecked()),
            str(self.layout.cmyk.isChecked()),
            str(self.layout.kkk.isChecked()),

            str(self.layout.har.isChecked()),
            str(self.layout.cotd.isChecked()),
            str(self.layout.pan.isChecked()),
            str(self.layout.dot.isChecked()),
            str(self.layout.obj.isChecked()),
            str(self.layout.tip.isChecked()),
            str(self.layout.tts.isChecked()),
            str(self.layout.mix.isChecked())
            )
        ui_string = ','.join(ui_list)
        Krita.instance().writeSetting("Pigment.O", "UI", ui_string)

    def Settings_Load_ActiveColor(self):
        try:
            # Active Color
            active_color_string = Krita.instance().readSetting("Pigment.O", "active_color", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
            active_color_split = active_color_string.split(",")
            self.rgb_1 = float(active_color_split[0])
            self.rgb_2 = float(active_color_split[1])
            self.rgb_3 = float(active_color_split[2])
            self.angle_live = float(active_color_split[3])
            self.uvd_1 = float(active_color_split[4])
            self.uvd_2 = float(active_color_split[5])
            self.uvd_3 = float(active_color_split[6])
            self.d_previous = float(active_color_split[7])
            self.kkk_0 = float(active_color_split[8])
            self.kkk_1 = float(active_color_split[9])
            self.kkk_2 = float(active_color_split[10])
            self.kkk_3 = float(active_color_split[11])
            # Apply
            self.UVD_Hexagon_Points()
            self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
            self.Pigment_Display_Release(0)

        except:
            # Active Color
            self.rgb_1 = 0
            self.rgb_2 = 0
            self.rgb_3 = 0
            self.angle_live = 0
            self.uvd_1 = 0
            self.uvd_2 = 0
            self.uvd_3 = 0
            self.d_previous = 0
            self.kkk_0 = 6500
            self.kkk_1 = 255/255
            self.kkk_2 = 249/255
            self.kkk_3 = 253/255
            self.harmony_index = "Analogous"
            self.harmony_delta = 30
            self.harmony_edit = False
            # Apply
            self.UVD_Hexagon_Points()
            self.Color_ANGLE(self.rgb_1, self.rgb_2, self.rgb_3)
            self.Color_APPLY("RGB", self.rgb_1, self.rgb_2, self.rgb_3, 0)
            self.Pigment_Display_Release(0)
    def Settings_Save_ActiveColor(self):
        try:
            # Active Color
            active_color_list = (
                str(self.rgb_1),
                str(self.rgb_2),
                str(self.rgb_3),
                str(self.angle_live),
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
            pass

    def Settings_Load_Misc(self):
        #\\ Variables ##########################################################
        # Gray Display
        self.gray = False
        # Initial Status
        self.zoom = 0
        # Panel Null Start
        self.panel_active = "None"
        self.pan_sec = "None"
        # Panel Dot
        self.dot_location_x = 0
        self.dot_location_y = 0
        # Panel Object
        self.obj_active = False
        self.obj_location_x = 0
        self.obj_location_y = 0
        # Kalvin
        self.kkk_lock = False
        # Harmony
        self.harmony_delta = 30
        self.har_1 = ["HSL", 190/kritaRGB,63/kritaRGB,190/kritaRGB, 300/kritaHUE,127/kritaSVLCY,127/kritaSVLCY]
        self.har_2 = ["HSL", 190/kritaRGB,63/kritaRGB,127/kritaRGB, 330/kritaHUE,127/kritaSVLCY,127/kritaSVLCY]
        self.har_3 = ["HSL", 190/kritaRGB,63/kritaRGB,63/kritaRGB, 0/kritaHUE,127/kritaSVLCY,127/kritaSVLCY]
        self.har_4 = ["HSL", 190/kritaRGB,127/kritaRGB,63/kritaRGB, 30/kritaHUE,127/kritaSVLCY,127/kritaSVLCY]
        self.har_5 = ["HSL", 190/kritaRGB,190/kritaRGB,63/kritaRGB, 60/kritaHUE,127/kritaSVLCY,127/kritaSVLCY]
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
        #//
        #\\ Palette ############################################################
        color_00_string = Krita.instance().readSetting("Pigment.O", "tip_color_00", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_01_string = Krita.instance().readSetting("Pigment.O", "tip_color_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_02_string = Krita.instance().readSetting("Pigment.O", "tip_color_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_03_string = Krita.instance().readSetting("Pigment.O", "tip_color_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_04_string = Krita.instance().readSetting("Pigment.O", "tip_color_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_05_string = Krita.instance().readSetting("Pigment.O", "tip_color_05", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_06_string = Krita.instance().readSetting("Pigment.O", "tip_color_06", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_07_string = Krita.instance().readSetting("Pigment.O", "tip_color_07", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_08_string = Krita.instance().readSetting("Pigment.O", "tip_color_08", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_09_string = Krita.instance().readSetting("Pigment.O", "tip_color_09", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        color_10_string = Krita.instance().readSetting("Pigment.O", "tip_color_10", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_00[1]*255, self.color_00[2]*255, self.color_00[3]*255))
            self.layout.cor_00.setStyleSheet(color)
        else:
            self.color_00 = ["False", 0, 0, 0]
            self.layout.cor_00.setStyleSheet(bg_alpha)
        if color_01_split[0] == "True":
            self.color_01 = ["True", float(color_01_split[1]), float(color_01_split[2]), float(color_01_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_01[1]*255, self.color_01[2]*255, self.color_01[3]*255))
            self.layout.cor_01.setStyleSheet(color)
        else:
            self.color_01 = ["False", 0, 0, 0]
            self.layout.cor_01.setStyleSheet(bg_alpha)
        if color_02_split[0] == "True":
            self.color_02 = ["True", float(color_02_split[1]), float(color_02_split[2]), float(color_02_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_02[1]*255, self.color_02[2]*255, self.color_02[3]*255))
            self.layout.cor_02.setStyleSheet(color)
        else:
            self.color_02 = ["False", 0, 0, 0]
            self.layout.cor_02.setStyleSheet(bg_alpha)
        if color_03_split[0] == "True":
            self.color_03 = ["True", float(color_03_split[1]), float(color_03_split[2]), float(color_03_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_03[1]*255, self.color_03[2]*255, self.color_03[3]*255))
            self.layout.cor_03.setStyleSheet(color)
        else:
            self.color_03 = ["False", 0, 0, 0]
            self.layout.cor_03.setStyleSheet(bg_alpha)
        if color_04_split[0] == "True":
            self.color_04 = ["True", float(color_04_split[1]), float(color_04_split[2]), float(color_04_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_04[1]*255, self.color_04[2]*255, self.color_04[3]*255))
            self.layout.cor_04.setStyleSheet(color)
        else:
            self.color_04 = ["False", 0, 0, 0]
            self.layout.cor_04.setStyleSheet(bg_alpha)
        if color_05_split[0] == "True":
            self.color_05 = ["True", float(color_05_split[1]), float(color_05_split[2]), float(color_05_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_05[1]*255, self.color_05[2]*255, self.color_05[3]*255))
            self.layout.cor_05.setStyleSheet(color)
        else:
            self.color_05 = ["False", 0, 0, 0]
            self.layout.cor_05.setStyleSheet(bg_alpha)
        if color_06_split[0] == "True":
            self.color_06 = ["True", float(color_06_split[1]), float(color_06_split[2]), float(color_06_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_06[1]*255, self.color_06[2]*255, self.color_06[3]*255))
            self.layout.cor_06.setStyleSheet(color)
        else:
            self.color_06 = ["False", 0, 0, 0]
            self.layout.cor_06.setStyleSheet(bg_alpha)
        if color_07_split[0] == "True":
            self.color_07 = ["True", float(color_07_split[1]), float(color_07_split[2]), float(color_07_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_07[1]*255, self.color_07[2]*255, self.color_07[3]*255))
            self.layout.cor_07.setStyleSheet(color)
        else:
            self.color_07 = ["False", 0, 0, 0]
            self.layout.cor_07.setStyleSheet(bg_alpha)
        if color_08_split[0] == "True":
            self.color_08 = ["True", float(color_08_split[1]), float(color_08_split[2]), float(color_08_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_08[1]*255, self.color_08[2]*255, self.color_08[3]*255))
            self.layout.cor_08.setStyleSheet(color)
        else:
            self.color_08 = ["False", 0, 0, 0]
            self.layout.cor_08.setStyleSheet(bg_alpha)
        if color_09_split[0] == "True":
            self.color_09 = ["True", float(color_09_split[1]), float(color_09_split[2]), float(color_09_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_09[1]*255, self.color_09[2]*255, self.color_09[3]*255))
            self.layout.cor_09.setStyleSheet(color)
        else:
            self.color_09 = ["False", 0, 0, 0]
            self.layout.cor_09.setStyleSheet(bg_alpha)
        if color_10_split[0] == "True":
            self.color_10 = ["True", float(color_10_split[1]), float(color_10_split[2]), float(color_10_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_10[1]*255, self.color_10[2]*255, self.color_10[3]*255))
            self.layout.cor_10.setStyleSheet(color)
        else:
            self.color_10 = ["False", 0, 0, 0]
            self.layout.cor_10.setStyleSheet(bg_alpha)
        #//
        #\\ Mixer TTS ##########################################################
        mixer_tts_string = Krita.instance().readSetting("Pigment.O", "mixer_TTS", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        mixer_tts_split = mixer_tts_string.split(",")
        if mixer_tts_split[0] == "True":
            self.color_tts = ["True", float(mixer_tts_split[1]), float(mixer_tts_split[2]), float(mixer_tts_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.color_tts[1]*255, self.color_tts[2]*255, self.color_tts[3]*255))
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
        self.spacer_tint = 0
        self.spacer_tone = 0
        self.spacer_shade = 0
        self.mixer_tint.Update(self.spacer_tint, self.layout.tint.width())
        self.mixer_tone.Update(self.spacer_tone, self.layout.tone.width())
        self.mixer_shade.Update(self.spacer_shade, self.layout.shade.width())
        #//
        #\\ Mixer RGB ##########################################################
        # Mixer RGB 1
        mixer_rgb_1_string = Krita.instance().readSetting("Pigment.O", "mixer_RGB_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_rgb_l1 = ["False", 0, 0, 0]
            self.color_rgb_r1 = ["False", 0, 0, 0]
            self.layout.rgb_l1.setStyleSheet(bg_alpha)
            self.layout.rgb_r1.setStyleSheet(bg_alpha)
        self.spacer_rgb_g1 = 0
        self.mixer_rgb_g1.Update(self.spacer_rgb_g1, self.layout.rgb_g1.width())
        # Mixer RGB 2
        mixer_rgb_2_string = Krita.instance().readSetting("Pigment.O", "mixer_RGB_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_rgb_l2 = ["False", 0, 0, 0]
            self.color_rgb_r2 = ["False", 0, 0, 0]
            self.layout.rgb_l2.setStyleSheet(bg_alpha)
            self.layout.rgb_r2.setStyleSheet(bg_alpha)
        self.spacer_rgb_g2 = 0
        self.mixer_rgb_g2.Update(self.spacer_rgb_g2, self.layout.rgb_g2.width())
        # Mixer RGB 3
        mixer_rgb_3_string = Krita.instance().readSetting("Pigment.O", "mixer_RGB_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_rgb_l3 = ["False", 0, 0, 0]
            self.color_rgb_r3 = ["False", 0, 0, 0]
            self.layout.rgb_l3.setStyleSheet(bg_alpha)
            self.layout.rgb_r3.setStyleSheet(bg_alpha)
        self.spacer_rgb_g3 = 0
        self.mixer_rgb_g3.Update(self.spacer_rgb_g3, self.layout.rgb_g3.width())
        #//
        #\\ Mixer ARD ##########################################################
        # Mixer ARD 1
        mixer_ard_1_string = Krita.instance().readSetting("Pigment.O", "mixer_ARD_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_ard_l1 = ["False", 0, 0, 0]
            self.color_ard_r1 = ["False", 0, 0, 0]
            self.layout.ard_l1.setStyleSheet(bg_alpha)
            self.layout.ard_r1.setStyleSheet(bg_alpha)
        self.spacer_ard_g1 = 0
        self.mixer_ard_g1.Update(self.spacer_ard_g1, self.layout.ard_g1.width())
        # Mixer ARD 2
        mixer_ard_2_string = Krita.instance().readSetting("Pigment.O", "mixer_ARD_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_ard_l2 = ["False", 0, 0, 0]
            self.color_ard_r2 = ["False", 0, 0, 0]
            self.layout.ard_l2.setStyleSheet(bg_alpha)
            self.layout.ard_r2.setStyleSheet(bg_alpha)
        self.spacer_ard_g2 = 0
        self.mixer_ard_g2.Update(self.spacer_ard_g2, self.layout.ard_g2.width())
        # Mixer ARD 3
        mixer_ard_3_string = Krita.instance().readSetting("Pigment.O", "mixer_ARD_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_ard_l3 = ["False", 0, 0, 0]
            self.color_ard_r3 = ["False", 0, 0, 0]
            self.layout.ard_l3.setStyleSheet(bg_alpha)
            self.layout.ard_r3.setStyleSheet(bg_alpha)
        self.spacer_ard_g3 = 0
        self.mixer_ard_g3.Update(self.spacer_ard_g3, self.layout.ard_g3.width())
        #//
        #\\ Mixer HSV ##########################################################
        # Mixer HSV 1
        mixer_hsv_1_string = Krita.instance().readSetting("Pigment.O", "mixer_HSV_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_hsv_l1 = ["False", 0, 0, 0]
            self.color_hsv_r1 = ["False", 0, 0, 0]
            self.layout.hsv_l1.setStyleSheet(bg_alpha)
            self.layout.hsv_r1.setStyleSheet(bg_alpha)
        self.spacer_hsv_g1 = 0
        self.mixer_hsv_g1.Update(self.spacer_hsv_g1, self.layout.hsv_g1.width())
        # Mixer HSV 2
        mixer_hsv_2_string = Krita.instance().readSetting("Pigment.O", "mixer_HSV_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_hsv_l2 = ["False", 0, 0, 0]
            self.color_hsv_r2 = ["False", 0, 0, 0]
            self.layout.hsv_l2.setStyleSheet(bg_alpha)
            self.layout.hsv_r2.setStyleSheet(bg_alpha)
        self.spacer_hsv_g2 = 0
        self.mixer_hsv_g2.Update(self.spacer_hsv_g2, self.layout.hsv_g2.width())
        # Mixer HSV 3
        mixer_hsv_3_string = Krita.instance().readSetting("Pigment.O", "mixer_HSV_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_hsv_l3 = ["False", 0, 0, 0]
            self.color_hsv_r3 = ["False", 0, 0, 0]
            self.layout.hsv_l3.setStyleSheet(bg_alpha)
            self.layout.hsv_r3.setStyleSheet(bg_alpha)
        self.spacer_hsv_g3 = 0
        self.mixer_hsv_g3.Update(self.spacer_hsv_g3, self.layout.hsv_g3.width())
        #//
        #\\ Mixer HSL ##########################################################
        # Mixer HSL 1
        mixer_hsl_1_string = Krita.instance().readSetting("Pigment.O", "mixer_HSL_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_hsl_l1 = ["False", 0, 0, 0]
            self.color_hsl_r1 = ["False", 0, 0, 0]
            self.layout.hsl_l1.setStyleSheet(bg_alpha)
            self.layout.hsl_r1.setStyleSheet(bg_alpha)
        self.spacer_hsl_g1 = 0
        self.mixer_hsl_g1.Update(self.spacer_hsl_g1, self.layout.hsl_g1.width())
        # Mixer HSL 2
        mixer_hsl_2_string = Krita.instance().readSetting("Pigment.O", "mixer_HSL_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_hsl_l2 = ["False", 0, 0, 0]
            self.color_hsl_r2 = ["False", 0, 0, 0]
            self.layout.hsl_l2.setStyleSheet(bg_alpha)
            self.layout.hsl_r2.setStyleSheet(bg_alpha)
        self.spacer_hsl_g2 = 0
        self.mixer_hsl_g2.Update(self.spacer_hsl_g2, self.layout.hsl_g2.width())
        # Mixer HSL 3
        mixer_hsl_3_string = Krita.instance().readSetting("Pigment.O", "mixer_HSL_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_hsl_l3 = ["False", 0, 0, 0]
            self.color_hsl_r3 = ["False", 0, 0, 0]
            self.layout.hsl_l3.setStyleSheet(bg_alpha)
            self.layout.hsl_r3.setStyleSheet(bg_alpha)
        self.spacer_hsl_g3 = 0
        self.mixer_hsl_g3.Update(self.spacer_hsl_g3, self.layout.hsl_g3.width())
        #//
        #\\ Mixer CMYK #########################################################
        # Mixer CMYK 1
        mixer_cmyk_1_string = Krita.instance().readSetting("Pigment.O", "mixer_CMYK_1", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_cmyk_l1 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r1 = ["False", 0, 0, 0, 0]
            self.layout.cmyk_l1.setStyleSheet(bg_alpha)
            self.layout.cmyk_r1.setStyleSheet(bg_alpha)
        self.spacer_cmyk_g1 = 0
        self.mixer_cmyk_g1.Update(self.spacer_cmyk_g1, self.layout.cmyk_g1.width())
        # Mixer CMYK 2
        mixer_cmyk_2_string = Krita.instance().readSetting("Pigment.O", "mixer_CMYK_2", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_cmyk_l2 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r2 = ["False", 0, 0, 0, 0]
            self.layout.cmyk_l2.setStyleSheet(bg_alpha)
            self.layout.cmyk_r2.setStyleSheet(bg_alpha)
        self.spacer_cmyk_g2 = 0
        self.mixer_cmyk_g2.Update(self.spacer_cmyk_g2, self.layout.cmyk_g2.width())
        # Mixer CMYK 3
        mixer_cmyk_3_string = Krita.instance().readSetting("Pigment.O", "mixer_CMYK_3", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
        else:
            self.color_cmyk_l3 = ["False", 0, 0, 0, 0]
            self.color_cmyk_r3 = ["False", 0, 0, 0, 0]
            self.layout.cmyk_l3.setStyleSheet(bg_alpha)
            self.layout.cmyk_r3.setStyleSheet(bg_alpha)
        self.spacer_cmyk_g3 = 0
        self.mixer_cmyk_g3.Update(self.spacer_cmyk_g3, self.layout.cmyk_g3.width())
        #//
        #\\ Mixer Gradient Display #############################################
        self.Mixer_Display()
        #//
        #\\ DOTs ###############################################################
        dot_01_string = Krita.instance().readSetting("Pigment.O", "dot_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        dot_02_string = Krita.instance().readSetting("Pigment.O", "dot_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        dot_03_string = Krita.instance().readSetting("Pigment.O", "dot_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        dot_04_string = Krita.instance().readSetting("Pigment.O", "dot_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        dot_01_split = dot_01_string.split(",")
        dot_02_split = dot_02_string.split(",")
        dot_03_split = dot_03_string.split(",")
        dot_04_split = dot_04_string.split(",")
        if dot_01_split[0] == "True":
            self.dot_1 = ["True", float(dot_01_split[1]), float(dot_01_split[2]), float(dot_01_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
            self.layout.dot_1.setStyleSheet(color)
        else:
            self.dot_1 = ["True", 183/255, 46/255, 53/255, 1] # Cadmium Red
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_1[1]*255, self.dot_1[2]*255, self.dot_1[3]*255))
            self.layout.dot_1.setStyleSheet(color)
        if dot_02_split[0] == "True":
            self.dot_2 = ["True", float(dot_02_split[1]), float(dot_02_split[2]), float(dot_02_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
            self.layout.dot_2.setStyleSheet(color)
        else:
            self.dot_2 = ["True", 237/255, 181/255, 37/255, 1] # Yellow Ochre
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_2[1]*255, self.dot_2[2]*255, self.dot_2[3]*255))
            self.layout.dot_2.setStyleSheet(color)
        if dot_03_split[0] == "True":
            self.dot_3 = ["True", float(dot_03_split[1]), float(dot_03_split[2]), float(dot_03_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
            self.layout.dot_3.setStyleSheet(color)
        else:
            self.dot_3 = ["True", 41/255, 36/255, 33/255, 1] # IvoryBlack
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_3[1]*255, self.dot_3[2]*255, self.dot_3[3]*255))
            self.layout.dot_3.setStyleSheet(color)
        if dot_04_split[0] == "True":
            self.dot_4 = ["True", float(dot_04_split[1]), float(dot_04_split[2]), float(dot_04_split[3])]
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
            self.layout.dot_4.setStyleSheet(color)
        else:
            self.dot_4 = ["True", 237/255, 240/255, 236/255, 1] # Titanium White
            color = str("background-color: rgb(%f, %f, %f); border: 1px solid rgba(56, 56, 56, 255) ;" % (self.dot_4[1]*255, self.dot_4[2]*255, self.dot_4[3]*255))
            self.layout.dot_4.setStyleSheet(color)
        #//
        #\\ Object #############################################################
        object_01_string = Krita.instance().readSetting("Pigment.O", "object_01", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_02_string = Krita.instance().readSetting("Pigment.O", "object_02", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_03_string = Krita.instance().readSetting("Pigment.O", "object_03", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_04_string = Krita.instance().readSetting("Pigment.O", "object_04", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_05_string = Krita.instance().readSetting("Pigment.O", "object_05", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_06_string = Krita.instance().readSetting("Pigment.O", "object_06", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_07_string = Krita.instance().readSetting("Pigment.O", "object_07", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_08_string = Krita.instance().readSetting("Pigment.O", "object_08", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_09_string = Krita.instance().readSetting("Pigment.O", "object_09", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_10_string = Krita.instance().readSetting("Pigment.O", "object_10", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_11_string = Krita.instance().readSetting("Pigment.O", "object_11", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
        object_12_string = Krita.instance().readSetting("Pigment.O", "object_12", "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,1|RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,1")
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
            # Reset Colors to Sphere when all are False
            if (str(object_01_split[0]) == "False" and
                str(object_02_split[0]) == "False" and
                str(object_03_split[0]) == "False" and
                str(object_04_split[0]) == "False" and
                str(object_05_split[0]) == "False" and
                str(object_06_split[0]) == "False" and
                str(object_07_split[0]) == "False" and
                str(object_08_split[0]) == "False" and
                str(object_09_split[0]) == "False" and
                str(object_10_split[0]) == "False" and
                str(object_11_split[0]) == "False" and
                str(object_12_split[0]) == "False"):
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
        except:
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
        #//
    def Settings_Save_Misc(self):
        #\\ SOF ################################################################
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Save Settings
            tip_sof_list = (str(self.lock_size), str(self.lock_opacity), str(self.lock_flow))
            tip_sof_string = ','.join(tip_sof_list)
            Krita.instance().writeSetting("Pigment.O", "tip_SOF", tip_sof_string)
        #//
        #\\ Palette ############################################################
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
        Krita.instance().writeSetting("Pigment.O", "tip_color_00", color_00_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_01", color_01_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_02", color_02_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_03", color_03_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_04", color_04_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_05", color_05_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_06", color_06_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_07", color_07_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_08", color_08_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_09", color_09_string)
        Krita.instance().writeSetting("Pigment.O", "tip_color_10", color_10_string)
        #//
        #\\ Mixer TTS ##########################################################
        color_tts_list = (str(self.color_tts[0]), str(self.color_tts[1]), str(self.color_tts[2]), str(self.color_tts[3]))
        color_tts_string = ','.join(color_tts_list)
        Krita.instance().writeSetting("Pigment.O", "mixer_TTS", color_tts_string)
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
        Krita.instance().writeSetting("Pigment.O", "mixer_RGB_1", mixer_string_rgb_1)
        Krita.instance().writeSetting("Pigment.O", "mixer_RGB_2", mixer_string_rgb_2)
        Krita.instance().writeSetting("Pigment.O", "mixer_RGB_3", mixer_string_rgb_3)
        Krita.instance().writeSetting("Pigment.O", "mixer_ARD_1", mixer_string_ard_1)
        Krita.instance().writeSetting("Pigment.O", "mixer_ARD_2", mixer_string_ard_2)
        Krita.instance().writeSetting("Pigment.O", "mixer_ARD_3", mixer_string_ard_3)
        Krita.instance().writeSetting("Pigment.O", "mixer_HSV_1", mixer_string_hsv_1)
        Krita.instance().writeSetting("Pigment.O", "mixer_HSV_2", mixer_string_hsv_2)
        Krita.instance().writeSetting("Pigment.O", "mixer_HSV_3", mixer_string_hsv_3)
        Krita.instance().writeSetting("Pigment.O", "mixer_HSL_1", mixer_string_hsl_1)
        Krita.instance().writeSetting("Pigment.O", "mixer_HSL_2", mixer_string_hsl_2)
        Krita.instance().writeSetting("Pigment.O", "mixer_HSL_3", mixer_string_hsl_3)
        Krita.instance().writeSetting("Pigment.O", "mixer_CMYK_1", mixer_string_cmyk_1)
        Krita.instance().writeSetting("Pigment.O", "mixer_CMYK_2", mixer_string_cmyk_2)
        Krita.instance().writeSetting("Pigment.O", "mixer_CMYK_3", mixer_string_cmyk_3)
        #//
        #\\ DOTs ###############################################################
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
        #\\ Object #############################################################
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
        Krita.instance().writeSetting("Pigment.O", "object_01", object_string_01)
        Krita.instance().writeSetting("Pigment.O", "object_02", object_string_02)
        Krita.instance().writeSetting("Pigment.O", "object_03", object_string_03)
        Krita.instance().writeSetting("Pigment.O", "object_04", object_string_04)
        Krita.instance().writeSetting("Pigment.O", "object_05", object_string_05)
        Krita.instance().writeSetting("Pigment.O", "object_06", object_string_06)
        Krita.instance().writeSetting("Pigment.O", "object_07", object_string_07)
        Krita.instance().writeSetting("Pigment.O", "object_08", object_string_08)
        Krita.instance().writeSetting("Pigment.O", "object_09", object_string_09)
        Krita.instance().writeSetting("Pigment.O", "object_10", object_string_10)
        Krita.instance().writeSetting("Pigment.O", "object_11", object_string_11)
        Krita.instance().writeSetting("Pigment.O", "object_12", object_string_12)
        #//

    #//
    #\\ Change the Canvas ######################################################
    def canvasChanged(self, canvas):
        # QMessageBox.information(QWidget(), i18n("Warnning"), i18n("message"))
        pass
    #//
