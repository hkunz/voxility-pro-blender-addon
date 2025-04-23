import bpy

from voxelity_pro.operators.common.handler_interface import IHandler
from voxelity_pro.operators.common.context.context_script_executer import ContextScriptExecuter
from voxelity_pro.enums.area_type import AreaType

class ObjectImportLimitedDissolveHandler(IHandler):
    def __init__(self, object: bpy.types.Object):
        self.object: bpy.types.Object = object

    def execute_handler(self) -> None:
         bpy.ops.object.mode_set(mode='EDIT')
         ContextScriptExecuter(
            area_type = AreaType.VIEW_3D.name,
            script = lambda override: (
                bpy.ops.mesh.dissolve_limited(override)
                if override.legacy
                else bpy.ops.mesh.dissolve_limited()
            )
        ).execute_script()
         bpy.ops.object.mode_set(mode='OBJECT')