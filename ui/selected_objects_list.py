import bpy

from voxility_pro.utils.icons_manager import IconsManager  # type: ignore
from voxility_pro.utils.voxel.voxel_utils import get_voxelizer_modifier # type: ignore

class ListItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        description="",
        default=""
    ) # type: ignore

    voxelized: bpy.props.StringProperty(
        name="Voxelized",
        description="",
        default=""
    ) # type: ignore

class MY_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            #layout.label(text=item.name, icon_value=IconsManager().get_icon_id(IconsManager.ICON_VOXELIZED if item.voxelized else IconsManager.ICON_MESH_OBJECT))
            layout.label(text=item.name, icon=IconsManager.BUILTIN_ICON_VOXELIZED if item.voxelized else IconsManager.BUILTIN_ICON_MESH_DATA)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "MESH_DATA")

class LIST_OT_NewItem(bpy.types.Operator):
    bl_idname = "voxelize_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        context.scene.voxelize_list.add()
        return{'FINISHED'}

class LIST_OT_PopulateList(bpy.types.Operator):
    bl_idname = "voxelize_list.populate_list"
    bl_label = "Populate List"

    def execute(self, context):
        context.scene.voxelize_list.clear()
        for i, obj in enumerate(bpy.context.selected_objects):
            item = context.scene.voxelize_list.add()
            item.name = obj.name
            item.voxelized = "1" if get_voxelizer_modifier(obj) else ""
            if obj == bpy.context.active_object:
                bpy.context.scene.voxelize_list_index = i
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class SelectedObjectsList:
    ACTIVE_OBJECT=None
    SELECTED_OBJECTS = None


def on_depsgraph_update(scene) -> None:
    if bpy.types.Scene.voxelize_list_update or SelectedObjectsList.SELECTED_OBJECTS != bpy.context.selected_objects or SelectedObjectsList.ACTIVE_OBJECT != bpy.context.active_object:
        SelectedObjectsList.SELECTED_OBJECTS = bpy.context.selected_objects
        SelectedObjectsList.ACTIVE_OBJECT = bpy.context.active_object
        bpy.types.Scene.voxelize_list_update = False
        bpy.ops.voxelize_list.populate_list()

def register() -> None:
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(LIST_OT_PopulateList)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.types.Scene.voxelize_list_update = False
    bpy.types.Scene.voxelize_list = bpy.props.CollectionProperty(type = ListItem)
    bpy.types.Scene.voxelize_list_index = bpy.props.IntProperty(name = "Index for voxelize_list", default = 0)
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

def unregister() -> None:
    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(LIST_OT_PopulateList)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(LIST_OT_NewItem)
    del bpy.types.Scene.voxelize_list_update
    del bpy.types.Scene.voxelize_list
    del bpy.types.Scene.voxelize_list_index
    bpy.app.handlers.depsgraph_update_post.clear()


# example usage:
def selected_objects_list_example():

    from voxility_pro.ui.selected_objects_list import register as register_selected_objects_list # type: ignore
    register_selected_objects_list()
    # inside bpy.types.Panel::draw:
    row = layout.row() # type: ignore
    row.template_list("MY_UL_List", "The_List", bpy.context.scene, "voxelize_list", bpy.context.scene, "voxelize_list_index")
    row.enabled = False
'''
template_list(listtype_name, list_id, dataptr, propname, active_dataptr, active_propname, item_dyntip_propname='', rows=5, maxrows=5, type='DEFAULT', columns=9, sort_reverse=False, sort_lock=False)
Item. A list widget to display data, e.g. vertexgroups.

Parameters:
listtype_name (string, (never None)) - Identifier of the list type to use
list_id (string, (never None)) - Identifier of this list widget (mandatory when using default “UI_UL_list” class). If this not an empty string, the uilist gets a custom ID, otherwise it takes the name of the class used to define the uilist (for example, if the class name is “OBJECT_UL_vgroups”, and list_id is not set by the script, then bl_idname = “OBJECT_UL_vgroups”)
dataptr (AnyType) - Data from which to take the Collection property
propname (string, (never None)) - Identifier of the Collection property in data
active_dataptr (AnyType, (never None)) - Data from which to take the integer property, index of the active item
active_propname (string, (never None)) - Identifier of the integer property in active_data, index of the active item
item_dyntip_propname (string, (optional, never None)) - Identifier of a string property in items, to use as tooltip content
rows (int in [0, inf], (optional)) - Default and minimum number of rows to display
maxrows (int in [0, inf], (optional)) - Default maximum number of rows to display
type (enum in Uilist Layout Type Items, (optional)) - Type, Type of layout to use: DEFAULT,GRID,COMPACT https://docs.blender.org/api/current/bpy_types_enum_items/uilist_layout_type_items.html#rna-enum-uilist-layout-type-items
columns (int in [0, inf], (optional)) - Number of items to display per row, for GRID layout
sort_reverse (boolean, (optional)) - Display items in reverse order by default
sort_lock (boolean, (optional)) - Lock display order to default value
'''