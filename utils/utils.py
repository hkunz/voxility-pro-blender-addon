import bpy
import re

from typing import Callable, Any, Tuple

from voxility_pro import bl_info

def get_blender_version(prependv: bool=True) -> str:
    v: Tuple[int, int, int] = bpy.app.version
    version: str = f"{v[0]}.{v[1]}.{v[2]}"
    return ('v' if prependv else '') + version

def get_addon_version(prependv: bool=True) -> str:
    return ('v' if prependv else '') + '.'.join(map(str, bl_info['version']))

def get_voxconvert_version() -> str:
    pattern = r' voxconvert-(\d+\.\d+\.\d+(?:-.*)?)$'
    match = re.search(pattern, bl_info["description"])
    version = match.group(1)
    return version

def abstract_method(func: Callable) -> Callable[..., Any]:
    #@wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"{func.__name__} must be overridden in subclass.")
    return wrapper