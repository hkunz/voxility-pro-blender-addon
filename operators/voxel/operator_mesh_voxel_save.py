import bpy
import bpy_types

from os import path as p
from typing import List

from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.ui.voxel_formats_export_menu import VoxelFormatsExportMenu

class OBJECT_OT_MeshVoxelSaveOperator(bpy.types.Operator):
    bl_idname = "object.voxility_mesh_voxel_save"
    bl_label = "Voxility Pro Save Voxelized Mesh"
    bl_description = "Save the voxelized mesh as specified in target voxel format"

    VOX_TARGET_FORMAT_CURRENT_SELECTION = VoxelFormatsExportMenu.get_formats_list_value()
    VOX_TARGET_FORMAT_EXT = VoxelFormatsExportMenu.get_formats_list_value()
    VOX_OUTPUT_PATH = None

    def execute(self, context: bpy_types.Context) -> set[str]:
        return {'FINISHED'}

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        none: str = VoxelFormatsExportMenu.get_formats_list_value()
        if cls.VOX_TARGET_FORMAT_EXT == none or cls.VOX_TARGET_FORMAT_CURRENT_SELECTION == none:
            return False
        if cls.VOX_TARGET_FORMAT_EXT != cls.VOX_TARGET_FORMAT_CURRENT_SELECTION:
            return False
        if not p.exists(cls.VOX_OUTPUT_PATH):
            return False
        return True

def register() -> None:
    bpy.utils.register_class(OBJECT_OT_MeshVoxelSaveOperator)

def unregister() -> None:
    bpy.utils.unregister_class(OBJECT_OT_MeshVoxelSaveOperator)