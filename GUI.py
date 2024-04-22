from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QFileDialog, QVBoxLayout
from RDT import AppClient
import os


class MessageReceiverThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, app_client: AppClient):
        super().__init__()
        self.app_client = app_client

    def run(self):
        while True:
            message = self.app_client.get_next_message()
            self.new_message.emit(message)


class TCPReceiverThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, app_client: AppClient):
        super().__init__()
        self.app_client = app_client

    def run(self):
        while True:
            message = self.app_client.get_next_file_sent()
            self.new_message.emit(message)


class UI_MainWindow(QMainWindow):
    def __init__(self, name, configs):
        super().__init__()
        self.app_client = AppClient(**configs)
        self.name = name

        self.setWindowTitle(self.name)
        self.setObjectName("MainWindow")
        self.resize(987, 672)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        #mainLayout
        mainLayout = QVBoxLayout(self.centralwidget)
        # View messages
        self.ViewMessages = QtWidgets.QTextEdit(self.centralwidget)
        self.ViewMessages.setReadOnly(True)
        self.ViewMessages.setObjectName("ViewMessages")
        mainLayout.addWidget(self.ViewMessages)
        # Input text
        ##LowerLayout
        lowerLayout = QHBoxLayout()
        self.InputText = QtWidgets.QLineEdit(self.centralwidget)
        self.InputText.setObjectName("InputText")
        self.InputText.setPlaceholderText("Input your text here.")
        self.InputText.setFixedHeight(55)
        lowerLayout.addWidget(self.InputText, stretch=10)
        
        # Send message button
        self.SendMessage = QtWidgets.QPushButton(self.centralwidget)
        self.SendMessage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/SendingMessage2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SendMessage.setIcon(icon)
        self.SendMessage.setIconSize(QtCore.QSize(50, 50))
        self.SendMessage.setObjectName("SendMessage")
        lowerLayout.addWidget(self.SendMessage, stretch=1)

        self.InputText.returnPressed.connect(self.SendMessage.click)
        # Send file button
        self.SendFile = QtWidgets.QPushButton(self.centralwidget)
        self.SendFile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/SendingFile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SendFile.setIcon(icon1)
        self.SendFile.setIconSize(QtCore.QSize(50, 50))
        self.SendFile.setObjectName("SendFile")
        lowerLayout.addWidget(self.SendFile, stretch=1)
        
        mainLayout.addLayout(lowerLayout)
        
        #status bar
        self.statusBar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # connect sending
        self.SendMessage.clicked.connect(self.send_message)
        self.SendFile.clicked.connect(self.send_file)

        # connect receiving messages
        self.receiver_thread = MessageReceiverThread(self.app_client)
        self.receiver_thread.new_message.connect(self.display_message)
        self.receiver_thread.start()

        # connect receiving files
        self.file_receiver_thread = TCPReceiverThread(self.app_client)
        self.file_receiver_thread.new_message.connect(self.file_received)
        self.file_receiver_thread.start()

    def send_message(self):
        message = self.InputText.text()
        if message:
            self.app_client.send_message(message)
            self.ViewMessages.append("<span style='color: orange;'>You: " + message + "</span>")
            self.InputText.clear()

    def display_message(self, message):
        self.ViewMessages.append("<span style='color: green;'>Them: " + message + "</span>")

    def send_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.centralwidget, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if not file_path:
            return

        if len(os.path.basename(file_path)) > 40:
            self.statusBar.showMessage("Failed: File name should be less than 20 characters", 4000)
            return

        success = self.app_client.send_file(file_path)
        if success:
            self.statusBar.showMessage("File is being sent", 4000)  # Show temporary message for 4 seconds
        else:
            self.statusBar.showMessage("Failed: another transfer in progress", 4000)

    def file_received(self, filename):
        self.ViewMessages.append("<span style='color: red;'>File \"" + filename + "\" received </span>")

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # Change this key to whichever you want
            self.SendMessage.click()

