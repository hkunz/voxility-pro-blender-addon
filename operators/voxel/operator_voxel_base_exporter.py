import bpy
import os
import time
import bpy_types

from mathutils import Vector
from typing import List
from abc import ABC, abstractmethod

from voxility_pro.enums.voxility_feature import VoxilityFeature # type: ignore
from voxility_pro.operators.voxel.operator_voxel_base import OperatorVoxelBase # type: ignore
from voxility_pro.translation.translations import get_translation # type: ignore
from voxility_pro.utils.temp_file_manager import TempFileManager # type: ignore
from voxility_pro.utils.object_utils import export_obj, check_mesh_exists, get_voxelizer_voxel_size, get_mesh_center_distance, get_voxel_distance # type: ignore
from voxility_pro.utils.file_utils import check_filepath, get_file_size # type: ignore
from voxility_pro.utils.time_utils import format_duration # type: ignore
from voxility_pro.utils.voxel.voxel_color_reader import VoxelColorReader # type: ignore
from voxility_pro.utils.voxel.qb_writer import Qb, QbMatrix # type: ignore
from voxility_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder # type: ignore

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
        default="built-in:nippon",
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
        if VoxilityFeature.GN_VOXELIZER_ACTIVE.value:
            pass
        else:
            super().draw(context)
            self.layout.prop(self, "surface_only")
            self.layout.prop(self, "voxformat_scale")

    def export_qb_get_reader(self, obj: bpy.types.Object) -> VoxelColorReader:
        t = time.time()
        voxel_size = get_voxelizer_voxel_size(obj)
        reader = VoxelColorReader(obj, voxel_size, VoxelColorReader.LEFT_HANDED_COORDINATE_SYSTEM, VoxelColorReader.COLOR_SPACE_SRGB, "UVMap")
        duration = format_duration(time.time() - t)
        print(f"Qb {obj.name} Read Time: {duration}")
        self.report({'INFO'}, f"Reading voxel colors took {duration}")
        return reader

    def export_qb(self, context, qb_file: str) -> str:
        t = time.time()
        qb: Qb = Qb()
        active_obj = context.active_object
        reader = self.export_qb_get_reader(active_obj)
        axis, up_amt = reader.get_up_axis_amount()
        adjust = reader.get_object_center()
        qb.matrixList.append(QbMatrix(active_obj.name, *reader.get_voxel_dimensions(), reader.get_color_data(), reader.get_object_center(axis)))
        for obj in context.selected_objects:
            if obj is active_obj:
                continue
            r = self.export_qb_get_reader(obj)
            x, y, z = r.get_remapped_coordinates(*get_voxel_distance(get_mesh_center_distance(active_obj, obj), r.voxel_size))
            pos = (x+adjust[0], y+adjust[1] - (up_amt if axis == "y" else 0), z+adjust[2])
            qb.matrixList.append(QbMatrix(obj.name, *r.get_voxel_dimensions(), r.get_color_data(), pos))
        tt = time.time()
        qb.save(qb_file)
        if self.voxel_type != "qb":
            size = get_file_size(qb_file)
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {qb_file} ({size}) in {format_duration(time.time() - tt)}")
        print("Qb Write Time:", format_duration(time.time() - tt))
        print("Qb Total Time:", format_duration(time.time() - t))
        return qb_file

    def export_obj(self, obj_file: str) -> str:
        start_time = time.time()
        export_obj(obj_file)
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_generated_files')} {obj_file} ({size}) in {duration}")
        return obj_file

    def setup_command(self, input: str, outputs: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = super().setup_command(input, outputs)
        c.vc_voxformat_withcolor = 0
        c.vc_voxformat_scale = float(self.voxformat_scale)
        c.vc_palette_file = str(self.palette_file)
        c.vc_export_palette = self.export_palette
        c.vc_surface_only = int(self.surface_only)
        return c

    def execute(self, context: bpy_types.Context) -> set[str]:
        if not check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_no_mesh_object_selected')}")
            return {'CANCELLED'}

        duration: int = time.time()
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        temp_dir: str = TempFileManager().create_temp_dir()
        obj_file: str = None

        if VoxilityFeature.GN_VOXELIZER_ACTIVE.value:
            obj_file = os.path.join(temp_dir, 'temp.qb')
            self.export_qb(context, self.filepath if self.voxel_type == "qb" else obj_file)
        else:
            obj_file = os.path.join(temp_dir, 'temp.obj')
            self.export_obj(obj_file)

        if not VoxilityFeature.GN_VOXELIZER_ACTIVE.value or VoxilityFeature.GN_VOXELIZER_ACTIVE.value and self.voxel_type != "qb":
            self.setup_command(obj_file, [self.filepath])
            self.execute_voxconvert()

        duration = time.time() - duration
        self.report({'INFO'}, f"{get_translation('info_vox_file_created')} {self.filepath} ({get_file_size(self.filepath)}) in {format_duration(duration)}")
        TempFileManager().delete_temp_dir(temp_dir)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        active_object: bpy_types.Object = context.active_object
        if VoxilityFeature.GN_VOXELIZER_ACTIVE.value and get_voxelizer_voxel_size(active_object) <= 0:
            return False
        return super().poll(context)

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        #self.voxformat_scale = 1.0
        return super().invoke(context, event)