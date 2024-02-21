import bpy
import time
import os
import bpy_types

from typing import List
from abc import ABC, abstractmethod

from voxility_pro.operators.voxel.operator_voxel_base import OperatorVoxelBase
from voxility_pro.operators.voxel.common.object_import_handlers.object_import_handler import ObjectImportHandler
from voxility_pro.translation.translations import get_translation
from voxility_pro.utils.temp_file_manager import TempFileManager
from voxility_pro.utils.file_utils import check_filepath, get_file_size
from voxility_pro.utils.object_utils import import_obj, deselect_all_objects, check_mesh_exists
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.enums.version_type import VersionType
from voxility_pro.operators.common.voxconvert_command_builder import VoxconvertCommandBuilder

VERTEX_COLORS_SUPPORT_BLENDER_VERSION = VersionType.VERTEX_COLORS_SUPPORT_BLENDER_VERSION.value

def get_blender_support_text():
    return f"Importing objects with vertex colors is only supported for Blender version {VERTEX_COLORS_SUPPORT_BLENDER_VERSION} and above"

class OperatorVoxelBaseImporter(OperatorVoxelBase):
    bl_description = "Operator Voxel Base Importer"
    vertex_color_support = False

    filter_glob: bpy.props.StringProperty(
        default="*.*",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    option_dissolve_limited: bpy.props.BoolProperty(
        name="Apply Limited Dissolve",
        description="Simplify mesh by dissolving vertices and edges separating flat regions.",
        default=False,
    ) # type: ignore

    voxformat_withcolor: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description=("Use vertex colors in model instead of image texture" if bpy.app.version >= VERTEX_COLORS_SUPPORT_BLENDER_VERSION else get_blender_support_text()),
        default=True,
    ) # type: ignore

    voxformat_mergequads: bpy.props.BoolProperty(
        name="Merge Quads",
        description=("Merge similar quads"),
        default=False,
    ) # type: ignore

    def draw(self, context: bpy_types.Context) -> None:
        self.layout.prop(self, "merge_vertices")
        #self.layout.prop(self, "option_dissolve_limited") #FIXME https://blender.stackexchange.com/questions/310984/how-can-i-preserve-face-corner-colors-when-doing-a-limited-dissolve
        col = self.layout.column()
        sub = col.row()
        sub.enabled = self.vertex_color_support
        sub.prop(self, "voxformat_withcolor")
        super().draw(context)

    def import_obj(self, obj_file: str) -> bool:
        deselect_all_objects()
        import_obj(obj_file)

        if not check_mesh_exists():
            self.report({'ERROR'}, f"{get_translation('error_nothing_to_import')} {self.filepath}")
            return False

        ObjectImportHandler(
            objects = bpy.context.selected_objects,
            merge_vertices = self.merge_vertices,
            dissolve_limited = self.option_dissolve_limited,
            with_vertex_colors = self.voxformat_withcolor
        ).on_object_import()

        return True

    def setup_command(self, input: str, outputs: List[str]) -> VoxconvertCommandBuilder:
        c: VoxconvertCommandBuilder = super().setup_command(input, outputs)
        c.vc_voxformat_withcolor = int(self.voxformat_withcolor)
        c.vc_voxformat_mergequads = int(self.voxformat_mergequads)
        c.vc_palette_file = ""
        return c

    def execute(self, _context: bpy_types.Context) -> set[str]:

        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, f"{get_translation('error_file_nonexistent')} {self.filepath}")
            return {'CANCELLED'}

        temp_dir: str = TempFileManager().create_temp_dir()
        out_filepath: str = os.path.join(temp_dir, 'temp.obj')

        self.setup_command(self.filepath, [out_filepath])
        success: bool = self.execute_voxconvert()

        if (success):
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {out_filepath} ({get_file_size(out_filepath)}) in {format_duration(self.voxconvert_duration)}")
        else:
            TempFileManager().delete_temp_dir(temp_dir)
            return {'CANCELLED'}

        start_time: float = time.time()
        self.import_obj(out_filepath)
        duration: str = format_duration(self.voxconvert_duration + (start_time - time.time()))
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {self.filepath} in {duration}")

        if self.voxformat_withcolor:
            TempFileManager().delete_temp_dir(temp_dir)
        #FIXME: we need to delete the temporary directory even without vertex colors but we can't because the color palette is used as texture in the imported object
        #TempFileManager().delete_temp_dir(temp_dir)

        return {'FINISHED'}

    def invoke(self, context: bpy_types.Context, _event: bpy.types.Event) -> set[str]:
        wm: bpy_types.WindowManager = context.window_manager
        wm.fileselect_add(self)
        self.filepath = check_filepath(self.filepath, self.filename_ext)
        self.vertex_color_support = bpy.app.version >= VERTEX_COLORS_SUPPORT_BLENDER_VERSION
        if not self.vertex_color_support:
            self.voxformat_withcolor = False
            print(get_blender_support_text())
        return {'RUNNING_MODAL'}

    @classmethod
    def poll(cls, _: bpy_types.Context) -> bool:
        return True