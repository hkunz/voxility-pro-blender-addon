# "MagicaVoxel Vox Exporter"
# Author: Harry McKenzie
#
# ##### BEGIN LICENSE BLOCK #####
#
# MagicaVoxel Vox Exporter
# Copyright (c) 2024 Harry McKenzie
#
# This program is licensed to you under a Royalty-Free License.
#
# You are allowed to use, modify, and distribute this software,
# royalty-free, for both personal and commercial purposes.
#
# This software is distributed WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "MagicaVoxel Vox Exporter",
    "description": "Vox Exporter addon that exports any mesh into vox format for MagicaVoxel and VoxEdit",
    "author" : "Harry McKenzie",
    "version": (1, 0, 2),
    "blender": (2, 93, 0),
    "voxconvert_version": (0, 0, 28),
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

