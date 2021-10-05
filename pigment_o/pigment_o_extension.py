# Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer.
# Copyright (C) 2020  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#\\ Import Modules #############################################################
from krita import *
from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtSvg, uic
from PyQt5.Qt import Qt
#//
#\\ Global Variables ###########################################################
EXTENSION_ID = 'pykrita_pigment_o_extension'
#//

class PigmentOExtension(Extension):
    """
    Extension Shortcuts and HUD.
    """
    SIGNAL_COR = QtCore.pyqtSignal(int)
    SIGNAL_KEY = QtCore.pyqtSignal(str)
    SIGNAL_HUD = QtCore.pyqtSignal(int)

    #\\ Initialize #############################################################
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    #//
    #\\ Actions ################################################################
    def createActions(self, window):
        #\\ Shortcut COR #######################################################
        # Create Menu
        action_cor = window.createAction("Pigment.O Menu Cor", "Pigment.O Color", "tools/scripts")
        menu_cor = QtWidgets.QMenu("Pigment.O Menu Cor", window.qwindow())
        action_cor.setMenu(menu_cor)
        # Create Action
        action_cor_0 = window.createAction(EXTENSION_ID+"_color_0", "P. Color 0", "tools/scripts/Pigment.O Menu Cor")
        action_cor_1 = window.createAction(EXTENSION_ID+"_color_1", "P. Color 1", "tools/scripts/Pigment.O Menu Cor")
        action_cor_2 = window.createAction(EXTENSION_ID+"_color_2", "P. Color 2", "tools/scripts/Pigment.O Menu Cor")
        action_cor_3 = window.createAction(EXTENSION_ID+"_color_3", "P. Color 3", "tools/scripts/Pigment.O Menu Cor")
        action_cor_4 = window.createAction(EXTENSION_ID+"_color_4", "P. Color 4", "tools/scripts/Pigment.O Menu Cor")
        action_cor_5 = window.createAction(EXTENSION_ID+"_color_5", "P. Color 5", "tools/scripts/Pigment.O Menu Cor")
        action_cor_6 = window.createAction(EXTENSION_ID+"_color_6", "P. Color 6", "tools/scripts/Pigment.O Menu Cor")
        action_cor_7 = window.createAction(EXTENSION_ID+"_color_7", "P. Color 7", "tools/scripts/Pigment.O Menu Cor")
        action_cor_8 = window.createAction(EXTENSION_ID+"_color_8", "P. Color 8", "tools/scripts/Pigment.O Menu Cor")
        action_cor_9 = window.createAction(EXTENSION_ID+"_color_9", "P. Color 9", "tools/scripts/Pigment.O Menu Cor")
        action_cor_10 = window.createAction(EXTENSION_ID+"_color_10", "P. Color 10", "tools/scripts/Pigment.O Menu Cor")
        # Connect with Trigger
        action_cor_0.triggered.connect(self.COR_0)
        action_cor_1.triggered.connect(self.COR_1)
        action_cor_2.triggered.connect(self.COR_2)
        action_cor_3.triggered.connect(self.COR_3)
        action_cor_4.triggered.connect(self.COR_4)
        action_cor_5.triggered.connect(self.COR_5)
        action_cor_6.triggered.connect(self.COR_6)
        action_cor_8.triggered.connect(self.COR_8)
        action_cor_7.triggered.connect(self.COR_7)
        action_cor_9.triggered.connect(self.COR_9)
        action_cor_10.triggered.connect(self.COR_10)

        #//
        #\\ Shortcut KEY #######################################################
        # Create Menu
        action_key = window.createAction("Pigment.O Menu Key", "Pigment.O Keys", "tools/scripts")
        menu_key = QtWidgets.QMenu("Pigment.O Menu Key", window.qwindow())
        action_key.setMenu(menu_key)
        # Create Action
        action_key_1_minus = window.createAction(EXTENSION_ID+"_key_1_minus", "P. Key 1 Minus", "tools/scripts/Pigment.O Menu Key")
        action_key_1_plus = window.createAction(EXTENSION_ID+"_key_1_plus", "P. Key 1 Plus", "tools/scripts/Pigment.O Menu Key")
        action_key_2_minus = window.createAction(EXTENSION_ID+"_key_2_minus", "P. Key 2 Minus", "tools/scripts/Pigment.O Menu Key")
        action_key_2_plus = window.createAction(EXTENSION_ID+"_key_2_plus", "P. Key 2 Plus", "tools/scripts/Pigment.O Menu Key")
        action_key_3_minus = window.createAction(EXTENSION_ID+"_key_3_minus", "P. Key 3 Minus", "tools/scripts/Pigment.O Menu Key")
        action_key_3_plus = window.createAction(EXTENSION_ID+"_key_3_plus", "P. Key 3 Plus", "tools/scripts/Pigment.O Menu Key")
        action_key_4_minus = window.createAction(EXTENSION_ID+"_key_4_minus", "P. Key 4 Minus", "tools/scripts/Pigment.O Menu Key")
        action_key_4_plus = window.createAction(EXTENSION_ID+"_key_4_plus", "P. Key 4 Plus", "tools/scripts/Pigment.O Menu Key")
        # Connect with Trigger
        action_key_1_minus.triggered.connect(self.KEY_1_Minus)
        action_key_1_plus.triggered.connect(self.KEY_1_Plus)
        action_key_2_minus.triggered.connect(self.KEY_2_Minus)
        action_key_2_plus.triggered.connect(self.KEY_2_Plus)
        action_key_3_minus.triggered.connect(self.KEY_3_Minus)
        action_key_3_plus.triggered.connect(self.KEY_3_Plus)
        action_key_4_minus.triggered.connect(self.KEY_4_Minus)
        action_key_4_plus.triggered.connect(self.KEY_4_Plus)

        #//
        #\\ Shortcut HUD #######################################################
        action_panel_hud = window.createAction(EXTENSION_ID+"_panel_hud", "Pigment.O Panel HUD", "tools/scripts")
        action_panel_hud.triggered.connect(self.Panel_HUD)
        action_panel_hud.setAutoRepeat(False)

        #//

    #//
    #\\ COR ####################################################################
    def COR_0(self):
        self.SIGNAL_COR.emit(0)
    def COR_1(self):
        self.SIGNAL_COR.emit(1)
    def COR_2(self):
        self.SIGNAL_COR.emit(2)
    def COR_3(self):
        self.SIGNAL_COR.emit(3)
    def COR_4(self):
        self.SIGNAL_COR.emit(4)
    def COR_5(self):
        self.SIGNAL_COR.emit(5)
    def COR_6(self):
        self.SIGNAL_COR.emit(6)
    def COR_7(self):
        self.SIGNAL_COR.emit(7)
    def COR_8(self):
        self.SIGNAL_COR.emit(8)
    def COR_9(self):
        self.SIGNAL_COR.emit(9)
    def COR_10(self):
        self.SIGNAL_COR.emit(10)

    #//
    #\\ KEY ####################################################################
    def KEY_1_Minus(self):
        self.SIGNAL_KEY.emit("K1 Minus")
    def KEY_1_Plus(self):
        self.SIGNAL_KEY.emit("K1 Plus")

    def KEY_2_Minus(self):
        self.SIGNAL_KEY.emit("K2 Minus")
    def KEY_2_Plus(self):
        self.SIGNAL_KEY.emit("K2 Plus")

    def KEY_3_Minus(self):
        self.SIGNAL_KEY.emit("K3 Minus")
    def KEY_3_Plus(self):
        self.SIGNAL_KEY.emit("K3 Plus")

    def KEY_4_Minus(self):
        self.SIGNAL_KEY.emit("K4 Minus")
    def KEY_4_Plus(self):
        self.SIGNAL_KEY.emit("K4 Plus")

    #//
    #\\ Panel HUD ##############################################################
    def Panel_HUD(self):
        self.SIGNAL_HUD.emit(0)

    #//
