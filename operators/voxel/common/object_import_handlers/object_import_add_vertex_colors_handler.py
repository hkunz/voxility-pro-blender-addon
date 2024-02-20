import bpy
import bpy_types

from bpy.types import (
    Area,
    Material,
    ShaderNodeTree,
    ShaderNodeBsdfPrincipled,
    ShaderNode,
)

from voxility_pro.operators.common.handler_interface import IHandler
from voxility_pro.operators.common.context.context_script_executer import ContextScriptExecuter
from voxility_pro.operators.common.context.context_executer_override import ContextExecuterOverride
from voxility_pro.enums.area_type import AreaType
from voxility_pro.enums.area_ui_type import AreaUiType

class ObjectImportAddVertexColorsHandler(IHandler):
    def __init__(self) -> None:
        pass

    def set_active_node_tree(self, area: Area, material_index: int=0) -> None:
        C: bpy_types.Context = bpy.context
        C.object.active_material_index = material_index
        mat: Material = C.active_object.active_material
        area.spaces.active.node_tree = mat.node_tree # https://blender.stackexchange.com/a/268511/14229

    def add_vertex_colors_context_callback(self, override: ContextExecuterOverride) -> None:
        self.set_active_node_tree(override.area)
        vc_type: str = 'ShaderNodeVertexColor'
        if override.legacy:
            bpy.ops.node.add_node(override.context, use_transform=True, type=vc_type)
        else:
            bpy.ops.node.add_node(use_transform=True, type=vc_type)

    def add_vertex_colors(self) -> None:
        ContextScriptExecuter(
            area_type=AreaType.NODE_EDITOR.name,
            ui_type=AreaUiType.ShaderNodeTree.name,
            script=self.add_vertex_colors_context_callback
        ).execute_script()

        mat: Material = bpy.context.active_object.active_material
        node_tree: ShaderNodeTree = mat.node_tree
        bsdf: ShaderNodeBsdfPrincipled = node_tree.nodes.get('Principled BSDF')
        vc_node: ShaderNode = node_tree.nodes.get("Color Attribute") or node_tree.nodes.get("Vertex Color")

        if not bsdf or not vc_node:
            print(f"Could not find BSDF node ({bsdf}) or vertex color node ({vc_node})")
            return False

        node_tree.links.new(vc_node.outputs["Color"], bsdf.inputs["Base Color"])
        vc_node.layer_name = "Color"

    def color_attribute_convert(self) -> None:
        ContextScriptExecuter(
            area_type = AreaType.VIEW_3D.name,
            script = lambda override: (
                bpy.ops.geometry.color_attribute_convert(override, domain='CORNER', data_type='FLOAT_COLOR')
                if override.legacy
                else bpy.ops.geometry.color_attribute_convert(domain='CORNER', data_type='FLOAT_COLOR')
            )
        ).execute_script()

    def execute_handler(self) -> None:
        self.add_vertex_colors()
        self.color_attribute_convert()