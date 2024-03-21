import bpy
import bpy_types
import re

from typing import List, Tuple
import time

from voxility_pro.ui.selected_objects_list import register as register_selected_objects_list, unregister as unregister_selected_objects_list # type: ignore
from voxility_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu # type: ignore
from voxility_pro.operators.voxel.operator_voxel_base_exporter import OperatorVoxelBaseExporter # type: ignore
from voxility_pro.operators.voxel.operator_voxelize import OBJECT_OT_OperatorVoxelize, register as register_gn_voxelizer, unregister as unregister_gn_voxelizer # type: ignore
from voxility_pro.operators.voxel.operator_unvoxelize import OBJECT_OT_OperatorUnvoxelize, register as register_gn_unvoxelizer, unregister as unregister_gn_unvoxelizer # type: ignore
from voxility_pro.operators.voxel.operator_voxelize_validity_check import OBJECT_OT_OperatorVoxelizeValidityCheck # type: ignore
from voxility_pro.operators.voxel.operator_clear_all_temp_cache import register as register_all_temp_cache_operator, unregister as unregister_all_temp_cache_operator # type: ignore
from voxility_pro.operators.voxel.operator_clear_temp_cache import register as register_temp_cache_operator, unregister as unregister_temp_cache_operator # type: ignore
from voxility_pro.utils.utils import get_addon_version # type: ignore
from voxility_pro.utils.voxel.voxel_utils import get_voxelizer_modifier # type: ignore

def my_settings_callback(scene: bpy.types.Scene, _: bpy_types.Context) -> List[Tuple[str, str, str]]:
    return VoxelFormatsExportMenu.PREFERENCES_FORMATS

class VoxilityProProperties(bpy.types.PropertyGroup):
    export_format: bpy.props.EnumProperty(
        name="Format",
        description="Select target voxel export format",
        items=my_settings_callback,
        #default="NONE", # cannot set a default when using dynamic EnumProperty
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770



class OBJECT_PT_voxility_pro(bpy.types.Panel):
    bl_label = f"Voxility Pro {get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxility'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        properties: VoxilityProProperties = context.scene.voxility_pro_properties

        selected_objects = context.selected_objects
        selected_mesh_objects = [obj for obj in selected_objects if obj.type == 'MESH']
        selected_voxelized_objects = [obj for obj in selected_objects if get_voxelizer_modifier(obj) is not None]
        num_selected_mesh_objects = len(selected_mesh_objects)

        active_object = context.active_object if len(selected_mesh_objects) > 0 and context.active_object in selected_mesh_objects else None
        error = self.check_valid(active_object, selected_objects, selected_mesh_objects, selected_voxelized_objects)
        row = layout.row()

        valid_selection = active_object and not error

        if valid_selection:
            split = layout.split(factor=0.5)
            split.label(text="Active Object:")
            split_prop = split.split(factor=1)
            split_prop.prop(active_object, "name", text="", expand=True)
            split_prop.enabled = False
        else:
            box = row.box()
            box2 = box.box()
            box2.alert = True
            box2.label(text=error)

        if num_selected_mesh_objects > 0 and not error:
            box = layout.row()
            row = box.row()
            box.scale_y = 1.0
            row.template_list("MY_UL_List", "The_List", bpy.context.scene, "voxelize_list", bpy.context.scene, "voxelize_list_index", sort_lock=True)

        if valid_selection:
            layout.operator(OBJECT_OT_OperatorVoxelizeValidityCheck.bl_idname, text="Validity Check")

        if not OBJECT_OT_OperatorVoxelize.poll(context) and OBJECT_OT_OperatorUnvoxelize.poll(context):
            layout.operator(OBJECT_OT_OperatorUnvoxelize.bl_idname, text="Unvoxelize")
        else:
            layout.operator(OBJECT_OT_OperatorVoxelize.bl_idname, text="Voxelize")
        

        obj = context.object
        if not obj or not obj.type == "MESH":
            return

        box = layout.box()
        row = box.row()
        row.prop(obj, "expanded_export",
            icon="TRIA_DOWN" if obj.expanded_export else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )
        row.label(text="Export")

        if obj.expanded_export:
            bl_idname = ""
            layout.prop(properties, "export_format")
            format_selected = properties.export_format != VoxelFormatsExportMenu.SELECTION_NONE
            if format_selected:
                bl_idname = "export.voxility_" + VoxelFormatsExportMenu.get_format_name(properties.export_format).replace(" ", "_").lower()
            layout.operator(bl_idname if bl_idname else "export.voxility_export", text="Export" + (" " + properties.export_format if bl_idname else ""))


    def check_valid(self, active_object, selected_objects, selected_mesh_objects, selected_voxelized_objects):
        non_mesh = next((obj for obj in bpy.context.selected_objects if obj.type != 'MESH'), None)
        active = active_object if len(selected_mesh_objects) > 0 and active_object in selected_mesh_objects else None
        if non_mesh:
            return f"Non-mesh \"{non_mesh.name}\""
        if active is None:
            return "No active mesh object!"
        return None

    @classmethod
    def poll(cls, context):
        return True


def register() -> None:
    bpy.types.Object.expanded_export = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(VoxilityProProperties)
    bpy.types.Scene.voxility_pro_properties = bpy.props.PointerProperty(type=VoxilityProProperties)
    bpy.utils.register_class(OBJECT_PT_voxility_pro)
    bpy.utils.register_class(OperatorVoxelBaseExporter)
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    register_gn_voxelizer()
    register_gn_unvoxelizer()
    register_selected_objects_list()
    register_temp_cache_operator()
    register_all_temp_cache_operator()

def unregister() -> None:
    del bpy.types.Object.expanded_export
    bpy.utils.unregister_class(VoxilityProProperties)
    del bpy.types.Scene.voxility_pro_properties
    bpy.utils.unregister_class(OBJECT_PT_voxility_pro)
    bpy.utils.unregister_class(OperatorVoxelBaseExporter)
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    unregister_gn_voxelizer()
    unregister_gn_unvoxelizer()
    unregister_selected_objects_list()
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()