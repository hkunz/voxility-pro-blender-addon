import bpy

from voxility_pro.operators.handler_interface import IHandler
from voxility_pro.utils.object_utils import auto_merge_vertices, validate_mesh

class ObjectImportMergeVerticesHandler(IHandler):
    def __init__(self, object, with_vertex_colors):
        self.object = object
        self.with_vertex_colors = with_vertex_colors

    def execute_handler(self):
        v = bpy.app.version
        V = (3, 5, 0)
        if v < V and self.with_vertex_colors:
            print(f"Merging vertices is compatible with vertex colors only in Blender version {V} and above")
            return
        auto_merge_vertices(self.object)
        validate_mesh(self.object)