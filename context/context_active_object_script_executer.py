import bpy

from voxility_pro.context.context_script_executer import ContextScriptExecuter

class ContextActiveObjectScriptExecuter(ContextScriptExecuter):
    def __init__(self, object, area_type, ui_type=None):
        super().__init__(area_type, ui_type)
        self.object = object

    def prepare_context_area(self, area):
        super().prepare_context_area(area)
        bpy.context.object.active_material_index = 0
        mat = bpy.context.active_object.active_material
        area.spaces.active.node_tree = mat.node_tree
        C = bpy.context
        C.view_layer.objects.active = self.object
