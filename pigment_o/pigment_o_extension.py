from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt


EXTENSION_ID = 'pykrita_pigment_o_extension'

class PigmentOExtension(Extension):
    """
    Extension Shortcuts and HUD.
    """
    SIGNAL_KEY = QtCore.pyqtSignal(str)

    #\\ Initialize #############################################################
    def __init__(self, parent):
        super().__init__(parent)
        self.setup()
    def setup(self):
        self.hud_size = 200
        self.circleIcon = None

    #//
    #\\ Actions ################################################################
    def createActions(self, window):
        # Shortcut Keys
        action_key_1_plus = window.createAction(EXTENSION_ID+"_key_1_plus", "P. Key 1 Plus", "tools/scripts")
        action_key_1_plus.triggered.connect(self.KEY_1_Plus)
        action_key_1_minus = window.createAction(EXTENSION_ID+"_key_1_minus", "P. Key 1 Minus", "tools/scripts")
        action_key_1_minus.triggered.connect(self.KEY_1_Minus)
        action_key_2_plus = window.createAction(EXTENSION_ID+"_key_2_plus", "P. Key 2 Plus", "tools/scripts")
        action_key_2_plus.triggered.connect(self.KEY_2_Plus)
        action_key_2_minus = window.createAction(EXTENSION_ID+"_key_2_minus", "P. Key 2 Minus", "tools/scripts")
        action_key_2_minus.triggered.connect(self.KEY_2_Minus)
        action_key_3_plus = window.createAction(EXTENSION_ID+"_key_3_plus", "P. Key 3 Plus", "tools/scripts")
        action_key_3_plus.triggered.connect(self.KEY_3_Plus)
        action_key_3_minus = window.createAction(EXTENSION_ID+"_key_3_minus", "P. Key 3 Minus", "tools/scripts")
        action_key_3_minus.triggered.connect(self.KEY_3_Minus)
        action_key_4_plus = window.createAction(EXTENSION_ID+"_key_4_plus", "P. Key 4 Plus", "tools/scripts")
        action_key_4_plus.triggered.connect(self.KEY_4_Plus)
        action_key_4_minus = window.createAction(EXTENSION_ID+"_key_4_minus", "P. Key 4 Minus", "tools/scripts")
        action_key_4_minus.triggered.connect(self.KEY_4_Minus)
        # Panel HUD
        action_panel_hud = window.createAction(EXTENSION_ID+"_panel_hud", "P. Panel HUD", "tools/scripts")
        action_panel_hud.triggered.connect(self.Panel_HUD)
        action_panel_hud.setAutoRepeat(False)


        # if self.circleIcon is None:
        #   self.circleIcon = RotationCentreIcon(QPoint(0, 0), self.hud_size, self.hud_size, window.qwindow())
        self.MAFilter = mdiAreaFilter()
        self.MAFilter.setMouseTracking(True)

    #//
    #\\ KEY ##################################################################
    def KEY_1_Plus(self):
        self.SIGNAL_KEY.emit("K1 Plus")
    def KEY_1_Minus(self):
        self.SIGNAL_KEY.emit("K1 Minus")

    def KEY_2_Plus(self):
        self.SIGNAL_KEY.emit("K2 Plus")
    def KEY_2_Minus(self):
        self.SIGNAL_KEY.emit("K2 Minus")

    def KEY_3_Plus(self):
        self.SIGNAL_KEY.emit("K3 Plus")
    def KEY_3_Minus(self):
        self.SIGNAL_KEY.emit("K3 Minus")

    def KEY_4_Plus(self):
        self.SIGNAL_KEY.emit("K4 Plus")
    def KEY_4_Minus(self):
        self.SIGNAL_KEY.emit("K4 Minus")

    #//
    #\\ Panel HUD ##############################################################
    def Panel_HUD(self):
        pass

    #//
    #\\ Events #################################################################


    #//

circleIcon = None
class mdiAreaFilter(QMdiArea):
    global circleIcon

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):

        # if Krita.instance().action('KritaSelected/KisToolColorPicker').trigger() == True:
        #     QtCore.qDebug("Picker Choosen")

        if (event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonDblClick):
            if event.buttons() == QtCore.Qt.LeftButton:
                # if Application.action("KritaSelected/KisToolColorPicker") == True:

                # QtCore.qDebug("press")

                # cursor_init_position = QCursor.pos()
                # circleIcon.showAt(cursor_init_position)

                pass


        if event.type() == QEvent.MouseButtonRelease:
            # QtCore.qDebug("release")
            pass

        return False

    # if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier or event.modifiers() == QtCore.Qt.AltModifier):


class RotationCentreIcon(QWidget):
  def __init__(self, position, width, height, parent=None):
    QWidget.__init__(self, parent)

    self.position = position
    self.width = int(width)
    self.height = int(height)
    self.setGeometry(int(position.x() - self.width / 2), int(position.y() - self.height / 2), self.width, self.height)
    self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.setStyleSheet("background: transparent;")
    self.setWindowTitle("icon")

  def showAt(self, position):
    self.move(position.x() - self.width / 2, position.y() - self.height / 2)
    self.show()

  def paintEvent(self, event):
    self.painter = QPainter(self)
    self.painter.setRenderHints( QPainter.HighQualityAntialiasing )
    self.painter.setPen( QPen(QColor(255, 255, 255, 150), 1) )
    self.painter.setBrush( QColor(47, 47, 47, 150) )
    self.painter.drawEllipse(0, 0, self.width, self.height)
    self.painter.end()
