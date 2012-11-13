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


class VocDialog(QDialog) :

    """This is the dialog which presents the interface and organise everything."""

    findDight = reCompile(r'\d+')

    def __init__(self, parent=None) :
        super(VocDialog, self).__init__(parent)
        self.setupUi()
        self.connect()

    def setupUi(self) :

        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.fileDialog.setViewMode(QFileDialog.Detail)

        self.loadButton = QPushButton( "Open\New :", self)
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
        inputLine = self.inputLine
        loadButton = self.loadButton
        loadButton.clicked.connect(self.loadFile)
        inputLine.returnPressed.connect(self.addText)

    def loadFile(self) :
        # Open the file dialog.
        textList = self.textList
        if ( self.fileDialog.exec() ) :
            fileName = self.fileDialog.selectedFiles()[0]
            # Create or read file.
            if QFile.exists(fileName) : # File exists.
                print(fileName)
                textFile = open(fileName, 'r+')
                writenText = textFile.read()
                writenText = writenText.splitlines()
                textList.clear()
                textList.addItems( writenText )
                textList.setCurrentRow( len(writenText)-1 )
            else : # File does not exists. We create one.
                listNumber = self.findDight.search(fileName)
                if listNumber is None : # No number found in the text.
                    QMessageBox.warning(self, 'List number NOT found.',
                            'No number found in the file name.\nPlease try again.',
                            QMessageBox.Ok)
                else : # No existing file and found the number in the file name.
                    textFile = open(fileName, 'x')
                    firstLine = '# list ' + str( listNumber.group() )
                    textFile.write( firstLine +'\n' )
                    textList.clear()
                    textList.addItem(firstLine)

            self.inputLine.setReadOnly(False)
            self.textFile = textFile




    def addText(self) :
        textList = self.textList
        write = self.textFile.write
        text = self.inputLine.text()
        addItem = textList.addItem
        setCurrentRow = textList.setCurrentRow

        addItem(text)
        setCurrentRow( textList.count() - 1 )
        write( text + '\n' )




if __name__ == '__main__' :

    import sys
    app = QApplication(sys.argv)
    dialog = VocDialog()
    dialog.show()
    sys.exit( app.exec_() )

