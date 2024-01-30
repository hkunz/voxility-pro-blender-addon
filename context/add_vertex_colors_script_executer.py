import bpy

from voxility_pro.context.context_script_executer import ContextScriptExecuter

AREA_TYPE='NODE_EDITOR'
AREA_UI_TYPE='ShaderNodeTree'

class AddVertexColorsScriptExecuter(ContextScriptExecuter):
    def __init__(self, object):
        super().__init__(AREA_TYPE, AREA_UI_TYPE)
        self.object = object

    def prepare_context_area(self, area):
        super().prepare_context_area(area)
        ContextScriptExecuter.set_active_node_tree(area, self.object)

    def script_content(self, override_context=None):
        vc_type = 'ShaderNodeVertexColor'
        if override_context:
            bpy.ops.node.add_node(override_context, use_transform=True, type=vc_type)
        else:
            bpy.ops.node.add_node(use_transform=True, type=vc_type)

        mat = bpy.context.active_object.active_material
        node_tree = mat.node_tree
        bsdf = node_tree.nodes.get('Principled BSDF')
        vc_node = node_tree.nodes.get("Color Attribute") or node_tree.nodes.get("Vertex Color")

        if not bsdf or not vc_node:
            self.report_execute_error(f"Could not find BSDF node ({bsdf}) or vertex color node ({vc_node})")
            return False

        node_tree.links.new(vc_node.outputs["Color"], bsdf.inputs["Base Color"])
        vc_node.layer_name = "Color"

        return True