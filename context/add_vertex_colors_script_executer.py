import bpy

from voxility_pro.context.context_script_executer import ContextScriptExecuter

class AddVertexColorsScriptExecuter(ContextScriptExecuter):
    def __init__(self):
        super().__init__('NODE_EDITOR', 'ShaderNodeTree')

    def report_execute_error(self):
        super().report_execute_error()
        self.report({'ERROR'}, f"Could not add vertex colors to shader editor")

    def execute_script_content(self, override_context=None):
        bpy.context.object.active_material_index = 0
        vc_type = 'ShaderNodeVertexColor'
        if override_context:
            bpy.ops.node.add_node(override_context, use_transform=True, type=vc_type)
        else:
            bpy.ops.node.add_node(use_transform=True, type=vc_type)