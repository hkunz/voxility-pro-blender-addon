import bpy
from enum import Enum

class VoxelityFeature(Enum):
    GN_VOXELIZER_ACTIVE = bpy.app.version >= (3,3,0)