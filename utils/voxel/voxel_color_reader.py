import bpy
import bmesh

from math import sqrt
from mathutils import Vector
from typing import Tuple

from voxility_pro.utils.color_utils import ColorUtils # type: ignore

Coordinate = Tuple[int, int, int]

class VoxelColorReader:
    RIGHT_ANGLED_COORDINATE_SYSTEM = 0
    LEFT_HANDED_COORDINATE_SYSTEM = 1

    COLOR_SPACE_LINEAR = 0
    COLOR_SPACE_SRGB = 1

    def __init__(self, object, voxel_size, coordinate_system, color_space, uv_name):

        dg = bpy.context.evaluated_depsgraph_get()
        e = object.evaluated_get(dg)

        self.voxel_size = voxel_size
        self.color_space = color_space
        self.coordinate_system = coordinate_system # We currently only read colors for QB files for qb_writer.py which uses LEFT_HANDED_COORDINATE_SYSTEM
        self.object = object
        self.uv_name = uv_name
        self.bm = bmesh.new()
        self.bm.from_object(object, dg)
        self.bm.faces.ensure_lookup_table()
        self.size_x, self.size_y, self.size_z = 0, 0, 0
        uv_maps = object.data.uv_layers.keys()

        if len(object.data.uv_layers) > 1:
            print("Warning:", f"Multiple UV layers not supported {uv_maps}")
        if self.uv_name not in uv_maps:
            print("Warning:", f"\"{self.uv_name}\" not found in UV Maps")

        self.materials = [self.get_material(m) for i, m in enumerate(e.data.materials) if m]
        self.colors = {}

        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = -float('inf'), -float('inf'), -float('inf')

        for f in self.bm.faces:
            center = f.calc_center_median()
            voxel_center = center + (-0.5 * f.normal * sqrt(f.calc_area()))
            center_x, center_y, center_z = self.get_remapped_coordinates(round(voxel_center.x / voxel_size - 0.5), round(voxel_center.y / voxel_size - 0.5), round(voxel_center.z / voxel_size - 0.5))
            center = (center_x, center_y, center_z)

            if not center in self.colors:
                col = self.get_voxel_color(f.index)
                self.colors[center] = col
                min_x, min_y, min_z = min(min_x, center_x), min(min_y, center_y), min(min_z, center_z)
                max_x, max_y, max_z = max(max_x, center_x), max(max_y, center_y), max(max_z, center_z)

        self.min_x, self.min_y, self.min_z = (round(min_x), round(min_y), round(min_z))
        self.max_x, self.max_y, self.max_z = (round(max_x), round(max_y), round(max_z))
        self.size_x, self.size_y, self.size_z = max_x-min_x+1, max_y-min_y+1, max_z-min_z+1

    def get_up_axis_amount(self):
        if self.coordinate_system == VoxelColorReader.LEFT_HANDED_COORDINATE_SYSTEM:
            return "y", -int(self.size_y / 2)
        return "z", -int(self.size_z / 2)

    def get_remapped_coordinates(self, cx, cy, cz) -> Coordinate:
        if self.coordinate_system == VoxelColorReader.LEFT_HANDED_COORDINATE_SYSTEM:
            return cy, cz, cx #Y > X #Z > Y #X > Z
        return cx, cy, cz

    def get_object_center(self, zero_axis=None):
        x = 0
        y = 0
        z = 0 # keep voxel object above the floor
        x, y, z = self.get_remapped_coordinates(x, y, z)
        if not zero_axis == "x": x = -int(self.size_x / 2)
        if not zero_axis == "y": y = -int(self.size_y / 2)
        if not zero_axis == "z": z = -int(self.size_z / 2)
        return (x, y, z)

    def get_principled_bsdf(self, m):
        nodes = m.node_tree.nodes
        if "Principled BSDF" in nodes:
            return nodes["Principled BSDF"]
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                return node
        print(f"Warning: No Principled BSDF found in material \"{m.name}\"")
        return None

    def get_color_space_display_color(self, r, g, b, check_space=True):
        if check_space and self.color_space == VoxelColorReader.COLOR_SPACE_SRGB:
            r, g, b = ColorUtils.linear_to_srgb(r), ColorUtils.linear_to_srgb(g), ColorUtils.linear_to_srgb(b)
        return (round(r*255), round(g*255), round(b*255), 255)

    def get_unsocketed_base_color(self, c):
        return self.get_color_space_display_color(c[0], c[1], c[2], False)

    def get_socketed_image_texture(self, p):
        tex_node = p.inputs[0].links[0].from_node
        image = tex_node.image
        return (image.size, image.pixels[:])

    def get_socketed_vertex_colors(self, attr):
        attributes = self.bm.loops.layers.float_color
        if attr in attributes:
            return (attributes[attr],)
        print(f"Warning: Multiple Color Attributes not supported: {self.object.data.color_attributes.keys()}")
        return (0, 0, 0, 255)

    def get_material(self, m):
        p = self.get_principled_bsdf(m)
        if not p:
            return (0, 0, 0, 255) # no principled bsdf found so return black
        base_color = p.inputs[0]
        link = base_color.links[0] if len(base_color.links) else None
        if not link: # nothing connected to Base Color socket
            return self.get_unsocketed_base_color(base_color.default_value)
        if link.from_node.type == 'TEX_IMAGE':
            return self.get_socketed_image_texture(p)
        if link.from_node.type == 'VERTEX_COLOR' or link.from_node.type == 'ATTRIBUTE':
            return self.get_socketed_vertex_colors(link.from_node.layer_name if hasattr(link.from_node, 'layer_name') else link.from_node.attribute_name)
        print(f"Warning: Unsupported node type \"{link.from_node.type}\" connected to Principled BSDF in material \"{m.name}\"")
        return (0, 0, 0, 255) # unhandled or undefined linked node

    def get_face_uv(self, f):
        uvs = self.bm.loops.layers.uv # uvs.keys() = ['UVMap.001', 'UVMap'] note index zero starts at list bottom
        if not self.uv_name in uvs:
            return None
        uv = f.loops[0][uvs[self.uv_name]].uv  # uvs[self.uv_name] returns a BMLayerItem which can be used as key
        return uv

    def get_face_uv_deprecated(self, f):
        uvs = self.bm.loops.layers.float_vector # uvs.keys() = ['UVMap.001', 'UVMap'] note index zero starts at list bottom
        if not self.uv_name in uvs:
            return None
        uv = f.loops[0][uvs[self.uv_name]] # uvs[self.uv_name] returns a BMLayerItem which can be used as key
        return uv

    def get_voxel_color_texture(self, face, size, pxs):
        uv = self.get_face_uv(face) if bpy.app.version > (3, 4, 0) else self.get_face_uv_deprecated(face)
        if not uv:
            return (255, 192, 203, 255)
        px = round((size[0]-1) * (uv.x%1))
        py = round((size[1]-1) * (uv.y%1))
        pixel = 4 * (size[0] * py + px)
        return self.get_color_space_display_color(pxs[pixel], pxs[pixel+1], pxs[pixel+2], False)

    def get_voxel_color_vertex(self, color):
        return self.get_color_space_display_color(color.x, color.y, color.z, False)

    def get_voxel_color(self, face_index):
        f = self.bm.faces[face_index]
        if f.material_index >= len(self.materials):
            return (255, 192, 203, 255) # pink for deleted material (last material deleted)
        m = self.materials[f.material_index]
        tuple_len = len(m)
        if tuple_len == 4: # either direct color as tuple length 4
            return m
        if tuple_len == 2: # or the color in the image texture
            return self.get_voxel_color_texture(f, m[0], m[1])
        if tuple_len == 1: # or vertex color
            return self.get_voxel_color_vertex(f.loops[0][m[0]])
        print(f"Warning: Unhandled tuple length: {tuple_len}")
        return (0, 0, 0, 255)

    def get_voxel_dimensions(self):
        return self.size_x, self.size_y, self.size_z

    def get_color_data(self): # coordinate_system = RIGHT_ANGLED_COORDINATE_SYSTEM
        min_x, min_y, min_z = self.min_x, self.min_y, self.min_z
        max_x, max_y, max_z = self.max_x, self.max_y, self.max_z
        empty = (0, 0, 0, 0)
        data = [
            self.colors[x, y, z] if self.colors.get((x,y,z)) else empty 
            for z in range(min_z, max_z + 1)
            for y in range(min_y, max_y + 1)
            for x in range(min_x, max_x + 1)
        ]
        return data


# Example Usage:
def test_read_voxel_colors_and_write_qb_file():
    import time
    s = time.time()
    obj = bpy.context.active_object
    geometry_nodes_modifier = obj.modifiers[-1]
    voxel_size_value = geometry_nodes_modifier["Socket_2" if bpy.app.version >= (4,0,0) else "Input_1"]
    voxel_size = round(voxel_size_value, 3)
    reader = VoxelColorReader(obj, voxel_size, "UVMap")
    print("Read time:", time.time() - s)
    file: str = "C:/out.qb"
    start = time.time()
    layer: QbMatrix = QbMatrix("cube", *reader.get_voxel_dimensions(), reader.get_color_data(), (0, 0, 0)) # type: ignore
    qb: Qb = Qb() # type: ignore
    qb.matrixList.append(layer)
    start = time.time()
    qb.save(file)
    print("Write time ========", time.time() - start)
    print("Total time ========", time.time() - s)

# test_read_voxel_colors_and_write_qb_file()