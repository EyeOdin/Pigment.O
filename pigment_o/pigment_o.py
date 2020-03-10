# Import Krita
from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic
import os.path
import colorsys

from .pigment_o_style import Style
from .pigment_o_channel import Channel
from .pigment_o_panel import PanelHsv

# Set Window Title Name
DOCKER_NAME = "Pigment.O"
check_timer = 0 # 1000 = 1 SECOND (Zero will Disable checks)
factor255 = 255
factor360 = 360
factor100 = 100

# Create Docker
class PigmentODocker(DockWidget):
    """
    Compact Color Selector with various Color Spaces to choose from
    """

    # Initialize the Dicker Window
    def __init__(self):
        super(PigmentODocker, self).__init__()

        # Window Title
        self.setWindowTitle(DOCKER_NAME)
        # Widget
        self.window = QWidget()
        self.layout = uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + '/pigment_o.ui', self.window)
        self.setWidget(self.window)

        # Start up Connections
        self.Connect()

        # Variables
        self.Color_Display(0,0,0, 0,0,0)
        self.layout.rgb_color_space.setChecked(True)
        self.layout.hsv_color_space.setChecked(False)
        self.Display_RGB()
        self.Display_HSV()

    def Connect(self):
        # Module Style
        self.style = Style()

        # Module Channel
        self.rgb_1_slider = Channel(self.layout.rgb_1_slider)
        self.rgb_2_slider = Channel(self.layout.rgb_2_slider)
        self.rgb_3_slider = Channel(self.layout.rgb_3_slider)
        self.rgb_1_slider.Setup("RGB", 1)
        self.rgb_2_slider.Setup("RGB", 2)
        self.rgb_3_slider.Setup("RGB", 3)
        self.hsv_1_slider = Channel(self.layout.hsv_1_slider)
        self.hsv_2_slider = Channel(self.layout.hsv_2_slider)
        self.hsv_3_slider = Channel(self.layout.hsv_3_slider)
        self.hsv_1_slider.Setup("HSV", 1)
        self.hsv_2_slider.Setup("HSV", 2)
        self.hsv_3_slider.Setup("HSV", 3)

        # Connect Channel Red
        self.layout.rgb_1_label.clicked.connect(lambda: self.Pigment_RGB_1("50", 0))
        self.layout.rgb_1_minus.clicked.connect(lambda: self.Pigment_RGB_1("M1", 1))
        self.layout.rgb_1_plus.clicked.connect(lambda: self.Pigment_RGB_1("P1", 1))
        self.rgb_1_slider.SIGNALVALUE.connect(self.layout.rgb_1_value.setValue)
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.rgb_1_slider.Update(self.layout.rgb_1_value.value(), factor255, self.layout.rgb_1_slider.width()))
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.Pigment_RGB_1("SYNC", 0))

        # Connect Channel Green
        self.layout.rgb_2_label.clicked.connect(lambda: self.Pigment_RGB_2("50", 0))
        self.layout.rgb_2_minus.clicked.connect(lambda: self.Pigment_RGB_2("M1", 1))
        self.layout.rgb_2_plus.clicked.connect(lambda: self.Pigment_RGB_2("P1", 1))
        self.rgb_2_slider.SIGNALVALUE.connect(self.layout.rgb_2_value.setValue)
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.rgb_2_slider.Update(self.layout.rgb_2_value.value(), factor255, self.layout.rgb_2_slider.width()))
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.Pigment_RGB_2("SYNC", 0))

        # Connect Channel Blue
        self.layout.rgb_3_label.clicked.connect(lambda: self.Pigment_RGB_3("50", 0))
        self.layout.rgb_3_minus.clicked.connect(lambda: self.Pigment_RGB_3("M1", 1))
        self.layout.rgb_3_plus.clicked.connect(lambda: self.Pigment_RGB_3("P1", 1))
        self.rgb_3_slider.SIGNALVALUE.connect(self.layout.rgb_3_value.setValue)
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.rgb_3_slider.Update(self.layout.rgb_3_value.value(), factor255, self.layout.rgb_3_slider.width()))
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.Pigment_RGB_3("SYNC", 0))

        # Connect Channel Hue
        self.layout.hsv_1_label.clicked.connect(lambda: self.Pigment_HSV_1("50", 0))
        self.layout.hsv_1_minus.clicked.connect(lambda: self.Pigment_HSV_1("M1", 1))
        self.layout.hsv_1_plus.clicked.connect(lambda: self.Pigment_HSV_1("P1", 1))
        self.hsv_1_slider.SIGNALVALUE.connect(self.layout.hsv_1_value.setValue)
        self.layout.hsv_1_value.valueChanged.connect(lambda: self.hsv_1_slider.Update(self.layout.hsv_1_value.value(), factor360, self.layout.hsv_1_slider.width()))

        # Connect Channel Saturation
        self.layout.hsv_2_label.clicked.connect(lambda: self.Pigment_HSV_2("50", 0))
        self.layout.hsv_2_minus.clicked.connect(lambda: self.Pigment_HSV_2("M1", 1))
        self.layout.hsv_2_plus.clicked.connect(lambda: self.Pigment_HSV_2("P1", 1))
        self.hsv_2_slider.SIGNALVALUE.connect(self.layout.hsv_2_value.setValue)
        self.layout.hsv_2_value.valueChanged.connect(lambda: self.hsv_2_slider.Update(self.layout.hsv_2_value.value(), factor100, self.layout.hsv_2_slider.width()))

        # Connect Channel Value
        self.layout.hsv_3_label.clicked.connect(lambda: self.Pigment_HSV_3("50", 0))
        self.layout.hsv_3_minus.clicked.connect(lambda: self.Pigment_HSV_3("M1", 1))
        self.layout.hsv_3_plus.clicked.connect(lambda: self.Pigment_HSV_3("P1", 1))
        self.hsv_3_slider.SIGNALVALUE.connect(self.layout.hsv_3_value.setValue)
        self.layout.hsv_3_value.valueChanged.connect(lambda: self.hsv_3_slider.Update(self.layout.hsv_3_value.value(), factor100, self.layout.hsv_3_slider.width()))

        # Connect Sync Signal
        self.rgb_1_slider.SIGNALSYNC.connect(self.Flow_RGB)
        self.rgb_2_slider.SIGNALSYNC.connect(self.Flow_RGB)
        self.rgb_3_slider.SIGNALSYNC.connect(self.Flow_RGB)
        self.hsv_1_slider.SIGNALSYNC.connect(self.Flow_HSV)
        self.hsv_2_slider.SIGNALSYNC.connect(self.Flow_HSV)
        self.hsv_3_slider.SIGNALSYNC.connect(self.Flow_HSV)

        # Active Color
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.Active_Color("RGB"))
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.Active_Color("RGB"))
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.Active_Color("RGB"))
        self.layout.hsv_1_value.valueChanged.connect(lambda: self.Active_Color("HSV"))
        self.layout.hsv_2_value.valueChanged.connect(lambda: self.Active_Color("HSV"))
        self.layout.hsv_3_value.valueChanged.connect(lambda: self.Active_Color("HSV"))

        # Hex Input
        self.layout.hex_string.returnPressed.connect(lambda: self.HEX_Code(self.layout.hex_string.text()))

        # Percentage Gradients Display
        p4 = self.style.Percentage("4")
        p6 = self.style.Percentage("6")
        p10 = self.style.Percentage("10")
        self.layout.percentage_top.setStyleSheet(p10)
        self.layout.percentage_bot.setStyleSheet(p10)
        self.layout.rgb_1_tick.setStyleSheet(p4)
        self.layout.rgb_2_tick.setStyleSheet(p4)
        self.layout.rgb_3_tick.setStyleSheet(p4)
        self.layout.hsv_1_tick.setStyleSheet(p6)
        self.layout.hsv_2_tick.setStyleSheet(p4)
        self.layout.hsv_3_tick.setStyleSheet(p4)

        # Krita Update Timer
        if check_timer >= 1000:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Krita_Update)
            self.timer.start(check_timer)
        else:
            pass

        # Channels Display
        self.layout.rgb_color_space.toggled.connect(self.Display_RGB)
        self.layout.hsv_color_space.toggled.connect(self.Display_HSV)

    # Function Operations
    def Document_Profile(self):
        ki = Krita.instance()
        ad = ki.activeDocument()
        color_model = ad.colorModel()
        color_depth = ad.colorDepth()
        color_profile = ad.colorProfile()
        doc = []
        doc.append(color_model)
        doc.append(color_depth)
        doc.append(color_profile)
        return doc

    def Active_Color(self, mode):
        if mode == "RGB":
            # Original
            rgb1 = self.layout.rgb_1_value.value() / factor255
            rgb2 = self.layout.rgb_2_value.value() / factor255
            rgb3 = self.layout.rgb_3_value.value() / factor255
            # Convert HSV
            hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
            hsv1 = hsv[0]
            hsv2 = hsv[1]
            hsv3 = hsv[2]
        if mode == "HSV":
            # Original
            hsv1 = self.layout.hsv_1_value.value() / factor360
            hsv2 = self.layout.hsv_2_value.value() / factor100
            hsv3 = self.layout.hsv_3_value.value() / factor100
            # Convert RGB
            rgb = colorsys.hsv_to_rgb(hsv1, hsv2, hsv3)
            rgb1 = rgb[0]
            rgb2 = rgb[1]
            rgb3 = rgb[2]
        # Update Values
        self.Pigment_2_Krita(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)
        self.Color_Display(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Pigment_2_Krita(self, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        # Set Krita Foreground Color
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            doc = self.Document_Profile()
            if doc[0] == "A":
                pass
            elif doc[0] == "RGBA": # The actual order of channels is most often BGR
                pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                pigment_color.setComponents([rgb3, rgb2, rgb1, 1.0])
                Application.activeWindow().activeView().setForeGroundColor(pigment_color)
            elif doc[0] == "XYZA":
                pass
            elif doc[0] == "LABA":
                pass
            elif doc[0] == "CMYKA":
                pass
            elif doc[0] == "GRAYA":
                pass
            elif doc[0] == "YCbCrA":
                pass
        self.update()

    def Color_Display(self, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        # Foreground Color Display (Top Left)
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (rgb1*255, rgb2*255, rgb3*255))
        self.layout.color_1.setStyleSheet(active_color_1)
        # Slider Gradients (Top Center)
        sss_rgb1 = str(self.style.Slider("RGB", 0, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3 ))
        sss_rgb2 = str(self.style.Slider("RGB", 1, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3 ))
        sss_rgb3 = str(self.style.Slider("RGB", 2, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3 ))
        sss_hsv1 = str(self.style.Slider("HSV", 0, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3 ))
        sss_hsv2 = str(self.style.Slider("HSV", 1, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3 ))
        sss_hsv3 = str(self.style.Slider("HSV", 2, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3 ))
        self.layout.rgb_1_slider.setStyleSheet(sss_rgb1)
        self.layout.rgb_2_slider.setStyleSheet(sss_rgb2)
        self.layout.rgb_3_slider.setStyleSheet(sss_rgb3)
        self.layout.hsv_1_slider.setStyleSheet(sss_hsv1)
        self.layout.hsv_2_slider.setStyleSheet(sss_hsv2)
        self.layout.hsv_3_slider.setStyleSheet(sss_hsv3)
        # Exception for Greys to become RED
        hue = hsv1 * 360
        if hue == -1:hue = 0
        else:pass
        # Colors for HSV Square Background Gradients
        base_color = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ffffff, stop:1 hsl(%f, %f, %f)); }" % (hue, 255, 255))
        self.layout.panel_bg.setStyleSheet(base_color)
        base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
        self.layout.panel_fg.setStyleSheet(base_value)
        # Hex Color
        hex = self.RGB_2_HEX(rgb1*255, rgb2*255, rgb3*255)
        self.layout.hex_string.setText(str(hex))

    def RGB_2_HEX(self, rgb1, rgb2, rgb3):
        hex1 = str(hex(int(rgb1)))[2:4].zfill(2)
        hex2 = str(hex(int(rgb2)))[2:4].zfill(2)
        hex3 = str(hex(int(rgb3)))[2:4].zfill(2)
        pigment_hex = str("#"+hex1+hex2+hex3)
        return pigment_hex

    def HEX_Code(self, hex):
        code = QColor(str(hex))
        # RGB
        rgb = code.toRgb()
        self.Pigment_RGB_1("HEX", rgb.redF()*factor255)
        self.Pigment_RGB_2("HEX", rgb.greenF()*factor255)
        self.Pigment_RGB_3("HEX", rgb.blueF()*factor255)
        # HSV
        hsv = code.toHsv()
        self.Pigment_HSV_1("HEX", hsv.hsvHueF()*factor360)
        self.Pigment_HSV_2("HEX", hsv.hsvSaturationF()*factor100)
        self.Pigment_HSV_3("HEX", hsv.valueF()*factor100)

    def Flow_RGB(self, SIGNALSYNC):
        self.layout.label.setText(str(SIGNALSYNC)+" RGB")
    def Flow_HSV(self, SIGNALSYNC):
        self.layout.label.setText(str(SIGNALSYNC)+" HSV")

    def Krita_Update(self):
        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Color Space Mode
            # self.mode = self.layout.space_display.currentText()
            # Pigment Values
            rgb1 = self.layout.rgb_1_value.value() / factor255
            rgb2 = self.layout.rgb_2_value.value() / factor255
            rgb3 = self.layout.rgb_3_value.value() / factor255
            hsv1 = self.layout.hsv_1_value.value() / factor360
            hsv2 = self.layout.hsv_2_value.value() / factor100
            hsv3 = self.layout.hsv_3_value.value() / factor100
            # Document Profile
            doc = self.Document_Profile()
            krita_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
            krita_color = Application.activeWindow().activeView().foregroundColor()
            components = krita_color.components()
            # Krita Current Foreground Color RGB
            if doc[0] == "RGBA":
                kac1 = components[2]
                kac2 = components[1]
                kac3 = components[0]
            else:
                kac1 = components[0]
                kac2 = components[1]
                kac3 = components[2]
            # Update Pigmento if Values Differ
            if doc[0] == "A":
                pass
            elif doc[0] == "RGBA":
                if (rgb1!=kac1 or rgb2!=kac2 or rgb3!=kac3):
                    r = kac1 * factor255
                    g = kac2 * factor255
                    b = kac3 * factor255
                    self.Pigment_RGB_1("KU", r)
                    self.Pigment_RGB_2("KU", g)
                    self.Pigment_RGB_3("KU", b)
                    self.Active_Color("RGB")
                    # HSV
                    # kac123 = colorsys.rgb_to_hsv(kac1, kac2, kac3)
                    # h = kac123[0] * factor360
                    # s = kac123[1] * factor100
                    # v = kac123[2] * factor100
                    # self.Pigment_RGB_1(self.mode, "KU", h)
                    # self.Pigment_RGB_2(self.mode, "KU", s)
                    # self.Pigment_RGB_3(self.mode, "KU", v)
                    # self.Active_Color()
            elif doc[0] == "XYZA":
                pass
            elif doc[0] == "LABA":
                pass
            elif doc[0] == "CMYKA":
                pass
            elif doc[0] == "GRAYA":
                pass
            elif doc[0] == "YCbCrA":
                pass

    def Display_RGB(self):
        if self.layout.rgb_color_space.isChecked():
            self.layout.rgb_1_label.setMinimumHeight(8)
            self.layout.rgb_1_label.setMaximumHeight(12)
            self.layout.rgb_1_minus.setMinimumHeight(8)
            self.layout.rgb_1_minus.setMaximumHeight(12)
            self.layout.rgb_1_slider.setMinimumHeight(8)
            self.layout.rgb_1_slider.setMaximumHeight(12)
            self.layout.rgb_1_plus.setMinimumHeight(8)
            self.layout.rgb_1_plus.setMaximumHeight(12)
            self.layout.rgb_1_value.setMinimumHeight(8)
            self.layout.rgb_1_value.setMaximumHeight(12)
            self.layout.rgb_1_tick.setMinimumHeight(1)

            self.layout.rgb_2_label.setMinimumHeight(8)
            self.layout.rgb_2_label.setMaximumHeight(12)
            self.layout.rgb_2_minus.setMinimumHeight(8)
            self.layout.rgb_2_minus.setMaximumHeight(12)
            self.layout.rgb_2_slider.setMinimumHeight(8)
            self.layout.rgb_2_slider.setMaximumHeight(12)
            self.layout.rgb_2_plus.setMinimumHeight(8)
            self.layout.rgb_2_plus.setMaximumHeight(12)
            self.layout.rgb_2_value.setMinimumHeight(8)
            self.layout.rgb_2_value.setMaximumHeight(12)
            self.layout.rgb_2_tick.setMinimumHeight(1)

            self.layout.rgb_3_label.setMinimumHeight(8)
            self.layout.rgb_3_label.setMaximumHeight(12)
            self.layout.rgb_3_minus.setMinimumHeight(8)
            self.layout.rgb_3_minus.setMaximumHeight(12)
            self.layout.rgb_3_slider.setMinimumHeight(8)
            self.layout.rgb_3_slider.setMaximumHeight(12)
            self.layout.rgb_3_plus.setMinimumHeight(8)
            self.layout.rgb_3_plus.setMaximumHeight(12)
            self.layout.rgb_3_value.setMinimumHeight(8)
            self.layout.rgb_3_value.setMaximumHeight(12)
            self.layout.rgb_3_tick.setMinimumHeight(1)
        else:
            self.layout.rgb_1_label.setMinimumHeight(0)
            self.layout.rgb_1_label.setMaximumHeight(0)
            self.layout.rgb_1_minus.setMinimumHeight(0)
            self.layout.rgb_1_minus.setMaximumHeight(0)
            self.layout.rgb_1_slider.setMinimumHeight(0)
            self.layout.rgb_1_slider.setMaximumHeight(0)
            self.layout.rgb_1_plus.setMinimumHeight(0)
            self.layout.rgb_1_plus.setMaximumHeight(0)
            self.layout.rgb_1_value.setMinimumHeight(0)
            self.layout.rgb_1_value.setMaximumHeight(0)
            self.layout.rgb_1_tick.setMinimumHeight(0)

            self.layout.rgb_2_label.setMinimumHeight(0)
            self.layout.rgb_2_label.setMaximumHeight(0)
            self.layout.rgb_2_minus.setMinimumHeight(0)
            self.layout.rgb_2_minus.setMaximumHeight(0)
            self.layout.rgb_2_slider.setMinimumHeight(0)
            self.layout.rgb_2_slider.setMaximumHeight(0)
            self.layout.rgb_2_plus.setMinimumHeight(0)
            self.layout.rgb_2_plus.setMaximumHeight(0)
            self.layout.rgb_2_value.setMinimumHeight(0)
            self.layout.rgb_2_value.setMaximumHeight(0)
            self.layout.rgb_2_tick.setMinimumHeight(0)

            self.layout.rgb_3_label.setMinimumHeight(0)
            self.layout.rgb_3_label.setMaximumHeight(0)
            self.layout.rgb_3_minus.setMinimumHeight(0)
            self.layout.rgb_3_minus.setMaximumHeight(0)
            self.layout.rgb_3_slider.setMinimumHeight(0)
            self.layout.rgb_3_slider.setMaximumHeight(0)
            self.layout.rgb_3_plus.setMinimumHeight(0)
            self.layout.rgb_3_plus.setMaximumHeight(0)
            self.layout.rgb_3_value.setMinimumHeight(0)
            self.layout.rgb_3_value.setMaximumHeight(0)
            self.layout.rgb_3_tick.setMinimumHeight(0)

    def Display_HSV(self):
        if self.layout.hsv_color_space.isChecked():
            self.layout.hsv_1_label.setMinimumHeight(8)
            self.layout.hsv_1_label.setMaximumHeight(12)
            self.layout.hsv_1_minus.setMinimumHeight(8)
            self.layout.hsv_1_minus.setMaximumHeight(12)
            self.layout.hsv_1_slider.setMinimumHeight(8)
            self.layout.hsv_1_slider.setMaximumHeight(12)
            self.layout.hsv_1_plus.setMinimumHeight(8)
            self.layout.hsv_1_plus.setMaximumHeight(12)
            self.layout.hsv_1_value.setMinimumHeight(8)
            self.layout.hsv_1_value.setMaximumHeight(12)
            self.layout.hsv_1_tick.setMinimumHeight(1)

            self.layout.hsv_2_label.setMinimumHeight(8)
            self.layout.hsv_2_label.setMaximumHeight(12)
            self.layout.hsv_2_minus.setMinimumHeight(8)
            self.layout.hsv_2_minus.setMaximumHeight(12)
            self.layout.hsv_2_slider.setMinimumHeight(8)
            self.layout.hsv_2_slider.setMaximumHeight(12)
            self.layout.hsv_2_plus.setMinimumHeight(8)
            self.layout.hsv_2_plus.setMaximumHeight(12)
            self.layout.hsv_2_value.setMinimumHeight(8)
            self.layout.hsv_2_value.setMaximumHeight(12)
            self.layout.hsv_2_tick.setMinimumHeight(1)

            self.layout.hsv_3_label.setMinimumHeight(8)
            self.layout.hsv_3_label.setMaximumHeight(12)
            self.layout.hsv_3_minus.setMinimumHeight(8)
            self.layout.hsv_3_minus.setMaximumHeight(12)
            self.layout.hsv_3_slider.setMinimumHeight(8)
            self.layout.hsv_3_slider.setMaximumHeight(12)
            self.layout.hsv_3_plus.setMinimumHeight(8)
            self.layout.hsv_3_plus.setMaximumHeight(12)
            self.layout.hsv_3_value.setMinimumHeight(8)
            self.layout.hsv_3_value.setMaximumHeight(12)
            self.layout.hsv_3_tick.setMinimumHeight(1)
        else:
            self.layout.hsv_1_label.setMinimumHeight(0)
            self.layout.hsv_1_label.setMaximumHeight(0)
            self.layout.hsv_1_minus.setMinimumHeight(0)
            self.layout.hsv_1_minus.setMaximumHeight(0)
            self.layout.hsv_1_slider.setMinimumHeight(0)
            self.layout.hsv_1_slider.setMaximumHeight(0)
            self.layout.hsv_1_plus.setMinimumHeight(0)
            self.layout.hsv_1_plus.setMaximumHeight(0)
            self.layout.hsv_1_value.setMinimumHeight(0)
            self.layout.hsv_1_value.setMaximumHeight(0)
            self.layout.hsv_1_tick.setMinimumHeight(0)

            self.layout.hsv_2_label.setMinimumHeight(0)
            self.layout.hsv_2_label.setMaximumHeight(0)
            self.layout.hsv_2_minus.setMinimumHeight(0)
            self.layout.hsv_2_minus.setMaximumHeight(0)
            self.layout.hsv_2_slider.setMinimumHeight(0)
            self.layout.hsv_2_slider.setMaximumHeight(0)
            self.layout.hsv_2_plus.setMinimumHeight(0)
            self.layout.hsv_2_plus.setMaximumHeight(0)
            self.layout.hsv_2_value.setMinimumHeight(0)
            self.layout.hsv_2_value.setMaximumHeight(0)
            self.layout.hsv_2_tick.setMinimumHeight(0)

            self.layout.hsv_3_label.setMinimumHeight(0)
            self.layout.hsv_3_label.setMaximumHeight(0)
            self.layout.hsv_3_minus.setMinimumHeight(0)
            self.layout.hsv_3_minus.setMaximumHeight(0)
            self.layout.hsv_3_slider.setMinimumHeight(0)
            self.layout.hsv_3_slider.setMaximumHeight(0)
            self.layout.hsv_3_plus.setMinimumHeight(0)
            self.layout.hsv_3_plus.setMaximumHeight(0)
            self.layout.hsv_3_value.setMinimumHeight(0)
            self.layout.hsv_3_value.setMaximumHeight(0)
            self.layout.hsv_3_tick.setMinimumHeight(0)

    # Button Controls
    def Pigment_RGB_1(self, case, value):
        width = self.layout.rgb_1_slider.width()
        if case == "50":
            min = self.layout.rgb_1_value.minimum()
            max = self.layout.rgb_1_value.maximum()
            half = (max-min)/2
            self.rgb_1_slider.Update(half, factor255, width)
            self.layout.rgb_1_value.setValue(half)
        elif case == "M1":
            channel = self.layout.rgb_1_value.value()
            self.rgb_1_slider.Update((channel-value), factor255, width)
            self.layout.rgb_1_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.rgb_1_value.value()
            self.rgb_1_slider.Update((channel+value), factor255, width)
            self.layout.rgb_1_value.setValue(channel+value)
        elif case == "KU":
            self.rgb_1_slider.Update(value, factor255, width)
            self.layout.rgb_1_value.setValue(value)
        elif case == "HEX":
            self.rgb_1_slider.Update(value, factor255, width)
            self.layout.rgb_1_value.setValue(value)
        elif case == "SYNC":
            ac1 = self.layout.rgb_1_value.value() / factor255
            ac2 = self.layout.rgb_2_value.value() / factor255
            ac3 = self.layout.rgb_3_value.value() / factor255
            hsv = colorsys.rgb_to_hsv(ac1, ac2, ac3)
            self.layout.hsv_1_value.setValue(hsv[0]*factor360)
            self.layout.hsv_2_value.setValue(hsv[1]*factor100)
            self.layout.hsv_3_value.setValue(hsv[2]*factor100)

    def Pigment_RGB_2(self, case, value):
        width = self.layout.rgb_2_slider.width()
        if case == "50":
            min = self.layout.rgb_2_value.minimum()
            max = self.layout.rgb_2_value.maximum()
            half = (max-min)/2
            self.rgb_2_slider.Update(half, factor255, width)
            self.layout.rgb_2_value.setValue(half)
        elif case == "M1":
            channel = self.layout.rgb_2_value.value()
            self.rgb_2_slider.Update((channel-value), factor255, width)
            self.layout.rgb_2_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.rgb_2_value.value()
            self.rgb_2_slider.Update((channel+value), factor255, width)
            self.layout.rgb_2_value.setValue(channel+value)
        elif case == "KU":
            self.rgb_2_slider.Update(value, factor255, width)
            self.layout.rgb_2_value.setValue(value)
        elif case == "HEX":
            self.rgb_2_slider.Update(value, factor255, width)
            self.layout.rgb_2_value.setValue(value)
        elif case == "SYNC":
            ac1 = self.layout.rgb_1_value.value() / factor255
            ac2 = self.layout.rgb_2_value.value() / factor255
            ac3 = self.layout.rgb_3_value.value() / factor255
            hsv = colorsys.rgb_to_hsv(ac1, ac2, ac3)
            self.layout.hsv_1_value.setValue(hsv[0]*factor360)
            self.layout.hsv_2_value.setValue(hsv[1]*factor100)
            self.layout.hsv_3_value.setValue(hsv[2]*factor100)

    def Pigment_RGB_3(self, case, value):
        width = self.layout.rgb_3_slider.width()
        if case == "50":
            min = self.layout.rgb_3_value.minimum()
            max = self.layout.rgb_3_value.maximum()
            half = (max-min)/2
            self.rgb_3_slider.Update(half, factor255, width)
            self.layout.rgb_3_value.setValue(half)
        elif case == "M1":
            channel = self.layout.rgb_3_value.value()
            self.rgb_3_slider.Update((channel-value), factor255, width)
            self.layout.rgb_3_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.rgb_3_value.value()
            self.rgb_3_slider.Update((channel+value), factor255, width)
            self.layout.rgb_3_value.setValue(channel+value)
        elif case == "KU":
            self.rgb_3_slider.Update(value, factor255, width)
            self.layout.rgb_3_value.setValue(value)
        elif case == "HEX":
            self.rgb_3_slider.Update(value, factor255, width)
            self.layout.rgb_3_value.setValue(value)
        elif case == "SYNC":
            ac1 = self.layout.rgb_1_value.value() / factor255
            ac2 = self.layout.rgb_2_value.value() / factor255
            ac3 = self.layout.rgb_3_value.value() / factor255
            hsv = colorsys.rgb_to_hsv(ac1, ac2, ac3)
            self.layout.hsv_1_value.setValue(hsv[0]*factor360)
            self.layout.hsv_2_value.setValue(hsv[1]*factor100)
            self.layout.hsv_3_value.setValue(hsv[2]*factor100)

    def Pigment_HSV_1(self, case, value):
        width = self.layout.hsv_1_slider.width()
        if case == "50":
            hue = self.layout.hsv_1_value.value()
            if   (hue >= 0 and hue <= 30):hue=0
            elif (hue > 30 and hue <= 90):hue=60
            elif (hue > 90 and hue <= 150):hue=120
            elif (hue > 150 and hue <= 210):hue=180
            elif (hue > 210 and hue <= 270):hue=240
            elif (hue > 270 and hue <= 330):hue=300
            elif (hue > 330 and hue <= 360):hue=360
            self.hsv_1_slider.Update(hue, factor360, width)
            self.layout.hsv_1_value.setValue(hue)
        elif case == "M1":
            channel = self.layout.hsv_1_value.value()
            self.hsv_1_slider.Update((channel-value),factor360,  width)
            self.layout.hsv_1_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsv_1_value.value()
            self.hsv_1_slider.Update((channel+value), factor360, width)
            self.layout.hsv_1_value.setValue(channel+value)
        elif case == "KU":
            self.hsv_1_slider.Update(value, factor360, width)
            self.layout.hsv_1_value.setValue(value)
        elif case == "HEX":
            self.hsv_1_slider.Update(value, factor360, width)
            self.layout.hsv_1_value.setValue(value)
        elif case == "SYNC":
            # ac1 = self.layout.hsv_1_value.value() / factor360
            # ac2 = self.layout.hsv_2_value.value() / factor100
            # ac3 = self.layout.hsv_3_value.value() / factor100
            # rgb = colorsys.hsv_to_rgb(ac1, ac2, ac3)
            # self.layout.rgb_1_value.setValue(rgb[0]*factor255)
            # self.layout.rgb_2_value.setValue(rgb[1]*factor255)
            # self.layout.rgb_3_value.setValue(rgb[2]*factor255)
            pass

    def Pigment_HSV_2(self, case, value):
        width = self.layout.hsv_2_slider.width()
        if case == "50":
            min = self.layout.hsv_2_value.minimum()
            max = self.layout.hsv_2_value.maximum()
            half = (max-min)/2
            self.hsv_2_slider.Update(half, factor100, width)
            self.layout.hsv_2_value.setValue(half)
        elif case == "M1":
            channel = self.layout.hsv_2_value.value()
            self.hsv_2_slider.Update((channel-value), factor100, width)
            self.layout.hsv_2_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsv_2_value.value()
            self.hsv_2_slider.Update((channel+value), factor100, width)
            self.layout.hsv_2_value.setValue(channel+value)
        elif case == "KU":
            self.hsv_2_slider.Update(value, factor100, width)
            self.layout.hsv_2_value.setValue(value)
        elif case == "HEX":
            self.hsv_2_slider.Update(value, factor100, width)
            self.layout.hsv_2_value.setValue(value)
        elif case == "SYNC":
            # ac1 = self.layout.hsv_1_value.value() / factor360
            # ac2 = self.layout.hsv_2_value.value() / factor100
            # ac3 = self.layout.hsv_3_value.value() / factor100
            # rgb = colorsys.hsv_to_rgb(ac1, ac2, ac3)
            # self.layout.rgb_1_value.setValue(rgb[0]*factor255)
            # self.layout.rgb_2_value.setValue(rgb[1]*factor255)
            # self.layout.rgb_3_value.setValue(rgb[2]*factor255)
            pass

    def Pigment_HSV_3(self, case, value):
        width = self.layout.hsv_3_slider.width()
        if case == "50":
            min = self.layout.hsv_3_value.minimum()
            max = self.layout.hsv_3_value.maximum()
            half = (max-min)/2
            self.hsv_3_slider.Update(half, factor100, width)
            self.layout.hsv_3_value.setValue(half)
        elif case == "M1":
            channel = self.layout.hsv_3_value.value()
            self.hsv_3_slider.Update((channel-value), factor100, width)
            self.layout.hsv_3_value.setValue(channel-value)
        elif case == "P1":
            channel = self.layout.hsv_3_value.value()
            self.hsv_3_slider.Update((channel+value), factor100, width)
            self.layout.hsv_3_value.setValue(channel+value)
        elif case == "KU":
            self.hsv_3_slider.Update(value, factor100, width)
            self.layout.hsv_3_value.setValue(value)
        elif case == "HEX":
            self.hsv_3_slider.Update(value, factor100, width)
            self.layout.hsv_3_value.setValue(value)
        elif case == "SYNC":
            # ac1 = self.layout.hsv_1_value.value() / factor360
            # ac2 = self.layout.hsv_2_value.value() / factor100
            # ac3 = self.layout.hsv_3_value.value() / factor100
            # rgb = colorsys.hsv_to_rgb(ac1, ac2, ac3)
            # self.layout.rgb_1_value.setValue(rgb[0]*factor255)
            # self.layout.rgb_2_value.setValue(rgb[1]*factor255)
            # self.layout.rgb_3_value.setValue(rgb[2]*factor255)
            pass

    # Widget Events
    def enterEvent(self, event):
        # Check Krita Once before edit
        self.Krita_Update()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:self.timer.stop()
        else:pass

    def leaveEvent(self, event):
        # Start Asking Krita the Current Color
        if check_timer >= 1000:self.timer.start()
        else:pass

    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:self.timer.stop()
        else:pass

    def resizeEvent(self, event):
        # Relocate Channel Handle due to Size Variation
        self.rgb_1_slider.Update(self.layout.rgb_1_value.value(), factor255, self.layout.rgb_1_slider.width())
        self.rgb_2_slider.Update(self.layout.rgb_2_value.value(), factor255, self.layout.rgb_2_slider.width())
        self.rgb_3_slider.Update(self.layout.rgb_3_value.value(), factor255, self.layout.rgb_3_slider.width())
        self.hsv_1_slider.Update(self.layout.hsv_1_value.value(), factor360, self.layout.hsv_1_slider.width())
        self.hsv_2_slider.Update(self.layout.hsv_2_value.value(), factor100, self.layout.hsv_2_slider.width())
        self.hsv_3_slider.Update(self.layout.hsv_3_value.value(), factor100, self.layout.hsv_3_slider.width())
        # Relocate Panel Cursor due to Size Variation
        # self.panel.Update(self.mode, self.layout.widget_pointer.width(), self.layout.widget_pointer.height())

    # Change the Canvas
    def canvasChanged(self, canvas):
        pass
