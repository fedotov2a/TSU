# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QSpinBox, QMenuBar, QMenu, QAction, QPushButton, QStatusBar
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor, QMouseEvent
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic

class GUI(QMainWindow):
    '''
    Графический интерфейс для VideoAnalyzer
    '''
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        
        self.move(70, 70)
        self.setFixedSize(1200, 680)

        self.COUNT_POINTS = 16
        self.curr_count_points = 0
        self.canvas_lbl.mousePressEvent = self.get_pos

        self.painter = QPainter(self)
        self.pen = QPen(Qt.red, 3)
        self.painter.setPen(self.pen)
        self.pixmap = QPixmap('scan1_r.jpg')
        self.canvas_lbl.setPixmap(self.pixmap)
        self.painter.drawPixmap(self.canvas_lbl.rect(), self.pixmap)


    def get_pos(self, event):
        self.curr_count_points += 1
        if self.curr_count_points <= self.COUNT_POINTS:
            print(event.pos().x())
            print(event.pos().y())
            
            self.painter.begin(self)
            pen = QPen(Qt.red, 3)
            self.painter.setPen(pen)
            self.painter.drawPoint(event.pos().x(), event.pos().y())
            self.painter.end()
            self.update()

app = QApplication(sys.argv)
gui = GUI()
gui.show()
sys.exit(app.exec_())
