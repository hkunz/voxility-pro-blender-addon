import bpy
from bpy_extras.io_utils import ExportHelper

import bpy
import time
import shutil
import subprocess
import platform

from voxility_pro.exceptions.command_execution_error import CommandExecutionError
from voxility_pro.translations import get_translation
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.utils.utils import abstract_method


class BaseVoxelOperator(bpy.types.Operator, ExportHelper):
    bl_description = "Base Voxel Operator"
    bl_options = {'REGISTER', 'UNDO'}
    voxility_type = ""

    filename_ext = ""  # You need to set this in your specific file format subclasses
    command_builder = None

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    )

    voxformat_voxelizemode: bpy.props.BoolProperty(
        name="Voxformat Voxelize Mode",
        description="Check for faster and less memory (lower quality) or Uncheck for high quality (slower)",
        default=False,
    )

    def execute_voxconvert(self, command, output, start_time, complete_msg, temp_dir):
        command_str = ' '.join(command)
        self.report({'INFO'}, get_translation('info_execute_command') + ' ' + command_str)

        try:
            cmd = command if platform.system().lower() == "windows" else command_str
            #process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            size = get_file_size(output)
            duration = format_duration(time.time() - start_time)
            self.report({'INFO'}, f"{complete_msg} {output} ({size}) in {duration}")
        except subprocess.CalledProcessError as e:
            if self.voxility_type == "importer":
                shutil.rmtree(temp_dir)
            print(f"Error: Command exited with return code {e.returncode}")
            print("Standard Output:\n", e.stdout)
            print("Standard Error:\n", e.stderr)
            self.report({'ERROR'}, f"voxconvert error: {e.stderr}{self.filepath}")
            #raise CommandExecutionError(e.returncode, e.stdout, e.stderr)
        finally:
            if self.voxility_type == "exporter":
                shutil.rmtree(temp_dir)

    def draw(self, context):
        self.layout.prop(self, "voxformat_voxelizemode")

    @abstract_method
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
