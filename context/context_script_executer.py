import bpy

from voxility_pro.utils.utils import abstract_method

class ContextScriptExecuter:

    def __init__(self, area_type, ui_type=None):
        self.area_type = area_type
        self.ui_type = ui_type # example for Shader Node Editor: bpy.context.area.ui_type = 'ShaderNodeTree'
        self.prev_ui_type = bpy.context.area.ui_type # most likely VIEW_3D

    @staticmethod
    def use_temp_override():
        version = bpy.app.version
        major = version[0]
        minor = version[1]
        return not (major < 3 or (major == 3 and minor < 2))

    @staticmethod
    def get_areas(type, ui_type):
        screen = bpy.context.window.screen
        return [area for area in screen.areas if area.type == type and (ui_type == None or area.ui_type == ui_type)]

    @staticmethod
    def get_regions(areas):
        return [region for region in areas[0].regions if region.type == 'WINDOW']

    @abstract_method
    def execute_script_content(_oneself, _override_context=None):
        pass # example: bpy.ops.view3d.background_image_add(override_context)

    def switch_context_area(self):
        if self.ui_type:
            bpy.context.area.ui_type = self.ui_type
        else:
            bpy.context.area.ui_type = self.area_type

    @staticmethod
    def return_to_prev_area(prev_ui_type):
        bpy.context.area.ui_type = prev_ui_type

    def report_execute_error(self, message):
        self.report({'ERROR'}, f"Error processing script executor in {self.__class__.__name__}. {message}")

    def prepare_context_area(self, _area):
        pass

    def execute_script(self):
        window = bpy.context.window
        screen = window.screen
        self.switch_context_area()
        areas  = ContextScriptExecuter.get_areas(self.area_type, self.ui_type)
        area = areas[0]
        region = ContextScriptExecuter.get_regions(areas)[0]
        self.prepare_context_area(area)

        if ContextScriptExecuter.use_temp_override():
            try:
                with bpy.context.temp_override(window=window, area=areas[0], region=region, screen=screen):
                    self.execute_script_content()
            except Exception as e:
                self.report_execute_error(str(e))
            finally:
                ContextScriptExecuter.return_to_prev_area(self.prev_ui_type)

        else: # execute using legacy override
            override_context = bpy.context.copy()
            override_context['window'] = window
            override_context['screen'] = screen
            override_context['area'] = area
            override_context['region'] = region
            try:
                self.execute_script_content(override_context)
            except Exception as e:
                self.report_execute_error(str(e))
            finally:
                ContextScriptExecuter.return_to_prev_area(self.prev_ui_type)

        return True