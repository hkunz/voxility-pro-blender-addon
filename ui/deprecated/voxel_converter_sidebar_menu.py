import bpy

from typing import Tuple, List

from voxelity_pro.operators.voxel.deprecated.operator_mesh_voxel_converter import (
    OBJECT_OT_MeshVoxelConvertOperator,
    register as register_mesh_voxel_operator,
    unregister as unregister_mesh_voxel_operator
)

from voxelity_pro.operators.voxel.deprecated.operator_mesh_voxel_save import (
    OBJECT_OT_MeshVoxelSaveOperator,
    register as register_mesh_voxel_save_operator,
    unregister as unregister_mesh_voxel_save_operator
)

from voxelity_pro.operators.voxel.operator_clear_all_temp_cache import (
    register as register_all_temp_cache_operator,
    unregister as unregister_all_temp_cache_operator,
)

from voxelity_pro.operators.voxel.operator_clear_temp_cache import (
    register as register_temp_cache_operator,
    unregister as unregister_temp_cache_operator,
)

from voxelity_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu
from voxelity_pro.utils.utils import Utils
from voxelity_pro.enums.version_type import VersionType

VERTEX_COLORS_SUPPORT_BLENDER_VERSION = VersionType.VERTEX_COLORS_SUPPORT_BLENDER_VERSION.value

def get_blender_support_text() -> str:
    return f"Vertex colors are supported in Blender version {VERTEX_COLORS_SUPPORT_BLENDER_VERSION} and above."

def my_settings_callback(scene: bpy.types.Scene, _: bpy.types.Context) -> List[Tuple[str, str, str]]:
    return VoxelFormatsExportMenu.PREFERENCES_FORMATS

class VoxelityProProperties(bpy.types.PropertyGroup):
    option_dissolve_limited: bpy.props.BoolProperty(
        name="Apply Limited Dissolve",
        description="Simplify mesh by dissolving vertices and edges separating flat regions.",
        default=False,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    voxformat_withcolor: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description=("Use vertex colors in model instead of image texture" if bpy.app.version >= VERTEX_COLORS_SUPPORT_BLENDER_VERSION else get_blender_support_text()),
        default=(bpy.app.version >= VERTEX_COLORS_SUPPORT_BLENDER_VERSION),
    ) # type: ignore

    merge_vertices: bpy.props.BoolProperty(
        name="Merge Vertices",
        description="Automatically merge vertices and split edges",
        default=True,
    ) # type: ignore

    voxformat_voxelizemode: bpy.props.BoolProperty(
        name="Voxformat Voxelize Mode",
        description="Check for faster and less memory (lower quality) or Uncheck for high quality (slower)",
        default=False,
    ) # type: ignore

    voxformat_scale: bpy.props.FloatProperty(
        name="Voxformat Scale",
        description="Scale the vertices on all axes by the given factor",
        default=1.0,
        min=0.0,
        max=100.0,
    ) # type: ignore

    palette_file: bpy.props.StringProperty(
        name="Palette File",
        description="Path to the palette file",
        default="",
        subtype='FILE_PATH',
    ) # type: ignore

    export_palette: bpy.props.BoolProperty(
        name="Export Palette",
        description="Save the included palette as png next to the source file",
        default=False,
    ) # type: ignore

    surface_only: bpy.props.BoolProperty(
        name="Surface Only",
        description="Remove any non surface voxel",
        default=False,
    ) # type: ignore

    voxformat_mergequads: bpy.props.BoolProperty(
        name="Merge Quads",
        description="Merge similar quads",
        default=True,
    ) # type: ignore

    hide_original_objects: bpy.props.BoolProperty(
        name="Hide Original Objects",
        description="Hide the original objects after voxelization is complete",
        default=True,
    ) # type: ignore

    export_format: bpy.props.EnumProperty(
        name="Target",
        description="Select target voxel export format",
        items=my_settings_callback,
        #default="NONE", # cannot set a default when using dynamic EnumProperty
    ) # type: ignore

class OBJECT_PT_voxelity_pro(bpy.types.Panel):
    bl_label = f"Voxelity Pro {Utils.get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxelity'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        properties: VoxelityProProperties = context.scene.voxelity_pro_properties

        vertex_color_support = bpy.app.version >= VERTEX_COLORS_SUPPORT_BLENDER_VERSION
        col: bpy.types.UILayout = layout.column()
        sub: bpy.types.UILayout = col.row()
        sub.enabled = vertex_color_support
        sub.prop(properties, "voxformat_withcolor")

        layout.prop(properties, "merge_vertices")
        layout.prop(properties, "voxformat_scale")
        layout.prop(properties, "voxformat_voxelizemode")
        layout.prop(properties, "surface_only")
        layout.prop(properties, "voxformat_mergequads")
        layout.prop(properties, "hide_original_objects")

        op = layout.operator(OBJECT_OT_MeshVoxelConvertOperator.bl_idname, text="Voxelize")
        op.vox_target_format_ext = properties.export_format # <bpy_struct, OBJECT_OT_voxelity_mesh_voxel_convert at 0x0000021AE2D89BC8> <class 'bpy.types.OBJECT_OT_voxelity_mesh_voxel_convert'>

        layout.prop(properties, "export_format")

        if properties.export_format == VoxelFormatsExportMenu.SELECTION_NONE:
            return

        op = layout.operator(OBJECT_OT_MeshVoxelSaveOperator.bl_idname, text="Save Target Format")
        OBJECT_OT_MeshVoxelSaveOperator.VOX_TARGET_FORMAT_CURRENT_SELECTION = properties.export_format

def register() -> None:
    bpy.utils.register_class(VoxelityProProperties)
    bpy.types.Scene.voxelity_pro_properties = bpy.props.PointerProperty(type=VoxelityProProperties)
    bpy.types.Object.voxelized = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(OBJECT_PT_voxelity_pro)
    register_mesh_voxel_operator()
    register_mesh_voxel_save_operator()
    register_temp_cache_operator()
    register_all_temp_cache_operator()

def unregister() -> None:
    bpy.utils.unregister_class(VoxelityProProperties)
    del bpy.types.Scene.voxelity_pro_properties
    del bpy.types.Object.voxelized
    bpy.utils.unregister_class(OBJECT_PT_voxelity_pro)
    unregister_mesh_voxel_operator()
    unregister_mesh_voxel_save_operator()
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()