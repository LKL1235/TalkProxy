from functools import partial
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,    # noqa: F401
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from talkProxy.ui_form import Ui_Widget
from typing import Optional

from .tools.config import GlobalConfig, Subscription

class Widget(QWidget):
    def __init__(self, parent:Optional[any]=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.globalConfig:GlobalConfig = GlobalConfig.InitConfig()
        self.subscription = None
        self.setupSubscriptionList()
        self.setupSideMenu()
        self.setupProxyPage()
        self.setupSubscriptionPage()

    def setupSubscriptionList(self):
        self.subscription_list = self.globalConfig.subscriptionConfig.get_subscription_all()
        
    def setupSideMenu(self):
        self.ui.proxyButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.proxyPage)))
        self.ui.subscriptionButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.subscriptionPage)))
        self.ui.connectionButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.connectionPage)))
        self.ui.ruleButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.rulePage)))
        self.ui.logButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.logPage)))
        self.ui.testButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.testPage)))
        self.ui.settingButton.clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex,self.ui.stackedWidget.indexOf(self.ui.settingPage)))
        
    def setupProxyPage(self,name:str=None):
        if not name:
            self.subscription = self.globalConfig.get_default_subscription()
        else:
            self.subscription = self.globalConfig.subscriptionConfig.get_subscription(name)
        if not self.subscription:
            return False
        for index, proxy in enumerate(self.subscription.files):
            button = QPushButton(self.ui.proxyPage)
            button.setObjectName(proxy['name'])
            size = self.ui.stackedWidget.geometry()
            button.setText(QCoreApplication.translate("Widget", proxy['name'], None))
            button.setGeometry(QRect(10, 10+index*85, int(size.width()/3), 100))
        return True
        
    def setupSubscriptionPage(self):
        for index, subscription in enumerate(self.subscription_list):
            button = QPushButton(self.ui.subscriptionPage)
            button.setObjectName(subscription.name)
            size = self.ui.stackedWidget.geometry()
            button.setText(QCoreApplication.translate("Widget", subscription.name, None))
            button.setGeometry(QRect(10, 10+index*85, int(size.width()/3), 100))
        

    def closeEvent(self, event:QCloseEvent):
        # 重写closeEvent事件处理函数
        self.hide()
        event.ignore()
    
    def minimize(self):
        self.showMinimized()
        