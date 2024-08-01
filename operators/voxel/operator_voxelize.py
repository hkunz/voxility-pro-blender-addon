import bpy
import bpy_types

from typing import List

from voxility_pro.utils.voxel.voxel_utils import Voxel, VoxelUtils # type: ignore

class BlenderVersionError(Exception):
    pass

class OBJECT_OT_OperatorVoxelize(bpy.types.Operator):
    bl_idname = "object.voxility_voxelize"
    bl_label = "Voxility Voxelize Object"
    bl_description = "Voxelize selected objects with colors, textures, and vertex colors"
    bl_options = {'REGISTER','UNDO'}

    min_value: bpy.props.FloatProperty(name="Min Value", default=Voxel.DEFAULT_MIN) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770
    max_value: bpy.props.FloatProperty(name="Max Value", default=Voxel.DEFAULT_MAX) # type: ignore
    default_value: bpy.props.FloatProperty(name="Default Value", default=Voxel.DEFAULT_VALUE) # type: ignore

    def execute(self, context):
        v = bpy.app.version
        if v >= (4, 1, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_4_1 import add_voxelizer_4_1 as add_voxelizer # type: ignore
        elif v >= (4, 0, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_4_0 import add_voxelizer_4_0 as add_voxelizer # type: ignore
        elif v >= (3, 4, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_3_4 import add_voxelizer_3_4 as add_voxelizer # type: ignore
        elif v >= (3, 3, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_3_3 import add_voxelizer_3_3 as add_voxelizer # type: ignore
        elif v >= (3, 1, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_3_1 import add_voxelizer_3_1 as add_voxelizer # type: ignore
        else:
            raise BlenderVersionError("Voxelize feature is not supported in this Blender version. This feature is only supported for Blender versions 3.3 and above.")

        update = False
        for obj in context.selected_objects:
            if VoxelUtils.get_voxelizer_modifier(obj):
                continue
            add_voxelizer(obj, self.min_value, self.max_value, self.default_value)
            obj.voxelized = True
            update = True
        if update:
            context.scene.voxelize_list_update = True

        context.scene.on_voxelize_button_click(context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if not active_object:
            return False
        m = VoxelUtils.get_voxelizer_modifier(active_object)
        selected_objects: List[bpy_types.Object] = context.selected_objects
        if m or context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for o in selected_objects:
            if o.type != 'MESH' or not o.data.polygons:
                return False
        return True

def register():
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelize)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelize)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.voxility_voxelize()







# NOTE: 0. In case new changes need to be done in the nodegroup, edit it in 4.0 then Node2Python
# NOTE: 1. Append the node group from higher version to the lower version
# NOTE: 2. Name the nodes "Voxelize" and "VoxelizeModifier" then use Node2Python
# NOTE: 3. After Node2Python copy/paste, we need to modify the script with the following:

# ========================================================================================================== ### Manual Entry
# Modification 4.1 - 0: Same as 4.0
# ========================================================================================================== ### Manual Entry

# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 1: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
import bpy ### Manual Entry
from voxility_pro.enums.name_constant import NameConstant # type: ignore ### Manual Entry
from voxility_pro.utils.voxel.voxel_utils import VoxelUtils # type: ignore ### Manual Entry
### Manual Entry
def voxelize_node_group_4_0(node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelize = VoxelUtils.get_voxility_node_group(node_group_name) ### Manual Entry
    if voxelize: ### Manual Entry
        return voxelize ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelize[node_group_name] = 1 # add a custom id with key of the voxility group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 1: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


    voxel_size_socket = voxel_size_socket # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 2: Assign default_value, min_value, max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxel_size_socket.default_value = default_value ### Manual Entry
    voxel_size_socket.min_value = min_value ### Manual Entry
    voxel_size_socket.max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 2: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 3: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
def voxelizemodifier_node_group_4_0(voxelize, node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelizemodifier = VoxelUtils.get_voxility_node_group(node_group_name) ### Manual Entry
    if voxelizemodifier: ### Manual Entry
        return voxelizemodifier ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelizemodifier[node_group_name] = 1 # add a custom id with key of the voxility modifier group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 3: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry


    voxel_size_socket_1 = voxel_size_socket_1 # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 4: Assign default_value, min_value, max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxel_size_socket_1.default_value = default_value ### Manual Entry
    voxel_size_socket_1.min_value = min_value ### Manual Entry
    voxel_size_socket_1.max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 4.0 - 4: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 1: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
import bpy ### Manual Entry
from voxility_pro.enums.name_constant import NameConstant # type: ignore ### Manual Entry
from voxility_pro.utils.voxel.voxel_utils import VoxelUtils # type: ignore ### Manual Entry
### Manual Entry
def voxelize_node_group_3_4(node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelize = VoxelUtils.get_voxility_node_group(node_group_name) ### Manual Entry
    if voxelize: ### Manual Entry
        return voxelize ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelize[node_group_name] = 1 # add a custom id with key of the voxility group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 1: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 2: Assign default_value, min_value, max_value within voxelize_node_group ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelize.inputs[1].default_value = default_value ### Manual Entry
    voxelize.inputs[1].min_value = min_value ### Manual Entry
    voxelize.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 2: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


    store_named_attribute = store_named_attribute # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 3: Use FLOAT2 if 3.5+ else FLOAT_VECTOR ### Manual Entry
# ========================================================================================================== ### Manual Entry
    v = bpy.app.version ### Manual Entry
    store_named_attribute.data_type = 'FLOAT2' if v >= (3,5,0) else 'FLOAT_VECTOR' ### Manual Entry
    store_named_attribute.domain = 'CORNER' ### Manual Entry
    store_named_attribute_inputs = store_named_attribute.inputs ### Manual Entry
    ### Manual Entry
    if v >= (3,5,0): ### Manual Entry
        store_named_attribute_inputs[1].default_value = True #Selection ### Manual Entry
        store_named_attribute_inputs[2].default_value = "UVMap" #Name ### Manual Entry
        store_named_attribute_inputs[4].default_value = 0.0 #Value_Float ### Manual Entry
        store_named_attribute_inputs[5].default_value = (0.0, 0.0, 0.0, 0.0) #Value_Color ### Manual Entry
        store_named_attribute_inputs[6].default_value = False #Value_Bool ### Manual Entry
        store_named_attribute_inputs[7].default_value = 0 #Value_Int ### Manual Entry
    else: ### Manual Entry
        store_named_attribute_inputs[1].default_value = "UVMap" #Name ### Manual Entry
        store_named_attribute_inputs[3].default_value = 0.0 #Value_Float ### Manual Entry
        store_named_attribute_inputs[4].default_value = (0.0, 0.0, 0.0, 0.0) #Value_Color ### Manual Entry
        store_named_attribute_inputs[5].default_value = False #Value_Bool ### Manual Entry
        store_named_attribute_inputs[6].default_value = 0 #Value_Int ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 3: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


        store_named_attribute_001 = store_named_attribute_001 # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 4: StoreNamedAttributeNode has changed in 3.5
# ========================================================================================================== ### Manual Entry
    if v >= (3,5,0): ### Manual Entry
        store_named_attribute_001.inputs[1].default_value = True #Selection ### Manual Entry
        store_named_attribute_001.inputs[3].default_value = (0.0, 0.0, 0.0) #Value_Vector ### Manual Entry
        store_named_attribute_001.inputs[6].default_value = False #Value Bool ### Manual Entry
        store_named_attribute_001.inputs[7].default_value = 0 #Value Int ### Manual Entry
    else: ### Manual Entry
        store_named_attribute_001.inputs[3].default_value = 0.0 #Value_Float ### Manual Entry
        store_named_attribute_001.inputs[5].default_value = False #Value_Bool ### Manual Entry
        store_named_attribute_001.inputs[6].default_value = 0 #Value_Int ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 4: StoreNamedAttributeNode has changed in 3.5
# ========================================================================================================== ### Manual Entry


    evaluate_on_domain = evaluate_on_domain # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 5: Index is shifted from 2 to 3 in the creating noodle link process (search voxelize.links.new)
# ========================================================================================================== ### Manual Entry
    iiiiiiii = 3 if v >= (3,5,0) else 2 ### Manual Entry
    voxelize.links.new(evaluate_on_domain.outputs[2], store_named_attribute.inputs[iiiiiiii]) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 5: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


    group_input_004 = group_input_004 # NOTE: Useless line used to remove errors below
    evaluate_on_domain_001 = evaluate_on_domain_001 # NOTE: Useless line used to remove errors below
    group_input_005 = group_input_005 # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 6: Index is shifted in the creating noodle link process ### Manual Entry
# ========================================================================================================== ### Manual Entry
    if v >= (3,5,0): ### Manual Entry
        voxelize.links.new(group_input_004.outputs[2], store_named_attribute.inputs[2]) ### Manual Entry
        voxelize.links.new(evaluate_on_domain_001.outputs[3], store_named_attribute_001.inputs[5]) ### Manual Entry
        voxelize.links.new(group_input_005.outputs[3], store_named_attribute_001.inputs[2]) ### Manual Entry
    else: ### Manual Entry
        voxelize.links.new(evaluate_on_domain_001.outputs[3], store_named_attribute_001.inputs[2]) ### Manual Entry
        voxelize.links.new(group_input_004.outputs[2], store_named_attribute.inputs[1]) ### Manual Entry
        voxelize.links.new(group_input_005.outputs[3], store_named_attribute_001.inputs[1]) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 6: Index is shifted in the creating noodle link process ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 7: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
def voxelizemodifier_node_group_3_4(voxelize, node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelizemodifier = VoxelUtils.get_voxility_node_group(node_group_name) ### Manual Entry
    if voxelizemodifier: ### Manual Entry
        return voxelizemodifier ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelizemodifier[node_group_name] = 1 # add a custom id with key of the voxility modifier group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 7: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 8: Assign default_value, min_value, max_value within voxelizemodifier_node_group ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelizemodifier.inputs[1].default_value = default_value ### Manual Entry
    voxelizemodifier.inputs[1].min_value = min_value ### Manual Entry
    voxelizemodifier.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 8: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 1: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
import bpy ### Manual Entry
from voxility_pro.enums.name_constant import NameConstant # type: ignore ### Manual Entry
from voxility_pro.utils.voxel.voxel_utils import VoxelUtils # type: ignore ### Manual Entry
### Manual Entry
def voxelize_node_group_3_3(node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelize = VoxelUtils.get_voxility_node_group(node_group_name) ### Manual Entry
    if voxelize: ### Manual Entry
        return voxelize ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelize[node_group_name] = 1 # add a custom id with key of the voxility group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 1: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


    voxel_size_socket = voxel_size_socket # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 2: Assign default_value, min_value, max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelize.inputs[1].default_value = default_value ### Manual Entry
    voxelize.inputs[1].min_value = min_value ### Manual Entry
    voxelize.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 2: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 3: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
def voxelizemodifier_node_group_3_3(voxelize, node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelizemodifier = VoxelUtils.get_voxility_node_group(node_group_name) ### Manual Entry
    if voxelizemodifier: ### Manual Entry
        return voxelizemodifier ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelizemodifier[node_group_name] = 1 # add a custom id with key of the voxility modifier group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 3: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 4: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelizemodifier.inputs[1].default_value = default_value
    voxelizemodifier.inputs[1].min_value = min_value
    voxelizemodifier.inputs[1].max_value = max_value
# ========================================================================================================== ### Manual Entry
# Modification 3.3 - 4: END ### Manual Entry
# ========================================================================================================== ### Manual Entry