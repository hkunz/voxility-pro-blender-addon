import bpy

from vox_exporter.operators.exporter_registration import ExporterRegistration
from vox_exporter.operators.voxel.base_operator_importer import BaseOperatorImporter

class IMPORT_OT_magica_voxel(BaseOperatorImporter):
    bl_idname = "import.magica_voxel"
    bl_label = "MagicaVoxel (.vox)"
    bl_description = "Import MagicaVoxel format (.vox)"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".vox"

    filter_glob: bpy.props.StringProperty(
        default="*.vox",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        # Your import logic goes here
        return {'FINISHED'}


def register():
    ExporterRegistration.register_operator(IMPORT_OT_magica_voxel, bpy.types.TOPBAR_MT_file_import)

def unregister():
    ExporterRegistration.unregister_operator(IMPORT_OT_magica_voxel, bpy.types.TOPBAR_MT_file_import)
