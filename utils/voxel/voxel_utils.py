import bpy
import numpy as np
import mathutils

from voxility_pro.enums.name_constant import NameConstant # type: ignore

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

def get_voxelizer_voxel_size(active_object: bpy.types.Object):
    mod = get_voxelizer_modifier(active_object)
    if mod:
            return round(mod["Socket_2" if bpy.app.version >= (4,0,0) else "Input_1"], 3)
    return 0

def get_voxelizer_voxel_modifier_attributes(active_object: bpy.types.Object):
    mod = get_voxelizer_modifier(active_object)
    voxel_size = 0
    uvmap = "UVMap"
    color = "Col"
    if mod:
            voxel_size = get_voxelizer_voxel_size(active_object)
            uvmap = mod["Socket_3" if bpy.app.version >= (4,0,0) else "Input_2"]
            color = mod["Socket_4" if bpy.app.version >= (4,0,0) else "Input_3"]
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