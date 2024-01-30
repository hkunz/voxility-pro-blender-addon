import bpy

class LegacyContextOverride:
    def __init__(self, window, screen, area, region):
        self.override_context = bpy.context.copy()
        self.override_context['window'] = window
        self.override_context['screen'] = screen
        self.override_context['area'] = area
        self.override_context['region'] = region

    def __enter__(self):
        return self.override_context

    def __exit__(self, exc_type, exc_value, traceback):
        pass