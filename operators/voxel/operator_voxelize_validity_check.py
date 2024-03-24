import bpy
import bpy_types

from typing import List

from voxility_pro.enums.name_constant import NameConstant # type: ignore

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
        for obj in context.selected_objects:
            print(f"Check for problems in materials in object \"{obj.name}\":")
            for slot in obj.material_slots:
                material = slot.material
                if material:
                    if material.use_nodes:
                        print(f"       => {material.name}")
                        for node in material.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                print("Material:", material.name)
                                print("Principled BSDF Node:", node)
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