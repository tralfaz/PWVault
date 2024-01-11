from functools import partial
import sys
 
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QFormLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from pwvdoc    import PWVKey
from pwvuiapp  import PWVApp
from pwvuipswd import PWVPswdLabel
from pwvuipswd import PWVPswdLineEdit



class PWVCardField(QWidget):

    def __init__(self, parent=None, id="", val="", fmt=None,  spaces=None,
                 ctrls="CE", url=False, pswd=False):
        super().__init__(parent)

        self._valPlain   = val
        self._valFormat  = fmt
        self._valUrl     = url
        
        self._idLBL  = QLabel(f"<big><b>{id}:</b></big>")
        if pswd:
            self._valLBL = PWVPswdLabel(val)
        else: 
            self._valLBL = QLabel(val)
        if fmt and not url:
            self._valLBL.setText(fmt.format(val))
        elif url:
            self.setURL(val)
            self._valLBL.setOpenExternalLinks(url)
            self._valLBL.setWordWrap(True)
            self._valLBL.setMinimumWidth(400)
            self._valLBL.setMaximumWidth(600)
        if pswd:
            self._valLE  = PWVPswdLineEdit()
        else:
            self._valLE  = QLineEdit()
        self._valLE.setVisible(False)
        self._valLE.editingFinished.connect(self._editDoneCB)
        icon = PWVApp.instance().asset("copy-button-icon")
        self._copyBTN = QPushButton()
        self._copyBTN.setFlat(True)
        self._copyBTN.setIcon(icon)
        self._copyBTN.clicked.connect(self._copyCB)
        self._copyBTN.setVisible('C' in ctrls)
            
        icon = PWVApp.instance().asset("edit-button-icon")
        self._editBTN = QPushButton()
        self._editBTN.setFlat(True)
        self._editBTN.setIcon(icon)
        self._editBTN.clicked.connect(self._editCB)
        self._editBTN.setVisible('E' in ctrls)

        if not spaces:
            spaces = (5, 0)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self._idLBL)
        hbox.addSpacing(spaces[0])
        hbox.addWidget(self._valLBL)
        hbox.addWidget(self._valLE)
        hbox.addStretch()
        hbox.addWidget(self._copyBTN)
        hbox.addWidget(self._editBTN)
        self.setLayout(hbox)

    def addEditDoneCallback(self, func, *args):
        self._valLE.editingFinished.connect(partial(func, self, *args))

    def plainText(self):
        return self._valPlain

    def richText(self):
        return self._valLBL.text()

    def setURL(self, url):
        self._valPlain = url
        self._valURL   = True
        self._valLBL.setOpenExternalLinks(True)
        self._valLBL.setText(f'<A HREF="{url}">{url}</A>')

    def setValueLabel(self, plain, richFmt=None):
        """Set the plain text and formated rich text value part of the field
        edit row.  The plain text value will be interpolated into the rich
        text label with {0} field."""
        self._plainText = plain
        self._valFormat = richFmt
        if self._valFormat:
            lbltxt = self._valFormat.format(self._plainText)
        else:
            lbltxt = self._plainText
        self._valLBL.setText(lbltxt)
        
    def urlText(self):
        return f'<A HREF="{self._plainText}">{self._plainText}</A>'

    def zoom(self, pointDelta):
        font = self._idLBL.font()
        font.setPointSize(font.pointSize()+pointDelta)
        self._idLBL.setFont(font)
        font = self._valLBL.font()
        font.setPointSize(font.pointSize()+pointDelta)
        self._valLBL.setFont(font)
        font = self._valLE.font()
        font.setPointSize(font.pointSize()+pointDelta)
        self._valLE.setFont(font)

    def _copyCB(self):
        clipb = QApplication.clipboard()
        clipb.setText(self._valPlain)
    
    def _editCB(self):
        print("PWVFieldEdit._editCB")
        self._valLBL.setVisible(False)
        self._valLE.setText(self._valPlain)
        self._valLE.setVisible(True)
        self._valLE.setFocus()
        self._valLE.selectAll()

    def _editDoneCB(self):
        newtxt = self._valLE.text()
        if self._valUrl:
            self.setURL(newtxt)
        elif self._valFormat:
            self._valLBL.setText(self._valFormat.format(newtxt))
        else:
            self._valLBL.setText(newtxt)            
        self._valPlain = newtxt
        self._valLBL.setVisible(True)
        self._valLE.setVisible(False)
        #MOVE
        self.window().docView().pwvDoc().setModified(True)
        self.window().docView().updateTitle()
# END PWVCardField


class PWVCard(QFrame):

    def __init__(self, entry):
        super().__init__()

        self._entry = entry

        self._expanded = False

        self.setLineWidth(5)
        self.setProperty("selected", "false")
        self._setStyle()
        
        self._entry = entry

        copyICO = QtGui.QIcon("copy-button-icon.png")

        vbox = QVBoxLayout()
        vbox.setSpacing(0)

        eid = entry.get(PWVKey.ID,"<I>Missing: ID</I>")
        self._idCF = PWVCardField(id="ID", val=eid, ctrls="CE",
                                  fmt='<b><font color="white">{0}</font></b>')
        self._idCF.addEditDoneCallback(self._cfEditDoneCB, entry, PWVKey.ID)
        vbox.addWidget(self._idCF)
        
        eurl = entry.get(PWVKey.URL, "<I>Missing: URL</I>")
        self._urlCF = PWVCardField(id="URL", val=eurl, url=True, ctrls="CE")
        self._urlCF.addEditDoneCallback(self._cfEditDoneCB, entry, PWVKey.URL)
        vbox.addWidget(self._urlCF)
        
        euser = entry.get(PWVKey.USER, "<I>Missing: USER</I>")
        upfmt = '<b><font color="yellow">{0}</font></b>'
        self._userCF = PWVCardField(id="USER", val=euser, fmt=upfmt, ctrls="CE")
        self._userCF.addEditDoneCallback(self._cfEditDoneCB, entry, PWVKey.USER)
        vbox.addWidget(self._userCF)
        
        epswd = entry.get(PWVKey.PSWD, "<I>Missing: PSWD</I>")
        self._pswdCF = PWVCardField(id="PSWD", val=epswd, ctrls="CE", pswd=True)
        self._pswdCF.addEditDoneCallback(self._cfEditDoneCB, entry, PWVKey.PSWD)
        vbox.addWidget(self._pswdCF)

        expVbox = QVBoxLayout()
        self._notesGRP = QGroupBox("NOTES:")
        self._notesGRP.setLayout(expVbox)
        self._notesGRP.setVisible(False)
        enotes = entry.get(PWVKey.NOTES, "")
        self._notesTXT = QTextEdit()
        self._notesTXT.setText(enotes)
        self._notesTXT.textChanged.connect(self._notesChangedCB)
        expVbox.addWidget(self._notesTXT)
        vbox.addWidget(self._notesGRP)
        
        self._expandBTN = QPushButton("V")
        self._expandBTN.clicked.connect(self._expandCB)
        vbox.addWidget(self._expandBTN)
        
        self.setLayout(vbox)

    def entry(self):
        return self._entry

    def entryID(self):
        return self._entry.get(PWVKey.ID)

    def searchMatch(self, text, fullSearch=False):
        if not text:
            return True
        text = text.lower()
        if text in self._entry.get(PWVKey.ID, "").lower():
            return True
        if fullSearch and text in self._entry.get(PWVKey.NOTES, "").lower():
            return True
        return False
    
    def selected(self):
        return self.property("selected") == "true"

    def _cfEditDoneCB(self, cfWgt, entry, key):
        #print(f"_cfEditDoneCB: {cfWgt} {key}\nBEFORE: {entry}")
        if entry.get(key) is not None:
            entry[key] = cfWgt.plainText()

    def _notesChangedCB(self):
        newtxt = self._notesTXT.toPlainText()
        self._entry[PWVKey.NOTES] = newtxt 
        self.window().docView().pwvDoc().setModified(True)
        self.window().docView().updateTitle()
        
    def entryUpdate(self):
        self._entry[PWVKey.ID]    = self._idCF.plainText()
        self._entry[PWVKey.URL]   = self._urlCF.plainText()
        self._entry[PWVKey.USER]  = self._userCF.plainText()
        self._entry[PWVKey.PSWD]  = self._pswdCF.plainText()
        self._entry[PWVKey.NOTES] = self._notesTXT.toPlainText()

    def setSelected(self, state):
        if state:
            self.setProperty("selected", "true")
        else:
            self.setProperty("selected", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def zoom(self, pointDelta):
        self._idCF.zoom(pointDelta)
        self._urlCF.zoom(pointDelta)
        self._userCF.zoom(pointDelta)
        self._pswdCF.zoom(pointDelta)
        
        font = self._notesGRP.font()
        font.setPointSize(font.pointSize()+pointDelta)
        self._notesGRP.setFont(font)        
        font = self._notesTXT.font()
        font.setPointSize(font.pointSize()+pointDelta)
        self._notesTXT.setFont(font)        

#    def pswdCopyCB(self):
#        clipb = QApplication.clipboard()
#        clipb.setText(self._entry.get(PWVKey.PSWD, ""))

#    def urlCopyCB(self):
#        print("urlCopyCB() %r" % self._entry.get(PWVKey.URL, ""))
#        clipb = QApplication.clipboard()
#        clipb.setText(self._entry.get(PWVKey.URL, ""))

#    def userCopyCB(self):
#        print("userCopyCB()")
#        clipb = QApplication.clipboard()
#        clipb.setText(self._entry.get(PWVKey.USER, ""))

    # EVENTS
    def mousePressEvent(self, qMouseEvt):
        mbtns = QtCore.Qt.MouseButton
        mevbtn = qMouseEvt.button()
        if mevbtn == mbtns.LeftButton:
            mmods = QtCore.Qt.KeyboardModifier
            mevmod = qMouseEvt.modifiers()
            if mevmod == mmods.NoModifier:
                ## New/Unselect
                self.window().docView().selectOne(self)
            elif mevmod == mmods.ControlModifier:
                # MacOS CMD, Add to selection
                self.window().docView().selectAdd(self)
            elif mevmod == mmods.ShiftModifier:
                # Start or extend selection
                self.window().docView().selectExtend(self)

    def _expandCB(self):
        if self._expanded:
            self._expandBTN.setText("V")
        else:
            self._expandBTN.setText("^")
        self._expanded = not self._expanded
        self._notesGRP.setVisible(self._expanded)
        
    def _setStyle(self):
        self.setStyleSheet("""
          [selected="false"] {
            background-color: black;
            border: 5px solid gray;
            border-radius: 0px;
          }
          [selected="true"] {
            background-color: gray;
            border: 5px solid yellow;
            border-radius: 10px;
          }
          """)
    

class PWVEncodedCard(QFrame):
    """The single DocView card displayed when showing an encoeded doc."""

    def __init__(self):
        super().__init__()

        icon = PWVApp.instance().asset("padlock-icon")
        pixmap = icon.pixmap(icon.availableSizes()[0])
        lockLBL = QLabel()
        lockLBL.setPixmap(pixmap)
        
        self._copyBTN = QPushButton()

        lbl = QLabel("<H1>ENCODED</H1>")
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        btn = QPushButton("Decode")
        btn.clicked.connect(self._decodeCB)
        
        vbox = QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(lockLBL)
        vbox.addWidget(lbl)
        vbox.addWidget(btn)
        self.setLayout(vbox)

        self._setStyle()
        
    def _decodeCB(self):
        mainWin = QApplication.instance().mainWin()
        mainWin.decodeVault()

    def _setStyle(self):
        self.setStyleSheet("""
            PWVEncodedCard {
              background-color: black;
              border: 2px solid red;
              border-radius: 0px;
            }""")


class PWVWindow(QWidget):
    def __init__(self, val):
        super().__init__()
        self.title = "PyQt56 Scroll Bar"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        formLayout = QFormLayout()
        groupBox = QGroupBox("This Is Group Box")
        labelLis = []
        comboList = []

        for i in  range(val):
            entry = {
                PWVKey.ID : f"id - {i}",
                PWVKey.URL: f"url - {i}",
                PWVKey.USER : f"user - {i}",
                PWVKey.PSWD : f"pswd - {i}"
                }
            card = PWVCard(entry)
            formLayout.addRow(card)

        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()


if __name__ == "__main__":
    from pwvuimain import PWVApp
    app = PWVApp()

    window = PWVWindow(30)

#    card = PWVCard()
#    card.show()
    
    status = app.exec()
    sys.exit(status)
