import bpy
from bpy_extras.io_utils import ExportHelper

from voxility_pro.utils.file_utils import check_filepath
from voxility_pro.utils.utils import abstract_method


class BaseVoxelOperator(bpy.types.Operator, ExportHelper):
    bl_description = "Base Voxel Operator"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ""  # You need to set this in your specific file format subclasses

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    )

    def draw(self, context):
        layout = self.layout

    @abstract_method
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
