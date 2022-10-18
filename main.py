from PyQt5 import QtWidgets
from ui import ManagerWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mw = ManagerWindow()
    mw.show()
    app.exec()
