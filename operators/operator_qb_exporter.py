import bpy

from vox_exporter.operators.exporter_registration import ExporterRegistration
from vox_exporter.operators.base_operator_exporter import BaseOperatorExporter


class EXPORT_OT_qubicle(BaseOperatorExporter):
    bl_idname = "export.qubicle"
    bl_label = "Qubicle (.qb)"
    bl_description = "Export selected objects to Qubicle format (.qb)"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".qb"

    filter_glob: bpy.props.StringProperty(
        default="*.qb",
        options={'HIDDEN'},
        maxlen=255,
    )
