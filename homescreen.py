'''Author :: Ankit Yadav
    Date :: 16/09/2022
'''
from awsDb import *
from card_functions import isValidCardNo,fetch_card
import sys,os,datetime
from PyQt5 import QtCore,QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication,QDialog,QStackedWidget
from PyQt5.uic import loadUi
    
# def countdown(interval):
#     current = datetime.datetime.now()
#     while(datetime.datetime.now()<current + datetime.timedelta(seconds=interval)):
#         pass

class Session():
    def setCardNo(self,cardNo):
        self.cardNo = cardNo
        self.accNo = fetchAccNoFromCard(cardNo)
        self.firstName = fetchFirstNameFromCard(cardNo)
        

def cssLoader(file):
    with open(file,'r') as f:
        rd = f.read()
    return rd

class homescreen(QDialog):
    path = '/'
    def __init__(self):
        super(homescreen,self).__init__()
        loadUi('UI/homescreen.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.DragDrop = self.lineEdit
        self.drop()

    def drop(self):
        self.DragDrop.installEventFilter(self)
        self.DragDrop.acceptDrops()
        self.DragDrop.setDragEnabled(True)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.DragEnter:
            if event.mimeData().hasFormat('text/plain'):
                event.accept()
                return True
        if event.type() == QtCore.QEvent.Drop:
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path):
                    self.path = path
            source.setText(os.path.basename(self.path))
            self.verifyCard()
            return True
        return False

    def verifyCard(self):
        if self.path[-5:]!='.card':
            print('invalid card')
            return
        
        try:
            card_no = fetch_card(self.path)
            print(card_no)
        except :
            print('Invalid Card  hehe')
            return
        if(isValidCardNo(card_no)):
            print('card accepted')
            newSession.setCardNo(card_no)
            self.menuObj = menu()
            widget.addWidget(self.menuObj)
            widget.setCurrentIndex(widget.indexOf(self.menuObj))
        else:
            print('Card Not found')

class menu(QDialog):
    def __init__(self):
        super(menu,self).__init__()
        loadUi('UI/menu.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.withdrawBtn.clicked.connect(self.withdraw)
        self.greetLabel.setText('Welcome '+newSession.firstName)

    def withdraw(self):
        self.withdrawObj = withdrawScr()
        widget.addWidget(self.withdrawObj)
        widget.setCurrentIndex(widget.indexOf(self.withdrawObj))

class withdrawScr(QDialog):
    def __init__(self):
        super(withdrawScr,self).__init__()
        loadUi('UI/withdraw.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.proceedBtn.clicked.connect(self.verifyAmount)
    def verifyAmount(self):
        try:
            self.amount = int(self.lineEdit.text())
            pinObj = pinScr(self)
            widget.addWidget(pinObj)
            widget.setCurrentIndex(widget.currentIndex()+1)

        except ValueError:
            print('Invalid Format')

    def proceed(self):
        print('Cashout Part')
        if self.amount>fetchBal(newSession.accNo):
            p = promptScr('INSUFFICIENT BALANCE','PLEASE TAKE OUT YOUR CARD')
        else:
            print(deductAmount(self.amount,newSession.accNo))
            p = promptScr('TRANSACTION SUCCESSFULL','PLEASE COLLECT YOUR CASH AND CARD')
        widget.addWidget(p)
        widget.setCurrentIndex(widget.indexOf(p))
        # gotoHome(widget)
        

class promptScr(QDialog):
    def __init__(self,message,desc):
        super(promptScr,self).__init__()
        loadUi('UI/prompt.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.instructLabel.setText(message)
        self.descLabel.setText(desc)
        self.cancelBtn.clicked.connect(self.gotoHome)

    def gotoHome(self):
        home = homescreen()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.indexOf(home))

class pinScr(QDialog):
    def __init__(self,parentObj):
        super(pinScr,self).__init__()
        loadUi('UI/pin.ui',self)
        self.parentObj = parentObj
        self.setStyleSheet(cssLoader('style.css'))
        self.proceedBtn.clicked.connect(self.verifyPin)
    # def keyPressEvent(self, event: QtGui.QKeyEvent):
    #     if event.key() == Qt.Key_Num0:
    #         self.lineEdit.setText('0')

    def verifyPin(self):
        if self.lineEdit.text() == fetchPin(newSession.cardNo):
            self.parentObj.proceed()
        else:
            p = promptScr('Invalid PIN','Please Takout Your Card')
            widget.addWidget(p)
            widget.setCurrentWidget(p)

if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    widget.setFixedHeight(420)
    widget.setFixedWidth(700)
    homeScr = homescreen()
    widget.addWidget(homeScr)
    newSession = Session()
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')