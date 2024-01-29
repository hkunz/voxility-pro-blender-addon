import bpy

from voxility_pro.context.context_active_object_script_executer import ContextActiveObjectScriptExecuter

class AddVertexColorsScriptExecuter(ContextActiveObjectScriptExecuter):
    def __init__(self, object):
        super().__init__(object, 'NODE_EDITOR', 'ShaderNodeTree')

    def report_execute_error(self, message):
        super().report_execute_error(message)
        self.report({'ERROR'}, f"Could not add vertex colors to shader editor")

    def execute_script_content(self, override_context=None):
        super().execute_script_content(self, override_context)
        bpy.context.object.active_material_index = 0
        vc_type = 'ShaderNodeVertexColor'
        if override_context:
            bpy.ops.node.add_node(override_context, use_transform=True, type=vc_type)
        else:
            bpy.ops.node.add_node(use_transform=True, type=vc_type)

        mat = bpy.context.active_object.active_material
        shader_tree = mat.node_tree
        bsdf = shader_tree.nodes.get('Principled BSDF')
        vc_node = shader_tree.nodes.get("Vertex Color")

        if bsdf and vc_node:
            shader_tree.links.new(bsdf.inputs["Base Color"], vc_node.outputs["Color"])
        else:
            self.report_execute_error(f"Could not find BSDF node ({bsdf}) or vertex color node ({vc_node})")