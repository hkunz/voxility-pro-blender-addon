import bpy

class GenericPopupOperator(bpy.types.Operator):
    bl_idname = "object.generic_popup_operator"
    bl_label = "Voxility Pro Message"
    bl_description = "Generic Popup Operator for displaying a custom message"

    message: bpy.props.StringProperty(name="Message")

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text=self.message)

    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(GenericPopupOperator)

def unregister():
    bpy.utils.unregister_class(GenericPopupOperator)

def create_generic_popup(message):
    bpy.ops.object.generic_popup_operator('INVOKE_DEFAULT', message=message)