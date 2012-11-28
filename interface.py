#!/usr/bin/env python3
"""
This is the interface of the VocVoc.
"""

# PyQt4
from PyQt4.QtGui import QDialog, QPushButton, QListWidget, QLineEdit,\
        QStatusBar, QLabel, QVBoxLayout, QFileDialog, QListWidgetItem,\
        QMessageBox, QApplication
from PyQt4.QtCore import QFile, Qt

# re
from re import compile as reCompile

# os
#from os.path import basename


__all__ = ['VocDialog', 'App']


class VocDialog(QDialog) :

    """This is the dialog which presents the interface and organise everything."""

    findDight = reCompile(r'\d+')

    def __init__(self, parent=None) :
        super(VocDialog, self).__init__(parent)
        self.setupUi()
        self.connect()

    def setupUi(self) :
        "Setup the UI."
        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.fileDialog.setViewMode(QFileDialog.Detail)

        self.loadButton = QPushButton( r"Open\New :", self)
        self.loadButton.setAutoDefault(False)

        self.textList = QListWidget(self)

        self.inputLine = QLineEdit(self)
        self.inputLine.setReadOnly(True)

        self.statusBar = QStatusBar(self)
        self.statusBar.addWidget( QLabel('Hello World! I love YOU!!!') )

        VBox = QVBoxLayout()
        for item in [self.loadButton, self.textList, self.inputLine, self.statusBar] :
            VBox.addWidget(item)

        self.setLayout(VBox)
        #self.resize()
        self.setWindowTitle("VocVoc -- Your Vocabulary Helper")

    def connect(self) :
        "Connect signals and slots in the UI."
        inputLine = self.inputLine
        loadButton = self.loadButton
        loadButton.clicked.connect(self.loadFile)
        inputLine.returnPressed.connect(self.addText)

    def loadFile(self) :
        "Open the file dialog to select the file and try to start."
        # Open the file dialog.
        textList = self.textList
        if ( self.fileDialog.exec() ) :
            fileName = self.fileDialog.selectedFiles()[0]
            # Create or read file.
            #if QFile.exists(fileName) : # File exists.
            try :
                textFile = open(fileName, 'r+')
                writenText = textFile.read()
                writenText = writenText.splitlines()
                textList.clear()
                textList.addItems( writenText )
                textList.setCurrentRow( len(writenText)-1 )
            except IOError as error : # File does not exists. We create one.
                listNumber = self.findDight.search(fileName)
                if listNumber is None : # No number found in the text.
                    msg = 'No number found in the file name.\nPlease try again.'
                    QMessageBox.warning(self, 'List number NOT found.',
                            msg,
                            QMessageBox.Ok)
                    return msg
                else : # No existing file but found the number in the file name.
                    textFile = open(fileName, 'x')
                    firstLine = '# list ' + str( listNumber.group() )
                    textFile.write( firstLine +'\n' )
                    textList.clear()
                    textList.addItem(firstLine)

            self.inputLine.setReadOnly(False)
            self.textFile = textFile




    def addText(self) :
        "Get the text from the input line and add it to the file and the list."
        textList = self.textList
        addItem = textList.addItem
        write = self.textFile.write
        text = self.inputLine.text()
        setCurrentRow = textList.setCurrentRow

        addItem(text)
        setCurrentRow( textList.count() - 1 )
        write( text + '\n' )


def App() :
    from sys import argv, exit
    app = QApplication(argv)
    dialog = VocDialog()
    dialog.show()
    exit( app.exec_() )


if __name__ == '__main__' :
    main()

