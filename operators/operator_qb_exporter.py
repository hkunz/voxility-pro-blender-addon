import bpy

from vox_exporter.operators.base_operator_exporter import BaseOperatorExporter


class EXPORT_OT_cubicle(BaseOperatorExporter):
    bl_idname = "export.cubicle"
    bl_label = "Cubicle (.qb)"
    bl_description = "Export selected objects to Cubicle format (.qb)"

    filename_ext = ".qb"

    filter_glob: bpy.props.StringProperty(
        default="*.qb",
        options={'HIDDEN'},
        maxlen=255,
    )


def on_file_export_qb_click(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(EXPORT_OT_cubicle.bl_idname, text="Cubicle (.qb)")

def register():
    bpy.utils.register_class(EXPORT_OT_cubicle)
    bpy.types.TOPBAR_MT_file_export.append(on_file_export_qb_click)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_cubicle)
    bpy.types.TOPBAR_MT_file_export.remove(on_file_export_qb_click)
