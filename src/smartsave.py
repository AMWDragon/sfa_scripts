import logging
import pymel.core as pmc
from pymel.core.system import Path

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

log = logging.getLogger(__name__)


def maya_main_window():
    """Return maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
    """Smart Save UI Class"""

    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(700)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scene_file = SceneFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 22px")

        self.folder_lay = self._create_folder_ui()
        self.filename_lay = self._create_filename_ui()
        self.button_lay = self._create_button_ui()

        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.folder_lay)
        self.main_lay.addLayout(self.filename_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        """Connect widget signals to slots"""
        self.cancel_btn.clicked.connect(self._cancel)
        self.folder_browse_btn.clicked.connect(self._browse_dir)

    @QtCore.Slot()
    def _cancel(self):
        """Quits the dialog"""
        self.close()

    @QtCore.Slot()
    def _browse_dir(self):
        """Browse Directory"""
        this_dir = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select Folder",
            dir=self.folder_le.text(),
            options=QtWidgets.QFileDialog.ShowDirsOnly |
                    QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(this_dir)

    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_increment_btn = QtWidgets.QPushButton("Save Increment")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        layout.addWidget(self.save_increment_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def _create_filename_ui(self):
        layout = self._create_filename_headers()

        self.descriptor_le = QtWidgets.QLineEdit(self.scene_file.descriptor)
        self.descriptor_le.setMinimumWidth(100)
        self.task_le = QtWidgets.QLineEdit(self.scene_file.task)
        self.task_le.setFixedWidth(70)
        self.version_sbx = QtWidgets.QSpinBox()
        self.version_sbx.setValue(self.scene_file.ver)
        self.version_sbx.setFixedWidth(70)
        self.version_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ext_lbl = QtWidgets.QLabel(".ma")

        layout.addWidget(self.descriptor_le, 1, 0)
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
        layout.addWidget(self.task_le, 1, 2)
        layout.addWidget(QtWidgets.QLabel("_V"), 1, 3)
        layout.addWidget(self.version_sbx, 1, 4)
        layout.addWidget(self.ext_lbl, 1, 5)
        return layout

    def _create_filename_headers(self):
        self.descriptor_header_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_header_lbl.setStyleSheet("font: bold 17px")
        self.task_header_lbl = QtWidgets.QLabel("Task")
        self.task_header_lbl.setStyleSheet("font: bold 17px")
        self.version_header_lbl = QtWidgets.QLabel("Version")
        self.version_header_lbl.setStyleSheet("font: bold 17px")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.descriptor_header_lbl, 0, 0)
        layout.addWidget(self.task_header_lbl, 0, 2)
        layout.addWidget(self.version_header_lbl, 0, 4)
        return layout

    def _create_folder_ui(self):
        default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
        default_folder = default_folder / "scenes"
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_btn = QtWidgets.QPushButton(". . .")
        self.folder_browse_btn.setStyleSheet("font: bold")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_btn)
        return layout


class SceneFile(object):
    """A representation of a Scene file"""
    def __init__(self, path=None):
        self.folder_path = Path(cmds.workspace(query=True,
                                               rootDirectory=True)) / "scenes"
        self.descriptor = "main"
        self.task = "model"
        self.ver = 1
        self.ext = ".ma"
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.info("Initialize with default properties.")
            return
        self._init_from_path(path)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """Saves the scene file"""
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directories in path. Creating directories.")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)

    def next_avail_ver(self):
        """Return next available version number in folder."""
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ext=self.ext)
        matching_scenefiles = []

        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)

        if not matching_scenefiles:
            return 1

        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        latest_scenefile = latest_scenefile.name.stripext()
        latest_ver_num = int(latest_scenefile.split("_v")[-1])

        return latest_ver_num + 1

    def increment_save(self):
        """Increments version and saves scene file"""
        self.ver = self.next_avail_ver()
        self.save()
