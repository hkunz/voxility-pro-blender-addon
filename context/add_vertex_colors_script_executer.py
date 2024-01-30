import bpy

from voxility_pro.context.context_script_executer import ContextScriptExecuter

AREA_TYPE='NODE_EDITOR'
AREA_UI_TYPE='ShaderNodeTree'

class AddVertexColorsScriptExecuter(ContextScriptExecuter):
    def __init__(self, object):
        super().__init__(AREA_TYPE, AREA_UI_TYPE)
        self.object = object

    @staticmethod
    def set_active_node_tree(area, object, material_index = 0):
        C = bpy.context
        C.view_layer.objects.active = object
        C.object.active_material_index = material_index
        mat = C.active_object.active_material
        area.spaces.active.node_tree = mat.node_tree # https://blender.stackexchange.com/a/268511/14229

    def script_content(self, context, legacy):
        AddVertexColorsScriptExecuter.set_active_node_tree(self.area, self.object)
        vc_type = 'ShaderNodeVertexColor'
        if legacy:
            bpy.ops.node.add_node(context, use_transform=True, type=vc_type)
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