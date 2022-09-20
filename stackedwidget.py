import sys
from PyQt5.QtWidgets import QStackedWidget,QApplication

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.setFixedHeight(420)
widget.setFixedWidth(700)

adminWidget = QStackedWidget()
adminWidget.setFixedHeight(420)
adminWidget.setFixedWidth(700)