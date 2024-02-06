import bpy
import time
import subprocess
import platform

from abc import ABC, abstractmethod

from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder
from voxility_pro.translations import get_translation

class VoxconvertOperator(bpy.types.Operator):
    bl_description = "Voxconvert Operator"
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ""

    def __init__(self):
        super().__init__()
        self.voxconvert_duration = 0
        self.command_builder = VoxConvertCommandBuilder()

    def setup_command(self, input, output):
        return self.command_builder

    def execute_voxconvert(self):
        start_time = time.time()
        self.command_builder.build_command()
        success = True
        command = self.command_builder.get_command()
        command_str = self.command_builder.get_command_str()
        cmd = command if platform.system().lower() == "windows" else command_str
        print("\nExecute voxconvert command: ", command_str, '\n' + self.command_builder.get_formatted_args())
        self.report({'INFO'}, f"{get_translation('info_execute_command')} {command_str}")
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            success = False
            print(f"Error: Command exited with return code {e.returncode}")
            print(f"Standard Error: {e.stderr}")
            self.report({'ERROR'}, f"Error processing file: {self.command_builder.get_input_filepath()}")
        self.voxconvert_duration = time.time() - start_time
        print("executed successfully:", success)
        return success

    @abstractmethod
    def execute(_self, _context):
        pass