VocVoc
======

VocVoc 是学习单词的小助手.

可以用它来做什么?
-------------

+ 或许, 你不确定单词的拼写.
+ 或许, 你正在记忆许多的单词.
+ 或许, 你想听听一个单个单词的读音.
+ 又或许, 你想把要学习的单词统统放进一个文件, 方便以后复习.

安装
----

请在[这里][master] 下载最新的版本.

在你通过点击 VocVoc.py 或从命令行运行它之前, 请先下载运行所需的相关库文件.
因为我使用了 [Python][] ,实际上是 [Python3.3][Python3], 这门语言写下了 VocVoc,
并且利用 [PyQt][] 作为图形库, 所以你需要先安装他们.
如果你使用 Linux 系统, 请使用发行版自带的相关命令安装 Python3 和 PyQt.
如果你使用 Windows 系统, 请看下面的 下载.

下载
----

[Python3.3 for Windows] [Python3.3-win]

[PyQt 4.9.5 for Windows-x86] [PyQt-Py3.3-x86-4.9.5]

[PyQt 4.9.5 for Windows-x64] [PyQt-Py3.3-x64-4.9.5]

为什么会写这个软件?
-------------------

当我自己准备 GRE 时, GRE 的词汇很是让我头疼. 特别是那么多词汇看着都差不多,
但是读音却不同. 我当时特别想要一款软件, 能够方便的播放输入单词的读音.
于是我决定利用 Python 以及自己熟悉的 PyQt 库为自己写这样一个小程序.
过了几天之后, 就有了 VocVoc.

目标
----
* ✓ 检查输入的拼写错误.
* ✓ 利用文本文件 `文件名.txt` 生成对应的单词库, 并且将这个单词库存在 `VocVoc/pickles/` 文件夹下.
* ✓ 播放单词的读音(Google 的发音文件).
*   将 `VocVoc/corpuses` 文件夹下的文本文件自动生成单词库并且保存.
*   在特定网站上搜索某一个单词, 并且显示其上下文.

许可证
------

请看 [GNU 通用授权条款][GPLv3]


[master]:https://github.com/thedevil7/VocVoc/archive/master.zip
[Python]:http://www.python.org/
[Python3]:http://www.python.org/download/releases/3.3.0/
[Python3.3-win]:http://www.python.org/ftp/python/3.3.0/python-3.3.0.msi
[PyQt]:http://www.riverbankcomputing.com/software/pyqt/intro
[PyQt-Py3.3-x64-4.9.5]:http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.5/PyQt-Py3.3-x64-gpl-4.9.5-1.exe
[PyQt-Py3.3-x86-4.9.5]:http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.5/PyQt-Py3.3-x86-gpl-4.9.5-1.exe
[GPLv3]:http://www.gnu.org/licenses/gpl-3.0-standalone.html
