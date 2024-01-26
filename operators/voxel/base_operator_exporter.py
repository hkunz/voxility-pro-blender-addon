import bpy
import os
import subprocess
import platform
import tempfile
import shutil
import time

from vox_exporter.operators.voxel.base_voxel_operator import BaseVoxelOperator
from vox_exporter.exceptions.command_execution_error import CommandExecutionError
from vox_exporter.translations import get_translation
from vox_exporter.utils.utils import export_obj, export_obj__deprecated
from vox_exporter.utils.file_utils import check_filepath, get_file_size
from vox_exporter.utils.time_utils import format_duration
from vox_exporter.voxconvert_command_builder import VoxConvertCommandBuilder


class BaseOperatorExporter(BaseVoxelOperator):
    bl_description = "Base Voxel Operator Exporter"

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

    voxformat_voxelizemode: bpy.props.BoolProperty(
        name="Voxformat Voxelize Mode",
        description="Check for faster and less memory (lower quality) or Uncheck for high quality (slower)",
        default=False,
    )

    def draw(self, context):
        super().draw(context)
        self.layout.prop(self, "voxformat_scale")
        self.layout.prop(self, "palette_file")
        self.layout.prop(self, "export_palette")
        self.layout.prop(self, "surface_only")
        self.layout.prop(self, "voxformat_voxelizemode")

    def export_obj(self, obj_file):
        start_time = time.time()
        try:
            export_obj__deprecated(obj_file)
        except Exception as e:
            export_obj(obj_file)

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
            obj_file,
            self.voxformat_scale,
            self.palette_file,
            self.export_palette,
            self.surface_only,
            int(self.voxformat_voxelizemode)
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
        self.voxformat_scale = 1.0
        return super().invoke(context, event)
