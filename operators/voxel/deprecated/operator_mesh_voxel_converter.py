import bpy
import time

from os import path as p
from typing import List
from mathutils import Vector

from voxelity_pro.operators.voxel.operator_voxconvert import OperatorVoxconvert
from voxelity_pro.operators.voxel.deprecated.operator_mesh_voxel_save import OBJECT_OT_MeshVoxelSaveOperator
from voxelity_pro.operators.voxel.common.object_import_handlers.object_import_handler import ObjectImportHandler
from voxelity_pro.translation.translations import get_translation
from voxelity_pro.utils.temp_file_manager import TempFileManager
from voxelity_pro.utils.object_utils import ObjectUtils
from voxelity_pro.utils.file_utils import FileUtils
from voxelity_pro.utils.time_utils import TimeUtils
from voxelity_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxelity_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu

class OBJECT_OT_MeshVoxelConvertOperator(OperatorVoxconvert):
    bl_idname = "object.voxelity_mesh_voxel_convert"
    bl_label = "Voxelity Pro Mesh-Voxel Convert"
    bl_description = "Voxelize or convert selected objects into a single voxel object"

    TEMP_DIR: str = None
    TARGET_FORMAT: str = None

    vox_target_format_ext: bpy.props.StringProperty(
        name="Target Voxel Format Extension",
        default=VoxelFormatsExportMenu.SELECTION_NONE
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    def create_temp_dup(self, objects: List[bpy_types.Object]) -> None:
        ObjectUtils.duplicate_objects(objects)
        bpy.ops.object.join()

    def export_obj(self, obj_file: str) -> str:
        start_time: float = time.time()
        ObjectUtils.export_obj(obj_file)
        duration: str = TimeUtils.format_duration(time.time() - start_time)
        size: str = FileUtils.get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_generated_files')} {obj_file} ({size}) in {duration}")
        return obj_file

    def import_obj(self, obj_file: str) -> bool:
        ObjectUtils.deselect_all_objects()
        ObjectUtils.import_obj(obj_file)
        properties = bpy.context.scene.voxelity_pro_properties
        ObjectImportHandler(
            objects = bpy.context.selected_objects,
            merge_vertices = properties.merge_vertices,
            dissolve_limited = properties.option_dissolve_limited,
            with_vertex_colors = properties.voxformat_withcolor
        ).on_object_import()
        return True

    def set_scale(self, scale: float) -> None:
        bpy.context.object.scale = Vector((scale, scale, scale))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    def setup_command(self, input: str, outputs: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = super().setup_command(input, outputs)
        c.vc_voxformat_withcolor = 1
        properties = bpy.context.scene.voxelity_pro_properties
        c.vc_voxformat_scale = float(properties.voxformat_scale)
        c.vc_surface_only = int(properties.surface_only)
        c.vc_voxformat_voxelizemode = int(properties.voxformat_voxelizemode)
        c.vc_voxformat_mergequads = int(properties.voxformat_mergequads)
        c.vc_merge_vertices = int(properties.merge_vertices)
        return c

    def generate_output_paths(self, temp_dir: str) -> List[str]:
        paths = [p.join(temp_dir, 'temp_out.obj')]
        type: str = self.vox_target_format_ext.lower()
        if type == VoxelFormatsExportMenu.SELECTION_NONE.lower():
            return paths
        type_dir = p.join(temp_dir, type)
        TempFileManager().create_directory(type_dir)
        paths.append(p.join(type_dir, f'temp_out.{type}'))
        return paths

    def execute(self, context: bpy.types.Context) -> set[str]:
        voxelize_duration: float = time.time()
        OBJECT_OT_MeshVoxelSaveOperator.VOX_TARGET_FORMAT_EXT = VoxelFormatsExportMenu.SELECTION_NONE
        active_object: bpy_types.Object = context.view_layer.objects.active
        if OBJECT_OT_MeshVoxelConvertOperator.TEMP_DIR is None or not p.exists(OBJECT_OT_MeshVoxelConvertOperator.TEMP_DIR):
            OBJECT_OT_MeshVoxelConvertOperator.TEMP_DIR = TempFileManager().create_temp_dir()
        temp_dir: str = OBJECT_OT_MeshVoxelConvertOperator.TEMP_DIR
        vc_in_path: str = p.join(temp_dir, 'temp_in.obj')
        objects: List[bpy_types.Object] = context.selected_objects.copy()
        self.create_temp_dup(objects)
        self.export_obj(vc_in_path)
        orig_width: float = context.object.dimensions[0]
        bpy.ops.object.delete(use_global=False)
        ObjectUtils.select_objects(objects, active_object)
        vc_out_paths = self.generate_output_paths(temp_dir)
        self.setup_command(vc_in_path, vc_out_paths)
        print("Target Voxel Format:", self.vox_target_format_ext)
        success: bool = self.execute_voxconvert()

        if (success):
            for out_path in vc_out_paths:
                self.report({'INFO'}, f"{get_translation('info_generated_files')} {out_path} ({FileUtils.get_file_size(out_path)}) in {TimeUtils.format_duration(self.voxconvert_duration)}")
        else:
            return {'CANCELLED'}

        start_time: float = time.time()
        obj_path: str = vc_out_paths[0]
        self.import_obj(obj_path)
        #FIXME: should not need to scale it https://github.com/vengi-voxel/vengi/issues/401
        self.set_scale(orig_width / context.object.dimensions[0])
        duration: str = TimeUtils.format_duration(self.voxconvert_duration + (start_time - time.time()))
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {obj_path} in {duration}")
        self.report({'INFO'}, f"Voxelized in {TimeUtils.format_duration(time.time() - voxelize_duration)}")
        properties = context.scene.voxelity_pro_properties # FIXME: if type is specified as VoxelityProProperties it get circular error

        if properties.hide_original_objects:
            ObjectUtils.hide_objects_from_viewport(objects)

        OBJECT_OT_MeshVoxelSaveOperator.VOX_TARGET_FORMAT_EXT = self.vox_target_format_ext
        OBJECT_OT_MeshVoxelSaveOperator.VOX_OUTPUT_PATH = vc_out_paths[1] if len(vc_out_paths) > 1 else None
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(OBJECT_OT_MeshVoxelConvertOperator)

def unregister() -> None:
    bpy.utils.unregister_class(OBJECT_OT_MeshVoxelConvertOperator)