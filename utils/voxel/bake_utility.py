import bpy
import math
import mathutils


class BakeUtility:
    def __init__(self, context, data) -> None:
        C = self.context = context
        self.data = data
        self.previous_selection = C.selected_objects[:]
        self.previous_active_object = C.active_object
        self.bake_image = None
        self.processed_materials = set()

    def setup(self) -> None:
        C = self.context
        C.scene.cycles.device = 'GPU'
        C.scene.render.engine = 'CYCLES'
        C.scene.cycles.use_adaptive_sampling = False
        C.scene.cycles.samples = 1
        C.scene.cycles.bake_type = 'DIFFUSE'
        C.scene.render.bake.use_pass_direct = False
        C.scene.render.bake.use_pass_indirect = False
        C.scene.render.bake.margin = 0
        C.scene.cycles.use_denoising = False

    def bake(self):
        C = self.context
        bpy.ops.object.duplicate()
        duplicated_objects = C.selected_objects[:]

        for obj in duplicated_objects:
            self.bake_object(obj)

    def bake_object(self, obj) -> None:
        C = self.context
        D = self.data
        self.processed_materials.clear()
        obj.select_set(True)
        C.view_layer.objects.active = obj

        for m in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=m.name)

        self.add_image_texture_for_baking(obj)
        prev_uvmap_names = [uv_layer.name for uv_layer in obj.data.uv_layers]
        self.create_uv_map_and_unwrap(obj)

        bpy.ops.object.bake(type='DIFFUSE')

        self.scale_uv_faces_to_zero(obj)
        self.setup_new_material_with_baked_texture(obj)

        for uvname in prev_uvmap_names:
            obj.data.uv_layers.remove(obj.data.uv_layers[uvname])

        #read_voxel_colors
        #self.cleanup

    def add_image_texture_for_baking(self, obj):
        D = self.data
        pixel_size = int(math.ceil(math.sqrt(len(obj.data.polygons))))
        self.bake_image = D.images.new(f"Image.VoxilityBaking", pixel_size, pixel_size)

        for slot in obj.material_slots:
            mat = slot.material
            if not mat or mat in self.processed_materials:
                continue
            nodes = mat.node_tree.nodes
            for n in nodes:
                n.select = False
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.image = self.bake_image
            tex_node.name = mat.name
            tex_node.select = True
            nodes.active = tex_node
            self.processed_materials.add(mat)

    def create_uv_map_and_unwrap(self, obj):
        obj.data.uv_layers.new(name="UVMap.VoxilityBaking")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_seam(clear=False)
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0)
        bpy.ops.object.mode_set(mode='OBJECT')

    def scale_uv_faces_to_zero(self, obj):
        for poly in obj.data.polygons:
            # Calculate the average UV coordinate of the face
            avg_uv = mathutils.Vector((0.0, 0.0))
            for loop_index in poly.loop_indices:
                uv_coord = obj.data.uv_layers.active.data[loop_index].uv
                avg_uv += uv_coord
            avg_uv /= len(poly.loop_indices)
            # Move each UV coordinate towards the average UV coordinate (scaling inward)
            for loop_index in poly.loop_indices:
                uv_coord = obj.data.uv_layers.active.data[loop_index].uv
                uv_coord += (avg_uv - uv_coord) * 1.0

    def setup_new_material_with_baked_texture(self, obj):
        D = self.data
        obj.data.materials.clear()
        mat = D.materials.new(name="VoxilityBakingMaterial")
        obj.data.materials.append(mat)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        tex_node = nodes.new(type='ShaderNodeTexImage')
        tex_node.image = self.bake_image
        mat.node_tree.links.new(tex_node.outputs['Color'], nodes['Principled BSDF'].inputs['Base Color'])
    
    def cleanup(self, obj):
        for mat in self.processed_materials:
            mat.node_tree.nodes.remove(mat.node_tree.nodes[mat.name])
        D = self.data
        D.images.remove(self.bake_image)
        D.objects.remove(obj)

        for obj in self.previous_selection:
            obj.select_set(True)

        if self.previous_active_object:
            self.context.view_layer.objects.active = self.previous_active_object