import bpy
import time

from vox_exporter.operators.voxel.base_voxel_operator import BaseVoxelOperator
from vox_exporter.exceptions.command_execution_error import CommandExecutionError
from vox_exporter.translations import get_translation
from vox_exporter.utils.file_utils import check_filepath, get_file_size
from vox_exporter.utils.time_utils import format_duration
from vox_exporter.voxconvert_command_builder import VoxConvertCommandBuilder


class BaseOperatorImporter(BaseVoxelOperator):
    bl_description = "Base Voxel Operator Importer"

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    )

    def draw(self, context):
        super().draw(context)
        layout = self.layout

    def import_obj(self, obj_file):
        start_time = time.time()
        #import_obj__(obj_file) #TODO import logic
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, get_translation('info_generated_files') + f" {obj_file} ({size}) in {duration}")
        return obj_file

    def execute(self, context):
        print("TODO") #TODO
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
