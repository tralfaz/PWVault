from PyQt6.QtCore import QObject
from PyQt6.QtCore import QSettings

class PWVSettings(QObject):

    def __init__(self, pwvapp, parent=None):
        super().__init__(parent)
        self._app = pwvapp

        self._modified = False

        pwvapp.setOrganizationName("MiDoMa")
        pwvapp.setOrganizationDomain("midoma.com")
        pwvapp.setApplicationName("PWVault")

        self._settings = QSettings()

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
        if not self._modified:
            return
        self._settings.beginGroup(self._group)
        for key,val in self._cache.items():
            self._settings.setValue(key,val)
        self._settings.endGroup()
        self.setModified(False)

    def setValue(self, key, value):
        self._cache[key] = value
        self.setModified(True)

    def setModified(self, state):
        self._modified = state

    def value(self, key, defaultValue=None):
        return self._cache.get(key, defaultValue)



class PWVCliSettings(PWVSettings):

    def __init__(self, cliapp, parent=None):
        super().__init__(cliapp, parent)

        self._group = "PwvCliApp"


class PWVUiSettings(PWVSettings):

    APP_VIEW_THEME = "AppViewTheme"
    RECENT_OPENS   = "RecentOpens"
    
    def __init__(self, uiapp, parent=None):
        super().__init__(uiapp, parent)

        self._group = "PwvUiApp"

    def appViewTheme(self):
        theme = self._cache.get(self.APP_VIEW_THEME, "Dark")
        return theme

    def cardZoom(self, winName, zoomDelta=0):
        if not winName:
            return 0
        zoomKey = "CardZoom::" + winName
        zoomVal = self._cache.get(zoomKey,0) + zoomDelta
        self.setValue(zoomKey, zoomVal)
        return zoomVal

    def recentOpens(self):
        return self._cache.get(self.RECENT_OPENS, [])
    
    def setAppViewTheme(self, theme):
        theme = theme.lower()
        if theme == "light":
            self.setValue(self.APP_VIEW_THEME, "Light")
        elif theme == "dark":
            self.setValue(self.APP_VIEW_THEME, "Dark")
        elif theme == "system":
            self.setValue(self.APP_VIEW_THEME, "System")

    def setRecentOpens(self, recentOpens):
        self.setValue(self.RECENT_OPENS, recentOpens)
    
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
                
        
