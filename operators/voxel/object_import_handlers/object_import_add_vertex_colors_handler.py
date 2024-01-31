import bpy

from voxility_pro.operators.handler_interface import IHandler
from voxility_pro.context.context_script_executer import ContextScriptExecuter
from voxility_pro.enums.area_type import AreaType
from voxility_pro.enums.area_ui_type import AreaUiType

class AddVertexColorsScriptExecuter(ContextScriptExecuter):
    def __init__(self):
        super().__init__(AreaType.NODE_EDITOR.name, AreaUiType.ShaderNodeTree.name)

    @staticmethod
    def set_active_node_tree(area, material_index = 0):
        C = bpy.context
        C.object.active_material_index = material_index
        mat = C.active_object.active_material
        area.spaces.active.node_tree = mat.node_tree # https://blender.stackexchange.com/a/268511/14229

    def script_content(self, context, legacy):
        AddVertexColorsScriptExecuter.set_active_node_tree(self.area)
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

class ObjectImportAddVertexColorsHandler(IHandler):
    def __init__(self):
        pass

    def script_content(self, context, legacy):
        AddVertexColorsScriptExecuter.set_active_node_tree(self.area)
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

    def add_vertex_colors(self):
        a = AddVertexColorsScriptExecuter()
        success = a.execute_script()
        print(f"{AddVertexColorsScriptExecuter.__name__} complete: {success or a.error_message}")

    def color_attribute_convert(self):
        ContextScriptExecuter(
            area_type=AreaType.VIEW_3D.name,
            script=lambda override, legacy: (
                bpy.ops.geometry.color_attribute_convert(override, domain='CORNER', data_type='FLOAT_COLOR')
                if legacy
                else bpy.ops.geometry.color_attribute_convert(domain='CORNER', data_type='FLOAT_COLOR')
            )
        ).execute_script()

    def execute_handler(self):
        self.add_vertex_colors()
        self.color_attribute_convert()