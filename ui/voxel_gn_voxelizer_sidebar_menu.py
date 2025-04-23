import bpy
import bpy_types
import os

from typing import List, Tuple
from bpy.app.handlers import persistent

from voxelity_pro.ui.selected_objects_list import register as register_selected_objects_list, unregister as unregister_selected_objects_list # type: ignore
from voxelity_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu # type: ignore
from voxelity_pro.ui.voxel_formats_import_menu import VoxelFormatsImportMenu # type: ignore
from voxelity_pro.operators.voxel.operator_empty import OBJECT_OT_OperatorEmpty # type: ignore
from voxelity_pro.operators.voxel.operator_bake import OBJECT_OT_OperatorBake, register as register_bake_utility, unregister as unregister_bake_utility # type: ignore
from voxelity_pro.operators.voxel.operator_voxelize import OBJECT_OT_OperatorVoxelize, register as register_gn_voxelizer, unregister as unregister_gn_voxelizer # type: ignore
from voxelity_pro.operators.voxel.operator_unvoxelize import OBJECT_OT_OperatorUnvoxelize, register as register_gn_unvoxelizer, unregister as unregister_gn_unvoxelizer # type: ignore
from voxelity_pro.operators.voxel.operator_voxelize_validity_check import OBJECT_OT_OperatorVoxelizeValidityCheck # type: ignore
from voxelity_pro.operators.voxel.operator_clear_all_temp_cache import register as register_all_temp_cache_operator, unregister as unregister_all_temp_cache_operator # type: ignore
from voxelity_pro.operators.voxel.operator_clear_temp_cache import register as register_temp_cache_operator, unregister as unregister_temp_cache_operator # type: ignore
from voxelity_pro.utils.utils import Utils # type: ignore
from voxelity_pro.utils.object_utils import ObjectUtils # type: ignore
from voxelity_pro.utils.material_utils import MaterialUtils # type: ignore
from voxelity_pro.utils.icons_manager import IconsManager  # type: ignore
from voxelity_pro.utils.voxel.voxel_utils import Voxel, VoxelUtils # type: ignore

IDNAME_ICONS = {
    "NodeSocketMaterial": "MATERIAL_DATA",
    "NodeSocketCollection": "OUTLINER_COLLECTION",
    "NodeSocketTexture": "TEXTURE_DATA",
    "NodeSocketImage": "IMAGE_DATA",
}
IDNAME_TYPE = {
    "NodeSocketMaterial": "materials",
    "NodeSocketCollection": "collections",
    "NodeSocketTexture": "textures",
    "NodeSocketImage": "images",
}

def my_settings_callback(self: bpy.types.Scene, context: bpy_types.Context) -> List[Tuple[str, str, str]]:
    return VoxelFormatsExportMenu.PREFERENCES_FORMATS

def on_voxelize_button_click(self: bpy.types.Scene, context: bpy_types.Context):
    properties: VoxelityProProperties = context.scene.voxelity_pro_properties
    Voxel.PREVIOUS_ACTIVE_OBJECT = None
    check_object_selection_change(context, properties, context.active_object)

@persistent
def on_depsgraph_update(scene, depsgraph=None):
    context = bpy.context
    if not hasattr(context, "active_object"): # context is different when baking image
        return
    obj = context.active_object
    if not obj or not VoxelUtils.is_object_voxelized(obj):
        return
    properties: VoxelityProProperties = context.scene.voxelity_pro_properties
    check_object_selection_change(context, properties, obj)

def check_object_selection_change(context, properties, obj):
    if Voxel.PREVIOUS_ACTIVE_OBJECT == obj:
        return
    Voxel.PREVIOUS_ACTIVE_OBJECT = obj

class VoxelityProProperties(bpy.types.PropertyGroup):
    IMPORT_FORMATS=VoxelFormatsImportMenu.FORMATS
    SELECTION_NONE: bpy.props.StringProperty(default=VoxelFormatsExportMenu.SELECTION_NONE) # type: ignore

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

    file_to_convert_path: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH'
    ) # type: ignore

class OBJECT_PT_voxelity_pro(bpy.types.Panel):
    bl_label = f"Voxelity Pro {Utils.get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxelity'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        selected_mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        active_object = context.active_object if len(selected_mesh_objects) > 0 and context.active_object in selected_mesh_objects else None
        error = self.check_valid(active_object, selected_mesh_objects)

        valid_selection = active_object and not error
        voxelize_progress = VoxelUtils.is_object_voxelized(active_object)
        properties: VoxelityProProperties = context.scene.voxelity_pro_properties

        if valid_selection:
            # layout.box().prop(properties, "multi_object_export")
            if len(selected_mesh_objects) > 1: # properties.multi_object_export
                ibox = layout.row().box()
                ibox.template_list("MY_UL_List", "The_List", bpy.context.scene, "voxelize_list", bpy.context.scene, "voxelize_list_index", sort_lock=True)
            else:
                ibox = layout.box().box()
                ibox.label(text=active_object.name, icon=IconsManager.BUILTIN_ICON_VOXELIZED if voxelize_progress else IconsManager.BUILTIN_ICON_MESH_DATA)
        else:
            ibox = layout.box().box()
            ibox.alert = True
            ibox.label(text=error)

        if selected_mesh_objects and valid_selection:
            unvox = not OBJECT_OT_OperatorVoxelize.poll(context) and OBJECT_OT_OperatorUnvoxelize.poll(context)
            mbox = layout.box()
            mbox.operator((OBJECT_OT_OperatorUnvoxelize if unvox else OBJECT_OT_OperatorVoxelize).bl_idname, text="Unvoxelize" if unvox else "Voxelize")
            if voxelize_progress:
                self.draw_voxelizer_options(context, properties, mbox)
            if active_object and active_object.voxelized:
                self.draw_export_options(context, properties, layout)
        elif not context.selected_objects:
            self.draw_file_conversion_options(context, properties, layout)

    def check_valid(self, active_object, selected_mesh_objects):
        non_mesh = next((obj for obj in bpy.context.selected_objects if obj.type != 'MESH'), None)
        active = active_object if len(selected_mesh_objects) > 0 and active_object in selected_mesh_objects else None
        if non_mesh:
            return f"Non-mesh \"{non_mesh.name}\""
        if active is None:
            return "No active mesh object!"
        return None

    def draw_voxelizer_options(self, context, properties, layout: bpy.types.UILayout):
        active_object = context.active_object
        modifier = VoxelUtils.get_voxelizer_modifier(active_object)
        box = layout.box()
        r1 = box.row()
        #r1.prop(properties, "voxel_size")
        self.add_layout_gn_prop(r1, modifier, VoxelUtils.get_voxelizer_voxel_size_attr_name())
        col = box.column()
        if not MaterialUtils.has_materials(active_object):
            col.label(text="Object has no Materials")
            return
        r2 = col.row()
        if len(active_object.data.uv_layers) > 0:
            #r2.label(text="UV Map:")
            #r2.prop(properties, "uvmap_attribute", text="")
            self.add_layout_gn_prop(r2, modifier, VoxelUtils.get_voxelizer_voxel_uv_attr_name())
        else:
            r2.label(text="No UV Map")
        r3 = col.row()
        if len(active_object.data.color_attributes) > 0:
            #r3.label(text="Vertex Colors:")
            #r3.prop(properties, "color_attribute", text="")
            self.add_layout_gn_prop(r3, modifier, VoxelUtils.get_voxelizer_voxel_vertex_colors_attr_name())
        else:
            r3.label(text="No Color Attribute")

    def draw_file_conversion_options(self, context, properties, layout):
        ebox = layout.box()
        row = ebox.box().row()
        row.prop(
            context.scene, "expanded_fileconvert",
            icon="TRIA_DOWN" if context.scene.expanded_fileconvert else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )

        row.label(text="File Conversion")

        if context.scene.expanded_fileconvert:
            col = ebox.column()
            col.prop(properties, "file_to_convert_path", text="File Input")
            ext = os.path.splitext(properties.file_to_convert_path)[1][1:].upper()
            to = properties.export_format
            button_text = "Convert Voxel File" if not ext or to == VoxelFormatsExportMenu.SELECTION_NONE else f"Convert {ext} to {to}"
            self.add_export_button(context, properties, col, button_text, False)

    def draw_export_options(self, context, properties, layout):
        ebox = layout.box()
        row = ebox.box().row()
        row.prop(
            context.scene, "expanded_export",
            icon="TRIA_DOWN" if context.scene.expanded_export else "TRIA_RIGHT",
            icon_only=True, emboss=False
        )

        row.label(text="Export")

        if context.scene.expanded_export:
            self.add_export_button(context, properties, ebox)

    def add_export_button(self, context, properties, layout, button_text=None, validity_check=True):
        layout.prop(properties, "export_format")
        format_selected = properties.export_format != VoxelFormatsExportMenu.SELECTION_NONE
        bl_idname = f"export.voxelity_{VoxelFormatsExportMenu.get_format_name(properties.export_format, True)}" if format_selected else ""
        if not button_text:
            button_text = "Export" + (" " + properties.export_format if bl_idname else "")
        btn = layout.column()
        if validity_check:
            btn.operator(OBJECT_OT_OperatorVoxelizeValidityCheck.bl_idname, text="Check for Problems")
            btn.operator(OBJECT_OT_OperatorBake.bl_idname, text="Bake")
        else:
            btn.label(text="")
        btn.operator(bl_idname if bl_idname else "object.voxelity_null_operator", text=button_text)

    def add_layout_gn_prop(self, layout, modifier, prop_id):
        name = ObjectUtils.get_modifier_prop_name(modifier, prop_id)
        layout.prop(data=modifier, property=f'["{prop_id}"]', text=name)

    def add_layout_gn_prop_pointer(self, layout, md, rna):
        if rna.bl_socket_idname == "NodeSocketGeometry":
            return
        if rna.bl_socket_idname in IDNAME_ICONS:
            layout.prop_search(md, f'["{rna.identifier}"]',
                search_data = bpy.data,
                search_property = IDNAME_TYPE[rna.bl_socket_idname],
                icon = IDNAME_ICONS[rna.bl_socket_idname],
                text = "My " + rna.name
            )
        else:
            layout.prop(md, f'["{rna.identifier}"]', text=rna.name)

    @classmethod
    def poll(cls, context):
        return True

def register() -> None:
    bpy.utils.register_class(VoxelityProProperties)
    bpy.types.Scene.voxelity_pro_properties = bpy.props.PointerProperty(type=VoxelityProProperties)
    bpy.types.Scene.expanded_export = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.expanded_fileconvert = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.on_voxelize_button_click = on_voxelize_button_click
    bpy.types.Object.voxelized = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(OBJECT_PT_voxelity_pro)
    bpy.utils.register_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    register_gn_voxelizer()
    register_gn_unvoxelizer()
    register_bake_utility()
    register_selected_objects_list()
    register_temp_cache_operator()
    register_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

def unregister() -> None:
    bpy.utils.unregister_class(VoxelityProProperties)
    del bpy.types.Scene.expanded_export
    del bpy.types.Scene.expanded_fileconvert
    del bpy.types.Scene.voxelity_pro_properties
    del bpy.types.Scene.on_voxelize_button_click
    bpy.utils.unregister_class(OBJECT_PT_voxelity_pro)
    bpy.utils.unregister_class(OBJECT_OT_OperatorEmpty)
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)
    unregister_gn_voxelizer()
    unregister_gn_unvoxelizer()
    unregister_bake_utility()
    unregister_selected_objects_list()
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()
    bpy.app.handlers.depsgraph_update_post.remove(on_depsgraph_update)