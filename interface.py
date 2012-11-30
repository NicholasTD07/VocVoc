#!/usr/bin/env python3
"""
This is the interface of the VocVoc.
"""

# PyQt4
from PyQt4.QtGui import QDialog, QPushButton, QListWidget, QLineEdit,\
        QStatusBar, QLabel, QVBoxLayout, QFileDialog, QListWidgetItem,\
        QMessageBox, QApplication
from PyQt4.QtCore import QFile, Qt
from PyQt4.phonon import Phonon

# re
from re import compile as reCompile

# logging
import logging

# os
from os.path import basename

# url
#from urllib.request import urlopen

# misc
from misc import *


__all__ = ['VocDialog', 'App']


class VocDialog(QDialog) :

    """This is the dialog which presents the interface and organise everything."""

    MAGICWORD = 'CHANGEME'
    findDight = reCompile(r'\d+')
    baseURL = 'http://www.gstatic.com/dictionary/static/sounds/de/0/CHANGEME.mp3'

    def __init__(self, parent=None) :
        super(VocDialog, self).__init__(parent)
        self.logger = logging.getLogger('VocVoc.VocDialog')
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.info('Starting VocDialog.')
        self.mediaObeject = Phonon.createPlayer(Phonon.MusicCategory, Phonon.MediaSource(''))
        self.setupUi()
        self.connect()
        self.info('VocDialog started.')

    def setupUi(self) :
        "Setup the UI."
        self.info('Seting up the UI.')
        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.fileDialog.setViewMode(QFileDialog.Detail)

        self.loadButton = QPushButton( r"Open\New :", self)
        self.loadButton.setAutoDefault(False)

        self.textList = QListWidget(self)

        self.inputLine = QLineEdit(self)

        self.statusBar = QStatusBar(self)
        self.statusBar.addWidget( QLabel('Hello World! I love YOU!!!') )

        VBox = QVBoxLayout()
        for item in [self.loadButton, self.textList, self.inputLine, self.statusBar] :
            VBox.addWidget(item)

        self.setLayout(VBox)
        #self.resize()
        self.setWindowTitle("VocVoc -- Your Vocabulary Helper")
        self.info('UI is set up now.')

    def connect(self) :
        "Connect signals and slots in the UI."
        self.info('Connecting signals and slots.')
        inputLine = self.inputLine
        loadButton = self.loadButton
        mediaObeject = self.mediaObeject
        loadButton.clicked.connect(self.loadFile)
        inputLine.returnPressed.connect(self.addText)
        if self.logger.isEnabledFor(logging.DEBUG) :
            mediaObeject.stateChanged.connect( self.errorState )
        self.info('Signals and slots connected.')

    def errorState(self, state) :
        errorStates = {
                        0: 'Loading',
                        1: 'Stopped',
                        2: 'Playing',
                        3: 'Buffering',
                        4: 'Paused',
                        5: 'Error'
                        }
        msg ='{} state in Phonon!'.format( errorStates[state]) 
        self.info(self.mediaObeject.errorType())
        if state == 5 :
            self.warn(msg)
        else :
            self.info(msg)

    def pronounce(self, word) :
        self.info('Preparing the url to pronounce.')
        url = self.baseURL.replace(self.MAGICWORD, word)
        self.mediaObeject.setCurrentSource(Phonon.MediaSource(url))
        self.mediaObeject.play()
        self.info('Pronounciation ended.')

    def addText(self) :
        "Get the text from the input line and add it to the file and the list."
        self.info('Adding text to textList and the file')
        textList = self.textList
        inputLine = self.inputLine
        addItem = textList.addItem
        text = inputLine.text().strip().lower()
        self.info( 'Input is {}.'.format(text) )
        setCurrentRow = textList.setCurrentRow

        addItem(text)
        inputLine.clear()
        setCurrentRow( textList.count() - 1 )
        if not text.startswith('#') : # Input with '#' means it is a comment. No need to pronounce it.
            self.pronounce(text)
        try : # With the try statement, it can be used as a pronounciation helper.
            flush(self.filePath, text)
        except Exception :
            self.info('Using this freely without writing to a file as a pronounciation helper.')

    def loadFile(self) :
        "Open the file dialog to select the file and try to start."
        # Open the file dialog.
        logger = logging.getLogger('VocVoc.VocDialog.loadFile')
        info = logger.info
        info('Preparing to load file.')
        textList = self.textList
        if ( self.fileDialog.exec() ) :
            info('Dialog executed sucessfully.')
            filePath = self.fileDialog.selectedFiles()[0]
            fileName = basename(filePath)
            # Create or read file.
            #if QFile.exists(filePath) : # File exists.
            try :
                with open(filePath, 'r+') as textFile :
                    info('File exists, openning up.')
                    writenText = textFile.read()
                writenText = writenText.splitlines()
                textList.clear()
                textList.addItems( writenText )
                textList.setCurrentRow( len(writenText)-1 )
                info('Added items to list and set current row to the last row.')
            except IOError as error : # File does not exist. We create one.
                info('File does not exist. Trying to find the dight in the name.')
                listNumber = self.findDight.search(fileName)
                if listNumber is None : # No number found in the text.
                    logger.warn('Dight not found in the filename. Try again.')
                    msg = 'No number found in the file name.\nPlease try again.'
                    QMessageBox.warning(self, 'List number NOT found.',
                            msg,
                            QMessageBox.Ok)
                    return msg
                else : # No existing file but found the number in the file name.
                    info('Dight Found. Creating file and adding first line.')
                    with open(filePath, 'x') as textFile :
                        firstLine = ''.join( ['# list ' ,str( listNumber.group() )] ) # Cannot put '\n' here.
                        textFile.write( ''.join([firstLine ,'\n']) )
                    textList.clear()
                    textList.addItem(firstLine) # Otherwise there would be a new line in the list.

            info('Set inputLine to write-enabled.')
            self.inputLine.setReadOnly(False)
            info('Pass textFile to the dialog')
            self.filePath = filePath


def App() :
    from sys import argv, exit
    app = QApplication(argv)
    app.setApplicationName(r"TheDevil's VocVoc")
    dialog = VocDialog()
    dialog.show()
    exit( app.exec_() )


if __name__ == '__main__' :
    App()

