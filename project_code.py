# -*- coding: utf-8 -*-

import threading
import sys
import pygame
import time
import random

from another import TIMINGS, NAMES, FONT_COLORS, ALL_TEXT

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic, QtCore

NUM = random.randint(0, len(ALL_TEXT)) % len(ALL_TEXT)
IMAGE_NUM = random.randint(0, len(FONT_COLORS)) % len(FONT_COLORS)
SONG_NAME = NAMES[NUM]
text = ALL_TEXT[NUM]
Timer = True


# parallel checking input of user without intervention in working of program
class TimerChange:
    # checking timer function
    def timer(timing, widget):
        while Timer:
            time.sleep(0.001)

            if time.time() - timing > TIMINGS[NUM][window.index]:
                window.index = (window.index + 1) % len(TIMINGS[NUM])
                window.update_text()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # program design
        self.uic = uic.loadUi('Project.ui', self)

        # conntect with cycle of functions which take part in parallel-checking
        self.text_line.textChanged.connect(self.solve_changes)

        # background image (chosen by random)
        s = "#MainWindow { border-image: url(images/"
        t = ") 0 0 0 0 stretch stretch; }"
        self.uic.setStyleSheet(s + str(IMAGE_NUM) + t)

        # background image (chosen by random but simultaneously)
        self.cur_color = FONT_COLORS[IMAGE_NUM]
        self.uic.label.setStyleSheet("color:" + self.cur_color + ";")
        self.uic.melodyList.setStyleSheet("color:" + self.cur_color + ";")

        # print name of a playing song
        self.uic.melodyList.setText(SONG_NAME.rstrip('.mp3'))

        self.index = 0
        self.score = 0

        # current time
        self.t = time.time()

        # music playing (SONG_NAME is a file going to play)
        pygame.mixer.music.load("music\\" + SONG_NAME)
        pygame.mixer.music.play()

    def solve_changes(self):
        tindex = 0
        for i in self.text_line.text():
            if i != text[self.index][tindex]:
                self.text_line.setText(self.text_line.text()[:-1])

            tindex = (tindex + 1) % len(text[self.index])

    def update_text(self):
        self.score += len(self.text_line.text())

        if self.index < len(text):
            self.label.setText(text[self.index])
            self.text_line.setText('')

        else:
            self.label.setText('your score is ' + str(self.score))
            self.text_line.setText('')

            while(1):
                pass


if __name__ == '__main__':
    pygame.mixer.init()
    app = QApplication(sys.argv)
    window = MyWidget()

    t = threading.Thread(target=TimerChange.timer, args=[time.time(), window])
    t.start()

    window.show()
    sys.exit(app.exec_())

    Timer = False
    t.join()
