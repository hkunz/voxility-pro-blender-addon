import bpy

from typing import List

from voxelity_pro.utils.utils import Utils
from voxelity_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxelity_pro.operators.voxel.operator_voxconvert import OperatorVoxconvert

class OperatorVoxconvertTest(OperatorVoxconvert):
    bl_idname = "export.voxelity_voxconvert_test"
    bl_label = "Voxconvert Test"
    bl_description = "Operator Voxconvert Test"
    bl_options = {'REGISTER'}

    def setup_command(self, _: str, __: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = self.command_builder
        c.test = True
        return c

    def execute(self, _: bpy.types.Context) -> set[str]:
        self.setup_command(None, None)
        success = self.execute_voxconvert()
        voxconvert_version: str = Utils.get_voxconvert_version()
        if success:
            self.report({'INFO'}, f"Voxconvert Test Success ({voxconvert_version})")
        else:
            self.report({'ERROR'}, f"Voxconvert Test Failed")
        return {'FINISHED'}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        super().invoke(context, event)
        return self.execute(context)

    @classmethod
    def poll(cls, _: bpy.types.Context) -> bool:
        return True