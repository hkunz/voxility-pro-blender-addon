import bpy

from typing import List

from voxility_pro.operators.voxel.operator_voxelize import OBJECT_OT_OperatorVoxelize
from voxility_pro.operators.voxel.operator_voxelize_validity_check import OBJECT_OT_OperatorVoxelizeValidityCheck

from voxility_pro.operators.voxel.operator_clear_all_temp_cache import (
    register as register_all_temp_cache_operator,
    unregister as unregister_all_temp_cache_operator,
)

from voxility_pro.operators.voxel.operator_clear_temp_cache import (
    register as register_temp_cache_operator,
    unregister as unregister_temp_cache_operator,
)

from voxility_pro.utils.utils import get_addon_version
from voxility_pro.enums.version_type import VersionType

class VoxilityProProperties(bpy.types.PropertyGroup):
    merge_vertices: bpy.props.BoolProperty(
        name="Apply Limited Dissolve",
        description="Simplify mesh by dissolving vertices and edges separating flat regions.",
        default=False,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770


class OBJECT_PT_voxility_pro(bpy.types.Panel):
    bl_label = f"Voxility Pro {get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxility'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        properties: VoxilityProProperties = context.scene.voxility_pro_properties

        col: bpy.types.UILayout = layout.column()
        sub: bpy.types.UILayout = col.row()
        sub.enabled = False
        sub.prop(properties, "voxformat_withcolor")

        layout.prop(properties, "merge_vertices")

        op = layout.operator(OBJECT_OT_OperatorVoxelizeValidityCheck.bl_idname, text="Validity Check")
        op = layout.operator(OBJECT_OT_OperatorVoxelize.bl_idname, text="Voxelize")

def register() -> None:
    bpy.utils.register_class(VoxilityProProperties)
    bpy.types.Scene.voxility_pro_properties = bpy.props.PointerProperty(type=VoxilityProProperties)
    bpy.utils.register_class(OBJECT_PT_voxility_pro)
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    register_temp_cache_operator()
    register_all_temp_cache_operator()

def unregister() -> None:
    bpy.utils.unregister_class(VoxilityProProperties)
    del bpy.types.Scene.voxility_pro_properties
    bpy.utils.unregister_class(OBJECT_PT_voxility_pro)
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()