# https://blender.stackexchange.com/questions/310837/camera-wont-be-aligned-to-current-view-with-python-scripting

import bpy
import bpy_types

from typing import List, Tuple

class ProCameraPanel(bpy.types.Panel):
    bl_label = "Pro Camera"
    bl_idname = "PT_ProCameraPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context: bpy_types.Context) -> None:
        layout: bpy.types.UILayout = self.layout

        # Add a new camera
        layout.label(text="Add a new Camera")
        layout.operator("scene.assign_camera", text="Assign a Camera")

        layout.separator()

        # Select a camera lens
        layout.label(text="Select a camera Lens:")
        layout.prop(context.scene, "pro_camera_lens", text="Lens")

        # Add a horizontal line
        layout.separator()

        # Enable/Disable Depth of Field checkbox
        layout.prop(context.scene.camera.data.dof, "use_dof", text="Enable DOF")

        # Focus on Object field
        layout.prop_search(context.scene.camera.data.dof, "focus_object", context.scene, "objects", text="Focus on Object")


class OBJECT_OT_assign_camera(bpy.types.Operator):
    bl_idname = "scene.assign_camera"
    bl_label = "Assign a Camera"

    def execute(self, context: bpy_types.Context) -> set[str]:
        # Add a new camera
        camera_data: bpy.types.Camera = bpy.data.cameras.new(name="Camera")
        if camera_data is None:
            return {"CANCELLED"}

        my_camera: bpy.types.Camera = bpy.data.objects.new("Camera", camera_data)

        if my_camera is None:
            return {"CANCELLED"}

        bpy.context.scene.collection.objects.link(my_camera)
        context.scene.camera = my_camera

        # Align the new camera to view
        bpy.ops.view3d.camera_to_view()

        return {"FINISHED"}

def update_camera_lens(_self, context: bpy_types.Context) -> None:
    selected_lens = context.scene.pro_camera_lens

    # Set the active camera's lens based on the selected option
    if context.scene.camera:
        if selected_lens == 'WIDE':
            context.scene.camera.data.lens = 24.0
        elif selected_lens == 'STANDARD':
            context.scene.camera.data.lens = 50.0
        elif selected_lens == 'PORTRAIT':
            context.scene.camera.data.lens = 80.0
        elif selected_lens == 'TELE':
            context.scene.camera.data.lens = 135.0
        elif selected_lens == 'SUPER_TELE':
            context.scene.camera.data.lens = 240.0

# Define the camera lens options
lens_options: List[Tuple[str, str, str]] = [
    ('WIDE', 'Wide - 24mm', 'Wide angle lens - 24mm'),
    ('STANDARD', 'Standard - 50mm', 'Standard lens - 50mm'),
    ('PORTRAIT', 'Portrait - 80mm', 'Portrait lens - 80mm'),
    ('TELE', 'Tele - 135mm', 'Telephoto lens - 135mm'),
    ('SUPER_TELE', 'Super Tele - 240mm', 'Super Telephoto lens - 240mm'),

]

def register() -> None:
    bpy.utils.register_class(ProCameraPanel)
    bpy.utils.register_class(OBJECT_OT_assign_camera)
    bpy.types.Scene.pro_camera_lens = bpy.props.EnumProperty(
        items=lens_options,
        name="Camera Lens",
        description="Select a camera lens",
        default='WIDE',
        update=update_camera_lens
    )

def unregister() -> None:
    bpy.utils.unregister_class(ProCameraPanel)
    bpy.utils.unregister_class(OBJECT_OT_assign_camera)
    del bpy.types.Scene.pro_camera_lens

if __name__ == "__main__":
    register()