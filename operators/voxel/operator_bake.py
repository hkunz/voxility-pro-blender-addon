import bpy
import bpy_types

from voxility_pro.utils.voxel.bake_utility import BakeUtility # type: ignore
from voxility_pro.operators.operator_generic_popup import create_generic_popup # type: ignore

class OBJECT_OT_OperatorBake(bpy.types.Operator):
    bl_idname = "object.voxility_bake"
    bl_label = "Voxility Bake Object"
    bl_description = "Bake voxel object including unsupported shader node colors"
    bl_options = {'REGISTER','UNDO'}

    def execute(self, context):
        required_engine = 'CYCLES'
        if context.scene.render.engine != required_engine:
            create_generic_popup(message=f"The baking feature compatible with {required_engine} only.|Please switch 'Render Engine` to '{required_engine}'")
            return {'CANCELLED'}
        BakeUtility.settings_init()
        b = BakeUtility()
        b.bake(context.selected_objects)
        BakeUtility.settings_revert()
        #b.cleanup() # cannot delete the images generated because the object needs to be used for voxel color reading by user
        return {'FINISHED'}

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        active_object: bpy_types.Object = context.active_object
        for obj in context.selected_objects:
            if not obj.voxelized:
                return False
        if not active_object or not active_object.voxelized:
            return False
        return super().poll(context)

def register():
    bpy.utils.register_class(OBJECT_OT_OperatorBake)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_OperatorBake)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.object.voxility_bake()