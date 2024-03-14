import struct

from typing import List, Dict, Tuple

class QbMatrix:
    def __init__(self, name: str, size_x, size_y, size_z, data, pos: Tuple[int, int, int]):
        self.name = name
        self.pos = pos
        self.data = data
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z

class Qb:
    def __init__(self) -> None:
        self.version: int = 0x0101
        self.colorFormat: int = 0
        self.zAxisOrientation: int = 0
        self.compressed: int = 0
        self.visibilityMaskEncoded: int = 0
        self.matrixList: List[QbMatrix] = []

    def add_matrix(self, name: str, data, pos: Tuple[int, int, int]) -> None:
        self.matrixList.append(QbMatrix(name, data, pos))

    def save(self, filename: str) -> None:
        with open(filename, "wb") as f: # type(f) = <class '_io.BufferedWriter'>
            self.compressed = 0  # Compression saving not supported

            f.write(struct.pack("I", self.version))
            f.write(struct.pack("I", self.colorFormat))
            f.write(struct.pack("I", self.zAxisOrientation))
            f.write(struct.pack("I", self.compressed))
            f.write(struct.pack("I", self.visibilityMaskEncoded))
            f.write(struct.pack("I", len(self.matrixList)))

            for matrix in self.matrixList: # QbMatrix
                self.save_matrix(f, matrix)

    def save_matrix(self, file: object, matrix: QbMatrix) -> None:
        file.write(struct.pack("B", len(matrix.name)))
        file.write(struct.pack(str(len(matrix.name.encode('ascii')))+"s", matrix.name.encode('ascii')))
        size_x = matrix.size_x
        size_y = matrix.size_y
        size_z = matrix.size_z
        file.write(struct.pack("III", size_x, size_y, size_z))
        file.write(struct.pack("iii", matrix.pos[0], matrix.pos[1], matrix.pos[2]))

        file.write(bytes([c for color in matrix.data for c in color]))


import bpy
import bmesh

from math import sqrt
from mathutils import Vector

class FaceColorReader:
    def __init__(self, object, voxel_size, uv_name):

        dg = bpy.context.evaluated_depsgraph_get()
        e = object.evaluated_get(dg)

        self.object = object
        self.uv_name = uv_name
        self.bm = bmesh.new()
        self.bm.from_object(object, dg)
        self.bm.faces.ensure_lookup_table()
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
            normal = f.normal
            area = sqrt(f.calc_area()) # as a face is a square, edge length is sqrt the surface
            displacement = -0.5 * normal * area
            voxel_center = center + displacement

            center_x, center_y, center_z = round(voxel_center.x / voxel_size - 0.5), round(voxel_center.y / voxel_size - 0.5), round(voxel_center.z / voxel_size - 0.5)
            center = (center_x, center_y, center_z)

            if not center in self.colors:
                col = self.get_face_color(f.index)
                self.colors[center] = col
                
                min_x, min_y, min_z = min(min_x, center_x), min(min_y, center_y), min(min_z, center_z)
                max_x, max_y, max_z = max(max_x, center_x), max(max_y, center_y), max(max_z, center_z)

        self.min_values = Vector((round(min_x), round(min_y), round(min_z)))
        self.max_values = Vector((round(max_x), round(max_y), round(max_z)))

    def get_principled_bsdf(self, m):
        nodes = m.node_tree.nodes
        if "Principled BSDF" in nodes:
            return nodes["Principled BSDF"]
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                return node
        print(f"Warning: No Principled BSDF found in material \"{m.name}\"")
        return None

    def get_material(self, m):
        p = self.get_principled_bsdf(m)
        if not p:
            return (0, 0, 0, 255) # no principled bsdf found so return black
        base_color = p.inputs[0]
        link = base_color.links[0] if len(base_color.links) else None
        if not link: # nothing connected to Base Color socket
            c = base_color.default_value
            return (round(c[0]*255), round(c[1]*255), round(c[2]*255), 255)
        if link.from_node.type == 'TEX_IMAGE':
            tex_node = p.inputs[0].links[0].from_node
            image = tex_node.image
            return (image.size, image.pixels[:])
        if link.from_node.type == 'VERTEX_COLOR':
            c = base_color.default_value
            attr = link.from_node.layer_name
            attributes = self.bm.loops.layers.float_color
            if attr in attributes:
                return (attributes[attr],)
            else:
                print(f"Warning: Multiple Color Attributes not supported: {self.object.data.color_attributes.keys()}")
                return (0, 0, 0, 255)
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

    def get_face_color(self, face_index):
        f = self.bm.faces[face_index]
        if f.material_index >= len(self.materials):
            return (255, 192, 203, 255) # pink for deleted material (last material deleted)
        m = self.materials[f.material_index]
        tuple_len = len(m)
        if tuple_len == 4: # either direct color as tuple length 4
            return m
        if tuple_len == 2: # or the color in the image texture
            uv = self.get_face_uv(f) if bpy.app.version > (3, 4, 0) else self.get_face_uv_deprecated(f)
            if not uv:
                return (255, 192, 203, 255)
            size = m[0]
            px = int((size[0]-1) * (uv.x%1))
            py = int((size[1]-1) * (uv.y%1))
            pixel = 4 * (size[0] * py + px)
            pxs = m[1]
            return (round(pxs[pixel]*255), round(pxs[pixel+1]*255), round(pxs[pixel+2]*255), 255)
        if tuple_len == 1: # or vertex color
            color = f.loops[0][m[0]]
            color_tuple = (round(color.x*255), round(color.y*255), round(color.z*255), 255)
            return color_tuple
        print(f"Warning: Unhandled tuple length: {tuple_len}")
        return (0, 0, 0, 255)

    def get_voxel_dimensions(self):
        min_x, min_y, min_z, max_x, max_y, max_z = self.get_voxel_ranges()
        return max_x-min_x+1, max_y-min_y+1, max_z-min_z+1

    def get_voxel_ranges(self):
        min_x, min_y, min_z = round(self.min_values.x), round(self.min_values.y), round(self.min_values.z)
        max_x, max_y, max_z = round(self.max_values.x), round(self.max_values.y), round(self.max_values.z)
        return min_x, min_y, min_z, max_x, max_y, max_z

    def get_color_data(self):
        min_x, min_y, min_z, max_x, max_y, max_z = self.get_voxel_ranges()
        empty = (0, 0, 0, 0)
        data = [self.colors[x, y, z] if self.colors.get((x,y,z)) else empty 
                for z in range(min_z, max_z + 1)
                for y in range(min_y, max_y + 1)
                for x in range(min_x, max_x + 1)]
        return data


# Example Usage:
def test_read_voxel_colors_and_write_qb_file():
    import time
    s = time.time()
    obj = bpy.context.active_object
    geometry_nodes_modifier = obj.modifiers[-1]
    voxel_size_value = geometry_nodes_modifier["Socket_2" if bpy.app.version >= (4,0,0) else "Input_1"]
    voxel_size = round(voxel_size_value, 3)
    reader = FaceColorReader(obj, voxel_size, "UVMap")
    print("Read time ========", time.time() - s)
    file: str = "C:/out.qb"
    start = time.time()
    layer: QbMatrix = QbMatrix("cube", *reader.get_voxel_dimensions(), reader.get_color_data(), (0, 0, 0)) # type: ignore
    qb: Qb = Qb() # type: ignore
    qb.matrixList.append(layer)
    start = time.time()
    qb.save(file)
    print("Write time ========", time.time() - start)
    print("Total time ========", time.time() - s)

test_read_voxel_colors_and_write_qb_file()