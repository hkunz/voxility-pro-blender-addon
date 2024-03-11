import struct

from mathutils import Color
from typing import List, Dict, Tuple

import random
import time

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
from mathutils import Color, kdtree, Vector

class FaceColorReader:
    def __init__(self, object, voxel_size):
        dg = bpy.context.evaluated_depsgraph_get()
        e = object.evaluated_get(dg)

        bm = bmesh.new()
        bm.from_object(object, dg)
        bm.faces.ensure_lookup_table()

        materials = self.get_materials(e)
        centers_kd = kdtree.KDTree(len(bm.faces)) # create a kd tree for fast distance comparison

        centers_voxel = []
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = -float('inf'), -float('inf'), -float('inf')

        for f in bm.faces:
            center = f.calc_center_median()
            normal = f.normal
            area = sqrt(f.calc_area()) # as a face is a square, edge length is sqrt the surface
            displacement = -0.5 * normal * area
            voxel_center = center + displacement
            voxel_center.x, voxel_center.y, voxel_center.z = (voxel_center.x / voxel_size - 0.5), (voxel_center.y / voxel_size - 0.5), (voxel_center.z / voxel_size - 0.5)
            centers_voxel.append(voxel_center)
            min_x, min_y, min_z = min(min_x, voxel_center.x), min(min_y, voxel_center.y), min(min_z, voxel_center.z)
            max_x, max_y, max_z = max(max_x, voxel_center.x), max(max_y, voxel_center.y), max(max_z, voxel_center.z)

        self.min_values = Vector((round(min_x), round(min_y), round(min_z)))
        self.max_values = Vector((round(max_x), round(max_y), round(max_z)))

        for i, f in enumerate(bm.faces):
            centers_kd.insert(centers_voxel[i], i) # populate the tree

        centers_kd.balance()

        epsilon = 0.001
        self.colors = {}

        for i, c in enumerate(centers_voxel):
            if not c:
                continue
            col = self.get_face_color(bm, materials, i)
            self.colors[(round(c.x-min_x), round(c.y-min_y), round(c.z-min_z))] = col
            # mark as processed
            for _, fi, d in centers_kd.find_n(c, 6):
                if d < epsilon:
                    centers_voxel[fi] = None

    def get_material(self, i, m):
        p = m.node_tree.nodes['Principled BSDF']
        if len(p.inputs[0].links) == 0:
            c = p.inputs[0].default_value
            return (i, m, Color((round(c[0]*255), round(c[1]*255), round(c[2]*255))), None, None)
        else:
            tex_node = p.inputs[0].links[0].from_node
            image = tex_node.image
            return (i, m, None, image.size, image.pixels[:])

    def get_materials(self, obj):
        return [self.get_material(i, m) for i, m in enumerate(obj.data.materials) if m]

    def get_face_color(self, bm, materials, face_index):
        m = materials[bm.faces[face_index].material_index]
        c = m[2]
        if c: # either direct color
            return (round(c.r), round(c.g), round(c.b))
        else: # or the color in the image texture
            uv = bm.faces[face_index].loops[0][bm.loops.layers.uv[0]].uv
            px = int((m[3][0]-1) * uv.x)
            py = int((m[3][1]-1) * uv.y)
            pixel = 4 * (m[3][0] * py + px)
            return (round(m[4][pixel]*255), round(m[4][pixel+1]*255), round(m[4][pixel+2]*255))
        #TODO: get vertex colors

    def get_voxel_dimensions(self):
        min_x, min_y, min_z = round(self.min_values.x), round(self.min_values.y), round(self.min_values.z)
        max_x, max_y, max_z = round(self.max_values.x), round(self.max_values.y), round(self.max_values.z)
        return max_x-min_x+1, max_y-min_y+1, max_z-min_z+1


def test_write_qb(size_x, size_y, size_z, colors) -> None:
    EMPTY_COLOR = (0, 0, 0, 0)

    start = time.time()
    data = [(*colors[x, y, z], 255) 
                if colors.get((x,y,z)) else EMPTY_COLOR 
                for z in range(size_z)
                for y in range(size_y)
                for x in range(size_x)]
    print("HEYY === ", time.time() - start)

    write(size_x, size_y, size_z, data)
    

def write(size_x, size_y, size_z, data):
    file: str = "C:/ou.qb"
    start = time.time()
    layer: QbMatrix = QbMatrix("cube", size_x, size_y, size_z, data, (0, 0, 0))
    qb: Qb = Qb()

    qb.matrixList.append(layer)
    qb.save(file)
    print("Write time ========", time.time() - start)

def test_read_and_write():
    start = time.time()
    
    obj = bpy.context.active_object
    geometry_nodes_modifier = obj.modifiers[-1]
    voxel_size = round(geometry_nodes_modifier["Socket_3"], 3)
    reader = FaceColorReader(obj, voxel_size)
    print("Read time ========", time.time() - start)

    max_x, max_y, max_z = reader.get_voxel_dimensions()
    start = time.time()
    colors = reader.colors

    test_write_qb(max_x, max_y, max_z, colors)

    

test_read_and_write()




def test_lemon():
    size_x=4
    size_y=4
    size_z=4
    #amount=10
    #colors = generate(size_x, size_y, size_z, amount)
    colors = {(2, 1, 0): (0.5498605976063163, 0.15785355756280972, 0.06738642483004531), (2, 0, 3): (0.44770916720010123, 0.12533987418453063, 0.7314108279878017), (1, 1, 3): (0.9121835620335241, 0.17995483722772, 0.3435748589736378), (1, 2, 1): (0.7741294241033942, 0.387267447465124, 0.5178432971673648), (1, 0, 3): (0.8940615518345553, 0.036730708410385726, 0.47701350324828107), (2, 0, 2): (0.5861547992102003, 0.3252095663155552, 0.429394337609752), (2, 2, 3): (0.5020412915301437, 0.9720496926315347, 0.6506084245229163), (2, 2, 1): (0.9261833304095134, 0.5130287107377194, 0.10950152665801305), (3, 2, 1): (0.04952230908734201, 0.7944893930962992, 0.08394754913473845), (0, 3, 0): (0.7580661850186802, 0.7489058297177904, 0.37813519984854316)}
    print(len(colors))

    import time
    start = time.time()
    test_write_qb(size_x, size_y, size_z, colors)
    print("===2 time taken is", time.time() - start)
    
    
#test_lemon()