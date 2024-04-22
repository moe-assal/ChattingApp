from GUI import UI_MainWindow
from PyQt5.Qt import QApplication
from infrastructure.config_reader import ConfigReader
import sys


def start(config_name):
    configs = ConfigReader(config_name)
    app = QApplication(sys.argv)
    ui = UI_MainWindow(configs.get_username(), configs.get_appclient_info())
    ui.show()
    app.exec_()
    ui.app_client.close_all()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: main <CONFIG FILE> ")
        exit(1)

    start(sys.argv[1])
