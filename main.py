from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, Qt
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import platform
import subprocess
import images

global paths
paths = {}


def reverse(pdf_reader, path):
    pdf_writer = PdfFileWriter()

    for page in reversed(range(pdf_reader.getNumPages())):
        pdf_writer.addPage(pdf_reader.getPage(page))

    with open(path, 'wb') as out:
        pdf_writer.write(out)


class PageSelectionButton(QtWidgets.QPushButton):
    def __init__(self, position: str, page_selected: QtWidgets.QCheckBox, status: QtWidgets.QLabel, generate: QtWidgets.QPushButton):
        super().__init__()
        self.setAcceptDrops(True)
        self.position = position
        self.page_selected = page_selected
        self.status = status
        self.generate = generate

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        if event.mimeData().hasUrls and len(event.mimeData().urls()) == 1 \
                and event.mimeData().urls()[0].toLocalFile().endswith(".pdf"):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            paths[self.position] = event.mimeData().urls()[0].toLocalFile()
            self.page_selected.setChecked(True)

            if paths.get('back') not in [None, "", "invalid type"] and paths.get('front') not in [None, "", "invalid type"]:
                self.generate.setDisabled(False)
                self.status.setText("Ready")
        else:
            event.ignore()


class Ui_MainWindow(QtGui.QWindow):
    def __init__(self):
        super().__init__()

    def setupWindowSettings(self):
        MainWindow.setObjectName("Double PDF")
        MainWindow.resize(800, 431)
        MainWindow.setFixedSize(800, 431)
        MainWindow.setWindowIcon(QtGui.QIcon(":/doublePDFicon/DoublePDF.ico"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(0, 40, 801, 21))
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        font.setPointSize(16)
        self.title.setFont(font)
        self.title.setTextFormat(QtCore.Qt.AutoText)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")

    def createVerticalLayout(self):
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 100, 331, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

    def createHorizontalLayout(self):
        self.frontPagesHorizontalLayout = QtWidgets.QHBoxLayout()
        self.backPagesHorizontalLayout = QtWidgets.QHBoxLayout()

    def createFrontAndBackPages(self):
        self.frontPagesSelected = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.frontPagesSelected.setDisabled(True)
        self.frontPages = PageSelectionButton("front", self.frontPagesSelected, self.status, self.generate)
        self.frontPages.setObjectName("Front Page")
        self.frontPagesHorizontalLayout.addWidget(self.frontPagesSelected, 0)
        self.frontPagesHorizontalLayout.addWidget(self.frontPages, 1)
        self.verticalLayout.addLayout(self.frontPagesHorizontalLayout)

        self.backPagesSelected = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.backPages = PageSelectionButton("back", self.backPagesSelected, self.status, self.generate)
        self.backPages.setObjectName("Back Page")
        self.backPagesSelected.setDisabled(True)
        self.backPagesHorizontalLayout.addWidget(self.backPagesSelected, 0)
        self.backPagesHorizontalLayout.addWidget(self.backPages, 1)
        self.verticalLayout.addLayout(self.backPagesHorizontalLayout)

    def createStatusLabel(self):
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(390, 220, 121, 21))
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        font.setPointSize(11)
        self.status.setFont(font)
        self.status.setObjectName("generated_status")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(280, 220, 81, 21))
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        font.setPointSize(12)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def setupUi(self, MainWindow):
        self.setupWindowSettings()
        self.createVerticalLayout()
        self.createHorizontalLayout()

        self.generate = QtWidgets.QPushButton(self.centralwidget)
        self.generate.setGeometry(QtCore.QRect(280, 260, 231, 81))
        self.generate.setObjectName("generate")
        self.generate.setDisabled(True)

        self.createStatusLabel()

        self.createFrontAndBackPages()

        self.credits = QtWidgets.QLabel(self.centralwidget)
        self.credits.setGeometry(QtCore.QRect(0, 360, 801, 41))
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        font.setPointSize(11)
        self.credits.setFont(font)
        self.credits.setTextFormat(QtCore.Qt.AutoText)
        self.credits.setAlignment(QtCore.Qt.AlignCenter)
        self.credits.setObjectName("credits")

        self.frontPages.clicked.connect(lambda: self.on_click("front"))
        self.backPages.clicked.connect(lambda: self.on_click("back"))
        self.generate.clicked.connect(lambda: self.on_click("generate"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_paths(self, position: str, url: str):
        paths[position] = url

    def on_click(self, position):
        self.generate.setDisabled(True)
        self.status.setText("Not Generated")

        if position != 'front' and position != 'back':
            if len(paths) >= 2:
                self.merge_pdfs()
            return

        self.openFileNameDialog(position)
        if position == 'front':
            if paths.get('front') == "invalid type":
                self.frontPagesSelected.setChecked(False)
                self.status.setText("Invalid Filetype")
                return
            elif paths.get('front') != "":
                self.frontPagesSelected.setChecked(True)
            else:
                self.frontPagesSelected.setChecked(False)
                return

        elif position == "back":
            if paths.get('back') == "invalid type":
                self.backPagesSelected.setChecked(False)
                self.status.setText("Invalid Filetype")
            elif paths.get('back') != "":
                self.backPagesSelected.setChecked(True)
            else:
                self.backPagesSelected.setChecked(False)
                return

        if paths.get('back') not in [None, "", "invalid type"] and paths.get('front') not in [None, "","invalid type"]:
            self.generate.setDisabled(False)
            self.status.setText("Ready")
        else:
            self.generate.setDisabled(True)

    def openFileNameDialog(self, position):
        filename: str = QFileDialog.getOpenFileName()[0]

        if filename.endswith(".pdf"):
            paths[position] = filename
        elif len(filename) == 0:
            paths[position] = ""
        else:
            paths[position] = "invalid type"

    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Double PDF"))
        self.title.setText(_translate("MainWindow", "Double Sided PDF Generator"))
        self.frontPages.setText(_translate("MainWindow", "Front Pages"))
        self.backPages.setText(_translate("MainWindow", "Back Pages"))
        self.generate.setText(_translate("MainWindow", "Generate"))
        self.credits.linkActivated.connect(self.link)
        self.credits.setText(
            _translate("MainWindow", 'Made with ♡ by <a href="https://techforgoodinc.org">Tech For Good Inc</a>'))
        self.status.setText(_translate("MainWindow", "Not Generated"))
        self.status_label.setText(_translate("MainWindow", "Status:"))

    def merge_pdfs(self):
        page_list = []
        pdf_writer = PdfFileWriter()

        output: str = paths['front']
        output = output[:output.rindex("/")]

        front_path = paths['front']
        back_path = paths['back']

        file_name = f'{front_path[front_path.rindex("/") + 1: front_path.rindex(".")]} + {back_path[back_path.rindex("/") + 1:back_path.rindex(".")]}.pdf'

        output += f'/{file_name}'

        for path in paths.keys():
            pdf_reader = PdfFileReader(paths[path])
            counter = 0

            if path == 'front':
                counter = 0

            if path == 'back':
                counter = 1

                pths = paths['front']
                pths = output[:output.rindex("/")]
                path_reversed = pths + "/reversed.pdf"
                reverse(pdf_reader, path_reversed)
                pdf_reader = PdfFileReader(path_reversed)

            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                page_list.insert(counter, pdf_reader.getPage(page))
                counter += 2

        for page in page_list:
            pdf_writer.addPage(page)


        if os.path.exists(output):

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Combined PDF already exists.')
            msg.setWindowTitle("Rewrite Error")
            msg.setWindowIcon(QtGui.QIcon(":/doublePDFicon/DoublePDF.ico"))
            msg.setStandardButtons(QMessageBox.Ignore | QMessageBox.Abort)
            msg.setDefaultButton(QMessageBox.Abort)
            return_value = msg.exec_()

            if return_value != QMessageBox.Ignore:
                self.generate.setDisabled(False)
                return


        # Write out the merged PDF
        with open(output, 'wb') as out:
            pdf_writer.write(out)

        self.status.setText("Generated")

        directory = output[:output.rindex("/")]

        os.remove(path_reversed)

        if platform.system() == "Windows":
            os.startfile(directory)
        elif platform.system() == "MacOS":  # TODO: Check if works on MacOS
            subprocess.call(["open", "-R", directory])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
