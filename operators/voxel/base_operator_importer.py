import bpy
import os
import subprocess
import platform
import tempfile
import shutil
import time

from bpy_extras.io_utils import ExportHelper

from vox_exporter.exceptions.command_execution_error import CommandExecutionError
from vox_exporter.translations import get_translation
from vox_exporter.utils.file_utils import check_filepath, get_file_size
from vox_exporter.utils.time_utils import format_duration
from vox_exporter.voxconvert_command_builder import VoxConvertCommandBuilder


class BaseOperatorImporter(bpy.types.Operator, ExportHelper):
    bl_description = "Base Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ""  # You need to set this in your specific file format subclasses

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "voxformat_scale")
        layout.prop(self, "palette_file")
        layout.prop(self, "export_palette")
        layout.prop(self, "surface_only")
        layout.prop(self, "voxformat_voxelizemode")

    def import_obj(self, obj_file):
        start_time = time.time()
        #import_obj__(obj_file) #TODO import logic
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, get_translation('info_generated_files') + f" {obj_file} ({size}) in {duration}")
        return obj_file

    def execute(self, context):

        start_time = time.time()
        self.filepath = check_filepath(self.filepath, self.filename_ext)

        temp_dir = tempfile.mkdtemp()
        obj_file = os.path.join(temp_dir, 'temp.obj')

        self.export_obj(obj_file)

        command_builder = VoxConvertCommandBuilder(
            self.filepath,
            obj_file
        )
        command = command_builder.build_command()
        command_str = ' '.join(command)
        self.report({'INFO'}, get_translation('info_execute_command') + ' ' + command_str)

        try:
            cmd = command if platform.system().lower() == "windows" else command_str
            #process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            size = get_file_size(self.filepath)
            duration = format_duration(time.time() - start_time)
            self.report({'INFO'}, get_translation('info_vox_file_created') + f"{self.filepath} ({size}) in {duration}")
        except subprocess.CalledProcessError as e:
            print(f"Error: Command exited with return code {e.returncode}")
            print("Standard Output:\n", e.stdout)
            print("Standard Error:\n", e.stderr)
            raise CommandExecutionError(e.returncode, e.stdout, e.stderr)
        finally:
            shutil.rmtree(temp_dir)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
