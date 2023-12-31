from PyQt6           import QtCore
from PyQt6.QtWidgets import QCompleter
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from pwvuiapp  import PWVApp
from pwvdoc    import PWVDoc
from pwvuipswd import PWVPswdDialog
from pwvuicard import PWVCard
from pwvuicard import PWVEncodedCard



class PWVDocView(QWidget):

    def __init__(self, pwvDoc=None):
        super().__init__(None)

        self.setGeometry(200, 200, 800, 600)
        
        self._pwvDoc = pwvDoc
        if not self._pwvDoc:
            self._pwvDoc = PWVDoc()
            self.setWindowTitle("PWVault: <New Vault>")
        else:
            fname = self._pwvDoc.fileName()
            self.setWindowTitle(f"PWVault: {fname}")

        self._entryAdded = False

        self._cards= []
        self._buildDocWindow()

    def addEntry(self):
        self._entryAdded = True
        nents = len(self._pwvDoc.entries())
        entry = self._pwvDoc.newEntry()
        self._pwvDoc.appendEntries([entry])
        card = PWVCard(entry)
        self._cards.append(card)
        vbar = self._docScrollArea.verticalScrollBar()
        saRect = self._formLayout.contentsRect()
        self._formLayout.addRow(card)
        cardGeom = card.geometry()
        self.updateEntriesCounter()
        self.updateTitle()

    def docView(self):
        return self

    def pwvDoc(self):
        return self._pwvDoc
    
    def queryPswd(self, title):
#        text, ok = QInputDialog.getText(self, title,
#                                        "Password:",
#                                        QLineEdit.EchoMode.Password)
        text, ok = PWVPswdDialog.getText(self, title, "Password:")
        if ok and text:
            return text
        return None
    
    def updateEntriesCounter(self):
        nents = 0
        if self._pwvDoc.entries():
            nents = len(self._pwvDoc.entries())
        self._entriesGRP.setTitle(f"Entries: {nents}")

    def updateTitle(self):
        title = "PWVault: "
        fname = self._pwvDoc.fileName()
        if not fname:
            fname = "<New Vault>"
#        print(f"updateTitle: {self._pwvDoc.modified()}")
        if self._pwvDoc.modified():
            fname = f"* {fname} *"
        encoded = " (ENCODED)" if self._pwvDoc.encoded() else ""
        if self.parent():
            self.parent().setWindowTitle(title + fname + encoded)
        else:
            self.setWindowTitle(title + fname + encoded)

    def decryptDoc(self):
        if not self.pwvDoc().encoded():
            QMessageBox.information(self, "FOO", "Vault is not encoded.")
            return

        pswd = self.queryPswd("Vault Password")
        if not pswd:
            return

        status = self._pwvDoc.decrypt(pswd)

        if status != "OK":
            QMessageBox.warning(self, status[0], status[1])
            return
    
        self._clearCards()

        self._buildCards()
        self.updateTitle()
        
    def encryptDoc(self, recode=True):
        #msgBox = QMessageBox.information(self, "FOO", "BAR")
        if self.pwvDoc().encoded():
            QMessageBox.information(self, "FOO", "Vault is already encoded.")
            return

        if recode or not self._pwvDoc.wasDecoded():
            pswd1 = self.queryPswd("Vault Password")
            if not pswd1:
                return
            pswd2 = self.queryPswd("Confirm Password")
            if pswd1 != pswd2:
                QMessageBox.warning(self, "XXX", "Passwords do not match.")
                return
        else:
            pswd1 = None

#        self._getCardValues()
        self._pwvDoc.encrypt(pswd1)
        pswd1 = pswd2 = None
        
        self._clearCards()
        self._buildCards()
        
        self.updateTitle()
        self.updateEntriesCounter()
        
    def openFile(self, path=None):
        self._pwvDoc.openDoc(path)
        self._buildCards()
        self.updateEntriesCounter()
        self.updateTitle()


    def saveDocument(self):
        docPath = self.pwvDoc().path()
        if not docPath:
            dlgcap = "Save current vault"
            docPath,fset = QFileDialog.getSaveFileName(self, caption=dlgcap)
            if not docPath:
                # canceled
                return "CANCELED"

        if not docPath.endswith(".pwv") and not docPath.endswith(".pwvx"):
            docPath += ".pwv"

        if self.pwvDoc().wasDecoded():
            self.encryptDoc(False)
    
        self.saveFile(docPath)
        self.pwvDoc().setModified(False)
        self.updateTitle()
        return "SAVED"
############
        
    def saveFile(self, path=None):
#        self._getCardValues()
        self._pwvDoc.saveDocAs(path)
        
    def _buildCards(self):
        if not self._pwvDoc.encoded():
            self._searchLE.setVisible(True)
            for entry in self._pwvDoc.entries():
                card = PWVCard(entry)
                self._cards.append(card)
                self._formLayout.addRow(card)
            self._searchMODL.setStringList(self._pwvDoc.searchCompletions())

        else:
            self._searchLE.setVisible(False)
            card = PWVEncodedCard()
#            self._cards.append(card)
            self._formLayout.addRow(card)

        self.updateEntriesCounter()
        self.updateTitle()

    def _clearCards(self):
        self._cards.clear()
        for cdx in range(self._formLayout.count()-1, -1, -1):
            self._formLayout.removeRow(cdx)

    def _buildDocWindow(self):
        self._formLayout = QFormLayout()
        self._formLayout.setContentsMargins(0, 0, 0, 0)
        self._searchLE = QLineEdit()
        self._searchLE.setPlaceholderText("Search Entries, Start with ~ for complete search")
        self._searchLE.textChanged.connect(self._searchCB)

        actPos = QLineEdit.ActionPosition.TrailingPosition
        searchIcon = PWVApp.instance().asset("search-icon-yellow")
        self._searchACT = self._searchLE.addAction(searchIcon, actPos)
        self._searchACT.triggered.connect(self._searchActCB)
#        self._searchACT.setEnabled(True)
        
        # Adding Completer.
        self._searchMODL = QtCore.QStringListModel()
        self._searchMODL.setStringList(self._pwvDoc.searchCompletions())
        self._searchCMPL = QCompleter(self._searchMODL, self._searchLE)
        self._searchCMPL.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self._searchLE.setCompleter(self._searchCMPL)

        if not self._pwvDoc.encoded():
            self._searchLE.setVisible(True)
            for entry in self._pwvDoc.entries():
                card = PWVCard(entry)
                self._cards.append(card)
                self._formLayout.addRow(card)

            nents = len(self._pwvDoc.entries())
        else:
            nents = 0
            print("_searchLE.setVisible(False)")
            self._searchLE.setVisible(False)
            card = PWVEncodedCard()
#            self._cards.append(card)
            self._formLayout.addRow(card)
            
        self._entriesGRP = QGroupBox(f"Entries: {nents}")
 
        cards = QWidget()
        cards.setLayout(self._formLayout)
        
        self._docScrollArea = scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.verticalScrollBar().rangeChanged.connect(self._docScrollRangeCB)
        scroll.setWidget(cards)

        self._addEntryBTN = QPushButton("+")
        self._addEntryBTN.clicked.connect(self.addEntry)

        vbox = QVBoxLayout()
        vbox.addWidget(self._searchLE)
        vbox.addWidget(self._entriesGRP)
        vbox.addWidget(scroll)
        vbox.addWidget(self._addEntryBTN)
        self.setLayout(vbox)
        
    def _docScrollRangeCB(self, xr, yr):
        vbar = self._docScrollArea.verticalScrollBar()
        if self._entryAdded:
            self._entryAdded = False
            vbar.setValue(vbar.maximum())

    def _getCardValues(self):
        print(f"_getCardValues RC: {len(self._cards)}")
        for card in  self._cards:
            card.entryUpdate()

    def _searchActCB(self):
        print("_searchActCB")

    def _searchCB(self, text):
        fullSearch = False
        if text.startswith("%"):
            fullSearch = True
            text = text[1:]
        for card in self._cards:
            card.setVisible(card.searchMatch(text, fullSearch))

