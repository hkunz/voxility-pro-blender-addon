import bpy

from abc import ABC, abstractmethod
from voxility_pro.context.legacy_context_override import LegacyContextOverride

class ContextScriptExecuter(ABC):

    def __init__(self, area_type, ui_type=None, script=None):
        self.area = None
        self.area_type = area_type
        self.ui_type = ui_type if ui_type else area_type
        self.script = script
        self.success = False
        self.error_message = None

    #@abstractmethod
    def script_content(self, context, legacy):
        self.script(context, legacy)

    def report_execute_error(self, message):
        self.error_message = f"Error processing script {self.__class__.__name__}. {message}"
        print(self.error_message)

    def execute_script(self):
        window = bpy.context.window
        screen = window.screen
        areas = [area for area in screen.areas if area.type == self.area_type]
        self.area = areas[0] if len(areas) else screen.areas[0]
        prev_ui_type = self.area.ui_type
        self.area.ui_type = self.ui_type
        regions = [region for region in self.area.regions if region.type == 'WINDOW']
        region = regions[0] if len(regions) else None
        temp_override = bpy.context.temp_override if hasattr(bpy.context, "temp_override") else LegacyContextOverride
        legacy = not hasattr(bpy.context, "temp_override")
        override = LegacyContextOverride if legacy else bpy.context.temp_override
        try:
            with temp_override(window=window, screen=screen, area=self.area, region=region) as override:
                self.success = self.script_content(override or bpy.context, legacy)
        except Exception as e:
            self.report_execute_error(str(e))
        finally:
            self.area.ui_type = prev_ui_type
        return self.success

#Sample Usage:
'''
ContextScriptExecuter(
    area_type='VIEW_3D',
    script=lambda override, legacy: (
        bpy.ops.view3d.view_axis(override, type='TOP')
        if legacy
        else bpy.ops.view3d.view_axis(type='TOP')
    )
).execute_script()
'''

#Sample usage assuming you have selected an object with material
'''
def my_context_script(context, legacy):
    legacy = not hasattr(context, "area")
    area = context['area'] if legacy else context.area
    area.spaces.active.node_tree = bpy.context.active_object.active_material.node_tree
    if legacy:
        bpy.ops.node.add_node(context, use_transform=True, type='ShaderNodeVertexColor')
        node_tree = bpy.context.active_object.active_material.node_tree
        active_node = node_tree.nodes[-1]
    else:
        bpy.ops.node.add_node(use_transform=True, type='ShaderNodeVertexColor')
        active_node = bpy.context.active_node
    active_node.location = (0, 0)

ContextScriptExecuter(
    area_type='NODE_EDITOR',
    ui_type='ShaderNodeTree',
    script=my_context_script
).execute_script()
'''