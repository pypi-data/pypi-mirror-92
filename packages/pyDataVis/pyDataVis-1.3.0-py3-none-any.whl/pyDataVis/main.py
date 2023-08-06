import sys
from PyQt5 import QtWidgets
from pyDataVis.pyDataVis import MainWindow


def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("pyDataVis")
    app.setOrganizationName("Pierre Alphonse")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

