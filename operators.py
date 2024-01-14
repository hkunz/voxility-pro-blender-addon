import bpy
import os
import glob
import subprocess

from bpy_extras.io_utils import ExportHelper
from vox_exporter.translations import get_translation
from vox_exporter.utils import getvoxdir


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

        bpy.ops.export_scene.obj(
            filepath=obj_file,
            check_existing=True,
            axis_forward='-Z',
            axis_up='Y',
            filter_glob="*.obj;*.mtl",
            use_selection=True,
            use_animation=False,
            use_mesh_modifiers=True,
            use_edges=True,
            use_smooth_groups=False,
            use_smooth_groups_bitflags=False,
            use_normals=True,
            use_uvs=True,
            use_materials=True,
            use_triangles=False,
            use_nurbs=False,
            use_vertex_groups=False,
            use_blen_objects=True,
            group_by_object=False,
            group_by_material=False,
            keep_vertex_order=False,
            global_scale=1,
            path_mode='AUTO'
        )
        self.report({'INFO'}, get_translation('info_generated_files') + ' ' + obj_file)
        return obj_file

    def check_filepath(self):
        if os.path.isdir(self.filepath):
            self.filepath = os.path.join(self.filepath, "untitled.vox")
        elif not self.filepath or os.path.isdir(self.filepath):
            self.filepath = os.path.join(bpy.path.abspath("//"), "untitled.vox")


    def execute(self, context):

        voxdir = getvoxdir()
        temp_dir = os.path.join(voxdir, "temp")
        obj_name = 'temp.obj'

        palette_file = self.palette_file if self.palette_file else "palette-nippon.png"
        self.check_filepath()

        matching_files = glob.glob(os.path.join(voxdir, "*vox*.exe"))

        assert len(matching_files) != 0, get_translation('error_no_converter_exe')

        exe = matching_files[0]

        #Usage: https://vengi-voxel.github.io/vengi/voxconvert/Usage/
        command = [
            os.path.join(voxdir, exe),
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