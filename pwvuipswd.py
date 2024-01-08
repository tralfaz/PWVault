import random
import string

from PyQt6.QtCore    import Qt
#from PyQt6.QtCore   import QClipboard
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout

from pwvuiapp import PWVApp


def GeneratePassword(length=12, puncts=string.punctuation):
    allChars = string.ascii_letters + string.digits + puncts

    # randomly select at least one character from each character set above
    pswd =  [ random.choice(string.digits),
              random.choice(string.ascii_uppercase),
              random.choice(string.ascii_lowercase),
              random.choice(puncts) ]

    for _ in range(length-4):
        pswd.append(random.choice(allChars))
        random.shuffle(pswd)

    return "".join(pswd)
    

class PWVPswdLineEdit(QLineEdit):
    """Password LineEdit with icons to show/hide password entries."""

    def __init__(self, hideText=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._hideText = hideText
        
        self.eyeOpenIcon = PWVApp.instance().asset("eye-open-yellow")
        self.eyeBlockedIcon = PWVApp.instance().asset("eye-blocked-yellow")

        if hideText:
            self.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            
        # Add hide/shown toggle at the end of the edit box.
        actPos = QLineEdit.ActionPosition.TrailingPosition
        actIcon = self.eyeOpenIcon if hideText else self.eyeBlockedIcon
        self._toggleVisACT = self.addAction(actIcon, actPos)
        self._toggleVisACT.triggered.connect(self._toggleVisCB)

        self.setStyleSheet("""
            PWVPswdLineEdit[echoMode="2"] {
              lineedit-password-character: 9679;
            }
            """)
        
    def _toggleVisCB(self):
        if self._hideText:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self._toggleVisACT.setIcon(self.eyeOpenIcon)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self._toggleVisACT.setIcon(self.eyeBlockedIcon)
        self._hideText = not self._hideText


class PWVPswdLabel(PWVPswdLineEdit):

    def __init__(self, text=None, parent=None, hideText=True):
        super().__init__(hideText, parent)
        self.setText(text)
        self.setReadOnly(True)

        self.setStyleSheet("""
            PWVPswdLabel {
              background: rgba(0,0,0, 0.0);
              border: 0px solid rgba(0,0,0, 0.0);
            }
            PWVPswdLabel[echoMode="2"] {
              lineedit-password-character: 9679;
            }
            """)
#QLineEdit[readOnly="true"] {
#  background: rgba(40,40,40, 1.0);
#  border: 1px solid rgba(50,50,50, 1.0);
#}



class PWVGeneratePswdDialog(QDialog):

    safeSpecials = '!#$%&*+,-./:;<=>?@^_|~'
    iffySpecials = '"\'()[\\]^`{}'
    
    def __init__(self, parent=None, title="", prompt="", pswd=None):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)

        self._pswdLength = 16
        
        self._buildUI(prompt, pswd)

        if pswd is None:
            self._generatePassword()

    @classmethod
    def getPassword(clazz, parent=None, title="", prompt=""):
        dialog = PWVGeneratePswdDialog(parent, title, prompt)
        status = dialog.exec()
        if status:
            return (dialog.pswdValue(), True)
        else:
            return ("", False)

    def pswdValue(self):
        return self._pswdLBL.text()

    def _buildUI(self, prompt, pswd):
        promptLBL = QLabel(prompt)

        if pswd is None:
            self._pswdLBL = PWVPswdLabel()
        else:
            self._pswdLBL = PWVPswdLabel(pswd)

        self._pswdLenLBL =  QLabel(f"Length: {self._pswdLength}")
        pswdLenSLDR = QSlider()
        pswdLenSLDR.setOrientation(Qt.Orientation.Horizontal)
        pswdLenSLDR.setTickPosition(QSlider.TickPosition.TicksBothSides)
        pswdLenSLDR.setTickInterval(1)
        pswdLenSLDR.setRange(12, 24)
        pswdLenSLDR.setValue(self._pswdLength)
        pswdLenSLDR.valueChanged.connect(self._pswdLenChangedCB)

        pswdLenBox = QHBoxLayout()
        pswdLenBox.addWidget(self._pswdLenLBL)
        pswdLenBox.addWidget(pswdLenSLDR)

        specialGRP = QGroupBox("Special Charcters")
        safeSpecialsBTN = QPushButton("Safe Specials")
        safeSpecialsBTN.clicked.connect(self._safeSpecialCB)
        safeBox = QHBoxLayout()
        safeBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        safeBox.setSpacing(2)
        safeBox.addWidget(safeSpecialsBTN)
        self._safeChecks = []
        for schr in self.safeSpecials:
            scBTN = QPushButton(schr)
            scBTN.setObjectName("SpecialCharToggle")
            scBTN.setCheckable(True)
            scBTN.setChecked(True)
            scBTN.setFlat(True)
            safeBox.addWidget(scBTN)
            self._safeChecks.append(scBTN)
        
        iffySpecialsBTN = QPushButton("Iffy Specials")
        iffySpecialsBTN.clicked.connect(self._iffySpecialCB)
        iffyBox = QHBoxLayout()
        iffyBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        iffyBox.setSpacing(4)
        iffyBox.addWidget(iffySpecialsBTN)
        self._iffyChecks = []
        for schr in self.iffySpecials:
            scBTN = QPushButton(schr)
            scBTN.setObjectName("SpecialCharToggle")
            scBTN.setCheckable(True)
            scBTN.setChecked(False)
            scBTN.setFlat(True)
            iffyBox.addWidget(scBTN)
            self._iffyChecks.append(scBTN)
            
        specialBox = QVBoxLayout()
        specialBox.setContentsMargins(0, 0, 0, 0)
        specialBox.addLayout(safeBox)
        specialBox.addLayout(iffyBox)

        specialGRP.setLayout(specialBox)

        #  QPushButton[accessibleName="SpecialCharToggle"] {
        self.setStyleSheet("""
                QPushButton#SpecialCharToggle {
                  border: 2px solid red;
                  margin: 0px;
                  padding: 3px;
                }
                QPushButton#SpecialCharToggle:checked {
                  border: 2px solid green;
                  margin: 0px;
                  padding: 3px;
                }
            """)
            
        buttonBox = QDialogButtonBox()
        btnRole = QDialogButtonBox.ButtonRole
        buttonBox.addButton("OK", btnRole.AcceptRole)
        self._genPswdBTN = buttonBox.addButton("Generate", btnRole.ApplyRole)
        self._copyBTN = buttonBox.addButton("Copy", btnRole.ApplyRole)
        buttonBox.addButton("Cancel", btnRole.RejectRole)
        buttonBox.accepted.connect(self._okCB)
        buttonBox.clicked.connect(self._buttonCB)
        buttonBox.rejected.connect(self._cancelCB)

        vbox = QVBoxLayout()
        vbox.addWidget(promptLBL)
        vbox.addWidget(self._pswdLBL)
        vbox.addLayout(pswdLenBox)
        vbox.addWidget(specialGRP)
        vbox.addWidget(buttonBox)
        self.setLayout(vbox)

    def _buttonCB(self, btn):
        if btn == self._copyBTN:
            clipboard = PWVApp.instance().clipboard()
            clipboard.setText(self._pswdLBL.text())
            return
        elif btn == self._genPswdBTN:
            self._generatePassword()

    def _generatePassword(self):
        specials = ""
        for scBTN in self._safeChecks:
            if scBTN.isChecked():
                specials += scBTN.text()
        for scBTN in self._iffyChecks:
            if scBTN.isChecked():
                specials += scBTN.text()

        newPswd = GeneratePassword(self._pswdLength, specials)
        self._pswdLBL.setText(newPswd)

    def _cancelCB(self):
        self.close()

    def _okCB(self):
        self.accept()
        
    def _pswdLenChangedCB(self):
        sldr = self.sender()
        self._pswdLength = sldr.value()
        self._pswdLenLBL.setText(f"Length: {self._pswdLength}")

    def _iffySpecialCB(self):
        for scBTN in self._iffyChecks:
            scBTN.setChecked(not scBTN.isChecked())

    def _safeSpecialCB(self):
        for scBTN in self._safeChecks:
            scBTN.setChecked(not scBTN.isChecked())



class PWVPswdDialog(QDialog):

    def __init__(self, parent=None, title="", prompt="", placeholder=""):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)

        promptLBL = QLabel(prompt)
        self._pswdLE = PWVPswdLineEdit()
        self._pswdLE.setPlaceholderText(placeholder)
        buttonBox = QDialogButtonBox()
        buttonBox.addButton("OK", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        buttonBox.accepted.connect(self._okCB)
        buttonBox.rejected.connect(self._cancelCB)
#        leVal = QRegExpValidator(QRegExp("[\\w\\d_ \\.]{24}"))
#        le.setValidator(leVal)

        vbox = QVBoxLayout()
        vbox.addWidget(promptLBL)
        vbox.addWidget(self._pswdLE)
        vbox.addWidget(buttonBox)
        self.setLayout(vbox)

    def _cancelCB(self):
        self.close()

    def _okCB(self):
        self.accept()

    def pswdValue(self):
        return self._pswdLE.text()

    @classmethod
    def getText(clazz, parent=None, title="", prompt="", placeholder=""):
        dialog = PWVPswdDialog(parent, title, prompt, placeholder)
        status = dialog.exec()
        if status:
            return (dialog.pswdValue(), True)
        else:
            return ("", False)



if __name__ == "__main__":
    from PyQt6.QtWidgets import (QFrame,QInputDialog,QPushButton)

    class TestFrame(QFrame):

        def __init__(self, parent=None):
            super().__init__(parent)
    
            self.setStyleSheet("""
              QInputDialog QLineEdit[echoMode="2"] {
                lineedit-password-character: 9679;
                background-color: green;
            }
              """)

            pswdLE = PWVPswdLineEdit()
            self._pswdLBL = PWVPswdLabel("ABCDEF")

            test1BTN = QPushButton("TEST 1")
            test1BTN.clicked.connect(self._test1CB)
            test2BTN = QPushButton("TEST 2")
            test2BTN.clicked.connect(self._test2CB)
            test3BTN = QPushButton("TEST 3")
            test3BTN.clicked.connect(self._test3CB)
            test4BTN = QPushButton("TEST 4")
            test4BTN.clicked.connect(self._test4CB)
            test4BTN = QPushButton("TEST 5")
            test4BTN.clicked.connect(self._test5CB)

            vbox = QVBoxLayout()
            vbox.addWidget(pswdLE)
            vbox.addWidget(self._pswdLBL)
            vbox.addWidget(test1BTN)
            vbox.addWidget(test2BTN)
            vbox.addWidget(test3BTN)
            vbox.addWidget(test4BTN)
            self.setLayout(vbox)

        def _test1CB(self):
            title = "THE TITLE"
            text, ok = QInputDialog.getText(self, title,
                                            "Password:",
                                            QLineEdit.EchoMode.Password)
            print(f"TEXT({text})  OK:{ok}")

        def _test2CB(self):
             dialog = PWVPswdDialog(self, "Title", "Enter Password", "Password")
             status = dialog.exec()
             print(f"STATUS: {status}")
             if status  == QDialog.DialogCode.Accepted:
                 retVal = dialog.getNewValue()
                 print(f"Dialog value: {retVal}")

        def _test3CB(self):
            title = "THE TITLE"
            text, ok = PWVPswdDialog.getText(self, title, "Enter Password:",
                                            "password")
            print(f"TEXT({text})  OK:{ok}")

        def _test4CB(self):
            newPswd = GeneratePassword(12)
            self._pswdLBL.setText(newPswd)

        def _test5CB(self):
            title = "Generate Secure Password"
            prompt = "Choose generation options then click Generate"
            dialog = PWVGeneratePswdDialog(self, title, prompt)
            status = dialog.exec()
            print(f"STATUS: {status}")

    ## TEST            
    app = PWVApp()

    win = TestFrame()
    win.show()
    
    app.exec()
