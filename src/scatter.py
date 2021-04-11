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

        self.scattering = Scatter()
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
        default_obj1 = self.scattering.to_transfer_sel
        default_obj2 = self.scattering.transfer_sel

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
        self.sx_min = QtWidgets.QSpinBox()
        self.sx_min.setValue(self.scattering.min_sx)
        self.sx_min.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.sx_max = QtWidgets.QSpinBox()
        self.sx_max.setValue(self.scattering.max_sx)
        self.sx_max.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.sy_min = QtWidgets.QSpinBox()
        self.sy_min.setValue(self.scattering.min_sy)
        self.sy_min.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.sy_max = QtWidgets.QSpinBox()
        self.sy_max.setValue(self.scattering.max_sy)
        self.sy_max.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.sz_min = QtWidgets.QSpinBox()
        self.sz_min.setValue(self.scattering.min_sz)
        self.sz_min.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.sz_max = QtWidgets.QSpinBox()
        self.sz_max.setValue(self.scattering.max_sz)
        self.sz_max.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.rx_min = QtWidgets.QSpinBox()
        self.rx_min.setValue(self.scattering.min_rx)
        self.rx_min.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.rx_max = QtWidgets.QSpinBox()
        self.rx_max.setValue(self.scattering.max_rx)
        self.rx_max.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.ry_min = QtWidgets.QSpinBox()
        self.ry_min.setValue(self.scattering.min_ry)
        self.ry_min.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.ry_max = QtWidgets.QSpinBox()
        self.ry_max.setValue(self.scattering.max_ry)
        self.ry_max.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.rz_min = QtWidgets.QSpinBox()
        self.rz_min.setValue(self.scattering.min_rz)
        self.rz_min.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        self.rz_max = QtWidgets.QSpinBox()
        self.rz_max.setValue(self.scattering.max_rz)
        self.rz_max.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("min"), 0, 1)
        layout.addWidget(QtWidgets.QLabel("max"), 0, 2)
        layout.addWidget(QtWidgets.QLabel("min"), 0, 4)
        layout.addWidget(QtWidgets.QLabel("max"), 0, 5)
        layout.addWidget(QtWidgets.QLabel("X:"), 1, 0)
        layout.addWidget(self.sx_min, 1, 1)
        layout.addWidget(self.sx_max, 1, 2)
        layout.addWidget(QtWidgets.QLabel("X:"), 1, 3)
        layout.addWidget(self.rx_min, 1, 4)
        layout.addWidget(self.rx_max, 1, 5)
        layout.addWidget(QtWidgets.QLabel("Y:"), 2, 0)
        layout.addWidget(self.sy_min, 2, 1)
        layout.addWidget(self.sy_max, 2, 2)
        layout.addWidget(QtWidgets.QLabel("X:"), 2, 3)
        layout.addWidget(self.ry_min, 2, 4)
        layout.addWidget(self.ry_max, 2, 5)
        layout.addWidget(QtWidgets.QLabel("Z:"), 3, 0)
        layout.addWidget(self.sz_min, 3, 1)
        layout.addWidget(self.sz_max, 3, 2)
        layout.addWidget(QtWidgets.QLabel("Z:"), 3, 3)
        layout.addWidget(self.rz_min, 3, 4)
        layout.addWidget(self.rz_max, 3, 5)

        return layout

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
