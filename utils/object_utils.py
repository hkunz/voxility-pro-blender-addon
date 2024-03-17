import bpy
import sys
import traceback
import bpy_types
import mathutils

from types import ModuleType
from typing import List
from voxility_pro.enums.name_constant import NameConstant # type: ignore

def check_mesh_exists() -> bool:
    o: bpy.types.Object
    for o in bpy.context.selected_objects:
        if o.type == 'MESH':
            return True
    return False

def deselect_all_objects() -> None:
    bpy.ops.object.select_all(action='DESELECT')

def auto_merge_vertices(object: bpy.types.Object) -> None:
    C: bpy_types.Context = bpy.context
    C.view_layer.objects.active = object
    s: bpy.types.ToolSettings = C.scene.tool_settings
    merge: bool = s.use_mesh_automerge
    split: bool = s.use_mesh_automerge_and_split
    s.use_mesh_automerge = True
    s.use_mesh_automerge_and_split = True
    ops: ModuleType = bpy.ops
    ops.object.mode_set(mode='EDIT')
    ops.mesh.select_all(action='SELECT')
    ops.transform.translate(value=(0, 0, 0))
    ops.mesh.select_all(action='SELECT')
    ops.mesh.remove_doubles()
    ops.object.mode_set(mode='OBJECT')
    s.use_mesh_automerge = merge
    s.use_mesh_automerge_and_split = split

def validate_mesh(object: bpy.types.Object=None) -> None:
    if object:
        object.data.validate()
    else:
        m: bpy_types.Mesh = None
        for m in bpy.data.meshes:
            m.validate()

def import_obj(filepath: str) -> bool:
    print("\nImport:")
    success: bool = False
    try:
        bpy.ops.wm.obj_import(filepath=filepath)
        success = True
    except Exception as e:
        import_obj__deprecated(filepath=filepath)
    finally:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    return success

def export_obj(filepath: str) -> None:
    print("\nExport:")
    try:
        bpy.ops.wm.obj_export(
            filepath=filepath,
            check_existing=True,
            filter_blender=False,
            filter_backup=False,
            filter_image=False,
            filter_movie=False,
            filter_python=False,
            filter_font=False,
            filter_sound=False,
            filter_text=False,
            filter_archive=False,
            filter_btx=False,
            filter_collada=False,
            filter_alembic=False,
            filter_usd=False,
            filter_obj=False,
            filter_volume=False,
            filter_folder=True,
            filter_blenlib=False,
            filemode=8,
            display_type='DEFAULT',
            sort_method='DEFAULT',
            export_animation=False,
            start_frame=-2147483648,
            end_frame=2147483647,
            forward_axis='NEGATIVE_Z',
            up_axis='Y',
            global_scale=1.0,
            apply_modifiers=True,
            export_eval_mode='DAG_EVAL_VIEWPORT',
            export_selected_objects=True,
            export_uv=True,
            export_normals=True,
            export_colors=False,
            export_materials=True,
            export_pbr_extensions=False,
            path_mode='AUTO',
            export_triangulated_mesh=False,
            export_curves_as_nurbs=False,
            export_object_groups=False,
            export_material_groups=False,
            export_vertex_groups=False,
            export_smooth_groups=False,
            smooth_group_bitflags=False,
            filter_glob='*.obj;*.mtl'
        )
    except Exception as e:
        export_obj__deprecated(filepath=filepath)
    finally:
        #exc_type:Optional[Type[BaseException]], exc_value:Optional[BaseException], traceback:Optional[TracebackType] = sys.exc_info()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    return filepath

# bpy.ops.import_scene.obj only works until blender version 3.6
def import_obj__deprecated(filepath: str) -> None:
    bpy.ops.import_scene.obj(filepath=filepath)

# bpy.ops.export_scene.obj only works until blender version 3.6
def export_obj__deprecated(filepath: str) -> None:
    bpy.ops.export_scene.obj(
        filepath=filepath,
        check_existing=True,
        axis_forward='-Z',
        axis_up='Y',
        filter_glob="*.obj;*.mtl",
        use_selection=True,
        use_animation=False,
        use_mesh_modifiers=True,
        use_edges=True,
        use_smooth_groups=False,
        use_smooth_groups_bitflags=False,
        use_normals=True,
        use_uvs=True,
        use_materials=True,
        use_triangles=False,
        use_nurbs=False,
        use_vertex_groups=False,
        use_blen_objects=True,
        group_by_object=False,
        group_by_material=False,
        keep_vertex_order=False,
        global_scale=1,
        path_mode='AUTO'
    )
    return filepath

def duplicate_objects(objects: List[bpy.types.Object]) -> None:
    C: bpy_types.Context = bpy.context
    duplicates: List[bpy.types.Object] = []
    active_obj: bpy.types.Object = C.view_layer.objects.active
    for ob in objects:
        copy: bpy.types.Object = duplicate_object(ob)
        if ob is active_obj:
            C.view_layer.objects.active = copy
        duplicates.append(copy)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in duplicates:
        ob.select_set(True)

def duplicate_object(ob: bpy.types.Object) -> bpy.types.Object:
    copy:bpy.types.Object = ob.copy()
    copy.data = copy.data.copy()
    bpy.context.collection.objects.link(copy)
    dg: bpy.types.Depsgraph = bpy.context.evaluated_depsgraph_get()
    dg.update()
    return copy

def select_objects(objects: List[bpy.types.Object], active_object: bpy.types.Object) -> None:
    for ob in objects:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = active_object

def hide_objects_from_viewport(objects: List[bpy.types.Object], hide: bool=True) -> None:
    for ob in objects:
        ob.hide_set(hide)

def get_voxelizer_voxel_size(active_object: bpy.types.Object):
    VOXILITY_MODIFIER_NAME = NameConstant.VOXILITY_MODIFIER_NAME.value
    node_groups = bpy.data.node_groups
    voxility_node_group = node_groups[VOXILITY_MODIFIER_NAME] if VOXILITY_MODIFIER_NAME in node_groups else None
    if not voxility_node_group:
        return 0
    for m in reversed(active_object.modifiers):
        if m.type == 'NODES' and voxility_node_group and m.node_group == voxility_node_group:
            return round(m["Socket_2" if bpy.app.version >= (4,0,0) else "Input_1"], 3)
    return 0

def get_mesh_center_of_mass_world(obj):
    vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
    return sum(vertices, mathutils.Vector()) / len(vertices)

import numpy as np

def get_mesh_center_world(obj):
    vertices = np.array([obj.matrix_world @ v.co for v in obj.data.vertices])
    min_coords = np.min(vertices, axis=0)
    max_coords = np.max(vertices, axis=0)
    bounding_box_center = (min_coords + max_coords) / 2.0
    return bounding_box_center

def get_mesh_center_voxel_distance(obj_A, obj_B, voxel_size) -> mathutils.Vector:
    xa, ya, za = get_voxel_distance(get_mesh_center_world(obj_A), voxel_size)
    xb, yb, zb = get_voxel_distance(get_mesh_center_world(obj_B), voxel_size)
    return xb - xa, yb - ya, zb - za

def get_voxel_distance(meters: np.ndarray, meter_per_voxel) -> int:
    x, y, z = meters
    return round(x / meter_per_voxel), round(y / meter_per_voxel), round(z / meter_per_voxel)