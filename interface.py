#!/usr/bin/env python3
"""
This is the interface of the VocVoc.
"""

# PyQt4
from PyQt4.QtGui import QDialog, QPushButton, QListWidget, QLineEdit,\
        QStatusBar, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog,\
        QListWidgetItem, QTextEdit, QMessageBox, QApplication
from PyQt4.QtCore import QFile, Qt, pyqtSignal, QSettings
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

# glob
from glob import glob
# config
from config import __dir__

# SpellChecker
from spellchecker import WordModel, SpellChecker

# misc
from misc import *


__all__ = ['VocDialog', 'App']


class tabEnabledLineEdit(QLineEdit) :

    keyCode = { 16777249: 'Ctrl',
                78 : 'n',
                80 : 'p'
                }

    ctrlN = pyqtSignal()
    ctrlP = pyqtSignal()
                
    def __init__(self, parent=None) :
        self.logger = getLogger('VocVoc.VocDialog.lineEdit')
        self.info = self.logger.info
        self.debug = self.logger.debug
        self.keys = list()
        super(tabEnabledLineEdit, self).__init__(parent)

    def keyPressEvent(self, event) :
        keys = self.keys
        keyCode = self.keyCode
        key = event.key()
        if key in keyCode.keys() :
            keys.append(keyCode[key])
        self.debug('Key pressed : {}.'.format(key))
        if 'Ctrl' in keys :
            if 'n' in keys :
                self.ctrlN.emit()
                self.debug('Ctrl and n pressed.')
            elif 'p' in keys :
                self.ctrlP.emit()
                self.debug('Ctrl and p pressed.')
        super(tabEnabledLineEdit, self).keyPressEvent(event)

    def keyReleaseEvent(self, event) :
        key = event.key()
        keyCode = self.keyCode
        if key in keyCode.keys() :
            self.keys.remove(keyCode[key])
        self.debug('Key released : {}.'.format(key))
        super(tabEnabledLineEdit, self).keyReleaseEvent(event)


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
        self.readSettings()
        self.initCountWord()
        self.readFile()
        self.textList.setCurrentRow(self.lastRow)
        self.candidates = None
        self.autoProxy = autoProxy
        self.spellChecker = SpellChecker()
        self.correct = self.spellChecker.correct
        self.corpusDir = self.spellChecker.corpusDir
        self.info('VocDialog started.')

    def closeEvent(self, event) :
        if True :
            self.warn('Exiting and saving the settings.')
            self.saveSettings()
            event.accept()
        else :
            event.reject()

    def keyPressEvent(self, event) :
        self.debug('Key is {}.'.format(event.key()))
        super(VocDialog, self).keyPressEvent(event)

    def resizeEvent(self, event) :
        self.debug("Resized to {}.".format(self.size()))
        super(VocDialog, self).resizeEvent(event)

    def readSettings(self) :
        settings = QSettings(r"TheDevil's World", r"TheDevil's VocVoc")
        lastFilePath = settings.value('lastFilePath', '')
        self.lastRow = int(settings.value('row', 0))
        self.info('Reading {} as the filePath.'.format(lastFilePath))
        self.filePath = lastFilePath

    def saveSettings(self) :
        settings = QSettings(r"TheDevil's World", r"TheDevil's VocVoc")
        self.info('Saving {} as the filePath.'.format(self.filePath))
        settings.setValue('lastFilePath', self.filePath)
        settings.setValue('row', self.textList.currentRow())

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

        self.inputLine = tabEnabledLineEdit(self)

        self.toggleButton = QPushButton(r'Show/Hide', self)
        self.toggleButton.setAutoDefault(False)
        self.toggleButton.setCheckable(True)

        self.textLabel = QLabel()

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.inputLine)
        self.hBox.addWidget(self.toggleButton)

        self.statusBar = QStatusBar(self)
        msg = 'Hello World! I love YOU!!!'
        self.statusBar.showMessage(msg, 5000)

        vBox = QVBoxLayout()
        items = [self.loadButton, self.textList, self.hBox, self.statusBar]
        for item in items :
            try :
                vBox.addWidget(item)
            except :
                vBox.addLayout(item)

        self.textViewer = QTextEdit()
        self.textViewer.setHidden(True)
        self.textViewer.setReadOnly(True)

        HBox = QHBoxLayout()

        items = [vBox, self.textViewer]
        for item in items :
            try :
                HBox.addWidget(item)
            except :
                HBox.addLayout(item)
                
        self.setLayout(HBox)
        self.resize(350, 500)
        self.setWindowTitle("VocVoc -- Your Vocabulary Helper")
        self.info('UI is set up now.')

    def connect(self) :
        "Connect signals and slots in the UI."
        self.info('Connecting signals and slots.')
        self.accepted.connect(self.saveSettings)
        self.rejected.connect(self.saveSettings)
        self.loadButton.clicked.connect(self.loadFile)
        self.inputLine.returnPressed.connect(self.enteredText)
        self.inputLine.ctrlN.connect(self.completeHandler)
        self.inputLine.ctrlP.connect(lambda : self.completeHandler(False))
        self.textList.itemActivated.connect(self.itemActivated)
        self.toggleButton.clicked.connect(self.toggleViewer)
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
        self.info('Item Activated!')
        row = self.textList.row(item)
        text = item.text()
        if not text.startswith('#') :
            self.pronounce(item.text())
            self.findWord(text)
        elif 'end' in text.strip().lower() :
            self.play('end.mp3')
        else :
            self.play('beep.mp3')
        if row+1 != self.textList.count() :
            self.debug('NOT last row!')
            self.textList.setCurrentRow(row+1)
        else :
            self.debug('Last row!')
        self.info('Processed the activated item.')

    def toggleViewer(self) :
        if self.textViewer.isHidden() :
            self.resize(700, 500)
            self.textViewer.show()
            self.textViewer.clear()
            text = self.textList.currentItem().text()
            if not text.startswith('#') :
                self.findWord(text)
        else :
            self.textViewer.hide()
            self.textList.setFocus()
            self.resize(350, 500)

    def backAndForward(self, forward=True) :
        inputLine = self.inputLine
        word = inputLine.text()
        setText = inputLine.setText
        candidates = self.candidates
        count = len(candidates)
        try :
            position = candidates.index(word)
            self.debug('Position found.')
        except :
            position = None
            self.debug('Position not found.')
        if forward :
            if position is None or position == count - 1 : # At end
                position = -1
            setText( candidates[position+1] )
        else :
            if position is None or position == 0 :
                position = count
            setText( candidates[position-1] )

    def completeHandler(self, goNext=True) :
        inputLine = self.inputLine
        candidates = self.candidates
        word = inputLine.text()
        if candidates :
            self.backAndForward(goNext)

    def play(self, path) :
        self.mediaObeject.setCurrentSource(Phonon.MediaSource(path))
        self.mediaObeject.play()
        
    def pronounce(self, word) :
        self.info('Preparing the url to pronounce.')
        url = self.baseURL.replace(self.MAGICWORD, word)
        if not self.autoProxy :
            self.debug('Without the autoProxy, play it using the url as the source.')
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

    def findWord(self, word) :
        self.info('Finding word in the text file.')
        textViewer = self.textViewer
        if textViewer.isHidden() :
            return
        else :
            pass
        limit = 5
        contexts = list()
        textLines = list()
        corpuses = glob(''.join([self.corpusDir, '/*']))
        self.debug('Found corpuses : {}.'.format(corpuses))
        textViewer.clear()
        for corpus in corpuses :
            textLines.append(locateWord(corpus, word))
        for textLine in textLines :
            text, lines = textLine[0], textLine[1]
            title = ''.join( ['Title : ', basename(text[-1])] )
            if lines :
                for line in lines :
                    wantedLines = text[line-limit: line+limit]
                    #cleanLines = map(self.replace, wantedLines)
                    context = ''.join(wantedLines)
                    context = context.replace(word, ' '.join(['*', word, '*']))
                    context = context.replace('\n\n', self.MAGICWORD)
                    context = context.replace('\n', ' ')
                    context = context.replace(self.MAGICWORD, '\n\n')
                    contexts.append(''.join([title, '\n', context, '\n\n']))
        if contexts :
            for context in contexts :
                textViewer.append(context)
        else :
            textViewer.append('Sorry, {} not found.'.format(word))
        self.info('Word found and showed in the textViewer.')

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
            self.debug(msg)
            self.countWord[1] = word
            self.play('beep.mp3')
            return False
        elif self.countWord[0] == 2 :
            if word != self.countWord[1] : # Different word.
                self.debug('DIFEFRENT WORD.')
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
            self.candidates = candidates
            msg = 'Do you mean {} ?'.format(' ,'.join(candidates))
            showMessage(msg, 5000)
        else : # Collected in the wordModel.
            self.findWord(word)
            self.countWord[0] = 0
            self.debug('Word collected in the wordModel.')
            return True

        msg = 'wrongTime = {} with the word {}.'.format(self.countWord[0], word)
        self.logger.debug(msg)

        return self.wordCount(word)

    def addText(self, text) :
        self.info('Starting to add text.')
        textList = self.textList

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
            self.debug('Using this freely without writing to a file as a pronunciation helper.')
        self.info('Text added.')

    def enteredText(self) :
        "Get the text from the input line and add it to the file and the list."
        self.info('Adding text to textList and the file!')
        textList = self.textList
        text = self.inputLine.text().strip().lower()
        self.debug( 'Input is {}.'.format(text) )

        self.addText(text)

        self.info('Text added.')

    def readFile(self) :
        filePath = self.filePath
        debug = self.debug
        textList = self.textList
        # Create or read file.
        fileName = basename(filePath)
        try :
            with open(filePath, 'r+') as textFile :
                debug('File exists, openning up.')
                writenText = textFile.read()
            writenText = writenText.splitlines()
            textList.clear()
            textList.addItems( writenText )
            if not 'end' in writenText[-1].strip().lower() :
                textList.setCurrentRow( len(writenText)-1 )
            else :
                textList.setCurrentRow( 0 )
            debug('Added items to list and set current row to the last row.')
        except IOError as error : # File does not exist. We create one.
            debug('File does not exist. Trying to find the dight in the name.')
            listNumber = self.findDight.search(fileName)
            if listNumber is None : # No number found in the text.
                self.warn('Dight not found in the filename. Try again.')
                msg = 'No number found in the file name.\nPlease try again.'
                QMessageBox.warning(self, 'List number NOT found.',
                        msg,
                        QMessageBox.Ok)
                return msg
            else : # No existing file but found the number in the file name.
                debug('Dight Found. Creating file and adding first line.')
                with open(filePath, 'x') as textFile :
                    firstLine = ''.join( ['# list ' ,str( listNumber.group() )] ) # Cannot put '\n' here.
                    textFile.write( ''.join([firstLine ,'\n']) )
                textList.clear()
                textList.addItem(firstLine) # Otherwise there would be a new line in the list.

    def loadFile(self) :
        "Open the file dialog to select the file and try to start."
        # Open the file dialog.
        logger = getLogger('VocVoc.VocDialog.loadFile')
        info = logger.info
        debug = logger.debug
        debug('Preparing to load file.')
        textList = self.textList
        if ( self.fileDialog.exec() ) :
            debug('Dialog executed sucessfully.')
            filePath = self.fileDialog.selectedFiles()[0]
            self.filePath = filePath

            self.readFile()

            debug('Pass textFile to the dialog')
            info('File loaded.')


def App(autoProxy=False) :
    from sys import argv, exit
    app = QApplication(argv)
    app.setOrganizationName(r"TheDevil's World")
    app.setOrganizationDomain(r"TheDevilsWorld.com")
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
