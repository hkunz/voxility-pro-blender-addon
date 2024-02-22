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

def is_class_registered(cls) -> bool:
    return True
    #FIXME: bpy.ops.import is invalid syntax
    idname: str = eval(f"bpy.ops.{cls.bl_idname}.idname()")
    return hasattr(bpy.types, idname)

def try_register_operator(cls) -> None:
    try:
        bpy.utils.register_class(cls)
    except:
        pass

def try_unregister_operator(cls) -> None:
    try:
        bpy.utils.unregister_class(cls)
    except:
        pass

def abstract_method(func: Callable) -> Callable[..., Any]:
    #@wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"{func.__name__} must be overridden in subclass.")
    return wrapper