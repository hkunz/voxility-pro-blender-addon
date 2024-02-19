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
    "description": "Voxility enables the import and export of various voxel file formats through voxconvert-0.0.28-80f09", # voxconvert-X.X.X is parsed out in utils.py
    "author" : "Harry McKenzie",
    "version": (1, 0, 8),
    "blender": (2, 93, 0),
    "location": "File > Import-Export > Voxility Voxel Formats",
    "warning": "",
    "doc_url": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import stat

from pathlib import Path
from typing import Union

from voxility_pro.utils.temp_file_manager import TempFileManager

from voxility_pro.utils.file_utils import (
    get_voxconvert_filepath,
    get_file_size
)

from voxility_pro.menus.voxel_formats_export_menu import (
    register as register_vox_export_menu,
    unregister as unregister_vox_export_menu
)

from voxility_pro.menus.voxel_formats_import_menu import (
    register as register_vox_import_menu,
    unregister as unregister_vox_import_menu
)

from voxility_pro.menus.voxel_converter_sidebar_menu import (
    register as register_sidebar_menu,
    unregister as unregister_sidebar_menu
)

from voxility_pro.operators.operator_generic_popup import (
    register as register_generic_popup,
    unregister as unregister_generic_popup
)

from voxility_pro.translations import (
    register as register_translations,
    unregister as unregister_translations
)

def add_executable_permission(exe: Union[str, Path]) -> Path:
    app = Path(__file__).parent / f"{exe}"
    print("Using voxconvert:", app, f"({get_file_size(app)})")
    app.chmod(app.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return app

def register() -> None:
    add_executable_permission(get_voxconvert_filepath()) #https://blender.stackexchange.com/questions/310144/mac-executable-binary-within-addon-zip-loses-execute-permission-when-addon-zip
    register_translations()
    register_vox_export_menu()
    register_vox_import_menu()
    #register_sidebar_menu()
    #register_generic_popup()

def unregister() -> None:
    unregister_translations()
    unregister_vox_export_menu()
    unregister_vox_import_menu()
    #unregister_sidebar_menu()
    #unregister_generic_popup()
    TempFileManager().cleanup()