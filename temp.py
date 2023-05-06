model = QFileSystemModel()
model.setRootPath(QDir.currentPath())
tree = QTreeView()

tree.setModel(model)
