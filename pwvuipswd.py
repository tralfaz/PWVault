import random
import string

from pwvuiapp import PWVApp

from PyQt6.QtCore    import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout


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

class PWVGeneratePswDialog(QDialog):

    def __init__(self, parent=None, title="", prompt=""):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)


        promptLBL = QLabel(prompt)

        self._pswdLBL = PWVPswdLabel("ABCDEF")

        specialBox = QHBoxLayout()
        for schr in string.punctuation:
            scBTN = QPushButton(schr)
            scBTN.setObjectName("SpecialCharToggle")
            scBTN.setCheckable(True)
            scBTN.setChecked(True)
            scBTN.setFlat(True)
#                QPushButton[accessibleName="SpecialCharToggle"] {
            scBTN.setStyleSheet("""
                QPushButton#SpecialCharToggle {
                  border: 2px solid red;
                }
                QPushButton#SpecialCharToggle:checked {
                  border: 2px solid green;
                }
            """)
            
            specialBox.addWidget(scBTN)

        buttonBox = QDialogButtonBox()
        buttonBox.addButton("OK", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        buttonBox.accepted.connect(self._okCB)
        buttonBox.rejected.connect(self._cancelCB)

        vbox = QVBoxLayout()
        vbox.addWidget(promptLBL)
        vbox.addWidget(self._pswdLBL)
        vbox.addLayout(specialBox)
        vbox.addWidget(buttonBox)
        self.setLayout(vbox)

    def _cancelCB(self):
        self.close()

    def _okCB(self):
        self.accept()

 
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

    def getNewValue(self):
        return self._pswdLE.text()

    @classmethod
    def getText(clazz, parent=None, title="", prompt="", placeholder=""):
        dialog = PWVPswdDialog(parent, title, prompt, placeholder)
        status = dialog.exec()
        if status:
            return (dialog._pswdLE.text(), True)
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
            dialog = PWVGeneratePswDialog(self, title, prompt)
            status = dialog.exec()

    ## TEST            
    app = PWVApp()

    win = TestFrame()
    win.show()
    
    app.exec()
