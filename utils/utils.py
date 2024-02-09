import re

from voxility_pro import bl_info

def get_addon_version(prependv = True):
    return ('v' if prependv else '') + '.'.join(map(str, bl_info['version']))

def get_voxconvert_version():
    pattern = r' voxconvert-(\d+\.\d+\.\d+(?:-.*)?)$'
    match = re.search(pattern, bl_info["description"])
    version = match.group(1)
    return version

def abstract_method(func):
    #@wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"{func.__name__} must be overridden in subclass.")
    return wrapper