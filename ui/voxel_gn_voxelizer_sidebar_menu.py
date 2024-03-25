import bpy
import bpy_types
import time

from typing import List, Tuple
from bpy.app.handlers import persistent

from voxility_pro.ui.selected_objects_list import register as register_selected_objects_list, unregister as unregister_selected_objects_list # type: ignore
from voxility_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu # type: ignore
from voxility_pro.operators.voxel.operator_empty import OBJECT_OT_OperatorEmpty # type: ignore
from voxility_pro.operators.voxel.operator_voxelize import OBJECT_OT_OperatorVoxelize, register as register_gn_voxelizer, unregister as unregister_gn_voxelizer # type: ignore
from voxility_pro.operators.voxel.operator_unvoxelize import OBJECT_OT_OperatorUnvoxelize, register as register_gn_unvoxelizer, unregister as unregister_gn_unvoxelizer # type: ignore
from voxility_pro.operators.voxel.operator_voxelize_validity_check import OBJECT_OT_OperatorVoxelizeValidityCheck # type: ignore
from voxility_pro.operators.voxel.operator_clear_all_temp_cache import register as register_all_temp_cache_operator, unregister as unregister_all_temp_cache_operator # type: ignore
from voxility_pro.operators.voxel.operator_clear_temp_cache import register as register_temp_cache_operator, unregister as unregister_temp_cache_operator # type: ignore
from voxility_pro.utils.utils import get_addon_version # type: ignore
from voxility_pro.utils.material_utils import has_materials # type: ignore
from voxility_pro.utils.icons_manager import IconsManager  # type: ignore
from voxility_pro.utils.voxel.voxel_utils import Voxel, is_object_voxelized, get_voxelizer_modifier, set_voxelizer_voxel_size, get_voxelizer_voxel_size, get_voxelizer_voxel_modifier_attributes, set_voxelizer_voxel_uvmap, set_voxelizer_voxel_vertex_colors # type: ignore

def my_settings_callback(self: bpy.types.Scene, context: bpy_types.Context) -> List[Tuple[str, str, str]]:
    return VoxelFormatsExportMenu.PREFERENCES_FORMATS

def on_input_voxelsize_change(self, context: bpy_types.Context):
    if context.scene.no_voxel_size_update:
        return
    for obj in context.selected_objects:
        vsize = get_voxelizer_voxel_size(obj)
        tolerance = 0.001
        if abs(vsize - self.voxel_size) < tolerance:
            continue
        set_voxelizer_voxel_size(obj, self.voxel_size)

def on_input_uvmap_change(self, context: bpy_types.Context):
    if context.scene.no_voxel_size_update:
        return
    obj = context.active_object
    set_voxelizer_voxel_uvmap(obj, self.uvmap_attribute)

def on_input_colorattr_change(self, context: bpy_types.Context):
    if context.scene.no_voxel_size_update:
        return
    obj = context.active_object
    set_voxelizer_voxel_vertex_colors(obj, self.color_attribute)

def on_voxelize_button_click(self: bpy.types.Scene, context: bpy_types.Context):
    properties: VoxilityProProperties = context.scene.voxility_pro_properties
    properties.voxel_size = Voxel.DEFAULT_VALUE
    Voxel.PREVIOUS_ACTIVE_OBJECT = None
    check_object_selection_change(context, properties, context.active_object)

@persistent
def on_depsgraph_update(scene, depsgraph=None):
    context = bpy.context
    obj = context.active_object
    if not obj or not is_object_voxelized(obj):
        return
    properties: VoxilityProProperties = context.scene.voxility_pro_properties
    check_object_selection_change(context, properties, obj)
    check_uv_map_change(properties, obj)
    check_color_attributes_change(properties, obj)

def check_object_selection_change(context, properties, obj):
    if Voxel.PREVIOUS_ACTIVE_OBJECT == obj:
        return
    Voxel.PREVIOUS_ACTIVE_OBJECT = obj
    voxel_size, uvmap, vertex_colors = get_voxelizer_voxel_modifier_attributes(obj)
    context.scene.no_voxel_size_update = True # so we don't trigger on_input_voxelsize_change which sets all objects
    if voxel_size <= 0.001:
        return
    properties.voxel_size = voxel_size
    properties.uvmap_attribute = uvmap
    properties.color_attribute = vertex_colors
    context.scene.no_voxel_size_update = False

def check_uv_map_change(properties, obj):
    uvmaps = obj.data.uv_layers
    uvname = uvmaps[0].name if len(uvmaps) == 1 else ""
    if Voxel.PREVIOUS_UVMAP_ATTRIBUTE == uvname:
        return
    if not len(uvmaps) > 1:
        properties.uvmap_attribute = uvname
    Voxel.PREVIOUS_UVMAP_ATTRIBUTE = uvname

def check_color_attributes_change(properties, obj):
    cattr = obj.data.color_attributes
    cname = cattr[0].name if len(cattr) == 1 else ""
    if Voxel.PREVIOUS_COLOR_ATTRIBUTE == cname:
        return
    if not len(cattr) > 1:
        properties.color_attribute = cname
    Voxel.PREVIOUS_COLOR_ATTRIBUTE = cname

class VoxilityProProperties(bpy.types.PropertyGroup):
    export_format: bpy.props.EnumProperty(
        name="Target",
        description="Select target voxel export format",
        items=my_settings_callback,
        #default="NONE", # cannot set a default when using dynamic EnumProperty
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    multi_object_export: bpy.props.BoolProperty(
        name="Edit Multiple Objects",
        description="Enable voxelizing and exporting multiple objects per file",
        default=False,
    ) # type: ignore

    voxel_size: bpy.props.FloatProperty(
        name="Voxel Size",
        description="Voxel size in meters",
        default=Voxel.DEFAULT_VALUE,
        min=Voxel.DEFAULT_MIN,
        max=Voxel.DEFAULT_MAX,
        update=on_input_voxelsize_change
    ) # type: ignore

    uvmap_attribute: bpy.props.StringProperty(
        name="UV",
        description="UVMap Attribute",
        update=on_input_uvmap_change
    ) # type: ignore

    color_attribute: bpy.props.StringProperty(
        name="Color",
        description="Vertex Colors Attribute",
        update=on_input_colorattr_change
    ) # type: ignore


class OBJECT_PT_voxility_pro(bpy.types.Panel):
    bl_label = f"Voxility Pro {get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxility'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        selected_mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        active_object = context.active_object if len(selected_mesh_objects) > 0 and context.active_object in selected_mesh_objects else None
        error = self.check_valid(active_object, selected_mesh_objects)

        valid_selection = active_object and not error
        voxelized = is_object_voxelized(active_object)

        if valid_selection:
            properties: VoxilityProProperties = context.scene.voxility_pro_properties
            layout.box().prop(properties, "multi_object_export")
            if properties.multi_object_export:
                ibox = layout.row().box()
                ibox.template_list("MY_UL_List", "The_List", bpy.context.scene, "voxelize_list", bpy.context.scene, "voxelize_list_index", sort_lock=True)
            else:
                ibox = layout.box().box()
                ibox.label(text=active_object.name, icon=IconsManager.BUILTIN_ICON_VOXELIZED if voxelized else IconsManager.BUILTIN_ICON_MESH_DATA)
        else:
            ibox = layout.box().box()
            ibox.alert = True
            ibox.label(text=error)

        unvox = not OBJECT_OT_OperatorVoxelize.poll(context) and OBJECT_OT_OperatorUnvoxelize.poll(context)
        mbox = layout.box()
        mbox.operator((OBJECT_OT_OperatorUnvoxelize if unvox else OBJECT_OT_OperatorVoxelize).bl_idname, text="Unvoxelize" if unvox else "Voxelize")

        if valid_selection:
            if voxelized:
                self.draw_voxelizer_options(context, mbox)
            self.draw_export_options(context, layout)

    def check_valid(self, active_object, selected_mesh_objects):
        non_mesh = next((obj for obj in bpy.context.selected_objects if obj.type != 'MESH'), None)
        active = active_object if len(selected_mesh_objects) > 0 and active_object in selected_mesh_objects else None
        if non_mesh:
            return f"Non-mesh \"{non_mesh.name}\""
        if active is None:
            return "No active mesh object!"
        return None

    def draw_voxelizer_options(self, context, layout: bpy.types.UILayout):
        properties: VoxilityProProperties = context.scene.voxility_pro_properties
        active_object = context.active_object
        box = layout.box()
        r1 = box.row()
        r1.prop(properties, "voxel_size")
        col = box.column()
        if not has_materials(active_object):
            col.label(text="Object has no Materials")
            return
        r2 = col.row()
        if len(active_object.data.uv_layers) > 0:
            r2.label(text="UV Map:")
            r2.prop(properties, "uvmap_attribute", text="")
        else:
            r2.label(text="No UV Map")
        r3 = col.row()
        if len(active_object.data.color_attributes) > 0:
            r3.label(text="Vertex Colors:")
            r3.prop(properties, "color_attribute", text="")
        else:
            r3.label(text="No Color Attribute")

    def draw_export_options(self, context, layout):
        ebox = layout.box()
        row = ebox.box().row()
        row.prop(
            context.scene, "expanded_export",
            icon="TRIA_DOWN" if context.scene.expanded_export else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )

        row.label(text="Export")

        if not context.scene.expanded_export:
            return

        properties: VoxilityProProperties = context.scene.voxility_pro_properties
        ebox.prop(properties, "export_format")
        format_selected = properties.export_format != VoxelFormatsExportMenu.SELECTION_NONE
        bl_idname = f"export.voxility_{VoxelFormatsExportMenu.get_format_name(properties.export_format, True)}" if format_selected else ""

        button_text = "Export" + (" " + properties.export_format if bl_idname else "")
        btn = ebox.column()
        btn.operator(OBJECT_OT_OperatorVoxelizeValidityCheck.bl_idname, text="Check for Problems")
        btn.operator(bl_idname if bl_idname else "object.voxility_null_operator", text=button_text)

    @classmethod
    def poll(cls, context):
        return True


def register() -> None:
    bpy.utils.register_class(VoxilityProProperties)
    bpy.types.Scene.voxility_pro_properties = bpy.props.PointerProperty(type=VoxilityProProperties)
    bpy.types.Scene.expanded_export = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.on_voxelize_button_click = on_voxelize_button_click
    bpy.types.Scene.no_voxel_size_update = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(OBJECT_PT_voxility_pro)
    bpy.utils.register_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    register_gn_voxelizer()
    register_gn_unvoxelizer()
    register_selected_objects_list()
    register_temp_cache_operator()
    register_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)


def unregister() -> None:
    bpy.utils.unregister_class(VoxilityProProperties)
    del bpy.types.Scene.expanded_export
    del bpy.types.Scene.voxility_pro_properties
    del bpy.types.Scene.on_voxelize_button_click
    del bpy.types.Scene.no_voxel_size_update
    bpy.utils.unregister_class(OBJECT_PT_voxility_pro)
    bpy.utils.unregister_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    unregister_gn_voxelizer()
    unregister_gn_unvoxelizer()
    unregister_selected_objects_list()
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.clear()