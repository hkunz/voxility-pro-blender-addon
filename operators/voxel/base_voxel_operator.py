import bpy
from bpy_extras.io_utils import ExportHelper

import bpy
import time
import shutil
import subprocess
import platform

from voxility_pro.translations import get_translation
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.utils.utils import abstract_method


class BaseVoxelOperator(bpy.types.Operator, ExportHelper):
    bl_description = "Base Voxel Operator"
    bl_options = {'REGISTER', 'UNDO'}
    voxility_type = ""
    voxconvert_duration = 0

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

    def execute_voxconvert(self, command, temp_dir):
        start_time = time.time()
        success = True
        command_str = ' '.join(command)
        self.report({'INFO'}, f"{get_translation('info_execute_command')} {command_str}")
        try:
            cmd = command if platform.system().lower() == "windows" else command_str
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            success = False
            print(f"Error: Command exited with return code {e.returncode}")
            print("Standard Error:\n", e.stderr)
            self.report({'ERROR'}, f"Error processing file: {self.filepath}")
        finally:
            if self.voxility_type == "exporter":
                shutil.rmtree(temp_dir)

        self.voxconvert_duration = time.time() - start_time
        return success

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