import bpy

from voxility_pro.operators.handler_interface import IHandler
from voxility_pro.utils.object_utils import auto_merge_vertices, validate_mesh
from voxility_pro.enums.version_type import VersionType

class ObjectImportMergeVerticesHandler(IHandler):
    def __init__(self, object, with_vertex_colors):
        self.object = object
        self.with_vertex_colors = with_vertex_colors

    def execute_handler(self):
        v = bpy.app.version
        V = VersionType.VERTEX_COLORS_W_MERGING_SUPPORT_BLENDER_VERSION.value
        if v < V and self.with_vertex_colors:
            print(f"Merging vertices is compatible with vertex colors only in Blender version {V} and above")
            return
        auto_merge_vertices(self.object)
        validate_mesh(self.object)