import bpy
import bpy_types

from typing import List

from voxelity_pro.operators.operator_generic_popup import OperatorGenericPopup
from voxelity_pro.utils.object_utils import ObjectUtils
from voxelity_pro.utils.voxel.voxel_utils import VoxelUtils
from voxelity_pro.utils.number_utils import NumberUtils

class VoxelError:
    ERROR_NONE = -1
    ERROR_NO_MATERIALS = 0
    ERROR_MULTIPLE_BSDF_NODES = 1
    ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES = 2
    ERROR_MISSING_INPUT_IN_MATERIAL_OUTPUT_NODE = 3
    ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE = 4
    ERROR_SURFACE_SOCKET_SUPPORTED_IN_MATERIAL_OUTPUT_NODE = 5
    ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT = 6
    ERROR_MISSING_MATERIAL_OUTPUT_NODE = 7
    ERROR_MISSING_IMAGE_TEXTURE_IMAGE = 8
    ERROR_MUST_USE_IMAGE_TEXTURE_COLOR_SOCKET = 9
    ERROR_OBJECT_MISSING_UVMAPS = 10
    ERROR_MISSING_UVMAP_NODE_INPUT_TO_IMAGE_TEXTURE = 11
    ERROR_INVALID_UVMAP_NAME_USED_IN_VOXILITY_PANEL = 12
    ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE = 13
    ERROR_ONLY_ATTRIBUTE_NODE_GEOMETRY_TYPE_ALLOWED = 14
    ERROR_ONLY_ATTRIBUTE_NODE_VECTOR_SOCKET_ALLOWED_FOR_UVMAP_USE = 15
    ERROR_INVALID_ATTRIBUTE_NODE_OUTPUT_SOCKET_USED_FOR_UVMAP = 16
    ERROR_UVMAP_NODE_INPUT_REQUIRED_TO_IMAGE_TEXTURE = 17
    ERROR_OBJECT_MISSING_COLOR_ATTRIBUTES = 18
    ERROR_INVALID_COLOR_ATTRIBUTE_NAME_USED_IN_VOXILITY_PANEL = 19
    ERROR_MUST_USE_COLOR_ATTRIBUTE_COLOR_SOCKET = 20
    ERROR_INVALID_COLOR_ATTRIBUTE_NAME_USED_IN_ATTRIBUTE_NODE = 21
    ERROR_ONLY_ATTRIBUTE_NODE_COLOR_SOCKET_ALLOWED_FOR_COLOR_ATTRIBUTE_USE = 22
    ERROR_ALL_SELECTED_OBJECT_MUST_USE_SAME_VOXEL_SIZE = 23
    ERROR_ALL_SELECTED_OBJECT_MUST_HAVE_SCALE_OF_1 = 24
    WARNING_MULTIPLE_UV_MAPS_PER_OBJECT_NOT_SUPPORTED = 25
    WARNING_MULTIPLE_COLOR_ATTRIBUTES_PER_OBJECT_NOT_SUPPORTED = 26

    def __init__(self):
        self.bake_fix_option = False

    @staticmethod
    def get_error(e):
        if e == VoxelError.ERROR_NO_MATERIALS:
            return "No materials found (or 'Use Nodes' is disabled)"
        if e == VoxelError.ERROR_NONE:
            return "No errors"
        if e == VoxelError.ERROR_MULTIPLE_BSDF_NODES:
            return "Only one 'Principled BSDF' node allowed"
        if e == VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES:
            return "Only one 'Material Output' node allowed"
        if e == VoxelError.ERROR_MISSING_INPUT_IN_MATERIAL_OUTPUT_NODE:
            return "Missing input to 'Surface' socket of 'Material Output' node"
        if e == VoxelError.ERROR_SURFACE_SOCKET_SUPPORTED_IN_MATERIAL_OUTPUT_NODE:
            return "Only 'Surface' socket of 'Material Output' node supported"
        if e == VoxelError.ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE:
            return "Only 'Princpled BSDF' allowed to 'Surface' socket of 'Material Output' node"
        if e == VoxelError.ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT:
            return "Only 'Image Texture' or 'Color Attribute' nodes allowed to 'Base Color' socket of 'Principled BSDF' node" # 91 characters max equivalent to 520 width
        if e == VoxelError.ERROR_MISSING_MATERIAL_OUTPUT_NODE:
            return "Missing 'Material Output' node"
        if e == VoxelError.ERROR_MISSING_IMAGE_TEXTURE_IMAGE:
            return "Missing image in 'Image Texture'"
        if e == VoxelError.ERROR_MUST_USE_IMAGE_TEXTURE_COLOR_SOCKET:
            return "Only 'Color' socket of 'Image Texture' node allowed to 'Base Color' socket of 'Principled BSDF'"
        if e == VoxelError.ERROR_OBJECT_MISSING_UVMAPS:
            return "Object 'PARAM' has no UV Maps"
        if e == VoxelError.ERROR_MISSING_UVMAP_NODE_INPUT_TO_IMAGE_TEXTURE:
            return "Missing 'UV Map' node to 'Vector' socket of 'Image Texture' node"
        if e == VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_VOXILITY_PANEL:
            return "Invalid 'UV Map' name specified in Voxelity panel. Possible values are: PARAM"
        if e == VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE:
            return "Invalid UV Map name used in 'UV Map' node. You must use name specified in Voxelity panel which is 'PARAM'"
        if e == VoxelError.ERROR_ONLY_ATTRIBUTE_NODE_GEOMETRY_TYPE_ALLOWED:
            return "Invalid attribute type 'PARAM' used in 'Attribute' node. You must use 'GEOMETRY'"
        if e == VoxelError.ERROR_ONLY_ATTRIBUTE_NODE_VECTOR_SOCKET_ALLOWED_FOR_UVMAP_USE:
            return "Only 'Vector' socket of 'Attribute' node allowed for UV Map"
        if e == VoxelError.ERROR_UVMAP_NODE_INPUT_REQUIRED_TO_IMAGE_TEXTURE:
            return "A 'UV Map' node is required as input to 'Vector' socket of 'Image Texture' node"
        if e == VoxelError.ERROR_OBJECT_MISSING_COLOR_ATTRIBUTES:
            return "Object 'PARAM' has no Color Attributes"
        if e == VoxelError.ERROR_INVALID_COLOR_ATTRIBUTE_NAME_USED_IN_VOXILITY_PANEL:
            return "Invalid 'Color Attribute' name specified in Voxelity panel. Possible values are: PARAM"
        if e == VoxelError.ERROR_MUST_USE_COLOR_ATTRIBUTE_COLOR_SOCKET:
            return "Only 'Color' socket of 'Color Attribute' node allowed to 'Base Color' socket of 'Principled BSDF'"
        if e == VoxelError.ERROR_INVALID_COLOR_ATTRIBUTE_NAME_USED_IN_ATTRIBUTE_NODE:
            return "Invalid Color Attribute name used in 'Color Attribute' node. You must use name specified in Voxelity panel which is 'PARAM'"
        if e == VoxelError.ERROR_ONLY_ATTRIBUTE_NODE_COLOR_SOCKET_ALLOWED_FOR_COLOR_ATTRIBUTE_USE:
            return "Only 'Color' socket of 'Attribute' node allowed for Color Attribute use"
        if e == VoxelError.ERROR_ALL_SELECTED_OBJECT_MUST_USE_SAME_VOXEL_SIZE:
            return "All selected objects must have the same voxel size as the active object which is PARAM"
        if e == VoxelError.ERROR_ALL_SELECTED_OBJECT_MUST_HAVE_SCALE_OF_1:
            return "All selected objects must have Scale applied. Apply scale (Object > Apply > Scale) or manually set it back to 1.0"
        if e == VoxelError.WARNING_MULTIPLE_UV_MAPS_PER_OBJECT_NOT_SUPPORTED:
            return "Warning: Multiple UV Maps per object is not yet supported"
        if e == VoxelError.WARNING_MULTIPLE_COLOR_ATTRIBUTES_PER_OBJECT_NOT_SUPPORTED:
            return "Warning: Multiple Color Attributes per object is not yet supported"
        return "Undefined Error"

class OBJECT_OT_OperatorVoxelizeValidityCheck(OperatorGenericPopup):
    bl_idname = "object.voxelity_voxelize_validity_check"
    bl_label = "Voxelity Voxelize Validity Check"
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

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        self.errors = self.get_errors(context)
        self.width = self.MIN_POPUP_WIDTH
        for o, e, p in self.errors:
            self.width = int(max(self.width, (len(VoxelError.get_error(e)) + len(o.name))/self.MAX_ERROR_CHARS*self.MAX_POPUP_WIDTH))
        self.width += self.POPUP_WIDTH_PAD
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
            cbox = col.box().column()
            cbox.label(text="Object OK.", icon='CHECKMARK')
            cbox.label(text="Select 'Target' and click 'Export'", icon='CHECKMARK')
            return

        col.label(text="The following problems were detected:")
        box = col.box()
        box.alert = True
        col = box.column()
        for i, tuple in enumerate(self.errors):
            mat_name = tuple[0].name
            e = VoxelError.get_error(tuple[1])
            param = tuple[2]
            if param:
                e = e.replace("PARAM", param)
            err = f"{mat_name}: {e}"
            col.label(text=err, icon='CANCEL')
        if not self.bake_fix_option:
            return
        cbox = layout.box().column()
        cbox.label(text="Fix these problems or click 'Bake' to bake object and materials")
        cbox.label(text="NOTE: Baking will apply all modifiers")

    def get_errors(self, context):
        errors = []
        self.bake_fix_option = True
        base_vox_size = VoxelUtils.get_voxelizer_voxel_size(context.active_object)
        for obj in context.selected_objects:
            num_mat = 0
            vox_size, vox_uvmap, vox_colattr = VoxelUtils.get_voxelizer_voxel_modifier_attributes(obj)
            if not NumberUtils.is_almost_equal(base_vox_size, vox_size):
                self.bake_fix_option = False
                self.add_error_obj(obj, errors, VoxelError.ERROR_ALL_SELECTED_OBJECT_MUST_USE_SAME_VOXEL_SIZE, NumberUtils.format_decimal_2(base_vox_size))
            if not ObjectUtils.is_scale_applied(obj):
                self.bake_fix_option = False
                self.add_error_obj(obj, errors, VoxelError.ERROR_ALL_SELECTED_OBJECT_MUST_HAVE_SCALE_OF_1, NumberUtils.format_decimal_2(base_vox_size))
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
                    input_volume = self.get_from_input_node(matout_node, 1)
                    input_displ = self.get_from_input_node(matout_node, 2)
                    if input_volume or input_displ:
                        self.add_error(mat, errors, VoxelError.ERROR_SURFACE_SOCKET_SUPPORTED_IN_MATERIAL_OUTPUT_NODE)
                    if not from_node:
                        self.add_error(mat, errors, VoxelError.ERROR_MISSING_INPUT_IN_MATERIAL_OUTPUT_NODE)
                    elif from_node.type != "BSDF_PRINCIPLED":
                        self.add_error(mat, errors, VoxelError.ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE)
                    else:
                        bsdf_node = from_node
                        from_node = self.get_from_input_node(bsdf_node)
                        from_socket = self.get_from_input_socket(bsdf_node)
                        if not from_node:
                            pass # pass coz it's ok to use base color or direct color from Principled BSDF
                        elif from_node.type == 'TEX_IMAGE':
                            tex_node = from_node
                            if from_socket.type != 'RGBA':
                                self.add_error(mat, errors, VoxelError.ERROR_MUST_USE_IMAGE_TEXTURE_COLOR_SOCKET)
                            uvmaps = obj.data.uv_layers.keys()
                            if not uvmaps:
                                self.add_error_obj(obj, errors, VoxelError.ERROR_OBJECT_MISSING_UVMAPS, obj.name)
                            elif vox_uvmap not in obj.data.uv_layers:
                                    self.add_error(mat, errors, VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_VOXILITY_PANEL, str(uvmaps))
                            if not tex_node.image:
                                self.add_error(mat, errors, VoxelError.ERROR_MISSING_IMAGE_TEXTURE_IMAGE)
                            from_node = self.get_from_input_node(tex_node)
                            if not from_node:
                                self.add_error(mat, errors, VoxelError.ERROR_MISSING_UVMAP_NODE_INPUT_TO_IMAGE_TEXTURE)
                            elif from_node.type != 'UVMAP' and from_node.type != 'ATTRIBUTE':
                                self.add_error(mat, errors, VoxelError.ERROR_UVMAP_NODE_INPUT_REQUIRED_TO_IMAGE_TEXTURE)
                            elif from_node.type == 'UVMAP':
                                uvmap_node = from_node
                                if uvmaps and (not uvmap_node.uv_map or uvmap_node.uv_map != vox_uvmap):
                                    self.add_error(mat, errors, VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE, vox_uvmap)
                            elif from_node.type == 'ATTRIBUTE':
                                attr_node = from_node
                                from_socket = self.get_from_input_socket(tex_node)
                                if from_socket and from_socket.type != 'VECTOR':
                                    self.add_error(mat, errors, VoxelError.ERROR_ONLY_ATTRIBUTE_NODE_VECTOR_SOCKET_ALLOWED_FOR_UVMAP_USE)
                                if attr_node.attribute_type != 'GEOMETRY':
                                    self.add_error(mat, errors, VoxelError.ERROR_ONLY_ATTRIBUTE_NODE_GEOMETRY_TYPE_ALLOWED, attr_node.attribute_type)
                                if uvmaps and (not attr_node.attribute_name or attr_node.attribute_name != vox_uvmap):
                                    self.add_error(mat, errors, VoxelError.ERROR_INVALID_UVMAP_NAME_USED_IN_UVMAP_NODE, vox_uvmap)

                        elif from_node.type == 'VERTEX_COLOR' or from_node.type == 'ATTRIBUTE':
                            is_attr_node = from_node.type == 'ATTRIBUTE'
                            attr_node = from_node
                            color_name = attr_node.attribute_name if is_attr_node else attr_node.layer_name
                            colors = obj.data.color_attributes.keys()
                            if not colors:
                                self.add_error_obj(obj, errors, VoxelError.ERROR_OBJECT_MISSING_COLOR_ATTRIBUTES, obj.name)
                            elif vox_colattr not in colors:
                                self.add_error(mat, errors, VoxelError.ERROR_INVALID_COLOR_ATTRIBUTE_NAME_USED_IN_VOXILITY_PANEL, str(colors))
                            if is_attr_node and attr_node.attribute_type != 'GEOMETRY':
                                    self.add_error(mat, errors, VoxelError.ERROR_ONLY_ATTRIBUTE_NODE_GEOMETRY_TYPE_ALLOWED, attr_node.attribute_type)
                            if from_socket.type != 'RGBA':
                                self.add_error(mat, errors, VoxelError.ERROR_MUST_USE_COLOR_ATTRIBUTE_COLOR_SOCKET)
                            if colors and (not color_name or color_name != vox_colattr):
                                self.add_error(mat, errors, VoxelError.ERROR_INVALID_COLOR_ATTRIBUTE_NAME_USED_IN_ATTRIBUTE_NODE, vox_colattr)
                        else:
                            self.add_error(mat, errors, VoxelError.ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT)

                if not matout_node:
                    self.add_error(mat, errors, VoxelError.ERROR_MISSING_MATERIAL_OUTPUT_NODE)


            if (num_mat <= 0):
                self.bake_fix_option = False
                self.add_error_obj(obj, errors, VoxelError.ERROR_NO_MATERIALS)

        return errors

    def add_error_obj(self, obj, errors, err, param=None):
        if not any(o == obj and e == err and p == param for o, e, p in errors):
            errors.append((obj, err, param))
            return True
        return False

    def add_error(self, mat, errors, err, param=None):
        if not any(o == mat and e == err for o, e, p in errors):
            errors.append((mat, err, param))
            return True
        return False

    def get_from_input_node(self, node, index=0):
        links = node.inputs[index].links
        return links[0].from_node if len(links) > 0 else None

    def get_from_input_socket(self, node, index=0):
        links = node.inputs[index].links
        return links[0].from_socket if len(links) > 0 else None



    @classmethod
    def poll(cls, context):
        active_object: bpy_types.Object = context.active_object
        selected_objects: List[bpy_types.Object] = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for o in selected_objects:
            if o.type != 'MESH' or not o.data.polygons or not o.voxelized: #is_object_voxelized(o):
                return False
        return True

def register():
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.voxelity_voxelize_validity_check()