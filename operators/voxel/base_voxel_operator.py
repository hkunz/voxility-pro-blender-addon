import bpy
from bpy_extras.io_utils import ExportHelper

import bpy

from voxility_pro.operators.voxel.voxconvert_operator import VoxconvertOperator
from voxility_pro.utils.file_utils import check_filepath

class BaseVoxelOperator(VoxconvertOperator, ExportHelper):
    bl_description = "Base Voxel Operator"

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
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

    def setup_command(self, input, output):
        c = super().setup_command(input, output)
        c.vc_voxformat_voxelizemode = int(self.voxformat_voxelizemode)
        c.vc_merge_vertices = int(self.merge_vertices)
        return c

    def draw(self, _context):
        self.layout.prop(self, "voxformat_voxelizemode")

    def invoke(self, context, _event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}