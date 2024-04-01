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
from voxility_pro.utils.object_utils import ObjectUtils # type: ignore
from voxility_pro.utils.voxel.voxel_utils import VoxelUtils # type: ignore
from voxility_pro.utils.file_utils import FileUtils # type: ignore
from voxility_pro.utils.number_utils import is_almost_equal # type: ignore
from voxility_pro.utils.time_utils import format_duration # type: ignore
from voxility_pro.utils.voxel.voxel_color_reader import VoxelColorReader # type: ignore
from voxility_pro.utils.voxel.qb_writer import Qb, QbMatrix # type: ignore
from voxility_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder # type: ignore
from voxility_pro.operators.operator_generic_popup import create_generic_popup # type: ignore

class OperatorVoxelBaseExporter(OperatorVoxelBase):
    bl_idname = "export.voxility_export"
    bl_label = "Export"
    bl_description = "Operator Voxel Base Exporter"

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    voxformat_scale: bpy.props.FloatProperty(
        name="Voxformat Scale",
        description="Scale the vertices on all axes by the given factor",
        default=1.0,
        min=0.0,
        max=100.0,
    ) # type: ignore

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
        voxel_size, uvmap, color = VoxelUtils.get_voxelizer_voxel_modifier_attributes(obj)
        reader = VoxelColorReader(obj, voxel_size, VoxelColorReader.LEFT_HANDED_COORDINATE_SYSTEM, VoxelColorReader.COLOR_SPACE_SRGB, uvmap)
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
        qb.matrixList.append(QbMatrix(active_obj.name, *reader.get_voxel_dimensions(), reader.get_color_data(), reader.get_object_center(axis)))
        for obj in context.selected_objects:
            if obj is active_obj:
                continue
            r = self.export_qb_get_reader(obj)
            c = r.get_object_center()
            x, y, z = r.get_remapped_coordinates(*VoxelUtils.get_mesh_center_voxel_distance(active_obj, obj, r.voxel_size))
            pos = (x+c[0], y+c[1] - (up_amt if axis == "y" else 0), z+c[2])
            qb.matrixList.append(QbMatrix(obj.name, *r.get_voxel_dimensions(), r.get_color_data(), pos))
        tt = time.time()
        qb.save(qb_file)
        if self.voxel_type != "qb":
            size = FileUtils.get_file_size(qb_file)
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {qb_file} ({size}) in {format_duration(time.time() - tt)}")
        print("Qb Write Time:", format_duration(time.time() - tt))
        print("Qb Total Time:", format_duration(time.time() - t))
        return qb_file

    def export_obj(self, obj_file: str) -> str:
        start_time = time.time()
        ObjectUtils.export_obj(obj_file)
        duration = format_duration(time.time() - start_time)
        size = FileUtils.get_file_size(obj_file)
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

    def check_valid_file_path_conversion(self, context, ext):
        for i, tuple in enumerate(context.scene.voxility_pro_properties.IMPORT_FORMATS):
            if i <= 0:
                continue
            if ext == tuple[0].lower():
                return True
        return False

    def create_success_popup(self, header, duration):
        size = FileUtils.get_file_size(self.filepath)
        fduration = format_duration(duration)
        self.report({'INFO'}, f"{get_translation('info_vox_file_created')} {self.filepath} ({size}) in {fduration}")
        create_generic_popup(message=f"{header}|Created: {self.filepath}|Size: {size}|Duration: {fduration}|Check the Info Editor for more information.")

    def execute_file_path_conversion(self, context):
        start: int = time.time()
        props = context.scene.voxility_pro_properties
        self.filepath = FileUtils.check_filepath(self.filepath, self.filename_ext)
        self.setup_command(props.file_to_convert_path, [self.filepath])
        self.execute_voxconvert()
        self.create_success_popup(f"Input file converted to '{self.filename_ext}'", time.time() - start)

    def execute(self, context: bpy_types.Context) -> set[str]:
        if self.is_file_path_conversion(context):
            self.execute_file_path_conversion(context)
            return {'FINISHED'}

        if not ObjectUtils.check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_no_mesh_object_selected')}")
            return {'CANCELLED'}

        duration: int = time.time()
        self.filepath = FileUtils.check_filepath(self.filepath, self.filename_ext)
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

        TempFileManager().delete_temp_dir(temp_dir)
        self.create_success_popup(f"Export to '{self.filename_ext}' successful", time.time() - duration)
        return {'FINISHED'}

    @classmethod
    def is_file_path_conversion(cls, context):
        props = context.scene.voxility_pro_properties
        return not context.selected_objects and os.path.isfile(props.file_to_convert_path) and props.export_format != props.SELECTION_NONE

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        active_object: bpy_types.Object = context.active_object
        if cls.is_file_path_conversion(context):
            return True
        if not cls.filename_ext or not active_object:
            return False
        if VoxilityFeature.GN_VOXELIZER_ACTIVE.value:
            for obj in context.selected_objects:
                if is_almost_equal(VoxelUtils.get_voxelizer_voxel_size(obj), 0) and not obj.voxelized:
                    return False
        return super().poll(context)

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        if self.is_file_path_conversion(context):
            props = context.scene.voxility_pro_properties
            ext = os.path.splitext(props.file_to_convert_path)[1][1:]
            if props.export_format.lower() == ext:
                create_generic_popup(message=f"ERROR: cannot convert same format '{ext}' to '{ext}'")
                return {'PASS_THROUGH'}
            if self.check_valid_file_path_conversion(context, ext):
                return super().invoke(context, event)
            create_generic_popup(message="ERROR: ." + ext + " unsupported. Supported formats include:|" + '|'.join(t[1] for i, t in enumerate(context.scene.voxility_pro_properties.IMPORT_FORMATS) if i > 0))
            return {'PASS_THROUGH'}
        return super().invoke(context, event)