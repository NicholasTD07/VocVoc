#!/usr/bin/env python3
"""
This is the interface of the VocVoc.
"""

# PyQt4
from PyQt4.QtGui import QDialog, QPushButton, QListWidget, QLineEdit,\
        QStatusBar, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog,\
        QListWidgetItem, QMessageBox, QApplication
from PyQt4.QtCore import QFile, Qt
from PyQt4.phonon import Phonon

# re
from re import compile as reCompile

# logging
from logging import DEBUG, getLogger

# os
from os.path import basename, join as pJoin

# tempfile
from tempfile import NamedTemporaryFile

# url
from urllib.request import urlopen
from urllib.error import HTTPError

# config
from config import __dir__

# SpellChecker
from spellchecker import WordModel, SpellChecker

# misc
from misc import *


__all__ = ['VocDialog', 'App']


class VocDialog(QDialog) :

    """This is the dialog which presents the interface and organise everything."""

    MAGICWORD = 'CHANGEME'
    findDight = reCompile(r'\d+')
    baseURL = 'http://www.gstatic.com/dictionary/static/sounds/de/0/CHANGEME.mp3'

    def __init__(self, autoProxy=False, parent=None) :
        super(VocDialog, self).__init__(parent)
        self.logger = getLogger('VocVoc.VocDialog')
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.debug = self.logger.debug
        if autoProxy :
            self.info('Starting VocDialog with autoProxy.')
        else :
            self.info('Starting VocDialog without autoProxy.')
        self.mediaObeject = Phonon.createPlayer(Phonon.MusicCategory, Phonon.MediaSource(''))
        self.setupUi()
        self.connect()
        self.autoProxy = autoProxy
        self.spellChecker = SpellChecker()
        self.correct = self.spellChecker.correct
        self.initCountWord()
        self.info('VocDialog started.')

    def resizeEvent(self, event) :
        self.debug("Resized to {}.".format(self.size()))
        super(VocDialog, self).resizeEvent(event)

    def initCountWord(self) :
        """
        The first one is a count about how many time the input is wrong.
          WRONG : Not collected in or can be corrected by the wordModel.
        The second one is the last time's wrong input.
        """
        self.countWord = [0, '']

    def setupUi(self) :
        "Setup the UI."
        self.info('Seting up the UI.')
        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.fileDialog.setViewMode(QFileDialog.Detail)

        self.loadButton = QPushButton( r'Open/New :', self)
        self.loadButton.setAutoDefault(False)

        self.textList = QListWidget(self)

        self.inputLine = QLineEdit(self)

        self.toggleButton = QPushButton(r'Show/Hide', self)
        self.toggleButton.setCheckable(True)

        self.textLabel = QLabel()

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.inputLine)
        self.hBox.addWidget(self.toggleButton)

        self.statusBar = QStatusBar(self)
        msg = 'Hello World! I love YOU!!!'
        self.statusBar.showMessage(msg, 5000)

        VBox = QVBoxLayout()
        items = [self.loadButton, self.textList, self.hBox, self.statusBar]
        for item in items :
            try :
                VBox.addWidget(item)
            except :
                VBox.addLayout(item)

        self.setLayout(VBox)
        self.resize(350, 500)
        self.setWindowTitle("VocVoc -- Your Vocabulary Helper")
        self.info('UI is set up now.')

    def connect(self) :
        "Connect signals and slots in the UI."
        self.info('Connecting signals and slots.')
        self.loadButton.clicked.connect(self.loadFile)
        self.inputLine.returnPressed.connect(self.addText)
        self.textList.itemActivated.connect(self.itemActivated)
        if self.logger.isEnabledFor(DEBUG) :
            self.mediaObeject.stateChanged.connect( self.errorState )
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

    def itemActivated(self, item) :
        row = self.textList.row(item)
        text = item.text()
        if not text.startswith('#') :
            self.pronounce(item.text())
        if row+1 != self.textList.count() :
            self.info('NOT last row!')
            self.textList.setCurrentRow(row+1)
        else :
            self.info('Last row!')

    def play(self, path) :
        self.mediaObeject.setCurrentSource(Phonon.MediaSource(path))
        self.mediaObeject.play()
        
    def pronounce(self, word) :
        self.info('Preparing the url to pronounce.')
        url = self.baseURL.replace(self.MAGICWORD, word)
        if not self.autoProxy :
            self.info('Without the autoProxy, play it using the url as the source.')
            self.play(url)
        else :
            self.info('With the autoProxy, play it after downloading the file.')
            try : # May happen HTTPError.
                resource = urlopen(url).read()
                tempFile = NamedTemporaryFile()
                tempFile.write(resource)
                self.play(tempFile.name)
            except HTTPError as error :
                self.warn(repr(error))
                self.warn('Pronounciation FAILED.')
        self.info('Pronounciation ended.')

    def wordCount(self, word=None) :
        """
        This function uses self.countWord to decide whether record and pronounce the input or not.
        RECORD : Add the input into the textList and write it into the file.
        If the word itself is correct, return True.
        Or if a wrong input were entered twice, return True.
        Otherwise with a one-time-entered wrong input, return False.
        """
        if self.countWord[0] == 0 : # The word is correct.
            self.countWord[1] = ''
            return True
        elif self.countWord[0] == 1 :
            msg = 'Maybe the word is WRONG? Playing beep and saving the word.'
            self.info(msg)
            self.countWord[1] = word
            self.play('beep.mp3')
            return False
        elif self.countWord[0] == 2 :
            if word != self.countWord[1] : # Different word.
                self.logger.debug('DIFFRENT WORD.')
                self.countWord[0] = 1 # Check again.
                self.countWord[1] = word # Update it.
                self.play('beep.mp3')
                return False
            else :
                self.countWord[0] = 0
                self.countWord[1] = ''
            return True
        else :
            self.countWord[0] = 0

    def checkWord(self, word) :
        statusBar = self.statusBar
        showMessage = statusBar.showMessage

        candidates = self.correct(word)
        if candidates is None : # Not collected.
            self.countWord[0] += 1
            showMessage('Are you sure?', 3000)
        elif candidates[0] != word : # Can be corrected.
            self.countWord[0] += 1
            msg = 'Do you mean {} ?'.format(' ,'.join(candidates))
            showMessage(msg, 5000)
        else : # Collected in the wordModel.
            self.info('Word collected in the wordModel.')
            self.countWord[0] = 0
            return True

        msg = 'wrongTime = {} with the word {}.'.format(self.countWord[0], word)
        self.logger.debug(msg)

        return self.wordCount(word)

    def addText(self) :
        "Get the text from the input line and add it to the file and the list."
        self.info('Adding text to textList and the file.')
        textList = self.textList
        text = self.inputLine.text().strip().lower()
        self.info( 'Input is {}.'.format(text) )

        if text.startswith('#') : # It is a comment.
            pass
        else : # It is a word.
            if self.checkWord(text) :
                self.pronounce(text)
            else : # self.checkWord(text) return False
                return

        self.inputLine.clear()
        textList.addItem(text)
        self.statusBar.clearMessage()
        textList.setCurrentRow( textList.count() - 1 )

        try : # With the try statement, it can be used as a pronunciation helper.
            flush(self.filePath, text)
        except Exception :
            self.info('Using this freely without writing to a file as a pronunciation helper.')

    def loadFile(self) :
        "Open the file dialog to select the file and try to start."
        # Open the file dialog.
        logger = getLogger('VocVoc.VocDialog.loadFile')
        info = logger.info
        info('Preparing to load file.')
        textList = self.textList
        if ( self.fileDialog.exec() ) :
            info('Dialog executed sucessfully.')
            filePath = self.fileDialog.selectedFiles()[0]
            fileName = basename(filePath)
            # Create or read file.
            try :
                with open(filePath, 'r+') as textFile :
                    info('File exists, openning up.')
                    writenText = textFile.read()
                writenText = writenText.splitlines()
                textList.clear()
                textList.addItems( writenText )
                if not 'end' in writenText[-1].strip().lower() :
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


def App(autoProxy=False) :
    from sys import argv, exit
    app = QApplication(argv)
    app.setApplicationName(r"TheDevil's VocVoc")
    dialog = VocDialog(autoProxy=autoProxy)
    dialog.show()
    exit( app.exec_() )


if __name__ == '__main__' :
    # this is why I have VocVoc.py
    #from VocVoc import getLogger as myLogger
    #myLogger()
    #App()
    pass
