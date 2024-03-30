import bpy
import math
import mathutils


class BakeUtility:
    def __init__(self, context=None, data=None) -> None:
        C = self.context = context if context else bpy.context
        self.data = data if data else bpy.data
        self.bake_images = None
        self.bake_image = None
        self.processed_materials = None
        self.prev_uvmap_names = None

    @staticmethod
    def setup() -> None:
        s = bpy.context.scene
        s.cycles.device = 'GPU'
        s.render.engine = 'CYCLES'
        s.cycles.use_adaptive_sampling = False
        s.cycles.samples = 1
        s.cycles.bake_type = 'DIFFUSE'
        s.render.bake.use_pass_direct = False
        s.render.bake.use_pass_indirect = False
        s.render.bake.margin = 0
        s.cycles.use_denoising = False

    def set_object_selected(self, obj, select):
        obj.select_set(select)
        self.context.view_layer.objects.active = obj if select else None

    def bake(self, bake_objects):
        self.processed_materials = set()
        self.bake_images = []

        for obj in bake_objects:
            obj.select_set(False)

        for obj in bake_objects:
            self.set_object_selected(obj, True)
            try:
                self.bake_object(obj)
            except Exception as e:
                self.cleanup()
                raise
            finally:
                self.cleanup_processed_materials()
                self.set_object_selected(obj, False)

    def bake_object(self, obj) -> None:
        for m in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=m.name)

        self.add_image_texture_for_baking(obj)
        self.prev_uvmap_names = [uv_layer.name for uv_layer in obj.data.uv_layers]
        self.create_uv_map_and_unwrap(obj)

        bpy.ops.object.bake(type='DIFFUSE')

        self.scale_uv_faces_to_zero(obj)
        self.setup_new_material_with_baked_texture(obj)

        for uvname in self.prev_uvmap_names:
            obj.data.uv_layers.remove(obj.data.uv_layers[uvname])

    def cleanup_processed_materials(self):
        for mat in self.processed_materials:
            mat.node_tree.nodes.remove(mat.node_tree.nodes[mat.name])
        self.processed_materials.clear()

    def add_image_texture_for_baking(self, obj):
        D = self.data
        pixel_size = int(math.ceil(math.sqrt(len(obj.data.polygons))))
        self.bake_image = D.images.new(f"Image.VoxilityBaking.{obj.name}", pixel_size, pixel_size)
        self.bake_images.append(self.bake_image)
        print(f"Created temporary bake image: {self.bake_image}")

        for slot in obj.material_slots:
            mat = slot.material
            if not mat or mat in self.processed_materials:
                continue
            nodes = mat.node_tree.nodes
            for n in nodes:
                n.select = False
            tex_node = nodes.new(type='ShaderNodeTexImage')
            self.processed_materials.add(mat)
            tex_node.image = self.bake_image
            tex_node.name = mat.name
            tex_node.select = True
            nodes.active = tex_node

    def create_uv_map_and_unwrap(self, obj):
        uvmap = obj.data.uv_layers.new(name="UVMap.VoxilityBaking")
        idx = obj.data.uv_layers.active_index = obj.data.uv_layers.find(uvmap.name)
        obj.data.uv_layers[idx].active = True
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

    def cleanup(self):
        D = self.data
        for img in self.bake_images:
            print(f"Remove temporary bake image: {img}")
            D.images.remove(img)


# usage:
def bake_all_selected_objects():
    from bpy import context as C
    from bpy import data as D
    previous_selection = C.selected_objects
    previous_active_object = C.active_object
    bpy.ops.object.duplicate(linked=False) # linked=False does not work if more than 1 object selected
    bpy.ops.object.make_single_user(object=True, obdata=True) # so we need to manually make it single user
    duplicated_objects = C.selected_objects

    # Important code start =====================
    BakeUtility.setup()
    b = BakeUtility()
    b.bake(duplicated_objects)
    # do stuff you need to do with the result before deleting and cleaning up
    b.cleanup()
    # Important code end =====================

    for obj in duplicated_objects[:]:
        D.objects.remove(obj)

    for obj in previous_selection:
            obj.select_set(True)

    if previous_active_object:
        C.view_layer.objects.active = previous_active_object

#bake_all_selected_objects()