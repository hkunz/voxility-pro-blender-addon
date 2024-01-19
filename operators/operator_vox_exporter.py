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
from vox_exporter.utils import export_obj, export_obj__deprecated, check_filepath, format_duration
from vox_exporter.voxconvert_command_builder import VoxConvertCommandBuilder


class EXPORT_OT_magica_voxel(bpy.types.Operator, ExportHelper):
    bl_idname = "export.magica_voxel"
    bl_label = "MagicaVoxel (.vox)"
    bl_description = "Export selected objects to MagicaVoxel format (.vox)"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".vox"

    filter_glob: bpy.props.StringProperty(
        default="*.vox",
        options={'HIDDEN'},
        maxlen=255,
    )

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
        layout = self.layout
        layout.prop(self, "voxformat_scale")
        layout.prop(self, "palette_file")
        layout.prop(self, "export_palette")
        layout.prop(self, "surface_only")
        layout.prop(self, "voxformat_voxelizemode")

    def export_obj(self, obj_file):
        start_time = time.time()
        try:
            export_obj__deprecated(obj_file)
        except Exception as e:
            export_obj(obj_file)

        duration = format_duration(time.time() - start_time)
        self.report({'INFO'}, get_translation('info_generated_files') + f" {obj_file} in {duration}")
        return obj_file

    def execute(self, context):

        #bpy.ops.wm.modal_timer_operator()
        start_time = time.time()
        self.filepath = check_filepath(self.filepath)

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
            duration = format_duration(time.time() - start_time)
            self.report({'INFO'}, get_translation('info_vox_file_created') + f"{self.filepath} in {duration}")
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
        self.filepath = check_filepath(self.filepath)
        self.voxformat_scale = 1.0
        return {'RUNNING_MODAL'}


def on_file_export_vox_click(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(EXPORT_OT_magica_voxel.bl_idname, text="MagicaVoxel (.vox)")

def register_vox_exporter():
    bpy.utils.register_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.append(on_file_export_vox_click)

def unregister_vox_exporter():
    bpy.utils.unregister_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.remove(on_file_export_vox_click)


'''
import threading

def export_in_thread():
    # This function will be called in a separate thread
    bpy.ops.export.magica_voxel('INVOKE_DEFAULT')

def on_file_export_vox_click(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'

    # Create a new thread for the export operation
    export_thread = threading.Thread(target=export_in_thread)

    # Start the thread
    export_thread.start()

def register_vox_exporter():
    bpy.utils.register_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.append(on_file_export_vox_click)

def unregister_vox_exporter():
    bpy.utils.unregister_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.remove(on_file_export_vox_click)
'''
