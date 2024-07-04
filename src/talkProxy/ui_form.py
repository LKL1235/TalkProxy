# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1140, 738)
        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(160, 10, 971, 721))
        self.stackedWidget.setMinimumSize(QSize(0, 75))
        self.page_0 = QWidget()
        self.page_0.setObjectName(u"page_0")
        self.stackedWidget.addWidget(self.page_0)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.stackedWidget.addWidget(self.page_6)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.stackedWidget.addWidget(self.page_1)
        self.verticalLayoutWidget = QWidget(Widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 10, 160, 531))
        self.verticalLayoutWidget.setMinimumSize(QSize(0, 75))
        self.sideMenuLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.sideMenuLayout.setSpacing(0)
        self.sideMenuLayout.setObjectName(u"sideMenuLayout")
        self.sideMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.proxyButton = QPushButton(self.verticalLayoutWidget)
        self.proxyButton.setObjectName(u"proxyButton")
        self.proxyButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.proxyButton)

        self.subscriptionButton = QPushButton(self.verticalLayoutWidget)
        self.subscriptionButton.setObjectName(u"subscriptionButton")
        self.subscriptionButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.subscriptionButton)

        self.connectionButton = QPushButton(self.verticalLayoutWidget)
        self.connectionButton.setObjectName(u"connectionButton")
        self.connectionButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.connectionButton)

        self.ruleButton = QPushButton(self.verticalLayoutWidget)
        self.ruleButton.setObjectName(u"ruleButton")
        self.ruleButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.ruleButton)

        self.logButton = QPushButton(self.verticalLayoutWidget)
        self.logButton.setObjectName(u"logButton")
        self.logButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.logButton)

        self.testButton = QPushButton(self.verticalLayoutWidget)
        self.testButton.setObjectName(u"testButton")
        self.testButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.testButton)

        self.settingButton = QPushButton(self.verticalLayoutWidget)
        self.settingButton.setObjectName(u"settingButton")
        self.settingButton.setMinimumSize(QSize(158, 75))

        self.sideMenuLayout.addWidget(self.settingButton)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"DashBoard", None))
        self.proxyButton.setText(QCoreApplication.translate("Widget", u"\u4ee3\u7406", None))
        self.subscriptionButton.setText(QCoreApplication.translate("Widget", u"\u8ba2\u9605", None))
        self.connectionButton.setText(QCoreApplication.translate("Widget", u"\u8fde\u63a5", None))
        self.ruleButton.setText(QCoreApplication.translate("Widget", u"\u89c4\u5219", None))
        self.logButton.setText(QCoreApplication.translate("Widget", u"\u65e5\u5fd7", None))
        self.testButton.setText(QCoreApplication.translate("Widget", u"\u6d4b\u8bd5", None))
        self.settingButton.setText(QCoreApplication.translate("Widget", u"\u8bbe\u7f6e", None))
    # retranslateUi

