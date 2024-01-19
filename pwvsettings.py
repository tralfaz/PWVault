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

    def load(self):
        self._settings.beginGroup(self._group)
        self._cache = { key:self._settings.value(key)
                            for key in self._settings.allKeys() }
        self._settings.endGroup()
        self.setModified(False)
        
    def fileName(self):
        return self._settings.fileName()

    def modified(self):
        return self._modified
    
    def saveAll(self):
        self._settings.beginGroup(self._group)
        for key,val in self._cache.items():
            print(f"{self._group}: {key} <- {val}")
            self._settings.setValue(key,val)
        self._settings.endGroup()
        self.setModified(False)

    def setValue(self, key, value):
        self._cache[key] = value
        self.setModified(True)

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

    def cardZoom(self, winName, zoomDelta=0):
        zoomKey = "CardZoom::" + winName
        zoomVal = self._cache.get(zoomKey,0) + zoomDelta
        self.setValue(zoomKey, zoomVal)
        return zoomVal

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    uiSettings = PWVUiSettings(app)
    uiSettings.load()
    print(f"PATH: {uiSettings.fileName()}")
    topKeys = uiSettings._settings.allKeys()
    for key in topKeys:
        print(f"TOP KEY: {key}")

    print(f"CACHE: {uiSettings._cache}")

    if len(sys.argv) > 1 and sys.argv[1] == "move":
        for key in topKeys:
            if key.endswith("::cardZoom"):
                toKey = "CardZoom::" + key[:-10]
                toVal = uiSettings._settings.value(key)
                print(f"{key} -> {toKey} = {toVal}")
                uiSettings.setValue(toKey, toVal)
            elif key == "appRecentFiles":
                toKey = "RecentOpens"
                toVal = uiSettings._settings.value(key)
                print(f"{key} -> {toKey} = {toVal}")
                uiSettings.setValue(toKey, toVal)

        print(f"CACHE: {uiSettings._cache}")
        uiSettings.saveAll()
                
        
