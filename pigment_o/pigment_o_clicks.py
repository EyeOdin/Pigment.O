from krita import *
from PyQt5 import QtWidgets, QtCore, QtGui
import threading

class Clicks(QWidget):
    SIGNAL_CLICKS = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super(Clicks, self).__init__(parent)
        self.cond = None

    def Setup(self, size, opacity, flow):
        self.cond = "TIP"
        self.size = size
        self.opacity = opacity
        self.flow = flow

    def mousePressevent(self, event):
        self.update()
    def mouseDoubleClickEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ShiftModifier or event.modifiers() == QtCore.Qt.ControlModifier):
            self.SIGNAL_CLICKS.emit("SAVE")
            self.update()
        elif event.modifiers() == QtCore.Qt.AltModifier:
            self.SIGNAL_CLICKS.emit("CLEAN")
            self.update()
        else:
            self.SIGNAL_CLICKS.emit("APPLY")
            self.update()

    def paintEvent(self, event):
        if self.cond == "TIP":
            # Text
            self.text = str(self.size)+"\n"+str(round(self.opacity*100,0))+"\n"+str(round(self.flow*100,0))
            # QPainter Start
            qp = QPainter()
            qp.begin(self)
            # Background
            brush = QBrush(QColor(0, 0, 0, 50), Qt.SolidPattern)
            qp.setBrush(brush)
            qp.drawRect(-5, -5, 50, 50)
            # Letters
            qp.setPen(QColor(255, 255, 255))
            qp.setFont(QFont('Monospace', 5))
            qp.drawText(event.rect(), Qt.AlignCenter|Qt.AlignVCenter, self.text)
            # Finish
            qp.end()
        else:
            pass
