import bpy
import os
import tempfile
import shutil

from voxility_pro.utils.utils import get_blender_version, get_addon_version
from voxility_pro.utils.string_utils import randomize_string


class TempFileManager:

    TEMP_PARENT_DIRECTORY = None

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        print("Initialized", self)

    def create_temp_parent_dir(self) -> None:
        appdata_local_temp_dir: str = tempfile.gettempdir() # C:/Users/<user>/AppData/Local/Temp/
        TempFileManager.TEMP_PARENT_DIRECTORY: str = os.path.join(appdata_local_temp_dir, f"b{get_blender_version()}-vx{get_addon_version()}-tmp{randomize_string(5)}") # bv4.0.1-vxv1.0.8-tmpEGjov
        os.makedirs(name=TempFileManager.TEMP_PARENT_DIRECTORY, exist_ok=True)
        print(f"Created temporary parent directory: {TempFileManager.TEMP_PARENT_DIRECTORY}")
    
    def create_temp_dir(self) -> str:
        if not TempFileManager.TEMP_PARENT_DIRECTORY:
            self.create_temp_parent_dir()
        dir: str = tempfile.mkdtemp(prefix="", dir=TempFileManager.TEMP_PARENT_DIRECTORY) # creates a temp directory in os.environ['TEMP']/TEMP_PARENT_DIRECTORY/
        print("Created temp directory:", dir)
        return dir

    def delete_temp_dir(self, directory: str, ignore_errors: bool=True) -> None:
        print("Removing temp directory...", directory)
        shutil.rmtree(directory, ignore_errors)

    def remove_temp_parent_dir(self) -> None:
        if not TempFileManager.TEMP_PARENT_DIRECTORY:
            print("No temporary parent directory to cleanup")
            return
        self.delete_temp_dir(TempFileManager.TEMP_PARENT_DIRECTORY)
        print(f"Removed temporary parent directory: {TempFileManager.TEMP_PARENT_DIRECTORY}")
    
    def cleanup(self) -> None:
        self.remove_temp_parent_dir()