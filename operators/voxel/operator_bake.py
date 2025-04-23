import bpy
import bpy_types

from voxelity_pro.utils.voxel.bake_utility import BakeUtility
from voxelity_pro.operators.operator_generic_popup import create_generic_popup

class OBJECT_OT_OperatorBake(bpy.types.Operator):
    bl_idname = "object.voxelity_bake"
    bl_label = "Voxelity Bake Object"
    bl_description = "Bake voxel object including unsupported shader node colors"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        required_engine = 'CYCLES'
        if context.scene.render.engine != required_engine:
            create_generic_popup(message=f"The baking feature is only compatible with {required_engine}|Please switch 'Render Engine' to '{required_engine}'")
            return {'CANCELLED'}
        BakeUtility.settings_store()
        b = BakeUtility()
        try:
            BakeUtility.settings_init()
            bpy.ops.object.make_single_user(object=True, obdata=True)
            b.bake(context.selected_objects)
        except:
            raise
        finally:
            BakeUtility.settings_revert()
            #b.cleanup() # cannot delete the images generated because the object needs to be used for voxel color reading by user
        return {'FINISHED'}

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        if context.mode != 'OBJECT':
            return False
        active_object: bpy_types.Object = context.active_object
        for obj in context.selected_objects:
            if not obj.voxelized:
                return False
        if not active_object or not active_object.voxelized:
            return False
        return True

def register():
    bpy.utils.register_class(OBJECT_OT_OperatorBake)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_OperatorBake)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.object.voxelity_bake()