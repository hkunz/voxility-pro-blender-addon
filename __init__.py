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
    "author" : "Harry McKenzie",
    "version": (0, 1, 0),
    "blender": (2, 93, 0),
    "description": "Vox Exporter addon that exports any mesh into vox format for MagicaVoxel and VoxEdit",
    "location": "File > Export > MagicaVoxel (.vox)",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
    "category": "Import-Export",
}

import bpy
import sys

print("========== ", sys.path)

from vox_exporter.operators import EXPORT_OT_magica_voxel
from vox_exporter.translations import register_translations, unregister_translations

print("START ==============================")

def menu_func_export(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(EXPORT_OT_magica_voxel.bl_idname, text="MagicaVoxel (.vox)")

def register():
    register_translations()
    bpy.utils.register_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    unregister_translations()
    bpy.utils.unregister_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
