from functools import partial
import os
import sys

from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QShortcut
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
#from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from pwvdoc       import PWVDoc
from pwvdoc       import PWVKey
from pwvuiapp     import PWVApp
from pwvuicard    import PWVCard
from pwvuidocview import PWVDocView
from pwvuipswd    import PWVGeneratePswdDialog

    

class PWVMainWin(QMainWindow):

    def __init__(self):
        super().__init__()

        self._docWins = []
        
        self._currentDoc = None
        self._entryAdded = False
        
        self.setWindowIcon(QtGui.QIcon("vault.jpeg"))
        self.setWindowTitle("PWVault")
        self.setGeometry(200, 500, 800, 600)

        self._docView = PWVDocView()
        self.setCentralWidget(self._docView)

        self._buildMenus()

        if len(sys.argv) > 1:
            self._docView.openFile(sys.argv[1])

        self.addDocView(self)

#        self.setStatusBar(QStatusBar(self))

    def addDocView(self, docView):
        self._docWins.append(docView)
        self.updateWindowsMenu()

    def decodeVault(self):
        """Public method to invoke _decodeVaultAction"""
        self._decodeVaultCB()
        
    def docView(self):
        """Return the document view associated with this top level window"""
        return self._docView

    def openVaultPath(self, path):
        actWin = QApplication.instance().findActive()
        if not actWin.docView().pwvDoc().encoded() and \
           not actWin.docView().pwvDoc().entries():
            actWin.docView().openFile(path)
        else:
            docView = PWVDocView()
            docView.setVisible(True)
            docView.openFile(path)
            self.addDocView(docView)
        self.updateWindowsMenu()

    def pwvDoc(self):
        """Return the PWVDoc object belonging to the PWVDocView"""
        return self._docView.pwvDoc()
        
    def fileMenuSaveAsCB(self):
#       __init__(parent: QWidget = None, caption: Optional[str] = '', directory: Optional[str] = '', filter: Optional[str] = '')
        dlgcap = "Save Current Vault As..."
        dialog = QFileDialog(self, caption=dlgcap,
                             directory="", filter="*.pwv")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setNameFilter("PWVDoc (*.pwv *.pwvx)")
        fname, fset = dialog.getSaveFileName(self, caption=dlgcap)
        if fname:
            print(f"FNAME: {fname}")
            print(f"FSET: {fset}")
            actWin = QApplication.instance().findActive()
            if actWin:
                actWin.docView().pwvDoc().saveDocAs(fname)
               
    def fileMenuSaveCB(self):
        actWin = QApplication.instance().findActive()
        docView = actWin.docView()
        docPath = docView.pwvDoc().path()
                
        if not docPath:
            dlgcap = "Save current vault"
            docPath,fset = QFileDialog.getSaveFileName(self, caption=dlgcap)
            if not docPath:
                # canceled
                return

        if not docPath.endswith(".pwv") and not docPath.endswith(".pwvx"):
            docPath += ".pwv"

        if docView.pwvDoc().wasDecoded():
            choice = self._saveWasDecodedDialog()
            if  choice == "Keep":
                docView.encryptDoc(False)
            else:
                return

        docView.saveFile(docPath)
        docView.pwvDoc().setModified(False)
        docView.updateTitle()

    def removeDocView(self, docView):
        if docView in self._docWins:
            self._docWins.remove(docView)
            self.updateWindowsMenu()

    def updateWindowsMenu(self):
        self._winMenu.clear()
        for dvx, docView in enumerate(self._docWins):
            actName = docView.pwvDoc().fileName()
            if not actName:
                actName = "<New Vault>"
            winAct = QAction(actName, self)
            winAct.setShortcut(QKeySequence(f"Ctrl+{dvx}"))
            winAct.setStatusTip(f"Make window {actName} active")
            winAct.triggered.connect(partial(self._winMenuCB, docView))
            self._winMenu.addAction(winAct)

    def _addEntryCB(self):
        self._entryAdded = True
        docEnts = self._mainDoc.entries()
        nents = len(docEnts)
        entry = { PWVKey.ID : f"Entry-{nents}",
                  PWVKey.URL: f"url - {nents}",
                  PWVKey.USER : f"user - {nents}",
                  PWVKey.PSWD : f"pswd - {nents}",
                  PWVKey.NOTES: f"This is note {nents}" }

        docEnts.append(entry)
        card = PWVCard(entry)
        vbar = self._docScrollArea.verticalScrollBar()
        print("PRE ADD: ", self._formLayout.contentsRect())
        print("PRE ADD W GEOM:", card.geometry())
        print("PRE VBAR MAX:", vbar.maximum())
        saRect = self._formLayout.contentsRect()
        self._formLayout.addRow(card)
        print("POST ADD: ", self._formLayout.contentsRect())
        cardGeom = card.geometry()
        print("POST ADD W GEOM:", card.geometry())
        print("POST VBAR MAX:", vbar.maximum())

    def _activeChangeCB(self):
        print("MainWin._activeChangeCB)")
        print(f"isActive: {self.isActive()}")
        
    def _appMenuQuitCB(self):
        status = self._askToSaveAllDocs()
        if status == "CANCEL":
            return
        PWVApp.instance().quit()
        
    def _askToSaveAllDocs(self):
        status = None
        for docw in self._docWins:
            if docw.docView().pwvDoc().modified():
                status = self._askToSaveDoc(docw)
                print(f"_askToSaveAllDocs: {docw.docView().pwvDoc().fileName()} status={status}")
                if status == "CANCEL":
                    return "CANCEL"
                elif status == "DISCARD":
                    docw.pwvDoc().setModified(False)
                    self.removeDocView(docw)
                    docw.close()
        return status

    def _askToSaveDoc(self, docw):
        fname = docw.docView().pwvDoc().fileName()
        msgBox = QMessageBox(docw)
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setText(f"The document {fname} has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        stdbtn = QMessageBox.StandardButton
        msgBox.setStandardButtons(stdbtn.Save | stdbtn.Discard | stdbtn.Cancel)
        msgBox.setDefaultButton(stdbtn.Save)
        status = msgBox.exec()
        if status == stdbtn.Save:
            docStatus = docw.docView().saveDocument()
            if docStatus == "CANCELED":
                return "CANCEL"
            else:
                return "SAVED"
        elif status == stdbtn.Discard:
            return "DISCARD"
        elif status == stdbtn.Cancel:
            return "CANCEL"

    def _buildMenus(self):
        # File menu
        fileMenu = self.menuBar().addMenu("&File")
        quitAct = QAction("E&xit", self)
        quitAct.setShortcuts(QKeySequence.StandardKey.Quit)
        quitAct.setStatusTip("Quit PWVault")
        quitAct.triggered.connect(self._appMenuQuitCB)
        fileMenu.addAction(quitAct)
        newAct = QAction("&New...", self)
        newAct.setShortcuts(QKeySequence.StandardKey.New)
        newAct.setStatusTip("Create a new Password Vault Document...")
        newAct.triggered.connect(self._menuFileNewCB)
        fileMenu.addAction(newAct)
        openAct = QAction("&Open...", self)
        openAct.setShortcuts(QKeySequence.StandardKey.Open)
        openAct.setStatusTip("Open an existing file")
        openAct.triggered.connect(self._menuFileOpenCB)
        fileMenu.addAction(openAct)
        self._buildOpenRecents(fileMenu)
        saveAct = QAction("Save...", self)
        saveAct.setShortcuts(QKeySequence.StandardKey.Save)
        saveAct.setStatusTip("Save curren vault")
        saveAct.triggered.connect(self.fileMenuSaveCB)
        fileMenu.addAction(saveAct)
        saveAsAct = QAction("Save As...", self)
        saveAsAct.setShortcuts(QKeySequence.StandardKey.SaveAs)
        saveAsAct.setStatusTip("Save current vault as...")
        saveAsAct.triggered.connect(self.fileMenuSaveAsCB)
        fileMenu.addAction(saveAsAct)

        # Edit menu
        editMenu = self.menuBar().addMenu("Edit")
        cutAct = QAction("Cut", self)
        cutAct.setShortcuts(QKeySequence.StandardKey.Cut)
        cutAct.setStatusTip("Cut selected entries")
        cutAct.triggered.connect(self._menuEditCutCB)
        editMenu.addAction(cutAct)
        undoAct = QAction("Cut", self)
        undoAct.setShortcuts(QKeySequence.StandardKey.Undo)
        undoAct.setStatusTip("Undo prior changes")
        undoAct.triggered.connect(self._menuEditUndoCB)
        editMenu.addAction(undoAct)
        addEntryAlt = QAction("Add  Entry", self)
        addEntryAlt.setShortcut(QKeySequence("Ctrl+e"))
        addEntryAlt.setStatusTip("Add new entry")
        addEntryAlt.triggered.connect(self._menuEditAddEntryCB)
        editMenu.addAction(addEntryAlt)

        # Arrange menu
        self._arrangeMenu = self.menuBar().addMenu("Arrange")
        self._arrangeStartAct = QAction("Move to start", self)
        self._arrangeStartAct.setStatusTip("Move selected start of entries.")
        self._arrangeStartAct.setShortcut(QKeySequence("Ctrl+Home"))
        self._arrangeStartAct.triggered.connect(self._menuArrangeStartCB)
        self._arrangeMenu.addAction(self._arrangeStartAct)
        self._arrangeUpAct = QAction("Move Up", self)
        self._arrangeUpAct.setStatusTip("Move selected up 1 position.")
        self._arrangeUpAct.setShortcut(QKeySequence("Ctrl+Up"))
        self._arrangeUpAct.triggered.connect(self._menuArrangeUpCB)
        self._arrangeMenu.addAction(self._arrangeUpAct)
        self._arrangeDownAct = QAction("Move Down", self)
        self._arrangeDownAct.setStatusTip("Move selected up 1 position.")
        self._arrangeDownAct.setShortcut(QKeySequence("Ctrl+Down"))
        self._arrangeDownAct.triggered.connect(self._menuArrangeDownCB)
        self._arrangeMenu.addAction(self._arrangeDownAct)
        self._arrangeEndAct = QAction("Move to end", self)
        self._arrangeEndAct.setStatusTip("Move selected end of entries.")
        self._arrangeEndAct.setShortcut(QKeySequence("Ctrl+End"))
        self._arrangeEndAct.triggered.connect(self._menuArrangeEndCB)
        self._arrangeMenu.addAction(self._arrangeEndAct)
        
        # Encode menu
        self._encodeMenu = self.menuBar().addMenu("Encoding")
        self._decodeVaultAct = QAction("Decode Vault...", self)
        self._decodeVaultAct.setStatusTip("Decode current vault...")
        self._decodeVaultAct.setShortcut(QKeySequence("Ctrl+="))
        self._decodeVaultAct.triggered.connect(self._decodeVaultCB)
        self._encodeMenu.addAction(self._decodeVaultAct)
        self._encodeVaultAct = QAction("Encode Vault...", self)
        self._encodeVaultAct.setStatusTip("Encode current vault...")
        self._encodeVaultAct.setShortcut(QKeySequence("Ctrl+~"))
        self._encodeVaultAct.triggered.connect(self._encodeVaultCB)
        self._encodeMenu.addAction(self._encodeVaultAct)
        self._genPswdAct = QAction("Generate Password...", self)
        self._genPswdAct.setStatusTip("Generate secure password.")
        self._genPswdAct.setShortcut(QKeySequence("Ctrl+g"))
        self._genPswdAct.triggered.connect(self._generatePswdCB)
        self._encodeMenu.addAction(self._genPswdAct)

        # View menu
        theme = PWVApp.instance().settings().appViewTheme()
        self._viewMenu = self.menuBar().addMenu("View")
        self._zoomPlusAct = QAction("Zoom In", self)
        self._zoomPlusAct.setStatusTip("Increase Font Size")
        self._zoomPlusAct.setShortcut(QKeySequence("Ctrl++"))
        self._zoomPlusAct.triggered.connect(self._menuZoomPlusCB)
        self._viewMenu.addAction(self._zoomPlusAct)
        self._zoomMinusAct = QAction("Zoom Out", self)
        self._zoomMinusAct.setStatusTip("Decrease Font Size")
        self._zoomMinusAct.setShortcut(QKeySequence("Ctrl+-"))
        self._zoomMinusAct.triggered.connect(self._menuZoomMinusCB)
        self._viewMenu.addAction(self._zoomMinusAct)
        self._themeMenu = self._viewMenu.addMenu("Theme")
        self._themeLightAct = QAction("Light", self)
        self._themeLightAct.setStatusTip("Light color theme")
        self._themeLightAct.setCheckable(True)
        self._themeLightAct.setChecked(theme == "Light")
        self._themeLightAct.triggered.connect(self._menuViewThemeLightCB)
        self._themeMenu.addAction(self._themeLightAct)
        self._themeDarkAct = QAction("Dark", self)
        self._themeDarkAct.setCheckable(True)
        self._themeDarkAct.setChecked(theme == "Dark")
        self._themeDarkAct.setStatusTip("Dark color theme")
        self._themeDarkAct.triggered.connect(self._menuViewThemeDarkCB)
        self._themeMenu.addAction(self._themeDarkAct)
        
        # Windows menu
        self._winMenu = self.menuBar().addMenu("Windows")

    def _buildOpenRecents(self, fileMenu):
        recents = PWVApp.instance().recentFileOpens()
        if not recents:
            return
        recents.reverse()
        self._recentOpenActs = {}
        recentMenu = fileMenu.addMenu("Recent Opens")
        for path in recents:
            recentAct = QAction(path)
            recentAct.triggered.connect(partial(self._menuFileOpenRecentCB,path))
            recentMenu.addAction(recentAct)
            self._recentOpenActs[recentAct] = path

    def _decodeVaultCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().decryptDoc()

    def _docScrollRangeCB(self, xr, yr):
#        print("FORM GEOM: ", self._formLayout.contentsRect())
        vbar = self._docScrollArea.verticalScrollBar()
#        print("VBAR MAX:", vbar.maximum())
        if self._entryAdded:
            self._entryAdded = False
            vbar.setValue(vbar.maximum())

    def _encodeVaultCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().encryptDoc()

    def _generatePswdCB(self):
        actWin = QApplication.instance().findActive()
        title = "Generate Secure Password"
        prompt = "Choose generation options then click Generate"

        pswd, ok = PWVGeneratePswdDialog.getPassword(actWin, title, prompt)

    def _menuArrangeDownCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().arrangeDown()

    def _menuArrangeEndCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().arrangeEnd()

    def _menuArrangeStartCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().arrangeStart()

    def _menuArrangeUpCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().arrangeUp()

    def _menuEditCutCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().deleteSelection()

    def _menuEditUndoCB(self):
        actWin = QApplication.instance().findActive()
        title = "<H2>Not Working Yet!</H2>"
        msgBox = QMessageBox(QMessageBox.Icon.Warning,
                             title,
                             title + "<P>That function is not yet working.</P>",
                             QMessageBox.StandardButton.Ok, actWin)
        info = """That feature is not implement yet.  Bummer!"""
        msgBox.setInformativeText(info)
        msgBox.exec()

    def _menuEditAddEntryCB(self):
        actWin = QApplication.instance().findActive()
        docView = actWin.docView()
        if docView.pwvDoc().encoded():
            return
        docView.addEntry()

    def _menuFileNewCB(self):
        docView = PWVDocView()
        docView.setVisible(True)
        self.addDocView(docView)

    def _menuFileOpenCB(self):
        dlgcap = "Open Vault..."
        dialog = QFileDialog(self, caption=dlgcap,
                             directory="", filter="*.pwv")
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
        dialog.setFilter(QtCore.QDir.Filter.Files)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("PWVDoc (*.pwv *.pwvx)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if dialog.exec():
            fnames = dialog.selectedFiles()
            self.openVaultPath(fnames[0])

    def _menuFileOpenRecentCB(self, path):
        if not os.path.exists(path):
            QMessageBox.warning(self, "File Not Found",
                                f"The path {path} does not exist")
            return
        self.openVaultPath(path)
        
    def _menuViewThemeDarkCB(self):
        print("_menuViewThemeDarkCB")
        PWVApp.instance().settings().setAppViewTheme("Dark")
        
    def _menuViewThemeLightCB(self):
        print("_menuViewThemeLightCB")
        PWVApp.instance().settings().setAppViewTheme("Light")
        
    def _menuZoomMinusCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().zoomCards(-1)

    def _menuZoomPlusCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().zoomCards(1)

    def _saveWasDecodedDialog(self):
        title = "<H2>Was Encoded</H2>"
        msgBox = QMessageBox(QMessageBox.Icon.Warning,
                             title,
                             title + "<P>Choose save mode.</P>",
                             QMessageBox.StandardButton.NoButton, self)
        info = """<B>Keep</B>, save with previous encoding<P>
<B>Recode</B>, save with different encoding<P>
<B>Clear</B>, save with no encoding"""
        msgBox.setInformativeText(info)
#        msgBox.setDetailedText('"A long time ago in a galaxy far, far away...."')
        keepBTN   = msgBox.addButton("&Keep", QMessageBox.ButtonRole.AcceptRole)
        recodeBTN = msgBox.addButton("Recode", QMessageBox.ButtonRole.ResetRole)
        clearBTN = msgBox.addButton("Clear", QMessageBox.ButtonRole.DestructiveRole)
        cancelBTN = msgBox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msgBox.exec()
        dlgBTN = msgBox.clickedButton()
        if dlgBTN == keepBTN:
            return "Keep"
        elif dlgBTN == recodeBTN:
            return "Recode"
        elif dlgBTN == clearBTN:
            return "Clear"
        else:
            return "Cancel"

    def _winMenuCB(self, docView):
#        print(f"_winMenuCB {docView}")
        docView.activateWindow()
        docView.raise_()

### BEGIN EVENT HANDLERS

    def closeEvent(self, qev):
        """Handle main window closure safely"""
        if self.pwvDoc().modified():
            status = self._askToSaveDoc(self)
            if status == "CANCEL":
                qev.ignore()
            elif status == "DISCARD":
                self.pwvDoc().setModified(False)
                self.removeDocView(self)
        # Save app settings
        stgmgr = PWVApp.instance().settings()
        stgmgr.saveAll()

### END EVENT HANDLERS


if __name__ == "__main__":
    from pwvuiapp import PWVApp

    with open("/Users/mdm/pwvault.log", "w") as logFP:
        print(f"{sys.argv}", file=logFP)

    app = PWVApp()

    mainW = PWVMainWin()
    mainW.show()

    status = app.exec()
    sys.exit(status)
