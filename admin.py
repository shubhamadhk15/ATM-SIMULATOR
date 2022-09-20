from stackedwidget import adminWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from card_functions import cssLoader

def createAdminMenu():
    adminMenuObj = AdminMenu()
    adminWidget.addWidget(adminMenuObj)
    adminWidget.show()

class AdminMenu(QDialog):
    def __init__(self):
        super(AdminMenu,self).__init__()
        loadUi('UI/admin_menu.ui',self)
        self.setStyleSheet(cssLoader('style.css'))

