import os
import sys

from PyQt6.QtCore    import QSettings
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication

from pwvsettings import PWVUiSettings


class PWVApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)

        self._mainWin = None
        
        self.focusChanged.connect(self._focusChangedCB)

        self._loadAssets()
        self._loadSettings()
        self._setAppWideStyles()

    def asset(self, name):
        return self._assets.get(name)

    def findActive(self):
        actwgt = None
        for tlwgt in QApplication.topLevelWidgets():
#            print(f"TOP WGT: {tlwgt.windowTitle()}  Active: {tlwgt.isActiveWindow()}")
            if tlwgt.isActiveWindow():
                actwgt = tlwgt
        return actwgt

    def mainWin(self):
        return self._mainWin

    def recentFileOpens(self):
        return self._settings.recentOpens()

    def recentFileUpdate(self, path):
        recentOpens = self._settings.recentOpens()
        if path in recentOpens:
            recentOpens.remove(path)
        recentOpens.append(path)
        maxRecents = 6
        rfLen = len(recentOpens)
        if rfLen > maxRecents:
            recentOpens = recentOpens[rfLen-maxRecents:]
        self._settings.setRecentOpens(recentOpens)
    
    def setMainWin(self, mainWin):
        self._mainWin = mainWin

    def settings(self):
        return self._settings
    
    def _focusChangedCB(fromWgt, toWgt):
        if type(fromWgt) is PWVApp:
            return
        
        print(f"_focusChangedCB: From: {fromWgt}  To: {toWgt}")
        fromWin = fromWgt.window() if fromWgt else fromWgt
        toWin = toWgt.window() if toWgt else toWgt
        print(f"    FromWin: {fromWin}  ToWin: {toWin}")
        self.findActive()

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
        icon = QtGui.QIcon(os.path.join(folder, "eye-blocked-yellow.svg"))
        self._assets["eye-blocked-yellow"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "search-icon-yellow.svg"))
        self._assets["search-icon-yellow"] = icon

    def _loadSettings(self):
        self._settings = PWVUiSettings(self)
        self._settings.load()
        print(f"SETTINGS FILE: {self._settings.fileName()}")
        try:
            self._recentFiles = self._settings.recentOpens()
            print(f"RECENT: {self._recentFiles}")
        except Exception as exc:
            print(f"SETTINGS: TYPE({type(exc)} {exc}")

    def _setAppWideStyles(self):
        pass
#        self.setStyleSheet("""
#        QLineEdit[echoMode="2"] {
#          lineedit-password-character: 9679;
#        }
#        QInputDialog QLineEdit[echoMode="2"] {
#              lineedit-password-character: 9679;
#            }
#        """)


if __name__ == "__main__":
    from pwvuimain import PWVMainWin
    
    app = PWVApp()

    mainWin = PWVMainWin()
    app.setMainWin(mainWin)

    mainWin.show()

    status = app.exec()
    sys.exit(status)
