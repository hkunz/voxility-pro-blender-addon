import bpy

class ContextExecuterOverride:
    def __init__(self, executer, window, screen, area, region):
        self.executer = executer
        self.window, self.screen, self.area, self.region = window, screen, area, region
        self.legacy = not hasattr(bpy.context, "temp_override")
        if self.legacy:
            self.context = bpy.context.copy()
            self.context['window'] = window
            self.context['screen'] = screen
            self.context['area'] = area
            self.context['region'] = region
        else:
            self.context = bpy.context.temp_override(window=window, screen=screen, area=area, region=region)

    def __enter__(self):
        if not self.legacy:
            self.context.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.legacy:
            self.context.__exit__(self, exc_type, exc_value, traceback)
        return self
