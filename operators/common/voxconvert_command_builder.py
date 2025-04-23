import platform
import re

from typing import List

from voxelity_pro.utils.file_utils import FileUtils # type: ignore

class VoxconvertCommandBuilder:
    def __init__(self) -> None:

        self.test = False

        self.vc_input_path: str = None
        self.vc_output_paths: List[str] = None
        self.vc_voxformat_voxelizemode: int = 0
        self.vc_merge_vertices: int = 0
        self.vc_voxformat_withcolor: int = 0
        self.vc_voxformat_scale: float = 1.0
        self.vc_palette_file: str = "built-in:nippon"
        self.vc_export_palette: bool = False
        self.vc_surface_only: int = 0
        self.vc_voxformat_ambientocclusion: int = 0
        self.vc_voxformat_mergequads: int = 0
        self.vc_core_colorreduction: bool = False
        self.vc_force_overwrite: bool = True
        self.vc_fillhollow: bool = False # actually this is useless, no effect. we use vc_script="fillhollow"
        self.vc_script: str = None

        self.vc_command: List[str] = None

    # ====================================================================
    # Documentation https://vengi-voxel.github.io/vengi/Configuration/
    #
    # linux: call vengi-voxconvert from anywhere
    # darwin:
    #   relative: open -a "appname" --args arg1 argn
    #   absolute: open "/full/path/to/appname.app" --args arg1 argn
    # windows: exe_path arg1 arg2 argn
    # ====================================================================

    def build_command(self, system) -> List[str]:
        self.vc_command = []
        command: List[str] = self.vc_command
        exe: str = FileUtils.get_voxconvert_filepath(system)

        if system == "windows":
            #command.append('powershell')
            #command.append('-Command')
            command.append(f'& "{exe}"')
        else:
            command.append(exe.replace(" ", "\ "))

        if self.test:
            command.append("--version")
            return command

        if self.vc_script:
            command.append("--script")
            command.append(self.vc_script)

        command.append("-set")
        command.append("metric_flavor")
        command.append("json")
        command.append("-set")
        command.append("voxformat_scale")
        command.append(str(round(self.vc_voxformat_scale, 2)))
        command.append("-set")
        command.append("voxformat_voxelizemode")
        command.append(str(self.vc_voxformat_voxelizemode))
        command.append("-set")
        command.append("voxformat_ambientocclusion")
        command.append(str(self.vc_voxformat_ambientocclusion))
        command.append("-set")
        command.append("voxformat_withcolor")
        command.append(str(self.vc_voxformat_withcolor))
        command.append("-set")
        command.append("voxformat_mergequads")
        command.append(str(self.vc_voxformat_mergequads))

        if self.vc_core_colorreduction:
            command.append("-set")
            command.append("core_colorreduction")
            command.append("KMeans")

        if self.vc_palette_file:
            command.append("-set")
            command.append("palette")
            command.append(self.vc_palette_file)

        if self.vc_export_palette:
            command.append("--export-palette")

        if self.vc_surface_only:
            command.append("--surface-only")

        if self.vc_fillhollow:
            command.append("-set")
            command.append("voxformat_fillhollow")
            command.append("1")

        if self.vc_merge_vertices:
            pass #command.append("--merge") #https://github.com/vengi-voxel/vengi/issues/389

        if self.vc_input_path:
            command.append("--input")
            command.append(f'"{self.vc_input_path}"')

        for output_path in self.vc_output_paths:
            command.append("--output")
            command.append(f'"{output_path}"')

        if self.vc_force_overwrite:
            command.append("--force")

        return command

    def get_command(self) -> List[str]:
        return self.vc_command

    def get_command_str(self) -> str:
        return ' '.join(self.vc_command)

    def get_input_filepath(self) -> str:
        return self.vc_input_path

    def get_formatted_args(self) -> str:
        command_str: str = self.get_command_str()
        vox_index: int = command_str.find("vox")
        split_args: List[str] = re.split(r' (?=-|--)', command_str[vox_index:])
        return '\n'.join(split_args[1:])