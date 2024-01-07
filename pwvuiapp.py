import os
import sys

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication


class PWVApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)

        self._mainWin = None
        
        self.focusChanged.connect(self._focusChangedCB)

        self._loadAssets()
        self._setAppWideStyles()

    def asset(self, name):
        return self._assets.get(name)

    def mainWin(self):
        return self._mainWin
    
    def setMainWin(self, mainWin):
        self._mainWin = mainWin

    def _focusChangedCB(fromWgt, toWgt):
        if type(fromWgt) is PWVApp:
            return
        
        print(f"_focusChangedCB: From: {fromWgt}  To: {toWgt}")
        fromWin = fromWgt.window() if fromWgt else fromWgt
        toWin = toWgt.window() if toWgt else toWgt
        print(f"    FromWin: {fromWin}  ToWin: {toWin}")
        self.findActive()

    def findActive(self):
        actwgt = None
        for tlwgt in QApplication.topLevelWidgets():
#            print(f"TOP WGT: {tlwgt.windowTitle()}  Active: {tlwgt.isActiveWindow()}")
            if tlwgt.isActiveWindow():
                actwgt = tlwgt
        return actwgt

    def _loadAssets(self):
        folder = os.path.dirname(__file__)
        folder = os.path.join(folder, "assets")
        self._assets = {}
        icon = QtGui.QIcon(os.path.join(folder, "copy-button-icon.png"))
        self._assets["copy-button-icon"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "edit-button-icon.png"))
        self._assets["edit-button-icon"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "padlock-icon.png"))
        self._assets["padlock-icon"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "eye-open-yellow.svg"))
        self._assets["eye-open-yellow"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "eye-blocked-yellow"))
        self._assets["eye-blocked-yellow"] = icon

    def _setAppWideStyles(self):
        self.setStyleSheet("""
        QLineEdit[echoMode="2"] {
          lineedit-password-character: 9679;
        }
        QInputDialog {
          background-color: red;
        }
        QLineEdit {
          background-color: blue;
        }
        QInputDialog*QLineEdit[echoMode="2"] {
              lineedit-password-character: 9679;
            }
        """)


if __name__ == "__main__":
    from pwvuimain import PWVMainWin
    
    app = PWVApp()

    mainWin = PWVMainWin()
    app.setMainWin(mainWin)

    mainWin.show()

    status = app.exec()
    sys.exit(status)
