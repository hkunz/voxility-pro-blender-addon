import bpy

from vox_exporter.operators.operator_qb_exporter import EXPORT_OT_qubicle

class VoxelFormatsMenu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_select_submenu"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout
        layout.operator(EXPORT_OT_qubicle.bl_idname, text=EXPORT_OT_qubicle.bl_label)

def menu_func_voxel_formats_menu(self, context):
    self.layout.menu(VoxelFormatsMenu.bl_idname, text="More Voxel Formats")

def register():
    bpy.utils.register_class(EXPORT_OT_qubicle)
    bpy.utils.register_class(VoxelFormatsMenu)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_voxel_formats_menu)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_qubicle)
    bpy.utils.unregister_class(VoxelFormatsMenu)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_voxel_formats_menu)