import os
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QSystemTrayIcon
from PySide6.QtGui import QIcon, QAction

class TrayIcon:
    def __init__(self, app:QApplication, mainWindow:QWidget) -> None:
        self.app = app
        self.tray_icon = QSystemTrayIcon()
        print(os.path.abspath(os.path.join(os.path.dirname(__file__),"static/icon.jpg")))
        self.tray_icon.setIcon(QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__),"static/icon.jpg"))))
        self.tray_icon.setToolTip("Hood Proxy")
        self.tray_icon.show()
        
        self.mainWindow:QWidget = mainWindow
        
        self.__create_context_menu()

        # Connect the system tray icon's signal
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Show the system tray icon
        self.tray_icon.show()

    def __create_context_menu(self) -> None:
        # Create the system tray context menu
        self.tray_menu = QMenu()
        self.show_action = QAction("显示主窗口", self.mainWindow)
        self.show_action.triggered.connect(self.show)
        self.proxy_action = QAction("开启代理")
        self.proxy_action.triggered.connect(self.change_proxy_status)
        self.quit_action = QAction("退出")
        self.quit_action.triggered.connect(self.quit)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.proxy_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
    

    def tray_icon_activated(self, reason:QSystemTrayIcon.ActivationReason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            print("Tray icon clicked!")
            self.mainWindow.show()
            
    def show(self):
        self.mainWindow.show()
        
    def change_proxy_status(self):
        pass
    
    def quit(self):
        self.mainWindow.close()
        self.app.quit()


if __name__ == "__main__":
    tray_icon = TrayIcon()