#!/usr/bin/python
# coding: utf-8

from PyQt4.QtCore import Qt

from PyQt4.QtGui import QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QLabel, QLayout, \
    QSizePolicy, QFont, QPushButton
import sys

from widgets import MonthFullWidget



def main2():
    app = QApplication(sys.argv)
    calendar = MonthFullWidget()
    calendar.show()
    sys.exit(app.exec_())
        

def main():
    '''
    >>> main()
    '''
    app = QApplication(sys.argv)
    week = MonthWidget()
    wd = QWidget()

    button_left = QPushButton("<")
    button_left.setMaximumSize(20, 30)
    button_right = QPushButton(">")
    button_right.setMaximumSize(20, 30)

    font = QFont("Arial")
    font.setPointSize(18)
    font.setBold(True)
    month_title = QLabel('title')
    month_title.setFont(font)
    month_title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

    vlayout = QHBoxLayout()
    vlayout.addWidget(button_left)
    vlayout.addWidget(button_right)
    vlayout.addWidget(month_title, 0, Qt.AlignHCenter)

    
    layout = QHBoxLayout()
    layout.addWidget(week)

    grid_layout = QGridLayout()
    grid_layout.addLayout(vlayout, 0, 0)
    grid_layout.addLayout(layout, 30, 0)

    wd.setLayout(grid_layout)


    wd.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main2()
