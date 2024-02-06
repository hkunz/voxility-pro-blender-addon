import bpy
import tempfile
import os
import time
import shutil

from mathutils import Vector

from voxility_pro.operators.voxel.object_import_handlers.object_import_handler import ObjectImportHandler
from voxility_pro.operators.voxel.voxconvert_operator import VoxconvertOperator
from voxility_pro.translations import get_translation
from voxility_pro.utils.object_utils import export_obj, check_mesh_exists, duplicate_objects, select_objects
from voxility_pro.utils.file_utils import get_file_size
from voxility_pro.utils.time_utils import format_duration
from voxility_pro.utils.object_utils import import_obj, deselect_all_objects, check_mesh_exists
from voxility_pro.context.context_script_executer import ContextScriptExecuter
from voxility_pro.enums.area_type import AreaType

class WM_OT_MeshVoxelConvertOperator(VoxconvertOperator):
    bl_idname = "wm.voxility_pro_mesh_voxel_convert_operator"
    bl_label = "Voxility Pro Mesh-Voxel Convert Operator"
    bl_description = "Voxelize or convert selected objects into a single voxel object"

    def create_temp_dup(self, objects):
        duplicate_objects(objects)
        bpy.ops.object.join()

    def export_obj(self, obj_file):
        start_time = time.time()
        export_obj(obj_file)
        duration = format_duration(time.time() - start_time)
        size = get_file_size(obj_file)
        self.report({'INFO'}, f"{get_translation('info_generated_files')} {obj_file} ({size}) in {duration}")
        return obj_file

    def import_obj(self, obj_file):
        deselect_all_objects()
        import_obj(obj_file)
        properties = bpy.context.scene.voxility_pro_properties
        ObjectImportHandler(
            objects = bpy.context.selected_objects,
            merge_vertices = properties.merge_vertices,
            dissolve_limited = properties.option_dissolve_limited,
            with_vertex_colors = properties.voxformat_withcolor
        ).on_object_import()
        return True

    def setup_command(self, input, output):
        c = super().setup_command(input, output)
        c.vc_merge_vertices = 0 #no --merge param but still merges vertices using python. remove line when this works
        c.vc_voxformat_withcolor = 1
        properties = bpy.context.scene.voxility_pro_properties
        c.vc_voxformat_scale = properties.voxformat_scale
        c.vc_surface_only = properties.surface_only
        c.vc_voxformat_voxelizemode = properties.voxformat_voxelizemode

    def execute(self, context):
        active_object = bpy.context.view_layer.objects.active
        temp_dir = tempfile.mkdtemp() # creates a temp directory in os.environ['TEMP']
        vc_in_path = os.path.join(temp_dir, 'temp_in.obj')
        vc_out_path = os.path.join(temp_dir, 'temp_out.obj')
        objects = bpy.context.selected_objects.copy()
        self.create_temp_dup(objects)
        self.export_obj(vc_in_path)
        orig_width = bpy.context.object.dimensions[0]
        bpy.ops.object.delete(use_global=False)
        select_objects(objects, active_object)
        print()
        self.setup_command(vc_in_path, vc_out_path)
        success = self.execute_voxconvert()

        if (success):
            self.report({'INFO'}, f"{get_translation('info_generated_files')} {vc_out_path} ({get_file_size(vc_out_path)}) in {format_duration(self.voxconvert_duration)}")
        else:
            shutil.rmtree(temp_dir)
            return {'CANCELLED'}

        start_time = time.time()
        self.import_obj(vc_out_path)
        scale = orig_width / bpy.context.object.dimensions[0]
        bpy.context.object.scale = Vector((scale, scale, scale))
        duration = format_duration(self.voxconvert_duration + (start_time - time.time()))
        self.report({'INFO'}, f"{get_translation('info_vox_data_imported')} {vc_out_path} in {duration}")
        properties = bpy.context.scene.voxility_pro_properties
        if properties.voxformat_withcolor:
            shutil.rmtree(temp_dir)
        #FIXME: we need to delete the temporary directory even without vertex colors but we can't because the color palette is used as texture in the imported object
        #shutil.rmtree(temp_dir)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        selected_objects = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for obj in selected_objects:
            if obj.type != 'MESH' or not obj.data.polygons:
                return False
        return True

def register():
    bpy.utils.register_class(WM_OT_MeshVoxelConvertOperator)

def unregister():
    bpy.utils.unregister_class(WM_OT_MeshVoxelConvertOperator)