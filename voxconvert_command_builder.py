import platform

from voxility_pro.utils.file_utils import get_voxconvert_filepath

class VoxConvertCommandBuilder:
    def __init__(self,
            input_filepath,
            output_filepath,
            voxformat_scale=1.0,
            palette_file=None,
            export_palette=False,
            surface_only=False,
            voxformat_voxelizemode=0
        ):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.voxformat_scale = round(voxformat_scale, 2)
        self.palette_file = palette_file
        self.export_palette = export_palette
        self.surface_only = surface_only
        self.voxformat_voxelizemode = voxformat_voxelizemode

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
        command = []
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
        command.append(str(self.voxformat_scale))
        command.append("-set")
        command.append("voxformat_voxelizemode")
        command.append(str(self.voxformat_voxelizemode))

        if self.palette_file:
            command.append("-set")
            command.append("palette")
            command.append(self.palette_file)

        if self.export_palette:
            command.append("--export-palette")

        if self.surface_only:
            command.append("--surface_only")

        command.append("--input")
        command.append(f'"{self.input_filepath}"')
        command.append("--output")
        command.append(f'"{self.output_filepath}"')
        command.append("--force")

        return command
