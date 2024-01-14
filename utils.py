import os

def get_addon_root_dir():
    # __file__ = C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\addons\vox_exporter\utils.py
    return os.path.dirname(__file__)
