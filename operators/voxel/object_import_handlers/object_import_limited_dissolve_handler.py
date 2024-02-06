import bpy

from voxility_pro.operators.handler_interface import IHandler
from voxility_pro.context.context_script_executer import ContextScriptExecuter
from voxility_pro.enums.area_type import AreaType

class ObjectImportLimitedDissolveHandler(IHandler):
    def __init__(self, object):
        self.object = object

    def execute_handler(self):
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