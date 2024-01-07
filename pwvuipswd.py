from pwvuiapp import PWVApp

from PyQt6.QtCore    import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout

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



class PWVPswdDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose, False)
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Type in your text:"))
        self.le = PWVPswdLineEdit()
    # le.setText("Profile")
    # le.selectAll()
        self.le.setPlaceholderText("Profile")
        vbox.addWidget(self.le)
#        leVal = QRegExpValidator(QRegExp("[\\w\\d_ \\.]{24}"))
#        le.setValidator(v);
        buttonBox = QDialogButtonBox()
        #QDialogButtonBox.StandardButton.Ok |
        #                             QDialogButtonBox.StandardButton.Cancel)
        #buttonBox.addButton("Help", QtGui.QDialogButtonBox.HelpRole)
        buttonBox.addButton("OK", QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        vbox.addWidget(buttonBox)
        self.setLayout(vbox)

        #

#    def signals_connection(self):
#        self.test_random.clicked.connect(self.test_rand)
#
#        # Is this the latest/correct way to write it?
        buttonBox.accepted.connect(self._okCB)
        buttonBox.rejected.connect(self._cancelCB)
#        buttonBox.helpRequested.connect(self.test_help)
#        self.accepted.connect(self.
#      connect(buttonBox, SIGNAL(accepted()), this, SIGNAL(accepted()));
#      connect(buttonBox, SIGNAL(rejected()), this, SIGNAL(rejected()));

    def _cancelCB(self):
        print("_cancelCB")
        self.close()

    def _okCB(self):
        print("_okCB")
        self.accept()

    def getNewValue(self):
        return self.le.text()


if __name__ == "__main__":
    from PyQt6.QtWidgets import (QFrame,QInputDialog,QPushButton)

    class TestFrame(QFrame):

        def __init__(self, parent=None):
            super().__init__(parent)
    
            self.setStyleSheet("""
              QLineEdit[echoMode="2"] {
                lineedit-password-character: 9679;
              }
              QInputDialog {
                background-color: red;
              }
              QLineEdit {
                background-color: blue;
              }
              QInputDialog QLineEdit[echoMode="2"] {
                lineedit-password-character: 9679;
              }
              """)

            pswdLE = PWVPswdLineEdit()

            testBTN = QPushButton("TEST")
            testBTN.clicked.connect(self._testCB)

            test2BTN = QPushButton("TEST 2")
            test2BTN.clicked.connect(self._test2CB)

            vbox = QVBoxLayout()
            vbox.addWidget(pswdLE)
            vbox.addWidget(testBTN)
            vbox.addWidget(test2BTN)
            self.setLayout(vbox)

        def _testCB(self):
            title = "THE TITLE"
            text, ok = QInputDialog.getText(self, title,
                                            "Password:",
                                            QLineEdit.EchoMode.Password)
            print(f"TEXT({text})  OK:{ok}")

        def _test2CB(self):
             dialog = PWVPswdDialog(self)
             status = dialog.exec()
             print(f"STATUS: {status}")
             if status  == QDialog.DialogCode.Accepted:
                 retVal = dialog.getNewValue()
                 print(f"Dialog value: {retVal}")

    
    app = PWVApp()

    win = TestFrame()
    win.show()
    
    app.exec()
