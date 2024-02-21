import bpy
import bpy_types
import os
import shutil

from os import path as p
from typing import List

from voxility_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu

class OBJECT_OT_MeshVoxelSaveOperator(bpy.types.Operator):
    bl_idname = "object.voxility_mesh_voxel_save"
    bl_label = "Save"
    bl_description = "Save the voxelized mesh as specified in target voxel format"

    VOX_TARGET_FORMAT_CURRENT_SELECTION: str = VoxelFormatsExportMenu.get_formats_list_value()
    VOX_TARGET_FORMAT_EXT: str = VoxelFormatsExportMenu.get_formats_list_value()
    VOX_OUTPUT_PATH: str = None

    directory: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory where the voxelized mesh will be saved",
        subtype='DIR_PATH'
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    filter_folder: bpy.props.BoolProperty(
        default=True,
        options={"HIDDEN"}
    ) # type: ignore

    option_overwrite: bpy.props.BoolProperty(
        name="Overwrite Files & Folders",
        description=("Overwrite files and folders with same name"),
        default=True,
    ) # type: ignore

    def draw(self, context: bpy_types.Context) -> None:
        col = self.layout.column()
        sub = col.row()
        sub.enabled = False
        sub.prop(self, "option_overwrite")

    def execute(self, _: bpy_types.Context) -> set[str]:
        temp_dir = os.path.dirname(OBJECT_OT_MeshVoxelSaveOperator.VOX_OUTPUT_PATH)
        print("Temporary contents in temp directory:", temp_dir)
        print("Save contents to destination directory:", self.directory)
        shutil.copytree(src=temp_dir, dst=self.directory, dirs_exist_ok=True)
        self.report({'INFO'}, f"Files saved in {self.directory}")
        return {'FINISHED'}

    @classmethod
    def poll(cls, _: bpy_types.Context) -> bool:
        none: str = VoxelFormatsExportMenu.get_formats_list_value()
        if cls.VOX_TARGET_FORMAT_EXT == none or cls.VOX_TARGET_FORMAT_CURRENT_SELECTION == none:
            return False
        if cls.VOX_TARGET_FORMAT_EXT != cls.VOX_TARGET_FORMAT_CURRENT_SELECTION:
            return False
        if not p.exists(cls.VOX_OUTPUT_PATH):
            return False
        return True

    def invoke(self, context: bpy_types.Context, _: bpy.types.Event) -> set[str]:
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register() -> None:
    bpy.utils.register_class(OBJECT_OT_MeshVoxelSaveOperator)

def unregister() -> None:
    bpy.utils.unregister_class(OBJECT_OT_MeshVoxelSaveOperator)