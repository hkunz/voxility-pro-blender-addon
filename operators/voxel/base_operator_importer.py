import bpy
import time
import tempfile
import shutil
import os

from voxility_pro.operators.voxel.base_voxel_operator import BaseVoxelOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.object_utils import import_obj, deselect_all_objects, auto_merge_vertices
from voxility_pro.utils.string_utils import randomize_string
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder

IMPORTED_OBJ_BASE_NAME = "voxility"

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

    def draw(self, context):
        self.layout.prop(self, "option_auto_merge_vertices")
        super().draw(context)

    def check_mesh_exists(self):
        for o in bpy.context.selected_objects:
            if o.type == 'MESH':
                return True
        return False

    def init_imported_objects(self):
        for o in bpy.context.selected_objects:
            if o.type != 'MESH':
                continue
            suffix = randomize_string()
            o.name = f"{IMPORTED_OBJ_BASE_NAME}_{suffix}"
            o.data.name = f"{IMPORTED_OBJ_BASE_NAME}_{suffix}"
            if self.option_auto_merge_vertices:
                auto_merge_vertices(o)
            bpy.ops.object.shade_flat()
            bpy.context.object.data.use_auto_smooth = False

    def import_obj(self, obj_file):
        start_time = time.time()
        deselect_all_objects()
        import_obj(obj_file)

        if not self.check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_nothing_to_import')} {self.filepath}")
            return False

        self.init_imported_objects()
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_imported_file')} {obj_file} ({size}) in {duration}")
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {self.filepath}")
        return True

    def execute(self, context):

        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, f"{get_translation('error_file_nonexistent')} {self.filepath}")
            return {'CANCELLED'}

        start_time = time.time()
        temp_dir = tempfile.mkdtemp() # creates a temp directory in os.environ['TEMP']
        output_obj_filepath = os.path.join(temp_dir, 'temp.obj')

        command_builder = VoxConvertCommandBuilder(
            self.filepath,
            output_obj_filepath,
            int(self.voxformat_voxelizemode)
        )
        command = command_builder.build_command()
        success = self.execute_voxconvert(command, output_obj_filepath, start_time, get_translation('info_generated_files'), temp_dir)
        if success:
            self.import_obj(output_obj_filepath)

        #FIXME: we need to delete the temporary directory but we can't because importing works asynchronously
        shutil
        #shutil.rmtree(temp_dir)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
