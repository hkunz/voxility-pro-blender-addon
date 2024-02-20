import bpy
import bpy_types

from typing import Callable

class ExporterRegistration:
    ATTR_NAME = "_menu_lambda"

    @staticmethod
    def on_file_export_click(self, _context:bpy_types.Context, cls) -> None:
        self.layout.operator_context = 'INVOKE_DEFAULT'
        self.layout.operator(cls.bl_idname, text=cls.bl_label)

    @staticmethod
    def register_operator(cls, menu_func) -> None:
        bpy.utils.register_class(cls)
        lambda_func: Callable = lambda self, context: ExporterRegistration.on_file_export_click(self, context, cls)
        menu_func.append(lambda_func)
        setattr(cls, ExporterRegistration.ATTR_NAME, lambda_func)

    @staticmethod
    def unregister_operator(cls, menu_func) -> None:
        bpy.utils.unregister_class(cls)
        lambda_func: Callable = getattr(cls, ExporterRegistration.ATTR_NAME, None)
        menu_func.remove(lambda_func)
        delattr(cls, ExporterRegistration.ATTR_NAME)
