import logging
import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


class SceneFile(object):
    """A representation of a Scene file"""
    def __init__(self, path=None):
        self.folder_path = Path()
        self.descriptor = "main"
        self.task = None
        self.ver = 1
        self.ext = ".ma"
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.warning("Unable to initialize SceneFile object from a "
                        "new scene. Please specify a path.")
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
