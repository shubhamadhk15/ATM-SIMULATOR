import sys
from PyQt5.QtWidgets import QStackedWidget,QApplication

from awsDb import fetchAccNoFromCard,fetchFirstNameFromCard,fetchCardExp,fetchLastNameFromAccNo,fetchCardType

class Session():
    def setCardNo(self,cardNo):
        self.cardNo = cardNo
        self.accNo = fetchAccNoFromCard(cardNo)
        self.firstName = fetchFirstNameFromCard(cardNo)
        self.lastName = fetchLastNameFromAccNo(self.accNo)
        self.cardExp = fetchCardExp(cardNo)
        self.cardType = fetchCardType(cardNo)

newSession = Session()

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.setFixedHeight(420)
widget.setFixedWidth(700)

adminWidget = QStackedWidget()
adminWidget.setFixedHeight(420)
adminWidget.setFixedWidth(700)