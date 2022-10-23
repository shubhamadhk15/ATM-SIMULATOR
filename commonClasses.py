from PyQt5.QtWidgets import QDialog
from card_functions import cssLoader
from stackedwidget import widget,adminWidget
from PyQt5.uic import loadUi
def prompt(heading='',msg='',proceedEnabled=False,parent = None,w = widget):
    p = promptScr(heading,msg,proceedEnabled,parent)
    w.addWidget(p)
    w.setCurrentWidget(p)

def gotoHome():
    print('Done')

class pinScr(QDialog):
    def __init__(self,parentObj):
        super(pinScr,self).__init__()
        loadUi('UI/pin.ui',self)
        self.parentObj = parentObj
        self.setStyleSheet(cssLoader('style.css'))
        self.proceedBtn.clicked.connect(self.verifyPin)
        self.clearBtn.clicked.connect(self.clear)
        self.cancelBtn.clicked.connect(gotoHome)

    def clear(self):
        self.lineEdit.setText('')

class promptScr(QDialog):
    def __init__(self,message = '',desc='',proceedEnabled = False,parent = None):
        super(promptScr,self).__init__()
        loadUi('UI/prompt.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.instructLabel.setText(message)
        self.descLabel.setText(desc)
        self.cancelBtn.clicked.connect(gotoHome)
        self.proceedBtn.clicked.connect(self.proceed)
        if not proceedEnabled:
            self.proceedBtn.hide()
        if proceedEnabled:
            self.cancelBtn.setText('CANCEL')
            self.parent = parent

    def proceed(self):
        p = pinScr(self.parent)
        widget.addWidget(p)
        widget.setCurrentWidget(p)