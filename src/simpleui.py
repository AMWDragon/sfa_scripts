import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def maya_main_window():
    """Return maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SimpleUI (QtWidgets.QDialog):

    def __init__(self):
        super(SimpleUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("A Simple UI")
