import maya.cmds as cmds
import maya.OpenMaya as om

# determine what the user has selected.

# Store all available objects in a list(drop down menu)and change the selection

# Store all available objects in a list to move objects to it's vertices

# create instances of the object

# move instances to polygon vertices

# change transform node scale randomly for instances

# change transform node rotation randomly for instances


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

        self.creating_instances()

    def creating_instances(self):
        for vertex in self.transfer_vert:
            new_geo = cmds.instance(self.to_transfer_sel)
            vtx_pos = cmds.xform([vertex], query=True, translation=True)
            cmds.xform(new_geo, translation=vtx_pos)
