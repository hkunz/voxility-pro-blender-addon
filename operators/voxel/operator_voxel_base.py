import bpy
import bpy_types

from bpy_extras.io_utils import ExportHelper

from voxility_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxility_pro.operators.voxel.operator_voxconvert import OperatorVoxconvert
from voxility_pro.utils.file_utils import check_filepath

class OperatorVoxelBase(OperatorVoxconvert, ExportHelper):
    bl_description = "Operator Voxel Base"

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

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

    def setup_command(self, input: str, output: str) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = super().setup_command(input, output)
        c.vc_voxformat_voxelizemode = int(self.voxformat_voxelizemode)
        c.vc_merge_vertices = int(self.merge_vertices)
        return c

    def draw(self, _context: bpy_types.Context) -> None:
        self.layout.prop(self, "voxformat_voxelizemode")

    def invoke(self, context: bpy_types.Context, _: bpy.types.Event) -> set[str]:
        wm: bpy_types.WindowManager = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}