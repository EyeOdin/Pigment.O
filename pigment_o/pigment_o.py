# Import Krita
from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtSvg, uic
import os.path
import colorsys

from .pigment_o_style import Style
from .pigment_o_channel import Channel
from .pigment_o_mixer import Mixer_Color, Mixer_Gradient
from .pigment_o_panel import PanelHsv

# Set Window Title Name
DOCKER_NAME = "Pigment.O"
check_timer = 1000  # 1000 = 1 SECOND (Zero will Disable checks)
factor255 = 255
factor360 = 360
factor100 = 100
cmin1 = 8
cmax1 = 15
cmin2 = 5
cmax2 = 10
cmin3 = 19
cmax3 = 34
margin = 5
vspacer = 2
unit = 1
null = 0

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

        # Set Menus Display
        self.Pigment_Display(0,0,0, 0,0,0)
        self.layout.rgb.setChecked(True)
        self.Display_RGB()
        self.layout.hsv.setChecked(False)
        self.Display_HSV()
        self.layout.tts.setChecked(False)
        self.Display_TTS()
        self.layout.mix1.setChecked(False)
        self.Display_MIX1()
        self.layout.mix2.setChecked(False)
        self.Display_MIX2()

        # Panel Selection
        index = self.layout.panel_selector.findText("HSV", QtCore.Qt.MatchFixedString)
        self.layout.panel_selector.setCurrentIndex(index)

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
        self.rgb_1_slider.SIGNAL_VALUE.connect(self.layout.rgb_1_value.setValue)
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.rgb_1_slider.Update(self.layout.rgb_1_value.value(), factor255, self.layout.rgb_1_slider.width()))

        # Connect Channel Green
        self.layout.rgb_2_label.clicked.connect(lambda: self.Pigment_RGB_2("50", 0))
        self.layout.rgb_2_minus.clicked.connect(lambda: self.Pigment_RGB_2("M1", 1))
        self.layout.rgb_2_plus.clicked.connect(lambda: self.Pigment_RGB_2("P1", 1))
        self.rgb_2_slider.SIGNAL_VALUE.connect(self.layout.rgb_2_value.setValue)
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.rgb_2_slider.Update(self.layout.rgb_2_value.value(), factor255, self.layout.rgb_2_slider.width()))

        # Connect Channel Blue
        self.layout.rgb_3_label.clicked.connect(lambda: self.Pigment_RGB_3("50", 0))
        self.layout.rgb_3_minus.clicked.connect(lambda: self.Pigment_RGB_3("M1", 1))
        self.layout.rgb_3_plus.clicked.connect(lambda: self.Pigment_RGB_3("P1", 1))
        self.rgb_3_slider.SIGNAL_VALUE.connect(self.layout.rgb_3_value.setValue)
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.rgb_3_slider.Update(self.layout.rgb_3_value.value(), factor255, self.layout.rgb_3_slider.width()))

        # Connect Channel Hue
        self.layout.hsv_1_label.clicked.connect(lambda: self.Pigment_HSV_1("50", 0))
        self.layout.hsv_1_minus.clicked.connect(lambda: self.Pigment_HSV_1("M1", 1))
        self.layout.hsv_1_plus.clicked.connect(lambda: self.Pigment_HSV_1("P1", 1))
        self.hsv_1_slider.SIGNAL_VALUE.connect(self.layout.hsv_1_value.setValue)
        self.layout.hsv_1_value.valueChanged.connect(lambda: self.hsv_1_slider.Update(self.layout.hsv_1_value.value(), factor360, self.layout.hsv_1_slider.width()))

        # Connect Channel Saturation
        self.layout.hsv_2_label.clicked.connect(lambda: self.Pigment_HSV_2("50", 0))
        self.layout.hsv_2_minus.clicked.connect(lambda: self.Pigment_HSV_2("M1", 1))
        self.layout.hsv_2_plus.clicked.connect(lambda: self.Pigment_HSV_2("P1", 1))
        self.hsv_2_slider.SIGNAL_VALUE.connect(self.layout.hsv_2_value.setValue)
        self.layout.hsv_2_value.valueChanged.connect(lambda: self.hsv_2_slider.Update(self.layout.hsv_2_value.value(), factor100, self.layout.hsv_2_slider.width()))

        # Connect Channel Value
        self.layout.hsv_3_label.clicked.connect(lambda: self.Pigment_HSV_3("50", 0))
        self.layout.hsv_3_minus.clicked.connect(lambda: self.Pigment_HSV_3("M1", 1))
        self.layout.hsv_3_plus.clicked.connect(lambda: self.Pigment_HSV_3("P1", 1))
        self.hsv_3_slider.SIGNAL_VALUE.connect(self.layout.hsv_3_value.setValue)
        self.layout.hsv_3_value.valueChanged.connect(lambda: self.hsv_3_slider.Update(self.layout.hsv_3_value.value(), factor100, self.layout.hsv_3_slider.width()))

        # Active Color
        self.layout.rgb_1_value.valueChanged.connect(lambda: self.Pigment_Color("RGB"))
        self.layout.rgb_2_value.valueChanged.connect(lambda: self.Pigment_Color("RGB"))
        self.layout.rgb_3_value.valueChanged.connect(lambda: self.Pigment_Color("RGB"))
        self.layout.hsv_1_value.valueChanged.connect(lambda: self.Pigment_Color("HSV"))
        self.layout.hsv_2_value.valueChanged.connect(lambda: self.Pigment_Color("HSV"))
        self.layout.hsv_3_value.valueChanged.connect(lambda: self.Pigment_Color("HSV"))

        # Hex Input
        self.layout.hex_string.returnPressed.connect(lambda: self.HEX_Code(self.layout.hex_string.text()))

        # Percentage Gradients Display
        p4 = self.style.Percentage("4")
        p6 = self.style.Percentage("6")
        p10 = self.style.Percentage("10")
        ten = self.style.Percentage("TEN")
        self.layout.percentage_top.setStyleSheet(ten)
        self.layout.percentage_bot.setStyleSheet(ten)
        self.layout.rgb_1_tick.setStyleSheet(p4)
        self.layout.rgb_2_tick.setStyleSheet(p4)
        self.layout.rgb_3_tick.setStyleSheet(p4)
        self.layout.hsv_1_tick.setStyleSheet(p6)
        self.layout.hsv_2_tick.setStyleSheet(p4)
        self.layout.hsv_3_tick.setStyleSheet(p4)
        self.layout.percentage_1.setStyleSheet(p10)
        self.layout.percentage_2.setStyleSheet(p10)
        self.layout.percentage_3.setStyleSheet(p10)
        self.layout.percentage_4.setStyleSheet(p10)
        self.layout.percentage_5.setStyleSheet(p10)
        self.layout.percentage_6.setStyleSheet(p10)

        # Krita Update Timer
        if check_timer >= 1000:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.Krita_Update)
            self.timer.start(check_timer)
        else:
            pass

        # Options Display
        self.layout.rgb.toggled.connect(self.Display_RGB)
        self.layout.hsv.toggled.connect(self.Display_HSV)
        self.layout.tts.toggled.connect(self.Display_TTS)
        self.layout.mix1.toggled.connect(self.Display_MIX1)
        self.layout.mix2.toggled.connect(self.Display_MIX2)
        self.layout.panel_selector.currentTextChanged.connect(lambda: self.Pigment_Color("RGB"))

        # Module Panel
        self.panel_hsv = PanelHsv(self.layout.panel_hsv_fg)
        self.panel_hsv.SIGNAL_HSV_NEW.connect(self.Signal_HSV)

        # Module Mixer Colors Init
        self.mixer_neutral = Mixer_Color(self.layout.neutral)
        self.mixer_rgb_l1 = Mixer_Color(self.layout.rgb_l1)
        self.mixer_rgb_l2 = Mixer_Color(self.layout.rgb_l2)
        self.mixer_rgb_l3 = Mixer_Color(self.layout.rgb_l3)
        self.mixer_rgb_r1 = Mixer_Color(self.layout.rgb_r1)
        self.mixer_rgb_r2 = Mixer_Color(self.layout.rgb_r2)
        self.mixer_rgb_r3 = Mixer_Color(self.layout.rgb_r3)
        self.mixer_hsv_l1 = Mixer_Color(self.layout.hsv_l1)
        self.mixer_hsv_l2 = Mixer_Color(self.layout.hsv_l2)
        self.mixer_hsv_l3 = Mixer_Color(self.layout.hsv_l3)
        self.mixer_hsv_r1 = Mixer_Color(self.layout.hsv_r1)
        self.mixer_hsv_r2 = Mixer_Color(self.layout.hsv_r2)
        self.mixer_hsv_r3 = Mixer_Color(self.layout.hsv_r3)
        self.mixer_tint = Mixer_Gradient(self.layout.tint)
        self.mixer_tone = Mixer_Gradient(self.layout.tone)
        self.mixer_shade = Mixer_Gradient(self.layout.shade)
        self.mixer_rgb_g1 = Mixer_Gradient(self.layout.rgb_g1)
        self.mixer_rgb_g2 = Mixer_Gradient(self.layout.rgb_g2)
        self.mixer_rgb_g3 = Mixer_Gradient(self.layout.rgb_g3)
        self.mixer_hsv_g1 = Mixer_Gradient(self.layout.hsv_g1)
        self.mixer_hsv_g2 = Mixer_Gradient(self.layout.hsv_g2)
        self.mixer_hsv_g3 = Mixer_Gradient(self.layout.hsv_g3)
        # Mixer Color Connect
        self.mixer_neutral.SIGNAL_MIXER_COLOR.connect(self.Mixer_Neutral)
        self.mixer_rgb_l1.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_L1)
        self.mixer_rgb_l2.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_L2)
        self.mixer_rgb_l3.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_L3)
        self.mixer_rgb_r1.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_R1)
        self.mixer_rgb_r2.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_R2)
        self.mixer_rgb_r3.SIGNAL_MIXER_COLOR.connect(self.Mixer_RGB_R3)
        self.mixer_hsv_l1.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_L1)
        self.mixer_hsv_l2.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_L2)
        self.mixer_hsv_l3.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_L3)
        self.mixer_hsv_r1.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_R1)
        self.mixer_hsv_r2.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_R2)
        self.mixer_hsv_r3.SIGNAL_MIXER_COLOR.connect(self.Mixer_HSV_R3)
        self.mixer_tint.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_Tint)
        self.mixer_tone.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_Tone)
        self.mixer_shade.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_Shade)
        self.mixer_rgb_g1.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_RGB_G1)
        self.mixer_rgb_g2.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_RGB_G2)
        self.mixer_rgb_g3.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_RGB_G3)
        self.mixer_hsv_g1.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_HSV_G1)
        self.mixer_hsv_g2.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_HSV_G2)
        self.mixer_hsv_g3.SIGNAL_MIXER_CHANNEL.connect(self.Mixer_HSV_G3)
        # Inicial Mixer Color Values
        self.color_neutral = [0,0,0, 0,0,0]
        self.color_white = [255,255,255, 0,0,100]
        self.color_grey = [127,127,127, 0,0,50]
        self.color_black = [0,0,0, 0,0,0]
        self.color_rgb_l1 = [0,0,0, 0,0,0]
        self.color_rgb_l2 = [0,0,0, 0,0,0]
        self.color_rgb_l3 = [0,0,0, 0,0,0]
        self.color_rgb_r1 = [0,0,0, 0,0,0]
        self.color_rgb_r2 = [0,0,0, 0,0,0]
        self.color_rgb_r3 = [0,0,0, 0,0,0]
        self.color_hsv_l1 = [0,0,0, 0,0,0]
        self.color_hsv_l2 = [0,0,0, 0,0,0]
        self.color_hsv_l3 = [0,0,0, 0,0,0]
        self.color_hsv_r1 = [0,0,0, 0,0,0]
        self.color_hsv_r2 = [0,0,0, 0,0,0]
        self.color_hsv_r3 = [0,0,0, 0,0,0]
        self.percentage_tint = 0
        self.percentage_tone = 0
        self.percentage_shade = 0
        self.percentage_rgb_g1 = 0
        self.percentage_rgb_g2 = 0
        self.percentage_rgb_g3 = 0
        self.percentage_hsv_g1 = 0
        self.percentage_hsv_g2 = 0
        self.percentage_hsv_g3 = 0
        # Neutral Start Colors
        black = str("background-color: rgb(%f, %f, %f);" % (0, 0, 0))
        self.layout.neutral.setStyleSheet(black)
        self.layout.rgb_l1.setStyleSheet(black)
        self.layout.rgb_l2.setStyleSheet(black)
        self.layout.rgb_l3.setStyleSheet(black)
        self.layout.rgb_r1.setStyleSheet(black)
        self.layout.rgb_r2.setStyleSheet(black)
        self.layout.rgb_r3.setStyleSheet(black)
        self.layout.hsv_l1.setStyleSheet(black)
        self.layout.hsv_l2.setStyleSheet(black)
        self.layout.hsv_l3.setStyleSheet(black)
        self.layout.hsv_r1.setStyleSheet(black)
        self.layout.hsv_r2.setStyleSheet(black)
        self.layout.hsv_r3.setStyleSheet(black)
        neutral = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
        self.layout.rgb_g1.setStyleSheet(neutral)
        self.layout.rgb_g2.setStyleSheet(neutral)
        self.layout.rgb_g3.setStyleSheet(neutral)
        self.layout.hsv_g1.setStyleSheet(neutral)
        self.layout.hsv_g2.setStyleSheet(neutral)
        self.layout.hsv_g3.setStyleSheet(neutral)

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

    def Pigment_Color(self, mode):
        # Change Color
        if mode == "RGB":
            # Original
            rgb1 = self.layout.rgb_1_value.value() / factor255
            rgb2 = self.layout.rgb_2_value.value() / factor255
            rgb3 = self.layout.rgb_3_value.value() / factor255
            # Convert to HSV
            hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
            hsv1 = hsv[0]
            hsv2 = hsv[1]
            hsv3 = hsv[2]
        if mode == "HSV":
            # Original
            hsv1 = self.layout.hsv_1_value.value() / factor360
            hsv2 = self.layout.hsv_2_value.value() / factor100
            hsv3 = self.layout.hsv_3_value.value() / factor100
            # Convert to RGB
            rgb = colorsys.hsv_to_rgb(hsv1, hsv2, hsv3)
            rgb1 = rgb[0]
            rgb2 = rgb[1]
            rgb3 = rgb[2]
        # Pigment Update Values
        self.Pigment_Sync(mode, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)
        self.Pigment_2_Krita(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)
        self.Pigment_Display(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Pigment_Sync(self, mode, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        if mode == "RGB":
            # Block Signals
            self.layout.hsv_1_value.blockSignals(True)
            self.layout.hsv_2_value.blockSignals(True)
            self.layout.hsv_3_value.blockSignals(True)
            self.layout.hsv_1_slider.blockSignals(True)
            self.layout.hsv_2_slider.blockSignals(True)
            self.layout.hsv_3_slider.blockSignals(True)
            # Set Values
            self.layout.hsv_1_value.setValue(hsv1 * factor360)
            self.layout.hsv_2_value.setValue(hsv2 * factor100)
            self.layout.hsv_3_value.setValue(hsv3 * factor100)
            self.hsv_1_slider.Update(hsv1 * factor360, factor360, self.layout.hsv_1_slider.width())
            self.hsv_2_slider.Update(hsv2 * factor100, factor100, self.layout.hsv_2_slider.width())
            self.hsv_3_slider.Update(hsv3 * factor100, factor100, self.layout.hsv_3_slider.width())
            self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.layout.hex_string.text())
            # UnBlock Signals
            self.layout.hsv_1_value.blockSignals(False)
            self.layout.hsv_2_value.blockSignals(False)
            self.layout.hsv_3_value.blockSignals(False)
            self.layout.hsv_1_slider.blockSignals(False)
            self.layout.hsv_2_slider.blockSignals(False)
            self.layout.hsv_3_slider.blockSignals(False)
        elif mode == "HSV":
            # Block Signals
            self.layout.rgb_1_value.blockSignals(True)
            self.layout.rgb_2_value.blockSignals(True)
            self.layout.rgb_3_value.blockSignals(True)
            self.layout.rgb_1_slider.blockSignals(True)
            self.layout.rgb_2_slider.blockSignals(True)
            self.layout.rgb_3_slider.blockSignals(True)
            # Set Values
            self.layout.rgb_1_value.setValue(rgb1 * factor255)
            self.layout.rgb_2_value.setValue(rgb2 * factor255)
            self.layout.rgb_3_value.setValue(rgb3 * factor255)
            self.rgb_1_slider.Update(rgb1 * factor255, factor255, self.layout.rgb_1_slider.width())
            self.rgb_2_slider.Update(rgb2 * factor255, factor255, self.layout.rgb_2_slider.width())
            self.rgb_3_slider.Update(rgb3 * factor255, factor255, self.layout.rgb_3_slider.width())
            self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.layout.hex_string.text())
            # UnBlock Signals
            self.layout.rgb_1_value.blockSignals(False)
            self.layout.rgb_2_value.blockSignals(False)
            self.layout.rgb_3_value.blockSignals(False)
            self.layout.rgb_1_slider.blockSignals(False)
            self.layout.rgb_2_slider.blockSignals(False)
            self.layout.rgb_3_slider.blockSignals(False)
        elif mode == "MIX":
            # Block Signals
            self.layout.rgb_1_value.blockSignals(True)
            self.layout.rgb_2_value.blockSignals(True)
            self.layout.rgb_3_value.blockSignals(True)
            self.layout.rgb_1_slider.blockSignals(True)
            self.layout.rgb_2_slider.blockSignals(True)
            self.layout.rgb_3_slider.blockSignals(True)
            self.layout.hsv_1_value.blockSignals(True)
            self.layout.hsv_2_value.blockSignals(True)
            self.layout.hsv_3_value.blockSignals(True)
            self.layout.hsv_1_slider.blockSignals(True)
            self.layout.hsv_2_slider.blockSignals(True)
            self.layout.hsv_3_slider.blockSignals(True)
            # Set Values
            self.layout.rgb_1_value.setValue(rgb1 * factor255)
            self.layout.rgb_2_value.setValue(rgb2 * factor255)
            self.layout.rgb_3_value.setValue(rgb3 * factor255)
            self.rgb_1_slider.Update(rgb1 * factor255, factor255, self.layout.rgb_1_slider.width())
            self.rgb_2_slider.Update(rgb2 * factor255, factor255, self.layout.rgb_2_slider.width())
            self.rgb_3_slider.Update(rgb3 * factor255, factor255, self.layout.rgb_3_slider.width())
            self.layout.hsv_1_value.setValue(hsv1 * factor360)
            self.layout.hsv_2_value.setValue(hsv2 * factor100)
            self.layout.hsv_3_value.setValue(hsv3 * factor100)
            self.hsv_1_slider.Update(hsv1 * factor360, factor360, self.layout.hsv_1_slider.width())
            self.hsv_2_slider.Update(hsv2 * factor100, factor100, self.layout.hsv_2_slider.width())
            self.hsv_3_slider.Update(hsv3 * factor100, factor100, self.layout.hsv_3_slider.width())
            self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.layout.hex_string.text())
            # UnBlock Signals
            self.layout.rgb_1_value.blockSignals(False)
            self.layout.rgb_2_value.blockSignals(False)
            self.layout.rgb_3_value.blockSignals(False)
            self.layout.rgb_1_slider.blockSignals(False)
            self.layout.rgb_2_slider.blockSignals(False)
            self.layout.rgb_3_slider.blockSignals(False)
            self.layout.hsv_1_value.blockSignals(False)
            self.layout.hsv_2_value.blockSignals(False)
            self.layout.hsv_3_value.blockSignals(False)
            self.layout.hsv_1_slider.blockSignals(False)
            self.layout.hsv_2_slider.blockSignals(False)
            self.layout.hsv_3_slider.blockSignals(False)

    def Pigment_2_Krita(self, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        # Check if there is a valid Document Active
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            # Set Krita Foreground Color
            doc = self.Document_Profile()
            if doc[0] == "A":
                pass
            elif doc[0] == "RGBA": # The actual order of channels is most often BGR
                # Apply Color to Krita in RGB (This nullifies the Eraser if it is ON)
                pigment_color = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
                pigment_color.setComponents([rgb3, rgb2, rgb1, 1.0])
                Application.activeWindow().activeView().setForeGroundColor(pigment_color)
                # If Eraser, set it ON again
                if kritaEraserAction.isChecked():
                    kritaEraserAction.trigger()
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

    def Pigment_Display(self, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        # Foreground Color Display (Top Left)
        active_color_1 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (rgb1*255, rgb2*255, rgb3*255))
        self.layout.color_1.setStyleSheet(active_color_1)
        active_color_2 = str("QWidget { background-color: rgb(%f, %f, %f);}" % (rgb1*255, rgb2*255, rgb3*255))
        self.layout.color_2.setStyleSheet(active_color_2)
        # Slider Gradients (Top Center)
        sss_rgb1 = str(self.style.Slider("RGB", 0, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3))
        sss_rgb2 = str(self.style.Slider("RGB", 1, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3))
        sss_rgb3 = str(self.style.Slider("RGB", 2, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3))
        sss_hsv1 = str(self.style.Slider("HSV", 0, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3))
        sss_hsv2 = str(self.style.Slider("HSV", 1, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3))
        sss_hsv3 = str(self.style.Slider("HSV", 2, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3))
        self.layout.rgb_1_slider.setStyleSheet(sss_rgb1)
        self.layout.rgb_2_slider.setStyleSheet(sss_rgb2)
        self.layout.rgb_3_slider.setStyleSheet(sss_rgb3)
        self.layout.hsv_1_slider.setStyleSheet(sss_hsv1)
        self.layout.hsv_2_slider.setStyleSheet(sss_hsv2)
        self.layout.hsv_3_slider.setStyleSheet(sss_hsv3)
        # Panel Display
        panel = self.layout.panel_selector.currentText()
        if panel == "NIL":
            # Colors for HSV Square Background Gradients
            base_color = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsv_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: rgba(0, 0, 0, 0); }")
            self.layout.panel_hsv_fg.setStyleSheet(base_value)
        elif panel == "HSV":
            # Colors for HSV Square Background Gradients
            hue = hsv1 * 360
            if hue == 360:
                hue = 1
            base_color = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ffffff, stop:1 hsl(%f, %f, %f)); }" % (hue, 255, 255))
            self.layout.panel_hsv_bg.setStyleSheet(base_color)
            base_value = str("QWidget { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 255)); }")
            self.layout.panel_hsv_fg.setStyleSheet(base_value)
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

    def Krita_Update(self):
        # Consider if nothing is on the Canvas
        if ((self.canvas() is not None) and (self.canvas().view() is not None)):
            # Check Eraser Mode ON or OFF
            kritaEraserAction = Application.action("erase_action")
            # Pigment Values
            rgb1 = self.layout.rgb_1_value.value() / factor255
            rgb2 = self.layout.rgb_2_value.value() / factor255
            rgb3 = self.layout.rgb_3_value.value() / factor255
            hsv1 = self.layout.hsv_1_value.value() / factor360
            hsv2 = self.layout.hsv_2_value.value() / factor100
            hsv3 = self.layout.hsv_3_value.value() / factor100
            # Document Profile
            doc = self.Document_Profile()
            color_foreground = ManagedColor(str(doc[0]), str(doc[1]), str(doc[2]))
            color_foreground = Application.activeWindow().activeView().foregroundColor()
            color_background = Application.activeWindow().activeView().backgroundColor()
            components_fg = color_foreground.components()
            components_bg = color_background.components()
            # Krita Current Foreground Color RGB
            if doc[0] == "RGBA":
                kac1 = components_fg[2]
                kac2 = components_fg[1]
                kac3 = components_fg[0]
                kbc1 = components_bg[2]
                kbc2 = components_bg[1]
                kbc3 = components_bg[0]
            else:
                kac1 = components_fg[0]
                kac2 = components_fg[1]
                kac3 = components_fg[2]
                kbc1 = components_bg[0]
                kbc2 = components_bg[1]
                kbc3 = components_bg[2]
            # Update Pigmento if Values Differ
            if doc[0] == "A":
                pass
            elif doc[0] == "RGBA":
                if (rgb1 != kac1 or rgb2 != kac2 or rgb3 != kac3):
                    if not kritaEraserAction.isChecked():
                        r = kac1 * factor255
                        g = kac2 * factor255
                        b = kac3 * factor255
                        self.Pigment_RGB_1("KU", r)
                        self.Pigment_RGB_2("KU", g)
                        self.Pigment_RGB_3("KU", b)
                        self.Pigment_Color("RGB")
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

    def Signal_HSV(self, SIGNAL_HSV):
        self.layout.hsv_2_value.setValue(round(SIGNAL_HSV[0], 2))
        self.layout.hsv_3_value.setValue(round(SIGNAL_HSV[1], 2))

    # Menu Displays
    def Display_RGB(self):
        if self.layout.rgb.isChecked():
            self.layout.rgb.setText("RGB")
            self.layout.rgb_1_label.setMinimumHeight(cmin1)
            self.layout.rgb_1_label.setMaximumHeight(cmax1)
            self.layout.rgb_1_minus.setMinimumHeight(cmin1)
            self.layout.rgb_1_minus.setMaximumHeight(cmax1)
            self.layout.rgb_1_slider.setMinimumHeight(cmin1)
            self.layout.rgb_1_slider.setMaximumHeight(cmax1)
            self.layout.rgb_1_plus.setMinimumHeight(cmin1)
            self.layout.rgb_1_plus.setMaximumHeight(cmax1)
            self.layout.rgb_1_value.setMinimumHeight(cmin1)
            self.layout.rgb_1_value.setMaximumHeight(cmax1)
            self.layout.rgb_1_tick.setMinimumHeight(unit)
            self.layout.rgb_2_label.setMinimumHeight(cmin1)
            self.layout.rgb_2_label.setMaximumHeight(cmax1)
            self.layout.rgb_2_minus.setMinimumHeight(cmin1)
            self.layout.rgb_2_minus.setMaximumHeight(cmax1)
            self.layout.rgb_2_slider.setMinimumHeight(cmin1)
            self.layout.rgb_2_slider.setMaximumHeight(cmax1)
            self.layout.rgb_2_plus.setMinimumHeight(cmin1)
            self.layout.rgb_2_plus.setMaximumHeight(cmax1)
            self.layout.rgb_2_value.setMinimumHeight(cmin1)
            self.layout.rgb_2_value.setMaximumHeight(cmax1)
            self.layout.rgb_2_tick.setMinimumHeight(unit)
            self.layout.rgb_3_label.setMinimumHeight(cmin1)
            self.layout.rgb_3_label.setMaximumHeight(cmax1)
            self.layout.rgb_3_minus.setMinimumHeight(cmin1)
            self.layout.rgb_3_minus.setMaximumHeight(cmax1)
            self.layout.rgb_3_slider.setMinimumHeight(cmin1)
            self.layout.rgb_3_slider.setMaximumHeight(cmax1)
            self.layout.rgb_3_plus.setMinimumHeight(cmin1)
            self.layout.rgb_3_plus.setMaximumHeight(cmax1)
            self.layout.rgb_3_value.setMinimumHeight(cmin1)
            self.layout.rgb_3_value.setMaximumHeight(cmax1)
            self.layout.rgb_3_tick.setMinimumHeight(unit)
            # Place Percentage Style
            if (self.layout.rgb.isChecked() == True or self.layout.hsv.isChecked() == True ):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            self.layout.rgb.setText("rgb")
            self.layout.rgb_1_label.setMinimumHeight(null)
            self.layout.rgb_1_label.setMaximumHeight(null)
            self.layout.rgb_1_minus.setMinimumHeight(null)
            self.layout.rgb_1_minus.setMaximumHeight(null)
            self.layout.rgb_1_slider.setMinimumHeight(null)
            self.layout.rgb_1_slider.setMaximumHeight(null)
            self.layout.rgb_1_plus.setMinimumHeight(null)
            self.layout.rgb_1_plus.setMaximumHeight(null)
            self.layout.rgb_1_value.setMinimumHeight(null)
            self.layout.rgb_1_value.setMaximumHeight(null)
            self.layout.rgb_1_tick.setMinimumHeight(null)
            self.layout.rgb_2_label.setMinimumHeight(null)
            self.layout.rgb_2_label.setMaximumHeight(null)
            self.layout.rgb_2_minus.setMinimumHeight(null)
            self.layout.rgb_2_minus.setMaximumHeight(null)
            self.layout.rgb_2_slider.setMinimumHeight(null)
            self.layout.rgb_2_slider.setMaximumHeight(null)
            self.layout.rgb_2_plus.setMinimumHeight(null)
            self.layout.rgb_2_plus.setMaximumHeight(null)
            self.layout.rgb_2_value.setMinimumHeight(null)
            self.layout.rgb_2_value.setMaximumHeight(null)
            self.layout.rgb_2_tick.setMinimumHeight(null)
            self.layout.rgb_3_label.setMinimumHeight(null)
            self.layout.rgb_3_label.setMaximumHeight(null)
            self.layout.rgb_3_minus.setMinimumHeight(null)
            self.layout.rgb_3_minus.setMaximumHeight(null)
            self.layout.rgb_3_slider.setMinimumHeight(null)
            self.layout.rgb_3_slider.setMaximumHeight(null)
            self.layout.rgb_3_plus.setMinimumHeight(null)
            self.layout.rgb_3_plus.setMaximumHeight(null)
            self.layout.rgb_3_value.setMinimumHeight(null)
            self.layout.rgb_3_value.setMaximumHeight(null)
            self.layout.rgb_3_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.rgb.isChecked() == False and self.layout.hsv.isChecked() == False ):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)

    def Display_HSV(self):
        if self.layout.hsv.isChecked():
            self.layout.hsv.setText("HSV")
            self.layout.hsv_1_label.setMinimumHeight(cmin1)
            self.layout.hsv_1_label.setMaximumHeight(cmax1)
            self.layout.hsv_1_minus.setMinimumHeight(cmin1)
            self.layout.hsv_1_minus.setMaximumHeight(cmax1)
            self.layout.hsv_1_slider.setMinimumHeight(cmin1)
            self.layout.hsv_1_slider.setMaximumHeight(cmax1)
            self.layout.hsv_1_plus.setMinimumHeight(cmin1)
            self.layout.hsv_1_plus.setMaximumHeight(cmax1)
            self.layout.hsv_1_value.setMinimumHeight(cmin1)
            self.layout.hsv_1_value.setMaximumHeight(cmax1)
            self.layout.hsv_1_tick.setMinimumHeight(unit)
            self.layout.hsv_2_label.setMinimumHeight(cmin1)
            self.layout.hsv_2_label.setMaximumHeight(cmax1)
            self.layout.hsv_2_minus.setMinimumHeight(cmin1)
            self.layout.hsv_2_minus.setMaximumHeight(cmax1)
            self.layout.hsv_2_slider.setMinimumHeight(cmin1)
            self.layout.hsv_2_slider.setMaximumHeight(cmax1)
            self.layout.hsv_2_plus.setMinimumHeight(cmin1)
            self.layout.hsv_2_plus.setMaximumHeight(cmax1)
            self.layout.hsv_2_value.setMinimumHeight(cmin1)
            self.layout.hsv_2_value.setMaximumHeight(cmax1)
            self.layout.hsv_2_tick.setMinimumHeight(unit)
            self.layout.hsv_3_label.setMinimumHeight(cmin1)
            self.layout.hsv_3_label.setMaximumHeight(cmax1)
            self.layout.hsv_3_minus.setMinimumHeight(cmin1)
            self.layout.hsv_3_minus.setMaximumHeight(cmax1)
            self.layout.hsv_3_slider.setMinimumHeight(cmin1)
            self.layout.hsv_3_slider.setMaximumHeight(cmax1)
            self.layout.hsv_3_plus.setMinimumHeight(cmin1)
            self.layout.hsv_3_plus.setMaximumHeight(cmax1)
            self.layout.hsv_3_value.setMinimumHeight(cmin1)
            self.layout.hsv_3_value.setMaximumHeight(cmax1)
            self.layout.hsv_3_tick.setMinimumHeight(unit)
            # Place Percetage Style
            if (self.layout.rgb.isChecked() == True or self.layout.hsv.isChecked() == True ):
                ten = self.style.Percentage("TEN")
                self.layout.percentage_top.setStyleSheet(ten)
                self.layout.percentage_bot.setStyleSheet(ten)
        else:
            self.layout.hsv.setText("hsv")
            self.layout.hsv_1_label.setMinimumHeight(null)
            self.layout.hsv_1_label.setMaximumHeight(null)
            self.layout.hsv_1_minus.setMinimumHeight(null)
            self.layout.hsv_1_minus.setMaximumHeight(null)
            self.layout.hsv_1_slider.setMinimumHeight(null)
            self.layout.hsv_1_slider.setMaximumHeight(null)
            self.layout.hsv_1_plus.setMinimumHeight(null)
            self.layout.hsv_1_plus.setMaximumHeight(null)
            self.layout.hsv_1_value.setMinimumHeight(null)
            self.layout.hsv_1_value.setMaximumHeight(null)
            self.layout.hsv_1_tick.setMinimumHeight(null)
            self.layout.hsv_2_label.setMinimumHeight(null)
            self.layout.hsv_2_label.setMaximumHeight(null)
            self.layout.hsv_2_minus.setMinimumHeight(null)
            self.layout.hsv_2_minus.setMaximumHeight(null)
            self.layout.hsv_2_slider.setMinimumHeight(null)
            self.layout.hsv_2_slider.setMaximumHeight(null)
            self.layout.hsv_2_plus.setMinimumHeight(null)
            self.layout.hsv_2_plus.setMaximumHeight(null)
            self.layout.hsv_2_value.setMinimumHeight(null)
            self.layout.hsv_2_value.setMaximumHeight(null)
            self.layout.hsv_2_tick.setMinimumHeight(null)
            self.layout.hsv_3_label.setMinimumHeight(null)
            self.layout.hsv_3_label.setMaximumHeight(null)
            self.layout.hsv_3_minus.setMinimumHeight(null)
            self.layout.hsv_3_minus.setMaximumHeight(null)
            self.layout.hsv_3_slider.setMinimumHeight(null)
            self.layout.hsv_3_slider.setMaximumHeight(null)
            self.layout.hsv_3_plus.setMinimumHeight(null)
            self.layout.hsv_3_plus.setMaximumHeight(null)
            self.layout.hsv_3_value.setMinimumHeight(null)
            self.layout.hsv_3_value.setMaximumHeight(null)
            self.layout.hsv_3_tick.setMinimumHeight(null)
            # Remove Percentage Style
            if (self.layout.rgb.isChecked() == False and self.layout.hsv.isChecked() == False ):
                alpha = self.style.Alpha()
                self.layout.percentage_top.setStyleSheet(alpha)
                self.layout.percentage_bot.setStyleSheet(alpha)

    def Display_TTS(self):
        if self.layout.tts.isChecked():
            self.layout.tts.setText("TTS")
            self.layout.neutral.setMinimumHeight(cmin3)
            self.layout.neutral.setMaximumHeight(cmax3)
            self.layout.tint.setMinimumHeight(cmin2)
            self.layout.tint.setMaximumHeight(cmax2)
            self.layout.tone.setMinimumHeight(cmin2)
            self.layout.tone.setMaximumHeight(cmax2)
            self.layout.shade.setMinimumHeight(cmin2)
            self.layout.shade.setMaximumHeight(cmax2)
            self.layout.white.setMinimumHeight(cmin2)
            self.layout.white.setMaximumHeight(cmax2)
            self.layout.grey.setMinimumHeight(cmin2)
            self.layout.grey.setMaximumHeight(cmax2)
            self.layout.black.setMinimumHeight(cmin2)
            self.layout.black.setMaximumHeight(cmax2)
            self.layout.spacer_tts_1.setMinimumHeight(cmin2)
            self.layout.spacer_tts_1.setMaximumHeight(cmax2)
            self.layout.spacer_tts_2.setMinimumHeight(cmin2)
            self.layout.spacer_tts_2.setMaximumHeight(cmax2)
            self.layout.spacer_tts_3.setMinimumHeight(cmin2)
            self.layout.spacer_tts_3.setMaximumHeight(cmax2)
            self.layout.spacer_tts_4.setMinimumHeight(cmin2)
            self.layout.spacer_tts_4.setMaximumHeight(cmax2)
            self.layout.percentage_1.setMinimumHeight(vspacer)
            self.layout.percentage_1.setMaximumHeight(vspacer)
            self.layout.percentage_2.setMinimumHeight(vspacer)
            self.layout.percentage_2.setMaximumHeight(vspacer)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, margin)
        else:
            self.layout.tts.setText("tts")
            self.layout.neutral.setMinimumHeight(null)
            self.layout.neutral.setMaximumHeight(null)
            self.layout.tint.setMinimumHeight(null)
            self.layout.tint.setMaximumHeight(null)
            self.layout.tone.setMinimumHeight(null)
            self.layout.tone.setMaximumHeight(null)
            self.layout.shade.setMinimumHeight(null)
            self.layout.shade.setMaximumHeight(null)
            self.layout.white.setMinimumHeight(null)
            self.layout.white.setMaximumHeight(null)
            self.layout.grey.setMinimumHeight(null)
            self.layout.grey.setMaximumHeight(null)
            self.layout.black.setMinimumHeight(null)
            self.layout.black.setMaximumHeight(null)
            self.layout.spacer_tts_1.setMinimumHeight(null)
            self.layout.spacer_tts_1.setMaximumHeight(null)
            self.layout.spacer_tts_2.setMinimumHeight(null)
            self.layout.spacer_tts_2.setMaximumHeight(null)
            self.layout.spacer_tts_3.setMinimumHeight(null)
            self.layout.spacer_tts_3.setMaximumHeight(null)
            self.layout.spacer_tts_4.setMinimumHeight(null)
            self.layout.spacer_tts_4.setMaximumHeight(null)
            self.layout.percentage_1.setMinimumHeight(null)
            self.layout.percentage_1.setMaximumHeight(null)
            self.layout.percentage_2.setMinimumHeight(null)
            self.layout.percentage_2.setMaximumHeight(null)
            self.layout.tint_tone_shade.setContentsMargins(0, 0, 0, null)

    def Display_MIX1(self):
        if self.layout.mix1.isChecked():
            self.layout.mix1.setText("MIX1")
            self.layout.rgb_l1.setMinimumHeight(cmin2)
            self.layout.rgb_l1.setMaximumHeight(cmax2)
            self.layout.rgb_l2.setMinimumHeight(cmin2)
            self.layout.rgb_l2.setMaximumHeight(cmax2)
            self.layout.rgb_l3.setMinimumHeight(cmin2)
            self.layout.rgb_l3.setMaximumHeight(cmax2)
            self.layout.rgb_r1.setMinimumHeight(cmin2)
            self.layout.rgb_r1.setMaximumHeight(cmax2)
            self.layout.rgb_r2.setMinimumHeight(cmin2)
            self.layout.rgb_r2.setMaximumHeight(cmax2)
            self.layout.rgb_r3.setMinimumHeight(cmin2)
            self.layout.rgb_r3.setMaximumHeight(cmax2)
            self.layout.rgb_g1.setMinimumHeight(cmin2)
            self.layout.rgb_g1.setMaximumHeight(cmax2)
            self.layout.rgb_g2.setMinimumHeight(cmin2)
            self.layout.rgb_g2.setMaximumHeight(cmax2)
            self.layout.rgb_g3.setMinimumHeight(cmin2)
            self.layout.rgb_g3.setMaximumHeight(cmax2)
            self.layout.spacer_mix1_1.setMinimumHeight(cmin2)
            self.layout.spacer_mix1_1.setMaximumHeight(cmax2)
            self.layout.spacer_mix1_2.setMinimumHeight(cmin2)
            self.layout.spacer_mix1_2.setMaximumHeight(cmax2)
            self.layout.spacer_mix1_3.setMinimumHeight(cmin2)
            self.layout.spacer_mix1_3.setMaximumHeight(cmax2)
            self.layout.spacer_mix1_4.setMinimumHeight(cmin2)
            self.layout.spacer_mix1_4.setMaximumHeight(cmax2)
            self.layout.percentage_3.setMinimumHeight(vspacer)
            self.layout.percentage_3.setMaximumHeight(vspacer)
            self.layout.percentage_4.setMinimumHeight(vspacer)
            self.layout.percentage_4.setMaximumHeight(vspacer)
            self.layout.mixer_1.setContentsMargins(0, 0, 0, margin)
        else:
            self.layout.mix1.setText("mix1")
            self.layout.rgb_l1.setMinimumHeight(null)
            self.layout.rgb_l1.setMaximumHeight(null)
            self.layout.rgb_l2.setMinimumHeight(null)
            self.layout.rgb_l2.setMaximumHeight(null)
            self.layout.rgb_l3.setMinimumHeight(null)
            self.layout.rgb_l3.setMaximumHeight(null)
            self.layout.rgb_r1.setMinimumHeight(null)
            self.layout.rgb_r1.setMaximumHeight(null)
            self.layout.rgb_r2.setMinimumHeight(null)
            self.layout.rgb_r2.setMaximumHeight(null)
            self.layout.rgb_r3.setMinimumHeight(null)
            self.layout.rgb_r3.setMaximumHeight(null)
            self.layout.rgb_g1.setMinimumHeight(null)
            self.layout.rgb_g1.setMaximumHeight(null)
            self.layout.rgb_g2.setMinimumHeight(null)
            self.layout.rgb_g2.setMaximumHeight(null)
            self.layout.rgb_g3.setMinimumHeight(null)
            self.layout.rgb_g3.setMaximumHeight(null)
            self.layout.spacer_mix1_1.setMinimumHeight(null)
            self.layout.spacer_mix1_1.setMaximumHeight(null)
            self.layout.spacer_mix1_2.setMinimumHeight(null)
            self.layout.spacer_mix1_2.setMaximumHeight(null)
            self.layout.spacer_mix1_3.setMinimumHeight(null)
            self.layout.spacer_mix1_3.setMaximumHeight(null)
            self.layout.spacer_mix1_4.setMinimumHeight(null)
            self.layout.spacer_mix1_4.setMaximumHeight(null)
            self.layout.percentage_3.setMinimumHeight(null)
            self.layout.percentage_3.setMaximumHeight(null)
            self.layout.percentage_4.setMinimumHeight(null)
            self.layout.percentage_4.setMaximumHeight(null)
            self.layout.mixer_1.setContentsMargins(0, 0, 0, null)

    def Display_MIX2(self):
        if self.layout.mix2.isChecked():
            self.layout.mix2.setText("MIX2")
            self.layout.hsv_l1.setMinimumHeight(cmin2)
            self.layout.hsv_l1.setMaximumHeight(cmax2)
            self.layout.hsv_l2.setMinimumHeight(cmin2)
            self.layout.hsv_l2.setMaximumHeight(cmax2)
            self.layout.hsv_l3.setMinimumHeight(cmin2)
            self.layout.hsv_l3.setMaximumHeight(cmax2)
            self.layout.hsv_r1.setMinimumHeight(cmin2)
            self.layout.hsv_r1.setMaximumHeight(cmax2)
            self.layout.hsv_r2.setMinimumHeight(cmin2)
            self.layout.hsv_r2.setMaximumHeight(cmax2)
            self.layout.hsv_r3.setMinimumHeight(cmin2)
            self.layout.hsv_r3.setMaximumHeight(cmax2)
            self.layout.hsv_g1.setMinimumHeight(cmin2)
            self.layout.hsv_g1.setMaximumHeight(cmax2)
            self.layout.hsv_g2.setMinimumHeight(cmin2)
            self.layout.hsv_g2.setMaximumHeight(cmax2)
            self.layout.hsv_g3.setMinimumHeight(cmin2)
            self.layout.hsv_g3.setMaximumHeight(cmax2)
            self.layout.spacer_mix2_1.setMinimumHeight(cmin2)
            self.layout.spacer_mix2_1.setMaximumHeight(cmax2)
            self.layout.spacer_mix2_2.setMinimumHeight(cmin2)
            self.layout.spacer_mix2_2.setMaximumHeight(cmax2)
            self.layout.spacer_mix2_3.setMinimumHeight(cmin2)
            self.layout.spacer_mix2_3.setMaximumHeight(cmax2)
            self.layout.spacer_mix2_4.setMinimumHeight(cmin2)
            self.layout.spacer_mix2_4.setMaximumHeight(cmax2)
            self.layout.percentage_5.setMinimumHeight(vspacer)
            self.layout.percentage_5.setMaximumHeight(vspacer)
            self.layout.percentage_6.setMinimumHeight(vspacer)
            self.layout.percentage_6.setMaximumHeight(vspacer)
            self.layout.mixer_2.setContentsMargins(0, 0, 0, margin)
        else:
            self.layout.mix2.setText("mix2")
            self.layout.hsv_l1.setMinimumHeight(null)
            self.layout.hsv_l1.setMaximumHeight(null)
            self.layout.hsv_l2.setMinimumHeight(null)
            self.layout.hsv_l2.setMaximumHeight(null)
            self.layout.hsv_l3.setMinimumHeight(null)
            self.layout.hsv_l3.setMaximumHeight(null)
            self.layout.hsv_r1.setMinimumHeight(null)
            self.layout.hsv_r1.setMaximumHeight(null)
            self.layout.hsv_r2.setMinimumHeight(null)
            self.layout.hsv_r2.setMaximumHeight(null)
            self.layout.hsv_r3.setMinimumHeight(null)
            self.layout.hsv_r3.setMaximumHeight(null)
            self.layout.hsv_g1.setMinimumHeight(null)
            self.layout.hsv_g1.setMaximumHeight(null)
            self.layout.hsv_g2.setMinimumHeight(null)
            self.layout.hsv_g2.setMaximumHeight(null)
            self.layout.hsv_g3.setMinimumHeight(null)
            self.layout.hsv_g3.setMaximumHeight(null)
            self.layout.spacer_mix2_1.setMinimumHeight(null)
            self.layout.spacer_mix2_1.setMaximumHeight(null)
            self.layout.spacer_mix2_2.setMinimumHeight(null)
            self.layout.spacer_mix2_2.setMaximumHeight(null)
            self.layout.spacer_mix2_3.setMinimumHeight(null)
            self.layout.spacer_mix2_3.setMaximumHeight(null)
            self.layout.spacer_mix2_4.setMinimumHeight(null)
            self.layout.spacer_mix2_4.setMaximumHeight(null)
            self.layout.percentage_5.setMinimumHeight(null)
            self.layout.percentage_5.setMaximumHeight(null)
            self.layout.percentage_6.setMinimumHeight(null)
            self.layout.percentage_6.setMaximumHeight(null)
            self.layout.mixer_2.setContentsMargins(0, 0, 0, null)

    # Pigment Color
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

    def Pigment_HSV_1(self, case, value):
        width = self.layout.hsv_1_slider.width()
        if case == "50":
            hue = self.layout.hsv_1_value.value()
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
            self.hsv_1_slider.Update(hue, factor360, width)
            self.layout.hsv_1_value.setValue(hue)
        elif case == "M1":
            channel = self.layout.hsv_1_value.value()
            self.hsv_1_slider.Update((channel-value), factor360,  width)
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

    # Mixer Colors
    def Mixer_Neutral(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_neutral = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_neutral[0], self.color_neutral[1], self.color_neutral[2]))
            white = str("background-color: rgb(%f, %f, %f);" % (self.color_white[0], self.color_white[1], self.color_white[2]))
            grey = str("background-color: rgb(%f, %f, %f);" % (self.color_grey[0], self.color_grey[1], self.color_grey[2]))
            black = str("background-color: rgb(%f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2]))
            self.layout.neutral.setStyleSheet(color)
            self.layout.white.setStyleSheet(white)
            self.layout.grey.setStyleSheet(grey)
            self.layout.black.setStyleSheet(black)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_neutral = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.neutral.setStyleSheet(black)
            self.layout.white.setStyleSheet(alpha)
            self.layout.grey.setStyleSheet(alpha)
            self.layout.black.setStyleSheet(alpha)
            self.layout.tint.setStyleSheet(alpha)
            self.layout.tone.setStyleSheet(alpha)
            self.layout.shade.setStyleSheet(alpha)
            # Correct Values
            self.percentage_tint = 0
            self.percentage_tone = 0
            self.percentage_shade = 0
            self.mixer_tint.Update(self.percentage_tint, self.layout.tint.width())
            self.mixer_tone.Update(self.percentage_tone, self.layout.tone.width())
            self.mixer_shade.Update(self.percentage_shade, self.layout.shade.width())

    def Mixer_RGB_L1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_l1 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_rgb_l1[0], self.color_rgb_l1[1], self.color_rgb_l1[2]))
            self.layout.rgb_l1.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_rgb_l1 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.rgb_l1.setStyleSheet(black)
            self.layout.rgb_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g1 = 0
            self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())

    def Mixer_RGB_L2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_l2 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_rgb_l2[0], self.color_rgb_l2[1], self.color_rgb_l2[2]))
            self.layout.rgb_l2.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_rgb_l2 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.rgb_l2.setStyleSheet(black)
            self.layout.rgb_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g2 = 0
            self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())

    def Mixer_RGB_L3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_l3 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_rgb_l3[0], self.color_rgb_l3[1], self.color_rgb_l3[2]))
            self.layout.rgb_l3.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_rgb_l3 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.rgb_l3.setStyleSheet(black)
            self.layout.rgb_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g3 = 0
            self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_RGB_R1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_r1 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_rgb_r1[0], self.color_rgb_r1[1], self.color_rgb_r1[2]))
            self.layout.rgb_r1.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_rgb_r1 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.rgb_r1.setStyleSheet(black)
            self.layout.rgb_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g1 = 0
            self.mixer_rgb_g1.Update(self.percentage_rgb_g1, self.layout.rgb_g1.width())

    def Mixer_RGB_R2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_r2 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_rgb_r2[0], self.color_rgb_r2[1], self.color_rgb_r2[2]))
            self.layout.rgb_r2.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_rgb_r2 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.rgb_r2.setStyleSheet(black)
            self.layout.rgb_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g2 = 0
            self.mixer_rgb_g2.Update(self.percentage_rgb_g2, self.layout.rgb_g2.width())

    def Mixer_RGB_R3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_rgb_r3 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_rgb_r3[0], self.color_rgb_r3[1], self.color_rgb_r3[2]))
            self.layout.rgb_r3.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_rgb_r3 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.rgb_r3.setStyleSheet(black)
            self.layout.rgb_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_rgb_g3 = 0
            self.mixer_rgb_g3.Update(self.percentage_rgb_g3, self.layout.rgb_g3.width())

    def Mixer_HSV_L1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_l1 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_hsv_l1[0], self.color_hsv_l1[1], self.color_hsv_l1[2]))
            self.layout.hsv_l1.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_hsv_l1 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.hsv_l1.setStyleSheet(black)
            self.layout.hsv_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g1 = 0
            self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_L2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_l2 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_hsv_l2[0], self.color_hsv_l2[1], self.color_hsv_l2[2]))
            self.layout.hsv_l2.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_hsv_l2 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.hsv_l2.setStyleSheet(black)
            self.layout.hsv_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g2 = 0
            self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_L3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_l3 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_hsv_l3[0], self.color_hsv_l3[1], self.color_hsv_l3[2]))
            self.layout.hsv_l3.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_hsv_l3 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.hsv_l3.setStyleSheet(black)
            self.layout.hsv_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g3 = 0
            self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_HSV_R1(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_r1 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_hsv_r1[0], self.color_hsv_r1[1], self.color_hsv_r1[2]))
            self.layout.hsv_r1.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_hsv_r1 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.hsv_r1.setStyleSheet(black)
            self.layout.hsv_g1.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g1 = 0
            self.mixer_hsv_g1.Update(self.percentage_hsv_g1, self.layout.hsv_g1.width())

    def Mixer_HSV_R2(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_r2 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_hsv_r2[0], self.color_hsv_r2[1], self.color_hsv_r2[2]))
            self.layout.hsv_r2.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_hsv_r2 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.hsv_r2.setStyleSheet(black)
            self.layout.hsv_g2.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g2 = 0
            self.mixer_hsv_g2.Update(self.percentage_hsv_g2, self.layout.hsv_g2.width())

    def Mixer_HSV_R3(self, SIGNAL_MIXER_COLOR):
        if SIGNAL_MIXER_COLOR == "Save":
            # Color Math
            self.color_hsv_r3 = [self.layout.rgb_1_value.value(), self.layout.rgb_2_value.value(), self.layout.rgb_3_value.value(), self.layout.hsv_1_value.value(), self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value()]
            # Display
            color = str("background-color: rgb(%f, %f, %f);" % (self.color_hsv_r3[0], self.color_hsv_r3[1], self.color_hsv_r3[2]))
            self.layout.hsv_r3.setStyleSheet(color)
            self.Mixer_Display()
        if SIGNAL_MIXER_COLOR == "Clear":
            # Color Math
            self.color_hsv_r3 = [0,0,0, 0,0,0]
            # Display
            black = str("background-color: rgba(%f, %f, %f, %f);" % (self.color_black[0], self.color_black[1], self.color_black[2], 255))
            alpha = str("background-color: rgba(%f, %f, %f, %f);" % (0, 0, 0, 0))
            self.layout.hsv_r3.setStyleSheet(black)
            self.layout.hsv_g3.setStyleSheet(alpha)
            # Correct Values
            self.percentage_hsv_g3 = 0
            self.mixer_hsv_g3.Update(self.percentage_hsv_g3, self.layout.hsv_g3.width())

    def Mixer_Tint(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_tint = SIGNAL_MIXER_CHANNEL / (self.layout.tint.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_neutral[0]) + (self.percentage_tint * (self.color_white[0] - self.color_neutral[0]))) / factor255
        rgb2 = ((self.color_neutral[1]) + (self.percentage_tint * (self.color_white[1] - self.color_neutral[1]))) / factor255
        rgb3 = ((self.color_neutral[2]) + (self.percentage_tint * (self.color_white[2] - self.color_neutral[2]))) / factor255
        # Convert to HSV
        hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_Tone(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_tone = SIGNAL_MIXER_CHANNEL / (self.layout.tone.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_neutral[0]) + (self.percentage_tone * (self.color_grey[0] - self.color_neutral[0]))) / factor255
        rgb2 = ((self.color_neutral[1]) + (self.percentage_tone * (self.color_grey[1] - self.color_neutral[1]))) / factor255
        rgb3 = ((self.color_neutral[2]) + (self.percentage_tone * (self.color_grey[2] - self.color_neutral[2]))) / factor255
        # Convert to HSV
        hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_Shade(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_shade = SIGNAL_MIXER_CHANNEL / (self.layout.shade.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = ((self.color_neutral[0]) + (self.percentage_shade * (self.color_black[0] - self.color_neutral[0]))) / factor255
        rgb2 = ((self.color_neutral[1]) + (self.percentage_shade * (self.color_black[1] - self.color_neutral[1]))) / factor255
        rgb3 = ((self.color_neutral[2]) + (self.percentage_shade * (self.color_black[2] - self.color_neutral[2]))) / factor255
        # Convert to HSV
        hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_RGB_G1(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_rgb_g1 = SIGNAL_MIXER_CHANNEL / (self.layout.rgb_g1.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l1[0] + (self.percentage_rgb_g1 * (self.color_rgb_r1[0] - self.color_rgb_l1[0]))) / factor255
        rgb2 = (self.color_rgb_l1[1] + (self.percentage_rgb_g1 * (self.color_rgb_r1[1] - self.color_rgb_l1[1]))) / factor255
        rgb3 = (self.color_rgb_l1[2] + (self.percentage_rgb_g1 * (self.color_rgb_r1[2] - self.color_rgb_l1[2]))) / factor255
        # Convert to HSV
        hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_RGB_G2(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_rgb_g2 = SIGNAL_MIXER_CHANNEL / (self.layout.rgb_g2.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l2[0] + (self.percentage_rgb_g2 * (self.color_rgb_r2[0] - self.color_rgb_l2[0]))) / factor255
        rgb2 = (self.color_rgb_l2[1] + (self.percentage_rgb_g2 * (self.color_rgb_r2[1] - self.color_rgb_l2[1]))) / factor255
        rgb3 = (self.color_rgb_l2[2] + (self.percentage_rgb_g2 * (self.color_rgb_r2[2] - self.color_rgb_l2[2]))) / factor255
        # Convert to HSV
        hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_RGB_G3(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_rgb_g3 = SIGNAL_MIXER_CHANNEL / (self.layout.rgb_g3.width())
        # Percentual Value added to Left Color Percentil
        rgb1 = (self.color_rgb_l3[0] + (self.percentage_rgb_g3 * (self.color_rgb_r3[0] - self.color_rgb_l3[0]))) / factor255
        rgb2 = (self.color_rgb_l3[1] + (self.percentage_rgb_g3 * (self.color_rgb_r3[1] - self.color_rgb_l3[1]))) / factor255
        rgb3 = (self.color_rgb_l3[2] + (self.percentage_rgb_g3 * (self.color_rgb_r3[2] - self.color_rgb_l3[2]))) / factor255
        # Convert to HSV
        hsv = colorsys.rgb_to_hsv(rgb1, rgb2, rgb3)
        hsv1 = hsv[0]
        hsv2 = hsv[1]
        hsv3 = hsv[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_HSV_G1(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_hsv_g1 = SIGNAL_MIXER_CHANNEL / (self.layout.hsv_g1.width())
        # Conditions
        cond1 = self.color_hsv_r1[3] - self.color_hsv_l1[3]
        cond2 = (self.color_hsv_l1[3] + factor360) - self.color_hsv_r1[3]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l1[3] + (self.percentage_hsv_g1 * cond1))
        else:
            hue = (self.color_hsv_l1[3] - (self.percentage_hsv_g1 * cond2))
            if hue <= 0:
                hue = hue + factor360
            else:
                pass
        hsv1 = hue / factor360
        hsv2 = (self.color_hsv_l1[4] + (self.percentage_hsv_g1 * (self.color_hsv_r1[4] - self.color_hsv_l1[4]))) / factor100
        hsv3 = (self.color_hsv_l1[5] + (self.percentage_hsv_g1 * (self.color_hsv_r1[5] - self.color_hsv_l1[5]))) / factor100
        # Convert to HSV
        rgb = colorsys.hsv_to_rgb(hsv1, hsv2, hsv3)
        rgb1 = rgb[0]
        rgb2 = rgb[1]
        rgb3 = rgb[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_HSV_G2(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_hsv_g2 = SIGNAL_MIXER_CHANNEL / (self.layout.hsv_g2.width())
        # Conditions
        cond1 = self.color_hsv_r2[3] - self.color_hsv_l2[3]
        cond2 = (self.color_hsv_l2[3] + factor360) - self.color_hsv_r2[3]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l2[3] + (self.percentage_hsv_g2 * cond1))
        else:
            hue = (self.color_hsv_l2[3] - (self.percentage_hsv_g2 * cond2))
            if hue <= 0:
                hue = hue + factor360
            else:
                pass
        hsv1 = hue / factor360
        hsv2 = (self.color_hsv_l2[4] + (self.percentage_hsv_g2 * (self.color_hsv_r2[4] - self.color_hsv_l2[4]))) / factor100
        hsv3 = (self.color_hsv_l2[5] + (self.percentage_hsv_g2 * (self.color_hsv_r2[5] - self.color_hsv_l2[5]))) / factor100
        # Convert to HSV
        rgb = colorsys.hsv_to_rgb(hsv1, hsv2, hsv3)
        rgb1 = rgb[0]
        rgb2 = rgb[1]
        rgb3 = rgb[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_HSV_G3(self, SIGNAL_MIXER_CHANNEL):
        # Percentage Value
        self.percentage_hsv_g3 = SIGNAL_MIXER_CHANNEL / (self.layout.hsv_g3.width())
        # Conditions
        cond1 = self.color_hsv_r3[3] - self.color_hsv_l3[3]
        cond2 = (self.color_hsv_l3[3] + factor360) - self.color_hsv_r3[3]
        # Descriminate Condition
        if cond1 <= cond2:
            hue = (self.color_hsv_l3[3] + (self.percentage_hsv_g3 * cond1))
        else:
            hue = (self.color_hsv_l3[3] - (self.percentage_hsv_g3 * cond2))
            if hue <= 0:
                hue = hue + factor360
            else:
                pass
        hsv1 = hue / factor360
        hsv2 = (self.color_hsv_l3[4] + (self.percentage_hsv_g3 * (self.color_hsv_r3[4] - self.color_hsv_l3[4]))) / factor100
        hsv3 = (self.color_hsv_l3[5] + (self.percentage_hsv_g3 * (self.color_hsv_r3[5] - self.color_hsv_l3[5]))) / factor100
        # Convert to HSV
        rgb = colorsys.hsv_to_rgb(hsv1, hsv2, hsv3)
        rgb1 = rgb[0]
        rgb2 = rgb[1]
        rgb3 = rgb[2]
        # Update Values
        self.Mixer_Color(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_Color(self, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        self.Pigment_Sync("MIX", rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)
        self.Pigment_2_Krita(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)
        self.Pigment_Display(rgb1, rgb2, rgb3, hsv1, hsv2, hsv3)

    def Mixer_Display(self):
        # Display Color with Tint, Tone, Shade
        mix_tint = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%f, %f, %f), stop:1 rgb(%f, %f, %f));" % (self.color_neutral[0], self.color_neutral[1], self.color_neutral[2], self.color_white[0], self.color_white[1], self.color_white[2]))
        self.layout.tint.setStyleSheet(mix_tint)
        mix_tone = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%f, %f, %f), stop:1 rgb(%f, %f, %f));" % (self.color_neutral[0], self.color_neutral[1], self.color_neutral[2], self.color_grey[0], self.color_grey[1], self.color_grey[2]))
        self.layout.tone.setStyleSheet(mix_tone)
        mix_shade = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%f, %f, %f), stop:1 rgb(%f, %f, %f));" % (self.color_neutral[0], self.color_neutral[1], self.color_neutral[2], self.color_black[0], self.color_black[1], self.color_black[2]))
        self.layout.shade.setStyleSheet(mix_shade)
        # RGB Gradients
        mix_rgb_g1 = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%f, %f, %f), stop:1 rgb(%f, %f, %f));" % (self.color_rgb_l1[0], self.color_rgb_l1[1], self.color_rgb_l1[2], self.color_rgb_r1[0], self.color_rgb_r1[1], self.color_rgb_r1[2]))
        self.layout.rgb_g1.setStyleSheet(mix_rgb_g1)
        mix_rgb_g2 = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%f, %f, %f), stop:1 rgb(%f, %f, %f));" % (self.color_rgb_l2[0], self.color_rgb_l2[1], self.color_rgb_l2[2], self.color_rgb_r2[0], self.color_rgb_r2[1], self.color_rgb_r2[2]))
        self.layout.rgb_g2.setStyleSheet(mix_rgb_g2)
        mix_rgb_g3 = str("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(%f, %f, %f), stop:1 rgb(%f, %f, %f));" % (self.color_rgb_l3[0], self.color_rgb_l3[1], self.color_rgb_l3[2], self.color_rgb_r3[0], self.color_rgb_r3[1], self.color_rgb_r3[2]))
        self.layout.rgb_g3.setStyleSheet(mix_rgb_g3)
        # HSV Gradients
        mix_hsv_g1 = self.style.HSV_Gradient(self.layout.hsv_g1.width(), self.color_hsv_l1, self.color_hsv_r1)
        self.layout.hsv_g1.setStyleSheet(str(mix_hsv_g1))
        mix_hsv_g2 = self.style.HSV_Gradient(self.layout.hsv_g2.width(), self.color_hsv_l2, self.color_hsv_r2)
        self.layout.hsv_g2.setStyleSheet(str(mix_hsv_g2))
        mix_hsv_g3 = self.style.HSV_Gradient(self.layout.hsv_g3.width(), self.color_hsv_l3, self.color_hsv_r3)
        self.layout.hsv_g3.setStyleSheet(str(mix_hsv_g3))

    # Widget Events
    def enterEvent(self, event):
        # Check Krita Once before edit
        self.Krita_Update()
        # Confirm Panel
        self.Ratio()
        # Stop Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.stop()
        else:
            pass

    def leaveEvent(self, event):
        # Start Asking Krita the Current Color
        if check_timer >= 1000:
            self.timer.start()
        else:
            pass

    def showEvent(self, event):
        # Update on init for correct window Size
        self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.layout.hex_string.text())

    def closeEvent(self, event):
        # Stop QTimer
        if check_timer >= 1000:
            self.timer.stop()
        else:
            pass

    def resizeEvent(self, event):
        self.Ratio()

    def Ratio(self):
        # Relocate Channel Handle due to Size Variation
        self.rgb_1_slider.Update(self.layout.rgb_1_value.value(), factor255, self.layout.rgb_1_slider.width())
        self.rgb_2_slider.Update(self.layout.rgb_2_value.value(), factor255, self.layout.rgb_2_slider.width())
        self.rgb_3_slider.Update(self.layout.rgb_3_value.value(), factor255, self.layout.rgb_3_slider.width())
        self.hsv_1_slider.Update(self.layout.hsv_1_value.value(), factor360, self.layout.hsv_1_slider.width())
        self.hsv_2_slider.Update(self.layout.hsv_2_value.value(), factor100, self.layout.hsv_2_slider.width())
        self.hsv_3_slider.Update(self.layout.hsv_3_value.value(), factor100, self.layout.hsv_3_slider.width())
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
        # Relocate Panel Cursor due to Size Variation
        self.panel_hsv.Update_Panel(self.layout.hsv_2_value.value(), self.layout.hsv_3_value.value(), self.layout.panel_hsv_fg.width(), self.layout.panel_hsv_fg.height(), self.layout.hex_string.text())

    # Change the Canvas
    def canvasChanged(self, canvas):
        pass
