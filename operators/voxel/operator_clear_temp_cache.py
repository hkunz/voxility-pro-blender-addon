import bpy

from voxelity_pro.utils.temp_file_manager import TempFileManager
from voxelity_pro.operators.operator_generic_popup import OperatorGenericPopup

class FILE_OT_ClearTempCacheOperator(OperatorGenericPopup):
    bl_idname = "file.voxelity_clear_temp_cache"
    bl_label = "Clear Voxelity Pro Cache"
    bl_description = "Delete temporary Voxelity Pro directories of current Blender and Voxelity Pro version"
    bl_options = {'REGISTER'}

    def draw(self, context: bpy.types.Context) -> None:
        self.message = "Delete temporary Voxelity Pro directories?"
        self.exec_message = "Deleted temporary Voxelity Pro directories"
        super().draw(context)

    def execute(self, context:bpy.types.Context) -> set[str]:
        TempFileManager().clear_temp_directories()
        super().execute(context)
        return {'FINISHED'}

def register() -> None:
    bpy.utils.register_class(FILE_OT_ClearTempCacheOperator)

def unregister() -> None:
    bpy.utils.unregister_class(FILE_OT_ClearTempCacheOperator)