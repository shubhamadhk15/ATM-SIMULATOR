'''Author :: Ankit Yadav
    Date :: 16/09/2022
'''
from awsDb import *
from admin import createAdminMenu
from stackedwidget import widget,app,newSession
from card_functions import getHwId, isValidCardNo,fetch_card,cssLoader
from sms import sendOtp
from commonClasses import pinScr,promptScr

import sys,os,threading,time
from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence,QPixmap,QIcon
from PyQt5.QtWidgets import QDialog,QShortcut,QLineEdit,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPropertyAnimation, QPoint
    
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
        self.cardFrame.hide()

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
            newSession.setCardNo(card_no)
        except :
            print('Invalid Card  hehe')
            return
        if(isValidCardNo(int(card_no))):
            self.dispCard()
            self.menuObj = menu()
            t = threading.Thread(target=self.changeScr)
            t.start()
            self.animate()
            
        else:
            print('Card Not found')

    def openAdminMenu(self):
        createAdminMenu()

    def dispCard(self):
        v = QPixmap('UI/platinum.png')
        self.bgLabel.setPixmap(v)
        self.bgLabel.adjustSize()
        if newSession.cardType[0] == 'VISA':
            type = 'visa1.png'
        elif newSession.cardType[0] == 'Matercard':
            type = 'mastercard.png'
        elif newSession.cardType[0] == 'American Express':
            type = 'amex2.jpg'
        else:
            type = 'rupay.png'
        v = QPixmap('UI/'+type)
        self.netLabel.setPixmap(v)
        self.netLabel.adjustSize()
        cardNo = newSession.cardNo
        i = 4
        while i<len(cardNo):
            cardNo = cardNo[:i]+' '+cardNo[i:]
            i+=5
        self.cardNoLabel.setText(cardNo)
        self.cardNoLabel.adjustSize()
        exp = str(newSession.cardExp)
        self.validLabel.setText('VALID THRU '+exp[:2]+'/'+exp[2:])
        self.validLabel.adjustSize()
        self.cardHoldLabel.setText(newSession.firstName+' '+newSession.lastName)
        self.cardHoldLabel.adjustSize()
        

    def animate(self):
        self.cardFrame.show()
        self.a = QPropertyAnimation(self.cardFrame, b"pos")
        self.a.setEndValue(QPoint(222, 240))
        self.a.setDuration(1500)
        self.a.start()

    def changeScr(self):
        widget.addWidget(self.menuObj)
        time.sleep(3)
        widget.setCurrentIndex(widget.indexOf(self.menuObj))
      
class menu(QDialog):
    def __init__(self):
        super(menu,self).__init__()
        loadUi('UI/menu.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.withdrawBtn.clicked.connect(self.withdraw)
        self.balBtn.clicked.connect(self.checkBal)
        self.greetLabel.setText('Welcome, '+newSession.firstName)
        self.cancelBtn.clicked.connect(gotoHome)
        self.resetBtn.clicked.connect(self.reset)
        self.transferBtn.clicked.connect(self.fundTransfer)
        self.miniBtn.clicked.connect(self.miniStatement)

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

    def miniStatement(self):
        obj = MIniStateMent()
        obj.proceed()

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
            if not self.amount%100 == 0:
                prompt('INVALID INPUT','AMOUNT NOT A MULTIPLE OF\nAVAILABLE DENOMINATIONS')
                return
            self.denoms = self.getDenominationCounts(self.amount)
            denoms_avl = getAtmDenoms(newSession.atmId)
            j = 0
            for i in self.denoms:
                if i > denoms_avl[j]:
                    prompt('INSUFFICIENT CASH IN ATM')
                    return
                j+=1
            pinObj = pinScr(self)
            widget.addWidget(pinObj)
            widget.setCurrentIndex(widget.currentIndex()+1)

        except ValueError:
            prompt('INVALID INPUT','PLEASE INPUT DIGITS ONLY')

    def getDenominationCounts(self,x):
        notes = [100,200,500,2000]
        result = [0,0,0,0]
        for i in range(4,0,-1):
            amt = x // notes[i-1]
            if(amt != 0):
                result[i-1] = amt 
                x = x % notes[i-1]
        return result

    def proceed(self):
        if self.amount>fetchBal(newSession.accNo):
            prompt('INSUFFICIENT BALANCE','PLEASE TAKE OUT YOUR CARD')
        else:
            transact(self.amount,newSession.atmId,newSession.accNo)   # deducts balance from  user Account
            refillAtm(newSession.atmId,-self.denoms[0],-self.denoms[1],-self.denoms[2],-self.denoms[3])   # deducts cash from ATM
            prompt('TRANSACTION SUCCESSFULL','PLEASE COLLECT YOUR CASH AND CARD')

    def clear(self):
        self.lineEdit.setText('')
        


class loadingScr(promptScr):
    def __init__(self, message, desc, proceedEnabled=False):
        super().__init__(message, desc, proceedEnabled)
        self.cancelBtn.hide()


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

class MIniStateMent():
    def __init__(self) -> None:
        self.pinEntered = False
    def proceed(self):
        if self.pinEntered:
            p = MiniStatementWindow()
            widget.addWidget(p)
            widget.setCurrentWidget(p)
        else:
            self.pinEntered = True
            p = pinScr(self)
            widget.addWidget(p)
            widget.setCurrentWidget(p)

class MiniStatementWindow(QDialog):
    def __init__(self):
        super(MiniStatementWindow,self).__init__()
        loadUi('UI/statement.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.instructLabel.setText(newSession.firstName.upper()+', YOUR MINI STATEMENT')
        self.insertData()
        self.table.setColumnWidth(3,200)
        for i in range(3):
            self.table.setColumnWidth(i,150)
        self.cancelBtn.clicked.connect(gotoHome)

    def insertData(self):
        data = genMiniStatement(newSession.accNo)
        self.table.setRowCount(len(data))
        bal = fetchBal(newSession.accNo)
        r = 0
        for row in data:
            c = 0
            for item in row:
                tableItem = QTableWidgetItem(item)
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(r,c,tableItem)
                c+=1
            if r>0:
                if data[r][2]=='Cr':
                    bal-=int(data[r][1])
                else:
                    bal+=int(data[r][1])
            tItem = QTableWidgetItem(str(bal))
            tItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(r,c,tItem)
            r+=1

def connectThread():
    hwId = getHwId()
    connectAtm(hwId)
    newSession.atmId = getAtmIdFromHwId(hwId[0])
    time.sleep(2)
    widget.setCurrentWidget(homeScr)
    
event = threading.Event()
if __name__=='__main__':
    threading.Thread(target=connectThread).start()
    l = loadingScr('WELCOME TO VELOCIITY BANK ATM','PLEASE WAIT...')
    widget.addWidget(l)
    widget.show()
    homeScr = homescreen()
    widget.addWidget(homeScr)
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')
