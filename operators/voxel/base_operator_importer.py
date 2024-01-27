import bpy
import time
import tempfile
import shutil
import os

from voxility_pro.operators.voxel.base_voxel_operator import BaseVoxelOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.utils import import_obj, import_obj__deprecated
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder


class BaseOperatorImporter(BaseVoxelOperator):
    bl_description = "Base Voxel Operator Importer"
    voxility_type = "importer"

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
        try:
            import_obj__deprecated(obj_file)
        except Exception as e:
            import_obj(obj_file)

        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, get_translation('info_imported_file') + f" {obj_file} ({size}) in {duration}")

    def execute(self, context):
        start_time = time.time()
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        temp_dir = tempfile.mkdtemp()
        output_obj_filepath = os.path.join(temp_dir, 'temp.obj')

        command_builder = VoxConvertCommandBuilder(
            self.filepath,
            output_obj_filepath
        )
        command = command_builder.build_command()

        self.execute_voxconvert(command, output_obj_filepath, start_time, get_translation('info_generated_files'), temp_dir)
        self.import_obj(output_obj_filepath)
        self.report({'INFO'}, get_translation('info_vox_data_imported') + f" {self.filepath}")

        shutil.rmtree(temp_dir)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
