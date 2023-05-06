from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem

from QtImageViewer import QtImageViewer


class TreeItem(QTreeWidgetItem):
    def __init__(self, path=""):
        super().__init__()
        self.dir = QDir(path)
        self.setText(0, self.dir.dirName())


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.setFocus()
        self.ui.btnOpenFolder.clicked.connect(self.OpenFolder)  # type: ignore
        self.ui.treeWidget.itemClicked.connect(self.fileSelected)  # type: ignore

        ### --- ### --- ###
        self.viewer = QtImageViewer()
        self.ui.mid.addWidget(self.viewer)

    def addFolder(self, path):
        # Create QDir object
        dir = QDir(path)

        # Create root item
        item = TreeItem(path)

        # If the folder is empty, we return root item
        if dir.count() == 2:
            return item

        # We filter files then add those files to the root item
        fileList = dir.entryInfoList(QDir.Filter(QDir.Files))
        children = map(lambda file: TreeItem(file.absoluteFilePath()), fileList)
        item.addChildren(list(children))

        # We filter folders then add to the root item
        # We run addFolder recursively to find all the sub-folders
        folderList = dir.entryInfoList(QDir.Filter(QDir.AllDirs | QDir.NoDotAndDotDot))
        items = []
        for folder in folderList:
            items.append(self.addFolder(folder.absoluteFilePath()))

        item.addChildren(items)

        return item

    @QtCore.pyqtSlot(QTreeWidgetItem)
    def fileSelected(self, item):
        path = item.dir.absolutePath()
        print(path)
        self.viewer.open(path)

    @QtCore.pyqtSlot()
    def OpenFolder(self):
        # Open file dialog to get the path
        path = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            QDir.currentPath(),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        # Init tree
        treeWidget = self.ui.treeWidget
        treeWidget.setColumnCount(1)

        # Add path as an item to tree
        item = self.addFolder(path)
        treeWidget.insertTopLevelItem(0, item)  # type: ignore
