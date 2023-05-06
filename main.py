import sys
from PyQt5 import QtWidgets
from app import ApplicationWindow

if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    # app.showMaximized()
    app.show()
    app.activateWindow()
    app.raise_()
    sys.exit(qapp.exec_())
