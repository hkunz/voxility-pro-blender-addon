import bpy
import mathutils

from voxelity_pro.enums.name_constant import NameConstant # type: ignore

class Voxel:
    SIZE_PRECISION = 2
    DEFAULT_MIN = 0.01
    DEFAULT_MAX = 100.0
    DEFAULT_VALUE = 0.5
    PREVIOUS_ACTIVE_OBJECT = None

class VoxelUtils:

    @staticmethod
    def check_voxelizer_compatibility():
        n1 = NameConstant.VOXILITY_NODE_GROUP_NAME.value
        p1 = NameConstant.VOXILITY_NODE_GROUP_NAME_PREFIX.value
        n2 = NameConstant.VOXILITY_MODIFIER_NAME.value
        p2 = NameConstant.VOXILITY_MODIFIER_NAME_PREFIX.value
        compatible = True
        # Check both node groups for compatibility just to make sure because user could have manually edited the name of one of them
        for g in bpy.data.node_groups[:]:
            for k in g.keys(): # VoxelityVoxelizeModifier_X_X_vZ_Z_Z e.g. VoxelityVoxelizeModifier_4_0_v1_0_12
                if (k.startswith(p1) and k != n1) or (k.startswith(p2) and k != n2):
                    print(f"WARNING: Removing incompatible node group '{k}'")
                    bpy.data.node_groups.remove(g)
                    compatible = False
                    break
        if compatible:
            return

        # Remove any additional included node groups of the voxelity addon feature
        for g in bpy.data.node_groups[:]:
            if not g.name.startswith(NameConstant.VOXILITY_EXTENDED_NODE_GROUP_PREFIX.value):
                continue
            bpy.data.node_groups.remove(g)
            break

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.voxelized = False

    @staticmethod
    def get_voxelity_node_group(node_group_name):
        for ng in bpy.data.node_groups:
            if node_group_name in ng: # check if it has key ng[node_group_name]:
                return ng
        return None

    @staticmethod
    def get_voxelizer_modifier(active_object):
        voxelity_node_group = VoxelUtils.get_voxelity_node_group(NameConstant.VOXILITY_MODIFIER_NAME.value)
        for m in reversed(active_object.modifiers):
            if m.type == 'NODES' and voxelity_node_group and m.node_group == voxelity_node_group:
                return m
        return None

    @staticmethod
    def remove_all_voxelizier_modifiers(active_object):
        m = VoxelUtils.get_voxelizer_modifier(active_object)
        remove = False
        while m:
            active_object.modifiers.remove(m)
            remove = True
            m = VoxelUtils.get_voxelizer_modifier(active_object)
        return remove

    @staticmethod
    def get_voxelizer_voxel_size_attr_name():
        return "Socket_2" if bpy.app.version >= (4,0,0) else "Input_1"

    @staticmethod
    def get_voxelizer_voxel_uv_attr_name():
        return "Socket_3" if bpy.app.version >= (4,0,0) else "Input_2"

    @staticmethod
    def get_voxelizer_voxel_vertex_colors_attr_name():
        return "Socket_4" if bpy.app.version >= (4,0,0) else "Input_3"

    @staticmethod
    def is_object_voxelized(active_object: bpy.types.Object):
        return bool(VoxelUtils.get_voxelizer_modifier(active_object)) if active_object else False

    @staticmethod
    def get_voxelizer_voxel_size(obj: bpy.types.Object):
        mod = VoxelUtils.get_voxelizer_modifier(obj)
        if mod and obj:
            return round(mod[VoxelUtils.get_voxelizer_voxel_size_attr_name()], Voxel.SIZE_PRECISION)
        return VoxelUtils.get_object_edge_size(obj) if obj.voxelized else 0

    @staticmethod
    def lock_voxelized_object(obj):
        obj.lock_location[0] = obj.lock_location[1] = obj.lock_location[2] = True
        obj.lock_rotation[0] = obj.lock_rotation[1] = obj.lock_rotation[2] = True
        obj.lock_scale[0] = obj.lock_scale[1] = obj.lock_scale[2] = True

    @staticmethod
    def get_object_edge_size(obj):
        d= obj.data
        e = d.edges[0]
        return round((d.vertices[e.vertices[1]].co - d.vertices[e.vertices[0]].co).length, Voxel.SIZE_PRECISION)

    @staticmethod
    def set_voxelizer_voxel_size(obj, voxel_size):
        return VoxelUtils.set_voxelizer_voxel_attribute(obj, VoxelUtils.get_voxelizer_voxel_size_attr_name(), voxel_size)

    @staticmethod
    def set_voxelizer_voxel_vertex_colors(obj, vertex_colors):
        return VoxelUtils.set_voxelizer_voxel_attribute(obj, VoxelUtils.get_voxelizer_voxel_vertex_colors_attr_name(), vertex_colors)

    @staticmethod
    def set_voxelizer_voxel_uvmap(obj, uvmap):
        return VoxelUtils.set_voxelizer_voxel_attribute(obj, VoxelUtils.get_voxelizer_voxel_uv_attr_name(), uvmap)

    @staticmethod
    def set_voxelizer_voxel_attribute(obj, attr_name, value):
        mod = VoxelUtils.get_voxelizer_modifier(obj)
        if not mod or not obj:
            return False
        if value == mod[attr_name]:
            return False
        mod[attr_name] = value
        obj.modifiers.update()
        obj.update_tag()
        return True

    @staticmethod
    def get_voxelizer_voxel_modifier_attributes(obj: bpy.types.Object):
        mod = VoxelUtils.get_voxelizer_modifier(obj)
        voxel_size = 0
        uvmap = "" #"UVMap"
        color = "" #"Col"
        voxel_size = VoxelUtils.get_voxelizer_voxel_size(obj)
        if mod:
            uvmap = mod[VoxelUtils.get_voxelizer_voxel_uv_attr_name()]
            color = mod[VoxelUtils.get_voxelizer_voxel_vertex_colors_attr_name()]
        elif obj.voxelized:
            uvmap = obj.data.uv_layers[0].name if len(obj.data.uv_layers) else None
            color = obj.data.color_attributes[0].name if len(obj.data.color_attributes) else None
        return voxel_size, uvmap, color

    @staticmethod
    def get_mesh_center_of_mass_world(obj):
        vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
        return sum(vertices, mathutils.Vector()) / len(vertices)

    @staticmethod
    def get_mesh_center_world(obj):
        import numpy as np
        vertices = np.array([obj.matrix_world @ v.co for v in obj.data.vertices])
        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)
        bounding_box_center = (min_coords + max_coords) / 2.0
        return bounding_box_center

    @staticmethod
    def get_mesh_center_voxel_distance(obj_A, obj_B, voxel_size) -> mathutils.Vector:
        xa, ya, za = VoxelUtils.get_voxel_distance(VoxelUtils.get_mesh_center_world(obj_A), voxel_size)
        xb, yb, zb = VoxelUtils.get_voxel_distance(VoxelUtils.get_mesh_center_world(obj_B), voxel_size)
        return xb - xa, yb - ya, zb - za

    @staticmethod
    def get_voxel_distance(meters, meter_per_voxel) -> int: # meters: np.ndarray
        x, y, z = meters
        return round(x / meter_per_voxel), round(y / meter_per_voxel), round(z / meter_per_voxel)