import bpy
import time
import subprocess
import os

from typing import List

from voxelity_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder
from voxelity_pro.translation.translations import get_translation
from voxelity_pro.utils.file_utils import FileUtils

class OperatorVoxconvert(bpy.types.Operator):
    bl_description = "Operator Voxconvert"
    bl_options = {'INTERNAL', 'UNDO'}
    filename_ext: str = ""

    def setup_command(self, input: str, outputs: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = self.command_builder
        c.vc_input_path = input
        c.vc_output_paths = outputs
        return c

    def get_script_args(self, system, c):
        command: List[str] = c.get_command()
        command_str: str = c.get_command_str()
        print("exec command: ", command_str)
        args = ["-command", command[0], "-command_str", command_str] if system == "windows" else [command[0], command_str]
        return args

    def get_script_path(self, system):
        file = "voxconvert.ps1" if system == "windows" else "voxconvert.zsh"
        script_path = os.path.join(FileUtils.get_addon_root_dir(), f"scripts/voxconvert/{system}/{file}")
        return script_path

    def get_command(self, system, c):
        if system != "windows":
            system = "unix"
        args = self.get_script_args(system, c)
        script_path = self.get_script_path(system)
        cmd = ["powershell", "-File", script_path] if system == "windows" else ["zsh", script_path]
        return cmd + list(args)

    def execute_voxconvert(self) -> bool:
        start_time: float = time.time()
        system = FileUtils.get_system()
        c:VoxconvertCommandBuilder = self.command_builder
        c.build_command(system)
        success: bool = True
        command = self.get_command(system, c)
        try:
            result = subprocess.run(command, shell=False, check=True, capture_output=True, text=True)
            #raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="Simulated error")
        except subprocess.CalledProcessError as e:
            success = False
            self.on_script_exit_error(c, e)
        self.voxconvert_duration = time.time() - start_time
        
        print("executed successfully:", c.test or success)
        if success:
            self.on_script_exit_success(c, result.stdout)
        return success

    def on_script_exit_success(self, c, stdout):
        self.report({'INFO'}, stdout)

    def on_script_exit_error(self, c, e):
        exit_code = e.returncode
        self.report({'ERROR'}, f"Error: Command exited with return code {exit_code}")
        self.report({'ERROR'}, f"Standard Error: {e.stderr}")
        if not c.test:
            self.report({'ERROR'}, f"Error processing file: {c.get_input_filepath()}")

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> set[str]:
        self.voxconvert_duration: int = 0
        self.command_builder: VoxconvertCommandBuilder = VoxconvertCommandBuilder()
        return {'FINISHED'}

    def execute(self, context: bpy.types.Context) -> set[str]:
        raise NotImplementedError("Subclasses must implement the execute() method")

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        active_object: bpy.types.Object = context.active_object
        selected_objects: List[bpy.types.Object] = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for obj in selected_objects:
            if obj.type != 'MESH' or not obj.data.polygons:
                return False
        return True