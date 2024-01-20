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
    "description": "Vox Exporter via voxconvert-0.0.28 exports any mesh into vox format for MagicaVoxel and VoxEdit", # voxconvert-X.X.X is parsed out in utils.py
    "author" : "Harry McKenzie",
    "version": (1, 0, 4),
    "blender": (2, 93, 0),
    "location": "File > Export > MagicaVoxel (.vox)",
    "warning": "",
    "doc_url": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import bpy

from vox_exporter.operators.operator_vox_exporter import register_vox_exporter, unregister_vox_exporter
from vox_exporter.operators.operator_modal_timer import register_modal_timer, unregister_modal_timer
from vox_exporter.translations import register_translations, unregister_translations


def register():
    register_translations()
    #register_modal_timer()
    register_vox_exporter()

def unregister():
    unregister_translations()
    #unregister_modal_timer()
    unregister_vox_exporter()

