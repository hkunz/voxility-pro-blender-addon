import bpy
import time
import subprocess
import platform
import bpy_types

from typing import List
from abc import ABC, abstractmethod

from voxility_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxility_pro.translation.translations import get_translation

class OperatorVoxconvert(bpy.types.Operator):
    bl_description = "Operator Voxconvert"
    bl_options = {'INTERNAL', 'UNDO'}
    filename_ext: str = ""

    def __init__(self) -> None:
        super().__init__()
        self.voxconvert_duration: int = 0
        self.command_builder: VoxconvertCommandBuilder = VoxconvertCommandBuilder()

    def setup_command(self, input: str, outputs: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = self.command_builder
        c.vc_input_path = input
        c.vc_output_paths = outputs
        return c

    def execute_voxconvert(self) -> bool:
        start_time: float = time.time()
        c:VoxconvertCommandBuilder = self.command_builder
        c.build_command()
        success: bool = True
        command: List[str] = c.get_command()
        command_str: str = c.get_command_str()
        cmd: str = command if platform.system().lower() == "windows" else command_str
        print("\nExecute voxconvert command: ", command_str, '\n' + c.get_formatted_args())
        self.report({'INFO'}, f"{get_translation('info_execute_command')} {command_str}")
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            success = False
            print(f"Error: Command exited with return code {e.returncode}")
            print(f"Standard Error: {e.stderr}")
            if not c.test:
                self.report({'ERROR'}, f"Error processing file: {c.get_input_filepath()}")
        self.voxconvert_duration = time.time() - start_time
        print("executed successfully:", success)
        return success

    @abstractmethod
    def execute(_self, _context: bpy_types.Context) -> set[str]:
        pass

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        active_object: bpy_types.Object = context.active_object
        selected_objects: List[bpy_types.Object] = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for obj in selected_objects:
            if obj.type != 'MESH' or not obj.data.polygons:
                return False
        return True