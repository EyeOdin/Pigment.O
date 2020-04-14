from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui
import threading

class Clicks(QWidget):
    SIGNAL_CLICKS = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Clicks, self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier):
            self.SIGNAL_CLICKS.emit("SAVE")
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.SIGNAL_CLICKS.emit("CLEAN")
        else:
            self.SIGNAL_CLICKS.emit("APPLY")
