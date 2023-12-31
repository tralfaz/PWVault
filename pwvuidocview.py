from pwvdoc    import PWVDoc
from pwvuicard import PWVCard

from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QGroupBox
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

    def docView(self):
        return self

    def pwvDoc(self):
        return self._pwvDoc
    
    def updateEntriesCounter(self):
        self._entriesGRP.setTitle(f"Entries: {len(self._pwvDoc.entries())}")

    def updateTitle(self):
        title = "PWVault: "
        fname = self._pwvDoc.fileName()
        if not fname:
            fname = "<New Vault>"
#        print(f"updateTitle: {self._pwvDoc.modified()}")
        if self._pwvDoc.modified():
            fname = f"* {fname} *"
#        print(self.parent())
        if self.parent():
            self.parent().setWindowTitle(title + fname)
        else:
            self.setWindowTitle(title + fname)

    def addEntry(self):
        self._entryAdded = True
        nents = len(self._pwvDoc.entries())
        entry = self._pwvDoc.newEntry()
        self._pwvDoc.appendEntries([entry])
        card = PWVCard(entry)
        selrf._cards.append(card)
        vbar = self._docScrollArea.verticalScrollBar()
        saRect = self._formLayout.contentsRect()
        self._formLayout.addRow(card)
        cardGeom = card.geometry()
        self.updateEntriesCounter()
        self.updateTitle()
        
    def openFile(self, path=None):
        self._pwvDoc.openDoc(path)
        self._buildCards()
        self.updateEntriesCounter()
        self.updateTitle()

    def saveFile(self, path=None):
        self._getCardValues()
        self._pwvDoc.saveDocAs(path)
        
    def _buildCards(self):
        for entry in self._pwvDoc.entries():
            card = PWVCard(entry)
            self._cards.append(card)
            self._formLayout.addRow(card)
        self.updateEntriesCounter()
        self.updateTitle()

    def _buildDocWindow(self):
        self._formLayout = QFormLayout()
        self._formLayout.setContentsMargins(0, 0, 0, 0)
        for entry in self._pwvDoc.entries():
            card = PWVCard(entry)
            self._cards.append(card)
            self._formLayout.addRow(card)

        nents = len(self._pwvDoc.entries())
        self._entriesGRP = QGroupBox(f"Entries: {nents}")

        cards = QWidget()
        cards.setLayout(self._formLayout)
        
        self._docScrollArea = scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.verticalScrollBar().rangeChanged.connect(self._docScrollRangeCB)
#        scroll.setWidget(self._entriesGRP)
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
