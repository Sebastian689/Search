import os
import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QComboBox, QListWidget, QListWidgetItem
from ctypes import windll
import platform
import string
import difflib
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_is_toggled = False

        self.setWindowTitle("Windows Search")
        # self.setFixedSize(QSize(400, 300))
        self.resize(QtCore.QSize(600,400))

        self.file_name = QLineEdit(self)
        self.file_name.installEventFilter(self)
        
        search_file_button = QPushButton("Search File")
        search_file_button.clicked.connect(self.search_file)
        
        self.drive_combo = QComboBox()
        self.populate_drives()
        
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.open_file)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select drive to search"))
        layout.addWidget(self.drive_combo)

        layout.addWidget(QLabel("Select file to search"))
        layout.addWidget(self.file_name)
        layout.addWidget(self.results_list)
        layout.addWidget(search_file_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        
    def populate_drives(self):
        system = platform.system()
        
        if system == 'Windows':
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & (1 << ord(letter) - ord('A')):
                    drive = f"{letter}:\\"
                    self.drive_combo.addItem(drive, drive)
        else:
            print("Sorry your system sucks")
        
    def search_file(self):
        print("Searching for files...")
        
        search_path = os.path.abspath(self.drive_combo.currentData())
        if not os.path.exists(search_path):
            return
        
        file_name = self.file_name.text().lower()
        
        matches = []
        
        for root, _, files in os.walk(search_path):
            for filename in files:
                similarity = difflib.SequenceMatcher(None, file_name, filename.lower()).ratio()
                
                if similarity >= 0.6:
                    full_path = os.path.join(root, filename)
                    matches.append((full_path, similarity))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        matches = matches[:10]
        
        for items in matches:
            print(items)
            
        for file_path, _ in matches:
            item = QListWidgetItem(f"{file_path}")
            self.results_list.addItem(item)
            
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and obj is self.file_name:
            if event.key() == QtCore.Qt.Key.Key_Return and self.file_name.hasFocus():
                print('Enter pressed')
                self.search_file()
        return super().eventFilter(obj, event)

    def open_file(self, item):
        file_path = item.data(QtCore.User)
        self.status_label.setText(f"Opening: {file_path}")
        import subprocess
        subprocess.Popen(['start', file_path], shell=True)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()