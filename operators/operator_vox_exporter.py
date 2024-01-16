import bpy
import os
import glob
import subprocess
import platform

from bpy_extras.io_utils import ExportHelper
from vox_exporter.translations import get_translation
from vox_exporter.utils import get_addon_root_dir, export_obj, export_obj__deprecated


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

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "palette_file")
        layout.prop(self, "export_palette")
        layout.prop(self, "surface_only")

    def export_obj(self, directory, obj_name):

        os.makedirs(directory, exist_ok=True)
        obj_file = os.path.join(directory, obj_name)

        try:
            export_obj__deprecated(obj_file)
        except Exception as e:
            export_obj(obj_file)

        self.report({'INFO'}, get_translation('info_generated_files') + ' ' + obj_file)
        return obj_file

    def check_filepath(self):
        if os.path.isdir(self.filepath):
            self.filepath = os.path.join(self.filepath, "untitled.vox")
        elif not self.filepath or os.path.isdir(self.filepath):
            self.filepath = os.path.join(bpy.path.abspath("//"), "untitled.vox")


    def execute(self, context):

        #bpy.ops.wm.modal_timer_operator()

        addon_root = get_addon_root_dir()
        temp_dir = os.path.join(addon_root, "temp")
        obj_name = 'temp.obj'

        palette_file = self.palette_file if self.palette_file else "palette-nippon.png"
        self.check_filepath()

        system = platform.system().lower()
        voxconvert_version = ""
        exe_base_dir = "executable"
        exe_base_name = "voxconvert"
        matching_files = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", system, f"*{exe_base_name}*"))

        assert len(matching_files) != 0, get_translation('error_no_converter_exe')

        exe = matching_files[0]

        #Usage: https://vengi-voxel.github.io/vengi/voxconvert/Usage/
        command = [
            os.path.join(addon_root, exe),
            "-set", f"palette {palette_file}",
            "--export-palette" if self.export_palette else " ",
            "--surface_only" if self.surface_only else " ",
            "--input", self.export_obj(temp_dir, obj_name),
            "--output", self.filepath,
            "--force"
        ]

        self.report({'INFO'}, get_translation('info_execute_command') + ' ' + ', '.join(command))
        #subprocess.run(command, shell=True)
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

        output, error = process.communicate()

        if process.returncode != 0:
            print(f"Error: {error.decode('utf-8')}")

        self.report({'INFO'}, get_translation('info_vox_file_created') + self.filepath)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.check_filepath()
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
