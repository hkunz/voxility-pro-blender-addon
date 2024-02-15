import bpy
import bpy_types

from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.operators.generic_popup_operator import create_generic_popup

class FILE_OT_ClearTempCacheOperator(bpy.types.Operator):
    bl_idname = "file.voxility_clear_temp_cache"
    bl_label = "Clear Temporary Voxility Pro Cache"
    bl_description = "Delete temporary Voxility Pro directories of current Blender and Voxility Pro version"
    bl_options = {'REGISTER'}

    def __init__(self) -> None:
        super().__init__()

    def execute(self, _:bpy_types.Context) -> set[str]:
        TempFileManager().clear_temp_directories()
        create_generic_popup("Deleted temporary Voxility Pro directories")
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearTempCacheOperator)