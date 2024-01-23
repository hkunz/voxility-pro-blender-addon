import bpy

from vox_exporter.operators.exporter_registration import ExporterRegistration
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

def register():
    ExporterRegistration.register_operator(EXPORT_OT_magica_voxel, bpy.types.TOPBAR_MT_file_export)

def unregister():
    ExporterRegistration.unregister_operator(EXPORT_OT_magica_voxel, bpy.types.TOPBAR_MT_file_export)
