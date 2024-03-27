from voxility_pro.enums.voxility_enum import VoxilityEnum # type: ignore
from voxility_pro.utils.utils import get_addon_version, get_gn_voxelizer_version # type: ignore

class NameConstant(VoxilityEnum):
    VOXILITY_VERSION_SUFFIX = get_gn_voxelizer_version() + "_" + get_addon_version(separator='_')
    VOXILITY_NAME="Voxility"
    VOXILITY_NODE_GROUP_NAME_PREFIX = "VoxilityVoxelize_"
    VOXILITY_NODE_GROUP_NAME = VOXILITY_NODE_GROUP_NAME_PREFIX + VOXILITY_VERSION_SUFFIX
    VOXILITY_MODIFIER_NAME_PREFIX = "VoxilityVoxelizeModifier_"
    VOXILITY_MODIFIER_NAME = VOXILITY_MODIFIER_NAME_PREFIX + VOXILITY_VERSION_SUFFIX