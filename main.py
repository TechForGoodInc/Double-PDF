from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import images


def reverse(pdf_reader, path):

    pdf_writer = PdfFileWriter()

    for page in reversed(range(pdf_reader.getNumPages())):
        pdf_writer.addPage(pdf_reader.getPage(page))

    with open(path, 'wb') as out:
        pdf_writer.write(out)


class Ui_MainWindow(object):
    def __init__(self):
        self.paths = {}

    def setupUi(self, MainWindow):
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
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 100, 331, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frontPages = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.frontPages.setObjectName("frontPages")
        self.verticalLayout.addWidget(self.frontPages)
        self.backPages = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.backPages.setObjectName("backPages")
        self.verticalLayout.addWidget(self.backPages)
        self.generate = QtWidgets.QPushButton(self.centralwidget)
        self.generate.setGeometry(QtCore.QRect(280, 260, 231, 81))
        self.generate.setObjectName("generate")
        self.credits = QtWidgets.QLabel(self.centralwidget)
        self.credits.setGeometry(QtCore.QRect(0, 360, 801, 41))
        font = QtGui.QFont()
        font.setFamily("IBM Plex Mono")
        font.setPointSize(11)
        self.credits.setFont(font)
        self.credits.setTextFormat(QtCore.Qt.AutoText)
        self.credits.setAlignment(QtCore.Qt.AlignCenter)
        self.credits.setObjectName("credits")
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

        self.frontPages.clicked.connect(lambda: self.on_click("front"))
        self.backPages.clicked.connect(lambda: self.on_click("back"))
        self.generate.clicked.connect(lambda: self.on_click("generate"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def on_click(self, position):
        if position == 'front' or position == 'back':
            self.openFileNameDialog(position)
        else:
            if len(self.paths) >= 2:
                self.merge_pdfs()

    def openFileNameDialog(self, position):
        self.paths[position] = QFileDialog.getOpenFileName()[0]

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
        self.credits.setText(_translate("MainWindow", 'Made with ♡ by <a href="https://techforgoodinc.org">Tech For Good Inc</a>'))
        self.status.setText(_translate("MainWindow", "Not Generated"))
        self.status_label.setText(_translate("MainWindow", "Status:"))

    def merge_pdfs(self):
        page_list = []
        pdf_writer = PdfFileWriter()

        output = self.paths['front']
        output = output[:output.rindex("/")]

        front_path = self.paths['front']
        back_path = self.paths['back']

        print(f'{front_path=}')
        print(f'{front_path.rindex("/")}')
        print(f'{front_path[front_path.rindex("/") + 1: front_path.rindex(".")]}')
        file_name = f'{front_path[front_path.rindex("/") + 1: front_path.rindex(".")]} + {back_path[back_path.rindex("/") + 1:back_path.rindex(".")]}.pdf'
        
        output += f'\{file_name}'

        for path in self.paths.keys():
            pdf_reader = PdfFileReader(self.paths[path])
            counter = 0

            if path == 'front':
                counter = 0

            if path == 'back':
                counter = 1

                pths = self.paths['front']
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

        os.remove(path_reversed)

        # Write out the merged PDF
        with open(output, 'wb') as out:
            pdf_writer.write(out)

        self.status.setText("Generated")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
