import bpy
import numpy as np
import mathutils

from voxility_pro.enums.name_constant import NameConstant # type: ignore

class Voxel:
    DEFAULT_MIN = 0.01
    DEFAULT_MAX = 100.0
    DEFAULT_VALUE = 0.5
    PREVIOUS_ACTIVE_OBJECT = None
    PREVIOUS_UVMAP_ATTRIBUTE = None
    PREVIOUS_COLOR_ATTRIBUTE = None

def get_voxility_node_group():
    VOXILITY_MODIFIER_NAME = NameConstant.VOXILITY_MODIFIER_NAME.value
    node_groups = bpy.data.node_groups
    voxility_node_group = node_groups[VOXILITY_MODIFIER_NAME] if VOXILITY_MODIFIER_NAME in node_groups else None
    return voxility_node_group

def get_voxelizer_modifier(active_object):
    voxility_node_group = get_voxility_node_group()
    for m in reversed(active_object.modifiers):
        if m.type == 'NODES' and voxility_node_group and m.node_group == voxility_node_group:
            return m
    return None

def remove_all_voxelizier_modifiers(active_object):
    m = get_voxelizer_modifier(active_object)
    remove = False
    while m:
        active_object.modifiers.remove(m)
        remove = True
        m = get_voxelizer_modifier(active_object)
    return remove

def get_voxelizer_voxel_size_attr_name():
    return "Socket_2" if bpy.app.version >= (4,0,0) else "Input_1"

def get_voxelizer_voxel_uv_attr_name():
    return "Socket_3" if bpy.app.version >= (4,0,0) else "Input_2"

def get_voxelizer_voxel_vertex_colors_attr_name():
    return "Socket_4" if bpy.app.version >= (4,0,0) else "Input_3"

def is_object_voxelized(active_object: bpy.types.Object):
    return bool(get_voxelizer_modifier(active_object))

def get_voxelizer_voxel_size(active_object: bpy.types.Object):
    mod = get_voxelizer_modifier(active_object)
    if mod and active_object:
        return round(mod[get_voxelizer_voxel_size_attr_name()], 3)
    return 0

def set_voxelizer_voxel_size(obj, voxel_size):
    return set_voxelizer_voxel_attribute(obj, get_voxelizer_voxel_size_attr_name(), voxel_size)

def set_voxelizer_voxel_vertex_colors(obj, vertex_colors):
    return set_voxelizer_voxel_attribute(obj, get_voxelizer_voxel_vertex_colors_attr_name(), vertex_colors)

def set_voxelizer_voxel_uvmap(obj, uvmap):
    return set_voxelizer_voxel_attribute(obj, get_voxelizer_voxel_uv_attr_name(), uvmap)

def set_voxelizer_voxel_attribute(obj, attr_name, value):
    mod = get_voxelizer_modifier(obj)
    if not mod or not obj:
        return False
    if value == mod[attr_name]:
        return False
    mod[attr_name] = value
    obj.modifiers.update()
    obj.update_tag()
    return True

def get_voxelizer_voxel_modifier_attributes(active_object: bpy.types.Object):
    mod = get_voxelizer_modifier(active_object)
    voxel_size = 0
    uvmap = "" #"UVMap"
    color = "" #"Col"
    if mod:
            voxel_size = get_voxelizer_voxel_size(active_object)
            uvmap = mod[get_voxelizer_voxel_uv_attr_name()]
            color = mod[get_voxelizer_voxel_vertex_colors_attr_name()]
    return voxel_size, uvmap, color

def get_mesh_center_of_mass_world(obj):
    vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
    return sum(vertices, mathutils.Vector()) / len(vertices)

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