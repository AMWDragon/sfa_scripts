import maya.cmds as cmds
import maya.OpenMaya as om
import random
import math

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
        cmds.selection(clear=True)

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
