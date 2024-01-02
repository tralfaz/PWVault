from pwvdoc    import PWVDoc
from pwvuicard import PWVCard
from pwvuicard import PWVEncodedCard

from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


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
        text, ok = QInputDialog.getText(self, title,
                                        "Password:",
                                        QLineEdit.EchoMode.Password)
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
        print(f"PSWD: {pswd}")

        status = self._pwvDoc.decrypt(pswd)
        print(f"STATUS: {status}")

        if status != "OK":
            QMessageBox.warning(self, status[0], status[1])
            return
    
        self._clearCards()

        self._buildCards()
        self.updateTitle()
        
    def encryptDoc(self):
        #msgBox = QMessageBox.information(self, "FOO", "BAR")
        if self.pwvDoc().encoded():
            QMessageBox.information(self, "FOO", "Vault is already encoded.")
            return

        pswd1 = self.queryPswd("Vault Password")
        print(f"PSWD: {pswd1}")
        pswd2 = self.queryPswd("Confirm Password")
        if pswd1 != pswd2:
            QMessageBox.warning(self, "XXX", "Passwords do not match.")
            return

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

    def saveFile(self, path=None):
        self._getCardValues()
        self._pwvDoc.saveDocAs(path)
        
    def _buildCards(self):
        if not self._pwvDoc.encoded():
            for entry in self._pwvDoc.entries():
                card = PWVCard(entry)
                self._cards.append(card)
                self._formLayout.addRow(card)
        else:
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
        if not self._pwvDoc.encoded():
            for entry in self._pwvDoc.entries():
                card = PWVCard(entry)
                self._cards.append(card)
                self._formLayout.addRow(card)

            nents = len(self._pwvDoc.entries())
        else:
            nents = 0
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
