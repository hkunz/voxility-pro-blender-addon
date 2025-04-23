import bpy
import os
import time

from mathutils import Vector
from typing import List
from abc import ABC, abstractmethod

from voxelity_pro.enums.voxelity_feature import VoxelityFeature
from voxelity_pro.operators.voxel.operator_voxel_base import OperatorVoxelBase
from voxelity_pro.translation.translations import get_translation
from voxelity_pro.utils.temp_file_manager import TempFileManager
from voxelity_pro.utils.object_utils import ObjectUtils
from voxelity_pro.utils.voxel.voxel_utils import VoxelUtils
from voxelity_pro.utils.file_utils import FileUtils
from voxelity_pro.utils.number_utils import NumberUtils
from voxelity_pro.utils.time_utils import TimeUtils
from voxelity_pro.utils.voxel.voxel_color_reader import VoxelColorReader
from voxelity_pro.utils.voxel.qb_writer import Qb, QbMatrix
from voxelity_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxelity_pro.operators.operator_generic_popup import create_generic_popup

class OperatorVoxelBaseExporter(OperatorVoxelBase):
    bl_idname = "export.voxelity_export"
    bl_label = "Export"
    bl_description = "Operator Voxel Base Exporter"

    SUPPORTED_INPUT_MESH_FORMATS=[
        ("OBJ", "obj (Wavefront Object)"),
        ("FBX", "fbx (Autodesk Filmbox)"),
        ("GLTF", "gltf (GL Transmission Format)"),
        ("PLY", "ply (Polygon File Format)"),
        ("BSP", "bsp (Quake 1)"),
        ("MD2", "md2 (Quake 2 Model)"),
        ("STL", "stl (Standard Triangle Language)"),
        ("BSP", "bsp (UFO:Alien Invasion)")
    ]

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

    voxformat_fillhollow: bpy.props.BoolProperty(
        name="Fill Hollow",
        description=("Fill the inner parts of completely close objects"),
        default=False,
    ) # type: ignore

    def draw(self, context: bpy.types.Context) -> None:
        super().draw(context)
        col = self.options_panel
        sub = col.row()
        super().draw_elements(context)
        if VoxelityFeature.GN_VOXELIZER_ACTIVE.value:
            if self.voxel_type == "qb":
                self.surface_only = True
                sub.enabled = False
            else:
                sub.enabled = True
            sub.prop(self, "surface_only") # surface_only=False will not work because we export QB surface voxels only, need fill option
            self.draw_file_conversion_options(context, col)
        else:
            col.prop(self, "surface_only")
            col.prop(self, "voxformat_scale")

    def draw_file_conversion_options(self, context, col):
        if context.selected_objects:
            return
        props = context.scene.voxelity_pro_properties
        ext = FileUtils.get_file_extension(props.file_to_convert_path)
        if self.is_object_format(ext):
            col.prop(self, "voxformat_scale")

    def is_object_format(self, ext) -> bool:
        return ext == "obj"

    def export_qb_get_reader(self, obj: bpy.types.Object) -> VoxelColorReader:
        t = time.time()
        voxel_size, uvmap, color = VoxelUtils.get_voxelizer_voxel_modifier_attributes(obj)
        reader = VoxelColorReader(obj, voxel_size, VoxelColorReader.LEFT_HANDED_COORDINATE_SYSTEM, VoxelColorReader.COLOR_SPACE_LINEAR, uvmap)
        duration = TimeUtils.format_duration(time.time() - t)
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
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {qb_file} ({size}) in {TimeUtils.format_duration(time.time() - tt)}")
        print("Qb Write Time:", TimeUtils.format_duration(time.time() - tt))
        print("Qb Total Time:", TimeUtils.format_duration(time.time() - t))
        return qb_file

    def export_obj(self, obj_file: str) -> str:
        start_time = time.time()
        ObjectUtils.export_obj(obj_file)
        duration = TimeUtils.format_duration(time.time() - start_time)
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
        c.vc_fillhollow = int(not self.surface_only)
        c.vc_script = "fillhollow" if not self.surface_only else None
        return c

    def check_valid_file_path_conversion(self, context, ext):
        if any(ext.upper() in format_tuple[0] for format_tuple in self.SUPPORTED_INPUT_MESH_FORMATS):
            return True
        for i, tuple in enumerate(context.scene.voxelity_pro_properties.IMPORT_FORMATS):
            if i <= 0:
                continue
            if ext == tuple[0].lower():
                return True
        return False

    def create_success_popup(self, header, duration):
        size = FileUtils.get_file_size(self.filepath)
        fduration = TimeUtils.format_duration(duration)
        self.report({'INFO'}, f"{get_translation('info_vox_file_created')} {self.filepath} ({size}) in {fduration}")
        create_generic_popup(message=f"{header},,INFO|Directory: {os.path.dirname(self.filepath)},,TRIA_RIGHT|Size: {size},,TRIA_RIGHT|Duration: {fduration},,TRIA_RIGHT|Check the Info Editor for more information.,,TRIA_RIGHT")

    def create_error_popup(self, header, duration):
        size = FileUtils.get_file_size(self.filepath)
        fduration = TimeUtils.format_duration(duration)
        self.report({'ERROR'}, f"Error creating {self.filepath} ({size}) in {fduration}")
        create_generic_popup(message=f"{header},,CANCEL,,1|Directory: {os.path.dirname(self.filepath)},,TRIA_RIGHT|Duration: {fduration},,TRIA_RIGHT|Check the Info Editor for more information.,,TRIA_RIGHT")

    def execute_file_path_conversion(self, context):
        start: int = time.time()
        props = context.scene.voxelity_pro_properties
        self.filepath = FileUtils.check_filepath(self.filepath, self.filename_ext)
        self.setup_command(props.file_to_convert_path, [self.filepath])
        success = self.execute_voxconvert()
        if success:
            self.create_success_popup(f"Input file converted to '{os.path.basename(self.filepath)}'", time.time() - start)
        else:
            self.create_error_popup(f"File conversion failed", time.time() - start)

    def execute(self, context: bpy.types.Context) -> set[str]:
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
        success = True

        if VoxelityFeature.GN_VOXELIZER_ACTIVE.value:
            obj_file = os.path.join(temp_dir, 'temp.qb')
            self.export_qb(context, self.filepath if self.voxel_type == "qb" else obj_file)
        else:
            obj_file = os.path.join(temp_dir, 'temp.obj')
            self.export_obj(obj_file)

        if not VoxelityFeature.GN_VOXELIZER_ACTIVE.value or VoxelityFeature.GN_VOXELIZER_ACTIVE.value and self.voxel_type != "qb":
            self.setup_command(obj_file, [self.filepath])
            success = self.execute_voxconvert()

        TempFileManager().delete_temp_dir(temp_dir)
        if success:
            self.create_success_popup(f"Export to '{os.path.basename(self.filepath)}' successful", time.time() - duration)
        else:
            self.create_error_popup(f"Export to '{os.path.basename(self.filepath)}' failed", time.time() - duration)
        return {'FINISHED'}

    @classmethod
    def is_file_path_conversion(cls, context):
        props = context.scene.voxelity_pro_properties
        return not context.selected_objects and os.path.isfile(props.file_to_convert_path) and props.export_format != props.SELECTION_NONE

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        active_object: bpy_types.Object = context.active_object
        if cls.is_file_path_conversion(context):
            return True
        if not cls.filename_ext or not active_object:
            return False
        if VoxelityFeature.GN_VOXELIZER_ACTIVE.value:
            for obj in context.selected_objects:
                if NumberUtils.is_almost_equal(VoxelUtils.get_voxelizer_voxel_size(obj), 0) and not obj.voxelized:
                    return False
        return super().poll(context)

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        if self.is_file_path_conversion(context):
            props = context.scene.voxelity_pro_properties
            ext = FileUtils.get_file_extension(props.file_to_convert_path)
            if props.export_format.lower() == ext:
                create_generic_popup(message=f"ERROR: cannot convert same format '{ext}' to '{ext}'")
                return {'PASS_THROUGH'}
            if self.check_valid_file_path_conversion(context, ext):
                return super().invoke(context, event)
            create_generic_popup(message="ERROR: ." + ext + " unsupported. Supported formats include:|" + '|'.join(t[1] for i, t in enumerate(context.scene.voxelity_pro_properties.IMPORT_FORMATS) if i > 0) + '|' + '|'.join(t[1] for i, t in enumerate(self.SUPPORTED_INPUT_MESH_FORMATS)))
            return {'PASS_THROUGH'}
        return super().invoke(context, event)