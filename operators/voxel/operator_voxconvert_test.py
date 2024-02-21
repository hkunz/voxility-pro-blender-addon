import bpy_types

from typing import List

from voxility_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxility_pro.operators.voxel.operator_voxconvert import OperatorVoxconvert

class OperatorVoxconvertTest(OperatorVoxconvert):
    bl_idname = "export.voxility_voxconvert_test"
    bl_label = "Voxconvert Test"
    bl_description = "Operator Voxconvert Test"
    bl_options = {'REGISTER'}

    def setup_command(self, _: str, __: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = self.command_builder
        c.test = True
        return c

    def execute(self, _: bpy_types.Context) -> set[str]:
        self.setup_command(None, None)
        self.execute_voxconvert()
        self.report({'INFO'}, f"Voxconvert Test Success")
        return {'FINISHED'}

    @classmethod
    def poll(cls, _: bpy_types.Context) -> bool:
        return True