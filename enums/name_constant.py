from voxility_pro.enums.voxility_enum import VoxilityEnum
from voxility_pro.utils.utils import get_blender_version, get_addon_version

class NameConstant(VoxilityEnum):
    VOXILITY_VERSION_SUFFIX = "_" + get_blender_version(separator='_') + "_" + get_addon_version(separator='_')
    VOXILITY_NAME="Voxility"
    VOXILITY_NODE_GROUP_NAME = "VoxilityVoxelize" + VOXILITY_VERSION_SUFFIX
    VOXILITY_MODIFIER_NAME = "VoxilityVoxelizeModifier" + VOXILITY_VERSION_SUFFIX