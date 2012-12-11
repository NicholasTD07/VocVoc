VocVoc
======

VocVoc is a vocabulary building helper.

Why use it?
----------------

+ If You want to know how a word sounds like.
+ If you are not sure about the spelling of a word.
+ If you are trying to memorize (a lot of) vocabulary.
+ If you want to put all these vocabulary into a file for later review.

Install
-------

Just download the latest version from [here] [master].

Before you run it by clicking VocVoc.py or ./VocVoc.py in the console,
as I wrote this in [Python][] ,actually in [Python3.3][Pthon3], and used [PyQt][] as the graphical library,
you need to have [Python3][] and [PyQt][].
If you use linux, say Arch, please install Python3 and PyQt with pacman command.
If you use Windows, see Download below.

Usage
-----

Not yet.

ShortCut
--------

### TextList ###

* 1. Enter : Read the word and go to the next one in the list.
* 2. J : The same as Enter.
* 3. K : Almost the same as J, and Enter, but go backward(upward) in the list.

### InputLine ###

* 1. CtrlN : If the `Do you mean` spelling tip is there, you can go through the candidates in the tip with CtrlN(forward).
* 2. CtrlP : Almost the same as CtrlN, but in another direction which is backward.

Download
--------

[Python3.3 for Windows] [Python3.3-win]

[PyQt 4.9.5 for Windows-x86] [PyQt-Py3.3-x86-4.9.5]

[PyQt 4.9.5 for Windows-x64] [PyQt-Py3.3-x64-4.9.5]

Why do I write it?
--------------

As preparing for the GRE test, especially the vocabulary part following a 
alphabetic order, with so many words looking just like each other but with 
different pronunciations, I fell really unconfident about their pronunciation,
through recentlly I got a score at 7.5 in IELTS. So I would like to write a
small program for myself which I can use to find out pronunciation of
different vocabulary. After some days of programming, this is it.

TODO
----
* ✓ check the spelling of the input.
* ✓ take text file `filename.txt` to generate a vocabulary model and save the model in `VocVoc/pickles/`.
* ✓ play the pronunciation of the word(using google's pronunciations).
* ✓ take text files in `VocVoc/corpuses` and automatically train the model and save that.
* ✓ find the word in all the corpuses inside the `VocVoc/corpuses` folder, and display its context in the dialog right to the list.
* ✓ able to use CtrlN and CtrlP to selete the canditates shown in the `Do you mean` tip.
*   find the word in certain websites' pages and present the context.

License
-------

Please see [GNU General Public License v3] [GPLv3]

[master]:https://github.com/thedevil7/VocVoc/archive/master.zip
[Python]:http://www.python.org/
[Python3]:http://www.python.org/download/releases/3.3.0/
[Python3.3-win]:http://www.python.org/ftp/python/3.3.0/python-3.3.0.msi
[PyQt]:http://www.riverbankcomputing.com/software/pyqt/intro
[PyQt-Py3.3-x64-4.9.5]:http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.5/PyQt-Py3.3-x64-gpl-4.9.5-1.exe
[PyQt-Py3.3-x86-4.9.5]:http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.5/PyQt-Py3.3-x86-gpl-4.9.5-1.exe
[GPLv3]:http://www.gnu.org/licenses/gpl-3.0-standalone.html
