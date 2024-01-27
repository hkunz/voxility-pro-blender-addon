import bpy
import os
import tempfile
import time

from voxility_pro.operators.voxel.base_voxel_operator import BaseVoxelOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.utils import export_obj, export_obj__deprecated
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder


class BaseOperatorExporter(BaseVoxelOperator):
    bl_description = "Base Voxel Operator Exporter"
    voxility_type = "exporter"

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

    def draw(self, context):
        super().draw(context)
        self.layout.prop(self, "voxformat_scale")
        self.layout.prop(self, "palette_file")
        self.layout.prop(self, "export_palette")
        self.layout.prop(self, "surface_only")

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
            obj_file,
            self.filepath,
            int(self.voxformat_voxelizemode),
            self.voxformat_scale,
            self.palette_file if self.palette_file else "palette-nippon.png",
            self.export_palette,
            self.surface_only
        )
        command = command_builder.build_command()
        self.execute_voxconvert(command, self.filepath, start_time, get_translation('info_vox_file_created'), temp_dir)

        return {'FINISHED'}

    def invoke(self, context, event):
        self.voxformat_scale = 1.0
        return super().invoke(context, event)
