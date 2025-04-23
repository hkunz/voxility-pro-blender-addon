# "Voxelity Pro: Voxel File Format Exchange"
# Author: Harry McKenzie
#
# ##### BEGIN LICENSE BLOCK #####
#
# Voxelity Pro: Voxel File Format Exchange
# Copyright (c) 2024 Harry McKenzie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "Voxelity Pro: Voxel File Format Exchange",
    "description": "Voxelity enables the manipulation, import, and export of various voxel file formats through voxconvert-0.0.29", # voxconvert-X.X.X is parsed out in utils.py
    "author" : "Harry McKenzie",
    "version": (1, 0, 15),
    "blender": (2, 93, 0),
    "location": "N-Panel > Voxelity | File > Import-Export > Voxelity Voxel Formats",
    "warning": "",
    "doc_url": "https://blendermarket.com/products/voxelity-pro-voxel-file-format-exchange/docs",
    "wiki_url": "https://blendermarket.com/products/voxelity-pro-voxel-file-format-exchange/docs",
    "tracker_url": "https://blendermarket.com/products/voxelity-pro-voxel-file-format-exchange/docs",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import bpy
import stat

from pathlib import Path
from typing import Union
from bpy.app.handlers import persistent

from voxelity_pro.enums.voxelity_feature import VoxelityFeature # type: ignore
from voxelity_pro.ui.addon_preferences import register as register_preferences, unregister as unregister_preferences # type: ignore
from voxelity_pro.utils.file_utils import FileUtils # type: ignore
from voxelity_pro.utils.temp_file_manager import TempFileManager # type: ignore
from voxelity_pro.utils.icons_manager import IconsManager # type: ignore
from voxelity_pro.utils.system_utils import SystemUtils # type: ignore
from voxelity_pro.utils.voxel.voxel_utils import VoxelUtils # type: ignore
from voxelity_pro.translation.translations import register as register_translations, unregister as unregister_translations # type: ignore
if VoxelityFeature.GN_VOXELIZER_ACTIVE.value and bpy.app.version >= (3,3,0):
    from voxelity_pro.ui.voxel_gn_voxelizer_sidebar_menu import register as register_sidebar_menu, unregister as unregister_sidebar_menu # type: ignore
else:
    from voxelity_pro.ui.deprecated.voxel_converter_sidebar_menu import register as register_sidebar_menu, unregister as unregister_sidebar_menu # type: ignore
from voxelity_pro.operators.installation.darwin.operator_macos_install_rosetta2 import WEB_OT_OperatorInstallMacRosetta2 # type: ignore
from voxelity_pro.operators.operator_generic_popup import register as register_generic_popup, unregister as unregister_generic_popup # type: ignore
from voxelity_pro.operators.voxel.operator_voxconvert_test import OperatorVoxconvertTest # type: ignore

def add_executable_permission(exe: Union[str, Path]) -> Path:
    app = Path(f"{exe}")
    print("Using voxconvert:", app, f"({FileUtils.get_file_size(app)})")
    app.chmod(app.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return app

@persistent
def on_application_load(a, b):
    print("Application load post handler ==============>", a, b)
    VoxelUtils.check_voxelizer_compatibility()

def register() -> None:
    print("Addon Registration Begin ==============>")
    add_executable_permission(FileUtils.get_voxconvert_filepath()) #https://blender.stackexchange.com/questions/310144/mac-executable-binary-within-addon-zip-loses-execute-permission-when-addon-zip
    register_preferences()
    bpy.utils.register_class(OperatorVoxconvertTest)
    if SystemUtils.is_darwin():
        bpy.utils.register_class(WEB_OT_OperatorInstallMacRosetta2)
    register_translations()
    register_sidebar_menu()
    register_generic_popup()
    TempFileManager().init()
    IconsManager().init()
    bpy.app.handlers.load_post.append(on_application_load)
    print("Addon Registration Complete <==========\n")

def unregister() -> None:
    print("Addon Unregistration Begin ============>")
    unregister_preferences()
    bpy.utils.unregister_class(OperatorVoxconvertTest)
    if SystemUtils.is_darwin():
        bpy.utils.unregister_class(WEB_OT_OperatorInstallMacRosetta2)
    unregister_translations()
    unregister_sidebar_menu()
    unregister_generic_popup()
    TempFileManager().cleanup()
    IconsManager().cleanup()
    bpy.app.handlers.load_post.remove(on_application_load)
    print("Addon Unregistration Complete <========\n")
