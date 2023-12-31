import sys

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication


class PWVApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)

        self._mainWin = None
        
        self.focusChanged.connect(self._focusChangedCB)

        self._loadAssets()

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
            print(f"TOP WGT: {tlwgt.windowTitle()}  Active: {tlwgt.isActiveWindow()}")
            if tlwgt.isActiveWindow():
                actwgt = tlwgt
        return actwgt

    def _loadAssets(self):
        self._assets = {}
        icon = QtGui.QIcon("assets/copy-button-icon.png")
        self._assets["copy-button-icon"] = icon
        icon = QtGui.QIcon("assets/edit-button-icon.png")
        self._assets["edit-button-icon"] = icon
        
        
if __name__ == "__main__":
    from pwvuimain import PWVMainWin
    
    app = PWVApp()

    mainWin = PWVMainWin()
    app.setMainWin(mainWin)

    mainWin.show()

    status = app.exec()
    sys.exit(status)
