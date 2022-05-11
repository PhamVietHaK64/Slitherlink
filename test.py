from slitherlink import solve
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30




class MyApp(QtWidgets.QMainWindow):
    __maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    __size = 0
    __map = 0
    __slitherlink_size = 0

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('ui.ui', self)
        self.flag = False
        self.setWindowTitle("Slitherlink")
        self.create_map(0)
        self.create_combobox(0)
        self.show()
        
        self.input_size.currentIndexChanged.connect(self.create_combobox)
        self.input_map.currentIndexChanged.connect(self.create_map)
        self.solveButton.clicked.connect(self.solver)
        

    def create_combobox(self, index):
        self.flag = False
        self.__size = index
        self.input_map.clear()
        length = len(self.__maps[self.__size])
        for i in range(length):
            self.input_map.addItem(str(i + 1))

    def create_map(self, index):
        self.flag = False
        h = self.height()
        self.__map = index
        size = len(self.__maps[self.__size][self.__map])
        
        self.__slitherlink_size = size
        self.map.setRowCount(size)
        self.map.setColumnCount(size)
        self.map.resize(size*20, size*20)
        self.map.setGeometry(0, 0, 20* (size + 1), 20 * (size + 1))
        self.map.resizeColumnsToContents()
        self.map.verticalHeader().setVisible(False)
        self.map.horizontalHeader().setVisible(False)
        for i in range(size):
            for j in range(size):
                item = self.__maps[self.__size][self.__map][i][j]
                item = str(item)
                item = QtWidgets.QTableWidgetItem(item)
                self.map.setItem(i, j, item)
                self.map.item(i, j).setTextAlignment(Qt.AlignCenter)
                
        self.map.setStyleSheet("QTableWidget {background-color: transparent; padding: 10px}")

    def solver(self):
        self.flag = True
        self.update()
        result = solve(self.__maps[self.__size][self.__map])
        self.clause.setText("Clause: " + str(result['clauses']))
        self.variable.setText('Variable: ' + str(result['variables']))
        self.time.setText("Time: %.5f s" % (result['time']))


    def paintEvent(self, event):
        if self.flag:
            from slitherlink import m, n, puzzle
            result = solve(self.__maps[self.__size][self.__map])
            sol = result['result']
            qp = QPainter()
            qp.begin(self)
            pen = QPen()
            pen.setWidth(1)
            
            qp.setPen(pen)
            
            size = len(self.__maps[self.__size][self.__map])
            qp.setPen(Qt.black)
            for i in range(m + 1):
                for j in range(n + 1):
                    #vẽ điểm
                    pen.setWidth(3)
                    qp.setPen(pen)
                    qp.drawPoint(20 + i*20, 20 + j*20)
                    if j != m:
                        line = i * n + j + 1
                        if sol[line - 1] > 0:
                            #vẽ cạnh ngang
                            pen.setWidth(1)
                            qp.setPen(pen)
                            qp.drawLine(20 + (line//size)*20, 20 + (line%size)*20, 40 + (line//size)*20, 20 + (line%size)*20)
                      
                       
                if i < m:
                    for j in range(m + 1):
                        line = (m + 1) * n + j * m + i + 1
                        if sol[line - 1] > 0:
                            #vẽ cạnh dọc
                            pen.setWidth(1)
                            qp.setPen(pen)
                            qp.drawLine(20 + (line//size)*20, 20 + (line%size)*20, 20 + (line//size)*20, 40 + (line%size)*20)
            
            qp.end()
            


app = QApplication(sys.argv)
UIWindow = MyApp()
#run_all_test()
sys.exit(app.exec_())

