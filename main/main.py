from os import path
from PySide6 import QtCore, QtWidgets, QtGui
import getpass
import sys
import os

class FolderAutomation(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FolderAutomation, self).__init__(parent)
        self.setWindowTitle("Simple Project Creator")

        user = getpass.getuser()

        PATH_LINE = "defaultPath="
        CONFIG_PATH = "conf.txt"
        DEFAULT_PATH = rf"C:\Users\{user}\Downloads"

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)

        if not path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "w") as file:
                file.write("Theres only one but he's the chosen one so he gets his own file \n\n")
                file.write(PATH_LINE+DEFAULT_PATH+"\n")
        
        with open(CONFIG_PATH, "r") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith(PATH_LINE):
                self.defaultPath = line.split(PATH_LINE)[-1].strip()

        self.title = QtWidgets.QLabel("Make A Project")
        self.title.setFont(font)

        self.text1 = QtWidgets.QLabel("Set a name for your Project:")
        self.text2 = QtWidgets.QLabel("Files to add in Project (Seperate with ',')")

        self.button = QtWidgets.QPushButton("Create Project")

        self.button.setFont(font)

        self.project_name_input = QtWidgets.QLineEdit("")
        self.project_name_input.setPlaceholderText("Type Project name here..")
        self.included_files_input = QtWidgets.QLineEdit("main.py,")
        self.included_files_input.setPlaceholderText("Put some files here..")

        self.default_path = QtWidgets.QCheckBox("Create in default path")
        self.default_path.setChecked(True)
        self.default_path.stateChanged.connect(self.toggle_path_search)

        self.path = QtWidgets.QLabel(self.defaultPath)
        self.path.setVisible(not self.default_path.isChecked())

        self.path_search = QtWidgets.QPushButton("Search..")
        self.path_search.setVisible(not self.default_path.isChecked())
        self.path_search.clicked.connect(self.browse_path)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(self.title)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.text1)
        self.layout.addWidget(self.project_name_input, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.default_path)
        self.layout.addWidget(self.path)
        self.layout.addWidget(self.path_search, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.included_files_input, alignment=QtCore.Qt.AlignLeft)
        self.layout.addStretch()
        self.layout.addWidget(self.button)


        self.button.clicked.connect(
            lambda: self.make_project(
                self.project_name_input.text(),
                self.path.text(),
                self.included_files_input.text()
            )
        )

    def make_project(self, name, path, included_files):
        if not name:
            QtWidgets.QMessageBox.information(self, "Error", "Name is not set")
            return

        project_dir = os.path.join(path, name)
        try:
            os.makedirs(project_dir, exist_ok=False)
        except FileExistsError:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Project folder '{project_dir}' already exists.")
            return

        files = [f.strip() for f in included_files.split(",") if f.strip()]
        for file_name in files:
            file_path = os.path.join(project_dir, file_name)
            try:
                with open(file_path, "x") as f:
                    pass
            except FileExistsError:
                QtWidgets.QMessageBox.warning(self, "Warning", f"File '{file_name}' already exists in the project folder.")

        QtWidgets.QMessageBox.information(self, "Info", f"Folder {name} was created succesfully in '{path}'")


    def browse_path(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path.setText(folder)       

    def toggle_path_search(self, state):
        self.path_search.setVisible(not self.default_path.isChecked())
        self.path.setVisible(not self.default_path.isChecked())
        self.path.setText(self.defaultPath)



if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # Create and show the form
    form = FolderAutomation()
    form.resize(800, 600)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
