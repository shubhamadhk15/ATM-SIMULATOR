'''Author :: Ankit Yadav
    Date :: 16/09/2022
'''
from awsDb import *
from admin import createAdminMenu
from stackedwidget import widget,app
from card_functions import getHwId, isValidCardNo,fetch_card,cssLoader
from sms import sendOtp

import sys,os,threading,time
from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog,QShortcut,QLineEdit
from PyQt5.uic import loadUi
    
def prompt(heading='',msg='',proceedEnabled=False,parent = None):
    p = promptScr(heading,msg,proceedEnabled,parent)
    widget.addWidget(p)
    widget.setCurrentWidget(p)
    interval = 5
    if proceedEnabled:
        interval = 30
    homeScr = homescreen()
    widget.addWidget(homeScr)
    timethread = threading.Thread(target=timoutThread,args=(homeScr,interval))
    timethread.daemon = True
    timethread.start()

def gotoHome():
    event.set()
    home = homescreen()
    widget.addWidget(home)
    widget.setCurrentIndex(widget.indexOf(home))

def timoutThread(nextObj,interval=3):
    time.sleep(interval)
    if not event.is_set():
        event.set()
        widget.setCurrentWidget(nextObj)

class Session():
    def setCardNo(self,cardNo):
        self.cardNo = cardNo
        self.accNo = fetchAccNoFromCard(cardNo)
        self.firstName = fetchFirstNameFromCard(cardNo)
        

class homescreen(QDialog):
    path = '/'
    def __init__(self):
        super(homescreen,self).__init__()
        loadUi('UI/homescreen.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.DragDrop = self.lineEdit
        self.shortcut = QShortcut(QKeySequence('Ctrl+O'),self)
        self.shortcut.activated.connect(self.openAdminMenu)
        self.drop()

    def drop(self):
        self.DragDrop.installEventFilter(self)
        self.DragDrop.acceptDrops()
        self.DragDrop.setDragEnabled(True)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.DragEnter:
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

    def openAdminMenu(self):
        createAdminMenu()

class menu(QDialog):
    def __init__(self):
        super(menu,self).__init__()
        loadUi('UI/menu.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.withdrawBtn.clicked.connect(self.withdraw)
        self.balBtn.clicked.connect(self.checkBal)
        self.greetLabel.setText('Welcome '+newSession.firstName)
        self.cancelBtn.clicked.connect(gotoHome)
        self.resetBtn.clicked.connect(self.reset)
        self.transferBtn.clicked.connect(self.fundTransfer)
        self.flag = True

    def withdraw(self):
        self.withdrawObj = withdrawScr()
        widget.addWidget(self.withdrawObj)
        widget.setCurrentIndex(widget.indexOf(self.withdrawObj))

    def checkBal(self):
        pinObj = pinScr(self)
        widget.addWidget(pinObj)
        widget.setCurrentWidget(pinObj)

    def proceed(self):
        prompt('Account Balance','Rs. '+str(fetchBal(newSession.accNo)))

    def reset(self):
        s = ResetPinSession()
        inp = InputStr(s,'ENTER MOBILE NUMBER')
        widget.addWidget(inp)
        widget.setCurrentWidget(inp)

    def fundTransfer(self):
        t = FundTransfer()
        t.proceed()

class ResetPinSession():
    def __init__(self) -> None:
        self.pins=[False,False]
        self.otpEntered = False
        self.mobileVerified= False
        self.otpVerified = False

    def proceed(self,inpObj):
        self.val = inpObj.getVal()
        if self.mobileVerified:
            if self.otpVerified:
                if self.pins[0]!=True and self.pins[0]!=False:
                    self.pins[1] = self.val
                    self.checkPins()
                elif self.pins[0]==False:
                    self.pins[0] = True
                    inpPin = InputStr(self,'ENTER NEW PIN',4,'pass')
                    widget.addWidget(inpPin)
                    widget.setCurrentWidget(inpPin)
                else:
                    self.pins[0] = self.val
                    inpPin = InputStr(self,'CONFIRM NEW PIN',4,'pass')
                    widget.addWidget(inpPin)
                    widget.setCurrentWidget(inpPin)

            elif self.otpEntered==False:
                self.otpEntered = True
                inpOtp = InputStr(self,'ENTER  OTP',4)
                widget.addWidget(inpOtp)
                widget.setCurrentWidget(inpOtp)

            else:
                self.verifyOtp()

        else:
            self.verifyMobile()

    def verifyMobile(self):
        mobile = fetchMobileFromAccNo(newSession.accNo)
        if self.val == mobile:
            self.mobileVerified = True
            self.otp = sendOtp(mobile,'Pin Reset')
            self.proceed(self)
        else:
            prompt('INVALID MOBILE NUMBER',"Please takeout your card")

    def verifyOtp(self):
        if self.val ==self.otp:
            self.otpVerified=True
            self.proceed(self)
        else:
            prompt('Invalid OTP',"Please takeout your card")

    def checkPins(self):
        if self.pins[0]==self.pins[1]:
            updatePin(newSession.cardNo,self.pins[0])
            msg = 'Pin Successfully Reset'.upper()
        else:
            msg = 'Pin does not Match'.upper()
        prompt(msg,"Please takeout your card")

    def getVal(self):
        pass
            
class withdrawScr(QDialog):
    def __init__(self):
        super(withdrawScr,self).__init__()
        loadUi('UI/withdraw.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.proceedBtn.clicked.connect(self.verifyAmount)
        self.clearBtn.clicked.connect(self.clear)
        self.cancelBtn.clicked.connect(gotoHome)

    def verifyAmount(self):
        try:
            self.amount = int(self.lineEdit.text())
            pinObj = pinScr(self)
            widget.addWidget(pinObj)
            widget.setCurrentIndex(widget.currentIndex()+1)

        except ValueError:
            print('Invalid Format')

    def proceed(self):
        if self.amount>fetchBal(newSession.accNo):
            prompt('INSUFFICIENT BALANCE','PLEASE TAKE OUT YOUR CARD')
        else:
            transact(self.amount,newSession.atmId,newSession.accNo)
            prompt('TRANSACTION SUCCESSFULL','PLEASE COLLECT YOUR CASH AND CARD')

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
class loadingScr(promptScr):
    def __init__(self, message, desc, proceedEnabled=False):
        super().__init__(message, desc, proceedEnabled)
        self.cancelBtn.hide()

class pinScr(QDialog):
    def __init__(self,parentObj):
        super(pinScr,self).__init__()
        loadUi('UI/pin.ui',self)
        self.parentObj = parentObj
        self.setStyleSheet(cssLoader('style.css'))
        self.proceedBtn.clicked.connect(self.verifyPin)
        self.clearBtn.clicked.connect(self.clear)
        self.cancelBtn.clicked.connect(gotoHome)
    # def keyPressEvent(self, event: QtGui.QKeyEvent):
    #     if event.key() == Qt.Key_Num0:
    #         self.lineEdit.setText('0')

    def verifyPin(self):
        if self.lineEdit.text() == fetchPin(newSession.cardNo):
            self.parentObj.proceed()
        else:
            prompt('Invalid PIN','Please Takout Your Card')

    def clear(self):
        self.lineEdit.setText('')

class InputStr(QDialog):
    def __init__(self,parent,fieldname,maxLen=10,type='normal'):
        super(InputStr,self).__init__()
        loadUi('UI/withdraw.ui',self)
        self.parent = parent
        self.instructLabel.setText(fieldname)
        self.setStyleSheet(cssLoader('style.css'))
        self.proceedBtn.clicked.connect(self.proceed)
        self.clearBtn.clicked.connect(self.clear)
        self.cancelBtn.clicked.connect(gotoHome)
        self.lineEdit.setMaxLength(maxLen)
        if type == 'pass':
            self.lineEdit.setEchoMode(QLineEdit.Password)

    def proceed(self):
        self.parent.proceed(self)
    def getVal(self):
        return self.lineEdit.text()

    def clear(self):
        self.lineEdit.setText('')

class FundTransfer():
    def __init__(self):
        self.amountEntered = False
        self.accNoEntered = False
        self.accNoConfirmed = False
        self.pinEntered = False

    def proceed(self,inpObj = None):
        if self.pinEntered:
            transact(self.amount,newSession.atmId,newSession.accNo,self.accNo)
            prompt('Transaction Successful'.upper(),'Thankyou For Using\nVELOCITY BANK ATM')
            return
        if self.amountEntered:
            self.amount = inpObj.getVal()
            if self.accNo == str(newSession.accNo):
                prompt('INVALID INPUT','YOU CANNOT TRANSFER TO\nYOUR OWN ACCOUNT')
            else:
                self.pinEntered = True
                prompt('CONFIRM DETAILS','Beneficiary Name : {} \nAmount : {} '.format(fetchNameFromAccNo(self.accNo),self.amount),True,self)

        elif self.accNoConfirmed:
            if inpObj.getVal() == self.accNo:
                self.amountEntered = True
                i = InputStr(self,'ENTER AMOUNT',6)
                widget.addWidget(i)
                widget.setCurrentWidget(i)
            else:
                prompt('MISMATCH INPUT','BENEFICIARY ACCOUNT NUMBER \nAND CONFIRMED ACCOUNT NUMBER \nDOES NOT MATCH.')
        elif self.accNoEntered:
            self.accNoConfirmed = True
            self.accNo = inpObj.getVal()
            i = InputStr(self,'CONFIRM BENEFICIARY ACCOUNT NUMBER',10)
            widget.addWidget(i)
            widget.setCurrentWidget(i)
        else:
            self.accNoEntered = True
            i = InputStr(self,'ENTER BENEFICIARY ACCOUNT NUMBER',10)
            widget.addWidget(i)
            widget.setCurrentWidget(i)
def connectThread():
    hwId = getHwId()
    connectAtm(hwId)
    newSession.atmId = getAtmIdFromHwId(hwId[0])
    time.sleep(2)
    widget.setCurrentWidget(homeScr)
    
if __name__=='__main__':
    threading.Thread(target=connectThread).start()
    l = loadingScr('WELCOME TO VELOCIITY BANK ATM','PLEASE WAIT...')
    widget.addWidget(l)
    widget.show()
    newSession = Session()
    homeScr = homescreen()
    widget.addWidget(homeScr)
    event = threading.Event()

    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')