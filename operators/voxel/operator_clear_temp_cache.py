import bpy
import bpy_types

from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.operators.operator_generic_popup import OperatorGenericPopup

class FILE_OT_ClearTempCacheOperator(OperatorGenericPopup):
    bl_idname = "file.voxility_clear_temp_cache"
    bl_label = "Clear Voxility Pro Cache"
    bl_description = "Delete temporary Voxility Pro directories of current Blender and Voxility Pro version"
    bl_options = {'REGISTER'}

    def draw(self, context: bpy_types.Context) -> None:
        self.message = "Delete temporary Voxility Pro directories?"
        self.exec_message = "Deleted temporary Voxility Pro directories"
        super().draw(context)

    def execute(self, context:bpy_types.Context) -> set[str]:
        TempFileManager().clear_temp_directories()
        super().execute(context)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearTempCacheOperator)