import bpy

class OBJECT_OT_OperatorEmpty(bpy.types.Operator):
    bl_idname = "object.voxility_null_operator"
    bl_label = "Disabled Button"
    bl_description = "Disabled Button"
    bl_options = {'INTERNAL'}

    def execute(self, _context):
        return {'FINISHED'}

    @classmethod
    def poll(cls, _context):
        return False