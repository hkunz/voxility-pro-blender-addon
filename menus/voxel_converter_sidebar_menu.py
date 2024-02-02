import bpy

from voxility_pro.operators.voxel.operator_mesh_voxel_converter import (
    WM_OT_MeshVoxelConvertOperator,
    register as register_mesh_voxel_operator,
    unregister as unregister_mesh_voxel_operator
)

from voxility_pro.utils.utils import get_addon_version

VERTEX_COLORS_SUPPORT_BLENDER_VERSION = (3,3,0) #fixme it's duplicated in base_operator_importer.py

def get_blender_support_text():
    return f"Vertex colors are supported in Blender version {VERTEX_COLORS_SUPPORT_BLENDER_VERSION} and above."

class VoxilityProProperties(bpy.types.PropertyGroup):
    option_dissolve_limited: bpy.props.BoolProperty(
        name="Apply Limited Dissolve",
        description="Simplify mesh by dissolving vertices and edges separating flat regions.",
        default=False,
    )

    voxformat_withcolor: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description=("Use vertex colors in model instead of image texture" if bpy.app.version >= VERTEX_COLORS_SUPPORT_BLENDER_VERSION else get_blender_support_text()),
        default=True,
    )

    merge_vertices: bpy.props.BoolProperty(
        name="Merge Vertices",
        description="Automatically merge vertices and split edges",
        default=True,
    )

    voxformat_voxelizemode: bpy.props.BoolProperty(
        name="Voxformat Voxelize Mode",
        description="Check for faster and less memory (lower quality) or Uncheck for high quality (slower)",
        default=False,
    )

    voxformat_scale: bpy.props.FloatProperty(
        name="Voxformat Scale",
        description="Scale the vertices on all axes by the given factor",
        default=1.0,
        min=0.0,
        max=100.0,
    )

    palette_file: bpy.props.StringProperty(
        name="Palette File",
        description="Path to the palette file",
        default="",
        subtype='FILE_PATH',
    )

    export_palette: bpy.props.BoolProperty(
        name="Export Palette",
        description="Save the included palette as png next to the source file",
        default=False,
    )

    surface_only: bpy.props.BoolProperty(
        name="Surface Only",
        description="Remove any non surface voxel",
        default=False,
    )

class OBJECT_PT_voxility_pro(bpy.types.Panel):
    bl_label = f"Voxility Pro {get_addon_version()}"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Voxility'

    def draw(self, context):
        layout = self.layout
        #layout.prop(context.scene.voxility_pro_properties, "option_dissolve_limited")
        layout.prop(context.scene.voxility_pro_properties, "voxformat_withcolor")
        layout.prop(context.scene.voxility_pro_properties, "merge_vertices")
        layout.prop(context.scene.voxility_pro_properties, "voxformat_scale")
        layout.prop(context.scene.voxility_pro_properties, "voxformat_voxelizemode")
        #layout.prop(context.scene.voxility_pro_properties, "palette_file")
        #layout.prop(context.scene.voxility_pro_properties, "export_palette")
        layout.prop(context.scene.voxility_pro_properties, "surface_only")
        layout.operator(WM_OT_MeshVoxelConvertOperator.bl_idname, text="Voxility Pro")

def register():
    bpy.utils.register_class(VoxilityProProperties)
    bpy.types.Scene.voxility_pro_properties = bpy.props.PointerProperty(type=VoxilityProProperties)
    bpy.utils.register_class(OBJECT_PT_voxility_pro)
    register_mesh_voxel_operator()

def unregister():
    bpy.utils.unregister_class(VoxilityProProperties)
    del bpy.types.Scene.voxility_pro_properties
    bpy.utils.unregister_class(OBJECT_PT_voxility_pro)
    unregister_mesh_voxel_operator()