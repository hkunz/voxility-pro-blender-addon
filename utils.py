import addon_utils
import os

from vox_exporter import bl_info
#from vox_exporter.translations import get_translation

def getvoxdir():
    voxdir = None
    addon_name = bl_info["name"]
    for mod in addon_utils.modules():
        if addon_name != mod.bl_info.get("name"):
            print("(" + addon_name + ")check== ", mod.bl_info.get("name"))
            continue
        voxdir = os.path.dirname(mod.__file__) #C:\Users\<user>\AppData\Roaming\Blender Foundation\Blender\x.x\scripts\addons\vox-exporter
        break
    #assert voxdir, get_translation('error_no_addon_dir_found')
    assert voxdir, 'error_no_addon_dir_found ' + addon_name
    return voxdir
