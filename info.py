from PyQt4.QtCore import Qt, QPointF
from PyQt4.QtGui import QColor
import numpy
import calendar
import datetime

class Var:
    ROW = 6
    COLUMN = 7
    line_color = Qt.blue
    line_width = 2
    background_color = QColor(233, 234, 214)
    cell_select_color = QColor(219,244, 246)
    calendar_min_width = 700
    calendar_min_height = 700


def dlog(msg):
    fd = file('log.log', 'w')
    fd.write(str(msg))
    fd.close()

class Calendar(calendar.Calendar):
    '''
    

    >>> cal = Calendar()
    >>> cal.monthdays2calendar2(2013, 2)
    [[(28, 0), (29, 1), (30, 2), (31, 3), (1, 4), (2, 5), (3, 6)], [(4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6)], [(11, 0), (12, 1), (13, 2), (14, 3), (15, 4), (16, 5), (17, 6)], [(18, 0), (19, 1), (20, 2), (21, 3), (22, 4), (23, 5), (24, 6)], [(25, 0), (26, 1), (27, 2), (28, 3), (1, 4), (2, 5), (3, 6)], [(4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6)]]

    >>> cal.monthdays2calendar3(2013, 2)
    [[(28, 0), (29, 1), (30, 2), (31, 3), (1, 4), (2, 5), (3, 6)], [(4, 7), (5, 8), (6, 9), (7, 10), (8, 11), (9, 12), (10, 13)], [(11, 14), (12, 15), (13, 16), (14, 17), (15, 18), (16, 19), (17, 20)], [(18, 21), (19, 22), (20, 23), (21, 24), (22, 25), (23, 26), (24, 27)], [(25, 28), (26, 29), (27, 30), (28, 31), (1, 32), (2, 33), (3, 34)], [(4, 35), (5, 36), (6, 37), (7, 38), (8, 39), (9, 40), (10, 41)]]
    '''

    def itermonthdates2(self, year, month):
        date = datetime.date(year, month, 1)
        days = (date.weekday() - self.firstweekday) % 7
        date -= datetime.timedelta(days=days)
        oneday = datetime.timedelta(days=1)
        for a in range(42):
            yield date
            date += oneday

    def itermonthdays3(self, year, month):
        for date in self.itermonthdates2(year, month):
            yield (date.day, date.weekday())

    def itermonthdays4(self, year, month):
        count = 0
        for date in self.itermonthdates2(year, month):
            yield (date.day, count)
            count += 1

    def monthdays2calendar2(self, year, month):
        days = list(self.itermonthdays3(year, month))
        return [ days[i:i+7] for i in range(0, len(days), 7) ]

    def monthdays2calendar3(self, year, month):
        days = list(self.itermonthdays4(year, month))
        return [ days[i:i+7] for i in range(0, len(days), 7) ]



class MonthStruct(object):
    __info = {"width"	: None,
              "height"	: None,
              "cell_width" : None,
              "cell_height" : None,
              "row"	: Var.ROW,    # height cell count
              "column"	: Var.COLUMN, # width cell count
              "most_x"	: None,
              "most_y"	: None,
              "year"	: None,
              "month"	: None,

              "select_start"	: None,
              "select_end"	: None,

              "base_array"		: None,
              "calendar_array"		: None,
              "base_coordinates"	: None,
              "paint_base_lines"	: None,
              "today"			: None
              }
    
    def __init__(self):
        self.__dict__ = self.__info

class MonthInfo(MonthStruct):
    '''

    >>> wi = MonthInfo(700, 700, 2013, 2)
    >>> wi.base_array
    array([[ 0,  1,  2,  3,  4,  5,  6],
           [ 7,  8,  9, 10, 11, 12, 13],
           [14, 15, 16, 17, 18, 19, 20],
           [21, 22, 23, 24, 25, 26, 27],
           [28, 29, 30, 31, 32, 33, 34],
           [35, 36, 37, 38, 39, 40, 41]])

    >>> wi.base_coordinates #doctest: +SKIP

    >>> wi.cellWidth()
    97.71428571428571
    >>> wi.cellHeight()
    114.33333333333333

    >>> wi.mostYCoordinate()
    (0.0, 698.0)
    >>> wi.mostXCoordinate()
    (697.99999999999989, 0.0)
    >>> wi.most_x #doctest: +SKIP
    >>> wi.most_y #doctest: +SKIP

    >>> import random
    >>> cid = random.randint(0, wi.column*wi.row)
    >>> coordinate = wi.cellIdentifier(cid)
    >>> r_cid = wi.cellId(coordinate)
    >>> assert cid == r_cid

    >>> assert wi.cellCoordinate((4, 1)) == wi.cellCoordinate(29)
    >>> wi.paint_baseLines() #doctest: +SKIP

    >>> wi.select_start = (1, 1)
    >>> wi.select_end = None
    >>> wi.selections()	#doctest: +SKIP

    ### === Calendar for month
    ### __________________________________________________________
    >>> calmon = MonthInfo(700, 700, 2013, 2)
    >>> calmon.calendar_array
    [[(28, 0), (29, 1), (30, 2), (31, 3), (1, 4), (2, 5), (3, 6)], [(4, 7), (5, 8), (6, 9), (7, 10), (8, 11), (9, 12), (10, 13)], [(11, 14), (12, 15), (13, 16), (14, 17), (15, 18), (16, 19), (17, 20)], [(18, 21), (19, 22), (20, 23), (21, 24), (22, 25), (23, 26), (24, 27)], [(25, 28), (26, 29), (27, 30), (28, 31), (1, 32), (2, 33), (3, 34)], [(4, 35), (5, 36), (6, 37), (7, 38), (8, 39), (9, 40), (10, 41)]]


    ### === Get coordinate and day from the cell id
    >>> calmon.getCoordinate(15)
    (99.71428571428571, 232.66666666666666)

    >>> calmon.getDay(15)
    12

    >>> calmon.getDay(30)
    27
    

    '''

    def __init__(self, width, height, year, month):
        super(MonthInfo, self).__init__()

        if not self.year == year or not self.month == month:
            self.update_calendar(year, month)

        if not self.width == width or not self.height == height:
            self.update_geometre(width, height)

    def update_geometre(self, width, height):
        self.width = width
        self.height = height
        self.cell_width = self.cellWidth()
        self.cell_height = self.cellHeight()
        self.base_array = numpy.arange(self.row * self.column).reshape(self.row, self.column)
        self.paint_base_lines = self.paint_baseLines()
        self.base_coordinates = self.baseCoordinates()

        self.most_x = self.mostXCoordinate()[0]
        self.most_y = self.mostYCoordinate()[1]

    def update_calendar(self, year, month):
        self.year = year
        self.month = month
        cal = Calendar()
        self.calendar_array = cal.monthdays2calendar3(year, month)
        
    def columns(self):
        '''
        To draw we need two point start_pointer and end_pointer. The
        method will return the list of pair of the coordinate.
        '''
        result = []
        cell_width = float(self.width)/float(self.column)
        for a in range(self.column + 1):
            start_pointer = QPointF(a * cell_width, 0)
            end_pointer = QPointF(a * cell_width, self.height)
            result.append((start_pointer, end_pointer))
        return result

    def rows(self):
        result = []
        cell_height = float(self.height)/float(self.row)
        for a in range(self.row + 1):
            start_pointer = QPointF(0 , a * cell_height)
            end_pointer = QPointF(self.width , a * cell_height)
            result.append((start_pointer, end_pointer))
        return result

    def baseCoordinates(self):
        result = []
        for cid in range(self.row * self.column):
            result.append(self.cellCoordinate(cid))
        return result

    def base(self):
        result_row = []
        result_column = []
        max_id = self.column * self.row
        left = range(0, max_id, self.column)
        right = range(self.column - 1, max_id, self.column)
        top = range(self.column)
        bottom = range(max_id - self.column, max_id)

        for row in range(self.row):
            result_row.append((left[row], right[row]))

        for column in range(self.column):
            result_column.append((top[column], bottom[column]))
        return (result_row, result_column)

    # TODO: Consider to draw directly for performence. Modify self.columns
    # and self.rows. self.rows is example.
    def paint_baseLines(self):
        result = []
        base_row, base_column = self.base()
        # left to right pairs
        for startp, endp in base_row:
            result.append((QPointF(*self.cellCoordinate(startp)), QPointF(*self.cellCoordinate(endp, 'x'))))
        # top to bottom pairs
        for startp, endp in base_column:
            result.append((QPointF(*self.cellCoordinate(startp)), QPointF(*self.cellCoordinate(endp, 'y'))))

        most_x = self.width - Var.line_width
        most_y = self.height - Var.line_width
        result.append((QPointF(*(most_x, 0)), QPointF(*(most_x, most_y))))
        result.append((QPointF(*(0, most_y)), QPointF(*(most_x, most_y))))
        return result

    def mostYCoordinate(self):
        cell_id = self.base_array[self.row - 1, 0]
        x, y = self.cellCoordinate(cell_id)
        y += Var.line_width + self.cell_height
        return (x, y)

    def mostXCoordinate(self):
        cell_id = self.base_array[0, self.column - 1]
        x, y = self.cellCoordinate(cell_id)
        x += Var.line_width + self.cell_width
        return (x, y)

    def selections(self):
        result = []
        if not self.select_start: return result
        if not self.select_end: self.select_end = self.select_start
        if isinstance(self.select_start, tuple):
            start = self.cellId(self.select_start)
        else: start = self.select_start
        if isinstance(self.select_end, tuple):
            end = self.cellId(self.select_end)
        else: end = self.select_end
        if not end: end = start

        cids = range(start, end + 1)
        coordinates = [self.cellCoordinate(a) for a in cids]
        dlog(coordinates)
        for x, y in coordinates:
            x += Var.line_width
            y += Var.line_width
            result.append((x, y, self.cell_width, self.cell_height, Var.cell_select_color))
        return result
            

    def selection_range(self, start, end):
        if start == None: return None
        if end == None: return start

        x1, y1 = start
        x2, y2 = end

        result = []
        if x1 == x2:
            for a in range(y2 - y1):
                result.append((x1, y1 + a))
        return result

    def cellWidth(self):
        column_line_count = self.column + 1
        all_cell_width = self.width - (column_line_count * Var.line_width)
        return float(all_cell_width)/float(self.column)

    def cellHeight(self):
        row_line_count = self.row + 1
        all_cell_height = self.height - (row_line_count * Var.line_width)
        return float(all_cell_height)/float(self.row)

    def cellIdentifier(self, num):
        '''
        Returns the identifier of cell from the id number of cell. the
        identifier of cell is the pair of column and row
        '''
        # j = (num - num%self.column)/self.column
        # i = (num%self.column)
        # where 0 =< i < self.column, 0 =< j < self.row
        # (j, i) --> (row, column)
        return divmod(num, self.column)

    def cellId(self, cell_identifier):
        '''
        Return the id number of cell from the coordinate of cell.
        '''
        j, i = cell_identifier
        return j * self.column + i
        
    def cellCoordinate(self, *args):
        '''
        Returns the x-y coordinate of cell. The cell contains the line.
        The argument can be int or tuple. The int is the id of cell. The
        tuple is the identifier of cell.

        The second argument can be 'x', 'y', 'xy'. We can obtaine the
        coordinate (x, 0), (0, y), (x, y) in the cell.
        '''
        arg = args[0]
        try:
            edge = args[1]          # 'x', 'y', 'xy'
            if edge == 'x': ei, ej = 1, 0
            elif edge == 'y': ei, ej = 0, 1
            elif edge == 'xy': ei, ej = 1, 1
            else: raise AttributeError('x, y, xy is required.')
        except IndexError:
            ei, ej = 0, 0

        if isinstance(arg, int): arg = self.cellIdentifier(arg)
        # (j, i) --> (row, column)
        j, i = arg
        y = (j + ej) * (Var.line_width + self.cell_height)
        x = (i + ei) * (Var.line_width + self.cell_width)
        return (x, y)

    def getCoordinate(self, cell_id):
        return self.base_coordinates[cell_id]

    def getDay(self, cell_id):
        week, the_day = divmod(cell_id, 7)
        return self.calendar_array[week][the_day][0]

class TaskStruct(object):
    pass
