import bpy
import sys
import traceback

def check_mesh_exists():
    for o in bpy.context.selected_objects:
        if o.type == 'MESH':
            return True
    return False

def deselect_all_objects():
    bpy.ops.object.select_all(action='DESELECT')

def auto_merge_vertices(obj):
    C = bpy.context
    C.view_layer.objects.active = obj
    s = C.scene.tool_settings
    merge = s.use_mesh_automerge
    split = s.use_mesh_automerge_and_split
    s.use_mesh_automerge = True
    s.use_mesh_automerge_and_split = True
    ops = bpy.ops
    ops.object.mode_set(mode='EDIT')
    ops.mesh.select_all(action='SELECT')
    ops.transform.translate(value=(0, 0, 0))
    ops.mesh.select_all(action='SELECT')
    ops.mesh.remove_doubles()
    ops.object.mode_set(mode='OBJECT')
    s.use_mesh_automerge = merge
    s.use_mesh_automerge_and_split = split

def validate_mesh(object=None):
    if object:
        object.data.validate()
    else:
        for m in bpy.data.meshes:
            m.validate()

def import_obj(filepath):
    print("\nImport:")
    try:
        bpy.ops.wm.obj_import(filepath=filepath)
    except Exception as e:
        import_obj__deprecated(filepath=filepath)
    finally:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, exc_traceback)

def export_obj(filepath):
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
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    return filepath

# bpy.ops.import_scene.obj only works until blender version 3.6
def import_obj__deprecated(filepath):
    bpy.ops.import_scene.obj(filepath=filepath)

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

def duplicate_objects(objects):
    C = bpy.context
    duplicates = []
    active_obj = C.view_layer.objects.active
    for ob in objects:
        copy = duplicate_object(ob)
        if ob is active_obj:
            C.view_layer.objects.active = copy
        duplicates.append(copy)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in duplicates:
        ob.select_set(True)

def duplicate_object(ob):
    copy = ob.copy()
    copy.data = copy.data.copy()
    bpy.context.collection.objects.link(copy)
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    return copy

def select_objects(objects, active_object):
    for ob in objects:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = active_object

def hide_objects_from_viewport(objects, hide=True):
    for ob in objects:
        ob.hide_set(hide)