from voxility_pro.operators.handler_interface import IHandler
from voxility_pro.utils.object_utils import auto_merge_vertices, validate_mesh

class ObjectImportMergeVerticesHandler(IHandler):
    def __init__(self, object):
        self.object = object

    def execute_handler(self):
        auto_merge_vertices(self.object)
        validate_mesh(self.object)