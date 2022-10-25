import sys
from PyQt5.QtWidgets import QStackedWidget,QApplication

from awsDb import fetchAccNoFromCard,fetchFirstNameFromCard

class Session():
    def setCardNo(self,cardNo):
        self.cardNo = cardNo
        self.accNo = fetchAccNoFromCard(cardNo)
        self.firstName = fetchFirstNameFromCard(cardNo)

newSession = Session()

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.setFixedHeight(420)
widget.setFixedWidth(700)

adminWidget = QStackedWidget()
adminWidget.setFixedHeight(420)
adminWidget.setFixedWidth(700)