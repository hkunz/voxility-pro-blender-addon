import bpy

from voxility_pro.operators.voxel.operator_mesh_voxel_converter import (
    OBJECT_OT_MeshVoxelConvertOperator,
    register as register_mesh_voxel_operator,
    unregister as unregister_mesh_voxel_operator
)

from voxility_pro.operators.voxel.operator_clear_all_temp_cache import (
    register as register_all_temp_cache_operator,
    unregister as unregister_all_temp_cache_operator,
)

from voxility_pro.operators.voxel.operator_clear_temp_cache import (
    register as register_temp_cache_operator,
    unregister as unregister_temp_cache_operator,
)

from voxility_pro.menus.voxel_formats_export_menu import VoxelFormatsExportMenu
from voxility_pro.utils.utils import get_addon_version
from voxility_pro.enums.version_type import VersionType

VERTEX_COLORS_SUPPORT_BLENDER_VERSION = VersionType.VERTEX_COLORS_SUPPORT_BLENDER_VERSION.value

def get_blender_support_text() -> str:
    return f"Vertex colors are supported in Blender version {VERTEX_COLORS_SUPPORT_BLENDER_VERSION} and above."

class VoxilityProProperties(bpy.types.PropertyGroup):
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
        items=VoxelFormatsExportMenu.FORMATS,
        default="NONE",
    ) # type: ignore

class OBJECT_PT_voxility_pro(bpy.types.Panel):
    bl_label = f"Voxility Pro {get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxility'

    def draw(self, context) -> None:
        layout: bpy.types.UILayout = self.layout
        properties: VoxilityProProperties = context.scene.voxility_pro_properties

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
        layout.operator(OBJECT_OT_MeshVoxelConvertOperator.bl_idname, text="Voxelize")
        layout.prop(properties, "export_format")

def register() -> None:
    bpy.utils.register_class(VoxilityProProperties)
    bpy.types.Scene.voxility_pro_properties = bpy.props.PointerProperty(type=VoxilityProProperties)
    bpy.utils.register_class(OBJECT_PT_voxility_pro)
    register_mesh_voxel_operator()
    register_temp_cache_operator()
    register_all_temp_cache_operator()

def unregister() -> None:
    bpy.utils.unregister_class(VoxilityProProperties)
    del bpy.types.Scene.voxility_pro_properties
    bpy.utils.unregister_class(OBJECT_PT_voxility_pro)
    unregister_mesh_voxel_operator()
    unregister_temp_cache_operator()
    unregister_all_temp_cache_operator()