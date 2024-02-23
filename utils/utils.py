import bpy
import re

from typing import List, Callable, Any, Tuple

from voxility_pro import bl_info

def get_addon_module_name() -> str:
    return "voxility_pro"

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