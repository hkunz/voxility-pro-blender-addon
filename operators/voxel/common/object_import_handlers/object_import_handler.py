import bpy

from voxility_pro.operators.voxel.common.object_import_handlers.object_import_fix_image_texture_handler import ObjectImportFixImageTextureHandler # type: ignore
from voxility_pro.operators.voxel.common.object_import_handlers.object_import_add_vertex_colors_handler import ObjectImportAddVertexColorsHandler # type: ignore
from voxility_pro.operators.voxel.common.object_import_handlers.object_import_merge_vertices_handler import ObjectImportMergeVerticesHandler # type: ignore
from voxility_pro.operators.voxel.common.object_import_handlers.object_import_limited_dissolve_handler import ObjectImportLimitedDissolveHandler # type: ignore
from voxility_pro.utils.string_utils import StringUtils # type: ignore
from voxility_pro.utils.object_utils import ObjectUtils # type: ignore

class ObjectImportHandler:
    IMPORTED_OBJ_BASE_NAME = "Voxility"

    def __init__(self, objects, merge_vertices, dissolve_limited, with_vertex_colors) -> None:
        self.objects = objects
        self.merge_vertices = merge_vertices
        self.dissolve_limited = dissolve_limited
        self.with_vertex_colors = with_vertex_colors

    def handle_object(self, obj) -> None:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if hasattr(obj.data, 'use_auto_smooth'):
            obj.data.use_auto_smooth = False # attribute does not exists in 4.1
        bpy.ops.object.shade_flat()
        ObjectUtils.apply_all_transforms(obj)
        suffix = StringUtils.randomize_string()
        obj.name = f"{ObjectImportHandler.IMPORTED_OBJ_BASE_NAME}_{suffix}"
        obj.data.name = f"{ObjectImportHandler.IMPORTED_OBJ_BASE_NAME}_{suffix}"
        obj.voxelized = True

        if self.with_vertex_colors:
            ObjectImportAddVertexColorsHandler(obj).execute_handler()
        else:
            ObjectImportFixImageTextureHandler(obj).execute_handler()

        if self.merge_vertices:
            ObjectImportMergeVerticesHandler(obj, self.with_vertex_colors).execute_handler()
        if self.dissolve_limited:
            ObjectImportLimitedDissolveHandler(obj).execute_handler()

    def on_object_import(self) -> None:
        for obj in bpy.context.scene.objects:
            obj.select_set(False)
        for obj in self.objects:
            if obj.type != 'MESH':
                continue
            self.handle_object(obj)