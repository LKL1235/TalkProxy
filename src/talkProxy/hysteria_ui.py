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

class Widget(QWidget):
    def __init__(self, parent:Optional[any]=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setupSideMenu()

        
    def setupSideMenu(self):
        # 向page_0添加一个QPushButton
        indexChangeFuncList = []
        for i in range(0,len(self.ui.stackedWidget.children())-1):
            indexChangeFuncList.append(partial(self.ui.stackedWidget.setCurrentIndex,i))
        self.ui.proxyButton.clicked.connect(indexChangeFuncList[0])
        self.ui.subscriptionButton.clicked.connect(indexChangeFuncList[1])
        self.ui.connectionButton.clicked.connect(indexChangeFuncList[2])
        self.ui.ruleButton.clicked.connect(indexChangeFuncList[3])
        self.ui.logButton.clicked.connect(indexChangeFuncList[4])
        self.ui.testButton.clicked.connect(indexChangeFuncList[5])
        self.ui.settingButton.clicked.connect(indexChangeFuncList[6])
        
    def setupProxyPage(self):
        pass

    def closeEvent(self, event:QCloseEvent):
        # 重写closeEvent事件处理函数
        self.hide()
        event.ignore()
    
    def minimize(self):
        self.showMinimized()
        