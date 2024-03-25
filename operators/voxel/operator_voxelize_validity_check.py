import bpy
import bpy_types

from typing import List

from voxility_pro.enums.name_constant import NameConstant # type: ignore

class VoxelError:
    ERROR_NONE = 0
    ERROR_MULTIPLE_BSDF_NODES = 1
    ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES = 2
    ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE = 3

    @staticmethod
    def get_error(e):
        if e == VoxelError.ERROR_NONE:
            return "No errors"
        if e == VoxelError.ERROR_MULTIPLE_BSDF_NODES:
            return "Only one Principled BSDF node allowed"
        if e == VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES:
            return "Only one Material Output node allowed"
        return "Undefined Error"

class OBJECT_OT_OperatorVoxelizeValidityCheck(bpy.types.Operator):
    bl_idname = "object.voxility_voxelize_validity_check"
    bl_label = "Voxility Voxelize Validity Check"
    bl_description = "Check for potential issues in the materials before voxel conversion"
    bl_options = {'REGISTER'}

    temp: bpy.props.StringProperty(
        name="Temp String",
        description="Temp descrption",
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    def execute(self, context):
        errors = []
        for obj in context.selected_objects:
            print(f"Check for problems in materials in object \"{obj.name}\":")
            for slot in obj.material_slots:
                material = slot.material
                if not material or not material.use_nodes:
                    continue
                bsdf_node = None
                output_node = None
                for n in material.node_tree.nodes:
                    t = n.type
                    if t == 'BSDF_PRINCIPLED':
                        if bsdf_node and VoxelError.ERROR_MULTIPLE_BSDF_NODES not in errors:
                            errors.append(VoxelError.ERROR_MULTIPLE_BSDF_NODES)
                        bsdf_node = n
                        node = bsdf_node.inputs[0].links[0].from_node
                        print("node ==== ", node, node.type)
                    elif t == 'OUTPUT_MATERIAL':
                        if output_node and VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES not in errors:
                            errors.append(VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES)
                        output_node = n
                        links = output_node.inputs[0].links
                        linked_node = links[0].from_node if len(links) > 0 else None
                        if not linked_node and VoxelError.ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE not in errors:
                            errors.append(VoxelError.ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE)
                        print("node input in material output: ", node, node.type)
        if errors:
            print(f"Error: {errors}")
            for i, e in enumerate(errors):
                print(f"{i}.) {VoxelError.get_error(e)}")

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        active_object: bpy_types.Object = context.active_object

        selected_objects: List[bpy_types.Object] = context.selected_objects
        if context.mode != 'OBJECT' or not selected_objects or active_object not in selected_objects:
            return False
        for o in selected_objects:
            if o.type != 'MESH' or not o.data.polygons:
                return False
        return True

def register():
    bpy.utils.register_class(OBJECT_OT_OperatorVoxelizeValidityCheck)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_OperatorVoxelizeValidityCheck)

# example usage:
# if __name__ == "__main__":
#    register()
#    bpy.ops.object.voxility_voxelize_validity_check()