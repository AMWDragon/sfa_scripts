from PySide2 import QtWidgets


class SimpleUI (QtWidgets.QDialog):

    def __init__(self):
        super(SimpleUI, self).__init__()
        self.setWindowTitle("A Simple UI")
