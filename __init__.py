# "Voxility Pro: Voxel File Format Exchange"
# Author: Harry McKenzie
#
# ##### BEGIN LICENSE BLOCK #####
#
# Voxility Pro: Voxel File Format Exchange
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
    "name": "Voxility Pro: Voxel File Format Exchange",
    "description": "Voxility enables the manipulation, import, and export of various voxel file formats through voxconvert-0.0.29", # voxconvert-X.X.X is parsed out in utils.py
    "author" : "Harry McKenzie",
    "version": (1, 0, 9),
    "blender": (2, 93, 0),
    "location": "N-Panel > Voxility | File > Import-Export > Voxility Voxel Formats",
    "warning": "",
    "doc_url": "https://blendermarket.com/products/vox-exporter-for-magicavoxel-and-voxedit/docs",
    "wiki_url": "https://blendermarket.com/products/vox-exporter-for-magicavoxel-and-voxedit/docs",
    "tracker_url": "https://blendermarket.com/products/vox-exporter-for-magicavoxel-and-voxedit/docs",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import bpy
import stat

from pathlib import Path
from typing import Union

from voxility_pro.enums.voxility_feature import VoxilityFeature # type: ignore
from voxility_pro.ui.addon_preferences import register as register_preferences, unregister as unregister_preferences # type: ignore
from voxility_pro.utils.file_utils import get_voxconvert_filepath, get_file_size # type: ignore
from voxility_pro.utils.temp_file_manager import TempFileManager # type: ignore
from voxility_pro.utils.icons_manager import IconsManager  # type: ignore
from voxility_pro.translation.translations import register as register_translations, unregister as unregister_translations # type: ignore
if VoxilityFeature.GN_VOXELIZER_ACTIVE.value and bpy.app.version >= (3,3,0):
    from voxility_pro.ui.voxel_gn_voxelizer_sidebar_menu import register as register_sidebar_menu, unregister as unregister_sidebar_menu # type: ignore
else:
    from voxility_pro.ui.deprecated.voxel_converter_sidebar_menu import register as register_sidebar_menu, unregister as unregister_sidebar_menu # type: ignore
from voxility_pro.operators.operator_generic_popup import register as register_generic_popup, unregister as unregister_generic_popup # type: ignore
from voxility_pro.operators.voxel.operator_voxelize import register as register_gn_voxelizer, unregister as unregister_gn_voxelizer # type: ignore
from voxility_pro.operators.voxel.operator_voxconvert_test import OperatorVoxconvertTest # type: ignore

def add_executable_permission(exe: Union[str, Path]) -> Path:
    app = Path(__file__).parent / f"{exe}"
    print("Using voxconvert:", app, f"({get_file_size(app)})")
    app.chmod(app.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return app

def register() -> None:
    print("Addon Registration Begin ==============>")
    add_executable_permission(get_voxconvert_filepath()) #https://blender.stackexchange.com/questions/310144/mac-executable-binary-within-addon-zip-loses-execute-permission-when-addon-zip
    register_preferences()
    bpy.utils.register_class(OperatorVoxconvertTest)
    register_gn_voxelizer()
    register_translations()
    register_sidebar_menu()
    register_generic_popup()
    TempFileManager().init()
    IconsManager().init()
    print("Addon Registration Complete <==========\n")

def unregister() -> None:
    print("Addon Unregistration Begin ============>")
    unregister_preferences()
    bpy.utils.unregister_class(OperatorVoxconvertTest)
    unregister_gn_voxelizer()
    unregister_translations()
    unregister_sidebar_menu()
    unregister_generic_popup()
    TempFileManager().cleanup()
    IconsManager().cleanup()
    print("Addon Unregistration Complete <========\n")