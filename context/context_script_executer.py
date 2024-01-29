import bpy

from abc import ABC, abstractmethod

class ContextScriptExecuter(ABC):

    def __init__(self, area_type, ui_type=None):
        self.area_type = area_type
        self.ui_type = ui_type
        self.error_message = None
        self.success = False

    @staticmethod
    def use_temp_override():
        version = bpy.app.version
        major = version[0]
        minor = version[1]
        return not (major < 3 or (major == 3 and minor < 2))

    @abstractmethod
    def execute_script_content(_oneself, _override_context=None):
        pass

    def report_execute_error(self, message):
        self.error_message = f"Error processing script executor in {self.__class__.__name__}. {message}"
        print(self.error_message)

    def prepare_context_area(self, _area):
        pass

    def execute_script(self):
        window = bpy.context.window
        screen = window.screen
        area = screen.areas[0]
        self.prev_ui_type = area.ui_type # most likely VIEW_3D
        area.ui_type = self.ui_type if self.ui_type else self.area_type
        region = area.regions[0]
        self.prepare_context_area(area)

        if ContextScriptExecuter.use_temp_override():
            try:
                with bpy.context.temp_override(window=window, area=area, region=region, screen=screen):
                    self.success = self.execute_script_content()
            except Exception as e:
                self.report_execute_error(str(e))
            finally:
                area.ui_type = self.prev_ui_type

        else:
            override_context = bpy.context.copy()
            override_context['window'] = window
            override_context['screen'] = screen
            override_context['area'] = area
            override_context['region'] = region
            try:
                self.success = self.execute_script_content(override_context)
            except Exception as e:
                self.report_execute_error(str(e))
            finally:
                area.ui_type = self.prev_ui_type

        return self.success