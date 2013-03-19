#!/usr/bin/python
# coding: utf-8

from PyQt4.QtCore import Qt, QPointF, QPoint, QSize, QString, QIODevice, QByteArray, \
    QDataStream, QMimeData, QVariant, pyqtSlot, QObject, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QColor, QPainter, QCursor, QApplication, QDialog, QHBoxLayout, \
    QWidget, QProgressBar, QDrag, QPixmap, QFrame, QLineEdit, QSizePolicy, QMainWindow, \
    QFont, QPushButton, QLabel, QGridLayout, QMessageBox

import datetime
import time
from dateutil import relativedelta

from info import MonthStruct, MonthInfo, Var

class MonthFullWidget(QWidget):
    def __init__(self, parent=None, date=None):
        if date: self.date = date
        else: self.date = datetime.date.today()

        super(MonthFullWidget, self).__init__(parent)

        self.button_left = None
        self.button_right = None
        self.month_title = None
        self.month_widget = None
        self.title_layout = self._month_title_layout()
        self.cal_layout = self._month_cal_layout()
        
        
        grid_layout = QGridLayout()
        grid_layout.addLayout(self.title_layout, 0, 0)
        grid_layout.addLayout(self.cal_layout, 30, 0)

        self.setLayout(grid_layout)
        self._connections()


    def _connections(self):
        self.button_left.clicked.connect(self.previous)
        self.button_right.clicked.connect(self.next)


    def next(self):
        onemonth = relativedelta.relativedelta(months=1)
        self.date += onemonth
        timestamp = time.mktime(self.date.timetuple())
        self.month_title.setText(self.date2string(self.date))
        self.month_widget.changed.emit(timestamp)

    def previous(self):
        onemonth = relativedelta.relativedelta(months=1)
        self.date -= onemonth
        timestamp = time.mktime(self.date.timetuple())
        self.month_title.setText(self.date2string(self.date))
        self.month_widget.changed.emit(timestamp)
        

    def date2string(self, date):
        return self.date.strftime("%B %Y")

    def _month_title_widget(self):
        font = QFont("Arial")
        font.setPointSize(18)
        font.setBold(True)

        title = self.date2string(self.date)
        self.month_title = QLabel(title)
        self.month_title.setFont(font)
        self.month_title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        return self.month_title


    def _month_title_layout(self):
        self.button_left = QPushButton("<")
        self.button_left.setMaximumSize(20, 30)
        self.button_right = QPushButton(">")
        self.button_right.setMaximumSize(20, 30)
        
        layout = QHBoxLayout()
        layout.addWidget(self.button_left)
        layout.addWidget(self.button_right)
        layout.addWidget(self._month_title_widget(), 0, Qt.AlignHCenter)
        return layout
        
    def _month_cal_layout(self):
        self.month_widget = MonthWidget(self, date=self.date)
        layout = QHBoxLayout()
        layout.addWidget(self.month_widget)
        return layout


class MonthWidget(QWidget):

    changed = pyqtSignal(float)

    def __init__(self, parent=None, date=None):
        self.parent = parent
        super(MonthWidget, self).__init__(self.parent)
        self.setFocusPolicy(Qt.WheelFocus)
        #self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,
        #                               QSizePolicy.Fixed))

        self.date = date
        self.back = True
        self.select_args = []
        self.installEventFilter(self)
        self.month_struct = MonthStruct()
        self.month_info = None

        self.changed.connect(self.on_month_changed)

    def minimumSizeHint(self):
        # font = QFont(self.font())
        # font.setPointSize(font.pointSize() -1)
        # fm = QFontMetricsF(font)
        # return QSize(fm.width(Mitem.WSTRING) * \
        #                  10.0,
        #              (fm.height() * 4) + 12.0)

        return QSize(700,700)

    def on_month_changed(self, timestamp):
        self.date = datetime.datetime.fromtimestamp(timestamp)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            cell_identifier = self.currentCell(self.month_struct.cell_width, self.month_struct.cell_height)
            self.month_struct.select_start = cell_identifier
            self.update()

    def mouseMoveEvent(self, event):
        cell_identifier = self.currentCell(self.month_struct.cell_width, self.month_struct.cell_height)
        self.month_struct.select_end = cell_identifier
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            #self.back = not self.back
            self.back = False
            self.month_struct.select_start = None
            self.month_struct.select_end = None
            self.update()

    def getYear(self):
        try:
            return self.date.year
        except:
            self.date = datetime.date.today()
            return self.date.year

    def getMonth(self):
        try:
            return self.date.month
        except:
            self.date = datetime.date.today()
            return self.date.month

    def paintEvent(self, event=None):
        self._drawMonthFrame()

    def initMonthInfo(self):

        ori_rect = self.rect()
        width = ori_rect.width()
        height = ori_rect.height()

        self.month_info = MonthInfo(width, height, self.getYear(), self.getMonth())

    def _drawMonthFrame(self):
        self.initMonthInfo()
        wi = self.month_info
        painter = QPainter(self)

        pen = painter.pen()
        pen.setWidth(Var.line_width)
        painter.setPen(pen)

        for coord in wi.paint_base_lines:
            painter.drawLine(*coord)

        # Draw selections
        for selection in wi.selections():
            painter.fillRect(*selection)


        # Draw dates
        font = painter.font()
        font.setPointSize(wi.cell_height/8)
        painter.setFont(font)

        for cell_id in range(42):
            x, y = wi.getCoordinate(cell_id)
            x += wi.cell_width * 74/100
            y += wi.cell_height/7
            
            day = wi.getDay(cell_id)

            painter.drawText(QPointF(x, y), QString(str(day)))

    def currentCell(self, cell_width, cell_height):
        cursor = self.mapFromGlobal(QCursor.pos())
        cursor_x = cursor.x()
        cursor_y = cursor.y()
        
        select_column = int((cursor_x)/cell_width)
        select_row = int((cursor_y)/cell_height)
        return (select_row, select_column)

    def log(self, msg):
        fd = file('log.log', 'w')
        fd.write(str(msg))
        fd.close()


class BarWidget(QProgressBar):
    def __init__(self, parent= None):
        super(BarWidget, self).__init__(parent)


class DLineEdit(QLineEdit):
    
    def __init__(self, parent=None):
        super(DLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-fridgemagnet"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-fridgemagnet"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-fridgemagnet"):
            data = event.mimeData().data("application/x-fridgemagnet")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            stream >> text
            self.setText(text)
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

class DWidget(QWidget):
    def __init__(self, parent=None):
        super(DWidget, self).__init__(parent)
        bar = BarWidget(self)
        bar.setValue(30)
        bar.move(QPoint(100, 200))
        bar.show()

        bar2 = BarWidget(self)
        bar2.setValue(80)
        bar2.move(QPoint(90, 190))
        bar2.show()

        self.setAcceptDrops(True)


    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.startDrag(event)

    def startDrag(self, event):
        child = self.childAt(event.pos())
        if not child:
            return
        pos_in_child = event.pos() - child.pos()
        
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << QVariant(child.value()) << QPoint(pos_in_child)
        
        mime = QMimeData()
        mime.setData("application/x-fridgemagnet", data)
        
        drag = QDrag(child)
        drag.setMimeData(mime)
        drag.setPixmap(QPixmap.grabWidget(child))
        drag.setHotSpot(pos_in_child)
        
        child.hide()
        
        if (drag.start(Qt.MoveAction or Qt.CopyAction) == Qt.MoveAction):
            child.close()
        else:
            child.show()
            

    def mouseMoveEvent(self, event):
        self.startDrag(event)
        QWidget.mouseMoveEvent(self, event)


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-fridgemagnet"):
            event.setDropAction(Qt.CopyAction)
            #event.acceptProposedAction()
            event.accept()
        else:
            event.ignore()

    # def dropMoveEvent(self, event):
    #     if event.mimeData().hasFormat("application/x-fridgemagnet"):
    #         event.setDropAction(Qt.MoveAction)
    #         event.accept()
    #     else:
    #         event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-fridgemagnet"):
            data = event.mimeData().data("application/x-fridgemagnet")
            stream = QDataStream(data, QIODevice.ReadOnly)
            position = QPoint()
            percent_value = QVariant()

            bar = BarWidget(self)
            bar.setValue(20)
            bar.move(QPoint(30, 30))
            bar.show()
            

            event.setDropAction(Qt.MoveAction)
            event.accept()
