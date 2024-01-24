# "MagicaVoxel Vox Exporter"
# Author: Harry McKenzie
#
# ##### BEGIN LICENSE BLOCK #####
#
# MagicaVoxel Vox Exporter
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
    "name": "MagicaVoxel Vox Exporter",
    "description": "Vox Exporter via voxconvert-0.0.28 exports any mesh into MagicaVoxel / VoxEdit (.vox) or Qubicle (.qb) format", # voxconvert-X.X.X is parsed out in utils.py
    "author" : "Harry McKenzie",
    "version": (1, 0, 8),
    "blender": (2, 93, 0),
    "location": "File > Export > MagicaVoxel (.vox)",
    "warning": "",
    "doc_url": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import stat
from pathlib import Path

from vox_exporter.utils.file_utils import get_voxconvert_filepath, get_file_size
from vox_exporter.menus.voxel_formats_menu import register as register_voxel_formats_menu, unregister as unregister_voxel_formats_menu
from vox_exporter.operators.voxel.operator_vox_exporter import register as register_vox, unregister as unregister_vox
from vox_exporter.translations import register_translations, unregister_translations


def add_executable_permission(exe):
    app = Path(__file__).parent / f"{exe}"
    print("Using voxconvert: ", app, f"({get_file_size(app)})")
    app.chmod(app.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

def register():
    add_executable_permission(get_voxconvert_filepath())
    register_translations()
    register_vox()
    register_voxel_formats_menu()

def unregister():
    unregister_translations()
    unregister_vox()
    unregister_voxel_formats_menu()
