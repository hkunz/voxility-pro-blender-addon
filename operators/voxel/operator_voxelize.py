import bpy
import bpy_types

from typing import List

from voxility_pro.enums.name_constant import NameConstant

class BlenderVersionError(Exception):
    pass

class OBJECT_OT_OperatorVoxelize(bpy.types.Operator):
    bl_idname = "object.voxility_voxelize"
    bl_label = "Voxility Voxelize Object"
    bl_description = "Voxelize or convert selected objects into a single voxel object"
    bl_options = {'REGISTER'}

    VOXILITY_MODIFIER_NAME = NameConstant.VOXILITY_MODIFIER_NAME.value

    min_value: bpy.props.FloatProperty(name="Min Value", default=0.0)
    max_value: bpy.props.FloatProperty(name="Max Value", default=100.0)
    default_value: bpy.props.FloatProperty(name="Default Value", default=0.4)

    def execute(self, context):
        v = bpy.app.version
        if v >= (4, 0, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_4_0 import add_voxelizer_4_0
            add_voxelizer_4_0(context.active_object, self.min_value, self.max_value, self.default_value)
        elif v >= (3, 4, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_3_4 import add_voxelizer_3_4
            add_voxelizer_3_4(context.active_object, self.min_value, self.max_value, self.default_value)
        elif v >= (3, 2, 0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_3_3 import add_voxelizer_3_3
            add_voxelizer_3_3(context.active_object, self.min_value, self.max_value, self.default_value)
        else:
            raise BlenderVersionError("Voxelize feature is not supported in this Blender version. This feature is only supported for Blender versions 3.3 and above.")
   
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        active_object: bpy_types.Object = context.active_object
        node_groups = bpy.data.node_groups
        voxility_node_group = node_groups[cls.VOXILITY_MODIFIER_NAME] if cls.VOXILITY_MODIFIER_NAME in node_groups else None

        for m in reversed(active_object.modifiers):
            if m.type == 'NODES' and voxility_node_group and m.node_group == voxility_node_group:
                return False

        selected_objects: List[bpy_types.Object] = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
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
# Modification 4.0 - 1: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
import bpy ### Manual Entry
from voxility_pro.enums.name_constant import NameConstant ### Manual Entry
 ### Manual Entry
def voxelize_node_group_4_0(node_group_name, min_value, max_value, default_value): ### Manual Entry
    if node_group_name in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups[node_group_name] ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
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
    if node_group_name in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups[node_group_name] ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
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
from voxility_pro.enums.name_constant import NameConstant ### Manual Entry
 ### Manual Entry
def voxelize_node_group_3_4(node_group_name, min_value, max_value, default_value): ### Manual Entry
    if node_group_name in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups[node_group_name] ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
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


    evaluate_on_domain = evaluate_on_domain # NOTE: Useless line used to remove errors below
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 4: Index is shifted from 2 to 3 in the creating noodle link process (search voxelize.links.new)
# ========================================================================================================== ### Manual Entry
    iiiiiiii = 3 if v >= (3,5,0) else 2 ### Manual Entry
    voxelize.links.new(evaluate_on_domain.outputs[2], store_named_attribute.inputs[iiiiiiii]) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 4: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 5: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
def voxelizemodifier_node_group_3_4(voxelize, node_group_name, min_value, max_value, default_value): ### Manual Entry
    if node_group_name in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups[node_group_name] ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 5: END ### Manual Entry
# ========================================================================================================== ### Manual Entry


# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 6: Assign default_value, min_value, max_value within voxelizemodifier_node_group ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelizemodifier.inputs[1].default_value = default_value ### Manual Entry
    voxelizemodifier.inputs[1].min_value = min_value ### Manual Entry
    voxelizemodifier.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.4 - 6: END ### Manual Entry
# ========================================================================================================== ### Manual Entry