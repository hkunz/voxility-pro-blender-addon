import bpy
import os
import glob
import subprocess

from bpy_extras.io_utils import ExportHelper
from vox_exporter.translations import get_translation
from vox_exporter.utils import get_addon_root_dir


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

        bpy.ops.wm.obj_export(
            filepath=obj_file,
            check_existing=True,
            filter_blender=False,
            filter_backup=False,
            filter_image=False,
            filter_movie=False,
            filter_python=False,
            filter_font=False,
            filter_sound=False,
            filter_text=False,
            filter_archive=False,
            filter_btx=False,
            filter_collada=False,
            filter_alembic=False,
            filter_usd=False,
            filter_obj=False,
            filter_volume=False,
            filter_folder=True,
            filter_blenlib=False,
            filemode=8,
            display_type='DEFAULT',
            sort_method='DEFAULT',
            export_animation=False,
            start_frame=-2147483648,
            end_frame=2147483647,
            forward_axis='NEGATIVE_Z',
            up_axis='Y',
            global_scale=1.0,
            apply_modifiers=True,
            export_eval_mode='DAG_EVAL_VIEWPORT',
            export_selected_objects=True,
            export_uv=True,
            export_normals=True,
            export_colors=False,
            export_materials=True,
            export_pbr_extensions=False,
            path_mode='AUTO',
            export_triangulated_mesh=False,
            export_curves_as_nurbs=False,
            export_object_groups=False,
            export_material_groups=False,
            export_vertex_groups=False,
            export_smooth_groups=False,
            smooth_group_bitflags=False,
            filter_glob='*.obj;*.mtl'
        )

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

        matching_files = glob.glob(os.path.join(addon_root, "*vox*.exe"))

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
        subprocess.run(command, shell=True)
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
