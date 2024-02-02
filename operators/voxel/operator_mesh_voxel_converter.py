import bpy
import tempfile
import os
import time

from voxility_pro.operators.voxel.base_voxel_operator import BaseVoxelOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.object_utils import export_obj, check_mesh_exists
from voxility_pro.utils.file_utils import get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.voxconvert_command_builder import VoxConvertCommandBuilder

class WM_OT_MeshVoxelConvertOperator(bpy.types.Operator):
    bl_idname = "wm.voxility_pro_mesh_voxel_convert_operator"
    bl_label = "Voxility Pro Mesh-Voxel Convert Operator"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        return active_object is not None and active_object.type == 'MESH' and context.mode == 'OBJECT'

    def export_obj(self, obj_file):
        start_time = time.time()
        export_obj(obj_file)
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_generated_files')} {obj_file} ({size}) in {duration}")
        return obj_file

    def execute(self, context):
        properties = context.scene.voxility_pro_properties

        temp_dir = tempfile.mkdtemp() # creates a temp directory in os.environ['TEMP']
        out_filepath = os.path.join(temp_dir, 'temp.obj')

        #print("Apply Limited Dissolve:", properties.option_dissolve_limited)
        #print("Use Vertex Colors:", properties.voxformat_withcolor)
        #print("Merge Vertices:", properties.merge_vertices)
        #print("Voxformat Voxelize Mode:", properties.voxformat_voxelizemode)
        #print("Voxformat Scale:", properties.voxformat_scale)
        #print("Palette File:", properties.palette_file)
        #print("Export Palette:", properties.export_palette)
        #print("Surface Only:", properties.surface_only)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(WM_OT_MeshVoxelConvertOperator)

def unregister():
    bpy.utils.unregister_class(WM_OT_MeshVoxelConvertOperator)