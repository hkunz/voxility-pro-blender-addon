import bpy
import os
import platform
import glob

from vox_exporter.utils import get_addon_root_dir
from vox_exporter.translations import get_translation

class VoxConvertCommandBuilder:
    def __init__(self, filepath, obj_path, palette_file=None, export_palette=False, surface_only=False):
        self.filepath = filepath
        self.obj_path = obj_path
        self.palette_file = palette_file
        self.export_palette = export_palette
        self.surface_only = surface_only

    def build_command(self):
        addon_root = get_addon_root_dir()

        palette_file = self.palette_file if self.palette_file else "palette-nippon.png"

        system = platform.system().lower()
        voxconvert_version = ""
        exe_base_dir = "executable"
        exe_base_name = "voxconvert"
        matching_files = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", system, f"*{exe_base_name}*"))

        assert len(matching_files) != 0, get_translation('error_no_converter_exe')

        exe = matching_files[0]

        command = [
            os.path.join(addon_root, exe),
            "-set", f"palette {palette_file}",
            "--export-palette" if self.export_palette else " ",
            "--surface_only" if self.surface_only else " ",
            "--input", self.obj_path,
            "--output", self.filepath,
            "--force"
        ]
        return command
