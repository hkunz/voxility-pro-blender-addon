import bpy


from vox_exporter.operators.base_operator_exporter import BaseOperatorExporter


class EXPORT_OT_magica_voxel(BaseOperatorExporter):
    bl_idname = "export.magica_voxel"
    bl_label = "MagicaVoxel (.vox)"
    bl_description = "Export selected objects to MagicaVoxel format (.vox)"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".vox"

    filter_glob: bpy.props.StringProperty(
        default="*.vox",
        options={'HIDDEN'},
        maxlen=255,
    )


def on_file_export_vox_click(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(EXPORT_OT_magica_voxel.bl_idname, text="MagicaVoxel (.vox)")

def register():
    bpy.utils.register_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.append(on_file_export_vox_click)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_magica_voxel)
    bpy.types.TOPBAR_MT_file_export.remove(on_file_export_vox_click)
