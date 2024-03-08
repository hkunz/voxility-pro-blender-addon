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
            self.colors[(round(c.x), round(c.y), round(c.z))] = col
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
        #FIXME check if index out of range
        if m[2]: # either direct color
            return m[2]
        else: # or the color in the image texture
            uv = bm.faces[face_index].loops[0][bm.loops.layers.uv[0]].uv
            px = int((m[3][0]-1) * uv.x)
            py = int((m[3][1]-1) * uv.y)
            pixel = 4 * (m[3][0] * py + px)
            return Color((round(m[4][pixel]*255), round(m[4][pixel+1]*255), round(m[4][pixel+2]*255)))
        #TODO: get vertex colors

    def get_min_max_voxel_dimensions(self):
        min_x, min_y, min_z = round(self.min_values.x), round(self.min_values.y), round(self.min_values.z)
        max_x, max_y, max_z = round(self.max_values.x), round(self.max_values.y), round(self.max_values.z)
        return min_x, min_y, min_z, max_x, max_y, max_z

    def get_voxel_color_data(self):
        min_x, min_y, min_z, max_x, max_y, max_z = self.get_min_max_voxel_dimensions()
        data = []
        for x in range(min_x, max_x + 1):
            layer = []
            for y in range(min_y, max_y + 1):
                row = []
                for z in range(min_z, max_z + 1):
                    color = self.colors.get((x, y, z))
                    if color:
                        row.append((int(color.r), int(color.g), int(color.b), 255))
                    else:
                        row.append((0, 0, 0, 0))
                layer.append(row)
            data.append(layer)
        return data


# Example Usage:
def write_sample_qb_file():
    #from voxility_pro.utils.voxel_writer.qb_writer import Qb, QbMatrix
    obj = bpy.context.active_object
    geometry_nodes_modifier = obj.modifiers["VoxelizeModifier"] # bpy.context.object.modifiers["VoxelizeModifier"].name = "VoxelizeModifier"
    voxel_size = round(geometry_nodes_modifier["Socket_3"], 3)
    reader = FaceColorReader(obj, voxel_size)
    data = reader.get_voxel_color_data()
    file = "C:/out.qb"
    layer = QbMatrix("cube", data, (0, 0, 0))
    qb = Qb()
    qb.matrixList.append(layer)
    qb.save(file)

# write_sample_qb_file()