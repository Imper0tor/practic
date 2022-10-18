from PyQt5 import QtWidgets, QtCore, QtGui
from file_methods import *
import time


class ManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ManagerWindow, self).__init__()
        self.setFixedSize(1024, 720)
        self.setWindowTitle('Файловый Менеджер')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.dir_view_widget = QTreeViewWithContextMenu()
        self.dir_view_widget.setModel(QDirModelWithSortingFlag())
        self.setCentralWidget(self.dir_view_widget)


class QTreeViewWithContextMenu(QtWidgets.QTreeView):
    def __init__(self):
        super().__init__()
        self.folders_to_copy = []
        self.files_to_copy = []
        self.cut_flag = False
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)

    def openContextMenu(self, position):
        folders, files = self.selectedFoldersAndFiles()
        menu = QtWidgets.QMenu()
        copy_action = menu.addAction('Копировать')
        cut_action = menu.addAction('Вырезать')
        if self.folders_to_copy != [] or self.files_to_copy != []:
            paste_action = menu.addAction('Вставить')
        else:
            paste_action = ''
        if len(folders) + len(files) == 1:
            rename_action = menu.addAction('Переименовать')
        else:
            rename_action = ''
        create_folder_action = menu.addAction('Создать Папку')
        delete_action = menu.addAction('Удалить')

        user_action = menu.exec_(self.sender().mapToGlobal(position))
        if user_action == delete_action:
            delete(folders, files)
        elif user_action == create_folder_action:
            try:
                folder_name, ok = QtWidgets.QInputDialog().getText(self, 'Создать папку', 'Введите имя папки:',
                                                                   text='Новая папка')
                path = folders[0]
                create_folder(f'{path}/{folder_name}')
            except Exception:
                dialog = QtWidgets.QMessageBox()
                dialog.critical(self, 'Ошибка!', 'Папка с заданным именем уже существует')

        elif user_action == copy_action:
            self.folders_to_copy = folders[:]
            self.files_to_copy = files[:]
            self.cut_flag = False
        elif user_action == cut_action:
            self.folders_to_copy = folders[:]
            self.files_to_copy = files[:]
            self.cut_flag = True
        elif user_action == paste_action:
            size = len(self.folders_to_copy) + len(self.files_to_copy)
            progress = QtWidgets.QProgressDialog('Пожалуйста, подождите', None, 0, size, self)
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setWindowTitle('Перемещение файлов')
            progress.setFixedSize(500, 200)
            progress.show()
            progress.setValue(size)
            try:
                if self.cut_flag:
                    cut_paste(self.folders_to_copy, self.files_to_copy, folders[0])
                else:
                    copy_paste(self.folders_to_copy, self.files_to_copy, folders[0])
            except Exception:
                if self.cut_flag:
                    cut_paste(self.folders_to_copy, self.files_to_copy, folders[0]+'(1)')
                else:
                    copy_paste(self.folders_to_copy, self.files_to_copy, folders[0]+'(1)')
            self.folders_to_copy = []
            self.files_to_copy = []
        elif user_action == rename_action:
            if len(folders) > len(files):
                index = folders[0]
            else:
                index = files[0]
            new_name, ok = QtWidgets.QInputDialog().getText(self, 'Переименовать', 'Введите новое имя:',
                                                            text=index[index.rindex('/') + 1:])
            if ok:
                rename(index, index[:index.rindex('/')+1] + new_name)
        self.model().refresh()

    def selectedFoldersAndFiles(self):
        folders = []
        files = []
        for index in self.selectedIndexes():
            path = self.model().filePath(index)
            if self.model().isDir(index):
                if path not in folders:
                    folders.append(path)
            else:
                if path not in files:
                    files.append(path)
        return folders, files

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control:
            self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Control:
            self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        super().keyReleaseEvent(event)


class QDirModelWithSortingFlag(QtWidgets.QDirModel):
    def __init__(self):
        super().__init__()
        self.setSorting(QtCore.QDir.SortFlag.DirsFirst)
