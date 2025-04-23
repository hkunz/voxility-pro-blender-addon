import bpy

from bpy.types import (
    Material,
    ShaderNodeTree,
)

from voxelity_pro.operators.common.handler_interface import IHandler

class ObjectImportFixImageTextureHandler(IHandler):
    def __init__(self, object: bpy.types.Object):
        self.object: bpy.types.Object = object

    def execute_handler(self) -> None:
        mat: Material = self.object.active_material
        node_tree: ShaderNodeTree = mat.node_tree
        nodes = node_tree.nodes
        tex = None
        for n in nodes:
            if n.type == "UVMAP":
                return # an object with the same material has already added this node
            if n.type == "TEX_IMAGE":
                tex = n
        if not tex:
            return
        uvmap_node = nodes.new(type='ShaderNodeUVMap')
        uvmap_node.location = (-700,200)
        uvmap_node.uv_map = self.object.data.uv_layers[0].name
        node_tree.links.new(uvmap_node.outputs['UV'], tex.inputs['Vector'])