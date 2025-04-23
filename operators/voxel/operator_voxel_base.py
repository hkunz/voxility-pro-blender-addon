import bpy

from typing import List
from bpy_extras.io_utils import ExportHelper

from voxelity_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxelity_pro.operators.voxel.operator_voxconvert import OperatorVoxconvert
from voxelity_pro.utils.file_utils import FileUtils

class OperatorVoxelBase(OperatorVoxconvert, ExportHelper):
    bl_description = "Operator Voxel Base"

    voxel_type: str = ""

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
        name="Faster but Low Quality", #name="Voxformat Voxelize Mode",
        description="Check for faster and less memory (lower quality) or Uncheck for high quality (slower)",
        default=False,
    ) # type: ignore

    def setup_command(self, input: str, outputs: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = super().setup_command(input, outputs)
        c.vc_voxformat_voxelizemode = int(self.voxformat_voxelizemode)
        c.vc_merge_vertices = int(self.merge_vertices)
        return c

    def draw(self, _context: bpy.types.Context) -> None:
        self.options_panel = self.layout.box().column()

    def draw_elements(self, _context):
        pass
        #self.options_panel.prop(self, "voxformat_voxelizemode")

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        super().invoke(context, event)
        self.options_panel = None
        wm: bpy_types.WindowManager = context.window_manager
        wm.fileselect_add(self)
        self.filepath = FileUtils.check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}