import bpy
import time
import tempfile
import shutil
import os

from voxility_pro.operators.voxel.base_voxel_operator import BaseVoxelOperator
from voxility_pro.context.add_vertex_colors_script_executer import AddVertexColorsScriptExecuter
from voxility_pro.translations import get_translation
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.object_utils import import_obj, deselect_all_objects, auto_merge_vertices, check_mesh_exists
from voxility_pro.utils.string_utils import randomize_string
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder

IMPORTED_OBJ_BASE_NAME = "Voxility"

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

    voxformat_withcolor: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description="Use vertex colors in model instead of image texture",
        default=False,
    )

    def draw(self, context):
        self.layout.prop(self, "option_auto_merge_vertices")
        self.layout.prop(self, "voxformat_withcolor")
        super().draw(context)

    @staticmethod
    def init_imported_objects(merge=True, vertex_colors=False):
        for o in bpy.context.selected_objects:
            if o.type != 'MESH':
                continue
            suffix = randomize_string()
            o.name = f"{IMPORTED_OBJ_BASE_NAME}_{suffix}"
            o.data.name = f"{IMPORTED_OBJ_BASE_NAME}_{suffix}"
            if merge:
                auto_merge_vertices(o)
            if vertex_colors:
                AddVertexColorsScriptExecuter(o).execute_script()
            bpy.ops.object.shade_flat()
            bpy.context.object.data.use_auto_smooth = False

    def import_obj(self, obj_file):
        deselect_all_objects()
        import_obj(obj_file)

        if not check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_nothing_to_import')} {self.filepath}")
            return False

        self.init_imported_objects(self.option_auto_merge_vertices, self.voxformat_withcolor)
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
            int(self.voxformat_voxelizemode)
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

        #FIXME: we need to delete the temporary directory but we can't because the color palette is used as texture in the imported object
        #shutil.rmtree(temp_dir)
        duration = format_duration(self.voxconvert_duration + (start_time - time.time()))
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {self.filepath} in {duration}")

        return {'FINISHED'}

    def invoke(self, context, _event):
        wm = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        return {'RUNNING_MODAL'}
