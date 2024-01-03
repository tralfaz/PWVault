from functools import partial
import sys

from pwvdoc    import PWVDoc
from pwvdoc    import PWVKey
from pwvuiapp  import PWVApp
from pwvuicard import PWVCard
from pwvuidocview import PWVDocView

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
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

    

class PWVMainWin(QMainWindow):

    def __init__(self):
        super().__init__()

        self._docWins = []
        
        self._currentDoc = None
        self._entryAdded = False
        
        self.setWindowIcon(QtGui.QIcon("vault.jpeg"))
        self.setWindowTitle("PWVault")
        self.setGeometry(200, 500, 800, 600)

#        self.msgSc = QShortcut(QKeySequence('Ctrl+M'), self)
#        self.msgSc.activated.connect(lambda : QMessageBox.information(self,
#            'Message', 'Ctrl + M initiated'))
#        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
#        self.quitSc.activated.connect(QApplication.instance().quit)

        self._docView = PWVDocView()
        self.setCentralWidget(self._docView)

        self._buildMenus()

        print(f"ARGV: {repr(sys.argv)}")
        if len(sys.argv) > 1:
            self._docView.openFile(sys.argv[1])

        self.addDocView(self)

    def addDocView(self, docView):
        self._docWins.append(docView)
        self.updateWindowsMenu()

    def decodeVault(self):
        """Public method to invoke _decodeVaultAction"""
        self._decodeVaultCB()
        
    def docView(self):
        """Return the document view associated with this top level window"""
        return self._docView

    def pwvDoc(self):
        """Return the PWVDoc object belonging to the PWVDocView"""
        return self._docView.pwvDoc()
        
    def fileMenuNewVaultCB(self):
        print("fileMenNewVault...")
#        getSaveFileName(parent: QWidget = None, caption: Optional[str] = '', directory: Optional[str] = '', filter: Optional[str] = '', initialFilter: Optional[str] = '', options: Option = QFileDialog.Options()) → Tuple[str, str]
        fnames = QFileDialog.getSaveFileName(self, 'New Vault File', '',
                                             "*.pwv *.pwvx")
        print(f"FNAMES: {fnames}")
        if fnames:
            docView = PWVDocView()
            docView.setVisible(True)
            self.addDocView(docView)
#        dialog = QFileDialog(self)
#        #dialog.setFileMode(QFileDialog.AnyFile)
#        dialog.setNameFilter(self.tr("PWVDoc (*.pwv *.pwvx)"))
#        dialog.setViewMode(QFileDialog.ViewMode.Detail)
#        if dialog.exec():
#            fileNames = dialog.selectedFiles()
#            print(f"FNAMES: {repr(fileNames)}")

    def fileMenuOpenCB(self):
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
            print(f"FNAMES: {repr(fnames)}")
            actWin = QApplication.instance().findActive()
            if not actWin.docView().pwvDoc().encoded() and \
               not actWin.docView().pwvDoc().entries():
                actWin.docView().openFile(fnames[0])
            else:
                pwvDoc = PWVDoc()
                pwvDoc.openDoc(fnames[0])
                docView = PWVDocView(pwvDoc)
                docView.setVisible(True)
                self._docWins.append(docView)
            self.updateWindowsMenu()
                
    def fileMenuSaveAsCB(self):
        print("fileMenuSaveAsCB")
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
        print("fileMenuSaveCB")
        actWin = QApplication.instance().findActive()
        docView = actWin.docView()
        print("DOCVIEW: ", docView)
        docPath = docView.pwvDoc().path()
        print(f"WIN DOC PATH {docPath}")
                
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
            print(f"CHOICE: {choice}")
            if  choice == "Keep":
                docView.encryptDoc(False)
            else:
                return

        docView.saveFile(docPath)
        docView.pwvDoc().setModified(False)
        docView.updateTitle()

    def queryPassword(self):
        text, ok = QInputDialog.getText(self, "Vault Password",
                                        "Password:",
                                        QLineEdit.EchoMode.Password)
# default input
#                                        QtCore.QDir.home().dirName())
        if ok and text:
            return text
        return None

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
        entry = {
            PWVKey.ID : f"Entry-{nents}",
                PWVKey.URL: f"url - {nents}",
                PWVKey.USER : f"user - {nents}",
                PWVKey.PSWD : f"pswd - {nents}",
                PWVKey.NOTES: f"This is note {nents}"
            }
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
        print("_appMenuQuitCB")
        PWVApp.instance().quit()
        
    def _buildMenus(self):
        print("_buildMenus")
        fileMenu = self.menuBar().addMenu("&File")

        quitAct = QAction("E&xit", self)
        quitAct.setShortcuts(QKeySequence.StandardKey.Quit)
        quitAct.setStatusTip("Quit PWVault")
        quitAct.triggered.connect(self._appMenuQuitCB)
        fileMenu.addAction(quitAct)
        
        newAct = QAction("&New...", self)
        newAct.setShortcuts(QKeySequence.StandardKey.New)
        newAct.setStatusTip("Create a new Password Vault Document...")
        newAct.triggered.connect(self.fileMenuNewVaultCB)
        fileMenu.addAction(newAct)
        
        openAct = QAction("&Open...", self)
        openAct.setShortcuts(QKeySequence.StandardKey.Open)
        openAct.setStatusTip("Open an existing file")
        openAct.triggered.connect(self.fileMenuOpenCB)
        fileMenu.addAction(openAct)

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

#        fileMenu.addSeparator()
#        fileMenu.addAction(self.exitAct)

        self._encodeMenu = self.menuBar().addMenu("Ecoding")
        
        self._decodeVaultAct = QAction("Decode Vault...", self)
        self._decodeVaultAct.setStatusTip("Decode current vault...")
        self._decodeVaultAct.triggered.connect(self._decodeVaultCB)
        self._encodeMenu.addAction(self._decodeVaultAct)

        self._encodeVaultAct = QAction("Encode Vault...", self)
        self._encodeVaultAct.setStatusTip("Encode current vault...")
        self._encodeVaultAct.triggered.connect(self._encodeVaultCB)
        self._encodeMenu.addAction(self._encodeVaultAct)

        self._winMenu = self.menuBar().addMenu("Windows")

    def _decodeVaultCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().decryptDoc()

    def _docScrollRangeCB(self, xr, yr):
        print(f"_docScrollRangeCB({xr}, {yr})")
        print("FORM GEOM: ", self._formLayout.contentsRect())
        vbar = self._docScrollArea.verticalScrollBar()
        print("VBAR MAX:", vbar.maximum())
        if self._entryAdded:
            self._entryAdded = False
            vbar.setValue(vbar.maximum())

    def _encodeVaultCB(self):
        actWin = QApplication.instance().findActive()
        actWin.docView().encryptDoc()

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
        print(f"_winMenuCB {docView}")
        docView.activateWindow()
        docView.raise_()


if __name__ == "__main__":
    from pwvuiapp import PWVApp

    app = PWVApp()

    mainW = PWVMainWin()
    mainW.show()

    status = app.exec()
    sys.exit(status)
