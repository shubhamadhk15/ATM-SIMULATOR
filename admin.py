from commonClasses import prompt
from sms import sendOtp
from stackedwidget import adminWidget
from PyQt5.QtWidgets import QDialog,QLineEdit
from PyQt5.uic import loadUi
from awsDb import createCust,fetchCustIdFromMob, fetchLastAc, getMobiles,insertAc
from card_functions import cssLoader

def createAdminMenu():
    adminMenuObj = AdminMenu()
    adminWidget.addWidget(adminMenuObj)
    adminWidget.show()

def gotoHome():
    a = AdminMenu()
    adminWidget.addWidget(a)
    adminWidget.setCurrentWidget(a)

def takeInp(parent,fieldname,maxLen=10,type='normal'):
    i = InputStr(parent,fieldname,maxLen,type)
    adminWidget.addWidget(i)
    adminWidget.setCurrentWidget(i)

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

class AdminMenu(QDialog):
    def __init__(self):
        super(AdminMenu,self).__init__()
        loadUi('UI/admin_menu.ui',self)
        self.setStyleSheet(cssLoader('style.css'))
        self.newAcBtn.clicked.connect(self.newAc)
        self.exAcBtn.clicked.connect(self.exUserAc)
        self.cancelBtn.clicked.connect(self.cancel)

    def cancel(self):
        adminWidget.hide()
        
    def newAc(self):
        obj = NewUser()
        obj.proceed()

    def exUserAc(self):
        obj = createAcc()
        obj.proceed(self)

class NewUser():
    def __init__(self) -> None:
        self.firstNameEntered = False
        self.lastNameEntered = False
    def proceed(self,i=None):
        if self.lastNameEntered:
            c = createAcc(True,[self.fName,i.getVal()])
            c.proceed()
        elif self.firstNameEntered:
            self.lastNameEntered = True
            self.fName = i.getVal()
            i = InputStr(self,'Enter Last Name',15)
            adminWidget.addWidget(i)
            adminWidget.setCurrentWidget(i)
        else:
            self.firstNameEntered = True
            i = InputStr(self,'Enter First Name',15)
            adminWidget.addWidget(i)
            adminWidget.setCurrentWidget(i)

class createAcc():
    def __init__(self,isNewUser = False,name = []) -> None:
        self.isNewUser = isNewUser
        self.otpVerified = False
        self.otpEntered = False
        self.mobileEntered = False
        self.name = name
    def proceed(self,i = None):
        if self.otpVerified:
            self.createUser()
        elif self.otpEntered:
            if self.otp==i.getVal():
                self.otpVerified = True
                self.proceed()
            else:
                prompt('INVALID OTP',w = adminWidget)
        elif self.mobileEntered:
            self.mob = i.getVal()
            if self.checkExMobiles():
                self.otpEntered = True
                try:
                    self.otp = sendOtp(self.mob,'creating new account')
                    takeInp(self,'ENTER OTP',4,'pass')
                except:
                    prompt('INVALID MOBILE NUMBER','Our System is unable to communicate\nwith the this mobile number.',w=adminWidget)
        else:
            self.mobileEntered = True
            takeInp(self,'ENTER MOBILE NUMBER')

    def checkExMobiles(self):
        if self.mob in getMobiles():
            if self.isNewUser:
                prompt('ERROR!','USER ALREADY EXISTS',w=adminWidget)
                return False
            else:
                return True
        else:
            if self.isNewUser:
                return True
            else:
                prompt('ERROR!','NO USER FOUND WITH THIS\nMOBILE NUMBER',w=adminWidget)
                return False

    def createUser(self):
        if self.isNewUser:
            createCust(self.name[0],self.name[1],self.mob)
        self.custId = str(fetchCustIdFromMob(self.mob))
        self.createAc()
    def createAc(self):
        insertAc(self.custId)
        self.accNo = fetchLastAc(self.custId)
        if self.isNewUser:
            msg = 'New Customer Id : '+self.custId+'\nAccount Number : '+str(self.accNo)
        else:
            msg = 'Existing Customer Id : '+self.custId+'\nAccount Number : '+str(self.accNo)
        prompt('ACCOUNT CREATED SUCCESSFULLY!',msg,w = adminWidget)