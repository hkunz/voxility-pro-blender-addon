import bpy
import glob
import os
import platform

from typing import List

from voxility_pro.utils.utils import Utils # type: ignore
from voxility_pro.exceptions.voxconvert_exe_missing_error import VoxConvertExeMissingError # type: ignore

class FileUtils:

    @staticmethod
    def get_addon_root_dir() -> str:
        # __file__ = C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\voxility_pro\utils.py
        script_directory: str = os.path.dirname(os.path.abspath(__file__))
        addon_directory: str = os.path.dirname(script_directory)
        return addon_directory

    @staticmethod
    def check_exe_match(matches: List[str], voxconvert_version: str) -> None:
        if len(matches) == 0:
            raise VoxConvertExeMissingError(voxconvert_version)

    @staticmethod
    def get_system() -> str:
        return platform.system().lower()

    @staticmethod
    def get_voxconvert_filepath() -> str:
        addon_root: str = FileUtils.get_addon_root_dir()
        system: str = FileUtils.get_system()
        voxconvert_version: str = Utils.get_voxconvert_version()
        exe_base_dir: str = "executable"
        exe_base_name: str = "voxconvert"

        if system == "darwin":
            matching_files: List[str] = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", f"{system}*", f"*{exe_base_name}*", "Contents", "MacOS", f"*{exe_base_name}*"))
            FileUtils.check_exe_match(matching_files, voxconvert_version)
            return os.path.join(addon_root, matching_files[0])

        if system == "windows":
            matching_files: List[str] = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", f"{system}*", f"*{exe_base_name}*"))
            FileUtils.check_exe_match(matching_files, voxconvert_version)
            return os.path.join(addon_root, matching_files[0])

        return "vengi-voxconvert"

    @staticmethod
    def check_filepath(path: str, ext: str) -> str:
        if os.path.isdir(path):
            path = os.path.join(path, f"untitled{ext}")
        elif not path or os.path.isdir(path):
            path = os.path.join(bpy.path.abspath("//"), f"untitled{ext}")
        return path

    @staticmethod
    def get_file_size(file_path: str) -> str:
        size: str = None
        try:
            size_in_bytes: int = os.path.getsize(file_path)
            if size_in_bytes < 1024:
                size = f"{size_in_bytes} bytes"
            elif size_in_bytes < 1024 * 1024:
                size = f"{size_in_bytes / 1024:.2f} KB"
            elif size_in_bytes < 1024 * 1024 * 1024:
                size = f"{size_in_bytes / (1024 * 1024):.2f} MB"
            else:
                size = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
        except FileNotFoundError:
            pass
        finally:
            pass
        return size

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        return os.path.splitext(file_path)[1][1:].lower()