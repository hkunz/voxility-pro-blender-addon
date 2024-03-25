import bpy
import bpy_types

from typing import List

from voxility_pro.operators.operator_generic_popup import OperatorGenericPopup

class VoxelError:
    ERROR_NONE = 0
    ERROR_MULTIPLE_BSDF_NODES = 1
    ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES = 2
    ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE = 3
    ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE = 4
    ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT = 5
    ERROR_MISSING_MATERIAL_OUTPUT_NODE = 6
    WARNING_NO_MATERIALS = 7

    @staticmethod
    def get_error(e):
        if e == VoxelError.ERROR_NONE:
            return "No errors"
        if e == VoxelError.ERROR_MULTIPLE_BSDF_NODES:
            return "Only one \"Principled BSDF\" node allowed"
        if e == VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES:
            return "Only one \"Material Output\" node allowed"
        if e == VoxelError.ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE:
            return "Missing input to \"Material Output\" node's \"Surface\" socket"
        if e == VoxelError.ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE:
            return "Only \"Princpled BSDF\" allowed in \"Material Output\" node"
        if e == VoxelError.ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT:
            return "Only \"Image Texture\" or \"Color Attribute\" nodes allowed in \"Principled BSDF\" node's \"Base Color\" socket" # 91 characters max equivalent to 520 width
        if e == VoxelError.ERROR_MISSING_MATERIAL_OUTPUT_NODE:
            return "Missing \"Material Output\" node"
        if e == VoxelError.WARNING_NO_MATERIALS:
            return "No materials found (or \"Use Nodes\" is disabled)"
        return "Undefined Error"

class OBJECT_OT_OperatorVoxelizeValidityCheck(OperatorGenericPopup):
    bl_idname = "object.voxility_voxelize_validity_check"
    bl_label = "Voxility Voxelize Validity Check"
    bl_description = "Check for potential issues in the materials before voxel conversion"
    bl_options = {'REGISTER'}

    MIN_POPUP_WIDTH = 250
    MAX_POPUP_WIDTH = 600
    MAX_ERROR_CHARS = 100
    width=0

    temp: bpy.props.StringProperty(
        name="Temp String",
        description="Temp descrption",
    ) # type: ignore https://blender.stackexchange.com/questions/311578/how-do-you-correctly-add-ui-elements-to-adhere-to-the-typing-spec/311770#311770

    def __init__(self):
        self.errors = None

    def invoke(self, context: bpy_types.Context, event: bpy.types.Event) -> set[str]:
        self.errors = self.get_errors(context)
        self.width = self.MIN_POPUP_WIDTH
        for o, e in self.errors:
            self.width = int(max(self.width, (len(VoxelError.get_error(e)) + len(o.name))/self.MAX_ERROR_CHARS*self.MAX_POPUP_WIDTH))
        return super().invoke(context, event)

    def execute(self, context):
        # No need to do anything when OK is clicked
        self.exec_message = None
        super().execute(context)
        return {'FINISHED'}

    def draw(self, context: bpy_types.Context) -> None:
        layout: bpy.types.UILayout = self.layout
        col: bpy.types.UILayout = layout.column()

        if not self.errors:
            col.label(text="No problems found")
            return

        for i, tuple in enumerate(self.errors):
            err = f"{tuple[0].name}: {VoxelError.get_error(tuple[1])}"
            col.label(text=err)

    def get_errors(self, context):
        errors = []
        for obj in context.selected_objects:
            #print(f"Check for problems in materials in object \"{obj.name}\":")
            num_mat = 0
            for slot in obj.material_slots:
                mat = slot.material
                if not mat or not mat.use_nodes:
                    continue
                num_mat += 1
                bsdf_node = None
                output_node = None
                for n in mat.node_tree.nodes:
                    t = n.type
                    if t == 'BSDF_PRINCIPLED':
                        if bsdf_node:
                            print("multiple bsdf detected: ", self.add_error(mat, errors, VoxelError.ERROR_MULTIPLE_BSDF_NODES))
                        bsdf_node = n
                        linked_node = self.get_linked_input_node(bsdf_node)
                        lt = linked_node.type if linked_node else None
                        if linked_node and lt != 'VERTEX_COLOR' and lt != 'ATTRIBUTE' and lt != 'TEX_IMAGE':
                            self.add_error(mat, errors, VoxelError.ERROR_ONLY_TEXTURE_OR_COLOR_ATTR_SUPPORTED_IN_BSDF_COLOR_INPUT)
                    elif t == 'OUTPUT_MATERIAL':
                        if output_node:
                            print("multiple mat-out detected: ", self.add_error(mat, errors, VoxelError.ERROR_MULTIPLE_MATERIAL_OUTPUT_NODES))
                        output_node = n
                        linked_node = self.get_linked_input_node(output_node)
                        if not linked_node:
                            self.add_error(mat, errors, VoxelError.ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE)
                        elif linked_node.type != "BSDF_PRINCIPLED":
                            self.add_error(mat, errors, VoxelError.ERROR_ONLY_BSDF_SUPPORTED_IN_MATERIAL_OUTPUT_NODE)
                    elif t == 'TEX_IMAGE':
                        print("Unsupported node: ", t)
                    elif t == 'VERTEX_COLOR' or t == 'ATTRIBUTE':
                        pass
                    elif t == 'UVMAP':
                        pass

                if not output_node:
                    self.add_error(mat, errors, VoxelError.ERROR_MISSING_MATERIAL_OUTPUT_NODE)
                if not bsdf_node:
                    self.add_error(mat, errors, VoxelError.ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE)


            if (num_mat <= 0):
                self.add_error(obj, errors, VoxelError.ERROR_NOTHING_LINKED_IN_MATERIAL_OUTPUT_NODE)

        return errors

    def add_error(self, obj, errors, err):
        if not any(o == obj and e == err for o, e in errors):
            errors.append((obj, err))
            return True
        return False

    def get_linked_input_node(self, node):
        links = node.inputs[0].links
        return links[0].from_node if len(links) > 0 else None

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