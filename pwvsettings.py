from PyQt6.QtCore import QObject
from PyQt6.QtCore import QSettings

class PWVSettings(QObject):

    def __init__(self, pwvapp, parent=None):
        super().__init__(parent)
        self._app = app

        self._modified = False

        app.setOrganizationName("MiDoMa")
        app.setOrganizationDomain("midoma.com")
        app.setApplicationName("PWVault")

        self._settings = QSettings()

        print(f"SETTINGS FILE: {self._settings.fileName()}")
        keys = self._settings.allKeys()
        for key in keys:
            print(f"KEY: {key}")
        try:
            self._recentFiles = self._settings.value("appRecentFiles")
            print(f"RECENT: {self._recentFiles}")
        except Exception as exc:
            print(f"SETTINGS: TYPE({type(exc)} {exc}")
#     def closeEvent(self, event):
#        self.settings.setValue('window size', self.size())
#        self.settings.setValue('window position', self.pos())
        if self._recentFiles:
            self._settings.beginGroup("PwvUiApp")
#            self._settings.setValue("appRecentFiles",  self._recentFiles)
            keys = self._settings.allKeys()
            for key in keys:
                print(f"    KEY: {key}")
                self._settings.endGroup()

    def load(self):
        self._settings.beginGroup(self._group)
#            self._settings.setValue("appRecentFiles",  self._recentFiles)

        self._cache = { key:self._settings.value(key)
                            for key in self._settings.allKeys() }


        for key in self._cache.keys():
            print(f"{self._group}[{key} = {self._cache}")

        self._settings.endGroup()
        
    def fileName(self):
        return self._settings.fileName()

    def saveAll(self):
        self._settings.beginGroup(self._group)
        for key,val in self._cache:
            self._settings.setValue(key,val)
        self._settings.endGroup()

    def setModified(self, state):
        self._modified = state



class PWVCliSettings(PWVSettings):

    def __init__(self, app, parent=None):
        super().__init__(app, parent)

        self._group = "PwvCliApp"


class PWVUiSettings(PWVSettings):

    def __init__(self, app, parent=None):
        super().__init__(app, parent)

        self._group = "PwvUiApp"

        

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    uiSettings = PWVUiSettings(app)
    uiSettings.load()
    print(f"PATH: {uiSettings.fileName()}")
    print(f"CACHE: {uiSettings._cache}")
