'''
    GUI Module for ANF Feed Reader

The run() - Function is the main function.
It is also imported by the __init__ so
it can be used by the __main__ of the
package.

This package is licensed under:
 -- GNU General Public License v3.0 --

For more informations, reading the License,
contributing and else you may visit
the Github Repository:

 --> https://github.com/m1ghtfr3e/ANF-Feed-Reader
'''

import sys
import qdarkstyle
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QPushButton,
                             QWidget,
                             QListWidget,
                             QVBoxLayout,
                             QLabel,
                             QTextEdit,
                             QSplitter,
                             QMenuBar,
                             QMessageBox,
                             )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

try:
    from anffeed import ANFFeed
except ImportError:
    from ..anffeed import ANFFeed

from pathlib import Path
# Get the current directory to set the Icon later.
DIR = Path(__file__).parents[1]

LANGUAGE = 'german'


class ArticleWidget(QWidget):
    '''
        Article Widget

    This widget is holding a
    :class: QTextEdit
    as read-only, so there is
    no edit enabled for the User.
    '''
    def __init__(self, *args):
        super().__init__(*args)

        self.initUi()

    def initUi(self):
        '''
        Defines UI of the
        :class: ArticleWidget
        '''
        self.hbox = QVBoxLayout(self)
        self.setLayout(self.hbox)

        self.label = QLabel('Your chosen Feed will be shown here:')
        self.hbox.addWidget(self.label)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.hbox.addWidget(self.text)


class TitleWidget(QWidget):
    '''
        Title Widget

    This widget is presenting
    the Feed titles of the
    :class: ANFFeed ;
    It is also containing a
    :class: pyqtSignal
    on double click which will
    be responsible to present
    the linked feed in the
    :class: ArticleWidget
    '''
    TitleClicked = pyqtSignal([list])

    def __init__(self, *args):
        super().__init__(*args)

        self.initUi()

    def initUi(self):
        '''
        Defines UI of the
        :class: TitleWidget
        '''
        self.hbox = QVBoxLayout()
        self.setLayout(self.hbox)

        self.label = QLabel('Double Click on a title:')
        self.hbox.addWidget(self.label)

        self.titleList = QListWidget()
        self.titleList.itemDoubleClicked.connect(self.onClicked)

        self.newsFeed()

    def newsFeed(self, language=None):
        '''
            Set ANF Feeds
        :class: ANFFeed
        '''
        self.news = ANFFeed()
        if language:
            self.news.set_language(language)
        for item in self.news.all_feeds:
            self.titleList.addItem(item[0])
            self.titleList.addItem('')
        self.hbox.addWidget(self.titleList)

    def onClicked(self, item):
        '''
        This method will be called
        on double click on one of
        the titles.

        :param item: Item contained
            by the article clicked on
        :type item: PyQt Obj
        '''
        feeds = self.news.all_feeds
        id = 0
        for elem in range(len(feeds)):
            if feeds[elem][0] == item.text():
                id = elem

        summary = feeds[id][1] + '\n\n'
        link = feeds[id][2]
        detailed = feeds[id][3]

        self.TitleClicked.emit([summary, link, detailed])


class ANFApp(QMainWindow):
    ''' Main Window '''
    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowState(Qt.WindowMaximized)
        self.setWindowIcon(QIcon(f'{DIR}/assets/anf.png'))
        self.setAutoFillBackground(True)
        self.setWindowTitle('ANF RSS Reader')
        self.statusBar()

        self.anfInit()

        self.show()

    def anfInit(self):
        '''
        Defines UI of the
        :class: ANFApp
            (Main Window)

        Both, the Article
        and the Title Widget
        are organized inside
        :class: QSplitter
        Moreover there is:
        :class: QMenuBar
        :class: QPushButton
            (Exit Button)
        '''
        self.central_widget = QSplitter()

        self.title_widget = TitleWidget()
        self.article_widget = ArticleWidget()

        self.setCentralWidget(self.central_widget)

        self.menu_bar = QMenuBar()
        self.actionEdit = self.menu_bar.addMenu('Edit')
        self.actionEdit.addAction('Size +')
        self.actionEdit.addAction('Size -')
        self.actionEdit.addSeparator()
        self.actionEdit.addAction('Settings')
        self.actionDownload = self.menu_bar.addMenu('Download')
        self.actionHelp = self.menu_bar.addMenu('Help')
        self.actionLang = self.menu_bar.addMenu('Language')
        self.actionLang.addAction('german')
        self.actionLang.addAction('english')
        self.actionLang.addAction('kurmanjî')
        self.actionLang.addAction('spanish')
        self.actionLang.addAction('arab')
        self.actionLang.hovered.connect(self.languageAction)
        self.central_widget.addWidget(self.menu_bar)

        self.central_widget.addWidget(self.title_widget)
        self.central_widget.addWidget(self.article_widget)

        self.exitBtn = QPushButton(self)
        self.exitBtn.setGeometry(50, 600, 100, 55)
        self.exitBtn.setText('Exit')
        self.exitBtn.setStyleSheet("background-color: red")
        self.exitBtn.setStatusTip('Exit the Application')
        self.exitBtn.clicked.connect(self.exit)

        # Catch Slot Signal from the TitleWidget
        self.title_widget.TitleClicked.connect(self.title_click)

        self.show()

    def languageAction(self, lang):
        '''
            Change Language
        Changing the Language
        of the Feeds if Menu
        Option is hovered.

        :param lang: The Language
            Text given by Menu Option
        :type lang: PyQt obj
        '''
        self.title_widget.titleList.clear()
        self.title_widget.newsFeed(lang.text())
        self.title_widget.update()

    def title_click(self, feed):
        '''
            Signal Catcher
        Catches the Slot Signal
        of the
        :class: TitleWidget
        and sets the Text for the
        :class: ArticleWidget;

        :param feed: The Signal
            in the TitleWidget
            emits a list with
            the contents;
        type feed: list
        '''
        # Title = feed[0]
        # Link = feed[1]
        # Detailed = feed[2]

        # Set Title with Italic Font.
        self.article_widget.text.setFontItalic(True)
        self.article_widget.text.setText(feed[0])
        self.article_widget.text.setFontItalic(False)
        # Underline & Append Link.
        self.article_widget.text.setFontUnderline(True)
        self.article_widget.text.append(feed[1])
        self.article_widget.text.setFontUnderline(False)
        # Append Detailed
        self.article_widget.text.append('\n\n')
        self.article_widget.text.append(feed[2])

    def exit(self):
        ''' Exit the Application '''
        self.close()


def run():
    '''
        Run the App
    '''
    app = QApplication(sys.argv)
    app.setStyle('breeze')
    #app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = ANFApp()
    sys.exit(app.exec_())



if __name__ == '__main__':
    run()
