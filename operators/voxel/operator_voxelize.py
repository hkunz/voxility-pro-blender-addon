import bpy

class BlenderVersionError(Exception):
    pass

class VoxelizeOperator(bpy.types.Operator):
    bl_idname = "object.voxility_voxelize"
    bl_label = "Voxility Voxelize Object"

    min_value: bpy.props.FloatProperty(name="Min Value", default=0.0)
    max_value: bpy.props.FloatProperty(name="Max Value", default=100.0)
    default_value: bpy.props.FloatProperty(name="Default Value", default=0.4)

    def execute(self, context):
        v = bpy.app.version
        if v >= (3,5,0) and v < (4,0,0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_3_5 import add_voxelizer_3_5
            add_voxelizer_3_5(context.active_object, self.min_value, self.max_value, self.default_value)
        elif v >= (4,0,0):
            from voxility_pro.utils.voxel.generate_gn_voxelize_4_0 import add_voxelizer_4_0
            add_voxelizer_4_0(context.active_object, self.min_value, self.max_value, self.default_value)
        else:
            raise BlenderVersionError("Voxelize feature is not supported in this Blender version. This feature is only supported for Blender versions 3.5 and above.")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VoxelizeOperator)

def unregister():
    bpy.utils.unregister_class(VoxelizeOperator)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.voxelize()
