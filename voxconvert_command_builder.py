import platform
import re

from voxility_pro.utils.file_utils import get_voxconvert_filepath

class VoxConvertCommandBuilder:
    def __init__(self):

        self.vc_input_path = None
        self.vc_output_path = None
        self.vc_voxformat_voxelizemode = 0
        self.vc_merge_vertices = 0
        self.vc_voxformat_withcolor = 0
        self.vc_voxformat_scale = 1.0
        self.vc_palette_file = None
        self.vc_export_palette = "palette-nippon.png"
        self.vc_surface_only = 0
        self.vc_voxformat_ambientocclusion = 0
        self.vc_voxformat_mergequads = 0

        self.vc_command = None

    # ====================================================================
    # Documentation https://vengi-voxel.github.io/vengi/Configuration/
    #
    # linux: call vengi-voxconvert from anywhere
    # darwin:
    #   relative: open -a "appname" --args arg1 argn
    #   absolute: open "/full/path/to/appname.app" --args arg1 argn
    # windows: exe_path arg1 arg2 argn
    # ====================================================================

    def build_command(self):
        command = self.vc_command = []
        system = platform.system().lower()
        exe = get_voxconvert_filepath()

        if system == "windows":
            command.append('powershell')
            command.append('-Command')
            command.append(f'& "{exe}"')
        else:
            command.append(exe)

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

        if self.vc_palette_file:
            command.append("-set")
            command.append("palette")
            command.append(self.palette_file)

        if self.vc_export_palette:
            command.append("--export-palette")

        if self.vc_surface_only:
            command.append("--surface-only")

        if self.vc_merge_vertices:
            command.append("--merge")

        command.append("--input")
        command.append(f'"{self.vc_input_path}"')
        command.append("--output")
        command.append(f'"{self.vc_output_path}"')
        command.append("--force")

        return command

    def get_command(self):
        return self.vc_command

    def get_command_str(self):
        return ' '.join(self.vc_command)

    def get_input_filepath(self):
        return self.vc_input_path

    def get_formatted_args(self):
        command_str = self.get_command_str()
        vox_index = command_str.find("vox")
        split_args = re.split(r' (?=-|--)', command_str[vox_index:])
        return "\nArguments:\n" + '\n'.join(split_args[1:])