import bpy

from vox_exporter.operators.base_operator_exporter import BaseOperatorExporter


class EXPORT_OT_qubicle(BaseOperatorExporter):
    bl_idname = "export.qubicle"
    bl_label = "Qubicle (.qb)"
    bl_description = "Export selected objects to Qubicle format (.qb)"

    filename_ext = ".qb"

    filter_glob: bpy.props.StringProperty(
        default="*.qb",
        options={'HIDDEN'},
        maxlen=255,
    )


def on_file_export_qb_click(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(EXPORT_OT_qubicle.bl_idname, text="Qubicle (.qb)")

def register():
    bpy.utils.register_class(EXPORT_OT_qubicle)
    bpy.types.TOPBAR_MT_file_export.append(on_file_export_qb_click)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_qubicle)
    bpy.types.TOPBAR_MT_file_export.remove(on_file_export_qb_click)
