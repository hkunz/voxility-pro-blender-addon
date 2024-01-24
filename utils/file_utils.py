import bpy
import glob
import os
import platform

from vox_exporter.utils.utils import get_voxconvert_version
from vox_exporter.exceptions.voxconvert_exe_missing_error import VoxConvertExeMissingError

def get_addon_root_dir():
    # __file__ = C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\vox_exporter\utils.py
    script_directory = os.path.dirname(os.path.abspath(__file__))
    addon_directory = os.path.dirname(script_directory)
    return addon_directory

def check_exe_match(matches, voxconvert_version):
    if len(matches) == 0:
        raise VoxConvertExeMissingError(voxconvert_version)

def get_voxconvert_filepath():
    addon_root = get_addon_root_dir()
    system = platform.system().lower()
    voxconvert_version = get_voxconvert_version()
    exe_base_dir = "executable"
    exe_base_name = "voxconvert"

    if system == "darwin":
        matching_files = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", system, f"*{exe_base_name}*", "Contents", "MacOS", f"*{exe_base_name}*"))
        check_exe_match(matching_files, voxconvert_version)
        return os.path.join(addon_root, matching_files[0]).replace(" ", "\ ")

    if system == "windows":
        matching_files = glob.glob(os.path.join(addon_root, f"*{exe_base_dir}*", f"*{voxconvert_version}*", system, f"*{exe_base_name}*"))
        check_exe_match(matching_files, voxconvert_version)
        return os.path.join(addon_root, matching_files[0])

    return "vengi-voxconvert"

def check_filepath(path, ext):
    if os.path.isdir(path):
        path = os.path.join(path, f"untitled{ext}")
    elif not path or os.path.isdir(path):
        path = os.path.join(bpy.path.abspath("//"), f"untitled{ext}")
    return path

def get_file_size(file_path):
    try:
        size_in_bytes = os.path.getsize(file_path)
        if size_in_bytes < 1024:
            size = f"{size_in_bytes} bytes"
        elif size_in_bytes < 1024 * 1024:
            size = f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            size = f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            size = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
        return size
    except FileNotFoundError:
        return None
