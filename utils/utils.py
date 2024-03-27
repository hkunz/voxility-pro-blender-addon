import bpy
import re

from typing import List, Callable, Any, Tuple

from voxility_pro import bl_info # type: ignore

def get_addon_module_name() -> str:
    return "voxility_pro"

def get_blender_version(prependv: bool=True, separator: str='.') -> str:
    v: Tuple[int, int, int] = bpy.app.version
    version: str = f"{v[0]}{separator}{v[1]}{separator}{v[2]}"
    return ('v' if prependv else '') + version

def get_addon_version(prependv: bool=True, separator: str='.') -> str:
    return ('v' if prependv else '') + separator.join(map(str, bl_info['version']))

def get_gn_voxelizer_version(): # version of generate_gn_voxelize_X_X.py
    v: Tuple[int, int, int] = bpy.app.version
    if v >= (4, 0, 0):
        return '4_0'
    elif v >= (3, 4, 0):
        return '3_4'
    elif v >= (3, 3, 0):
        return '3_3'
    elif v >= (3, 1, 0):
        return '3_1'
    else:
        pass
    return '2_93'

def get_voxconvert_version() -> str:
    pattern = r' voxconvert-(\d+\.\d+\.\d+(?:-.*)?)$'
    match = re.search(pattern, bl_info["description"])
    version = match.group(1)
    return version

def get_voxconvert_author() -> str:
    return "Martin Gerhardy"

def get_preferences_voxel_types() -> List[str]:
    addon: bpy.types.Addon = bpy.context.preferences.addons[get_addon_module_name()]
    addon_prefs = addon.preferences
    types: List[str] = []
    for prop_name in addon_prefs.CHECKBOXES:
        if getattr(addon_prefs, prop_name):
            types.append(prop_name.split("_")[1])
    return types

def is_class_registered(cls) -> bool:
    idname_py = cls.bl_idname
    module, op = idname_py.split(".")
    idname = module.upper() + "_" + "OT" + "_" + op
    return hasattr(bpy.types, idname)

def try_register_operator(cls) -> None:
    if not is_class_registered(cls):
        bpy.utils.register_class(cls)

def try_unregister_operator(cls) -> None:
    if is_class_registered(cls):
        bpy.utils.unregister_class(cls)

def abstract_method(func: Callable) -> Callable[..., Any]:
    #@wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"{func.__name__} must be overridden in subclass.")
    return wrapper