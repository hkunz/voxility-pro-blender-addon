import bpy
import os
import platform
import glob

from vox_exporter.utils import get_addon_root_dir, get_voxconvert_version
from vox_exporter.translations import get_translation

class VoxConvertCommandBuilder:
    def __init__(self,
            filepath,
            obj_path,
            voxformat_scale=1.0,
            palette_file=None,
            export_palette=False,
            surface_only=False,
            voxformat_voxelizemode=0
        ):
        self.filepath = filepath
        self.obj_path = obj_path
        self.voxformat_scale = round(voxformat_scale, 2)
        self.palette_file = palette_file if palette_file else "palette-nippon.png"
        self.export_palette = export_palette
        self.surface_only = surface_only
        self.voxformat_voxelizemode = voxformat_voxelizemode

    def build_command(self):
        addon_root = get_addon_root_dir()

        system = platform.system().lower()
        voxconvert_version = get_voxconvert_version()
        exe_base_dir = "executable"
        exe_base_name = "voxconvert"
        matching_files = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", system, f"*{exe_base_name}*"))

        assert len(matching_files) != 0, get_translation('error_no_converter_exe')

        exe = "vengi-voxconvert" if system=="linux" else os.path.join(addon_root, matching_files[0])

        # Documentation https://vengi-voxel.github.io/vengi/Configuration/

        command = [exe]
        command.append("-set")
        command.append("voxformat_scale")
        command.append(str(self.voxformat_scale))
        command.append("-set")
        command.append("palette")
        command.append(self.palette_file)
        command.append("-set")
        command.append("voxformat_voxelizemode")
        command.append(str(self.voxformat_voxelizemode))



        if self.export_palette:
            command.append("--export-palette")

        if self.surface_only:
            command.append("--surface_only")

        command.append("--input")
        command.append(self.obj_path)
        command.append("--output")
        command.append(self.filepath)
        command.append("--force")

        return command
