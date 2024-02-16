import bpy
import os
import time
import bpy_types

from abc import ABC, abstractmethod

from voxility_pro.operators.voxel.operator_voxel_base import OperatorVoxelBase
from voxility_pro.translations import get_translation
from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.utils.object_utils import export_obj, check_mesh_exists
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxconvertCommandBuilder

class OperatorVoxelBaseExporter(OperatorVoxelBase):
    bl_description = "Operator Voxel Base Exporter"

    voxformat_scale: bpy.props.FloatProperty(
        name="Voxformat Scale",
        description="Scale the vertices on all axes by the given factor",
        default=1.0,
        min=0.0,
        max=100.0,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    palette_file: bpy.props.StringProperty(
        name="Palette File",
        description="Path to the palette file",
        default="",
        subtype='FILE_PATH',
    ) # type: ignore

    export_palette: bpy.props.BoolProperty(
        name="Export Palette",
        description="Save the included palette as png next to the source file",
        default=False,
    ) # type: ignore

    surface_only: bpy.props.BoolProperty(
        name="Surface Only",
        description="Remove any non surface voxel",
        default=False,
    ) # type: ignore

    def draw(self, context: bpy_types.Context) -> None:
        super().draw(context)
        self.layout.prop(self, "voxformat_scale")
        self.layout.prop(self, "palette_file")
        self.layout.prop(self, "export_palette")
        self.layout.prop(self, "surface_only")

    def export_obj(self, obj_file: str) -> str:
        start_time = time.time()
        export_obj(obj_file)
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_generated_files')} {obj_file} ({size}) in {duration}")
        return obj_file

    def setup_command(self, input: str, output: str) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = super().setup_command(input, output)
        c.vc_voxformat_withcolor = 0
        c.vc_voxformat_scale = float(self.voxformat_scale)
        c.vc_palette_file = str(self.palette_file)
        c.vc_export_palette = str(self.export_palette)
        c.vc_surface_only = int(self.surface_only)
        return c

    def execute(self, _:bpy_types.Context) -> set[str]:
        if not check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_no_mesh_object_selected')}")
            return {'CANCELLED'}

        self.filepath = check_filepath(self.filepath, self.filename_ext)
        temp_dir: str = TempFileManager().create_temp_dir()
        obj_file: str = os.path.join(temp_dir, 'temp.obj')
        self.export_obj(obj_file)
        self.setup_command(obj_file, self.filepath)
        self.execute_voxconvert()
        self.report({'INFO'}, f"{get_translation('info_vox_file_created')} {self.filepath} ({get_file_size(self.filepath)}) in {format_duration(self.voxconvert_duration)}")
        TempFileManager().delete_temp_dir(temp_dir)
        return {'FINISHED'}

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        #self.voxformat_scale = 1.0
        return super().invoke(context, event)