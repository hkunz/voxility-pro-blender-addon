import bpy
import time
import tempfile
import shutil
import os

from abc import ABC, abstractmethod

from voxility_pro.operators.voxel.object_import_handlers.object_import_handler import ObjectImportHandler
from voxility_pro.operators.voxel.base_voxel_operator import BaseVoxelOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.object_utils import import_obj, deselect_all_objects, check_mesh_exists
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder

class BaseOperatorImporter(BaseVoxelOperator):
    bl_description = "Base Voxel Operator Importer"
    voxility_type = "importer"

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    )

    option_auto_merge_vertices: bpy.props.BoolProperty(
        name="Auto Merge Vertices",
        description="Automatically merge vertices and split edges",
        default=True,
    )

    option_dissolve_limited: bpy.props.BoolProperty(
        name="Apply Limited Dissolve",
        description="Simplify mesh by dissolving vertices and edges separating flat regions.",
        default=False,
    )

    voxformat_withcolor: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description="Use vertex colors in model instead of image texture",
        default=True,
    )

    def draw(self, context):
        self.layout.prop(self, "option_auto_merge_vertices")
        #self.layout.prop(self, "option_dissolve_limited") #FIXME https://blender.stackexchange.com/questions/310984/how-can-i-preserve-face-corner-colors-when-doing-a-limited-dissolve
        self.layout.prop(self, "voxformat_withcolor")
        super().draw(context)

    def import_obj(self, obj_file):
        deselect_all_objects()
        import_obj(obj_file)

        if not check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_nothing_to_import')} {self.filepath}")
            return False

        ObjectImportHandler(
            objects = bpy.context.selected_objects,
            merge_vertices = self.option_auto_merge_vertices,
            dissolve_limited = self.option_dissolve_limited,
            with_vertex_colors = self.voxformat_withcolor
        ).on_object_import()

        return True

    def execute(self, _context):

        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, f"{get_translation('error_file_nonexistent')} {self.filepath}")
            return {'CANCELLED'}

        temp_dir = tempfile.mkdtemp() # creates a temp directory in os.environ['TEMP']
        out_filepath = os.path.join(temp_dir, 'temp.obj')

        command_builder = VoxConvertCommandBuilder(
            self.filepath,
            out_filepath,
            int(self.voxformat_voxelizemode),
            int(self.voxformat_withcolor)
        )
        command = command_builder.build_command()
        success = self.execute_voxconvert(command)
        if (success):
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {out_filepath} ({get_file_size(out_filepath)}) in {format_duration(self.voxconvert_duration)}")
        else:
            shutil.rmtree(temp_dir)
            return {'CANCELLED'}

        start_time = time.time()
        self.import_obj(out_filepath)
        duration = format_duration(self.voxconvert_duration + (start_time - time.time()))
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {self.filepath} in {duration}")

        if self.voxformat_withcolor:
            shutil.rmtree(temp_dir)
        #FIXME: we need to delete the temporary directory even without vertex colors but we can't because the color palette is used as texture in the imported object
        #shutil.rmtree(temp_dir)

        return {'FINISHED'}

    def invoke(self, context, _event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
