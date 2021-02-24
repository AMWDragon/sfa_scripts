# this will be a workspace for notes while I'm following the lectures

class SceneFile(object):
    """A representation of a Scene file"""
    def __init__(self, folder_path, descriptor, task, ver, ext):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.ver = ver
        self.ext = ext


scene_file = SceneFile("D:\\", "tank", "model", "v001", ".ma")
print(scene_file.descriptor)
