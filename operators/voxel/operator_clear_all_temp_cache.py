import bpy
import bpy_types

from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.operators.operator_generic_popup import create_generic_popup

class FILE_OT_ClearAllTempCacheOperator(bpy.types.Operator):
    bl_idname = "file.voxility_clear_all_temp_cache"
    bl_label = "Clear All Temporary Voxility Pro Cache"
    bl_description = "Delete all temporary Voxility Pro cache directories regardless of Blender or Voxility Pro versions"
    bl_options = {'REGISTER'}

    def __init__(self) -> None:
        super().__init__()

    def execute(self, _:bpy_types.Context) -> set[str]:
        TempFileManager().clear_all_temp_directories()
        create_generic_popup("Deleted all temporary Voxility Pro directories")
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearAllTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearAllTempCacheOperator)