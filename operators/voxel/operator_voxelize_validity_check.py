import bpy
import bpy_types

from typing import List

from voxility_pro.operators.operator_generic_popup import OperatorGenericPopup # type: ignore
from voxility_pro.utils.voxel.voxel_utils import is_object_voxelized, get_voxelizer_voxel_modifier_attributes # type: ignore

class VoxelError:
    ERROR_NONE = 0
    ERROR_MULTIPLE_BSDF_NODES = 1
    ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES = 2
    ERROR_MISSING_INPUT_IN_MATERIAL_OUTPUT_NODE = 3
    ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE = 4
    ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT = 5
    ERROR_MISSING_MATERIAL_OUTPUT_NODE = 6
    ERROR_MISSING_IMAGE_TEXTURE_IMAGE = 7
    ERROR_OBJECT_MISSING_UVMAPS = 8
    ERROR_MISSING_UVMAP_NODE_INPUT_TO_IMAGE_TEXTURE = 9
    ERROR_INVALID_UVMAP_NAME_USED_IN_VOXILITY_PANEL = 10
    ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE = 11
    ERROR_UVMAP_NODE_INPUT_REQUIRED_TO_IMAGE_TEXTURE = 12
    WARNING_NO_MATERIALS = 13

    @staticmethod
    def get_error(e):
        if e == VoxelError.ERROR_NONE:
            return "No errors"
        if e == VoxelError.ERROR_MULTIPLE_BSDF_NODES:
            return "Only one \"Principled BSDF\" node allowed"
        if e == VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES:
            return "Only one \"Material Output\" node allowed"
        if e == VoxelError.ERROR_MISSING_INPUT_IN_MATERIAL_OUTPUT_NODE:
            return "Missing input to \"Material Output\" node's \"Surface\" socket"
        if e == VoxelError.ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE:
            return "Only \"Princpled BSDF\" allowed in \"Material Output\" node"
        if e == VoxelError.ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT:
            return "Only \"Image Texture\" or \"Color Attribute\" nodes allowed in \"Principled BSDF\" node's \"Base Color\" socket" # 91 characters max equivalent to 520 width
        if e == VoxelError.ERROR_MISSING_MATERIAL_OUTPUT_NODE:
            return "Missing \"Material Output\" node"
        if e == VoxelError.ERROR_MISSING_IMAGE_TEXTURE_IMAGE:
            return "Missing image in \"Image Texture\""
        if e == VoxelError.ERROR_OBJECT_MISSING_UVMAPS:
            return "Object \"PARAM\" has no UV Maps"
        if e == VoxelError.ERROR_MISSING_UVMAP_NODE_INPUT_TO_IMAGE_TEXTURE:
            return "Missing \"UV Map\" node in \"Image Texture\" node's \"Vector\" socket"
        if e == VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_VOXILITY_PANEL:
            return "Invalid UV Map name specified in Voxility panel. Possible UV Map values are: PARAM"
        if e == VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE:
            return "Invalid UV Map name used in \"UV Map\" node. You must use name specified in Voxility panel which is \"PARAM\""
        if e == VoxelError.ERROR_UVMAP_NODE_INPUT_REQUIRED_TO_IMAGE_TEXTURE:
            return "A \"UV Map\" node is required as input to \"Image Texture\" node's \"Vector\" socket"
        if e == VoxelError.WARNING_NO_MATERIALS:
            return "No materials found (or \"Use Nodes\" is disabled)"
        return "Undefined Error"

class OBJECT_OT_OperatorVoxelizeValidityCheck(OperatorGenericPopup):
    bl_idname = "object.voxility_voxelize_validity_check"
    bl_label = "Voxility Voxelize Validity Check"
    bl_description = "Check for potential issues in the materials before voxel conversion"
    bl_options = {'REGISTER'}

    POPUP_WIDTH_PAD = 50
    MIN_POPUP_WIDTH = 250
    MAX_POPUP_WIDTH = 600
    MAX_ERROR_CHARS = 100
    width=0

    temp: bpy.props.StringProperty(
        name="Temp String",
        description="Temp descrption",
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    def __init__(self):
        self.errors = None

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        self.errors = self.get_errors(context)
        self.width = self.MIN_POPUP_WIDTH
        for o, e, p in self.errors:
            self.width = int(max(self.width, (len(VoxelError.get_error(e)) + len(o.name))/self.MAX_ERROR_CHARS*self.MAX_POPUP_WIDTH)) + self.POPUP_WIDTH_PAD
        return super().invoke(context, event)

    def execute(self, context):
        # No need to do anything when OK is clicked
        self.exec_message = None
        super().execute(context)
        return {'FINISHED'}

    def draw(self, context: bpy_types.Context) -> None:
        layout: bpy.types.UILayout = self.layout
        col: bpy.types.UILayout = layout.column()

        if not self.errors:
            col.label(text="No problems found")
            return

        for i, tuple in enumerate(self.errors):
            e = VoxelError.get_error(tuple[1])
            if tuple[2]:
                e = e.replace("PARAM", tuple[2])
            err = f"{tuple[0].name}: {e}"
            col.label(text=err)

    def get_errors(self, context):
        errors = []
        for obj in context.selected_objects:
            #print(f"Check for problems in materials in object \"{obj.name}\":")
            num_mat = 0
            for slot in obj.material_slots:
                mat = slot.material
                if not mat or not mat.use_nodes:
                    continue
                num_mat += 1
                matout_node = None
                for n in mat.node_tree.nodes:
                    if n.type != 'OUTPUT_MATERIAL':
                        continue
                    if matout_node:
                        self.add_error(mat, errors, VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES)
                    matout_node = n
                    from_node = self.get_from_input_node(matout_node)
                    if not from_node:
                        self.add_error(mat, errors, VoxelError.ERROR_MISSING_INPUT_IN_MATERIAL_OUTPUT_NODE)
                    elif from_node.type != "BSDF_PRINCIPLED":
                        self.add_error(mat, errors, VoxelError.ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE)
                    else:
                        bsdf_node = from_node
                        from_node = self.get_from_input_node(bsdf_node)
                        _, vox_uvmap, vox_colattr = get_voxelizer_voxel_modifier_attributes(obj)
                        if not from_node:
                            pass # pass coz it's ok to use base color or direct color from Principled BSDF
                        elif from_node.type == 'TEX_IMAGE':
                            tex_node = from_node
                            if not obj.data.uv_layers.keys():
                                self.add_error(mat, errors, VoxelError.ERROR_OBJECT_MISSING_UVMAPS, obj.name)
                            elif not tex_node.image:
                                self.add_error(mat, errors, VoxelError.ERROR_MISSING_IMAGE_TEXTURE_IMAGE)
                            else:
                                #TODO check if Color output socket is used instead of Alpha
                                from_node = self.get_from_input_node(tex_node)
                                if not from_node:
                                    self.add_error(mat, errors, VoxelError.ERROR_MISSING_UVMAP_NODE_INPUT_TO_IMAGE_TEXTURE)
                                elif from_node.type != 'UVMAP':
                                    self.add_error(mat, errors, VoxelError.ERROR_UVMAP_NODE_INPUT_REQUIRED_TO_IMAGE_TEXTURE)
                                else:
                                    uvmap_node = from_node
                                    if vox_uvmap not in obj.data.uv_layers:
                                        self.add_error(mat, errors, VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_VOXILITY_PANEL, str(obj.data.uv_layers.keys()))
                                    elif not uvmap_node.uv_map or uvmap_node.uv_map != vox_uvmap:
                                        self.add_error(mat, errors, VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE, vox_uvmap)

                        elif from_node.type == 'VERTEX_COLOR':
                            #bpy.data.scenes["Scene"].voxility_pro_properties.color_attribute
                            #TODO bpy.data.materials["Material"].node_tree.nodes["Color Attribute"].layer_name
                            pass
                        elif from_node.type == 'ATTRIBUTE':
                            #TODO bpy.data.materials["Material"].node_tree.nodes["Color Attribute"].layer_name
                            pass
                        else:
                            self.add_error(mat, errors, VoxelError.ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT)

                if not matout_node:
                    self.add_error(mat, errors, VoxelError.ERROR_MISSING_MATERIAL_OUTPUT_NODE)


            if (num_mat <= 0):
                self.add_error(obj, errors, VoxelError.WARNING_NO_MATERIALS)

        return errors

    def add_error(self, obj, errors, err, param=None):
        if not any(o == obj and e == err for o, e, p in errors):
            errors.append((obj, err, param))
            return True
        return False

    def get_from_input_node(self, node):
        links = node.inputs[0].links
        return links[0].from_node if len(links) > 0 else None

    def get_to_output_node(self, node):
        links = node.outputs[0].links
        return links[0].to_node if len(links) > 0 else None

    @classmethod
    def poll(cls, context):
        active_object: bpy_types.Object = context.active_object

        selected_objects: List[bpy_types.Object] = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for o in selected_objects:
            if o.type != 'MESH' or not o.data.polygons or not is_object_voxelized(o):
                return False
        return True

def register():
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.voxility_voxelize_validity_check()