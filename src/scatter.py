import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import random
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance


def maya_main_window():
    """Return maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())

        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(700)
        self.setMaximumHeight(700)

        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)

        # self.scattering = Scatter()
        self.create_ui()

    def create_ui(self):
        self.heading = QtWidgets.QLabel("Scatter Tool")
        self.heading.setStyleSheet("font: bold 25px")

        self.object_layout = self._create_object_ui()
        self.rs_headers = self._create_scale_rotate_headers()
        self.rs_layout = self._create_scale_rotate_ui()
        self.btn_layout = self._create_button_ui()

        self.primary_layout = QtWidgets.QVBoxLayout()
        self.primary_layout.addWidget(self.heading)
        self.primary_layout.addLayout(self.object_layout)
        self.primary_layout.addLayout(self.rs_headers)
        self.primary_layout.addLayout(self.rs_layout)
        self.primary_layout.addStretch()
        self.primary_layout.addLayout(self.btn_layout)

        self.setLayout(self.primary_layout)

    def _create_object_ui(self):
        default_obj1 = "Connect Something Here"
        default_obj2 = "Connect Something Else Here"

        self.obj1_le = QtWidgets.QLineEdit(default_obj1)
        self.obj2_le = QtWidgets.QLineEdit(default_obj2)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Scatter"), 0, 0)
        layout.addWidget(self.obj1_le, 0, 1)
        layout.addWidget(QtWidgets.QLabel("on to"), 0, 2)
        layout.addWidget(self.obj2_le, 0, 3)

        return layout

    def _create_scale_rotate_headers(self):
        self.scale_header = QtWidgets.QLabel("Randomize Scale")
        self.scale_header.setStyleSheet("font: bold 20px")
        self.rotation_header = QtWidgets.QLabel("Randomize Rotation")
        self.rotation_header.setStyleSheet("font: bold 20px")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_header, 2, 0)
        layout.addWidget(self.rotation_header, 2, 2)

        return layout

    def _create_scale_rotate_ui(self):
        pass

    def _create_button_ui(self):
        pass

    def _create_connections(self):
        pass


class Scatter(object):
    """My code for the Scatter Tool"""

    def __init__(self):
        self.cur_sel = cmds.ls(selection=True)
        self.to_transfer_sel = self.cur_sel[0]

        self.all_geo = cmds.ls(geometry=True)
        self.all_trans = cmds.ls(transforms=True)

        self.transfer_sel = self.cur_sel[1]
        self.transfer_vert = cmds.ls(self.transfer_sel + ".vtx[*]",
                                     flatten=True)

        self.min_sx = 1.0
        self.max_sx = 2.0
        self.min_sy = 1.0
        self.max_sy = 2.0
        self.min_sz = 1.0
        self.max_sz = 2.0

        self.min_rx = 1.0
        self.max_rx = 360.0
        self.min_ry = 1.0
        self.max_ry = 360.0
        self.min_rz = 1.0
        self.max_rz = 360.0

        self.creating_instances()

    def creating_instances(self):
        for vertex in self.transfer_vert:
            new_geo = cmds.instance(self.to_transfer_sel)
            vtx_pos = cmds.xform([vertex], query=True, translation=True)
            print(vtx_pos)
            cmds.xform(new_geo, translation=vtx_pos,
                       scale=self.randomize_scale(),
                       rotation=self.randomize_rotation())

    def randomize_scale(self):
        random_sx = random.uniform(self.min_sx, self.max_sx)
        random_sy = random.uniform(self.min_sy, self.max_sy)
        random_sz = random.uniform(self.min_sz, self.max_sz)

        rand_scale = [random_sx, random_sy, random_sz]
        return rand_scale

    def randomize_rotation(self):
        random_rx = random.uniform(self.min_rx, self.max_rx)
        random_ry = random.uniform(self.min_ry, self.max_ry)
        random_rz = random.uniform(self.min_rz, self.max_rz)

        rand_rotate = (random_rx, random_ry, random_rz)
        return rand_rotate
