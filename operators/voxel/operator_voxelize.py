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
