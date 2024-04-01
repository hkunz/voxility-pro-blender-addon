import bpy

from typing import Tuple

from voxility_pro.operators.common.handler_interface import IHandler # type: ignore
from voxility_pro.utils.object_utils import ObjectUtils # type: ignore
from voxility_pro.enums.version_type import VersionType # type: ignore

class ObjectImportMergeVerticesHandler(IHandler):
    def __init__(self, object: bpy.types.Object, with_vertex_colors: bool) -> None:
        self.object: bpy.types.Object = object
        self.with_vertex_colors: bool = with_vertex_colors

    def execute_handler(self) -> None:
        v: Tuple[int, int, int] = bpy.app.version
        V: Tuple[int, int, int] = VersionType.VERTEX_COLORS_W_MERGING_SUPPORT_BLENDER_VERSION.value
        if v < V and self.with_vertex_colors:
            print(f"Merging vertices is compatible with vertex colors only in Blender version {V} and above")
            return
        #ObjectUtils.merge_vertices(self.object) #
        ObjectUtils.auto_merge_vertices(self.object)
        ObjectUtils.validate_mesh(self.object)