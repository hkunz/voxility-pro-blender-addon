import bpy
import os
import time
import bpy_types

from typing import List
from mathutils import Vector

from voxility_pro.operators.voxel.object_import_handlers.object_import_handler import ObjectImportHandler
from voxility_pro.operators.voxel.voxconvert_operator import VoxconvertOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.utils.object_utils import export_obj, import_obj, deselect_all_objects, duplicate_objects, select_objects, hide_objects_from_viewport
from voxility_pro.utils.file_utils import get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder

class OBJECT_OT_MeshVoxelConvertOperator(VoxconvertOperator):
    bl_idname = "object.voxility_mesh_voxel_convert"
    bl_label = "Voxility Pro Mesh-Voxel Convert "
    bl_description = "Voxelize or convert selected objects into a single voxel object"

    TARGET_FORMAT: str = None

    def create_temp_dup(self, objects: List[bpy_types.Object]) -> None:
        duplicate_objects(objects)
        bpy.ops.object.join()

    def export_obj(self, obj_file: str) -> str:
        start_time: float = time.time()
        export_obj(obj_file)
        duration: str = format_duration(time.time() - start_time)
        size: str = get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_generated_files')} {obj_file} ({size}) in {duration}")
        return obj_file

    def import_obj(self, obj_file: str) -> bool:
        deselect_all_objects()
        import_obj(obj_file)
        properties = bpy.context.scene.voxility_pro_properties
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

    def setup_command(self, input: str, output: str) -> VoxConvertCommandBuilder:
        c: VoxConvertCommandBuilder = super().setup_command(input, output)
        c.vc_voxformat_withcolor = 1
        properties = bpy.context.scene.voxility_pro_properties
        c.vc_voxformat_scale = float(properties.voxformat_scale)
        c.vc_surface_only = int(properties.surface_only)
        c.vc_voxformat_voxelizemode = int(properties.voxformat_voxelizemode)
        c.vc_voxformat_mergequads = int(properties.voxformat_mergequads)
        c.vc_merge_vertices = int(properties.merge_vertices)
        return c

    def execute(self, context: bpy_types.Context) -> set[str]:
        voxelize_duration: float = time.time()
        active_object: bpy_types.Object = context.view_layer.objects.active
        temp_dir: str = TempFileManager().create_temp_dir()
        vc_in_path: str = os.path.join(temp_dir, 'temp_in.obj')
        vc_out_path: str = os.path.join(temp_dir, 'temp_out.obj')
        objects: List[bpy_types.Object] = context.selected_objects.copy()
        self.create_temp_dup(objects)
        self.export_obj(vc_in_path)
        orig_width: float = context.object.dimensions[0]
        bpy.ops.object.delete(use_global=False)
        select_objects(objects, active_object)
        self.setup_command(vc_in_path, vc_out_path)
        success: bool = self.execute_voxconvert()

        if (success):
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {vc_out_path} ({get_file_size(vc_out_path)}) in {format_duration(self.voxconvert_duration)}")
        else:
            TempFileManager().delete_temp_dir(temp_dir)
            return {'CANCELLED'}

        start_time: float = time.time()
        self.import_obj(vc_out_path)
        self.set_scale(orig_width / context.object.dimensions[0])
        duration: str = format_duration(self.voxconvert_duration + (start_time - time.time()))
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {vc_out_path} in {duration}")
        self.report({'INFO'}, f"Voxelized in {format_duration(time.time() - voxelize_duration)}")
        properties = context.scene.voxility_pro_properties # FIXME: if type is specified as VoxilityProProperties it get circular error
        if properties.voxformat_withcolor:
            TempFileManager().delete_temp_dir(temp_dir)

        #FIXME: we need to delete the temporary directory even without vertex colors but we can't because the color palette is used as texture in the imported object
        #TempFileManager().delete_temp_dir(temp_dir)
        if properties.hide_original_objects:
            hide_objects_from_viewport(objects)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(OBJECT_OT_MeshVoxelConvertOperator)

def unregister() -> None:
    bpy.utils.unregister_class(OBJECT_OT_MeshVoxelConvertOperator)