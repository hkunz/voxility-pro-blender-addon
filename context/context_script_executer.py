import bpy

from abc import ABC, abstractmethod

class ContextScriptExecuter(ABC):

    def __init__(self, area_type, ui_type=None):
        self.area_type = area_type
        self.ui_type = ui_type if ui_type else area_type
        self.prev_ui_type = None
        self.success = False
        self.error_message = None

    @abstractmethod
    def script_content(_self, _override_context=None):
        pass

    @staticmethod
    def use_temp_override():
        version = bpy.app.version
        major = version[0]
        minor = version[1]
        return not (major < 3 or (major == 3 and minor < 2))

    def report_execute_error(self, message):
        self.error_message = f"Error processing script {self.__class__.__name__}. {message}"
        print(self.error_message)

    def prepare_context_area(self, area):
        self.prev_ui_type = area.ui_type
        area.ui_type = self.ui_type

    def get_legacy_context_override(window, screen, area, region):
        override_context = bpy.context.copy()
        override_context['window'] = window
        override_context['screen'] = screen
        override_context['area'] = area
        override_context['region'] = region
        return override_context

    def execute_script(self):
        window = bpy.context.window
        screen = window.screen
        area = screen.areas[0]
        region = None #area.regions[0]
        self.prepare_context_area(area)

        try:
            if ContextScriptExecuter.use_temp_override():
                with bpy.context.temp_override(window=window, screen=screen, area=area, regions=region):
                    self.success = self.script_content()
            else:
                override_context = self.get_legacy_context_override(window, screen, area, regions=region)
                self.success = self.script_content(override_context)

        except Exception as e:
            self.report_execute_error(str(e))
        finally:
            area.ui_type = self.prev_ui_type

        return self.success

    @staticmethod
    def set_active_node_tree(area, object, material_index = 0):
        C = bpy.context
        C.view_layer.objects.active = object
        C.object.active_material_index = material_index
        mat = C.active_object.active_material
        area.spaces.active.node_tree = mat.node_tree # https://blender.stackexchange.com/a/268511/14229