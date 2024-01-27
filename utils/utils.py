import bpy
import re

from vox_exporter import bl_info

def get_voxconvert_version():
    pattern = r' voxconvert-(\d+\.\d+\.\d+)$'
    match = re.search(pattern, bl_info["description"])
    version = match.group(1)
    return version

def export_obj(filepath):

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

    return filepath

# bpy.ops.export_scene.obj only works until blender version 3.6
def export_obj__deprecated(filepath):

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

def abstract_method(func):
    def wrapper(*args, **kwargs):
        raise NotImplementedError(f"{func.__name__} must be overridden in subclass.")
    return wrapper