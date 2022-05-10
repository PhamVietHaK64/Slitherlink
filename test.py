from slitherlink import solve
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30

outputFile = 'output/output.txt'




class MyApp(QtWidgets.QMainWindow):
    __maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    __size = 0
    __map = 0
    __slitherlink_size = 0

    def __init__(self):
        super(MyApp, self).__init__()
        """uic.loadUi('ui.ui', self)
        self.setWindowTitle("Slitherlink")
        self.create_combobox(0)
        self.create_map(0)
        self.input_size.currentIndexChanged.connect(self.create_combobox)
        self.input_map.currentIndexChanged.connect(self.create_map)
        self.solveButton.clicked.connect(self.solver)
        """

        #đây là đoạn test Qpainter nếu ko chạy đoạn ẩn bên trên thì đc 
        #nhưng chạy cả bên trên thì cái trên nó che mất 
        self.repaint()
        self.show()

    def create_combobox(self, index):
        self.__size = index
        self.input_map.clear()
        length = len(self.__maps[self.__size])
        for i in range(length):
            self.input_map.addItem(str(i + 1))
    def create_map(self, index):
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
        self.setStyleSheet("background-color: #C6E2FF")
        for i in range(size):
            for j in range(size):
                item = self.__maps[self.__size][self.__map][i][j]
                item = str(item)
                item = QtWidgets.QTableWidgetItem(item)
                self.map.setItem(i, j, item)
                self.map.item(i, j).setTextAlignment(Qt.AlignCenter)
                if item.text():
                    self.map.item(i, j).setBackground(Qt.white)
    
    def solver(self):
        run_all_test()
        result = solve(self.__maps[self.__size][self.__map])
        self.clause.setText("Clause: " + str(result['clauses']))
        self.variable.setText('Variable: ' + str(result['variables']))
        self.time.setText("Time: %.5f s" % (result['time']))


        self.repaint()
        
        
     
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.red)
        qp.drawRect(0, 0, 30, 30)
        qp.end()

def read_result(result, file):
    sol = result["result"]
    time = result['time']
    variables = result['variables']
    clauses = result['clauses']
    from slitherlink import m, n, puzzle
    file.write(f'{m} x {n}\n')
    if type(sol) is str:
        file.write(f'Result: {sol}\nTime: %.3f ms\nVariables: {variables}\n' % time)
        file.write(f'Clauses: {clauses}\n\n')
        return
    reload = result['reload']
    file.write("Result:\n")
    for i in range(m + 1):
        for j in range(n + 1):
            if j == m:
                file.write("*")
            else:
                line = i * n + j + 1
                if sol[line - 1] > 0:
                    file.write("*---")
                else:
                    file.write("*   ")
        file.write("\n")
        if i < m:
            for j in range(m + 1):
                line = (m + 1) * n + j * m + i + 1
                if sol[line - 1] > 0:
                    file.write("|")
                else:
                    file.write(" ")
                if j <= n - 1 and i <= m - 1:
                    if puzzle[i][j] > -1:
                        file.write(f' {puzzle[i][j]} ')
                    else:
                        file.write('   ')
            file.write("\n")
    file.write(f'Time: %.3f ms\nVariables: {variables}\n' % time)
    file.write(f'Clauses: {clauses}\nReload: {reload}\n\n')


def run_all_test():
    # maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    maps = [maps5, maps7, maps10]
    file = open(outputFile, 'w')
    for mapi in maps:
        for m in mapi:
            read_result(solve(m), file)
    file.close()

app = QApplication(sys.argv)
UIWindow = MyApp()
#run_all_test()
sys.exit(app.exec_())

