import bpy
import bpy_types

class GenericPopupOperator(bpy.types.Operator):
    bl_idname = "object.generic_popup_operator"
    bl_label = "Voxility Pro Message"
    bl_description = "Generic Popup Operator for displaying a custom message"

    message: bpy.props.StringProperty(name="Message") # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        return (context.object is not None and
                context.object.type == 'MESH')

    def invoke(self, context: bpy_types.Context, _: bpy.types.Event) -> set[str]:
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, _: bpy_types.Context) -> None:
        layout: bpy.types.UILayout = self.layout
        col: bpy.types.UILayout = layout.column()
        col.label(text=self.message)

    def execute(self, _: bpy_types.Context) -> set[str]:
        self.report({'INFO'}, self.message)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(GenericPopupOperator)

def unregister() -> None:
    bpy.utils.unregister_class(GenericPopupOperator)

def create_generic_popup(message) -> None:
    bpy.ops.object.generic_popup_operator('INVOKE_DEFAULT', message=message)