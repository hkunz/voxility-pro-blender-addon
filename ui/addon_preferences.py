import bpy

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "voxility_pro" # __name__

    magica_voxel_enable: bpy.props.BoolProperty(
        name="Enable MagicaVoxel",
        default=True,
        #update=update_type_vox
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    qubicle_binary_enable: bpy.props.BoolProperty(
        name="Enable Qubicle Binary Exchange",
        default=True,
        #update=update_type_qb
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        #layout.label(text="Default Export Formats:")
        #layout.prop(self, "magica_voxel_enable")
        #layout.prop(self, "qubicle_binary_enable")