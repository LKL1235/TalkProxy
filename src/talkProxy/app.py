import logging
import os
import sys

from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from talkProxy.hysteria_ui import Widget
from talkProxy.trayIcon import TrayIcon
from talkProxy.tools.settingReader import SettingReader
from talkProxy.tools.config import GlobalConfig

def main():
    app = QApplication(sys.argv)
    widget = Widget()
    apply_stylesheet(app, theme='dark_teal.xml')
    widget.show()
    trayIcon = TrayIcon(app, widget)  # noqa: F841
    res = SettingReader.InitConfig(os.path.join(os.path.dirname(__file__),'config/config.yaml'))
    if not res:
        logging.error('config文件读取失败')
        sys.exit(1)
    config = GlobalConfig.InitConfig()
    if not config:
        logging.error('GlobalConfig 初始化失败')
        sys.exit(1)
    
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()