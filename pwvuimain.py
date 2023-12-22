import sys

from pwvdoc    import PWVDoc
from pwvdoc    import PWVKey
from pwvuiapp    import PWVApp
from pwvuicard import PWVCard
from pwvuidocview import PWVDocView

from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QShortcut

#from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

    

class PWVMainWin(QMainWindow):

    def __init__(self):
        super().__init__()

        self._docViews = []
        
        self._mainDoc = PWVDoc()
        self._entryAdded = False
        
        self.setWindowIcon(QtGui.QIcon("vault.jpeg"))
        self.setWindowTitle("PWVault")
        self.setGeometry(200, 500, 600, 800)

        fileMenu = self.menuBar().addMenu("&File")

        newSC = QShortcut(QKeySequence("Ctrl+n"), self)
        newSC.activated.connect(self.fileMenuNewVaultCB)
        newVaultACT = QAction("&New Vault...", self)
        newVaultACT.triggered.connect(self.fileMenuNewVaultCB)
        fileMenu.addAction(newVaultACT)

        saveACT = QAction("&Save", self)
        saveACT.triggered.connect(self.fileMenuSaveCB)
        fileMenu.addAction(saveACT)
        
        saveAsACT = QAction("Save &As...", self)
        saveAsACT.triggered.connect(self.fileMenuSaveAsCB)
        fileMenu.addAction(saveAsACT)

        openSC = QShortcut(QKeySequence("Ctrl+o"), self)
        openSC.activated.connect(self.fileMenuOpenCB)
#        self.msgSc = QShortcut(QKeySequence('Ctrl+M'), self)
#        self.msgSc.activated.connect(lambda : QMessageBox.information(self,
#            'Message', 'Ctrl + M initiated'))
#        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
#        self.quitSc.activated.connect(QApplication.instance().quit)
        openACT = QAction("&Open...", self)
        openACT.triggered.connect(self.fileMenuOpenCB)
#        openACT.setShortcut(openSC)
        fileMenu.addAction(openACT)

        ctrWgt = QWidget()

        vbox = QVBoxLayout()

        self._formLayout = QFormLayout()
        groupBox = QGroupBox("This Is Group Box")

        docEnts = self._mainDoc.entries()
        for i in  range(10):
            entry = {
                PWVKey.ID : f"id - {i}",
                PWVKey.URL: f"url - {i}",
                PWVKey.USER : f"user - {i}",
                PWVKey.PSWD : f"pswd - {i}",
                PWVKey.NOTES: f"This is note {i}"
            }
            docEnts.append(entry)
        for entry in self._mainDoc.entries():
            card = PWVCard(entry)
            self._formLayout.addRow(card)

        groupBox.setLayout(self._formLayout)
        self._docScrollArea = scroll = QScrollArea()
        print("VBAR:", scroll.verticalScrollBar())
        scroll.verticalScrollBar().rangeChanged.connect(self._docScrollRangeCB)
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        vbox.addWidget(scroll)

        wgt = QPushButton("Add Card")
        wgt.clicked.connect(self._addEntryCB)
        vbox.addWidget(wgt)
        
        ctrWgt.setLayout(vbox)
        self.setCentralWidget(ctrWgt)

    def fileMenuNewVaultCB(self):
        print("fileMenNewVault...")
#        getSaveFileName(parent: QWidget = None, caption: Optional[str] = '', directory: Optional[str] = '', filter: Optional[str] = '', initialFilter: Optional[str] = '', options: Option = QFileDialog.Options()) → Tuple[str, str]
        fnames = QFileDialog.getSaveFileName(self, 'New Vault File', '',
                                             "*.pwv *.pwvx")
        print(f"FNAMES: {fnames}")
        if fnames:
            docView = PWVDocView()
            docView.setVisible(True)
            self._docViews.append(docView)
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
#        dialog.setNameFilter("*.pwv *.pwvx")
        dialog.setFilter(QtCore.QDir.Filter.Files)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("PWVDoc (*.pwv *.pwvx)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
#        fname, fset = dialog.getOpenFileName(self, caption=dlgcap)
#        if fname:
#            print(f"FNAME: {fname}")
#            print(f"FSET: {fset}")
        if dialog.exec():
            fnames = dialog.selectedFiles()
            print(f"FNAMES: {repr(fnames)}")
            pwvDoc = PWVDoc()
            pwvDoc.openDoc(fnames[0])
            print(f"{pwvDoc.entries()}")
            docView = PWVDocView(pwvDoc)
            docView.setVisible(True)
            self._docViews.append(docView)

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
            self._mainDoc.saveDocAs(fname)
               
    def fileMenuSaveCB(self):
        print("File-Save")
        x,y = QFileDialog.getSaveFileName(self, caption="Save current vault")
        #', directory: Optional[str] = '', filter: Optional[str] = '', initialFilter: Optional[str] = '', options: Option = QFileDialog.Options())
        print(repr(x))
        print(repr(y))

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

 
    def _docScrollRangeCB(self, xr, yr):
        print(f"_docScrollRangeCB({xr}, {yr})")
        print("FORM GEOM: ", self._formLayout.contentsRect())
        vbar = self._docScrollArea.verticalScrollBar()
        print("VBAR MAX:", vbar.maximum())
        if self._entryAdded:
            self._entryAdded = False
            vbar.setValue(vbar.maximum())

        
if __name__ == "__main__":
    from pwvuiapp import PWVApp

    app = PWVApp()

    mainW = PWVMainWin()
    mainW.show()

    status = app.exec()
    sys.exit(status)
